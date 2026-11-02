"""Evidentiary indicator bit-vector sequences (`src/Sequences.lex.tex`, `model/sequences.toml`)
for PrismLegal Reference Matter (Case No. 2030-FAM-9010).

Each sequence represents a Boolean evidentiary indicator across a 64-checkpoint
record window (`2` words of 32 bits each, every word `< 2^32`), addressed by a
canonical Rivest S-expression SHA-256 `kappa` label `(sequence <lexeme qid> <params...>)`.
The Lean 4 kernel decides `sequenceIdsDistinct`, `sequenceKappasDistinct`,
`everyWindowHasExpectedWords`, `everyWordBelowBound`, and `sequenceCountIs`."""

import hashlib
import json
import tomllib

from . import ROOT
from .semantic import (
    BOOL,
    NAT,
    STR,
    b,
    beq,
    blt,
    call,
    definition,
    field_of_each,
    holds,
    if_,
    list_t,
    lst,
    match_list,
    member_string,
    n,
    proj,
    record,
    s,
    structure,
    theorem,
    var,
)

MODULE = ROOT / "src" / "Sequences.lex.tex"
DATA = ROOT / "model" / "sequences.toml"
NAME = "Sequences"
LEAN_MODULE = "PrismLegal.Sequences"
CHUNK_BITS = 32
CHUNK_BOUND = 1 << CHUNK_BITS
WINDOW = 64
SPEC = "prism-legal/sequences/1"


def _sexp_bytes(val):
    if isinstance(val, (list, tuple)):
        return b"(" + b"".join(_sexp_bytes(x) for x in val) + b")"
    raw = str(val).encode("utf-8")
    return f"{len(raw)}:".encode("ascii") + raw


def kappa(value):
    return "sha256:" + hashlib.sha256(_sexp_bytes(value)).hexdigest()


def sequence_kappa(lexeme, parameters=()):
    return kappa(["sequence", lexeme, *[str(p) for p in parameters]])


def chunks(bits):
    out = []
    for i in range(0, len(bits), CHUNK_BITS):
        w = 0
        for k, bit in enumerate(bits[i : i + CHUNK_BITS]):
            if bit:
                w |= 1 << k
        out.append(w)
    return out


def unchunk(words, width=WINDOW):
    bits = [(c >> k) & 1 for c in words for k in range(CHUNK_BITS)]
    return bits[:width]


# Deterministic 64-checkpoint evidentiary bit-vectors over the trial record
def _build_basis():
    one = [1] * WINDOW
    alt = [t % 2 for t in range(WINDOW)]
    week_alt = [(t // 2) % 2 for t in range(WINDOW)]
    routine = [1 if (t % 4 != 3) else 0 for t in range(WINDOW)]
    best_int = [a ^ r for a, r in zip(alt, routine)]  # linear invariant: corroborated-finding = equal-overnights XOR routine-continuity
    joint_dec = [1 if (t % 3 != 2) else 0 for t in range(WINDOW)]
    unilat = [1 ^ j for j in joint_dec]  # linear invariant: unilateral-relocation = one XOR joint-governance
    stip_inc = [1] * WINDOW  # constant stipulated baseline across all 64 checkpoints
    champva = [1] * WINDOW
    dup_med = [1 ^ c for c in champva]  # 0 everywhere: duplicate medical add-on = one XOR champva
    reserve_omitted = [1 if (t % 5 in (0, 2, 4)) else 0 for t in range(WINDOW)]
    crcp162 = list(reserve_omitted)  # exact match: disclosure-reopening = undisclosed-balance
    gps_comp = [1 ^ (a & r) for a, r in zip(alt, routine)]

    raw = [
        ("one", "lexlean.std.bool::true", "Bool.true", [], one, "Constant reference indicator (1 across all 64 record checkpoints)"),
        ("equal-overnights", "prism.legal::equal-overnights", "PrismLegal.Parenting.equalOvernights", [], alt, "Alternating equal parenting time parity (Uniform Domestic Relations Act § 402(a))"),
        ("week-parity", "prism.legal::overnights-of", "PrismLegal.Parenting.overnightsOf", [7], week_alt, "Week-on/week-off block schedule period-4 indicator (Ex. L)"),
        ("routine-continuity", "prism.legal::routine-continuity", "PrismLegal.Parenting.routineContinuity", [], routine, "Daily school, medical, and bedtime continuity indicator (Ex. B, E, K, O)"),
        ("corroborated-finding", "prism.legal::corroborated-finding", "PrismLegal.Litigation.corroboratedFinding", [], best_int, "Composite Uniform Domestic Relations Act § 402(a) corroborated-finding indicator"),
        ("joint-governance", "prism.legal::joint-governance", "PrismLegal.Governance.jointGovernance", [], joint_dec, "Joint major decision-making & mutual consent indicator (Ex. A, D, L)"),
        ("unilateral-act", "prism.legal::unilateral-action", "PrismLegal.Governance.unilateralAction", [], unilat, "Unilateral relocation / schedule cut indicator (one XOR joint-governance)"),
        ("stipulated-income", "prism.legal::stipulated-income", "PrismLegal.Remedies.stipulatedIncome", [], stip_inc, "Stipulated JTMC income baseline ($8,000/mo vs. $5,000/mo, Ex. N)"),
        ("statutory-benefit", "prism.legal::statutory-benefit-covered", "PrismLegal.Remedies.statutoryBenefitCovered", [], champva, "38 U.S.C. § 1781 statutory dependent healthcare coverage (Ex. E)"),
        ("duplicate-expense", "prism.legal::duplicate-expense-addon", "PrismLegal.Remedies.duplicateExpenseAddon", [], dup_med, "Duplicate medical insurance add-on (vanishes under 38 U.S.C. § 1781, Ex. N vs. OP Ex. 2)"),
        ("reserve-omission", "prism.legal::undisclosed-balance", "PrismLegal.Disclosure.undisclosedBalance", [], reserve_omitted, "Undisclosed $30,000.00 escrow bank accounts indicator (Ex. G, H, J)"),
        ("disclosure-reopening", "prism.legal::mandatory-disclosure-reopening", "PrismLegal.Disclosure.mandatoryDisclosureReopening", [], crcp162, "FRCP 26(e) / Rule 16.2(e)(10) mandatory reopening trigger (equals reserve-omission)"),
        ("order-compliant", "prism.legal::court-order-compliant", "PrismLegal.Compliance.courtOrderCompliant", [], gps_comp, "512-yd transit telemetry & order-compliance indicator (Ex. A, J, M)"),
    ]
    rows = []
    for sid, lex, lean, params, bits, desc in raw:
        rows.append(
            {
                "id": sid,
                "lexeme": lex,
                "lean": lean,
                "parameters": params,
                "kappa": sequence_kappa(lex, params),
                "window": chunks(bits),
                "description": desc,
            }
        )
    return rows


BASIS_ROWS = _build_basis()


def default_data():
    return {"spec": SPEC, "window": WINDOW, "sequence": BASIS_ROWS}


def load():
    if DATA.exists():
        d = tomllib.loads(DATA.read_text())
        if d.get("sequence"):
            return d
    return default_data()


def render_toml(data=None):
    data = default_data() if data is None else data
    lines = [
        "# Evidentiary indicator bit-vector sequences (src/Sequences.lex.tex)",
        f'spec = "{SPEC}"',
        f"window = {WINDOW}",
        "",
    ]
    for r in data["sequence"]:
        lines += [
            "[[sequence]]",
            f'id = {json.dumps(r["id"])}',
            f'lexeme = {json.dumps(r["lexeme"])}',
            f'lean = {json.dumps(r["lean"])}',
            f'parameters = [{", ".join(str(p) for p in r["parameters"])}]',
            f'kappa = {json.dumps(r["kappa"])}',
            f'window = [{", ".join(str(w) for w in r["window"])}]',
            f'description = {json.dumps(r["description"])}',
            "",
        ]
    return "\n".join(lines)


SEQ_T = {"kind": "named", "member": {"name": "Sequence"}, "arguments": []}
LN = list_t(NAT)
LLN = list_t(LN)
LS = list_t(STR)


def _and(a, c):
    return {"kind": "and", "left": a, "right": c}


def _not(a):
    return {"kind": "not", "value": a}


def _len(x):
    return {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [x]}


def declarations(data=None):
    data = default_data() if data is None else data
    seqs = data["sequence"]
    expected_words = WINDOW // CHUNK_BITS
    h, t = var("head"), var("tail")
    return [
        structure(
            "Sequence",
            [
                ("id", STR),
                ("lexeme", STR),
                ("lean", STR),
                ("parameters", LN),
                ("kappa", STR),
                ("window", LN),
            ],
        ),
        member_string(),
        definition(
            "distinctStrings",
            BOOL,
            match_list(
                var("values"),
                b(True),
                "head",
                "tail",
                _and(_not(call("memberString", h, t)), call("distinctStrings", t)),
            ),
            parameters=[("values", LS)],
            recursive="values",
        ),
        definition("windowLength", NAT, n(WINDOW), executable=True),
        definition(
            "sequences",
            list_t(SEQ_T),
            lst(
                [
                    record(
                        "Sequence",
                        id=s(r["id"]),
                        lexeme=s(r["lexeme"]),
                        lean=s(r["lean"]),
                        parameters=lst([n(p) for p in r["parameters"]], NAT),
                        kappa=s(r["kappa"]),
                        window=lst([n(w) for w in r["window"]], NAT),
                    )
                    for r in seqs
                ],
                SEQ_T,
            ),
            executable=True,
        ),
        definition(
            "windows",
            LLN,
            lst([lst([n(w) for w in r["window"]], NAT) for r in seqs], LN),
            executable=True,
        ),
        field_of_each("idsOf", SEQ_T, "id"),
        field_of_each("kappasOf", SEQ_T, "kappa"),
        definition(
            "wordsBelow",
            BOOL,
            match_list(var("ws"), b(True), "head", "tail", _and(blt(h, n(CHUNK_BOUND)), call("wordsBelow", t))),
            parameters=[("ws", LN)],
            recursive="ws",
        ),
        definition(
            "windowsValid",
            BOOL,
            match_list(
                var("xs"),
                b(True),
                "head",
                "tail",
                _and(
                    _and(beq(_len(proj(h, "window")), n(expected_words)), call("wordsBelow", proj(h, "window"))),
                    call("windowsValid", t),
                ),
            ),
            parameters=[("xs", list_t(SEQ_T))],
            recursive="xs",
        ),
        definition("sequenceCount", NAT, _len(call("sequences"))),
        holds("sequenceIdsDistinct", call("distinctStrings", call("idsOf", call("sequences")))),
        holds("sequenceKappasDistinct", call("distinctStrings", call("kappasOf", call("sequences")))),
        holds("everyWindowValid", call("windowsValid", call("sequences"))),
        theorem("sequenceCountIs", call("sequenceCount"), n(len(seqs)), "reflexivity"),
    ]


def render(data=None):
    from . import lexmod

    return lexmod.module(NAME, declarations(data))


def sync():
    data = default_data()
    DATA.parent.mkdir(parents=True, exist_ok=True)
    MODULE.parent.mkdir(parents=True, exist_ok=True)
    toml_text = render_toml(data)
    mod_text = render(data)
    changed = False
    if not DATA.exists() or DATA.read_text() != toml_text:
        DATA.write_text(toml_text)
        changed = True
    if not MODULE.exists() or MODULE.read_text() != mod_text:
        MODULE.write_text(mod_text)
        changed = True
    return {"module": "src/Sequences.lex.tex", "sequences": len(data["sequence"]), "changed": changed}


def check():
    data = default_data()
    if not DATA.exists() or DATA.read_text() != render_toml(data):
        return {"ok": False, "reason": "model/sequences.toml drifted; run `bin/prism-legal api sync`"}
    if not MODULE.exists() or MODULE.read_text() != render(data):
        return {"ok": False, "reason": "src/Sequences.lex.tex drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}
