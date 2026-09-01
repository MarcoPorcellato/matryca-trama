# Persistent Goal: Matryca Trama Public Foundation

## Objective

Establish a trustworthy public source-available Community monorepo for Matryca
Trama while preserving clean commercial, Pro, and Matryca Brain boundaries.

## Current scope

Complete the foundation specification, architecture, ADRs, roadmap, repository
policy, and reviewable evidence. The next planning boundary defines public
Parser/Plumber compatibility and a future Logseq read-only contract for graph
identification, page reads, and complete block-subtree reads. Do not add Pro
source, Brain implementation, secrets, private dependencies, runtime adapters,
or a write path.

## Completion criteria

- Public repository structure and licensing are unambiguous.
- Parser, Plumber, OG, DB, and Nodi boundaries are documented.
- Fork-safe CI and the temporary contributor licensing gate are defined.
- Every later milestone has a testable evidence gate.
- Public contract tests reject private Brain imports, unsupported versions, and
  authority or provenance omissions.
- The initial Logseq adapter scope remains read-only and independently usable
  without a Brain service.
- A future Pro decision is explicitly deferred rather than implied.

## Stop conditions

Stop before creating private integrations, changing licences again, accepting
external copyright-bearing contributions, importing legacy history, selling a
commercial licence, or publishing artifacts without the required separate
authorization and review.

Also stop before selecting a DB host surface without a focused compatibility
spike, treating a Tine workflow as write authority, adding events or Shadow
acceleration, or implementing any read or write adapter without an accepted
contract and executable evidence.
