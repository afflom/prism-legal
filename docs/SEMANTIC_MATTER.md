# Semantic matter implementation

`matter.lexlean.toml` selects the executable source graph. `prismpm.toml`
selects that project for PrismPM builds. No application behavior in this
graph is authored in JavaScript, Python, Rust, or Lean. The browser, native
CLI, byte guest, Rust library, and archive are generated from LexLean by
the pinned PrismPM compiler.

## What runs

`MatterText.IntakeModel` extracts nonempty lines from actual UTF-8 resource
text. Every passage has its original bytes, source identity and revision,
and a half-open UTF-8 byte range. Its contract checks every returned
quotation against that exact source. A passage starts unreviewed.
Neither extraction nor a matching word authenticates evidence.

`MatterReview` applies a review only when a quotation identifies exactly
one complete source line. An interpretation can differ from the quotation;
the quotation remains intact. An absent or ambiguous quotation is a typed
refusal. Blank intake produces no matter facts.

`MatterText.attend` is a transparent lexical retrieval model. It learns its
labels from the supplied reviewed examples, compares sets of space-delimited
terms using Jaccard overlap, and compares fractions exactly by cross
multiplication. Repeated terms cannot inflate a score. Zero overlap and
equal best scores for different facets cause abstention. It uses no preset
domain weights, default jurisdiction, random classification, or claimed
probability. All inferred facets remain suggestions. Token matching is
case-sensitive and punctuation-sensitive; it is not a general semantic
language model. The original wording, including negation, stays visible.

The generated view leads with one unreviewed passage. It shows the reviewed
interpretation that informs that suggestion; the lawyer view adds source
locations for those passages. Unrelated passages stay out of the result. It starts with
empty fields. The optional example is explicitly an example. Editing an
input clears the previous result in PrismPM's generated view.

## Revisions and dependencies

`Matter.Node` separates origin, review acceptance, interpretation,
citations, and versioned dependencies. Here, “current” means usable in the
reviewed matter context; it does not mean legally proved or admissible.

`Matter.current` computes the least grounded closure from an empty set,
bounded by the number of nodes. Each round admits only accepted nodes
whose citations match and whose versioned premises were admitted. This
handles arbitrary node order and transitive dependencies. Missing nodes,
obsolete revisions, changed source bytes, duplicate identities, self
cycles, and mutually supporting cycles cannot establish support.
Computed collections use named records (`Nodes`, `Admission`, `TextItems`)
to declare owned storage in the SDK's Rust ABI. A bare list return uses a
caller-owned output buffer and cannot represent these intermediate values.

`Matter.commitEdit` checks both the expected matter revision and node
revision, preserves the original citations and dependencies, advances the
revision, and retains the before/after nodes in a change history. The caller
must atomically store the returned state. A rejected edit returns no state.
Recomputing `current` invalidates affected dependents while retaining
unrelated context. Reconsidering stale conclusions requires new inference
and review; updating a premise's revision alone does not re-establish a
conclusion.

The kernel laws in `MatterLaws.lex.tex` exercise reverse-ordered dependency
chains, direct and transitive invalidation, unrelated context, obsolete
edits, missing support, unreviewed support, cycles, and duplicate IDs.
Universal correction laws preserve provenance and dependencies and advance
the node revision. These are precise properties, not a proof of legal
correctness or of an entire production service.

## Current application boundary

The Text/3 workbench recomputes **one excerpt review with one reviewed
exemplar** from the visible inputs. It does not persist a matter or
accumulate reviews. The full revision/dependency library is exported for a
matter host; the excerpt UI does not yet provide that host. This boundary
is also stated in the generated view.

The existing portal in `tools/case/site.py` still contains handwritten
application behavior. It has not been replaced by this source graph.
PDF/image/audio extraction, learned semantic interpretation, legal
authority selection, strategy generation, persistent multi-user matter
editing, and the complete client/lawyer journeys are not implemented by
this change. The legacy portal's heuristic output must not be described as
those capabilities being complete or kernel verified.

PrismPM at the pinned revision can generate the portable text workbench.
Its production browser application profile is still refused by the SDK
with `PP2011`. Closing the full application requires extending and
verifying that modeled host/profile, including storage, interactions,
resource processing, and the inference provider. Adding a handwritten
browser implementation alongside these models would not satisfy the
project's architecture.

## Limits and evidence

The excerpt boundary is 8192 UTF-8 bytes and 64 lines; a facet is at most
128 bytes and an interpretation at most 8192 bytes. Transport requests
are bounded to 32768 bytes, responses to 262144 bytes. The guest input
allocation boundary is 32769 bytes, exercised by a refusal vector. Core
Wasm has 1024 memory pages and a 4 MiB stack. These are operational bounds,
not legal constants or claims about model accuracy.

Application acceptance vectors are declared in `MatterApp.lex.tex` and
mirrored as readable requests/results in `tests/matter/acceptance.json`.
They cover real dispatch behavior rather than an input-to-fixture lookup.
PrismPM validates example bindings and runs generated acceptance oracles.
The generated program must also be tested on previously unseen inputs and
the maximum accepted excerpt, because fixture parity alone is insufficient.
The JSON escaper uses an accumulator so maximum-size excerpts do not depend
on a byte-per-call WebAssembly stack depth.

`tests/matter/behavior.rs` tests the generated Rust library, including retained
history, source-byte forgery, dependency invalidation, ambiguous attention,
and overflow. To run it, patch the two test dependencies to the actual
generated application package and the pinned SDK's generated stdlib:

```sh
cargo test --offline --locked --manifest-path tests/matter/Cargo.toml \
  --config 'patch.crates-io.prism-legal-matter.path="<build>/cargo/package"' \
  --config 'patch.crates-io.prism-stdlib.path="<unpacked-sdk-stdlib>"'
```

The SDK ships the latter archive at `stdlib/generated/prism-stdlib-0.2.0.crate`.
Extract it into a temporary directory; do not change the generated packages
to insert tests. `tests/matter/runtime.mjs` exercises the WebAssembly
transport. To test the actual interface, serve the generated browser
directory locally, then run:

```sh
npm ci --prefix tests/matter
CHROMIUM_EXECUTABLE=/path/to/chromium BROWSER_URL=http://127.0.0.1:8794/ \
  npm run --prefix tests/matter test:browser
```

These browser tests check blank intake, source review, changed interpretations,
stale result clearing, role-specific source context, and mobile overflow.
They do not replace PrismPM's separately pinned browser-oracle verification.

The Foundation Text/V1 and Text/V3 modules and two lexicon entries come
from PrismPM commit `f0c479e94c87ffc18c79b4632b8c73b44993da5b`.
The existing Foundation Bytes/Utf8 wrappers now explicitly declare their
pure definitions executable, as required by model runtime validators.
