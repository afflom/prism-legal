"""Cross-examination trap audit & Opening-Statement-aligned pivot matrix
(`src/Audit.lex.tex` and `model/audit.toml`) for PrismLegal."""

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

REGISTER = ROOT / "model" / "audit.toml"
MODULE = ROOT / "src" / "Audit.lex.tex"

TRAPS = [
    {
        "id": "TRAP-01",
        "title": "Pre-Separation Household Disagreements & Audio Clips (Spring 2029)",
        "statutoryAnchor": "Uniform Best-Interests § 402(a)(5)-(6) & FRE 106",
        "pillarId": "OS-1",
        "allegation": "Opposing counsel plays curated audio clips (OP-Ex-10) from Spring 2029 household disagreements to allege tension.",
        "trapWarning": "Do not argue over who started the 2029 disagreement or accuse the opposing party of baiting you.",
        "openingAlignedPivot": "I take full responsibility for my share of pre-separation household stress; since separating nine months ago we have had zero incidents, and I completed the Collaborative Seminar 30 days ahead of schedule (Ex-M, Ex-O).",
        "opposingExhibits": ["OP-Ex-10"],
        "rebuttalExhibits": ["Ex-K", "Ex-M", "Ex-O"],
    },
    {
        "id": "TRAP-02",
        "title": "Dismissed Interim Administrative Petition (Oct 2029)",
        "statutoryAnchor": "State Protection Statute & Uniform § 402(b)",
        "pillarId": "OS-4",
        "allegation": "Opposing counsel cites the ex parte Oct 2029 interim petition (OP-Ex-08) to oppose joint decision-making.",
        "trapWarning": "Do not relitigate the unsworn ex parte allegations line by line.",
        "openingAlignedPivot": "That interim petition was dismissed by joint stipulation on November 18, 2029 with zero findings (Ex-J), and we have had nine incident-free months of structured co-parenting since.",
        "opposingExhibits": ["OP-Ex-08"],
        "rebuttalExhibits": ["Ex-A", "Ex-J", "Ex-O"],
    },
    {
        "id": "TRAP-03",
        "title": "Alleged School Transit Corridor Proximity & Telemetry Log",
        "statutoryAnchor": "FRE 901(b)(9) & State Protection Statute",
        "pillarId": "OS-4",
        "allegation": "Opposing counsel cites municipal dispatch log OP-Ex-09 claiming Respondent drove near the school buffer zone.",
        "trapWarning": "Do not guess distances from memory; rely strictly on the verified telemetry log.",
        "openingAlignedPivot": "Verified transit telemetry (Ex-A) proves I remained 512 yards away on the public arterial boulevard and complied strictly with the 500-yard buffer.",
        "opposingExhibits": ["OP-Ex-09"],
        "rebuttalExhibits": ["Ex-A", "Ex-J"],
    },
    {
        "id": "TRAP-04",
        "title": "Speculative $14,000/mo Income Imputation on Retired Pensioner",
        "statutoryAnchor": "Uniform Support Guidelines § 305(5)(b)",
        "pillarId": "OS-5",
        "allegation": "Opposing counsel argues Respondent should be imputed $9,000/mo in consulting wages on top of $5,000/mo disability pension (OP-Ex-02).",
        "trapWarning": "Do not debate hypothetical consulting rates from 2026.",
        "openingAlignedPivot": "As the Court recognized at Temporary Orders (Ex-N ¶ 15), I have a certified full disability retirement determination (Ex-E), and the guidelines prohibit imputing speculative wages on top of verified disability benefits.",
        "opposingExhibits": ["OP-Ex-02", "OP-Ex-07"],
        "rebuttalExhibits": ["Ex-D", "Ex-E", "Ex-F", "Ex-N"],
    },
    {
        "id": "TRAP-05",
        "title": "Unpaid Civic Curriculum Research Mischaracterized as Commercial Consulting",
        "statutoryAnchor": "IRC § 61 & Support Guidelines § 305",
        "pillarId": "OS-3",
        "allegation": "Opposing counsel points to public-interest educational repositories (OP-Ex-06) as proof of commercial consulting revenue.",
        "trapWarning": "Do not get drawn into technical jargon; anchor in the IRS transcripts.",
        "openingAlignedPivot": "Certified IRS transcripts from 2026 through 2029 (Ex-C, Ex-D) confirm $0.00 in consulting revenue, wages, or distributions; self-paced civic writing at home leaves me 100% available for all three minor children.",
        "opposingExhibits": ["OP-Ex-06"],
        "rebuttalExhibits": ["Ex-C", "Ex-D", "Ex-E"],
    },
    {
        "id": "TRAP-06",
        "title": "Retroactive Nov 2029–May 2030 Expense Demand vs. $30,000.00 Escrow Omission",
        "statutoryAnchor": "FRCP 26(e) / Mandatory Disclosure Rule 16.2(e)(10)",
        "pillarId": "OS-6",
        "allegation": "Opposing counsel demands retroactive household reimbursement under the Nov 2029 interim stipulation (OP-Ex-12).",
        "trapWarning": "Do not sound angry; let the Court's Temporary Orders ruling speak for itself.",
        "openingAlignedPivot": "At Temporary Orders (Ex-N ¶¶ 24-26), the Court held that stipulation unconscionable because $30,000.00 in escrow accounts (Ex-H) had been omitted from the initial Sworn Financial Statement (Ex-G).",
        "opposingExhibits": ["OP-Ex-12", "OP-Ex-03"],
        "rebuttalExhibits": ["Ex-G", "Ex-H", "Ex-J", "Ex-N"],
    },
    {
        "id": "TRAP-07",
        "title": "Commercial $2,400/mo After-School Agency Demand vs. Free Parental Care",
        "statutoryAnchor": "Uniform Support Guidelines § 305(9) & § 402(a)",
        "pillarId": "OS-3",
        "allegation": "Opposing counsel demands $900/mo child support add-on for a $2,400/mo commercial tutoring/care agency (OP-Ex-04).",
        "trapWarning": "Do not criticize Petitioner's regional travel schedule; frame your availability as a resource for both parents.",
        "openingAlignedPivot": "Because of my retirement schedule, I am available full-time to care for the three children during every regional travel week for $0, rather than placing them with a commercial agency.",
        "opposingExhibits": ["OP-Ex-04"],
        "rebuttalExhibits": ["Ex-E", "Ex-L", "Ex-N"],
    },
    {
        "id": "TRAP-08",
        "title": "Duplicate $320/mo Medical Insurance Add-On vs. Zero-Premium Statutory Plan",
        "statutoryAnchor": "38 U.S.C. § 1781 & Support Guidelines § 305(10)",
        "pillarId": "OS-5",
        "allegation": "Opposing counsel includes a $320/mo medical insurance add-on on OP-Ex-02.",
        "trapWarning": "Keep the explanation simple and statutory.",
        "openingAlignedPivot": "Through my statutory retirement benefit package, all three minor children have comprehensive medical and dental coverage at $0 monthly premium (Ex-E, Ex-N).",
        "opposingExhibits": ["OP-Ex-02"],
        "rebuttalExhibits": ["Ex-E", "Ex-N"],
    },
    {
        "id": "TRAP-09",
        "title": "Attack on 50/50 2-2-5-5 Schedule (90-Overnight Restriction)",
        "statutoryAnchor": "Uniform Best-Interests § 402(a)(1), (4)",
        "pillarId": "OS-2",
        "allegation": "Opposing counsel claims equal 50/50 time is disruptive and proposes restricting Respondent to 90 overnights/year (OP-Ex-01).",
        "trapWarning": "Do not become defensive; point to the Temporary Orders ruling and the 90-day track record.",
        "openingAlignedPivot": "Temporary Orders found zero basis to restrict my parenting time (Ex-N ¶ 8), and we successfully practiced equal 50/50 parenting time for 90 days in Summer 2030.",
        "opposingExhibits": ["OP-Ex-01"],
        "rebuttalExhibits": ["Ex-I", "Ex-L", "Ex-N", "Ex-O"],
    },
    {
        "id": "TRAP-10",
        "title": "Wednesday School Exchange Logistics & Calendar Notes",
        "statutoryAnchor": "Uniform Best-Interests § 402(a)(4), (8)",
        "pillarId": "OS-5",
        "allegation": "Opposing counsel cites calendar notes (OP-Ex-11) to claim mid-week exchanges cause confusion.",
        "trapWarning": "Agree that clear rules are helpful and pivot to Ex-L.",
        "openingAlignedPivot": "That is exactly why our proposed Parenting Plan (Ex-L) uses a bright-line Wednesday school drop-off and pick-up exchange, eliminating doorstep transitions.",
        "opposingExhibits": ["OP-Ex-11"],
        "rebuttalExhibits": ["Ex-L", "Ex-O"],
    },
    {
        "id": "TRAP-11",
        "title": "Selective Co-Parenting Message Excerpts (180-Page Export)",
        "statutoryAnchor": "FRE 106 (Completeness) & Uniform § 402(a)(6)",
        "pillarId": "OS-4",
        "allegation": "Opposing counsel reads isolated tense messages from late 2029 out of OP-Ex-05.",
        "trapWarning": "Request the full thread context calmly.",
        "openingAlignedPivot": "Looking at the complete co-parenting log (Ex-O) over the past nine months, our communications have been polite, logistical, and focused on the three children.",
        "opposingExhibits": ["OP-Ex-05"],
        "rebuttalExhibits": ["Ex-O", "Ex-M"],
    },
    {
        "id": "TRAP-12",
        "title": "Cherry-Picked 2028 Homework Study Log Line (FRE 106 Completeness)",
        "statutoryAnchor": "FRE 106 & Uniform Best-Interests § 402(a)(5)",
        "pillarId": "OS-1",
        "allegation": "Opposing counsel reads a single sentence from page 6 of the 2028-2029 study log (OP-Ex-13) regarding screen-time limits.",
        "trapWarning": "Do not deny writing the study log; immediately read lines 15-28 on the exact same page.",
        "openingAlignedPivot": "Under the Rule of Completeness, lines 15 through 28 on that exact same page from October 14, 2028 record our collaborative study routine and positive reinforcement checklist.",
        "opposingExhibits": ["OP-Ex-13"],
        "rebuttalExhibits": ["Ex-I", "Ex-M"],
    },
    {
        "id": "TRAP-13",
        "title": "Occupational Fatigue Rating Mischaracterized Against Parenting",
        "statutoryAnchor": "38 C.F.R. § 4.130 & Uniform § 402(a)(5)",
        "pillarId": "OS-3",
        "allegation": "Opposing counsel argues Respondent's disability retirement rating impairs parenting capacity.",
        "trapWarning": "Distinguish high-travel corporate consulting from structured home parenting.",
        "openingAlignedPivot": "My retirement rating reflects commercial travel environments (Ex-N ¶ 15); at home, I have cared for our three children safely and consistently for ten years (Ex-E, Ex-I).",
        "opposingExhibits": ["OP-Ex-07"],
        "rebuttalExhibits": ["Ex-E", "Ex-I", "Ex-M", "Ex-N"],
    },
    {
        "id": "TRAP-14",
        "title": "Youth Text Messages with Oldest Minor Child (Age 15)",
        "statutoryAnchor": "Uniform Best-Interests § 402(a)(2) & § 404",
        "pillarId": "OS-6",
        "allegation": "Opposing counsel claims Respondent improperly discussed parenting schedules with the 15-year-old child in OP-Ex-14.",
        "trapWarning": "Point to the full message thread showing you reassured the child and redirected adult topics.",
        "openingAlignedPivot": "The complete message thread shows our oldest child asking about robotics club pickup and me reassuring our child that both parents support their activities while keeping schedule logistics between the adults.",
        "opposingExhibits": ["OP-Ex-14"],
        "rebuttalExhibits": ["Ex-I", "Ex-L"],
    },
    {
        "id": "TRAP-15",
        "title": "Neighbor Testimony Lacking Post-Separation Personal Knowledge",
        "statutoryAnchor": "FRE 602 (Personal Knowledge) & FRE 802",
        "pillarId": "OS-2",
        "allegation": "Former neighbors offer opinions on Respondent's townhouse without having visited the residence.",
        "trapWarning": "Let counsel handle the FRE 602 objection; stay calm and factual.",
        "openingAlignedPivot": "Those witnesses have never visited our townhouse; the photographs (Ex-I, Ex-K) and first-hand observations from our local community witnesses confirm the children's safe, structured routine.",
        "opposingExhibits": ["OP-Ex-15"],
        "rebuttalExhibits": ["Ex-I", "Ex-K"],
    },
    {
        "id": "TRAP-16",
        "title": "Townhouse Living Arrangement & Long-Term School District Stability",
        "statutoryAnchor": "Uniform Best-Interests § 402(a)(3), (4)",
        "pillarId": "OS-3",
        "allegation": "Opposing counsel questions whether residing in the three-bedroom townhouse is temporary.",
        "trapWarning": "Emphasize the multi-bedroom layout, study space, and neighborhood stability.",
        "openingAlignedPivot": "The townhouse provides dedicated bedrooms, quiet study desks, courtyard access, and supportive neighbors 8 minutes from school (Ex-I), giving all three minor children lasting stability.",
        "opposingExhibits": ["OP-Ex-01"],
        "rebuttalExhibits": ["Ex-I", "Ex-K", "Ex-L"],
    },
]

for _t in TRAPS:
    _t.setdefault("status", "neutralized")
    _t.setdefault("category", f"Pillar {_t['pillarId']} Rebuttal")



def declarations():
    trap_t = named("CrossExamTrap")
    exhibit_ids = [e["id"] for e in casemodel.all_exhibits()]
    pillar_ids = [p["id"] for p in casemodel.OPENING_PILLARS]

    return [
        structure(
            "CrossExamTrap",
            [
                ("id", STR),
                ("title", STR),
                ("statutoryAnchor", STR),
                ("pillarId", STR),
                ("openingAlignedPivot", STR),
                ("rebuttalExhibits", list_t(STR)),
            ],
        ),
        member_string(),
        all_members(),
        distinct_strings(),
        definition(
            "traps",
            list_t(trap_t),
            lst(
                [
                    record(
                        "CrossExamTrap",
                        id=s(t["id"]),
                        title=s(t["title"]),
                        statutoryAnchor=s(t["statutoryAnchor"]),
                        pillarId=s(t["pillarId"]),
                        openingAlignedPivot=s(t["openingAlignedPivot"]),
                        rebuttalExhibits=strings(t["rebuttalExhibits"]),
                    )
                    for t in TRAPS
                ],
                trap_t,
            ),
        ),
        field_of_each("trapIds", trap_t, "id"),
        field_of_each("trapPillarIds", trap_t, "pillarId"),
        definition("validPillarIds", list_t(STR), strings(pillar_ids)),
        definition("validExhibitIds", list_t(STR), strings(exhibit_ids)),
        definition(
            "rebuttalsResolve",
            BOOL,
            match_list(
                var("xs"),
                b(True),
                "head",
                "tail",
                if_(
                    call("allMembers", proj(var("head"), "rebuttalExhibits"), var("exIds")),
                    call("rebuttalsResolve", var("tail"), var("exIds")),
                    b(False),
                ),
            ),
            parameters=[("xs", list_t(trap_t)), ("exIds", list_t(STR))],
            recursive="xs",
        ),
        holds("auditTrapIdsDistinct", call("distinctStrings", call("trapIds", call("traps")))),
        holds("auditEveryTrapHasOpeningPivot", call("allMembers", call("trapPillarIds", call("traps")), call("validPillarIds"))),
        holds("auditRebuttalExhibitsResolve", call("rebuttalsResolve", call("traps"), call("validExhibitIds"))),
    ]


def render_module():
    return lexmod.module("Audit", declarations())


def render_toml():
    lines = ['spec = "prism-legal/audit/1"', ""]
    for t in TRAPS:
        lines += [
            "[[trap]]",
            f'id = {json.dumps(t["id"])}',
            f'title = {json.dumps(t["title"])}',
            f'statutory_anchor = {json.dumps(t["statutoryAnchor"])}',
            f'pillar_id = {json.dumps(t["pillarId"])}',
            f'opening_aligned_pivot = {json.dumps(t["openingAlignedPivot"])}',
            f'rebuttal_exhibits = {json.dumps(t["rebuttalExhibits"])}',
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
    return {"module": "src/Audit.lex.tex", "traps": len(TRAPS), "changed": changed}


def check():
    if not MODULE.exists() or MODULE.read_text() != render_module():
        return {"ok": False, "reason": "src/Audit.lex.tex drifted; run `bin/prism-legal api sync`"}
    if not REGISTER.exists() or REGISTER.read_text() != render_toml():
        return {"ok": False, "reason": "model/audit.toml drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}
