# PrismLegal

PrismLegal is a local legal matter workspace authored in LexLean and compiled
by PrismPM. Its evidence and inference discipline follows
[afflom/rule30](https://github.com/afflom/rule30): source material, reviewed
interpretations, rules, and conclusions remain distinguishable and connected.
No remote model, inference service, or model credentials are used.

The compiled application lets a client or lawyer create a matter, import actual
UTF-8 resources, review passages, record goals and jurisdiction, and connect
reviewed authority to conditional strategies. Reviewed source wording teaches
facet and meaning suggestions. A passage can support several interpretations. Further learned aspects stay
visible as focused review steps, with the original resource and line identified;
withdrawal preserves their history. Changes invalidate dependent conclusions
and expose related facts and strategies. A saved matter file replays the complete accepted command history.
The view offers the next useful form, with focused facet inspection and
supporting source context available when needed. Source locations distinguish
equal interpretations during correction or withdrawal and retain the original
line and version after a resource changes. A chronology combines selected date
aspects, orders valid dates, and keeps uncertain or conflicting dates visible
for review.

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
inventory. The generic file-session capability is proposed upstream in
[PrismPM #495](https://github.com/UOR-Foundation/PrismPM/pull/495), following
[issue #491](https://github.com/UOR-Foundation/PrismPM/issues/491). The app uses
that fix directly while it awaits upstream review. Its bounded portable session
transport fix is tracked in [#496](https://github.com/UOR-Foundation/PrismPM/issues/496),
with the carried dependency patch identified in verification evidence. Legal
behavior stays here.
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
npm ci --prefix tests/matter
CHROMIUM_EXECUTABLE=/path/to/chromium \
  node tests/matter/run_browser.mjs .prism/build/<build-id>/view/browser
```

Native test instructions and evidence boundaries are in
[docs/SEMANTIC_MATTER.md](docs/SEMANTIC_MATTER.md). A successful build, kernel
proof, or development-browser run is not a full PrismPM verification attestation.
CI runs the pinned SDK verification pipeline without a static fallback. Pages
publishes only the emitted `matter-site/` after that gate passes.

The prior Text/3 excerpt application remains selectable with
`matter.prismpm.toml`. The older portal in `view/`, `site/`, and `docs/*.html`
and its generators remain migration references; they are not the new runtime or
the new Pages artifact. `bin/prism-legal api check` and `check` continue checking
those legacy model-generated artifacts for drift. No deployment is implied by
the draft implementation PR.
