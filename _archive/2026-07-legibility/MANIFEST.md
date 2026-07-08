# _archive/2026-07-legibility — ClawSeal legibility reorg manifest

**Date:** 2026-07-07. **Rationale:** repository legibility (a stranger should see
load-bearing vs. scaffolding at the root). Nothing deleted — moved only. Per
REORG_PLAN.md (bridge root). All moves via explicit `git mv` (history preserved).

## Moved

| Source | Destination | Why archived |
|---|---|---|
| `VERIFICATION_REPORT_1.1.6.md` | `reports/VERIFICATION_REPORT_1.1.6.md` | Dated point-in-time verification report (2026-04-22). Superseded; no tracked path-reference. |
| `FRESH_INSTALL_VALIDATION.md` | `reports/FRESH_INSTALL_VALIDATION.md` | Dated one-off fresh-install validation run (ClawSeal 1.1.3). Confirmed NOT cited as live claim-provenance (zero tracked references). |
| `clawseal_dashboard_preview.html` | `previews/clawseal_dashboard_preview.html` | Standalone static HTML preview artifact at repo root. Not imported, no tracked references. |

## Held (NOT moved — pending decision)

| Item | Status |
|---|---|
| `clawseal-openclaw-plugin/` | **ARCHIVE PENDING SHAWN'S CANONICAL-PLUGIN DECISION.** Near-duplicate of `openclaw-plugin/`; left in place until the canonical plugin is confirmed. Do not archive without that confirmation. |

## Not touched (out of scope this pass)

- Root `demo_layer*.py` + `run_full_demo.sh` — import-coupled (`from demo_layer2_with_mirra import main`, root-relative invocation in docs/script). Consolidation into `demo/` is a code-change decision for a separate diff-reviewed pass, not hygiene.
