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
synapses once. Features combine its interpretation with its cited source wording;
repeating a feature inside either does not create another example. Activation sums those weights and normalizes by the number of
reviewed examples for that facet, comparing fractions exactly. Zero support and
equal best scores for different facets abstain. Feature extraction exceeding
its token boundary also abstains. No seeded legal vocabulary, arbitrary
confidence threshold, pretrained weights, or hidden model calls supply answers.
Corrections remove obsolete training through the current-reference closure.

This is bounded learned lexical association. Punctuation and non-ASCII case
remain significant. Ordered pairs distinguish some wording changes but do not
establish general negation, syntax, semantic entailment, or legal truth. A
suggestion never silently becomes an accepted interpretation. The user reviews
the actual passage and accepts or supplies its meaning.

`MatterLanguage` learns literal meaning transfers from current reviewed citations.
An identical quotation can suggest its reviewed meaning. When a reviewed value
occurs exactly once inside a quotation, its unchanged prefix and suffix can
anchor a new value: reviewing `Payment: 50 USD.` as `payment.amount = 50` permits
a suggestion of `75` for `Payment: 75 USD.`. Empty or unanchored slots, repeated
values, changed anchors and conflicting examples abstain. Each suggestion retains
the example references that produced it. This is an explicit learned grammar,
not unrestricted language understanding.

Several independently reviewed literal values in the same exact source span can
form one joint grammar. Reviewing both fields of `Amount: 50; day: Monday.`
permits separate suggestions of `75` and `Tuesday` from
`Amount: 75; day: Tuesday.`. All participating interpretations remain attached
as training provenance. UTF-8 byte ranges preserve non-ASCII values. Multiple
facets may share the same literal span; partial overlaps, adjacent slots with
no separating anchor, repeated separators, empty values, and unanchored aliases
abstain. Equal wording at different source locations does not combine training.
A competing interpretation marks even a single matching transfer ambiguous and
retains the conflicting example, rather than allowing a partial match to settle
that disagreement.

One passage may have independently reviewed interpretations for several facets.
Meaning candidates are evaluated per facet, so a date interpretation does not
conflict with an amount interpretation. A blank review cannot resolve conflicting
meanings within one facet; the user must enter the intended interpretation.
Source replacement, correction and withdrawal remove stale examples from learning.

`MatterInference` binds a rule's exact content to reviewed authority,
jurisdiction, and goal references. Authority must have source citations. The
lawyer supplies required `facet = value` conditions, possible exceptions, and an
action. Those conditions are a controlled language, not simulated understanding
of unrestricted legal prose. An assessment is inactive, missing support,
blocked by an observed exception, or supported. Missing conditions become
questions. A supported proposal still requires lawyer review. Competing reviewed meanings
of the same facet from the same exact source span suspend support from that
passage. Contested exceptions remain unresolved instead of being treated as
absent; contested authority suspends the rule. The next form opens the affected
facet for correction, separation or withdrawal. Resolving the conflict does not
automatically reaccept an earlier conclusion. Separate source spans can carry
different values without an invented mutual-exclusion rule.

Draft strategy text presents the reviewed goal, action, support, and citations.
It is assembled from the current matter, not a generated pleading or invented
legal analysis. A draft's revision and dependency references determine its
freshness. No default jurisdiction, authority, deadline, or remedy is supplied.

## Relative changes and history

`Matter.current` computes a least grounded closure starting from no admitted
nodes, bounded by node count and stopping at a fixed point. Only accepted nodes with matching citations and
current dependencies enter the closure. Missing or duplicate identities,
obsolete revisions, changed source bytes, and circular support fail to ground a
conclusion. “Current” means usable in this reviewed context, not proved in court.

`MatterSession` applies commands with expected matter and object revisions.
Edits retain before/after history and original citations. Source replacement
retains the old source version. Rules have structured revision commands so a
plain text edit cannot change an accepted rule's meaning. Reconciliation also
retracts previously accepted conclusions when a new exception becomes current,
even though the exception was absent from the original supporting references.
A lawyer cannot reaccept a conclusion while its rule is unsupported, or
substitute a different conclusion under the old rule binding.

Additional interpretations retain the same exact quotation without making their
acceptance depend on one another. Withdrawal preserves history and source bytes,
removes the interpretation from current support and training, and does not
requeue it as an unreviewed passage. `MatterContext` follows both explicit support
references and semantic rule-condition links when presenting the latest change.
A newly observed exception therefore reaches an existing conclusion even though
it was absent from that conclusion's original supporting references. Renaming a
facet follows connections from both its immediately previous and current name;
older facet history does not create unrelated current impacts.

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
appear as lawyer review tasks. Pending passages are prioritized by their learned
facets' connections to unresolved rule conditions; ties retain source order.
A supported strategy cannot hide an unresolved assessment from another rule.

After pending passages are reviewed, the journey checks their original quotations
for additional learned facets that have not yet been interpreted. It presents
one such aspect at a time, prioritizing unresolved rule conditions. Accepting one
field does not hide the other fields learned from the same passage. A withdrawn
interpretation remains represented, so it does not become an endless review task.
Withdrawing the only supporting training removes its pending suggestion.

The existing review operation applies to the exact displayed passage. It can
therefore review equal values at distinct source locations without an ambiguous
text selector. Its prepared form contains only the aspect and editable meaning.
Changing an aspect with an empty meaning cannot reuse a different aspect's
inference. Conflicting meanings require explicit interpretation. The focused
node and facet are independent of workflow role: switching between client and
lawyer does not silently change the source. A privileged aspect remains a lawyer
review task; client and reader views do not prepare an unauthorized action.

Review context names the resource and its original text line. Duplicate resource
titles include their resource number. UTF-8 and CRLF do not shift those locations.
Detailed byte citations remain available in the lawyer view. Attention checks
reuse the current-reference closure across their facet scan.
`MatterWorkspace` exposes 19 operations for
creation, intake, review, assertions, source and rule revisions, strategy,
proposals, restoration, additional interpretations, withdrawal, change impact,
and paginated facet and strategy inspection. It selects objects by
unique visible wording rather than asking users to find internal IDs. Ambiguous
selection refuses rather than choosing arbitrarily.

`HolisticApp` declares the forms, plain-language copy, palette, density, file
controls, errors, empty states, and 30 acceptance vectors. Unused help and
transport details are collapsed. Facet inspection shows eight items per page;
the lawyer view adds source locations. Control characters are rendered safely
without altering retained source bytes. Long context is explicitly truncated
for presentation while the journal preserves the original.

`MatterWorkspace.nextStep` selects a declared form from the current journey.
It can prepare intake, goal, passage review, jurisdiction, missing context or
strategy inspection. It retains the selected workflow and never fills a missing
fact with the value a rule requires. The view offers the source-owned operation
label as a button. Opening it prepares editable fields without executing a command
or changing accepted state. Malformed next-form proposals invalidate a response
before any state is accepted.

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

The application source with source ID
`72437fc926c7f93ba10376272d5b4cf7b26eb8c0522f2e02d3ac971585864931`
and semantic ID
`75ed91c631e38c872dfd6ff074b6424b914822510e923b07f2fb4d1cec06d675`
was emitted as build
`172c345aebd4159da19c8617fe64006d567c78c04442f59fc585b084725e8d70`
and passed LexLean verification with attestation
`9bf3643cff2db3d961fdcd2ff6846f3c800db7222e2f468c9c0ce04a78fb02dd`.

The generated native library passes 36 tests across `behavior.rs` and
`holistic.rs`. They cover relative edits, transitive invalidation, source
forgery, conflicts, cycles, learned abstention/retraining, exact rule binding,
new exceptions, stale reacceptance, ambiguous actions, replay, draft freshness,
learned literal and joint-slot extraction, overlapping and ambiguous training,
multiple facets, withdrawal and facet-rename impact.
Patch test dependencies to actual emitted packages rather than editing generated
code:

```sh
cargo test --offline --locked --manifest-path tests/matter/Cargo.toml \
  --config 'patch.crates-io.prism-legal-matter.path="<build>/cargo/package"' \
  --config 'patch.crates-io.prism-stdlib.path="<sdk>/stdlib/generated/package"'
```

`holistic_runtime.mjs` runs all 30 source vectors and unseen framing, Unicode,
control-display, malformed replay, pagination, and resource-boundary inputs
against generated Wasm. `run_browser.mjs` serves only emitted files and runs
`holistic_browser.mjs` through creation, exact file import, passage review,
rule assessment/revision, proposal review, exception/correction propagation,
inspection, save/reopen, failed restoration, learned multi-facet review, withdrawal,
next-form navigation, source locations, additional-facet review, role consistency,
and mobile layout.

The source corpus includes a 70,831-byte restore request containing nine imported
resources. It exceeds the old portable transport limit and returns the exact
accepted journal. The previous 25-vector artifact passed direct and resident Hologram execution
and all nine portable browser journeys, including actual file reopening of the
larger matter. The current 30-vector artifact passes native, Wasm and application
browser checks. The intermediate 28-vector artifact's development portable-browser
run failed while reading a response through Playwright (`Network.getResponseBody: No data found for
resource`). Repeating the run and starting body capture earlier did not resolve
it. That portable gate remains unverified; the required pinned-browser CI must
resolve it without replacing the response-body assertion or changing retention
buffers.

The source-pinned SDK carries explicit transport bounds from
[PrismPM #496](https://github.com/UOR-Foundation/PrismPM/issues/496).
The host selects the application's declared 2 MiB request / 8 MiB response limits
before starting the session. Decoded-byte and HTTP-envelope checks retain those
limits. The SDK records the upstream base, exact dependency patch, and patched
archive digests in its execution report; the patch is not described as an
unmodified upstream runtime.

Application browser checks pass in development Chromium 154.0.8037.57 with
Playwright 1.62.1. They are distinct from PrismPM's pinned Chromium 157 oracle. Full SDK verification
has not completed locally: its oracle environment is unavailable, and the network
policy denies the exact browser archive. CI constructs the complete SDK image from the pinned source with its official
image-input recipe, including the browser and sealed inventory. An older
candidate image passed the application browser journey but failed full
verification because its inventory named a different browser. The replacement
pipeline must pass full verification before publication. The upstream SDK PR also needs its
reviewed native golden records regenerated in the required environment; existing
records must not be relabeled as current evidence.

`matter.prismpm.toml`, `MatterApp`, and the old `runtime.mjs`/`browser.mjs` retain
the prior single-excerpt Text/3 target for comparison. The older Python-generated
portal uses `lexlean.toml`; it is neither part of this application runtime nor
covered by the holistic kernel attestation.
