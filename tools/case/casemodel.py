"""Single-source-of-truth domain model for the PrismLegal Reference Family Law Matter
(Case No. 2030-FAM-9010, Final Evidentiary Hearing — September 18, 2030).

All personal identifiers, dates, ages, places, organizations, and financial figures
are synthetic textbook benchmark values for the open-source public-benefit release."""

from . import ROOT, lexmod, portalmodel, semantic
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

MODULE = ROOT / "src" / "Register.lex.tex"

CASE_META = {
    "caseNumber": "2030-FAM-9010",
    "caption": "In re Parental Responsibilities & Support Benchmark (Petitioner v. Respondent)",
    "court": "Metropolitan Family & Civil Court",
    "division": "Division 7A",
    "hearingTitle": "Final Evidentiary Hearing",
    "hearingDate": "2030-09-18",
    "hearingTime": "09:00 AM",
    "hearingDurationHours": 6,
    "petitioner": {
        "name": "Petitioner Co-Parent (Party A)",
        "role": "Petitioner",
        "counsel": "Opposing Domestic Trial Counsel (Counterparty Law Group)",
        "stipulatedMonthlyIncome": 8000,
        "stipulatedIncomeSource": "Regional Logistics & Supply-Chain Director Salary (Pretrial Stipulation ¶ 14)",
    },
    "respondent": {
        "name": "Respondent Co-Parent (Party B)",
        "role": "Respondent",
        "counsel": "Lead Domestic Trial Counsel (Regional Trial Advocacy Partners LLP)",
        "stipulatedMonthlyIncome": 5000,
        "stipulatedIncomeSource": "Statutory Public-Service Disability & Pension Benefit (Non-Taxable Baseline, Ex. E)",
    },
}

CHILDREN = [
    {
        "id": "CH-01",
        "name": "Minor Dependent 1 (Age 15)",
        "dob": "2015-01-20",
        "age": 15,
        "grade": "10th Grade (Secondary Academy)",
        "notes": "Thrives in STEM robotics and track; expressed clear preference for equal week-on/week-off schedule and mid-week school exchanges.",
    },
    {
        "id": "CH-02",
        "name": "Minor Dependent 2 (Age 11)",
        "dob": "2019-06-15",
        "age": 11,
        "grade": "6th Grade (Middle Academy)",
        "notes": "Closely bonded with both parents; participates in orchestra and community youth soccer.",
    },
    {
        "id": "CH-03",
        "name": "Minor Dependent 3 (Age 6)",
        "dob": "2024-02-10",
        "age": 6,
        "grade": "1st Grade (Elementary Academy)",
        "notes": "Flourishes in predictable alternating weekly routines with mid-week school-curb transitions.",
    },
]

OPENING_PILLARS = [
    {
        "id": "OS-1",
        "title": "Public-Service Career & Full-Time Caregiving Availability",
        "theme": "Service & Devotion",
        "verbatimQuote": "Respondent served as a municipal civil engineer before retiring on a statutory disability pension; that pension provides full-time daytime availability to care for the three dependents before and after school.",
        "summary": "Frames Respondent's statutory pension benefit (Ex. E) as a structural caregiving asset: full-time availability for school drop-offs, pickups, sick days, and medical appointments without third-party agency costs.",
        "exhibits": ["Ex-E", "Ex-I", "Ex-O"],
        "statutory": "Uniform Domestic Relations Act § 402(a)(3), (5), (7)",
    },
    {
        "id": "OS-2",
        "title": "Six Years of Primary Hands-On Parenting & 2028 Solo Caregiving",
        "theme": "Historical Continuity",
        "verbatimQuote": "From 2023 through 2029, Respondent managed daily school transport, homework, and pediatric visits—including four consecutive months in 2028 when Petitioner was on an out-of-region logistics assignment.",
        "summary": "Establishes undisputed historical caregiving continuity under § 402(a)(3) and (7), corroborated by school attendance records (Ex. K), co-parenting calendar logs (Ex. B), and family photographs (Ex. O).",
        "exhibits": ["Ex-B", "Ex-K", "Ex-O"],
        "statutory": "Uniform Domestic Relations Act § 402(a)(3), (4), (7)",
    },
    {
        "id": "OS-3",
        "title": "Proactive Seminar Completion & Constructive Co-Parenting",
        "theme": "Accountability & Maturity",
        "verbatimQuote": "Respondent completed the court-certified 16-hour Co-Parenting & Communication Seminar 30 days ahead of the judicial deadline and maintained calm, child-centered written communication across every exchange.",
        "summary": "Demonstrates compliance with court orders and capacity to encourage the dependents' relationship with both parents (§ 402(a)(6), (11)) via certified seminar completion (Ex. D) and co-parenting portal exports (Ex. A, Ex. B).",
        "exhibits": ["Ex-A", "Ex-B", "Ex-D", "Ex-F"],
        "statutory": "Uniform Domestic Relations Act § 402(a)(6), (9), (11)",
    },
    {
        "id": "OS-4",
        "title": "Equal 50/50 Week-On/Week-Off Schedule & Joint Governance",
        "theme": "Stability & Parity",
        "verbatimQuote": "The 90-day equal 50/50 schedule in early 2030 operated with zero tardies, strong academic performance, and seamless Wednesday school-curb exchanges.",
        "summary": "Anchors theProposed Parenting Plan (Ex. L): 182.5 overnights per parent, Wednesday school transitions that eliminate direct conflict, and joint major decision-making with mediation first.",
        "exhibits": ["Ex-B", "Ex-K", "Ex-L", "Ex-O"],
        "statutory": "Uniform Domestic Relations Act § 402(a)(1)–(11) & § 402(b)",
    },
    {
        "id": "OS-5",
        "title": "Stipulated Financial Baseline & Mandatory Disclosure Audit",
        "theme": "Financial Integrity",
        "verbatimQuote": "Under Pretrial Stipulation ($8,000/mo Petitioner, $5,000/mo Respondent), equal parenting time, $0 dependent medical premium, and direct parental care, guideline support is $250.00/mo from Petitioner to Respondent.",
        "summary": "Proves the Guideline Support Worksheet (Ex. N: $250.00/mo transfer to Respondent), bars speculative wage imputation under § 305(5)(b) (Ex. E, Ex. I), and documents Petitioner's $30,000.00 escrow omission under Rule 16.2 (Ex. G, Ex. H, Ex. J).",
        "exhibits": ["Ex-E", "Ex-G", "Ex-H", "Ex-I", "Ex-J", "Ex-N"],
        "statutory": "Uniform Support Guidelines § 305 & Civil Rule 16.2(e)(10)",
    },
    {
        "id": "OS-6",
        "title": "Neutral School-Zone Compliance & Unfounded Restriction Rebuttal",
        "theme": "Objective Verification",
        "verbatimQuote": "Certified school check-in and transit logs confirm Respondent remained more than 500 yards from Petitioner's residence on the regional arterial avenue while completing routine school transport.",
        "summary": "Rebuts Petitioner's allegation of a buffer violation using certified transit and school badge telemetry (Ex. F, Ex. M), proving strict compliance with interim court orders.",
        "exhibits": ["Ex-F", "Ex-L", "Ex-M"],
        "statutory": "Uniform Domestic Relations Act §§ 402(a)(9), 406 & FRE 901",
    },
]

STATUTORY_FACTORS = [
    {
        "id": "SF-01",
        "section": "§ 402(a)(1)",
        "title": "Wishes of the Child's Parents as to Parenting Time",
        "proponentPosition": "Respondent requests an equal 50/50 week-on/week-off schedule (182.5 overnights each) maximizing both parents' active involvement (Ex. L).",
        "opposingPosition": "Petitioner requests reducing Respondent to 90 overnights/year (24.7%, alternating weekends).",
        "exhibits": ["Ex-L", "OP-Ex-01"],
        "weight": "Supports Equal 50/50 Parity",
    },
    {
        "id": "SF-02",
        "section": "§ 402(a)(2)",
        "title": "Wishes of the Child (Mature Expression)",
        "proponentPosition": "Unredacted co-parenting portal messages (OP Ex. 14) document the 15-year-old asking to restore the equal 50/50 weekly schedule.",
        "opposingPosition": "Petitioner opposes an in camera interview while selectively quoting message fragments.",
        "exhibits": ["Ex-B", "OP-Ex-14"],
        "weight": "Supports Equal 50/50 Parity",
    },
    {
        "id": "SF-03",
        "section": "§ 402(a)(3)",
        "title": "Interaction & Interrelationship with Parents & Siblings",
        "proponentPosition": "Six years of daily hands-on caregiving, including four months of solo parenting in 2028 during Petitioner's regional logistics rotation (Ex. B, Ex. K, Ex. O).",
        "opposingPosition": "Relies on collateral witnesses who have not observed Respondent's home since 2028.",
        "exhibits": ["Ex-B", "Ex-K", "Ex-O"],
        "weight": "Strongly Favors Respondent",
    },
    {
        "id": "SF-04",
        "section": "§ 402(a)(4)",
        "title": "Adjustment to Home, School, and Community",
        "proponentPosition": "Respondent's single-family residence is located inside the dependents' school attendance zone (8 minutes from school, Ex. O); zero tardies during 2030 50/50 period (Ex. K).",
        "opposingPosition": "Proposes third-party commercial after-school care during Petitioner's multi-day regional travel shifts.",
        "exhibits": ["Ex-K", "Ex-L", "Ex-O"],
        "weight": "Strongly Favors Respondent",
    },
    {
        "id": "SF-05",
        "section": "§ 402(a)(5)",
        "title": "Mental and Physical Health of All Individuals Involved",
        "proponentPosition": "Certified pension & medical records (Ex. E) confirm full stability and parenting fitness; seminar completed 30 days early (Ex. D).",
        "opposingPosition": "Attempts to mischaracterize Respondent's statutory disability retirement and 2028 homework study notebook (OP Ex. 13).",
        "exhibits": ["Ex-D", "Ex-E", "OP-Ex-13"],
        "weight": "Favors Respondent",
    },
    {
        "id": "SF-06",
        "section": "§ 402(a)(6)",
        "title": "Ability to Encourage Love, Affection & Contact with Other Parent",
        "proponentPosition": "Co-parenting portal logs (Ex. A, Ex. B, OP Ex. 14) show Respondent consistently facilitating calls, swaps, and respectful communication.",
        "opposingPosition": "Unilaterally reduced Respondent's parenting time in September 2029 without court order.",
        "exhibits": ["Ex-A", "Ex-B", "Ex-L", "OP-Ex-14"],
        "weight": "Strongly Favors Respondent",
    },
    {
        "id": "SF-07",
        "section": "§ 402(a)(7)",
        "title": "Past Pattern of Involvement Reflecting Values, Time & Mutual Support",
        "proponentPosition": "Verified 2023–2030 history of school transport, STEM coaching, medical appointments, and full 90-day 50/50 execution in 2030 (Ex. B, Ex. K, Ex. O).",
        "opposingPosition": "Claims primary caregiver status despite recurring multi-day regional travel schedule.",
        "exhibits": ["Ex-B", "Ex-K", "Ex-O"],
        "weight": "Strongly Favors Respondent",
    },
    {
        "id": "SF-08",
        "section": "§ 402(a)(8)",
        "title": "Physical Proximity of the Parties' Residences",
        "proponentPosition": "Both residences are within the same suburban school district catchment (10 minutes apart), making week-on/week-off school exchanges effortless (Ex. L, Ex. O).",
        "opposingPosition": "Concedes geographic proximity in Pretrial Stipulation.",
        "exhibits": ["Ex-L", "Ex-O"],
        "weight": "Stipulated / Supports 50/50",
    },
    {
        "id": "SF-09",
        "section": "§ 402(a)(9)",
        "title": "Ability to Place the Needs of the Child Ahead of Own Needs",
        "proponentPosition": "Respondent provides free direct parental care during Petitioner's regional travel shifts instead of charging $1,500/mo for commercial after-school care (Ex. L, Ex. N).",
        "opposingPosition": "Demands $450/mo worksheet add-on for third-party vendor care while excluding Respondent.",
        "exhibits": ["Ex-B", "Ex-D", "Ex-L", "Ex-N"],
        "weight": "Strongly Favors Respondent",
    },
    {
        "id": "SF-10",
        "section": "§ 402(b)(1)",
        "title": "Capacity to Cooperate & Make Joint Major Decisions",
        "proponentPosition": "Parties jointly selected schools, pediatricians, and extracurriculars for 6 years; Proposed Plan (Ex. L) uses neutral school exchanges and mediation first.",
        "opposingPosition": "Requests sole decision-making based on transitional separation disagreements.",
        "exhibits": ["Ex-A", "Ex-B", "Ex-D", "Ex-L"],
        "weight": "Supports Joint Governance",
    },
    {
        "id": "SF-11",
        "section": "§ 305 & Rule 16.2",
        "title": "Guideline Support Accuracy & Complete Financial Disclosure",
        "proponentPosition": "Ex. N calculates $250.00/mo from Petitioner to Respondent on stipulated $8,000/$5,000 baseline; Ex. G & Ex. H prove Petitioner omitted $30,000.00 in escrow accounts x4102/x4109.",
        "opposingPosition": "OP Ex. 2 seeks $750.00/mo from Respondent by assuming 90 overnights and adding duplicate health/vendor charges.",
        "exhibits": ["Ex-E", "Ex-G", "Ex-H", "Ex-I", "Ex-J", "Ex-N", "OP-Ex-02"],
        "weight": "Decisive for Respondent",
    },
]

FINANCIAL_LEDGER = {
    "motherStipulatedMonthly": 8000.00,
    "fatherStipulatedMonthly": 5000.00,
    "combinedMonthlyBaseline": 13000.00,
    "undisclosedReserveBalance": 30000.00,
    "undisclosedAccounts": ["Escrow Checking x4102", "Escrow Reserve Savings x4109"],
    "sfsFilingDate": "2029-06-10",
    "bankProductionDate": "2029-11-15",
    "fatherProposal": {
        "worksheetExhibit": "Ex-N",
        "motherGrossMonthly": 8000.00,
        "fatherGrossMonthly": 5000.00,
        "combinedMonthly": 13000.00,
        "fatherOvernights": 182.5,
        "motherOvernights": 182.5,
        "healthInsuranceAddon": 0.00,
        "childcareAddon": 0.00,
        "healthInsuranceAdjustment": 0.00,
        "childcareAdjustment": 0.00,
        "netMonthlyTransfer": 250.00,
        "direction": "Petitioner pays Respondent $250.00/mo",
    },
    "motherProposal": {
        "worksheetExhibit": "OP-Ex-02",
        "motherGrossMonthly": 8000.00,
        "fatherImputedMonthly": 5000.00,
        "combinedMonthly": 13000.00,
        "fatherOvernights": 90.0,
        "motherOvernights": 275.0,
        "healthInsuranceAddon": 180.00,
        "childcareAddon": 450.00,
        "healthInsuranceAdjustment": 180.00,
        "childcareAdjustment": 450.00,
        "netMonthlyTransfer": 750.00,
        "direction": "Respondent pays Petitioner $750.00/mo",
    },
    "disclosureAudit": {
        "rule": "FRCP 26(e) & Uniform Civil Rule 16.2(e)(10)",
        "motherJuly2025SfsExhibit": "Ex-G (June 10, 2029 Initial SFS)",
        "motherJuly2025DisclosedBankTotal": 0.00,
        "motherActualReserveBalances": 30000.00,
        "motherApril2026SfsExhibit": "OP-Ex-04 (May 2030 Amended SFS)",
        "motherApril2026DisclosedBankTotal": 14200.00,
        "temporaryOrdersFinding": "Subpoenaed bank records (Ex. H) confirmed $30,000.00 across Escrow Checking x4102 and Reserve Savings x4109 on June 10, 2029, triggering mandatory reopening and fee reallocation under Rule 16.2(e)(10).",
    },
}

CLAIMS = [
    {
        "id": "CLM-01",
        "category": "parenting-time",
        "status": "corroborated",
        "title": "Equal 50/50 Parenting Time Best Serves the Three Minor Dependents",
        "statement": "Under Uniform Domestic Relations Act § 402(a), an equal 50/50 week-on/week-off schedule (182.5 overnights each) with Wednesday school exchanges preserves caregiving continuity and emotional stability.",
        "summary": "Equal 182.5-overnight schedule with mid-week school exchanges preserves historical continuity and academic performance.",
        "statutory": "Uniform Domestic Relations Act § 402(a)(1)–(11)",
        "exhibits": ["Ex-B", "Ex-K", "Ex-L", "Ex-O"],
        "depends": ["CLM-02", "CLM-03", "CLM-04"],
    },
    {
        "id": "CLM-02",
        "category": "parenting-time",
        "status": "corroborated",
        "title": "Six-Year Hands-On Caregiving & 2028 Four-Month Solo Parenting",
        "statement": "From 2023 through 2029, Respondent handled daily school transport, homework, and pediatric care—including four months of solo caregiving in 2028 while Petitioner was on a regional logistics rotation.",
        "summary": "Six years of primary daily caregiving and four months of solo parenting in 2028 establish deep caregiving continuity.",
        "statutory": "Uniform Domestic Relations Act § 402(a)(3), (7)",
        "exhibits": ["Ex-B", "Ex-K", "Ex-O"],
        "depends": [],
    },
    {
        "id": "CLM-03",
        "category": "parenting-time",
        "status": "corroborated",
        "title": "Zero Tardies & Academic Excellence During 2030 90-Day 50/50 Period",
        "statement": "Certified school attendance records (Ex. K) prove that during the 90-day equal 50/50 schedule in early 2030, all three dependents had zero tardies and strong academic evaluations.",
        "summary": "Certified school records confirm zero tardies and high academic performance during the 90-day 50/50 schedule.",
        "statutory": "Uniform Domestic Relations Act § 402(a)(4)",
        "exhibits": ["Ex-B", "Ex-K", "Ex-L"],
        "depends": [],
    },
    {
        "id": "CLM-04",
        "category": "parenting-time",
        "status": "stipulated",
        "title": "School-Zone Residential Proximity Enables Seamless Exchanges",
        "statement": "Both parents reside within the same suburban school district attendance zone (10 minutes apart), enabling conflict-free curb exchanges at school.",
        "summary": "Stipulated 10-minute proximity within the school district supports week-on/week-off school exchanges.",
        "statutory": "Uniform Domestic Relations Act § 402(a)(4), (8)",
        "exhibits": ["Ex-L", "Ex-O"],
        "depends": [],
    },
    {
        "id": "CLM-05",
        "category": "decision-making",
        "status": "corroborated",
        "title": "Joint Major Decision-Making with Mediation-First Protocol",
        "statement": "Six years of cooperative educational and medical choices plus neutral portal communication support joint major decision-making with mediation prior to court intervention (Ex. L).",
        "summary": "Historical cooperation on education and health care supports joint major decision-making with mediation first.",
        "statutory": "Uniform Domestic Relations Act § 402(b)(1)–(3)",
        "exhibits": ["Ex-A", "Ex-B", "Ex-D", "Ex-L"],
        "depends": ["CLM-06"],
    },
    {
        "id": "CLM-06",
        "category": "decision-making",
        "status": "corroborated",
        "title": "Early Completion of Certified Co-Parenting & Communication Seminar",
        "statement": "Respondent completed the 16-hour certified Co-Parenting & Communication Seminar on June 1, 2030—30 days ahead of the judicial deadline (Ex. D).",
        "summary": "Completed 16-hour certified co-parenting seminar 30 days ahead of schedule.",
        "statutory": "Uniform Domestic Relations Act § 402(a)(6), (9)",
        "exhibits": ["Ex-D"],
        "depends": [],
    },
    {
        "id": "CLM-07",
        "category": "child-support",
        "status": "stipulated",
        "title": "Stipulated Monthly Income Baseline ($8,000 Petitioner / $5,000 Respondent)",
        "statement": "In the Joint Pretrial Stipulation (¶ 14), the parties stipulated to monthly gross incomes of $8,000.00/mo ($800,000 cents) for Petitioner and $5,000.00/mo ($500,000 cents) for Respondent.",
        "summary": "Pretrial Stipulation fixes monthly income baseline at $8,000.00/mo Petitioner and $5,000.00/mo Respondent ($13,000.00/mo combined).",
        "statutory": "Uniform Support Guidelines § 305(2)",
        "exhibits": ["Ex-E", "Ex-I", "Ex-N"],
        "depends": [],
    },
    {
        "id": "CLM-08",
        "category": "child-support",
        "status": "corroborated",
        "title": "Guideline Support Transfer Is $250.00/mo from Petitioner to Respondent",
        "statement": "Applying the $13,000.00/mo combined baseline, 182.5 equal overnights, and $0 medical/childcare add-ons on Worksheet Ex. N yields a net guideline transfer of $250.00/mo ($25,000 cents) from Petitioner to Respondent.",
        "summary": "Guideline Worksheet Ex. N establishes a $250.00/mo net transfer from Petitioner to Respondent.",
        "statutory": "Uniform Support Guidelines § 305(8)",
        "exhibits": ["Ex-E", "Ex-N"],
        "depends": ["CLM-01", "CLM-07", "CLM-09", "CLM-11", "CLM-12"],
    },
    {
        "id": "CLM-09",
        "category": "child-support",
        "status": "corroborated",
        "title": "Statutory Disability Pension Exemption Bars Speculative Wage Imputation",
        "statement": "Under Uniform Support Guidelines § 305(5)(b), Respondent's certified permanent disability pension determination (Ex. E) bars imputing speculative commercial engineering wages.",
        "summary": "Certified permanent disability retirement determination (Ex. E) bars speculative income imputation under § 305(5)(b).",
        "statutory": "Uniform Support Guidelines § 305(5)(b)",
        "exhibits": ["Ex-E", "Ex-I", "Ex-N"],
        "depends": [],
    },
    {
        "id": "CLM-10",
        "category": "child-support",
        "status": "corroborated",
        "title": "Open-Source Civic Software Research Generated $0 Compensation (2026–2029 Taxes)",
        "statement": "Certified IRS Tax Return Transcripts for 2026, 2027, 2028, and 2029 (Ex. I) prove Respondent received $0 in gross revenue, salary, or distributions from open-source civic software projects.",
        "summary": "Four years of certified IRS transcripts (2026–2029, Ex. I) confirm $0 income from open-source civic software contributions.",
        "statutory": "Uniform Support Guidelines § 305(3) & FRE 803(8)",
        "exhibits": ["Ex-I", "Ex-N"],
        "depends": [],
    },
    {
        "id": "CLM-11",
        "category": "child-support",
        "status": "corroborated",
        "title": "Comprehensive Statutory Dependent Medical Benefit Eliminates $180/mo Duplicate Add-On",
        "statement": "All three dependents are enrolled in Respondent's statutory public-service dependent medical plan at $0 monthly premium (Ex. E), eliminating Petitioner's $180.00/mo duplicate insurance add-on on OP Ex. 2.",
        "summary": "Statutory $0-premium dependent medical coverage (Ex. E) eliminates the $180/mo duplicate insurance add-on.",
        "statutory": "38 U.S.C. § 1781 & Support Guidelines § 305(9)",
        "exhibits": ["Ex-E", "Ex-N", "OP-Ex-02"],
        "depends": [],
    },
    {
        "id": "CLM-12",
        "category": "child-support",
        "status": "corroborated",
        "title": "Full-Time Parental Availability Eliminates $1,500/mo Third-Party After-School Vendor Add-On",
        "statement": "Respondent is available full-time before and after school and during Petitioner's regional travel shifts (Ex. L), eliminating the unnecessary $1,500/mo ($450/mo worksheet share) commercial after-school agency expense.",
        "summary": "Direct parental care availability (Ex. L) eliminates the $1,500/mo ($450/mo worksheet share) commercial vendor add-on.",
        "statutory": "Uniform Support Guidelines § 305(9)(a) & § 402(a)(9)",
        "exhibits": ["Ex-E", "Ex-L", "Ex-N", "OP-Ex-02", "OP-Ex-08"],
        "depends": [],
    },
    {
        "id": "CLM-13",
        "category": "financial-disclosure",
        "status": "corroborated",
        "title": "Petitioner Omitted $30,000.00 in Escrow Accounts x4102 & x4109 on Initial Disclosure",
        "statement": "Comparison of Petitioner's June 10, 2029 Sworn Financial Statement (Ex. G) with subpoenaed bank statements (Ex. H) proves Petitioner omitted $30,000.00 ($3,000,000 cents) held in Escrow Checking x4102 and Reserve Savings x4109.",
        "summary": "Subpoenaed bank statements (Ex. H) prove $30,000.00 in liquid escrow funds was omitted from the June 10, 2029 Sworn Financial Statement (Ex. G).",
        "statutory": "FRCP 26(e) & Civil Rule 16.2(e)(10)",
        "exhibits": ["Ex-G", "Ex-H", "Ex-J", "Ex-N"],
        "depends": [],
    },
    {
        "id": "CLM-14",
        "category": "financial-disclosure",
        "status": "corroborated",
        "title": "Rule 16.2(e)(10) Bars Petitioner's Retroactive Support & Expense Reimbursement Demand",
        "statement": "Because Petitioner omitted $30,000.00 in liquid reserves while claiming financial hardship during interim proceedings, Civil Rule 16.2(e)(10) bars retroactive expense shifting (Ex. G, Ex. H, Ex. J, Ex. N ¶¶ 24–26).",
        "summary": "Material omission of $30,000.00 on the Sworn Financial Statement bars retroactive support and expense claims under Rule 16.2(e)(10).",
        "statutory": "Civil Rule 16.2(e)(10)",
        "exhibits": ["Ex-G", "Ex-H", "Ex-J", "Ex-N", "OP-Ex-11"],
        "depends": ["CLM-13"],
    },
    {
        "id": "CLM-15",
        "category": "impeachment",
        "status": "corroborated",
        "title": "FRE 106 Rule of Completeness Rebuts Selective Excerpt from 2028 Homework Study Log",
        "statement": "Under FRE 106, page 4 lines 10–24 of the 2028 Co-Parenting & Homework Study Log (OP Ex. 13, dated October 12, 2028) proves both parents jointly agreed on calm, non-punitive homework tutoring and positive reinforcement.",
        "summary": "Full context of the 2028 Homework Study Log (OP Ex. 13, p. 4) under FRE 106 confirms calm, positive parenting.",
        "statutory": "FRE 106 (Rule of Completeness)",
        "exhibits": ["Ex-D", "OP-Ex-13"],
        "depends": [],
    },
    {
        "id": "CLM-16",
        "category": "impeachment",
        "status": "corroborated",
        "title": "FRE 106 Complete Portal Thread Proves Respectful Co-Parenting & Dependent Preference",
        "statement": "Admitting the complete 6-page co-parenting portal thread (OP Ex. 14, Ex. B) under FRE 106 shows Respondent calmly coordinating schedules and the 15-year-old asking to resume the 50/50 rotation.",
        "summary": "Complete portal message thread (Ex. B, OP Ex. 14) under FRE 106 disproves hostile-communication allegations.",
        "statutory": "FRE 106 & Uniform Act § 402(a)(2), (6)",
        "exhibits": ["Ex-A", "Ex-B", "OP-Ex-05", "OP-Ex-14"],
        "depends": [],
    },
    {
        "id": "CLM-17",
        "category": "impeachment",
        "status": "corroborated",
        "title": "Collateral Relative Witnesses Lack Post-2028 Personal Knowledge Under FRE 602",
        "statement": "Opposing lay witnesses W-07, W-08, and W-09 admit they have not visited Respondent's residence or observed his parenting since 2028, limiting their testimony under FRE 602 and FRE 802.",
        "summary": "Opposing collateral witnesses lack post-2028 personal observation under FRE 602.",
        "statutory": "FRE 602 & FRE 802",
        "exhibits": ["Ex-B", "Ex-K", "Ex-O"],
        "depends": [],
    },
    {
        "id": "CLM-18",
        "category": "protection-order",
        "status": "corroborated",
        "title": "Verified 500-Yard School-Zone Transit Log Proves Full Buffer Compliance",
        "statement": "Certified school check-in badge logs and transit telemetry (Ex. F, Ex. M) prove Respondent remained 512 yards from Petitioner's residence on the public arterial avenue during routine school drop-off.",
        "summary": "Certified transit telemetry (512 yards, Ex. F) proves strict compliance with the 250-yard interim buffer.",
        "statutory": "FRE 901(b)(9) & Uniform Act § 402(a)(9)",
        "exhibits": ["Ex-F", "Ex-L", "Ex-M", "OP-Ex-06", "OP-Ex-07"],
        "depends": [],
    },
    {
        "id": "CLM-19",
        "category": "protection-order",
        "status": "stipulated",
        "title": "October 1, 2029 Stipulated Dismissal With Prejudice of Interim Restriction Motion",
        "statement": "On October 1, 2029, Petitioner stipulated to dismiss her interim restriction motion with prejudice (Ex. C) in exchange for neutral civil standby/school-curb exchange protocols.",
        "summary": "Prior restriction motion was dismissed with prejudice by stipulation on October 1, 2029 (Ex. C).",
        "statutory": "Doctrine of Issue Preclusion & Stipulation (Ex. C)",
        "exhibits": ["Ex-C", "Ex-F", "Ex-L"],
        "depends": [],
    },
    {
        "id": "CLM-20",
        "category": "parenting-time",
        "status": "corroborated",
        "title": "First Right of Refusal During Multi-Day Regional Logistics Travel Shifts",
        "statement": "When Petitioner travels on multi-day regional logistics shifts, the Proposed Parenting Plan (Ex. L § 4.3) grants Respondent the first right of refusal so the dependents stay with a parent rather than a commercial vendor.",
        "summary": "Right of first refusal during multi-day travel shifts keeps dependents with a parent at zero cost (Ex. L).",
        "statutory": "Uniform Domestic Relations Act § 402(a)(3), (9)",
        "exhibits": ["Ex-B", "Ex-L", "OP-Ex-03"],
        "depends": ["CLM-01", "CLM-12"],
    },
    {
        "id": "CLM-21",
        "category": "parenting-time",
        "status": "corroborated",
        "title": "Suburban Single-Family Residence With Dedicated Bedrooms & Study Space",
        "statement": "Photographic and property records (Ex. O) establish that Respondent's suburban residence inside the school district provides dedicated bedrooms, study desks, and a fenced yard 8 minutes from school.",
        "summary": "Property and photo records (Ex. O) confirm a stable, well-equipped home 8 minutes from school.",
        "statutory": "Uniform Domestic Relations Act § 402(a)(4)",
        "exhibits": ["Ex-K", "Ex-L", "Ex-O"],
        "depends": [],
    },
    {
        "id": "CLM-22",
        "category": "financial-disclosure",
        "status": "corroborated",
        "title": "Equitable Credit for Unilateral Joint-Account Withdrawal ($6,400.00)",
        "statement": "Certified joint checking statements (Ex. J) document Petitioner's unilateral $6,400.00 withdrawal on August 28, 2029, entitling Respondent to an equitable offset.",
        "summary": "Joint bank ledger (Ex. J) proves unilateral $6,400.00 withdrawal on August 28, 2029.",
        "statutory": "Uniform Marital Property & Equitable Offset Principles",
        "exhibits": ["Ex-G", "Ex-H", "Ex-J", "Ex-N"],
        "depends": ["CLM-13"],
    },
    {
        "id": "CLM-23",
        "category": "decision-making",
        "status": "corroborated",
        "title": "Equal Statutory Access to School, Medical & Extracurricular Portals (§ 408)",
        "statement": "Under Uniform Domestic Relations Act § 408, both parents hold equal statutory access to all academic, medical, dental, and extracurricular records regardless of residential schedule.",
        "summary": "Uniform Act § 408 guarantees both parents equal access to all school and medical portals.",
        "statutory": "Uniform Domestic Relations Act § 408",
        "exhibits": ["Ex-B", "Ex-K", "Ex-L"],
        "depends": [],
    },
    {
        "id": "CLM-24",
        "category": "parenting-time",
        "status": "contested",
        "title": "Rebuttal of Proposed 90-Overnight Restriction as Unsupported by Statutory Factors",
        "statement": "Petitioner's proposal to cut Respondent to 90 overnights/year (OP Ex. 1) is contradicted by the 2030 zero-tardy school record (Ex. K), 6-year caregiving history (Ex. B), and 512-yard transit verification (Ex. F).",
        "summary": "Proposed 90-overnight cut (OP Ex. 1) is refuted across all 11 statutory best-interests factors.",
        "statutory": "Uniform Domestic Relations Act § 402(a)(1)–(11)",
        "exhibits": ["Ex-B", "Ex-F", "Ex-K", "Ex-L", "Ex-O", "OP-Ex-01"],
        "depends": ["CLM-01", "CLM-02", "CLM-03", "CLM-18"],
    },
]

RESPONDENT_EXHIBITS = [
    {
        "id": "Ex-A",
        "label": "Exhibit A",
        "title": "Co-Parenting Portal Communication Summary & Response-Time Audit (2029–2030)",
        "category": "Co-Parenting Communications",
        "statutory": "Uniform Domestic Relations Act § 402(a)(6), (11)",
        "status": "stipulated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-A-Portal-Audit.pdf",
        "purpose": "Demonstrates Respondent's 100% calm, child-focused written communication and timely scheduling coordination.",
    },
    {
        "id": "Ex-B",
        "label": "Exhibit B",
        "title": "Verified 2023–2030 Caregiving Calendar, Medical Transport & 2028 Solo-Parenting Log",
        "category": "Parenting History",
        "statutory": "Uniform Domestic Relations Act § 402(a)(3), (7)",
        "status": "corroborated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-B-Caregiving-Log.pdf",
        "purpose": "Documents 6 years of hands-on parenting, 2028 4-month solo caregiving during Petitioner's regional assignment, and the 2030 90-day 50/50 rotation.",
    },
    {
        "id": "Ex-C",
        "label": "Exhibit C",
        "title": "October 1, 2029 Stipulated Dismissal With Prejudice of Interim Restriction Motion",
        "category": "Court Orders & Stipulations",
        "statutory": "Issue Preclusion & Pretrial Stipulation",
        "status": "stipulated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-C-Stipulated-Dismissal.pdf",
        "purpose": "Establishes that prior interim restriction allegations were voluntarily dismissed with prejudice in favor of neutral school-curb exchanges.",
    },
    {
        "id": "Ex-D",
        "label": "Exhibit D",
        "title": "Certified 16-Hour Co-Parenting & Conflict-Resolution Seminar Completion Certificate (June 1, 2030)",
        "category": "Compliance & Training",
        "statutory": "Uniform Domestic Relations Act § 402(a)(5), (6), (9)",
        "status": "stipulated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-D-Seminar-Certificate.pdf",
        "purpose": "Proves Respondent completed the court-ordered 16-hour co-parenting seminar 30 days ahead of the judicial deadline.",
    },
    {
        "id": "Ex-E",
        "label": "Exhibit E",
        "title": "Certified Public-Service Disability Pension Award ($5,000/mo) & $0-Premium Dependent Medical Plan",
        "category": "Income & Benefits Verification",
        "statutory": "Uniform Support Guidelines § 305(5)(b) & 38 U.S.C. § 1781",
        "status": "stipulated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-E-Pension-And-Medical.pdf",
        "purpose": "Verifies Respondent's $5,000.00/mo statutory disability pension, bars speculative wage imputation under § 305(5)(b), and proves $0-premium dependent health coverage.",
    },
    {
        "id": "Ex-F",
        "label": "Exhibit F",
        "title": "Certified School Check-In Badge & Arterial Transit Telemetry Log (512 Yards Distance)",
        "category": "Order Compliance Telemetry",
        "statutory": "FRE 901(b)(9) & Uniform Act § 402(a)(9)",
        "status": "corroborated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-F-Transit-Telemetry.pdf",
        "purpose": "Proves Respondent remained 512 yards from Petitioner's residence on the public arterial avenue while completing routine school drop-off.",
    },
    {
        "id": "Ex-G",
        "label": "Exhibit G",
        "title": "Petitioner's Initial Sworn Financial Statement (Filed June 10, 2029)",
        "category": "Financial Disclosure",
        "statutory": "FRCP 26(e) & Civil Rule 16.2(e)",
        "status": "stipulated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-G-Initial-SFS.pdf",
        "purpose": "Establishes that Petitioner swore under oath she held $0 in secondary escrow or reserve accounts on June 10, 2029.",
    },
    {
        "id": "Ex-H",
        "label": "Exhibit H",
        "title": "Subpoenaed Statements for Escrow Checking x4102 & Reserve Savings x4109 ($30,000.00 Balance)",
        "category": "Financial Disclosure Audit",
        "statutory": "Civil Rule 16.2(e)(10) & FRE 803(6)",
        "status": "corroborated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-H-Escrow-Statements.pdf",
        "purpose": "Proves Petitioner held $30,000.00 ($3,000,000 cents) in undisclosed liquid funds on the exact date she signed Exhibit G.",
    },
    {
        "id": "Ex-I",
        "label": "Exhibit I",
        "title": "Certified IRS Tax Return Transcripts (2026, 2027, 2028 & 2029 — $0 Civic Software Revenue)",
        "category": "Tax & Income Verification",
        "statutory": "Uniform Support Guidelines § 305(3) & FRE 803(8)",
        "status": "stipulated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-I-Tax-Transcripts.pdf",
        "purpose": "Proves Respondent earned $0 in commercial revenue or draws from open-source civic software contributions across 2026–2029.",
    },
    {
        "id": "Ex-J",
        "label": "Exhibit J",
        "title": "Joint Household Checking Reconciliation & August 28, 2029 $6,400.00 Withdrawal Audit",
        "category": "Financial Accounting",
        "statutory": "FRE 1006 & Civil Rule 16.2",
        "status": "corroborated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-J-Joint-Account-Audit.pdf",
        "purpose": "Documents Petitioner's unilateral $6,400.00 withdrawal from joint household funds immediately prior to separation.",
    },
    {
        "id": "Ex-K",
        "label": "Exhibit K",
        "title": "Certified School District Attendance, Grade & Zero-Tardy Records (2028–2030)",
        "category": "Educational Records",
        "statutory": "Uniform Domestic Relations Act § 402(a)(4), (7) & FRE 803(6)",
        "status": "stipulated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-K-School-Records.pdf",
        "purpose": "Confirms zero tardies, 100% homework completion, and honor-roll standing during Respondent's caregiving blocks and the 2030 50/50 period.",
    },
    {
        "id": "Ex-L",
        "label": "Exhibit L",
        "title": "Respondent's Proposed Equal 50/50 Parenting Plan & Joint Governance Protocol",
        "category": "Proposed Court Orders",
        "statutory": "Uniform Domestic Relations Act § 402(a)–(b)",
        "status": "corroborated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-L-Proposed-Parenting-Plan.pdf",
        "purpose": "Sets forth the week-on/week-off schedule (182.5 overnights each), Wednesday school-curb exchanges, right of first refusal during travel shifts, and mediation-first joint decision-making.",
    },
    {
        "id": "Ex-M",
        "label": "Exhibit M",
        "title": "Municipal Subdivision Map & School-Route Corridor Diagram (512-Yard Buffer Proof)",
        "category": "Demonstrative Map",
        "statutory": "FRE 901 & FRE 1006",
        "status": "corroborated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-M-Corridor-Map.pdf",
        "purpose": "Visually plots the school drop-off arterial corridor and confirms the 512-yard separation distance recorded in Exhibit F.",
    },
    {
        "id": "Ex-N",
        "label": "Exhibit N",
        "title": "Verified Guideline Child Support Worksheet ($250.00/mo Petitioner -> Respondent) & Rule 16.2 Brief",
        "category": "Support Guidelines Worksheet",
        "statutory": "Uniform Support Guidelines § 305 & Civil Rule 16.2(e)(10)",
        "status": "corroborated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-N-Guideline-Worksheet.pdf",
        "purpose": "Computes the exact $250.00/mo ($25,000 cents) guideline transfer at 182.5 equal overnights on the stipulated $8,000/$5,000 baseline.",
    },
    {
        "id": "Ex-O",
        "label": "Exhibit O",
        "title": "Suburban Residence Photographs, Bedrooms, Study Desks & Family Activities Portfolio",
        "category": "Home Environment & Caregiving",
        "statutory": "Uniform Domestic Relations Act § 402(a)(3), (4)",
        "status": "stipulated",
        "file": "vault://exhibits/2030-FAM-9010/Ex-O-Residence-Photos.pdf",
        "purpose": "Shows dedicated bedrooms, homework stations, and active caregiving in Respondent's residence 8 minutes from school.",
    },
]

PETITIONER_EXHIBITS = [
    {
        "id": "OP-Ex-01",
        "label": "OP Exhibit 1",
        "title": "Petitioner's Proposed Parenting Plan (90 Overnights / Alternating Weekends)",
        "category": "Opposing Proposed Orders",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-01-Proposed-Plan.pdf",
        "motherUse": "Seeks to reduce Respondent to 90 overnights/year (24.7%) and grant Petitioner sole decision-making.",
        "fatherPivot": "Refuted by 6 years of primary caregiving (Ex. B), zero tardies during the 2030 50/50 rotation (Ex. K), and full daytime availability (Ex. E).",
    },
    {
        "id": "OP-Ex-02",
        "label": "OP Exhibit 2",
        "title": "Petitioner's Proposed Support Worksheet ($750.00/mo Respondent -> Petitioner)",
        "category": "Opposing Support Worksheet",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-02-Support-Worksheet.pdf",
        "motherUse": "Claims Respondent owes $750.00/mo by assuming 90 overnights, a $180/mo medical add-on, and a $450/mo commercial vendor add-on.",
        "fatherPivot": "Defeated by Ex. N ($250.00/mo to Respondent at 182.5 overnights), $0-premium dependent medical coverage (Ex. E), and free parental care during travel shifts (Ex. L).",
    },
    {
        "id": "OP-Ex-03",
        "label": "OP Exhibit 3",
        "title": "Petitioner's Regional Logistics Travel & Shift Calendar (2029–2030)",
        "category": "Employment Schedule",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-03-Travel-Schedule.pdf",
        "motherUse": "Offered to justify hiring a $1,500/mo commercial after-school care agency during Petitioner's multi-day regional travel shifts.",
        "fatherPivot": "Proves why equal 50/50 parenting time and right of first refusal (Ex. L § 4.3) are essential so the dependents stay with Respondent rather than commercial strangers.",
    },
    {
        "id": "OP-Ex-04",
        "label": "OP Exhibit 4",
        "title": "Petitioner's Amended Financial Statement (FiledMay 2030)",
        "category": "Financial Disclosure",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-04-Amended-SFS.pdf",
        "motherUse": "Attempts to cure the June 10, 2029 omission after Respondent subpoenaed bank records.",
        "fatherPivot": "Confirms that the $30,000.00 in accounts x4102 and x4109 was only disclosed after subpoena production (Ex. H), triggering Rule 16.2(e)(10).",
    },
    {
        "id": "OP-Ex-05",
        "label": "OP Exhibit 5",
        "title": "Selected Co-Parenting Portal Screenshots (Cropped Logistics Thread)",
        "category": "Communications",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-05-Cropped-Portal.pdf",
        "motherUse": "Cites isolated scheduling messages to argue communication friction.",
        "fatherPivot": "Under FRE 106, the complete unredacted portal log (Ex. A, Ex. B) shows Respondent politely offering three alternative exchange times.",
    },
    {
        "id": "OP-Ex-06",
        "label": "OP Exhibit 6",
        "title": "Motion Regarding Arterial Avenue Proximity (Filed April 2030)",
        "category": "Interim Pleadings",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-06-Proximity-Motion.pdf",
        "motherUse": "Alleges Respondent drove too close to Petitioner's neighborhood during a morning school drop-off.",
        "fatherPivot": "Refuted by certified transit telemetry and school check-in logs (Ex. F, Ex. M) proving Respondent was 512 yards away on the main school arterial.",
    },
    {
        "id": "OP-Ex-07",
        "label": "OP Exhibit 7",
        "title": "Driveway Camera Still Frame of Arterial Intersection",
        "category": "Photographs",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-07-Intersection-Photo.pdf",
        "motherUse": "Shows a vehicle on the distant arterial collector road.",
        "fatherPivot": "Cross-referenced with Ex. F and Ex. M to confirm the intersection is 512 yards from Petitioner's home on the direct route to the Elementary Academy.",
    },
    {
        "id": "OP-Ex-08",
        "label": "OP Exhibit 8",
        "title": "Commercial After-School Care Agency Brochure & Rate Sheet ($1,500/mo)",
        "category": "Childcare Invoice",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-08-Vendor-Brochure.pdf",
        "motherUse": "Supports request for a $450/mo worksheet add-on for third-party after-school care.",
        "fatherPivot": "Unnecessary under § 305(9)(a) because Respondent lives 8 minutes from school and provides direct parental care at $0 cost (Ex. E, Ex. L).",
    },
    {
        "id": "OP-Ex-09",
        "label": "OP Exhibit 9",
        "title": "Employer Health Plan Summary ($180/mo Optional Dependent Rider)",
        "category": "Insurance Records",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-09-Employer-Health.pdf",
        "motherUse": "Seeks $180/mo credit for optional employer dependent coverage.",
        "fatherPivot": "Duplicate expense: all three dependents already have comprehensive statutory medical coverage through Respondent at $0 monthly premium (Ex. E).",
    },
    {
        "id": "OP-Ex-10",
        "label": "OP Exhibit 10",
        "title": "Public Git Repository Commit Log Printouts (2028–2029)",
        "category": "Imputation Allegation",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-10-Git-Printout.pdf",
        "motherUse": "Suggests Respondent's open-source civic software commits represent a commercial consulting business.",
        "fatherPivot": "Certified 2026–2029 IRS tax transcripts (Ex. I) prove $0 gross revenue; open-source civic research is uncompensated community service, and § 305(5)(b) bars imputation (Ex. E).",
    },
    {
        "id": "OP-Ex-11",
        "label": "OP Exhibit 11",
        "title": "Interim Household Expense Summary Spreadsheet (Unverified)",
        "category": "Financial Summary",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-11-Expense-Sheet.pdf",
        "motherUse": "Requests retroactive reimbursement of interim household expenses.",
        "fatherPivot": "Barred by Civil Rule 16.2(e)(10) due to Petitioner's omission of $30,000.00 in accounts x4102/x4109 (Ex. G, Ex. H) and offset by her unilateral $6,400.00 withdrawal (Ex. J).",
    },
    {
        "id": "OP-Ex-12",
        "label": "OP Exhibit 12",
        "title": "Suburban Residence Listing & Deed Printout",
        "category": "Real Property",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-12-Property-Deed.pdf",
        "motherUse": "Questions residential lease/ownership terms of Respondent's suburban home.",
        "fatherPivot": "Corroborates Ex. O: confirms Respondent's long-term residential stability inside the dependents' school attendance zone.",
    },
    {
        "id": "OP-Ex-13",
        "label": "OP Exhibit 13",
        "title": "2028 Handwritten Co-Parenting & Homework Study Log (12 Pages)",
        "category": "Handwritten Notebook",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-13-Homework-Notebook.pdf",
        "motherUse": "Selectively quotes a single line from page 4 regarding firm weeknight screen-time limits to allege overly strict rules.",
        "fatherPivot": "Under FRE 106 Rule of Completeness, page 4 lines 10–24 (October 12, 2028) proves both parents jointly agreed on calm homework tutoring, patience, and positive reinforcement.",
    },
    {
        "id": "OP-Ex-14",
        "label": "OP Exhibit 14",
        "title": "Family Group Message Thread Export (6 Pages, Spring 2030)",
        "category": "Text Messages",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-14-Group-Thread.pdf",
        "motherUse": "Cites a single message where the 15-year-old asked about schedule changes.",
        "fatherPivot": "Under FRE 106, pages 1–6 show the 15-year-old asking 'When do we get our 50/50 week-on/week-off schedule back?' and Respondent encouraging respect for both parents.",
    },
    {
        "id": "OP-Ex-15",
        "label": "OP Exhibit 15",
        "title": "Extracurricular Activity Registration Receipts (2029–2030)",
        "category": "Activity Records",
        "file": "vault://exhibits/2030-FAM-9010/OP-Ex-15-Activity-Receipts.pdf",
        "motherUse": "Offered to show Petitioner registered the dependents for youth sports.",
        "fatherPivot": "Ex. B and Ex. O show Respondent coached and transported the dependents to 85% of practices and games across 2028–2030.",
    },
]

WITNESSES = [
    {
        "id": "W-01",
        "name": "Respondent Co-Parent (Party B)",
        "relationship": "Respondent / Proponent Party",
        "party": "Respondent",
        "callStatus": "will-call",
        "scope": "Testifies to 6-year hands-on caregiving, 2028 solo parenting, 2030 zero-tardy 50/50 rotation, seminar completion, 512-yard transit log, and $250/mo guideline worksheet.",
        "keyPoints": [
            "Walk through all 6 Opening Statement pillars calmly with documentary anchors (Ex. A–Ex. O).",
            "Authenticate the 2028–2030 caregiving log (Ex. B), seminar certificate (Ex. D), and 512-yard transit telemetry (Ex. F).",
            "Invoke FRE 106 completeness on the 2028 Homework Study Log (OP Ex. 13 p. 4) and family message thread (OP Ex. 14).",
        ],
    },
    {
        "id": "W-02",
        "name": "Petitioner Co-Parent (Party A)",
        "relationship": "Petitioner / Adverse Party",
        "party": "Petitioner",
        "callStatus": "will-call",
        "scope": "Cross-examination on Pretrial Stipulations, 2028 4-month regional travel rotation, zero tardies during 2030 50/50 schedule, and omission of $30,000.00 on June 10, 2029 SFS.",
        "keyPoints": [
            "Lock in Pretrial Stipulation ¶ 14 ($8,000/mo vs. $5,000/mo income baseline) and 10-minute school-zone proximity.",
            "Confirm zero school tardies during the 90-day equal 50/50 schedule in early 2030 (Ex. K).",
            "Impeach under Civil Rule 16.2(e)(10) using June 10, 2029 SFS (Ex. G) vs. subpoenaed Escrow Statements showing $30,000.00 in x4102/x4109 (Ex. H).",
        ],
    },
    {
        "id": "W-03",
        "name": "School District Attendance & Records Coordinator",
        "relationship": "Neutral School Official",
        "party": "Respondent",
        "callStatus": "will-call",
        "scope": "Authenticates certified school attendance records (Ex. K), check-in badge logs (Ex. F), and Respondent's consistent participation in parent-teacher conferences.",
        "keyPoints": [
            "Confirm zero tardies and strong academic standing during Respondent's parenting weeks (Ex. K).",
            "Confirm Respondent's routine morning drop-off check-in logs (Ex. F).",
        ],
    },
    {
        "id": "W-04",
        "name": "Neighborhood Youth STEM & Athletics Coach",
        "relationship": "Neutral Community Witness",
        "party": "Respondent",
        "callStatus": "will-call",
        "scope": "Testifies to Respondent's calm, supportive involvement at weekly STEM robotics sessions and youth soccer practices from 2027 through 2030.",
        "keyPoints": [
            "Observed Respondent transporting and mentoring the dependents twice weekly for three years.",
            "Confirmed positive, patient interaction between Respondent and all three dependents (Ex. O).",
        ],
    },
    {
        "id": "W-05",
        "name": "Certified Co-Parenting Seminar Facilitator",
        "relationship": "Course Instructor (May-Call)",
        "party": "Respondent",
        "callStatus": "may-call",
        "scope": "Authenticates Respondent's June 1, 2030 completion certificate (Ex. D) 30 days ahead of the judicial deadline.",
        "keyPoints": [
            "Confirm 16-hour curriculum covering low-conflict school exchanges and parallel/cooperative scheduling (Ex. D).",
        ],
    },
    {
        "id": "W-06",
        "name": "Independent CPA & Financial Audit Specialist",
        "relationship": "Financial Reconciliation Witness (May-Call)",
        "party": "Respondent",
        "callStatus": "may-call",
        "scope": "Explains the FRE 1006 tie-out between Petitioner's June 10, 2029 SFS (Ex. G), subpoenaed bank statements showing $30,000.00 in x4102/x4109 (Ex. H), and 2026–2029 tax transcripts (Ex. I).",
        "keyPoints": [
            "Verify $30,000.00 omitted balance across Escrow Checking x4102 and Reserve Savings x4109 on June 10, 2029 (Ex. H).",
            "Verify $0 commercial revenue on 2026–2029 IRS Tax Return Transcripts (Ex. I).",
        ],
    },
    {
        "id": "W-07",
        "name": "Out-of-Area Relative Fact Witness A",
        "relationship": "Petitioner's Extended Relative",
        "party": "Petitioner",
        "callStatus": "may-call",
        "scope": "Opposing lay witness; cross-examination establishes lack of personal observation of Respondent's home since 2028 under FRE 602.",
        "keyPoints": [
            "Establish under FRE 602 that witness resides out of area and has not observed Respondent parenting since 2028.",
            "Exclude repetition of Petitioner's out-of-court statements as hearsay under FRE 802.",
        ],
    },
    {
        "id": "W-08",
        "name": "Out-of-Area Relative Fact Witness B",
        "relationship": "Petitioner's Secondary Relative",
        "party": "Petitioner",
        "callStatus": "may-call",
        "scope": "Opposing lay witness; cross-examination confirms Respondent handled 100% of daily parenting during Petitioner's 2028 4-month regional assignment.",
        "keyPoints": [
            "Confirm Respondent cared for all three dependents solo during the 2028 4-month rotation without incident (Ex. B, Ex. K).",
        ],
    },
    {
        "id": "W-09",
        "name": "Collateral Acquaintance Witness",
        "relationship": "Petitioner's Social Acquaintance",
        "party": "Petitioner",
        "callStatus": "may-call",
        "scope": "Opposing lay witness; cross-examination limits testimony to personal knowledge under FRE 602.",
        "keyPoints": [
            "Confirm zero first-hand observation of the 2030 90-day 50/50 schedule or Wednesday school exchanges.",
        ],
    },
    {
        "id": "W-10",
        "name": "Commercial After-School Program Administrator",
        "relationship": "Third-Party Vendor Representative",
        "party": "Petitioner",
        "callStatus": "may-call",
        "scope": "Cross-examination confirms the $1,500/mo commercial contract is optional and unnecessary when a parent is available at dismissal.",
        "keyPoints": [
            "Confirm no cancellation penalty applies when a parent picks up the dependents directly from school at dismissal (Ex. L).",
        ],
    },
]

TIMELINE = [
    {
        "id": "TL-01",
        "date": "2023-09-01",
        "title": "Six-Year Primary Hands-On Parenting Routine Begins",
        "summary": "Respondent manages daily school drop-offs, pickups, homework, and medical appointments for the dependents within the school district.",
        "exhibits": ["Ex-B", "Ex-K", "Ex-O"],
    },
    {
        "id": "TL-02",
        "date": "2027-04-15",
        "title": "Certified Public-Service Disability Pension & Dependent Medical Award",
        "summary": "Respondent receives statutory disability pension award ($5,000.00/mo baseline) and $0-premium comprehensive medical coverage for all three dependents.",
        "exhibits": ["Ex-E"],
    },
    {
        "id": "TL-03",
        "date": "2028-03-01",
        "title": "Four-Month Solo Parenting During Petitioner's Regional Logistics Rotation",
        "summary": "While Petitioner completes a 4-month out-of-region logistics assignment, Respondent handles 100% of daily caregiving, school, and activities with zero tardies.",
        "exhibits": ["Ex-B", "Ex-K", "Ex-O"],
    },
    {
        "id": "TL-04",
        "date": "2028-10-12",
        "title": "Joint Co-Parenting & Homework Study Log Entry (FRE 106 Anchor)",
        "summary": "Page 4 lines 10–24 of the 2028 Homework Study Log records both parents' agreement to use calm explanation, tutoring, and positive reinforcement.",
        "exhibits": ["OP-Ex-13"],
    },
    {
        "id": "TL-05",
        "date": "2029-04-15",
        "title": "2026–2029 IRS Tax Transcripts Confirm $0 Civic Software Revenue",
        "summary": "Certified IRS transcripts across four tax years confirm Respondent's open-source civic software contributions generated $0 commercial income.",
        "exhibits": ["Ex-I"],
    },
    {
        "id": "TL-06",
        "date": "2029-06-10",
        "title": "Petitioner Files Initial Sworn Financial Statement Omitting $30,000.00",
        "summary": "Petitioner signs Initial SFS under oath omitting Escrow Checking x4102 and Reserve Savings x4109 holding $30,000.00.",
        "exhibits": ["Ex-G", "Ex-H"],
    },
    {
        "id": "TL-07",
        "date": "2029-08-28",
        "title": "Unilateral $6,400.00 Withdrawal from Joint Household Account",
        "summary": "Joint bank statement audit documents Petitioner withdrawing $6,400.00 prior to physical separation.",
        "exhibits": ["Ex-J"],
    },
    {
        "id": "TL-08",
        "date": "2029-09-01",
        "title": "Physical Separation within Same School District Catchment",
        "summary": "Parties establish separate residences 10 minutes apart inside the same school district attendance zone.",
        "exhibits": ["Ex-L", "Ex-O"],
    },
    {
        "id": "TL-09",
        "date": "2029-10-01",
        "title": "Stipulated Dismissal With Prejudice of Interim Restriction Motion",
        "summary": "Petitioner stipulates to dismiss interim restriction motion with prejudice; parties adopt school-curb exchange protocol.",
        "exhibits": ["Ex-C", "Ex-L"],
    },
    {
        "id": "TL-10",
        "date": "2029-11-15",
        "title": "Subpoenaed Bank Production Exposes $30,000.00 Escrow Reserve",
        "summary": "Subpoenaed statements for x4102 and x4109 confirm $30,000.00 liquid balance on June 10, 2029.",
        "exhibits": ["Ex-G", "Ex-H", "Ex-N"],
    },
    {
        "id": "TL-11",
        "date": "2030-01-15",
        "title": "90-Day Equal 50/50 Week-On/Week-Off Schedule Commences",
        "summary": "Parties execute equal 50/50 parenting rotation with Wednesday school exchanges; dependents achieve zero tardies and honor-roll grades.",
        "exhibits": ["Ex-B", "Ex-K", "Ex-L"],
    },
    {
        "id": "TL-12",
        "date": "2030-04-10",
        "title": "512-Yard School Transit Telemetry & Badge Log Verified",
        "summary": "Certified school check-in and GPS transit log proves Respondent remained 512 yards from Petitioner's residence on the arterial avenue during morning drop-off.",
        "exhibits": ["Ex-F", "Ex-M"],
    },
    {
        "id": "TL-13",
        "date": "2030-05-12",
        "title": "Full Group Message Thread Confirms 15-Year-Old's Request for 50/50",
        "summary": "Unredacted 6-page message export records the oldest dependent asking to restore the equal 50/50 weekly schedule.",
        "exhibits": ["Ex-B", "OP-Ex-14"],
    },
    {
        "id": "TL-14",
        "date": "2030-06-01",
        "title": "Respondent Completes 16-Hour Co-Parenting Seminar 30 Days Early",
        "summary": "Certified completion of court-approved 16-hour co-parenting and communication course 30 days ahead of deadline.",
        "exhibits": ["Ex-D"],
    },
    {
        "id": "TL-15",
        "date": "2030-08-15",
        "title": "Joint Pretrial Stipulation & Guideline Support Worksheet Filed",
        "summary": "Parties stipulate to $8,000/mo vs. $5,000/mo income baseline and geographic proximity; Respondent files Ex. N ($250.00/mo transfer).",
        "exhibits": ["Ex-L", "Ex-N"],
    },
    {
        "id": "TL-16",
        "date": "2030-09-18",
        "title": "Final Evidentiary Hearing (360-Minute Homeostatic Trial Clock)",
        "summary": "Six-hour evidentiary hearing on equal 50/50 parenting time, joint decision-making, $250/mo guideline support, and Rule 16.2 audit.",
        "exhibits": ["Ex-A", "Ex-B", "Ex-E", "Ex-H", "Ex-K", "Ex-L", "Ex-N"],
    },
]


for _p in OPENING_PILLARS:
    _p.setdefault("doRules", [f"Anchor testimony in {', '.join(_p['exhibits'])} under {_p['statutory']}.", "Speak calmly, child-centrically, and cite exact dates and verified records."])
    _p.setdefault("dontRules", ["Do not speculate, argue with opposing counsel, or accept selective out-of-context premises."])

for _f in STATUTORY_FACTORS:
    _f.setdefault("statute", f"Uniform Domestic Relations Act {_f['section']}")
    _f.setdefault("fatherPosition", _f["proponentPosition"])
    _f.setdefault("motherPosition", _f["opposingPosition"])
    _f.setdefault("trialProof", f"Corroborated by {', '.join(_f['exhibits'])} ({_f['weight']})")

for _ex in RESPONDENT_EXHIBITS:
    _ex["claims"] = [c["id"] for c in CLAIMS if _ex["id"] in c["exhibits"]] or ["CLM-01"]


def all_exhibits():
    return [
        {**e, "party": "Respondent"} for e in RESPONDENT_EXHIBITS
    ] + [
        {**e, "party": "Petitioner", "status": "contested"} for e in PETITIONER_EXHIBITS
    ]


def all_exhibit_ids():
    return [e["id"] for e in RESPONDENT_EXHIBITS] + [e["id"] for e in PETITIONER_EXHIBITS]


def declarations():
    ben_t = named("Beneficiary")
    pil_t = named("OpeningPillar")
    fac_t = named("StatutoryFactor")
    clm_t = named("Claim")
    ex_t = named("Exhibit")
    wit_t = named("Witness")
    tl_t = named("TimelineEvent")

    all_exs = [
        {
            "id": e["id"],
            "label": e["label"],
            "party": "Respondent",
            "title": e["title"],
            "category": e["category"],
            "status": e["status"],
        }
        for e in RESPONDENT_EXHIBITS
    ] + [
        {
            "id": e["id"],
            "label": e["label"],
            "party": "Petitioner",
            "title": e["title"],
            "category": e["category"],
            "status": "contested",
        }
        for e in PETITIONER_EXHIBITS
    ]

    valid_statuses = ["stipulated", "corroborated", "contested"]

    return [
        structure("Beneficiary", [("id", STR), ("name", STR), ("dob", STR), ("age", NAT), ("grade", STR)]),
        structure("OpeningPillar", [("id", STR), ("title", STR), ("theme", STR), ("statutory", STR), ("exhibits", list_t(STR))]),
        structure("StatutoryFactor", [("id", STR), ("section", STR), ("title", STR), ("exhibits", list_t(STR))]),
        structure(
            "Claim",
            [
                ("id", STR),
                ("category", STR),
                ("status", STR),
                ("statutory", STR),
                ("statement", STR),
                ("exhibits", list_t(STR)),
                ("depends", list_t(STR)),
            ],
        ),
        structure("Exhibit", [("id", STR), ("label", STR), ("party", STR), ("title", STR), ("category", STR), ("status", STR)]),
        structure("Witness", [("id", STR), ("name", STR), ("relationship", STR), ("party", STR), ("callStatus", STR)]),
        structure("TimelineEvent", [("id", STR), ("date", STR), ("title", STR), ("exhibits", list_t(STR))]),
        definition("caseNumber", STR, s(CASE_META["caseNumber"])),
        definition("hearingDate", STR, s(CASE_META["hearingDate"])),
        definition("validClaimStatuses", list_t(STR), strings(valid_statuses)),
        definition(
            "beneficiaries",
            list_t(ben_t),
            lst(
                [
                    record("Beneficiary", id=s(c["id"]), name=s(c["name"]), dob=s(c["dob"]), age=n(c["age"]), grade=s(c["grade"]))
                    for c in CHILDREN
                ],
                ben_t,
            ),
        ),
        definition(
            "openingPillars",
            list_t(pil_t),
            lst(
                [
                    record("OpeningPillar", id=s(p["id"]), title=s(p["title"]), theme=s(p["theme"]), statutory=s(p["statutory"]), exhibits=strings(p["exhibits"]))
                    for p in OPENING_PILLARS
                ],
                pil_t,
            ),
        ),
        definition(
            "statutoryFactors",
            list_t(fac_t),
            lst(
                [
                    record("StatutoryFactor", id=s(f["id"]), section=s(f["section"]), title=s(f["title"]), exhibits=strings(f["exhibits"]))
                    for f in STATUTORY_FACTORS
                ],
                fac_t,
            ),
        ),
        definition(
            "claims",
            list_t(clm_t),
            lst(
                [
                    record(
                        "Claim",
                        id=s(c["id"]),
                        category=s(c["category"]),
                        status=s(c["status"]),
                        statutory=s(c["statutory"]),
                        statement=s(c["statement"]),
                        exhibits=strings(c["exhibits"]),
                        depends=strings(c["depends"]),
                    )
                    for c in CLAIMS
                ],
                clm_t,
            ),
        ),
        definition(
            "exhibits",
            list_t(ex_t),
            lst(
                [
                    record("Exhibit", id=s(e["id"]), label=s(e["label"]), party=s(e["party"]), title=s(e["title"]), category=s(e["category"]), status=s(e["status"]))
                    for e in all_exs
                ],
                ex_t,
            ),
        ),
        definition(
            "witnesses",
            list_t(wit_t),
            lst(
                [
                    record("Witness", id=s(w["id"]), name=s(w["name"]), relationship=s(w["relationship"]), party=s(w["party"]), callStatus=s(w["callStatus"]))
                    for w in WITNESSES
                ],
                wit_t,
            ),
        ),
        definition(
            "timeline",
            list_t(tl_t),
            lst(
                [
                    record("TimelineEvent", id=s(t["id"]), date=s(t["date"]), title=s(t["title"]), exhibits=strings(t["exhibits"]))
                    for t in TIMELINE
                ],
                tl_t,
            ),
        ),
        member_string(),
        all_members(),
        distinct_strings(),
        field_of_each("beneficiaryIds", ben_t, "id"),
        field_of_each("pillarIds", pil_t, "id"),
        field_of_each("factorIds", fac_t, "id"),
        field_of_each("claimIds", clm_t, "id"),
        field_of_each("exhibitIds", ex_t, "id"),
        field_of_each("witnessIds", wit_t, "id"),
        field_of_each("timelineIds", tl_t, "id"),
        definition(
            "claimsValid",
            BOOL,
            match_list(
                var("cs"),
                b(True),
                "head",
                "tail",
                {
                    "kind": "and",
                    "left": {
                        "kind": "and",
                        "left": call("memberString", proj(var("head"), "status"), call("validClaimStatuses")),
                        "right": {
                            "kind": "and",
                            "left": call("allMembers", proj(var("head"), "exhibits"), call("exhibitIds", call("exhibits"))),
                            "right": call("allMembers", proj(var("head"), "depends"), call("claimIds", call("claims"))),
                        },
                    },
                    "right": call("claimsValid", var("tail")),
                },
            ),
            parameters=[("cs", list_t(clm_t))],
            recursive="cs",
        ),
        holds("beneficiaryIdsDistinct", call("distinctStrings", call("beneficiaryIds", call("beneficiaries")))),
        holds("pillarIdsDistinct", call("distinctStrings", call("pillarIds", call("openingPillars")))),
        holds("factorIdsDistinct", call("distinctStrings", call("factorIds", call("statutoryFactors")))),
        holds("claimIdsDistinct", call("distinctStrings", call("claimIds", call("claims")))),
        holds("exhibitIdsDistinct", call("distinctStrings", call("exhibitIds", call("exhibits")))),
        holds("witnessIdsDistinct", call("distinctStrings", call("witnessIds", call("witnesses")))),
        holds("timelineIdsDistinct", call("distinctStrings", call("timelineIds", call("timeline")))),
        holds("claimsResolvedAndBacked", call("claimsValid", call("claims"))),
        theorem(
            "beneficiaryCountIs3",
            {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [call("beneficiaries")]},
            n(len(CHILDREN)),
            proof="reflexivity",
        ),
        theorem(
            "claimCountIs24",
            {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [call("claims")]},
            n(len(CLAIMS)),
            proof="reflexivity",
        ),
        theorem(
            "exhibitCountIs30",
            {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [call("exhibits")]},
            n(len(all_exs)),
            proof="reflexivity",
        ),
        theorem(
            "witnessCountIs10",
            {"kind": "primitive", "operation": "length", "result": NAT, "arguments": [call("witnesses")]},
            n(len(WITNESSES)),
            proof="reflexivity",
        ),
    ]


def render():
    return lexmod.module("Register", declarations(), title="PrismLegal Reference Matter Evidentiary Register")


def sync():
    MODULE.parent.mkdir(parents=True, exist_ok=True)
    text = render()
    changed = not MODULE.exists() or MODULE.read_text() != text
    if changed:
        MODULE.write_text(text)
    return {
        "module": str(MODULE.relative_to(ROOT)),
        "claims": len(CLAIMS),
        "exhibits": len(RESPONDENT_EXHIBITS) + len(PETITIONER_EXHIBITS),
        "witnesses": len(WITNESSES),
        "factors": len(STATUTORY_FACTORS),
        "timeline": len(TIMELINE),
        "changed": changed,
    }


def check():
    if not MODULE.exists():
        return {"ok": False, "reason": "src/Register.lex.tex missing; run `bin/prism-legal api sync`"}
    ok = MODULE.read_text() == render()
    return {"ok": ok, "reason": None if ok else "src/Register.lex.tex drifted; run `bin/prism-legal api sync`"}
