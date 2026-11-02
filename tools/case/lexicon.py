"""Combined LexLean lexicon for PrismLegal: builtin core/std entries
plus project language packages (`prism.arch`, `prism.qual`, `prism.sec`, `prism.legal`),
indexed by qualified ID, by Lean denotation, and by surface."""

from dataclasses import dataclass
import json
from pathlib import Path
import tomllib

from . import ROOT

BUILTIN = Path(__file__).with_name("builtin_lexicon.json")
LANG_DIR = ROOT / "language"
CASE_LEX_DIR = LANG_DIR / "prism.legal"

DOMAIN_ENTRIES = [
    {
        "id": "equal-overnights",
        "category": "function",
        "signature": "(pi ((explicit c (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Parenting",
        "name": "PrismLegal.Parenting.equalOvernights",
        "surface": "equalOvernights",
    },
    {
        "id": "routine-continuity",
        "category": "function",
        "signature": "(pi ((explicit c (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Parenting",
        "name": "PrismLegal.Parenting.routineContinuity",
        "surface": "routineContinuity",
    },
    {
        "id": "corroborated-finding",
        "category": "function",
        "signature": "(pi ((explicit c (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Litigation",
        "name": "PrismLegal.Litigation.corroboratedFinding",
        "surface": "corroboratedFinding",
    },
    {
        "id": "overnights-of",
        "category": "function",
        "signature": "(pi ((explicit p (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Parenting",
        "name": "PrismLegal.Parenting.overnightsOf",
        "surface": "overnights",
    },
    {
        "id": "joint-governance",
        "category": "function",
        "signature": "(pi ((explicit d (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Governance",
        "name": "PrismLegal.Governance.jointGovernance",
        "surface": "jointGovernance",
    },
    {
        "id": "mutual-consent",
        "category": "function",
        "signature": "(pi ((explicit d (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Governance",
        "name": "PrismLegal.Governance.mutualConsent",
        "surface": "mutualConsent",
    },
    {
        "id": "unilateral-action",
        "category": "function",
        "signature": "(pi ((explicit d (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Governance",
        "name": "PrismLegal.Governance.unilateralAction",
        "surface": "unilateralAction",
    },
    {
        "id": "stipulated-income",
        "category": "function",
        "signature": "(pi ((explicit p (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Remedies",
        "name": "PrismLegal.Remedies.stipulatedIncome",
        "surface": "stipulatedIncome",
    },
    {
        "id": "combined-baseline",
        "category": "function",
        "signature": "(pi ((explicit m (const lexlean.std.nat::nat)) (explicit f (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 2,
        "frame": "call",
        "module": "PrismLegal.Remedies",
        "name": "PrismLegal.Remedies.combinedBaseline",
        "surface": "combinedBaseline",
    },
    {
        "id": "guideline-remedy",
        "category": "function",
        "signature": "(pi ((explicit m (const lexlean.std.nat::nat)) (explicit f (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 2,
        "frame": "call",
        "module": "PrismLegal.Remedies",
        "name": "PrismLegal.Remedies.guidelineRemedy",
        "surface": "guidelineRemedy",
    },
    {
        "id": "statutory-benefit-covered",
        "category": "function",
        "signature": "(pi ((explicit c (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Remedies",
        "name": "PrismLegal.Remedies.statutoryBenefitCovered",
        "surface": "statutoryBenefitCovered",
    },
    {
        "id": "duplicate-expense-addon",
        "category": "function",
        "signature": "(pi ((explicit c (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Remedies",
        "name": "PrismLegal.Remedies.duplicateExpenseAddon",
        "surface": "duplicateExpenseAddon",
    },
    {
        "id": "direct-party-performance",
        "category": "function",
        "signature": "(pi ((explicit c (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Remedies",
        "name": "PrismLegal.Remedies.directPartyPerformance",
        "surface": "directPartyPerformance",
    },
    {
        "id": "third-party-vendor-addon",
        "category": "function",
        "signature": "(pi ((explicit c (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Remedies",
        "name": "PrismLegal.Remedies.thirdPartyVendorAddon",
        "surface": "thirdPartyVendorAddon",
    },
    {
        "id": "undisclosed-balance",
        "category": "function",
        "signature": "(pi ((explicit a (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Disclosure",
        "name": "PrismLegal.Disclosure.undisclosedBalance",
        "surface": "undisclosedBalance",
    },
    {
        "id": "sworn-omission",
        "category": "function",
        "signature": "(pi ((explicit a (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Disclosure",
        "name": "PrismLegal.Disclosure.swornOmission",
        "surface": "swornOmission",
    },
    {
        "id": "mandatory-disclosure-reopening",
        "category": "function",
        "signature": "(pi ((explicit a (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Disclosure",
        "name": "PrismLegal.Disclosure.mandatoryDisclosureReopening",
        "surface": "mandatoryDisclosureReopening",
    },
    {
        "id": "verified-telemetry-distance",
        "category": "function",
        "signature": "(pi ((explicit t (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Compliance",
        "name": "PrismLegal.Compliance.verifiedTelemetryDistance",
        "surface": "verifiedTelemetryDistance",
    },
    {
        "id": "court-order-compliant",
        "category": "function",
        "signature": "(pi ((explicit t (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Compliance",
        "name": "PrismLegal.Compliance.courtOrderCompliant",
        "surface": "courtOrderCompliant",
    },
    {
        "id": "uncompensated-research-revenue",
        "category": "function",
        "signature": "(pi ((explicit y (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Remedies",
        "name": "PrismLegal.Remedies.uncompensatedResearchRevenue",
        "surface": "uncompensatedResearchRevenue",
    },
    {
        "id": "habitability-breach",
        "category": "function",
        "signature": "(pi ((explicit u (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Housing",
        "name": "PrismLegal.Housing.habitabilityBreach",
        "surface": "habitabilityBreach",
    },
    {
        "id": "rent-abatement-cents",
        "category": "function",
        "signature": "(pi ((explicit u (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Housing",
        "name": "PrismLegal.Housing.rentAbatementCents",
        "surface": "rentAbatementCents",
    },
    {
        "id": "combined-disability-rating",
        "category": "function",
        "signature": "(pi ((explicit v (const lexlean.std.nat::nat))) (const lexlean.std.nat::nat))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Veterans",
        "name": "PrismLegal.Veterans.combinedDisabilityRating",
        "surface": "combinedDisabilityRating",
    },
    {
        "id": "tdiu-schedular-eligible",
        "category": "function",
        "signature": "(pi ((explicit v (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Veterans",
        "name": "PrismLegal.Veterans.tdiuSchedularEligible",
        "surface": "tdiuSchedularEligible",
    },
    {
        "id": "reasonable-accommodation-duty",
        "category": "function",
        "signature": "(pi ((explicit e (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Employment",
        "name": "PrismLegal.Employment.reasonableAccommodationDuty",
        "surface": "reasonableAccommodationDuty",
    },
    {
        "id": "chain-of-title-verified",
        "category": "function",
        "signature": "(pi ((explicit d (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Commercial",
        "name": "PrismLegal.Commercial.chainOfTitleVerified",
        "surface": "chainOfTitleVerified",
    },
    {
        "id": "fiduciary-accounting-duty",
        "category": "function",
        "signature": "(pi ((explicit m (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Governance",
        "name": "PrismLegal.Governance.fiduciaryAccountingDuty",
        "surface": "fiduciaryAccountingDuty",
    },
    {
        "id": "multimodal-upload-authenticated",
        "category": "function",
        "signature": "(pi ((explicit x (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Evidence",
        "name": "PrismLegal.Evidence.multimodalUploadAuthenticated",
        "surface": "multimodalUploadAuthenticated",
    },
    {
        "id": "rule-106-completeness-required",
        "category": "function",
        "signature": "(pi ((explicit x (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Evidence",
        "name": "PrismLegal.Evidence.rule106CompletenessRequired",
        "surface": "rule106CompletenessRequired",
    },
    {
        "id": "sha256-custody-verified",
        "category": "function",
        "signature": "(pi ((explicit x (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Evidence",
        "name": "PrismLegal.Evidence.sha256CustodyVerified",
        "surface": "sha256CustodyVerified",
    },
    {
        "id": "filing-deadline-timely",
        "category": "function",
        "signature": "(pi ((explicit f (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Procedure",
        "name": "PrismLegal.Procedure.filingDeadlineTimely",
        "surface": "filingDeadlineTimely",
    },
    {
        "id": "proposed-finding-admissible",
        "category": "function",
        "signature": "(pi ((explicit f (const lexlean.std.nat::nat))) (sort prop))",
        "surface_arity": 1,
        "frame": "call",
        "module": "PrismLegal.Procedure",
        "name": "PrismLegal.Procedure.proposedFindingAdmissible",
        "surface": "proposedFindingAdmissible",
    },
]


def _render_entry_toml(e):
    slots = " (token comma) (space) ".join(f"(slot {i})" for i in range(e["surface_arity"]))
    math_render = f"(seq (operator-name {e['surface']}) (paren (seq {slots})))" if e["surface_arity"] else f"(operator-name {e['surface']})"
    lines = [
        'spec = "lexlean/entry/1"',
        f'id = "{e["id"]}"',
        f'category = "{e["category"]}"',
        f'signature = "{e["signature"]}"',
        f'surface_arity = {e["surface_arity"]}',
        f'frame = "{e["frame"]}"',
        "",
        "[denotation]",
        'kind = "lean"',
        f'module = "{e["module"]}"',
        f'name = "{e["name"]}"',
        "",
        "[[form]]",
        f'id = "{e["id"]}"',
        'channel = "math"',
        f'surface = "{e["surface"]}"',
        "canonical_source = true",
        "features = []",
        "",
        "[render]",
        f'math = "{math_render}"',
        "",
    ]
    return "\n".join(lines)


def sync_domain_lexicon():
    entries_dir = CASE_LEX_DIR / "entries"
    entries_dir.mkdir(parents=True, exist_ok=True)
    lex_toml = "\n".join(
        [
            'spec = "lexlean/lexicon/1"',
            'package = "prism.legal"',
            'version = "1.0.0"',
            'language = "1.2"',
            'imports = ["lexlean.core@1.2.0", "lexlean.std.bool@1.2.0", "lexlean.std.int@1.2.0", "lexlean.std.nat@1.2.0", "prism.arch@1.0.0", "prism.qual@1.0.0", "prism.sec@1.0.0"]',
            "",
        ]
    )
    changed = False
    lex_file = CASE_LEX_DIR / "lexicon.toml"
    if not lex_file.exists() or lex_file.read_text() != lex_toml:
        lex_file.write_text(lex_toml)
        changed = True
    for e in DOMAIN_ENTRIES:
        p = entries_dir / f"{e['id']}.toml"
        body = _render_entry_toml(e)
        if not p.exists() or p.read_text() != body:
            p.write_text(body)
            changed = True
    return {"package": "prism.legal", "entries": len(DOMAIN_ENTRIES), "changed": changed}


@dataclass
class Entry:
    qid: str
    category: str
    frame: str
    arity: int
    surface: str | None
    precedence: int | None = None
    associativity: str | None = None
    signature: str | None = None
    lean_name: str | None = None
    lean_module: str | None = None
    core_constructor: str | None = None
    path: Path | None = None
    project: str | None = None
    render_math: str | None = None

    @property
    def package(self):
        return self.qid.split("::")[0]

    @property
    def id(self):
        return self.qid.split("::")[1]

    def row(self):
        return {
            "id": self.qid,
            "surface": self.surface,
            "frame": self.frame,
            "arity": self.arity,
            "lean": self.lean_name,
            "category": self.category,
        }


class Lexicon:
    def __init__(self):
        sync_domain_lexicon()
        self.entries: dict[str, Entry] = {}
        self.by_lean: dict[str, list[Entry]] = {}
        self.imports: dict[str, list[str]] = {}
        self.lexicon_dir: dict[str, Path] = {}
        self._load_builtin()
        for lexicon_toml in sorted(LANG_DIR.glob("*/lexicon.toml")):
            self._load_lexicon(lexicon_toml)

    def _load_builtin(self):
        data = json.loads(BUILTIN.read_text())
        self.builtin_revision = data["lexlean_revision"]
        for qid, e in data["entries"].items():
            den = e.get("denotation") or {}
            entry = Entry(
                qid,
                e.get("category"),
                e.get("frame"),
                e.get("arity") or 0,
                e.get("surface"),
                e.get("precedence"),
                e.get("associativity"),
                e.get("signature"),
                den.get("name"),
                den.get("module"),
                den.get("constructor"),
                None,
                "builtin",
            )
            self._add(entry)

    def _load_lexicon(self, lexicon_toml: Path):
        meta = tomllib.loads(lexicon_toml.read_text())
        package = meta["package"]
        self.imports[package] = [i.split("@")[0] for i in meta.get("imports", [])]
        self.lexicon_dir[package] = lexicon_toml.parent
        for path in sorted((lexicon_toml.parent / "entries").glob("*.toml")):
            e = tomllib.loads(path.read_text())
            forms = [f for f in e.get("form", []) if f.get("channel") == "math"] or [
                f for f in e.get("form", []) if f.get("channel") == "text"
            ]
            den = e.get("denotation") or {}
            entry = Entry(
                f"{package}::{e['id']}",
                e.get("category"),
                e.get("frame"),
                e.get("surface_arity", 0),
                forms[0]["surface"] if forms else None,
                e.get("precedence"),
                e.get("associativity"),
                e.get("signature"),
                den.get("name"),
                den.get("module"),
                den.get("constructor"),
                path,
                "case",
                (e.get("render") or {}).get("math"),
            )
            self._add(entry)

    def _add(self, entry: Entry):
        self.entries[entry.qid] = entry
        if entry.lean_name:
            self.by_lean.setdefault(entry.lean_name, []).append(entry)

    def get(self, qid: str):
        return self.entries.get(qid)

    def for_lean(self, name: str, visible=None):
        found = self.by_lean.get(name, [])
        if visible is not None:
            for e in found:
                if e.package in visible or e.project == "builtin":
                    return e
        return found[0] if found else None

    def visible_from(self, package: str):
        seen, todo = set(), [package]
        while todo:
            p = todo.pop()
            if p in seen:
                continue
            seen.add(p)
            todo.extend(self.imports.get(p, []))
        return seen


def sync():
    return sync_domain_lexicon()


def check() -> bool:
    res = sync_domain_lexicon()
    return not res["changed"]

