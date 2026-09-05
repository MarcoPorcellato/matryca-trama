# Matryca Trama Claim Ledger

This ledger records current capability claims under the
[delivery program](../specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md). It is not a
release-support matrix. Every entry must retain its exact scope, revision,
evidence, and limitations.

## Current anchors

- Repository head observed during planning: `9905e8a36acb83a17a33b702a5fa620d6bfed185`.
- Qualified baseline: `862c5c89157f28c1985cde6145fc2c8af04a70b4`.
- Baseline evidence:
  [`862c5c89157f28c1985cde6145fc2c8af04a70b4.md`](../spikes/evidence/python-read-contract-v1/862c5c89157f28c1985cde6145fc2c8af04a70b4.md).
- These anchors are historical observations. Reverify live state before using
  them for delivery.

- V0 anchor audit: candidate `2de8069ce450daa3b2f7ca591d09d73a951150f4`,
  tree `7104e1bdf4a272a31128d01adb13bd3fc1e8d4e7`; remote-tracking `origin/main`
  `9905e8a36acb83a17a33b702a5fa620d6bfed185`; baseline tree
  `f1dacc9b30c993b2b69a48c20e73281732e781b3`. See
  [the sanitized receipt](receipts/2026-09-05-v0-anchor-audit.md). Initial
  sandbox fetch was blocked; the coordinator subsequently refreshed remote state
  with one elevated fetch (exit 0). Current-head qualification remains blocked.

## Claims

| Claim ID | Class | Claim and scope | Qualified revision | Evidence | Limitations / next action |
|---|---|---|---|---|---|
| `V0-FOUNDATION-001` | Documented | Public source-available foundation, PolyForm Noncommercial boundary, governance, and fork-safe policy checks exist. | Not assigned by this ledger. | Foundation specification and repository policy files. | Reverify mutable GitHub settings and exact-head checks. |
| `V0-SOURCE-001` | Implemented | `9905e8a` contains bounded Python contracts, core, Parser bridge, Plumber bridge, and synthetic OG adapter source. | None. | Repository tree at `9905e8a`. | Implementation is not current-head qualification or publication. |
| `V1-BASELINE-001` | Qualified baseline | Synthetic OG fixtures cover `graph.identify`, `page.read`, and complete ordered `block.subtree.read.complete`. | `862c5c89157f28c1985cde6145fc2c8af04a70b4` | Baseline evidence record linked above. | No user graph, host, DB, write, event, Shadow, sync, export, recovery, UI, performance, distribution, or network claim. |
| `V1-CURRENT-001` | Blocked | Qualify one exact current head with locked local and hosted evidence. | None. | No current-head evidence record. | Complete V0 reconciliation, then execute the V1 plan. |
| `V2-CONTRACT-001` | Implemented | Bounded `trama.logseq.read/v1` source and rejection tests exist. | None. | Repository tree at `9905e8a`; baseline evidence covers only the bounded slice. | Contract is not frozen or published. |
| `V3-PARSER-001` | Blocked | Qualify exact public Parser versions and package-root symbols. | None. | Candidate profile only. | Requires V1 and V2 plus cross-repository evidence. |
| `V4-PLUMBER-001` | Blocked | Qualify exact Plumber consumption of public Trama envelopes. | None. | Local synthetic consumer tests only. | Requires exact Trama, Parser, and Plumber revisions. |
| `V5-OG-001` | Unsupported | Operational OG support beyond public synthetic fixtures. | None. | None. | Requires sanitized fixture classes and containment evidence; private vaults are forbidden. |
| `V6-DB-001` | Blocked | Official-host, read-only Logseq DB profile. | None. | PR #14 is a mutable proposal, not evidence. | Requires accepted host decision and exact-version read-only evidence. |
| `V7-NODI-001` | Unsupported | Nodi runtime and accessible UI. | None. | Design direction only. | Requires qualified data profile, state contract, and WCAG 2.2 AA evidence. |
| `V8-AGENT-001` | Unsupported | Agent and plugin execution surface. | None. | Safety requirements only. | Requires default-deny capability model and adversarial evaluation corpus. |
| `V9-DIST-001` | Unsupported | Reproducible Community artifacts. | None. | None. | Requires qualified runtime, SBOM, provenance, artifact inspection, and rehearsal. |
| `V10-RELEASE-001` | Blocked | Public Community release. | None. | None. | Requires V0–V9 evidence and separate maintainer authorization. |

## Update rule

Never overwrite a historical claim to make it appear current. Add or revise an
entry only after recording the exact qualified revision, evidence revision,
subject digest where relevant, commands, platforms, results, limitations, and
authority. Negative and unsupported outcomes remain first-class evidence.
