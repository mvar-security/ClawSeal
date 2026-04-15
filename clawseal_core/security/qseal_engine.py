"""
mirra_core/security/qseal_engine.py
QSEAL Engine – Core Signing and Verification Logic
Handles creation and verification of tamper-evident signature chains for MIRRA systems.
"""

import json
import hashlib
import os
import base64
import hmac
from datetime import datetime, timezone
from .qseal_utils import compute_meta_hash, inject_derived_fields, prepare_for_signature, verify_meta_hash

# Default signing secret (production mode requires this to be set)
# For MCP servers, we allow this to be None and raise error only when actually used
QSEAL_SECRET = os.getenv("QSEAL_SECRET")
QSEAL_ENABLED = QSEAL_SECRET is not None


def generate_signature(payload: dict) -> str:
    """
    Generate an HMAC-SHA256 signature for the given payload.
    Uses canonical JSON string with sorted keys.
    """
    if not QSEAL_ENABLED:
        raise RuntimeError(
            "QSEAL_SECRET environment variable must be set. "
            "Generate one with: openssl rand -hex 32"
        )
    canonical = prepare_for_signature(payload)
    signature = hmac.new(
        QSEAL_SECRET.encode("utf-8"),
        canonical.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode("utf-8")


def sign_entry(entry: dict, agent_id: str = None) -> dict:
    """
    Sign a ledger entry with QSEAL.
    Injects derived fields and computes signature over canonical form.
    Returns a signed entry dictionary with qseal_signature.
    """
    enriched = inject_derived_fields(entry, agent_id=agent_id)
    signature = generate_signature(enriched)
    enriched["qseal_signature"] = signature
    enriched["qseal_verified"] = True
    enriched["qseal_meta_hash"] = enriched.get("meta_hash")
    return enriched


def verify_signature(entry: dict) -> bool:
    """
    Verify the HMAC signature of an entry.
    Returns True if valid, False otherwise.

    CRITICAL: Only excludes QSEAL metadata fields added AFTER signing.
    All other fields (including retrieved_count initialized to 0) are part of the signed payload.
    """
    if "qseal_signature" not in entry:
        return False

    provided_sig = entry["qseal_signature"]

    # Filter out ONLY the QSEAL metadata fields added after signing:
    # - qseal_signature (the signature itself)
    # - qseal_verified (verification flag)
    # - qseal_meta_hash (duplicate of meta_hash)
    # - qseal_prev_signature (chain link added by link_signatures() after initial signing)
    #
    # NOTE: retrieved_count, drift fields, etc. are part of the signed payload
    # (initialized before signing, updated after). Changing them breaks the signature.
    # This is INTENTIONAL - it creates a tamper-evident seal on the original state.
    excluded_fields = {"qseal_signature", "qseal_verified", "qseal_meta_hash", "qseal_prev_signature"}
    filtered = {k: v for k, v in entry.items() if k not in excluded_fields}

    expected_sig = generate_signature(filtered)

    return hmac.compare_digest(provided_sig, expected_sig)


def link_signatures(previous_entry: dict, current_entry: dict) -> dict:
    """
    Create a chain link between two entries by embedding previous signature hash.
    """
    prev_sig = previous_entry.get("qseal_signature", "")
    current_entry["qseal_prev_signature"] = hashlib.sha256(prev_sig.encode()).hexdigest()[:16]
    return current_entry


def verify_chain(entries: list) -> bool:
    """
    Verify the integrity of a QSEAL signature chain.
    Ensures genesis entry has no previous link and each subsequent entry
    correctly references the hash of the previous signature.
    """
    if not entries:
        return True
    
    # Genesis entry should not have a previous link
    if entries[0].get("qseal_prev_signature"):
        print("⚠️ Genesis entry should not have a previous link")
        return False
    
    for i in range(1, len(entries)):
        prev = entries[i - 1]
        curr = entries[i]
        
        # Each entry after genesis must have a chain link
        if "qseal_prev_signature" not in curr:
            print(f"⚠️ Entry {i} missing chain link")
            return False
        
        expected_prev_hash = hashlib.sha256(prev["qseal_signature"].encode()).hexdigest()[:16]
        if curr.get("qseal_prev_signature") != expected_prev_hash:
            print(f"⚠️ Chain broken between entries {i-1} and {i}")
            return False
    
    return True


def qseal_status_report(entry: dict) -> dict:
    """
    Generate a verification status report for a signed entry.
    """
    verified_hash = verify_meta_hash(entry)
    verified_sig = verify_signature(entry)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verified_meta_hash": verified_hash,
        "verified_signature": verified_sig,
        "chain_linked": "qseal_prev_signature" in entry,
        "summary": "VALID" if verified_hash and verified_sig else "INVALID"
    }


def qseal_info() -> dict:
    """Return QSEAL engine metadata."""
    return {
        "module": "qseal_engine",
        "version": "1.0.0",
        "description": "Core cryptographic signing and verification for MIRRA QSEAL",
        "functions": [
            "generate_signature",
            "sign_entry",
            "verify_signature",
            "link_signatures",
            "verify_chain",
            "qseal_status_report"
        ]
    }


def repair_chain(entries: list) -> list:
    """
    Repair broken chain links by recomputing previous signature hashes.
    WARNING: This invalidates cryptographic trust. Use only for recovering
    from honest structural errors, not tampering.
    """
    if not entries:
        return entries
    
    # Remove prev link from genesis
    if "qseal_prev_signature" in entries[0]:
        del entries[0]["qseal_prev_signature"]
    
    for i in range(1, len(entries)):
        prev_sig = entries[i - 1].get("qseal_signature", "")
        entries[i]["qseal_prev_signature"] = hashlib.sha256(prev_sig.encode()).hexdigest()[:16]
    
    return entries


# ==============================================================================
# DEPRECATED: Legacy QSEALEngine Class (Entry 86 compatibility)
# ==============================================================================
# ⚠️  DEPRECATION WARNING ⚠️
#
# This class uses INSECURE signing: sha256(payload + secret)
# This is vulnerable to length extension attacks and lacks proper key derivation.
#
# DO NOT USE for new code.
#
# For secure QSEAL signatures, use the HMAC-based functions instead:
#   - sign_entry(entry, agent_id)  → Returns signed entry with HMAC-SHA256
#   - verify_signature(entry)      → Verifies HMAC signature
#   - generate_signature(payload)  → Raw HMAC-SHA256 signature
#
# This class is retained ONLY for backward compatibility with Entry 86.
# It will be removed in a future version.
# ==============================================================================

class QSEALEngine:
    """
    DEPRECATED: Minimal QSEAL for Entry 86 compatibility.

    ⚠️  Uses insecure sha256(payload + secret) signing.
    ⚠️  DO NOT USE for new code.
    ⚠️  Use sign_entry() / verify_signature() instead (HMAC-SHA256).
    """
    def __init__(self):
        import os
        import warnings
        warnings.warn(
            "QSEALEngine is DEPRECATED and uses insecure sha256(payload + secret) signing. "
            "Use sign_entry() and verify_signature() instead for HMAC-SHA256 signatures.",
            DeprecationWarning,
            stacklevel=2
        )
        self.secret = os.getenv("QSEAL_SECRET")
        if not self.secret:
            print("⚠️  QSEAL_SECRET not found in environment")
            self.available = False
        else:
            self.available = True
            print(f"✅ QSEAL initialized with secret: {self.secret[:8]}...")

    def sign_transition(self, data):
        """
        DEPRECATED: Sign a transition with INSECURE sha256(payload + secret).
        Use sign_entry() instead for HMAC-SHA256.
        """
        if not self.available:
            return None
        import hashlib
        import json
        payload = json.dumps(data, sort_keys=True)
        return hashlib.sha256((payload + self.secret).encode()).hexdigest()
    
    def sign_entry(self, data):
        """Alias for sign_transition"""
        return self.sign_transition(data)


def sign_scroll(entry: dict, agent_id: str = None) -> dict:
    """Backward-compatible alias for sign_entry."""
    return sign_entry(entry, agent_id=agent_id)
