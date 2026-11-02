"""The `prism-legal` CLI command surface modeled as a LexLean semantic module (`src/Api.lex.tex`)."""

from . import ROOT, lexmod, semantic
from .semantic import BOOL, NAT, STR, b, call, definition, lst, n, named, record, s, strings, structure, theorem

MODULE = ROOT / "src" / "Api.lex.tex"

PRODUCTION_ROOTS = {
    "commands": {"effects": ["allocation"], "targets": ["rust-std"]},
    "commandCount": {"effects": ["allocation"], "targets": ["rust-std"]},
}

COMMANDS = [
    {
        "name": "brief",
        "path": ["brief"],
        "help": "Print the complete trial brief: Public-Benefit Charter, Opening Statement pillars, stipulated facts, disputed issues, and top cross-exam pivots.",
        "arguments": [],
    },
    {
        "name": "claim",
        "path": ["claim"],
        "help": "Inspect a specific case claim (CLM-01 to CLM-24) with its supporting exhibits, statutory anchor, and dependents.",
        "arguments": [{"name": "id", "kind": "string", "many": False, "optional": False, "help": "Claim ID (e.g. CLM-22)"}],
    },
    {
        "name": "exhibit",
        "path": ["exhibit"],
        "help": "Inspect any Respondent (Ex-A to Ex-O) or Petitioner (OP-Ex-01 to OP-Ex-15) exhibit with its trial purpose and pivot.",
        "arguments": [{"name": "id", "kind": "string", "many": False, "optional": False, "help": "Exhibit ID (e.g. Ex-A or OP-Ex-13)"}],
    },
    {
        "name": "witness",
        "path": ["witness"],
        "help": "Inspect examination plan and cross-examination points for a witness (W-01 to W-10).",
        "arguments": [{"name": "id", "kind": "string", "many": False, "optional": False, "help": "Witness ID (e.g. W-01 or W-02)"}],
    },
    {
        "name": "audit",
        "path": ["audit"],
        "help": "List all 16 opposing allegations / cross-examination traps with their status, rebuttal exhibits, and Opening-Statement-aligned pivots.",
        "arguments": [{"name": "status", "kind": "string", "many": False, "optional": True, "help": "Filter by status"}],
    },
    {
        "name": "tune",
        "path": ["tune"],
        "help": "Inspect, export, or apply Lawyer & Client model-tuning patches and strategy co-design agenda (`model/tuning.json`).",
        "arguments": [{"name": "action", "kind": "string", "many": False, "optional": True, "help": "status | export | apply | reset"}],
    },
    {
        "name": "meta",
        "path": ["meta"],
        "help": "Inspect the formal Legal Meta-Theory & International Standards register (Hohfeldian jural relations, OASIS LegalRuleML rules & overrides, ASPIC+ argumentation graph, Akoma Ntoso FRBR URIs, ISO 15489/27037 chain of custody).",
        "arguments": [{"name": "section", "kind": "string", "many": False, "optional": True, "help": "all | hohfeld | rules | arguments | akn | coc"}],
    },
    {
        "name": "portal",
        "path": ["portal"],
        "help": "Inspect or serve the Multi-Tenant Public-Benefit Legal Platform (`status` or `serve --port 8766`): Auth Providers, Cryptographic Sharing, Firms, Courts, Legal Frameworks, Clients, Lawyers, and Multi-Domain Cases.",
        "arguments": [{"name": "action", "kind": "string", "many": False, "optional": True, "help": "status | serve"}],
    },
    {
        "name": "convert",
        "path": ["convert"],
        "help": "Compile formal legal propositions of PrismLegal into deterministic controlled English (`src/Convert.lex.tex` + `prism.legal` lexicon, zero external LLM).",
        "arguments": [{"name": "id", "kind": "string", "many": False, "optional": True, "help": "Optional proposition or refusal fixture ID (e.g. PROP-01 or REF-13)"}],
    },
    {
        "name": "engine",
        "path": ["engine"],
        "help": "Run the compiled neuromorphic courtroom strategy engine (`src/Engine.lex.tex` & certified Rust crate): Hebbian plasticity (`learn_all`), weight-ordered strategy scheduling (`schedule`), and 360-minute homeostatic trial clock.",
        "arguments": [{"name": "action", "kind": "string", "many": False, "optional": True, "help": "status | schedule | learn | rust"}],
    },
    {
        "name": "discover",
        "path": ["discover"],
        "help": "Run the compiled F_2 relation & Berlekamp-Massey recurrence discovery engine (`src/Discovery.lex.tex` & certified Rust crate) over the 13 evidentiary bit-vector sequences (`src/Sequences.lex.tex`).",
        "arguments": [{"name": "action", "kind": "string", "many": False, "optional": True, "help": "status | relations | recurrences | rust"}],
    },
    {
        "name": "intake",
        "path": ["intake"],
        "help": "Run the compiled in-browser intake classifiers and per-node multi-head attention extrapolation network (`src/Intake.lex.tex`, 12 schema classifiers, 18 node attention heads).",
        "arguments": [{"name": "action", "kind": "string", "many": False, "optional": True, "help": "status | heads | schemas | fixtures"}],
    },
    {
        "name": "exam",
        "path": ["exam"],
        "help": "Inspect Lead Trial Counsel's Intended Direct Examination of Respondent (`src/DirectExam.lex.tex`, 6 chapters, 36 Q&A blocks, yellow highlights, red strikethroughs, and exhibit admission moves).",
        "arguments": [{"name": "filter", "kind": "string", "many": False, "optional": True, "help": "all | highlights | admissions | stricken | <DX-ID or CH-ID>"}],
    },
    {
        "name": "visual",
        "path": ["visual"],
        "help": "Inspect handwritten journal forensics (`OP Ex. 13`), visual/scanned exhibit extractions, 12-photo catalog (`Ex. E`, `Ex. O`, `Ex. L`), and the 30-exhibit Content-Meaning & Intent Matrix (`src/VisualEvidence.lex.tex`).",
        "arguments": [{"name": "section", "kind": "string", "many": False, "optional": True, "help": "all | mappings | diary | forensics | photos"}],
    },
    {
        "name": "sanitize",
        "path": ["sanitize"],
        "help": "Run the Zero-PII & Public-Benefit Sanitization Auditor across the entire prism-legal repository.",
        "arguments": [],
    },
    {
        "name": "api_production",
        "path": ["api", "production"],
        "help": "Emit certified Rust production packages (`prism_legal_*`) from `production/request.json` via `lexlean production build`.",
        "arguments": [],
    },
    {
        "name": "api_sync",
        "path": ["api", "sync"],
        "help": "Regenerate all LexLean semantic modules (src/*.lex.tex), PrismPM registers (model/*.toml), schemas, and conformance suites from the single domain model.",
        "arguments": [],
    },
    {
        "name": "api_check",
        "path": ["api", "check"],
        "help": "Verify zero drift and zero-PII sanitization across the domain model, src/*.lex.tex modules, model/*.toml registers, schemas, and CONFORMANCE.md.",
        "arguments": [],
    },
    {
        "name": "check",
        "path": ["check"],
        "help": "Run LexLean static type and lexicon checking across all semantic modules in src/ and stdlib/.",
        "arguments": [],
    },
    {
        "name": "verify",
        "path": ["verify"],
        "help": "Run full Lean 4 kernel verification (`lexlean verify`) across all 17 platform & case semantic modules and decided theorems.",
        "arguments": [],
    },
    {
        "name": "view_render",
        "path": ["view", "render"],
        "help": "Mechanically render the GitHub-Pages-ready Public-Benefit Platform Hub (`index.html`), Client Workspace (`client.html`), Counsel Workbench (`lawyer.html`), and Courtroom Mode (`courtroom.html`), SVG graphics, and Markdown/JSON sheets directly from the verified model.",
        "arguments": [{"name": "out", "kind": "string", "many": False, "optional": True, "help": "Output directory (default: view)"}],
    },
]


def surface():
    return COMMANDS


def declarations(rows=None):
    rows = rows or surface()
    arg_t = named("Argument")
    cmd_t = named("Command")
    arg_rec = lambda a: record(
        "Argument",
        name=s(a["name"]),
        kind=s(a["kind"]),
        many=b(a["many"]),
        optional=b(a["optional"]),
        help=s(a["help"]),
    )
    cmd_rec = lambda c: record(
        "Command",
        name=s(c["name"]),
        path=strings(c["path"]),
        help=s(c["help"]),
        arguments=lst([arg_rec(a) for a in c["arguments"]], arg_t),
    )
    return [
        structure("Argument", [("name", STR), ("kind", STR), ("many", BOOL), ("optional", BOOL), ("help", STR)]),
        structure("Command", [("name", STR), ("path", semantic.list_t(STR)), ("help", STR), ("arguments", semantic.list_t(arg_t))]),
        definition(
            "commands",
            semantic.list_t(cmd_t),
            lst([cmd_rec(c) for c in rows], cmd_t),
            executable=True,
            production=PRODUCTION_ROOTS["commands"],
        ),
        definition(
            "commandCount",
            NAT,
            {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [call("commands")]},
            executable=True,
            production=PRODUCTION_ROOTS["commandCount"],
        ),
        theorem("commandCountIs", call("commandCount"), n(len(rows)), proof="reflexivity"),
    ]


def render():
    return lexmod.module("Api", declarations(), title="PrismLegal Public-Benefit Platform Automation Command Surface")


def sync():
    MODULE.parent.mkdir(parents=True, exist_ok=True)
    text = render()
    changed = not MODULE.exists() or MODULE.read_text() != text
    if changed:
        MODULE.write_text(text)
    return {"module": str(MODULE.relative_to(ROOT)), "commands": len(surface()), "changed": changed}


def check():
    if not MODULE.exists():
        return {"ok": False, "reason": "src/Api.lex.tex is missing; run `bin/prism-legal api sync`"}
    ok = MODULE.read_text() == render()
    return {"ok": ok, "reason": None if ok else "Api.lex.tex drifted; run `bin/prism-legal api sync`"}

