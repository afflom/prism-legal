# Semantic matter implementation

The root PrismPM project selects `holistic.lexlean.toml` and
`src/HolisticApp.lex.tex`. The application graph is executable LexLean: PrismPM
emits its Rust library, native CLI, Core-Wasm guest, browser view, and Hologram.
The generic Text/4 host comes from the pinned SDK fix. It does not implement
legal decisions or substitute a remote language model.

## Matter language and learning

`MatterText.IntakeModel` extracts nonempty lines from actual UTF-8 resource
bytes. Each passage retains source identity, source revision, exact quotation,
and a half-open byte range. Contracts check quotations against the source.
Original wording and reviewed interpretation are separate values.

`MatterNetwork` learns an associative network from current accepted matter
nodes. Each facet has a neuron; distinct features are ASCII-case-folded words
and ordered adjacent word pairs. Each reviewed example strengthens its observed
synapses once. Activation sums those weights and normalizes by the number of
reviewed examples for that facet, comparing fractions exactly. Zero support and
equal best scores for different facets abstain. Feature extraction exceeding
its token boundary also abstains. No seeded legal vocabulary, arbitrary
confidence threshold, pretrained weights, or hidden model calls supply answers.
Corrections remove obsolete training through the current-reference closure.

This is bounded learned lexical association. Punctuation and non-ASCII case
remain significant. Ordered pairs distinguish some wording changes but do not
establish general negation, syntax, semantic entailment, or legal truth. A
suggestion never silently becomes an accepted interpretation. The user reviews
the actual passage and supplies its meaning.

`MatterInference` binds a rule's exact content to reviewed authority,
jurisdiction, and goal references. Authority must have source citations. The
lawyer supplies required `facet = value` conditions, possible exceptions, and an
action. Those conditions are a controlled language, not simulated understanding
of unrestricted legal prose. An assessment is inactive, missing support,
blocked by an observed exception, or supported. Missing conditions become
questions. A supported proposal still requires lawyer review.

Draft strategy text presents the reviewed goal, action, support, and citations.
It is assembled from the current matter, not a generated pleading or invented
legal analysis. A draft's revision and dependency references determine its
freshness. No default jurisdiction, authority, deadline, or remedy is supplied.

## Relative changes and history

`Matter.current` computes a least grounded closure starting from no admitted
nodes, bounded by node count. Only accepted nodes with matching citations and
current dependencies enter the closure. Missing or duplicate identities,
obsolete revisions, changed source bytes, and circular support fail to ground a
conclusion. “Current” means usable in this reviewed context, not proved in court.

`MatterSession` applies commands with expected matter and object revisions.
Edits retain before/after history and original citations. Source replacement
retains the old source version. Rules have structured revision commands so a
plain text edit cannot change an accepted rule's meaning. Reconciliation also
retracts previously accepted conclusions when a new exception becomes current,
even though the exception was absent from the original supporting references.
A lawyer cannot reaccept a conclusion while its rule is unsupported.

Client commands cannot accept authority, rules, or rule-linked legal conclusions;
reader commands cannot mutate the session. These are modeled workflow checks,
not identity verification. A local actor can choose a role and author a new
journal. Shared editing, signed history, access control, and encryption are not
implemented by these checks.

## Persistence and journeys

`MatterJournal` stores a versioned journal with canonical UTF-8 byte-length
framing. Newlines, CRLF, Unicode, BOMs, embedded separators, and NUL bytes survive
save and replay. Invalid lengths, incomplete frames, unsupported commands,
stale revisions, and over-bound input are refused. Corrupt replay does not
return a partially accepted matter. A failed transaction preserves the complete
previous session and journal.

`MatterJourney` selects useful next context: intake, goal, one passage review,
jurisdiction, authority, then strategy assessment. Pending legal conclusions
appear as lawyer review tasks. `MatterWorkspace` exposes 15 operations for
creation, intake, review, assertions, source and rule revisions, strategy,
proposals, restoration, and paginated facet inspection. It selects objects by
unique visible wording rather than asking users to find internal IDs. Ambiguous
selection refuses rather than choosing arbitrarily.

`HolisticApp` declares the forms, plain-language copy, palette, density, file
controls, errors, empty states, and 20 acceptance examples. Unused help and
transport details are collapsed. Facet inspection shows eight items per page;
the lawyer view adds source locations. Control characters are rendered safely
without altering retained source bytes. Long context is explicitly truncated
for presentation while the journal preserves the original.

The Text/4 SDK host sends each command with the last accepted journal. Only a
successful, validated, bounded response replaces it. File restoration goes
through the guest. Refusal, malformed response, cancellation, timeout, and
retired asynchronous reads preserve accepted state. File inputs retain original
bytes across HTML textarea newline normalization until edited. Downloads are
explicit; unsaved-state warnings remain conservative. Nothing is stored in
localStorage, IndexedDB, or a service. Refresh requires reopening the saved file.

## Operational bounds

| Boundary | Limit |
| --- | --- |
| Source text | 8192 UTF-8 bytes, 64 lines |
| Matter | 32 sources, 1024 nodes, 128 rules |
| Network input | 256 split tokens |
| Journal history | 512 commands |
| Native journal decoder | 8 MiB |
| Browser journal | 1 MiB |
| Workspace request / response | 2 MiB / 8 MiB |
| Browser execution | 30 seconds per command |

These are explicit resource bounds, not legal constants. This implementation
serves bounded text matters. PDF, image, audio, email-container decoding,
external authority retrieval, filing, unrestricted drafting, authenticated
multi-user storage, and broad semantic language learning remain outside its
implemented boundary. Unsupported capabilities are not shown as working tools.

## Verification

`MatterLaws` checks revision, provenance, missing support, dependency chains,
cycles, and conflict cases. General laws preserve citations and dependencies on
correction and advance revisions. Additional general theorems state that an
untrained network cannot invent a facet, proposals require review, and refusal
preserves the complete session. Lean checks the declared exact axiom policies.
These properties do not prove legal correctness or complete application safety.

The final application source with source ID
`36126ff11ef2ed8f6e7b58db049afea114d6501795d3b95af9519a08b7c4334c`
and semantic ID
`1b983c3cab7d72580f49e413fb25a6cefce2fcd2772f44b6e40d9ade9ff40e2d`
passed LexLean verification with attestation
`0b710da73bf656fbb28307542f7bddaa0568a5b66ad709bb80dca52e47e2f6e0`.

The generated native library passes 15 tests across `behavior.rs` and
`holistic.rs`. They cover relative edits, transitive invalidation, source
forgery, conflicts, cycles, learned abstention/retraining, exact rule binding,
new exceptions, stale reacceptance, ambiguous actions, replay, and draft freshness.
Patch test dependencies to actual emitted packages rather than editing generated
code:

```sh
cargo test --offline --locked --manifest-path tests/matter/Cargo.toml \
  --config 'patch.crates-io.prism-legal-matter.path="<build>/cargo/package"' \
  --config 'patch.crates-io.prism-stdlib.path="<sdk>/stdlib/generated/package"'
```

`holistic_runtime.mjs` runs all 20 source vectors and unseen framing, Unicode,
control-display, malformed replay, pagination, and resource-boundary inputs
against generated Wasm. `run_browser.mjs` serves only emitted files and runs
`holistic_browser.mjs` through creation, exact file import, passage review,
rule assessment/revision, proposal review, exception/correction propagation,
inspection, save/reopen, failed restoration, and mobile layout.

Those checks pass in development Chromium 154.0.8037.57 with Playwright 1.62.1.
They are distinct from PrismPM's pinned Chromium 157 oracle. Full SDK verification
has not completed locally: its oracle environment is unavailable, and the network
policy denies the exact browser archive. CI requires the complete pinned SDK
pipeline and must not publish on failure. The upstream SDK PR also needs its
reviewed native golden records regenerated in the required environment; existing
records must not be relabeled as current evidence.

`matter.prismpm.toml`, `MatterApp`, and the old `runtime.mjs`/`browser.mjs` retain
the prior single-excerpt Text/3 target for comparison. The older Python-generated
portal uses `lexlean.toml`; it is neither part of this application runtime nor
covered by the holistic kernel attestation.
