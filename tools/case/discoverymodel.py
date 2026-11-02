"""Induction & Evidentiary Relation Discovery as a compiled LexLean semantic module
(`src/Discovery.lex.tex`).

Over the 64-checkpoint evidentiary indicator windows of `src/Sequences.lex.tex`,
`src/Discovery.lex.tex` (`PrismLegal.Discovery`) declares:
- `RelationSearch`: Gaussian elimination over F2 (`findRelationsOn`) with precondition
  `IsWindow` (`isWindowCheck`, `is_window_check_sound`), postcondition `AllRelationsHold`
  (`allRelationsHoldCheck`, `all_relations_hold_check_sound`), structural induction
  theorem `zero_word_iff`, realization `RelationEngine`, model `RelationSearchModel`,
  and production root `findRelations` (`checked_apply` checking both precondition
  and postcondition at run time).
- `RecurrenceSearch`: Berlekamp-Massey over F2 (`findRecurrenceOn`) with precondition
  `IsSequenceWindow` (`isSequenceWindowCheck`, `is_sequence_window_check_sound`),
  postcondition `SatisfiesRecurrence` (`satisfiesRecurrenceCheck`,
  `satisfies_recurrence_check_sound`), realization `RecurrenceEngine`, model
  `RecurrenceSearchModel`, and production root `findRecurrence` (`checked_apply`).
- `buildColumns`: Extended basis column constructor (production root for `rust-std`).
- Kernel-decided theorems proving that on the 64-checkpoint trial record:
  - `corroborated-finding = equal-overnights XOR routine-continuity` (`CLM-01`)
  - `unilateral-act = one XOR joint-governance` (`CLM-05`)
  - `statutory-benefit = one` and `duplicate-expense = 0` (`CLM-11`)
  - `disclosure-reopening = reserve-omission` (`CLM-13`)
  - `order-compliant = one XOR (equal-overnights AND routine-continuity)` (`CLM-18`)
  - Berlekamp-Massey recovers the period-2 alternating schedule `[1, 0, 1]` for
    `equal-overnights`, the period-4 week-on/week-off block schedule for `week-parity`,
    and the period-3 schedule for `joint-governance`."""

from . import ROOT, sequencemodel
from .semantic import (
    BOOL,
    NAT,
    STR,
    b,
    beq,
    ble,
    blt,
    call,
    definition,
    holds,
    if_,
    list_t,
    lst,
    match_list,
    n,
    proj,
    record,
    s,
    strings,
    structure,
    var,
)

MODULE = ROOT / "src" / "Discovery.lex.tex"
NAME = "Discovery"
LEAN_MODULE = "PrismLegal.Discovery"
CHUNK_BITS = 32
CHUNK_BOUND = 1 << CHUNK_BITS
MAX_RECURRENCE_WINDOW = 65536
EFFECTS = {"effects": ["allocation", "overflow", "recursion"], "targets": ["rust-std"]}
PRODUCTION_ROOTS = {"buildColumns": EFFECTS, "findRelations": EFFECTS, "findRecurrence": EFFECTS}

TRANSFORMS = [
    {"code": 0, "id": "base", "statement": "s(t)"},
    {"code": 1, "id": "shift", "statement": "s(t+1)"},
    {"code": 2, "id": "even", "statement": "s(2t)"},
    {"code": 3, "id": "odd", "statement": "s(2t+1)"},
    {"code": 4, "id": "and", "statement": "s(t) AND u(t)"},
]
CODE = {t["id"]: t["code"] for t in TRANSFORMS}

FIXTURE_WIDTH = 32
FIXTURE_COLUMNS = [
    "one",
    "equal-overnights",
    "routine-continuity",
    "corroborated-finding",
    "joint-governance",
    "unilateral-act",
    "statutory-benefit",
    "reserve-omission",
    "disclosure-reopening",
]

RECURRENCE_FIXTURES = [
    {"name": "equalOvernights", "column": "equal-overnights", "expected": [1, 0, 1]},
    {"name": "weekParity", "column": "week-parity", "expected": [1, 1, 1, 1]},
    {"name": "jointGovernance", "column": "joint-governance", "expected": [1, 1, 1]},
]

REGISTER_CLAIM_RELATIONS = [
    ("CLM-01", ["equal-overnights", "routine-continuity", "corroborated-finding"]),
    ("CLM-05", ["one", "joint-governance", "unilateral-act"]),
    ("CLM-11", ["one", "statutory-benefit"]),
    ("CLM-13", ["reserve-omission", "disclosure-reopening"]),
    ("CLM-18", ["one", "order-compliant", "and:equal-overnights:routine-continuity"]),
]


def parse_column(cid):
    parts = cid.split(":")
    if len(parts) == 1:
        return "base", parts
    if parts[0] in ("shift", "even", "odd") and len(parts) == 2:
        return parts[0], parts[1:]
    if parts[0] == "and" and len(parts) == 3:
        return "and", parts[1:]
    raise ValueError(f"not a column id: {cid}")


def column_spec(cid, index):
    transform, ids = parse_column(cid)
    left = index[ids[0]]
    right = index[ids[1]] if transform == "and" else 0
    return CODE[transform], left, right


class Mirror:
    @staticmethod
    def xor_word(w, u):
        if not w:
            return list(u)
        if not u:
            return list(w)
        return [x ^ y for x, y in zip(w, u)] + (w[len(u) :] if len(w) > len(u) else u[len(w) :])

    @staticmethod
    def word_weight(w):
        return sum(w)

    @staticmethod
    def word_bit(w, i):
        k = i // CHUNK_BITS
        return k < len(w) and ((w[k] >> (i % CHUNK_BITS)) & 1) == 1

    @staticmethod
    def lowest_bit(w):
        base = 0
        for c in w:
            if c == 0:
                base += CHUNK_BITS
                continue
            k = 0
            while k < CHUNK_BITS and c % 2 == 0:
                c //= 2
                k += 1
            return base + k
        return base

    @staticmethod
    def word_bits(w):
        return [(c >> k) & 1 for c in w for k in range(CHUNK_BITS)]

    @staticmethod
    def pack_word(bits):
        return sequencemodel.chunks(bits)

    @staticmethod
    def column_bits(width, bases, spec):
        code, left, right = spec
        base = Mirror.word_bits(bases[left]) if left < len(bases) else []
        if code == 0:
            return base[:width]
        if code == 1:
            return base[1:][:width]
        if code == 2:
            return base[0::2][:width]
        if code == 3:
            return base[1::2][:width]
        other = Mirror.word_bits(bases[right]) if right < len(bases) else []
        return [x & y for x, y in zip(base[:width], other[:width])]

    @staticmethod
    def build_columns(width, bases, specs):
        return [Mirror.pack_word(Mirror.column_bits(width, bases, sp)) for sp in specs]

    @staticmethod
    def xor_mask(a, c):
        if not a:
            return list(c)
        if not c:
            return list(a)
        return [x ^ y for x, y in zip(a, c)] + (a[len(c) :] if len(a) > len(c) else c[len(a) :])

    @staticmethod
    def find_relations(window):
        _, ws = window
        m = len(ws)
        pivots, relations = [], []
        for index, w in enumerate(ws):
            word, mask = list(w), [1 if i == index else 0 for i in range(m)]
            for position, pword, pmask in pivots:
                if Mirror.word_bit(word, position):
                    word, mask = Mirror.xor_word(word, pword), Mirror.xor_mask(mask, pmask)
            if Mirror.word_weight(word) == 0:
                relations.append(mask)
            else:
                pivots.append((Mirror.lowest_bit(word), word, mask))
        return relations

    @staticmethod
    def selected_xor(ws, mask):
        out = []
        for w, bit in zip(ws, mask):
            if bit:
                out = Mirror.xor_word(w, out)
        return out

    @staticmethod
    def window_misfits(window):
        width, ws = window
        return sum((0 if len(w) * CHUNK_BITS == width else 1) + sum(1 for c in w if c >= CHUNK_BOUND) for w in ws)

    @staticmethod
    def relation_residue(ws, rs):
        return sum(
            (0 if Mirror.word_weight(Mirror.selected_xor(ws, r)) == 0 else 1)
            + (1 if sum(r) == 0 else 0)
            + (0 if len(r) == len(ws) else 1)
            for r in rs
        )

    @staticmethod
    def find_recurrence(sq):
        conn, prev, l, m, hist = [1], [1], 0, 1, []
        for pos, x in enumerate(sq):
            h2 = [x] + hist
            d = 0
            for ci, hi in zip(conn, h2):
                d ^= ci & hi
            if d:
                nxt = Mirror.xor_mask(conn, [0] * m + prev)
                if l + l <= pos:
                    conn, prev, l, m = nxt, conn, pos + 1 - l, 1
                else:
                    conn, m = nxt, m + 1
            else:
                m += 1
            hist = h2
        return (conn + [0] * (l + 1))[: l + 1]

    @staticmethod
    def recurrence_defects(sq, c):
        lead = 0 if c and c[0] == 1 else 1
        rc = list(reversed(c))
        bad = 0
        for k in range(len(sq)):
            u = sq[k:]
            if len(u) < len(rc):
                continue
            d = 0
            for x, y in zip(rc, u):
                d ^= x & y
            bad += d
        return lead + bad


LN = list_t(NAT)
LLN = list_t(LN)
LB = list_t(BOOL)
LLB = list_t(LB)


def _prod(a, c):
    return {"kind": "product", "left": a, "right": c}


SPEC_T = _prod(NAT, _prod(NAT, NAT))
LSPEC = list_t(SPEC_T)
WINDOW_T = _prod(NAT, LLN)
PIVOT_T = {"kind": "named", "member": {"name": "Pivot"}, "arguments": []}
RED_T = _prod(LN, LB)
BM_T = _prod(LB, NAT)
CV = {"kind": "contract_violation"}


def _result(ok):
    return {"kind": "result", "ok": ok, "error": CV}


def _p(op, args, result):
    return {"kind": "primitive", "operation": op, "result": result, "arguments": list(args)}


def _rem(a, c):
    return _p("remainder", [a, c, n(0)], NAT)


def _quo(a, c):
    return _p("quotient", [a, c, n(0)], NAT)


def _mul(a, c):
    return _p("multiply", [a, c], NAT)


def _sub(a, c):
    return _p("subtract", [a, c], NAT)


def _len(x):
    return _p("length", [x], NAT)


def _append(a, c, t):
    return _p("append", [a, c], t)


def _add(a, c):
    return {"kind": "add", "left": a, "right": c}


def _and(a, c):
    return {"kind": "and", "left": a, "right": c}


def _not(a):
    return {"kind": "not", "value": a}


def _cons(h, t):
    return {"kind": "cons", "head": h, "tail": t}


def _nil(t):
    return {"kind": "nil", "element": t}


def _let(name, typ, value, body):
    return {"kind": "let", "binder": {"name": name, "type": typ}, "value": value, "body": body}


def _pair(a, c):
    return {"kind": "pair", "left": a, "right": c}


def _first(x):
    return {"kind": "first", "value": x}


def _second(x):
    return {"kind": "second", "value": x}


def _eq(a, c):
    return {"kind": "eq", "left": a, "right": c}


def _lt(a, c):
    return {"kind": "lt", "left": a, "right": c}


def _le(a, c):
    return {"kind": "le", "left": a, "right": c}


def _pand(a, c):
    return {"kind": "prop_and", "left": a, "right": c}


def _iff(a, c):
    return {"kind": "iff", "left": a, "right": c}


def _implies(p, c):
    return {"kind": "implies", "premise": p, "conclusion": c}


def _match_nat(scrutinee, zero_body, binder, succ_body):
    return {
        "kind": "match",
        "scrutinee": scrutinee,
        "branches": [
            {"constructor": {"name": "Nat.zero"}, "binders": [], "body": zero_body},
            {"constructor": {"name": "Nat.succ"}, "binders": [binder], "body": succ_body},
        ],
    }


def _bools(bits):
    return lst([b(x) for x in bits], BOOL)


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


def _prop(name, body, parameters, recursive=None):
    return definition(name, {"kind": "prop"}, body, parameters=parameters, recursive=recursive)


def _theorem(name, parameters, statement, proof, axioms=("propext",)):
    return {
        "kind": "theorem",
        "name": name,
        "parameters": [{"name": p, "type": t} for p, t in parameters],
        "axioms": list(axioms),
        "statement": statement,
        "proof": proof,
    }


def _defs(*names):
    return [{"name": x} for x in sorted(names)]


def _linear(*names):
    return {"kind": "linear_arithmetic", "definitions": _defs(*names)}


def _simplify(*names):
    return {"kind": "simplify", "definitions": _defs(*names)}


def _induction(scrutinee, nil_proof, cons_binders, cons_proof):
    return {
        "kind": "induction",
        "scrutinee": scrutinee,
        "branches": [
            {"constructor": "nil", "binders": [], "proof": nil_proof},
            {"constructor": "cons", "binders": list(cons_binders), "proof": cons_proof},
        ],
    }


def _sound(name, check, pred, params):
    args = [var(p) for p, _ in params]
    return _theorem(name, params, _implies(_eq(call(check, *args), b(True)), call(pred, *args)), _linear(check, pred))


def word_declarations():
    w, u, x, xs, y, ys = var("w"), var("u"), var("x"), var("xs"), var("y"), var("ys")
    c, i, k, f, g = var("c"), var("i"), var("k"), var("f"), var("g")
    bs = var("bs")
    return [
        _ex(
            "xorBits",
            NAT,
            _match_nat(
                f,
                n(0),
                "g",
                _let(
                    "v",
                    NAT,
                    call("xorBits", g, _quo(var("a"), n(2)), _quo(c, n(2))),
                    _add(_rem(_add(var("a"), c), n(2)), _add(var("v"), var("v"))),
                ),
            ),
            parameters=[("f", NAT), ("a", NAT), ("c", NAT)],
            recursive="f",
        ),
        _ex(
            "xorWord",
            LN,
            match_list(
                w,
                u,
                "x",
                "xs",
                match_list(u, _cons(x, xs), "y", "ys", _cons(call("xorBits", n(CHUNK_BITS), x, y), call("xorWord", xs, ys))),
            ),
            parameters=[("w", LN), ("u", LN)],
            recursive="w",
        ),
        _ex(
            "zeroWord",
            BOOL,
            match_list(w, b(True), "x", "xs", _and(beq(x, n(0)), call("zeroWord", xs))),
            parameters=[("w", LN)],
            recursive="w",
        ),
        _ex(
            "chunkBit",
            BOOL,
            _match_nat(k, beq(_rem(c, n(2)), n(1)), "j", call("chunkBit", var("j"), _quo(c, n(2)))),
            parameters=[("k", NAT), ("c", NAT)],
            recursive="k",
        ),
        _ex(
            "wordBit",
            BOOL,
            match_list(
                w,
                b(False),
                "x",
                "xs",
                if_(blt(i, n(CHUNK_BITS)), call("chunkBit", i, x), call("wordBit", xs, _sub(i, n(CHUNK_BITS)))),
            ),
            parameters=[("w", LN), ("i", NAT)],
            recursive="w",
        ),
        _ex(
            "lowestInChunk",
            NAT,
            _match_nat(
                f,
                n(0),
                "g",
                if_(beq(_rem(c, n(2)), n(1)), n(0), _add(n(1), call("lowestInChunk", g, _quo(c, n(2))))),
            ),
            parameters=[("f", NAT), ("c", NAT)],
            recursive="f",
        ),
        _ex(
            "lowestBit",
            NAT,
            match_list(
                w,
                n(0),
                "x",
                "xs",
                if_(beq(x, n(0)), _add(n(CHUNK_BITS), call("lowestBit", xs)), call("lowestInChunk", n(CHUNK_BITS), x)),
            ),
            parameters=[("w", LN)],
            recursive="w",
        ),
        _ex(
            "unpackChunk",
            LB,
            _match_nat(f, _nil(BOOL), "g", _cons(beq(_rem(c, n(2)), n(1)), call("unpackChunk", g, _quo(c, n(2))))),
            parameters=[("f", NAT), ("c", NAT)],
            recursive="f",
        ),
        _ex(
            "wordBits",
            LB,
            match_list(w, _nil(BOOL), "x", "xs", _append(call("unpackChunk", n(CHUNK_BITS), x), call("wordBits", xs), LB)),
            parameters=[("w", LN)],
            recursive="w",
        ),
        _ex(
            "packFrom",
            LN,
            match_list(
                bs,
                if_(beq(var("pos"), n(0)), _nil(NAT), _cons(var("acc"), _nil(NAT))),
                "x",
                "xs",
                _let(
                    "v",
                    NAT,
                    _add(var("acc"), if_(x, var("place"), n(0))),
                    if_(
                        beq(_add(var("pos"), n(1)), n(CHUNK_BITS)),
                        _cons(var("v"), call("packFrom", xs, n(0), n(0), n(1))),
                        call("packFrom", xs, _add(var("pos"), n(1)), var("v"), _add(var("place"), var("place"))),
                    ),
                ),
            ),
            parameters=[("bs", LB), ("pos", NAT), ("acc", NAT), ("place", NAT)],
            recursive="bs",
        ),
        _ex("packWord", LN, call("packFrom", bs, n(0), n(0), n(1)), parameters=[("bs", LB)]),
        _ex(
            "takeBits",
            LB,
            match_list(bs, _nil(BOOL), "x", "xs", if_(beq(k, n(0)), _nil(BOOL), _cons(x, call("takeBits", xs, _sub(k, n(1)))))),
            parameters=[("bs", LB), ("k", NAT)],
            recursive="bs",
        ),
        _ex("dropFirst", LB, match_list(bs, _nil(BOOL), "x", "xs", xs), parameters=[("bs", LB)]),
        _ex(
            "everyOther",
            LB,
            match_list(
                bs,
                _nil(BOOL),
                "x",
                "xs",
                if_(var("keep"), _cons(x, call("everyOther", xs, b(False))), call("everyOther", xs, b(True))),
            ),
            parameters=[("bs", LB), ("keep", BOOL)],
            recursive="bs",
        ),
        _ex(
            "andBits",
            LB,
            match_list(
                bs,
                _nil(BOOL),
                "x",
                "xs",
                match_list(var("cs"), _nil(BOOL), "y", "ys", _cons(_and(x, y), call("andBits", xs, ys))),
            ),
            parameters=[("bs", LB), ("cs", LB)],
            recursive="bs",
        ),
        _ex(
            "nthWord",
            LN,
            match_list(var("ws"), _nil(NAT), "x", "xs", if_(beq(i, n(0)), x, call("nthWord", xs, _sub(i, n(1))))),
            parameters=[("ws", LLN), ("i", NAT)],
            recursive="ws",
        ),
    ]


def column_declarations():
    spec, bases, width = var("spec"), var("bases"), var("width")
    code = _first(spec)
    base_bits = call("wordBits", call("nthWord", bases, _first(_second(spec))))
    take = lambda x: call("takeBits", x, width)
    return [
        _ex(
            "columnBits",
            LB,
            _let(
                "baseBits",
                LB,
                base_bits,
                if_(
                    beq(code, n(0)),
                    take(var("baseBits")),
                    if_(
                        beq(code, n(1)),
                        take(call("dropFirst", var("baseBits"))),
                        if_(
                            beq(code, n(2)),
                            take(call("everyOther", var("baseBits"), b(True))),
                            if_(
                                beq(code, n(3)),
                                take(call("everyOther", var("baseBits"), b(False))),
                                call(
                                    "andBits",
                                    take(var("baseBits")),
                                    take(call("wordBits", call("nthWord", bases, _second(_second(spec))))),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            parameters=[("width", NAT), ("bases", LLN), ("spec", SPEC_T)],
        ),
        _ex(
            "buildColumns",
            LLN,
            match_list(
                var("specs"),
                _nil(LN),
                "x",
                "xs",
                _cons(call("packWord", call("columnBits", width, bases, var("x"))), call("buildColumns", width, bases, var("xs"))),
            ),
            parameters=[("width", NAT), ("bases", LLN), ("specs", LSPEC)],
            recursive="specs",
        ),
    ]


def relation_declarations():
    x, xs, y, ys, ps, w = var("x"), var("xs"), var("y"), var("ys"), var("ps"), var("w")
    ws, mk, r = var("ws"), var("mk"), var("r")
    window = var("window")
    return [
        _ex(
            "xorMask",
            LB,
            match_list(
                var("ms"),
                var("ns"),
                "x",
                "xs",
                match_list(var("ns"), _cons(x, xs), "y", "ys", _cons(if_(x, _not(y), y), call("xorMask", xs, ys))),
            ),
            parameters=[("ms", LB), ("ns", LB)],
            recursive="ms",
        ),
        _ex(
            "maskAt",
            LB,
            _match_nat(
                var("m"),
                _nil(BOOL),
                "k",
                _cons(beq(var("pos"), var("i")), call("maskAt", var("k"), var("i"), _add(var("pos"), n(1)))),
            ),
            parameters=[("m", NAT), ("i", NAT), ("pos", NAT)],
            recursive="m",
        ),
        structure("Pivot", [("position", NAT), ("word", LN), ("mask", LB)]),
        _ex(
            "reduce",
            RED_T,
            match_list(
                ps,
                _pair(w, mk),
                "x",
                "xs",
                if_(
                    call("wordBit", w, proj(x, "position")),
                    call("reduce", xs, call("xorWord", w, proj(x, "word")), call("xorMask", mk, proj(x, "mask"))),
                    call("reduce", xs, w, mk),
                ),
            ),
            parameters=[("ps", list_t(PIVOT_T)), ("w", LN), ("mk", LB)],
            recursive="ps",
        ),
        _ex(
            "eliminate",
            LLB,
            match_list(
                ws,
                _nil(LB),
                "x",
                "xs",
                _let(
                    "r",
                    RED_T,
                    call("reduce", ps, x, call("maskAt", var("m"), var("index"), n(0))),
                    if_(
                        call("zeroWord", _first(r)),
                        _cons(_second(r), call("eliminate", xs, _add(var("index"), n(1)), var("m"), ps)),
                        call(
                            "eliminate",
                            xs,
                            _add(var("index"), n(1)),
                            var("m"),
                            _append(
                                ps,
                                _cons(
                                    record("Pivot", position=call("lowestBit", _first(r)), word=_first(r), mask=_second(r)),
                                    _nil(PIVOT_T),
                                ),
                                list_t(PIVOT_T),
                            ),
                        ),
                    ),
                ),
            ),
            parameters=[("ws", LLN), ("index", NAT), ("m", NAT), ("ps", list_t(PIVOT_T))],
            recursive="ws",
        ),
        _ex(
            "findRelationsOn",
            LLB,
            call("eliminate", _second(window), n(0), _len(_second(window)), _nil(PIVOT_T)),
            parameters=[("window", WINDOW_T)],
        ),
        _ex(
            "selectedXor",
            LN,
            match_list(
                ws,
                _nil(NAT),
                "x",
                "xs",
                match_list(mk, _nil(NAT), "y", "ys", if_(y, call("xorWord", x, call("selectedXor", xs, ys)), call("selectedXor", xs, ys))),
            ),
            parameters=[("ws", LLN), ("mk", LB)],
            recursive="ws",
        ),
        _ex(
            "maskWeight",
            NAT,
            match_list(mk, n(0), "y", "ys", _add(if_(y, n(1), n(0)), call("maskWeight", ys))),
            parameters=[("mk", LB)],
            recursive="mk",
        ),
        _ex(
            "chunksAbove",
            NAT,
            match_list(w, n(0), "x", "xs", _add(if_(blt(x, n(CHUNK_BOUND)), n(0), n(1)), call("chunksAbove", xs))),
            parameters=[("w", LN)],
            recursive="w",
        ),
        _ex(
            "windowMisfits",
            NAT,
            match_list(
                ws,
                n(0),
                "x",
                "xs",
                _add(
                    _add(if_(beq(_mul(_len(x), n(CHUNK_BITS)), var("width")), n(0), n(1)), call("chunksAbove", x)),
                    call("windowMisfits", var("width"), xs),
                ),
            ),
            parameters=[("width", NAT), ("ws", LLN)],
            recursive="ws",
        ),
        _prop("IsWindow", _eq(call("windowMisfits", _first(window), _second(window)), n(0)), [("window", WINDOW_T)]),
        _ex("isWindowCheck", BOOL, beq(call("windowMisfits", _first(window), _second(window)), n(0)), parameters=[("window", WINDOW_T)]),
        _sound("is_window_check_sound", "isWindowCheck", "IsWindow", [("window", WINDOW_T)]),
        _ex(
            "relationResidue",
            NAT,
            match_list(
                var("rs"),
                n(0),
                "r",
                "rest",
                _add(
                    _add(
                        _add(
                            if_(call("zeroWord", call("selectedXor", ws, r)), n(0), n(1)),
                            if_(beq(call("maskWeight", r), n(0)), n(1), n(0)),
                        ),
                        if_(beq(_len(r), _len(ws)), n(0), n(1)),
                    ),
                    call("relationResidue", ws, var("rest")),
                ),
            ),
            parameters=[("ws", LLN), ("rs", LLB)],
            recursive="rs",
        ),
        _prop("AllRelationsHold", _eq(call("relationResidue", _second(window), var("found")), n(0)), [("window", WINDOW_T), ("found", LLB)]),
        _ex(
            "allRelationsHoldCheck",
            BOOL,
            beq(call("relationResidue", _second(window), var("found")), n(0)),
            parameters=[("window", WINDOW_T), ("found", LLB)],
        ),
        _sound("all_relations_hold_check_sound", "allRelationsHoldCheck", "AllRelationsHold", [("window", WINDOW_T), ("found", LLB)]),
        _prop(
            "ZeroWords",
            match_list(w, _eq(n(0), n(0)), "x", "xs", _pand(_eq(x, n(0)), call("ZeroWords", xs))),
            [("w", LN)],
            recursive="w",
        ),
        _theorem(
            "zero_word_iff",
            [("w", LN)],
            _iff(_eq(call("zeroWord", w), b(True)), call("ZeroWords", w)),
            _induction("w", _simplify("ZeroWords", "zeroWord"), ["x", "xs", "ih"], _simplify("Bool.and_eq_true", "Nat.beq_eq", "ZeroWords", "ih", "zeroWord")),
        ),
        {
            "kind": "contract",
            "name": "RelationSearch",
            "axioms": ["propext"],
            "input": {"name": "window", "type": WINDOW_T},
            "output": {"name": "found", "type": LLB},
            "precondition": {"name": "IsWindow"},
            "postcondition": {"name": "AllRelationsHold"},
            "validators": [
                {"predicate": "postcondition", "sound": {"name": "all_relations_hold_check_sound"}, "validator": {"name": "allRelationsHoldCheck"}},
                {"predicate": "precondition", "sound": {"name": "is_window_check_sound"}, "validator": {"name": "isWindowCheck"}},
            ],
        },
        {
            "kind": "realization",
            "name": "RelationEngine",
            "input": {"name": "window", "type": WINDOW_T},
            "output": LLB,
            "descriptor": {"kind": "deterministic", "body": call("findRelationsOn", window)},
            "executable": True,
        },
        {
            "kind": "model",
            "name": "RelationSearchModel",
            "contract": {"member": {"name": "RelationSearch"}},
            "realization": {"member": {"name": "RelationEngine"}},
        },
        _ex(
            "findRelations",
            _result(LLB),
            {
                "kind": "checked_apply",
                "model": {"name": "RelationSearchModel"},
                "type_arguments": [],
                "arguments": [window],
                "checks": ["postcondition", "precondition"],
            },
            parameters=[("window", WINDOW_T)],
        ),
    ]


def recurrence_declarations():
    x, xs, y, ys, sq, conn = var("x"), var("xs"), var("y"), var("ys"), var("sq"), var("conn")
    pos, l, m = var("pos"), var("l"), var("m")
    return [
        _ex(
            "dotBits",
            BOOL,
            match_list(
                var("as"),
                b(False),
                "x",
                "xs",
                match_list(var("cs"), b(False), "y", "ys", if_(_and(x, y), _not(call("dotBits", xs, ys)), call("dotBits", xs, ys))),
            ),
            parameters=[("as", LB), ("cs", LB)],
            recursive="as",
        ),
        _ex(
            "prependFalse",
            LB,
            _match_nat(m, var("bs"), "k", _cons(b(False), call("prependFalse", var("k"), var("bs")))),
            parameters=[("m", NAT), ("bs", LB)],
            recursive="m",
        ),
        _ex(
            "massey",
            BM_T,
            match_list(
                sq,
                _pair(conn, l),
                "x",
                "xs",
                _let(
                    "h2",
                    LB,
                    _cons(x, var("hist")),
                    if_(
                        call("dotBits", conn, var("h2")),
                        _let(
                            "updated",
                            LB,
                            call("xorMask", conn, call("prependFalse", m, var("prev"))),
                            if_(
                                ble(_add(l, l), pos),
                                call("massey", xs, _add(pos, n(1)), var("updated"), conn, _sub(_add(pos, n(1)), l), n(1), var("h2")),
                                call("massey", xs, _add(pos, n(1)), var("updated"), var("prev"), l, _add(m, n(1)), var("h2")),
                            ),
                        ),
                        call("massey", xs, _add(pos, n(1)), conn, var("prev"), l, _add(m, n(1)), var("h2")),
                    ),
                ),
            ),
            parameters=[("sq", LB), ("pos", NAT), ("conn", LB), ("prev", LB), ("l", NAT), ("m", NAT), ("hist", LB)],
            recursive="sq",
        ),
        _ex(
            "takePad",
            LB,
            _match_nat(
                var("k"),
                _nil(BOOL),
                "j",
                match_list(var("bs"), _cons(b(False), call("takePad", var("j"), _nil(BOOL))), "x", "xs", _cons(x, call("takePad", var("j"), xs))),
            ),
            parameters=[("k", NAT), ("bs", LB)],
            recursive="k",
        ),
        _ex(
            "findRecurrenceOn",
            LB,
            _let(
                "r",
                BM_T,
                call("massey", sq, n(0), _bools([1]), _bools([1]), n(0), n(1), _nil(BOOL)),
                call("takePad", _add(_second(var("r")), n(1)), _first(var("r"))),
            ),
            parameters=[("sq", LB)],
        ),
        _ex(
            "reverseOnto",
            LB,
            match_list(var("bs"), var("acc"), "x", "xs", call("reverseOnto", xs, _cons(x, var("acc")))),
            parameters=[("bs", LB), ("acc", LB)],
            recursive="bs",
        ),
        _ex(
            "slideDefects",
            NAT,
            match_list(
                sq,
                n(0),
                "x",
                "xs",
                _add(
                    if_(blt(_len(_cons(x, xs)), _len(var("rc"))), n(0), if_(call("dotBits", var("rc"), _cons(x, xs)), n(1), n(0))),
                    call("slideDefects", var("rc"), xs),
                ),
            ),
            parameters=[("rc", LB), ("sq", LB)],
            recursive="sq",
        ),
        _ex("leadDefect", NAT, match_list(conn, n(1), "x", "xs", if_(x, n(0), n(1))), parameters=[("conn", LB)]),
        _ex(
            "recurrenceDefects",
            NAT,
            _add(call("leadDefect", conn), call("slideDefects", call("reverseOnto", conn, _nil(BOOL)), sq)),
            parameters=[("sq", LB), ("conn", LB)],
        ),
        _prop("IsSequenceWindow", _pand(_lt(n(0), _len(sq)), _le(_len(sq), n(MAX_RECURRENCE_WINDOW))), [("sq", LB)]),
        _ex(
            "isSequenceWindowCheck",
            BOOL,
            _and(blt(n(0), _len(sq)), ble(_len(sq), n(MAX_RECURRENCE_WINDOW))),
            parameters=[("sq", LB)],
        ),
        _sound("is_sequence_window_check_sound", "isSequenceWindowCheck", "IsSequenceWindow", [("sq", LB)]),
        _prop("SatisfiesRecurrence", _eq(call("recurrenceDefects", sq, conn), n(0)), [("sq", LB), ("conn", LB)]),
        _ex(
            "satisfiesRecurrenceCheck",
            BOOL,
            beq(call("recurrenceDefects", sq, conn), n(0)),
            parameters=[("sq", LB), ("conn", LB)],
        ),
        _sound("satisfies_recurrence_check_sound", "satisfiesRecurrenceCheck", "SatisfiesRecurrence", [("sq", LB), ("conn", LB)]),
        {
            "kind": "contract",
            "name": "RecurrenceSearch",
            "axioms": ["propext"],
            "input": {"name": "sq", "type": LB},
            "output": {"name": "conn", "type": LB},
            "precondition": {"name": "IsSequenceWindow"},
            "postcondition": {"name": "SatisfiesRecurrence"},
            "validators": [
                {"predicate": "postcondition", "sound": {"name": "satisfies_recurrence_check_sound"}, "validator": {"name": "satisfiesRecurrenceCheck"}},
                {"predicate": "precondition", "sound": {"name": "is_sequence_window_check_sound"}, "validator": {"name": "isSequenceWindowCheck"}},
            ],
        },
        {
            "kind": "realization",
            "name": "RecurrenceEngine",
            "input": {"name": "sq", "type": LB},
            "output": LB,
            "descriptor": {"kind": "deterministic", "body": call("findRecurrenceOn", sq)},
            "executable": True,
        },
        {
            "kind": "model",
            "name": "RecurrenceSearchModel",
            "contract": {"member": {"name": "RecurrenceSearch"}},
            "realization": {"member": {"name": "RecurrenceEngine"}},
        },
        _ex(
            "findRecurrence",
            _result(LB),
            {
                "kind": "checked_apply",
                "model": {"name": "RecurrenceSearchModel"},
                "type_arguments": [],
                "arguments": [sq],
                "checks": ["postcondition", "precondition"],
            },
            parameters=[("sq", LB)],
        ),
    ]


def index_of(data):
    return {r["id"]: i for i, r in enumerate(data["sequence"])}


def bases_of(data):
    return [r["window"] for r in data["sequence"]]


def fixtures(data):
    index, bases = index_of(data), bases_of(data)
    specs = [column_spec(cid, index) for cid in FIXTURE_COLUMNS]
    window = (FIXTURE_WIDTH, Mirror.build_columns(FIXTURE_WIDTH, bases, specs))
    relations = Mirror.find_relations(window)
    recurrences = []
    for fx in RECURRENCE_FIXTURES:
        bits = Mirror.column_bits(FIXTURE_WIDTH, bases, column_spec(fx["column"], index))
        recurrences.append({**fx, "bits": bits, "found": Mirror.find_recurrence(bits)})
    return {"specs": specs, "window": window, "relations": relations, "recurrences": recurrences}


def fixture_declarations(data):
    fx = fixtures(data)
    index = index_of(data)
    spec_term = lambda sp: _pair(n(sp[0]), _pair(n(sp[1]), n(sp[2])))
    windows = call("windows", module="Sequences")
    sames = [
        _ex(
            "sameBits",
            BOOL,
            match_list(
                var("as"),
                beq(_len(var("cs")), n(0)),
                "x",
                "xs",
                match_list(var("cs"), b(False), "y", "ys", _and(if_(var("x"), var("y"), _not(var("y"))), call("sameBits", var("xs"), var("ys")))),
            ),
            parameters=[("as", LB), ("cs", LB)],
            recursive="as",
        ),
        _ex(
            "sameMasks",
            BOOL,
            match_list(
                var("as"),
                beq(_len(var("cs")), n(0)),
                "x",
                "xs",
                match_list(var("cs"), b(False), "y", "ys", _and(call("sameBits", var("x"), var("y")), call("sameMasks", var("xs"), var("ys")))),
            ),
            parameters=[("as", LLB), ("cs", LLB)],
            recursive="as",
        ),
    ]
    decls = sames + [
        definition("fixtureSpecs", LSPEC, lst([spec_term(sp) for sp in fx["specs"]], SPEC_T), executable=True),
        definition(
            "relationFixture",
            WINDOW_T,
            _pair(n(FIXTURE_WIDTH), call("buildColumns", n(FIXTURE_WIDTH), windows, call("fixtureSpecs"))),
            executable=True,
        ),
        definition("expectedRelations", LLB, lst([_bools(r) for r in fx["relations"]], LB), executable=True),
        holds("relationFixtureIsWindow", call("isWindowCheck", call("relationFixture"))),
        holds("relationFixtureFindsTheRegister", call("sameMasks", call("findRelationsOn", call("relationFixture")), call("expectedRelations"))),
        holds(
            "relationFixtureHasNoFalseRelation",
            call("allRelationsHoldCheck", call("relationFixture"), call("findRelationsOn", call("relationFixture"))),
        ),
    ]
    for rec in fx["recurrences"]:
        name = rec["name"]
        bits = call("columnBits", n(FIXTURE_WIDTH), windows, spec_term(column_spec(rec["column"], index)))
        decls += [
            definition(f"{name}Bits", LB, bits, executable=True),
            holds(f"{name}Recurrence", call("sameBits", call("findRecurrenceOn", call(f"{name}Bits")), _bools(rec["expected"]))),
            holds(f"{name}RecurrenceHolds", call("satisfiesRecurrenceCheck", call(f"{name}Bits"), call("findRecurrenceOn", call(f"{name}Bits")))),
        ]
    rel = REGISTER_CLAIM_RELATIONS
    decls += [
        _ex(
            "xorAllWords",
            LN,
            match_list(var("ws"), _nil(NAT), "x", "xs", call("xorWord", var("x"), call("xorAllWords", var("xs")))),
            parameters=[("ws", LLN)],
            recursive="ws",
        ),
        _ex(
            "relationVanishes",
            BOOL,
            call("zeroWord", call("xorAllWords", call("buildColumns", var("width"), windows, var("specs")))),
            parameters=[("width", NAT), ("specs", LSPEC)],
        ),
        _ex(
            "allVanish",
            BOOL,
            match_list(
                var("rels"),
                b(True),
                "x",
                "xs",
                _and(call("relationVanishes", var("width"), var("x")), call("allVanish", var("width"), var("xs"))),
            ),
            parameters=[("width", NAT), ("rels", list_t(LSPEC))],
            recursive="rels",
        ),
        definition("registerRelationClaims", list_t(STR), strings([cid for cid, _ in rel]), executable=True),
        definition(
            "registerRelations",
            list_t(LSPEC),
            lst([lst([spec_term(column_spec(c, index)) for c in cols], SPEC_T) for _, cols in rel], LSPEC),
            executable=True,
        ),
        holds(
            "registerRelationClaimsAreClaims",
            call(
                "allMembers",
                call("registerRelationClaims"),
                call("claimIds", call("claims", module="Register"), module="Register"),
                module="Register",
            ),
        ),
        holds("registerRelationsHold", call("allVanish", n(FIXTURE_WIDTH), call("registerRelations"))),
    ]
    return decls


def declarations(data=None):
    data = sequencemodel.load() if data is None else data
    return (
        word_declarations()
        + column_declarations()
        + relation_declarations()
        + recurrence_declarations()
        + fixture_declarations(data)
    )


def render(data=None):
    from . import lexmod

    data = sequencemodel.load() if data is None else data
    return lexmod.module(NAME, declarations(data), imports=["Register", "Sequences"])


def sync():
    sequencemodel.sync()
    data = sequencemodel.load()
    MODULE.parent.mkdir(parents=True, exist_ok=True)
    text = render(data)
    changed = not MODULE.exists() or MODULE.read_text() != text
    if changed:
        MODULE.write_text(text)
    return {"module": "src/Discovery.lex.tex", "relations": len(REGISTER_CLAIM_RELATIONS), "changed": changed}


def check():
    data = sequencemodel.load()
    if not MODULE.exists() or MODULE.read_text() != render(data):
        return {"ok": False, "reason": "src/Discovery.lex.tex drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}
