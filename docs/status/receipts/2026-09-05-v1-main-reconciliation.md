# V1 current-main reconciliation

- Reconciled revision: `a3411df1989095abdea708526843bfcfe10b9c49`
- Reconciled tree: `49aa088561f939872beabd6b179d4652a5571241`
- Merge time: `2026-09-05T12:28:21Z`
- Local status: clean, branch-only worktree at the reconciled revision
- `uv.lock` SHA-256: `1987e031fa247cfa67dd0f991385e6bcbb15aab3f1c7f097a2af379861e24bfb`

Exact-main push evidence:

| Check | Run / job | Evidence |
|---|---|---|
| Foundation | `33966129554` / `101306479482` | [job](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/33966129554/job/101306479482) |
| Python contracts | `33966129576` / `101306479228` | [job](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/33966129576/job/101306479228) |

Dependency Review remains PR-scoped. Its successful exact PR base/head result
is [recorded separately](../../spikes/evidence/python-read-contract-v1/49aae4f21b1f466604f74a4d1d66b5cdc02933d4.md);
the identical PR-head/main tree corroborates provenance and is not a push result.

Local reconciliation passed locked sync, 38 contract tests, 6 containment
tests, 7 Plumber-consumer tests, 10 foundation-validator tests,
`validate_foundation.py` (1036 files), and `git diff --check`.

Qualified scope remains synthetic OG fixtures only. V2 execution and all
unsupported host, DB, write, event, sync, export, recovery, UI, performance,
distribution, and release claims remain out of scope.
