---
name: clawseal
description: Cryptographically-verified memory for AI agents with QSEAL tamper-evidence
version: 1.0.0
author: Shawn Cohen
repository: https://github.com/clawzero/clawseal
license: Apache-2.0
required_binaries:
  - python3
  - openssl
environment_variables:
  - name: QSEAL_SECRET
    description: 256-bit secret for HMAC-SHA256 scroll signing
    required: true
    generation_command: openssl rand -hex 32
---

# ClawSeal — Cryptographic Memory for AI Agents

ClawSeal gives AI agents persistent, tamper-evident memory with zero database dependencies.

## What You Get

- **Scroll-native YAML storage** — Human-readable memory files
- **QSEAL signatures** — HMAC-SHA256 cryptographic verification
- **Chain linking** — Merkle-like temporal lineage
- **Text-based search** — Keyword matching (no vector embeddings)

## Installation via ClawHub

```bash
clawhub install clawseal
```

This will:
1. Clone the repository
2. Generate a secure QSEAL_SECRET (256-bit)
3. Add QSEAL_SECRET to your shell profile
4. Create Python virtual environment
5. Install dependencies (PyYAML only)
6. Run verification tests

## Manual Installation

```bash
git clone https://github.com/clawzero/clawseal.git
cd clawseal
./setup.sh
```

## Quick Start

```bash
# Run the three-layer demo
./run_full_demo.sh
```

Expected output:
- **Layer 1:** 100% drift (baseline AI without memory)
- **Layer 2:** 0% drift (ClawSeal with QSEAL verification)
- **Layer 3:** Cryptographic proof (HMAC-SHA256 signatures verified)

## Usage as Python Package

```python
from clawseal import ScrollMemoryStore

# Initialize memory store
memory = ScrollMemoryStore(user_id="demo_agent")

# Create a memory scroll
memory.remember(
    content="User prefers concise explanations",
    memory_type="preference"
)

# Recall memories (QSEAL-verified)
results = memory.recall(query="explanation")
for scroll in results:
    print(f"✅ {scroll['content']}")
    print(f"   QSEAL: {scroll['qseal_signature'][:32]}...")
```

## Security Model

**QSEAL_SECRET is critical** — treat it like a database password.

- ✅ **DO:** Store in environment variables, rotate regularly
- ❌ **DON'T:** Commit to git, share via email, use demo secret in production

The demo secret `test_secret_key_for_demo` is **PUBLIC** — only for demos/tests.

## Architecture

```
Stateless LLM
     ↓
ClawSeal Memory Layer (this package)
     ↓
YAML Scroll Files (data/scrolls/)
     ↓
QSEAL Signatures (HMAC-SHA256)
```

No ChromaDB. No vector database. No Docker. Just YAML + cryptography.

## What This Is NOT

- ❌ Not claiming sentience or consciousness
- ❌ Not a vector database replacement for semantic similarity
- ❌ Not a distributed system (local-first, single agent)

## What It Actually Does

- ✅ Persistent state across sessions
- ✅ Identity continuity (measurable drift metrics)
- ✅ Cryptographic tamper-evidence
- ✅ Human-readable, Git-friendly storage

## Performance

- **Scroll creation:** ~1-2ms (HMAC + YAML write)
- **Recall (100 scrolls):** ~10-50ms (linear search)
- **Recall (1,000 scrolls):** ~100-500ms

For >10,000 scrolls, indexing planned for v1.2.

## Support

- **Issues:** https://github.com/clawzero/clawseal/issues
- **Docs:** https://github.com/clawzero/clawseal#readme
- **Security:** security@mvar.io

## License

Apache 2.0 — Open source, commercial use allowed.

---

**This isn't theory. This is running code.**

All claims proven with timestamped ground truth artifacts dated April 14, 2026.
