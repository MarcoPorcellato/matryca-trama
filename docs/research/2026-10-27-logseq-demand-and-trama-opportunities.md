# Logseq community demand and Matryca Trama opportunities

**Research date:** 27 October 2026, Europe/Rome.
**Status:** research and planning proposal; no feature implementation or compatibility admission.
**Research execution:** five independent GPT-6 Luna workers at Max reasoning, consolidated and cross-checked against primary sources by the Trama activity.
**Planning:** explicit GPT-6 Astra xhigh handoff; its proposed delivery sequence is recorded in this same document.
**Local execution record:** Beads `matryca-trama-l5a.26`; no tracker synchronization or public issue creation.

## 1. Decision summary

The evidence supports a product opportunity in **helping people understand and
navigate their own knowledge with less effort**, especially users retaining
Logseq OG. It does not support cloning every highly voted editor, reader,
mobile or synchronization feature into Trama.

There are two distinct opportunities:

1. **Remaining or partially served needs:** alias-aware graph presentation,
   useful relationship explanations, stable reference review, long-page
   navigation and a safe, evidence-rich asset/reference audit. Some remain
   unverified rather than conclusively absent in current Logseq.
2. **OG parity without DB migration:** bring appropriate newer presentation
   experiences to OG users when Plumber can supply the necessary data. A
   capability already present in DB can still be valuable here, but must be
   described as OG-oriented parity or a better workflow, not an invention or a
   capability missing from all Logseq products.

The owner explicitly requested the second opportunity during this research.
It has its own lane below. "Easy" means both a small implementation and
available, admitted data; a simple-looking button does not make an unsupported
source contract easy. Current Trama source permits only the synthetic demo and
its separately restricted synthetic consumer. **No real OG or DB graph access,
MA attempt, producer execution, migration or write is authorized here.**

Do not position Trama as simply "a faster graph than Logseq." Logseq's May 2026
DB announcement describes a rebuilt graph experience, and released DB and OG source already contains depth controls, saved settings
and navigation hooks. We have
not benchmarked either product. The narrower opportunity is a coherent,
explainable experience, including OG users, whose usefulness must be tested.
[Graph View V2 announcement][DB-MAY] [Released DB graph source][DB-GRAPH]

## 2. Method, demand measures and limits

### 2.1 What was sampled

The primary quantitative sample is the first **four pages, 0–3**, of the
public Feature Requests category ordered by `vote_count`:

- [Page 0 metadata](https://discuss.logseq.com/c/feedback/feature-requests/7/l/latest.json?order=votes&page=0)
- [Page 1 metadata](https://discuss.logseq.com/c/feedback/feature-requests/7/l/latest.json?order=votes&page=1)
- [Page 2 metadata](https://discuss.logseq.com/c/feedback/feature-requests/7/l/latest.json?order=votes&page=2)
- [Page 3 metadata](https://discuss.logseq.com/c/feedback/feature-requests/7/l/latest.json?order=votes&page=3)

The live metadata capture yielded **120 unique topics**, in descending vote
order, from **285 to 23 votes**. It includes **21 topics carrying `done` or
`done-with-db-version` tags**. Those topics are retained as negative controls,
not counted as missing features. Appendix A preserves the entire sampled
register, exact topic links, creation dates, last-post dates and observed tags.
The metadata-only capture SHA-256 is
`88e9319b0ff3c0b6baf46a358030dadfc6f1377aa078135e857994070fa4b4c9`.
The pages were fetched sequentially, not as an atomic database snapshot.

Five independent searches covered graph/search, organization/review,
mobile/sync/collaboration, current releases/capabilities, and the highest-voted
reader/editor/export/reminder requests. Additional targeted topics were checked
for recent regressions, migration sentiment and less popular but directly
relevant Trama workflows. Their discussion histories and implementation
counter-evidence inform the family register below.

### 2.2 What the numbers mean

- Votes are the observed Discourse `vote_count`; views, likes and post counts
  are different measures. None is a count of paying customers or market share.
- Rankings apply only to this sample. We did not poll the whole user base,
  read private Discord channels, or recover deleted/hidden discussions.
- Long-lived requests accumulate votes. A recent request with few votes may
  still matter; a high-vote old request may already be solved.
- A topic's creation date is not its most recent activity date. `last_posted_at`
  is not a delivery or resolution date. Examples corrected during review:
  the unused-assets help topic began on 18 April 2023, not its May 2025 follow-up;
  the scroll-restoration request began on 23 December 2025, not May 2026.
- A closed GitHub issue is not proof of delivery. Logseq has directed feature
  requests to its forum and has closed GitHub feature requests administratively.
  [Example routing notice](https://github.com/logseq/logseq/issues/4979)
- We do not add votes across related requests as if they were independent
  users. Replies and linked duplicate topics are qualitative corroboration.

This is a reconstruction of the **located public history**, not an exhaustive
archive of every request or every comment. Appendix A is a metadata census of
the sampled topics; only the detailed families received deeper status review.

### 2.3 Status vocabulary and contradiction rule

| Status | Meaning in this dossier |
| --- | --- |
| Core documented / implemented in source | Positive evidence in official docs or a named release's source; not a runtime test performed here. |
| Partial | Some requested behavior is evidenced, but the narrower requested workflow is not established. |
| Plugin workaround | A maintainer repository documents an alternative; its current compatibility and safety are not automatically established. |
| No shipped evidence located | The inspected sources did not establish delivery; this is not a proof of universal absence. |
| Unknown / conflict | Evidence is insufficient or sources describe different dates/channels. |
| OG parity candidate | Potential value for OG users even if DB already offers related behavior. |
| Trama hypothesis | Our product interpretation; not a verbatim community request or a commitment. |

Positive released-source evidence overrides an inference of absence from a
feature announcement. A roadmap entry is not a release receipt; an open request
can coexist with implemented behavior. This rule materially changed the graph
recommendations during consolidation.

## 3. Current Logseq context and reconstructed release history

| Date | Located milestone | Interpretation |
| --- | --- | --- |
| 2024-04-29 | [Why the database version and how it is going](https://discuss.logseq.com/t/why-the-database-version-and-how-its-going/26744) | Development rationale; not a shipped release or two-way Markdown promise. |
| 2024-10-31 | [DB release-schedule discussion](https://discuss.logseq.com/t/logseq-db-version-release-schedule/29668) | Historical caution about development maturity; not current status. |
| 2026-04-15 | [OG 1.0.0 release][OG-RELEASE] | Desktop/Android file-product release, named Beta Testing. |
| 2026-04-24 | [Official product split][SPLIT] | OG retains file graphs; DB is the main new-feature track; migration is not compulsory. |
| 2026-04-28 | [DB guide's own feature-description date][DB-GUIDE] | Feature reference, not a guarantee of October platform availability. |
| 2026-05-16 | [DB update][DB-MAY] | Announces Graph View V2 and a Markdown Mirror; describes two-way mirror edits as still in development at that date. |
| 2026-07-13 | [DB 2.0.1 beta](https://github.com/logseq/logseq/releases/tag/2.0.1) | First public DB beta described in the release. |
| 2026-10-07 | [DB 2.0.2 beta][DB-RELEASE] | Latest versioned DB release located; published at 14:18:57 UTC. |
| 2026-10-21 | [Public roadmap][ROADMAP] | Visible roadmap date; still labels product Beta testing. |
| 2026-10-25 | [Nightly release][NIGHTLY] | Live GitHub API reports nightly 20261025 at 06:33:22 UTC, prerelease. Replaces a stale search result showing October 21. |

GitHub's `prerelease=false` for 2.0.2 and OG 1.0.0 does not erase **Beta Testing**
from their release names. Packaging flags and product maturity are distinct.
No Logseq binaries were downloaded or run in this research.

The [split announcement][SPLIT] says OG will receive maintenance/security and
dependency work while new features concentrate on DB. This creates a genuine
reason to assess OG sidecar parity. It does not grant Trama permission to
become an editor, synchronize canonical storage, or bypass Plumber.

### 3.1 Capabilities that must not be advertised as universally missing

The following short summaries rely on official DB documentation; each still
needs product/channel-specific qualification before any interoperability claim.

| Area | Counter-evidence and remaining distinction |
| --- | --- |
| Properties, tasks and tables | DB documents typed properties, custom task/status behavior, query construction and editable table/list/gallery views. OG already has query and task tools, but parity is not assumed. |
| Reference views | DB documents view filters and sorting. Mention-event chronology is a different requirement from a node's Created/Updated timestamp. |
| Capture and assets | DB documents iOS capture/share/voice and an asset library. These do not establish Android public availability or an orphan-reference audit. |
| Source interchange | DB documents multiple export formats. Standard Markdown export is not a lossless source-equivalence guarantee. |
| Native graph controls | Released 2.0.2 source implements depth 1–5, tag filtering, journal visibility, local settings persistence, a created-at time control, and node-open/activate hooks. |

[DB guide][DB-GUIDE] [DB changes guide][DB-CHANGES] [Released graph implementation][DB-GRAPH]

The changes guide explicitly says **whiteboards, Excalidraw and slides are no
longer built-in DB features**, with plugin possibilities discussed. It also
documents restricted no-effect web plugins: "web plugins are absent" would be
wrong. This is more specific than the mixed-status roadmap, which still lists
whiteboard and plugin work. [DB changes guide][DB-CHANGES]

Mobile remains a dated-source conflict: the October beta release links to
TestFlight and records App Store review at release time; README and the older
guide still use alpha/invite language. Android bug fixes do not prove public
DB Android distribution. Mobile availability and plugin/PDF parity remain
unverified here. [DB release][DB-RELEASE] [DB README][DB-README]

### 3.2 Corrections made during primary verification

| Initial lead | Stronger evidence | Adopted conclusion |
| --- | --- | --- |
| Alias-hide PR is open | [PR #11760 API](https://api.github.com/repos/logseq/logseq/pulls/11760): closed 2026-05-11, `merged_at=null` | Closed unmerged; no shipped implementation follows. |
| Latest nightly is October 21 | [Live release metadata](https://api.github.com/repos/logseq/logseq/releases?per_page=5) | Latest listed nightly was October 25 at retrieval. |
| Adjustable neighborhood depth is absent | [2.0.2 graph source, lines 445–452][DB-DEPTH] | Existing depth slider, not a DB gap. |
| DB cannot open a graph node | [Selected-node buttons and activation hooks][DB-OPEN] | Implementation exists; the newer one-tap request may concern UX/regression, not feature absence. |
| Graph preferences are unsaved | [Graph settings load/save, lines 98–113][DB-SETTINGS] | Settings persist; exact manual coordinates and named multi-view bookmarks are separate, unverified questions. |
| DB whiteboard and web plugins are simply unknown | [Explicit differences guide][DB-CHANGES] | Whiteboards removed from core; restricted web plugins documented. |

The DB 2.0.2 annotated tag resolves to commit
`533ac4382a7b69baa98de3a973bff90305b212dc`; the inspected graph file Git blob is
`7d38c1fde761e3e3b9f52f7be1c147c85d5000f9`. OG 1.0.0 graph-panel blob is
`9dd61dc3dd79b83e149f1c2a310317562d156035`, graph-interaction blob
`2d5116238c3ff9c046dee99fbab48f32440c8d21`, and query-table blob
`2ebc5e3b6fd06fae6006ccdad243d6488eed1cc1`. These bind static source observations,
not binaries or runtime qualification.

These corrections are retained because the roadmap must not inherit stale
subagent claims. No worker report is itself an authority over the source.

## 4. Request-family register and history

Votes below come from Appendix A unless identified as targeted metadata.
**Trama fit** distinguishes product value from present source readiness.

### F01 — EPUB reading (285 votes)

- **History:** [Request opened 2021-08-10](https://discuss.logseq.com/t/support-epub-format-ebooks/2010); [June 2026 follow-up](https://discuss.logseq.com/t/support-epub-format-ebooks/2010?page=2) asks about earlier roadmap interest.
- **Status:** no native EPUB delivery established in the inspected current releases. The [Calibre plugin](https://github.com/duydl/logseq-calibre-plugin) documents a reader/annotation workflow through an external Calibre service; DB compatibility was not established.
- **Remaining need:** reading and annotating books within a linked-note workflow. A plugin is meaningful competition, not evidence that the request has no solution.
- **Trama decision:** defer native EPUB. It introduces document ingestion, rendering and annotations beyond current graph presentation. A later source-linked reading-review surface would need separately admitted content/asset contracts. **Complexity:** large; not an easy OG parity win.

### F02 — Custom task states (263 votes; DB-covered negative control)

- **History:** [Request opened 2021-03-30](https://discuss.logseq.com/t/add-support-for-customisable-todo-keywords/696), with later forum tags `done-with-db-version` and `on-roadmap` retained in the snapshot.
- **Status:** newer DB task/property behavior addresses the central custom-state request; this does not create equal OG behavior.
- **OG opportunity:** a read-only Trama task/status view could display existing OG values without converting the graph or modifying task syntax. That is a presentation hypothesis; arbitrary DB task/class semantics must not be projected into OG.
- **Trama decision:** assess as parity only when task/status payload is admitted through Plumber. Current synthetic topology cannot supply it. **UI effort:** potentially small; **source readiness:** gated.

### F03 — Long-form writing (248 votes)

- **History:** [Opened 2021-11-19](https://discuss.logseq.com/t/longform-writing-in-logseq/3527); a May 2023 developer reply describes improvements rather than completion; [September 2025 follow-up](https://discuss.logseq.com/t/longform-writing-in-logseq/3527?page=4) reports contents-plugin and lazy-loading problems.
- **Status:** document-style viewing and plugins offer partial routes. Improved large-page rendering does not establish a complete writing, citation and document-export workflow.
- **Trama opportunity:** a read-only long-page outline and contextual preview are narrower than building a second editor. Preserve ordered blocks and source anchors; an OG user should not need DB migration to benefit.
- **Decision:** prioritize the navigation subset for design; defer editing, citation editing and publishing. **UI effort:** small/medium after content admission; full editor: large.

### F04 — Vim-style editing (221 votes)

- **History:** [Opened 2021-02-03](https://discuss.logseq.com/t/vim-mode-powerful-shortcuts/275); [later thread](https://discuss.logseq.com/t/vim-mode-powerful-shortcuts/275?page=2) remains active through August 2024.
- **Status:** [Vim Shortcuts plugin](https://github.com/vipzhicheng/logseq-plugin-vim-shortcuts) documents modal controls. Native current DB support and plugin DB compatibility were not established.
- **Trama decision:** defer a Vim editor. Accessible keyboard graph navigation is a separate, narrower product-quality goal, not delivery of this request. Reusing common shortcuts must not be advertised as implementing Vim editing. **Complexity:** large for editing; small for selected navigation shortcuts.

### F05 — Mobile PDF annotation (200 votes)

- **History:** [Opened 2022-01-05](https://discuss.logseq.com/t/pdf-annotation-on-mobile-devices/4449); 2023 replies describe study workflows and reliance on other tablet tools; later discussion continues in 2024.
- **Status:** desktop annotations and importer preservation do not establish mobile reading/annotation parity. Current mobile behavior remains unverified.
- **Trama decision:** defer a mobile PDF editor. A later read-only evidence panel could link an existing annotation to its source, subject to asset/annotation contracts and platform support. **Complexity:** large; not part of the current app shell.

### F06 — Mobile plugin parity (147 votes)

- **History:** [Opened 2022-08-25](https://discuss.logseq.com/t/plugin-support-for-ios-android-apps/10109); a March 2025 maintainer response discusses DB browser plugin progress; [November 2025 follow-up](https://discuss.logseq.com/t/plugin-support-for-ios-android-apps/10109?page=2) still asks about mobile workflows.
- **Status:** DB-compatible desktop plugins and restricted web plugins do not establish mobile runtime parity.
- **Trama decision:** do not create a mobile plugin runtime to satisfy this request. Prefer integrated, tested user tasks where Trama owns the UI. Mobile distribution and extension security require separate decisions. **Complexity:** large.

### F07 — Fast search and body/refinement filters (142 / 140 / 83 votes; distinct topics)

- **History:** [Search operators, 2020-12-16](https://discuss.logseq.com/t/add-search-operator-filters-for-the-search-box/74); [note-body filters, 2021-06-21](https://discuss.logseq.com/t/filters-for-note-body-not-just-backlinks/1305); [general search complaints, 2021-10-23](https://discuss.logseq.com/t/please-fix-the-search/3113).
- **Status:** the general search thread is tagged done. DB has search/refinement improvements; the exact global-operator request differs from filtering a saved view. The [Filter Page plugin](https://github.com/benjypng/logseq-filterpage-plugin) provides another body-filter workflow.
- **Remaining need:** narrow results transparently, showing the active scope and why an item matched. Do not claim that Logseq has no search or filter system.
- **OG opportunity:** a simple read-only filtering panel over admitted OG content, with visible inclusion rules and a path back to source. Existing Trama demo filters are synthetic presentation only. **UI effort:** small/medium; content indexing, freshness and payload completeness are separate costs.

### F08 — Existing cloud providers on iOS (130 votes)

- **History:** [Opened 2022-01-12](https://discuss.logseq.com/t/sync-on-ios-with-onedrive-dropbox-googledrive-icloud/4685), with activity through March 2026. [Dropbox support discussion](https://discuss.logseq.com/t/how-to-sync-to-iphone-using-dropbox/28579) distinguishes OG provider choices.
- **Status:** Logseq's own sync does not satisfy every existing-provider requirement. Arbitrary provider support in DB was not established.
- **Trama decision:** not a source-reader or UI shortcut. Sync providers, credential handling and canonical storage remain outside this roadmap. Show source freshness honestly once Plumber supplies it; do not silently replicate files. **Complexity:** large and security-sensitive.

### F09 — Long-page outline and sidebar overview (121 votes)

- **History:** [Opened 2021-04-06](https://discuss.logseq.com/t/outline-overview-for-sidebar/740); early discussion points to a community TOC solution rather than an established built-in outcome.
- **Status:** a namespace Library tree is not a contents outline. Current all-platform built-in parity was not established; plugins remain alternatives.
- **OG opportunity:** headings and ordered block hierarchy can drive a read-only outline next to the graph, without a DB migration. Plumber must expose source-bound ordered content; Trama cannot call Parser directly.
- **Decision:** high-fit navigation candidate. Include source context, collapse state, keyboard access and current-view boundaries. **UI effort:** small/medium; source ordering and payload admission remain gates.

### F10 — Namespace/folder organization (114 / 67 / 31 votes)

- **History:** [Folders, 2021-11-14](https://discuss.logseq.com/t/feature-request-creation-of-folders-and-subfolders-will-make-knowledge-management-more-feasible/3446); [namespace proposal, 2021-12-01](https://discuss.logseq.com/t/proposal-changing-how-namespaces-function-in-logseq/3727); [filesystem subdirectories, 2022-08-15](https://discuss.logseq.com/t/support-subdirs-for-namespace-hierarchy/9763).
- **Status:** DB's virtual Library covers part of organization. Actual directory layout, page namespaces and DB class hierarchy are different concepts; no universal folder gap is established.
- **OG opportunity:** optional virtual browsing based on explicit existing hierarchy, never file moves. A friendly tree can be useful even when similar native/plugin tools exist.
- **Decision:** parity/discovery candidate, not automatic reorganization. **UI effort:** small if normalized hierarchy exists; semantic mapping must be owned by Plumber.

### F11 — Clean PDF/document export (110 votes)

- **History:** [Opened 2021-06-16](https://discuss.logseq.com/t/pandoc-plugin-for-exporting-export-to-pdf/1247); [later reports through February 2025](https://discuss.logseq.com/t/pandoc-plugin-for-exporting-export-to-pdf/1247?page=2) discuss output and conversion limits.
- **Status:** [Pandoc plugin](https://github.com/benjypng/logseq-pandoc-plugin) and [PDF export plugin](https://github.com/sawhney17/logseq-pdf-export) are real alternatives. DB HTML-export fixes do not prove clean publication across every format.
- **Trama opportunity:** exporting an explicitly selected derived analysis is narrower than exporting or publishing a whole graph. It still requires a separate output/privacy scope; references, hidden content and attachments must not leak.
- **Decision:** defer document conversion; later assess a bounded analysis report. **Complexity:** medium/large, format-dependent.

### F12 — Alias-aware graph presentation (109 votes)

- **History:** [Opened 2022-02-12](https://discuss.logseq.com/t/hide-aliases-circles-in-graph-view/5455); [PR #11760](https://github.com/logseq/logseq/pull/11760) proposed a toggle on 2025-02-26; live API shows closure without merge on 2026-05-11. Forum activity extends through April 2026.
- **Status:** current native alias-collapse behavior is not established by that PR. Hiding an individual page is not equivalent to redirecting alias edges to a canonical page.
- **OG opportunity:** explain aliases and optionally collapse their visual duplicates while retaining provenance. Do not silently merge pages, infer identities from equal titles, or hide conflicting canonical targets.
- **Decision:** strong graph-specific candidate for synthetic design first. Needs explicit alias/identity mapping from Plumber for real OG use. **UI effort:** small/medium; mapping correctness is not a UI-only task.

### F13 — Readable/basic UI settings (104 votes)

- **History:** [Opened 2021-10-13](https://discuss.logseq.com/t/basic-ui-settings-e-g-font-size/2946); later replies include small-text concerns on mobile. A newer [iOS toolbar issue](https://github.com/logseq/logseq/issues/13140) was opened in August 2026.
- **Status:** newer mobile Dynamic Type and toolbar work are progress, not universal accessibility qualification.
- **Trama decision:** readable text, native controls, visible disabled-state explanations, keyboard focus and a usable narrow layout are baseline quality. They must not depend on a plugin. Current prototype evidence covers a measured small viewport, not a shipped mobile app or full accessibility audit. **UI effort:** often small; complete assistive-technology/platform coverage requires actual testing.

### F14 — Kanban, editable query tables and custom views (100 / 58 / 28 votes; mixed coverage)

- **History:** [Kanban, 2021-06-02](https://discuss.logseq.com/t/introduce-kanban-boards-as-a-new-primitive/1095); [ordinary table UI, 2021-08-09](https://discuss.logseq.com/t/table-creation-interface-not-query-table/1974); [query-table redesign, 2022-08-08](https://discuss.logseq.com/t/reimagining-query-tables-editing-database-features-etc/9568); [DB Query Builder announcement, 2026-02-13](https://discuss.logseq.com/t/introducing-the-logseq-db-query-builder/34794).
- **Status:** DB editable tables/views answer substantial parts of this cluster. The roadmap's Kanban entry alone does not prove a released Kanban view. A freeform table editor is different from a query-result table.
- **OG opportunity:** a read-only property/status table with clear sorts and filters; an optional board view only after data shape and semantics are explicit. No editing of OG properties from Trama in this scope.
- **Decision:** high potential parity value, but not a claim of a generic Logseq database gap. **UI effort:** small/medium after payload; editing and new status semantics are a separate project.

### F15 — Task reminders and calendar integration (86 / 78 votes)

- **History:** [Task notifications, 2022-04-13](https://discuss.logseq.com/t/task-notifications/6638), last metadata activity August 2026; [Google Calendar sync, 2021-04-26](https://discuss.logseq.com/t/google-calendar-sync/830), later discussion through March 2025. Not all recent notification-post text was retrievable.
- **Status:** task date/repeat fixes do not establish timed OS alerts. [Calendar plugin](https://github.com/sawhney17/logseq-calendars-plugin), [Agenda](https://github.com/haydenull/logseq-plugin-agenda) and [Orbitals](https://github.com/yfhuang7/logseq-orbitals) cover different import/overlay tasks. Full two-way current DB parity is not established; [marketplace metadata](https://github.com/logseq/marketplace/blob/master/plugins.json) records version-support distinctions.
- **Trama decision:** a read-only dated-item review may fit later. Background reminders and calendar writes add scheduling, permissions, credentials and external state; defer them. A task table must not be sold as delivering reminders. **Complexity:** medium for read-only review, large for reliable cross-platform integration.

### F16 — Predictable reference ordering and explanations (78 votes)

- **History:** [Opened 2022-09-01](https://discuss.logseq.com/t/sort-linked-references/10391); later OG-era [reference-order report #10854](https://github.com/logseq/logseq/issues/10854) concerns 0.10.2/0.10.3 and is not a fresh OG 1.0.0 test.
- **Status:** DB supports controllable views; Created/Updated sorting does not prove a timestamp for when a particular mention was created. Current exact event-order parity remains unverified.
- **OG opportunity:** show stable, explicit ordering and the source block/page explaining each relationship. Only offer chronological sorts for timestamps actually supplied, with their precise meaning.
- **Decision:** high-fit read-only review candidate. Needs complete occurrence/provenance payload rather than a bare page-to-page edge. **UI effort:** small/medium; occurrence coverage is the harder contract gate.

### F17 — Orphan asset/reference audit (77 votes)

- **History:** [Opened 2022-04-13](https://discuss.logseq.com/t/view-and-delete-orphan-assets/6626); a December 2022 script workaround was followed by Unicode/space misclassification reports and a May 2024 correction. A December 2025 reply adds whiteboard coverage. [Related help topic](https://discuss.logseq.com/t/remove-unused-linked-assets/17038) began 2023-04-18 and continued in May 2025.
- **Status:** an asset library is not a complete reference audit. No current release-specific user-facing audit satisfying these cases was established. Forum scripts were **not run or copied**.
- **OG opportunity:** review candidates with supporting references, scan coverage and uncertainty, not a delete button. A file may be used by whiteboards, PDF annotations or plugins even when ordinary Markdown links do not mention it.
- **Decision:** useful later, but not easy or first. Requires Plumber-owned bounded asset inventory, normalized identities and complete reference coverage. **Complexity:** medium/large; no automatic deletion or moving assets.

### F18 — Locking, privacy and shared/personal graph boundaries (69 votes plus related discussion)

- **History:** [Read-only page lock, 2022-02-12](https://discuss.logseq.com/t/ability-to-lock-a-page-as-read-only-view-only/5457); [cross-graph references, 2021-10-28](https://discuss.logseq.com/t/cross-graph-referencing/3182); an older [multi-repository graph proposal](https://github.com/logseq/logseq/issues/770) describes private/shared boundaries.
- **Status:** a UI lock, source permissions, encryption and access control are different guarantees. Existing publishing/export behavior also warrants careful scope; historical [export privacy issue #10514](https://github.com/logseq/logseq/issues/10514) is not proof of a current unresolved vulnerability.
- **Trama decision:** keep a single user's work/personal perspectives as derived views, not security boundaries. No source federation, permission claims, publishing or team isolation from this research. **Complexity:** large for security/federation; simple view filtering remains presentation only.

### F19 — Page/block relationships and richer edge presentation (56 / 38 votes)

- **History:** [Block references in the graph, 2021-12-06](https://discuss.logseq.com/t/the-option-to-show-block-references-on-the-graphview/3814); [relationship types and link styling, 2022-04-29](https://discuss.logseq.com/t/improve-graph-view-relationship-types-link-styling-and-graph-parameters-like-in-cosma/7023). A July 2022 reply points to [Graph Analysis](https://github.com/trashhalo/logseq-graph-analysis); a February 2024 reply links layout-force improvements in 0.10.6, which are not the same as predicate evidence.
- **Status:** the DB roadmap/source includes richer tags/properties graph behavior. Do not claim that native Logseq has no relationship visualization. Exact arbitrary predicate styles and explainable source occurrences need narrower verification.
- **Trama opportunity:** let a person inspect why an edge exists and distinguish source-declared relationship kinds from a computed route. The shortest path already present in Trama is also available in the Graph Analysis plugin; it is not algorithmic novelty.
- **Decision:** strong product direction, conditional on owner-provided relation semantics and occurrence evidence. **UI effort:** medium; data semantics and complete coverage must precede real-graph claims.

### F20 — Adjustable graph depth, settings and layout persistence (40 votes / 5 targeted votes)

- **History:** [Depth request, 2020-12-14](https://discuss.logseq.com/t/graph-view-add-depth-levels-adjustment/67); [manual layout request, 2022-06-07](https://discuss.logseq.com/t/have-nodes-in-graph-view-stay-put-unless-moved/7942). A February 2024 reply distinguishes force settings/pause from saved manual positions.
- **Status:** released DB source already implements depth 1–5 and saved settings. It also contains a time-based graph control. OG 1.0.0 also has N-hops 1–10 and saved graph/force settings. Therefore adjustable depth and generic saved preferences are negative controls, not new missing OG or DB functions. Exact manual-node coordinates and named view collections were not established by those settings functions.
- **Trama decision:** depth is ordinary parity work if needed for Trama, not a unique Logseq gap. Saved local presentation state may help, but scope it separately from canonical data and define privacy/deletion behavior before persistence. **UI effort:** small for bounded depth; medium for robust persisted view/layout lifecycle.

### F21 — Page/graph navigation and returning to context (8 targeted votes; recent issue)

- **History:** [Sidebar-from-graph question, 2023-02-17](https://discuss.logseq.com/t/is-it-possible-to-open-a-page-in-the-sidebar-from-the-graph-view/15283); [scroll restoration, 2025-12-23](https://discuss.logseq.com/t/back-button-should-restore-previous-scroll-position/34541); [Remember My Block, May 2026](https://discuss.logseq.com/t/plugin-remember-my-block-to-restore-your-position-when-navigating-between-pages/35027); [DB graph-to-page issue #13759, 2026-10-14](https://github.com/logseq/logseq/issues/13759).
- **Status:** DB 2.0.2 already contains selected-node open buttons and activation/preview hooks. The October issue has zero reactions at retrieval and is not proof of a popular absent function. The [Remember My Block plugin](https://github.com/PaulNoth/logseq-remember-my-block) documents long-page/journal limitations and session-only positions.
- **Trama opportunity:** keep graph/detail/route context and restore the actual user view when navigating. Trama already has a details panel and bounded history; camera and scroll are not currently stored. This is a precise improvement to our app, not proof Logseq lacks all navigation.
- **Decision:** small synthetic-first UX candidate, with keyboard/focus and explicit reset semantics. A future open-in-Logseq action needs a supported, bounded owner/source link contract.

### F22 — Capture, widgets and audio (26 / 26 votes)

- **History:** [Native capture, 2021-12-17](https://discuss.logseq.com/t/native-quick-capture-clipper/4037); [phone widget, 2022-02-25](https://discuss.logseq.com/t/phone-widget-for-quick-capture-and-reference/5762). DB changelog entries in 2025 describe newer capture/widget workflows.
- **Status:** DB already documents native capture paths; OG/platform parity varies. These are not universally missing Logseq capabilities.
- **Trama decision:** exclude canonical capture/writes from this plan. A future explicit handoff is different from writing files or mutating DB. **Complexity:** medium/large across platforms; not required for the graph sidecar.

### F23 — Background sync and collaboration (15 targeted votes / qualitative team requests)

- **History:** [Collaboration question, 2022-05-30](https://discuss.logseq.com/t/collaboration-question/7756) and [background mobile sync, 2023-04-24](https://discuss.logseq.com/t/logseq-mobile-sync-in-background/17214). The [2024 Sync guide](https://blog.logseq.com/how-to-setup-and-use-logseq-sync/) distinguishes single-user sync from collaboration. [2026 worker-sync notes](https://discuss.logseq.com/t/logseq-db-changelog/30013/35) describe substantial DB progress.
- **Status:** a dated OG sync complaint does not describe every current DB client. Public maturity remains testing, with the source-date conflicts noted above.
- **Trama decision:** do not build another sync or collaboration engine. Keep source lifecycle/freshness in Plumber and product boundaries explicit; Brain remains an independent consumer, not a Trama dependency. **Complexity:** large; outside the easy OG lane.

### F24 — Whiteboards, mindmaps and visual organization (27 votes for mindmaps)

- **History:** [Mindmap request, 2021-01-14](https://discuss.logseq.com/t/possibility-to-create-mindmaps/144); OG later has whiteboards, while the [DB changes guide][DB-CHANGES] explicitly says built-in whiteboards/Excalidraw were removed. The October roadmap lists whiteboard work without proving a current release.
- **Status:** an actual product-line difference, not evidence that OG lacks visual boards. A graph renderer is not a full whiteboard editor.
- **Trama decision:** a future derived layout/outline might fit; authoring boards, drawings and canonical edits is a separate project. Do not discard OG board content or claim an unused asset based on incomplete board coverage. **Complexity:** medium/large.

### F25 — Migration confidence and users who choose OG (qualitative, not a vote rank)

- **History:** [Leaving Logseq, 2026-04-06](https://discuss.logseq.com/t/leaving-logseq-alternative-suggestions/34942) contains 62 posts in the metadata snapshot; [staying on OG, 2026-07-11](https://discuss.logseq.com/t/is-anyone-planning-to-use-og-version-indefinitely/35091) contains 51 posts through October 20.
- **Evidence limit:** these are selected public accounts, not a churn rate, survey or proof all users dislike DB. Preferences include plain files, trust in sync and existing workflows.
- **Trama direction:** make remaining on OG a supported product goal to evaluate, with no compulsory import or DB conversion. Reuse the same Trama use cases over separately admitted Plumber modes; never fork domain logic into a second direct OG adapter.

## 5. Trama baseline and repository responsibilities

At research time public Trama `main` is
`51ddc684249d6e8c02ba991e23a972f8a0a58ba1` ([source](https://github.com/MarcoPorcellato/matryca-trama/tree/51ddc684249d6e8c02ba991e23a972f8a0a58ba1)).
It contains the fictional demo, filters, node details, bounded Back/Forward,
Focus connections and shortest paths. [PR #43](https://github.com/MarcoPorcellato/matryca-trama/pull/43)
adds selected-page endpoint shortcuts at
`328c8f3b95dca87d66fe957038c24d009678153d`; it remains a separate draft,
not a main/release capability. That implementation tranche is already delivered;
this research must not duplicate it.

| Owner | Responsibility for the proposed work |
| --- | --- |
| Parser | Pure OG parsing through its published interface. Preserve source facts and bounded coverage; no Trama UI or direct consumer coupling. |
| Plumber | The unconditional Logseq gateway for OG and DB: source adapters, identities, provenance, complete bounded reads and versioned public capability/data contracts. |
| Trama | UI, derived views, explanation/review use cases and application composition over its own port and admitted Plumber contracts. No direct Parser/Logseq/SQLite/Markdown source access. |
| Brain | Separate Plumber consumer. It must not need Trama or know Parser. No Brain private code or model runtime is introduced here. |

Accepted direction: **OG: Logseq OG → Parser → Plumber → Trama**;
**DB: official Logseq DB host → Plumber → Trama**. Brain substitutes for Trama
as an independent consumer in either route. The direction is ownership, not
current runtime compatibility. [Accepted gateway ADR][TRAMA-GATEWAY]

The current [Trama admission record][TRAMA-ADMISSION] admits only the exact
synthetic read/topology capsule. Titles/text/properties require additional
payload evidence/admission; assets, occurrence links, hierarchy, source-open
handles and freshness may need further explicit capabilities. A feature's data
requirements must be audited against actual published owner artifacts, not an
invented transport or copied schema. Native DB remains a separate qualification. Existing core
[`TopologyNode` values](https://github.com/MarcoPorcellato/matryca-trama/blob/51ddc684249d6e8c02ba991e23a972f8a0a58ba1/packages/core/src/trama_core/graph_values.py#L65-L75)
already have `parent_id` and `ordinal`; these content-free fields are not proof
of an admitted labelled OG outline. Audit existing fields before requesting a
new owner capability.

The Matryca Knowledge MCP reported **degraded** with a last successful refresh
on 2026-10-01 and no configured Trama source in that snapshot. It was used only
for orientation; exact Trama GitHub/source evidence controls this dossier.
No stale projection was promoted to a live contract decision.

Trama remains **source-available under PolyForm Noncommercial 1.0.0**, not open
source. Commercial rights and the lawyer-reviewed contributor-agreement hold
remain unchanged. Research demand creates no license, external-contribution or
release exception. [Clean Architecture standard][TRAMA-ARCH]

### 5.1 Current OG controls verified in the tagged release

The OG 1.0.0 source puts graph UI in `components/page.cljs`, not the guessed
`components/graph.cljs`. Its [graph controls](https://github.com/logseq/og/blob/1.0.0/src/main/frontend/components/page.cljs#L576-L768)
include filters, forces and PNG export. The [N-hops control](https://github.com/logseq/og/blob/1.0.0/src/main/frontend/components/page.cljs#L673-L687)
ranges 1–10; [selection/hop state](https://github.com/logseq/og/blob/1.0.0/src/main/frontend/components/page.cljs#L787-L841)
is distinct from graph settings written to the source graph's configuration.
Trama must not copy that write behavior into an assumed read-only feature.

OG also has [query-table column/sort behavior](https://github.com/logseq/og/blob/1.0.0/src/main/frontend/components/query_table.cljs#L64-L110)
and [sidebar/navigation tools](https://github.com/logseq/og/blob/1.0.0/src/main/frontend/components/container.cljs#L418-L477).
Therefore graph depth, basic property tables, favorites, a sidebar and virtual
namespaces are **not missing OG features**. Trama should only offer them when
an integrated or easier workflow adds value. This source verification resolves
the earlier wrong-path 404; it does not runtime-test OG on any platform.

## 6. OG parity lane: value without migration

**Owner steering incorporated:** offer easy newer experiences to people who
retain OG. Require neither DB conversion nor a direct source reader in Trama.

The complexity estimates below are engineering judgments, not measured delivery
times. XS/S refer to presentation work on already available fixture/data values;
they do not imply the real-graph admission is complete. M/L indicates new data,
coverage or lifecycle work as well as UI work.

| Candidate | Value for an OG user | Existing alternatives / risk of duplication | UI estimate | Required data and separate gates |
| --- | --- | --- | --- | --- |
| Keep exact exploration context when navigating | Return to where the user was, not just the same node ID | Native/plugin approaches exist; Trama history currently omits camera/scroll | S | Current synthetic diagram suffices for UX prototype; no persistent graph data needed |
| Friendly read-only property/status review | Table and filters without requiring users to write queries or migrate | OG queries/plugins already exist; DB tables are not novel | S–M | Admitted page/block/property payload and explicit missing-value/type semantics |
| Stable reference panel with “why linked” | Review relationships and retain source context | Ordinary backlinks and DB sort views already exist | S–M | Complete occurrence/provenance payload; chronology only if supplied |
| Virtual namespace/outline browsing | Navigate existing hierarchy in one Trama workspace | Do not confuse OG namespace tree, DB Library or actual directories | S–M | Source-bound hierarchy/order via Plumber; no moves or renames |
| Alias-aware visual noise reduction | One visual identity with explainable aliases | Existing page exclusion is not alias canonicalization | S–M | Explicit alias targets, collision rules and provenance; no title-based identity guesses |
| Review saved views / readable graph presets | Reuse useful presentation choices | DB already saves settings; arbitrary named layouts not verified | S initially | In-memory synthetic presets first; persistence needs its own privacy/lifecycle design |
| Orphan-asset candidate review | Understand storage and references safely | Existing libraries/scripts; hidden references make deletion dangerous | M–L | Asset inventory + complete reference coverage; no deletion in this lane |

A visual task/status board, new search builder or graph depth slider may be
reasonable Trama parity work after comparison with current OG controls. They
are not automatically unmet community features. Full DB property inheritance,
RTC, editors, mobile plugin runtimes, canonical writes and two-way mirror sync
are outside this easy lane.

### 6.1 Recommended OG-specific subsets and data contracts

- **Page-body filtering with ancestor context:** retain matched blocks and
  their source ancestry, rather than pretending a separate query result is an
  in-place page filter. The Filter Page plugin is an alternative to compare.
  Needs content, tags/properties, ordered hierarchy and complete coverage.
- **Reference review:** begin with source-page name, journal date where explicit,
  and physical block order. OG linked-reference filters already exist. Do not
  infer a block-created timestamp from filesystem modification time.
- **Read-only property/task review:** make common sorts/grouping discoverable
  without requiring a query language, rather than duplicate OG's table engine.
  Preserve raw OG values alongside any view labels; do not convert them to DB
  classes or rewrite source syntax.
- **Alias clarity:** show original aliases and candidate targets, including
  ambiguity. A visual canonicalization option needs owner-approved identity
  semantics; identical names alone never establish identity.
- **Time filtering:** possible only for trustworthy source timestamps. DB's
  created-at graph control is existing behavior; OG field availability and its
  meaning must be proved through Plumber first.

All five subsets use the same Trama-owned use-case boundary over Plumber. No
OG-only domain fork or direct Parser reader is introduced. A source missing a
required capability must show an explicit unavailable/partial state; no DB
fallback, inferred timestamps or guessed aliases may make the display seem
complete. Compare UX ideas, not copied Logseq implementation code; code reuse
would require a separate license and architecture assessment.


## 7. Prioritization and acceptance rules

Do not assign a precise numeric ROI score without evidence. Use this order:

1. **Fit:** does the user task belong to Trama and preserve source ownership?
2. **Readiness:** can the current admitted fixture/contract support it honestly?
3. **Evidence:** is the need repeated/high-vote/recent, and what is already solved?
4. **Marginal value:** what does Trama improve beyond a native feature or plugin?
5. **Risk and scope:** data completeness, privacy, writes, persistence and cost.

Initial recommendation for Astra: first select one small, visible synthetic UX
slice; design the strongest OG read-only parity surface in parallel on paper;
then request the smallest necessary Plumber capability evidence. Treat asset
cleanup and full reader/editor/sync features as later or out of scope. This is
a proposal, not execution authorization.

Every candidate card must state source topics, product/channel status, an
observable user outcome, fixture cases, required fields, owner, no-data behavior,
known alternatives, acceptance evidence and a stop condition. A synthetic pass
cannot be renamed a real OG/DB pass. A query result or edge must explain
inclusion, source and completeness rather than imply certainty.

No source code, dependency, qualification workflow, MA tooling or runtime is
changed by this dossier. No new producer/comparator/real-graph attempt is part
of the plan. The broader programme remains gated independently.

## 8. Astra xhigh proposed delivery plan

**Planning review:** GPT-6 Astra xhigh returned **PASS_WITH_NOTES** after
reading the full dossier and canonical Trama boundaries. Its pre-plan input
SHA-256 was `6d408cdd8c3ad3d4a94fac74616c4b48474b678583b4dc725982ca715834a667`.
That hash identifies the research input, not this document after insertion.
The plan below includes its subsequent CI-trigger clarification. This is an
implementation proposal, not a replacement for accepted repository contracts.

### 8.1 Audit conclusion and planning boundary

The dossier supports a staged Trama exploration programme, with a specific
goal of helping people remain on OG. It does not establish a backlog of 120
missing features. Retain the released-source negative controls: OG and DB
already provide graph-depth controls and saved settings; OG has query tables;
DB has graph-opening hooks and a time control. Alias PR #11760 was closed
without merging. None establishes runtime compatibility with Trama.

Existing Trama topology values already contain `parent_id` and `ordinal`.
Content-free synthetic hierarchy is therefore available. A readable OG outline
still requires admitted labels/content, source semantics and mode-specific
evidence. Do not request a duplicate hierarchy contract before auditing what
the owner already supplies.

The recommended first delivery is **session-only restoration of exploration
context**. It improves Trama's existing experience using available fictional
data and avoids making properties, aliases or occurrences appear available
before admission. It is a Trama UX improvement, not proof of an upstream gap.

### 8.2 Proposed priority and dependency order

1. Restore camera and scrolling context in the current synthetic demo.
2. Establish the smallest evidence package for read-only OG property/status
   review, then validate that experience with fictional data.
3. Add ordered outline and page-body filtering with ancestor context.
4. Add source-explained reference review.
5. Add alias-aware presentation after identity semantics are established.
6. Consider asset/reference candidate review only after coverage is sufficient.

This order puts ownership, available evidence and reusable prerequisites before
votes. Property/status review is the first proposed OG parity surface because
it can offer a discoverable task without requiring a query language and aligns
with the accepted payload direction. Its scope remains conditional on the
actual published artifact.

Section 6 estimates cover presentation only. Payload admission, completeness,
source-version qualification and integration are additional work. If owner
evidence favours another subset, record the reason and review the revised order;
do not fill missing fields by inference.

### 8.3 Slice 1 — Return to the previous exploration view

**User outcome:** Back/Forward restores camera centre, zoom and document/list/
detail scrolling alongside selection, filters, scope and path endpoints.

Likely changes are `apps/synthetic_demo/web/state.js`,
`apps/synthetic_demo/web/app.js`, `tests/demo/test_state.cjs` and demo docs.
Preserve `initialHistory`, `historyState` and `reduceHistory` responsibilities.
Couple each entry with a nullable presentation snapshot; keep `historyState`
returning the existing semantic view. DOM/renderer capture and restore belong
in `app.js`; pure history bookkeeping remains in `state.js`.

Capture the departing view before navigation. Restore after rendering the
destination without a later automatic fit overriding it. Camera/scroll changes
update the current entry, without adding navigation steps. Preserve search
coalescing, forward truncation, no-op behaviour and the 100-entry bound. Reset
and reload clear captures. Exclude browser storage, source configuration writes,
named bookmarks and saved manual node coordinates.

Cases: Back/Forward after pan/zoom; search coalescing without overwriting its
predecessor; branching; eviction; empty results; Focus; path endpoints; absent
renderer; invalid captures; resized layouts. Clamp scroll to available content
and retain usable keyboard focus when controls become disabled.

Acceptance requires an observed round trip at a fixed viewport, followed by a
narrow-layout check. The same semantic view returns with captured presentation;
reduced motion and keyboard navigation remain usable. A synthetic pass proves
only the demo behaviour. PR #43 shortcuts remain independently tracked and
must not be reimplemented.

### 8.4 Slice 2 — Resolve the payload prerequisite on paper

Before adding a content-backed consumer, compare the intended property/status
task against Plumber's published owner artifacts. The accepted
`plumber.graph.payload.read/v1` decision establishes a direction, not a released
implementation.

Request the minimum evidence for bounded page/subtree labels and declared
properties: immutable artifacts, schema/profile versions, fixtures/TCKs,
provenance, supported modes/versions, completeness and bounds behaviour, and
compatibility with required read/topology profiles. Require exact graph/session/
source-revision coherence across combined results.

Plumber owns source interpretation and normalization. Ask it to document missing
versus empty values, value types, raw source values, task/status meaning and
unsupported cases. Trama may choose display labels and presentation rules; it
must not invent OG task semantics, map arbitrary values into DB classes or copy
owner schemas.

Exit: a capability matrix in this dossier, listing available/missing evidence,
owner and next gate for each required input. An incomplete matrix blocks the
corresponding consumer work. This slice sends no requests or changes to another
repository without separate authorization.

### 8.5 Slice 3 — Fictional property/status review, then separate integration

Once semantics are explicit and expanded synthetic scope is approved, prototype
one read-only table with a small named set of filters/sorts. Show raw values,
missing-value states and why each row appears. Do not begin with a board, query
language, editor or universal search engine.

Possible Trama-owned modules are `packages/core/src/trama_core/review_values.py`
and `review.py`, with `tests/core/` coverage. These are conditional internal
locations, not admitted packages or Plumber interfaces. Input is a bounded,
source-bound review selection; output is a presentation-independent result.
Freeze the exact internal interface after the artifact audit. Keep
`KnowledgeGraphGateway.snapshot()` content-free.

Reusable filtering/grouping and inclusion decisions belong below `apps/`.
`apps/synthetic_demo/scenario.py` and `presentation.py` may supply fictional
annotations and present core-derived results. The static demo can embed results
for a bounded set of fixture choices. A new application runtime requires its
own design; do not introduce an unreviewed backend or duplicate business rules
in browser code.

Cases: unknown/custom statuses, absent versus empty properties, multiple values,
mixed types, duplicate labels with distinct identities, hostile text and stable
ties. Acceptance: an OG-oriented user reviews the fictional task without writing
a query, understands omissions and returns to context. No OG data has been read.

Only separate artifact admission and implementation approval may allow
`packages/plumber-client/src/trama_plumber_client/` mapping changes, with client
and architecture tests. Current synthetic-root guards remain intact until an
explicitly reviewed replacement scope exists. Apply the CI-publication gate
in Section 8.8 before any core/client PR.

### 8.6 Later slices reuse the same boundaries

**Outline/body filtering:** reuse qualified ordered hierarchy and separately
admitted content. Retain ancestors and distinguish structural context from
matches. Cases include deep nesting, empty pages, repeated headings, Unicode
and incomplete/changed revisions. Acceptance is locating a fictional block and
returning without losing context. No file organization or source edits follow.

**Reference explanations:** require occurrence/provenance evidence before
showing source passages or occurrence counts. A bare `ReferenceEdge` is not a
mention event. Cases include repeated mentions, page/block references, self-links,
missing dates and inconsistent revisions. Begin with explicit source/order
sorts; chronology needs supplied timestamps with known meaning.

**Aliases:** require Plumber's identity and ambiguity rules. Cases include several
aliases for one identity, equal titles for different identities, conflicts,
cycles and references crossing collapsed nodes. Retain source identities and
explanations. Ambiguity stays visible; no silent page merge follows.

Each slice needs an observable task, focused fixtures and independent exit
review. An earlier successful slice does not admit its successor.

### 8.7 Additional owner evidence and source-mode gates

Request only capabilities the selected slice consumes. References need occurrence
coverage/provenance; aliases need identity mappings; opening sources needs a
bounded supported handle; assets need inventory identities and coverage across
supported Markdown, boards, annotations and other reference forms. These are
evidence requirements, not invented wire API names.

For assets, distinguish unreferenced within a complete declared scope from safe
to delete. Unknown coverage prevents an orphan claim. Distinguish source
revision from elapsed age; filesystem timestamps cannot substitute for missing
mention/creation times.

OG follows Parser and Plumber; DB follows its official host and Plumber. Trama
consumes Plumber and Brain remains independent. OG qualification can proceed
independently when separately authorized. DB needs its own supported-host and
profile evidence, without Markdown fallback. No real graph is accessed here.

### 8.8 Review, stop conditions and deferred work

Each later authorized implementation uses focused behaviour tests, affected
architecture/demo validators and appropriate hosted checks. Verify visible
browser behaviour where required. Independent GPT-6 Astra Medium reviews the
exact candidate under the current execution profile. Review verdicts describe
that bounded check, never publication or runtime authority.

**CI-publication gate:** before pushing or opening/updating any PR touching
core, client or qualification-input paths, inspect effective CI triggers.
The current `.github/workflows/plumber-og-consumer-qualification.yml` includes
`tests/core/**` and `tests/client/**` among paths triggering producer probes,
even when the workflow itself is unchanged. Proceed only with separate explicit
authority for those runs, or an owner-reviewed CI-isolation route preserving
required checks and protections. Ordinary synthetic-UI approval does not
authorize these probes. The proposed Section 8.5 paths remain conditional.
No workflow change or additional execution is authorized by this study.

Stop on owner-artifact mismatch, absent admission, incompatible profiles,
uncertain coverage, changed source revisions, architecture-policy disagreement
or a requirement to read canonical storage directly. Optional missing values
may show unavailable states; required failures must not masquerade as complete
results.

Defer native EPUB/PDF readers, long-form/Vim editors, sync providers,
collaboration, mobile/plugin runtimes, reminders, calendar writes, canonical
capture, migrations, automatic asset cleanup and all source writes. Persisted
views and exports need separate privacy/lifecycle designs.

This study authorizes **no feature implementation, producer/comparator/MA
attempt, installation, real-runtime qualification, release or automatic merge**.
Future execution must select one bounded slice and obtain applicable approval.

## Appendix A. Complete 120-topic vote sample

This is the complete **metadata sample**, not 120 verified missing features.
Titles are source identifiers, votes are the captured counts, and tags are
observed forum labels rather than our status verdict. Dates use the source's
UTC calendar day for unambiguous reproduction; user-facing research date is
Europe/Rome. Ranks are ordinal in the captured response order; tied votes are
not ordered as a preference judgment.

| Rank | Topic / source | Votes | Created | Last post | Observed tags |
| --- | --- | ---: | --- | --- | --- |
| 1 | [Support epub format ebooks](https://discuss.logseq.com/t/support-epub-format-ebooks/2010) | 285 | 2021-08-10 | 2026-06-13 | estimate-very-large |
| 2 | [Add support for customisable TODO keywords](https://discuss.logseq.com/t/add-support-for-customisable-todo-keywords/696) | 263 | 2021-03-30 | 2024-08-02 | done-with-db-version, on-roadmap |
| 3 | [Longform writing in Logseq](https://discuss.logseq.com/t/longform-writing-in-logseq/3527) | 248 | 2021-11-19 | 2025-09-07 | on-roadmap, estimate-very-large |
| 4 | [Vim-mode Powerful Shortcuts](https://discuss.logseq.com/t/vim-mode-powerful-shortcuts/275) | 221 | 2021-02-03 | 2024-08-25 | estimate-very-large |
| 5 | [PDF annotation on mobile devices](https://discuss.logseq.com/t/pdf-annotation-on-mobile-devices/4449) | 200 | 2022-01-05 | 2024-10-12 | — |
| 6 | [Plugin Support for iOS & Android Apps](https://discuss.logseq.com/t/plugin-support-for-ios-android-apps/10109) | 147 | 2022-08-25 | 2025-11-14 | — |
| 7 | [PLEASE fix the search 💙](https://discuss.logseq.com/t/please-fix-the-search/3113) | 142 | 2021-10-23 | 2024-07-10 | done, estimate-very-large |
| 8 | [Filters for note body, not just backlinks](https://discuss.logseq.com/t/filters-for-note-body-not-just-backlinks/1305) | 140 | 2021-06-21 | 2024-09-23 | estimate-large |
| 9 | [Sync on iOS with OneDrive, Dropbox, GoogleDrive, iCloud](https://discuss.logseq.com/t/sync-on-ios-with-onedrive-dropbox-googledrive-icloud/4685) | 130 | 2022-01-12 | 2026-03-30 | estimate-very-large |
| 10 | [Outline Overview for sidebar](https://discuss.logseq.com/t/outline-overview-for-sidebar/740) | 121 | 2021-04-06 | 2024-08-12 | estimate-large |
| 11 | [Proposal: Changing How Namespaces Function in Logseq](https://discuss.logseq.com/t/proposal-changing-how-namespaces-function-in-logseq/3727) | 114 | 2021-12-01 | 2024-03-15 | — |
| 12 | [Pandoc plugin for exporting & Export to PDF](https://discuss.logseq.com/t/pandoc-plugin-for-exporting-export-to-pdf/1247) | 110 | 2021-06-16 | 2025-02-09 | estimate-large |
| 13 | [Hide aliases circles in Graph View](https://discuss.logseq.com/t/hide-aliases-circles-in-graph-view/5455) | 109 | 2022-02-12 | 2026-04-16 | — |
| 14 | [Mermaid diagram render support](https://discuss.logseq.com/t/mermaid-diagram-render-support/582) | 104 | 2021-03-15 | 2025-11-06 | done |
| 15 | [Basic UI Settings e.g. Font Size](https://discuss.logseq.com/t/basic-ui-settings-e-g-font-size/2946) | 104 | 2021-10-13 | 2025-03-08 | — |
| 16 | [Introduce Kanban boards as a new primitive](https://discuss.logseq.com/t/introduce-kanban-boards-as-a-new-primitive/1095) | 100 | 2021-06-02 | 2023-12-06 | — |
| 17 | [Task notifications](https://discuss.logseq.com/t/task-notifications/6638) | 86 | 2022-04-13 | 2026-08-25 | — |
| 18 | [Outlines Collapsed by Default](https://discuss.logseq.com/t/outlines-collapsed-by-default/300) | 84 | 2021-02-05 | 2022-11-22 | — |
| 19 | [[Partial Done] Add tabbed windows to desktop client / Multiple instances of Logseq](https://discuss.logseq.com/t/partial-done-add-tabbed-windows-to-desktop-client-multiple-instances-of-logseq/429) | 83 | 2021-02-24 | 2026-04-12 | done |
| 20 | [Add search operator / filters for the search box](https://discuss.logseq.com/t/add-search-operator-filters-for-the-search-box/74) | 83 | 2020-12-16 | 2023-03-17 | — |
| 21 | [Auto delete empty journal](https://discuss.logseq.com/t/auto-delete-empty-journal/1825) | 81 | 2021-08-01 | 2025-03-21 | — |
| 22 | [Sort linked references](https://discuss.logseq.com/t/sort-linked-references/10391) | 78 | 2022-09-01 | 2024-05-31 | — |
| 23 | [Google Calendar Sync](https://discuss.logseq.com/t/google-calendar-sync/830) | 78 | 2021-04-26 | 2025-03-29 | — |
| 24 | [Please add pdf search word at pdf and page search word at page, use shortcut ctrl+F](https://discuss.logseq.com/t/please-add-pdf-search-word-at-pdf-and-page-search-word-at-page-use-shortcut-ctrl-f/1988) | 78 | 2021-08-09 | 2024-09-07 | done |
| 25 | [View and delete orphan assets](https://discuss.logseq.com/t/view-and-delete-orphan-assets/6626) | 77 | 2022-04-13 | 2025-12-03 | — |
| 26 | [Option to disable auto-close parenthesis?](https://discuss.logseq.com/t/option-to-disable-auto-close-parenthesis/2531) | 73 | 2021-09-13 | 2025-09-16 | — |
| 27 | [Allow for customized Zotero import fields](https://discuss.logseq.com/t/allow-for-customized-zotero-import-fields/3526) | 73 | 2021-11-19 | 2023-09-07 | — |
| 28 | [Portable Windows Installer](https://discuss.logseq.com/t/portable-windows-installer/4465) | 70 | 2022-01-05 | 2025-01-23 | — |
| 29 | [Ability to lock a page as read-only/view-only](https://discuss.logseq.com/t/ability-to-lock-a-page-as-read-only-view-only/5457) | 69 | 2022-02-12 | 2025-11-12 | — |
| 30 | [Find and replace a word in multiple occurrences](https://discuss.logseq.com/t/find-and-replace-a-word-in-multiple-occurrences/1777) | 67 | 2021-07-28 | 2026-01-01 | — |
| 31 | [Feature request : Creation of Folders and subfolders, will make knowledge management more feasible](https://discuss.logseq.com/t/feature-request-creation-of-folders-and-subfolders-will-make-knowledge-management-more-feasible/3446) | 67 | 2021-11-14 | 2025-12-20 | — |
| 32 | [Local (on-server) storage for self-hosted Logseq](https://discuss.logseq.com/t/local-on-server-storage-for-self-hosted-logseq/6613) | 61 | 2022-04-12 | 2026-02-02 | — |
| 33 | [Export PDF with Highlights / Save highlights to PDF file](https://discuss.logseq.com/t/export-pdf-with-highlights-save-highlights-to-pdf-file/6076) | 61 | 2022-03-15 | 2024-05-20 | — |
| 34 | [Table creation interface (not query table)](https://discuss.logseq.com/t/table-creation-interface-not-query-table/1974) | 58 | 2021-08-09 | 2026-05-21 | — |
| 35 | [Progressive Web App with full features](https://discuss.logseq.com/t/progressive-web-app-with-full-features/15112) | 58 | 2023-02-12 | 2025-09-29 | — |
| 36 | [Merge pages into one page](https://discuss.logseq.com/t/merge-pages-into-one-page/506) | 58 | 2021-03-04 | 2024-02-26 | — |
| 37 | [The option to show block references on the graphview](https://discuss.logseq.com/t/the-option-to-show-block-references-on-the-graphview/3814) | 56 | 2021-12-06 | 2024-04-22 | — |
| 38 | [Collapse namespace prefixes](https://discuss.logseq.com/t/collapse-namespace-prefixes/199) | 56 | 2021-01-23 | 2023-11-03 | — |
| 39 | [Support for Zotero 6 Notes import](https://discuss.logseq.com/t/support-for-zotero-6-notes-import/2087) | 56 | 2021-08-15 | 2022-05-10 | — |
| 40 | [Additional repeater options](https://discuss.logseq.com/t/additional-repeater-options/1315) | 54 | 2021-06-23 | 2025-09-02 | — |
| 41 | [Readwise integration](https://discuss.logseq.com/t/readwise-integration/251) | 52 | 2021-02-02 | 2023-11-24 | done |
| 42 | [Enhancement of aliases](https://discuss.logseq.com/t/enhancement-of-aliases/14466) | 52 | 2023-01-21 | 2023-09-21 | — |
| 43 | [Moving a block to another page/location, or converting it to a page (and vice versa)](https://discuss.logseq.com/t/moving-a-block-to-another-page-location-or-converting-it-to-a-page-and-vice-versa/156) | 52 | 2021-01-17 | 2022-04-15 | — |
| 44 | [Hierarchy can be augmented by tree structure with collapse buttons](https://discuss.logseq.com/t/hierarchy-can-be-augmented-by-tree-structure-with-collapse-buttons/3282) | 51 | 2021-11-04 | 2023-08-16 | — |
| 45 | [Better math experience](https://discuss.logseq.com/t/better-math-experience/69) | 50 | 2020-12-15 | 2025-08-04 | — |
| 46 | [Logseq and Obsidian.md Colaboration Projects](https://discuss.logseq.com/t/logseq-and-obsidian-md-colaboration-projects/473) | 50 | 2021-02-28 | 2022-09-04 | — |
| 47 | [Treat Markdown checkboxes as LS tasks](https://discuss.logseq.com/t/treat-markdown-checkboxes-as-ls-tasks/965) | 49 | 2021-05-15 | 2024-12-15 | — |
| 48 | [Add date ranges](https://discuss.logseq.com/t/add-date-ranges/1610) | 47 | 2021-07-17 | 2023-08-01 | — |
| 49 | [Block Timestamps](https://discuss.logseq.com/t/block-timestamps/3346) | 46 | 2021-11-09 | 2024-08-21 | done-with-db-version |
| 50 | [Support diagrams.net (draw.io) for diagramming](https://discuss.logseq.com/t/support-diagrams-net-draw-io-for-diagramming/4611) | 46 | 2022-01-09 | 2023-09-02 | — |
| 51 | [WYSIWYG editing mode](https://discuss.logseq.com/t/wysiwyg-editing-mode/2216) | 43 | 2021-08-23 | 2026-05-17 | on-roadmap |
| 52 | [Audio recorder option ( / )](https://discuss.logseq.com/t/audio-recorder-option/3778) | 43 | 2021-12-03 | 2024-03-31 | — |
| 53 | [Add a done date to done tasks that is query-able](https://discuss.logseq.com/t/add-a-done-date-to-done-tasks-that-is-query-able/5196) | 42 | 2022-02-02 | 2025-02-09 | db-version, done-with-db-version |
| 54 | [PDF annotation in Logseq](https://discuss.logseq.com/t/pdf-annotation-in-logseq/1427) | 42 | 2021-07-03 | 2024-05-20 | done, considering |
| 55 | [Calendar plugin should be improved and integrated into Logseq](https://discuss.logseq.com/t/calendar-plugin-should-be-improved-and-integrated-into-logseq/2349) | 42 | 2021-09-01 | 2024-03-08 | — |
| 56 | [Make Advanced Queries reusable](https://discuss.logseq.com/t/make-advanced-queries-reusable/15281) | 41 | 2023-02-17 | 2025-04-17 | — |
| 57 | [Delete a page and also delete its assets](https://discuss.logseq.com/t/delete-a-page-and-also-delete-its-assets/4424) | 41 | 2022-01-04 | 2024-02-25 | — |
| 58 | [Assets reference suggestions](https://discuss.logseq.com/t/assets-reference-suggestions/3868) | 41 | 2021-12-09 | 2024-02-02 | — |
| 59 | [Block reference to allow ((page-name#block-ref-name)) not just UUID](https://discuss.logseq.com/t/block-reference-to-allow-page-name-block-ref-name-not-just-uuid/2746) | 40 | 2021-09-28 | 2026-06-08 | done-with-db-version |
| 60 | [Adding cheklists](https://discuss.logseq.com/t/adding-cheklists/1528) | 40 | 2021-07-12 | 2026-03-23 | — |
| 61 | [Nextcloud integration](https://discuss.logseq.com/t/nextcloud-integration/3460) | 40 | 2021-11-15 | 2024-09-06 | — |
| 62 | [PDF - Option to open PDF in directory or in default viewer](https://discuss.logseq.com/t/pdf-option-to-open-pdf-in-directory-or-in-default-viewer/4156) | 40 | 2021-12-23 | 2023-09-04 | — |
| 63 | [Graph view : add depth levels adjustment](https://discuss.logseq.com/t/graph-view-add-depth-levels-adjustment/67) | 40 | 2020-12-14 | 2023-06-22 | — |
| 64 | [Automatically link Unlinked References [Done with Plugin]](https://discuss.logseq.com/t/automatically-link-unlinked-references-done-with-plugin/699) | 40 | 2021-03-30 | 2022-10-30 | done |
| 65 | [Hide namespace parents](https://discuss.logseq.com/t/hide-namespace-parents/1595) | 39 | 2021-07-16 | 2025-01-23 | done-with-db-version |
| 66 | [Prompt user to confirm deleting block when an existing block reference is linked to the block](https://discuss.logseq.com/t/prompt-user-to-confirm-deleting-block-when-an-existing-block-reference-is-linked-to-the-block/1638) | 39 | 2021-07-19 | 2024-05-22 | — |
| 67 | [Flashcards/SRS Improvements](https://discuss.logseq.com/t/flashcards-srs-improvements/5932) | 38 | 2022-03-08 | 2024-09-09 | — |
| 68 | [Improve Graph View: Relationship Types, Link Styling and Graph Parameters like in Cosma](https://discuss.logseq.com/t/improve-graph-view-relationship-types-link-styling-and-graph-parameters-like-in-cosma/7023) | 38 | 2022-04-29 | 2024-03-11 | — |
| 69 | [Knowledge Management for Tags / Tag Hierarchies](https://discuss.logseq.com/t/knowledge-management-for-tags-tag-hierarchies/8574) | 38 | 2022-07-06 | 2023-01-26 | — |
| 70 | [Pomodoro - Roam inspired](https://discuss.logseq.com/t/pomodoro-roam-inspired/419) | 38 | 2021-02-23 | 2022-02-22 | — |
| 71 | [Cursor placement within a template](https://discuss.logseq.com/t/cursor-placement-within-a-template/4659) | 36 | 2022-01-11 | 2026-03-26 | — |
| 72 | [NOW / NEXT / LATER tasks workflow](https://discuss.logseq.com/t/now-next-later-tasks-workflow/3703) | 36 | 2021-11-30 | 2025-01-23 | done-with-db-version |
| 73 | [Feature Request: Title independent of namespace path](https://discuss.logseq.com/t/feature-request-title-independent-of-namespace-path/4335) | 36 | 2022-01-01 | 2022-01-02 | — |
| 74 | [Option to ignore certain nodes in the graph](https://discuss.logseq.com/t/option-to-ignore-certain-nodes-in-the-graph/1312) | 35 | 2021-06-22 | 2024-03-19 | done |
| 75 | [Ability to edit Logbook times](https://discuss.logseq.com/t/ability-to-edit-logbook-times/5589) | 34 | 2022-02-18 | 2024-12-15 | — |
| 76 | [Read html documents like pdf](https://discuss.logseq.com/t/read-html-documents-like-pdf/2012) | 34 | 2021-08-10 | 2023-06-13 | — |
| 77 | [[Partial Done] Hide query-table property heading](https://discuss.logseq.com/t/partial-done-hide-query-table-property-heading/4296) | 34 | 2021-12-30 | 2023-04-04 | queries |
| 78 | [Drawing / Excalidraw embed improvements](https://discuss.logseq.com/t/drawing-excalidraw-embed-improvements/921) | 34 | 2021-05-10 | 2022-11-13 | — |
| 79 | [[Plugin Available] 🙏 Word & Character Count?](https://discuss.logseq.com/t/plugin-available-word-character-count/611) | 34 | 2021-03-18 | 2021-11-10 | done |
| 80 | [Make PDF Annotation Timeless](https://discuss.logseq.com/t/make-pdf-annotation-timeless/11754) | 32 | 2022-10-19 | 2025-05-10 | — |
| 81 | [In page search/filter](https://discuss.logseq.com/t/in-page-search-filter/6084) | 32 | 2022-03-15 | 2025-03-14 | — |
| 82 | [Image asset as page icon](https://discuss.logseq.com/t/image-asset-as-page-icon/3826) | 32 | 2021-12-06 | 2024-02-08 | — |
| 83 | [Arm64 Native Build](https://discuss.logseq.com/t/arm64-native-build/16125) | 31 | 2023-03-20 | 2025-12-02 | — |
| 84 | [Support subdirs for namespace hierarchy](https://discuss.logseq.com/t/support-subdirs-for-namespace-hierarchy/9763) | 31 | 2022-08-15 | 2024-03-14 | — |
| 85 | [Expanded Zotero import selection](https://discuss.logseq.com/t/expanded-zotero-import-selection/4899) | 31 | 2022-01-21 | 2022-09-28 | — |
| 86 | [PDF annotation: add pin reference in addition to quote reference](https://discuss.logseq.com/t/pdf-annotation-add-pin-reference-in-addition-to-quote-reference/4802) | 31 | 2022-01-17 | 2022-07-11 | pdf |
| 87 | [Allow non-outline (freeform) text](https://discuss.logseq.com/t/allow-non-outline-freeform-text/172) | 31 | 2021-01-20 | 2022-01-20 | — |
| 88 | [Render datalog queries in an editor rather than raw text](https://discuss.logseq.com/t/render-datalog-queries-in-an-editor-rather-than-raw-text/1241) | 30 | 2021-06-16 | 2025-01-23 | done-with-db-version |
| 89 | [Automatic linking](https://discuss.logseq.com/t/automatic-linking/763) | 30 | 2021-04-11 | 2024-07-30 | — |
| 90 | [Copy and paste rich text](https://discuss.logseq.com/t/copy-and-paste-rich-text/5327) | 29 | 2022-02-07 | 2024-08-01 | — |
| 91 | [Syntax for inline properties::](https://discuss.logseq.com/t/syntax-for-inline-properties/10031) | 29 | 2022-08-23 | 2023-11-30 | — |
| 92 | [Better support for obsidian-style Wiki-Links when it comes to displayname & pagename](https://discuss.logseq.com/t/better-support-for-obsidian-style-wiki-links-when-it-comes-to-displayname-pagename/2014) | 29 | 2021-08-10 | 2023-10-28 | — |
| 93 | [Embed local video and add timestamps](https://discuss.logseq.com/t/embed-local-video-and-add-timestamps/3610) | 28 | 2021-11-24 | 2025-01-21 | — |
| 94 | [Add :pages to :default-queries in config](https://discuss.logseq.com/t/add-pages-to-default-queries-in-config/675) | 28 | 2021-03-26 | 2024-10-17 | — |
| 95 | [Reimagining Query Tables (editing, database features, etc.)](https://discuss.logseq.com/t/reimagining-query-tables-editing-database-features-etc/9568) | 28 | 2022-08-08 | 2024-07-22 | queries, done-with-db-version |
| 96 | [Shortcut to focus sidebar/main pane](https://discuss.logseq.com/t/shortcut-to-focus-sidebar-main-pane/2053) | 28 | 2021-08-12 | 2024-03-29 | — |
| 97 | [Add multiple selections (multi cursor) feature in Logseq](https://discuss.logseq.com/t/add-multiple-selections-multi-cursor-feature-in-logseq/16486) | 28 | 2023-03-31 | 2024-02-07 | — |
| 98 | [Introduce UI elements to select spellcheckers](https://discuss.logseq.com/t/introduce-ui-elements-to-select-spellcheckers/14232) | 27 | 2023-01-13 | 2026-07-30 | — |
| 99 | [Password protection for journal](https://discuss.logseq.com/t/password-protection-for-journal/944) | 27 | 2021-05-13 | 2025-08-17 | — |
| 100 | [[Enhancement] Resize the image size that got with area-highlight during PDF reading](https://discuss.logseq.com/t/enhancement-resize-the-image-size-that-got-with-area-highlight-during-pdf-reading/3976) | 27 | 2021-12-14 | 2025-02-02 | — |
| 101 | [Encrypted blocks](https://discuss.logseq.com/t/encrypted-blocks/1957) | 27 | 2021-08-07 | 2024-04-04 | — |
| 102 | [Whiteboard iPad + Apple Pencil Support](https://discuss.logseq.com/t/whiteboard-ipad-apple-pencil-support/17526) | 27 | 2023-05-05 | 2023-11-17 | — |
| 103 | [Relative path for Zotero data directory](https://discuss.logseq.com/t/relative-path-for-zotero-data-directory/4568) | 27 | 2022-01-08 | 2023-10-18 | — |
| 104 | [Option to show page hierarchies above backlinks](https://discuss.logseq.com/t/option-to-show-page-hierarchies-above-backlinks/2170) | 27 | 2021-08-20 | 2023-04-23 | — |
| 105 | [Possibility to create mindmaps](https://discuss.logseq.com/t/possibility-to-create-mindmaps/144) | 27 | 2021-01-14 | 2023-04-14 | — |
| 106 | [Plugins on multiple machines](https://discuss.logseq.com/t/plugins-on-multiple-machines/5639) | 27 | 2022-02-20 | 2022-11-04 | — |
| 107 | [Phone widget for quick capture and reference](https://discuss.logseq.com/t/phone-widget-for-quick-capture-and-reference/5762) | 26 | 2022-02-25 | 2024-12-02 | — |
| 108 | [Discussion: Unify pages and blocks](https://discuss.logseq.com/t/discussion-unify-pages-and-blocks/12872) | 26 | 2022-11-29 | 2024-08-19 | done-with-db-version, estimate-very-large |
| 109 | [Project Pages for Task Mangagement](https://discuss.logseq.com/t/project-pages-for-task-mangagement/1810) | 26 | 2021-07-31 | 2024-08-19 | done-with-db-version |
| 110 | [Native Quick Capture / Clipper](https://discuss.logseq.com/t/native-quick-capture-clipper/4037) | 26 | 2021-12-17 | 2024-04-02 | — |
| 111 | [Cross-graph referencing](https://discuss.logseq.com/t/cross-graph-referencing/3182) | 26 | 2021-10-28 | 2023-10-09 | on-roadmap, considering, planned-for-future |
| 112 | [Web annotation / higlights via text fragments](https://discuss.logseq.com/t/web-annotation-higlights-via-text-fragments/9171) | 25 | 2022-07-24 | 2025-05-19 | — |
| 113 | [Single button filter to show/hide journal pages in linked references](https://discuss.logseq.com/t/single-button-filter-to-show-hide-journal-pages-in-linked-references/4643) | 25 | 2022-01-10 | 2024-12-04 | — |
| 114 | [Make "First day of the week" in the date picker configurable](https://discuss.logseq.com/t/make-first-day-of-the-week-in-the-date-picker-configurable/1920) | 25 | 2021-08-06 | 2023-09-09 | — |
| 115 | [Configurable block background color](https://discuss.logseq.com/t/configurable-block-background-color/415) | 25 | 2021-02-22 | 2022-06-22 | done |
| 116 | [Provide option to disable "lazy-load"](https://discuss.logseq.com/t/provide-option-to-disable-lazy-load/9784) | 24 | 2022-08-16 | 2026-01-05 | — |
| 117 | [Command Line to Export Pages and Data](https://discuss.logseq.com/t/command-line-to-export-pages-and-data/2871) | 24 | 2021-10-06 | 2025-11-27 | done |
| 118 | [Be able to adjust the width of content area](https://discuss.logseq.com/t/be-able-to-adjust-the-width-of-content-area/2749) | 24 | 2021-09-28 | 2023-11-06 | — |
| 119 | [Markdown emojis support](https://discuss.logseq.com/t/markdown-emojis-support/6199) | 23 | 2022-03-22 | 2024-05-09 | — |
| 120 | [Support checkboxes syntax from GitHub Flavoured Markdown](https://discuss.logseq.com/t/support-checkboxes-syntax-from-github-flavoured-markdown/7330) | 23 | 2022-05-11 | 2024-04-08 | — |

## Appendix B. Additional dated topics and verification limits

These targeted topics sit outside the ranked sample or serve as current-status and historical context. Zero votes on a non-request topic is not an absence-of-demand finding.

| Topic / source | Created | Last post | Posts | Votes |
| --- | --- | --- | ---: | ---: |
| [Have nodes in graph view stay put unless moved](https://discuss.logseq.com/t/have-nodes-in-graph-view-stay-put-unless-moved/7942) | 2022-06-07 | 2024-02-06 | 4 | 5 |
| [Graph performance](https://discuss.logseq.com/t/graph-performance/34524) | 2025-12-16 | 2025-12-21 | 2 | 0 |
| [Is it possible to open a page in the sidebar from the graph view?](https://discuss.logseq.com/t/is-it-possible-to-open-a-page-in-the-sidebar-from-the-graph-view/15283) | 2023-02-17 | 2024-12-29 | 13 | 8 |
| [Logseq mobile sync in background](https://discuss.logseq.com/t/logseq-mobile-sync-in-background/17214) | 2023-04-24 | 2026-03-29 | 6 | 15 |
| [Collaboration question](https://discuss.logseq.com/t/collaboration-question/7756) | 2022-05-30 | 2022-10-18 | 12 | 0 |
| [Leaving Logseq - Alternative suggestions?](https://discuss.logseq.com/t/leaving-logseq-alternative-suggestions/34942) | 2026-04-06 | 2026-08-24 | 62 | 0 |
| [Is anyone planning to use OG version indefinitely?](https://discuss.logseq.com/t/is-anyone-planning-to-use-og-version-indefinitely/35091) | 2026-07-11 | 2026-10-20 | 51 | 0 |
| [Introducing the Logseq DB Query Builder!](https://discuss.logseq.com/t/introducing-the-logseq-db-query-builder/34794) | 2026-02-13 | 2026-08-15 | 14 | 0 |
| [Tags vs Pages in the New Logseq DB: A Missed Chance for Unification?](https://discuss.logseq.com/t/tags-vs-pages-in-the-new-logseq-db-a-missed-chance-for-unification/33684) | 2025-10-01 | 2026-04-09 | 12 | 13 |
| [Same name for Tag and Page in the database version?](https://discuss.logseq.com/t/same-name-for-tag-and-page-in-the-database-version/35144) | 2026-08-02 | 2026-08-10 | 10 | 0 |
| [Remove unused / linked assets](https://discuss.logseq.com/t/remove-unused-linked-assets/17038) | 2023-04-18 | 2025-05-12 | 3 | 0 |
| [What's New with Logseq DB - May 16th 2026](https://discuss.logseq.com/t/whats-new-with-logseq-db-may-16th-2026/35020) | 2026-05-16 | 2026-05-16 | 1 | 0 |
| [Logseq DB Android app access?](https://discuss.logseq.com/t/logseq-db-android-app-access/34924) | 2026-03-30 | 2026-09-04 | 4 | 0 |

No private Discord, private graphs, credentials or customer material were read.
No referenced plugin, forum script, application artifact or Logseq source code
was executed. We inspected public text/source and release metadata only.
Plugin compatibility not established in a named product/version remains unknown.
An inaccessible page or an unsuccessful guessed path is not evidence of absence.
The initial OG path guess was corrected using the tagged release source above.
Source implementations were not runtime-qualified.

## Reference anchors

[DB-GUIDE]: https://github.com/logseq/docs/blob/master/db-version.md
[DB-CHANGES]: https://github.com/logseq/docs/blob/master/db-version-changes.md
[DB-RELEASE]: https://github.com/logseq/logseq/releases/tag/2.0.2
[DB-README]: https://github.com/logseq/logseq/blob/master/README.md
[DB-MAY]: https://discuss.logseq.com/t/whats-new-with-logseq-db-may-16th-2026/35020
[DB-GRAPH]: https://github.com/logseq/logseq/blob/533ac4382a7b69baa98de3a973bff90305b212dc/src/main/frontend/components/graph.cljs
[DB-DEPTH]: https://github.com/logseq/logseq/blob/533ac4382a7b69baa98de3a973bff90305b212dc/src/main/frontend/components/graph.cljs#L445-L452
[DB-OPEN]: https://github.com/logseq/logseq/blob/533ac4382a7b69baa98de3a973bff90305b212dc/src/main/frontend/components/graph.cljs#L226-L245
[DB-SETTINGS]: https://github.com/logseq/logseq/blob/533ac4382a7b69baa98de3a973bff90305b212dc/src/main/frontend/components/graph.cljs#L98-L113
[OG-RELEASE]: https://github.com/logseq/og/releases/tag/1.0.0
[NIGHTLY]: https://github.com/logseq/logseq/releases/tag/nightly
[ROADMAP]: https://logseq.io/p/NX4mc_ggEV
[SPLIT]: https://logseq.io/page/b2ad9ce1-9cb7-4436-8083-54cb4516d324/df4dc09d-0a12-4c87-904e-22a9bf4c350a
[TRAMA-GATEWAY]: https://github.com/MarcoPorcellato/matryca-trama/blob/51ddc684249d6e8c02ba991e23a972f8a0a58ba1/docs/decisions/ADR-0006-PLUMBER-GATEWAY-ADOPTION.md
[TRAMA-ADMISSION]: https://github.com/MarcoPorcellato/matryca-trama/blob/51ddc684249d6e8c02ba991e23a972f8a0a58ba1/docs/contracts/PLUMBER_SOURCE_ADMISSION.md
[TRAMA-ARCH]: https://github.com/MarcoPorcellato/matryca-trama/blob/51ddc684249d6e8c02ba991e23a972f8a0a58ba1/docs/standards/CLEAN_ARCHITECTURE.md
