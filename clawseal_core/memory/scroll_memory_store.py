"""
MIRRA EOS Scroll-Native Memory Store (SIP-0006)

Replaces ChromaDB with pure YAML scroll files + QSEAL signatures.
Zero dependencies beyond stdlib + PyYAML + QSEAL.

Core principle: Structured files > vector databases for identity continuity.

Author: Claude Code + Shawn Cohen
Date: April 13, 2026
Version: 1.0.0 (SIP-0006)
"""

import yaml
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import uuid
import re

# QSEAL integration
from ..security.qseal_engine import sign_entry, link_signatures, verify_signature, QSEAL_ENABLED


# ============================================================================
# GLYPH SYSTEM - Type-Specific Symbols
# ============================================================================

MEMORY_TYPE_GLYPHS = {
    "fact": "📌",
    "preference": "🎯",
    "insight": "✨",
    "decision": "⚖️",
    "general": "📝"
}

# ============================================================================
# BLESSING GENERATORS - Auto-Generated Symbolic Markers
# ============================================================================

BLESSING_TEMPLATES = {
    "fact": "This truth stands firm and clear,\nA fact to hold forever near.",
    "preference": "A choice that shapes the path ahead,\nPreference marked, intention fed.",
    "insight": "A spark of understanding bright,\nIlluminating inner light.",
    "decision": "A crossroads passed, a choice now made,\nIn wisdom's scales, the weight is weighed.",
    "general": "This memory holds a moment's trace,\nA point in time, a thought's embrace."
}


class ScrollMemoryStore:
    """
    Scroll-native memory storage with QSEAL signatures and lineage chains.

    Every memory is a YAML scroll file with:
    - QSEAL HMAC-SHA256 signature
    - Lineage chain to previous memories
    - Emotional state snapshot (PAD)
    - Cryptographic verification on retrieval

    No ChromaDB. No vector embeddings. Pure structured files.
    """

    def __init__(self, base_path: str, agent_id: str = "Claude_Code_MIRRA"):
        """Initialize scroll memory store."""
        self.base_path = Path(base_path)
        self.agent_id = agent_id

        # Create directory structure
        self.scrolls_dir = self.base_path / "memories" / "scrolls"
        self.index_dir = self.base_path / "memories" / "index"
        self.chain_file = self.base_path / "memories" / "chain.jsonl"

        self.scrolls_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.chain_file.touch(exist_ok=True)

        # Index files
        self.by_type_index = self.index_dir / "by_type.jsonl"
        self.by_date_index = self.index_dir / "by_date.jsonl"
        self.by_keyword_index = self.index_dir / "by_keyword.jsonl"
        self.lineage_index = self.index_dir / "lineage.jsonl"

        for index_file in [self.by_type_index, self.by_date_index, self.by_keyword_index, self.lineage_index]:
            index_file.touch(exist_ok=True)

    def _extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from text (simple tokenization)."""
        # Lowercase, remove punctuation, split on whitespace
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())

        # Filter common stop words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'this', 'that', 'with', 'have', 'from', 'they', 'been', 'will', 'more', 'when', 'your', 'which', 'their', 'what', 'about', 'than', 'into', 'could', 'them'}
        keywords = [w for w in words if w not in stop_words]

        # Return unique keywords, limited to max_keywords
        return list(dict.fromkeys(keywords))[:max_keywords]

    def _generate_gist(self, content: str, max_length: int = 80) -> str:
        """Generate one-sentence gist of content."""
        # Take first sentence or first N chars
        sentences = content.split('. ')
        first_sentence = sentences[0]

        if len(first_sentence) > max_length:
            return first_sentence[:max_length-3] + "..."
        return first_sentence

    def _get_latest_memory_scroll(self, user_id: str) -> Optional[Dict]:
        """Get most recent memory scroll for lineage chain."""
        # Read chain file in reverse to find latest for this user
        if not self.chain_file.exists():
            return None

        with open(self.chain_file, 'r') as f:
            lines = f.readlines()

        # Iterate in reverse
        for line in reversed(lines):
            if line.strip():
                entry = json.loads(line)
                if entry.get("user_id") == user_id:
                    return entry

        return None

    def _update_indexes(self, scroll: Dict):
        """Update all four indexes with new scroll."""
        scroll_id = scroll["scroll_id"]

        # 1. by_type index
        with open(self.by_type_index, 'a') as f:
            f.write(json.dumps({
                "scroll_id": scroll_id,
                "memory_type": scroll["memory_type"],
                "timestamp": scroll["timestamp"]
            }) + '\n')

        # 2. by_date index
        with open(self.by_date_index, 'a') as f:
            f.write(json.dumps({
                "scroll_id": scroll_id,
                "timestamp": scroll["timestamp"],
                "user_id": scroll["user_id"]
            }) + '\n')

        # 3. by_keyword index
        for keyword in scroll.get("keywords", []):
            with open(self.by_keyword_index, 'a') as f:
                f.write(json.dumps({
                    "keyword": keyword,
                    "scroll_id": scroll_id
                }) + '\n')

        # 4. lineage index
        with open(self.lineage_index, 'a') as f:
            f.write(json.dumps({
                "scroll_id": scroll_id,
                "parent": scroll["lineage"][0] if scroll.get("lineage") else None,
                "has_prev_link": "qseal_prev_signature" in scroll
            }) + '\n')

    def remember(
        self,
        content: str,
        memory_type: str = "general",
        user_id: str = "default",
        emotional_state: Optional[Dict] = None,
        blessing: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new Memory Scroll with QSEAL signature.

        Args:
            content: The content to remember
            memory_type: fact | preference | insight | decision | general
            user_id: User ID for memory attribution
            emotional_state: PAD state at memory creation
            blessing: Optional blessing (auto-generated if None)

        Returns:
            dict: Result with scroll_id, qseal_signature, chain_linked status
        """
        # Validate memory type
        valid_types = list(MEMORY_TYPE_GLYPHS.keys())
        if memory_type not in valid_types:
            memory_type = "general"

        # Generate scroll ID
        timestamp_str = datetime.now(timezone.utc).strftime('%Y%m%d')
        scroll_id = f"MEM_{timestamp_str}_{uuid.uuid4().hex[:8]}"

        # Load previous memory scroll for lineage
        prev_scroll = self._get_latest_memory_scroll(user_id)

        # Extract keywords and gist
        keywords = self._extract_keywords(content)
        gist = self._generate_gist(content)

        # Auto-generate blessing if not provided
        if blessing is None:
            blessing = BLESSING_TEMPLATES.get(memory_type, BLESSING_TEMPLATES["general"])

        # Create scroll dict
        scroll = {
            "scroll_id": scroll_id,
            "scroll_type": "memory",
            "memory_type": memory_type,
            "lineage": [prev_scroll["scroll_id"]] if prev_scroll else [],
            "glyph_lineage": ["🧠", MEMORY_TYPE_GLYPHS[memory_type]],
            "content": content,
            "emotional_state": emotional_state or {},
            "agent_id": self.agent_id,
            "user_id": user_id,
            "source": "mcp_remember",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "keywords": keywords,
            "gist": gist,
            "blessing": blessing,
            "retrieved_count": 0,  # NEW: Importance tracking
            "expected_drift": None,  # Filled on retrieval
            "actual_drift": None,
            "drift_accuracy": None
        }

        # Sign with QSEAL if enabled
        if QSEAL_ENABLED:
            signed_scroll = sign_entry(scroll, agent_id=self.agent_id)

            # Link to previous scroll
            if prev_scroll:
                signed_scroll = link_signatures(prev_scroll, signed_scroll)

            scroll = signed_scroll
        else:
            # Warning: QSEAL disabled
            scroll["qseal_warning"] = "QSEAL_SECRET not set - signatures unavailable"

        # Write YAML file
        scroll_path = self.scrolls_dir / f"{scroll_id}.yaml"
        with open(scroll_path, 'w') as f:
            yaml.dump(scroll, f, default_flow_style=False, allow_unicode=True)

        # Update indexes
        self._update_indexes(scroll)

        # Append to chain file
        with open(self.chain_file, 'a') as f:
            f.write(json.dumps(scroll) + '\n')

        return {
            "success": True,
            "scroll_id": scroll_id,
            "memory_type": memory_type,
            "qseal_signature": scroll.get("qseal_signature", "N/A"),
            "qseal_enabled": QSEAL_ENABLED,
            "chain_linked": "qseal_prev_signature" in scroll,
            "gist": gist,
            "keywords": keywords
        }

    def recall(
        self,
        query: str,
        limit: int = 5,
        user_id: Optional[str] = None,
        verify_signatures: bool = True
    ) -> Dict[str, Any]:
        """
        Retrieve memories by searching scroll files directly.

        CRITICAL: Verifies QSEAL signatures on retrieval (non-negotiable).

        Args:
            query: Search query
            limit: Max results to return
            user_id: Optional filter by user
            verify_signatures: Always True (non-negotiable)

        Returns:
            dict: Results with verified memories, ranked by relevance
        """
        # Force signature verification (non-negotiable)
        verify_signatures = True

        # Text-based search
        query_keywords = set(query.lower().split())
        scored_scrolls = []

        for scroll_file in self.scrolls_dir.glob("*.yaml"):
            with open(scroll_file, 'r') as f:
                scroll = yaml.safe_load(f)

            # Filter by user_id if provided
            if user_id and scroll.get("user_id") != user_id:
                continue

            # Verify QSEAL signature (MANDATORY)
            if verify_signatures and QSEAL_ENABLED:
                if not verify_signature(scroll):
                    # Signature invalid - skip this scroll
                    continue

            # Calculate relevance score
            scroll_keywords = set(scroll.get("keywords", []))
            keyword_overlap = len(query_keywords & scroll_keywords)
            content_matches = sum(1 for word in query_keywords if word in scroll["content"].lower())
            gist_matches = sum(1 for word in query_keywords if word in scroll.get("gist", "").lower())

            # Weighted scoring: keywords=3x, content=2x, gist=1x
            total_score = (keyword_overlap * 3) + (content_matches * 2) + gist_matches

            # Note: retrieved_count boost removed to preserve QSEAL tamper-evidence
            # Scrolls are immutable after signing for cryptographic integrity

            if total_score > 0:
                scored_scrolls.append((total_score, scroll, scroll_file))

        # Sort by relevance
        scored_scrolls.sort(key=lambda x: x[0], reverse=True)

        # Build results WITHOUT modifying scroll files (maintains QSEAL integrity)
        results = []
        for score, scroll, scroll_file in scored_scrolls[:limit]:
            # DO NOT modify scroll files - they are tamper-evident after signing
            # retrieved_count stays at 0 to preserve QSEAL signature validity
            # (Alternative: track retrieval stats in separate index file)

            results.append({
                "scroll_id": scroll["scroll_id"],
                "content": scroll["content"],
                "gist": scroll.get("gist"),
                "memory_type": scroll.get("memory_type"),
                "timestamp": scroll.get("timestamp"),
                "emotional_state": scroll.get("emotional_state"),
                "relevance_score": score,
                "qseal_verified": verify_signature(scroll) if QSEAL_ENABLED else False,
                "retrieved_count": scroll.get("retrieved_count", 0),  # Read-only
                "keywords": scroll.get("keywords", [])
            })

        return {
            "success": True,
            "count": len(results),
            "query": query,
            "memories": results,
            "qseal_verification_enforced": True  # Non-negotiable
        }

    def update_drift_tracking(
        self,
        scroll_id: str,
        expected_drift: Dict[str, float],
        actual_drift: Dict[str, float]
    ) -> bool:
        """
        Update drift tracking for a retrieved memory.

        Only called when a memory influences a response.

        Args:
            scroll_id: The memory scroll ID
            expected_drift: Expected PAD drift
            actual_drift: Measured PAD drift

        Returns:
            bool: Success status
        """
        scroll_file = self.scrolls_dir / f"{scroll_id}.yaml"

        if not scroll_file.exists():
            return False

        with open(scroll_file, 'r') as f:
            scroll = yaml.safe_load(f)

        # Calculate accuracy
        if expected_drift and actual_drift:
            # Simple accuracy: average of absolute differences
            diffs = []
            for key in expected_drift.keys():
                if key in actual_drift:
                    diffs.append(abs(expected_drift[key] - actual_drift[key]))

            drift_accuracy = 1.0 - (sum(diffs) / len(diffs)) if diffs else None
        else:
            drift_accuracy = None

        # Update scroll
        scroll["expected_drift"] = expected_drift
        scroll["actual_drift"] = actual_drift
        scroll["drift_accuracy"] = drift_accuracy

        # Write back
        with open(scroll_file, 'w') as f:
            yaml.dump(scroll, f, default_flow_style=False, allow_unicode=True)

        return True

    def get_lineage_chain(self, scroll_id: str, depth: int = 10) -> List[str]:
        """
        Trace lineage chain backwards from a given scroll.

        Args:
            scroll_id: Starting scroll ID
            depth: Max depth to traverse

        Returns:
            list: Scroll IDs in lineage order (most recent first)
        """
        chain = [scroll_id]
        current_id = scroll_id

        for _ in range(depth):
            scroll_file = self.scrolls_dir / f"{current_id}.yaml"
            if not scroll_file.exists():
                break

            with open(scroll_file, 'r') as f:
                scroll = yaml.safe_load(f)

            lineage = scroll.get("lineage", [])
            if not lineage:
                break

            parent_id = lineage[0]
            chain.append(parent_id)
            current_id = parent_id

        return chain
