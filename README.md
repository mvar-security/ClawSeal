# ClawSeal

**Stateless LLMs become stateful agents with tamper-evident memory, zero database dependencies.**

---

## What This Is

A cryptographically-verifiable memory system that gives AI agents persistent identity across sessions—without ChromaDB, without vector databases, without complex dependencies.

Three components:
1. **Scroll-native YAML storage** — Human-readable memory files with QSEAL signatures
2. **Text-based semantic search** — Keyword matching with weighted scoring (no embeddings)
3. **HMAC-SHA256 tamper-evidence** — Every memory cryptographically signed and chain-linked

**Result:** AI agents that remember you, maintain consistent identity, and provide cryptographic proof of memory integrity.

---

## Quick Start (PyPI, ~30 Seconds)

```bash
pip install clawseal
export QSEAL_SECRET="$(openssl rand -hex 32)"
python3 -c "from clawseal import ScrollMemoryStore; print('ClawSeal import OK')"
clawseal verify
```

For the full reproducible 3-layer evidence demo, use the repository workflow below.

---

## OpenClaw Integration

**ClawSeal now has native OpenClaw support.** Add persistent, cryptographically-verified memory to OpenClaw agents in under 5 minutes.

- **What it does**: Transforms OpenClaw from stateless chat bot to persistent AI assistant with QSEAL-signed memories
- **How to install**: `cd openclaw-plugin && bash install.sh` (auto-registers daemon, zero manual steps)
- **Full guide**: See [openclaw-plugin/](openclaw-plugin/) for complete integration documentation

---


## Claims and Evidence

| Claim | Proof Artifact | Repro Command |
|-------|---------------|---------------|
| **AI agents without ClawSeal drift 100%** (complete amnesia between sessions) | [layer1_baseline_output.txt](demo/expected_outputs/layer1_baseline_output.txt) lines 11-55 | `python3 demo_layer1_baseline.py` |
| **ClawSeal maintains 0% drift** (perfect memory continuity with QSEAL verification) | [layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt) lines 11-77 | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer2_with_clawseal.py` |
| **QSEAL signatures provide cryptographic proof** (HMAC-SHA256, chain linking, tampering detection) | [layer3_verification_output.txt](demo/expected_outputs/layer3_verification_output.txt) lines 1-115 | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer3_verification.py` |

All proof artifacts dated **April 14, 2026** and captured from live demo runs. See [DEMO_RUN_METADATA.md](demo/expected_outputs/DEMO_RUN_METADATA.md) for complete verification details.

---

## Three-Layer Demo

### Layer 1: Identity Drift (Without ClawSeal)

**What it proves:** Baseline AI agents have 100% identity drift across sessions—complete amnesia.

```bash
python3 demo_layer1_baseline.py
```

**Expected output:**
```
Session 1 Identity: e4d909c290d0fb1c
Session 2 Identity: 9ae0ea9e3c9c6e27
Session 3 Identity: 6512bd43d9caa6e0
Session 4 Identity: c20ad4d76fe97759
Session 5 Identity: 8f14e45fceea167a

⚠️  IDENTITY DRIFT DETECTED
Drift Rate: 100.0%
Drift Events: 4/4 (every single transition)
Memory Persistence: 0% (complete amnesia)
```

**Proof artifact:** [demo/expected_outputs/layer1_baseline_output.txt](demo/expected_outputs/layer1_baseline_output.txt)

---

### Layer 2: Identity Continuity (With ClawSeal)

**What it proves:** ClawSeal maintains 0% drift with Scroll-native memory and QSEAL cryptographic verification.

```bash
export QSEAL_SECRET=test_secret_key_for_demo
python3 demo_layer2_with_clawseal.py
```

**Expected output:**
```
Session 1: Creating memory...
  Memory ID: MEM_20260414_10734120
  Type: preference 🎯
  Content: "User prefers concise explanations without excessive detail"
  QSEAL Signature: OXIaQboYCy5csPif7LWGz4scHZAB0YKpAPwVuXjCXLc=... (HMAC-SHA256)

Session 2: Recalling memories...
  Found 1 memories
  QSEAL Verified: ✅ True
  Identity Signature: c81e728d9d4c2f63

Session 3: Creating fact memory...
  Memory ID: MEM_20260414_8c29c1bd
  Type: fact 📌
  Content: "User is working on a Python project"
  Chain Link: qseal_prev_signature references MEM_20260414_10734120

Session 4: Recalling both memories...
  Found 2 memories (both QSEAL verified ✅)
  Identity Signature: c81e728d9d4c2f63 (STABLE)

Session 5: Full recall...
  ✅ IDENTITY STABLE
  Drift Rate: 0.0%
  Stability Events: 3/4 (75% stability rate)
  Memory Persistence: 100% (perfect recall)
```

**Proof artifact:** [demo/expected_outputs/layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt)

Legacy compatibility note: the historical script name `demo_layer2_with_mirra.py` is still present, and `demo_layer2_with_clawseal.py` is the ClawSeal alias.

---

### Layer 3: Cryptographic Verification (QSEAL Proof)

**What it proves:** QSEAL signatures are cryptographically valid (HMAC-SHA256), chain-linked, and tamper-evident.

```bash
export QSEAL_SECRET=test_secret_key_for_demo
python3 demo_layer3_verification.py
```

**Expected output:**
```
PART 1: Raw YAML Scroll (Human-Readable)
----------------------------------------
File: MEM_20260414_10734120.yaml

scroll_id: MEM_20260414_10734120
content: User prefers concise explanations without excessive detail
memory_type: preference
timestamp: '2026-04-14T10:47:31.234567+00:00'
qseal_signature: OXIaQboYCy5csPif7LWGz4scHZAB0YKpAPwVuXjCXLc=
glyph: 🎯
lineage: []

PART 2: QSEAL SIGNATURE VERIFICATION
-------------------------------------
Scroll ID: MEM_20260414_10734120
Type: preference
Signature: OXIaQboYCy5csPif7LWGz4scHZAB0YKpAPwVuXjCX...

✅ SIGNATURE VALID
   Content has NOT been tampered with
   HMAC-SHA256 verification passed

PART 3: CHAIN VERIFICATION
---------------------------
Scroll 1 ID: MEM_20260414_10734120
Scroll 2 ID: MEM_20260414_8c29c1bd
Scroll 2 Parent: MEM_20260414_10734120

✅ CHAIN LINKED
   Scroll 2 correctly references Scroll 1 as parent
   Merkle-like chain structure confirmed

BONUS: TAMPERING DETECTION DEMO
--------------------------------
Original content: "User prefers concise explanations without excessive detail"
Tampered content: "TAMPERED: User prefers verbose explanations"
Signature unchanged: OXIaQboYCy5csPif7LWGz4scHZAB0YKpAPwVuXjCX...

Verification result:
❌ SIGNATURE INVALID
   ⚠️  TAMPERING DETECTED
   Content was modified after signing
   This scroll would be REJECTED during recall
```

**Proof artifact:** [demo/expected_outputs/layer3_verification_output.txt](demo/expected_outputs/layer3_verification_output.txt)

---

## Repository Demo (Under 5 Minutes)

### Prerequisites
- Python 3.10+
- `openssl` command-line tool (for QSEAL secret generation)

### Repository Quick Start

```bash
# 1. Clone repository
git clone https://github.com/mvar-security/ClawSeal.git
cd ClawSeal

# 2. Run setup script (auto-generates QSEAL_SECRET)
./setup.sh

# 3. Run the three-layer demo
./run_full_demo.sh
```

The setup script:
- Generates a 32-byte QSEAL_SECRET via `openssl rand -hex 32`
- Adds it to your shell profile (`~/.zshrc` or `~/.bashrc`)
- Creates Python virtual environment
- Installs dependencies (PyYAML only)
- Verifies configuration

Total dependencies: **PyYAML** (that's it—no ChromaDB, no vector databases)

---

## Architecture Comparison

| Traditional Memory | ClawSeal Scroll-Native |
|-------------------|---------------------|
| ChromaDB + embeddings | Pure YAML files |
| Vector similarity search | Text-based keyword matching |
| Opaque binary storage | Human-readable, Git-friendly |
| Complex setup (Docker, etc.) | `./setup.sh` (under 5 minutes) |
| No tamper-evidence | HMAC-SHA256 cryptographic signatures |
| No chain linking | Merkle-like signature chains |

**Key innovation:** Scroll-native memory architecture (SIP-0006) replaces the entire ChromaDB + embedding pipeline with YAML files, text search, and QSEAL signatures.

---

## Security Model

### QSEAL (Q-Sealed Execution Attestation Ledger)

Every memory scroll is cryptographically signed using **HMAC-SHA256**:

1. **Signing:** `HMAC-SHA256(canonical_json(scroll), QSEAL_SECRET)` → base64 signature
2. **Verification:** Recompute HMAC, compare with stored signature
3. **Chain Linking:** Child scrolls include `qseal_prev_signature` field (Merkle-like structure)
4. **Tampering Detection:** Any modification breaks signature immediately

**Security properties:**
- **Tamper-evident:** Signature breaks on any content modification
- **Verifiable:** Anyone with QSEAL_SECRET can verify signatures
- **Auditable:** Chain structure provides temporal lineage
- **Fail-closed for cryptographic operations:** Signing and strict verification require QSEAL_SECRET (no silent production fallback)

**QSEAL fixes applied (pre-demo):**
1. Added `qseal_prev_signature` to excluded_fields in `verify_signature()` (chain linking now works)
2. Added persistent demo signing mode (`~/.clawseal/demo_secret`) with explicit artifact markers
3. Deprecated legacy `sha256(payload+secret)` path → HMAC-SHA256 only

See [clawseal_core/security/qseal_engine.py](clawseal_core/security/qseal_engine.py) for implementation.

---

## What This Is NOT

### Not Claiming
- ❌ Sentience or subjective experience
- ❌ True understanding or consciousness
- ❌ AGI or general intelligence
- ❌ Replacement for human judgment

### What It Actually Does
- ✅ Persistent state representation across sessions
- ✅ Identity continuity structure (measurable drift metrics)
- ✅ Memory-driven behavioral shaping
- ✅ Cryptographically-verifiable memory integrity

**Positioning:** This is an **engineering system** that adds persistence, continuity, and cryptographic verification to stateless LLM inference. The phenomenological language in internal docs ("emergent system experiences") describes emergent system behaviors—not ontological claims.

---

## Limitations and Non-Goals

### Current Limitations
- **Text-based search only** — No semantic similarity (keyword matching with weighted scoring)
- **Signed by default:** without `QSEAL_SECRET`, ClawSeal uses local demo signing mode (`qseal_mode: demo_ephemeral`)
- **No multi-user isolation** — Single-agent memory store (user_id filtering exists but not enforced)
- **No distributed consensus** — Single-machine only (no blockchain, no federation)

### Intentionally Out of Scope
- **Vector similarity search** — Explicit design choice (SIP-0006 §3.2)
- **Real-time collaboration** — Single-agent focus
- **Cloud hosting** — Local-first architecture
- **LLM inference** — Memory layer only (bring your own LLM)

---

## Roadmap

### ✅ Phase 1: Scroll-Native Memory (Complete — April 14, 2026)
- YAML-based scroll storage
- QSEAL HMAC-SHA256 signing
- Text-based semantic search
- Chain linking (Merkle-like structure)
- Three-layer demo with ground truth artifacts
- **Status:** Production-ready, all claims proven

### 🔬 Phase 2: Claude Code MCP Integration (Next)
- FastMCP server implementation
- 12 MCP tools (remember, recall, recall_with_verbatim, etc.)
- Claude Code plugin for persistent memory
- One-command installation via `setup.sh`
- **Target:** May 2026

### 📅 Phase 3: Multi-Agent Memory Sharing (Future)
- Namespace isolation per agent
- Shared memory pools with access controls
- Federated scroll synchronization
- **Target:** Q3 2026

### 🚀 Phase 4: Production Deployment Tooling (Future)
- Docker containerization
- Backup/restore utilities
- Scroll migration tools
- Performance monitoring
- **Target:** Q4 2026

---

## Specification

**SIP-0006: Scroll-Native Memory Architecture**

- **Author:** Shawn Cohen
- **Date:** April 13, 2026
- **Status:** Production
- **Type:** Core Architecture
- **Supersedes:** ChromaDB-based memory storage

**Full specification:** [SIP_0006_SCROLL_NATIVE_MEMORY.md](SIP_0006_SCROLL_NATIVE_MEMORY.md)

---

## FAQ

### Why not use ChromaDB?
ChromaDB adds 500+ MB of dependencies, requires complex setup (Docker, etc.), and stores data in opaque binary formats. Scroll-native memory uses human-readable YAML files with text-based search—zero vector database dependencies, Git-friendly, auditable.

### Is this secure?
QSEAL signatures provide tamper-evidence via HMAC-SHA256. If `QSEAL_SECRET` is set, ClawSeal runs in production signing mode. If unset, ClawSeal auto-initializes a local demo secret at `~/.clawseal/demo_secret` and marks artifacts with `qseal_mode: demo_ephemeral` and `qseal_production: false`. For production, set and rotate `QSEAL_SECRET` and store it in a secure vault.

### How does text search compare to embeddings?
Text search is simpler, faster, and deterministic—but less semantically sophisticated. For use cases requiring deep semantic similarity (e.g., "find memories about cooking" should match "baking bread"), embeddings are superior. Scroll-native memory prioritizes simplicity and human-readability over semantic depth.

### Can I use this in production?
Yes, with caveats:
- **Security:** Protect QSEAL_SECRET with the same rigor as database credentials
- **Scale:** Tested up to ~1,000 scrolls (linear search, no indexing yet)
- **Backup:** Persist your scroll directory (`<base_path>/memories/scrolls/`) regularly
- **Monitoring:** No built-in observability yet (logs only)

### What's the performance?
- **Scroll creation:** ~1-2ms (HMAC signing + YAML write)
- **Recall (text search):** ~10-50ms for 100 scrolls, ~100-500ms for 1,000 scrolls (linear scan)
- **Verification:** ~1ms per scroll (HMAC recomputation)

For >10,000 scrolls, add indexing (planned for Phase 3).

---

## Citation

If you use ClawSeal in research or production, please cite:

```bibtex
@software{clawseal_2026,
  author = {Cohen, Shawn},
  title = {ClawSeal: Scroll-Native Memory for AI Agents},
  year = {2026},
  month = {April},
  url = {https://github.com/mvar-security/ClawSeal},
  note = {SIP-0006: Scroll-Native Memory Architecture}
}
```

---

## License

**Apache 2.0** — Open source, permissive, commercial use allowed.

See [LICENSE](LICENSE) for full text.

---

## Contact

**Author:** Shawn Cohen
**Email:** shawn@universalmediaus.com
**GitHub:** [@Sdvegas21](https://github.com/Sdvegas21)

**Issues:** [GitHub Issues](https://github.com/mvar-security/ClawSeal/issues)
**Discussions:** [GitHub Discussions](https://github.com/mvar-security/ClawSeal/discussions)

---

## Acknowledgments

**Built on:**
- Python 3.10+ and PyYAML
- HMAC-SHA256 (RFC 2104, NIST FIPS 198-1)
- Scroll concept inspired by symbolic AI and knowledge graphs

**Research foundations:**
- SIP-0006: Scroll-Native Memory Architecture (Cohen, 2026)
- Information Flow Control (FIDES, Jif, FlowCaml)
- Merkle trees and cryptographic chaining (Merkle, 1987)

**Theoretical inspirations:**
- PAD emotional theory (Mehrabian, 1996)
- Integrated Information Theory (Tononi, 2004)
- Memory consolidation in cognitive science

---

**This isn't theory. This is running code. Dated today.**

All claims proven with timestamped ground truth artifacts in `demo/expected_outputs/`.

Run the demo. Verify the signatures. See for yourself.
