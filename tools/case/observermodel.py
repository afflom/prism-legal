"""Observer-Vantage Quadruple Model (`src/Observer.lex.tex` and `model/observer.toml`) for PrismLegal."""

import json
from . import ROOT, lexmod
from .semantic import (
    BOOL,
    STR,
    b,
    call,
    definition,
    distinct_strings,
    field_of_each,
    holds,
    list_t,
    lst,
    member_string,
    named,
    record,
    s,
    structure,
)

REGISTER = ROOT / "model" / "observer.toml"
MODULE = ROOT / "src" / "Observer.lex.tex"

QUADRUPLES = [
    {
        "id": "OBS-CLIENT",
        "observer": "Client Litigant (Respondent)",
        "observed": "Direct Walkthrough, Cross-Exam Flashcards & Shared Strategy",
        "vantage": "Client Workspace (client.html)",
        "focus": "Calm testimony delivery, 50/50 parenting stability for the three minor children, and co-design with counsel.",
    },
    {
        "id": "OBS-COUNSEL",
        "observer": "Lead & Specialized Co-Counsel (Trial, Veterans, Commercial & Legal Aid)",
        "observed": "Statutory Proof Matrix, 30-Exhibit Vault, Visual Forensics & Jural Tuner",
        "vantage": "Counsel Workbench (lawyer.html)",
        "focus": "Evidentiary foundation, FRE 106/602/613 objections, Rule 26(e)/16.2 impeachment, and 360-minute trial clock.",
    },
    {
        "id": "OBS-BENCH",
        "observer": "Presiding Judicial Fact-Finder (Division 7C)",
        "observed": "Stipulated Pretrial Facts, Statutory Factors & Credibility",
        "vantage": "Courtroom Hearing Mode (courtroom.html)",
        "focus": "Best-interests compliance (§ 402), guideline support accuracy (§ 305), and clear documentary proof.",
    },
    {
        "id": "OBS-BENEFICIARIES",
        "observer": "Minor Beneficiaries (Ages 15, 11 & 6)",
        "observed": "Equal 50/50 Routine & Wednesday School Exchanges",
        "vantage": "Equal Parenting Schedule & Townhouse Environment",
        "focus": "Loving access to both parents, continuity of school/friends, and zero exposure to parental conflict.",
    },
    {
        "id": "OBS-CLINIC",
        "observer": "Public-Benefit Legal Aid Clinic & Open-Source Adopters",
        "observed": "Multi-Domain Legal Framework & Cryptographic Sharing",
        "vantage": "Platform Hub (index.html)",
        "focus": "Formally verified legal case preparation across family, civil, veterans, employment, and housing law.",
    },
]


def declarations():
    q_t = named("ObserverQuadruple")
    return [
        structure("ObserverQuadruple", [("id", STR), ("observer", STR), ("observed", STR), ("vantage", STR), ("focus", STR)]),
        member_string(),
        distinct_strings(),
        definition(
            "quadruples",
            list_t(q_t),
            lst(
                [
                    record("ObserverQuadruple", id=s(q["id"]), observer=s(q["observer"]), observed=s(q["observed"]), vantage=s(q["vantage"]), focus=s(q["focus"]))
                    for q in QUADRUPLES
                ],
                q_t,
            ),
        ),
        field_of_each("quadrupleIds", q_t, "id"),
        holds("observerQuadrupleIdsDistinct", call("distinctStrings", call("quadrupleIds", call("quadruples")))),
    ]


def render_module():
    return lexmod.module("Observer", declarations())


def render_toml():
    lines = ['spec = "prism-legal/observer/1"', ""]
    for q in QUADRUPLES:
        lines += [
            "[[quadruple]]",
            f'id = {json.dumps(q["id"])}',
            f'observer = {json.dumps(q["observer"])}',
            f'vantage = {json.dumps(q["vantage"])}',
            f'focus = {json.dumps(q["focus"])}',
            "",
        ]
    return "\n".join(lines)


def sync():
    MODULE.parent.mkdir(parents=True, exist_ok=True)
    REGISTER.parent.mkdir(parents=True, exist_ok=True)
    m = render_module()
    t = render_toml()
    changed = False
    if not MODULE.exists() or MODULE.read_text() != m:
        MODULE.write_text(m)
        changed = True
    if not REGISTER.exists() or REGISTER.read_text() != t:
        REGISTER.write_text(t)
        changed = True
    return {"module": "src/Observer.lex.tex", "quadruples": len(QUADRUPLES), "changed": changed}


def check():
    if not MODULE.exists() or MODULE.read_text() != render_module():
        return {"ok": False, "reason": "src/Observer.lex.tex drifted; run `bin/prism-legal api sync`"}
    if not REGISTER.exists() or REGISTER.read_text() != render_toml():
        return {"ok": False, "reason": "model/observer.toml drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}

