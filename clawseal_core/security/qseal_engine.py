"""QSEAL Engine – signing and verification logic for ClawSeal."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import warnings
from datetime import datetime, timezone

from .qseal_utils import (
    get_qseal_context,
    get_qseal_secret,
    inject_derived_fields,
    is_qseal_enabled,
    prepare_for_signature,
    verify_meta_hash,
)

logger = logging.getLogger(__name__)



def qseal_enabled() -> bool:
    """Backward-compatible helper for runtime QSEAL availability checks."""
    return is_qseal_enabled()



def generate_signature(payload: dict) -> str:
    """Generate HMAC-SHA256 signature over canonical payload."""
    secret = get_qseal_context(require=True)["secret"]
    canonical = prepare_for_signature(payload)
    signature = hmac.new(
        secret.encode("utf-8"),
        canonical.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return base64.b64encode(signature).decode("utf-8")



def sign_entry(entry: dict, agent_id: str | None = None) -> dict:
    """Sign an entry and inject QSEAL metadata."""
    enriched = inject_derived_fields(entry, agent_id=agent_id)
    signature = generate_signature(enriched)
    enriched["qseal_signature"] = signature
    enriched["qseal_verified"] = True
    enriched["qseal_meta_hash"] = enriched.get("meta_hash")
    return enriched



def verify_signature(entry: dict) -> bool:
    """Verify HMAC signature of an entry."""
    if "qseal_signature" not in entry:
        return False

    provided_sig = entry["qseal_signature"]
    excluded_fields = {
        "qseal_signature",
        "qseal_verified",
        "qseal_meta_hash",
        "qseal_prev_signature",
    }
    filtered = {k: v for k, v in entry.items() if k not in excluded_fields}
    expected_sig = generate_signature(filtered)
    return hmac.compare_digest(provided_sig, expected_sig)



def link_signatures(previous_entry: dict, current_entry: dict) -> dict:
    """Attach previous signature hash to current entry for chain integrity."""
    prev_sig = previous_entry.get("qseal_signature", "")
    current_entry["qseal_prev_signature"] = hashlib.sha256(prev_sig.encode()).hexdigest()[:16]
    return current_entry



def verify_chain(entries: list[dict]) -> bool:
    """Verify signature-chain continuity across entries."""
    if not entries:
        return True

    if entries[0].get("qseal_prev_signature"):
        logger.warning("Genesis entry should not have a previous link")
        return False

    for i in range(1, len(entries)):
        prev = entries[i - 1]
        curr = entries[i]
        if "qseal_prev_signature" not in curr:
            logger.warning("Entry %s missing chain link", i)
            return False

        expected_prev_hash = hashlib.sha256(prev["qseal_signature"].encode()).hexdigest()[:16]
        if curr.get("qseal_prev_signature") != expected_prev_hash:
            logger.warning("Chain broken between entries %s and %s", i - 1, i)
            return False

    return True



def qseal_status_report(entry: dict) -> dict:
    """Return verification status details for an entry."""
    verified_hash = verify_meta_hash(entry)
    verified_sig = verify_signature(entry)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verified_meta_hash": verified_hash,
        "verified_signature": verified_sig,
        "chain_linked": "qseal_prev_signature" in entry,
        "summary": "VALID" if verified_hash and verified_sig else "INVALID",
    }



def qseal_info() -> dict:
    """Return QSEAL engine metadata."""
    return {
        "module": "qseal_engine",
        "version": "1.1.1",
        "description": "Core cryptographic signing and verification for ClawSeal QSEAL",
        "functions": [
            "generate_signature",
            "sign_entry",
            "verify_signature",
            "link_signatures",
            "verify_chain",
            "qseal_status_report",
        ],
    }



def repair_chain(entries: list[dict]) -> list[dict]:
    """Repair broken chain links. Use only for structural recovery."""
    if not entries:
        return entries

    if "qseal_prev_signature" in entries[0]:
        del entries[0]["qseal_prev_signature"]

    for i in range(1, len(entries)):
        prev_sig = entries[i - 1].get("qseal_signature", "")
        entries[i]["qseal_prev_signature"] = hashlib.sha256(prev_sig.encode()).hexdigest()[:16]

    return entries


class QSEALEngine:
    """DEPRECATED legacy class using insecure sha256(payload + secret)."""

    def __init__(self):
        warnings.warn(
            "QSEALEngine is DEPRECATED and uses insecure sha256(payload + secret) signing. "
            "Use sign_entry() and verify_signature() instead for HMAC-SHA256.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.secret = get_qseal_secret(require=False)
        if not self.secret:
            warnings.warn(
                "QSEAL secret not found; deprecated QSEALEngine disabled.",
                UserWarning,
                stacklevel=2,
            )
            self.available = False
        else:
            self.available = True

    def sign_transition(self, data: dict):
        """DEPRECATED insecure signer retained only for compatibility."""
        if not self.available:
            return None
        payload = json.dumps(data, sort_keys=True)
        return hashlib.sha256((payload + self.secret).encode()).hexdigest()

    def sign_entry(self, data: dict):
        """Alias for sign_transition()."""
        return self.sign_transition(data)



def sign_scroll(entry: dict, agent_id: str | None = None) -> dict:
    """Backward-compatible alias for sign_entry."""
    return sign_entry(entry, agent_id=agent_id)
