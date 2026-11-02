"""Handwritten, Visual & 30-Exhibit Content-Meaning / Proponent-Intent Model
(`src/VisualEvidence.lex.tex` and `model/visual-evidence.toml`) for PrismLegal.

Lowers:
1. Handwritten journal entries (`DIARY-01`..`DIARY-08`) with FRE 106 completeness rebuttals
2. Scanned/visual exhibit forensic extractions (`VIS-01`..`VIS-12`)
3. Photographic page-by-page catalog (`PHOTO-01`..`PHOTO-12`)
4. Complete 30-Exhibit Content-Meaning & Proponent-Intent Matrix (`MAP-Ex-A`..`MAP-OP-Ex-15`)
   with Lean 4 kernel theorem `everyRegisterExhibitHasSemanticAndIntentMapping`."""

import json
from . import ROOT, casemodel, lexmod
from .semantic import (
    BOOL,
    NAT,
    STR,
    add,
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
    n,
    named,
    proj,
    record,
    s,
    strings,
    structure,
    theorem,
    var,
)

REGISTER = ROOT / "model" / "visual-evidence.toml"
MODULE = ROOT / "src" / "VisualEvidence.lex.tex"

HANDWRITTEN_DIARY_ENTRIES = [
    {"id": "DIARY-01", "exhibitId": "OP-Ex-13", "entryDate": "2028-09-10", "pageRange": "pp. 1-2", "handwrittenExcerpt": "Reflecting on balancing project travel with caring for our older children and preschooler; grateful for household teamwork.", "motherCherryPick": "Attempts to portray early project fatigue as household detachment.", "fullContextRebuttal": "FRE 106 full page shows loving commitment to morning routines and family stability."},
    {"id": "DIARY-02", "exhibitId": "OP-Ex-13", "entryDate": "2028-09-24", "pageRange": "pp. 3-5", "handwrittenExcerpt": "Discussing savings plan so Petitioner can complete professional fellowship debt-free.", "motherCherryPick": "Omitted by Petitioner.", "fullContextRebuttal": "Corroborates OS-2 shared sacrifice and joint planning for graduate credentials."},
    {"id": "DIARY-03", "exhibitId": "OP-Ex-13", "entryDate": "2028-10-14 (Lines 1-14)", "pageRange": "p. 6, ll. 1-14", "handwrittenExcerpt": "Initial reflection on structured homework schedules vs. flexible evening screen-time rules.", "motherCherryPick": "Reads only lines 4-8 out of context to allege rigid study expectations.", "fullContextRebuttal": "Immediately refuted by lines 15-28 on the exact same page (DIARY-04) under FRE 106."},
    {"id": "DIARY-04", "exhibitId": "OP-Ex-13", "entryDate": "2028-10-14 (Lines 15-28)", "pageRange": "p. 6, ll. 15-28", "handwrittenExcerpt": "We agreed that positive reinforcement, collaborative study breaks, and patient explanation always come first.", "motherCherryPick": "Concealed by opposing counsel's selective quote.", "fullContextRebuttal": "FRE 106 completeness rebuttal: proves Respondent committed to patient, positive study habits."},
    {"id": "DIARY-05", "exhibitId": "OP-Ex-13", "entryDate": "2028-11-18", "pageRange": "pp. 7-10", "handwrittenExcerpt": "First month of disability retirement; walking the children to the neighborhood park every afternoon.", "motherCherryPick": "Omitted by Petitioner.", "fullContextRebuttal": "Proves hands-on daily caregiving immediately upon November 2028 retirement."},
    {"id": "DIARY-06", "exhibitId": "OP-Ex-13", "entryDate": "2029-01-15", "pageRange": "pp. 11-13", "handwrittenExcerpt": "Organizing the children's school carpool, robotics club schedule, and bedtime reading.", "motherCherryPick": "Omitted by Petitioner.", "fullContextRebuttal": "Documents deep emotional bond and organized daily routine with all three children."},
    {"id": "DIARY-07", "exhibitId": "OP-Ex-13", "entryDate": "2029-03-08", "pageRange": "pp. 14-17", "handwrittenExcerpt": "Solo parenting week during Petitioner's regional seminar; cooked meals, robotics project with our oldest child, dental checkups.", "motherCherryPick": "Omitted by Petitioner.", "fullContextRebuttal": "Demonstrates seamless solo caregiving across medical and educational routines."},
    {"id": "DIARY-08", "exhibitId": "OP-Ex-13", "entryDate": "2029-06-12", "pageRange": "pp. 18-21", "handwrittenExcerpt": "Gratitude for all three children and commitment to always putting their peace and education first.", "motherCherryPick": "Omitted by Petitioner.", "fullContextRebuttal": "Closes the 21-page study log on a theme of patience and child-focused devotion."},
]

VISUAL_FORENSIC_RECORDS = [
    {"id": "VIS-01", "exhibitId": "Ex-A", "modality": "Digital Transit Telemetry Map", "pageCount": 4, "handwrittenDetails": "Timestamped coordinate pins showing 512-yard minimum separation on public arterial boulevard.", "evidentiarySignificance": "Refutes OP-Ex-09 proximity allegation with objective transit telemetry.", "trialPivot": "Admit in DX-021 and cross-examination of OP-Ex-09."},
    {"id": "VIS-02", "exhibitId": "Ex-E", "modality": "Official Retirement Board Decision", "pageCount": 8, "handwrittenDetails": "Highlighted p. 1 (Disability Retirement effective 11/12/2028) and p. 7 (38 U.S.C. § 1781 dependent medical eligibility).", "evidentiarySignificance": "Bars income imputation (§ 305(5)(b)) and eliminates $320/mo duplicate insurance add-on.", "trialPivot": "Admit in DX-010 and cite on support worksheet Ex-N."},
    {"id": "VIS-03", "exhibitId": "Ex-G", "modality": "Sworn Financial Statement (Initial)", "pageCount": 7, "handwrittenDetails": "Section 5 (Bank Accounts) lists only primary checking; omits Escrow Checking x4102 and Reserve Savings x4109.", "evidentiarySignificance": "Establishes material non-disclosure under FRCP 26(e) / Rule 16.2(e)(10).", "trialPivot": "Pair with Ex-H bank statements to defeat retroactive expense claim."},
    {"id": "VIS-04", "exhibitId": "Ex-H", "modality": "Subpoenaed Bank Statements", "pageCount": 18, "handwrittenDetails": "Ending balances on x4102 ($12,000.00) and x4109 ($18,000.00) totaling $30,000.00 during Ex-G/Ex-J period.", "evidentiarySignificance": "Documentary proof backing Temporary Orders unconscionability ruling (Ex-N ¶¶ 24-26).", "trialPivot": "Admit in DX-018 and cross-examination of W-02."},
    {"id": "VIS-05", "exhibitId": "Ex-I", "modality": "Photographic Compendium", "pageCount": 11, "handwrittenDetails": "Captioned photographs of townhouse exterior, the three children's bedrooms, study desks, and greenbelt courtyard.", "evidentiarySignificance": "Visual proof of safe, structured, joyful townhouse environment 8 minutes from school.", "trialPivot": "Walk through page-by-page in DX-025."},
    {"id": "VIS-06", "exhibitId": "Ex-K", "modality": "Multimedia & Activity Stills", "pageCount": 9, "handwrittenDetails": "Time-stamped video frames and outdoor robotics/music activities with all three children.", "evidentiarySignificance": "Corroborates calm parental demeanor and de-escalation.", "trialPivot": "Admit in DX-019."},
    {"id": "VIS-07", "exhibitId": "Ex-M", "modality": "Signed Completion Certificate", "pageCount": 1, "handwrittenDetails": "Instructor signature and verification seal dated August 15, 2030 (30 days prior to judicial deadline).", "evidentiarySignificance": "Proves proactive accountability and compliance with court orders.", "trialPivot": "Admit in DX-031."},
    {"id": "VIS-08", "exhibitId": "Ex-N", "modality": "Signed Court Order & Guideline Worksheet", "pageCount": 12, "handwrittenDetails": "Judicial findings at ¶ 8 (no basis to restrict time), ¶ 15 (disability retirement), ¶¶ 24-26 ($30,000.00 omission unconscionable), plus $250/mo worksheet.", "evidentiarySignificance": "Law-of-the-case anchor for Permanent Orders.", "trialPivot": "Admit in DX-034."},
    {"id": "VIS-09", "exhibitId": "OP-Ex-04", "modality": "Commercial Childcare Quote", "pageCount": 5, "handwrittenDetails": "Rate sheet showing $2,400/mo agency fee for after-school coverage.", "evidentiarySignificance": "Unnecessary expense when fit retired parent is available 100% of travel blocks for $0.", "trialPivot": "Rebut in DX-029 and TRAP-07."},
    {"id": "VIS-10", "exhibitId": "OP-Ex-11", "modality": "Handwritten Calendar Annotations", "pageCount": 3, "handwrittenDetails": "Color-coded margin notes showing confusion over non-school exchange times.", "evidentiarySignificance": "Demonstrates why Ex-L's bright-line Wednesday school exchange rule is superior.", "trialPivot": "Turn into affirmative proof for Ex-L § 2.3 in TRAP-10."},
    {"id": "VIS-11", "exhibitId": "OP-Ex-13", "modality": "Scanned Homework Study Log (2028-2029)", "pageCount": 21, "handwrittenDetails": "Entries across 21 pages; p. 6 ll. 15-28 explicitly records positive reinforcement checklist on 10/14/2028.", "evidentiarySignificance": "FRE 106 completeness neutralizes opposing cherry-pick.", "trialPivot": "Read p. 6 ll. 15-28 verbatim in DX-023 and TRAP-12."},
    {"id": "VIS-12", "exhibitId": "OP-Ex-14", "modality": "Youth Device Message Screenshots", "pageCount": 6, "handwrittenDetails": "Message bubbles showing the 15-year-old child asking about robotics club pickup and Respondent's supportive reassurance.", "evidentiarySignificance": "Corroborates mature beneficiary preference for equal 50/50 time under § 402(a)(2).", "trialPivot": "Cite full thread under FRE 106 in TRAP-14."},
]

for _v in VISUAL_FORENSIC_RECORDS:
    _v.setdefault("statutoryAnchor", "FRE 106 & Uniform Best-Interests Standard § 402")


PHOTO_PAGE_CATALOG = [
    {"id": "PHOTO-01", "exhibitId": "Ex-I", "pageNumber": 1, "subjects": "Townhouse Exterior & Courtyard Walkway", "setting": "Townhouse Greenbelt (8 min from schools)", "visualDescription": "Brick facade, landscaped courtyard path, and covered entry.", "statutoryFactorId": "SF-04"},
    {"id": "PHOTO-02", "exhibitId": "Ex-I", "pageNumber": 2, "subjects": "Living Room & Family Reading Area", "setting": "Townhouse Interior", "visualDescription": "Bright living space with bookshelves, board games, and family photos of the three children.", "statutoryFactorId": "SF-04"},
    {"id": "PHOTO-03", "exhibitId": "Ex-I", "pageNumber": 3, "subjects": "Kitchen & Family Dining Table", "setting": "Townhouse Interior", "visualDescription": "Full kitchen where Respondent prepares daily meals and weekly school lunches.", "statutoryFactorId": "SF-03"},
    {"id": "PHOTO-04", "exhibitId": "Ex-I", "pageNumber": 4, "subjects": "Oldest Minor Child's Bedroom & Study Desk (Age 15)", "setting": "Townhouse Bedroom 1", "visualDescription": "Dedicated desk, high-school robotics kits, textbooks, and personal decor.", "statutoryFactorId": "SF-02"},
    {"id": "PHOTO-05", "exhibitId": "Ex-I", "pageNumber": 5, "subjects": "Middle Minor Child's Bedroom & Music Corner (Age 11)", "setting": "Townhouse Bedroom 2", "visualDescription": "Music stand, middle-school science models, organized wardrobe, and reading lamp.", "statutoryFactorId": "SF-03"},
    {"id": "PHOTO-06", "exhibitId": "Ex-I", "pageNumber": 6, "subjects": "Youngest Minor Child's Bedroom & Reading Nook (Age 6)", "setting": "Townhouse Bedroom 3", "visualDescription": "Cozy bed, illustrated 1st-grade storybooks, and easel artwork.", "statutoryFactorId": "SF-03"},
    {"id": "PHOTO-07", "exhibitId": "Ex-I", "pageNumber": 7, "subjects": "Dedicated Homework & Music Alcove", "setting": "Townhouse Study", "visualDescription": "Quiet study table with acoustic guitar, keyboard, and school calendar.", "statutoryFactorId": "SF-04"},
    {"id": "PHOTO-08", "exhibitId": "Ex-I", "pageNumber": 8, "subjects": "Children's Courtyard Planter Project", "setting": "Townhouse Courtyard", "visualDescription": "All three children smiling while tending herb planters with Respondent.", "statutoryFactorId": "SF-03"},
    {"id": "PHOTO-09", "exhibitId": "Ex-I", "pageNumber": 9, "subjects": "Summer 2030 50/50 Bicycle & Park Outing", "setting": "Community Greenway", "visualDescription": "All three children in helmets riding bikes during the Summer 2030 50/50 schedule.", "statutoryFactorId": "SF-04"},
    {"id": "PHOTO-10", "exhibitId": "Ex-K", "pageNumber": 1, "subjects": "Family Board Game Night (2029)", "setting": "Family Living Room", "visualDescription": "Calm, joyful evening routine with all three children laughing together.", "statutoryFactorId": "SF-06"},
    {"id": "PHOTO-11", "exhibitId": "Ex-K", "pageNumber": 2, "subjects": "School Robotics & Science Fair Preparation", "setting": "Study Table", "visualDescription": "Respondent helping the two older children assemble project display boards.", "statutoryFactorId": "SF-07"},
    {"id": "PHOTO-12", "exhibitId": "Ex-K", "pageNumber": 3, "subjects": "Neighborhood Community Picnic Dinner", "setting": "Townhouse Dining Room", "visualDescription": "All three children sharing dinner with Respondent in a calm, structured routine.", "statutoryFactorId": "SF-03"},
]
PHOTO_PAGE_CATALOG[0]["setting"] = "Townhouse Greenbelt (8 min from schools)"

EXHIBIT_SEMANTIC_MAPPINGS = []
for e in casemodel.RESPONDENT_EXHIBITS:
    EXHIBIT_SEMANTIC_MAPPINGS.append(
        {
            "id": f"MAP-{e['id']}",
            "exhibitId": e["id"],
            "proponent": "Respondent",
            "modality": e["category"],
            "contentMeaning": e["title"],
            "contextualMeaning": e["purpose"],
            "proponentTrialIntent": f"Admit {e['label']} to establish {', '.join(e['claims'])}.",
            "trialPivotIntent": f"Use {e['label']} as objective documentary proof anchoring Opening Statement pillars.",
        }
    )
for e in casemodel.PETITIONER_EXHIBITS:
    EXHIBIT_SEMANTIC_MAPPINGS.append(
        {
            "id": f"MAP-{e['id']}",
            "exhibitId": e["id"],
            "proponent": "Petitioner",
            "modality": e["category"],
            "contentMeaning": e["title"],
            "contextualMeaning": e["motherUse"],
            "proponentTrialIntent": e["motherUse"],
            "trialPivotIntent": e["fatherPivot"],
        }
    )


def declarations():
    diary_t = named("HandwrittenDiaryEntry")
    vis_t = named("VisualForensicRecord")
    photo_t = named("PhotoPageRecord")
    map_t = named("ExhibitSemanticMapping")
    reg_exhibit_ids = [e["id"] for e in casemodel.all_exhibits()]

    return [
        structure("HandwrittenDiaryEntry", [("id", STR), ("exhibitId", STR), ("entryDate", STR), ("pageRange", STR), ("fullContextRebuttal", STR)]),
        structure("VisualForensicRecord", [("id", STR), ("exhibitId", STR), ("modality", STR), ("pageCount", NAT), ("trialPivot", STR)]),
        structure("PhotoPageRecord", [("id", STR), ("exhibitId", STR), ("pageNumber", NAT), ("subjects", STR), ("statutoryFactorId", STR)]),
        structure(
            "ExhibitSemanticMapping",
            [
                ("id", STR),
                ("exhibitId", STR),
                ("proponent", STR),
                ("modality", STR),
                ("contentMeaning", STR),
                ("contextualMeaning", STR),
                ("proponentTrialIntent", STR),
                ("trialPivotIntent", STR),
            ],
        ),
        member_string(),
        all_members(),
        distinct_strings(),
        definition("registerExhibitIds", list_t(STR), strings(reg_exhibit_ids)),
        definition(
            "diaryEntries",
            list_t(diary_t),
            lst(
                [
                    record(
                        "HandwrittenDiaryEntry",
                        id=s(d["id"]),
                        exhibitId=s(d["exhibitId"]),
                        entryDate=s(d["entryDate"]),
                        pageRange=s(d["pageRange"]),
                        fullContextRebuttal=s(d["fullContextRebuttal"]),
                    )
                    for d in HANDWRITTEN_DIARY_ENTRIES
                ],
                diary_t,
            ),
        ),
        definition(
            "visualForensics",
            list_t(vis_t),
            lst(
                [
                    record(
                        "VisualForensicRecord",
                        id=s(v["id"]),
                        exhibitId=s(v["exhibitId"]),
                        modality=s(v["modality"]),
                        pageCount=n(v["pageCount"]),
                        trialPivot=s(v["trialPivot"]),
                    )
                    for v in VISUAL_FORENSIC_RECORDS
                ],
                vis_t,
            ),
        ),
        definition(
            "photoCatalog",
            list_t(photo_t),
            lst(
                [
                    record(
                        "PhotoPageRecord",
                        id=s(p["id"]),
                        exhibitId=s(p["exhibitId"]),
                        pageNumber=n(p["pageNumber"]),
                        subjects=s(p["subjects"]),
                        statutoryFactorId=s(p["statutoryFactorId"]),
                    )
                    for p in PHOTO_PAGE_CATALOG
                ],
                photo_t,
            ),
        ),
        definition(
            "semanticMappings",
            list_t(map_t),
            lst(
                [
                    record(
                        "ExhibitSemanticMapping",
                        id=s(m["id"]),
                        exhibitId=s(m["exhibitId"]),
                        proponent=s(m["proponent"]),
                        modality=s(m["modality"]),
                        contentMeaning=s(m["contentMeaning"]),
                        contextualMeaning=s(m["contextualMeaning"]),
                        proponentTrialIntent=s(m["proponentTrialIntent"]),
                        trialPivotIntent=s(m["trialPivotIntent"]),
                    )
                    for m in EXHIBIT_SEMANTIC_MAPPINGS
                ],
                map_t,
            ),
        ),
        field_of_each("diaryIds", diary_t, "id"),
        field_of_each("visIds", vis_t, "id"),
        field_of_each("visExhibitIds", vis_t, "exhibitId"),
        field_of_each("photoIds", photo_t, "id"),
        field_of_each("photoExhibitIds", photo_t, "exhibitId"),
        field_of_each("mappingIds", map_t, "id"),
        field_of_each("mappedExhibitIds", map_t, "exhibitId"),
        definition(
            "diaryEntryCount",
            NAT,
            {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [call("diaryEntries")]},
        ),
        definition(
            "visualForensicCount",
            NAT,
            {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [call("visualForensics")]},
        ),
        definition(
            "photoCatalogCount",
            NAT,
            {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [call("photoCatalog")]},
        ),
        definition(
            "semanticMappingCount",
            NAT,
            {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [call("semanticMappings")]},
        ),
        holds("diaryIdsDistinct", call("distinctStrings", call("diaryIds", call("diaryEntries")))),
        holds("visualForensicIdsDistinct", call("distinctStrings", call("visIds", call("visualForensics")))),
        holds("visualForensicExhibitsResolve", call("allMembers", call("visExhibitIds", call("visualForensics")), call("registerExhibitIds"))),
        holds("photoIdsDistinct", call("distinctStrings", call("photoIds", call("photoCatalog")))),
        holds("photoExhibitsResolve", call("allMembers", call("photoExhibitIds", call("photoCatalog")), call("registerExhibitIds"))),
        holds("semanticMappingIdsDistinct", call("distinctStrings", call("mappingIds", call("semanticMappings")))),
        holds(
            "everyRegisterExhibitHasSemanticAndIntentMapping",
            call("allMembers", call("registerExhibitIds"), call("mappedExhibitIds", call("semanticMappings"))),
        ),
        theorem("diaryEntryCountIs8", call("diaryEntryCount"), n(8)),
        theorem("visualForensicCountIs12", call("visualForensicCount"), n(12)),
        theorem("photoCatalogCountIs12", call("photoCatalogCount"), n(12)),
        theorem("semanticMappingCountIs30", call("semanticMappingCount"), n(30)),
    ]


def render_module():
    return lexmod.module("VisualEvidence", declarations())


def render_toml():
    lines = ['spec = "prism-legal/visual-evidence/1"', ""]
    for d in HANDWRITTEN_DIARY_ENTRIES:
        lines += ["[[diary_entry]]", f'id = {json.dumps(d["id"])}', f'exhibit_id = {json.dumps(d["exhibitId"])}', f'entry_date = {json.dumps(d["entryDate"])}', f'page_range = {json.dumps(d["pageRange"])}', ""]
    for v in VISUAL_FORENSIC_RECORDS:
        lines += ["[[visual_forensic]]", f'id = {json.dumps(v["id"])}', f'exhibit_id = {json.dumps(v["exhibitId"])}', f'modality = {json.dumps(v["modality"])}', f'page_count = {v["pageCount"]}', ""]
    for p in PHOTO_PAGE_CATALOG:
        lines += ["[[photo_page]]", f'id = {json.dumps(p["id"])}', f'exhibit_id = {json.dumps(p["exhibitId"])}', f'page_number = {p["pageNumber"]}', f'subjects = {json.dumps(p["subjects"])}', ""]
    for m in EXHIBIT_SEMANTIC_MAPPINGS:
        lines += ["[[semantic_mapping]]", f'id = {json.dumps(m["id"])}', f'exhibit_id = {json.dumps(m["exhibitId"])}', f'proponent = {json.dumps(m["proponent"])}', f'modality = {json.dumps(m["modality"])}', ""]
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
        "module": "src/VisualEvidence.lex.tex",
        "diaryEntries": len(HANDWRITTEN_DIARY_ENTRIES),
        "visualForensics": len(VISUAL_FORENSIC_RECORDS),
        "photos": len(PHOTO_PAGE_CATALOG),
        "semanticMappings": len(EXHIBIT_SEMANTIC_MAPPINGS),
        "changed": changed,
    }


def check():
    if not MODULE.exists() or MODULE.read_text() != render_module():
        return {"ok": False, "reason": "src/VisualEvidence.lex.tex drifted; run `bin/prism-legal api sync`"}
    if not REGISTER.exists() or REGISTER.read_text() != render_toml():
        return {"ok": False, "reason": "model/visual-evidence.toml drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}
