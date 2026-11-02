"""In-Browser Intake Classifiers & Multi-Head Attention Extrapolation Engine
modeled as a compiled LexLean semantic module (`src/Intake.lex.tex`) and
PrismPM register (`model/intake.toml`).

Following the certified neural classifier pattern of `UOR-Foundation/MNIST`
(`dot`, `requant`, `argmax`, `contract`, `realization`, `model`, `checked_apply`)
and the inductive/deductive synthesis architecture of `rule30`
(`Engine.lex.tex` Hebbian strategy scheduling + `Discovery.lex.tex` F_2 relation
and Berlekamp-Massey recurrence matching):

1. Zero Defaults Guarantee:
   - Every `AttentionHead` has zero prior bias (`biases = [0, 0, 0, 0, 0, 0]`),
     so zero intake signal `[0, 0, 0, 0, 0, 0, 0, 0]` produces strictly zero
     attention activation (`[0, 0, 0, 0, 0, 0]`, theorem `zeroIntakeProducesZeroScores`).
   - The contract precondition `IsIntakeVector` requires positive signal energy
     (`vectorEnergy(features) > 0`), so `isIntakeVectorCheck([0,0,0,0,0,0,0,0]) = false`
     (theorem `zeroIntakeRejected`) and `classifyIntake` refuses empty intake
     rather than emitting any default class.
2. Every schema element in the PrismLegal model (`SCHEMA_CLASSIFIERS`, 12 schema
   elements covering front matter, relief goals, timeline events, exhibits,
   statutory claims, witnesses, cross-exam traps, direct examination, visual
   forensics, remedy calculators, hearing clock stages, and counsel alignment
   agenda) has a formal `SchemaClassifier` with its own bespoke key matrix.
3. Every node in the model is an `AttentionHead` (`NODE_ATTENTION_HEADS`, 18
   heads across all 12 schema elements and 6 legal domain nodes) with quantized
   integer `query` weights, bespoke `keys` matrix, zero `biases`, fixed-point
   `multiplier` and `shift`, and target `classLabels`.
4. In the browser (`docs/index.html`, `docs/client.html`, `docs/lawyer.html`,
   `docs/courtroom.html`), the attention heads run client-side over the user's
   actual intake clauses, dates, numbers, and exhibits to synthesize bespoke
   case completions with zero canned defaults."""

import json
from . import ROOT, lexmod
from .semantic import (
    BOOL,
    NAT,
    STR,
    all_members,
    b,
    beq,
    ble,
    blt,
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

MODULE = ROOT / "src" / "Intake.lex.tex"
LEDGER = ROOT / "model" / "intake.toml"
NAME = "Intake"
LEAN_MODULE = "PrismLegal.Intake"

FEATURE_DIM = 8
MAX_CHANNEL = 255
NUM_DOMAIN_CLASSES = 6
EFFECTS = {"effects": ["allocation", "overflow", "recursion"], "targets": ["rust-std"]}
PRODUCTION_ROOTS = {
    "classifyIntake": EFFECTS,
    "classifyAllHeads": EFFECTS,
}

# 8-channel lexical & structural intake feature basis (each channel in [0, 255], 0 when absent):
#   ch0: parenting / custody / overnights / school / decision-making signal
#   ch1: housing / lease / habitability / mold / heat / eviction / rent escrow signal
#   ch2: veterans / VA / 38 CFR / service-connected / TDIU / nexus / rating signal
#   ch3: employment / ADA / accommodation / retaliation / HR / FMLA / Title VII signal
#   ch4: commercial / UCC / contract / delivery / nonconforming / invoice / cure signal
#   ch5: fiduciary / business / DGCL / partnership / accounting / buyout / ledger signal
#   ch6: documentary corroboration density (exhibits, timestamps, bank/tax/certified records)
#   ch7: adversarial / impeachment / completeness urgency (prior inconsistent statement, omission, trap)
FEATURE_CHANNELS = [
    {
        "index": 0,
        "id": "ch-family-custody",
        "label": "Parenting, Custody & Support Signal",
        "keywords": [
            "parenting", "custody", "overnight", "overnights", "child", "children",
            "dependent", "dependents", "school", "decision-making", "50/50", "support",
            "coparenting", "visitation", "parent", "guardian", "best interests", "402", "305",
        ],
    },
    {
        "index": 1,
        "id": "ch-housing-habitability",
        "label": "Housing, Lease & Habitability Signal",
        "keywords": [
            "tenant", "landlord", "lease", "rent", "habitability", "eviction",
            "mold", "heat", "heating", "plumbing", "code", "inspection", "escrow",
            "abatement", "apartment", "premises", "retaliatory", "urlta", "repair",
        ],
    },
    {
        "index": 2,
        "id": "ch-veterans-disability",
        "label": "Veterans Benefits & Disability Rating Signal",
        "keywords": [
            "veteran", "veterans", "va", "tdiu", "service-connected", "rating",
            "38 cfr", "bva", "nexus", "tinnitus", "lumbar", "unemployability",
            "c-file", "dbq", "benefit", "1781", "disability", "schedular",
        ],
    },
    {
        "index": 3,
        "id": "ch-employment-ada",
        "label": "Employment, ADA & Workplace Retaliation Signal",
        "keywords": [
            "employment", "employer", "employee", "workplace", "ada", "accommodation",
            "ergonomic", "remote", "hr", "retaliation", "termination", "pip",
            "eeoc", "title vii", "fmla", "wage", "overtime", "interactive process",
        ],
    },
    {
        "index": 4,
        "id": "ch-commercial-ucc",
        "label": "Commercial Contract, Consumer & UCC Signal",
        "keywords": [
            "commercial", "contract", "ucc", "buyer", "seller", "goods", "shipment",
            "delivery", "nonconforming", "rejection", "revocation", "cure", "warranty",
            "invoice", "purchase order", "breach", "cover", "fdcpa", "validation", "debt",
        ],
    },
    {
        "index": 5,
        "id": "ch-fiduciary-governance",
        "label": "Business Governance & Fiduciary Accounting Signal",
        "keywords": [
            "fiduciary", "member", "llc", "corporation", "shareholder", "partner",
            "partnership", "dgcl", "books and records", "220", "accounting", "buyout",
            "diversion", "operating agreement", "board", "distribution", "k-1",
        ],
    },
    {
        "index": 6,
        "id": "ch-corroboration-density",
        "label": "Multi-Modal Documentary, Visual & Cryptographic Corroboration Density",
        "keywords": [
            "exhibit", "certified", "bank", "tax", "ledger", "photo", "photograph", "image",
            "video", "audio", "pdf", "csv", "scan", "handwritten", "badge", "sha256",
            "statement", "receipt", "log", "email", "letter", "report", "stipulated",
            "contract", "notice", "medical", "record", "affidavit", "transcript", "upload",
        ],
    },
    {
        "index": 7,
        "id": "ch-impeachment-completeness",
        "label": "Impeachment, Completeness Context & Procedural Filing Urgency Signal",
        "keywords": [
            "omission", "undisclosed", "contradiction", "inconsistent", "selective",
            "excerpt", "completeness", "106", "608", "613", "26(e)", "16.2",
            "rebuttal", "allegation", "disputed", "hostile", "impeach", "escrow",
            "deadline", "filing", "motion", "subpoena", "pretrial", "timely",
        ],
    },
]

# Every schema element in the PrismPM model has a formal classifier (12 Schema Classifiers)
SCHEMA_CLASSIFIERS = [
    {
        "id": "schema-case-meta",
        "schemaElement": "caseMeta",
        "title": "Case Front Matter & Jurisdiction Classifier",
        "headId": "HEAD-01",
        "classes": [
            "DOM-FAM-103",
            "DOM-HOU-URLTA",
            "DOM-VET-38CFR",
            "DOM-EMP-ADA",
            "DOM-COM-UCC",
            "DOM-BIZ-DGCL",
        ],
        "extrapolationTarget": "Infers governing legal framework and statutory authority strictly from non-empty user intake tokens.",
    },
    {
        "id": "schema-relief-goal",
        "schemaElement": "reliefGoals",
        "title": "Relief Goals & Requested Judicial Orders Classifier",
        "headId": "HEAD-02",
        "classes": [
            "relief-parenting-and-guideline-support",
            "relief-habitability-repairs-and-abatement",
            "relief-schedular-tdiu-and-effective-date",
            "relief-accommodation-and-wage-remedy",
            "relief-contract-rejection-or-validation",
            "relief-fiduciary-accounting-and-distributions",
        ],
        "extrapolationTarget": "Synthesizes bespoke relief orders directly from the user's intake clauses, party names, and requested terms.",
    },
    {
        "id": "schema-timeline-event",
        "schemaElement": "timeline",
        "title": "Chronological Event & Fact Intake Classifier",
        "headId": "HEAD-03",
        "classes": [
            "event-caregiving-and-schedule-compliance",
            "event-repair-notice-and-escrow-deposit",
            "event-claim-filing-and-medical-opinion",
            "event-accommodation-request-and-response",
            "event-notice-of-dispute-or-nonconformity",
            "event-agreement-execution-and-audit",
        ],
        "extrapolationTarget": "Extracts dated factual clauses from user intake into chronological timeline events linked to user exhibits.",
    },
    {
        "id": "schema-exhibit",
        "schemaElement": "exhibits",
        "title": "Documentary & Visual Evidence Intake Classifier",
        "headId": "HEAD-04",
        "classes": [
            "fre-901-authenticated-log",
            "fre-803-6-business-record",
            "fre-801d2-opposing-admission",
            "fre-106-completeness-context",
            "frcp-26e-disclosure-audit",
            "fre-1006-voluminous-summary",
        ],
        "extrapolationTarget": "Computes bespoke evidentiary foundation, purpose, and visual callouts for each user-supplied document.",
    },
    {
        "id": "schema-claim",
        "schemaElement": "claims",
        "title": "Statutory Propositions & Proof Matrix Classifier",
        "headId": "HEAD-05",
        "classes": [
            "claim-best-interests-allocation",
            "claim-warranty-habitability-breach",
            "claim-tdiu-service-connection",
            "claim-ada-reasonable-accommodation",
            "claim-ucc-or-fdcpa-compliance",
            "claim-fiduciary-duty-accounting",
        ],
        "extrapolationTarget": "Synthesizes bespoke statutory claims and rule exceptions directly from the user's goals, timeline, and exhibits.",
    },
    {
        "id": "schema-witness",
        "schemaElement": "witnesses",
        "title": "Witness Roster & Examination Scope Classifier",
        "headId": "HEAD-06",
        "classes": [
            "witness-coparent-and-corroborator",
            "witness-tenant-and-code-inspector",
            "witness-claimant-and-medical-examiner",
            "witness-employee-and-hr-representative",
            "witness-contract-party-and-custodian",
            "witness-member-and-forensic-accountant",
        ],
        "extrapolationTarget": "Builds bespoke witness examination scopes referencing the user's actual party names, dates, and exhibits.",
    },
    {
        "id": "schema-trap",
        "schemaElement": "traps",
        "title": "Cross-Examination Trap & FRE 106 Rebuttal Classifier",
        "headId": "HEAD-07",
        "classes": [
            "documentary-impeachment",
            "statutory-factor-deduction",
            "stipulated-anchor-lock",
            "calm-opening-pivot",
            "fre-106-completeness-restoration",
            "affirmative-cure-and-mitigation",
        ],
        "extrapolationTarget": "Synthesizes bespoke anticipated cross-examination challenges and calm responses anchored to the user's exhibits.",
    },
    {
        "id": "schema-direct-exam",
        "schemaElement": "directExam",
        "title": "Direct Examination Q&A Script Classifier",
        "headId": "HEAD-08",
        "classes": [
            "dx-parenting-and-financial-walkthrough",
            "dx-habitability-notice-and-escrow",
            "dx-service-history-and-functional-limits",
            "dx-essential-duties-and-accommodation",
            "dx-contract-terms-and-validation-demand",
            "dx-governance-instrument-and-ledger-audit",
        ],
        "extrapolationTarget": "Constructs bespoke Direct Examination Q&A scripts from the user's actual goals, timeline dates, and exhibits.",
    },
    {
        "id": "schema-visual-forensics",
        "schemaElement": "visualForensics",
        "title": "Visual Evidence Callout & Proponent Intent Classifier",
        "headId": "HEAD-09",
        "classes": [
            "vis-schedule-log-and-notebook-completeness",
            "vis-inspection-citation-and-escrow-receipts",
            "vis-rating-code-sheet-and-nexus-opinion",
            "vis-evaluation-metrics-and-hr-thread",
            "vis-validation-letter-and-assignment-gap",
            "vis-operating-clause-and-k1-reconciliation",
        ],
        "extrapolationTarget": "Generates bespoke page/paragraph visual inspection notes tailored to each user exhibit's title and purpose.",
    },
    {
        "id": "schema-calculator",
        "schemaElement": "calculators",
        "title": "Statutory & Financial Remedy Calculator Classifier",
        "headId": "HEAD-10",
        "classes": [
            "calc-family-305-shared-support",
            "calc-housing-urlta-rent-abatement",
            "calc-veterans-38cfr-combined-rating",
            "calc-employment-backpay-and-damages",
            "calc-commercial-ucc-cover-damages",
            "calc-fiduciary-disgorgement-surcharge",
        ],
        "extrapolationTarget": "Extracts monetary amounts, percentages, and durations from user intake into the governing statutory calculator.",
    },
    {
        "id": "schema-hearing-stage",
        "schemaElement": "hearingStages",
        "title": "Homeostatic Hearing Clock Stage Classifier",
        "headId": "HEAD-11",
        "classes": [
            "clock-evidentiary-Custody-hearing",
            "clock-housing-abatement-hearing",
            "clock-administrative-review-hearing",
            "clock-workplace-remedy-hearing",
            "clock-commercial-dispute-hearing",
            "clock-fiduciary-accounting-hearing",
        ],
        "extrapolationTarget": "Allocates hearing-stage minute budgets proportional to the user's witness roster and hearing duration.",
    },
    {
        "id": "schema-agenda",
        "schemaElement": "agenda",
        "title": "Client–Counsel Strategy Co-Design Agenda Classifier",
        "headId": "HEAD-12",
        "classes": [
            "agenda-stipulations-and-disclosure-audit",
            "agenda-escrow-release-and-inspection",
            "agenda-effective-date-and-nexus",
            "agenda-interactive-process-and-mitigation",
            "agenda-chain-of-title-and-hearsay-motion",
            "agenda-fre1006-summary-and-audit-scope",
        ],
        "extrapolationTarget": "Generates bespoke Client–Counsel alignment notes for actual exhibits and unbacked claims in the user's intake.",
    },
    {
        "id": "schema-multimodal-upload",
        "schemaElement": "multimodalUploads",
        "title": "Multi-Modal Evidence Upload Parser & Case Linker Classifier",
        "headId": "HEAD-19",
        "classes": [
            "modality-pleading-or-court-order",
            "modality-financial-ledger-or-tax-csv",
            "modality-visual-photo-or-premises-media",
            "modality-handwritten-notebook-or-scan",
            "modality-digital-message-or-email-thread",
            "modality-official-certificate-or-medical-record",
        ],
        "extrapolationTarget": "Parses client-side PDF, image, CSV, text, email, and audio/video uploads, computes SHA-256 digests, and links extracted facts to case elements.",
    },
    {
        "id": "schema-jural-posture",
        "schemaElement": "juralPosture",
        "title": "Enforceable Legal Right, Duty, Power & Immunity Classifier",
        "headId": "HEAD-20",
        "classes": [
            "jural-enforceable-claim-right-and-duty",
            "jural-joint-governance-authority",
            "jural-statutory-benefit-immunity",
            "jural-disclosure-reopening-remedy",
            "jural-completeness-restoration-right",
            "jural-fiduciary-accounting-entitlement",
        ],
        "extrapolationTarget": "Maps each synthesized statutory claim to its enforceable legal posture and controlling statutory exception.",
    },
    {
        "id": "schema-filing-artifact",
        "schemaElement": "filingArtifacts",
        "title": "Court-Ready Filing Packet & Pleading Generator Classifier",
        "headId": "HEAD-21",
        "classes": [
            "filing-parenting-and-support-position-statement",
            "filing-habitability-abatement-and-escrow-motion",
            "filing-veterans-tdiu-and-nexus-brief",
            "filing-workplace-accommodation-and-remedy-brief",
            "filing-commercial-validation-and-rejection-brief",
            "filing-fiduciary-accounting-and-audit-petition",
        ],
        "extrapolationTarget": "Generates bespoke court-captioned pleadings, exhibit indexes, witness disclosures, and proposed findings from the user's matter.",
    },
    {
        "id": "schema-filing-deadline",
        "schemaElement": "filingDeadlines",
        "title": "Procedural Timeline & On-Time Filing Schedule Classifier",
        "headId": "HEAD-22",
        "classes": [
            "deadline-mandatory-financial-and-exhibit-disclosures",
            "deadline-municipal-inspection-and-escrow-notice",
            "deadline-administrative-record-and-medical-submission",
            "deadline-interactive-process-and-pretrial-exchange",
            "deadline-statutory-validation-and-cure-window",
            "deadline-books-and-records-and-summary-tieout",
        ],
        "extrapolationTarget": "Computes backward-scheduled statutory filing deadlines from the user's hearing date and exports calendar reminders.",
    },
]

# Bespoke 6x8 key matrices per attention head role (with zero default bias)
_DOMAIN_KEYS = [
    [16, 1, 2, 1, 1, 1, 4, 4],  # Class 0: Family Law (DOM-FAM-103)
    [1, 16, 1, 1, 2, 1, 4, 3],  # Class 1: Housing / URLTA (DOM-HOU-URLTA)
    [2, 1, 16, 2, 1, 1, 4, 2],  # Class 2: Veterans / 38 CFR (DOM-VET-38CFR)
    [1, 1, 2, 16, 1, 2, 4, 4],  # Class 3: Employment / ADA (DOM-EMP-ADA)
    [1, 2, 1, 1, 16, 2, 4, 3],  # Class 4: Commercial / UCC (DOM-COM-UCC)
    [1, 1, 1, 2, 2, 16, 4, 4],  # Class 5: Business / Fiduciary (DOM-BIZ-DGCL)
]

_EXHIBIT_KEYS = [
    [14, 6, 4, 6, 4, 4, 14, 4],  # Class 0: FRE 901 Authenticated Log / Timeline
    [4, 14, 14, 6, 10, 12, 16, 4],  # Class 1: FRE 803(6) Certified Business / Official Record
    [6, 8, 4, 16, 12, 8, 10, 12],  # Class 2: FRE 801(d)(2) Opposing Party Admission
    [12, 4, 4, 8, 6, 4, 10, 16],  # Class 3: FRE 106 Rule of Completeness Context
    [10, 6, 4, 6, 8, 16, 12, 16],  # Class 4: FRCP 26(e) / Rule 16.2 Mandatory Disclosure Audit
    [6, 6, 8, 6, 16, 14, 16, 8],  # Class 5: FRE 1006 Voluminous Financial / Damage Summary
]

_TRAP_KEYS = [
    [8, 8, 6, 10, 10, 12, 14, 16],  # Class 0: Documentary Impeachment (FRE 608/613/26(e))
    [16, 10, 14, 8, 8, 8, 12, 6],   # Class 1: Statutory Factor Deduction
    [10, 8, 12, 8, 14, 14, 16, 8],  # Class 2: Stipulated Anchor Lock
    [14, 8, 8, 14, 6, 6, 8, 12],    # Class 3: Calm Opening-Aligned Pivot
    [12, 6, 4, 8, 6, 6, 10, 16],    # Class 4: FRE 106 Completeness Restoration
    [6, 16, 8, 12, 16, 10, 12, 10], # Class 5: Affirmative Cure & Mitigation
]

_MULTIMODAL_KEYS = [
    [12, 10, 10, 8, 10, 10, 14, 10],  # Class 0: Court Pleading / Stipulation / Order PDF
    [8, 10, 6, 6, 14, 16, 16, 12],    # Class 1: Financial Ledger / Bank / Tax / CSV
    [12, 16, 4, 6, 6, 4, 14, 6],      # Class 2: Visual Photograph / Premises / Inspection Media
    [14, 6, 6, 6, 6, 6, 12, 16],      # Class 3: Handwritten Log / Scanned Notebook (FRE 106)
    [14, 8, 4, 16, 10, 6, 12, 14],    # Class 4: Digital Message / Email / Portal Thread
    [8, 12, 16, 12, 6, 6, 16, 4],     # Class 5: Official Certificate / Medical / Agency Record
]

_JURAL_KEYS = [
    [16, 14, 8, 12, 14, 8, 12, 6],    # Class 0: Enforceable Claim-Right & Correlative Duty
    [14, 6, 4, 10, 8, 14, 10, 8],     # Class 1: Joint Governance Authority & Decision Power
    [10, 6, 16, 12, 6, 6, 14, 6],     # Class 2: Statutory Benefit & Exemption Immunity
    [10, 8, 4, 8, 10, 14, 12, 16],    # Class 3: Mandatory Disclosure Reopening Power
    [12, 6, 4, 10, 8, 6, 12, 16],     # Class 4: FRE 106 Completeness Restoration Right
    [4, 8, 4, 6, 14, 16, 16, 12],     # Class 5: Fiduciary Accounting & Audit Entitlement
]

_FILING_KEYS = [
    [16, 2, 2, 2, 2, 2, 10, 8],       # Class 0: Family Law Position Statement & Worksheets
    [2, 16, 2, 2, 4, 2, 10, 8],       # Class 1: Housing Habitability & Rent Escrow Motion
    [2, 2, 16, 4, 2, 2, 10, 6],       # Class 2: Veterans TDIU & Nexus Appeal Brief
    [2, 2, 4, 16, 2, 4, 10, 8],       # Class 3: Employment Accommodation & Remedy Brief
    [2, 4, 2, 2, 16, 4, 10, 8],       # Class 4: Commercial / FDCPA Validation & Rejection Brief
    [2, 2, 2, 4, 4, 16, 12, 10],      # Class 5: Fiduciary Accounting & Rule 1006 Audit Petition
]

_ZERO_BIASES = [0, 0, 0, 0, 0, 0]

# Every node in the PrismLegal model is an AttentionHead with zero default bias and its own keys matrix (18 Heads)
NODE_ATTENTION_HEADS = [
    {
        "id": "HEAD-01",
        "nodeId": "node-case-meta",
        "schemaId": "schema-case-meta",
        "title": "Front-Matter & Jurisdiction Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 2, 2],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[0]["classes"],
        "inductiveRelation": "corroborated-finding = equal-overnights XOR routine-continuity",
        "deductiveStrategy": "statutory-factor-deduction",
    },
    {
        "id": "HEAD-02",
        "nodeId": "node-relief-goal",
        "schemaId": "schema-relief-goal",
        "title": "Relief Posture & Requested Orders Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 3, 2],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[1]["classes"],
        "inductiveRelation": "order-compliant = one XOR (equal-overnights AND routine-continuity)",
        "deductiveStrategy": "stipulated-anchor-lock",
    },
    {
        "id": "HEAD-03",
        "nodeId": "node-timeline-event",
        "schemaId": "schema-timeline-event",
        "title": "Chronological Fact & Sequence Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 4, 2],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[2]["classes"],
        "inductiveRelation": "equalOvernights recurrence c(D) = [1, 0, 1]",
        "deductiveStrategy": "statutory-factor-deduction",
    },
    {
        "id": "HEAD-04",
        "nodeId": "node-exhibit-intake",
        "schemaId": "schema-exhibit",
        "title": "Evidence Intake & Admissibility Foundation Attention Head",
        "query": [3, 3, 3, 3, 3, 3, 5, 4],
        "keys": _EXHIBIT_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[3]["classes"],
        "inductiveRelation": "disclosure-reopening = reserve-omission",
        "deductiveStrategy": "documentary-impeachment",
    },
    {
        "id": "HEAD-05",
        "nodeId": "node-claim-synthesis",
        "schemaId": "schema-claim",
        "title": "Statutory Claim & Proof Matrix Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 4, 3],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[4]["classes"],
        "inductiveRelation": "corroborated-finding = equal-overnights XOR routine-continuity",
        "deductiveStrategy": "statutory-factor-deduction",
    },
    {
        "id": "HEAD-06",
        "nodeId": "node-witness-plan",
        "schemaId": "schema-witness",
        "title": "Witness Roster & Scope Allocation Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 3, 3],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[5]["classes"],
        "inductiveRelation": "jointGovernance recurrence c(D) = [1, 1, 1]",
        "deductiveStrategy": "calm-opening-pivot",
    },
    {
        "id": "HEAD-07",
        "nodeId": "node-trap-rebuttal",
        "schemaId": "schema-trap",
        "title": "Cross-Examination Trap & Pivot Attention Head",
        "query": [3, 3, 3, 3, 3, 3, 4, 5],
        "keys": _TRAP_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[6]["classes"],
        "inductiveRelation": "unilateral-act = one XOR joint-governance",
        "deductiveStrategy": "documentary-impeachment",
    },
    {
        "id": "HEAD-08",
        "nodeId": "node-direct-script",
        "schemaId": "schema-direct-exam",
        "title": "Direct Examination Q&A Synthesis Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 4, 2],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[7]["classes"],
        "inductiveRelation": "weekParity recurrence c(D) = [1, 1, 1, 1]",
        "deductiveStrategy": "statutory-factor-deduction",
    },
    {
        "id": "HEAD-09",
        "nodeId": "node-visual-callout",
        "schemaId": "schema-visual-forensics",
        "title": "Visual Evidence Callout & Intent Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 5, 3],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[8]["classes"],
        "inductiveRelation": "disclosure-reopening = reserve-omission",
        "deductiveStrategy": "documentary-impeachment",
    },
    {
        "id": "HEAD-10",
        "nodeId": "node-remedy-calc",
        "schemaId": "schema-calculator",
        "title": "Statutory & Financial Calculator Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 3, 2],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[9]["classes"],
        "inductiveRelation": "one = statutory-benefit",
        "deductiveStrategy": "stipulated-anchor-lock",
    },
    {
        "id": "HEAD-11",
        "nodeId": "node-hearing-clock",
        "schemaId": "schema-hearing-stage",
        "title": "Homeostatic Hearing Clock Budget Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 2, 3],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[10]["classes"],
        "inductiveRelation": "stageBudgetsFillTheTick = 360",
        "deductiveStrategy": "calm-opening-pivot",
    },
    {
        "id": "HEAD-12",
        "nodeId": "node-counsel-agenda",
        "schemaId": "schema-agenda",
        "title": "Client–Counsel Strategy Agenda Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 3, 4],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[11]["classes"],
        "inductiveRelation": "corroborated-finding = equal-overnights XOR routine-continuity",
        "deductiveStrategy": "statutory-factor-deduction",
    },
    {
        "id": "HEAD-13",
        "nodeId": "node-domain-family",
        "schemaId": "schema-case-meta",
        "title": "Family Law & Parental Responsibilities Domain Node Head",
        "query": [6, 1, 2, 1, 1, 1, 3, 3],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[0]["classes"],
        "inductiveRelation": "corroborated-finding = equal-overnights XOR routine-continuity",
        "deductiveStrategy": "statutory-factor-deduction",
    },
    {
        "id": "HEAD-14",
        "nodeId": "node-domain-housing",
        "schemaId": "schema-case-meta",
        "title": "Housing Defense & Habitability Domain Node Head",
        "query": [1, 6, 1, 1, 2, 1, 3, 3],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[0]["classes"],
        "inductiveRelation": "order-compliant = one XOR (equal-overnights AND routine-continuity)",
        "deductiveStrategy": "documentary-impeachment",
    },
    {
        "id": "HEAD-15",
        "nodeId": "node-domain-veterans",
        "schemaId": "schema-case-meta",
        "title": "Veterans Benefits & 38 CFR Appeals Domain Node Head",
        "query": [2, 1, 6, 2, 1, 1, 3, 2],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[0]["classes"],
        "inductiveRelation": "one = statutory-benefit",
        "deductiveStrategy": "stipulated-anchor-lock",
    },
    {
        "id": "HEAD-16",
        "nodeId": "node-domain-employment",
        "schemaId": "schema-case-meta",
        "title": "Employment Law & ADA Accommodation Domain Node Head",
        "query": [1, 1, 2, 6, 1, 2, 3, 3],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[0]["classes"],
        "inductiveRelation": "unilateral-act = one XOR joint-governance",
        "deductiveStrategy": "documentary-impeachment",
    },
    {
        "id": "HEAD-17",
        "nodeId": "node-domain-commercial",
        "schemaId": "schema-case-meta",
        "title": "Commercial Contract & UCC Article 2 Domain Node Head",
        "query": [1, 2, 1, 1, 6, 2, 3, 3],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[0]["classes"],
        "inductiveRelation": "disclosure-reopening = reserve-omission",
        "deductiveStrategy": "documentary-impeachment",
    },
    {
        "id": "HEAD-18",
        "nodeId": "node-domain-business",
        "schemaId": "schema-case-meta",
        "title": "Business Governance & Fiduciary Accounting Domain Node Head",
        "query": [1, 1, 1, 2, 2, 6, 3, 4],
        "keys": _DOMAIN_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[0]["classes"],
        "inductiveRelation": "disclosure-reopening = reserve-omission",
        "deductiveStrategy": "stipulated-anchor-lock",
    },
    {
        "id": "HEAD-19",
        "nodeId": "node-multimodal-upload",
        "schemaId": "schema-multimodal-upload",
        "title": "Multi-Modal Evidence Upload & Case Relation Attention Head",
        "query": [3, 3, 3, 3, 3, 3, 6, 4],
        "keys": _MULTIMODAL_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[12]["classes"],
        "inductiveRelation": "corroborated-finding = equal-overnights XOR routine-continuity",
        "deductiveStrategy": "documentary-impeachment",
    },
    {
        "id": "HEAD-20",
        "nodeId": "node-jural-posture",
        "schemaId": "schema-jural-posture",
        "title": "Enforceable Legal Posture & Statutory Immunity Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 4, 4],
        "keys": _JURAL_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[13]["classes"],
        "inductiveRelation": "one = statutory-benefit",
        "deductiveStrategy": "statutory-factor-deduction",
    },
    {
        "id": "HEAD-21",
        "nodeId": "node-filing-artifact",
        "schemaId": "schema-filing-artifact",
        "title": "Court-Ready Filing Pleading & Packet Synthesis Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 4, 3],
        "keys": _FILING_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[14]["classes"],
        "inductiveRelation": "order-compliant = one XOR (equal-overnights AND routine-continuity)",
        "deductiveStrategy": "stipulated-anchor-lock",
    },
    {
        "id": "HEAD-22",
        "nodeId": "node-filing-deadline",
        "schemaId": "schema-filing-deadline",
        "title": "Procedural Timeline & On-Time Filing Schedule Attention Head",
        "query": [4, 4, 4, 4, 4, 4, 3, 5],
        "keys": _FILING_KEYS,
        "biases": _ZERO_BIASES,
        "multiplier": 1,
        "shift": 64,
        "classLabels": SCHEMA_CLASSIFIERS[15]["classes"],
        "inductiveRelation": "stageBudgetsFillTheTick = 360",
        "deductiveStrategy": "statutory-factor-deduction",
    },
]

# 6 canonical non-empty intake feature vectors (one per legal domain) verified in the Lean 4 kernel
INTAKE_FIXTURES = [
    {
        "name": "familyCustodyIntake",
        "domainId": "DOM-FAM-103",
        "features": [220, 10, 35, 10, 5, 10, 180, 140],
        "expectedClass": 0,
    },
    {
        "name": "housingHabitabilityIntake",
        "domainId": "DOM-HOU-URLTA",
        "features": [10, 230, 5, 10, 25, 10, 175, 120],
        "expectedClass": 1,
    },
    {
        "name": "veteransDisabilityIntake",
        "domainId": "DOM-VET-38CFR",
        "features": [20, 5, 240, 25, 5, 5, 190, 90],
        "expectedClass": 2,
    },
    {
        "name": "employmentAdaIntake",
        "domainId": "DOM-EMP-ADA",
        "features": [10, 10, 25, 235, 15, 20, 170, 150],
        "expectedClass": 3,
    },
    {
        "name": "commercialUccIntake",
        "domainId": "DOM-COM-UCC",
        "features": [5, 20, 5, 15, 235, 30, 185, 130],
        "expectedClass": 4,
    },
    {
        "name": "businessFiduciaryIntake",
        "domainId": "DOM-BIZ-DGCL",
        "features": [10, 5, 5, 20, 30, 240, 195, 160],
        "expectedClass": 5,
    },
]


class Mirror:
    """Exact integer reference oracle for `src/Intake.lex.tex` (mirrors the
    LexLean definitions and the client-side browser attention engine)."""

    @staticmethod
    def vector_energy(xs):
        return sum(int(x) for x in xs)

    @staticmethod
    def dot(xs, ws):
        return sum(int(x) * int(w) for x, w in zip(xs, ws))

    @staticmethod
    def attend(query, features):
        return [int(q) * int(x) for q, x in zip(query, features)]

    @staticmethod
    def requant(m, shift, bias, x):
        s_div = max(int(shift), 1)
        q = ((int(x) + int(bias)) * int(m)) // s_div
        if q > MAX_CHANNEL:
            return MAX_CHANNEL
        if q < 0:
            return 0
        return q

    @staticmethod
    def score_keys(attended, keys, biases, m, shift):
        return [
            Mirror.requant(m, shift, b_val, Mirror.dot(attended, k_vec))
            for k_vec, b_val in zip(keys, biases)
        ]

    @staticmethod
    def argmax(scores):
        best_val = 0
        best_idx = 0
        for idx, val in enumerate(scores):
            if idx == 0 or val > best_val:
                best_val = val
                best_idx = idx
        return best_idx

    @staticmethod
    def eval_head(head, features):
        attended = Mirror.attend(head["query"], features)
        scores = Mirror.score_keys(attended, head["keys"], head["biases"], head["multiplier"], head["shift"])
        return Mirror.argmax(scores)

    @staticmethod
    def classify_all_heads(features):
        return [Mirror.eval_head(h, features) for h in NODE_ATTENTION_HEADS]


LN = list_t(NAT)
LLN = list_t(LN)
LS = list_t(STR)
CV = {"kind": "contract_violation"}
SCHEMA_CLS_T = named("SchemaClassifier")
HEAD_T = named("AttentionHead")


def _result(ok):
    return {"kind": "result", "ok": ok, "error": CV}


def _p(op, args, result):
    return {"kind": "primitive", "operation": op, "result": result, "arguments": list(args)}


def _mul(a, c):
    return _p("multiply", [a, c], NAT)


def _quo(a, c):
    return _p("quotient", [a, c, n(0)], NAT)


def _len(x):
    return _p("length", [x], NAT)


def _add(a, c):
    return {"kind": "add", "left": a, "right": c}


def _and(a, c):
    return {"kind": "and", "left": a, "right": c}


def _not(a):
    return {"kind": "not", "value": a}


def _cons(h, t):
    return {"kind": "cons", "head": h, "tail": t}


def _nil(t):
    return {"kind": "nil", "element": t}


def _let(name, typ, value, body):
    return {"kind": "let", "binder": {"name": name, "type": typ}, "value": value, "body": body}


def _eq(a, c):
    return {"kind": "eq", "left": a, "right": c}


def _lt(a, c):
    return {"kind": "lt", "left": a, "right": c}


def _implies(p, c):
    return {"kind": "implies", "premise": p, "conclusion": c}


def _nats(vals):
    return lst([n(v) for v in vals], NAT)


def _nat_matrix(rows):
    return lst([_nats(r) for r in rows], LN)


def _ex(name, result, body, parameters=(), recursive=None):
    return definition(
        name,
        result,
        body,
        parameters=parameters,
        recursive=recursive,
        production=PRODUCTION_ROOTS.get(name),
        executable=True,
    )


def _prop(name, body, parameters):
    return definition(name, {"kind": "prop"}, body, parameters=parameters)


def _defs(*names):
    return [{"name": x} for x in sorted(names)]


def _linear(*names):
    return {"kind": "linear_arithmetic", "definitions": _defs(*names)}


def _sound(name, check, pred, params):
    args = [var(p) for p, _ in params]
    return {
        "kind": "theorem",
        "name": name,
        "parameters": [{"name": p, "type": t} for p, t in params],
        "axioms": ["propext"],
        "statement": _implies(_eq(call(check, *args), b(True)), call(pred, *args)),
        "proof": _linear(check, pred),
    }


def declarations():
    xs, ws = var("xs"), var("ws")
    x, x_tail = var("x"), var("xTail")
    w, w_tail = var("w"), var("wTail")
    m, shift, bias = var("m"), var("shift"), var("bias")
    keys, biases = var("keys"), var("biases")
    k_vec, k_tail = var("kVec"), var("kTail")
    b_val, b_tail = var("bVal"), var("bTail")
    scores = var("scores")
    best_val, best_idx, idx = var("bestVal"), var("bestIdx"), var("idx")
    query, features = var("query"), var("features")
    heads, h_head, h_tail = var("heads"), var("hHead"), var("hTail")
    cls_idx = var("clsIdx")

    cls_rec = lambda c: record(
        "SchemaClassifier",
        id=s(c["id"]),
        schemaElement=s(c["schemaElement"]),
        title=s(c["title"]),
        headId=s(c["headId"]),
        classes=strings(c["classes"]),
        extrapolationTarget=s(c["extrapolationTarget"]),
    )

    head_rec = lambda h: record(
        "AttentionHead",
        id=s(h["id"]),
        nodeId=s(h["nodeId"]),
        schemaId=s(h["schemaId"]),
        title=s(h["title"]),
        query=_nats(h["query"]),
        keys=_nat_matrix(h["keys"]),
        biases=_nats(h["biases"]),
        multiplier=n(h["multiplier"]),
        shift=n(h["shift"]),
        classLabels=strings(h["classLabels"]),
        inductiveRelation=s(h["inductiveRelation"]),
        deductiveStrategy=s(h["deductiveStrategy"]),
    )

    decls = [
        structure(
            "SchemaClassifier",
            [
                ("id", STR),
                ("schemaElement", STR),
                ("title", STR),
                ("headId", STR),
                ("classes", LS),
                ("extrapolationTarget", STR),
            ],
        ),
        structure(
            "AttentionHead",
            [
                ("id", STR),
                ("nodeId", STR),
                ("schemaId", STR),
                ("title", STR),
                ("query", LN),
                ("keys", LLN),
                ("biases", LN),
                ("multiplier", NAT),
                ("shift", NAT),
                ("classLabels", LS),
                ("inductiveRelation", STR),
                ("deductiveStrategy", STR),
            ],
        ),
        _ex(
            "schemaClassifiers",
            list_t(SCHEMA_CLS_T),
            lst([cls_rec(c) for c in SCHEMA_CLASSIFIERS], SCHEMA_CLS_T),
        ),
        _ex(
            "attentionHeads",
            list_t(HEAD_T),
            lst([head_rec(h) for h in NODE_ATTENTION_HEADS], HEAD_T),
        ),
        _ex(
            "domainKeys",
            LLN,
            _nat_matrix(_DOMAIN_KEYS),
        ),
        _ex(
            "primaryQuery",
            LN,
            _nats(NODE_ATTENTION_HEADS[0]["query"]),
        ),
        _ex(
            "primaryBiases",
            LN,
            _nats(NODE_ATTENTION_HEADS[0]["biases"]),
        ),
        # Quantized Neural & Multi-Head Attention Primitives (MNIST + rule30 pattern)
        _ex(
            "vectorEnergy",
            NAT,
            match_list(
                xs,
                n(0),
                "x",
                "xTail",
                _add(x, call("vectorEnergy", x_tail)),
            ),
            parameters=[("xs", LN)],
            recursive="xs",
        ),
        _ex(
            "dot",
            NAT,
            match_list(
                xs,
                n(0),
                "x",
                "xTail",
                match_list(
                    ws,
                    n(0),
                    "w",
                    "wTail",
                    _add(_mul(x, w), call("dot", x_tail, w_tail)),
                ),
            ),
            parameters=[("xs", LN), ("ws", LN)],
            recursive="xs",
        ),
        _ex(
            "attend",
            LN,
            match_list(
                query,
                _nil(NAT),
                "x",
                "xTail",
                match_list(
                    features,
                    _nil(NAT),
                    "w",
                    "wTail",
                    _cons(_mul(x, w), call("attend", x_tail, w_tail)),
                ),
            ),
            parameters=[("query", LN), ("features", LN)],
            recursive="query",
        ),
        _ex(
            "requant",
            NAT,
            _let(
                "q",
                NAT,
                _quo(_mul(_add(x, bias), m), shift),
                if_(blt(n(MAX_CHANNEL), var("q")), n(MAX_CHANNEL), var("q")),
            ),
            parameters=[("m", NAT), ("shift", NAT), ("bias", NAT), ("x", NAT)],
        ),
        _ex(
            "dotKeys",
            LN,
            match_list(
                keys,
                _nil(NAT),
                "kVec",
                "kTail",
                _cons(
                    call("dot", xs, k_vec),
                    call("dotKeys", k_tail, xs),
                ),
            ),
            parameters=[("keys", LLN), ("xs", LN)],
            recursive="keys",
        ),
        _ex(
            "requantScores",
            LN,
            match_list(
                xs,
                _nil(NAT),
                "x",
                "xTail",
                match_list(
                    biases,
                    _nil(NAT),
                    "bVal",
                    "bTail",
                    _cons(
                        call("requant", m, shift, b_val, x),
                        call("requantScores", x_tail, b_tail, m, shift),
                    ),
                ),
            ),
            parameters=[("xs", LN), ("biases", LN), ("m", NAT), ("shift", NAT)],
            recursive="xs",
        ),
        _ex(
            "scoreKeys",
            LN,
            call("requantScores", call("dotKeys", keys, xs), biases, m, shift),
            parameters=[("xs", LN), ("keys", LLN), ("biases", LN), ("m", NAT), ("shift", NAT)],
        ),
        _ex(
            "argmaxLoop",
            NAT,
            match_list(
                scores,
                best_idx,
                "x",
                "xTail",
                if_(
                    blt(best_val, x),
                    call("argmaxLoop", x_tail, x, idx, _add(idx, n(1))),
                    call("argmaxLoop", x_tail, best_val, best_idx, _add(idx, n(1))),
                ),
            ),
            parameters=[("scores", LN), ("bestVal", NAT), ("bestIdx", NAT), ("idx", NAT)],
            recursive="scores",
        ),
        _ex(
            "argmax",
            NAT,
            match_list(
                scores,
                n(0),
                "x",
                "xTail",
                call("argmaxLoop", x_tail, x, n(0), n(1)),
            ),
            parameters=[("scores", LN)],
        ),
        _ex(
            "evalHead",
            NAT,
            _let(
                "attended",
                LN,
                call("attend", query, features),
                _let(
                    "scores",
                    LN,
                    call(
                        "scoreKeys",
                        var("attended"),
                        keys,
                        biases,
                        m,
                        shift,
                    ),
                    call("argmax", var("scores")),
                ),
            ),
            parameters=[
                ("query", LN),
                ("keys", LLN),
                ("biases", LN),
                ("m", NAT),
                ("shift", NAT),
                ("features", LN),
            ],
        ),
        _ex(
            "evalHeadsOn",
            LN,
            match_list(
                heads,
                _nil(NAT),
                "hHead",
                "hTail",
                _cons(
                    call(
                        "evalHead",
                        proj(h_head, "query"),
                        proj(h_head, "keys"),
                        proj(h_head, "biases"),
                        proj(h_head, "multiplier"),
                        proj(h_head, "shift"),
                        features,
                    ),
                    call("evalHeadsOn", h_tail, features),
                ),
            ),
            parameters=[("heads", list_t(HEAD_T)), ("features", LN)],
            recursive="heads",
        ),
        _ex(
            "classifyAllHeads",
            LN,
            call("evalHeadsOn", call("attentionHeads"), features),
            parameters=[("features", LN)],
        ),
        _ex(
            "classifyDomainOn",
            NAT,
            call(
                "evalHead",
                call("primaryQuery"),
                call("domainKeys"),
                call("primaryBiases"),
                n(1),
                n(64),
                features,
            ),
            parameters=[("features", LN)],
        ),
        # Precondition & Postcondition Validators + Soundness Theorems
        # Note: intakeMisfits requires positive signal energy (vectorEnergy > 0), so empty/zero intake is rejected!
        _ex(
            "channelOutOfBounds",
            NAT,
            match_list(
                xs,
                n(0),
                "x",
                "xTail",
                _add(if_(ble(x, n(MAX_CHANNEL)), n(0), n(1)), call("channelOutOfBounds", x_tail)),
            ),
            parameters=[("xs", LN)],
            recursive="xs",
        ),
        _ex(
            "intakeMisfits",
            NAT,
            _add(
                _add(
                    if_(beq(_len(features), n(FEATURE_DIM)), n(0), n(1)),
                    if_(beq(call("vectorEnergy", features), n(0)), n(1), n(0)),
                ),
                call("channelOutOfBounds", features),
            ),
            parameters=[("features", LN)],
        ),
        _prop("IsIntakeVector", _eq(call("intakeMisfits", features), n(0)), [("features", LN)]),
        _ex(
            "isIntakeVectorCheck",
            BOOL,
            beq(call("intakeMisfits", features), n(0)),
            parameters=[("features", LN)],
        ),
        _sound("is_intake_vector_check_sound", "isIntakeVectorCheck", "IsIntakeVector", [("features", LN)]),
        _prop(
            "IsValidClassification",
            _lt(cls_idx, n(NUM_DOMAIN_CLASSES)),
            [("features", LN), ("clsIdx", NAT)],
        ),
        _ex(
            "isValidClassificationCheck",
            BOOL,
            blt(cls_idx, n(NUM_DOMAIN_CLASSES)),
            parameters=[("features", LN), ("clsIdx", NAT)],
        ),
        _sound(
            "is_valid_classification_check_sound",
            "isValidClassificationCheck",
            "IsValidClassification",
            [("features", LN), ("clsIdx", NAT)],
        ),
        {
            "kind": "contract",
            "name": "IntakeClassification",
            "axioms": ["propext"],
            "input": {"name": "features", "type": LN},
            "output": {"name": "clsIdx", "type": NAT},
            "precondition": {"name": "IsIntakeVector"},
            "postcondition": {"name": "IsValidClassification"},
            "validators": [
                {
                    "predicate": "postcondition",
                    "sound": {"name": "is_valid_classification_check_sound"},
                    "validator": {"name": "isValidClassificationCheck"},
                },
                {
                    "predicate": "precondition",
                    "sound": {"name": "is_intake_vector_check_sound"},
                    "validator": {"name": "isIntakeVectorCheck"},
                },
            ],
        },
        {
            "kind": "realization",
            "name": "IntakeAttentionEngine",
            "input": {"name": "features", "type": LN},
            "output": NAT,
            "descriptor": {"kind": "deterministic", "body": call("classifyDomainOn", features)},
            "executable": True,
        },
        {
            "kind": "model",
            "name": "IntakeClassificationModel",
            "contract": {"member": {"name": "IntakeClassification"}},
            "realization": {"member": {"name": "IntakeAttentionEngine"}},
        },
        _ex(
            "classifyIntake",
            _result(NAT),
            {
                "kind": "checked_apply",
                "model": {"name": "IntakeClassificationModel"},
                "type_arguments": [],
                "arguments": [features],
                "checks": ["postcondition", "precondition"],
            },
            parameters=[("features", LN)],
        ),
        # Zero-Default Verification Helpers & Theorems
        _ex("zeroIntakeVector", LN, _nats([0, 0, 0, 0, 0, 0, 0, 0])),
        holds("zeroIntakeRejected", _not(call("isIntakeVectorCheck", call("zeroIntakeVector")))),
        holds(
            "zeroIntakeProducesZeroScores",
            beq(
                call(
                    "vectorEnergy",
                    call(
                        "scoreKeys",
                        call("attend", call("primaryQuery"), call("zeroIntakeVector")),
                        call("domainKeys"),
                        call("primaryBiases"),
                        n(1),
                        n(64),
                    ),
                ),
                n(0),
            ),
        ),
        # Structural well-formedness & coverage helpers
        member_string(),
        all_members(),
        distinct_strings(),
        field_of_each("schemaClassifierIds", SCHEMA_CLS_T, "id"),
        field_of_each("schemaClassifierHeads", SCHEMA_CLS_T, "headId"),
        field_of_each("attentionHeadIds", HEAD_T, "id"),
        field_of_each("attentionHeadNodes", HEAD_T, "nodeId"),
        field_of_each("attentionHeadSchemas", HEAD_T, "schemaId"),
        _ex(
            "allClassesValid",
            BOOL,
            match_list(
                xs,
                b(True),
                "x",
                "xTail",
                _and(blt(x, n(NUM_DOMAIN_CLASSES)), call("allClassesValid", x_tail)),
            ),
            parameters=[("xs", LN)],
            recursive="xs",
        ),
        holds("schemaClassifierIdsDistinct", call("distinctStrings", call("schemaClassifierIds", call("schemaClassifiers")))),
        holds("attentionHeadIdsDistinct", call("distinctStrings", call("attentionHeadIds", call("attentionHeads")))),
        holds("attentionHeadNodesDistinct", call("distinctStrings", call("attentionHeadNodes", call("attentionHeads")))),
        holds(
            "everySchemaElementHasAttentionHead",
            call(
                "allMembers",
                call("schemaClassifierIds", call("schemaClassifiers")),
                call("attentionHeadSchemas", call("attentionHeads")),
            ),
        ),
        holds(
            "everySchemaClassifierHeadResolves",
            call(
                "allMembers",
                call("schemaClassifierHeads", call("schemaClassifiers")),
                call("attentionHeadIds", call("attentionHeads")),
            ),
        ),
        holds(
            "attentionHeadsResolveToSchemas",
            call(
                "allMembers",
                call("attentionHeadSchemas", call("attentionHeads")),
                call("schemaClassifierIds", call("schemaClassifiers")),
            ),
        ),
    ]

    for fx in INTAKE_FIXTURES:
        fname = fx["name"]
        fvec = _nats(fx["features"])
        decls += [
            _ex(f"{fname}Vector", LN, fvec),
            holds(f"{fname}IsValidVector", call("isIntakeVectorCheck", call(f"{fname}Vector"))),
            holds(
                f"{fname}ClassifiesDomain",
                beq(call("classifyDomainOn", call(f"{fname}Vector")), n(fx["expectedClass"])),
            ),
            holds(
                f"{fname}AllHeadsValid",
                call("allClassesValid", call("classifyAllHeads", call(f"{fname}Vector"))),
            ),
        ]

    return decls


def render_ledger_toml():
    lines = [
        "# PrismPM Intake Classifiers & Per-Node Attention Heads (src/Intake.lex.tex)",
        'spec = "prism-legal/intake/1"',
        f"feature_dim = {FEATURE_DIM}",
        f"max_channel = {MAX_CHANNEL}",
        f"num_domain_classes = {NUM_DOMAIN_CLASSES}",
        "",
    ]
    for ch in FEATURE_CHANNELS:
        lines += [
            "[[feature_channel]]",
            f'index = {ch["index"]}',
            f'id = {json.dumps(ch["id"])}',
            f'label = {json.dumps(ch["label"])}',
            f'keywords = {json.dumps(ch["keywords"])}',
            "",
        ]
    for sc in SCHEMA_CLASSIFIERS:
        lines += [
            "[[schema_classifier]]",
            f'id = {json.dumps(sc["id"])}',
            f'schema_element = {json.dumps(sc["schemaElement"])}',
            f'title = {json.dumps(sc["title"])}',
            f'head_id = {json.dumps(sc["headId"])}',
            f'classes = {json.dumps(sc["classes"])}',
            f'extrapolation_target = {json.dumps(sc["extrapolationTarget"])}',
            "",
        ]
    for h in NODE_ATTENTION_HEADS:
        lines += [
            "[[attention_head]]",
            f'id = {json.dumps(h["id"])}',
            f'node_id = {json.dumps(h["nodeId"])}',
            f'schema_id = {json.dumps(h["schemaId"])}',
            f'title = {json.dumps(h["title"])}',
            f'query = {json.dumps(h["query"])}',
            f'biases = {json.dumps(h["biases"])}',
            f'multiplier = {h["multiplier"]}',
            f'shift = {h["shift"]}',
            f'class_labels = {json.dumps(h["classLabels"])}',
            f'inductive_relation = {json.dumps(h["inductiveRelation"])}',
            f'deductive_strategy = {json.dumps(h["deductiveStrategy"])}',
            "",
        ]
    for fx in INTAKE_FIXTURES:
        lines += [
            "[[fixture]]",
            f'name = {json.dumps(fx["name"])}',
            f'domain_id = {json.dumps(fx["domainId"])}',
            f'features = {json.dumps(fx["features"])}',
            f'expected_class = {fx["expectedClass"]}',
            "",
        ]
    return "\n".join(lines)


def render():
    return lexmod.module(NAME, declarations(), title="PrismLegal Intake Classifiers & Multi-Head Attention Extrapolation")


def sync():
    MODULE.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    text = render()
    ltext = render_ledger_toml()
    changed = False
    if not MODULE.exists() or MODULE.read_text() != text:
        MODULE.write_text(text)
        changed = True
    if not LEDGER.exists() or LEDGER.read_text() != ltext:
        LEDGER.write_text(ltext)
        changed = True
    return {
        "module": "src/Intake.lex.tex",
        "ledger": "model/intake.toml",
        "schemaClassifiers": len(SCHEMA_CLASSIFIERS),
        "attentionHeads": len(NODE_ATTENTION_HEADS),
        "fixtures": len(INTAKE_FIXTURES),
        "changed": changed,
    }


def check():
    if not MODULE.exists() or MODULE.read_text() != render():
        return {"ok": False, "reason": "src/Intake.lex.tex drifted; run `bin/prism-legal api sync`"}
    if not LEDGER.exists() or LEDGER.read_text() != render_ledger_toml():
        return {"ok": False, "reason": "model/intake.toml drifted; run `bin/prism-legal api sync`"}
    for fx in INTAKE_FIXTURES:
        got = Mirror.eval_head(NODE_ATTENTION_HEADS[0], fx["features"])
        if got != fx["expectedClass"]:
            return {"ok": False, "reason": f"Intake fixture {fx['name']} classified as {got}, expected {fx['expectedClass']}"}
    return {"ok": True, "reason": None}
