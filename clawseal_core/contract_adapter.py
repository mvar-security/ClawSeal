"""ClawSeal conformance adapter — exposes the scroll memory store via the core contract.

Migrate-don't-rewrite (Phase 4C): a thin shim over ScrollMemoryStore so any edge can use
ClawSeal purely through `mirra_core_contract.MemoryStore` (remember / recall / verify)
without importing ClawSeal internals. Verify-on-read (the load-bearing guarantee) is
preserved — recall() returns only verified scrolls.

The contract package is optional: if absent, this module still imports and the adapter
returns native dicts.
"""

from __future__ import annotations

from typing import Any, List, Optional

try:
    from mirra_core_contract import Scroll, SignatureScheme, VerificationResult
    _CONTRACT = True
except Exception:
    Scroll = Any  # type: ignore
    VerificationResult = Any  # type: ignore
    SignatureScheme = None  # type: ignore
    _CONTRACT = False

from clawseal_core.memory.scroll_memory_store import ScrollMemoryStore
from clawseal_core.security import qseal_engine as _qe


class ClawSealMemoryStore:
    """Implements the contract's MemoryStore over ClawSeal's ScrollMemoryStore."""

    def __init__(self, base_path: str, agent_id: str = "mirra_agent"):
        self._store = ScrollMemoryStore(base_path=base_path, agent_id=agent_id)
        self._agent_id = agent_id

    def remember(self, agent_id: str, subject_id: str, content: Any) -> "Scroll":
        # ClawSeal's store is constructed per agent_id; subject_id maps to user_id
        # (who the memory is about → enables per-relationship recall).
        result = self._store.remember(content=str(content), user_id=subject_id)
        if not _CONTRACT:
            return result
        scroll = Scroll(
            scroll_id=str(result.get("scroll_id", "")),
            agent_id=agent_id,
            subject_id=subject_id,
            content=content,
            qseal_signature=str(result.get("qseal_signature", "")),
            qseal_prev_signature=str(result.get("qseal_prev_signature", "")),
            qseal_scheme=(SignatureScheme.HMAC_SHA256.value if _CONTRACT else "hmac-sha256"),
        )
        return scroll

    def recall(self, agent_id: str, subject_id: str, query: Optional[str] = None) -> List["Scroll"]:
        # recall() in the store verifies on read and drops tampered scrolls. It returns a
        # dict wrapper {success, count, memories, ...}; the verified scrolls are in "memories".
        # Contract semantics: no query = the subject's full verified history (the store's
        # native recall is relevance-ranked and returns nothing for an empty query).
        if query:
            recall_result = self._store.recall(query=query, user_id=subject_id)
            memories = recall_result.get("memories", []) if isinstance(recall_result, dict) else recall_result
        else:
            memories = self._list_verified(subject_id)
        results: List[Any] = []
        for m in memories:
            if not _CONTRACT:
                results.append(m)
                continue
            results.append(
                Scroll(
                    scroll_id=str(m.get("scroll_id", "")),
                    agent_id=agent_id,
                    subject_id=subject_id,
                    content=m.get("content"),
                    qseal_signature=str(m.get("qseal_signature", "")),
                    qseal_scheme=(SignatureScheme.HMAC_SHA256.value if _CONTRACT else "hmac-sha256"),
                )
            )
        return results

    def _list_verified(self, subject_id: str) -> List[dict]:
        """Every scroll for this subject whose signature verifies, oldest first.

        Same mandatory verify-on-read as the store's recall(): unverified or
        tampered scrolls are dropped, never returned.
        """
        import yaml

        verified: List[dict] = []
        for scroll_file in sorted(self._store.scrolls_dir.glob("*.yaml")):
            with open(scroll_file, "r") as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict) or data.get("user_id") != subject_id:
                continue
            if not _qe.verify_signature(data):
                continue
            verified.append(data)
        verified.sort(key=lambda d: str(d.get("timestamp", "")))
        return verified

    def verify(self, scroll: "Scroll") -> "VerificationResult":
        """Real HMAC verification against the ACTUAL stored signed scroll.

        ClawSeal signs the full scroll dict, so we must verify the stored artifact (loaded
        from disk), not a reconstructed subset. We locate the stored scroll by id and run
        the same verify_signature() the recall path uses. If the caller mutated the
        in-memory Scroll.content, we detect the mismatch against what was signed on disk.
        """
        import yaml

        scroll_id = getattr(scroll, "scroll_id", "")
        stored = None
        for scroll_file in self._store.scrolls_dir.glob("*.yaml"):
            with open(scroll_file, "r") as f:
                data = yaml.safe_load(f)
            if data.get("scroll_id") == scroll_id:
                stored = data
                break

        if stored is None:
            ok = False
            reason = "scroll not found in store"
        else:
            ok = bool(_qe.verify_signature(stored))
            # Also confirm the caller's in-memory content matches what was signed —
            # a mutated in-memory Scroll must not report verified.
            if ok and getattr(scroll, "content", None) is not None:
                if str(scroll.content) != str(stored.get("content")):
                    ok = False
                    reason = "in-memory content differs from signed scroll"
                else:
                    reason = ""
            else:
                reason = "" if ok else "signature verification failed"

        if not _CONTRACT:
            return ok
        return VerificationResult(
            verified=ok,
            scheme=SignatureScheme.HMAC_SHA256.value,
            reason=reason,
        )
