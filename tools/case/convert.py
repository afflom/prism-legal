"""Deterministic controlled-English legal proposition compiler for PrismLegal.
Compiles formal first-order Lean/LexLean signatures into controlled-English prose
and math/statutory islands with zero remote or external LLM."""

from dataclasses import dataclass, field
import re

from . import sexpr
from .lexicon import Entry as _Entry, Lexicon

SORT_WORD = {
    "lexlean.std.nat::nat": "natural number",
    "lexlean.std.int::int": "integer",
    "lexlean.std.bool::bool": "truth value",
}
SORT_LEAN = {
    "Nat": "lexlean.std.nat::nat",
    "Int": "lexlean.std.int::int",
    "Bool": "lexlean.std.bool::bool",
}
CORE = {
    "Eq": "lexlean.core::eq",
    "And": "lexlean.core::land",
    "Or": "lexlean.core::lor",
    "Iff": "lexlean.core::iff",
    "Not": "lexlean.core::lnot",
}
HOPS = {
    "HAdd.hAdd": {"Nat": "Nat.add", "Int": "Int.add"},
    "HSub.hSub": {"Nat": "Nat.sub", "Int": "Int.sub"},
    "HMul.hMul": {"Nat": "Nat.mul", "Int": "Int.mul"},
    "HDiv.hDiv": {"Nat": "Nat.div", "Int": "Int.div"},
    "HMod.hMod": {"Nat": "Nat.mod", "Int": "Int.emod"},
    "HPow.hPow": {"Nat": "Nat.pow"},
    "HXor.hXor": {"Nat": "Nat.xor"},
    "HAnd.hAnd": {"Nat": "Nat.land"},
    "HOr.hOr": {"Nat": "Nat.lor"},
    "LE.le": {"Nat": "Nat.le", "Int": "Int.le"},
    "LT.lt": {"Nat": "Nat.lt", "Int": "Int.lt"},
    "Neg.neg": {"Int": "Int.neg"},
}
ALIASES = {
    "and": "Bool.and",
    "or": "Bool.or",
    "not": "Bool.not",
    "Bool.true": "Bool.true",
    "Bool.false": "Bool.false",
}
DEFEQ = {
    "PrismLegal.Remedies.omittedLedgerCents": "PrismLegal.Disclosure.undisclosedBalance",
    "PrismLegal.Parenting.equalSchedule": "PrismLegal.Parenting.equalOvernights",
}
HINTS = {
    "Nat.cast": "no lexeme for casts; state the fact over one carrier type",
    "Decidable.decide": "no lexeme for decide; state the Bool directly",
    "ite": "no lexeme for if-then-else; use a named function",
    "PrismLegal.Litigation.subjectiveOpinion": "use PrismLegal.Litigation.corroboratedFinding (prism.legal::corroborated-finding)",
}

LOGIC = ("lexlean.core::land", "lexlean.core::lor", "lexlean.core::iff", "->")
RESERVED_SURFACES = {"and", "or", "if", "then", "for", "every", "there", "exists", "such", "that", "implies"}
RESERVED_BINDERS = {"a"}


class Unsupported(Exception):
    pass


@dataclass
class Term:
    kind: str
    head: str = ""
    args: list = field(default_factory=list)
    binders: list = field(default_factory=list)
    body: "Term | None" = None


def _is_function_type(ty):
    if not (isinstance(ty, list) and ty[0] == "pi"):
        return False
    body = ty
    while isinstance(body, list) and body[0] == "pi":
        body = body[4]
    return isinstance(body, list) and (
        (body[0] == "const" and body[1] in ("Nat", "Int", "Bool"))
        or (body[0] == "sort" and body[1] not in ("prop", "0"))
    )


def _numeral_under_eq(node):
    if not isinstance(node, list):
        return False
    if sexpr.is_app(node, "Eq") and any(sexpr.is_app(a, "OfNat.ofNat") for a in node[2:]):
        return True
    return any(_numeral_under_eq(x) for x in node)


_ARROW = _Entry("->", "infix-function", "infix", 2, "→", 25, "right")
_NE = _Entry("lexlean.core::ne", "infix-predicate", "infix", 2, "≠", 50, "none")


class Converter:
    def __init__(self, lexicon: Lexicon, target_package: str = "prism.legal"):
        self.lx = lexicon
        self.target = target_package
        self.visible = lexicon.visible_from(target_package)
        self.used: set[str] = set()
        self.rename: list[tuple[str, str]] = []
        self.bound: set[str] = set()
        self.hyp_counter = 0
        self.has_numeral = False
        self.sorts: dict[str, str] = {}

    def term(self, node):
        if not self.rename and not self.bound:
            self.has_numeral = _numeral_under_eq(node)
        return self._term(node)

    def _term(self, node):
        if isinstance(node, list):
            tag = node[0]
            if tag == "local":
                for raw, new in reversed(self.rename):
                    if raw == node[1]:
                        return Term("local", new)
                return Term("local", node[1])
            if tag == "nat":
                return Term("nat", node[1])
            if tag == "sort":
                if node[1] in ("0", "Prop"):
                    return Term("sort")
                raise Unsupported(f"type-level sort {node[1]} is not a proposition")
            if tag == "const":
                return self.const(node[1], [])
            if tag == "app":
                head = node[1]
                args = node[2:]
                if sexpr.const_name(head) is not None:
                    return self.const(sexpr.const_name(head), args)
                raise Unsupported(f"application of a non-constant head: {sexpr.dumps(head)[:60]}")
            if tag == "pi":
                return self.pi(node)
            if tag == "lam":
                _, name, ty, body = node
                t = self._term(ty)
                new = self.binder_name(name, False)
                self.rename.append((name, new))
                self.bound.add(new)
                if t.kind == "app" and t.head in SORT_WORD:
                    self.sorts[new] = t.head
                out = Term("lam", binders=[(new, t)], body=self._term(body))
                self.rename.pop()
                return out
        raise Unsupported(f"cannot translate {sexpr.dumps(node)[:80]}")

    def binder_name(self, raw, is_hyp):
        name = raw
        if "._@" in name or name == "[anonymous]" or not name:
            name = None
        else:
            name = name.replace("'", "prime").lstrip("_")
            name = re.sub(r"[^A-Za-z0-9]", "", name)
        if not name:
            self.hyp_counter += 1
            name = f"h{self.hyp_counter}"
        if name in RESERVED_BINDERS and self.has_numeral:
            name += "0"
        while name in self.bound:
            name += "0"
        return name

    def pi(self, node):
        vars_, hyps = [], []
        cur = node
        while isinstance(cur, list) and cur[0] == "pi":
            _, kind, name, ty, body = cur
            if kind != "explicit":
                raise Unsupported(f"{kind} binder `{name}` cannot be stated in LexLean; make it explicit")
            if _is_function_type(ty):
                raise Unsupported(
                    f"argument `{name}` has a function type; LexLean's surface is first-order "
                    "(state the theorem on the orbit's own functions, or keep it as a host lemma)"
                )
            t = self._term(ty)
            is_var = t.kind == "app" and t.head in SORT_WORD and not t.args
            new = self.binder_name(name, not is_var)
            self.rename.append((name, new))
            self.bound.add(new)
            if is_var:
                self.sorts[new] = t.head
                if hyps:
                    raise Unsupported(f"variable `{name}` is bound after a hypothesis; reorder binders")
                vars_.append((new, t))
            else:
                hyps.append((new, t))
            cur = body
        body = self._term(cur)
        for _ in range(len(vars_) + len(hyps)):
            self.rename.pop()
        if hyps:
            body = Term("pi", binders=hyps, body=body)
        if vars_:
            body = Term("pi", binders=vars_, body=body)
        return body

    def const(self, name, args):
        if name == "OfNat.ofNat":
            lit = args[1]
            if isinstance(lit, list) and lit[0] == "nat":
                return Term("nat", lit[1])
            raise Unsupported("non-literal OfNat")
        if name in SORT_LEAN and not args:
            return Term("app", SORT_LEAN[name])
        if name == "Nat.zero" and not args:
            return Term("nat", "0")
        if name in CORE:
            payload = args[1:] if name == "Eq" else args
            return Term("app", CORE[name], [self._term(a) for a in payload])
        if name == "Ne":
            return Term(
                "app",
                "lexlean.core::lnot",
                [Term("app", "lexlean.core::eq", [self._term(a) for a in args[1:]])],
            )
        if name == "Exists":
            lam = args[1]
            if not (isinstance(lam, list) and lam[0] == "lam"):
                raise Unsupported("existential without a literal binder")
            return Term("app", "lexlean.core::exists-op", [self._term(lam)])
        if name in HOPS:
            carrier = sexpr.const_name(args[0])
            under = HOPS[name].get(carrier)
            if under is None:
                raise Unsupported(f"{name} over {carrier}")
            n_type = {"LE.le": 1, "LT.lt": 1, "Neg.neg": 1}.get(name, 3)
            payload = args[n_type + 1 :]
            return self.lexeme(under, payload, name)
        name = ALIASES.get(name, name)
        if name in DEFEQ and self.lx.for_lean(DEFEQ[name]) is not None:
            return self.lexeme(DEFEQ[name], args, name)
        return self.lexeme(name, args, name)

    def lexeme(self, lean_name, args, shown):
        entry = self.lx.for_lean(lean_name, self.visible)
        if entry is None:
            hint = HINTS.get(shown) or HINTS.get(lean_name)
            msg = f"no lexeme denotes `{shown}`"
            if hint:
                msg += f"; {hint}"
            raise Unsupported(msg)
        if entry.package not in self.visible and entry.project != "builtin":
            raise Unsupported(f"`{entry.qid}` is not visible from {self.target} (imports: {sorted(self.visible)})")
        if entry.arity != len(args):
            raise Unsupported(f"`{entry.qid}` takes {entry.arity} arguments, got {len(args)}")
        self.used.add(entry.qid)
        return Term("app", entry.qid, [self._term(a) for a in args])

    def statement(self, t: Term):
        return self._prop(t, top=True, spine=True)

    def _prop(self, t, top, spine=False):
        if t.kind == "pi":
            if all(ty.kind == "app" and ty.head in SORT_WORD for _, ty in t.binders):
                lead = "For every " if top else "for every "
                names = " and ".join(f"{SORT_WORD[ty.head]} \\({n}\\)" for n, ty in t.binders)
                return lead + names + ", " + self._prop(t.body, False, True)
            if not spine and not self._quantified(t):
                return "\\(" + self.math(t) + "\\)"
            out = ""
            for _, ty in t.binders:
                out += "if " + self._prop(ty, False, True) + ", then "
            return out + self._prop(t.body, False, True)
        if t.kind == "app" and t.head == "lexlean.core::exists-op":
            lam = t.args[0]
            (n, ty), = lam.binders
            word = SORT_WORD.get(ty.head)
            if word is None:
                raise Unsupported("existential over a non-basic type")
            art = "an" if word[0] in "aeiou" else "a"
            return f"there exists {art} {word} \\({n}\\) such that " + self._prop(lam.body, False, True)
        if t.kind == "app" and t.head == "lexlean.core::lnot" and self._quantified(t.args[0]):
            return "not " + self._prop(t.args[0], False, True)
        if t.kind == "app" and t.head == "lexlean.core::land" and any(self._quantified(a) for a in t.args):
            return " and ".join(self._prop(a, False, True) for a in t.args)
        return "\\(" + self.math(t) + "\\)"

    def _quantified(self, t):
        if t.kind == "pi":
            return (
                any(ty.kind == "app" and ty.head in SORT_WORD for _, ty in t.binders)
                or any(self._quantified(ty) for _, ty in t.binders)
                or self._quantified(t.body)
            )
        if t.kind == "app" and t.head == "lexlean.core::exists-op":
            return True
        return (
            t.kind == "app"
            and t.head in ("lexlean.core::lnot", "lexlean.core::land")
            and any(self._quantified(a) for a in t.args)
        )

    def sort_of(self, t):
        if t.kind == "local":
            return self.sorts.get(t.head)
        if t.kind == "nat":
            return None
        if t.kind == "app":
            e = self.lx.get(t.head)
            if e and e.signature:
                node = sexpr.parse(e.signature)
                while isinstance(node, list) and node and node[0] == "pi":
                    node = node[2]
                return sexpr.const_name(node)
        return None

    def _is_nat_eq(self, eq):
        a, b = (self.sort_of(x) for x in eq.args)
        return {a, b} <= {"lexlean.std.nat::nat", None} and (a or b) is not None

    def _compound(self, t):
        return t.kind == "app" and bool(t.args) and self.lx.get(t.head).frame in ("infix", "prefix")

    def math_child(self, child, parent, side):
        s = self.math(child)
        if child.kind == "pi":
            return "(" + s + ")"
        if child.kind != "app" or not child.args:
            return s
        if (
            child.head == "lexlean.core::lnot"
            and child.args[0].kind == "app"
            and child.args[0].head == "lexlean.core::eq"
            and self._is_nat_eq(child.args[0])
        ):
            ce = _NE
        else:
            ce = self.lx.get(child.head)
        if ce.frame not in ("infix", "prefix"):
            return s
        cp, pp = ce.precedence or 0, parent.precedence or 0
        if cp > pp:
            return s
        if (
            cp == pp
            and ce.associativity == parent.associativity
            and side == parent.associativity
            and parent.associativity in ("left", "right")
        ):
            return s
        return "(" + s + ")"

    def math(self, t: Term, parent=None, side=None):
        if t.kind == "local" or t.kind == "nat":
            return t.head
        if t.kind == "pi":
            if any(ty.kind == "app" and ty.head in SORT_WORD for _, ty in t.binders):
                raise Unsupported("quantifier inside a math island")
            parts = [self.math_child(ty, _ARROW, "left") for _, ty in t.binders]
            return " → ".join(parts + [self.math_child(t.body, _ARROW, "right")])
        if t.kind in ("lam", "sort"):
            raise Unsupported("binder inside a math island")
        if (
            t.kind == "app"
            and t.head == "lexlean.core::lnot"
            and t.args[0].kind == "app"
            and t.args[0].head == "lexlean.core::eq"
            and self._is_nat_eq(t.args[0])
        ):
            l, r = t.args[0].args
            ne = _NE
            return f"{self.math_child(l, ne, 'left')} ≠ {self.math_child(r, ne, 'right')}"
        e = self.lx.get(t.head)
        if e is None or e.surface is None:
            raise Unsupported(f"`{t.head}` has no math surface; it cannot appear in a statement")
        if e.frame == "atom" or not t.args:
            return e.surface
        surface = f"\\lexeme{{{e.qid}}}" if e.surface in RESERVED_SURFACES else e.surface
        if e.frame == "call":
            return surface + "(" + ", ".join(self.math(a) for a in t.args) + ")"
        if e.frame == "prefix":
            a = t.args[0]
            inner = self.math(a)
            return f"{surface} ({inner})" if self._compound(a) else f"{surface} {inner}"
        if e.frame == "infix":
            l, r = t.args
            return f"{self.math_child(l, e, 'left')} {e.surface} {self.math_child(r, e, 'right')}"
        raise Unsupported(f"frame {e.frame} of {e.qid}")
