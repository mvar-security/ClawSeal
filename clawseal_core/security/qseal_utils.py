"""QSEAL utility helpers for canonicalization and metadata."""

import os

import json
import hashlib
from datetime import datetime, timezone


def compute_meta_hash(data: dict) -> str:
    """
    Compute a deterministic hash over a dictionary.
    Uses sorted keys and UTF-8 encoding for consistency.
    Includes QSEAL_SECRET in the hash input for extra entropy.
    """
    canonical_json = json.dumps(data, sort_keys=True, ensure_ascii=False)
    combined = canonical_json + get_qseal_secret(require=True)
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:16]


def inject_derived_fields(entry: dict, agent_id: str = None) -> dict:
    """
    Enrich an entry with standard QSEAL metadata fields:
    - timestamp (UTC ISO8601)
    - meta_hash (short SHA256)
    - agent_id (if provided)
    """
    enriched = entry.copy()
    enriched["timestamp"] = datetime.now(timezone.utc).isoformat()
    enriched["meta_hash"] = compute_meta_hash(entry)
    if agent_id:
        enriched["agent_id"] = agent_id
    return enriched


def prepare_for_signature(entry: dict) -> str:
    """
    Prepare canonical string for signing.
    Sorts keys, removes non-essential fields like qseal_signature.
    """
    filtered = {k: v for k, v in entry.items() if k != "qseal_signature"}
    canonical_json = json.dumps(filtered, sort_keys=True, ensure_ascii=False)
    return canonical_json


def verify_meta_hash(entry: dict) -> bool:
    """
    Verify that the meta_hash matches recomputed value.
    Returns True if valid, False if mismatch.
    """
    if "meta_hash" not in entry:
        return False
    expected = compute_meta_hash({k: v for k, v in entry.items() if k != "meta_hash"})
    return entry["meta_hash"] == expected


def timestamp_iso() -> str:
    """Utility for standardized UTC timestamps."""
    return datetime.now(timezone.utc).isoformat()


def qseal_info() -> dict:
    """Return QSEAL utility metadata."""
    return {
        "module": "qseal_utils",
        "version": "1.0.0",
        "functions": [
            "compute_meta_hash",
            "inject_derived_fields",
            "prepare_for_signature",
            "verify_meta_hash",
            "timestamp_iso",
            "is_qseal_enabled",
            "get_qseal_secret",
        ]
    }


def is_qseal_enabled() -> bool:
    """Return True when QSEAL signing is configured in env."""
    return bool(os.getenv("QSEAL_SECRET"))


def get_qseal_secret(require: bool = True) -> str | None:
    """
    Read QSEAL secret from environment.

    When ``require`` is True, missing secret raises a fail-closed error.
    When ``require`` is False, returns None if not configured.
    """
    secret = os.getenv("QSEAL_SECRET")
    if secret:
        return secret
    if not require:
        return None
    raise RuntimeError(
        "QSEAL_SECRET not set. "
        "Run: export QSEAL_SECRET=$(openssl rand -hex 32) "
        "then run: clawseal verify. "
        "Docs: https://github.com/mvar-security/ClawSeal#readme"
    )
