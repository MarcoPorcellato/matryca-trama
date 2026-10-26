# Third-Party Licence Inventory

## Current shipped dependencies

The fictional browser demo admitted by ADR-0011 includes the following local
asset. Trama-owned source remains PolyForm Noncommercial; upstream terms apply
to the asset itself. No Python application dependency is added.

| Asset | Version | Licence choice | Distribution |
| --- | --- | --- | --- |
| vis-network standalone UMD | 9.1.2 | MIT, offered alongside Apache-2.0 | Unmodified browser bundle in `apps/synthetic_demo/vendor`, embedded in the local demo artifact |

Official source: `https://registry.npmjs.org/vis-network/-/vis-network-9.1.2.tgz`.
Archive SHA-1 `ddaca300a9764bbf1646a0aa03eb28fe55823ca8`; asset SHA-256
`3729be2f3994c83229106c3d34fb8de807572cf6f282c23e2b34ecf4e84ce863`.
Retain both upstream license files, all copyright/license comments in the
standalone bundle, and the readable license text in generated HTML. Embedded
third-party notices are preserved; no source-minification or header stripping.
This reuses the renderer family/version used by Parser LENS, not Parser code.

## Planned external integrations

Matryca Parser and Matryca Plumber are independent Apache-2.0 projects. They are
planned integrations, not vendored or distributed by this repository at the
foundation stage. Logseq is an independent project and is not bundled here.

Before adding or packaging any dependency, record its exact package, version,
source, licence, notice obligations, distribution status, and compatibility
decision here or in a generated inventory governed by an accepted ADR. The
dependency's own terms continue to apply.

## M1 qualification-only dependencies

The following exact distributions are confined to a disposable test-only
validator environment under ADR-0008. They are not vendored, shipped with a
Trama application or admitted as adapter runtime dependencies. The root
workspace lock and package dependencies are unchanged. Exact wheel identities,
sizes, SHA-256 values and registry URLs are in
`tests/qualification/inputs.json`; the multi-platform hash-locked closure is
`tests/qualification/requirements.txt`. Before installation, the lane checks
wheel METADATA identity/licence declarations and hashes the bundled notices.

| Distribution | Version | Declared licence | Official version source |
| --- | --- | --- | --- |
| attrs | 26.1.0 | MIT | <https://pypi.org/project/attrs/26.1.0/> |
| jsonschema | 4.26.0 | MIT | <https://pypi.org/project/jsonschema/4.26.0/> |
| jsonschema-specifications | 2025.9.1 | MIT | <https://pypi.org/project/jsonschema-specifications/2025.9.1/> |
| referencing | 0.37.0 | MIT | <https://pypi.org/project/referencing/0.37.0/> |
| rpds-py | 0.30.0 | MIT | <https://pypi.org/project/rpds-py/0.30.0/> |
| typing-extensions | 4.15.0 | PSF-2.0 | <https://pypi.org/project/typing-extensions/4.15.0/> |

Preserve each distribution's own licence and notice files in its test
installation. Any later redistribution must carry the required copyright,
permission and disclaimer notices under those exact terms; no legal or
commercial-use permission is inferred from test qualification. Runtime use in
a real adapter requires a separate dependency decision.

The immutable Plumber 2.1.0a3 wheel and its hash-locked producer closure occupy
another disposable environment. Their existing upstream licences remain in
force. Released schemas, fixtures, golden results and TCK resources are read
transiently from the authenticated Apache-2.0 owner artifact, not copied into
this repository. No compatibility admission follows.
