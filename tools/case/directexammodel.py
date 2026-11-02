"""Intended Direct Examination Model (`src/DirectExam.lex.tex` and `model/direct-exam.toml`) for PrismLegal.

Models a structured 6-chapter, 36-question Direct Examination script (`DX-001`..`DX-036`)
with visual script annotations (`standard`, `yellow-highlight`, `red-strikethrough`),
exhibit admission moves (`movesToAdmit`), counsel prompts, and full Opening-aligned witness answers."""

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

REGISTER = ROOT / "model" / "direct-exam.toml"
MODULE = ROOT / "src" / "DirectExam.lex.tex"

VISUAL_CUES = ["standard", "yellow-highlight", "red-strikethrough"]

DIRECT_EXAM_CHAPTERS = [
    {"id": "CH-01", "title": "Chapter 1: Beneficiaries, Household History & 10-Year Public Service Career", "pageRange": "pp. 1-3", "pillarId": "OS-1", "statutoryId": "SF-01", "exhibitsAdmitted": [], "summary": "Introduce the three minor children (ages 15, 11, and 6), affirm co-parent's professional role, and establish 10 years of public administration and early caregiving."},
    {"id": "CH-02", "title": "Chapter 2: Equal Caregiving (2020-2027), Sabbatical Solo Care & 2027 Medical Leave", "pageRange": "pp. 3-5", "pillarId": "OS-2", "statutoryId": "SF-07", "exhibitsAdmitted": ["Ex-C", "Ex-E"], "summary": "Establish 4 months as sole primary caregiver during out-of-region fellowship, graduate tuition funding, and the 2027 medical transition leading to disability retirement."},
    {"id": "CH-03", "title": "Chapter 3: Disability Retirement, Zero-Revenue Civic Writing & 2026-2029 Tax Records", "pageRange": "pp. 5-8", "pillarId": "OS-3", "statutoryId": "SF-10", "exhibitsAdmitted": ["Ex-B", "Ex-D", "Ex-F", "Ex-H"], "summary": "Admit Ex-C, Ex-D, Ex-E, and Ex-F proving $5,000/mo disability pension, $0 civic writing draws, and zero-premium statutory dependent medical coverage."},
    {"id": "CH-04", "title": "Chapter 4: 2029 De-Escalation Videos, Transit Telemetry & Stipulated Dismissal", "pageRange": "pp. 8-11", "pillarId": "OS-4", "statutoryId": "SF-09", "exhibitsAdmitted": ["Ex-A", "Ex-J", "Ex-K"], "summary": "Admit Ex-A, Ex-J, and Ex-K refuting proximity allegations (512-yard telemetry) and establishing 9 incident-free post-separation months."},
    {"id": "CH-05", "title": "Chapter 5: Townhouse Environment, 90-Day 50/50 Execution & Photo Walkthrough", "pageRange": "pp. 11-14", "pillarId": "OS-3", "statutoryId": "SF-04", "exhibitsAdmitted": ["Ex-I"], "summary": "Admit Ex-I and walk page-by-page through the townhouse bedrooms, study desks, and Summer 2030 50/50 schedule."},
    {"id": "CH-06", "title": "Chapter 6: Early Seminar Completion (Ex. M), 50/50 Plan (Ex. L) & Guideline Support (Ex. N)", "pageRange": "pp. 14-17", "pillarId": "OS-5", "statutoryId": "SF-10", "exhibitsAdmitted": ["Ex-L", "Ex-M", "Ex-N", "Ex-O"], "summary": "Admit Ex-G, Ex-H, Ex-L, Ex-M, Ex-N, and Ex-O establishing early compliance, $30,000.00 Rule 16.2 impeachment, and the $250/mo guideline worksheet."},
]

DIRECT_EXAM_QUESTIONS = [
    {"id": "DX-001", "chapterId": "CH-01", "page": 1, "visualCue": "standard", "question": "Please state your role as Respondent and your relationship to the three minor children.", "counselPrompt": "Identify yourself as Respondent and parent of the three children (ages 15, 11, 6).", "fullTestimony": "I am the Respondent in this proceeding and the devoted parent of our three minor children, ages 15, 11, and 6.", "exhibitId": "NONE", "movesToAdmit": False, "statutoryId": "SF-01", "coachingNote": "Warm, steady eye contact with the Bench."},
    {"id": "DX-002", "chapterId": "CH-01", "page": 1, "visualCue": "yellow-highlight", "question": "How do you view Petitioner's role in the children's lives?", "counselPrompt": "⭐ Highlight: Affirm co-parent's professional skill and dedication (OS-1).", "fullTestimony": "Petitioner is a dedicated parent and a skilled professional. A choice between parents is unnecessary when both of us love and are dedicated to our three children.", "exhibitId": "NONE", "movesToAdmit": False, "statutoryId": "SF-01", "coachingNote": "Core credibility anchor from OS-1."},
    {"id": "DX-003", "chapterId": "CH-01", "page": 2, "visualCue": "standard", "question": "Summarize your 10 years of public administration and civil service from 2010 to 2020.", "counselPrompt": "10 years civil service, transition to home caregiving in 2020.", "fullTestimony": "I served 10 years in regional public administration from 2010 to 2020 before transitioning to flexible work so I could be home daily with our growing family.", "exhibitId": "Ex-E", "movesToAdmit": False, "statutoryId": "SF-07", "coachingNote": "Keep concise and factual."},
    {"id": "DX-004", "chapterId": "CH-01", "page": 2, "visualCue": "standard", "question": "Describe each child's current school, grade, and academic interests.", "counselPrompt": "Oldest Child (10th Grade), Middle Child (6th Grade), Youngest Child (1st Grade).", "fullTestimony": "Our oldest child is 15 and in 10th grade; our middle child is 11 and in 6th grade; and our youngest child is 6 and in 1st grade at the unified district schools 8 minutes from our townhouse.", "exhibitId": "Ex-I", "movesToAdmit": False, "statutoryId": "SF-02", "coachingNote": "Show detailed knowledge of daily school life."},
    {"id": "DX-005", "chapterId": "CH-01", "page": 3, "visualCue": "standard", "question": "How did you and Petitioner divide caregiving from 2020 onward?", "counselPrompt": "Equal daily care from 2020 onward.", "fullTestimony": "From 2020 onward, we shared all parenting duties equally—morning routines, school drop-offs, meals, homework, and bedtime.", "exhibitId": "Ex-I", "movesToAdmit": False, "statutoryId": "SF-03", "coachingNote": "Establishes 10-year caregiving baseline."},
    {"id": "DX-006", "chapterId": "CH-01", "page": 3, "visualCue": "red-strikethrough", "question": "[Stricken in Script] Historical pre-2020 lease renewal discussion.", "counselPrompt": "🚫 Red Strikethrough: Skip unless opened on cross.", "fullTestimony": "I am focused on the children's present routine and future stability.", "exhibitId": "NONE", "movesToAdmit": False, "statutoryId": "SF-01", "coachingNote": "Counsel struck this topic as unnecessary."},
    {"id": "DX-007", "chapterId": "CH-02", "page": 3, "visualCue": "yellow-highlight", "question": "Who cared for the three children during Petitioner's four-month out-of-region training sabbatical?", "counselPrompt": "⭐ Highlight: 4 months sole primary parent.", "fullTestimony": "I served as the sole primary day-to-day caregiver for all three children during those four months while supporting Petitioner's professional fellowship.", "exhibitId": "Ex-C", "movesToAdmit": False, "statutoryId": "SF-07", "coachingNote": "Refutes any claim that you cannot manage extended solo parenting."},
    {"id": "DX-008", "chapterId": "CH-02", "page": 4, "visualCue": "standard", "question": "How were Petitioner's graduate credentials funded during the household partnership?", "counselPrompt": "Pre-partnership savings, fellowship stipends, and consulting income (Ex-C).", "fullTestimony": "We funded Petitioner's graduate credentials together using our joint savings, education stipends, and my prior consulting salary so our family would have long-term security.", "exhibitId": "Ex-C", "movesToAdmit": True, "statutoryId": "SF-07", "coachingNote": "Move to admit Ex-C (2026-2027 Joint Tax Returns)."},
    {"id": "DX-009", "chapterId": "CH-02", "page": 4, "visualCue": "yellow-highlight", "question": "What happened in Autumn 2027 that affected your health and commercial consulting career?", "counselPrompt": "⭐ Highlight: Occupational health condition ended commercial travel career (Ex-N ¶ 15).", "fullTestimony": "In Autumn 2027, a chronic occupational health condition ended my ability to work in high-travel commercial systems consulting.", "exhibitId": "Ex-E", "movesToAdmit": False, "statutoryId": "SF-05", "coachingNote": "Matches Temporary Orders finding Ex-N ¶ 15."},
    {"id": "DX-010", "chapterId": "CH-02", "page": 5, "visualCue": "standard", "question": "What determination did the retirement board make regarding your disability in November 2028?", "counselPrompt": "Admit Ex-E — Full Disability Retirement effective 11/12/2028.", "fullTestimony": "Effective November 12, 2028, I received a certified full disability retirement determination, as documented in Exhibit E.", "exhibitId": "Ex-E", "movesToAdmit": True, "statutoryId": "SF-10", "coachingNote": "Move to admit Ex-E."},
    {"id": "DX-011", "chapterId": "CH-02", "page": 5, "visualCue": "standard", "question": "Does your disability retirement rating impair your ability to care for the three children at home?", "counselPrompt": "Distinguish commercial travel stress from calm home parenting.", "fullTestimony": "No. While I cannot work in high-travel commercial consulting, caring for our three children in our calm home routine is my greatest strength.", "exhibitId": "Ex-E", "movesToAdmit": False, "statutoryId": "SF-05", "coachingNote": "Clear, reassuring tone."},
    {"id": "DX-012", "chapterId": "CH-02", "page": 5, "visualCue": "standard", "question": "What medical benefits does Exhibit E provide for the three children?", "counselPrompt": "38 U.S.C. § 1781 zero-premium dependent coverage.", "fullTestimony": "Exhibit E provides comprehensive statutory medical coverage for all three minor children at $0 monthly premium.", "exhibitId": "Ex-E", "movesToAdmit": False, "statutoryId": "SF-10", "coachingNote": "Eliminates $320/mo duplicate insurance add-on."},
    {"id": "DX-013", "chapterId": "CH-03", "page": 6, "visualCue": "yellow-highlight", "question": "Have you received any wages, salary, or distributions from open-source civic curriculum research?", "counselPrompt": "⭐ Highlight: Admit Ex-D (2028-2029 IRS Transcripts) — $0.00 revenue.", "fullTestimony": "No. As verified by our certified 2028 and 2029 IRS transcripts in Exhibit D, those civic curriculum projects have generated $0.00 in revenue, wages, or distributions.", "exhibitId": "Ex-D", "movesToAdmit": True, "statutoryId": "SF-10", "coachingNote": "Move to admit Ex-D."},
    {"id": "DX-014", "chapterId": "CH-03", "page": 6, "visualCue": "standard", "question": "Why do you engage in self-paced educational curriculum writing at home?", "counselPrompt": "Structured intellectual activity compatible with 100% parenting availability.", "fullTestimony": "It serves as self-paced intellectual activity that I can pause at any moment whenever any of our three children need me.", "exhibitId": "Ex-D", "movesToAdmit": False, "statutoryId": "SF-03", "coachingNote": "Frames research positively."},
    {"id": "DX-015", "chapterId": "CH-03", "page": 7, "visualCue": "standard", "question": "What is your exact stipulated monthly income on your Sworn Financial Statement (Exhibit F)?", "counselPrompt": "Admit Ex-F — $5,000.00/mo tax-free disability pension.", "fullTestimony": "My total monthly income is $5,000.00 per month from my disability retirement benefits, as shown on Exhibit F.", "exhibitId": "Ex-F", "movesToAdmit": True, "statutoryId": "SF-10", "coachingNote": "Move to admit Ex-F."},
    {"id": "DX-016", "chapterId": "CH-03", "page": 7, "visualCue": "standard", "question": "What is Petitioner's stipulated monthly income in Exhibit B?", "counselPrompt": "Admit Ex-B — $8,000.00/mo salary.", "fullTestimony": "Petitioner's stipulated gross monthly salary is $8,000.00 per month, as shown in Exhibit B.", "exhibitId": "Ex-B", "movesToAdmit": True, "statutoryId": "SF-10", "coachingNote": "Move to admit Ex-B."},
    {"id": "DX-017", "chapterId": "CH-03", "page": 8, "visualCue": "red-strikethrough", "question": "[Stricken in Script] Secondary pre-2024 credit union account closure.", "counselPrompt": "🚫 Red Strikethrough: Immaterial to current ledger.", "fullTestimony": "All current accounts are fully disclosed on Exhibit F.", "exhibitId": "Ex-F", "movesToAdmit": False, "statutoryId": "SF-10", "coachingNote": "Skip on direct."},
    {"id": "DX-018", "chapterId": "CH-03", "page": 8, "visualCue": "yellow-highlight", "question": "What did Exhibit G and Exhibit H reveal regarding Petitioner's initial financial disclosures?", "counselPrompt": "⭐ Highlight: Admit Ex-G & Ex-H — $30,000.00 omitted in Escrow Accounts x4102 & x4109.", "fullTestimony": "Exhibit G is Petitioner's initial Sworn Financial Statement, which omitted Escrow Checking x4102 and Reserve Savings x4109. Subpoenaed statements in Exhibit H proved those accounts held $30,000.00.", "exhibitId": "Ex-H", "movesToAdmit": True, "statutoryId": "SF-11", "coachingNote": "Move to admit Ex-G and Ex-H calmly."},
    {"id": "DX-019", "chapterId": "CH-04", "page": 9, "visualCue": "standard", "question": "Turning to 2029, what do the unedited home videos in Exhibit K show?", "counselPrompt": "Admit Ex-K — calm voice and de-escalation.", "fullTestimony": "Exhibit K shows our calm daily interactions with the children and my efforts to de-escalate tension respectfully.", "exhibitId": "Ex-K", "movesToAdmit": True, "statutoryId": "SF-06", "coachingNote": "Move to admit Ex-K."},
    {"id": "DX-020", "chapterId": "CH-04", "page": 9, "visualCue": "yellow-highlight", "question": "How was the October 2029 interim administrative petition resolved on November 18, 2029?", "counselPrompt": "⭐ Highlight: Admit Ex-J — dismissed by joint stipulation with zero findings.", "fullTestimony": "We resolved and dismissed it by joint stipulation on November 18, 2029 in Exhibit J, with zero findings of fault, and agreed to structured co-parenting protocols.", "exhibitId": "Ex-J", "movesToAdmit": True, "statutoryId": "SF-09", "coachingNote": "Move to admit Ex-J."},
    {"id": "DX-021", "chapterId": "CH-04", "page": 10, "visualCue": "yellow-highlight", "question": "What does the transit telemetry log in Exhibit A prove regarding the school corridor allegation?", "counselPrompt": "⭐ Highlight: Admit Ex-A — 512+ yards away on a public arterial boulevard.", "fullTestimony": "Exhibit A is the verified transit telemetry log proving I remained more than 512 yards away on a public arterial boulevard and complied strictly with the 500-yard buffer.", "exhibitId": "Ex-A", "movesToAdmit": True, "statutoryId": "SF-09", "coachingNote": "Move to admit Ex-A."},
    {"id": "DX-022", "chapterId": "CH-04", "page": 10, "visualCue": "standard", "question": "Have there been any household incidents in the nine months since you separated on November 1, 2029?", "counselPrompt": "Zero incidents across 9 months of separation.", "fullTestimony": "None at all. Every exchange and communication over the past nine months has been completely peaceful and incident-free.", "exhibitId": "Ex-O", "movesToAdmit": False, "statutoryId": "SF-06", "coachingNote": "Emphasize 9-month track record."},
    {"id": "DX-023", "chapterId": "CH-04", "page": 11, "visualCue": "standard", "question": "If opposing counsel points to page 6 of your 2028 homework study log (OP Ex. 13), what does the full page say?", "counselPrompt": "FRE 106 completeness — lines 15-28 record collaborative study habits and positive reinforcement.", "fullTestimony": "Lines 15 through 28 on that exact same page from October 14, 2028 record our commitment to positive reinforcement, structured study breaks, and patient explanation.", "exhibitId": "OP-Ex-13", "movesToAdmit": False, "statutoryId": "SF-05", "coachingNote": "Pre-empts TRAP-12."},
    {"id": "DX-024", "chapterId": "CH-04", "page": 11, "visualCue": "red-strikethrough", "question": "[Stricken in Script] Collateral dispute over 2028 winter break travel.", "counselPrompt": "🚫 Red Strikethrough: Omit.", "fullTestimony": "Our proposed plan sets clear holiday schedules going forward.", "exhibitId": "Ex-L", "movesToAdmit": False, "statutoryId": "SF-01", "coachingNote": "Stricken in counsel script."},
    {"id": "DX-025", "chapterId": "CH-05", "page": 12, "visualCue": "yellow-highlight", "question": "Please walk the Court through the townhouse photographs in Exhibit I (pages 1 through 11).", "counselPrompt": "⭐ Highlight: Admit Ex-I — review each picture of bedrooms, study areas, and courtyard routine.", "fullTestimony": "Exhibit I shows our three-bedroom townhouse 8 minutes from the children's schools, including each of the three children's bedrooms, their study desks, our kitchen, and the greenbelt courtyard where we play and study together.", "exhibitId": "Ex-I", "movesToAdmit": True, "statutoryId": "SF-04", "coachingNote": "Move to admit Ex-I and use the 12-photo guide."},
    {"id": "DX-026", "chapterId": "CH-05", "page": 12, "visualCue": "standard", "question": "What community support network surrounds your townhouse neighborhood?", "counselPrompt": "Adjacent neighborhood families & retired school librarian.", "fullTestimony": "Our townhouse community includes long-standing neighborhood families and a retired school librarian next door who regularly sees our children's calm after-school routine.", "exhibitId": "Ex-I", "movesToAdmit": False, "statutoryId": "SF-03", "coachingNote": "Corroborated by W-03 and W-04."},
    {"id": "DX-027", "chapterId": "CH-05", "page": 13, "visualCue": "yellow-highlight", "question": "How did the equal 50/50 2-2-5-5 schedule work during the 90-day summer period?", "counselPrompt": "⭐ Highlight: May 15 to August 15, 2030 — seamless 50/50 execution.", "fullTestimony": "From mid-May through mid-August 2030, we practiced an equal 50/50 parenting schedule. All three children thrived, and every exchange went smoothly.", "exhibitId": "Ex-L", "movesToAdmit": False, "statutoryId": "SF-04", "coachingNote": "Proves 50/50 works in practice."},
    {"id": "DX-028", "chapterId": "CH-05", "page": 13, "visualCue": "standard", "question": "What did the Court find at Temporary Orders (Exhibit N ¶ 8) regarding your parenting time?", "counselPrompt": "Court found no basis to restrict parenting time.", "fullTestimony": "In Paragraph 8 of Temporary Orders, the Court found no basis to restrict my parenting time.", "exhibitId": "Ex-N", "movesToAdmit": False, "statutoryId": "SF-01", "coachingNote": "Direct judicial finding."},
    {"id": "DX-029", "chapterId": "CH-05", "page": 13, "visualCue": "yellow-highlight", "question": "Are you available to care for the three children during Petitioner's regional travel weeks?", "counselPrompt": "⭐ Highlight: 100% available at $0 cost vs. $2,400/mo commercial agency (OP Ex. 4).", "fullTestimony": "Yes. Because I am retired on disability pension, I am available to care for our three children during every regional travel block for $0, rather than placing them with a $2,400-per-month commercial agency.", "exhibitId": "Ex-L", "movesToAdmit": False, "statutoryId": "SF-10", "coachingNote": "Defeats OP-Ex-04 childcare add-on."},
    {"id": "DX-030", "chapterId": "CH-05", "page": 14, "visualCue": "standard", "question": "What have the three children expressed about the parenting schedule?", "counselPrompt": "Consistent wish for equal 50/50 time.", "fullTestimony": "All three children have consistently asked to continue our equal 50/50 parenting schedule.", "exhibitId": "OP-Ex-14", "movesToAdmit": False, "statutoryId": "SF-02", "coachingNote": "Supports SF-02."},
    {"id": "DX-031", "chapterId": "CH-06", "page": 14, "visualCue": "yellow-highlight", "question": "Did you complete the court-ordered Collaborative Co-Parenting Seminar?", "counselPrompt": "⭐ Highlight: Admit Ex-M — completed August 15, 2030 (30 days early).", "fullTestimony": "Yes. I completed the entire seminar on August 15, 2030—thirty days ahead of the Court's deadline—as shown in Exhibit M.", "exhibitId": "Ex-M", "movesToAdmit": True, "statutoryId": "SF-06", "coachingNote": "Move to admit Ex-M."},
    {"id": "DX-032", "chapterId": "CH-06", "page": 15, "visualCue": "standard", "question": "How have you and Petitioner communicated since November 2029?", "counselPrompt": "Admit Ex-O — polite, structured co-parenting logs.", "fullTestimony": "We have communicated exclusively through the co-parenting platform in Exhibit O in a polite, brief, child-focused manner.", "exhibitId": "Ex-O", "movesToAdmit": True, "statutoryId": "SF-09", "coachingNote": "Move to admit Ex-O."},
    {"id": "DX-033", "chapterId": "CH-06", "page": 15, "visualCue": "yellow-highlight", "question": "What parenting schedule and decision-making framework are you asking the Court to adopt in Exhibit L?", "counselPrompt": "⭐ Highlight: Admit Ex-L — Equal 50/50 2-2-5-5 schedule (182.5 overnights), Wednesday school exchanges, Joint Decisions with mediation first.", "fullTestimony": "In Exhibit L, we ask for an equal 50/50 schedule with Wednesday school exchanges, plus joint major decision-making with mediation before court.", "exhibitId": "Ex-L", "movesToAdmit": True, "statutoryId": "SF-01", "coachingNote": "Move to admit Ex-L."},
    {"id": "DX-034", "chapterId": "CH-06", "page": 16, "visualCue": "yellow-highlight", "question": "What is the guideline child support result in Exhibit N based on your stipulated incomes?", "counselPrompt": "⭐ Highlight: Admit Ex-N — $8,000/mo vs. $5,000/mo at 182.5 overnights = $250.00/mo Petitioner to Respondent.", "fullTestimony": "Using our stipulated incomes of $8,000 and $5,000 per month and 182.5 overnights each, the guideline worksheet in Exhibit N results in $250.00 per month from Petitioner to me.", "exhibitId": "Ex-N", "movesToAdmit": True, "statutoryId": "SF-10", "coachingNote": "Move to admit Ex-N."},
    {"id": "DX-035", "chapterId": "CH-06", "page": 16, "visualCue": "yellow-highlight", "question": "Why should the Court deny Petitioner's request for retroactive support from November 2029 through May 2030?", "counselPrompt": "⭐ Highlight: Cite Ex-N ¶¶ 24-26 — unconscionability due to $30,000.00 undisclosed escrow accounts (Ex-G/Ex-H).", "fullTestimony": "At Temporary Orders (Exhibit N ¶¶ 24-26), the Court ruled that the interim expense stipulation was unconscionable because Petitioner had omitted $30,000.00 in escrow accounts from the initial Sworn Financial Statement.", "exhibitId": "Ex-N", "movesToAdmit": False, "statutoryId": "SF-11", "coachingNote": "Calm, factual reference to judicial ruling."},
    {"id": "DX-036", "chapterId": "CH-06", "page": 17, "visualCue": "standard", "question": "In one sentence, why is your proposed plan in the best interests of the three minor children?", "counselPrompt": "Closing summary anchored in equal love and stability.", "fullTestimony": "Our three children thrive when they have equal, loving time with both of their capable parents in a calm, predictable 50/50 routine.", "exhibitId": "Ex-L", "movesToAdmit": False, "statutoryId": "SF-01", "coachingNote": "Strong, child-focused finish."},
]

_CHAPTER_PILLAR = {ch["id"]: ch["pillarId"] for ch in DIRECT_EXAM_CHAPTERS}
for _q in DIRECT_EXAM_QUESTIONS:
    _q.setdefault("pillarId", _CHAPTER_PILLAR[_q["chapterId"]])



def declarations():
    ch_t = named("DirectExamChapter")
    q_t = named("DirectExamQuestion")
    exhibit_ids = ["NONE"] + [e["id"] for e in casemodel.all_exhibits()]
    factor_ids = [f["id"] for f in casemodel.STATUTORY_FACTORS]

    return [
        structure("DirectExamChapter", [("id", STR), ("title", STR), ("pageRange", STR), ("pillarId", STR)]),
        structure(
            "DirectExamQuestion",
            [
                ("id", STR),
                ("chapterId", STR),
                ("page", NAT),
                ("visualCue", STR),
                ("question", STR),
                ("fullTestimony", STR),
                ("exhibitId", STR),
                ("movesToAdmit", BOOL),
                ("statutoryId", STR),
            ],
        ),
        member_string(),
        all_members(),
        distinct_strings(),
        definition("visualCues", list_t(STR), strings(VISUAL_CUES)),
        definition(
            "chapters",
            list_t(ch_t),
            lst([record("DirectExamChapter", id=s(c["id"]), title=s(c["title"]), pageRange=s(c["pageRange"]), pillarId=s(c["pillarId"])) for c in DIRECT_EXAM_CHAPTERS], ch_t),
        ),
        definition(
            "questions",
            list_t(q_t),
            lst(
                [
                    record(
                        "DirectExamQuestion",
                        id=s(q["id"]),
                        chapterId=s(q["chapterId"]),
                        page=n(q["page"]),
                        visualCue=s(q["visualCue"]),
                        question=s(q["question"]),
                        fullTestimony=s(q["fullTestimony"]),
                        exhibitId=s(q["exhibitId"]),
                        movesToAdmit=b(q["movesToAdmit"]),
                        statutoryId=s(q["statutoryId"]),
                    )
                    for q in DIRECT_EXAM_QUESTIONS
                ],
                q_t,
            ),
        ),
        definition("validExhibitIds", list_t(STR), strings(exhibit_ids)),
        definition("validFactorIds", list_t(STR), strings(factor_ids)),
        field_of_each("chapterIds", ch_t, "id"),
        field_of_each("questionIds", q_t, "id"),
        field_of_each("questionChapterIds", q_t, "chapterId"),
        field_of_each("questionVisualCues", q_t, "visualCue"),
        field_of_each("questionExhibitIds", q_t, "exhibitId"),
        field_of_each("questionStatutoryIds", q_t, "statutoryId"),
        definition(
            "allQuestionsHaveTestimony",
            BOOL,
            match_list(
                var("xs"),
                b(True),
                "head",
                "tail",
                if_(eq_string(proj(var("head"), "fullTestimony"), s("")), b(False), call("allQuestionsHaveTestimony", var("tail"))),
            ),
            parameters=[("xs", list_t(q_t))],
            recursive="xs",
        ),
        definition(
            "countByVisualCue",
            NAT,
            match_list(
                var("xs"),
                n(0),
                "head",
                "tail",
                if_(
                    eq_string(proj(var("head"), "visualCue"), var("cue")),
                    add(n(1), call("countByVisualCue", var("cue"), var("tail"))),
                    call("countByVisualCue", var("cue"), var("tail")),
                ),
            ),
            parameters=[("cue", STR), ("xs", list_t(q_t))],
            recursive="xs",
        ),
        definition(
            "countAdmissionMoves",
            NAT,
            match_list(
                var("xs"),
                n(0),
                "head",
                "tail",
                if_(
                    proj(var("head"), "movesToAdmit"),
                    add(n(1), call("countAdmissionMoves", var("tail"))),
                    call("countAdmissionMoves", var("tail")),
                ),
            ),
            parameters=[("xs", list_t(q_t))],
            recursive="xs",
        ),
        holds("directExamChapterIdsDistinct", call("distinctStrings", call("chapterIds", call("chapters")))),
        holds("directExamQuestionIdsDistinct", call("distinctStrings", call("questionIds", call("questions")))),
        holds("directExamQuestionChaptersResolve", call("allMembers", call("questionChapterIds", call("questions")), call("chapterIds", call("chapters")))),
        holds("directExamVisualCuesValid", call("allMembers", call("questionVisualCues", call("questions")), call("visualCues"))),
        holds("directExamQuestionExhibitsResolve", call("allMembers", call("questionExhibitIds", call("questions")), call("validExhibitIds"))),
        holds("directExamQuestionStatutesResolve", call("allMembers", call("questionStatutoryIds", call("questions")), call("validFactorIds"))),
        holds("everyDirectExamQuestionHasFullTestimony", call("allQuestionsHaveTestimony", call("questions"))),
        theorem("directExamYellowHighlightCount", call("countByVisualCue", s("yellow-highlight"), call("questions")), n(14)),
        theorem("directExamRedStrikethroughCount", call("countByVisualCue", s("red-strikethrough"), call("questions")), n(3)),
        theorem("directExamAdmissionMoveCount", call("countAdmissionMoves", call("questions")), n(14)),
    ]


def render_module():
    return lexmod.module("DirectExam", declarations())


def render_toml():
    lines = ['spec = "prism-legal/direct-exam/1"', ""]
    for c in DIRECT_EXAM_CHAPTERS:
        lines += ["[[chapter]]", f'id = {json.dumps(c["id"])}', f'title = {json.dumps(c["title"])}', f'page_range = {json.dumps(c["pageRange"])}', ""]
    for q in DIRECT_EXAM_QUESTIONS:
        lines += [
            "[[question]]",
            f'id = {json.dumps(q["id"])}',
            f'chapter_id = {json.dumps(q["chapterId"])}',
            f'page = {q["page"]}',
            f'visual_cue = {json.dumps(q["visualCue"])}',
            f'question = {json.dumps(q["question"])}',
            f'exhibit_id = {json.dumps(q["exhibitId"])}',
            f'moves_to_admit = {"true" if q["movesToAdmit"] else "false"}',
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
    return {
        "module": "src/DirectExam.lex.tex",
        "chapters": len(DIRECT_EXAM_CHAPTERS),
        "questions": len(DIRECT_EXAM_QUESTIONS),
        "changed": changed,
    }


def check():
    if not MODULE.exists() or MODULE.read_text() != render_module():
        return {"ok": False, "reason": "src/DirectExam.lex.tex drifted; run `bin/prism-legal api sync`"}
    if not REGISTER.exists() or REGISTER.read_text() != render_toml():
        return {"ok": False, "reason": "model/direct-exam.toml drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}
