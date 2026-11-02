"""ISO/IEC/IEEE 42010 & 25010 Architecture Model (`src/Architecture.lex.tex`) for PrismLegal."""

from . import ROOT, lexmod
from .semantic import (
    BOOL,
    NAT,
    STR,
    all_members,
    b,
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
    strings,
    structure,
    var,
)

MODULE = ROOT / "src" / "Architecture.lex.tex"

STAKEHOLDERS = [
    {"id": "SH-CLIENT", "name": "Client & Witness-Stand Litigant", "role": "Primary Portal User (Client Workspace)", "concerns": ["CON-STRATEGY", "CON-TESTIMONY", "CON-PRIVACY", "CON-SHARING"]},
    {"id": "SH-LAWYER", "name": "Lead Trial Counsel, Co-Counsel & Legal Aid Clinic", "role": "Primary Portal User (Counsel Workbench)", "concerns": ["CON-STRATEGY", "CON-PROOF", "CON-IMPEACHMENT", "CON-CLOCK", "CON-SHARING"]},
    {"id": "SH-BENEFICIARIES", "name": "Protected Minor Beneficiaries & Dependents (Ages 15, 11 & 6)", "role": "Statutory Best-Interests & Remedy Subjects", "concerns": ["CON-STABILITY", "CON-REMEDIES"]},
    {"id": "SH-COURT", "name": "Presiding Judicial Fact-Finder & Administrative Tribunal", "role": "Adjudicative Forum", "concerns": ["CON-PROOF", "CON-CLOCK", "CON-STABILITY"]},
    {"id": "SH-COUNTERPARTY", "name": "Opposing Party & Adverse Counsel", "role": "Adversarial Counterparty", "concerns": ["CON-IMPEACHMENT", "CON-REMEDIES"]},
]

CONCERNS = [
    {"id": "CON-STRATEGY", "title": "Coherent Case Theory & Client-Counsel Alignment", "isoCharacteristic": "Functional Suitability"},
    {"id": "CON-TESTIMONY", "title": "Calm, Record-Anchored Direct & Cross-Examination Testimony", "isoCharacteristic": "Usability / Operability"},
    {"id": "CON-PROOF", "title": "Complete Statutory & Evidentiary Backing of All Claims", "isoCharacteristic": "Reliability"},
    {"id": "CON-IMPEACHMENT", "title": "Documentary Impeachment & Rule 106 Completeness", "isoCharacteristic": "Functional Appropriateness"},
    {"id": "CON-STABILITY", "title": "Protected Beneficiary Stability & Equal Schedule Continuity", "isoCharacteristic": "Safety / Best Interests"},
    {"id": "CON-REMEDIES", "title": "Accurate Guideline Support, Damages & Statutory Benefit Protection", "isoCharacteristic": "Functional Correctness"},
    {"id": "CON-CLOCK", "title": "Homeostatic 360-Minute Hearing Clock Regulation", "isoCharacteristic": "Performance Efficiency"},
    {"id": "CON-PRIVACY", "title": "Zero-PII Public-Benefit Sanitization & Local-First Privilege", "isoCharacteristic": "Security / Confidentiality"},
    {"id": "CON-SHARING", "title": "Cryptographic Multi-Party Case Sharing & Unbundled Co-Counsel Access", "isoCharacteristic": "Interoperability / Security"},
]

VIEWPOINTS = [
    {"id": "VP-PORTAL-HUB", "title": "Platform Hub, Auth & Multi-Domain Registry Viewpoint", "concerns": ["CON-PRIVACY", "CON-SHARING", "CON-STRATEGY"]},
    {"id": "VP-CLIENT-PREP", "title": "Client Strategy, Direct Walkthrough & Rehearsal Viewpoint", "concerns": ["CON-STRATEGY", "CON-TESTIMONY", "CON-STABILITY", "CON-SHARING"]},
    {"id": "VP-COUNSEL-BENCH", "title": "Counsel Statutory Proof, Impeachment & Remedies Viewpoint", "concerns": ["CON-PROOF", "CON-IMPEACHMENT", "CON-REMEDIES"]},
    {"id": "VP-COUNSEL-EXAMS", "title": "Counsel Witness Examinations, Objections & Vault Viewpoint", "concerns": ["CON-TESTIMONY", "CON-IMPEACHMENT", "CON-CLOCK"]},
    {"id": "VP-COUNSEL-TUNER", "title": "Counsel Formal Legal Meta-Theory & Strategy Tuner Viewpoint", "concerns": ["CON-STRATEGY", "CON-PROOF", "CON-CLOCK"]},
    {"id": "VP-COURTROOM-STAND", "title": "Day-of-Hearing Quick Responder Viewpoint", "concerns": ["CON-TESTIMONY", "CON-PROOF", "CON-CLOCK"]},
]

VIEWS = [
    {"id": "VIEW-INDEX", "viewpointId": "VP-PORTAL-HUB", "route": "index.html", "title": "Platform Hub, Login, Firms, Courts & Case Sharing"},
    {"id": "VIEW-CLIENT", "viewpointId": "VP-CLIENT-PREP", "route": "client.html", "title": "Client Workspace (4-Step Preparation & Rehearsal)"},
    {"id": "VIEW-LAWYER", "viewpointId": "VP-COUNSEL-BENCH", "route": "lawyer.html", "title": "Counsel Workbench (5-Workspace Legal Practice & Tuner)"},
    {"id": "VIEW-COURTROOM", "viewpointId": "VP-COURTROOM-STAND", "route": "courtroom.html", "title": "Hearing & Trial Mode (High-Legibility Quick Reference)"},
]

MEASURES = [
    {"id": "QM-01", "name": "Claim Evidentiary Backing Ratio", "characteristic": "Reliability", "target": "100% (24/24 claims)"},
    {"id": "QM-02", "name": "Cross-Examination Rebuttal Coverage", "characteristic": "Functional Completeness", "target": "100% (16/16 traps)"},
    {"id": "QM-03", "name": "Exhibit Semantic & Intent Mapping Coverage", "characteristic": "Functional Correctness", "target": "100% (30/30 exhibits)"},
    {"id": "QM-04", "name": "WCAG 2.2 AA Contrast Compliance", "characteristic": "Accessibility", "target": ">= 4.5:1 across light & dark themes"},
    {"id": "QM-05", "name": "Zero-PII Sanitization Verification", "characteristic": "Security", "target": "0 private tokens across repository"},
]

TRIAL_RISKS = [
    {"id": "RISK-01", "title": "Adversarial Baiting on Pre-Separation Stress", "mitigation": "Anchor in OS-1 humility, 9 incident-free post-separation months, and Ex-M early seminar completion."},
    {"id": "RISK-02", "title": "Speculative Income Imputation on Retired Pensioner", "mitigation": "Invoke Uniform Support Guidelines § 305(5)(b) disability exemption and Ex-D certified IRS transcripts ($0 curriculum draw)."},
    {"id": "RISK-03", "title": "Out-of-Context Quotes from 2028-2029 Homework Study Log", "mitigation": "Invoke FRE 106 Rule of Completeness on OP-Ex-13 p. 6 lines 15-28 (collaborative study & positive reinforcement checklist)."},
    {"id": "RISK-04", "title": "Hearing Clock Exhaustion Before Financial Impeachment", "mitigation": "Enforce 360-minute homeostatic stage budgets reserving 60 minutes for closing and final orders."},
]

TUNING_PARAMETERS = [
    {"id": "TUNE-01", "name": "Client Flashcard Readiness Status", "title": "Client Flashcard Readiness Status", "owner": "Client Litigant (Respondent)", "collaborator": "Lead Trial Counsel", "targetModule": "src/Audit.lex.tex", "scope": "TRAP-01..TRAP-16", "description": "Interactive witness-stand readiness tracking across all 16 cross-examination flashcards."},
    {"id": "TUNE-02", "name": "Witness Examination Minute Allocation", "title": "Witness Examination Minute Allocation", "owner": "Lead Trial Counsel", "collaborator": "Client Litigant (Respondent)", "targetModule": "src/Engine.lex.tex", "scope": "W-01..W-10 (360-min ceiling)", "description": "Homeostatic 360-minute trial clock budgeting across all 10 witnesses and 5 hearing stages."},
    {"id": "TUNE-03", "name": "Claim Evidentiary Status & Framing", "title": "Claim Evidentiary Status & Framing", "owner": "Lead Trial Counsel", "collaborator": "Specialized Co-Counsel", "targetModule": "src/Register.lex.tex", "scope": "CLM-01..CLM-24", "description": "Stipulated vs. corroborated status and statutory framing across all 24 evidentiary claims."},
    {"id": "TUNE-04", "name": "Client-Counsel Co-Design Strategy Agenda", "title": "Client-Counsel Co-Design Strategy Agenda", "owner": "Client Litigant (Respondent)", "collaborator": "Lead Trial Counsel", "targetModule": "model/tuning.json", "scope": "AGENDA-01..N", "description": "Shared client-counsel strategy questions, exhibit sequencing notes, and direct-exam alignment."},
    {"id": "TUNE-05", "name": "Active Matter & Practice Area Context", "title": "Active Matter & Practice Area Context", "owner": "Platform Hub", "collaborator": "All Portal Roles", "targetModule": "src/Portal.lex.tex", "scope": "CASE-2030-*", "description": "Multi-domain matter switcher across Family Law, Statutory Benefits, Entity Governance, Employment, UCC, and Housing."},
    {"id": "TUNE-06", "name": "Cryptographic Case Sharing Grants", "title": "Cryptographic Case Sharing Grants", "owner": "Client Litigant (Respondent)", "collaborator": "Firm & Clinic Counsel", "targetModule": "src/Portal.lex.tex", "scope": "SHARE-01..N", "description": "End-to-end encrypted, revocable, least-privilege capability grants for co-counsel and legal aid clinics."},
    {"id": "TUNE-07", "name": "Courtroom Large-Text & Theme Mode", "title": "Courtroom Large-Text & Theme Mode", "owner": "All Portal Roles", "collaborator": "WCAG 2.2 AA Design System", "targetModule": "src/Presentation.lex.tex", "scope": "UI Accessibility State", "description": "Light/dark theme toggle and witness-stand high-legibility typography scaling."},
]


def declarations():
    sh_t = named("Stakeholder")
    con_t = named("Concern")
    vp_t = named("Viewpoint")
    vw_t = named("ArchView")
    return [
        structure("Stakeholder", [("id", STR), ("name", STR), ("role", STR), ("concerns", list_t(STR))]),
        structure("Concern", [("id", STR), ("title", STR), ("isoCharacteristic", STR)]),
        structure("Viewpoint", [("id", STR), ("title", STR), ("concerns", list_t(STR))]),
        structure("ArchView", [("id", STR), ("viewpointId", STR), ("route", STR), ("title", STR)]),
        member_string(),
        all_members(),
        distinct_strings(),
        definition(
            "stakeholders",
            list_t(sh_t),
            lst([record("Stakeholder", id=s(x["id"]), name=s(x["name"]), role=s(x["role"]), concerns=strings(x["concerns"])) for x in STAKEHOLDERS], sh_t),
        ),
        definition(
            "concerns",
            list_t(con_t),
            lst([record("Concern", id=s(x["id"]), title=s(x["title"]), isoCharacteristic=s(x["isoCharacteristic"])) for x in CONCERNS], con_t),
        ),
        definition(
            "viewpoints",
            list_t(vp_t),
            lst([record("Viewpoint", id=s(x["id"]), title=s(x["title"]), concerns=strings(x["concerns"])) for x in VIEWPOINTS], vp_t),
        ),
        definition(
            "views",
            list_t(vw_t),
            lst([record("ArchView", id=s(x["id"]), viewpointId=s(x["viewpointId"]), route=s(x["route"]), title=s(x["title"])) for x in VIEWS], vw_t),
        ),
        field_of_each("stakeholderIds", sh_t, "id"),
        field_of_each("concernIds", con_t, "id"),
        field_of_each("viewpointIds", vp_t, "id"),
        field_of_each("viewIds", vw_t, "id"),
        field_of_each("viewViewpointIds", vw_t, "viewpointId"),
        holds("stakeholderIdsDistinct", call("distinctStrings", call("stakeholderIds", call("stakeholders")))),
        holds("concernIdsDistinct", call("distinctStrings", call("concernIds", call("concerns")))),
        holds("viewpointIdsDistinct", call("distinctStrings", call("viewpointIds", call("viewpoints")))),
        holds("viewIdsDistinct", call("distinctStrings", call("viewIds", call("views")))),
        holds("viewsResolveToViewpoints", call("allMembers", call("viewViewpointIds", call("views")), call("viewpointIds", call("viewpoints")))),
    ]


def render_module():
    return lexmod.module("Architecture", declarations(), glossaries=["prism.arch@1.0.0", "prism.qual@1.0.0"])


def sync():
    MODULE.parent.mkdir(parents=True, exist_ok=True)
    m = render_module()
    changed = not MODULE.exists() or MODULE.read_text() != m
    if changed:
        MODULE.write_text(m)
    return {
        "module": "src/Architecture.lex.tex",
        "stakeholders": len(STAKEHOLDERS),
        "concerns": len(CONCERNS),
        "viewpoints": len(VIEWPOINTS),
        "risks": len(TRIAL_RISKS),
        "tuningParams": len(TUNING_PARAMETERS),
        "tuningParameters": len(TUNING_PARAMETERS),
        "changed": changed,
    }


def check():
    if not MODULE.exists() or MODULE.read_text() != render_module():
        return {"ok": False, "reason": "src/Architecture.lex.tex drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}
