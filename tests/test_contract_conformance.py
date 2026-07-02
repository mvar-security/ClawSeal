"""ClawSeal conforms to the frozen core contract (MemoryStore).

stdlib unittest (no pytest dependency). Skips cleanly if mirra-core-contract is absent.
"""

import os
import tempfile
import unittest

os.environ.setdefault("QSEAL_SECRET", "unittest_clawseal_contract_secret")

try:
    import mirra_core_contract as c
    from clawseal_core.contract_adapter import ClawSealMemoryStore
    _HAVE = True
except Exception:
    _HAVE = False


@unittest.skipUnless(_HAVE, "mirra-core-contract not installed")
class TestClawSealContractConformance(unittest.TestCase):
    def _store(self):
        return ClawSealMemoryStore(base_path=tempfile.mkdtemp(), agent_id="agentX")

    def test_satisfies_memory_store(self):
        self.assertIsInstance(self._store(), c.MemoryStore)

    def test_remember_returns_signed_scroll(self):
        store = self._store()
        s = store.remember("agentX", "jack", "Jack prefers concise answers")
        self.assertTrue(s.qseal_signature)
        self.assertEqual(s.subject_id, "jack")

    def test_verify_genuine_true_tampered_false(self):
        store = self._store()
        s = store.remember("agentX", "jack", "the original memory")
        self.assertTrue(store.verify(s).verified)
        s.content = "TAMPERED"
        self.assertFalse(store.verify(s).verified)


if __name__ == "__main__":
    unittest.main()
