# Contributing to ClawSeal

Thanks for helping improve ClawSeal.

This guide is intentionally practical: how to run it, how to submit changes, and what must not break.

## Scope

This document covers contributions to the OSS-facing Node Runtime under:
- `clawseal/`

If your change touches broader MIRRA subsystems, include that context in your PR.

## Quick Start

```bash
# From repo root
cd clawseal
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python api_server.py
```

In a second terminal:

```bash
curl http://localhost:5002/health
curl -X POST http://localhost:5002/start
curl -X POST http://localhost:5002/process \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello MIRRA"}'
```

Expected: successful JSON responses from all three endpoints.

## Contribution Workflow

1. Fork the repo.
2. Create a branch from `main`.
3. Make a focused change.
4. Run validation (below).
5. Open a PR with clear scope and rationale.

Use branch names like:
- `feat/node-runtime-plugin-xyz`
- `fix/node-runtime-health-endpoint`
- `docs/node-runtime-onboarding`

## Required Validation Before PR

At minimum, for runtime-impacting changes:

```bash
cd clawseal
source .venv/bin/activate
python api_server.py
```

Then verify:
- `GET /health` returns healthy status
- `POST /start` succeeds
- `POST /process` returns response payload

If your change affects other modules, run relevant targeted tests in repo root (for touched components) and include commands/results in PR description.

## What We Welcome

- Runtime reliability fixes
- Plugin examples and integration patterns
- Documentation clarity improvements
- Performance profiling and measured optimizations
- Better error handling and observability

## Non-Negotiable Invariants

Do not merge changes that break these:

1. API contract stability for core endpoints (`/health`, `/start`, `/process`)
2. Backward-compatible behavior for existing plugin interface patterns
3. No hardcoded secrets, tokens, or private keys
4. Clear error responses instead of silent failures

## Security & Secrets

- Never commit `.env` files, credentials, or tokens.
- Use placeholders in docs and examples.
- If you find a security issue, do not open a public exploit issue. Report privately to maintainers.

## Code Style

- Follow PEP 8
- Add type hints for new public interfaces
- Add docstrings for public functions/classes
- Keep changes small and cohesive

## Pull Request Requirements

Every PR should include:

1. What changed
2. Why it changed
3. How you tested it (exact commands)
4. Any API or behavior impacts
5. Follow-up work (if any)

PR title format:
- `[Feature] ...`
- `[Fix] ...`
- `[Docs] ...`
- `[Refactor] ...`
- `[Perf] ...`
- `[Test] ...`

## Suggested Starter Contributions

- Add one production-grade plugin example in `clawseal/plugins/`
- Add API usage examples under `clawseal/README.md`
- Improve runtime error messages in `clawseal/api_server.py`
- Add focused tests for node runtime behavior under a new `tests/node_runtime/` directory

## Questions

Open an issue with:
- current behavior
- expected behavior
- reproduction steps

Clear repro steps get fastest turnaround.
