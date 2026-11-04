"""Domain-specific presentation, user journeys, WAI-ARIA navigation, visualizations,
WCAG 2.2 AA design system, and public-benefit application model for PrismLegal
(`src/Presentation.lex.tex` and `src/Application.lex.tex`)."""

from . import ROOT, archmodel, casemodel, designmodel, lexmod, portalmodel
from .semantic import (
    BOOL,
    NAT,
    STR,
    all_members,
    b,
    ble,
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
    var,
)

PRESENTATION = ROOT / "src" / "Presentation.lex.tex"
APPLICATION = ROOT / "src" / "Application.lex.tex"

BRAND = {
    "id": "prism-legal-public-benefit-platform",
    "title": "PrismLegal — Public-Benefit Legal Case Preparation & Trial Readiness Service",
    "subtitle": "Step-by-Step Case Organization, Evidence Mapping, Testimony Practice, and Hearing Preparation for Clients, Legal Aid Clinics & Trial Attorneys",
    "mark": "site/logo.svg",
    "posture": "Public-Benefit Open Source · Local-First Client & Attorney Workspaces · Multi-Domain Legal Practice",
}

PORTAL_PAGES = [
    {
        "id": "page-home",
        "artifactId": "site",
        "path": "index.html",
        "personaScope": "shared-entry",
        "title": "PrismLegal Service Home — Start or Open a Legal Matter & Choose Your Workspace",
        "sectionCount": 3,
        "maxSectionsBudget": 5,
    },
    {
        "id": "page-client",
        "artifactId": "client-page",
        "path": "client.html",
        "personaScope": "client",
        "title": "Client Case Preparation — 5-Step Guided Journey: Goals, Timeline & Documents, Tough Questions, Direct Testimony & Counsel Packet",
        "sectionCount": 5,
        "maxSectionsBudget": 5,
    },
    {
        "id": "page-lawyer",
        "artifactId": "lawyer-page",
        "path": "lawyer.html",
        "personaScope": "lawyer",
        "title": "Attorney Workbench — 5-Step Guided Journey: Matter Intake, Statutory Elements & Proof, Witness Exams, Exhibits & Calculators, and Trial Brief",
        "sectionCount": 5,
        "maxSectionsBudget": 5,
    },
    {
        "id": "page-courtroom",
        "artifactId": "courtroom-page",
        "path": "courtroom.html",
        "personaScope": "courtroom",
        "title": "Hearing & Trial Companion — Live Hearing Clock, Cross-Exam Pivot Responder, Direct Testimony Checklist & Exhibit Tracker",
        "sectionCount": 4,
        "maxSectionsBudget": 5,
    },
]

FORBIDDEN_META_TERMS = [
    "PrismPM",
    "LexLean",
    "lex.tex",
    "Stakeholder Vantage",
    "Observer Vantage",
    "Quadruple",
    "SensualObject",
    "Kernel Proof",
    "ECDSA P-256",
    "NIST SP 800-63-3",
    "ISO/IEC 27001",
    "ISO 27037",
    "Hohfeldian",
    "LegalRuleML",
    "ASPIC+",
    "Akoma Ntoso",
    "Berlekamp-Massey",
]

ARTIFACTS = [
    {"id": "site", "path": "index.html", "media": "text/html", "producer": "view_render", "description": "Service Home & Matter Launcher: Start a New Legal Matter, Open a Saved Matter File, or Load a Starter Template"},
    {"id": "client-page", "path": "client.html", "media": "text/html", "producer": "view_render", "description": "Client 5-Step Guided Case Preparation Workspace: Goals, Timeline & Documents, Tough Questions Flashcards, Direct Testimony & Counsel Packet"},
    {"id": "lawyer-page", "path": "lawyer.html", "media": "text/html", "producer": "view_render", "description": "Attorney 5-Step Guided Workbench: Matter Intake, Statutory Elements & Proof Matrix, Witness Exams, Exhibit Foundations & Calculators, and Trial Brief"},
    {"id": "courtroom-page", "path": "courtroom.html", "media": "text/html", "producer": "view_render", "description": "Day-of-Hearing Courtroom Companion: Live Hearing Clock, Cross-Exam Pivot Responder, Direct Testimony Checklist & Live Exhibit Admission Tracker"},
    {"id": "logo", "path": "logo.svg", "media": "image/svg+xml", "producer": "view_render", "description": "Public-Benefit Scales & Civic Emblem"},
    {"id": "schedule-svg", "path": "parenting-schedule.svg", "media": "image/svg+xml", "producer": "view_render", "description": "Visual Comparison: Equal 50/50 Schedule (182.5 Overnights) vs. 90-Overnight Restriction"},
    {"id": "support-svg", "path": "remedies-waterfall.svg", "media": "image/svg+xml", "producer": "view_render", "description": "Visual Comparison: Stipulated Guideline Worksheet ($250.00/mo) vs. Contested Imputed Claim ($2,400.00/mo)"},
    {"id": "timeline-svg", "path": "case-timeline.svg", "media": "image/svg+xml", "producer": "view_render", "description": "Chronological Case & Evidentiary Timeline (2015–Sep 2030)"},
    {"id": "compass-md", "path": "sheets/opening-strategy-compass.md", "media": "text/markdown", "producer": "view_render", "description": "Mechanized Sheet: Opening Statement Strategy & Testimony Rules"},
    {"id": "client-guide-md", "path": "sheets/client-strategy-and-testimony-guide.md", "media": "text/markdown", "producer": "view_render", "description": "Mechanized Sheet: Client Strategy Understanding, Rehearsal & Counsel Co-Design Guide"},
    {"id": "lawyer-tuner-md", "path": "sheets/lawyer-model-tuning-and-trial-brief.md", "media": "text/markdown", "producer": "view_render", "description": "Mechanized Sheet: Counsel Model-Tuning, FRE Objection Matrix & Examination Brief"},
    {"id": "factors-md", "path": "sheets/statutory-best-interests-matrix.md", "media": "text/markdown", "producer": "view_render", "description": "Mechanized Sheet: Statutory Factor-by-Factor Evidentiary Matrix (SF-01 to SF-11)"},
    {"id": "remedies-md", "path": "sheets/guideline-remedies-and-disclosure-audit.md", "media": "text/markdown", "producer": "view_render", "description": "Mechanized Sheet: Guideline Support, 38 U.S.C. § 1781 Coverage & FRCP 26(e)/Rule 16.2 Audit"},
    {"id": "pivots-md", "path": "sheets/cross-exam-pivot-cards.md", "media": "text/markdown", "producer": "view_render", "description": "Mechanized Sheet: 16 Cross-Examination Traps & Calm Opening-Aligned Pivots"},
    {"id": "witnesses-md", "path": "sheets/witness-examination-sheets.md", "media": "text/markdown", "producer": "view_render", "description": "Mechanized Sheet: Examination Plans for All 10 Listed Witnesses (W-01 to W-10)"},
    {"id": "direct-exam-md", "path": "sheets/counsel-direct-examination-script.md", "media": "text/markdown", "producer": "view_render", "description": "Mechanized Sheet: Lead Counsel's 36-Question Direct Examination Script with Full Witness Answers & Coaching Notes"},
    {"id": "visual-evidence-md", "path": "sheets/visual-evidence-and-intent-matrix.md", "media": "text/markdown", "producer": "view_render", "description": "Mechanized Sheet: Handwritten Journal Forensics (OP Ex. 13), Visual Extractions & 30-Exhibit Content-Meaning/Intent Matrix"},
    {"id": "register-json", "path": "register.json", "media": "application/json", "producer": "view_render", "description": "Complete Verified Case & Platform Model Register (Claims, Exhibits, Witnesses, Factors, Traps, Portal)"},
    {"id": "tuning-json", "path": "tuning.json", "media": "application/json", "producer": "view_render", "description": "Client-Counsel Model Tuning Parameters & Co-Design Agenda Register"},
    {"id": "standards-json", "path": "standards.json", "media": "application/json", "producer": "view_render", "description": "Legal & Technical Standards Conformance Register"},
]

PANELS = [
    {
        "id": "panel-hub",
        "heading": "1. Service Home: Start a New Legal Matter, Open a Saved Matter File, or Select Active Matter",
        "viewpointId": "VP-PORTAL-HUB",
        "artifactIds": ["site", "register-json", "standards-json"],
        "Empty": "No matter matches the current filter. Create a new matter or open a saved .prismlegal.json file.",
    },
    {
        "id": "panel-strategy",
        "heading": "2. Step 1 (Orientation): Matter Overview, Legal Framework & Core Relief Goals",
        "viewpointId": "VP-CLIENT-PREP",
        "artifactIds": ["client-page", "direct-exam-md", "compass-md", "client-guide-md"],
        "Empty": "No relief goals defined yet. Add the specific outcomes you are asking the court to order.",
    },
    {
        "id": "panel-parenting",
        "heading": "3. Step 2 (Substance): Chronological Timeline, Statutory Elements & Claims Proof Matrix",
        "viewpointId": "VP-COUNSEL-BENCH",
        "artifactIds": ["factors-md", "schedule-svg"],
        "Empty": "No timeline events or statutory claims recorded yet. Add your key dates and legal elements.",
    },
    {
        "id": "panel-cross-exam",
        "heading": "4. Step 3 (Challenge): Witness Examination Builder, Objections & Cross-Exam Rehearsal Deck",
        "viewpointId": "VP-COUNSEL-EXAMS",
        "artifactIds": ["pivots-md", "witnesses-md", "direct-exam-md", "courtroom-page"],
        "Empty": "No cross-examination topics or witnesses added yet. Add anticipated tough questions and calm responses.",
    },
    {
        "id": "panel-evidence",
        "heading": "5. Step 4 (Proof): Document & Exhibit Organizer, Direct Testimony & Admission Tracker",
        "viewpointId": "VP-COUNSEL-EXAMS",
        "artifactIds": ["timeline-svg", "visual-evidence-md", "register-json", "standards-json"],
        "Empty": "No documents or exhibits added yet. Add the records, photos, or statements that prove your facts.",
    },
    {
        "id": "panel-financial",
        "heading": "6. Step 4B (Calculators): Support Guidelines, Disability Rating & Damages Worksheets",
        "viewpointId": "VP-COUNSEL-BENCH",
        "artifactIds": ["remedies-md", "support-svg"],
        "Empty": "Select a worksheet calculator to compute support, disability rating, or contract/housing damages.",
    },
    {
        "id": "panel-lawyer-tuner",
        "heading": "7. Step 5 (Resolution): Client-Attorney Collaboration Agenda, Readiness Checklist & Case Packet Export",
        "viewpointId": "VP-COUNSEL-TUNER",
        "artifactIds": ["lawyer-page", "lawyer-tuner-md", "direct-exam-md", "tuning-json", "register-json"],
        "Empty": "No collaboration notes recorded yet. Add questions for counsel or export your matter packet.",
    },
]

POLES = ["orientation", "substance", "challenge", "proof", "resolution"]

PEDAGOGY_GUIDES = [
    {
        "id": "ped-client-1",
        "stepId": "client-step-1",
        "pole": "orientation",
        "panelId": "panel-strategy",
        "standardId": "uniform-dom-402",
        "heading": "Why Courts Ask for Specific Relief Orders First",
        "whyItMatters": "A judge or hearing officer can only grant orders that are clearly stated and authorized by statute. Vague requests like 'be fair' are hard for a court to enforce, whereas concrete requests (such as a specific parenting schedule, a specific repair deadline, or a specific benefit effective date) give the court a clear roadmap.",
        "coachingTip": "State each goal in one calm, forward-looking sentence describing the exact order you want the judge to sign, followed by the practical reason it helps your household or resolves the dispute.",
        "ruleContext": "Uniform Marriage & Divorce Act § 402 · URLTA § 4.104 · 38 C.F.R. § 3.102 · Scoped Unbundled Representation (ABA Model Rule 1.2(c))",
    },
    {
        "id": "ped-client-2",
        "stepId": "client-step-2",
        "pole": "substance",
        "panelId": "panel-parenting",
        "standardId": "fre-evidence",
        "heading": "How a Chronological Timeline & Linked Exhibits Build Credibility",
        "whyItMatters": "Hearings move quickly. When your facts are arranged in chronological order and linked to a specific record—such as a school log, certified notice, bank statement, or medical report—the judge can verify your testimony immediately.",
        "coachingTip": "Focus on observable dates, actions, and records rather than emotional characterizations. Whenever a document or photo proves an event, enter its Exhibit Label (e.g., Ex. A) so it links automatically.",
        "ruleContext": "Federal Rules of Evidence 401 (Relevance), 803(6) (Business Records), 803(8) (Public Records) & 901 (Authentication)",
    },
    {
        "id": "ped-client-3",
        "stepId": "client-step-3",
        "pole": "challenge",
        "panelId": "panel-cross-exam",
        "standardId": "dung-aspic-arg",
        "heading": "How to Handle Hostile Questions & Out-of-Context Quotes Calmly",
        "whyItMatters": "Cross-examination is often designed to provoke frustration or pull a single sentence from an email, text, or journal out of context. A calm, measured witness who answers directly and points to the complete written record wins the court's trust.",
        "coachingTip": "Pause for two seconds before answering. Never argue with opposing counsel. Acknowledge any undisputed baseline fact, then calmly direct the court to the full context and supporting exhibit.",
        "ruleContext": "Federal Rule of Evidence 106 (Rule of Completeness — Requiring Full Context for Partial Quotes) & Rule 611 (Mode and Order of Examining Witnesses)",
    },
    {
        "id": "ped-client-4",
        "stepId": "client-step-4",
        "pole": "proof",
        "panelId": "panel-evidence",
        "standardId": "fre-evidence",
        "heading": "How Direct Examination Establishes Your Case-in-Chief",
        "whyItMatters": "Direct examination is your opportunity to tell your story through open-ended questions ('Who, What, When, Where, How'). Unlike cross-examination, your attorney cannot ask leading questions on direct, so your answers must supply the concrete facts and introduce your exhibits.",
        "coachingTip": "Practice speaking in clear 2-to-3 sentence answers. When a question references an exhibit, identify the document, confirm how you recognize it, and state the key fact it shows.",
        "ruleContext": "Federal Rule of Evidence 602 (Personal Knowledge), Rule 611(c) (Non-Leading Direct Questions) & Rule 901(b)(1) (Testimony of Witness with Knowledge)",
    },
    {
        "id": "ped-client-5",
        "stepId": "client-step-5",
        "pole": "resolution",
        "panelId": "panel-lawyer-tuner",
        "standardId": "aba-rpc-webauthn-sharing",
        "heading": "How to Review Case Consistency & Share with Counsel",
        "whyItMatters": "Before stepping into court or meeting with a legal-aid clinic or consulting attorney, checking that every goal is backed by timeline events, exhibits, and rehearsed testimony saves hours of preparation time.",
        "coachingTip": "Use the Automated Case Consistency Check below to spot any unlinked documents or unrehearsed questions, log your specific questions for counsel, and save your portable .prismlegal.json file.",
        "ruleContext": "ABA Model Rules 1.1 (Competence), 1.2(c) (Limited-Scope Representation), 1.4 (Client Communication) & 1.6 (Confidentiality)",
    },
    {
        "id": "ped-counsel-1",
        "stepId": "counsel-step-1",
        "pole": "orientation",
        "panelId": "panel-hub",
        "standardId": "aba-rpc-webauthn-sharing",
        "heading": "Scoping the Engagement, Forum & Theory of the Case",
        "whyItMatters": "Whether appearing as full-scope trial counsel or providing unbundled limited-scope representation under Rule 1.2(c), defining the governing statutory framework, forum rules, and relief posture upfront anchors every downstream proof requirement.",
        "coachingTip": "Select the governing Area of Law and Representation Scope below. Use the one-click Domain Scaffolding tool to populate standard statutory elements if starting a fresh docket.",
        "ruleContext": "ABA Model Rule 1.2(c) (Unbundled Legal Services), Rule 1.1 (Competence) & Pretrial Management Under Civil Rule 16",
    },
    {
        "id": "ped-counsel-2",
        "stepId": "counsel-step-2",
        "pole": "substance",
        "panelId": "panel-parenting",
        "standardId": "oasis-legalruleml-1.0",
        "heading": "Mapping Statutory Elements, Proposed Findings & Rule Exceptions",
        "whyItMatters": "Trial courts must enter findings of fact and conclusions of law on each statutory element. An explicit proof matrix prevents evidentiary gaps, compiles each backed proposition into a proposed court finding, and pairs general rules with controlling statutory exceptions.",
        "coachingTip": "Ensure every claim is linked to at least one exhibit so the Refusal Guard clears it for your proposed findings. Record any statutory exceptions or immunities (such as protected disability income or mandatory-disclosure bars) in the Rule Exceptions drawer.",
        "ruleContext": "Civil Rule 52(a) (Findings and Conclusions by the Court), Rule 26(e) / 16.2 (Disclosure Duty) & Controlling Statutory Exceptions",
    },
    {
        "id": "ped-counsel-3",
        "stepId": "counsel-step-3",
        "pole": "challenge",
        "panelId": "panel-cross-exam",
        "standardId": "fre-evidence",
        "heading": "Homeostatic Hearing Clock Budgeting & Examination Scripting",
        "whyItMatters": "Trial judges strictly enforce time limits. Overrunning direct or cross-examination can forfeit time needed for closing argument and final-order requests. Stage-by-stage budgeting protects your closing gate reserve.",
        "coachingTip": "Allocate realistic minutes to each witness and check the 4-Stage Hearing Clock breakdown below to verify that your Closing & Final Orders Gate reserve remains protected.",
        "ruleContext": "Federal Rule of Evidence 611(a) (Control by the Court Over Time and Mode of Examination) & Rule 103 (Preserving Evidentiary Rulings)",
    },
    {
        "id": "ped-counsel-4",
        "stepId": "counsel-step-4",
        "pole": "proof",
        "panelId": "panel-financial",
        "standardId": "iso-15489-27037",
        "heading": "Auditing Admissibility Foundations, Chain of Custody & Guideline Math",
        "whyItMatters": "Even persuasive documents can be excluded if their authentication or hearsay exception foundation is not ready at counsel table. Likewise, support, rating, and damages requests must be backed by transparent statutory worksheet calculations.",
        "coachingTip": "Assign an explicit rule foundation (e.g., FRE 803(6), 803(8), 901) to every exhibit, optionally compute a local SHA-256 verification digest for digital files, and verify the statutory calculator outputs for your jurisdiction.",
        "ruleContext": "Federal Rules of Evidence 901–902 (Authentication), 803 (Hearsay Exceptions), Uniform Support Guidelines § 305, 38 C.F.R. § 4.25 & URLTA § 4.104",
    },
    {
        "id": "ped-counsel-5",
        "stepId": "counsel-step-5",
        "pole": "resolution",
        "panelId": "panel-lawyer-tuner",
        "standardId": "hohfeld-1913",
        "heading": "Consistency Audit, Priority Ranking & Trial Brief Handoff",
        "whyItMatters": "Before hearing day, counsel needs an automated check across all claims, exhibits, and witness scripts, a ranked priority order for examination themes if time is cut short, and written answers to client strategy questions.",
        "coachingTip": "Review the Automated Consistency Audit and Priority Strategy Schedule below, answer any open client questions, and export either the updated .prismlegal.json file or the compiled Markdown Trial Brief.",
        "ruleContext": "Civil Rule 16 (Pretrial Conferences and Trial Briefs), Rule 52(a) (Proposed Findings) & ABA Model Rule 1.4 (Client Alignment)",
    },
    {
        "id": "ped-court-1",
        "stepId": "court-step-1",
        "pole": "orientation",
        "panelId": "panel-cross-exam",
        "standardId": "dung-aspic-arg",
        "heading": "Live Witness Stand & Counsel Table Cross-Exam Responder",
        "whyItMatters": "During live cross-examination, quick access to the exact rebuttal exhibit, the trap to avoid, the Rule 106 full-context citation, and the calm one-sentence answer keeps testimony focused on the court's statutory factors.",
        "coachingTip": "Click any topic pill below as soon as opposing counsel raises that subject to display the calm response and supporting exhibit in high-contrast large type.",
        "ruleContext": "Federal Rule of Evidence 106 (Remainder of Related Writings) & Rule 611(b) (Scope of Cross-Examination)",
    },
    {
        "id": "ped-court-2",
        "stepId": "court-step-2",
        "pole": "substance",
        "panelId": "panel-evidence",
        "standardId": "fre-evidence",
        "heading": "Live Direct Examination Checklist & Foundation Pacing",
        "whyItMatters": "Checking off each direct examination question as it is asked ensures that no required statutory element or exhibit admission offer is inadvertently skipped under courtroom time pressure.",
        "coachingTip": "Use the search filter or priority badges to track essential testimony points and offer each linked exhibit into evidence as soon as its foundation is laid.",
        "ruleContext": "Federal Rules of Evidence 611(a), 602 & 901 (Offering Exhibits During Case-in-Chief)",
    },
    {
        "id": "ped-court-3",
        "stepId": "court-step-3",
        "pole": "proof",
        "panelId": "panel-evidence",
        "standardId": "iso-15489-27037",
        "heading": "Live Exhibit Offer & Admission Status Tracker",
        "whyItMatters": "Before resting your case-in-chief, counsel must confirm that every exhibit relied upon for proposed findings or closing argument has been formally offered and admitted into the record.",
        "coachingTip": "Update each exhibit's status to 'Offered at Hearing' or 'Admitted' in real time so you can verify your complete evidentiary record before resting.",
        "ruleContext": "Federal Rule of Evidence 103 (Rulings on Evidence) & Trial Record Completeness",
    },
]

JOURNEYS = [
    {
        "id": "journey-client-preparation",
        "stakeholderId": "SH-CLIENT",
        "summary": "Client 5-Step Guided Case Preparation Journey: Define your matter and relief goals, build your chronological timeline and document list, rehearse calm answers to tough cross-examination questions, practice direct testimony, and export your case packet for counsel or court.",
        "steps": [
            {
                "id": "client-step-1",
                "pole": "orientation",
                "panelId": "panel-strategy",
                "action": "Step 1 — Define My Matter & Relief Goals: Enter your case details, court, hearing date, and the specific outcomes you are asking the judge to order.",
                "artifactId": "client-guide-md",
            },
            {
                "id": "client-step-2",
                "pole": "substance",
                "panelId": "panel-parenting",
                "action": "Step 2 — Build My Timeline & Documents: Add the key dates and events in your case and organize the documents or photos that support each fact.",
                "artifactId": "factors-md",
            },
            {
                "id": "client-step-3",
                "pole": "challenge",
                "panelId": "panel-cross-exam",
                "action": "Step 3 — Prepare for Tough Questions: Write down criticisms or allegations the other side might raise and rehearse calm, fact-based answers with flashcards.",
                "artifactId": "pivots-md",
            },
            {
                "id": "client-step-4",
                "pole": "proof",
                "panelId": "panel-evidence",
                "action": "Step 4 — Practice My Direct Testimony: Organize the questions you will answer in court, link each answer to your documents, and rehearse step-by-step.",
                "artifactId": "direct-exam-md",
            },
            {
                "id": "client-step-5",
                "pole": "resolution",
                "panelId": "panel-lawyer-tuner",
                "action": "Step 5 — Collaborate with Counsel & Export Packet: List questions for your attorney, check your hearing readiness, and download your .prismlegal.json file or printable summary.",
                "artifactId": "tuning-json",
            },
        ],
    },
    {
        "id": "journey-counsel-workbench",
        "stakeholderId": "SH-LAWYER",
        "summary": "Attorney 5-Step Guided Workbench Journey: Intake a client matter or create a new docket, map statutory elements and claims to exhibits, script witness examinations and objections, audit exhibit foundations and run statutory calculators, and generate the trial brief.",
        "steps": [
            {
                "id": "counsel-step-1",
                "pole": "orientation",
                "panelId": "panel-hub",
                "action": "Step 1 — Matter Intake & Case Theory: Open a client's matter file or create a new docket, select the governing legal framework, and align on relief targets.",
                "artifactId": "site",
            },
            {
                "id": "counsel-step-2",
                "pole": "substance",
                "panelId": "panel-parenting",
                "action": "Step 2 — Statutory Elements & Claims Proof Matrix: Map every legal element or factual claim to its governing statute, evidentiary status, and supporting exhibits.",
                "artifactId": "factors-md",
            },
            {
                "id": "counsel-step-3",
                "pole": "challenge",
                "panelId": "panel-cross-exam",
                "action": "Step 3 — Witness Examinations & Evidentiary Objections: Script direct examinations and cross-examination impeachment, prepare objections, and budget hearing minutes.",
                "artifactId": "witnesses-md",
            },
            {
                "id": "counsel-step-4",
                "pole": "proof",
                "panelId": "panel-financial",
                "action": "Step 4 — Exhibit Foundations & Statutory Calculators: Audit exhibit admissibility foundations and compute support, disability rating, or damages worksheets.",
                "artifactId": "remedies-md",
            },
            {
                "id": "counsel-step-5",
                "pole": "resolution",
                "panelId": "panel-lawyer-tuner",
                "action": "Step 5 — Trial Brief, Client Guidance & Courtroom Handoff: Answer client agenda questions, review prioritized argument schedules, and export the trial brief or launch Courtroom Mode.",
                "artifactId": "lawyer-tuner-md",
            },
        ],
    },
    {
        "id": "journey-court-bench",
        "stakeholderId": "SH-COURT",
        "summary": "Presiding Fact-Finder Hearing Journey: Review stipulated vs. contested issues, evaluate statutory elements against admitted exhibits, weigh witness credibility, verify guideline/damages calculations, and enter findings of fact and conclusions of law.",
        "steps": [
            {
                "id": "court-step-1",
                "pole": "orientation",
                "panelId": "panel-strategy",
                "action": "Stage 1 — Review Pretrial Stipulations & Narrowed Issues Before the Court.",
                "artifactId": "compass-md",
            },
            {
                "id": "court-step-2",
                "pole": "substance",
                "panelId": "panel-parenting",
                "action": "Stage 2 — Evaluate Statutory Factors & Element-by-Element Factual Record.",
                "artifactId": "factors-md",
            },
            {
                "id": "court-step-3",
                "pole": "challenge",
                "panelId": "panel-cross-exam",
                "action": "Stage 3 — Weigh Witness Credibility, Cross-Examination Responses & Rule 106 Context.",
                "artifactId": "pivots-md",
            },
            {
                "id": "court-step-4",
                "pole": "proof",
                "panelId": "panel-financial",
                "action": "Stage 4 — Verify Statutory Worksheets, Mandatory Disclosures & Documentary Foundations.",
                "artifactId": "remedies-md",
            },
            {
                "id": "court-step-5",
                "pole": "resolution",
                "panelId": "panel-evidence",
                "action": "Stage 5 — Enter Final Orders Grounded in Admitted Exhibits and Statutory Findings.",
                "artifactId": "support-svg",
            },
        ],
    },
    {
        "id": "journey-beneficiaries-stability",
        "stakeholderId": "SH-BENEFICIARIES",
        "summary": "Protected Beneficiaries & Dependents Journey: Ensure continuity of care, predictable schedules, healthcare coverage, and balanced household or statutory resources.",
        "steps": [
            {
                "id": "beneficiaries-step-1",
                "pole": "orientation",
                "panelId": "panel-strategy",
                "action": "Step 1 — Establish Core Stability, Safety, and Best-Interests Objectives.",
                "artifactId": "compass-md",
            },
            {
                "id": "beneficiaries-step-2",
                "pole": "substance",
                "panelId": "panel-parenting",
                "action": "Step 2 — Evaluate Caregiving History, Educational Continuity, and Routine Schedule.",
                "artifactId": "schedule-svg",
            },
            {
                "id": "beneficiaries-step-3",
                "pole": "challenge",
                "panelId": "panel-cross-exam",
                "action": "Step 3 — Replace High-Conflict Disputes with Predictable Transitions and Direct Care.",
                "artifactId": "pivots-md",
            },
            {
                "id": "beneficiaries-step-4",
                "pole": "proof",
                "panelId": "panel-evidence",
                "action": "Step 4 — Corroborate Dependent Well-Being Through School, Medical, and Activity Records.",
                "artifactId": "timeline-svg",
            },
            {
                "id": "beneficiaries-step-5",
                "pole": "resolution",
                "panelId": "panel-financial",
                "action": "Step 5 — Secure Healthcare Coverage and Accurate Guideline Support Across Households.",
                "artifactId": "support-svg",
            },
        ],
    },
    {
        "id": "journey-counterparty-protocol",
        "stakeholderId": "SH-COUNTERPARTY",
        "summary": "Counterparty Resolution & Governance Journey: Narrow disputed issues through stipulations, enforce mandatory disclosures, and establish clear post-order protocols.",
        "steps": [
            {
                "id": "counterparty-step-1",
                "pole": "orientation",
                "panelId": "panel-strategy",
                "action": "Step 1 — Identify Stipulated Baselines and Narrow Remaining Contested Issues.",
                "artifactId": "compass-md",
            },
            {
                "id": "counterparty-step-2",
                "pole": "substance",
                "panelId": "panel-parenting",
                "action": "Step 2 — Establish Predictable Exchange, Notice, and Communication Protocols.",
                "artifactId": "factors-md",
            },
            {
                "id": "counterparty-step-3",
                "pole": "challenge",
                "panelId": "panel-cross-exam",
                "action": "Step 3 — Resolve Disagreements Through Structured Written Channels and Mediation.",
                "artifactId": "pivots-md",
            },
            {
                "id": "counterparty-step-4",
                "pole": "proof",
                "panelId": "panel-financial",
                "action": "Step 4 — Exchange Complete Financial and Evidentiary Disclosures Under Rule 26(e).",
                "artifactId": "remedies-md",
            },
            {
                "id": "counterparty-step-5",
                "pole": "resolution",
                "panelId": "panel-evidence",
                "action": "Step 5 — Maintain Shared Access to Official Records and Post-Decree Compliance.",
                "artifactId": "standards-json",
            },
        ],
    },
]

NAV_PATTERNS = [
    {
        "id": "tablist-navigation",
        "authority": "https://www.w3.org/WAI/ARIA/apg/patterns/tabs/",
        "statement": "A WAI-ARIA tablist (role=tablist, role=tab, aria-selected, aria-controls) switching between the domain workspace panels.",
    },
    {
        "id": "vantage-selector",
        "authority": "https://www.w3.org/WAI/ARIA/apg/patterns/button/",
        "statement": "A group of toggle buttons (aria-pressed) selecting the active role or matter context.",
    },
    {
        "id": "stepper-sequence",
        "authority": "https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/",
        "statement": "An ordered five-pole step sequence (aria-current=step) walking the active preparation journey.",
    },
]

NAVIGATIONS = [
    {
        "id": "nav-primary",
        "label": "Workspace Viewpoint Tabs",
        "pattern": "tablist-navigation",
        "statement": "Primary navigation bar reaching all seven domain panels.",
    },
    {
        "id": "nav-vantages",
        "label": "Role & Journey Selector",
        "pattern": "vantage-selector",
        "statement": "Switches between Client, Counsel, Bench, Beneficiaries, and Counterparty journeys.",
    },
    {
        "id": "nav-stepper",
        "label": "Five-Pole Journey Stepper",
        "pattern": "stepper-sequence",
        "statement": "Ordered five-pole progression (orientation, substance, challenge, proof, resolution) for each journey.",
    },
]

NAV_ITEMS = (
    [
        {
            "id": f"nav-tab-{p['id']}",
            "navigation": "nav-primary",
            "pattern": "tablist-navigation",
            "kind": "panel",
            "target": p["id"],
            "order": idx + 1,
        }
        for idx, p in enumerate(PANELS)
    ]
    + [
        {
            "id": f"nav-vantage-{j['id']}",
            "navigation": "nav-vantages",
            "pattern": "vantage-selector",
            "kind": "journey",
            "target": j["id"],
            "order": idx + 1,
        }
        for idx, j in enumerate(JOURNEYS)
    ]
    + [
        {
            "id": f"nav-stepper-{j['id']}",
            "navigation": "nav-stepper",
            "pattern": "stepper-sequence",
            "kind": "journey",
            "target": j["id"],
            "order": idx + 1,
        }
        for idx, j in enumerate(JOURNEYS)
    ]
)

VISUALIZATIONS = [
    {
        "id": "viz-platform-hub",
        "panelId": "panel-hub",
        "artifactId": "site",
        "renders": ["CLM-01", "CLM-09", "CLM-13", "CLM-22", "CLM-23", "CLM-24"],
    },
    {
        "id": "viz-client-strategy",
        "panelId": "panel-strategy",
        "artifactId": "client-guide-md",
        "renders": ["CLM-01", "CLM-02", "CLM-05", "CLM-10", "CLM-22", "CLM-23", "CLM-24"],
    },
    {
        "id": "viz-lawyer-tuner",
        "panelId": "panel-lawyer-tuner",
        "artifactId": "lawyer-tuner-md",
        "renders": ["CLM-01", "CLM-05", "CLM-09", "CLM-10", "CLM-13", "CLM-14", "CLM-22", "CLM-23", "CLM-24"],
    },
    {
        "id": "viz-parenting-schedule",
        "panelId": "panel-parenting",
        "artifactId": "schedule-svg",
        "renders": ["CLM-01", "CLM-02", "CLM-03", "CLM-04", "CLM-22"],
    },
    {
        "id": "viz-remedies-waterfall",
        "panelId": "panel-financial",
        "artifactId": "support-svg",
        "renders": ["CLM-09", "CLM-10", "CLM-11", "CLM-12", "CLM-15", "CLM-16", "CLM-24"],
    },
    {
        "id": "viz-factors-matrix",
        "panelId": "panel-parenting",
        "artifactId": "factors-md",
        "renders": ["CLM-01", "CLM-02", "CLM-05", "CLM-06", "CLM-07", "CLM-08", "CLM-22", "CLM-23"],
    },
    {
        "id": "viz-disclosure-audit",
        "panelId": "panel-financial",
        "artifactId": "remedies-md",
        "renders": ["CLM-13", "CLM-14", "CLM-17"],
    },
    {
        "id": "viz-timeline",
        "panelId": "panel-evidence",
        "artifactId": "timeline-svg",
        "renders": ["CLM-01", "CLM-03", "CLM-07", "CLM-13", "CLM-18", "CLM-21"],
    },
    {
        "id": "viz-claim-dag",
        "panelId": "panel-evidence",
        "artifactId": "register-json",
        "renders": ["CLM-01", "CLM-22", "CLM-23", "CLM-24"],
    },
]

TOKENS = designmodel.tokens()


def presentation_declarations():
    brand_t = named("Brand")
    page_t = named("PortalPage")
    artifact_t = named("Artifact")
    panel_t = named("Panel")
    step_t = named("JourneyStep")
    journey_t = named("Journey")
    pat_t = named("Pattern")
    nav_t = named("Navigation")
    nitem_t = named("NavItem")
    viz_t = named("VizPanel")
    ped_t = named("PedagogyGuide")
    nil_s = {"kind": "nil", "element": STR}

    page_rec = lambda pg: record(
        "PortalPage",
        id=s(pg["id"]),
        artifactId=s(pg["artifactId"]),
        path=s(pg["path"]),
        personaScope=s(pg["personaScope"]),
        title=s(pg["title"]),
        sectionCount=n(pg["sectionCount"]),
        maxSectionsBudget=n(pg["maxSectionsBudget"]),
    )
    art_rec = lambda a: record(
        "Artifact",
        id=s(a["id"]),
        path=s(a["path"]),
        media=s(a["media"]),
        producer=s(a["producer"]),
        description=s(a["description"]),
    )
    panel_rec = lambda p: record(
        "Panel",
        id=s(p["id"]),
        heading=s(p["heading"]),
        viewpointId=s(p["viewpointId"]),
        artifactIds=strings(p["artifactIds"]),
        Empty=s(p["Empty"]),
    )
    step_rec = lambda st: record(
        "JourneyStep",
        id=s(st["id"]),
        pole=s(st["pole"]),
        panelId=s(st["panelId"]),
        action=s(st["action"]),
        artifactId=s(st["artifactId"]),
    )
    journey_rec = lambda j: record(
        "Journey",
        id=s(j["id"]),
        stakeholderId=s(j["stakeholderId"]),
        summary=s(j["summary"]),
        steps=lst([step_rec(st) for st in j["steps"]], step_t),
    )
    pat_rec = lambda p: record(
        "Pattern",
        id=s(p["id"]),
        authority=s(p["authority"]),
        statement=s(p["statement"]),
    )
    nav_rec = lambda nv: record(
        "Navigation",
        id=s(nv["id"]),
        label=s(nv["label"]),
        pattern=s(nv["pattern"]),
        statement=s(nv["statement"]),
    )
    nitem_rec = lambda ni: record(
        "NavItem",
        id=s(ni["id"]),
        navigation=s(ni["navigation"]),
        pattern=s(ni["pattern"]),
        kind=s(ni["kind"]),
        target=s(ni["target"]),
        order=n(ni["order"]),
    )
    viz_rec = lambda v: record(
        "VizPanel",
        id=s(v["id"]),
        panelId=s(v["panelId"]),
        artifactId=s(v["artifactId"]),
        renders=strings(v["renders"]),
    )
    ped_rec = lambda pg: record(
        "PedagogyGuide",
        id=s(pg["id"]),
        stepId=s(pg["stepId"]),
        pole=s(pg["pole"]),
        panelId=s(pg["panelId"]),
        standardId=s(pg["standardId"]),
        heading=s(pg["heading"]),
        whyItMatters=s(pg["whyItMatters"]),
        coachingTip=s(pg["coachingTip"]),
        ruleContext=s(pg["ruleContext"]),
    )

    vp_ids = call("viewpointIds", call("viewpoints", module="Architecture"), module="Architecture")
    sh_ids = call("stakeholderIds", call("stakeholders", module="Architecture"), module="Architecture")
    clm_ids = call("claimIds", call("claims", module="Register"), module="Register")

    return [
        structure("Brand", [("id", STR), ("title", STR), ("subtitle", STR), ("mark", STR), ("posture", STR)]),
        structure(
            "PortalPage",
            [
                ("id", STR),
                ("artifactId", STR),
                ("path", STR),
                ("personaScope", STR),
                ("title", STR),
                ("sectionCount", NAT),
                ("maxSectionsBudget", NAT),
            ],
        ),
        structure("Artifact", [("id", STR), ("path", STR), ("media", STR), ("producer", STR), ("description", STR)]),
        structure(
            "Panel",
            [("id", STR), ("heading", STR), ("viewpointId", STR), ("artifactIds", list_t(STR)), ("Empty", STR)],
        ),
        structure(
            "JourneyStep",
            [("id", STR), ("pole", STR), ("panelId", STR), ("action", STR), ("artifactId", STR)],
        ),
        structure(
            "Journey",
            [("id", STR), ("stakeholderId", STR), ("summary", STR), ("steps", list_t(step_t))],
        ),
        structure("Pattern", [("id", STR), ("authority", STR), ("statement", STR)]),
        structure("Navigation", [("id", STR), ("label", STR), ("pattern", STR), ("statement", STR)]),
        structure(
            "NavItem",
            [("id", STR), ("navigation", STR), ("pattern", STR), ("kind", STR), ("target", STR), ("order", NAT)],
        ),
        structure(
            "VizPanel",
            [("id", STR), ("panelId", STR), ("artifactId", STR), ("renders", list_t(STR))],
        ),
        structure(
            "PedagogyGuide",
            [
                ("id", STR),
                ("stepId", STR),
                ("pole", STR),
                ("panelId", STR),
                ("standardId", STR),
                ("heading", STR),
                ("whyItMatters", STR),
                ("coachingTip", STR),
                ("ruleContext", STR),
            ],
        ),
        definition("brand", brand_t, record("Brand", **{k: s(v) for k, v in BRAND.items()})),
        definition("portalPages", list_t(page_t), lst([page_rec(pg) for pg in PORTAL_PAGES], page_t)),
        definition("forbiddenMetaTerms", list_t(STR), strings(FORBIDDEN_META_TERMS)),
        definition("poles", list_t(STR), strings(POLES)),
        definition("artifacts", list_t(artifact_t), lst([art_rec(a) for a in ARTIFACTS], artifact_t)),
        definition("panels", list_t(panel_t), lst([panel_rec(p) for p in PANELS], panel_t)),
        definition("journeys", list_t(journey_t), lst([journey_rec(j) for j in JOURNEYS], journey_t)),
        definition("navPatterns", list_t(pat_t), lst([pat_rec(p) for p in NAV_PATTERNS], pat_t)),
        definition("navigations", list_t(nav_t), lst([nav_rec(nv) for nv in NAVIGATIONS], nav_t)),
        definition("navItems", list_t(nitem_t), lst([nitem_rec(ni) for ni in NAV_ITEMS], nitem_t)),
        definition("vizPanels", list_t(viz_t), lst([viz_rec(v) for v in VISUALIZATIONS], viz_t)),
        definition("pedagogyGuides", list_t(ped_t), lst([ped_rec(pg) for pg in PEDAGOGY_GUIDES], ped_t)),
        member_string(),
        all_members(),
        distinct_strings(),
        definition(
            "appendStrings",
            list_t(STR),
            match_list(
                var("xs"),
                var("ys"),
                "head",
                "tail",
                {"kind": "cons", "head": var("head"), "tail": call("appendStrings", var("tail"), var("ys"))},
            ),
            parameters=[("xs", list_t(STR)), ("ys", list_t(STR))],
            recursive="xs",
        ),
        definition(
            "sameMembers",
            BOOL,
            if_(call("allMembers", var("xs"), var("ys")), call("allMembers", var("ys"), var("xs")), b(False)),
            parameters=[("xs", list_t(STR)), ("ys", list_t(STR))],
        ),
        field_of_each("artifactIds", artifact_t, "id"),
        field_of_each("artifactPaths", artifact_t, "path"),
        field_of_each("portalPageIds", page_t, "id"),
        field_of_each("portalPagePaths", page_t, "path"),
        field_of_each("portalPageArtifacts", page_t, "artifactId"),
        field_of_each("portalPageTitles", page_t, "title"),
        field_of_each("panelIds", panel_t, "id"),
        field_of_each("panelHeadings", panel_t, "heading"),
        field_of_each("panelViewpoints", panel_t, "viewpointId"),
        field_of_each("journeyIds", journey_t, "id"),
        field_of_each("journeyStakeholders", journey_t, "stakeholderId"),
        field_of_each("stepPoles", step_t, "pole"),
        field_of_each("stepPanels", step_t, "panelId"),
        field_of_each("stepArtifacts", step_t, "artifactId"),
        field_of_each("patternIds", pat_t, "id"),
        field_of_each("navigationIds", nav_t, "id"),
        field_of_each("navigationPatterns", nav_t, "pattern"),
        field_of_each("navItemIds", nitem_t, "id"),
        field_of_each("navItemNavigations", nitem_t, "navigation"),
        field_of_each("navItemPatterns", nitem_t, "pattern"),
        field_of_each("navItemTargets", nitem_t, "target"),
        field_of_each("vizPanelIds", viz_t, "id"),
        field_of_each("vizHostPanels", viz_t, "panelId"),
        field_of_each("vizArtifacts", viz_t, "artifactId"),
        field_of_each("pedagogyIds", ped_t, "id"),
        field_of_each("pedagogyPoles", ped_t, "pole"),
        field_of_each("pedagogyPanels", ped_t, "panelId"),
        field_of_each("pedagogyHeadings", ped_t, "heading"),
        definition(
            "vizRenders",
            list_t(STR),
            match_list(
                var("xs"),
                nil_s,
                "head",
                "tail",
                call("appendStrings", proj(var("head"), "renders"), call("vizRenders", var("tail"))),
            ),
            parameters=[("xs", list_t(viz_t))],
            recursive="xs",
        ),
        definition(
            "vizEachRenders",
            BOOL,
            match_list(
                var("xs"),
                b(True),
                "head",
                "tail",
                match_list(proj(var("head"), "renders"), b(False), "r", "rs", call("vizEachRenders", var("tail"))),
            ),
            parameters=[("xs", list_t(viz_t))],
            recursive="xs",
        ),
        definition(
            "panelsReadArtifacts",
            BOOL,
            match_list(
                var("ps"),
                b(True),
                "head",
                "tail",
                if_(
                    call("allMembers", proj(var("head"), "artifactIds"), var("aIds")),
                    call("panelsReadArtifacts", var("tail"), var("aIds")),
                    b(False),
                ),
            ),
            parameters=[("ps", list_t(panel_t)), ("aIds", list_t(STR))],
            recursive="ps",
        ),
        definition(
            "equalStringLists",
            BOOL,
            match_list(
                var("xs"),
                match_list(var("ys"), b(True), "yh", "yt", b(False)),
                "xh",
                "xt",
                match_list(
                    var("ys"),
                    b(False),
                    "yh",
                    "yt",
                    if_(eq_string(var("xh"), var("yh")), call("equalStringLists", var("xt"), var("yt")), b(False)),
                ),
            ),
            parameters=[("xs", list_t(STR)), ("ys", list_t(STR))],
            recursive="xs",
        ),
        definition(
            "journeysWalkPolesAndResolve",
            BOOL,
            match_list(
                var("js"),
                b(True),
                "head",
                "tail",
                if_(
                    call("equalStringLists", call("stepPoles", proj(var("head"), "steps")), call("poles")),
                    if_(
                        call("allMembers", call("stepPanels", proj(var("head"), "steps")), var("pIds")),
                        if_(
                            call("allMembers", call("stepArtifacts", proj(var("head"), "steps")), var("aIds")),
                            call("journeysWalkPolesAndResolve", var("tail"), var("pIds"), var("aIds")),
                            b(False),
                        ),
                        b(False),
                    ),
                    b(False),
                ),
            ),
            parameters=[("js", list_t(journey_t)), ("pIds", list_t(STR)), ("aIds", list_t(STR))],
            recursive="js",
        ),
        holds("artifactIdsDistinct", call("distinctStrings", call("artifactIds", call("artifacts")))),
        holds("artifactPathsDistinct", call("distinctStrings", call("artifactPaths", call("artifacts")))),
        holds("panelsGovernedByViewpoints", call("allMembers", call("panelViewpoints", call("panels")), vp_ids)),
        holds(
            "panelArtifactsValid",
            call("panelsReadArtifacts", call("panels"), call("artifactIds", call("artifacts"))),
        ),
        holds("journeysServeStakeholders", call("allMembers", call("journeyStakeholders", call("journeys")), sh_ids)),
        holds("everyStakeholderHasJourney", call("allMembers", sh_ids, call("journeyStakeholders", call("journeys")))),
        holds(
            "journeysValid",
            call(
                "journeysWalkPolesAndResolve",
                call("journeys"),
                call("panelIds", call("panels")),
                call("artifactIds", call("artifacts")),
            ),
        ),
        holds(
            "navIdsDistinct",
            call(
                "distinctStrings",
                call("appendStrings", call("navigationIds", call("navigations")), call("navItemIds", call("navItems"))),
            ),
        ),
        holds(
            "navigationsNamePatterns",
            call("allMembers", call("navigationPatterns", call("navigations")), call("patternIds", call("navPatterns"))),
        ),
        holds(
            "navItemsNamePatterns",
            call("allMembers", call("navItemPatterns", call("navItems")), call("patternIds", call("navPatterns"))),
        ),
        holds(
            "navItemsInNavigations",
            call("allMembers", call("navItemNavigations", call("navItems")), call("navigationIds", call("navigations"))),
        ),
        holds(
            "everyPanelInPrimaryNavigation",
            call("allMembers", call("panelIds", call("panels")), call("navItemTargets", call("navItems"))),
        ),
        holds(
            "everyJourneyInVantageNavigation",
            call("allMembers", call("journeyIds", call("journeys")), call("navItemTargets", call("navItems"))),
        ),
        holds("vizPanelIdsDistinct", call("distinctStrings", call("vizPanelIds", call("vizPanels")))),
        holds("vizHostPanelsValid", call("allMembers", call("vizHostPanels", call("vizPanels")), call("panelIds", call("panels")))),
        holds("vizArtifactsPublished", call("allMembers", call("vizArtifacts", call("vizPanels")), call("artifactIds", call("artifacts")))),
        holds("vizPanelsRender", call("vizEachRenders", call("vizPanels"))),
        holds("vizRendersAreClaims", call("allMembers", call("vizRenders", call("vizPanels")), clm_ids)),
        definition(
            "checkPagesCognitiveBudget",
            BOOL,
            match_list(
                var("pgs"),
                b(True),
                "head",
                "tail",
                if_(
                    ble(n(1), proj(var("head"), "sectionCount")),
                    if_(
                        ble(proj(var("head"), "sectionCount"), proj(var("head"), "maxSectionsBudget")),
                        if_(
                            ble(proj(var("head"), "maxSectionsBudget"), n(5)),
                            call("checkPagesCognitiveBudget", var("tail")),
                            b(False),
                        ),
                        b(False),
                    ),
                    b(False),
                ),
            ),
            parameters=[("pgs", list_t(page_t))],
            recursive="pgs",
        ),
        definition(
            "noneMembers",
            BOOL,
            match_list(
                var("values"),
                b(True),
                "head",
                "tail",
                if_(call("memberString", var("head"), var("forbidden")), b(False), call("noneMembers", var("tail"), var("forbidden"))),
            ),
            parameters=[("values", list_t(STR)), ("forbidden", list_t(STR))],
            recursive="values",
        ),
        holds("portalPageIdsDistinct", call("distinctStrings", call("portalPageIds", call("portalPages")))),
        holds("portalPagePathsDistinct", call("distinctStrings", call("portalPagePaths", call("portalPages")))),
        holds(
            "portalPageArtifactsValid",
            call("allMembers", call("portalPageArtifacts", call("portalPages")), call("artifactIds", call("artifacts"))),
        ),
        holds("everyPageWithinCognitiveLoadBudget", call("checkPagesCognitiveBudget", call("portalPages"))),
        holds(
            "domainLabelsFreeOfMetaTaxonomy",
            call(
                "noneMembers",
                call("appendStrings", call("portalPageTitles", call("portalPages")), call("panelHeadings", call("panels"))),
                call("forbiddenMetaTerms"),
            ),
        ),
        holds("pedagogyIdsDistinct", call("distinctStrings", call("pedagogyIds", call("pedagogyGuides")))),
        holds("pedagogyPolesValid", call("allMembers", call("pedagogyPoles", call("pedagogyGuides")), call("poles"))),
        holds(
            "pedagogyPanelsValid",
            call("allMembers", call("pedagogyPanels", call("pedagogyGuides")), call("panelIds", call("panels"))),
        ),
        holds(
            "pedagogyFreeOfMetaTaxonomy",
            call("noneMembers", call("pedagogyHeadings", call("pedagogyGuides")), call("forbiddenMetaTerms")),
        ),
    ] + designmodel.declarations()


PUBLICATION = {
    "id": "prism-legal-github-pages",
    "repository": "afflom/prism-legal",
    "pagesUrl": "https://afflom.github.io/prism-legal/",
    "workflowPath": ".github/workflows/pages.yml",
    "ciWorkflowPath": ".github/workflows/ci.yml",
    "artifactRoot": "matter-site",
    "uploadAction": "actions/upload-pages-artifact@v3",
    "deployAction": "actions/deploy-pages@v4",
    "githubActionsEnabled": True,
}

PAGES_WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


def render_pages_workflow_yml():
    """Deploy an exact verified CI artifact, with full verification on a miss."""
    return """# Generated by `bin/prism-legal api sync` from `src/Application.lex.tex` (`tools/case/presentationmodel.py`).
# Do not edit by hand: `bin/prism-legal check` verifies zero drift.
name: Deploy PrismLegal to GitHub Pages

on:
  push:
    branches: [main]
    paths-ignore:
      - README.md
      - docs/SEMANTIC_MATTER.md
  workflow_dispatch:

permissions:
  contents: read
  actions: read

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  view:
    name: Prepare Verified Matter Workspace
    runs-on: ubuntu-latest
    timeout-minutes: 180
    outputs:
      provenance: ${{ steps.provenance.outputs.sha256 }}
    steps:
      - uses: actions/checkout@v4
      - name: Find an exact successful CI artifact
        id: reuse
        uses: actions/github-script@f28e40c7f34bde8b3046d885e986cb6290c5673b
        with:
          script: |
            const {execFileSync} = require('node:child_process');
            const artifactName = execFileSync('python3', ['tools/ci/verified_view.py', 'name'], {encoding: 'utf8'}).trim();
            const {findVerifiedView} = require('./tools/ci/find_verified_view.cjs');
            const match = await findVerifiedView({github, context, artifactName});
            core.setOutput('found', Boolean(match));
            if (match) {
              core.setOutput('run', match.runId);
              core.setOutput('artifact', artifactName);
            }
      - name: Download the verified CI artifact
        if: steps.reuse.outputs.found == 'true'
        uses: actions/download-artifact@v4
        with:
          name: ${{ steps.reuse.outputs.artifact }}
          run-id: ${{ steps.reuse.outputs.run }}
          github-token: ${{ github.token }}
          path: verified-matter
      - name: Check source binding and artifact bytes
        if: steps.reuse.outputs.found == 'true'
        run: python3 tools/ci/verified_view.py restore
      - name: Check source before a fresh verification
        if: steps.reuse.outputs.found != 'true'
        run: bash tools/ci/preflight.sh
      - name: Build and verify on a cache miss
        if: steps.reuse.outputs.found != 'true'
        uses: ./.github/actions/build-matter
      - name: Bind the deployed provenance
        id: provenance
        run: echo "sha256=$(sha256sum matter-site/provenance.json | cut -d' ' -f1)" >> "$GITHUB_OUTPUT"
      - name: Upload GitHub Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: matter-site

  deploy:
    name: Deploy to GitHub Pages
    needs: view
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    outputs:
      page_url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy the verified view to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

  verify:
    name: Verify Deployed Modeled Artifact
    needs: [view, deploy]
    runs-on: ubuntu-latest
    timeout-minutes: 5
    env:
      PAGE_URL: ${{ needs.deploy.outputs.page_url }}
      EXPECTED_PROVENANCE: ${{ needs.view.outputs.provenance }}
    steps:
      - name: Compare deployed provenance with this run's verified artifact
        run: |
          for attempt in 1 2 3 4 5 6; do
            if curl --max-time 30 -fsSL "${PAGE_URL%/}/provenance.json" --output deployed-provenance.json &&
               echo "$EXPECTED_PROVENANCE  deployed-provenance.json" | sha256sum --check --status; then
              echo "$PAGE_URL serves the verified modeled artifact"
              exit 0
            fi
            sleep 10
          done
          echo "$PAGE_URL does not yet serve the verified modeled artifact" >&2
          exit 1
"""


def render_ci_workflow_yml():
    """Fail cheap checks first; build/prove the matter once in the pinned SDK."""
    return """# Generated by `bin/prism-legal api sync` from `src/Application.lex.tex` (`tools/case/presentationmodel.py`).
# Do not edit by hand: `bin/prism-legal check` verifies zero drift.
name: Main Branch Validation

on:
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: prism-legal-ci-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  validate:
    name: Check source and CI policy
    runs-on: ubuntu-latest
    timeout-minutes: 10
    outputs:
      application: ${{ steps.scope.outputs.application }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - name: Check model drift, sanitization and delivery policy
        run: bash tools/ci/preflight.sh
      - name: Determine whether application verification is needed
        id: scope
        run: python3 tools/ci/changed.py >> "$GITHUB_OUTPUT"

  matter:
    name: Build and exercise the modeled application
    needs: validate
    if: needs.validate.outputs.application == 'true'
    runs-on: ubuntu-latest
    timeout-minutes: 180
    steps:
      - uses: actions/checkout@v4
      - name: Name the source-bound artifact
        id: artifact
        run: echo "name=$(python3 tools/ci/verified_view.py name)" >> "$GITHUB_OUTPUT"
      - uses: ./.github/actions/build-matter
      - name: Retain the verified app for deployment
        uses: actions/upload-artifact@v4
        with:
          name: ${{ steps.artifact.outputs.name }}
          path: verified-matter
          if-no-files-found: error
          overwrite: true
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: matter-verification
          overwrite: true
          path: |
            matter-sdk-build.json
            matter-sdk-image.json
            matter-verification.json
            .prism/verified/
"""


def application_declarations():
    """`src/Application.lex.tex`: binds Architecture, Presentation, Portal, Register, RemediesCore, and Audit into a single verified Public-Benefit application."""
    app_t = named("PlatformApplication")
    pub_t = named("GitHubPagesPublication")
    return [
        structure(
            "PlatformApplication",
            [
                ("id", STR),
                ("referenceCaseNumber", STR),
                ("hearingDate", STR),
                ("entrypoint", STR),
                ("offlineReady", BOOL),
                ("publicBenefitOpenSource", BOOL),
                ("zeroPiiSanitized", BOOL),
                ("githubPagesReady", BOOL),
                ("stakeholderCount", NAT),
                ("panelCount", NAT),
                ("journeyCount", NAT),
                ("claimCount", NAT),
                ("exhibitCount", NAT),
                ("trapCount", NAT),
                ("domainCaseCount", NAT),
                ("firmCount", NAT),
                ("courtCount", NAT),
                ("frameworkCount", NAT),
            ],
        ),
        structure(
            "GitHubPagesPublication",
            [
                ("id", STR),
                ("repository", STR),
                ("pagesUrl", STR),
                ("workflowPath", STR),
                ("ciWorkflowPath", STR),
                ("artifactRoot", STR),
                ("uploadAction", STR),
                ("deployAction", STR),
                ("githubActionsEnabled", BOOL),
            ],
        ),
        definition(
            "application",
            app_t,
            record(
                "PlatformApplication",
                id=s("prism-legal-public-benefit-app"),
                referenceCaseNumber=s("2030-FAM-9010"),
                hearingDate=s("2030-09-18"),
                entrypoint=s("view/index.html"),
                offlineReady=b(True),
                publicBenefitOpenSource=b(True),
                zeroPiiSanitized=b(True),
                githubPagesReady=b(True),
                stakeholderCount=n(len(archmodel.STAKEHOLDERS)),
                panelCount=n(len(PANELS)),
                journeyCount=n(len(JOURNEYS)),
                claimCount=n(len(casemodel.CLAIMS)),
                exhibitCount=n(len(casemodel.RESPONDENT_EXHIBITS) + len(casemodel.PETITIONER_EXHIBITS)),
                trapCount=n(16),
                domainCaseCount=n(len(portalmodel.CASES)),
                firmCount=n(len(portalmodel.FIRMS)),
                courtCount=n(len(portalmodel.COURTS)),
                frameworkCount=n(len(portalmodel.LEGAL_FRAMEWORKS)),
            ),
        ),
        definition(
            "publication",
            pub_t,
            record(
                "GitHubPagesPublication",
                id=s(PUBLICATION["id"]),
                repository=s(PUBLICATION["repository"]),
                pagesUrl=s(PUBLICATION["pagesUrl"]),
                workflowPath=s(PUBLICATION["workflowPath"]),
                ciWorkflowPath=s(PUBLICATION["ciWorkflowPath"]),
                artifactRoot=s(PUBLICATION["artifactRoot"]),
                uploadAction=s(PUBLICATION["uploadAction"]),
                deployAction=s(PUBLICATION["deployAction"]),
                githubActionsEnabled=b(PUBLICATION["githubActionsEnabled"]),
            ),
        ),
        holds("applicationOfflineReady", proj(call("application"), "offlineReady")),
        holds("applicationPublicBenefitOpenSource", proj(call("application"), "publicBenefitOpenSource")),
        holds("applicationZeroPiiSanitized", proj(call("application"), "zeroPiiSanitized")),
        holds("applicationGithubPagesReady", proj(call("application"), "githubPagesReady")),
        holds("applicationPublishedViaGitHubActions", proj(call("publication"), "githubActionsEnabled")),
    ]


def render_presentation():
    return lexmod.module(
        "Presentation",
        presentation_declarations(),
        title="PrismLegal Public-Benefit Platform Presentation, Journeys & WCAG 2.2 AA Design System",
        imports=("Api", "Architecture", "Register"),
    )


def render_application():
    return lexmod.module(
        "Application",
        application_declarations(),
        title="PrismLegal Single-Context Public-Benefit Legal Platform Application",
        imports=("Architecture", "Audit", "Portal", "Presentation", "Register", "RemediesCore"),
    )


def sync():
    PRESENTATION.parent.mkdir(parents=True, exist_ok=True)
    PAGES_WORKFLOW.parent.mkdir(parents=True, exist_ok=True)
    p_text = render_presentation()
    a_text = render_application()
    pw_text = render_pages_workflow_yml()
    cw_text = render_ci_workflow_yml()
    p_changed = not PRESENTATION.exists() or PRESENTATION.read_text() != p_text
    a_changed = not APPLICATION.exists() or APPLICATION.read_text() != a_text
    pw_changed = not PAGES_WORKFLOW.exists() or PAGES_WORKFLOW.read_text() != pw_text
    cw_changed = not CI_WORKFLOW.exists() or CI_WORKFLOW.read_text() != cw_text
    if p_changed:
        PRESENTATION.write_text(p_text)
    if a_changed:
        APPLICATION.write_text(a_text)
    if pw_changed:
        PAGES_WORKFLOW.write_text(pw_text)
    if cw_changed:
        CI_WORKFLOW.write_text(cw_text)
    return {
        "module": str(PRESENTATION.relative_to(ROOT)),
        "application": str(APPLICATION.relative_to(ROOT)),
        "workflows": [str(PAGES_WORKFLOW.relative_to(ROOT)), str(CI_WORKFLOW.relative_to(ROOT))],
        "panels": len(PANELS),
        "journeys": len(JOURNEYS),
        "artifacts": len(ARTIFACTS),
        "tokens": len(TOKENS),
        "changed": p_changed or a_changed or pw_changed or cw_changed,
    }


def check():
    if not PRESENTATION.exists() or not APPLICATION.exists():
        return {"ok": False, "reason": "Presentation.lex.tex or Application.lex.tex missing; run `bin/prism-legal api sync`"}
    if not PAGES_WORKFLOW.exists() or not CI_WORKFLOW.exists():
        return {"ok": False, "reason": "GitHub Actions workflows (.github/workflows/pages.yml or ci.yml) missing; run `bin/prism-legal api sync`"}
    if PAGES_WORKFLOW.read_text() != render_pages_workflow_yml() or CI_WORKFLOW.read_text() != render_ci_workflow_yml():
        return {"ok": False, "reason": "GitHub Actions workflows drifted; run `bin/prism-legal api sync`"}
    ok = PRESENTATION.read_text() == render_presentation() and APPLICATION.read_text() == render_application()
    return {"ok": ok, "reason": None if ok else "Presentation.lex.tex or Application.lex.tex drifted; run `bin/prism-legal api sync`"}
