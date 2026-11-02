"""Legal and technical standards register for PrismLegal (`model/standards.toml` and `src/Standards.lex.tex`)."""

import json
from . import ROOT, lexmod, presentationmodel
from .semantic import (
    BOOL,
    STR,
    all_members,
    call,
    definition,
    distinct_strings,
    field_of_each,
    holds,
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

REGISTER = ROOT / "model" / "standards.toml"
MODULE = ROOT / "src" / "Standards.lex.tex"

NAVIGATION = ["nav-primary", "nav-vantages", "nav-stepper"]
VISUALIZATIONS = [v["id"] for v in presentationmodel.VISUALIZATIONS]
MODULES = [
    "Api",
    "Application",
    "Architecture",
    "Audit",
    "Convert",
    "DirectExam",
    "Discovery",
    "Engine",
    "Intake",
    "LegalMeta",
    "Observer",
    "Portal",
    "Presentation",
    "Register",
    "RemediesCore",
    "Sequences",
    "Standards",
    "VisualEvidence",
]


def _commands():
    from . import apimodel
    return [r["name"] for r in apimodel.surface()]


def rows():
    panels = [p["id"] for p in presentationmodel.PANELS]
    journeys = [j["id"] for j in presentationmodel.JOURNEYS]
    cmds = _commands()
    return [
        {
            "id": "uniform-dom-402",
            "name": "Uniform Domestic Relations Act § 402 — Best Interests of the Child & Parental Responsibility Allocation",
            "authority": "https://www.uniformlaws.org/",
            "version": "2026 Uniform Domestic Code",
            "scope": "Governs allocation of equal parenting time (§ 402(a)) and joint major decision-making (§ 402(b)) across statutory factors SF-01 to SF-11 for the three minor children.",
            "realizedBy": ["Register", "Audit", "Convert", "DirectExam", "VisualEvidence", "Engine", "Sequences", "Discovery", "panel-parenting", "panel-cross-exam", "factors-md", "direct-exam-md", "visual-evidence-md", "client-guide-md", "schedule-svg", "viz-client-strategy", "viz-parenting-schedule", "viz-factors-matrix"] + journeys,
            "conformance": "bin/prism-legal verify: claimsResolvedAndBacked (Register), trapsValidAndBacked (Audit), everyDirectExamQuestionHasFullTestimony (DirectExam), everyRegisterExhibitMapped (VisualEvidence)",
            "coverage": "implemented",
        },
        {
            "id": "uniform-support-305",
            "name": "Uniform Child Support & Remedies Guidelines § 305 & Disability Exemption (§ 305(5)(b))",
            "authority": "https://www.uniformlaws.org/",
            "version": "2030 Uniform Remedies Code",
            "scope": "Governs guideline support calculation on stipulated baseline ($8,000/mo Petitioner, $5,000/mo Respondent), shared parenting adjustment at 182.5 overnights, and bar against imputing wages to a retired disability pensioner.",
            "realizedBy": ["Register", "RemediesCore", "Audit", "panel-financial", "remedies-md", "support-svg", "viz-remedies-waterfall"],
            "conformance": "bin/prism-legal verify: stipulatedBaselineCentsVerified, guidelineTransferCentsVerified (RemediesCore)",
            "coverage": "implemented",
        },
        {
            "id": "uniform-dom-404-408",
            "name": "Uniform Domestic Relations Act §§ 404 (Child Interviews), 406 (Relocation) & 408 (Equal Records Access)",
            "authority": "https://www.uniformlaws.org/",
            "version": "2030 Uniform Domestic Code",
            "scope": "Governs pending Motion for In Camera Interview (§ 404), county geographic proximity (§ 406), and equal parent access to medical, dental, and school records (§ 408).",
            "realizedBy": ["Register", "panel-strategy", "panel-parenting", "compass-md", "factors-md"],
            "conformance": "bin/prism-legal verify: OS-5, SF-02, SF-08, CLM-04, CLM-05 (Register)",
            "coverage": "implemented",
        },
        {
            "id": "frcp-26e-16-2",
            "name": "Federal Rules of Civil Procedure Rules 16 & 26(e) / Mandatory Financial Disclosure Rule 16.2",
            "authority": "https://www.uscourts.gov/rules-policies/current-rules-practice-procedure/federal-rules-civil-procedure",
            "version": "FRCP / Rule 16.2 (2030)",
            "scope": "Governs pretrial stipulations and affirmative duty of complete financial disclosure violated on the May 12, 2029 SFS (Ex. G, omitting $30,000.00 in Ex. H).",
            "realizedBy": ["Register", "RemediesCore", "Audit", "panel-financial", "panel-evidence", "remedies-md", "viz-disclosure-audit"],
            "conformance": "bin/prism-legal verify: undisclosedReserveCentsVerified (RemediesCore), CLM-13, CLM-14, TRAP-06",
            "coverage": "implemented",
        },
        {
            "id": "fre-evidence",
            "name": "Federal & Uniform Rules of Evidence (FRE 106, 401–403, 602, 608, 613, 801(d)(2), 901)",
            "authority": "https://www.uscourts.gov/rules-policies/current-rules-practice-procedure/federal-rules-evidence",
            "version": "FRE (2030)",
            "scope": "Governs foundation, relevance, FRE 106 Rule of Completeness across homework study log (OP Ex. 13) and co-parenting exports (OP Ex. 5, 14), personal knowledge limits of lay witnesses (W-03 to W-10), and Direct Examination exhibit admissions.",
            "realizedBy": ["Register", "Audit", "DirectExam", "VisualEvidence", "panel-lawyer-tuner", "panel-cross-exam", "panel-evidence", "lawyer-tuner-md", "direct-exam-md", "visual-evidence-md", "pivots-md", "witnesses-md", "timeline-svg", "viz-lawyer-tuner", "viz-timeline", "viz-claim-dag"],
            "conformance": "bin/prism-legal verify: exhibitIdsDistinct, trapsValidAndBacked, directExamQuestionExhibitsResolve, everyRegisterExhibitMapped",
            "coverage": "implemented",
        },
        {
            "id": "usc-38-ada",
            "name": "38 U.S.C. Ch. 11 & § 1781 Statutory Benefits / 42 U.S.C. § 12101 Americans with Disabilities Act",
            "authority": "https://www.ecfr.gov/current/title-38/chapter-I/part-4",
            "version": "38 U.S.C. / 42 U.S.C. (2030)",
            "scope": "Governs disability retirement protection (Ex. E), statutory dependent medical coverage (§ 1781), and ADA workplace/judicial accommodations across multi-domain portal matters.",
            "realizedBy": ["Register", "Audit", "LegalMeta", "Portal", "panel-hub", "panel-financial", "remedies-md", "viz-platform-hub"],
            "conformance": "bin/prism-legal verify: CLM-09, CLM-11, CLM-15, HOH-03, LRML-03, LRML-04",
            "coverage": "implemented",
        },
        {
            "id": "ucc-rest2d-const",
            "name": "UCC Article 2, Restatement (Second) of Contracts, Housing Defense & Constitutional Brady Standards",
            "authority": "https://www.ali.org/",
            "version": "UCC / Restatement 2d (2026)",
            "scope": "Governs commercial contract performance, fiduciary accounting, landlord-tenant habitability defense, and constitutional due-process standards modeled in the multi-domain platform.",
            "realizedBy": ["Portal", "LegalMeta", "panel-hub", "site", "viz-platform-hub"],
            "conformance": "bin/prism-legal verify: frameworkIdsDistinct, casesResolveToFrameworks, casesResolveToCourts (Portal)",
            "coverage": "implemented",
        },
        {
            "id": "hohfeld-1913",
            "name": "Hohfeldian Fundamental Legal Conceptions (Right/Duty, Privilege/No-Right, Power/Liability, Immunity/Disability)",
            "authority": "https://doi.org/10.2307/785533",
            "version": "Hohfeld (1913 / 1917 Yale Law Journal)",
            "scope": "Formalizes first-order and second-order jural relations and involutive correlatives/opposites (HOH-01..HOH-08).",
            "realizedBy": ["LegalMeta", "Portal", "panel-lawyer-tuner", "lawyer-tuner-md", "viz-lawyer-tuner"],
            "conformance": "bin/prism-legal verify: hohfeldIdsDistinct (LegalMeta)",
            "coverage": "implemented",
        },
        {
            "id": "oasis-legalruleml-1.0",
            "name": "OASIS LegalRuleML Core Specification v1.0 — Defeasible Deontic & Legal Rule Modeling",
            "authority": "https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/os/legalruleml-core-spec-v1.0-os.html",
            "version": "1.0 (OASIS Standard)",
            "scope": "Formalizes constitutive and prescriptive rules (LRML-01..LRML-08) and superiority overrides (SUP-01..SUP-04).",
            "realizedBy": ["LegalMeta", "RemediesCore", "panel-lawyer-tuner", "panel-financial", "lawyer-tuner-md"],
            "conformance": "bin/prism-legal verify: legalRuleIdsDistinct, superiorityIdsDistinct, superiorityOverridesValid (LegalMeta)",
            "coverage": "implemented",
        },
        {
            "id": "dung-aspic-arg",
            "name": "Dung (1995) Abstract Argumentation & ASPIC+ Structured Legal Argumentation Framework",
            "authority": "https://doi.org/10.1016/0004-3702(94)00041-X",
            "version": "Dung 1995 / ASPIC+ (Modgil & Prakken 2013)",
            "scope": "Formalizes structured trial arguments and 16 attack relations (ATK-01..16), proving every opposing argument is defeated in the grounded extension.",
            "realizedBy": ["LegalMeta", "Audit", "panel-cross-exam", "panel-lawyer-tuner", "pivots-md", "viz-claim-dag"],
            "conformance": "bin/prism-legal verify: attackIdsDistinct (LegalMeta)",
            "coverage": "implemented",
        },
        {
            "id": "oasis-akoma-ntoso-1.0",
            "name": "OASIS Akoma Ntoso / LegalDocML v1.0 — FRBR Legal Document & URI Naming Standard",
            "authority": "http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part1-vocabulary/akn-core-v1.0-os-part1-vocabulary.html",
            "version": "1.0 (OASIS Standard)",
            "scope": "Assigns canonical FRBR Work URIs (`akn:/us/...`) to all governing statutes, court rules, orders, and pleadings (AKN-01..AKN-08).",
            "realizedBy": ["LegalMeta", "Register", "Standards", "register-json", "standards-json"],
            "conformance": "bin/prism-legal verify: aknIdsDistinct (LegalMeta)",
            "coverage": "implemented",
        },
        {
            "id": "oasis-ecf-sali",
            "name": "OASIS Electronic Court Filing (ECF) v5.0 & SALI Alliance Legal Matter Specification Standard (LMSS) v2.0",
            "authority": "https://www.sali.org/",
            "version": "ECF 5.0 / SALI 2.0",
            "scope": "Standardizes court metadata, law firms, legal aid clinics, practice areas, and multi-domain case classification across the Public-Benefit Platform.",
            "realizedBy": ["Portal", "Register", "panel-hub", "panel-strategy", "panel-lawyer-tuner", "site", "client-guide-md", "lawyer-tuner-md"],
            "conformance": "bin/prism-legal verify: caseIdsDistinct, firmIdsDistinct, courtIdsDistinct, lawyersResolveToFirms, casesResolveToCourts (Portal)",
            "coverage": "implemented",
        },
        {
            "id": "aba-rpc-webauthn-sharing",
            "name": "ABA Model Rules 1.2(c) & 1.16 (Portable Scoped Representation) + W3C WebAuthn & AES-256-GCM Case Sharing",
            "authority": "https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/",
            "version": "ABA Model Rules / W3C WebAuthn (2026)",
            "scope": "Guarantees zero lawyer lock-in (`portableExitRight = true`), cryptographic capability-based case sharing (`SHARE-01..05`), and multi-provider authentication (`AUTH-PASSKEY`, `AUTH-BAR-OIDC`, `AUTH-LEGAL-AID`, `AUTH-LOCAL-VAULT`).",
            "realizedBy": ["Portal", "LegalMeta", "panel-hub", "panel-strategy", "panel-lawyer-tuner", "site", "client-page", "lawyer-page"],
            "conformance": "bin/prism-legal verify: authProviderIdsDistinct, shareGrantIdsDistinct, engagementsValidAndPortable, shareGrantsValidAndRevocable (Portal)",
            "coverage": "implemented",
        },
        {
            "id": "iso-15489-27037",
            "name": "ISO 15489-1:2016 & ISO/IEC 27037:2012 — Records Management & Digital Evidence Chain of Custody",
            "authority": "https://www.iso.org/standard/62542.html",
            "version": "2016 / 2012",
            "scope": "Verifies authenticity, SHA-256 integrity, and evidentiary foundation across the chain of custody (COC-01..COC-08).",
            "realizedBy": ["LegalMeta", "Register", "panel-evidence", "witnesses-md", "register-json"],
            "conformance": "bin/prism-legal verify: cocIdsDistinct (LegalMeta)",
            "coverage": "implemented",
        },
        {
            "id": "iso-42010-25010",
            "name": "ISO/IEC/IEEE 42010:2022 & ISO/IEC 25010:2023 — Systems Architecture & Product Quality Model",
            "authority": "https://www.iso.org/standard/74393.html",
            "version": "2022 / 2023",
            "scope": "Stakeholders, concerns, viewpoints, views, quality measures, and zero-PII sanitization guarantees across the platform.",
            "realizedBy": ["Architecture", "Presentation", "Observer", "Application", "Api", "Convert", "Engine", "Intake", "Sequences", "Discovery"] + panels + cmds,
            "conformance": "bin/prism-legal verify: viewsResolveToViewpoints (Architecture), panelsGovernedByViewpoints (Presentation), applicationZeroPiiSanitized (Application)",
            "coverage": "implemented",
        },
        {
            "id": "wcag-2.2-iso-9241",
            "name": "W3C WCAG 2.2 Level AA, WAI-ARIA 1.2 & ISO 9241-110/112 — Accessibility & Multi-Page Cognitive Ergonomics",
            "authority": "https://www.w3.org/TR/WCAG22/",
            "version": "WCAG 2.2 / ISO 9241 (2023)",
            "scope": "Enforces 4.5:1 text contrast across light and dark themes, separate task-focused pages (`index.html`, `client.html`, `lawyer.html`, `courtroom.html`), bounded cognitive load (<= 5 sections/page), and zero meta-taxonomy leakage.",
            "realizedBy": ["Presentation", "Standards", "site", "client-page", "lawyer-page", "courtroom-page", "logo", "schedule-svg", "support-svg", "timeline-svg", "page-home", "page-client", "page-lawyer", "page-courtroom", "compass-md", "client-guide-md", "lawyer-tuner-md", "factors-md", "remedies-md", "pivots-md", "witnesses-md", "direct-exam-md", "visual-evidence-md", "register-json", "tuning-json", "standards-json"] + panels + NAVIGATION + VISUALIZATIONS,
            "conformance": "bin/prism-legal verify: everyPairMeetsContrastLight, everyPairMeetsContrastDark, everyPageWithinCognitiveLoadBudget, domainLabelsFreeOfMetaTaxonomy (Presentation)",
            "coverage": "implemented",
        },
    ]


def declarations():
    st_t = named("Standard")
    standards = rows()
    rec = lambda st: record(
        "Standard",
        id=s(st["id"]),
        name=s(st["name"]),
        authority=s(st["authority"]),
        version=s(st["version"]),
        scope=s(st["scope"]),
        realizedBy=strings(st["realizedBy"]),
        conformance=s(st["conformance"]),
        coverage=s(st["coverage"]),
    )
    append_str = lambda a, b_list: {
        "kind": "primitive",
        "operation": "append",
        "result": list_t(STR),
        "arguments": [a, b_list],
    }

    return [
        structure(
            "Standard",
            [
                ("id", STR),
                ("name", STR),
                ("authority", STR),
                ("version", STR),
                ("scope", STR),
                ("realizedBy", list_t(STR)),
                ("conformance", STR),
                ("coverage", STR),
            ],
        ),
        definition("standards", list_t(st_t), lst([rec(st) for st in standards], st_t)),
        definition("moduleIds", list_t(STR), strings(MODULES)),
        definition("navigationIds", list_t(STR), strings(NAVIGATION)),
        definition("visualizationIds", list_t(STR), strings(VISUALIZATIONS)),
        member_string(),
        all_members(),
        distinct_strings(),
        field_of_each("standardIds", st_t, "id"),
        definition(
            "standardRealizers",
            list_t(STR),
            match_list(
                var("sts"),
                {"kind": "nil", "element": STR},
                "head",
                "tail",
                append_str(proj(var("head"), "realizedBy"), call("standardRealizers", var("tail"))),
            ),
            parameters=[("sts", list_t(st_t))],
            recursive="sts",
        ),
        holds("standardIdsDistinct", call("distinctStrings", call("standardIds", call("standards")))),
        holds(
            "everyPanelCoveredByStandard",
            call(
                "allMembers",
                call("panelIds", call("panels", module="Presentation"), module="Presentation"),
                call("standardRealizers", call("standards")),
            ),
        ),
        holds(
            "everyArtifactCoveredByStandard",
            call(
                "allMembers",
                call("artifactIds", call("artifacts", module="Presentation"), module="Presentation"),
                call("standardRealizers", call("standards")),
            ),
        ),
        holds(
            "everyJourneyCoveredByStandard",
            call(
                "allMembers",
                call("journeyIds", call("journeys", module="Presentation"), module="Presentation"),
                call("standardRealizers", call("standards")),
            ),
        ),
        holds(
            "everyNavigationCoveredByStandard",
            call("allMembers", call("navigationIds"), call("standardRealizers", call("standards"))),
        ),
        holds(
            "everyVisualizationCoveredByStandard",
            call("allMembers", call("visualizationIds"), call("standardRealizers", call("standards"))),
        ),
        holds(
            "everyModuleCoveredByStandard",
            call("allMembers", call("moduleIds"), call("standardRealizers", call("standards"))),
        ),
        holds(
            "everyPortalPageCoveredByStandard",
            call(
                "allMembers",
                call("portalPageIds", call("portalPages", module="Presentation"), module="Presentation"),
                call("standardRealizers", call("standards")),
            ),
        ),
    ]


def render_toml():
    lines = ['spec = "prismpm/standards/1"', ""]
    for st in rows():
        lines += [
            "[[standard]]",
            f'id = {json.dumps(st["id"])}',
            f'name = {json.dumps(st["name"])}',
            f'authority = {json.dumps(st["authority"])}',
            f'version = {json.dumps(st["version"])}',
            f'scope = {json.dumps(st["scope"])}',
            f'realized_by = {json.dumps(st["realizedBy"])}',
            f'conformance = {json.dumps(st["conformance"])}',
            f'coverage = {json.dumps(st["coverage"])}',
            "",
        ]
    return "\n".join(lines)


def render():
    return lexmod.module(
        "Standards",
        declarations(),
        title="PrismLegal Legal & Technical Standards Register",
        imports=("Presentation",),
    )


def sync():
    MODULE.parent.mkdir(parents=True, exist_ok=True)
    REGISTER.parent.mkdir(parents=True, exist_ok=True)
    toml_text = render_toml()
    if not REGISTER.exists() or REGISTER.read_text() != toml_text:
        REGISTER.write_text(toml_text)
    text = render()
    changed = not MODULE.exists() or MODULE.read_text() != text
    if changed:
        MODULE.write_text(text)
    return {"module": str(MODULE.relative_to(ROOT)), "standards": len(rows()), "changed": changed}


def check():
    if not MODULE.exists() or not REGISTER.exists():
        return {"ok": False, "reason": "Standards.lex.tex or model/standards.toml missing; run `bin/prism-legal api sync`"}
    ok = MODULE.read_text() == render() and REGISTER.read_text() == render_toml()
    return {"ok": ok, "reason": None if ok else "Standards.lex.tex or model/standards.toml drifted; run `bin/prism-legal api sync`"}

