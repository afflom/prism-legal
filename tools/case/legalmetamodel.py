"""Formal Legal Meta-Theory & International Case Management Standards
(`src/LegalMeta.lex.tex` and `model/legal-meta.toml`) for PrismLegal:
1. Hohfeldian Jural Relations (`HOH-01`..`HOH-10`)
2. OASIS LegalRuleML v1.0 Defeasible Rules (`LRML-01`..`LRML-12`) & Superiority (`SUP-01`..`SUP-06`)
3. Dung (1995) / ASPIC+ Structured Legal Argumentation (`ARG-OP-01`..`16`, `ARG-RESP-01`..`16`, `ATK-01`..`16`)
4. OASIS Akoma Ntoso v1.0 FRBR Legal Document URIs (`AKN-01`..`AKN-10`)
5. ISO 15489 / ISO/IEC 27037 Evidentiary Chain of Custody (`COC-01`..`COC-12`)"""

import json
from . import ROOT, casemodel, lexmod
from .semantic import (
    BOOL,
    STR,
    all_members,
    b,
    call,
    definition,
    distinct_strings,
    eq_string,
    field_of_each,
    holds,
    if_,
    list_t,
    lst,
    match_list,
    member_string,
    named,
    proj,
    record,
    s,
    strings,
    structure,
    var,
)

REGISTER = ROOT / "model" / "legal-meta.toml"
MODULE = ROOT / "src" / "LegalMeta.lex.tex"

HOHFELD_POSITIONS = ["Right", "Duty", "Privilege", "NoRight", "Power", "Liability", "Immunity", "Disability"]

HOHFELD_RELATIONS = [
    {"id": "HOH-01", "title": "Equal Parenting Time Claim-Right", "dominantParty": "Minor Beneficiaries (Ages 15, 11 & 6) & Respondent", "subordinateParty": "Petitioner", "dominantPosition": "Right", "correlativePosition": "Duty", "juralOpposite": "NoRight", "subjectMatter": "182.5 annual overnights each with Wednesday school exchanges (Ex-L).", "statutoryAuthority": "Uniform Best-Interests Standard § 402(a)", "backingExhibits": ["Ex-I", "Ex-L", "Ex-N"]},
    {"id": "HOH-02", "title": "Joint Major Decision-Making Power", "dominantParty": "Both Co-Parents Jointly", "subordinateParty": "Unilateral Decision-Maker", "dominantPosition": "Power", "correlativePosition": "Liability", "juralOpposite": "Disability", "subjectMatter": "Shared educational, medical, and developmental governance with mediation first (Ex-L § 4.11).", "statutoryAuthority": "Uniform Best-Interests Standard § 402(b)", "backingExhibits": ["Ex-J", "Ex-L", "Ex-M", "Ex-O"]},
    {"id": "HOH-03", "title": "Disability Pension Statutory Immunity Against Income Imputation", "dominantParty": "Respondent (Retired Disability Pensioner)", "subordinateParty": "Petitioner / Tribunal", "dominantPosition": "Immunity", "correlativePosition": "Disability", "juralOpposite": "Liability", "subjectMatter": "Exemption from speculative potential-income imputation on top of verified disability benefits.", "statutoryAuthority": "Uniform Support Guidelines § 305(5)(b) & 38 U.S.C. Ch. 11", "backingExhibits": ["Ex-D", "Ex-E", "Ex-F", "Ex-N"]},
    {"id": "HOH-04", "title": "Guideline Support Transfer Claim-Right ($250.00/mo)", "dominantParty": "Respondent", "subordinateParty": "Petitioner", "dominantPosition": "Right", "correlativePosition": "Duty", "juralOpposite": "NoRight", "subjectMatter": "Guideline child support calculated on stipulated incomes ($8,000/mo vs. $5,000/mo) at 182.5 overnights.", "statutoryAuthority": "Uniform Support Guidelines § 305(8)", "backingExhibits": ["Ex-B", "Ex-E", "Ex-N"]},
    {"id": "HOH-05", "title": "Rule 26(e) / Rule 16.2 Reopening & Unconscionability Power", "dominantParty": "Respondent & Tribunal", "subordinateParty": "Petitioner", "dominantPosition": "Power", "correlativePosition": "Liability", "juralOpposite": "Disability", "subjectMatter": "Judicial power to set aside interim expense stipulations procured during a $30,000.00 sworn escrow omission.", "statutoryAuthority": "FRCP 26(e) & Mandatory Disclosure Rule 16.2(e)(10)", "backingExhibits": ["Ex-G", "Ex-H", "Ex-J", "Ex-N"]},
    {"id": "HOH-06", "title": "Direct Parental Care Privilege During Regional Travel Blocks", "dominantParty": "Respondent", "subordinateParty": "Petitioner", "dominantPosition": "Privilege", "correlativePosition": "NoRight", "juralOpposite": "Duty", "subjectMatter": "Right of first refusal and full-time availability to care for the children for $0 instead of a $2,400/mo agency.", "statutoryAuthority": "Uniform Support Guidelines § 305(9) & § 402(a)", "backingExhibits": ["Ex-E", "Ex-L", "OP-Ex-04"]},
    {"id": "HOH-07", "title": "Equal Statutory Access to School & Medical Records", "dominantParty": "Respondent", "subordinateParty": "Schools, Clinics & Petitioner", "dominantPosition": "Right", "correlativePosition": "Duty", "juralOpposite": "NoRight", "subjectMatter": "Unrestricted statutory access to all academic, medical, and counseling records of the three minor children.", "statutoryAuthority": "Uniform Records Access Statute § 123.8", "backingExhibits": ["Ex-L"]},
    {"id": "HOH-08", "title": "Zero-Premium Statutory Dependent Healthcare Immunity", "dominantParty": "Respondent & Minor Beneficiaries", "subordinateParty": "Petitioner", "dominantPosition": "Immunity", "correlativePosition": "Disability", "juralOpposite": "Liability", "subjectMatter": "Immunity from duplicate $320/mo medical insurance add-ons when comprehensive statutory coverage is active.", "statutoryAuthority": "38 U.S.C. § 1781 & Support Guidelines § 305(10)", "backingExhibits": ["Ex-E", "Ex-N"]},
    {"id": "HOH-09", "title": "FRE 106 Rule of Completeness Evidentiary Right", "dominantParty": "Respondent", "subordinateParty": "Petitioner", "dominantPosition": "Right", "correlativePosition": "Duty", "juralOpposite": "NoRight", "subjectMatter": "Immediate introduction of full page/thread context whenever an isolated study log or message line is offered.", "statutoryAuthority": "Federal & Uniform Rule of Evidence 106", "backingExhibits": ["Ex-O", "OP-Ex-13", "OP-Ex-14"]},
    {"id": "HOH-10", "title": "ABA Rule 1.2(c) & 1.16(a)(3) Client Freedom of Counsel Choice", "dominantParty": "Client Litigant", "subordinateParty": "Engaged Law Firms", "dominantPosition": "Power", "correlativePosition": "Liability", "juralOpposite": "Disability", "subjectMatter": "Power to retain specialized counsel per matter without single-lawyer lock-in.", "statutoryAuthority": "ABA Model Rules 1.2(c) & 1.16(a)(3)", "backingExhibits": ["Ex-L", "Ex-N"]},
]

LEGAL_RULES = [
    {"id": "LRML-01", "strength": "StrictRule", "deonticModality": "Obligation", "statutorySource": "Uniform Best-Interests § 402(a)", "antecedent": "Both parents are fit, capable, and practiced a 90-day 50/50 schedule without incident.", "consequent": "Allocate equal 50/50 parenting time (182.5 overnights each) with Wednesday school exchanges."},
    {"id": "LRML-02", "strength": "DefeasibleRule", "deonticModality": "Obligation", "statutorySource": "Uniform Support Guidelines § 305(5)(a)", "antecedent": "A parent is voluntarily unemployed or underemployed.", "consequent": "Potential income may be imputed unless a statutory exception applies."},
    {"id": "LRML-03", "strength": "StrictRule", "deonticModality": "Prohibition", "statutorySource": "Uniform Support Guidelines § 305(5)(b)", "antecedent": "A parent receives certified disability retirement benefits (Ex-E).", "consequent": "Prohibit imputing speculative potential wages on top of disability retirement benefits."},
    {"id": "LRML-04", "strength": "StrictRule", "deonticModality": "Immunity", "statutorySource": "38 U.S.C. § 1781 & Guidelines § 305(10)", "antecedent": "Minor beneficiaries are covered by zero-premium statutory dependent medical insurance (Ex-E).", "consequent": "Eliminate duplicate commercial health insurance add-on ($0 medical add-on)."},
    {"id": "LRML-05", "strength": "DefeasibleRule", "deonticModality": "Permission", "statutorySource": "Uniform Support Guidelines § 305(9)", "antecedent": "Work-related childcare expenses are actually necessary.", "consequent": "Include reasonable childcare costs in the worksheet."},
    {"id": "LRML-06", "strength": "StrictRule", "deonticModality": "Prohibition", "statutorySource": "Uniform Support Guidelines § 305(9) & § 402(a)", "antecedent": "A fit co-parent is available full-time at $0 cost during the other parent's regional travel blocks.", "consequent": "Disallow $2,400/mo commercial agency add-on ($0 childcare add-on)."},
    {"id": "LRML-07", "strength": "DefeasibleRule", "deonticModality": "Obligation", "statutorySource": "Contract / Stipulation Baseline", "antecedent": "Parties sign an interim household expense stipulation (Ex-J).", "consequent": "Enforce interim expense terms unless procured by material non-disclosure."},
    {"id": "LRML-08", "strength": "StrictRule", "deonticModality": "Power", "statutorySource": "FRCP 26(e) / Mandatory Disclosure Rule 16.2(e)(10)", "antecedent": "Party omits $30,000.00 in escrow bank accounts (Ex-H) on Sworn Financial Statement (Ex-G).", "consequent": "Hold interim expense stipulation unconscionable and bar retroactive support claim (Ex-N ¶¶ 24-26)."},
    {"id": "LRML-09", "strength": "DefeasibleRule", "deonticModality": "Prohibition", "statutorySource": "Uniform Best-Interests § 402(b)", "antecedent": "Credible finding of ongoing household conflict exists.", "consequent": "Restrict joint decision-making."},
    {"id": "LRML-10", "strength": "StrictRule", "deonticModality": "Obligation", "statutorySource": "Uniform Best-Interests § 402(b) & Ex-J", "antecedent": "Interim petition was dismissed by stipulation (Ex-J), telemetry refutes proximity (Ex-A), and 9 months are incident-free (Ex-O).", "consequent": "Order Joint Major Decision-Making with mediation first (Ex-L)."},
    {"id": "LRML-11", "strength": "StrictRule", "deonticModality": "Obligation", "statutorySource": "FRE 106 (Rule of Completeness)", "antecedent": "Opposing party introduces a partial excerpt from a study log (OP-Ex-13) or message log (OP-Ex-05).", "consequent": "Require immediate admission of the remainder of the page/thread establishing full meaning."},
    {"id": "LRML-12", "strength": "StrictRule", "deonticModality": "Prohibition", "statutorySource": "FRE 602 & FRE 802", "antecedent": "Third-party witness lacks personal observation of Respondent's post-separation townhouse.", "consequent": "Exclude speculative opinion and hearsay testimony."},
]

SUPERIORITY_OVERRIDES = [
    {"id": "SUP-01", "superiorRuleId": "LRML-03", "inferiorRuleId": "LRML-02", "authority": "Uniform Support Guidelines § 305(5)(b)", "rationale": "Statutory disability retirement exemption strictly overrides general potential-income imputation."},
    {"id": "SUP-02", "superiorRuleId": "LRML-06", "inferiorRuleId": "LRML-05", "authority": "Uniform Support Guidelines § 305(9)", "rationale": "Available fit parent providing free care during travel blocks overrides $2,400/mo commercial agency add-on."},
    {"id": "SUP-03", "superiorRuleId": "LRML-08", "inferiorRuleId": "LRML-07", "authority": "Rule 16.2(e)(10) & Ex-N ¶¶ 24-26", "rationale": "Sworn omission of $30,000.00 in escrow accounts overrides interim stipulation and bars retroactive claims."},
    {"id": "SUP-04", "superiorRuleId": "LRML-10", "inferiorRuleId": "LRML-09", "authority": "Uniform Best-Interests § 402(b) & Ex-J", "rationale": "Stipulated petition dismissal, 512-yd telemetry proof, and 9 incident-free months defeat unilateral governance claim."},
    {"id": "SUP-05", "superiorRuleId": "LRML-04", "inferiorRuleId": "LRML-02", "authority": "38 U.S.C. § 1781", "rationale": "Zero-premium statutory dependent medical coverage overrides duplicate insurance add-ons."},
    {"id": "SUP-06", "superiorRuleId": "LRML-11", "inferiorRuleId": "LRML-09", "authority": "FRE 106", "rationale": "Complete October 14, 2028 study log recording positive reinforcement overrides cherry-picked quote."},
]

ARGUMENTS = []
ATTACKS = []
for i, t in enumerate(range(1, 17), 1):
    op_id = f"ARG-OP-{i:02d}"
    resp_id = f"ARG-RESP-{i:02d}"
    atk_id = f"ATK-{i:02d}"
    ARGUMENTS.append({"id": op_id, "party": "Petitioner", "trapId": f"TRAP-{i:02d}", "claim": f"Opposing allegation in TRAP-{i:02d}"})
    ARGUMENTS.append({"id": resp_id, "party": "Respondent", "trapId": f"TRAP-{i:02d}", "claim": f"Corroborated rebuttal in TRAP-{i:02d}"})
    ATTACKS.append({"id": atk_id, "attackerId": resp_id, "targetId": op_id, "kind": "rebuts", "succeeded": True})

AKN_DOCUMENTS = [
    {"id": "AKN-01", "workUri": "akn:/us-uniform/act/marriage-and-divorce/sec-402", "title": "Uniform Best-Interests & Parenting Allocation Standard (§ 402)"},
    {"id": "AKN-02", "workUri": "akn:/us-uniform/act/child-support-guidelines/sec-305", "title": "Uniform Child Support Guidelines & Disability Exception (§ 305)"},
    {"id": "AKN-03", "workUri": "akn:/us/act/usc-title-38/sec-1781", "title": "38 U.S.C. § 1781 — Statutory Dependent Medical Coverage"},
    {"id": "AKN-04", "workUri": "akn:/us/rule/frcp/rule-26-e", "title": "FRCP 26(e) / Mandatory Financial Disclosure Rule 16.2(e)(10)"},
    {"id": "AKN-05", "workUri": "akn:/us/rule/fre/rule-106", "title": "Federal & Uniform Rule of Evidence 106 — Rule of Completeness"},
    {"id": "AKN-06", "workUri": "akn:/us/rule/fre/rule-602", "title": "Federal & Uniform Rule of Evidence 602 — Personal Knowledge"},
    {"id": "AKN-07", "workUri": "akn:/us/rule/fre/rule-901", "title": "Federal & Uniform Rule of Evidence 901 — Authentication"},
    {"id": "AKN-08", "workUri": "akn:/us/rule/aba-model-rules/rule-1-2", "title": "ABA Model Rules 1.2(c) & 1.16(a)(3) — Unbundled Counsel & Client Choice"},
    {"id": "AKN-09", "workUri": "akn:/us-state/court/2030-fam-9010/order-temporary-2030-06-20", "title": "Temporary Orders Ruling (Ex. N)"},
    {"id": "AKN-10", "workUri": "akn:/us-state/court/2030-fam-9010/jtmc-2030-08-29", "title": "Joint Pretrial Management Certificate"},
]

CHAIN_OF_CUSTODY = [
    {"id": "COC-01", "exhibitId": "Ex-A", "iso15489Class": "Authenticated Transit Telemetry Log", "iso27037Acquisition": "Cryptographic SHA-256 export from transit telemetry database", "creFoundation": "FRE 901(b)(9) Automated System Process"},
    {"id": "COC-02", "exhibitId": "Ex-B", "iso15489Class": "Stipulated Payroll Advisory", "iso27037Acquisition": "Party-produced mandatory disclosure record", "creFoundation": "FRE 801(d)(2) & Joint Pretrial Stipulation"},
    {"id": "COC-03", "exhibitId": "Ex-C", "iso15489Class": "Joint Federal Tax Returns (2026-2027)", "iso27037Acquisition": "CPA archive export with electronic filing confirmation", "creFoundation": "FRE 901(b)(1) & Stipulated Tax Record"},
    {"id": "COC-04", "exhibitId": "Ex-D", "iso15489Class": "Certified IRS Tax Transcripts (2028-2029)", "iso27037Acquisition": "Direct IRS Transcript Delivery System PDF", "creFoundation": "FRE 902(1)/(4) Self-Authenticating Public Record"},
    {"id": "COC-05", "exhibitId": "Ex-E", "iso15489Class": "Disability Retirement Decision Letter", "iso27037Acquisition": "Official Retirement Board digital original", "creFoundation": "FRE 902(5) Official Publication & Stipulation"},
    {"id": "COC-06", "exhibitId": "Ex-G", "iso15489Class": "Sworn Court Filing (Initial SFS)", "iso27037Acquisition": "Court E-Filing stamped pleading", "creFoundation": "FRE 801(d)(2) Opposing Party Sworn Statement"},
    {"id": "COC-07", "exhibitId": "Ex-H", "iso15489Class": "Subpoenaed Financial Institution Statements", "iso27037Acquisition": "Custodian-certified bank production (Accounts x4102 & x4109)", "creFoundation": "FRE 803(6) & 902(11) Certified Business Record"},
    {"id": "COC-08", "exhibitId": "Ex-I", "iso15489Class": "Townhouse Photographic Compendium", "iso27037Acquisition": "EXIF-preserved digital photographs taken by Respondent", "creFoundation": "FRE 901(b)(1) Witness with Personal Knowledge"},
    {"id": "COC-09", "exhibitId": "Ex-J", "iso15489Class": "Court-Approved Stipulation", "iso27037Acquisition": "Court docket certified order", "creFoundation": "FRE 201 Judicial Notice of Court Record"},
    {"id": "COC-10", "exhibitId": "Ex-M", "iso15489Class": "Seminar Completion Certificate", "iso27037Acquisition": "Provider-issued verifiable certificate", "creFoundation": "FRE 901(b)(1) & Stipulated Authenticity"},
    {"id": "COC-11", "exhibitId": "Ex-N", "iso15489Class": "Judicial Temporary Orders & Guideline Worksheet", "iso27037Acquisition": "Division 7C signed order & statutory calculation", "creFoundation": "FRE 201 Judicial Notice"},
    {"id": "COC-12", "exhibitId": "Ex-O", "iso15489Class": "Co-Parenting Platform Export", "iso27037Acquisition": "Tamper-evident platform PDF export", "creFoundation": "FRE 901(b)(9) & 803(6)"},
]


def declarations():
    hoh_t = named("HohfeldRelation")
    rule_t = named("LegalRule")
    sup_t = named("SuperiorityOverride")
    akn_t = named("AknDocument")
    coc_t = named("ChainOfCustodyRecord")
    exhibit_ids = [e["id"] for e in casemodel.all_exhibits()]

    return [
        structure("HohfeldRelation", [("id", STR), ("dominantPosition", STR), ("correlativePosition", STR), ("backingExhibits", list_t(STR))]),
        structure("LegalRule", [("id", STR), ("strength", STR), ("deonticModality", STR), ("statutorySource", STR)]),
        structure("SuperiorityOverride", [("id", STR), ("superiorRuleId", STR), ("inferiorRuleId", STR)]),
        structure("AknDocument", [("id", STR), ("workUri", STR), ("title", STR)]),
        structure("ChainOfCustodyRecord", [("id", STR), ("exhibitId", STR), ("iso15489Class", STR)]),
        member_string(),
        all_members(),
        distinct_strings(),
        definition(
            "hohfeldRelations",
            list_t(hoh_t),
            lst(
                [
                    record(
                        "HohfeldRelation",
                        id=s(r["id"]),
                        dominantPosition=s(r["dominantPosition"]),
                        correlativePosition=s(r["correlativePosition"]),
                        backingExhibits=strings(r["backingExhibits"]),
                    )
                    for r in HOHFELD_RELATIONS
                ],
                hoh_t,
            ),
        ),
        definition(
            "legalRules",
            list_t(rule_t),
            lst(
                [
                    record("LegalRule", id=s(r["id"]), strength=s(r["strength"]), deonticModality=s(r["deonticModality"]), statutorySource=s(r["statutorySource"]))
                    for r in LEGAL_RULES
                ],
                rule_t,
            ),
        ),
        definition(
            "superiorityOverrides",
            list_t(sup_t),
            lst(
                [
                    record("SuperiorityOverride", id=s(x["id"]), superiorRuleId=s(x["superiorRuleId"]), inferiorRuleId=s(x["inferiorRuleId"]))
                    for x in SUPERIORITY_OVERRIDES
                ],
                sup_t,
            ),
        ),
        definition(
            "aknDocuments",
            list_t(akn_t),
            lst([record("AknDocument", id=s(a["id"]), workUri=s(a["workUri"]), title=s(a["title"])) for a in AKN_DOCUMENTS], akn_t),
        ),
        definition(
            "chainOfCustody",
            list_t(coc_t),
            lst([record("ChainOfCustodyRecord", id=s(c["id"]), exhibitId=s(c["exhibitId"]), iso15489Class=s(c["iso15489Class"])) for c in CHAIN_OF_CUSTODY], coc_t),
        ),
        definition("validExhibitIds", list_t(STR), strings(exhibit_ids)),
        field_of_each("hohfeldIds", hoh_t, "id"),
        field_of_each("legalRuleIds", rule_t, "id"),
        field_of_each("superiorityIds", sup_t, "id"),
        field_of_each("supSuperiorIds", sup_t, "superiorRuleId"),
        field_of_each("supInferiorIds", sup_t, "inferiorRuleId"),
        field_of_each("aknIds", akn_t, "id"),
        field_of_each("aknWorkUris", akn_t, "workUri"),
        field_of_each("cocIds", coc_t, "id"),
        field_of_each("cocExhibitIds", coc_t, "exhibitId"),
        holds("hohfeldIdsDistinct", call("distinctStrings", call("hohfeldIds", call("hohfeldRelations")))),
        holds("legalRuleIdsDistinct", call("distinctStrings", call("legalRuleIds", call("legalRules")))),
        holds("superiorityIdsDistinct", call("distinctStrings", call("superiorityIds", call("superiorityOverrides")))),
        holds("superioritySuperiorRulesResolve", call("allMembers", call("supSuperiorIds", call("superiorityOverrides")), call("legalRuleIds", call("legalRules")))),
        holds("superiorityInferiorRulesResolve", call("allMembers", call("supInferiorIds", call("superiorityOverrides")), call("legalRuleIds", call("legalRules")))),
        holds("aknIdsDistinct", call("distinctStrings", call("aknIds", call("aknDocuments")))),
        holds("aknWorkUrisDistinct", call("distinctStrings", call("aknWorkUris", call("aknDocuments")))),
        holds("cocIdsDistinct", call("distinctStrings", call("cocIds", call("chainOfCustody")))),
        holds("cocExhibitsResolve", call("allMembers", call("cocExhibitIds", call("chainOfCustody")), call("validExhibitIds"))),
    ]


def render_module():
    return lexmod.module("LegalMeta", declarations())


def render_toml():
    lines = ['spec = "prism-legal/legal-meta/1"', ""]
    for r in HOHFELD_RELATIONS:
        lines += ["[[hohfeld]]", f'id = {json.dumps(r["id"])}', f'title = {json.dumps(r["title"])}', f'dominant_position = {json.dumps(r["dominantPosition"])}', f'correlative_position = {json.dumps(r["correlativePosition"])}', ""]
    for r in LEGAL_RULES:
        lines += ["[[legal_rule]]", f'id = {json.dumps(r["id"])}', f'strength = {json.dumps(r["strength"])}', f'modality = {json.dumps(r["deonticModality"])}', ""]
    for s_ov in SUPERIORITY_OVERRIDES:
        lines += ["[[superiority]]", f'id = {json.dumps(s_ov["id"])}', f'superior = {json.dumps(s_ov["superiorRuleId"])}', f'inferior = {json.dumps(s_ov["inferiorRuleId"])}', ""]
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
    return {
        "module": "src/LegalMeta.lex.tex",
        "hohfeld": len(HOHFELD_RELATIONS),
        "rules": len(LEGAL_RULES),
        "attacks": len(ATTACKS),
        "akn": len(AKN_DOCUMENTS),
        "coc": len(CHAIN_OF_CUSTODY),
        "changed": changed,
    }


def check():
    if not MODULE.exists() or MODULE.read_text() != render_module():
        return {"ok": False, "reason": "src/LegalMeta.lex.tex drifted; run `bin/prism-legal api sync`"}
    if not REGISTER.exists() or REGISTER.read_text() != render_toml():
        return {"ok": False, "reason": "model/legal-meta.toml drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}

