"""Builders for the data form of LexLean 1.2 semantic modules (`lexlean/semantic-module/1`).
Every module is pure domain data plus decidable well-formedness predicates and
theorems checked by the Lean 4 kernel (`decide` / `reflexivity`)."""

STR = {"kind": "string"}
BOOL = {"kind": "bool"}
NAT = {"kind": "nat"}


def s(v):
    return {"kind": "string", "value": str(v)}


def b(v):
    return {"kind": "bool", "value": bool(v)}


def n(v):
    return {"kind": "nat", "value": int(v)}


def var(name):
    return {"kind": "var", "name": name}


def named(name, module=None):
    member = {"name": name}
    if module:
        member["module"] = module
    return {"kind": "named", "member": member, "arguments": []}


def list_t(t):
    return {"kind": "list", "element": t}


def call(f, *args, module=None):
    function = {"name": f}
    if module:
        function["module"] = module
    return {"kind": "call", "function": function, "arguments": list(args)}


def ctor(name, module=None):
    c = {"name": name}
    if module:
        c["module"] = module
    return {"kind": "constructor", "constructor": c, "arguments": []}


CHUNK = 35


def lst(elements, element_type):
    """A literal list, chunked through `prim append` below CHUNK elements to avoid parser recursion limits."""
    if len(elements) > CHUNK:
        return {
            "kind": "primitive",
            "operation": "append",
            "result": list_t(element_type),
            "arguments": [lst(elements[:CHUNK], element_type), lst(elements[CHUNK:], element_type)],
        }
    node = {"kind": "nil", "element": element_type}
    for e in reversed(elements):
        node = {"kind": "cons", "head": e, "tail": node}
    return node


def strings(values):
    return lst([s(v) for v in values], STR)


def proj(v, field):
    return {"kind": "project", "value": v, "field": field}


def record(type_name, module=None, **fields):
    t = {"name": type_name}
    if module:
        t["module"] = module
    return {"kind": "record", "type": t, "fields": [{"field": k, "value": v} for k, v in fields.items()]}


def eq_string(a, c):
    return {"kind": "primitive", "operation": "equal", "result": BOOL, "arguments": [a, c]}


def beq(a, c):
    return {"kind": "beq", "left": a, "right": c}


def blt(a, c):
    return {"kind": "blt", "left": a, "right": c}


def ble(a, c):
    return {"kind": "ble", "left": a, "right": c}


def add(a, c):
    return {"kind": "add", "left": a, "right": c}


def if_(c, t, e):
    return {"kind": "if", "condition": c, "then_value": t, "else_value": e}


def match_list(scrutinee, nil_body, head, tail, cons_body):
    return {
        "kind": "match",
        "scrutinee": scrutinee,
        "branches": [
            {"constructor": {"name": "List.nil"}, "binders": [], "body": nil_body},
            {"constructor": {"name": "List.cons"}, "binders": [head, tail], "body": cons_body},
        ],
    }


def structure(name, fields):
    return {
        "kind": "structure",
        "name": name,
        "parameters": [],
        "type_parameters": [],
        "fields": [{"name": f, "type": t} for f, t in fields],
    }


def definition(name, result, body, parameters=(), recursive=None, production=None, executable=False):
    d = {
        "kind": "definition",
        "name": name,
        "parameters": [{"name": p, "type": t} for p, t in parameters],
        "result": result,
        "axioms": [],
        "body": body,
    }
    if recursive:
        d["recursive_argument"] = recursive
    if production or executable:
        d["executable"] = True
    if production:
        d["production"] = {"effects": sorted(production["effects"]), "targets": sorted(production["targets"])}
    return d


def theorem(name, left, right, proof="decide"):
    return {
        "kind": "theorem",
        "name": name,
        "parameters": [],
        "axioms": [],
        "statement": {"kind": "eq", "left": left, "right": right},
        "proof": {"kind": proof},
    }


def holds(name, expression):
    return theorem(name, expression, b(True))


def member_string():
    return definition(
        "memberString",
        BOOL,
        match_list(
            var("values"),
            b(False),
            "head",
            "tail",
            if_(eq_string(var("value"), var("head")), b(True), call("memberString", var("value"), var("tail"))),
        ),
        parameters=[("value", STR), ("values", list_t(STR))],
        recursive="values",
    )


def all_members():
    return definition(
        "allMembers",
        BOOL,
        match_list(
            var("values"),
            b(True),
            "head",
            "tail",
            if_(call("memberString", var("head"), var("ids")), call("allMembers", var("tail"), var("ids")), b(False)),
        ),
        parameters=[("values", list_t(STR)), ("ids", list_t(STR))],
        recursive="values",
    )


def distinct_strings():
    return definition(
        "distinctStrings",
        BOOL,
        match_list(
            var("values"),
            b(True),
            "head",
            "tail",
            if_(call("memberString", var("head"), var("tail")), b(False), call("distinctStrings", var("tail"))),
        ),
        parameters=[("values", list_t(STR))],
        recursive="values",
    )


def index_of():
    return definition(
        "indexOf",
        NAT,
        match_list(
            var("values"),
            n(0),
            "head",
            "tail",
            if_(eq_string(var("value"), var("head")), n(0), add(n(1), call("indexOf", var("value"), var("tail")))),
        ),
        parameters=[("value", STR), ("values", list_t(STR))],
        recursive="values",
    )


def field_of_each(name, element_type, field, result=STR, path=()):
    value = var("head")
    for p in path:
        value = proj(value, p)
    return definition(
        name,
        list_t(result),
        match_list(
            var("xs"),
            {"kind": "nil", "element": result},
            "head",
            "tail",
            {"kind": "cons", "head": proj(value, field), "tail": call(name, var("tail"))},
        ),
        parameters=[("xs", list_t(element_type))],
        recursive="xs",
    )


def each_resolves(name, element_type, field, index_field, ids_param="ids"):
    return definition(
        name,
        BOOL,
        match_list(
            var("xs"),
            b(True),
            "head",
            "tail",
            if_(
                beq(proj(proj(var("head"), "entity"), index_field), call("indexOf", proj(var("head"), field), var(ids_param))),
                call(name, var("tail"), var(ids_param)),
                b(False),
            ),
        ),
        parameters=[("xs", list_t(element_type)), (ids_param, list_t(STR))],
        recursive="xs",
    )


def each_indexed(name, element_type):
    return definition(
        name,
        BOOL,
        match_list(
            var("xs"),
            b(True),
            "head",
            "tail",
            if_(
                beq(proj(proj(var("head"), "entity"), "index"), var("next")),
                call(name, var("tail"), add(var("next"), n(1))),
                b(False),
            ),
        ),
        parameters=[("xs", list_t(element_type)), ("next", NAT)],
        recursive="xs",
    )


def lookup_field(name, element_type, key_field, value_field, result, default, path=()):
    value = var("head")
    for p in path:
        value = proj(value, p)
    return definition(
        name,
        result,
        match_list(
            var("xs"),
            default,
            "head",
            "tail",
            if_(
                eq_string(var("key"), proj(var("head"), key_field)),
                proj(value, value_field),
                call(name, var("key"), var("tail")),
            ),
        ),
        parameters=[("key", STR), ("xs", list_t(element_type))],
        recursive="xs",
    )

