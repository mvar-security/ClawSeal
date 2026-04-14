# Threat Model

**ClawSeal — Scroll-Native Memory Architecture**

**Version:** 1.0.0
**Date:** April 14, 2026
**Author:** Shawn Cohen

---

## Overview

This document analyzes the security properties and attack surface of ClawSeal v1.0.0. It is based directly on the security analysis in [docs/OPEN_CORE_BOUNDARY.md](docs/OPEN_CORE_BOUNDARY.md) and reflects the current public release scope.

**Key principle:** MIRRA provides **tamper-evidence**, not **confidentiality**. The security model assumes attackers do NOT have your `QSEAL_SECRET`.

---

## Assets

### What We're Protecting

| Asset | Description | Sensitivity |
|-------|-------------|-------------|
| **Scroll Content** | Memory data stored in YAML files | **HIGH** — May contain personal data, preferences, facts |
| **QSEAL_SECRET** | 256-bit secret for HMAC-SHA256 signing | **CRITICAL** — Compromise = full forgery capability |
| **Scroll Signatures** | HMAC-SHA256 signatures on each scroll | **MEDIUM** — Public in demo, sensitive in production |
| **Chain Integrity** | Temporal lineage via `qseal_prev_signature` | **MEDIUM** — Prevents history rewriting |
| **Identity Signatures** | Agent identity fingerprints | **LOW** — Derived from scroll IDs |

---

## Threat Actors

### Attacker Profiles

#### 1. Curious Researcher

**Motivation:** Understand MIRRA architecture, verify claims

**Capabilities:**
- ✅ Access to public GitHub repository
- ✅ Can read SIP-0006 specification
- ✅ Can run demo scripts
- ❌ No access to production deployments
- ❌ No access to production `QSEAL_SECRET`

**Threat level:** **Low** — Not adversarial, learning-focused

#### 2. Malicious Actor (External)

**Motivation:** Steal data, disrupt service, forge memories

**Capabilities:**
- ✅ Access to public repository
- ✅ Knowledge of HMAC-SHA256 internals
- ✅ May attempt timing attacks
- ❌ No access to production `QSEAL_SECRET` (unless leaked)
- ❌ No file system access (unless exploited)

**Threat level:** **Medium** — Adversarial, but limited access

#### 3. Malicious Insider

**Motivation:** Data theft, sabotage, espionage

**Capabilities:**
- ✅ File system access to `data/` directory
- ✅ Access to environment variables (`QSEAL_SECRET` may be exposed)
- ✅ Network access to API (if deployed)
- ✅ May have `git` access to internal repos

**Threat level:** **High** — Full access to deployment environment

#### 4. State-Level Actor

**Motivation:** Espionage, surveillance, data collection

**Capabilities:**
- ✅ All of the above
- ✅ May have access to encrypted backups (coercion, legal orders)
- ✅ May perform side-channel attacks (power analysis, EM leakage)
- ✅ Unlimited compute resources (brute force, precomputation)

**Threat level:** **Critical** — Nation-state resources

---

## Attack Surface

### What Attackers Can Learn from Public Repo

Based on [docs/OPEN_CORE_BOUNDARY.md](docs/OPEN_CORE_BOUNDARY.md) §Security Implications:

#### Public Knows:
- ✅ Scroll YAML structure (visible in `demo/expected_outputs/`)
- ✅ QSEAL signing uses HMAC-SHA256 (documented in `qseal_engine.py`)
- ✅ Chain linking via `qseal_prev_signature` field
- ✅ Text search uses keyword matching with weighted scoring
- ✅ Memory types: fact (📌), preference (🎯), insight (✨), decision (⚖️), general (📝)
- ✅ Demo secret: `test_secret_key_for_demo` (PUBLIC, demo only)

#### Public Does NOT Know:
- ❌ Your production `QSEAL_SECRET`
- ❌ Your scroll content (stored locally, not in repo)
- ❌ Your deployment architecture (ports, reverse proxies, etc.)
- ❌ Your user data (user IDs, preferences, facts)
- ❌ Entry 500 verification logic (proprietary, not in public repo)
- ❌ MVAR security internals (proprietary)

### Attack Vectors

#### Vector 1: QSEAL_SECRET Compromise

**Attack:** Attacker obtains `QSEAL_SECRET` via:
- Environment variable leak (e.g., logged to stdout)
- Shell history (`export QSEAL_SECRET=...`)
- Git commit (accidentally committed `.env` file)
- Server-side request forgery (SSRF) reading `/proc/self/environ`)

**Impact:**
- ✅ **Full forgery capability** — Can create valid signatures for arbitrary content
- ✅ **Impersonation** — Can create scrolls as any user
- ✅ **History rewriting** — Can forge chain links
- ❌ **Cannot read existing scrolls** — Content is plaintext anyway (no encryption)

**Likelihood:** **Medium** (common misconfiguration)

**Mitigation:**
1. Never log environment variables
2. Use `.gitignore` to block `.env` files
3. Store secrets in secure vaults (HashiCorp Vault, AWS Secrets Manager)
4. Rotate `QSEAL_SECRET` regularly (monthly)
5. Monitor for unexpected scroll creation patterns

**Detection:**
- Audit all scrolls created during exposure window
- Check for scrolls with timestamps before/after known legitimate activity
- Verify chain links point to known scrolls

#### Vector 2: File System Access

**Attack:** Attacker gains read access to `data/` directory via:
- Local privilege escalation (LPE)
- Remote code execution (RCE) in web server
- Backup theft (unencrypted backups on cloud storage)
- Physical access to disk

**Impact:**
- ✅ **Full read access** — All scroll content visible (plaintext YAML)
- ❌ **Cannot forge signatures** — No `QSEAL_SECRET`
- ❌ **Cannot modify undetected** — Signature breaks on edit

**Likelihood:** **Low** (requires exploitation)

**Mitigation:**
1. Restrict file permissions (`chmod 600 data/`)
2. Use full-disk encryption (FileVault, LUKS, BitLocker)
3. Encrypt backups before uploading to cloud
4. Never expose `data/` via web server

**Detection:**
- File access logs (if enabled)
- Unexpected reads in audit logs

#### Vector 3: Timing Attack (Scroll Count Inference)

**Attack:** Attacker measures `recall()` response times to infer number of scrolls:
- Send queries and measure latency
- O(n) search means response time ∝ scroll count
- Infer approximate scroll count from timing

**Impact:**
- ✅ **Metadata leakage** — Can estimate number of scrolls
- ❌ **Cannot read content**
- ❌ **Cannot forge signatures**

**Likelihood:** **Low** (requires precise timing, noisy network)

**Mitigation:**
1. Constant-time search (always scan full dataset, even after match found)
2. Add random delay to responses (0-100ms jitter)
3. Rate limiting (prevent mass timing measurements)

**Detection:**
- Monitor for repeated queries from same IP
- Anomaly detection on query patterns

#### Vector 4: Replay Attack

**Attack:** Attacker copies valid scroll and re-submits it:
- Read scroll from `data/` directory (Vector 2)
- Copy YAML file byte-for-byte
- Submit to `remember()` via API

**Impact:**
- ✅ **Duplicate memories** — Same content stored twice
- ❌ **Detectable** — Duplicate will have different timestamp
- ❌ **Cannot modify content** — Signature breaks on edit

**Likelihood:** **Low** (requires file access + API access)

**Mitigation:**
1. Deduplication logic (check for existing scroll with same content)
2. Timestamp validation (reject scrolls with old timestamps)
3. Nonce tracking (reject scrolls seen before)

**Detection:**
- Check for exact duplicate `scroll_id` or `content`
- Alert on multiple scrolls with identical signatures

#### Vector 5: Demo Secret Reuse in Production

**Attack:** Developer uses `test_secret_key_for_demo` in production deployment

**Impact:**
- ✅ **Public secret** — Anyone can forge signatures
- ✅ **Full compromise** — Equivalent to Vector 1 (secret leak)

**Likelihood:** **Medium** (common copy-paste error)

**Mitigation:**
1. Add runtime check: If `QSEAL_SECRET == "test_secret_key_for_demo"`, raise error
2. Documentation warnings (SECURITY.md, README.md, setup.sh)
3. Pre-commit hook to detect demo secret in env files

**Detection:**
- Log `QSEAL_SECRET` hash on startup (not the secret itself)
- Alert if hash matches known demo secret hash

#### Vector 6: Supply Chain Attack

**Attack:** Attacker compromises PyYAML or other dependencies:
- Malicious PyYAML version with backdoor
- Steals `QSEAL_SECRET` from environment
- Exfiltrates scroll content to attacker server

**Impact:**
- ✅ **Full compromise** — Secret + content exfiltration
- ✅ **Undetectable** — Backdoor runs in legitimate dependency

**Likelihood:** **Very Low** (PyYAML is well-maintained, widely used)

**Mitigation:**
1. Pin dependency versions in `requirements.txt`
2. Use `pip-audit` to check for known vulnerabilities
3. Verify package hashes (`pip install --require-hashes`)
4. Monitor PyPI security advisories

**Detection:**
- Network monitoring (unexpected outbound connections)
- Dependency integrity checks (compare hashes)

---

## Trust Boundaries

### Boundary 1: Public Repo ↔ Production Deployment

**Public repo contains:**
- Source code for Scroll-native memory
- QSEAL signing primitives
- Demo scripts with test secret
- SIP-0006 specification

**Production deployment contains:**
- Above, plus:
- Production `QSEAL_SECRET` (user-generated, private)
- User scroll data (plaintext YAML in `data/`)
- Environment-specific configuration

**Threat:** Public disclosure of production `QSEAL_SECRET` or scroll data

**Control:** Never commit `QSEAL_SECRET` or `data/` to git (`.gitignore`)

---

### Boundary 2: File System ↔ Network

**File system contains:**
- Scroll YAML files (plaintext)
- `QSEAL_SECRET` in environment (or vault)

**Network exposes:**
- `remember()` and `recall()` API endpoints
- No direct file access

**Threat:** RCE in web server → file system access

**Control:** Sandboxing, principle of least privilege, input validation

---

### Boundary 3: User Data ↔ Application Logic

**User provides:**
- Memory content (untrusted)
- Queries (untrusted)

**Application processes:**
- Scroll creation with QSEAL signing
- Text search with keyword matching

**Threat:** Injection attacks (e.g., YAML injection, command injection)

**Control:** Input sanitization, use safe YAML library (`yaml.safe_load`)

---

## Security Properties

### What QSEAL Guarantees

Based on HMAC-SHA256 properties:

✅ **Integrity:** Any modification to scroll content breaks the signature
- **Guarantee:** If `verify_signature(scroll) == True`, content is unchanged
- **Assumption:** Attacker does NOT have `QSEAL_SECRET`

✅ **Authenticity:** Only holder of `QSEAL_SECRET` can create valid signatures
- **Guarantee:** Valid signature → created by legitimate agent
- **Assumption:** `QSEAL_SECRET` not leaked

✅ **Binding:** Signature cryptographically bound to content
- **Guarantee:** Cannot reuse signature on different content
- **Assumption:** HMAC collision resistance (2^128 operations)

---

### What QSEAL Does NOT Guarantee

❌ **Confidentiality:** Scroll content is plaintext YAML
- **Implication:** Anyone with file access can read all memories
- **Mitigation:** Use full-disk encryption (separate from QSEAL)

❌ **Non-repudiation:** Symmetric key (anyone with secret can sign)
- **Implication:** Cannot prove who created a specific scroll
- **Note:** For non-repudiation, use asymmetric crypto (Ed25519)

❌ **Forward secrecy:** Old scrolls remain valid after secret rotation
- **Implication:** Compromised old secret → can still verify old scrolls
- **Mitigation:** Re-sign all scrolls with new secret during rotation

❌ **Access control:** No authentication/authorization layer
- **Implication:** Anyone with API access can read/write scrolls
- **Mitigation:** Deploy behind authenticated API gateway

---

## Risk Assessment

| Threat | Likelihood | Impact | Risk | Mitigation Status |
|--------|-----------|--------|------|-------------------|
| **QSEAL_SECRET leak** | Medium | Critical | **High** | ⚠️ Partial (docs, no runtime checks) |
| **File system access** | Low | High | **Medium** | ✅ Complete (encryption, permissions) |
| **Timing attack** | Low | Low | **Low** | ❌ Not implemented (planned v1.2) |
| **Replay attack** | Low | Medium | **Low** | ❌ Not implemented (planned v1.2) |
| **Demo secret reuse** | Medium | Critical | **High** | ⚠️ Partial (docs only, no runtime checks) |
| **Supply chain attack** | Very Low | Critical | **Medium** | ⚠️ Partial (pinned deps, no hash verification) |

---

## Security Assumptions

ClawSeal security depends on these assumptions:

1. **QSEAL_SECRET is secret** — Never leaked, logged, or committed to git
2. **File system is secure** — Full-disk encryption + restricted permissions
3. **Dependencies are trusted** — PyYAML and other deps are not compromised
4. **Deployment is hardened** — API behind authentication, rate limiting, monitoring
5. **Scroll count is not sensitive** — Timing attacks acceptable (for v1.0)

**If any assumption breaks, security degrades.**

---

## Future Security Enhancements

### v1.1.0 (Phase 2 — May 2026)
- API key authentication
- Rate limiting (per-user quotas)
- Audit logging (all memory operations)

### v1.2.0 (Phase 3 — Q3 2026)
- Constant-time search (timing attack mitigation)
- Deduplication logic (replay attack prevention)
- Runtime check for demo secret (prevent production reuse)

### v2.0.0 (Phase 4 — Q4 2026)
- Encryption-at-rest (AES-256-GCM)
- Asymmetric signatures (Ed25519, non-repudiation)
- SOC 2 Type II compliance
- External security audit (third-party)

---

## Responsible Disclosure

Found a vulnerability? See [SECURITY.md](SECURITY.md) for responsible disclosure process.

**Contact:** security@mvar.io

---

**Last Updated:** April 14, 2026
**Next Review:** May 1, 2026
