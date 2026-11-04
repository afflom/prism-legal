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

`MatterChronology` orders current reviewed date interpretations from explicitly
selected aspects. One aspect per line combines related dates without assuming
which fields represent dates or repeating entries for duplicate selections.
The date language is Gregorian `YYYY-MM-DD`, years 0001–9999, with actual month
lengths and leap-year checks. Unknown formats, impossible dates, and competing
interpretations remain visible for review ahead of the ordered entries.
Independent passages with equal dates remain separate and retain their sources.

The view includes each original quotation and resource location; when several
aspects are selected it also names the aspect. Directly recorded assertions are
labeled accordingly. Corrections reorder the chronology, withdrawal removes
support, and source replacement excludes obsolete interpretations. The view is
read-only and paginated; it computes neither legal deadlines nor missing dates.

## Structured CSV intake

`MatterCsv` parses actual comma-separated UTF-8 resource bytes. The first record
contains distinct, nonempty headings of at most 128 bytes. Every later record
must have the same column count. LF and CRLF record separators, an optional
initial UTF-8 BOM, quoted commas and newlines, and doubled quotes are supported.
Malformed quoting, ragged rows, empty or duplicate headings and over-bound input
refuse the whole transaction. Empty cells create no assertions.

Each populated data cell becomes an unaccepted interpretation with its heading
as an editable aspect and its decoded content as the value. The original source
is retained byte-for-byte. A citation identifies the complete raw cell, including
its quoting; the existing checked intake contract verifies that quotation against
the source. Shared header citations do not manufacture conflicts between rows.
Locations use record and column numbers, counting the header as row 1; embedded
newlines do not turn one record into several table rows.

Blank review retains the decoded cell rather than transferring a different
column's meaning. Additional learned interpretations use examples from the same
column of that source version. Equal bare values in unrelated columns therefore
do not create extra review tasks. A reviewed additional interpretation can still
teach another cell in the same column. This is contextual literal learning;
column names do not establish legal truth or imply relations between entities.
Rules continue to use their explicit reviewed facet/value conditions.

The source format is retained in modeled session metadata and reconstructed by
the `ingest-csv` journal command. Replacement uses the original format, retains
the old bytes, and invalidates interpretations, chronology entries and strategy
support that depended on the old revision. Readers cannot import data; authority
and legal-conclusion review retain lawyer workflow checks. Older text-resource
journals retain their existing encoding and behavior.

The CSV byte scan divides its bounded steps into balanced groups rather than
recursing once per byte. Fifteen levels cover the declared 8192-byte input plus
its end-of-input step. The table is also bounded to 64 physical text lines and
1024 cells, including headings and empty cells. These are execution limits.

## Original source context

`MatterResources` exposes original text lines and decoded CSV cells without
changing the journal or accepting an interpretation. A source location selects
the corresponding text page or complete CSV record. Eight items appear per
page; a wide row opens at the page containing the selected cell. Blank lines
and empty cells remain visible as source context and create no assertions.

Resource names select a unique current source. With both selectors blank,
multiple resources appear in a paginated catalogue. Exact displayed source
locations distinguish duplicate names. Earlier-version locations select the
retained original bytes and their own CSV headings. A mismatched name and
location, unknown source, or invalid page refuses without changing the journal.
Current and earlier versions are labeled explicitly. Text controls are normalized
only for display; saved resource bytes and citation ranges remain unchanged.

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

## Strategy proposal continuation

A strategy view prepares the operation appropriate to its current assessment:
create a proposal from supported evidence, review that strategy's pending
proposal, inspect its current reviewed conclusion, or resolve missing context.
The dedicated proposal-review form selects the named strategy, independently
of the automatic attention queue. Clients cannot accept a legal conclusion;
changing support before review refuses the transaction. Missing-fact forms
leave the answer blank rather than inserting the value a rule requires.

`MatterSession.currentProposal` compares the rule, conclusion, and complete
support-reference set. Repeated creation with the same current support leaves
the session and journal unchanged. Retraction or withdrawal permits a fresh
unaccepted proposal when support becomes available again. Existing reviewed
conclusions take precedence over pending duplicates retained from older journals;
equivalent legacy candidates use their earliest identity consistently.

The new `propose-current` journal command enforces this behavior for new requests.
The earlier `propose` command keeps its original replay semantics, so a saved
history containing duplicate proposals remains readable. Proposal matching
executes across large matters without increasing native test stack limits.

## Persistence and journeys

`MatterJournal` stores a versioned journal with canonical UTF-8 byte-length
framing. Newlines, CRLF, Unicode, BOMs, embedded separators, and NUL bytes survive
save and replay. Invalid lengths, incomplete frames, unsupported commands,
stale revisions, and over-bound input are refused. Corrupt replay does not
return a partially accepted matter. A failed transaction preserves the complete
previous session and journal.

The history budget is twice the 1,024-node matter capacity. It admits intake and
review of every node, while corrections consume the same finite command budget.
Reaching it preserves the existing matter and leaves inspection and saving
available; the view identifies the history limit separately from input size.
Journal field decoding and replay use balanced first-order traversals. Their
depth is derived from the actual field budget or command count. Decoding keeps
UTF-8 byte offsets and original field order; replay stops at the first refused
command. Neither traversal retains a recursive frame for every earlier session.
These definitions compile through the pinned PrismPM exporter without requiring
higher-order runtime closures or changing the saved-file format.

`MatterJourney` selects useful next context: intake, goal, one review task,
jurisdiction, authority, then strategy assessment. The pending review and additional learned facets participate in a shared
attention selection. Connections to unresolved conditions of current reviewed rules take
priority. Distinct words and adjacent word pairs shared with any current goal
break ties; remaining ties preserve source order and the existing pending-review
precedence. No numeric tuning weights or remote inference service are used.
All admitted, undisputed goals contribute to that shared context. Repeated
vocabulary counts once; adding the same wording cannot outweigh another goal.
Word pairs stay within their original goal, so two separate goals cannot create
an invented phrase. Correcting, withdrawing, disputing or replacing a source
removes that goal's old contribution immediately. Goal features retain the
matter's bounded groups rather than constructing an unbounded flattened list.

**Add another desired outcome** appends a goal without replacing an existing one.
**Set the desired outcome** refuses to choose silently when several goals exist;
**Correct an interpretation** selects the intended goal by its exact wording.
Existing strategies remain bound to their particular goal revision. Adding or
correcting another goal preserves that binding; changing the bound goal makes
its dependent reasoning inactive. Saving and reopening retains those relations.

Learned feature updates also preserve their original order and weights while
processing bounded groups. A matter with 1,022 distinct goals and two pending passages exceeded the
browser deadline with the initial guest allocator, despite native reference
generation completing.
The regression retains all 1,024 nodes and selects the oldest relevant goal;
no vocabulary, goals, or acceptance expectations are truncated to reduce work.

Goal matching is bounded literal vocabulary attention, not evidence that a
legal condition is satisfied. Editing or withdrawing the goal recomputes focus;
only current admitted context contributes. Selection never accepts a fact.
For pending text, selection uses the same learned facet and literal meaning
that the review view offers and automatic review accepts. For example, a
reviewed `Amount: 50.` → `amount: 50` interpretation lets `Amount: 75.`
receive attention for the goal `75`, even though the raw token includes a
period. A usable learned meaning takes precedence over a conflicting neural
facet suggestion. Ambiguous literal meanings cannot manufacture goal overlap.
The pending scan compiles current cited training into `CompiledMeanings` once.
Each example retains its exact quotation, joint extraction slots, conflicting
references, and training reference. Candidate inference reuses that context;
it no longer reconstructs source-slot and conflict information for every pending
passage. The context is rebuilt from current admission after each matter change
and is not serialized as an independent authority. Uncited assertions remain
classifier context, not literal extraction examples. Matters with no pending
text avoid compiling an unused language model.
A supported strategy cannot hide an unresolved assessment from another rule.

The journey checks reviewed passages' original quotations for additional learned
facets that have not yet been interpreted. A relevant missing aspect can receive
attention before an unrelated new passage. It presents one aspect at a time,
using the same rule and goal priorities within a passage and between passages.
Accepting one field does not hide other fields learned from the same passage.
A withdrawn interpretation remains represented, so it does not become an endless
review task. Withdrawing the only supporting training removes its suggestion.
The overview and automatic review operation use the same attention selector.

`MatterBatch` preserves node order while splitting traversal into groups of at
most 32 nodes: at the 1,024-node matter limit, both traversal levels have at
most 32 elements. Attention and meaning scans fold those groups without changing
their candidate priorities. This is an execution bound, not an inference weight
or a truncation limit: all nodes remain eligible, including the final cell of a
maximum-size table. Candidate scoring and citation construction run outside the
recursive traversal frames. Repeated represented facets are checked once per
passage. These model changes keep nested review explanations within ordinary
native test stacks.

The existing review operation applies to the exact displayed passage. It can
therefore review equal values at distinct source locations without an ambiguous
text selector. Its prepared form contains the aspect, editable meaning, and exact source location. A blank location retains the automatic next-review path; an explicit location selects one current pending source interpretation.
Changing an aspect with an empty meaning cannot reuse a different aspect's
inference. Conflicting meanings require explicit interpretation. The focused
node and facet are independent of workflow role: switching between client and
lawyer does not silently change the source. A privileged aspect remains a lawyer
review task; client and reader views do not prepare an unauthorized action.

A selected source-context view can prepare that pending passage’s review form. Opening it is read-only; submitting uses the same journal command and workflow checks as automatic review. Accepted, withdrawn, historical, missing, and ambiguous selections cannot silently replace an interpretation. Current interpretations use the correction and withdrawal operations. Older four-field review requests remain supported.

Review context names the resource and its original text line. Duplicate resource
titles include their resource number. UTF-8 and CRLF do not shift those locations.
Detailed byte citations remain available in the lawyer view. Attention checks
reuse the current-reference closure across their facet scan.
`MatterWorkspace` exposes 23 operations for
creation, intake, review, assertions, chronology, source and rule revisions, strategy,
proposals, restoration, additional interpretations, withdrawal, change impact,
and paginated facet and strategy inspection. It selects objects by
unique visible wording rather than asking users to find internal IDs. Ambiguous
selection refuses rather than choosing arbitrarily. When multiple passages share
an interpretation, correction, annotation, and withdrawal accept an optional
source location copied from facet inspection. The location narrows the current
candidate set; a missing or still-ambiguous match leaves the entire matter
unchanged. Original citations, other passages, role checks, and normal journal
replay are preserved. Earlier requests without this qualifier remain supported.
Resource replacement also accepts an optional current source location. This
distinguishes duplicate resource titles without changing the journal format.
A location must match the selected current resource even when its name is unique;
historical locations and mismatched titles refuse. A resource can still be
replaced after its interpretations are withdrawn.
Historical interpretations show their source revision and original line, using
the retained source bytes rather than the replacement resource's text.

`HolisticApp` declares the forms, plain-language copy, palette, density, file
controls, errors, empty states, and 118 acceptance vectors. The shorter opening and help sections leave more room for the active matter. Unused help and
transport details are collapsed. Shorter field guidance and the neutral Continue
action serve both review and read-only forms. Acceptance bytes are factored into
closed byte aliases. Content-based boundaries let differently framed requests
and responses share identical journal segments. The 118-case corpus retained
every request and response byte while unique literal data fell from 1,116,424
to 328,339 bytes. This reduces compiler work without weakening a capacity case. Facet inspection shows eight items per page;
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
| Source text or CSV | 8192 UTF-8 bytes, 64 physical text lines |
| CSV table | 1024 cells including headings and empty cells |
| Matter | 32 sources, 1024 nodes, 128 rules |
| Network input | 256 split tokens |
| Journal history | 2048 commands |
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
`cb1a54eba44fb66a30af9a686ddefcf892fc3d5a410c02e79a9876e9eadf014b`
and semantic ID
`24435175b9fe068b0cd2004f31abfeab25a09f2c2ac680838416ad3edfd01b37`
passed LexLean verification with attestation
`0327f9b2f0720ae407d7a3053b2d7bc0f6d897f67d6824a780bdd394461b1d92`.

The generated native library passes 96 tests across `behavior.rs` and
`holistic.rs`. They cover relative edits, transitive invalidation, source
forgery, conflicts, cycles, learned abstention/retraining, exact rule binding,
new exceptions, stale reacceptance, ambiguous actions, replay, draft freshness,
learned literal and joint-slot extraction, overlapping and ambiguous training,
multiple facets, withdrawal, facet-rename impact, CSV quoting and byte provenance,
column-aware learning, source replacement, large-table reconciliation, retained-version source inspection, automatic passage pagination, goal-relative attention, learned-value attention, classifier/meaning disagreement, disputed-value abstention, and unified additional-facet review.
CSV boundaries exercise 8192 bytes and 1024 cells, including 1008 populated
cells in both an empty matter and a matter with an existing legal rule. The
boundary checks also select the last cell through a changed goal and render the
review overview. A separate native core-session test selects attention in an untrained 1,008-passage matter, then reviews all its text passages before
checking that no pending interpretation remains. A saved-file test separately replays all 1,008 reviews, accepts a correction
to the last passage, and replays the corrected matter exactly. A second test
retains 2,047 successive corrections, admits the 2,048th command, and refuses
the next command without losing the session or journal. Late corruption returns
an empty refused session. UTF-8 field tests cover both sides of traversal
boundaries through 2,050 fields. Native tests retain their ordinary stack configuration; the recursive byte scan, node
construction and matter reconciliation were refined in the model. No test stack
limit was increased to conceal a failure. The compiled and direct meaning paths
are compared with exact training-reference order across joint extraction,
conflicts, withdrawal and source replacement. Corrections at the first, last
and traversal-boundary passages preserve every other node and its order.
Selecting the replacement head before rebuilding the list avoids repeated deep
copies of the remaining records. Reviews without dependencies avoid computing
an admission set that the empty dependency check cannot use.
Patch test dependencies to actual emitted packages rather than editing generated
code:

```sh
cargo test --offline --locked --manifest-path tests/matter/Cargo.toml \
  --config 'patch.crates-io.prism-legal-matter.path="<build>/cargo/package"' \
  --config 'patch.crates-io.prism-stdlib.path="<sdk>/stdlib/generated/package"'
```

`holistic_runtime.mjs` runs all 131 source vectors and unseen framing, Unicode,
control-display, malformed replay, pagination, and resource-boundary inputs
against generated Wasm. `run_browser.mjs` serves only emitted files and runs
`holistic_browser.mjs` through creation, exact file import, passage review,
rule assessment/revision, proposal review, exception/correction propagation,
inspection, save/reopen, failed restoration, learned multi-facet review, withdrawal,
next-form navigation, source locations, additional-facet review, role consistency,
source-qualified corrections, historical source locations, learned date chronology,
combined date aspects, source-qualified resource replacement, CSV file import
and refusal, table revision and replay, source-context browsing, source-selected review, selected-strategy proposal continuation, and mobile layout.

Named acceptance definitions and ordered list segments preserve every vector while avoiding a deeply nested inline snapshot. An unfactored 111-vector corpus exposed [LexLean #430](https://github.com/UOR-Foundation/LexLean/issues/430); the repair is proposed in [LexLean PR #431](https://github.com/UOR-Foundation/LexLean/pull/431). The application uses the pinned SDK with factored constants, so it does not depend on that repair.

The source corpus also exercises a complete strategy lifecycle: reviewed authority and conditions, proposal creation, refused client acceptance, lawyer acceptance, a newly observed exception, fresh proposal and review after withdrawal, correction, source replacement, and replay.

The source corpus includes a 70,831-byte restore request containing nine imported
resources. It exceeds the old portable transport limit and returns the exact
accepted journal. The current corpus also restores an actual 81-command
journal with 1,008 source passages and 64 reviews, then continues at the exact
next passage. The browser imports that saved file and submits the prepared
review under its existing command deadline. A local Wasm probe of this journal
fell from exceeding 45 seconds before the refinement to 1,265 ms after it;
a 512-command, 495-review journal reopened in 11,406 ms. These are local
measurements, not universal latency guarantees.

Two development Chromium 154 portable diagnostics for the preceding 111-vector
artifact failed at response-body retrieval: the first at file-session vector 20
(withdrawal without a matter), the second during saved-file roundtrip restoration.
The second recorded the exact expected message and nonempty journal in the page,
ready controls, and `ERR_ABORTED`; Playwright still could not retrieve the response
body. These passive client observations are diagnostic evidence only and do not
replace the required response assertion. No timeout, retry, assertion or retention
buffer was changed. The failure remains relevant to
[PrismPM #67](https://github.com/UOR-Foundation/PrismPM/issues/67).

The preceding 107-vector artifact passed native, Wasm and
application-browser checks. Its development Chromium 154 portable diagnostic failed during file-session vectors at index 18 (empty-file restoration), with the response-body-unavailable condition (`Network.getResponseBody: No data found for resource`). The response assertion was retained and this is not a pinned-browser attestation. The preceding 82-vector artifact failed a local Chromium 154 diagnostic during file-session vectors at index 24 with `Network.getResponseBody: No data found for resource`; this is relevant to [PrismPM #67](https://github.com/UOR-Foundation/PrismPM/issues/67) and is not a pinned-browser result. The prior
40-vector and 34-vector artifacts' development portable-browser runs failed while
reading a response through Playwright (`Network.getResponseBody: No data found
for resource`). A diagnostic run of the prior 30-vector artifact also failed;
a second diagnostic run passed direct/resident execution and all nine portable
journeys. These observations establish intermittence, not a resolved gate.
The 40-vector diagnostic observed a successful HTTP response followed by
`ERR_ABORTED` during blank-file restoration; the application had reached its
ready state. The cause remains unestablished. Earlier body capture did not
resolve it. The required pinned-browser CI must
pass without replacing the response-body assertion or changing retention
buffers to hide the failure.

The earlier 118-vector source corpus also restored a fully reviewed 1,008-passage
intake and a 2,048-command correction history, inspects the final correction,
and refuses both another edit and a 2,049-command restore. The generated-browser
journey opens both files, saves their exact bytes, corrects the last passage
by source location, and keeps the accepted file after each refusal. A local probe of the initial capacity build
`980b07ad1b371c36f9d4c936f799040a2fc760433a7e5aea52764a541ef2e52c`
measured 10,991 ms for the 67,239-byte fully reviewed intake and 1,934 ms for
the 134,971-byte correction history. Neither test nor browser command deadline
was increased. These timings are observations on this machine, not latency
guarantees. That revision did not establish full portable verification of the expanded corpus.

The subsequent pinned [CI run 41676256220](https://github.com/afflom/prism-legal/actions/runs/41676256220)
for commit `575b038768fd56027154e5c4e8a276ebe200d464` passed source verification,
87 native tests, the Wasm-adapter corpus, and the generated application browser.
Full verification failed in the actual Core-Wasm guest. Direct local execution
reproduced the trap at stored vector index 110 (10,633 request bytes), with
linear memory at the declared 256 MiB maximum. The guest's cumulative bump
allocator retained dropped Rust temporaries; the browser adapter used a different
allocator. This is a separate, concrete failure from the older development-browser
response-body diagnostics. [PrismPM #507](https://github.com/UOR-Foundation/PrismPM/issues/507)
is addressed by [PR #508](https://github.com/UOR-Foundation/PrismPM/pull/508),
which reuses temporary allocations while preserving resident ABI buffers and
original V1 generation. `core_runtime.mjs` now executes the actual
archive guest independently of the browser adapter and is a required CI step.

The current 131-vector corpus also restores 1,022 distinct goals and two pending
passages at full node capacity, selecting the oldest relevant goal. Its actual
Core-Wasm guest was regenerated from the compiled model with the final pinned
Rust allocator and passed every source vector. The vocabulary case took 5,712 ms
using 67,633,152 bytes; the fully reviewed 1,008-passage restore took 8,072 ms
using 16,056,320 bytes. These are local observations with unchanged bounds.
The initial coalescing free-list implementation failed to complete this corpus
within 200 seconds; a 10-second profile concentrated samples in allocation and
release searches. The final adapter uses the pinned toolchain's standard Wasm
allocator, preserving the import-free binary and modeled memory/stack contract.
This is generic SDK behavior; application learning and grouped feature updates
remain LexLean definitions. The generated browser also restores the full goal
file, retains its exact bytes, and prepares the selected source passage without
accepting it. Its existing command deadline is unchanged.

Full pinned-image results belong to the exact commit and artifact reported by
[the application PR](https://github.com/afflom/prism-legal/pull/1) and its Actions
checks. These local measurements and component checks do not constitute that
full verification attestation.

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
verification because its inventory named a different browser. The rebuilt-source pipeline passed both jobs in
[CI run 41606014103](https://github.com/afflom/prism-legal/actions/runs/41606014103)
for commit `9a9d140720061049bd397f85859930e82c858296` (28 acceptance vectors).
The downloaded verification artifact reports verified native CLI, Core-Wasm,
browser projection, Hologram oracle, artifact closure, and byte-identical
regeneration. Its full PrismPM attestation is
`ea12cdd98b9022e94feb9ec95a6370d7b5d5ffad096a5a4c6d04d6a72d047563`,
for build `98cb44be28db930e74f5885b27397de84d94f38ee86d77a016abd20c9b690628`
and source `3688c15bdc0fcaf3f5ad46166016f29aed79f9abf4393dbae2ec8bcf20e1b060`.
The artifact ZIP SHA-256 is
`29b4e58916be64b861432a6296f667cf7e80ad3ae13a010b4b8517ab34dd16a6`.
This evidence applies to that revision; later changes still require their own
full verification before publication. The later 42-vector commit `fff875e` passed native, Wasm and application-browser checks in [CI run 41620717145](https://github.com/afflom/prism-legal/actions/runs/41620717145), but its Hologram oracle exited with `Elapsed(())`. That portable timeout is unresolved and the run is not a full verification pass. Two later local diagnostic runs of its 42-vector source produced a browser failure and a pass of direct/resident execution and all nine portable journeys in Chromium 154; this does not establish the cause of the pinned CI timeout. The upstream SDK PR also needs its
reviewed native golden records regenerated in the required environment; existing
records must not be relabeled as current evidence.

`matter.prismpm.toml`, `MatterApp`, and the old `runtime.mjs`/`browser.mjs` retain
the prior single-excerpt Text/3 target for comparison. The older Python-generated
portal uses `lexlean.toml`; it is neither part of this application runtime nor
covered by the holistic kernel attestation.
