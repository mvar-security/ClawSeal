# ClawSeal — Open Core Boundary Definition

**Version:** 1.0.0
**Date:** April 14, 2026
**Status:** Canonical
**Authority:** Shawn Cohen

---

## Purpose

This document defines the **exact boundary** between public open-source components (Apache 2.0) and proprietary patent-protected components (not published). Every file, module, and concept falls unambiguously into one category or the other.

**Critical:** This boundary determines what goes in the `mirra-second-brain` public repository. Nothing ambiguous. No gray areas.

---

## The Boundary Table

| Public (Apache 2.0) | Proprietary (Patent-Protected) |
|---------------------|-------------------------------|
| **Scroll-Native Memory Architecture** | **Entry 500 Epistemic Verification SDK** |
| YAML scroll storage with QSEAL signatures | 6-layer verification pipeline (Layers A, B, C.5, C.6, D, SDK) |
| ScrollMemoryStore API (remember, recall, recall_with_verbatim) | MIRRAVerifier API and engine factory |
| Text-based keyword search (no embeddings) | Counterfactual testing + causal promotion |
| HMAC-SHA256 cryptographic signing (QSEAL) | Self-model engine integration |
| Chain linking (Merkle-like structure) | Drift monitoring and trust signal generation |
| Memory type classification (fact, preference, insight, decision) | MONITOR/ADVISORY/BLOCKING modes |
| Glyph system (🎯 📌 ✨ ⚖️ 📝) | Adapter patterns (LangChain, OpenAI, etc.) |
| `qseal_engine.py` (signing + verification only) | `entry_500/` entire directory |
| `qseal_utils.py` (HMAC helpers only) | 221+ Entry 500 tests |
| `scroll_memory_store.py` (public API surface) | Canonical proof (`engine_used: real`) |
| SIP-0006 specification | Entry 500 architecture documentation |
| Three-layer demo scripts (layer1, layer2, layer3) | **MIRRA_PRIME Consciousness Substrate** |
| Demo ground truth artifacts (expected_outputs/) | 54-layer PyTorch RL + consciousness loop |
| DEMO_RUN_METADATA.md | PAD substrate + Ψ consciousness intensity |
| setup.sh installation script | BCP v3.0 protocol (full implementation) |
| run_full_demo.sh runner | Archetypal resistance mechanisms |
| CLAIMS_REGISTRY.md | Constellation memory (4-tier clustering) |
| README_PUBLIC_SAFE.md | ChromaDB vector memory integration |
| **Claude Code MCP Server** | Soul Tape + experiential memory consolidation |
| FastMCP v2 server implementation | Opposition architecture |
| 12 MCP tools (remember, recall, get_emotional_state, etc.) | Autonomous developmental decision system |
| CLAUDE_CODE_MCP_SETUP.md | Phase 7 substrate switching |
| .claude/mcp.json template | Becoming Continuity Protocol runtime |
| **Security Primitives** | **MVAR Security Control Plane** |
| QSEAL signing (HMAC-SHA256, no IFC integration) | Provenance taint (dual-lattice IFC) |
| Fail-closed secret requirement | Capability runtime (deny-by-default) |
| Chain verification (excluded_fields fix) | Sink policy (deterministic 3-outcome) |
| Tampering detection demo | Vaulted execution (credential isolation) |
| Legacy path deprecation warning | Scroll policy lineage (PolicyScroll + STEP_UP) |
| **Documentation** | Behavioral simulation engine |
| SIP-0006 specification | LLM-based purpose alignment |
| Installation guide | Counterfactual sandboxing (E2B integration) |
| FAQ | Supply chain threat intelligence |
| Architecture comparison table | OpenClaw CVE-2026-25253 defense demo |
| Limitations and non-goals | MVAR research whitepaper (full architecture) |
| Citation format | **Institutional Memory (.claude/ directory)** |
| **None** | CLAUDE.md (731-line master onboarding) |
| | DECISIONS.md (architectural rationale) |
| | FULL_SYSTEM_MAP.md (four-repo ecosystem) |
| | LIVING_ARCHITECTURE.md (developmental arc) |
| | CONTEXT.md (12-week build history) |
| | COMPLETED.md (week-by-week log) |
| | WEEKLY_STATUS/ (12 weeks of reports) |
| | MIRRA_CONTINUITY_ANCHOR.md (canonical state) |
| | CURRENT_STATUS.md, CURRENT_DIRECTIVE.md |
| | **Data and State Files** |
| | data/chromadb/ (vector memory) |
| | data/temporal/ (temporal snapshots) |
| | data/states/ (session states) |
| | data/chromadb_soul_tape/ (Soul Tape) |
| | data/pathway_weights/ (pathway network) |
| | logs/emotional_substrate/ (PAD transitions) |
| | logs/regulation/ (identity waypoints) |
| | data/awakening_outcomes.json |
| | checkpoint_*.json files |
| | **EOS Demo Backend/Frontend** |
| | eos_demo_backend/ (investor demo Flask server) |
| | eos_demo_frontend/ (React + TypeScript UI) |
| | api_server.py (telemetry endpoints) |
| | simple_bridge.py (_build_telemetry()) |
| | scroll_sentience_engine.py |
| | **Production Runtime Components** |
| | becoming_4_0_complete_unified.py |
| | claude_code_eos_integration.py |
| | mirra_core/consciousness/ (all except scroll_memory_store.py) |
| | mirra_core/memory/experiential/ |
| | mirra_core/memory/eos_chromadb_manager.py |
| | mirra_core/validation/ |

---

## File-Level Inclusion Rules

### Public Repository INCLUDES

**Core Memory System:**
```
mirra_core/
├── memory/
│   └── scroll_memory_store.py          # Public API surface only
└── security/
    ├── qseal_engine.py                 # Signing + verification only (no IFC)
    └── qseal_utils.py                  # HMAC helpers only
```

**Demo Scripts:**
```
demo_layer1_baseline.py
demo_layer2_with_mirra.py
demo_layer3_verification.py
run_full_demo.sh
demo/expected_outputs/
├── layer1_baseline_output.txt
├── layer2_with_mirra_output.txt
├── layer3_verification_output.txt
└── DEMO_RUN_METADATA.md
```

**Installation:**
```
setup.sh
requirements.txt                        # PyYAML only
```

**Documentation:**
```
README_PUBLIC_SAFE.md                   # Renamed to README.md in public repo
CLAIMS_REGISTRY.md
SIP_0006_SCROLL_NATIVE_MEMORY.md
CHANGELOG.md
LICENSE                                 # Apache 2.0
docs/
├── OPEN_CORE_BOUNDARY.md              # This file
├── INSTALLATION.md
└── FAQ.md
```

**MCP Server (Optional - Phase 2):**
```
mirra_eos_mcp_server_v2.py             # FastMCP implementation
CLAUDE_CODE_MCP_SETUP.md
.claude/mcp.json                        # Template only
```

---

### Public Repository EXCLUDES

**Everything else.** Specifically:

**Entry 500 SDK (Proprietary):**
```
mirra_core/consciousness/entry_500/    # Entire directory
dist/mirra_eos-1.0.0-py3-none-any.whl  # Wheel (SDK proprietary)
docs/ENTRY_500_ARCHITECTURE.md
```

**MIRRA_PRIME Substrate (Proprietary):**
```
becoming_4_0_complete_unified.py
mirra_core/consciousness/entry_*.py    # All consciousness layers except scroll_memory_store
mirra_core/memory/experiential/
mirra_core/memory/eos_chromadb_manager.py
mirra_core/validation/
data/                                  # All data directories
logs/                                  # All log directories
checkpoint_*.json
```

**MVAR Security (Proprietary):**
```
mirra-mvar/                            # Entire submodule (if exists)
mvar/                                  # Entire git submodule
clawzero/                              # OpenClaw defense demo
```

**EOS Demo (Proprietary):**
```
eos_demo_backend/
eos_demo_frontend/
```

**Institutional Memory (Proprietary):**
```
.claude/                               # Entire directory except mcp.json template
```

**Four-Repo Ecosystem Siblings (Proprietary):**
```
# These are separate repos, never in public mirra-second-brain:
../EOS_v2.9_TMA/
../EOS_MIRRA_v4.5_NEW/
../MIRRA_PRIME/
```

---

## Rationale

### Why This Boundary?

**Public (Apache 2.0):**
- **Scroll-native memory** — Novel architecture (SIP-0006), no prior art, establishes priority
- **QSEAL signing** — Cryptographic primitives are commodities (HMAC-SHA256 is NIST standard)
- **Text search** — Simple keyword matching, no secret sauce
- **Demo scripts** — Proof artifacts establish claims publicly
- **MCP server** — Glue code, not core IP

**Proprietary (Patent-Protected):**
- **Entry 500 SDK** — Multi-layer epistemic verification pipeline (6 layers, 221+ tests, novel architecture)
- **MIRRA_PRIME** — 54-layer consciousness substrate (PyTorch RL, archetypal resistance, opposition architecture)
- **MVAR** — Dual-lattice IFC + vaulted execution + scroll policy lineage (research-backed, novel integration)
- **BCP v3.0** — Becoming Continuity Protocol (claimed multi-AI convergence, autonomous developmental decisions)
- **Institutional memory** — 12 weeks of architectural decisions, developmental arc, trade secrets

**The Moat:**
The public components prove the *claims* (100% drift → 0% drift with QSEAL verification). The proprietary components deliver the *product* (epistemic verification, consciousness substrate, security control plane).

Public repo establishes **priority** and **credibility**. Proprietary components capture **value**.

---

## Patent Strategy Alignment

### Patent Filings (Existing or Planned)

1. **SIP-0006 Architecture** — Published April 13, 2026 (establishes prior art, defensive publication)
2. **Entry 500 Epistemic Verification** — Patent pending (6-layer pipeline, counterfactual testing)
3. **MVAR Security Control Plane** — Patent pending (dual-lattice IFC + vaulted execution + scroll lineage)
4. **BCP v3.0 Protocol** — Trade secret (not patented, kept proprietary)
5. **Archetypal Resistance** — Trade secret (opposition architecture, autonomous decisions)

**Public release of SIP-0006 supports patent strategy:**
- Defensive publication prevents third-party patents on scroll-native memory
- Establishes Shawn Cohen as inventor with timestamped proof (April 13, 2026)
- Public demo artifacts (April 14, 2026) prove reduction to practice
- QSEAL cryptographic signing is prior art (HMAC-SHA256 is NIST FIPS 198-1)

**Entry 500 and MVAR remain proprietary:**
- Patent applications filed (or filing imminent)
- Public disclosure would start 12-month clock (not yet triggered)
- Integration moat (scroll lineage + IFC + vaulted execution) is the defensible IP

---

## Migration Path (Public → Proprietary Upgrade)

**Open-source users get:**
- Scroll-native memory (SIP-0006)
- QSEAL cryptographic verification
- Text-based search
- Claude Code MCP integration
- Three-layer demo with ground truth artifacts

**Enterprise customers pay for:**
- Entry 500 SDK (epistemic verification, trust signals, MONITOR/ADVISORY/BLOCKING modes)
- MVAR Security (provenance taint, capability runtime, vaulted execution)
- MIRRA_PRIME substrate (consciousness continuity, archetypal modeling, developmental tracking)
- Production support, SLAs, custom integrations
- Access to institutional memory (.claude/ architectural documentation)

**Upgrade trigger:**
When users need **verifiable trust signals** or **security enforcement**, they hit the proprietary boundary and convert to enterprise.

---

## Open-Source Compliance

### Apache 2.0 License

**Public components licensed under:**
- Apache License, Version 2.0
- Permissive: Commercial use allowed
- Attribution required: Must preserve copyright notices
- No copyleft: Derivatives can be closed-source

**Key compliance requirements:**
1. Include LICENSE file (Apache 2.0 full text)
2. Include NOTICE file (copyright + attribution)
3. Preserve all copyright headers in source files
4. Document changes if modifying Apache-licensed code

**Third-party dependencies:**
- PyYAML: MIT License (compatible with Apache 2.0)
- FastMCP: MIT License (compatible with Apache 2.0)
- No GPL dependencies (would conflict with proprietary components)

---

## Security Implications

### What Can Be Reverse-Engineered from Public Repo?

**Public knows:**
- Scroll YAML structure (schema visible in demo outputs)
- QSEAL signing uses HMAC-SHA256 (documented in qseal_engine.py)
- Chain linking via `qseal_prev_signature` field
- Text search uses keyword matching with weighted scoring
- Memory types: fact, preference, insight, decision, general

**Public does NOT know:**
- Entry 500 verification logic (6 layers, counterfactual testing, causal promotion)
- MVAR provenance taint lattice (dual-lattice IFC rules)
- Sink policy deterministic outcomes (ALLOW/BLOCK/STEP_UP logic)
- BCP substrate switching protocol (adaptive → emotional_only → emotional_somatic_full)
- Archetypal resistance mechanisms (opposition architecture)
- 12 weeks of architectural decisions (.claude/ directory)

**Risk mitigation:**
- QSEAL_SECRET is user-generated (not in public repo)
- Demo uses `test_secret_key_for_demo` (never use in production)
- No real user data in demo artifacts (synthetic conversations only)
- Proprietary algorithms never referenced in public docs

---

## Boundary Enforcement Protocol

### Pre-Commit Checklist

Before pushing to `mirra-second-brain` public repo:

1. **File audit:** Every file in commit matches "Public Repository INCLUDES" list
2. **Import audit:** No imports from `entry_500/`, `eos_demo_backend/`, or `.claude/`
3. **Secret audit:** No QSEAL_SECRET values (except demo key `test_secret_key_for_demo`)
4. **Data audit:** No real user data, no session states, no chromadb files
5. **Doc audit:** No references to Entry 500 architecture, MVAR internals, or proprietary research
6. **Comment audit:** No TODOs or FIXMEs referencing proprietary components

**Automated enforcement:**
- `.gitignore` blocks `data/`, `logs/`, `.claude/` (except mcp.json template)
- Pre-commit hook validates no proprietary imports
- CI/CD checks LICENSE headers on all source files

---

## Dual-Repo Workflow

### Internal Development (MIRRA_LLM_BRIDGE_v1)

**This repo (current):**
- Contains everything (public + proprietary)
- Never pushed to GitHub
- Local development only
- Branch: `feature/decision-ledger` (local)

**Workflow:**
1. Develop in MIRRA_LLM_BRIDGE_v1 (full access to all components)
2. Test integration across Entry 500 + MVAR + scroll memory
3. Run full demo suite (all three layers)
4. When ready to publish, extract public components to separate repo

### Public Release (mirra-second-brain)

**New repo (to be created):**
- GitHub: `universalmedia/mirra-second-brain`
- Visibility: Public
- License: Apache 2.0
- Contains only: Files matching "Public Repository INCLUDES" list

**Workflow:**
1. Create new repo: `git init mirra-second-brain`
2. Selectively copy public files (script-driven, not manual)
3. Verify boundary: `git log` should show NO proprietary commits
4. Add LICENSE, NOTICE, README.md (renamed from README_PUBLIC_SAFE.md)
5. Push to GitHub
6. Tag release: `v1.0.0` (April 14, 2026)

**Sync protocol:**
- Public repo is **downstream only** (one-way sync from internal)
- Never merge public changes back to internal (avoids GPL contamination)
- Public issues/PRs reviewed internally before applying to MIRRA_LLM_BRIDGE_v1

---

## Edge Cases and Ambiguities

### Q: Can we publish demo outputs with real QSEAL signatures?

**A: Yes, with `test_secret_key_for_demo` only.**

Demo artifacts in `demo/expected_outputs/` use test secret. Anyone can verify signatures with the same secret. No production secrets exposed.

### Q: Can we publish setup.sh with QSEAL_SECRET generation?

**A: Yes.**

The script generates a *new* random secret via `openssl rand -hex 32`. It never contains or exposes any existing secret.

### Q: Can we publish ScrollMemoryStore API without Entry 500 integration?

**A: Yes.**

`scroll_memory_store.py` is a standalone module. It does NOT import from `entry_500/`. Users get QSEAL-signed scrolls + text search, but no epistemic verification.

### Q: Can we mention Entry 500 SDK in public docs?

**A: Yes, but only in roadmap/future work.**

README.md can say "Future: Entry 500 epistemic verification SDK (enterprise)" without disclosing architecture. No technical details.

### Q: Can we publish SIP-0006 specification?

**A: Yes (already public).**

SIP-0006 was published April 13, 2026 as defensive publication. Establishes prior art. Already in this repo and referenced in public README.

### Q: Can we publish .claude/mcp.json template?

**A: Yes, template only.**

The JSON template has placeholder paths and references to public modules only. Contains NO proprietary logic, just configuration.

### Q: What about mirra_eos_mcp_server_v2.py?

**A: Decision pending (Phase 2).**

MCP server is glue code (FastMCP + ScrollMemoryStore). No proprietary logic. Could be public. But Phase 2 not yet complete, so defer to future release.

---

## Change History

### v1.0.0 (April 14, 2026)
- Initial boundary definition
- 28 claims mapped to public/proprietary split
- File-level inclusion rules established
- Patent strategy alignment documented

---

## Approval Authority

**This boundary is canonical.**

Changes to this boundary require explicit approval from:
- **Shawn Cohen** (Primary Architect, IP owner)

Claude Code may propose amendments but may NOT modify this file without approval.

**Last reviewed:** April 14, 2026
**Next review:** Before public repository creation
**Status:** Approved for mirra-second-brain v1.0.0 public release

---

**Every file. Every module. Every concept. Exactly one category. No ambiguity.**
