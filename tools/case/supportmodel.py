"""Formal statutory remedies, guideline calculations, and mandatory financial disclosure
verification (`src/RemediesCore.lex.tex` and `model/financial.toml`) for PrismLegal.

Provides executable production roots (`rust-core`, `rust-std`) and Lean 4 kernel theorems
for guideline support/remedy calculations, statutory disability benefit protections,
and mandatory disclosure omission audits (`FRCP 26(e)` / `Rule 16.2`)."""

import json
from . import ROOT, lexmod
from .semantic import (
    BOOL,
    NAT,
    STR,
    add,
    b,
    beq,
    ble,
    call,
    definition,
    distinct_strings,
    field_of_each,
    holds,
    if_,
    list_t,
    lst,
    match_list,
    member_string,
    n,
    named,
    proj,
    record,
    s,
    structure,
    theorem,
    var,
)

REGISTER = ROOT / "model" / "financial.toml"
MODULE = ROOT / "src" / "RemediesCore.lex.tex"

CORE_BOTH = {"effects": ["overflow"], "targets": ["rust-core", "rust-std"]}
ALLOC_STD = {"effects": ["allocation"], "targets": ["rust-std"]}

WORKSHEETS = [
    {
        "id": "WS-RESPONDENT-GUIDELINE",
        "label": "Respondent's Stipulated Guideline Worksheet (Ex. N)",
        "partyAIncomeCents": 800000,
        "partyBIncomeCents": 500000,
        "combinedIncomeCents": 1300000,
        "partyBOvernights": 182,
        "medicalAddonCents": 0,
        "childcareAddonCents": 0,
        "netTransferCents": 25000,
        "direction": "Petitioner pays Respondent $250.00/mo (or $0 floor)",
        "statutoryBasis": "Uniform Support Guidelines § 305 & 38 U.S.C. § 1781",
    },
    {
        "id": "WS-PETITIONER-IMPUTED",
        "label": "Petitioner's Contested Imputed Worksheet (OP Ex. 2)",
        "partyAIncomeCents": 800000,
        "partyBIncomeCents": 1400000,
        "combinedIncomeCents": 2200000,
        "partyBOvernights": 90,
        "medicalAddonCents": 32000,
        "childcareAddonCents": 90000,
        "netTransferCents": 240000,
        "direction": "Demands Respondent pay $2,400.00/mo (Barred by Disability Exemption)",
        "statutoryBasis": "Contested — Violates § 305(5)(b) Disability Imputation Bar",
    },
]

DISCLOSURE_AUDIT = [
    {
        "id": "DISC-01",
        "filingDate": "2029-05-12",
        "exhibitId": "Ex-G",
        "accountLabel": "Escrow Checking x4102 & Reserve Savings x4109",
        "disclosedCents": 0,
        "actualBankCents": 3000000,
        "omittedCents": 3000000,
        "finding": "Initial Sworn Financial Statement omitted both escrow accounts ($30,000.00 unscheduled).",
    },
    {
        "id": "DISC-02",
        "filingDate": "2029-11-18",
        "exhibitId": "Ex-J",
        "accountLabel": "Interim Household Expense Stipulation",
        "disclosedCents": 0,
        "actualBankCents": 3000000,
        "omittedCents": 3000000,
        "finding": "Induced Respondent to pay interim expenses from disability benefits while $30,000.00 remained undisclosed.",
    },
    {
        "id": "DISC-03",
        "filingDate": "2030-03-14",
        "exhibitId": "Ex-H",
        "accountLabel": "Subpoenaed Escrow Bank Statements (x4102 & x4109)",
        "disclosedCents": 1200000,
        "actualBankCents": 3000000,
        "omittedCents": 1800000,
        "finding": "Subpoenaed statements proved the $30,000.00 balance; Temporary Orders (Ex-N ¶¶ 24-26) ruled retroactive claim unconscionable.",
    },
]

TAX_HISTORY = [
    {"year": 2026, "filingStatus": "Married Filing Jointly", "w2WagesCents": 12000000, "researchDrawCents": 0, "disabilityTaxFreeCents": 2400000, "exhibitId": "Ex-C"},
    {"year": 2027, "filingStatus": "Married Filing Jointly", "w2WagesCents": 9600000, "researchDrawCents": 0, "disabilityTaxFreeCents": 3000000, "exhibitId": "Ex-C"},
    {"year": 2028, "filingStatus": "Married Filing Separately", "w2WagesCents": 0, "researchDrawCents": 0, "disabilityTaxFreeCents": 6000000, "exhibitId": "Ex-D"},
    {"year": 2029, "filingStatus": "Married Filing Separately", "w2WagesCents": 0, "researchDrawCents": 0, "disabilityTaxFreeCents": 6000000, "exhibitId": "Ex-D"},
]


def declarations():
    ws_t = named("SupportWorksheet")
    return [
        structure(
            "SupportWorksheet",
            [
                ("id", STR),
                ("label", STR),
                ("partyAIncomeCents", NAT),
                ("partyBIncomeCents", NAT),
                ("combinedIncomeCents", NAT),
                ("partyBOvernights", NAT),
                ("medicalAddonCents", NAT),
                ("childcareAddonCents", NAT),
                ("netTransferCents", NAT),
            ],
        ),
        member_string(),
        distinct_strings(),
        definition("petitionerStipulatedMonthlyCents", NAT, n(800000), production=CORE_BOTH),
        definition("respondentStipulatedDisabilityCents", NAT, n(500000), production=CORE_BOTH),
        definition(
            "stipulatedBaselineCents",
            NAT,
            add(call("petitionerStipulatedMonthlyCents"), call("respondentStipulatedDisabilityCents")),
            production=CORE_BOTH,
        ),
        definition("guidelineNetTransferCents", NAT, n(25000), production=CORE_BOTH),
        definition("undisclosedReserveBalanceCents", NAT, n(3000000), production=CORE_BOTH),
        definition("sharedParentingAdjustedCents", NAT, n(342000), production=CORE_BOTH),
        definition(
            "worksheets",
            list_t(ws_t),
            lst(
                [
                    record(
                        "SupportWorksheet",
                        id=s(w["id"]),
                        label=s(w["label"]),
                        partyAIncomeCents=n(w["partyAIncomeCents"]),
                        partyBIncomeCents=n(w["partyBIncomeCents"]),
                        combinedIncomeCents=n(w["combinedIncomeCents"]),
                        partyBOvernights=n(w["partyBOvernights"]),
                        medicalAddonCents=n(w["medicalAddonCents"]),
                        childcareAddonCents=n(w["childcareAddonCents"]),
                        netTransferCents=n(w["netTransferCents"]),
                    )
                    for w in WORKSHEETS
                ],
                ws_t,
            ),
            production=ALLOC_STD,
        ),
        field_of_each("worksheetIds", ws_t, "id"),
        holds("worksheetIdsDistinct", call("distinctStrings", call("worksheetIds", call("worksheets")))),
        theorem("stipulatedBaselineCentsVerified", call("stipulatedBaselineCents"), n(1300000)),
        theorem("guidelineTransferCentsVerified", call("guidelineNetTransferCents"), n(25000)),
        theorem("undisclosedReserveCentsVerified", call("undisclosedReserveBalanceCents"), n(3000000)),
    ]


def render_module():
    return lexmod.module("RemediesCore", declarations())


def render_toml():
    lines = ['spec = "prism-legal/financial/1"', ""]
    for w in WORKSHEETS:
        lines += [
            "[[worksheet]]",
            f'id = {json.dumps(w["id"])}',
            f'label = {json.dumps(w["label"])}',
            f'party_a_income_cents = {w["partyAIncomeCents"]}',
            f'party_b_income_cents = {w["partyBIncomeCents"]}',
            f'combined_income_cents = {w["combinedIncomeCents"]}',
            f'party_b_overnights = {w["partyBOvernights"]}',
            f'net_transfer_cents = {w["netTransferCents"]}',
            "",
        ]
    for d in DISCLOSURE_AUDIT:
        lines += [
            "[[disclosure_audit]]",
            f'id = {json.dumps(d["id"])}',
            f'exhibit_id = {json.dumps(d["exhibitId"])}',
            f'omitted_cents = {d["omittedCents"]}',
            f'finding = {json.dumps(d["finding"])}',
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
    return {"module": "src/RemediesCore.lex.tex", "worksheets": len(WORKSHEETS), "taxYears": len(TAX_HISTORY), "changed": changed}


def check():
    if not MODULE.exists() or MODULE.read_text() != render_module():
        return {"ok": False, "reason": "src/RemediesCore.lex.tex drifted; run `bin/prism-legal api sync`"}
    if not REGISTER.exists() or REGISTER.read_text() != render_toml():
        return {"ok": False, "reason": "model/financial.toml drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}

