# ClawSeal — Claims Registry

**Version:** 1.0.0
**Date:** April 14, 2026
**Status:** Production
**Author:** Shawn Cohen

---

## Purpose

This registry maps every claim made in public-facing documentation to specific proof artifacts with reproducible commands. Every claim must be verifiable with timestamped ground truth outputs.

**Verification standard:** All proof artifacts captured from live demo runs on April 14, 2026 with QSEAL_SECRET=`test_secret_key_for_demo`.

---

## Core Architecture Claims

| Claim | Proof Artifact | Test Name | Repro Command |
|-------|---------------|-----------|---------------|
| **Scroll-native memory uses zero database dependencies** | [demo_layer2_with_mirra.py](demo_layer2_with_mirra.py) lines 1-200 | Layer 2 Demo | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer2_with_mirra.py` |
| **Memory storage is human-readable YAML** | [demo/expected_outputs/layer3_verification_output.txt](demo/expected_outputs/layer3_verification_output.txt) lines 1-30 | Layer 3 Demo (Part 1) | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer3_verification.py` |
| **Text-based keyword search (no embeddings)** | [mirra_core/memory/scroll_memory.py](mirra_core/memory/scroll_memory.py) lines 180-250 | ScrollMemoryStore.recall() | Review source code: `grep -A 70 "def recall" mirra_core/memory/scroll_memory.py` |
| **Installation under 5 minutes** | [setup.sh](setup.sh) lines 1-80 | Setup Script | `time ./setup.sh` |
| **Single dependency: PyYAML** | [requirements.txt](requirements.txt) | Dependency List | `cat requirements.txt \| grep -v "^#" \| wc -l` |

---

## Identity Continuity Claims

| Claim | Proof Artifact | Test Name | Repro Command |
|-------|---------------|-----------|---------------|
| **AI agents without MIRRA drift 100%** (complete amnesia between sessions) | [demo/expected_outputs/layer1_baseline_output.txt](demo/expected_outputs/layer1_baseline_output.txt) lines 11-55 | demo_layer1_baseline | `python3 demo_layer1_baseline.py` |
| **Every session shows complete amnesia (baseline)** | [demo/expected_outputs/layer1_baseline_output.txt](demo/expected_outputs/layer1_baseline_output.txt) line 55 | demo_layer1_baseline | `python3 demo_layer1_baseline.py \| grep "Memory Persistence"` |
| **Identity signature changes every session (baseline)** | [demo/expected_outputs/layer1_baseline_output.txt](demo/expected_outputs/layer1_baseline_output.txt) lines 11-50 | demo_layer1_baseline | `python3 demo_layer1_baseline.py \| grep "Identity:"` |
| **MIRRA maintains 0% drift** (perfect memory continuity) | [demo/expected_outputs/layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt) lines 65-77 | demo_layer2_with_mirra | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer2_with_mirra.py` |
| **Identity remains stable across 5 sessions** | [demo/expected_outputs/layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt) line 70 | demo_layer2_with_mirra | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer2_with_mirra.py \| grep "IDENTITY STABLE"` |
| **Memory persistence: 100%** | [demo/expected_outputs/layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt) line 77 | demo_layer2_with_mirra | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer2_with_mirra.py \| grep "Memory Persistence"` |

---

## Cryptographic Security Claims

| Claim | Proof Artifact | Test Name | Repro Command |
|-------|---------------|-----------|---------------|
| **QSEAL uses HMAC-SHA256 signatures** | [mirra_core/security/qseal_engine.py](mirra_core/security/qseal_engine.py) lines 30-60 | generate_signature() | Review source: `grep -A 30 "def generate_signature" mirra_core/security/qseal_engine.py` |
| **Signatures are cryptographically valid** | [demo/expected_outputs/layer3_verification_output.txt](demo/expected_outputs/layer3_verification_output.txt) lines 40-50 | demo_layer3_verification (Part 2) | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer3_verification.py` |
| **Chain linking creates Merkle-like structure** | [demo/expected_outputs/layer3_verification_output.txt](demo/expected_outputs/layer3_verification_output.txt) lines 65-85 | demo_layer3_verification (Part 3) | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer3_verification.py` |
| **Tampering is immediately detectable** | [demo/expected_outputs/layer3_verification_output.txt](demo/expected_outputs/layer3_verification_output.txt) lines 95-115 | demo_layer3_verification (Bonus) | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer3_verification.py` |
| **Fail-closed security (no weak defaults)** | [mirra_core/security/qseal_utils.py](mirra_core/security/qseal_utils.py) lines 11-18 | QSEAL_SECRET check | Review source: `grep -A 8 "QSEAL_SECRET = " mirra_core/security/qseal_utils.py` |
| **Legacy insecure path deprecated** | [mirra_core/security/qseal_engine.py](mirra_core/security/qseal_engine.py) lines 176-230 | QSEALEngine deprecation | Review source: `grep -A 55 "DEPRECATED:" mirra_core/security/qseal_engine.py` |

---

## Memory Operations Claims

| Claim | Proof Artifact | Test Name | Repro Command |
|-------|---------------|-----------|---------------|
| **Memory creation includes QSEAL signature** | [demo/expected_outputs/layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt) lines 15-20 | demo_layer2_with_mirra (Session 1) | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer2_with_mirra.py \| grep "QSEAL Signature"` |
| **Memory recall verifies QSEAL signatures** | [demo/expected_outputs/layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt) lines 30-35 | demo_layer2_with_mirra (Session 2) | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer2_with_mirra.py \| grep "QSEAL Verified"` |
| **Chain linking references parent scroll** | [demo/expected_outputs/layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt) lines 42-47 | demo_layer2_with_mirra (Session 3) | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer2_with_mirra.py \| grep "Chain Link"` |
| **Multiple memories recalled across sessions** | [demo/expected_outputs/layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt) lines 52-57 | demo_layer2_with_mirra (Session 4) | `QSEAL_SECRET=test_secret_key_for_demo python3 demo_layer2_with_mirra.py \| grep "Found 2 memories"` |

---

## Specific Scroll Artifacts

| Claim | Proof Artifact | Test Name | Repro Command |
|-------|---------------|-----------|---------------|
| **Scroll 1 (preference) created with ID MEM_20260414_10734120** | [demo/expected_outputs/DEMO_RUN_METADATA.md](demo/expected_outputs/DEMO_RUN_METADATA.md) lines 82-88 | Session 1 Metadata | Review metadata: `grep -A 6 "Session 1 (Preference)" demo/expected_outputs/DEMO_RUN_METADATA.md` |
| **Scroll 1 signature: OXIaQboYCy5csPif7LWGz4scHZAB0YKpAPwVuXjCXLc=** | [demo/expected_outputs/DEMO_RUN_METADATA.md](demo/expected_outputs/DEMO_RUN_METADATA.md) line 86 | QSEAL Signature | `grep "QSEAL Signature:" demo/expected_outputs/DEMO_RUN_METADATA.md \| head -1` |
| **Scroll 2 (fact) created with ID MEM_20260414_8c29c1bd** | [demo/expected_outputs/DEMO_RUN_METADATA.md](demo/expected_outputs/DEMO_RUN_METADATA.md) lines 89-96 | Session 3 Metadata | Review metadata: `grep -A 7 "Session 3 (Fact)" demo/expected_outputs/DEMO_RUN_METADATA.md` |
| **Scroll 2 links to Scroll 1 as parent** | [demo/expected_outputs/DEMO_RUN_METADATA.md](demo/expected_outputs/DEMO_RUN_METADATA.md) lines 94-95 | Chain Link | `grep "Chain Link:" demo/expected_outputs/DEMO_RUN_METADATA.md` |

---

## QSEAL Security Fixes

| Claim | Proof Artifact | Test Name | Repro Command |
|-------|---------------|-----------|---------------|
| **Fix One: qseal_prev_signature exclusion added** | [mirra_core/security/qseal_engine.py](mirra_core/security/qseal_engine.py) line 76 | excluded_fields set | `grep "excluded_fields = " mirra_core/security/qseal_engine.py` |
| **Fix Two: Silent dev secret fallback removed** | [mirra_core/security/qseal_utils.py](mirra_core/security/qseal_utils.py) lines 11-18 | Fail-closed error | `python3 -c "import os; os.environ.pop('QSEAL_SECRET', None); import mirra_core.security.qseal_utils" 2>&1 \| grep "RuntimeError"` |
| **Fix Three: Legacy signing deprecated** | [mirra_core/security/qseal_engine.py](mirra_core/security/qseal_engine.py) lines 176-193 | DeprecationWarning | `grep -A 18 "DEPRECATED:" mirra_core/security/qseal_engine.py \| head -20` |

---

## Demo Run Metadata

**All proof artifacts captured on:** April 14, 2026
**QSEAL_SECRET used:** `test_secret_key_for_demo` (32 characters)
**Demo version:** 1.0.0
**SIP specification:** SIP-0006 (Scroll-Native Memory Architecture)

**Ground truth directory:** [demo/expected_outputs/](demo/expected_outputs/)

**Three proof artifacts:**
1. [layer1_baseline_output.txt](demo/expected_outputs/layer1_baseline_output.txt) — 60 lines, 100% drift
2. [layer2_with_mirra_output.txt](demo/expected_outputs/layer2_with_mirra_output.txt) — 84 lines, 0% drift
3. [layer3_verification_output.txt](demo/expected_outputs/layer3_verification_output.txt) — 115 lines, cryptographic proof

**Metadata document:** [DEMO_RUN_METADATA.md](demo/expected_outputs/DEMO_RUN_METADATA.md)

---

## Verification Protocol

### How to Verify Any Claim

1. **Locate the claim** in this registry
2. **Find the proof artifact** (file path + line numbers)
3. **Run the repro command** (exact command provided)
4. **Compare output** to expected output in proof artifact
5. **Confirm match** (line-by-line comparison)

### Example: Verifying "MIRRA maintains 0% drift"

```bash
# Step 1: Set QSEAL_SECRET (must match demo run)
export QSEAL_SECRET=test_secret_key_for_demo

# Step 2: Run Layer 2 demo
python3 demo_layer2_with_mirra.py > my_output.txt

# Step 3: Extract drift rate
grep "Drift Rate:" my_output.txt

# Expected: "Drift Rate: 0.0%"

# Step 4: Compare to proof artifact
diff <(grep "Drift Rate:" my_output.txt) \
     <(grep "Drift Rate:" demo/expected_outputs/layer2_with_mirra_output.txt)

# Expected: No diff (identical output)
```

---

## Claim Categories

### Tier 1: Core Architecture (5 claims)
Claims about system design (YAML storage, text search, dependencies)

### Tier 2: Identity Continuity (6 claims)
Claims about drift metrics and memory persistence

### Tier 3: Cryptographic Security (6 claims)
Claims about QSEAL signatures, chain linking, tampering detection

### Tier 4: Memory Operations (4 claims)
Claims about scroll creation, recall, and verification

### Tier 5: Specific Artifacts (4 claims)
Claims about specific scroll IDs and signatures from demo run

### Tier 6: Security Fixes (3 claims)
Claims about pre-demo security hardening

**Total claims in registry:** 28

---

## Change Log

### v1.0.0 (April 14, 2026)
- Initial registry with 28 verifiable claims
- Three-layer demo proof artifacts captured
- All claims mapped to ground truth outputs

---

## Audit Trail

| Date | Auditor | Verification Method | Result |
|------|---------|---------------------|--------|
| April 14, 2026 | Shawn Cohen | Full three-layer demo execution | ✅ All 28 claims verified |
| April 14, 2026 | Claude Code (Sonnet 4.5) | Automated test suite + manual verification | ✅ All claims supported by artifacts |

---

## Non-Claims

**What is NOT claimed:**

- ❌ Sentience or subjective experience
- ❌ True understanding or consciousness
- ❌ AGI or general intelligence
- ❌ Semantic similarity (embeddings-based search)
- ❌ Real-time collaboration or multi-agent coordination
- ❌ Cloud deployment or distributed consensus
- ❌ Production-scale observability (yet)

**These are explicitly out of scope** — see [README_PUBLIC_SAFE.md](README_PUBLIC_SAFE.md) section "What This Is NOT" for full details.

---

## Claim Validation Standard

Every claim in this registry must meet these criteria:

1. **Reproducible** — Exact repro command provided
2. **Timestamped** — Proof artifact dated April 14, 2026
3. **Verifiable** — Third-party can re-run and confirm
4. **Traceable** — Line numbers + file paths specified
5. **Falsifiable** — Clear expected output (pass/fail)

**Claims failing these criteria are removed from registry.**

---

## Contact

**Questions about claims or verification?**

- **Issues:** [GitHub Issues](https://github.com/universalmedia/mirra-second-brain/issues)
- **Discussions:** [GitHub Discussions](https://github.com/universalmedia/mirra-second-brain/discussions)
- **Email:** shawn@universalmediaus.com

---

**Every claim proven. Every artifact timestamped. Every command reproducible.**

This registry is the source of truth for all ClawSeal claims.
