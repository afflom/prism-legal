"""Multi-Tenant Public-Benefit Legal Platform & Portal Model (`src/Portal.lex.tex` and `model/portal.toml`).

Models PrismLegal as both a free Public-Benefit Service and a full Production Platform:
- Public-Benefit Governance Charter (`PUBLIC_BENEFIT_CHARTER`)
- Authentication, Identity & Session Providers (`AUTH_PROVIDERS`, `USER_SESSIONS`)
- Cryptographic Case Sharing & Capability Grants (`SHARE_GRANTS`)
- Law Firms & Legal Aid Clinics (`FIRMS`)
- Courts & Administrative Tribunals (`COURTS`)
- Multi-Domain Legal Frameworks (`LEGAL_FRAMEWORKS`)
- Clients (`CLIENTS`), Attorneys (`LAWYERS`), Multi-Domain Cases (`CASES`),
  and Many-to-Many (`M:N`) Engagements (`ENGAGEMENTS`) with zero single-lawyer lock-in."""

import json
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

REGISTER = ROOT / "model" / "portal.toml"
MODULE = ROOT / "src" / "Portal.lex.tex"

PUBLIC_BENEFIT_CHARTER = {
    "id": "CHARTER-PRISM-LEGAL-1.0",
    "mission": "Free, open-source, formally verified legal case preparation, evidence structuring, and courtroom strategy platform empowering clients, legal aid clinics, and trial attorneys to improve legal outcomes.",
    "license": "MIT OR Apache-2.0 (Public Benefit Open Source)",
    "privacyGuarantee": "Local-first client-side execution; zero remote LLM calls; zero third-party telemetry; cryptographic AES-256-GCM bundle sharing.",
    "ethicsCompliance": "ABA Model Rules 1.1 (Competence), 1.2(c) (Unbundled/Scoped Representation), 1.4 (Client Communication), 1.6 (Confidentiality), 1.16(a)(3) (Client Freedom of Counsel Choice).",
}

AUTH_PROVIDERS = [
    {
        "id": "AUTH-PASSKEY",
        "name": "WebAuthn / FIDO2 Passkey Sign-In",
        "protocol": "W3C WebAuthn Level 3 / FIDO2",
        "supportedRoles": ["client", "lawyer", "clinic-advocate"],
        "securityLevel": "Hardware-Bound Asymmetric Keypair",
    },
    {
        "id": "AUTH-BAR-OIDC",
        "name": "State Bar & Court ECF Attorney Verification",
        "protocol": "OpenID Connect 1.0 / SAML 2.0",
        "supportedRoles": ["lawyer", "firm-admin"],
        "securityLevel": "Verified Bar Number & Multi-Factor Auth",
    },
    {
        "id": "AUTH-LEGAL-AID",
        "name": "Public-Benefit Legal Aid Clinic Voucher Sign-In",
        "protocol": "OAuth 2.0 PKCE + Clinic Fellowship Token",
        "supportedRoles": ["client", "clinic-advocate", "lawyer"],
        "securityLevel": "Zero-Cost Pro Bono Access Grant",
    },
    {
        "id": "AUTH-LOCAL-VAULT",
        "name": "Offline Courtroom AES-256-GCM Local Vault",
        "protocol": "WebCrypto PBKDF2-SHA256 + AES-256-GCM",
        "supportedRoles": ["client", "lawyer", "courtroom-stand"],
        "securityLevel": "Zero-Network Local Browser Persistence",
    },
]

SHARE_GRANTS = [
    {
        "id": "SHARE-01",
        "caseId": "CASE-2030-FAM-9010",
        "granterId": "CLIENT-DOM-RESPONDENT",
        "granteeId": "LAWYER-LEAD-TRIAL",
        "capability": "cap-lead-counsel-codesign",
        "encryption": "AES-256-GCM + Ed25519 Signed Manifest",
        "scope": "Full read/write access to claims, exhibits, witness examination scripts, and strategy tuning.",
        "revocable": True,
    },
    {
        "id": "SHARE-02",
        "caseId": "CASE-2030-ADM-9020",
        "granterId": "CLIENT-DOM-RESPONDENT",
        "granteeId": "LAWYER-VET-BENEFITS",
        "capability": "cap-scoped-benefits-counsel",
        "encryption": "AES-256-GCM Scoped Matter Key",
        "scope": "Scoped access to statutory disability & dependent healthcare records under ABA Rule 1.2(c); isolated from unrelated matters.",
        "revocable": True,
    },
    {
        "id": "SHARE-03",
        "caseId": "CASE-2030-COM-9030",
        "granterId": "CLIENT-DOM-RESPONDENT",
        "granteeId": "LAWYER-COMMERCIAL-TAX",
        "capability": "cap-commercial-fiduciary-counsel",
        "encryption": "AES-256-GCM Scoped Matter Key",
        "scope": "Scoped access to commercial contract, IP, and tax ledger exhibits.",
        "revocable": True,
    },
    {
        "id": "SHARE-04",
        "caseId": "CASE-2030-EMP-9040",
        "granterId": "CLIENT-ADA-CLAIMANT",
        "granteeId": "LAWYER-PUBLIC-DEFENSE",
        "capability": "cap-employment-civil-rights",
        "encryption": "AES-256-GCM Scoped Matter Key",
        "scope": "Full co-design access for ADA workplace accommodation and administrative appeal.",
        "revocable": True,
    },
    {
        "id": "SHARE-05",
        "caseId": "CASE-2030-HSG-9060",
        "granterId": "CLIENT-HOUSING-TENANTS",
        "granteeId": "LAWYER-PUBLIC-DEFENSE",
        "capability": "cap-housing-clinic-defense",
        "encryption": "AES-256-GCM Clinic Vault Key",
        "scope": "Pro bono legal aid representation on habitability and statutory notice defense.",
        "revocable": True,
    },
]

FIRMS = [
    {
        "id": "FIRM-CIVIC-ADVOCACY",
        "name": "Civic Justice & Trial Advocacy LLP",
        "kind": "Litigation & Family Law Firm",
        "jurisdictions": ["State Trial & Appellate Courts", "Mediation Forums"],
        "proBonoTier": "Public-Benefit Partner (25% Pro Bono / Sliding Scale)",
    },
    {
        "id": "FIRM-VET-CLINIC",
        "name": "Statutory & Federal Benefits Public Law Clinic",
        "kind": "Non-Profit Legal Aid Clinic",
        "jurisdictions": ["Administrative Appeals Board", "Federal Benefits Tribunal"],
        "proBonoTier": "100% Free Public-Benefit Representation",
    },
    {
        "id": "FIRM-PACIFIC-COMMERCIAL",
        "name": "Meridian Commercial, IP & Fiduciary Law Group",
        "kind": "Civil & Commercial Boutique",
        "jurisdictions": ["U.S. District Court", "State Commercial Docket"],
        "proBonoTier": "Unbundled & Limited-Scope Co-Counsel (ABA Rule 1.2(c))",
    },
    {
        "id": "FIRM-METRO-LEGAL-AID",
        "name": "Metro Access-to-Justice Legal Aid Society",
        "kind": "Community Legal Aid Clinic",
        "jurisdictions": ["Housing Court", "Employment & Civil Rights Commission", "Criminal Defense"],
        "proBonoTier": "100% Free Public-Benefit Service",
    },
]

COURTS = [
    {
        "id": "COURT-STATE-DIST",
        "name": "State District Court — Civil & Domestic Relations Division",
        "level": "State Trial Court of General Jurisdiction",
        "rulesFramework": "FW-UNIFORM-DOM",
        "location": "Regional Judicial Center, Division 7C",
    },
    {
        "id": "COURT-FED-DIST",
        "name": "United States District Court — Civil & Constitutional Docket",
        "level": "Federal Article III Trial Court",
        "rulesFramework": "FW-FRCP",
        "location": "Federal Courthouse, Room 310",
    },
    {
        "id": "COURT-BVA-FED",
        "name": "Federal Administrative & Pension Appeals Tribunal",
        "level": "Federal Administrative & Article I Appellate Forum",
        "rulesFramework": "FW-USC-38-ADA",
        "location": "Regional Administrative Forum / Video Tele-Hearing",
    },
    {
        "id": "COURT-ADMIN-CIV",
        "name": "Office of Administrative Courts — Employment & Housing Division",
        "level": "State Administrative Law Tribunal",
        "rulesFramework": "FW-UCC-REST2D",
        "location": "Civic Administrative Building, Hearing Room 2",
    },
]

LEGAL_FRAMEWORKS = [
    {
        "id": "FW-FRE",
        "name": "Federal & Uniform Rules of Evidence (FRE 106, 401-403, 602, 608, 613, 801, 901)",
        "domain": "Evidentiary Admissibility & Impeachment",
        "summary": "Governs Rule 106 completeness, foundation, witness personal knowledge, and documentary impeachment across all trial matters.",
    },
    {
        "id": "FW-FRCP",
        "name": "Federal & State Rules of Civil Procedure (FRCP 16, 26(a)/(e), 37 & Rule 16.2)",
        "domain": "Civil Procedure & Mandatory Disclosures",
        "summary": "Governs pretrial stipulations, mandatory financial/evidentiary disclosures, and remedies for sworn omissions.",
    },
    {
        "id": "FW-UNIFORM-DOM",
        "name": "Uniform Domestic Relations, Best-Interests (§ 402) & Support Guidelines (§ 305)",
        "domain": "Family & Domestic Relations Law",
        "summary": "Governs equal parenting allocation, joint decision-making, mediation-first protocols, and guideline child support.",
    },
    {
        "id": "FW-USC-38-ADA",
        "name": "38 U.S.C. Ch. 11 & § 1781 Statutory Benefits / 42 U.S.C. § 12101 ADA Rights",
        "domain": "Statutory Benefits, Disability & Civil Rights",
        "summary": "Governs disability retirement protection, dependent healthcare eligibility, and workplace/judicial accommodations.",
    },
    {
        "id": "FW-UCC-REST2D",
        "name": "UCC Article 2, Restatement (Second) of Contracts & Fiduciary Accounting",
        "domain": "Commercial, Contract, Housing & Trust Law",
        "summary": "Governs contract performance, damages mitigation, fiduciary accounting, and landlord-tenant habitability duties.",
    },
    {
        "id": "FW-CRIM-CONST",
        "name": "U.S. Constitution Amends. IV, V, VI, XIV & Brady Evidentiary Standards",
        "domain": "Constitutional & Criminal Defense",
        "summary": "Governs unlawful search/seizure suppression, exculpatory disclosure duties, and confrontation rights.",
    },
]

CLIENTS = [
    {
        "id": "CLIENT-DOM-RESPONDENT",
        "name": "Respondent (Client Litigant)",
        "profile": "Retired Disability Pensioner, Custodial Co-Parent of Three Minor Children (Ages 15, 11 & 6) & Public-Interest Curriculum Author",
        "activeCaseIds": ["CASE-2030-FAM-9010", "CASE-2030-ADM-9020", "CASE-2030-COM-9030"],
    },
    {
        "id": "CLIENT-ADA-CLAIMANT",
        "name": "Employee Civil Rights Claimant",
        "profile": "Senior Systems Analyst & ADA Workplace Accommodation / Commercial Contract Claimant",
        "activeCaseIds": ["CASE-2030-EMP-9040", "CASE-2030-CON-9050"],
    },
    {
        "id": "CLIENT-HOUSING-TENANTS",
        "name": "Residential Tenant Association Household",
        "profile": "Small Business Owners & Community Housing Tenants Association Representatives",
        "activeCaseIds": ["CASE-2030-HSG-9060"],
    },
]

LAWYERS = [
    {
        "id": "LAWYER-LEAD-TRIAL",
        "name": "Lead Domestic Relations Trial Counsel",
        "firmId": "FIRM-CIVIC-ADVOCACY",
        "firm": "Civic Justice & Trial Advocacy LLP",
        "barNumber": "BAR-44109",
        "specialty": "Lead Trial Counsel — Family Law, Complex Financial Impeachment & Evidentiary Trials",
    },
    {
        "id": "LAWYER-VET-BENEFITS",
        "name": "Statutory & Administrative Benefits Counsel",
        "firmId": "FIRM-VET-CLINIC",
        "firm": "Statutory & Federal Benefits Public Law Clinic",
        "barNumber": "BAR-31892",
        "specialty": "Statutory Disability Protection & Dependent Healthcare Benefits Counsel",
    },
    {
        "id": "LAWYER-COMMERCIAL-TAX",
        "name": "Commercial, Entity Governance & Tax Counsel",
        "firmId": "FIRM-PACIFIC-COMMERCIAL",
        "firm": "Meridian Commercial, IP & Fiduciary Law Group",
        "barNumber": "BAR-52904",
        "specialty": "Commercial Litigation, Open-Source Entity Governance & Tax Audit Counsel",
    },
    {
        "id": "LAWYER-PUBLIC-DEFENSE",
        "name": "Public-Benefit Employment & Housing Defense Counsel",
        "firmId": "FIRM-METRO-LEGAL-AID",
        "firm": "Metro Access-to-Justice Legal Aid Society",
        "barNumber": "BAR-60218",
        "specialty": "Public-Benefit Employment, Civil Rights (ADA) & Housing Defense Counsel",
    },
]

CASES = [
    {
        "id": "CASE-2030-FAM-9010",
        "docketNumber": "2030-FAM-9010",
        "title": "In re Household Dissolution & Parenting Allocation",
        "practiceArea": "Family & Domestic Relations",
        "courtId": "COURT-STATE-DIST",
        "forum": "State District Court, Division 7C",
        "frameworkId": "FW-UNIFORM-DOM",
        "status": "Permanent Orders Hearing — Trial Readiness Active",
        "summary": "Equal 50/50 parenting plan (182.5 overnights) for three minor children (Ages 15, 11 & 6), joint decision-making, $250/mo guideline support, and $30,000.00 Rule 16.2 disclosure impeachment.",
    },
    {
        "id": "CASE-2030-ADM-9020",
        "docketNumber": "2030-ADM-9020",
        "title": "In re Statutory Disability Retirement & Dependent Healthcare Benefits",
        "practiceArea": "Administrative & Benefits Law",
        "courtId": "COURT-BVA-FED",
        "forum": "Federal Administrative & Pension Appeals Tribunal",
        "frameworkId": "FW-USC-38-ADA",
        "status": "Disability Retirement Active — Dependent Benefit Audit Complete",
        "summary": "Preserves certified disability retirement rating ($5,000/mo tax-free) and zero-premium statutory medical coverage for all three minor dependents.",
    },
    {
        "id": "CASE-2030-COM-9030",
        "docketNumber": "2030-COM-9030",
        "title": "Open-Source Civic Curriculum Foundation — Non-Profit Governance & Tax Compliance",
        "practiceArea": "Commercial & Non-Profit Governance",
        "courtId": "COURT-FED-DIST",
        "forum": "U.S. District Court / IRS Exempt Organizations Compliance",
        "frameworkId": "FW-UCC-REST2D",
        "status": "Verified Zero-Revenue Compliance (2026-2029)",
        "summary": "Confirms $0.00 wages, draws, or commercial distributions across 2026-2029 tax transcripts (Ex-C, Ex-D) and protects open-source public-benefit IP.",
    },
    {
        "id": "CASE-2030-EMP-9040",
        "docketNumber": "2030-EMP-9040",
        "title": "Employee Claimant v. Horizon Logistics Corp. — ADA Reasonable Accommodation",
        "practiceArea": "Employment & Civil Rights Law",
        "courtId": "COURT-ADMIN-CIV",
        "forum": "Office of Administrative Courts — Civil Rights Division",
        "frameworkId": "FW-USC-38-ADA",
        "status": "Evidentiary Summary Judgment Briefing",
        "summary": "Formalizes interactive-process timeline, medical accommodation records, and back-pay mitigation ledger under 42 U.S.C. § 12112.",
    },
    {
        "id": "CASE-2030-CON-9050",
        "docketNumber": "2030-CON-9050",
        "title": "Commercial Buyer Entity v. Precision Components Inc. — UCC Article 2 Warranty",
        "practiceArea": "Civil & Commercial Litigation",
        "courtId": "COURT-FED-DIST",
        "forum": "U.S. District Court — Commercial Docket",
        "frameworkId": "FW-UCC-REST2D",
        "status": "Discovery & Rule 26(e) Audit",
        "summary": "Models UCC Article 2 express warranty breach, cover damages calculation, and chain-of-custody inspection logs.",
    },
    {
        "id": "CASE-2030-HSG-9060",
        "docketNumber": "2030-HSG-9060",
        "title": "Oakridge Tenants Association v. Oakridge Property Holdings LLC — Habitability & Escrow",
        "practiceArea": "Housing & Real Property Law",
        "courtId": "COURT-ADMIN-CIV",
        "forum": "Metro Housing & Civil Tribunal",
        "frameworkId": "FW-UCC-REST2D",
        "status": "Preliminary Injunction Granted — Trial Prep",
        "summary": "Public-benefit legal aid matter modeling municipal code inspection forensics, rent-escrow accounting, and statutory notice defenses.",
    },
]

ENGAGEMENTS = [
    {"id": "ENG-01", "clientId": "CLIENT-DOM-RESPONDENT", "lawyerId": "LAWYER-LEAD-TRIAL", "caseId": "CASE-2030-FAM-9010", "role": "Lead Trial Counsel", "coloRpcRule": "ABA Model Rule 1.2(a) & 1.4", "scopeOfRepresentation": "Full trial representation for Permanent Orders hearing, witness examinations, and guideline support."},
    {"id": "ENG-02", "clientId": "CLIENT-DOM-RESPONDENT", "lawyerId": "LAWYER-VET-BENEFITS", "caseId": "CASE-2030-ADM-9020", "role": "Specialized Statutory Benefits Counsel", "coloRpcRule": "ABA Model Rule 1.2(c) & 1.16(a)(3)", "scopeOfRepresentation": "Dedicated representation on disability pension protection and dependent healthcare benefits."},
    {"id": "ENG-03", "clientId": "CLIENT-DOM-RESPONDENT", "lawyerId": "LAWYER-VET-BENEFITS", "caseId": "CASE-2030-FAM-9010", "role": "Consulting Co-Counsel (Statutory Exemption)", "coloRpcRule": "ABA Model Rule 1.2(c)", "scopeOfRepresentation": "Limited-scope statutory briefing on disability anti-imputation rules."},
    {"id": "ENG-04", "clientId": "CLIENT-DOM-RESPONDENT", "lawyerId": "LAWYER-COMMERCIAL-TAX", "caseId": "CASE-2030-COM-9030", "role": "Corporate & Tax Compliance Counsel", "coloRpcRule": "ABA Model Rule 1.2(c)", "scopeOfRepresentation": "Independent representation on open-source entity governance and IRS transcript verification."},
    {"id": "ENG-05", "clientId": "CLIENT-ADA-CLAIMANT", "lawyerId": "LAWYER-PUBLIC-DEFENSE", "caseId": "CASE-2030-EMP-9040", "role": "Lead Civil Rights Counsel", "coloRpcRule": "ABA Model Rule 1.2(a)", "scopeOfRepresentation": "Representation in ADA accommodation hearing and damages calculation."},
    {"id": "ENG-06", "clientId": "CLIENT-ADA-CLAIMANT", "lawyerId": "LAWYER-COMMERCIAL-TAX", "caseId": "CASE-2030-CON-9050", "role": "Commercial Litigation Counsel", "coloRpcRule": "ABA Model Rule 1.2(c)", "scopeOfRepresentation": "Client retains separate commercial counsel for UCC warranty dispute without lock-in."},
    {"id": "ENG-07", "clientId": "CLIENT-HOUSING-TENANTS", "lawyerId": "LAWYER-PUBLIC-DEFENSE", "caseId": "CASE-2030-HSG-9060", "role": "Pro Bono Legal Aid Lead Counsel", "coloRpcRule": "ABA Model Rule 6.1 & 1.2(a)", "scopeOfRepresentation": "Zero-cost public-benefit representation for tenant association habitability action."},
    {"id": "ENG-08", "clientId": "CLIENT-HOUSING-TENANTS", "lawyerId": "LAWYER-LEAD-TRIAL", "caseId": "CASE-2030-HSG-9060", "role": "Pro Bono Trial Co-Counsel", "coloRpcRule": "ABA Model Rule 6.1", "scopeOfRepresentation": "Evidentiary hearing co-counsel for municipal inspection impeachment."},
]

for _lw in LAWYERS:
    _lw.setdefault("practiceAreas", [s.strip() for s in _lw["specialty"].split(",")])

for _cs in CASES:
    _cs.setdefault("areaOfLaw", _cs["practiceArea"])

for _en in ENGAGEMENTS:
    _en.setdefault("ethicsRule", _en["coloRpcRule"])

PORTAL_VIEWS = [
    {"id": "PV-CLIENT-GOALS", "audience": "client", "route": "client.html", "title": "Step 1: Relief Goals & 6 Narrative Pillars", "purpose": "Helps the client internalize the core case theory and DO/AVOID witness rules."},
    {"id": "PV-CLIENT-DIRECT", "audience": "client", "route": "client.html", "title": "Step 2: Direct Testimony Walkthrough & Photo Guide", "purpose": "Guides the client through all 6 direct-examination chapters, 36 Q&As, and 12 photo pages."},
    {"id": "PV-CLIENT-REHEARSAL", "audience": "client", "route": "client.html", "title": "Step 3: Cross-Examination Flashcard Trainer & Study Log Completeness", "purpose": "Interactive blind-rehearsal flashcards for 16 cross-examination traps and FRE 106 completeness context."},
    {"id": "PV-CLIENT-COUNSEL", "audience": "client", "route": "client.html", "title": "Step 4: My Matters, Engaged Counsel & Secure Case Sharing", "purpose": "Multi-matter client switcher, strategy notes for counsel, and AES-256-GCM sharing grants."},
    {"id": "PV-LAWYER-ROSTER", "audience": "lawyer", "route": "lawyer.html", "title": "Workspace 1: Firm Roster, Courts, Frameworks & Participants", "purpose": "Multi-client, multi-matter practice management across courts and legal frameworks."},
    {"id": "PV-LAWYER-BENCH", "audience": "lawyer", "route": "lawyer.html", "title": "Workspace 2: Statutory Proof, Remedies Calculator & Disclosure Impeachment", "purpose": "Side-by-side statutory proof matrix, guideline calculator, and Rule 26(e)/16.2 omission audit."},
    {"id": "PV-LAWYER-EXAMS", "audience": "lawyer", "route": "lawyer.html", "title": "Workspace 3: Witness Examinations, 360-Min Trial Clock & FRE Objections", "purpose": "Witness time budgeting, 16 cross-exam objections/redirects, and 36-question direct exam script."},
    {"id": "PV-LAWYER-VAULT", "audience": "lawyer", "route": "lawyer.html", "title": "Workspace 4: Master Exhibit Vault, Visual Forensics & Chain of Custody", "purpose": "30-exhibit semantic/intent matrix, handwritten/scanned forensics, and ISO 27037 chain of custody."},
]

COUNTERPARTY_PROFILES = [
    {
        "id": "CP-BENCH-DIV7C",
        "name": "Presiding Trial Judge (Division 7C)",
        "subjectRole": "Judicial Fact-Finder",
        "governingStandards": "Uniform Best-Interests § 402, Support Guidelines § 305, FRE 106/401/602/901",
        "analyticalFocus": "Enforces the 360-minute trial clock, relies on Joint Pretrial Certificate stipulations, and evaluates calm, child-focused credibility.",
    },
    {
        "id": "CP-BENEFICIARIES",
        "name": "Minor Children (Ages 15, 11 & 6)",
        "subjectRole": "Protected Minor Beneficiaries",
        "governingStandards": "Uniform Best-Interests § 402(a)(1)-(8) & § 404 In Camera Interview",
        "analyticalFocus": "Need equal 50/50 stability with both capable parents, seamless Wednesday school exchanges, and zero-cost parental care during regional travel weeks.",
    },
    {
        "id": "CP-PETITIONER",
        "name": "Petitioner (Opposing Party & Co-Parent)",
        "subjectRole": "Opposing Party & Co-Parent",
        "governingStandards": "FRCP 26(e) / Rule 16.2 Mandatory Disclosures & FRE 613 Impeachment",
        "analyticalFocus": "Stipulated $8,000/mo salary (Ex-B); omitted $30,000.00 in escrow accounts on Initial SFS (Ex-G/Ex-H); travels regionally requiring co-parent availability.",
    },
]


def declarations():
    client_t = named("ClientEntity")
    lawyer_t = named("LawyerEntity")
    firm_t = named("FirmEntity")
    court_t = named("CourtEntity")
    fw_t = named("FrameworkEntity")
    case_t = named("CaseEntity")
    eng_t = named("EngagementEntity")
    share_t = named("ShareGrantEntity")
    pv_t = named("PortalViewEntity")

    return [
        structure("ClientEntity", [("id", STR), ("name", STR)]),
        structure("LawyerEntity", [("id", STR), ("name", STR), ("firmId", STR), ("barNumber", STR)]),
        structure("FirmEntity", [("id", STR), ("name", STR), ("kind", STR)]),
        structure("CourtEntity", [("id", STR), ("name", STR), ("rulesFramework", STR)]),
        structure("FrameworkEntity", [("id", STR), ("name", STR), ("domain", STR)]),
        structure("CaseEntity", [("id", STR), ("docketNumber", STR), ("practiceArea", STR), ("courtId", STR), ("frameworkId", STR)]),
        structure("EngagementEntity", [("id", STR), ("clientId", STR), ("lawyerId", STR), ("caseId", STR), ("role", STR)]),
        structure("ShareGrantEntity", [("id", STR), ("caseId", STR), ("granterId", STR), ("granteeId", STR), ("capability", STR)]),
        structure("PortalViewEntity", [("id", STR), ("audience", STR), ("route", STR), ("title", STR)]),
        member_string(),
        all_members(),
        distinct_strings(),
        definition("clients", list_t(client_t), lst([record("ClientEntity", id=s(c["id"]), name=s(c["name"])) for c in CLIENTS], client_t)),
        definition(
            "lawyers",
            list_t(lawyer_t),
            lst([record("LawyerEntity", id=s(l["id"]), name=s(l["name"]), firmId=s(l["firmId"]), barNumber=s(l["barNumber"])) for l in LAWYERS], lawyer_t),
        ),
        definition("firms", list_t(firm_t), lst([record("FirmEntity", id=s(f["id"]), name=s(f["name"]), kind=s(f["kind"])) for f in FIRMS], firm_t)),
        definition("courts", list_t(court_t), lst([record("CourtEntity", id=s(c["id"]), name=s(c["name"]), rulesFramework=s(c["rulesFramework"])) for c in COURTS], court_t)),
        definition("frameworks", list_t(fw_t), lst([record("FrameworkEntity", id=s(fw["id"]), name=s(fw["name"]), domain=s(fw["domain"])) for fw in LEGAL_FRAMEWORKS], fw_t)),
        definition(
            "cases",
            list_t(case_t),
            lst(
                [
                    record(
                        "CaseEntity",
                        id=s(k["id"]),
                        docketNumber=s(k["docketNumber"]),
                        practiceArea=s(k["practiceArea"]),
                        courtId=s(k["courtId"]),
                        frameworkId=s(k["frameworkId"]),
                    )
                    for k in CASES
                ],
                case_t,
            ),
        ),
        definition(
            "engagements",
            list_t(eng_t),
            lst(
                [
                    record("EngagementEntity", id=s(e["id"]), clientId=s(e["clientId"]), lawyerId=s(e["lawyerId"]), caseId=s(e["caseId"]), role=s(e["role"]))
                    for e in ENGAGEMENTS
                ],
                eng_t,
            ),
        ),
        definition(
            "shareGrants",
            list_t(share_t),
            lst(
                [
                    record(
                        "ShareGrantEntity",
                        id=s(sh["id"]),
                        caseId=s(sh["caseId"]),
                        granterId=s(sh["granterId"]),
                        granteeId=s(sh["granteeId"]),
                        capability=s(sh["capability"]),
                    )
                    for sh in SHARE_GRANTS
                ],
                share_t,
            ),
        ),
        definition(
            "portalViews",
            list_t(pv_t),
            lst([record("PortalViewEntity", id=s(v["id"]), audience=s(v["audience"]), route=s(v["route"]), title=s(v["title"])) for v in PORTAL_VIEWS], pv_t),
        ),
        field_of_each("clientIds", client_t, "id"),
        field_of_each("lawyerIds", lawyer_t, "id"),
        field_of_each("firmIds", firm_t, "id"),
        field_of_each("courtIds", court_t, "id"),
        field_of_each("frameworkIds", fw_t, "id"),
        field_of_each("caseIds", case_t, "id"),
        field_of_each("engagementIds", eng_t, "id"),
        field_of_each("shareGrantIds", share_t, "id"),
        field_of_each("portalViewIds", pv_t, "id"),
        field_of_each("lawyerFirmIds", lawyer_t, "firmId"),
        field_of_each("caseCourtIds", case_t, "courtId"),
        field_of_each("caseFrameworkIds", case_t, "frameworkId"),
        field_of_each("engClientIds", eng_t, "clientId"),
        field_of_each("engLawyerIds", eng_t, "lawyerId"),
        field_of_each("engCaseIds", eng_t, "caseId"),
        definition(
            "viewsAudienceRouteWellFormed",
            BOOL,
            match_list(
                var("xs"),
                b(True),
                "head",
                "tail",
                if_(
                    if_(
                        eq_string(proj(var("head"), "audience"), s("client")),
                        eq_string(proj(var("head"), "route"), s("client.html")),
                        eq_string(proj(var("head"), "route"), s("lawyer.html")),
                    ),
                    call("viewsAudienceRouteWellFormed", var("tail")),
                    b(False),
                ),
            ),
            parameters=[("xs", list_t(pv_t))],
            recursive="xs",
        ),
        holds("portalClientIdsDistinct", call("distinctStrings", call("clientIds", call("clients")))),
        holds("portalLawyerIdsDistinct", call("distinctStrings", call("lawyerIds", call("lawyers")))),
        holds("portalFirmIdsDistinct", call("distinctStrings", call("firmIds", call("firms")))),
        holds("portalCourtIdsDistinct", call("distinctStrings", call("courtIds", call("courts")))),
        holds("portalFrameworkIdsDistinct", call("distinctStrings", call("frameworkIds", call("frameworks")))),
        holds("portalCaseIdsDistinct", call("distinctStrings", call("caseIds", call("cases")))),
        holds("portalEngagementIdsDistinct", call("distinctStrings", call("engagementIds", call("engagements")))),
        holds("portalShareGrantIdsDistinct", call("distinctStrings", call("shareGrantIds", call("shareGrants")))),
        holds("portalViewIdsDistinct", call("distinctStrings", call("portalViewIds", call("portalViews")))),
        holds("lawyersResolveToFirms", call("allMembers", call("lawyerFirmIds", call("lawyers")), call("firmIds", call("firms")))),
        holds("casesResolveToCourts", call("allMembers", call("caseCourtIds", call("cases")), call("courtIds", call("courts")))),
        holds("casesResolveToFrameworks", call("allMembers", call("caseFrameworkIds", call("cases")), call("frameworkIds", call("frameworks")))),
        holds("engagementsResolveClients", call("allMembers", call("engClientIds", call("engagements")), call("clientIds", call("clients")))),
        holds("engagementsResolveLawyers", call("allMembers", call("engLawyerIds", call("engagements")), call("lawyerIds", call("lawyers")))),
        holds("engagementsResolveCases", call("allMembers", call("engCaseIds", call("engagements")), call("caseIds", call("cases")))),
        holds("clientAndLawyerPortalViewsDisjoint", call("viewsAudienceRouteWellFormed", call("portalViews"))),
    ]


def render_module():
    return lexmod.module("Portal", declarations())


def render_toml():
    lines = [
        'spec = "prism-legal/portal/1"',
        f'charter_id = {json.dumps(PUBLIC_BENEFIT_CHARTER["id"])}',
        f'license = {json.dumps(PUBLIC_BENEFIT_CHARTER["license"])}',
        "",
    ]
    for f in FIRMS:
        lines += ["[[firm]]", f'id = {json.dumps(f["id"])}', f'name = {json.dumps(f["name"])}', f'kind = {json.dumps(f["kind"])}', ""]
    for c in COURTS:
        lines += ["[[court]]", f'id = {json.dumps(c["id"])}', f'name = {json.dumps(c["name"])}', f'rules_framework = {json.dumps(c["rulesFramework"])}', ""]
    for fw in LEGAL_FRAMEWORKS:
        lines += ["[[framework]]", f'id = {json.dumps(fw["id"])}', f'name = {json.dumps(fw["name"])}', f'domain = {json.dumps(fw["domain"])}', ""]
    for cl in CLIENTS:
        lines += ["[[client]]", f'id = {json.dumps(cl["id"])}', f'name = {json.dumps(cl["name"])}', ""]
    for lw in LAWYERS:
        lines += ["[[lawyer]]", f'id = {json.dumps(lw["id"])}', f'name = {json.dumps(lw["name"])}', f'firm_id = {json.dumps(lw["firmId"])}', ""]
    for k in CASES:
        lines += ["[[case]]", f'id = {json.dumps(k["id"])}', f'docket_number = {json.dumps(k["docketNumber"])}', f'practice_area = {json.dumps(k["practiceArea"])}', f'court_id = {json.dumps(k["courtId"])}', f'framework_id = {json.dumps(k["frameworkId"])}', ""]
    for e in ENGAGEMENTS:
        lines += ["[[engagement]]", f'id = {json.dumps(e["id"])}', f'client_id = {json.dumps(e["clientId"])}', f'lawyer_id = {json.dumps(e["lawyerId"])}', f'case_id = {json.dumps(e["caseId"])}', f'role = {json.dumps(e["role"])}', ""]
    for sh in SHARE_GRANTS:
        lines += ["[[share_grant]]", f'id = {json.dumps(sh["id"])}', f'case_id = {json.dumps(sh["caseId"])}', f'granter_id = {json.dumps(sh["granterId"])}', f'grantee_id = {json.dumps(sh["granteeId"])}', f'capability = {json.dumps(sh["capability"])}', ""]
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
        "module": "src/Portal.lex.tex",
        "clients": len(CLIENTS),
        "lawyers": len(LAWYERS),
        "firms": len(FIRMS),
        "courts": len(COURTS),
        "frameworks": len(LEGAL_FRAMEWORKS),
        "cases": len(CASES),
        "engagements": len(ENGAGEMENTS),
        "shareGrants": len(SHARE_GRANTS),
        "changed": changed,
    }


def check():
    if not MODULE.exists() or MODULE.read_text() != render_module():
        return {"ok": False, "reason": "src/Portal.lex.tex drifted; run `bin/prism-legal api sync`"}
    if not REGISTER.exists() or REGISTER.read_text() != render_toml():
        return {"ok": False, "reason": "model/portal.toml drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}

