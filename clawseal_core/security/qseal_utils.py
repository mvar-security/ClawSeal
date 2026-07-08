"""QSEAL utility helpers for canonicalization and metadata.

ClawSeal v1.1.1
- Call-time secret resolution (no import-time cache)
- Persistent demo secret at ~/.clawseal/demo_secret (chmod 600)
- Demo/production mode markers for signed artifacts
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEMO_SECRET_PATH = Path.home() / ".clawseal" / "demo_secret"



def _ensure_demo_secret() -> str:
    """Create/read demo secret from ~/.clawseal/demo_secret."""
    if DEMO_SECRET_PATH.exists():
        try:
            secret = DEMO_SECRET_PATH.read_text(encoding="utf-8").strip()
            if len(secret) >= 32:
                return secret
        except OSError:
            pass
        warnings.warn(
            f"Demo secret at {DEMO_SECRET_PATH} is unreadable/corrupted. Regenerating.",
            UserWarning,
            stacklevel=2,
        )

    demo_secret = secrets.token_hex(32)
    DEMO_SECRET_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEMO_SECRET_PATH.write_text(demo_secret, encoding="utf-8")
    DEMO_SECRET_PATH.chmod(0o600)
    warnings.warn(
        (
            "ClawSeal demo mode enabled. Generated local demo secret at "
            f"{DEMO_SECRET_PATH}. Run `clawseal init` for production setup."
        ),
        UserWarning,
        stacklevel=2,
    )
    return demo_secret



def get_qseal_context(require: bool = True) -> dict[str, Any]:
    """Return resolved signing context and mode metadata.

    Non-breaking helper: callers that need mode metadata can use this,
    while legacy callers can continue to use get_qseal_secret().
    """
    env_secret = os.getenv("QSEAL_SECRET")
    if env_secret:
        return {
            "secret": env_secret,
            "is_demo": False,
            "qseal_mode": "production",
            "qseal_production": True,
            "qseal_secret_source": "QSEAL_SECRET",
        }

    # FAIL-CLOSED opt-in (Phase 4B / finding G-19). By default ClawSeal falls back to an
    # ephemeral demo secret when QSEAL_SECRET is unset (convenient for local demos). In
    # production you can require a real secret: with CLAWSEAL_REQUIRE_PRODUCTION=1 set, a
    # missing QSEAL_SECRET raises instead of silently demo-signing — so signatures are
    # never mistaken for production trust. This makes the "fail-closed / no weak defaults"
    # posture real when opted in (previously claimed unconditionally, which was false).
    _require_prod = os.getenv("CLAWSEAL_REQUIRE_PRODUCTION", "").strip().lower() in {"1", "true", "yes"}
    if _require_prod:
        raise RuntimeError(
            "CLAWSEAL_REQUIRE_PRODUCTION is set but QSEAL_SECRET is not. Refusing to fall "
            "back to an ephemeral demo secret (fail-closed). Set QSEAL_SECRET to a 256-bit "
            "value (e.g. `openssl rand -hex 32`)."
        )

    if not require:
        return {
            "secret": None,
            "is_demo": True,
            "qseal_mode": "demo_ephemeral",
            "qseal_production": False,
            "qseal_secret_source": None,
        }

    demo_secret = _ensure_demo_secret()
    return {
        "secret": demo_secret,
        "is_demo": True,
        "qseal_mode": "demo_ephemeral",
        "qseal_production": False,
        "qseal_secret_source": str(DEMO_SECRET_PATH),
    }



def get_qseal_secret(require: bool = True) -> str | None:
    """Backward-compatible secret getter.

    Returns string secret (or None when require=False and unavailable).
    """
    return get_qseal_context(require=require)["secret"]



def is_qseal_enabled() -> bool:
    """QSEAL is enabled in production (env) or demo (local persisted) mode."""
    return True



def compute_meta_hash(data: dict, secret: str | None = None) -> str:
    """Compute deterministic hash over dictionary + secret entropy."""
    if secret is None:
        secret = get_qseal_secret(require=True)
    canonical_json = json.dumps(data, sort_keys=True, ensure_ascii=False)
    combined = canonical_json + secret
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:16]



def inject_derived_fields(entry: dict, agent_id: str | None = None) -> dict:
    """Enrich entries with timestamp/hash and QSEAL mode markers."""
    enriched = entry.copy()
    ctx = get_qseal_context(require=True)
    # `timestamp` is injected BEFORE signing and is therefore INSIDE the signed
    # payload by design — it is deliberately signed here. This differs from the
    # bridge/on-device engines (mirra_core/identity/fingerprint.py,
    # mirra_device/qseal_lite.py), which EXCLUDE the timestamp from their signed
    # fields. Do NOT "harmonize" the two: do not add `timestamp` to
    # prepare_for_signature()'s filter below as a consistency fix — that would
    # remove tamper-evidence from the timestamp in ClawSeal.
    enriched["timestamp"] = datetime.now(timezone.utc).isoformat()
    enriched["meta_hash"] = compute_meta_hash(entry, secret=ctx["secret"])
    if agent_id:
        enriched["agent_id"] = agent_id

    # Mode markers for auditable provenance
    enriched["qseal_mode"] = ctx["qseal_mode"]
    enriched["qseal_production"] = ctx["qseal_production"]
    return enriched



def prepare_for_signature(entry: dict) -> str:
    """Prepare canonical JSON string for signing.

    Only `qseal_signature` is excluded (a field can't sign itself). Every other
    field — including `timestamp` (injected by inject_derived_fields above) —
    is INSIDE the signed payload by design and stays tamper-evident. Do not add
    `timestamp` here to match the bridge/qseal_lite exclusion; ClawSeal
    deliberately signs it.
    """
    filtered = {k: v for k, v in entry.items() if k != "qseal_signature"}
    canonical_json = json.dumps(filtered, sort_keys=True, ensure_ascii=False)
    return canonical_json



def verify_meta_hash(entry: dict, secret: str | None = None) -> bool:
    """Verify stored meta_hash against recomputed value."""
    if "meta_hash" not in entry:
        return False
    expected = compute_meta_hash(
        {k: v for k, v in entry.items() if k != "meta_hash"},
        secret=secret,
    )
    return entry["meta_hash"] == expected



def timestamp_iso() -> str:
    """Utility for standardized UTC timestamps."""
    return datetime.now(timezone.utc).isoformat()



def qseal_info() -> dict[str, Any]:
    """Return QSEAL utility metadata and runtime mode."""
    ctx = get_qseal_context(require=False)
    return {
        "module": "qseal_utils",
        "version": "1.1.1",
        "mode": ctx["qseal_mode"],
        "production": ctx["qseal_production"],
        "functions": [
            "compute_meta_hash",
            "inject_derived_fields",
            "prepare_for_signature",
            "verify_meta_hash",
            "timestamp_iso",
            "is_qseal_enabled",
            "get_qseal_secret",
            "get_qseal_context",
            "qseal_info",
        ],
    }
