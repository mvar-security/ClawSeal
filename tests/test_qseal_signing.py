"""Cryptographic signing / tamper / chain / fail-closed tests for ClawSeal QSEAL.

Closes Phase 2 finding G-19: the flagship tamper-evidence guarantee had ZERO tests in
its own repo (only CLI entry-point tests existed). Written with stdlib unittest so it runs
even when pytest is not installed in the venv (also runnable under pytest).

Run: python3 -m unittest tests.test_qseal_signing   (from repo root, with QSEAL_SECRET set)
"""

import importlib
import os
import unittest

# Deterministic throwaway secret for the whole module (never reads the real one).
os.environ["QSEAL_SECRET"] = "unittest_clawseal_secret_do_not_use_in_prod"

from clawseal_core.security import qseal_engine as qe  # noqa: E402
from clawseal_core.security import qseal_utils as qu  # noqa: E402


class TestSigning(unittest.TestCase):
    def test_sign_then_verify_roundtrips(self):
        entry = {"content": "hello world", "subject": "jack"}
        signed = qe.sign_entry(dict(entry))
        self.assertIn("qseal_signature", signed)
        self.assertTrue(qe.verify_signature(signed))

    def test_single_char_tamper_is_detected(self):
        signed = qe.sign_entry({"content": "the original content", "subject": "jill"})
        self.assertTrue(qe.verify_signature(signed))
        # flip one character in a signed field
        tampered = dict(signed)
        tampered["content"] = "The original content"  # capital T
        self.assertFalse(qe.verify_signature(tampered))

    def test_algorithm_is_hmac_sha256(self):
        # The canonical primitive is symmetric HMAC-SHA256 (not Ed25519).
        signed = qe.sign_entry({"content": "x"})
        self.assertIsInstance(signed["qseal_signature"], str)
        # base64 of a 32-byte HMAC digest → 44 chars with '=' padding
        self.assertGreaterEqual(len(signed["qseal_signature"]), 40)


class TestChain(unittest.TestCase):
    def test_chain_links_and_verifies(self):
        a = qe.sign_entry({"content": "first"})
        b = qe.link_signatures(a, qe.sign_entry({"content": "second"}))
        c = qe.link_signatures(b, qe.sign_entry({"content": "third"}))
        self.assertTrue(qe.verify_chain([a, b, c]))

    def test_chain_break_is_detected(self):
        a = qe.sign_entry({"content": "first"})
        b = qe.link_signatures(a, qe.sign_entry({"content": "second"}))
        c = qe.link_signatures(b, qe.sign_entry({"content": "third"}))
        # tamper the middle link's signature → chain must fail
        b_broken = dict(b)
        b_broken["qseal_signature"] = "AAAA_invalid_AAAA"
        self.assertFalse(qe.verify_chain([a, b_broken, c]))


class TestFailClosed(unittest.TestCase):
    def test_production_secret_is_production_mode(self):
        ctx = qu.get_qseal_context()
        self.assertFalse(ctx["is_demo"])
        self.assertTrue(ctx["qseal_production"])

    def test_require_production_raises_without_secret(self):
        # With CLAWSEAL_REQUIRE_PRODUCTION=1 and no QSEAL_SECRET, must fail closed.
        saved_secret = os.environ.pop("QSEAL_SECRET", None)
        os.environ["CLAWSEAL_REQUIRE_PRODUCTION"] = "1"
        try:
            with self.assertRaises(RuntimeError):
                qu.get_qseal_context()
        finally:
            os.environ.pop("CLAWSEAL_REQUIRE_PRODUCTION", None)
            if saved_secret is not None:
                os.environ["QSEAL_SECRET"] = saved_secret


if __name__ == "__main__":
    unittest.main()
