# V0 anchor audit

- Candidate revision: `2de8069ce450daa3b2f7ca591d09d73a951150f4`; tree: `7104e1bdf4a272a31128d01adb13bd3fc1e8d4e7`
- Remote main: `9905e8a36acb83a17a33b702a5fa620d6bfed185` (verified by a successful `git fetch origin --prune` after the initial sandbox-restricted attempt)
- Baseline revision: `862c5c89157f28c1985cde6145fc2c8af04a70b4`
- Baseline tree: `f1dacc9b30c993b2b69a48c20e73281732e781b3`
- Worktree state: `clean; candidate branch ahead of remote-tracking main by 1 commit`
- Runtime comparison: no differences in `pyproject.toml`, `uv.lock`, `packages`, `tests`, or `.github/workflows/python-contracts.yml` between baseline and candidate.
- Known qualification: baseline bounded Python read-contract evidence at `docs/spikes/evidence/python-read-contract-v1/862c5c89157f28c1985cde6145fc2c8af04a70b4.md`; comparison evidence does not qualify the candidate.
- Checks: `python3 scripts/validate_foundation.py` and `git diff --check` passed (exit 0).
- Unknowns: current-head qualification suites and hosted evidence are not established; maintainer approval of unresolved V0 unknowns is pending.
- Next gate: `V1 exact-head local qualification`
