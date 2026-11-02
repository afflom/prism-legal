"""The neuromorphic courtroom learning, strategy scheduling, and trial-clock
homeostasis engine as a compiled LexLean semantic module (`src/Engine.lex.tex`).

`src/Engine.lex.tex` (`PrismLegal.Engine`) declares:
- Homeostasis (Trial Clock Budget Regulation): the 6 stages of the 360-minute
  Permanent Orders Hearing (`opening-and-stipulations`, `petitioner-case-and-cross`,
  `respondent-direct-walkthrough`, `corroborating-witnesses`,
  `financial-and-16-2-impeachment`, `closing-and-final-orders-gate`), with
  kernel-decided theorems (`stageBudgetsFillTheTick`, `stageBudgetsFitTheTimeout`,
  `gateKeepsItsShare`) proving that the stage budgets sum to 360 minutes and
  reserve the 60-minute closing/final-orders gate (`gateMinimum = 45`).
- The Portfolio of Courtroom Examination & Rebuttal Strategies (`PORTFOLIO`),
  each pinned by the SHA-256 digest of its courtroom template (`tools/case/templates/`).
- The Neuromorphic Learning Layer:
  - Units: basis evidentiary sequences & claims (`Sequences.lex.tex`, `Register.lex.tex`).
  - Synapses: courtroom strategy weights per statutory/examination family (`Weight`).
  - Events: rehearsal & examination outcomes (`Outcome { strategy, family, success }`).
  - Plasticity: bounded Hebbian rule `learn(w, success)` on integer weights in
    `[W_MIN, W_MAX] = [1, 16]` (`W_INIT = 8`, `RAISE = 2`, `LOWER = 1`),
    `updateWeight`, and `learnAll` folding outcomes into the synaptic table.
  - Scheduling: `insertByWeight`, `scheduleFrom`, `schedule` ordering applicable
    strategies by learned weight (ties preserving portfolio order).
  - Consolidation: `committedWeights` persisted in `model/engine.toml` and verified
    in the Lean 4 kernel (`learnStaysInBounds`, `initialWeightsBounded`,
    `committedWeightsBounded`, `learnAllFixture`, `learnAllFixtureBounded`,
    `everyScheduleIsSound` across all 2^4 subsets and all 7 statutory families).
- `learnAll` and `schedule` are executable production roots (`rust-std`) compiled
  to certified safe Rust via `lexlean production build` and driven by `engine_rust.py`."""

import hashlib
import json
from pathlib import Path
import tomllib

from . import ROOT
from .semantic import (
    BOOL,
    NAT,
    STR,
     all_members,
    b,
    beq,
    ble,
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
    strings,
    structure,
    var,
)

MODULE = ROOT / "src" / "Engine.lex.tex"
LEDGER = ROOT / "model" / "engine.toml"
NAME = "Engine"
LEAN_MODULE = "PrismLegal.Engine"
TEMPLATES = Path(__file__).with_name("templates")
EFFECTS = {"effects": ["allocation", "overflow", "recursion"], "targets": ["rust-std"]}
PRODUCTION_ROOTS = {"learnAll": EFFECTS, "schedule": EFFECTS}

# Plasticity parameters (bounded Hebbian rule)
W_MIN, W_MAX, W_INIT, RAISE, LOWER = 1, 16, 8, 2, 1
SUCCESS = ("proved", "mastered", "verified", "rebutted")

# Statutory & courtroom examination families
FAMILIES = [
    "crs-124-parenting-time",
    "crs-124-decision-making",
    "crs-115-child-support",
    "crcp-16-2-disclosure",
    "cre-608-impeachment",
    "crs-129-protection-order",
    "champva-38-usc-1781",
]

PORTFOLIO = [
    {
        "id": "documentary-impeachment",
        "template": "documentary-impeachment.lean.tmpl",
        "title": "Documentary Impeachment (FRE 608(b) / 613 / FRCP 26(e) & Rule 16.2)",
        "statement": "Establish prior sworn omission or allegation, authenticate contemporaneous bank/tax/GPS/OFW exhibit, and close contradiction on the record.",
    },
    {
        "id": "statutory-factor-deduction",
        "template": "statutory-factor-deduction.lean.tmpl",
        "title": "Statutory Factor Deduction (Uniform Domestic Relations Act § 402 & Support Guidelines § 305)",
        "statement": "Map corroborated factual record directly onto statutory best-interests factors (§ 402) and guideline remedy rules (§ 305) for the three minor children.",
    },
    {
        "id": "stipulated-anchor-lock",
        "template": "stipulated-anchor-lock.lean.tmpl",
        "title": "Stipulated Anchor Lock (Pretrial Stipulation & Case Management Order)",
        "statement": "Bind examination to Pretrial stipulations ($8,000/mo vs. $5,000/mo baseline, $0 open-source curriculum draw across 2026-2029 taxes, 38 U.S.C. § 1781 medical coverage).",
    },
    {
        "id": "calm-opening-pivot",
        "template": "calm-opening-pivot.lean.tmpl",
        "title": "Calm Opening-Aligned Pivot (6 Opening Statement Pillars)",
        "statement": "De-escalate adversarial cross-examination trap in one calm sentence and return to child-focused 50/50 stability for the three minor children.",
    },
]


def template_path(strategy):
    return TEMPLATES / next(p["template"] for p in PORTFOLIO if p["id"] == strategy)


def template_digest(strategy):
    h = hashlib.sha256()
    h.update(b"template\0" + template_path(strategy).read_bytes() + b"\0strategy\0" + strategy.encode())
    return "sha256:" + h.hexdigest()


# Homeostatic Trial Clock Workload (360-minute Permanent Orders Hearing)
WORKLOAD = {
    "hearing": "Evidentiary Hearing on Parenting Plan & Support (Case No. 2030-FAM-9010)",
    "courtroom": "Superior Court — Family & Civil Trial Division 7C",
    "timeoutMinutes": 390,
    "setupMinutes": 30,
    "tickBudget": 360,
    "gateMinimum": 45,
    "stages": [
        ("opening-and-stipulations", 30, False),
        ("petitioner-case-and-cross", 120, False),
        ("respondent-direct-walkthrough", 75, False),
        ("corroborating-witnesses", 45, False),
        ("financial-and-16-2-impeachment", 30, False),
        ("closing-and-final-orders-gate", 60, True),
    ],
}


class Mirror:
    """The bounded Hebbian learning rule and weight-ordered scheduler in Python
    (fallback runtime and fixture oracle for `src/Engine.lex.tex`)."""

    @staticmethod
    def learn(w, success):
        if success:
            return w + RAISE if w + RAISE <= W_MAX else W_MAX
        return w - LOWER if W_MIN + LOWER <= w else W_MIN

    @staticmethod
    def weight_of(strategy, fam, table):
        for st, f, v in table:
            if st == strategy and f == fam:
                return v
        return W_INIT

    @staticmethod
    def update(table, strategy, fam, success):
        out, done = [], False
        for st, f, v in table:
            if not done and st == strategy and f == fam:
                out.append((st, f, Mirror.learn(v, success)))
                done = True
            else:
                out.append((st, f, v))
        if not done:
            out.append((strategy, fam, Mirror.learn(W_INIT, success)))
        return out

    @staticmethod
    def learn_all(table, outcomes):
        for strategy, fam, success in outcomes:
            table = Mirror.update(table, strategy, fam, success)
        return table

    @staticmethod
    def insert(fam, table, x, ordered):
        for i, h in enumerate(ordered):
            if Mirror.weight_of(h, fam, table) < Mirror.weight_of(x, fam, table):
                return ordered[:i] + [x] + ordered[i:]
        return ordered + [x]

    @staticmethod
    def schedule(table, fam, applicable):
        ordered = []
        for x in applicable:
            ordered = Mirror.insert(fam, table, x, ordered)
        return ordered


def initial_table():
    return [(p["id"], f, W_INIT) for p in PORTFOLIO for f in FAMILIES]


FIXTURE_OUTCOMES = [
    ("documentary-impeachment", "crcp-16-2-disclosure", True),
    ("documentary-impeachment", "crcp-16-2-disclosure", True),
    ("statutory-factor-deduction", "crs-124-parenting-time", True),
    ("calm-opening-pivot", "crs-124-parenting-time", True),
    ("stipulated-anchor-lock", "crs-115-child-support", True),
    ("documentary-impeachment", "cre-608-impeachment", True),
    ("stipulated-anchor-lock", "champva-38-usc-1781", True),
    ("calm-opening-pivot", "crs-129-protection-order", True),
    ("statutory-factor-deduction", "crs-124-decision-making", True),
    ("calm-opening-pivot", "crcp-16-2-disclosure", False),
]

FIXTURE_SCHEDULES = [
    (
        "crcp-16-2-disclosure",
        ["calm-opening-pivot", "statutory-factor-deduction", "documentary-impeachment", "stipulated-anchor-lock"],
    ),
    (
        "crs-124-parenting-time",
        ["stipulated-anchor-lock", "statutory-factor-deduction", "calm-opening-pivot"],
    ),
    (
        "crs-115-child-support",
        ["documentary-impeachment", "stipulated-anchor-lock", "statutory-factor-deduction"],
    ),
]


def default_committed_table():
    return Mirror.learn_all(initial_table(), FIXTURE_OUTCOMES)


def load_committed_table():
    if LEDGER.exists():
        data = tomllib.loads(LEDGER.read_text())
        rows = data.get("weight", [])
        if rows:
            have = {(r["strategy"], r["family"]): int(r["value"]) for r in rows}
            return [(st, f, have.get((st, f), v)) for st, f, v in initial_table()]
    return default_committed_table()


def render_ledger_toml(committed=None):
    committed = default_committed_table() if committed is None else committed
    lines = [
        "# Consolidated neuromorphic synaptic weights and rehearsal outcomes (src/Engine.lex.tex)",
        'spec = "prism-legal/engine/1"',
        f"w_min = {W_MIN}",
        f"w_max = {W_MAX}",
        f"w_init = {W_INIT}",
        f"raise_step = {RAISE}",
        f"lower_step = {LOWER}",
        "",
    ]
    for st, f, val in committed:
        lines += [
            "[[weight]]",
            f"strategy = {json.dumps(st)}",
            f"family = {json.dumps(f)}",
            f"value = {int(val)}",
            "",
        ]
    for st, f, ok in FIXTURE_OUTCOMES:
        lines += [
            "[[outcome]]",
            f"strategy = {json.dumps(st)}",
            f"family = {json.dumps(f)}",
            f"success = {'true' if ok else 'false'}",
            "",
        ]
    return "\n".join(lines)


WEIGHT_T = {"kind": "named", "member": {"name": "Weight"}, "arguments": []}
OUTCOME_T = {"kind": "named", "member": {"name": "Outcome"}, "arguments": []}
STRATEGY_T = {"kind": "named", "member": {"name": "Strategy"}, "arguments": []}
STAGE_T = {"kind": "named", "member": {"name": "Stage"}, "arguments": []}
LS = list_t(STR)
LN = list_t(NAT)


def _and(a, c):
    return {"kind": "and", "left": a, "right": c}


def _not(a):
    return {"kind": "not", "value": a}


def _eqs(a, c):
    return {"kind": "primitive", "operation": "equal", "result": BOOL, "arguments": [a, c]}


def _p(op, args, result):
    return {"kind": "primitive", "operation": op, "result": result, "arguments": list(args)}


def _add(a, c):
    return {"kind": "add", "left": a, "right": c}


def _sub(a, c):
    return _p("subtract", [a, c], NAT)


def _len(x):
    return _p("length", [x], NAT)


def _cons(h, t):
    return {"kind": "cons", "head": h, "tail": t}


def _nil(t):
    return {"kind": "nil", "element": t}


def _ex(name, result, body, parameters=(), recursive=None):
    return definition(
        name,
        result,
        body,
        parameters=parameters,
        recursive=recursive,
        production=PRODUCTION_ROOTS.get(name),
        executable=True,
    )


def _weight(st, f, v):
    return record("Weight", strategy=s(st), family=s(f), value=n(v))


def _outcome(st, f, ok):
    return record("Outcome", strategy=s(st), family=s(f), success=b(ok))


def _match_nat(scrutinee, zero_body, binder, succ_body):
    return {
        "kind": "match",
        "scrutinee": scrutinee,
        "branches": [
            {"constructor": {"name": "Nat.zero"}, "binders": [], "body": zero_body},
            {"constructor": {"name": "Nat.succ"}, "binders": [binder], "body": succ_body},
        ],
    }


def learning_declarations():
    w, x, h, t = var("w"), var("x"), var("head"), var("tail")
    table, fam, st = var("table"), var("family"), var("strategy")
    matches = lambda r: _and(_eqs(proj(r, "strategy"), st), _eqs(proj(r, "family"), fam))
    return [
        structure("Weight", [("strategy", STR), ("family", STR), ("value", NAT)]),
        structure("Outcome", [("strategy", STR), ("family", STR), ("success", BOOL)]),
        definition("weightMin", NAT, n(W_MIN), executable=True),
        definition("weightMax", NAT, n(W_MAX), executable=True),
        definition("weightInitial", NAT, n(W_INIT), executable=True),
        _ex(
            "learn",
            NAT,
            if_(
                var("success"),
                if_(ble(_add(w, n(RAISE)), n(W_MAX)), _add(w, n(RAISE)), n(W_MAX)),
                if_(ble(n(W_MIN + LOWER), w), _sub(w, n(LOWER)), n(W_MIN)),
            ),
            parameters=[("w", NAT), ("success", BOOL)],
        ),
        _ex(
            "weightOf",
            NAT,
            match_list(
                table,
                n(W_INIT),
                "head",
                "tail",
                if_(matches(h), proj(h, "value"), call("weightOf", st, fam, t)),
            ),
            parameters=[("strategy", STR), ("family", STR), ("table", list_t(WEIGHT_T))],
            recursive="table",
        ),
        _ex(
            "updateWeight",
            list_t(WEIGHT_T),
            match_list(
                table,
                _cons(record("Weight", strategy=st, family=fam, value=call("learn", n(W_INIT), var("success"))), _nil(WEIGHT_T)),
                "head",
                "tail",
                if_(
                    matches(h),
                    _cons(
                        record("Weight", strategy=st, family=fam, value=call("learn", proj(h, "value"), var("success"))),
                        t,
                    ),
                    _cons(h, call("updateWeight", t, st, fam, var("success"))),
                ),
            ),
            parameters=[("table", list_t(WEIGHT_T)), ("strategy", STR), ("family", STR), ("success", BOOL)],
            recursive="table",
        ),
        _ex(
            "learnAll",
            list_t(WEIGHT_T),
            match_list(
                var("outcomes"),
                table,
                "head",
                "tail",
                call(
                    "learnAll",
                    call("updateWeight", table, proj(h, "strategy"), proj(h, "family"), proj(h, "success")),
                    t,
                ),
            ),
            parameters=[("table", list_t(WEIGHT_T)), ("outcomes", list_t(OUTCOME_T))],
            recursive="outcomes",
        ),
        _ex(
            "insertByWeight",
            LS,
            match_list(
                var("ordered"),
                _cons(x, _nil(STR)),
                "head",
                "tail",
                if_(
                    blt(call("weightOf", h, fam, table), call("weightOf", x, fam, table)),
                    _cons(x, _cons(h, t)),
                    _cons(h, call("insertByWeight", fam, table, x, t)),
                ),
            ),
            parameters=[("family", STR), ("table", list_t(WEIGHT_T)), ("x", STR), ("ordered", LS)],
            recursive="ordered",
        ),
        _ex(
            "scheduleFrom",
            LS,
            match_list(
                var("pending"),
                var("ordered"),
                "head",
                "tail",
                call("scheduleFrom", fam, table, t, call("insertByWeight", fam, table, h, var("ordered"))),
            ),
            parameters=[("family", STR), ("table", list_t(WEIGHT_T)), ("pending", LS), ("ordered", LS)],
            recursive="pending",
        ),
        _ex(
            "schedule",
            LS,
            call("scheduleFrom", fam, table, var("applicable"), _nil(STR)),
            parameters=[("table", list_t(WEIGHT_T)), ("family", STR), ("applicable", LS)],
        ),
        definition("inBounds", BOOL, _and(ble(n(W_MIN), w), ble(w, n(W_MAX))), parameters=[("w", NAT)]),
        definition(
            "learnBoundedUpTo",
            BOOL,
            _match_nat(
                var("k"),
                if_(
                    call("inBounds", n(0)),
                    _and(call("inBounds", call("learn", n(0), b(True))), call("inBounds", call("learn", n(0), b(False)))),
                    b(True),
                ),
                "j",
                _and(
                    if_(
                        call("inBounds", _add(var("j"), n(1))),
                        _and(
                            call("inBounds", call("learn", _add(var("j"), n(1)), b(True))),
                            call("inBounds", call("learn", _add(var("j"), n(1)), b(False))),
                        ),
                        b(True),
                    ),
                    call("learnBoundedUpTo", var("j")),
                ),
            ),
            parameters=[("k", NAT)],
            recursive="k",
        ),
        definition(
            "weightsBounded",
            BOOL,
            match_list(table, b(True), "head", "tail", _and(call("inBounds", proj(h, "value")), call("weightsBounded", t))),
            parameters=[("table", list_t(WEIGHT_T))],
            recursive="table",
        ),
        definition(
            "countString",
            NAT,
            match_list(
                var("values"),
                n(0),
                "head",
                "tail",
                _add(if_(_eqs(var("value"), h), n(1), n(0)), call("countString", var("value"), t)),
            ),
            parameters=[("value", STR), ("values", LS)],
            recursive="values",
        ),
        definition(
            "sameCounts",
            BOOL,
            match_list(
                var("probe"),
                b(True),
                "head",
                "tail",
                _and(
                    beq(call("countString", h, var("xs")), call("countString", h, var("ys"))),
                    call("sameCounts", t, var("xs"), var("ys")),
                ),
            ),
            parameters=[("probe", LS), ("xs", LS), ("ys", LS)],
            recursive="probe",
        ),
        definition(
            "isPermutation",
            BOOL,
            _and(
                beq(_len(var("xs")), _len(var("ys"))),
                _and(call("sameCounts", var("xs"), var("xs"), var("ys")), call("sameCounts", var("ys"), var("xs"), var("ys"))),
            ),
            parameters=[("xs", LS), ("ys", LS)],
        ),
        definition(
            "byWeight",
            BOOL,
            match_list(
                var("ordered"),
                b(True),
                "head",
                "tail",
                match_list(
                    t,
                    b(True),
                    "later",
                    "more",
                    _and(
                        ble(call("weightOf", var("later"), fam, table), call("weightOf", h, fam, table)),
                        call("byWeight", table, fam, t),
                    ),
                ),
            ),
            parameters=[("table", list_t(WEIGHT_T)), ("family", STR), ("ordered", LS)],
            recursive="ordered",
        ),
        definition(
            "scheduleSound",
            BOOL,
            _and(
                call("isPermutation", call("schedule", table, fam, var("applicable")), var("applicable")),
                call("byWeight", table, fam, call("schedule", table, fam, var("applicable"))),
            ),
            parameters=[("table", list_t(WEIGHT_T)), ("family", STR), ("applicable", LS)],
        ),
        definition(
            "soundForSubsets",
            BOOL,
            match_list(
                var("subsets"),
                b(True),
                "head",
                "tail",
                _and(call("scheduleSound", table, fam, h), call("soundForSubsets", table, fam, t)),
            ),
            parameters=[("table", list_t(WEIGHT_T)), ("family", STR), ("subsets", list_t(LS))],
            recursive="subsets",
        ),
        definition(
            "soundForFamilies",
            BOOL,
            match_list(
                var("families"),
                b(True),
                "head",
                "tail",
                _and(call("soundForSubsets", table, h, var("subsets")), call("soundForFamilies", table, t, var("subsets"))),
            ),
            parameters=[("table", list_t(WEIGHT_T)), ("families", LS), ("subsets", list_t(LS))],
            recursive="families",
        ),
    ]


def subsets(ids):
    out = []
    for mask in range(1 << len(ids)):
        out.append([x for i, x in enumerate(ids) if (mask >> i) & 1])
    return out


def fixture_declarations(committed):
    ids = [p["id"] for p in PORTFOLIO]
    start = initial_table()
    learned = Mirror.learn_all(start, FIXTURE_OUTCOMES)
    decls = [
        definition("initialWeights", list_t(WEIGHT_T), lst([_weight(*r) for r in start], WEIGHT_T), executable=True),
        definition(
            "fixtureOutcomes",
            list_t(OUTCOME_T),
            lst([_outcome(*o) for o in FIXTURE_OUTCOMES], OUTCOME_T),
            executable=True,
        ),
        definition("fixtureLearned", list_t(WEIGHT_T), lst([_weight(*r) for r in learned], WEIGHT_T), executable=True),
        definition("committedWeights", list_t(WEIGHT_T), lst([_weight(*r) for r in committed], WEIGHT_T), executable=True),
        definition("strategyIds", LS, strings(ids)),
        definition("familyIds", LS, strings(FAMILIES)),
        definition("portfolioSubsets", list_t(LS), lst([strings(x) for x in subsets(ids)], LS)),
        definition(
            "sameWeights",
            BOOL,
            match_list(
                var("xs"),
                beq(_len(var("ys")), n(0)),
                "head",
                "tail",
                match_list(
                    var("ys"),
                    b(False),
                    "y",
                    "rest",
                    _and(
                        _and(
                            _eqs(proj(var("head"), "strategy"), proj(var("y"), "strategy")),
                            _eqs(proj(var("head"), "family"), proj(var("y"), "family")),
                        ),
                        _and(
                            beq(proj(var("head"), "value"), proj(var("y"), "value")),
                            call("sameWeights", var("tail"), var("rest")),
                        ),
                    ),
                ),
            ),
            parameters=[("xs", list_t(WEIGHT_T)), ("ys", list_t(WEIGHT_T))],
            recursive="xs",
        ),
        definition(
            "sameStrings",
            BOOL,
            match_list(
                var("xs"),
                beq(_len(var("ys")), n(0)),
                "head",
                "tail",
                match_list(
                    var("ys"),
                    b(False),
                    "y",
                    "rest",
                    _and(_eqs(var("head"), var("y")), call("sameStrings", var("tail"), var("rest"))),
                ),
            ),
            parameters=[("xs", LS), ("ys", LS)],
            recursive="xs",
        ),
        holds("learnStaysInBounds", call("learnBoundedUpTo", n(W_MAX))),
        holds("initialWeightsBounded", call("weightsBounded", call("initialWeights"))),
        holds("committedWeightsBounded", call("weightsBounded", call("committedWeights"))),
        holds(
            "learnAllFixture",
            call("sameWeights", call("learnAll", call("initialWeights"), call("fixtureOutcomes")), call("fixtureLearned")),
        ),
        holds("learnAllFixtureBounded", call("weightsBounded", call("learnAll", call("initialWeights"), call("fixtureOutcomes")))),
        holds(
            "everyScheduleIsSound",
            call("soundForFamilies", call("committedWeights"), call("familyIds"), call("portfolioSubsets")),
        ),
    ]
    for i, (fam, apps) in enumerate(FIXTURE_SCHEDULES):
        expected = Mirror.schedule(learned, fam, apps)
        decls.append(
            holds(
                f"scheduleFixture{i}",
                call("sameStrings", call("schedule", call("fixtureLearned"), s(fam), strings(apps)), strings(expected)),
            )
        )
    return decls


def workload_declarations():
    wl = WORKLOAD
    h, t = var("head"), var("tail")
    stage_budget_sum = definition(
        "budgetSum",
        NAT,
        match_list(var("xs"), n(0), "head", "tail", _add(proj(h, "budget"), call("budgetSum", t))),
        parameters=[("xs", list_t(STAGE_T))],
        recursive="xs",
    )
    gate_share = definition(
        "gateShare",
        NAT,
        match_list(
            var("xs"),
            n(0),
            "head",
            "tail",
            _add(if_(proj(h, "gate"), proj(h, "budget"), n(0)), call("gateShare", t)),
        ),
        parameters=[("xs", list_t(STAGE_T))],
        recursive="xs",
    )
    distinct = definition(
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
    )
    nonempty = definition(
        "allNonEmpty",
        BOOL,
        match_list(var("values"), b(True), "head", "tail", _and(_not(_eqs(h, s(""))), call("allNonEmpty", t))),
        parameters=[("values", LS)],
        recursive="values",
    )
    return [
        structure("Stage", [("id", STR), ("budget", NAT), ("gate", BOOL)]),
        structure("Strategy", [("id", STR), ("template", STR), ("digest", STR)]),
        definition("hearingName", STR, s(wl["hearing"])),
        definition("courtroomName", STR, s(wl["courtroom"])),
        definition("timeoutMinutes", NAT, n(wl["timeoutMinutes"])),
        definition("setupMinutes", NAT, n(wl["setupMinutes"])),
        definition("tickBudget", NAT, n(wl["tickBudget"])),
        definition("gateMinimum", NAT, n(wl["gateMinimum"])),
        definition(
            "stages",
            list_t(STAGE_T),
            lst([record("Stage", id=s(a), budget=n(c), gate=b(g)) for a, c, g in wl["stages"]], STAGE_T),
        ),
        definition(
            "portfolio",
            list_t(STRATEGY_T),
            lst(
                [
                    record("Strategy", id=s(p["id"]), template=s(p["template"]), digest=s(template_digest(p["id"])))
                    for p in PORTFOLIO
                ],
                STRATEGY_T,
            ),
        ),
        field_of_each("strategyIdsOf", STRATEGY_T, "id"),
        field_of_each("digestsOf", STRATEGY_T, "digest"),
        field_of_each("stageIdsOf", STAGE_T, "id"),
        stage_budget_sum,
        gate_share,
        distinct,
        nonempty,
        holds("stageBudgetsFillTheTick", beq(call("budgetSum", call("stages")), call("tickBudget"))),
        holds(
            "stageBudgetsFitTheTimeout",
            ble(_add(call("setupMinutes"), call("budgetSum", call("stages"))), call("timeoutMinutes")),
        ),
        holds("gateKeepsItsShare", ble(call("gateMinimum"), call("gateShare", call("stages")))),
        holds("portfolioIdsDistinct", call("distinctStrings", call("strategyIdsOf", call("portfolio")))),
        holds(
            "templatesPinnedByDigest",
            _and(call("distinctStrings", call("digestsOf", call("portfolio"))), call("allNonEmpty", call("digestsOf", call("portfolio")))),
        ),
        holds("stageIdsDistinct", call("distinctStrings", call("stageIdsOf", call("stages")))),
    ]


def declarations(committed=None):
    committed = load_committed_table() if committed is None else committed
    return (
        [member_string(), all_members()]
        + workload_declarations()
        + learning_declarations()
        + fixture_declarations(committed)
    )


def render(committed=None):
    from . import lexmod

    return lexmod.module(NAME, declarations(committed))


def sync():
    committed = load_committed_table()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    MODULE.parent.mkdir(parents=True, exist_ok=True)
    toml_text = render_ledger_toml(committed)
    mod_text = render(committed)
    changed = False
    if not LEDGER.exists() or LEDGER.read_text() != toml_text:
        LEDGER.write_text(toml_text)
        changed = True
    if not MODULE.exists() or MODULE.read_text() != mod_text:
        MODULE.write_text(mod_text)
        changed = True
    return {
        "module": "src/Engine.lex.tex",
        "strategies": len(PORTFOLIO),
        "families": len(FAMILIES),
        "weights": len(committed),
        "changed": changed,
    }


def check():
    committed = load_committed_table()
    if not LEDGER.exists() or LEDGER.read_text() != render_ledger_toml(committed):
        return {"ok": False, "reason": "model/engine.toml drifted; run `bin/prism-legal api sync`"}
    if not MODULE.exists() or MODULE.read_text() != render(committed):
        return {"ok": False, "reason": "src/Engine.lex.tex drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}
