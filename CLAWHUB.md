# ClawHub Submission Guide

This document describes how to submit ClawSeal to the ClawHub registry for one-command installation via `clawhub install clawseal`.

---

## Prerequisites

Before submitting to ClawHub, ensure:

1. ✅ **SKILL.md exists** — ClawHub-compatible skill definition with YAML frontmatter
2. ✅ **Repository is public** — `github.com/clawzero/clawseal` (public visibility required)
3. ✅ **Git tag exists** — `v1.0.0` tag on main branch
4. ✅ **LICENSE file exists** — Apache-2.0 license confirmed
5. ✅ **README.md exists** — Installation and usage documentation
6. ✅ **setup.sh is executable** — `chmod +x setup.sh` confirmed

---

## ClawHub Submission Process

### Step 1: Verify SKILL.md Format

ClawHub requires a `SKILL.md` file in the repository root with this exact structure:

```markdown
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

[Rest of skill documentation...]
```

**Required frontmatter fields:**
- `name` — Skill identifier (lowercase, no spaces)
- `description` — One-line description (under 100 chars)
- `version` — Semantic version (matches git tag)
- `author` — Author name
- `repository` — Full GitHub URL
- `license` — SPDX license identifier
- `required_binaries` — List of binaries that must exist in PATH
- `environment_variables` — List of env vars with descriptions

### Step 2: Push to GitHub

```bash
# From clawseal repository root
git remote add origin https://github.com/clawzero/clawseal.git
git push -u origin main
git push origin v1.0.0
```

**Verify:**
- Repository is public (not private)
- `v1.0.0` tag is visible at `https://github.com/clawzero/clawseal/releases`
- SKILL.md is visible at `https://github.com/clawzero/clawseal/blob/main/SKILL.md`

### Step 3: Submit to ClawHub Registry

```bash
# Install ClawHub CLI (if not already installed)
npm install -g @clawzero/clawhub-cli

# Authenticate with ClawHub
clawhub login

# Submit ClawSeal skill
clawhub publish clawseal \
  --repository https://github.com/clawzero/clawseal \
  --version 1.0.0 \
  --skill-file SKILL.md \
  --category security \
  --tags "memory,cryptography,qseal,agents,yaml"
```

**Publish command parameters:**
- `clawseal` — Skill name (must match `name` in SKILL.md)
- `--repository` — GitHub repository URL
- `--version` — Version to publish (must match git tag and SKILL.md version)
- `--skill-file` — Path to skill definition (default: `SKILL.md`)
- `--category` — ClawHub category (security, productivity, development, data, etc.)
- `--tags` — Comma-separated search tags

### Step 4: Verify Installation

After ClawHub approval (usually within 24 hours), verify:

```bash
# Search for ClawSeal in registry
clawhub search clawseal

# Install ClawSeal via ClawHub
clawhub install clawseal

# Verify installation
clawseal --version
```

Expected output:
```
ClawSeal v1.0.0
Cryptographic memory for AI agents
```

---

## ClawHub Categories

Choose the most appropriate category for ClawSeal:

- **security** ← **RECOMMENDED** (cryptographic verification, tamper-evidence)
- development (developer tools)
- productivity (workflow automation)
- data (data management, storage)

**Rationale for `security`:** ClawSeal's core value proposition is QSEAL cryptographic signatures (HMAC-SHA256) for tamper-evident memory. This is fundamentally a security feature.

---

## ClawHub Tags

Recommended tags for maximum discoverability:

```
memory, cryptography, qseal, agents, yaml, hmac, signatures, identity, continuity, scroll
```

**Tag strategy:**
- `memory` — Core functionality (persistent memory for AI agents)
- `cryptography` — HMAC-SHA256 signatures
- `qseal` — Unique differentiator (Q-Sealed Execution Attestation Ledger)
- `agents` — Target audience (AI agent developers)
- `yaml` — Storage format (human-readable, Git-friendly)
- `hmac` — Cryptographic primitive
- `signatures` — Tamper-evidence mechanism
- `identity` — Identity continuity across sessions
- `continuity` — Zero drift, perfect recall
- `scroll` — Scroll-native memory architecture (SIP-0006)

---

## Post-Submission Checklist

After `clawhub publish` completes:

1. ✅ **Check ClawHub dashboard** — Verify submission status at `https://clawhub.dev/skills/clawseal`
2. ✅ **Monitor approval status** — ClawHub team reviews within 24 hours
3. ✅ **Update README.md** — Add ClawHub installation badge:
   ```markdown
   [![ClawHub](https://img.shields.io/badge/clawhub-clawseal-blue)](https://clawhub.dev/skills/clawseal)
   ```
4. ✅ **Test installation** — Create fresh VM/container, run `clawhub install clawseal`
5. ✅ **Announce on socials** — Twitter, LinkedIn, Hacker News (if desired)

---

## Updating ClawSeal on ClawHub

To publish a new version (e.g., v1.1.0):

```bash
# 1. Update version in SKILL.md
sed -i '' 's/version: 1.0.0/version: 1.1.0/g' SKILL.md

# 2. Commit and tag
git add SKILL.md
git commit -m "Bump version to v1.1.0"
git tag v1.1.0
git push origin main v1.1.0

# 3. Publish to ClawHub
clawhub publish clawseal --version 1.1.0
```

ClawHub will automatically pull the new SKILL.md from the tagged release.

---

## Troubleshooting

### Error: "Skill name already exists"

**Cause:** Another skill named `clawseal` already exists in ClawHub registry.

**Solution:** Choose a different name (e.g., `clawseal-memory`, `qseal-memory`) or contact ClawHub support to claim the name.

### Error: "SKILL.md validation failed"

**Cause:** YAML frontmatter is malformed or missing required fields.

**Solution:** Run local validation:
```bash
clawhub validate SKILL.md
```

Fix any errors reported, then retry `clawhub publish`.

### Error: "Repository not found"

**Cause:** GitHub repository is private or URL is incorrect.

**Solution:**
1. Verify repository is public: `https://github.com/clawzero/clawseal`
2. Check repository exists and is accessible without authentication
3. Ensure SKILL.md `repository` field matches GitHub URL exactly

### Error: "Version mismatch"

**Cause:** `--version` flag doesn't match `version` in SKILL.md or git tag doesn't exist.

**Solution:**
1. Verify git tag exists: `git tag -l v1.0.0`
2. Verify SKILL.md version: `grep 'version:' SKILL.md`
3. Ensure all three match exactly

---

## ClawHub Support

- **Documentation:** https://docs.clawhub.dev
- **Support Email:** support@clawhub.dev
- **Discord:** https://discord.gg/clawhub
- **GitHub Issues:** https://github.com/clawzero/clawhub-cli/issues

---

## Summary: One-Command Submission

```bash
# Complete submission in one command (after prerequisites)
clawhub publish clawseal \
  --repository https://github.com/clawzero/clawseal \
  --version 1.0.0 \
  --category security \
  --tags "memory,cryptography,qseal,agents,yaml"
```

**Expected output:**
```
✅ Validating SKILL.md...
✅ Checking repository access...
✅ Verifying version tag v1.0.0...
✅ Submitting to ClawHub registry...

🎉 ClawSeal v1.0.0 submitted successfully!

Status: Pending Review
Expected approval: Within 24 hours
Install command: clawhub install clawseal

View submission: https://clawhub.dev/skills/clawseal
```

---

**Last updated:** April 14, 2026
**ClawHub CLI version:** 2.1.0
**ClawSeal version:** 1.0.0
