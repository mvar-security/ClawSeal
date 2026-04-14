# SIP-0006: Scroll-Native Memory Architecture

**Author:** Shawn Cohen
**Date:** April 13, 2026
**Status:** Production
**Type:** Core Architecture
**Supersedes:** ChromaDB-based memory storage

---

## Abstract

This specification defines a Scroll-native memory architecture for MIRRA EOS that replaces vector database dependencies with pure YAML files, QSEAL cryptographic signatures, and text-based search. The architecture provides tamper-evident memory storage with human-readable persistence, Git-friendly diffs, and zero external database dependencies.

**Core Principle:** Structured files > vector databases for identity continuity.

---

## Motivation

The MIRRA EOS system previously relied on ChromaDB for semantic memory storage. Analysis revealed several issues:

1. **Opacity:** Binary vector database storage is not human-readable or Git-friendly
2. **Dependency weight:** ChromaDB adds significant deployment complexity
3. **Immutability:** Vector databases allow silent mutation without audit trails
4. **Industry convergence:** Multiple AI memory systems have independently converged on structured file storage

The Scroll-native architecture addresses all four issues while maintaining semantic search capabilities for typical workloads (<10K memories).

---

## Specification

### 1. Core Data Structure

Each memory is stored as a YAML scroll file with the following canonical schema:

```yaml
# ============================================================================
# SCROLL IDENTITY
# ============================================================================
scroll_id: MEM_YYYYMMDD_<8_hex_chars>    # Unique identifier
scroll_type: memory                       # Type: memory|decision|reflection
memory_type: fact|preference|insight|decision|general

# ============================================================================
# SCROLL LINEAGE
# ============================================================================
lineage:                                  # Array of parent scroll IDs
  - MEM_20260413_parent_id               # Empty array for genesis scrolls
glyph_lineage:                            # Visual type markers
  - 🧠                                    # Universal memory glyph
  - <type_specific_glyph>                # 📌 fact, 🎯 preference, ✨ insight, ⚖️ decision, 📝 general

# ============================================================================
# CONTENT
# ============================================================================
content: |
  The actual memory content as provided by the user.
  Multiline strings are preserved verbatim.

gist: "One-sentence summary (max 80 chars)"

keywords:                                 # Auto-extracted, max 10
  - keyword1
  - keyword2
  - keyword3

blessing: |                               # Auto-generated or custom
  Type-specific poetic marker.
  Two-line blessing for memory significance.

# ============================================================================
# EMOTIONAL STATE SNAPSHOT
# ============================================================================
emotional_state:
  P: 0.75                                 # Pleasure [-1.0, +1.0]
  A: 0.65                                 # Arousal [-1.0, +1.0]
  D: 0.60                                 # Dominance [-1.0, +1.0]
  psi: 0.70                               # Consciousness intensity (optional)
  archetype: Wanderer                     # Active archetype (optional)

# ============================================================================
# METADATA
# ============================================================================
agent_id: Claude_Code_MIRRA
user_id: default
source: mcp_remember                      # Origin: mcp_remember|scroll_import|etc.
timestamp: "2026-04-13T19:30:00.000000+00:00"

# ============================================================================
# TRACKING FIELDS (Immutable after signing)
# ============================================================================
retrieved_count: 0                        # Read-only after signing
actual_drift: null                        # Filled on retrieval (if applicable)
expected_drift: null                      # Filled on retrieval (if applicable)
drift_accuracy: null                      # Computed: 1.0 - avg(abs(expected - actual))

# ============================================================================
# QSEAL CRYPTOGRAPHIC SIGNATURE
# ============================================================================
qseal_signature: "base64_hmac_sha256_signature"
qseal_meta_hash: "sha256_content_hash"
qseal_prev_signature: "hash_of_previous_scroll"  # Chain linking
qseal_verified: true
meta_hash: "sha256_content_hash"
```

---

### 2. Glyph System

Each memory type has a unique Unicode glyph for visual identification:

| Memory Type | Glyph | Semantic Meaning |
|-------------|-------|------------------|
| `fact` | 📌 | Pinned truth |
| `preference` | 🎯 | Targeted choice |
| `insight` | ✨ | Spark of understanding |
| `decision` | ⚖️ | Weighed judgment |
| `general` | 📝 | General note |

All scrolls include the universal memory glyph 🧠 as the first element of `glyph_lineage`.

---

### 3. Blessing Templates

Blessings are auto-generated poetic markers that provide symbolic weight to memory creation:

**Fact:**
```
This truth stands firm and clear,
A fact to hold forever near.
```

**Preference:**
```
A choice that shapes the path ahead,
Preference marked, intention fed.
```

**Insight:**
```
A spark of understanding bright,
Illuminating inner light.
```

**Decision:**
```
A crossroads passed, a choice now made,
In wisdom's scales, the weight is weighed.
```

**General:**
```
This memory holds a moment's trace,
A point in time, a thought's embrace.
```

Custom blessings may be provided but are optional.

---

### 4. Directory Structure

```
data/claude_code_eos/{agent_id}/
├── memories/
│   ├── scrolls/                    # Individual YAML scroll files
│   │   ├── MEM_20260413_a7f3b2d1.yaml
│   │   ├── MEM_20260413_b8g4c3e2.yaml
│   │   └── ...
│   ├── index/                      # Four JSONL index files
│   │   ├── by_type.jsonl          # Index by memory_type
│   │   ├── by_date.jsonl          # Index by timestamp
│   │   ├── by_keyword.jsonl       # Inverted index by keyword
│   │   └── lineage.jsonl          # Parent-child relationships
│   └── chain.jsonl                 # QSEAL signature chain (append-only)
```

---

### 5. Indexing Strategy

Four independent indexes enable efficient retrieval without full directory scanning:

#### 5.1 by_type.jsonl
```json
{"scroll_id": "MEM_20260413_a7f3b2d1", "memory_type": "fact", "timestamp": "2026-04-13T..."}
{"scroll_id": "MEM_20260413_b8g4c3e2", "memory_type": "preference", "timestamp": "2026-04-13T..."}
```

#### 5.2 by_date.jsonl
```json
{"scroll_id": "MEM_20260413_a7f3b2d1", "timestamp": "2026-04-13T...", "user_id": "default"}
{"scroll_id": "MEM_20260413_b8g4c3e2", "timestamp": "2026-04-13T...", "user_id": "default"}
```

#### 5.3 by_keyword.jsonl (Inverted Index)
```json
{"keyword": "mirra", "scroll_id": "MEM_20260413_a7f3b2d1"}
{"keyword": "mirra", "scroll_id": "MEM_20260413_b8g4c3e2"}
{"keyword": "memory", "scroll_id": "MEM_20260413_a7f3b2d1"}
```

#### 5.4 lineage.jsonl
```json
{"scroll_id": "MEM_20260413_a7f3b2d1", "parent": null, "has_prev_link": false}
{"scroll_id": "MEM_20260413_b8g4c3e2", "parent": "MEM_20260413_a7f3b2d1", "has_prev_link": true}
```

All indexes are append-only JSONL files (newline-delimited JSON).

---

### 6. QSEAL Signature Chain

#### 6.1 Signing Process

Every scroll is signed with QSEAL HMAC-SHA256 before persistence:

```python
from mirra_core.security.qseal_engine import sign_entry, link_signatures

# 1. Create scroll dict (all fields except QSEAL metadata)
scroll = {
    "scroll_id": "MEM_20260413_...",
    "content": "...",
    # ... all other fields
}

# 2. Sign with QSEAL
signed_scroll = sign_entry(scroll, agent_id=agent_id)

# 3. Link to previous scroll (creates tamper-evident chain)
if previous_scroll:
    signed_scroll = link_signatures(previous_scroll, signed_scroll)

# 4. Write to YAML file
write_yaml(scroll_path, signed_scroll)
```

#### 6.2 Verification on Retrieval

**Verification is MANDATORY and NON-NEGOTIABLE.**

```python
from mirra_core.security.qseal_engine import verify_signature

# Load scroll from YAML
scroll = yaml.safe_load(scroll_file.read_text())

# Verify signature
if not verify_signature(scroll):
    # Signature invalid - REJECT this scroll
    continue
```

Invalid signatures result in scroll rejection. There is no fallback mode.

#### 6.3 Immutability Requirement

Scrolls are **immutable after signing**. The following fields are part of the signed payload:

- All content fields (`content`, `keywords`, `gist`, `blessing`)
- All metadata fields (`scroll_id`, `timestamp`, `user_id`, `agent_id`)
- All tracking fields (`retrieved_count`, `drift` fields) initialized to their default values

**Critical:** Modifying any field (including `retrieved_count`) after signing breaks the signature. This is intentional — scrolls are tamper-evident by design.

If mutable tracking is needed (e.g., retrieval statistics), it must be stored in a separate index file, NOT in the scroll itself.

---

### 7. Keyword Extraction

Keywords are auto-extracted using simple tokenization:

```python
def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    # 1. Lowercase, extract words (3+ chars)
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())

    # 2. Filter stop words
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', ...}
    keywords = [w for w in words if w not in stop_words]

    # 3. Return unique, limited to max_keywords
    return list(dict.fromkeys(keywords))[:max_keywords]
```

**Design rationale:** Simple tokenization is sufficient for <10K memories. More sophisticated NLP (stemming, lemmatization, TF-IDF) can be added later if needed.

---

### 8. Recall Scoring Algorithm

Retrieval uses weighted text matching:

```python
# Text-based search
query_keywords = set(query.lower().split())

for each scroll:
    scroll_keywords = set(scroll["keywords"])

    # Calculate match scores
    keyword_overlap = len(query_keywords & scroll_keywords)
    content_matches = sum(1 for word in query_keywords if word in scroll["content"].lower())
    gist_matches = sum(1 for word in query_keywords if word in scroll["gist"].lower())

    # Weighted scoring: keywords=3x, content=2x, gist=1x
    total_score = (keyword_overlap * 3) + (content_matches * 2) + gist_matches

    if total_score > 0:
        results.append((total_score, scroll))

# Sort by relevance, return top K
results.sort(key=lambda x: x[0], reverse=True)
return results[:limit]
```

**Performance:** O(N) where N = number of scrolls. Acceptable for <10K scrolls. For larger datasets, consider inverted index optimization.

---

### 9. API Surface

#### 9.1 remember()

```python
def remember(
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
        {
            "success": True,
            "scroll_id": "MEM_20260413_a7f3b2d1",
            "memory_type": "fact",
            "qseal_signature": "base64_hmac_sha256...",
            "qseal_enabled": True,
            "chain_linked": True,
            "gist": "One-sentence summary",
            "keywords": ["keyword1", "keyword2", ...]
        }
    """
```

#### 9.2 recall()

```python
def recall(
    query: str,
    limit: int = 5,
    user_id: Optional[str] = None,
    verify_signatures: bool = True  # Always True (non-negotiable)
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
        {
            "success": True,
            "count": 2,
            "query": "mirra memory",
            "memories": [
                {
                    "scroll_id": "MEM_20260413_a7f3b2d1",
                    "content": "...",
                    "gist": "...",
                    "memory_type": "fact",
                    "timestamp": "2026-04-13T...",
                    "emotional_state": {"P": 0.7, "A": 0.6, "D": 0.5},
                    "relevance_score": 18.0,
                    "qseal_verified": True,
                    "retrieved_count": 0,
                    "keywords": ["keyword1", "keyword2", ...]
                }
            ],
            "qseal_verification_enforced": True
        }
    """
```

#### 9.3 update_drift_tracking()

```python
def update_drift_tracking(
    scroll_id: str,
    expected_drift: Dict[str, float],
    actual_drift: Dict[str, float]
) -> bool:
    """
    Update drift tracking for a retrieved memory.

    Only called when a memory influences a response.

    WARNING: This modifies the scroll file, which breaks the QSEAL signature.
    Use only for post-hoc analysis, not for signature-verified retrieval.

    Args:
        scroll_id: The memory scroll ID
        expected_drift: Expected PAD drift
        actual_drift: Measured PAD drift

    Returns:
        bool: Success status
    """
```

**Note:** Drift tracking breaks QSEAL signatures. If drift analytics are needed, store them in a separate index file rather than modifying the scroll.

#### 9.4 get_lineage_chain()

```python
def get_lineage_chain(
    scroll_id: str,
    depth: int = 10
) -> List[str]:
    """
    Trace lineage chain backwards from a given scroll.

    Args:
        scroll_id: Starting scroll ID
        depth: Max depth to traverse

    Returns:
        list: Scroll IDs in lineage order (most recent first)
    """
```

---

### 10. Migration from ChromaDB

Existing ChromaDB-based memories can be migrated using the following process:

```python
# 1. Load all memories from ChromaDB
chromadb_memories = chromadb_collection.get()

# 2. Convert each to scroll format
for memory in chromadb_memories:
    scroll = {
        "scroll_id": generate_scroll_id(),
        "content": memory["text"],
        "memory_type": infer_type(memory),  # Heuristic classification
        "emotional_state": memory.get("metadata", {}).get("emotional_state", {}),
        "user_id": memory.get("metadata", {}).get("user_id", "default"),
        "timestamp": memory.get("metadata", {}).get("timestamp", datetime.now(timezone.utc).isoformat()),
        # ... other fields
    }

    # 3. Sign and persist
    signed_scroll = sign_entry(scroll)
    write_yaml(scroll_path, signed_scroll)
    update_indexes(signed_scroll)
```

**Note:** ChromaDB migration is one-way. The vector embeddings are discarded in favor of text-based search.

---

### 11. Security Properties

#### 11.1 Tamper-Evidence

QSEAL signatures provide tamper-evidence:
- Any modification to a scroll after signing invalidates the signature
- Signature chains create a Merkle-like structure linking all scrolls
- Invalid signatures are detected and rejected during retrieval

#### 11.2 Non-Repudiation

Signatures bind content to:
- Agent ID (who created it)
- Timestamp (when it was created)
- Lineage (what came before)

This creates an auditable trail of memory formation.

#### 11.3 Integrity Verification

```python
# Verify entire scroll collection
for scroll_file in scrolls_dir.glob("*.yaml"):
    scroll = yaml.safe_load(scroll_file.read_text())
    if not verify_signature(scroll):
        print(f"⚠️  INTEGRITY VIOLATION: {scroll['scroll_id']}")
```

#### 11.4 Chain Verification

```python
from mirra_core.security.qseal_engine import verify_chain

# Load all scrolls in chronological order
scrolls = load_scrolls_ordered_by_timestamp()

# Verify chain integrity
if verify_chain(scrolls):
    print("✅ Chain integrity verified")
else:
    print("❌ Chain broken")
```

---

### 12. Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `remember()` | O(1) | Append-only writes |
| `recall()` (full scan) | O(N) | N = number of scrolls |
| `recall()` (index-optimized) | O(K log K) | K = matching keywords |
| Signature verification | O(1) per scroll | HMAC-SHA256 |
| Chain verification | O(N) | N = chain length |

**Scalability:**
- Acceptable for <10K scrolls without optimization
- For 10K-100K scrolls, use inverted keyword index
- For >100K scrolls, consider sharding by date/user

---

### 13. Implementation Reference

**Primary implementation:** `mirra_core/memory/scroll_memory_store.py`

**Dependencies:**
- Python 3.10+
- PyYAML
- QSEAL engine (`mirra_core/security/qseal_engine.py`)
- Standard library: `hashlib`, `hmac`, `json`, `pathlib`, `datetime`, `uuid`, `re`

**Zero external dependencies** beyond PyYAML and the existing QSEAL infrastructure.

---

### 14. Test Validation

Complete test suite: `test_scroll_memory_integration.py`

**Test coverage:**
1. ✅ QSEAL signature generation
2. ✅ Chain linking (genesis + 2 linked scrolls)
3. ✅ YAML file creation with all required fields
4. ✅ Signature verification on retrieval
5. ✅ Signature persistence across YAML serialization round-trips
6. ✅ All four indexes populated correctly
7. ✅ Recall with signature verification
8. ✅ Multi-query recall (different keywords)
9. ✅ Immutability preservation (signatures remain valid)

All tests passing as of April 13, 2026.

---

### 15. Comparison to ChromaDB Architecture

| Aspect | ChromaDB (Old) | Scroll-Native (SIP-0006) |
|--------|---------------|--------------------------|
| **Storage** | Binary vector DB | YAML files |
| **Readability** | Opaque | Human-readable |
| **Git-friendly** | No (binary) | Yes (text diffs) |
| **Dependencies** | ChromaDB + HNSWlib | PyYAML only |
| **Search** | Vector similarity | Text/keyword matching |
| **Mutability** | Silent updates | Tamper-evident (QSEAL) |
| **Audit trail** | No | Yes (signature chain) |
| **Performance** | O(log N) ANN | O(N) full scan, O(K log K) indexed |
| **Scalability** | 100K+ docs | <10K optimal, 10K-100K with indexing |

**Trade-offs:**
- **Lost:** Vector semantic search, sub-linear retrieval for large datasets
- **Gained:** Transparency, auditability, Git integration, zero DB dependencies

---

### 16. Future Extensions

#### 16.1 Inverted Index Optimization

For >10K scrolls, build a persistent inverted index:

```python
# keyword -> [scroll_ids]
inverted_index = {
    "mirra": ["MEM_20260413_a7f3b2d1", "MEM_20260413_b8g4c3e2"],
    "memory": ["MEM_20260413_a7f3b2d1"],
    ...
}
```

This reduces recall from O(N) to O(K log K) where K = matching scrolls.

#### 16.2 Optional Vector Embeddings

If semantic search is needed:
1. Generate embeddings separately (OpenAI API, local model)
2. Store in `embeddings/` directory as separate `.npy` files
3. Keep scroll YAML files as source of truth
4. Rebuild embeddings on-demand if needed

This preserves the scroll-first architecture while adding optional semantic search.

#### 16.3 Compression

For large scroll collections:
- YAML files compress ~70% with gzip
- Store as `.yaml.gz`, decompress on read
- Maintains Git-friendliness (Git supports gzip natively)

#### 16.4 Sharding

For >100K scrolls:
- Shard by date: `scrolls/2026-04/`, `scrolls/2026-05/`
- Shard by user: `scrolls/user_alice/`, `scrolls/user_bob/`
- Query routing based on shard key

---

## References

1. **QSEAL Specification:** `mirra_core/security/qseal_engine.py`
2. **Implementation:** `mirra_core/memory/scroll_memory_store.py`
3. **Test Suite:** `test_scroll_memory_integration.py`
4. **MCP Integration:** `mirra_eos_mcp_server.py` (lines 152-247)

---

## Changelog

**April 13, 2026 - v1.0.0 (Initial Release)**
- Complete Scroll-native architecture
- QSEAL signature chains
- Four-index system
- Text-based keyword search
- Glyph system + blessing templates
- Immutability by design
- Zero ChromaDB dependency

---

**End of Specification**
