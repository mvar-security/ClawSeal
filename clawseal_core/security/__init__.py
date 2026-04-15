"""ClawSeal security module - QSEAL cryptographic signing and verification"""

from .qseal_engine import sign_entry, sign_scroll, verify_signature
from .qseal_utils import get_qseal_secret, compute_meta_hash

__all__ = [
    "sign_entry",
    "sign_scroll",
    "verify_signature",
    "get_qseal_secret",
    "compute_meta_hash",
]
