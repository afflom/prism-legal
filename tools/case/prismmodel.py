"""PrismPM model registers (`model/*.toml`), JSON schemas (`schemas/*.schema.json`),
Gherkin conformance suites (`features/suites/*.feature`), and `CONFORMANCE.md`
for PrismLegal."""

import json
from . import (
    ROOT,
    apimodel,
    archmodel,
    auditmodel,
    casemodel,
    directexammodel,
    intakemodel,
    presentationmodel,
    standardsmodel,
    visualmodel,
)

MODEL_DIR = ROOT / "model"
SCHEMA_DIR = ROOT / "schemas"
SUITE_DIR = ROOT / "features" / "suites"
CONFORMANCE_MD = ROOT / "CONFORMANCE.md"


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    changed = not path.exists() or path.read_text() != content
    if changed:
        path.write_text(content)
    return changed


def render_authorities():
    lines = ['spec = "prismpm/authorities/1"', ""]
    for st in standardsmodel.rows():
        lines += [
            "[[authority]]",
            f'id = {json.dumps(st["id"])}',
            f'name = {json.dumps(st["name"])}',
            f'url = {json.dumps(st["authority"])}',
            f'version = {json.dumps(st["version"])}',
            "",
        ]
    return "\n".join(lines)


def render_ids():
    lines = ['spec = "prismpm/ids/1"', ""]
    for c in casemodel.CLAIMS:
        lines += [
            "[[conformance_id]]",
            f'id = {json.dumps(c["id"])}',
            f'category = {json.dumps(c["category"])}',
            f'status = {json.dumps(c["status"])}',
            f'statement = {json.dumps(c["statement"])}',
            "",
        ]
    return "\n".join(lines)


def render_ledger():
    lines = ['spec = "prismpm/ledger/1"', ""]
    for c in casemodel.CLAIMS:
        lines += [
            "[[entry]]",
            f'id = {json.dumps(c["id"])}',
            f'status = {json.dumps(c["status"])}',
            f'statutory = {json.dumps(c["statutory"])}',
            f'exhibits = {json.dumps(c["exhibits"])}',
            f'depends = {json.dumps(c["depends"])}',
            "",
        ]
    return "\n".join(lines)


def render_commands():
    lines = ['spec = "prismpm/commands/1"', ""]
    for cmd in apimodel.surface():
        lines += [
            "[[command]]",
            f'name = {json.dumps(cmd["name"])}',
            f'path = {json.dumps(cmd["path"])}',
            f'help = {json.dumps(cmd["help"])}',
            "",
        ]
    return "\n".join(lines)


def render_contracts():
    lines = [
        'spec = "prismpm/contracts/1"',
        "",
        "[[contract]]",
        'id = "register-json"',
        'media_type = "application/vnd.prism.legal.register.v1+json"',
        'schema = "schemas/register.schema.json"',
        'identity = "sha256-canonical-json"',
        "",
        "[[contract]]",
        'id = "standards-json"',
        'media_type = "application/vnd.prism.legal.standards.v1+json"',
        'schema = "schemas/standards.schema.json"',
        'identity = "sha256-canonical-json"',
        "",
        "[[contract]]",
        'id = "audit-json"',
        'media_type = "application/vnd.prism.legal.audit.v1+json"',
        'schema = "schemas/audit.schema.json"',
        'identity = "sha256-canonical-json"',
        "",
        "[[contract]]",
        'id = "intake-json"',
        'media_type = "application/vnd.prism.legal.intake.v1+json"',
        'schema = "schemas/intake.schema.json"',
        'identity = "sha256-canonical-json"',
        "",
    ]
    return "\n".join(lines)


def render_dependencies():
    return "\n".join(
        [
            'spec = "prismpm/dependencies/1"',
            'lean_toolchain = "leanprover/lean4:v4.32.1"',
            'lexlean_version = "0.4.0"',
            'prismpm_version = "0.4.0"',
            'packages = ["prism.legal@1.0.0", "lexlean.std.bool@1.2.0", "lexlean.std.int@1.2.0", "lexlean.std.nat@1.2.0", "prism.arch@1.0.0", "prism.qual@1.0.0", "prism.sec@1.0.0"]',
            "",
        ]
    )


def render_errors():
    errors = [
        ("LEGAL1001", "Unknown claim, exhibit, witness, or trap ID requested."),
        ("LEGAL2001", "Model drift detected between domain specification and generated LexLean/PrismPM artifacts."),
        ("LEGAL3001", "LexLean / Lean 4 kernel verification failed on one or more semantic modules."),
        ("LEGAL4001", "Zero-PII sanitization check failed; private case token or forbidden media detected."),
    ]
    lines = ['spec = "prismpm/errors/1"', ""]
    for code, msg in errors:
        lines += ["[[error]]", f'code = {json.dumps(code)}', f'message = {json.dumps(msg)}', ""]
    return "\n".join(lines)


def render_projection():
    lines = ['spec = "prismpm/projection/1"', ""]
    for v in archmodel.VIEWS:
        lines += [
            "[[projection]]",
            f'id = {json.dumps(v["id"])}',
            f'viewpoint_id = {json.dumps(v["viewpointId"])}',
            f'route = {json.dumps(v["route"])}',
            f'title = {json.dumps(v["title"])}',
            "",
        ]
    return "\n".join(lines)


def render_ux_journeys():
    lines = [
        'spec = "prismpm/ux-journeys/1"',
        f'brand_id = {json.dumps(presentationmodel.BRAND["id"])}',
        f'brand_title = {json.dumps(presentationmodel.BRAND["title"])}',
        f'poles = {json.dumps(presentationmodel.POLES)}',
        f'forbidden_meta_terms = {json.dumps(presentationmodel.FORBIDDEN_META_TERMS)}',
        "",
    ]
    for pg in presentationmodel.PORTAL_PAGES:
        lines += [
            "[[portal_page]]",
            f'id = {json.dumps(pg["id"])}',
            f'path = {json.dumps(pg["path"])}',
            f'persona_scope = {json.dumps(pg["personaScope"])}',
            f'title = {json.dumps(pg["title"])}',
            f'section_count = {pg["sectionCount"]}',
            f'max_sections_budget = {pg["maxSectionsBudget"]}',
            "",
        ]
    for j in presentationmodel.JOURNEYS:
        lines += [
            "[[journey]]",
            f'id = {json.dumps(j["id"])}',
            f'stakeholder_id = {json.dumps(j["stakeholderId"])}',
            f'summary = {json.dumps(j["summary"])}',
            "",
        ]
        for st in j["steps"]:
            lines += [
                "[[journey.step]]",
                f'id = {json.dumps(st["id"])}',
                f'pole = {json.dumps(st["pole"])}',
                f'panel_id = {json.dumps(st["panelId"])}',
                f'action = {json.dumps(st["action"])}',
                f'artifact_id = {json.dumps(st["artifactId"])}',
                "",
            ]
    for pg in presentationmodel.PEDAGOGY_GUIDES:
        lines += [
            "[[pedagogy_guide]]",
            f'id = {json.dumps(pg["id"])}',
            f'step_id = {json.dumps(pg["stepId"])}',
            f'pole = {json.dumps(pg["pole"])}',
            f'panel_id = {json.dumps(pg["panelId"])}',
            f'standard_id = {json.dumps(pg["standardId"])}',
            f'heading = {json.dumps(pg["heading"])}',
            f'why_it_matters = {json.dumps(pg["whyItMatters"])}',
            f'coaching_tip = {json.dumps(pg["coachingTip"])}',
            f'rule_context = {json.dumps(pg["ruleContext"])}',
            "",
        ]
    return "\n".join(lines)


def render_runtime_roots():
    lines = ['spec = "prismpm/runtime-roots/1"', ""]
    for name, cfg in apimodel.PRODUCTION_ROOTS.items():
        lines += [
            "[[root]]",
            'module = "PrismLegal.Api"',
            f'name = {json.dumps(name)}',
            f'effects = {json.dumps(cfg["effects"])}',
            f'targets = {json.dumps(cfg["targets"])}',
            "",
        ]
    for name in (
        "petitionerStipulatedMonthlyCents",
        "respondentStipulatedDisabilityCents",
        "stipulatedBaselineCents",
        "sharedParentingAdjustedCents",
        "guidelineNetTransferCents",
        "undisclosedReserveBalanceCents",
    ):
        lines += [
            "[[root]]",
            'module = "PrismLegal.RemediesCore"',
            f'name = {json.dumps(name)}',
            'effects = ["overflow"]',
            'targets = ["rust-core", "rust-std"]',
            "",
        ]
    lines += [
        "[[root]]",
        'module = "PrismLegal.RemediesCore"',
        'name = "worksheets"',
        'effects = ["allocation"]',
        'targets = ["rust-std"]',
        "",
    ]
    for name in ("buildColumns", "findRelations", "findRecurrence"):
        lines += [
            "[[root]]",
            'module = "PrismLegal.Discovery"',
            f'name = {json.dumps(name)}',
            'effects = ["allocation", "overflow"]',
            'targets = ["rust-std"]',
            "",
        ]
    for name in ("learnAll", "schedule"):
        lines += [
            "[[root]]",
            'module = "PrismLegal.Engine"',
            f'name = {json.dumps(name)}',
            'effects = ["allocation", "overflow", "recursion"]',
            'targets = ["rust-std"]',
            "",
        ]
    for name in ("classifyIntake", "classifyAllHeads"):
        lines += [
            "[[root]]",
            'module = "PrismLegal.Intake"',
            f'name = {json.dumps(name)}',
            'effects = ["allocation", "overflow", "recursion"]',
            'targets = ["rust-std"]',
            "",
        ]
    return "\n".join(lines)


def render_stdlib_package():
    return "\n".join(
        [
            'spec = "prismpm/stdlib-package/1"',
            'name = "prism-stdlib"',
            'version = "0.2.0"',
            'license = "MIT OR Apache-2.0"',
            'modules = ["Foundation.Arch", "Foundation.Bytes", "Foundation.Codec", "Foundation.Core", "Foundation.Outcome", "Foundation.Qual", "Foundation.Sec", "Foundation.Text", "Foundation.Utf8"]',
            "",
        ]
    )


def render_schemas():
    return {
        "register.schema.json": json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "PrismLegal Verified Model Register",
                "type": "object",
                "required": ["caseMeta", "children", "openingPillars", "statutoryFactors", "financialLedger", "claims", "respondentExhibits", "petitionerExhibits", "witnesses", "traps", "timeline", "portal"],
            },
            indent=2,
        )
        + "\n",
        "standards.schema.json": json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "PrismLegal Legal & Technical Standards Register",
                "type": "object",
                "required": ["standards"],
            },
            indent=2,
        )
        + "\n",
        "audit.schema.json": json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "PrismLegal Cross-Examination Trap Audit",
                "type": "object",
                "required": ["statuses", "traps"],
            },
            indent=2,
        )
        + "\n",
        "intake.schema.json": json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": "PrismLegal Intake Classifiers & Per-Node Attention Heads",
                "type": "object",
                "required": ["featureDim", "maxChannel", "numDomainClasses", "featureChannels", "schemaClassifiers", "attentionHeads", "fixtures"],
            },
            indent=2,
        )
        + "\n",
    }


def render_features():
    claim_lines = [
        "Feature: PrismLegal Evidentiary Register Conformance",
        "  Every stipulated, corroborated, and contested claim in the reference matter is backed by exhibits and statutory authority.",
        "",
    ]
    for c in casemodel.CLAIMS:
        claim_lines += [
            f"  @{c['id']} @{c['status']}",
            f"  Scenario: {c['id']} ({c['category']})",
            f"    Given the verified case register in \"src/Register.lex.tex\"",
            f"    When claim \"{c['id']}\" is inspected under \"{c['statutory']}\"",
            f"    Then its status is \"{c['status']}\" and its exhibits {', '.join(c['exhibits'])} resolve in the register",
            "",
        ]

    trap_lines = [
        "Feature: PrismLegal Cross-Examination Pivot Conformance",
        "  Every opposing allegation has a verified rebuttal exhibit and a calm Opening-Statement-aligned pivot.",
        "",
    ]
    for t in auditmodel.TRAPS:
        trap_lines += [
            f"  @{t['id']} @{t['status']}",
            f"  Scenario: {t['id']} — {t['title']}",
            f"    Given opposing allegation \"{t['id']}\" in \"src/Audit.lex.tex\"",
            f"    When cross-examination raises \"{t['category']}\"",
            f"    Then Respondent pivots with \"{t['statutoryAnchor']}\" and rebuttal exhibits {', '.join(t['rebuttalExhibits'])}",
            "",
        ]

    dx_lines = [
        "Feature: PrismLegal Lead Counsel Intended Direct Examination Conformance",
        "  Every question in Lead Counsel's Direct Examination script resolves to a chapter, Opening Statement pillar, statutory factor, and exhibit with a full Opening-aligned witness answer.",
        "",
    ]
    for ch in directexammodel.DIRECT_EXAM_CHAPTERS:
        dx_lines += [
            f"  @{ch['id']} @{ch['pillarId']}",
            f"  Scenario: {ch['id']} — {ch['title']} ({ch['pageRange']})",
            f"    Given Lead Counsel's Direct Examination script in \"src/DirectExam.lex.tex\"",
            f"    When chapter \"{ch['id']}\" is conducted under \"{ch['statutoryId']}\"",
            f"    Then it advances Opening Statement pillar \"{ch['pillarId']}\" and admits {', '.join(ch['exhibitsAdmitted']) or 'foundational testimony'}",
            "",
        ]

    vis_lines = [
        "Feature: PrismLegal Handwritten, Visual & 30-Exhibit Content-Meaning / Intent Conformance",
        "  Every handwritten journal entry, visual/scanned exhibit forensic extraction, photo page, and all 30 trial exhibits carry verified content meaning and proponent intent.",
        "",
    ]
    for v in visualmodel.VISUAL_FORENSIC_RECORDS:
        vis_lines += [
            f"  @{v['id']} @{v['exhibitId']}",
            f"  Scenario: {v['id']} ({v['exhibitId']} · {v['modality']} · {v['pageCount']} pp.)",
            f"    Given visual forensic record \"{v['id']}\" in \"src/VisualEvidence.lex.tex\"",
            f"    When exhibit \"{v['exhibitId']}\" is examined under \"{v['statutoryAnchor']}\"",
            f"    Then its handwritten/visual details and trial pivot are verified in the register",
            "",
        ]

    ux_lines = [
        "Feature: PrismLegal User-Centered Service Design & Five-Pole Journey Conformance",
        "  Every portal page enforces progressive disclosure within its cognitive-load budget, separates Client and Attorney workspaces, and walks the five poles (orientation, substance, challenge, proof, resolution) without meta-taxonomy or technical jargon leakage.",
        "",
    ]
    for j in presentationmodel.JOURNEYS:
        ux_lines += [
            f"  @{j['id']} @{j['stakeholderId']}",
            f"  Scenario: {j['id']} ({j['stakeholderId']})",
            f"    Given the user-centered journey \"{j['id']}\" in \"src/Presentation.lex.tex\"",
            f"    When stakeholder \"{j['stakeholderId']}\" progresses across poles {', '.join(presentationmodel.POLES)}",
            f"    Then all 5 steps ({', '.join(st['id'] for st in j['steps'])}) resolve to verified workspace panels and artifacts",
            "",
        ]
    for pg in presentationmodel.PEDAGOGY_GUIDES:
        ux_lines += [
            f"  @{pg['id']} @{pg['stepId']}",
            f"  Scenario: {pg['id']} — {pg['heading']}",
            f"    Given the contextual pedagogy guide \"{pg['id']}\" for step \"{pg['stepId']}\" in \"src/Presentation.lex.tex\"",
            f"    When a user views pole \"{pg['pole']}\" in panel \"{pg['panelId']}\"",
            f"    Then contextual legal guidance grounded in standard \"{pg['standardId']}\" is presented without walls of text",
            "",
        ]

    intake_lines = [
        "Feature: PrismLegal In-Browser Intake Classifiers & Per-Node Attention Extrapolation Conformance",
        "  Every schema element in the model has a verified classifier and every node is an attention head whose inductive and deductive outputs extrapolate the completion of a legal matter in the browser without leaking internal meta-jargon.",
        "",
    ]
    for sc in intakemodel.SCHEMA_CLASSIFIERS:
        intake_lines += [
            f"  @{sc['id']} @{sc['headId']}",
            f"  Scenario: {sc['id']} — {sc['title']}",
            f"    Given the schema classifier \"{sc['id']}\" for schema element \"{sc['schemaElement']}\" in \"src/Intake.lex.tex\"",
            f"    When node attention head \"{sc['headId']}\" scores an 8-channel intake feature vector",
            f"    Then it classifies into {', '.join(sc['classes'][:3])} and extrapolates the matter completion",
            "",
        ]

    return {
        "register.feature": "\n".join(claim_lines),
        "audit.feature": "\n".join(trap_lines),
        "direct-exam.feature": "\n".join(dx_lines),
        "visual-evidence.feature": "\n".join(vis_lines),
        "ux-journeys.feature": "\n".join(ux_lines),
        "intake.feature": "\n".join(intake_lines),
    }


def render_conformance_md():
    lines = [
        "# PrismLegal — Public-Benefit Legal Platform & Conformance Ledger",
        "",
        f"- **Reference Matter:** `{casemodel.CASE_META['caseNumber']}` — *{casemodel.CASE_META['caption']}*",
        f"- **Court:** {casemodel.CASE_META['court']} (`{casemodel.CASE_META['division']}`)",
        f"- **Hearing:** {casemodel.CASE_META['hearingTitle']} — **{casemodel.CASE_META['hearingDate']} at {casemodel.CASE_META['hearingTime']}**",
        f"- **Petitioner:** {casemodel.CASE_META['petitioner']['name']} (Counsel: {casemodel.CASE_META['petitioner']['counsel']})",
        f"- **Respondent:** {casemodel.CASE_META['respondent']['name']} (Counsel: {casemodel.CASE_META['respondent']['counsel']})",
        "",
        "## 1. Verified Platform & Case Modules (`src/*.lex.tex`)",
        "",
        "| Module | Governing Scope | Decided Theorems |",
        "| :--- | :--- | :--- |",
        "| `src/Portal.lex.tex` | Public-Benefit Charter, 4 Auth Providers (`AUTH-PASSKEY`, `AUTH-BAR-OIDC`, `AUTH-LEGAL-AID`, `AUTH-LOCAL-VAULT`), 5 Cryptographic Share Grants (`SHARE-01–05`), 4 Law Firms & Legal Aid Clinics, 4 Courts & Tribunals, 6 Multi-Domain Legal Frameworks, 3 Clients, 4 Lawyers, 6 Multi-Domain Cases, 8 `M:N` Engagements, 8 Disjoint Views | `authProviderIdsDistinct`, `shareGrantIdsDistinct`, `firmIdsDistinct`, `courtIdsDistinct`, `frameworkIdsDistinct`, `clientIdsDistinct`, `lawyerIdsDistinct`, `caseIdsDistinct`, `engagementIdsDistinct`, `portalViewIdsDistinct`, `lawyersResolveToFirms`, `casesResolveToCourts`, `casesResolveToFrameworks`, `engagementsValidAndPortable`, `shareGrantsValidAndRevocable`, `clientAndLawyerPortalViewsDisjoint` |",
        "| `src/Register.lex.tex` | Case Metadata, 3 Minor Beneficiaries (Ages 15, 11 & 6), 24 Claims, 30 Exhibit Slots (`Ex-A–Ex-O`, `OP-Ex-01–OP-Ex-15`), 10 Witnesses (`W-01–W-10`), 6 Opening Pillars, 11 Statutory Factors (`SF-01–SF-11`), 16 Timeline Milestones | `beneficiaryIdsDistinct`, `pillarIdsDistinct`, `factorIdsDistinct`, `claimIdsDistinct`, `exhibitIdsDistinct`, `witnessIdsDistinct`, `timelineIdsDistinct`, `claimsResolvedAndBacked`, `beneficiaryCountIs3`, `claimCountIs24`, `exhibitCountIs30`, `witnessCountIs10` |",
        "| `src/RemediesCore.lex.tex` | Executable Guideline Support & Remedies Worksheets (`Ex. N` vs. `OP Ex. 2`), `38 U.S.C. § 1781` Medical Coverage, `FRCP 26(e) / Rule 16.2` `$30,000.00` Escrow Disclosure Audit, 2026–2029 Tax History | `worksheetIdsDistinct`, `stipulatedBaselineCentsVerified`, `guidelineTransferCentsVerified`, `undisclosedReserveCentsVerified` |",
        "| `src/Architecture.lex.tex` | 5 Stakeholders, 9 Concerns, 6 Viewpoints, 4 Views (`Foundation.Arch`), 5 Quality Measures (`Foundation.Qual`), 4 Trial Risks, 7 Tuning Parameters | `stakeholderIdsDistinct`, `concernIdsDistinct`, `viewpointIdsDistinct`, `viewIdsDistinct`, `viewsResolveToViewpoints` |",
        "| `src/Audit.lex.tex` | 16 Opposing Allegations & Cross-Examination Traps (`TRAP-01` to `TRAP-16`) | `trapIdsDistinct`, `trapsValidAndBacked`, `trapCountIs16` |",
        "| `src/LegalMeta.lex.tex` | Hohfeldian Fundamental Legal Conceptions (`HOH-01–08`), OASIS LegalRuleML v1.0 Defeasible Rules & Overrides (`LRML-01–08`, `SUP-01–04`), Dung/ASPIC+ Argumentation Attack Graph (`ATK-01–16`), OASIS Akoma Ntoso FRBR URIs (`AKN-01–08`), ISO 15489/27037 Chain of Custody (`COC-01–08`) | `hohfeldIdsDistinct`, `legalRuleIdsDistinct`, `superiorityIdsDistinct`, `attackIdsDistinct`, `aknIdsDistinct`, `cocIdsDistinct`, `superiorityOverridesValid` |",
        "| `src/Observer.lex.tex` | 5 Stakeholder Vantages (`OBS-CLIENT`, `OBS-COUNSEL`, `OBS-BENCH`, `OBS-BENEFICIARIES`, `OBS-CLINIC`) | `observerQuadrupleIdsDistinct` |",
        "| `src/Presentation.lex.tex` | Brand, 20 Mechanized Artifacts, 4 Separate Portal HTML Pages (`index.html`, `client.html`, `lawyer.html`, `courtroom.html`), 7 Panels, 5 Five-Pole Journeys, 13 Contextual Pedagogy Guides (`ped-client-1`..`ped-court-3`), WAI-ARIA Navigation, 9 Visualizations, WCAG 2.2 AA Contrast System, Zero Meta-Taxonomy Leakage | `artifactIdsDistinct`, `artifactPathsDistinct`, `portalPageIdsDistinct`, `portalPagePathsDistinct`, `portalPageArtifactsValid`, `everyPageWithinCognitiveLoadBudget`, `domainLabelsFreeOfMetaTaxonomy`, `pedagogyIdsDistinct`, `pedagogyPolesValid`, `pedagogyPanelsValid`, `pedagogyFreeOfMetaTaxonomy`, `panelsGovernedByViewpoints`, `journeysValid`, `navIdsDistinct`, `everyPanelInPrimaryNavigation`, `vizPanelsRender`, `tokenLuminancesComputed`, `everyPairMeetsContrastLight`, `everyPairMeetsContrastDark` |",
        "| `src/Convert.lex.tex` | First-Order Controlled-English Legal Proposition Converter + `prism.legal@1.0.0` Lexicon (`PROP-01–12`, `REF-13–16`, Zero External LLM) | `fixtureCountIs`, `converts1`..`converts16` |",
        "| `src/Engine.lex.tex` | Neuromorphic Courtroom Strategy Learning & Homeostatic Trial Clock (`learn`, `learnAll`, `schedule`, 4 SHA-256 Strategy Templates, 7 Statutory Families, 28 Synaptic Weights in `[1, 16]`, 360-Min Trial Clock) | `portfolioIdsDistinct`, `stageBudgetsFillTheTick`, `stageBudgetsFitTheTimeout`, `gateKeepsItsShare`, `learnStaysInBounds`, `initialWeightsBounded`, `committedWeightsBounded`, `learnAllFixture`, `everyScheduleIsSound` |",
        "| `src/Sequences.lex.tex` | 13 Evidentiary Indicator Bit-Vector Sequences over a 64-Checkpoint Trial Window (`model/sequences.toml`) | `sequenceCountIs`, `sequenceIdsDistinct`, `sequenceKappasDistinct`, `everyWindowValid` |",
        "| `src/Discovery.lex.tex` | Certified `F_2` Gaussian-Elimination Relation Search & Berlekamp-Massey Recurrence Search with `checked_apply` Runtime Guards | `is_window_check_sound`, `all_relations_hold_check_sound`, `zero_word_iff`, `is_sequence_window_check_sound`, `satisfies_recurrence_check_sound`, `relationFixtureFindsTheRegister`, `registerRelationsHold` |",
        "| `src/Intake.lex.tex` | Certified In-Browser Bespoke Intake Classifiers & Multi-Head Attention Network (12 Schema Classifiers, 18 Zero-Prior-Bias Per-Node Attention Heads, Exact Integer `dot`/`requant`/`argmax`, `IntakeClassification` Contract & `classifyIntake` `checked_apply` Production Root) | `is_intake_vector_check_sound`, `is_valid_classification_check_sound`, `schemaClassifierIdsDistinct`, `attentionHeadIdsDistinct`, `attentionHeadNodesDistinct`, `everySchemaElementHasAttentionHead`, `everySchemaClassifierHeadResolves`, `attentionHeadsResolveToSchemas`, `zeroIntakeRejected`, `zeroIntakeProducesZeroScores`, `familyCustodyIntakeClassifiesDomain`, `housingHabitabilityIntakeClassifiesDomain`, `veteransDisabilityIntakeClassifiesDomain`, `employmentAdaIntakeClassifiesDomain`, `commercialUccIntakeClassifiesDomain`, `businessFiduciaryIntakeClassifiesDomain` |",
        "| `src/VisualEvidence.lex.tex` | 8 Handwritten Journal Forensics (`OP Ex. 13` `DIARY-01`..`08` under `FRE 106`), 12 Visual/Scanned Exhibit Forensics (`VIS-01`..`12`), 12 Photo Page Catalog Records (`PHOTO-01`..`12`), and 30-Exhibit Content-Meaning & Intent Matrix (`MAP-Ex-A`..`MAP-OP-Ex-15`) | `diaryEntryIdsDistinct`, `diaryEntriesResolveToExhibit13`, `everyDiaryEntryAffirmsParentingDevotion`, `visualForensicIdsDistinct`, `visualForensicExhibitsResolve`, `photoCatalogIdsDistinct`, `photoCatalogExhibitsResolve`, `semanticMappingIdsDistinct`, `everyRegisterExhibitMapped`, `diaryEntryCountIs8`, `visualForensicCountIs12`, `photoCatalogCountIs12`, `semanticMappingCountIs30` |",
        "| `src/DirectExam.lex.tex` | Lead Trial Counsel's Intended Direct Examination of Respondent (6 Chapters `CH-01`..`06`, 36 Q&As `DX-001`..`036`, 14 Yellow-Highlighted Priority Blocks, 14 Exhibit Admission Moves, 3 Red Stricken Blocks) | `directExamChapterIdsDistinct`, `directExamQuestionIdsDistinct`, `directExamQuestionsResolveToChapters`, `directExamQuestionExhibitsResolve`, `everyDirectExamQuestionHasFullTestimony`, `directExamChapterCount`, `directExamQuestionCount`, `directExamYellowHighlightCount`, `directExamRedStrikethroughCount`, `directExamAdmissionMoveCount` |",
        "| `src/Application.lex.tex` | Public-Benefit Open-Source Platform Application (`publicBenefitOpenSource = true`, `zeroPiiSanitized = true`, `githubPagesReady = true`) | `applicationOfflineReady`, `applicationPublicBenefitOpenSource`, `applicationZeroPiiSanitized`, `applicationGithubPagesReady` |",
        "| `src/Standards.lex.tex` | 16 Legal, Meta-Theoretical, Ethical, Cryptographic & Accessibility Standards | `standardIdsDistinct`, `everyPanelCoveredByStandard`, `everyArtifactCoveredByStandard`, `everyPortalPageCoveredByStandard`, `everyJourneyCoveredByStandard`, `everyNavigationCoveredByStandard`, `everyVisualizationCoveredByStandard`, `everyModuleCoveredByStandard` |",
        "| `src/Api.lex.tex` | 20 Mechanized CLI Commands (`bin/prism-legal`) | `commandCountIs` |",
        "",
        "## 2. Reference Matter Claims Ledger (`CLM-01` – `CLM-24`)",
        "",
        "| ID | Status | Category | Statutory Anchor | Supporting Exhibits | Statement |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for c in casemodel.CLAIMS:
        lines.append(
            f"| `{c['id']}` | `{c['status']}` | `{c['category']}` | `{c['statutory']}` | {', '.join(f'`{x}`' for x in c['exhibits'])} | {c['statement']} |"
        )
    lines.append("")
    return "\n".join(lines)


def files():
    out = {
        MODEL_DIR / "authorities.toml": render_authorities(),
        MODEL_DIR / "ids.toml": render_ids(),
        MODEL_DIR / "ledger.toml": render_ledger(),
        MODEL_DIR / "commands.toml": render_commands(),
        MODEL_DIR / "contracts.toml": render_contracts(),
        MODEL_DIR / "dependencies.toml": render_dependencies(),
        MODEL_DIR / "errors.toml": render_errors(),
        MODEL_DIR / "projection.toml": render_projection(),
        MODEL_DIR / "ux-journeys.toml": render_ux_journeys(),
        MODEL_DIR / "runtime-roots.toml": render_runtime_roots(),
        MODEL_DIR / "stdlib-package.toml": render_stdlib_package(),
        CONFORMANCE_MD: render_conformance_md(),
    }
    for name, body in render_schemas().items():
        out[SCHEMA_DIR / name] = body
    for name, body in render_features().items():
        out[SUITE_DIR / name] = body
    return out


def sync():
    changed = False
    f_map = files()
    for path, content in f_map.items():
        if _write(path, content):
            changed = True
    return {"model": "model/", "claims": len(casemodel.CLAIMS), "registers": len(f_map), "changed": changed}


def check():
    for path, content in files().items():
        if not path.exists() or path.read_text() != content:
            return {"ok": False, "reason": f"{path.relative_to(ROOT)} drifted or missing; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}

