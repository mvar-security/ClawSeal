# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

---

## Reporting a Vulnerability

**We take security seriously.** If you discover a security vulnerability in ClawSeal, please report it responsibly.

### Responsible Disclosure Process

1. **DO NOT** open a public GitHub issue for security vulnerabilities
2. Email: **security@mvar.io** with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)
3. **Response timeline:**
   - Acknowledgment within 48 hours
   - Initial assessment within 7 days
   - Fix timeline provided within 14 days
4. **Coordinated disclosure:**
   - We will coordinate a disclosure timeline with you
   - Public disclosure only after a patch is available
   - Credit given to reporter (if desired)

### Security Contact

- **Primary:** security@mvar.io
- **Backup:** shawn@universalmediaus.com
- **PGP Key:** Available on request

---

## Security Model

### QSEAL_SECRET Protection

**CRITICAL:** The security of ClawSeal depends entirely on keeping your `QSEAL_SECRET` secure.

#### What QSEAL_SECRET Protects

- **Tamper-evidence:** Anyone modifying a scroll without the secret will break the signature
- **Authenticity:** Only someone with the secret can create valid scrolls
- **Chain integrity:** Forged scrolls cannot be inserted into the chain undetected

#### What QSEAL_SECRET Does NOT Protect

- **Confidentiality:** Scroll content is NOT encrypted (YAML files are plaintext)
- **Access control:** Anyone with file system access can read scrolls
- **Forgery prevention:** Anyone WITH the secret can forge signatures

**Key insight:** QSEAL provides tamper-evidence, not encryption. Treat `QSEAL_SECRET` like a database password.

---

## Best Practices

### QSEAL_SECRET Management

#### DO:
- ✅ Generate with `openssl rand -hex 32` (256-bit entropy)
- ✅ Store in environment variables only (never commit to git)
- ✅ Rotate secrets regularly (monthly recommended)
- ✅ Use different secrets for dev/staging/prod environments
- ✅ Store in secure vaults (HashiCorp Vault, AWS Secrets Manager, etc.)

#### DO NOT:
- ❌ Use `test_secret_key_for_demo` in production (DEMO ONLY)
- ❌ Commit secrets to git (even in private repos)
- ❌ Store secrets in shell history
- ❌ Share secrets via email, Slack, or other unencrypted channels
- ❌ Hardcode secrets in source code

### File System Security

Since scroll content is stored in plaintext YAML:

- Restrict file system permissions to application user only (`chmod 600`)
- Use full-disk encryption (FileVault, LUKS, BitLocker)
- Back up scrolls to encrypted storage only
- Never expose `data/` directory via web server

### Secret Rotation

When rotating `QSEAL_SECRET`:

1. **Stop accepting new writes** with old secret
2. **Re-sign all existing scrolls** with new secret:
   ```bash
   export NEW_SECRET=$(openssl rand -hex 32)
   python3 scripts/rotate_secret.py --old "$QSEAL_SECRET" --new "$NEW_SECRET"
   ```
3. **Verify all signatures** with new secret
4. **Update environment variable** everywhere
5. **Archive old secret** securely (for forensics)

**Warning:** Rotation is disruptive. Plan for downtime.

---

## Known Security Limitations

### 1. Plaintext Storage

**Issue:** Scroll content is stored in plaintext YAML files.

**Impact:** Anyone with file system access can read all memories.

**Mitigation:** Use full-disk encryption + restrict file permissions.

**Future:** Encryption-at-rest planned for v2.0 (Phase 4).

### 2. Single Secret for All Users

**Issue:** One `QSEAL_SECRET` signs all scrolls (no per-user secrets).

**Impact:** Compromised secret affects all users/agents.

**Mitigation:** Use separate deployment per user (isolated secrets).

**Future:** Per-user secret derivation planned for v1.2 (Phase 3).

### 3. No Built-In Access Control

**Issue:** No authentication/authorization layer.

**Impact:** Anyone who can run the API can access all memories.

**Mitigation:** Deploy behind authenticated API gateway.

**Future:** API key authentication planned for v1.1 (Phase 2).

### 4. Linear Search Performance

**Issue:** Text search is O(n) — all scrolls must be scanned.

**Impact:** Timing attacks could leak scroll count.

**Mitigation:** Constant-time search (always scan full dataset).

**Future:** Indexed search with constant-time padding planned for v1.2.

### 5. No Rate Limiting

**Issue:** No built-in rate limiting for memory operations.

**Impact:** DoS via excessive `remember()` calls (disk exhaustion).

**Mitigation:** Deploy behind rate-limiting reverse proxy.

**Future:** Built-in rate limiting planned for v2.0.

---

## Demo Security Warning

### NEVER Use Demo Secret in Production

**Demo secret:** `test_secret_key_for_demo`

**Used in:**
- `demo/expected_outputs/` ground truth artifacts
- `demo_layer2_with_mirra.py`
- `demo_layer3_verification.py`
- `run_full_demo.sh`

**This secret is PUBLIC.** Anyone can:
- Forge signatures for demo scrolls
- Create fake demo artifacts
- Impersonate demo agent

**For production:**
```bash
# Generate NEW secret
export QSEAL_SECRET=$(openssl rand -hex 32)

# Add to shell profile
echo "export QSEAL_SECRET=\"$QSEAL_SECRET\"" >> ~/.zshrc

# NEVER commit this value to git
```

---

## Attack Surface Analysis

### What Attackers Can Learn from Public Repo

**Public knows:**
- Scroll YAML structure (visible in demo outputs)
- QSEAL signing uses HMAC-SHA256
- Chain linking via `qseal_prev_signature`
- Text search uses keyword matching
- Memory types: fact, preference, insight, decision, general

**Public does NOT know:**
- Your production `QSEAL_SECRET`
- Your scroll content (stored locally, not in repo)
- Your deployment architecture
- Your user data

### Threat Scenarios

#### Scenario 1: Compromised QSEAL_SECRET

**Attack:** Attacker obtains `QSEAL_SECRET` (e.g., via environment leak)

**Impact:**
- ✅ Can forge valid scrolls (full write access)
- ✅ Can create fake memories
- ✅ Can impersonate legitimate agent
- ❌ Cannot read existing scrolls (plaintext anyway)

**Mitigation:** Rotate secret immediately, audit all scrolls created during exposure window.

#### Scenario 2: File System Access

**Attack:** Attacker gains read access to `data/` directory

**Impact:**
- ✅ Can read all scroll content (plaintext YAML)
- ❌ Cannot forge signatures (no secret)
- ❌ Cannot modify without detection (signatures break)

**Mitigation:** Full-disk encryption + strict file permissions.

#### Scenario 3: Timing Attack

**Attack:** Attacker measures search response times to infer scroll count

**Impact:**
- ✅ Can estimate number of scrolls (O(n) search)
- ❌ Cannot read content
- ❌ Cannot forge signatures

**Mitigation:** Constant-time search (always scan full dataset).

#### Scenario 4: Replay Attack

**Attack:** Attacker copies valid scroll and re-submits it

**Impact:**
- ✅ Can create duplicate memories
- ❌ Duplicate will have different timestamp (detectable)
- ❌ Cannot modify content (signature breaks)

**Mitigation:** Timestamp validation + deduplication logic.

---

## Cryptographic Guarantees

### What QSEAL Guarantees

**HMAC-SHA256 provides:**
- ✅ **Integrity:** Any modification breaks signature
- ✅ **Authenticity:** Only holder of secret can create valid signatures
- ✅ **Binding:** Signature is cryptographically bound to content

**HMAC-SHA256 does NOT provide:**
- ❌ **Confidentiality:** Content is plaintext (use encryption separately)
- ❌ **Non-repudiation:** Symmetric key (anyone with secret can sign)
- ❌ **Forward secrecy:** Old scrolls remain valid after secret rotation

### HMAC-SHA256 Security Properties

**Algorithm:** NIST FIPS 198-1 approved

**Key size:** 256 bits (recommended: 32-byte hex = 64 characters)

**Output size:** 256 bits (32 bytes, base64-encoded to 44 characters)

**Collision resistance:** 2^128 operations (SHA-256 property)

**Preimage resistance:** 2^256 operations (SHA-256 property)

**Security assumption:** Attacker does NOT have `QSEAL_SECRET`

---

## Compliance and Auditing

### Security Audits

**v1.0.0 (April 14, 2026):**
- Internal security review by Codex (OpenAI)
- Three critical fixes applied pre-release
- All 28 claims verified with ground truth artifacts

**Next audit:** Planned for v1.1.0 (external third-party)

### Compliance Considerations

**GDPR (EU):**
- Scroll content may contain personal data
- Users have right to erasure (delete scrolls)
- Plaintext storage = data protection concern

**CCPA (California):**
- Same considerations as GDPR

**HIPAA (Healthcare):**
- ❌ Not HIPAA-compliant (no encryption-at-rest)
- Do NOT use for protected health information (PHI)

**SOC 2:**
- ❌ Not SOC 2 compliant (no access controls, no audit logs)
- Enterprise version (v2.0+) will target SOC 2

---

## Security Roadmap

### v1.1.0 (Phase 2 — May 2026)
- API key authentication
- Rate limiting (per-user quotas)
- Audit logging (all memory operations)

### v1.2.0 (Phase 3 — Q3 2026)
- Per-user secret derivation
- Indexed search with constant-time padding
- Deduplication logic (replay attack prevention)

### v2.0.0 (Phase 4 — Q4 2026)
- Encryption-at-rest (AES-256-GCM)
- SOC 2 Type II compliance
- External security audit (third-party)
- Bug bounty program launch

---

## Security Contact

**Primary:** security@mvar.io
**Backup:** shawn@universalmediaus.com

**Response SLA:**
- Acknowledgment: 48 hours
- Initial assessment: 7 days
- Fix timeline: 14 days

**Severity Levels:**
- **Critical:** `QSEAL_SECRET` leak, signature forgery, data breach
- **High:** Authentication bypass, privilege escalation
- **Medium:** DoS, timing attacks, information disclosure
- **Low:** Minor bugs, documentation errors

---

**Last Updated:** April 14, 2026
**Next Review:** May 1, 2026
