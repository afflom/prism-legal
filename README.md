# PrismLegal

PrismLegal is a local legal matter workspace authored in LexLean and compiled
by PrismPM. Its evidence and inference discipline follows
[afflom/rule30](https://github.com/afflom/rule30): source material, reviewed
interpretations, rules, and conclusions remain distinguishable and connected.
No remote model, inference service, or model credentials are used.

The compiled application lets a client or lawyer create a matter, import actual
UTF-8 text and CSV resources, review passages and cells, record goals and jurisdiction, and connect
reviewed authority to conditional strategies. Reviewed source wording teaches
facet and meaning suggestions. CSV headings suggest editable aspects; exact cell quotations and table locations
remain available through review and replacement. A passage can support several interpretations. Further learned aspects stay
visible as focused review steps, with the original resource and line identified;
withdrawal preserves their history. Reviewed rule requirements and vocabulary shared with all current goals guide attention across new passages and learned missing aspects. Attention uses the same learned facet and literal meaning offered for review; disputed meanings cannot create goal relevance. It compiles current extraction and conflict context once per pending scan, so a large partially reviewed intake can reopen and continue. Changes invalidate dependent conclusions
and expose related facts and strategies. Strategy inspection leads to its own proposal review; repeated requests do not create duplicate proposals from the same current support. A saved matter file replays the complete accepted command history, including review of a full intake. Its 2,048-command budget preserves earlier corrections; reaching it leaves inspection and saving available.
The view offers the next useful form, with focused facet inspection and
supporting source context available when needed. Source locations distinguish
equal interpretations during correction or withdrawal and retain the original
line and version after a resource changes. Identical directly recorded entries
have copyable entry locations, so correcting or withdrawing one preserves the
others and their strategy bindings. Resource replacement can also use
these locations to distinguish duplicate filenames. Source inspection opens the complete CSV row or the text page containing a passage, including retained earlier versions. From a selected current passage, users can open its review form without changing the automatic attention order. A chronology combines selected date
aspects, orders valid dates, and keeps uncertain or conflicting dates visible
for review. It shows eight entries at a time with complete counts, and a compact
selection heading keeps broad chronologies readable.

**This is an implemented local workspace, not a completed production legal
service.** Its associative classifier learns words and ordered word pairs from
current reviewed examples. It abstains without support or on conflicting best
matches. It is not a general pretrained language model. Legal inference uses
explicit, lawyer-reviewed conditions; it does not invent law, search authorities,
read PDFs/images/audio, or provide authenticated collaboration. See
[the implementation and verification boundary](docs/SEMANTIC_MATTER.md).

## Source and build

`holistic.lexlean.toml`, selected by `prismpm.toml`, compiles
`src/HolisticApp.lex.tex` and the `Matter*.lex.tex` modules. They own state,
intake, learning, inference, journal replay, journeys, UI copy, design, resource
bounds, and acceptance vectors. Product behavior is not handwritten in a second
application runtime. Rust and JavaScript under `tests/matter/` are test harnesses.

[toolchain/prismpm.json](toolchain/prismpm.json) pins the SDK source fix.
CI constructs its verification image and sealed tool inventory from that exact
source using the SDK’s own image recipe. It does not patch an older installed
inventory. The workflow reuses scoped BuildKit cache layers while preserving
the exact source closure and complete application verification. Bounded retries
for temporary SDK download failures and the cache transport are proposed in
[PrismPM #523](https://github.com/UOR-Foundation/PrismPM/pull/523).
The generic file-session capability is proposed upstream in
[PrismPM #495](https://github.com/UOR-Foundation/PrismPM/pull/495), following
[issue #491](https://github.com/UOR-Foundation/PrismPM/issues/491). The app uses
that fix directly while it awaits upstream review. Its bounded portable session
transport fix is tracked in [#496](https://github.com/UOR-Foundation/PrismPM/issues/496),
with the carried dependency patch identified in verification evidence. Bounded
reuse of temporary Core-Wasm allocations is proposed in
[PrismPM #508](https://github.com/UOR-Foundation/PrismPM/pull/508), following
[issue #507](https://github.com/UOR-Foundation/PrismPM/issues/507). Legal behavior
stays here.
LexLean is 0.4.0 (`e0b74b81e6f49c83596a957d232c8383a5db1a25`), with Lean 4.32.1.

With that SDK's pinned toolchain installed:

```sh
lexlean --project holistic.lexlean.toml lock --check
lexlean --project holistic.lexlean.toml verify
prismpm --project . check
prismpm --project . build
prismpm --project . verify
```

Builds emit Rust, a native CLI, Core-Wasm, a browser view, and a Hologram archive
under `.prism/build/<build-id>/`. Serve `view/browser/` over HTTP to use the app.
Use **Save matter** to download the journal and **Open matter** to restore it.
No ambient browser storage or server stores the matter. A download is not proof
that the user retained the file. Client/lawyer selection is a local workflow
choice, not authentication; journals are not encrypted or tamper-proof.

## Validation and publication

```sh
python -m unittest discover -s tests -p 'test_*.py'
node tests/matter/holistic_runtime.mjs .prism/build/<build-id>/view/browser
node tests/matter/core_runtime.mjs .prism/build/<build-id>
npm ci --prefix tests/matter
CHROMIUM_EXECUTABLE=/path/to/chromium \
  node tests/matter/run_browser.mjs .prism/build/<build-id>/view/browser
```

Native test instructions and evidence boundaries are in
[docs/SEMANTIC_MATTER.md](docs/SEMANTIC_MATTER.md). A successful build, kernel
proof, or development-browser run is not a full PrismPM verification attestation.
CI checks model drift and sanitization before constructing the SDK. The SDK's
`prismpm verify` owns the application build and Lean proof; native, Core-Wasm,
and browser tests then exercise that verified build. Superseded PR runs are
cancelled, while deployments remain serialized without cancellation.

Pages reuses a successful same-repository PR CI artifact only when its complete
Git tree and SDK pin match the merged source. It checks every packaged file's
hash and the verification/build binding before publishing. A changed merge
tree, direct push, fork PR or expired/missing artifact runs full verification.
The final live check still compares the deployed provenance with the verified
artifact. Explanatory changes limited to `README.md` and
`docs/SEMANTIC_MATTER.md` run preflight checks but need no application build or
automatic deployment. Manual workflows retain full verification as needed.

The prior Text/3 excerpt application remains selectable with
`matter.prismpm.toml`. The older portal in `view/`, `site/`, and `docs/*.html`
and its generators remain migration references; they are not the new runtime or
the new Pages artifact. `bin/prism-legal api check` and `check` continue checking
those legacy model-generated artifacts for drift.
