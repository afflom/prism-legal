"""Mechanized generator of the multi-page Public-Benefit Legal Platform (`view/index.html`,
`view/client.html`, `view/lawyer.html`, `view/courtroom.html`, plus `site/` and `docs/` with `.nojekyll`
for GitHub Pages), SVG visualizations, Markdown sheets, and JSON registers directly from the
verified PrismLegal model."""

import html
import json
import os
import re
import subprocess
from pathlib import Path

from . import (
    ROOT,
    archmodel,
    auditmodel,
    casemodel,
    convertmodel,
    designmodel,
    directexammodel,
    discoverymodel,
    enginemodel,
    intakemodel,
    legalmetamodel,
    observermodel,
    portalmodel,
    presentationmodel,
    standardsmodel,
    supportmodel,
    tunemodel,
    visualmodel,
)

LOGO_PATH = ROOT / "site" / "logo.svg"


def commit_id():
    env_sha = os.environ.get("GITHUB_SHA", "").strip()
    if env_sha:
        return env_sha
    return "HEAD"


def render_logo_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-labelledby="logo-title logo-desc">
  <title id="logo-title">PrismLegal — Public-Benefit Legal Strategy &amp; Evidence Emblem</title>
  <desc id="logo-desc">Architectural legal prism and balanced scales of justice representing open-source evidentiary clarity for clients, legal aid clinics, and trial counsel.</desc>
  <defs>
    <linearGradient id="prism-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b1528"/>
      <stop offset="100%" stop-color="#172b4d"/>
    </linearGradient>
    <linearGradient id="prism-gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fde68a"/>
      <stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
    <linearGradient id="prism-beam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#1e3a8a" stop-opacity="0.12"/>
    </linearGradient>
  </defs>
  <rect width="120" height="120" rx="24" fill="url(#prism-bg)" stroke="#334155" stroke-width="2"/>
  <rect x="7" y="7" width="106" height="106" rx="18" fill="none" stroke="url(#prism-gold)" stroke-width="1" stroke-opacity="0.45"/>
  <polygon points="60,18 102,94 18,94" fill="url(#prism-beam)" stroke="#60a5fa" stroke-width="1.6" stroke-linejoin="round"/>
  <polygon points="60,18 102,94 60,82" fill="#1e3a8a" opacity="0.5"/>
  <line x1="60" y1="26" x2="60" y2="94" stroke="#f8fafc" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="28" y1="48" x2="92" y2="48" stroke="url(#prism-gold)" stroke-width="3.2" stroke-linecap="round"/>
  <path d="M28 48 L20 66 L36 66 Z" fill="none" stroke="#93c5fd" stroke-width="2.2" stroke-linejoin="round"/>
  <path d="M20 66 Q28 73 36 66 Z" fill="url(#prism-gold)"/>
  <path d="M92 48 L84 66 L100 66 Z" fill="none" stroke="#93c5fd" stroke-width="2.2" stroke-linejoin="round"/>
  <path d="M84 66 Q92 73 100 66 Z" fill="url(#prism-gold)"/>
  <circle cx="60" cy="24" r="5" fill="url(#prism-gold)"/>
  <rect x="38" y="92" width="44" height="5.5" rx="2.75" fill="#f8fafc"/>
  <rect x="30" y="98" width="60" height="4" rx="2" fill="url(#prism-gold)"/>
</svg>
"""


def render_schedule_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 290" role="img" aria-labelledby="sched-title sched-desc">
  <title id="sched-title">Annual Parenting Overnights Comparison (Uniform Domestic Relations Act § 402)</title>
  <desc id="sched-desc">Comparison of Respondent's Proposed Equal 50/50 Plan for the Three Minor Children (182.5 overnights each) versus Petitioner's Proposed 90-Overnight Restriction (24.7% Respondent, 75.3% Petitioner).</desc>
  <rect width="820" height="290" rx="12" fill="#0f172a"/>
  <text x="28" y="38" fill="#f8fafc" font-family="Inter, sans-serif" font-size="18" font-weight="700">Statutory Best-Interests Parenting Time (Ages 15, 11 &amp; 6) — Annual Overnights (365 Days)</text>
  <text x="28" y="62" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="13">Respondent's Proposal (Ex. L): Equal 2-2-5-5 Rotation with Seamless Monday/Wednesday School Exchanges</text>
  <rect x="28" y="76" width="380" height="46" rx="6" fill="#15803d"/>
  <rect x="412" y="76" width="380" height="46" rx="6" fill="#1d4ed8"/>
  <text x="218" y="104" text-anchor="middle" fill="#ffffff" font-family="Inter, sans-serif" font-size="14" font-weight="700">Respondent: 182.5 Overnights (50.0%)</text>
  <text x="602" y="104" text-anchor="middle" fill="#ffffff" font-family="Inter, sans-serif" font-size="14" font-weight="700">Petitioner: 182.5 Overnights (50.0%)</text>

  <text x="28" y="162" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="13">Petitioner's Proposal: Restricts Respondent to 90 Overnights/Year + Replaces Available Parent with $2,400/mo After-School Agency (OP Ex. 4)</text>
  <rect x="28" y="176" width="188" height="46" rx="6" fill="#b45309"/>
  <rect x="220" y="176" width="572" height="46" rx="6" fill="#334155"/>
  <text x="122" y="204" text-anchor="middle" fill="#ffffff" font-family="Inter, sans-serif" font-size="13" font-weight="700">90 (24.7%)</text>
  <text x="506" y="204" text-anchor="middle" fill="#f8fafc" font-family="Inter, sans-serif" font-size="14" font-weight="700">Petitioner + Commercial Agency (OP Ex. 4): 275 Overnights (75.3%)</text>

  <text x="28" y="256" fill="#86efac" font-family="Inter, sans-serif" font-size="12.5" font-weight="600">✓ Temporary Orders (Ex. N ¶ 8): Court found NO basis to restrict Respondent's parenting time; parties practiced 50/50 from March 1 to May 1, 2030.</text>
</svg>
"""


def render_support_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 320" role="img" aria-labelledby="sup-title sup-desc">
  <title id="sup-title">Uniform Support Guidelines § 305 &amp; Mandatory Disclosure Comparison</title>
  <desc id="sup-desc">Comparison of Respondent's Guideline Worksheet Ex. N on stipulated baseline ($250.00/mo Petitioner to Respondent) versus Petitioner's imputed worksheet OP Ex. 2 ($2,150.00/mo) and $30,000.00 undisclosed escrow accounts.</desc>
  <rect width="820" height="320" rx="12" fill="#0f172a"/>
  <text x="28" y="38" fill="#f8fafc" font-family="Inter, sans-serif" font-size="18" font-weight="700">Uniform Support Guidelines § 305 &amp; Mandatory Disclosure Comparison</text>

  <rect x="28" y="58" width="370" height="232" rx="10" fill="#111827" stroke="#15803d" stroke-width="2"/>
  <text x="46" y="86" fill="#86efac" font-family="Inter, sans-serif" font-size="15" font-weight="700">Respondent's Guideline Worksheet (Ex. N)</text>
  <text x="46" y="114" fill="#f8fafc" font-family="Inter, sans-serif" font-size="13">• Petitioner Stipulated Income (Ex. B): $8,000/mo (61.54%)</text>
  <text x="46" y="138" fill="#f8fafc" font-family="Inter, sans-serif" font-size="13">• Respondent Stipulated Pension (Ex. E): $5,000/mo (38.46%)</text>
  <text x="46" y="162" fill="#f8fafc" font-family="Inter, sans-serif" font-size="13">• Overnights (Ex. L): 182.5 Respondent / 182.5 Petitioner (50/50)</text>
  <text x="46" y="186" fill="#f8fafc" font-family="Inter, sans-serif" font-size="13">• Childcare &amp; Medical Add-Ons: $0 (38 U.S.C. § 1781 + Parent)</text>
  <rect x="46" y="210" width="334" height="58" rx="8" fill="#14532d"/>
  <text x="213" y="236" text-anchor="middle" fill="#ffffff" font-family="Inter, sans-serif" font-size="14" font-weight="700">Guideline Result: Petitioner Pays $250.00/mo</text>
  <text x="213" y="256" text-anchor="middle" fill="#bbf7d0" font-family="Inter, sans-serif" font-size="12">(Or $0/mo minimum floor · $0 Retroactive Support)</text>

  <rect x="422" y="58" width="370" height="232" rx="10" fill="#111827" stroke="#b45309" stroke-width="2"/>
  <text x="440" y="86" fill="#fdba74" font-family="Inter, sans-serif" font-size="15" font-weight="700">Petitioner's Imputed Worksheet (OP Ex. 2)</text>
  <text x="440" y="114" fill="#f8fafc" font-family="Inter, sans-serif" font-size="13">• Imputes $9,000/mo on top of $5,000 = $14,000/mo</text>
  <text x="440" y="138" fill="#f8fafc" font-family="Inter, sans-serif" font-size="13">• Violates Support Guidelines § 305(5)(b) (100% P&amp;T Bar)</text>
  <text x="440" y="162" fill="#f8fafc" font-family="Inter, sans-serif" font-size="13">• Adds $923/mo Agency (OP Ex. 4) &amp; $180/mo Medical</text>
  <text x="440" y="186" fill="#f8fafc" font-family="Inter, sans-serif" font-size="13">• Omitted $30,000.00 on Initial SFS (Ex. G/H/N)</text>
  <rect x="440" y="210" width="334" height="58" rx="8" fill="#7c2d12"/>
  <text x="607" y="236" text-anchor="middle" fill="#ffffff" font-family="Inter, sans-serif" font-size="14" font-weight="700">Petitioner Demands: Respondent Pay $2,150.00/mo</text>
  <text x="607" y="256" text-anchor="middle" fill="#fed7aa" font-family="Inter, sans-serif" font-size="12">Rebutted by Ex. E, Ex. C/D, Ex. G/H/J &amp; Ex. N ¶¶ 15, 24–26</text>
</svg>
"""


def render_timeline_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 240" role="img" aria-labelledby="tl-title tl-desc">
  <title id="tl-title">Case No. 2030-FAM-9010 Chronological Milestones (2015–2030)</title>
  <desc id="tl-desc">Timeline showing 2015-2025 Public-Sector Service, 2020-2027 Equal Parenting and Solo Care, May 2028 100% P&amp;T Rating, Jan 2030 Incident-Free Separation, Mar-May 2030 50/50 Schedule, Aug 2030 Seminar Completion, and Sep 18, 2030 Evidentiary Hearing.</desc>
  <rect width="860" height="240" rx="12" fill="#0f172a"/>
  <text x="28" y="36" fill="#f8fafc" font-family="Inter, sans-serif" font-size="17" font-weight="700">Chronological Case &amp; Co-Parenting Arc (2015 – September 18, 2030)</text>
  <line x1="45" y1="125" x2="815" y2="125" stroke="#60a5fa" stroke-width="3"/>

  <circle cx="65" cy="125" r="8" fill="#93c5fd"/>
  <text x="65" y="95" text-anchor="middle" fill="#f8fafc" font-family="Inter, sans-serif" font-size="11" font-weight="700">2015–2025</text>
  <text x="65" y="152" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">10 Yrs Service</text>
  <text x="65" y="167" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">2 Overseas Tours</text>

  <circle cx="190" cy="125" r="8" fill="#93c5fd"/>
  <text x="190" y="95" text-anchor="middle" fill="#f8fafc" font-family="Inter, sans-serif" font-size="11" font-weight="700">2020–2027</text>
  <text x="190" y="152" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">Equal Care + 4m</text>
  <text x="190" y="167" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">Solo Caregiving</text>

  <circle cx="315" cy="125" r="8" fill="#fbbf24"/>
  <text x="315" y="95" text-anchor="middle" fill="#fbbf24" font-family="Inter, sans-serif" font-size="11" font-weight="700">May 10, 2028</text>
  <text x="315" y="152" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">100% P&amp;T Rating</text>
  <text x="315" y="167" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">Ex. E ($5,000/m)</text>

  <circle cx="440" cy="125" r="8" fill="#f87171"/>
  <text x="440" y="95" text-anchor="middle" fill="#fca5a5" font-family="Inter, sans-serif" font-size="11" font-weight="700">Initial SFS</text>
  <text x="440" y="152" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">Omitted Escrow</text>
  <text x="440" y="167" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">$30,000 (Ex. G/H)</text>

  <circle cx="565" cy="125" r="8" fill="#86efac"/>
  <text x="565" y="95" text-anchor="middle" fill="#86efac" font-family="Inter, sans-serif" font-size="11" font-weight="700">Jan–May 2030</text>
  <text x="565" y="152" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">0 Incidents;</text>
  <text x="565" y="167" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">Mar–May 50/50</text>

  <circle cx="690" cy="125" r="8" fill="#86efac"/>
  <text x="690" y="95" text-anchor="middle" fill="#86efac" font-family="Inter, sans-serif" font-size="11" font-weight="700">Aug 12, 2030</text>
  <text x="690" y="152" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">Seminar Completed</text>
  <text x="690" y="167" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">30d Early (Ex.M)</text>

  <circle cx="800" cy="125" r="9" fill="#38bdf8"/>
  <text x="800" y="95" text-anchor="middle" fill="#38bdf8" font-family="Inter, sans-serif" font-size="11" font-weight="700">Sep 18, 2030</text>
  <text x="800" y="152" text-anchor="middle" fill="#f8fafc" font-family="Inter, sans-serif" font-size="10.5" font-weight="700">Final Hearing</text>
  <text x="800" y="167" text-anchor="middle" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="10.5">Dept. 12 · 9:30 AM</text>
</svg>
"""


def render_compass_md():
    lines = [
        "# Opening Statement & Testimony Compass — Case No. 2030-FAM-9010",
        "",
        f"**Hearing:** {casemodel.CASE_META['hearingTitle']} · **{casemodel.CASE_META['hearingDate']} at {casemodel.CASE_META['hearingTime']}** · `{casemodel.CASE_META['division']}`",
        "**Minor Beneficiaries:** Three Minor Children (Ages 15, 11, and 6)",
        "",
        "> **Core Trial Theme:** *\"Children thrive when they do not have to choose between two capable, loving parents. Petitioner is a dedicated parent and a skilled regional operations manager. Our three children thrive when they have equal time with both of us.\"*",
        "",
    ]
    for p in casemodel.OPENING_PILLARS:
        lines += [
            f"## {p['id']}: {p['title']}",
            f"- **Statutory Focus:** `{p['theme']}`",
            f"- **Supporting Exhibits:** {', '.join(f'`{x}`' for x in p['exhibits'])}",
            f"- **Summary:** {p['summary']}",
            f"- **Anchor Quote:** *\"{p['verbatimQuote']}\"*",
            "- **DO on the Witness Stand:**",
        ]
        for r in p["doRules"]:
            lines.append(f"  - {r}")
        lines.append("- **DO NOT on the Witness Stand:**")
        for r in p["dontRules"]:
            lines.append(f"  - {r}")
        lines.append("")
    return "\n".join(lines)


def render_factors_md():
    lines = [
        "# Statutory Best-Interests & Decision-Making Matrix (Minor Children, Ages 15, 11 & 6)",
        "",
        "| Factor | Statutory Provision | Respondent's Position (50/50 & Joint) | Petitioner's Position (90 Overnights & Sole) | Trial Proof & Exhibits |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for f in casemodel.STATUTORY_FACTORS:
        lines.append(
            f"| **{f['title']}** | `{f['statute']}` | {f['fatherPosition']} | {f['motherPosition']} | {f['trialProof']} ({', '.join(f'`{x}`' for x in f['exhibits'])}) |"
        )
    lines.append("")
    return "\n".join(lines)


def render_remedies_md():
    fl = casemodel.FINANCIAL_LEDGER
    fp = fl["fatherProposal"]
    mp = fl["motherProposal"]
    da = fl["disclosureAudit"]
    lines = [
        "# Uniform Support Guidelines § 305, 38 U.S.C. § 1781 Coverage & Mandatory Disclosure Audit",
        "",
        "## 1. Side-by-Side Support Worksheet Comparison",
        "",
        "| Line Item | Respondent's Guideline Worksheet (`Ex. N`) | Petitioner's Imputed Worksheet (`OP Ex. 2`) | Statutory / Evidentiary Proof |",
        "| :--- | :--- | :--- | :--- |",
        f"| **Petitioner Gross Monthly Income** | `${fp['motherGrossMonthly']:,.2f}/mo` (`$96,000/yr`) | `${mp['motherGrossMonthly']:,.2f}/mo` | Stipulated in `Pretrial Order § IV` & `Ex. B` (1.0 FTE Regional Operations Manager) |",
        f"| **Respondent Gross Monthly Income** | `${fp['fatherGrossMonthly']:,.2f}/mo` (100% P&T) | `${mp['fatherImputedMonthly']:,.2f}/mo` (Imputed) | Stipulated 100% P&T disabled (`Ex. E`). Imputation barred by `§ 305(5)(b)` & `Ex. N ¶ 15` |",
        f"| **Combined Monthly Income** | `${fp['combinedMonthly']:,.2f}/mo` | `${mp['combinedMonthly']:,.2f}/mo` | Actual combined baseline is `$13,000/mo` (Petitioner `61.54%`, Respondent `38.46%`) |",
        f"| **Overnights (365 Days)** | `{fp['fatherOvernights']}` Respondent / `{fp['motherOvernights']}` Petitioner (`50/50`) | `{mp['fatherOvernights']}` Respondent / `{mp['motherOvernights']}` Petitioner (`24.7%`) | `Ex. L` 2-2-5-5 rotation vs. Petitioner's proposed restriction |",
        f"| **Work-Related Childcare** | `${fp['childcareAdjustment']:,.2f}/mo` | `${mp['childcareAdjustment']:,.2f}/mo` (`$2,400/mo` quote) | `OP Ex. 4` is an unsworn estimate; Respondent is available full-time for `$0` during regional travel shifts |",
        f"| **Health Insurance Add-On** | `${fp['healthInsuranceAdjustment']:,.2f}/mo` | `${mp['healthInsuranceAdjustment']:,.2f}/mo` | All three minor children have **zero-premium medical coverage via 38 U.S.C. § 1781 (`Ex. E`)** |",
        f"| **Net Monthly Guideline Transfer** | **Petitioner pays Respondent `${fp['netMonthlyTransfer']:,.2f}/mo`** | Petitioner demands Respondent pay `${mp['netMonthlyTransfer']:,.2f}/mo` | `Ex. N` (or `$0/mo` minimum floor) |",
        "",
        "## 2. FRCP 26(e) / Rule 16.2 Mandatory Financial Disclosure Audit",
        "",
        f"- **Rule:** `{da['rule']}`",
        f"- **Petitioner's Initial SFS (`{da['motherJuly2025SfsExhibit']}`):** Disclosed `${da['motherJuly2025DisclosedBankTotal']:,.2f}` in Escrow Checking `x4102` and Savings `x4109`.",
        f"- **Subpoenaed Bank Statements (`Ex. H`):** Proved Petitioner held **`${da['motherActualReserveBalances']:,.2f}`** across those accounts while inducing the interim expense stipulation.",
        f"- **Petitioner's Amended SFS (`{da['motherApril2026SfsExhibit']}`):** First disclosed the accounts with `${da['motherApril2026DisclosedBankTotal']:,.2f}` remaining.",
        f"- **Temporary Orders Judicial Finding (`Ex. N ¶¶ 24–26`):** {da['temporaryOrdersFinding']}",
        "",
    ]
    return "\n".join(lines)


def render_pivots_md():
    lines = [
        "# Cross-Examination Pivot Cards (`TRAP-01` – `TRAP-16`)",
        "",
        "Prepared for Client Litigant (Respondent) & Lead Trial Counsel.",
        "",
    ]
    for t in auditmodel.TRAPS:
        lines += [
            f"## {t['id']}: {t['title']} [`{t['status']}`]",
            f"- **Category:** `{t['category']}` · **Statutory Anchor:** `{t['statutoryAnchor']}`",
            f"- **Opposing Exhibits:** {', '.join(f'`{x}`' for x in t['opposingExhibits']) or 'None'}",
            f"- **Rebuttal Exhibits:** {', '.join(f'`{x}`' for x in t['rebuttalExhibits'])}",
            f"- **Opposing Allegation:** {t['allegation']}",
            f"- **⚠️ Trap Warning (What NOT to do):** {t['trapWarning']}",
            f"- **✅ Calm Opening-Aligned Response (Say This):** *\"{t['openingAlignedPivot']}\"*",
            "",
        ]
    return "\n".join(lines)


def render_witnesses_md():
    lines = [
        "# Trial Witness Examination Sheets (`W-01` – `W-10`)",
        "",
        "Prepared for Case No. 2030-FAM-9010 Evidentiary Hearing (September 18, 2030 at 9:30 a.m.).",
        "",
    ]
    for w in casemodel.WITNESSES:
        lines += [
            f"## {w['id']}: {w['name']} ({w['relationship']})",
            f"- **Party Listing:** `{w['party']}` · **Call Status:** `{w['callStatus']}`",
            f"- **Expected Testimony Scope:** {w['scope']}",
            "- **Examination / Cross-Examination Key Points:**",
        ]
        for pt in w["keyPoints"]:
            lines.append(f"  - {pt}")
        lines.append("")
    return "\n".join(lines)


def render_client_guide_md():
    tuning = tunemodel.load_state()
    lines = [
        "# Client Strategy Understanding, Testimony Rehearsal & Counsel Co-Design Guide",
        "",
        "**Client:** Respondent (Client Litigant) · **Lead Trial Counsel:** Lead Domestic Relations Trial Counsel (Civic Justice & Trial Advocacy LLP)  ",
        "**Minor Beneficiaries:** Three Minor Children (Ages 15, 11, and 6)  ",
        f"**Hearing:** {casemodel.CASE_META['hearingTitle']} · **{casemodel.CASE_META['hearingDate']} at {casemodel.CASE_META['hearingTime']}**",
        "",
        "## 1. How Your Case Strategy Connects (The 3 Relief Goals for the Minor Children)",
        "",
        "1. **Equal 50/50 Parenting Time (`Ex. L` — 182.5 Overnights Each):** Proven by your 10-year service record, equal hands-on care (2020–2027), 4 months solo caregiving during out-of-state corporate fellowship, full-time availability via 100% P&T disability (`Ex. E`), the successful March 1–May 1, 2030 50/50 schedule, and Temporary Orders finding no basis to restrict parenting time (`Ex. N ¶ 8`).",
        "2. **Joint Major Decision-Making with Mediation First (`Ex. L`):** Proven by mutual pre-separation stress (`Ex. K`), Petitioner's admission that no emergency report was ever required, the stipulated dismissal of the Nov 2029 temporary civil standby order (`Ex. J`), 8 incident-free months since Jan 2030 separation, early seminar completion (`Ex. M`), and polite co-parenting messages (`Ex. O`).",
        "3. **Guideline Support (`Ex. N` — Petitioner Pays `$250.00/mo`) & `$0` Retroactive Support:** Proven by stipulated baseline (`$8,000/mo` Petitioner `Ex. B`, `$5,000/mo` Respondent `Ex. E`), `§ 305(5)(b)` disability protection, `$0` open-source research draw (`Ex. D`), free 38 U.S.C. § 1781 medical coverage (`Ex. E`), free parental care during regional shifts, and Petitioner's `$30,000.00` escrow omission (`Ex. G/H/J`, `Ex. N ¶¶ 24–26`).",
        "",
        "## 2. Active Client–Counsel Strategy Agenda",
        "",
    ]
    for item in tuning["agenda"]:
        lines += [
            f"### {item['id']} [{item['status']}] — {item['category']} (Focus: `{item['targetId']}`)",
            f"- **Raised By:** {item['author']}",
            f"- **Strategy Question / Focus:** {item['questionForLawyer']}",
            f"- **Counsel Guidance:** {item['lawyerGuidance']}",
            "",
        ]
    return "\n".join(lines)


def render_lawyer_tuner_md():
    tuning = tunemodel.load_state()
    lines = [
        "# Trial Counsel Case Engineering, FRE Evidentiary Audit & Trial Brief",
        "",
        "**Lead Trial Counsel:** Lead Domestic Relations Trial Counsel · **Client:** Respondent (Client Litigant)  ",
        "**Minor Beneficiaries:** Three Minor Children (Ages 15, 11, and 6)",
        "",
        "## 1. Case Strategy & Evidentiary Tuning Dimensions",
        "",
        "| Dimension | Owner ↔ Collaborator | Title & Scope |",
        "| :--- | :--- | :--- |",
    ]
    for d in tuning["dimensions"]:
        lines.append(
            f"| `{d['id']}` | `{d['owner']}` ↔ `{d['collaborator']}` | **{d['title']}** — {d['description']} |"
        )
    lines += [
        "",
        "## 2. Case Claims & Evidentiary Chain (`CLM-01` – `CLM-24`)",
        "",
        "| Claim ID | Status | Statutory Anchor | Statement | Exhibits | Depends On |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for c in casemodel.CLAIMS:
        lines.append(
            f"| `{c['id']}` | `{c['status']}` | `{c['statutory']}` | {c['statement']} | {', '.join(f'`{x}`' for x in c['exhibits'])} | {', '.join(f'`{x}`' for x in c['depends']) or '—'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_direct_exam_md():
    lines = [
        "# Lead Trial Counsel's Intended Direct Examination of Respondent (`DX-001` – `DX-036`)",
        "",
        "**Structure:** 6 Chapters · 36 Q&A Blocks · 14 Yellow-Highlighted Priority Blocks · 14 Exhibit Admission Moves · 3 Red Stricken Blocks  ",
        "**Trial Counsel:** Lead Domestic Relations Trial Counsel · **Witness:** Respondent (Client Litigant)  ",
        "**Minor Beneficiaries:** Three Minor Children (Ages 15, 11, and 6)",
        "",
    ]
    for ch in directexammodel.DIRECT_EXAM_CHAPTERS:
        lines += [
            f"## {ch['id']}: {ch['title']} ({ch['pageRange']})",
            f"- **Opening Pillar:** `{ch['pillarId']}` · **Statutory Factor:** `{ch['statutoryId']}` · **Exhibits Admitted:** {', '.join(f'`{x}`' for x in ch['exhibitsAdmitted']) or 'None'}",
            f"- **Chapter Summary:** {ch['summary']}",
            "",
        ]
        qs = [q for q in directexammodel.DIRECT_EXAM_QUESTIONS if q["chapterId"] == ch["id"]]
        for q in qs:
            cue = f" · **[{q['visualCue'].upper()}]**" if q["visualCue"] != "standard" else ""
            adm = f" · **[MOVE TO ADMIT `{q['exhibitId']}`]**" if q["movesToAdmit"] else ""
            lines += [
                f"### {q['id']} (p. {q['page']} · `{q['statutoryId']}` · `{q['exhibitId']}`){cue}{adm}",
                f"- **Q (Lead Trial Counsel):** {q['question']}",
                f"- **Counsel Script Prompt:** {q['counselPrompt']}",
                f"- **✅ Full Opening-Aligned Answer:** *\"{q['fullTestimony']}\"*",
                f"- **💡 Coaching Note:** {q['coachingNote']}",
                "",
            ]
    return "\n".join(lines)


def render_visual_evidence_md():
    lines = [
        "# Handwritten, Visual & 30-Exhibit Content-Meaning / Intent Matrix",
        "",
        "Prepared for Case No. 2030-FAM-9010 Evidentiary Hearing (September 18, 2030 at 9:30 a.m.).",
        "",
        "## 1. Visual & Scanned Exhibit Forensic Extractions (`VIS-01` – `VIS-12`)",
        "",
        "| ID | Exhibit | Modality | Pages | Handwritten / Visual Details | Evidentiary Significance & Trial Pivot |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for v in visualmodel.VISUAL_FORENSIC_RECORDS:
        lines.append(
            f"| `{v['id']}` | `{v['exhibitId']}` | `{v['modality']}` | `{v['pageCount']}` | {v['handwrittenDetails']} | **{v['evidentiarySignificance']}** — *Pivot:* {v['trialPivot']} |"
        )
    lines += [
        "",
        "## 2. `OP Ex. 13` Handwritten Study Log `FRE 106` Completeness Register (`DIARY-01` – `DIARY-08`)",
        "",
        "| ID | Date & Pages | Handwritten Excerpt | Opposing Cherry-Pick | `FRE 106` Completeness Rebuttal |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for d in visualmodel.HANDWRITTEN_DIARY_ENTRIES:
        lines.append(
            f"| `{d['id']}` | `{d['entryDate']}` ({d['pageRange']}) | *\"{d['handwrittenExcerpt']}\"* | {d['motherCherryPick']} | {d['fullContextRebuttal']} |"
        )
    lines += [
        "",
        "## 3. Photographic Page Catalog (`PHOTO-01` – `PHOTO-12` across `Ex. E`, `Ex. O` & `Ex. L`)",
        "",
        "| ID | Exhibit & Page | Subjects & Setting | Visual Description | Statutory Factor |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for p in visualmodel.PHOTO_PAGE_CATALOG:
        lines.append(
            f"| `{p['id']}` | `{p['exhibitId']}` p. {p['pageNumber']} | {p['subjects']} ({p['setting']}) | {p['visualDescription']} | `{p['statutoryFactorId']}` |"
        )
    lines += [
        "",
        "## 4. Complete 30-Exhibit Content-Meaning & Proponent-Intent Matrix (`MAP-Ex-A` – `MAP-OP-Ex-15`)",
        "",
        "| Mapping ID | Exhibit | Proponent | Modality | Content Meaning | Contextual Meaning | Proponent Intent | Trial Pivot Intent |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for m in visualmodel.EXHIBIT_SEMANTIC_MAPPINGS:
        lines.append(
            f"| `{m['id']}` | `{m['exhibitId']}` | `{m['proponent']}` | `{m['modality']}` | {m['contentMeaning']} | {m['contextualMeaning']} | {m['proponentTrialIntent']} | {m['trialPivotIntent']} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_payload():
    """Single-context JSON payload embedded across the portal pages and written to `register.json`."""
    resp_exhibits = [{**e, "fileUrl": "sheets/visual-evidence-and-intent-matrix.md"} for e in casemodel.RESPONDENT_EXHIBITS]
    pet_exhibits = [{**e, "fileUrl": "sheets/visual-evidence-and-intent-matrix.md"} for e in casemodel.PETITIONER_EXHIBITS]

    return {
        "caseMeta": casemodel.CASE_META,
        "children": casemodel.CHILDREN,
        "openingPillars": casemodel.OPENING_PILLARS,
        "statutoryFactors": casemodel.STATUTORY_FACTORS,
        "financialLedger": casemodel.FINANCIAL_LEDGER,
        "claims": casemodel.CLAIMS,
        "respondentExhibits": resp_exhibits,
        "petitionerExhibits": pet_exhibits,
        "witnesses": casemodel.WITNESSES,
        "traps": auditmodel.TRAPS,
        "timeline": casemodel.TIMELINE,
        "stakeholders": archmodel.STAKEHOLDERS,
        "concerns": archmodel.CONCERNS,
        "viewpoints": archmodel.VIEWPOINTS,
        "views": archmodel.VIEWS,
        "qualityMeasures": archmodel.MEASURES,
        "trialRisks": archmodel.TRIAL_RISKS,
        "tuningParameters": archmodel.TUNING_PARAMETERS,
        "tuningState": tunemodel.load_state(),
        "quadruples": observermodel.QUADRUPLES,
        "brand": presentationmodel.BRAND,
        "portalPages": presentationmodel.PORTAL_PAGES,
        "panels": presentationmodel.PANELS,
        "journeys": presentationmodel.JOURNEYS,
        "tokens": presentationmodel.TOKENS,
        "contrastPairs": designmodel.contrast_pairs(),
        "typeScale": designmodel.TYPE_SCALE,
        "spacingScale": designmodel.SPACING,
        "motion": designmodel.MOTION,
        "worksheets": supportmodel.WORKSHEETS,
        "disclosureAudit": supportmodel.DISCLOSURE_AUDIT,
        "taxHistory": supportmodel.TAX_HISTORY,
        "standards": standardsmodel.rows(),
        "legalMeta": {
            "hohfeldPositions": legalmetamodel.HOHFELD_POSITIONS,
            "hohfeldRelations": legalmetamodel.HOHFELD_RELATIONS,
            "legalRules": legalmetamodel.LEGAL_RULES,
            "superiorityOverrides": legalmetamodel.SUPERIORITY_OVERRIDES,
            "arguments": legalmetamodel.ARGUMENTS,
            "attacks": legalmetamodel.ATTACKS,
            "aknDocuments": legalmetamodel.AKN_DOCUMENTS,
            "chainOfCustody": legalmetamodel.CHAIN_OF_CUSTODY,
        },
        "portal": {
            "charter": portalmodel.PUBLIC_BENEFIT_CHARTER,
            "authProviders": portalmodel.AUTH_PROVIDERS,
            "shareGrants": portalmodel.SHARE_GRANTS,
            "firms": portalmodel.FIRMS,
            "courts": portalmodel.COURTS,
            "frameworks": portalmodel.LEGAL_FRAMEWORKS,
            "clients": portalmodel.CLIENTS,
            "lawyers": portalmodel.LAWYERS,
            "cases": portalmodel.CASES,
            "engagements": portalmodel.ENGAGEMENTS,
            "portalViews": portalmodel.PORTAL_VIEWS,
            "counterpartyProfiles": portalmodel.COUNTERPARTY_PROFILES,
        },
        "directExam": {
            "visualCues": directexammodel.VISUAL_CUES,
            "chapters": directexammodel.DIRECT_EXAM_CHAPTERS,
            "questions": directexammodel.DIRECT_EXAM_QUESTIONS,
        },
        "visualEvidence": {
            "diaryEntries": visualmodel.HANDWRITTEN_DIARY_ENTRIES,
            "visualForensics": visualmodel.VISUAL_FORENSIC_RECORDS,
            "photoPages": visualmodel.PHOTO_PAGE_CATALOG,
            "semanticMappings": visualmodel.EXHIBIT_SEMANTIC_MAPPINGS,
        },
        "convertPropositions": convertmodel.compiled_fixtures(),
        "strategyEngine": {
            "workload": {
                "hearing": enginemodel.WORKLOAD["hearing"],
                "courtroom": enginemodel.WORKLOAD["courtroom"],
                "tickBudget": enginemodel.WORKLOAD["tickBudget"],
                "gateMinimum": enginemodel.WORKLOAD["gateMinimum"],
                "stages": [
                    {"id": s_id, "minutes": mins, "isGate": is_gate}
                    for s_id, mins, is_gate in enginemodel.WORKLOAD["stages"]
                ],
            },
            "portfolio": enginemodel.PORTFOLIO,
            "schedules": [
                {
                    "family": fam,
                    "orderedStrategies": enginemodel.Mirror.schedule(
                        enginemodel.default_committed_table(), fam, [p["id"] for p in enginemodel.PORTFOLIO]
                    ),
                }
                for fam in enginemodel.FAMILIES
            ],
        },
        "evidentiaryDiscovery": {
            "claimRelations": [
                {"claimId": cid, "columns": cols} for cid, cols in discoverymodel.REGISTER_CLAIM_RELATIONS
            ],
            "recurrences": discoverymodel.RECURRENCE_FIXTURES,
        },
        "intakeClassifier": {
            "featureDim": intakemodel.FEATURE_DIM,
            "maxChannel": intakemodel.MAX_CHANNEL,
            "numDomainClasses": intakemodel.NUM_DOMAIN_CLASSES,
            "featureChannels": intakemodel.FEATURE_CHANNELS,
            "schemaClassifiers": intakemodel.SCHEMA_CLASSIFIERS,
            "attentionHeads": intakemodel.NODE_ATTENTION_HEADS,
            "fixtures": intakemodel.INTAKE_FIXTURES,
        },
        "pedagogyGuides": presentationmodel.PEDAGOGY_GUIDES,
        "publication": presentationmodel.PUBLICATION,
        "commit": commit_id(),
    }


def _shared_css():
    return """
    :root, [data-theme="light"] {
      --bg: #f6f5f0;
      --surface: #ffffff;
      --surface-alt: #efede6;
      --ink: #0c1526;
      --muted: #3b485e;
      --accent: #162d59;
      --accent-soft: #e0e8f6;
      --brass: #92400e;
      --brass-soft: #fef3c7;
      --stipulated: #134e2a;
      --stipulated-bg: #dcfce7;
      --warning: #7c2d12;
      --warning-bg: #ffedd5;
      --danger: #7f1d1d;
      --danger-bg: #fee2e2;
      --border: #cfc9bc;
      --border-strong: #94a3b8;
      --focus: #1d4ed8;
      --shadow: 0 2px 12px rgba(12, 21, 38, 0.06), 0 1px 2px rgba(12, 21, 38, 0.04);
      --shadow-elevated: 0 8px 24px rgba(12, 21, 38, 0.09);
      --font-scale: 1;
      --serif: "Charter", "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
      --sans: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    [data-theme="dark"] {
      --bg: #080d17;
      --surface: #0f172a;
      --surface-alt: #182338;
      --ink: #f1f5f9;
      --muted: #cbd5e1;
      --accent: #93c5fd;
      --accent-soft: #1e3a8a;
      --brass: #fbbf24;
      --brass-soft: #3b2506;
      --stipulated: #86efac;
      --stipulated-bg: #14532d;
      --warning: #fdba74;
      --warning-bg: #431407;
      --danger: #fca5a5;
      --danger-bg: #450a0a;
      --border: #2a3950;
      --border-strong: #475569;
      --focus: #60a5fa;
      --shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
      --shadow-elevated: 0 12px 32px rgba(0, 0, 0, 0.65);
    }
    [data-stand-mode="true"] {
      --font-scale: 1.18;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: var(--sans);
      font-size: calc(16px * var(--font-scale));
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }
    h1, h2, h3, .serif-heading {
      font-family: var(--serif);
      letter-spacing: -0.015em;
      line-height: 1.28;
      color: var(--ink);
    }
    code, pre, .tabular, .kpi-val, #court-timer-readout {
      font-variant-numeric: tabular-nums;
    }
    a { color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }
    a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible, summary:focus-visible {
      outline: 3px solid var(--focus);
      outline-offset: 2px;
    }
    .skip-link {
      position: absolute;
      left: -9999px;
      top: 8px;
      background: var(--accent);
      color: #fff;
      padding: 8px 16px;
      border-radius: 6px;
      z-index: 1000;
    }
    .skip-link:focus { left: 12px; }
    /* Institutional Legal Command Bar */
    header.portal-header {
      background: var(--surface);
      border-top: 4px solid var(--accent);
      border-bottom: 1.5px solid var(--border);
      padding: 11px 24px;
      position: sticky;
      top: 0;
      z-index: 60;
      box-shadow: var(--shadow);
    }
    .header-inner {
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }
    .brand-row {
      display: flex;
      align-items: center;
      gap: 13px;
      text-decoration: none;
      color: inherit;
    }
    .brand-logo { width: 42px; height: 42px; flex-shrink: 0; border-radius: 10px; box-shadow: 0 2px 6px rgba(12, 21, 38, 0.16); }
    .brand-logo svg { width: 100%; height: 100%; display: block; }
    .brand-title-row {
      display: flex;
      align-items: center;
      gap: 9px;
      flex-wrap: wrap;
    }
    .brand-title {
      margin: 0;
      font-family: var(--serif);
      font-size: calc(1.26rem * var(--font-scale));
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--ink);
    }
    .brand-pill {
      font-family: var(--sans);
      font-size: calc(0.68rem * var(--font-scale));
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 2px 9px;
      border-radius: 4px;
      background: var(--brass-soft);
      color: var(--brass);
      border: 1px solid rgba(146, 64, 14, 0.25);
    }
    .brand-sub {
      margin: 1px 0 0;
      font-size: calc(0.76rem * var(--font-scale));
      color: var(--muted);
      max-width: 440px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .portal-nav-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      align-items: center;
      background: var(--surface-alt);
      padding: 4px;
      border-radius: 10px;
      border: 1px solid var(--border);
    }
    .nav-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: transparent;
      color: var(--muted);
      border: 1px solid transparent;
      padding: 6px 13px;
      border-radius: 7px;
      font-size: calc(0.84rem * var(--font-scale));
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      transition: background 0.15s ease, color 0.15s ease, box-shadow 0.15s ease;
    }
    .nav-pill:hover {
      background: var(--surface);
      color: var(--ink);
    }
    .nav-pill.active {
      background: var(--accent);
      color: var(--bg);
      border-color: var(--accent);
      box-shadow: 0 1px 4px rgba(12, 21, 38, 0.2);
    }
    .header-utilities {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }
    .header-matter-Cluster {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 4px 10px;
      font-size: calc(0.78rem * var(--font-scale));
      font-weight: 700;
    }
    .header-matter-Cluster select {
      border: none;
      background: transparent;
      color: var(--ink);
      font-weight: 700;
      font-size: calc(0.8rem * var(--font-scale));
      max-width: 220px;
      cursor: pointer;
    }
    .btn.primary, .btn[aria-pressed="true"] {
      background: var(--accent);
      color: var(--bg);
      border-color: var(--accent);
      box-shadow: 0 1px 3px rgba(12, 21, 38, 0.16);
    }
    .btn {
      background: var(--surface);
      color: var(--ink);
      border: 1px solid var(--border);
      padding: 7px 14px;
      border-radius: 7px;
      font-size: calc(0.84rem * var(--font-scale));
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background 0.12s ease, border-color 0.12s ease, transform 0.08s ease;
    }
    .btn:hover { background: var(--surface-alt); border-color: var(--border-strong); }
    .btn.primary:hover { filter: brightness(1.08); background: var(--accent); }
    .btn.danger-btn {
      color: var(--danger);
      border-color: var(--danger);
      background: transparent;
      padding: 4px 10px;
      font-size: calc(0.78rem * var(--font-scale));
    }
    .container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 20px 24px 72px;
    }
    /* Active Matter Context Bar */
    .matter-bar {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 5px solid var(--accent);
      border-radius: 10px;
      padding: 12px 18px;
      margin-bottom: 16px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      box-shadow: var(--shadow);
    }
    .matter-bar-left, .matter-bar-right, .matter-bar-controls {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }
    .matter-bar-info {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .matter-bar-title {
      font-family: var(--serif);
      font-size: calc(1.06rem * var(--font-scale));
      font-weight: 800;
    }
    .matter-bar-meta {
      font-size: calc(0.82rem * var(--font-scale));
      color: var(--muted);
    }
    /* Formal Court Pleading Caption Masthead */
    .court-caption-masthead {
      background: var(--surface);
      border: 1.5px solid var(--border-strong);
      border-top: 4px solid var(--accent);
      border-radius: 8px;
      margin: 12px 0 14px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }
    .court-caption-header {
      background: var(--surface-alt);
      border-bottom: 1.5px solid var(--border);
      padding: 9px 16px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      font-family: var(--serif);
      font-weight: 800;
      font-size: calc(0.92rem * var(--font-scale));
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--ink);
    }
    .court-caption-grid {
      display: grid;
      grid-template-columns: 1.35fr 1fr;
    }
    @media (max-width: 760px) {
      .court-caption-grid { grid-template-columns: 1fr; }
    }
    .court-caption-parties {
      padding: 14px 18px;
      border-right: 2px double var(--border-strong);
      font-family: var(--serif);
      font-size: calc(0.95rem * var(--font-scale));
      line-height: 1.48;
    }
    @media (max-width: 760px) {
      .court-caption-parties { border-right: none; border-bottom: 1.5px solid var(--border); }
    }
    .court-caption-docket {
      padding: 14px 18px;
      font-family: var(--mono);
      font-size: calc(0.8rem * var(--font-scale));
      line-height: 1.65;
      background: rgba(15, 23, 42, 0.015);
    }
    .court-caption-theme {
      padding: 11px 18px;
      border-top: 1px solid var(--border);
      background: var(--surface-alt);
      font-size: calc(0.9rem * var(--font-scale));
    }
    /* Five-Pole Guided Journey Stepper */
    nav.journey-stepper {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 18px;
    }
    @media (max-width: 960px) {
      nav.journey-stepper { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 560px) {
      nav.journey-stepper { grid-template-columns: 1fr; }
    }
    .step-tab {
      background: var(--surface);
      color: var(--ink);
      border: 1.5px solid var(--border);
      border-top: 3px solid var(--border-strong);
      border-radius: 9px;
      padding: 11px 13px;
      text-align: left;
      cursor: pointer;
      display: flex;
      align-items: flex-start;
      gap: 10px;
      box-shadow: var(--shadow);
      transition: border-color 0.15s ease, background 0.15s ease, transform 0.1s ease;
    }
    .step-tab:hover { background: var(--surface-alt); border-color: var(--accent); }
    .step-tab[aria-selected="true"] {
      background: var(--accent);
      color: var(--bg);
      border-color: var(--accent);
      border-top-color: var(--brass);
      box-shadow: var(--shadow-elevated);
    }
    .step-num {
      width: 26px;
      height: 26px;
      border-radius: 6px;
      background: var(--accent-soft);
      color: var(--ink);
      font-family: var(--mono);
      font-weight: 800;
      font-size: calc(0.8rem * var(--font-scale));
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      margin-top: 1px;
    }
    .step-tab[aria-selected="true"] .step-num {
      background: var(--bg);
      color: var(--accent);
    }
    .step-title {
      display: block;
      font-family: var(--serif);
      font-size: calc(0.93rem * var(--font-scale));
      font-weight: 800;
      line-height: 1.25;
    }
    .step-sub {
      display: block;
      font-size: calc(0.75rem * var(--font-scale));
      opacity: 0.86;
      margin-top: 2px;
      line-height: 1.25;
    }
    /* Contextual Pedagogy Guide Banner */
    .pedagogy-banner {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 5px solid var(--stipulated);
      border-radius: 9px;
      padding: 13px 18px;
      margin-bottom: 16px;
      box-shadow: var(--shadow);
    }
    .pedagogy-banner-top {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .pedagogy-tip {
      margin: 5px 0 0;
      font-size: calc(0.9rem * var(--font-scale));
      color: var(--ink);
    }
    .pedagogy-details {
      margin-top: 6px;
      font-size: calc(0.84rem * var(--font-scale));
      color: var(--muted);
    }
    .pedagogy-details summary {
      cursor: pointer;
      font-weight: 700;
      color: var(--accent);
      user-select: none;
    }
    /* Progressive Disclosure Action Drawers */
    details.action-drawer {
      background: var(--surface-alt);
      border: 1.5px solid var(--border);
      border-radius: 9px;
      padding: 10px 15px;
      margin-top: 12px;
    }
    details.action-drawer > summary {
      cursor: pointer;
      font-weight: 700;
      font-size: calc(0.9rem * var(--font-scale));
      color: var(--ink);
      display: flex;
      align-items: center;
      justify-content: space-between;
      list-style: none;
      user-select: none;
    }
    details.action-drawer > summary::-webkit-details-marker { display: none; }
    details.action-drawer > summary::after {
      content: "+ Open Form";
      font-size: calc(0.75rem * var(--font-scale));
      padding: 3px 10px;
      border-radius: 5px;
      background: var(--accent);
      color: var(--bg);
    }
    details.action-drawer[open] > summary {
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
    }
    details.action-drawer[open] > summary::after {
      content: "− Close";
      background: var(--surface);
      color: var(--ink);
      border: 1px solid var(--border);
    }
    .preset-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      padding: 10px 12px;
      background: var(--surface-alt);
      border: 1px dashed var(--border);
      border-radius: 8px;
      margin-bottom: 12px;
    }
    .finding-box {
      background: var(--stipulated-bg);
      color: var(--stipulated);
      border-left: 4px solid var(--stipulated);
      padding: 9px 13px;
      border-radius: 6px;
      font-size: calc(0.84rem * var(--font-scale));
      margin-top: 8px;
    }
    .refusal-box {
      background: var(--danger-bg);
      color: var(--danger);
      border-left: 4px solid var(--danger);
      padding: 9px 13px;
      border-radius: 6px;
      font-size: calc(0.84rem * var(--font-scale));
      margin-top: 8px;
    }
    .workspace-section { display: none; }
    .workspace-section.active { display: block; }
    .step-footer {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-top: 22px;
      padding: 16px 20px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      box-shadow: var(--shadow);
    }
    .kpi-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }
    .kpi-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 5px solid var(--accent);
      border-radius: 9px;
      padding: 13px 16px;
      box-shadow: var(--shadow);
    }
    .kpi-card.stip { border-left-color: var(--stipulated); }
    .kpi-card.warn { border-left-color: var(--warning); }
    .kpi-label { font-size: calc(0.73rem * var(--font-scale)); text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); font-weight: 700; }
    .kpi-val { font-family: var(--serif); font-size: calc(1.18rem * var(--font-scale)); font-weight: 800; margin: 4px 0 2px; }
    .kpi-note { font-size: calc(0.8rem * var(--font-scale)); color: var(--muted); }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 16px; }
    .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 16px; }
    .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 12px; }
    @media (max-width: 640px) {
      .grid-2, .grid-3, .form-grid { grid-template-columns: 1fr; }
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px 22px;
      box-shadow: var(--shadow);
      margin-bottom: 18px;
    }
    .card h2 { margin-top: 0; margin-bottom: 6px; font-size: calc(1.26rem * var(--font-scale)); }
    .card h3 { margin-top: 0; margin-bottom: 8px; font-size: calc(1.08rem * var(--font-scale)); }
    .card h4 { font-family: var(--serif); margin-top: 4px; margin-bottom: 6px; font-size: calc(1.0rem * var(--font-scale)); }
    .field-label, .form-field label {
      display: block;
      font-size: calc(0.81rem * var(--font-scale));
      font-weight: 700;
      color: var(--ink);
      margin-bottom: 4px;
    }
    .field-label input, .field-label select, .field-label textarea,
    .form-field input, .form-field select, .form-field textarea {
      width: 100%;
    }
    .badge {
      display: inline-block;
      padding: 3px 9px;
      border-radius: 5px;
      font-size: calc(0.73rem * var(--font-scale));
      font-weight: 700;
      letter-spacing: 0.02em;
      margin-right: 6px;
    }
    .badge.stip { background: var(--stipulated-bg); color: var(--stipulated); }
    .badge.warn { background: var(--warning-bg); color: var(--warning); }
    .badge.danger { background: var(--danger-bg); color: var(--danger); }
    .badge.info { background: var(--accent-soft); color: var(--ink); }
    .quote-box {
      background: var(--surface-alt);
      border-left: 4px solid var(--accent);
      padding: 13px 16px;
      border-radius: 0 8px 8px 0;
      font-size: calc(0.95rem * var(--font-scale));
      margin: 10px 0;
    }
    .pivot-say {
      background: var(--stipulated-bg);
      color: var(--stipulated);
      border-left: 5px solid var(--stipulated);
      padding: 12px 15px;
      border-radius: 7px;
      font-weight: 600;
      margin-top: 10px;
    }
    .trap-dont {
      background: var(--danger-bg);
      color: var(--danger);
      border-left: 4px solid var(--danger);
      padding: 9px 13px;
      border-radius: 6px;
      font-size: calc(0.88rem * var(--font-scale));
      margin-top: 8px;
    }
    .search-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 14px;
      align-items: center;
    }
    .search-input {
      padding: 8px 11px;
      border: 1.5px solid var(--border);
      border-radius: 7px;
      background: var(--surface);
      color: var(--ink);
      font-size: calc(0.9rem * var(--font-scale));
    }
    .svg-frame {
      width: 100%;
      overflow-x: auto;
      margin: 10px 0;
      border-radius: 9px;
    }
    .svg-frame svg { width: 100%; height: auto; display: block; }
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: calc(0.87rem * var(--font-scale));
    }
    table.data-table th, table.data-table td {
      border-bottom: 1px solid var(--border);
      padding: 10px 12px;
      text-align: left;
      vertical-align: top;
    }
    table.data-table th {
      background: var(--surface-alt);
      font-weight: 700;
      text-transform: uppercase;
      font-size: calc(0.74rem * var(--font-scale));
      letter-spacing: 0.04em;
      color: var(--muted);
    }
    .exhibit-pill {
      display: inline-block;
      background: var(--surface-alt);
      border: 1px solid var(--border-strong);
      border-radius: 5px;
      padding: 2px 8px;
      font-family: var(--mono);
      font-size: calc(0.76rem * var(--font-scale));
      margin: 2px 4px 2px 0;
      font-weight: 700;
      text-decoration: none;
    }
    .exhibit-thumb {
      margin-top: 8px;
      border: 1px solid var(--border);
      border-radius: 7px;
      background: var(--surface);
      padding: 6px;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      max-width: 100%;
    }
    .exhibit-thumb img {
      max-width: 140px;
      max-height: 92px;
      border-radius: 4px;
      object-fit: cover;
      border: 1px solid var(--border);
      display: block;
    }
    .empty-state {
      background: var(--surface-alt);
      border: 1.5px dashed var(--border-strong);
      border-radius: 9px;
      padding: 20px;
      text-align: center;
      color: var(--muted);
      margin: 10px 0;
    }
    .intake-dropzone {
      background: var(--surface-alt);
      border: 2px dashed var(--accent);
      border-radius: 10px;
      padding: 16px 18px;
      margin: 12px 0;
      transition: background 0.15s ease, border-color 0.15s ease;
    }
    .intake-dropzone.drag-active {
      background: var(--accent-soft);
      border-color: var(--stipulated);
    }
    .format-chip-row {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-top: 8px;
    }
    .format-chip {
      font-family: var(--mono);
      font-size: calc(0.7rem * var(--font-scale));
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--muted);
    }
    .modality-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 8px;
      border-radius: 5px;
      font-size: calc(0.73rem * var(--font-scale));
      font-weight: 700;
      background: var(--accent-soft);
      color: var(--ink);
    }
    .jural-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 9px;
      border-radius: 999px;
      font-size: calc(0.73rem * var(--font-scale));
      font-weight: 700;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--accent);
    }
    .deadline-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px;
      margin: 12px 0;
    }
    .deadline-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 8px;
      padding: 10px 12px;
    }
    .deadline-card.ready { border-left-color: var(--stipulated); }
    .deadline-card.urgent { border-left-color: var(--warning); }
    .pleading-preview {
      background: var(--surface);
      border: 1.5px solid var(--border-strong);
      border-left: 5px solid var(--accent);
      border-radius: 8px;
      padding: 18px 20px;
      font-family: var(--mono);
      font-size: calc(0.81rem * var(--font-scale));
      line-height: 1.58;
      white-space: pre-wrap;
      max-height: 440px;
      overflow-y: auto;
      margin-top: 12px;
    }
    footer.site-footer {
      border-top: 1.5px solid var(--border);
      padding: 22px 24px;
      text-align: center;
      font-size: 0.84rem;
      color: var(--muted);
      background: var(--surface);
    }
"""


def _shared_header_html(active_page):
    logo_svg = render_logo_svg()
    nav_items = [
        ("index.html", "Overview &amp; Matters"),
        ("client.html", "Client Workspace"),
        ("lawyer.html", "Counsel Workbench"),
        ("courtroom.html", "Courtroom Mode"),
    ]
    pills = "\n".join(
        f'<a href="{href}" class="nav-pill{" active" if href == active_page else ""}"{" aria-current=\"page\"" if href == active_page else ""}>{label}</a>'
        for href, label in nav_items
    )
    return f"""
  <header class="portal-header" role="banner">
    <div class="header-inner">
      <a href="index.html" class="brand-row">
        <div class="brand-logo">{logo_svg}</div>
        <div>
          <div class="brand-title-row">
            <span class="brand-title">PrismLegal</span>
            <span class="brand-pill">Public-Benefit Legal Service</span>
          </div>
          <p class="brand-sub" id="global-header-sub">Case Preparation, Evidence Mapping &amp; Hearing Readiness</p>
        </div>
      </a>
      <nav class="portal-nav-pills" aria-label="Primary Service Workspaces">
        {pills}
      </nav>
      <div class="header-utilities">
        <label class="header-matter-Cluster" title="Switch Active Legal Matter">
          <span>Matter:</span>
          <select id="global-matter-select" aria-label="Switch Active Legal Matter"></select>
        </label>
        <button type="button" id="btn-global-save-json" class="btn" title="Download active matter file (.prismlegal.json)">💾 Save .json</button>
        <button type="button" id="btn-stand-mode" class="btn" aria-pressed="false" title="Toggle large courtroom text">Aa</button>
        <button type="button" id="btn-theme" class="btn" aria-pressed="false" title="Toggle light or dark display">◐ Theme</button>
      </div>
    </div>
  </header>
"""


def _shared_js_helpers():
    return r"""
      const DATA = JSON.parse(document.getElementById('case-model-data').textContent);

      function escapeHtml(str) {
        return String(str === undefined || str === null ? '' : str)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;');
      }

      const WORKSPACE_KEY = 'prism_legal_workspace_v4';
      const THEME_KEY = 'prism_legal_theme';
      const STAND_KEY = 'prism_legal_stand';

      function normalizeMatter(m) {
        if (!m) return m;
        m.areaOfLaw = m.areaOfLaw || m.practiceArea || '';
        m.practiceArea = m.areaOfLaw;
        m.reliefGoals = Array.isArray(m.reliefGoals) ? m.reliefGoals : (Array.isArray(m.goals) ? m.goals : []);
        m.goals = m.reliefGoals;
        m.timeline = (m.timeline || []).map(ev => {
          ev.exhibitId = ev.exhibitId || ev.exhibitLabel || (Array.isArray(ev.exhibits) && ev.exhibits.length ? ev.exhibits.join(', ') : '');
          ev.exhibitLabel = ev.exhibitId;
          ev.description = ev.description || ev.summary || '';
          return ev;
        });
        const isFamBenchmark = Boolean(m.isExample && (m.id === 'EXAMPLE-FAMILY' || m.id === 'CASE-2030-FAM-9010'));
        const visList = (isFamBenchmark && DATA && DATA.visualEvidence && DATA.visualEvidence.visualForensics) ? DATA.visualEvidence.visualForensics : [];
        const diaryList = (isFamBenchmark && DATA && DATA.visualEvidence && DATA.visualEvidence.diaryEntries) ? DATA.visualEvidence.diaryEntries : [];
        const photoList = (isFamBenchmark && DATA && DATA.visualEvidence && DATA.visualEvidence.photoPages) ? DATA.visualEvidence.photoPages : [];
        const mapList = (isFamBenchmark && DATA && DATA.visualEvidence && DATA.visualEvidence.semanticMappings) ? DATA.visualEvidence.semanticMappings : [];
        const cocList = (isFamBenchmark && DATA && DATA.legalMeta && DATA.legalMeta.chainOfCustody) ? DATA.legalMeta.chainOfCustody : [];
        m.exhibits = (m.exhibits || []).map(e => {
          const eid = e.id || e.label || '';
          const vMatch = visList.find(v => v.exhibitId === eid);
          const mMatch = mapList.find(mp => mp.exhibitId === eid);
          const cMatch = cocList.find(c => c.exhibitId === eid);
          const dMatches = diaryList.filter(d => d.exhibitId === eid);
          const pMatches = photoList.filter(p => p.exhibitId === eid);
          if (!e.visualNotes && isFamBenchmark) {
            const parts = [];
            if (vMatch && vMatch.handwrittenDetails) parts.push(`${vMatch.modality} (${vMatch.pageCount} pp.): ${vMatch.handwrittenDetails}`);
            if (dMatches.length) parts.push(`Handwritten Study Log (${dMatches.length} entries): e.g. ${dMatches[0].pageRange} — ${dMatches[0].fullContextRebuttal}`);
            if (pMatches.length) parts.push(`Photo Compendium (${pMatches.length} captioned pages): pp. 1-${pMatches.length} covering ${pMatches.slice(0, 3).map(p => p.subjects).join('; ')}`);
            e.visualNotes = parts.join(' | ');
          }
          if (!e.pivotIntent && mMatch) {
            e.pivotIntent = `${mMatch.proponentTrialIntent} · Trial Pivot: ${mMatch.trialPivotIntent}`;
          }
          if (!e.sha256 && cMatch && cMatch.sha256Digest) {
            e.sha256 = cMatch.sha256Digest;
          }
          if (!e.foundation && cMatch && cMatch.foundationRule) {
            e.foundation = cMatch.foundationRule;
          }
          return e;
        });
        m.claims = (m.claims || []).map(c => {
          c.statute = c.statute || c.statutory || '';
          c.statement = c.statement || c.summary || c.title || '';
          return c;
        });
        m.traps = (m.traps || []).map(t => {
          t.question = t.question || t.allegation || '';
          t.allegation = t.question;
          t.avoid = t.avoid || t.trapWarning || '';
          t.trapWarning = t.avoid;
          t.response = t.response || t.openingAlignedPivot || '';
          t.exhibitId = t.exhibitId || (Array.isArray(t.exhibits) && t.exhibits.length ? t.exhibits.join(', ') : (Array.isArray(t.rebuttalExhibits) && t.rebuttalExhibits.length ? t.rebuttalExhibits.join(', ') : ''));
          t.exhibits = t.exhibitId ? t.exhibitId.split(',').map(s => s.trim()).filter(Boolean) : [];
          t.readiness = t.readiness || 'Ready for Court';
          return t;
        });
        m.directExam = (m.directExam || []).map(d => {
          d.chapter = d.chapter || d.section || 'Direct Examination';
          d.section = d.chapter;
          d.answer = d.answer || d.fullTestimony || '';
          d.fullTestimony = d.answer;
          d.exhibitId = (d.exhibitId && d.exhibitId !== 'NONE') ? d.exhibitId : (d.exhibitLabel || '');
          d.exhibitLabel = d.exhibitId;
          d.visualCue = d.visualCue || (d.priority ? 'yellow-highlight' : 'standard');
          d.movesToAdmit = Boolean(d.movesToAdmit);
          d.coachingNote = d.coachingNote || '';
          d.counselPrompt = d.counselPrompt || '';
          return d;
        });
        m.witnesses = (m.witnesses || []).map(w => {
          w.role = w.role || w.relationship || 'Fact Witness';
          w.status = w.status || w.callStatus || 'will-call';
          w.callStatus = w.status;
          return w;
        });
        m.agenda = (m.agenda || []).map(a => {
          a.topic = a.topic || a.category || a.targetId || 'Case Strategy';
          a.questionForCounsel = a.questionForCounsel || a.clientQuestion || a.questionForLawyer || '';
          a.clientQuestion = a.questionForCounsel;
          a.counselGuidance = a.counselGuidance || a.attorneyGuidance || a.lawyerGuidance || 'Pending attorney review.';
          a.attorneyGuidance = a.counselGuidance;
          return a;
        });
        m.ruleExceptions = m.ruleExceptions || [];
        m.representationScope = m.representationScope || '';
        m.calculators = m.calculators || {};
        return m;
      }

      function createBlankMatter(overrides) {
        const id = 'MATTER-' + Date.now().toString(36).toUpperCase();
        return normalizeMatter(Object.assign({
          id: id,
          title: '',
          docketNumber: '',
          practiceArea: '',
          areaOfLaw: '',
          forum: '',
          framework: '',
          hearingDate: '',
          hearingMinutes: 180,
          clientName: '',
          clientRole: '',
          opposingParty: '',
          counselName: '',
          summary: '',
          goals: [],
          reliefGoals: [],
          timeline: [],
          exhibits: [],
          claims: [],
          traps: [],
          directExam: [],
          witnesses: [],
          agenda: [],
          calculators: {}
        }, overrides || {}));
      }

      function buildBenchmarkMatterFromData() {
        const cm = (DATA && DATA.caseMeta) ? DATA.caseMeta : {};
        const pillars = (DATA && DATA.openingPillars) ? DATA.openingPillars : [];
        const tl = (DATA && DATA.timeline) ? DATA.timeline : [];
        const respEx = (DATA && DATA.respondentExhibits) ? DATA.respondentExhibits : [];
        const petEx = (DATA && DATA.petitionerExhibits) ? DATA.petitionerExhibits : [];
        const claims = (DATA && DATA.claims) ? DATA.claims : [];
        const traps = (DATA && DATA.traps) ? DATA.traps : [];
        const dxChapters = (DATA && DATA.directExam && DATA.directExam.chapters) ? DATA.directExam.chapters : [];
        const dxQs = (DATA && DATA.directExam && DATA.directExam.questions) ? DATA.directExam.questions : [];
        const wits = (DATA && DATA.witnesses) ? DATA.witnesses : [];
        const tuneWits = (DATA && DATA.tuningState && DATA.tuningState.overrides && DATA.tuningState.overrides.witnesses) ? DATA.tuningState.overrides.witnesses : {};
        const tuneAg = (DATA && DATA.tuningState && DATA.tuningState.agenda) ? DATA.tuningState.agenda : [];
        const chMap = {};
        dxChapters.forEach(c => { chMap[c.id] = c.title; });

        const allExs = respEx.map(e => ({
          id: e.id,
          label: e.label,
          party: 'Respondent (Client)',
          title: e.title,
          date: 'Verified Record',
          category: e.category,
          foundation: 'FRE 803 / 901 Stipulated & Authenticated',
          purpose: e.purpose,
          status: e.status === 'stipulated' ? 'Stipulated' : 'Ready to Offer'
        })).concat(petEx.map(e => ({
          id: e.id,
          label: e.label,
          party: 'Petitioner (Opposing)',
          title: e.title,
          date: 'Opposing Filing',
          category: e.category,
          foundation: 'Objection / FRE 106 Completeness & Rebuttal',
          purpose: e.fatherPivot,
          pivotIntent: `Opposing Use: ${e.motherUse} · Trial Pivot: ${e.fatherPivot}`,
          status: 'Objected / Contested'
        })));

        return createBlankMatter({
          id: 'CASE-2030-FAM-9010',
          isExample: true,
          title: 'Parenting Plan & Guideline Support Benchmark (30 Exhibits · 36 Q&As)',
          docketNumber: cm.caseNumber || '2030-FAM-9010',
          practiceArea: 'Family & Parenting Law',
          areaOfLaw: 'Family & Parenting Law',
          forum: cm.court || 'Metropolitan Superior Court — Family Law Department',
          framework: 'Uniform Best-Interests (§ 402), Support Guidelines (§ 305) & Rule 16.2',
          hearingDate: cm.hearingDate || '2030-09-18',
          hearingMinutes: 360,
          clientName: 'Respondent Co-Parent (100% P&T Disabled Retiree)',
          clientRole: 'Respondent',
          opposingParty: 'Petitioner Co-Parent (Regional Operations Manager)',
          counselName: 'Lead Domestic Relations Trial Counsel',
          summary: 'Equal 50/50 2-2-5-5 parenting schedule (182.5 overnights each) for the three minor children (ages 15, 11 & 6) with Monday/Wednesday school exchanges, joint major decision-making with mediation-first protocol (Ex. L), and $250.00/mo guideline support worksheet (Ex. N).',
          reliefGoals: pillars.map(p => ({
            id: p.id,
            title: p.title,
            requestedOrder: p.summary,
            rationale: `${p.verbatimQuote} (Backed by ${p.exhibits.join(', ')})`
          })),
          timeline: tl.map(ev => ({
            id: ev.id,
            date: ev.date,
            title: ev.title,
            description: ev.summary,
            exhibitId: (ev.exhibits || []).join(', ')
          })),
          exhibits: allExs,
          claims: claims.map(c => ({
            id: c.id,
            statute: c.statutory,
            status: c.status,
            statement: `${c.title}: ${c.summary}`,
            exhibits: c.exhibits || []
          })),
          ruleExceptions: [
            {
              id: 'EXC-01',
              rule: 'Uniform Support Guidelines § 305(5)(b) (100% P&T Disability Bar)',
              type: 'Statutory Exception / Override',
              effect: 'Overrides general potential-income imputation rule: a parent rated 100% Permanently & Totally disabled (Ex-E) cannot be imputed speculative commercial wages.',
              statute: 'Uniform Support Guidelines § 305(5)(b)',
              exhibitId: 'Ex-E'
            },
            {
              id: 'EXC-02',
              rule: 'FRCP 26(e) & Civil Rule 16.2(e)(10) (Unconscionability Override)',
              type: 'Equitable & Procedural Bar',
              effect: 'Overrides interim expense stipulation: omission of $30,000.00 across Escrow Accounts x4102 & x4109 on Initial SFS (Ex-G / Ex-H) renders retroactive reimbursement unconscionable (Ex-N ¶¶ 24-26).',
              statute: 'Civil Rule 16.2(e)(10)',
              exhibitId: 'Ex-H'
            },
            {
              id: 'EXC-03',
              rule: '38 U.S.C. § 1781 Dependent Medical Coverage Exemption',
              type: 'Federal Statutory Benefit Override',
              effect: 'Eliminates $180/mo duplicate health insurance add-on because all three minor children have comprehensive federal medical coverage at $0 monthly premium (Ex-E).',
              statute: '38 U.S.C. § 1781',
              exhibitId: 'Ex-E'
            },
            {
              id: 'EXC-04',
              rule: 'FRE 106 Rule of Completeness (Immediate Context Admission)',
              type: 'Evidentiary Completeness Override',
              effect: 'Requires immediate admission of p. 6 ll. 15-28 of the 2028 handwritten study log (OP-Ex-13) proving Respondent permanently adopted structured study-break coaching.',
              statute: 'FRE 106',
              exhibitId: 'OP-Ex-13'
            }
          ],
          traps: traps.map(t => ({
            id: t.id,
            title: t.title,
            question: t.allegation,
            avoid: t.trapWarning,
            response: t.openingAlignedPivot,
            exhibitId: (t.rebuttalExhibits || []).join(', '),
            readiness: 'Ready for Court',
            rule106Context: t.id === 'TRAP-12'
              ? 'FRE 106 Study Log Completeness (OP-Ex-13 p. 6, ll. 15-28, April 10, 2028): "I have decided permanently that rigid homework timers are counterproductive; our home will always use patient step-by-step coaching and encouragement."'
              : (t.id === 'TRAP-14' ? 'FRE 106 Full Message Thread (OP-Ex-14 pp. 1-6): Full thread shows the 15-year-old asking "When do we get 50/50 back?" and Respondent encouraging respect for both parents.' : '')
          })),
          directExam: dxQs.map(q => ({
            id: q.id,
            chapter: chMap[q.chapterId] || q.chapterId,
            visualCue: q.visualCue || 'standard',
            movesToAdmit: Boolean(q.movesToAdmit),
            coachingNote: q.coachingNote || '',
            counselPrompt: q.counselPrompt || '',
            question: q.question,
            answer: q.fullTestimony,
            exhibitId: q.exhibitId === 'NONE' ? '' : q.exhibitId
          })),
          witnesses: wits.map(w => ({
            id: w.id,
            name: w.name,
            role: w.relationship,
            status: w.callStatus,
            minutes: (tuneWits[w.id] && tuneWits[w.id].examMinutes) ? tuneWits[w.id].examMinutes : 20,
            scope: w.scope
          })),
          agenda: tuneAg.map(a => ({
            id: a.id,
            topic: `${a.category} (${a.targetId})`,
            questionForCounsel: a.questionForLawyer,
            counselGuidance: a.lawyerGuidance,
            status: 'Aligned'
          })),
          calculators: {
            supportParty1Income: 8000,
            supportParty2Income: 5000,
            supportParty2Nights: 182.5,
            supportAddons: 0
          }
        });
      }

      function buildStarterTemplates() {
        const benchmark = buildBenchmarkMatterFromData();
        benchmark.id = 'EXAMPLE-FAMILY';
        benchmark.isExample = true;
        return {
          benchmark: benchmark,
          family: benchmark,
          housing: createBlankMatter({
            id: 'EXAMPLE-HOUSING',
            isExample: true,
            title: 'Tenant Household v. Property Management LLC — Habitability & Escrow',
            docketNumber: '2030-HSG-9060',
            practiceArea: 'Housing & Tenant Rights',
            areaOfLaw: 'Housing & Tenant Rights',
            forum: 'Municipal Housing & Civil Tribunal',
            framework: 'Uniform Residential Landlord & Tenant Act (URLTA § 2.104 & § 4.104)',
            hearingDate: '2030-10-15',
            hearingMinutes: 120,
            clientName: 'Tenant Household',
            clientRole: 'Tenant / Claimant',
            opposingParty: 'Property Management LLC',
            counselName: 'Legal Aid Housing Counsel',
            summary: 'Warranty of habitability enforcement, municipal code inspection proof, and statutory 40% rent abatement from court-supervised escrow.',
            goals: [
              { id: 'GOAL-1', title: 'Order Immediate Heating & Roof Repairs', requestedOrder: 'Mandatory injunction requiring licensed remediation of heating and water intrusion within 14 days.', rationale: 'Confirmed by Municipal Code Enforcement Notice of Violation.' },
              { id: 'GOAL-2', title: '40% Statutory Rent Abatement', requestedOrder: 'Release $4,800.00 from rent escrow to Tenant Household representing a 40% habitability abatement over 6 months.', rationale: 'Timely written notice was given on March 1, 2030 and full monthly rent was deposited into court escrow.' }
            ],
            timeline: [
              { id: 'TL-1', date: '2030-03-01', title: 'Written Repair Notice Delivered', description: 'Delivered certified written notice of roof leak and heating failure to landlord.', exhibitLabel: 'Ex. A' },
              { id: 'TL-2', date: '2030-03-18', title: 'Municipal Code Violation Issued', description: 'City Inspector cited Property Management LLC for Class 2 habitability violations.', exhibitLabel: 'Ex. B' },
              { id: 'TL-3', date: '2030-04-01', title: 'Court Escrow Deposits Commenced', description: 'Tenant deposited 100% of monthly rent ($2,000/mo) into the clerk’s registry each month.', exhibitLabel: 'Ex. C' }
            ],
            exhibits: [
              { id: 'EX-1', label: 'Ex. A', party: 'Tenant', title: 'March 1 Written Habitability Notice & Delivery Receipt', category: 'Notice / Correspondence', foundation: 'FRE 901(b)(1) / Certified Mail Receipt', purpose: 'Proves statutory 14-day notice under URLTA § 4.101.', visualNotes: '2 pages: Certified Mail receipt signed 03/02/2030 + portal timestamp.', status: 'Stipulated' },
              { id: 'EX-2', label: 'Ex. B', party: 'Tenant', title: 'Municipal Code Enforcement Inspection Report & Photos', category: 'Official Inspection Record', foundation: 'FRE 803(8) Public Agency Report', purpose: 'Corroborates active water intrusion and heating failure.', visualNotes: '6 pages: Inspector Citation #2030-410 with 8 moisture-meter photographs.', status: 'Admitted' },
              { id: 'EX-3', label: 'Ex. C', party: 'Tenant', title: 'Court Clerk Rent Escrow Receipts (6 Months @ $2,000/mo)', category: 'Financial Receipt', foundation: 'Judicial Notice / Court Registry', purpose: 'Proves good-faith payment of $12,000 into escrow.', visualNotes: '6 official registry receipts totaling $12,000.00.', status: 'Stipulated' }
            ],
            claims: [
              { id: 'CLM-1', statute: 'URLTA § 2.104(a)(1)-(4)', status: 'corroborated', statement: 'Unrepaired water intrusion and heating failure materially impair health and safety.', exhibits: ['Ex. A', 'Ex. B'] },
              { id: 'CLM-2', statute: 'URLTA § 4.104 / Escrow Abatement', status: 'stipulated', statement: 'Tenant deposited $12,000 into court escrow after written notice, entitling household to a 40% diminution abatement ($4,800).', exhibits: ['Ex. A', 'Ex. C'] }
            ],
            ruleExceptions: [
              { id: 'EXC-1', rule: 'URLTA § 4.104(a) & § 5.101 Retaliatory Eviction Bar', type: 'Statutory Affirmative Defense', effect: 'Good-faith rent deposit into court escrow after 14-day written repair notice bars possession for nonpayment and creates a presumption against retaliatory eviction.' }
            ],
            traps: [
              { id: 'TRAP-1', title: 'Alleged Delay in Contractor Access', allegation: 'Landlord may claim tenant rescheduled one inspection window in April.', trapWarning: 'Do not argue; point directly to the written access log.', response: 'Exhibit A shows we offered 5 weekday and weekend access windows in writing and admitted the city inspector and landlord’s technician on every scheduled date.', exhibits: ['Ex. A', 'Ex. B'], readiness: 'Ready for Court', rule106Context: 'FRE 106 Full Portal Thread (Ex. A p. 2): Shows tenant offered 4 alternative dates within 24 hours.' }
            ],
            directExam: [
              { id: 'DX-1', section: '1. Notice & Condition of Premises', visualCue: 'yellow-highlight', movesToAdmit: true, question: 'When did the water intrusion and heating outage begin, and how did you notify the landlord?', answer: 'It began in late February, and on March 1 we sent written notice with photos by certified mail and portal message, marked as Exhibit A.', exhibitLabel: 'Ex. A' },
              { id: 'DX-2', section: '2. City Inspection & Rent Escrow', visualCue: 'yellow-highlight', movesToAdmit: true, question: 'Did you withhold rent personally or deposit it with the court?', answer: 'We deposited 100% of our $2,000 monthly rent into the Court’s escrow registry every month on time, as shown in Exhibit C.', exhibitLabel: 'Ex. C' }
            ],
            witnesses: [
              { id: 'W-1', name: 'Tenant Household Representative', role: 'Claimant', callStatus: 'will-call', minutes: 35, scope: 'Notice delivery (Ex. A), living conditions, and escrow receipts (Ex. C).' },
              { id: 'W-2', name: 'Municipal Housing Code Inspector', role: 'Subpoenaed Official Witness', callStatus: 'will-call', minutes: 25, scope: 'Authentication of March 18 Notice of Violation and inspection photos (Ex. B).' }
            ],
            agenda: [
              { id: 'AG-1', topic: 'Escrow Disbursement Order', questionForCounsel: 'Can we ask the Court to release the $4,800 abatement directly from the registry at the conclusion of the hearing?', counselGuidance: 'Yes—we have prepared a proposed Registry Disbursement Order under URLTA § 4.104.', status: 'Aligned' }
            ],
            calculators: {
              civilContractRate: 2000,
              civilImpairedMonths: 6,
              civilDiminutionPct: 40
            }
          }),
          veterans: createBlankMatter({
            id: 'EXAMPLE-VETERANS',
            isExample: true,
            title: 'Benefit Claimant Service-Connected Disability & TDIU Appeal',
            docketNumber: '2030-ADM-9020',
            practiceArea: 'Veterans & Administrative Appeals',
            areaOfLaw: 'Veterans & Administrative Appeals',
            forum: 'Administrative Appeals Tribunal',
            framework: '38 U.S.C. § 1110 & 38 C.F.R. §§ 3.102, 4.16, 4.25',
            hearingDate: '2030-10-22',
            hearingMinutes: 90,
            clientName: 'Benefit Claimant',
            clientRole: 'Appellant / Claimant',
            opposingParty: 'Regional Rating Agency',
            counselName: 'Administrative Law Clinic Counsel',
            summary: 'Service connection, combined rating calculation under 38 C.F.R. § 4.25, and Total Disability based on Individual Unemployability (§ 4.16).',
            goals: [
              { id: 'GOAL-1', title: '100% Schedular / TDIU Rating (§ 4.16)', requestedOrder: 'Grant Total Disability based on Individual Unemployability effective from the initial claim date.', rationale: 'Service-connected conditions (60%, 40%, 20%) yield an 80% combined rating under § 4.25 and preclude substantially gainful employment.' }
            ],
            timeline: [
              { id: 'TL-1', date: '2029-02-10', title: 'Intent to File & Initial Claim', description: 'Submitted formal claim preserving effective date.', exhibitLabel: 'Ex. A' },
              { id: 'TL-2', date: '2030-01-15', title: 'Independent Medical Nexus & Vocational Report', description: 'Board-certified specialist documented functional occupational limitations.', exhibitLabel: 'Ex. B' }
            ],
            exhibits: [
              { id: 'EX-1', label: 'Ex. A', party: 'Claimant', title: 'Service Treatment Records & Rating Decision', category: 'Official Service Record', foundation: '38 C.F.R. § 3.156 Service Record', purpose: 'Establishes in-service event and 80% combined schedular rating.', visualNotes: '8 pages: Highlighted rating code sheet and effective-date stamp.', status: 'Stipulated' },
              { id: 'EX-2', label: 'Ex. B', party: 'Claimant', title: 'Independent Medical Nexus & Vocational Assessment', category: 'Expert Medical Record', foundation: '38 C.F.R. § 4.16(a) Functional Opinion', purpose: 'Proves service-connected disabilities preclude substantially gainful work.', visualNotes: '12 pages: Rationale on pp. 8-11 linking functional limitations to service.', status: 'Admitted' }
            ],
            claims: [
              { id: 'CLM-1', statute: '38 C.F.R. §§ 4.25 & 4.16(a)', status: 'corroborated', statement: 'Combined 80% rating (60%, 40%, 20%) with a single 60% disability and vocational nexus satisfies § 4.16(a).', exhibits: ['Ex. A', 'Ex. B'] }
            ],
            ruleExceptions: [
              { id: 'EXC-1', rule: '38 U.S.C. § 5107(b) & 38 C.F.R. § 3.102 Benefit of the Doubt', type: 'Statutory Burden Override', effect: 'When positive and negative medical evidence are in approximate balance, reasonable doubt must be resolved in favor of the claimant.' }
            ],
            traps: [
              { id: 'TRAP-1', title: 'Sedentary Work Speculation', allegation: 'Examiner may ask if you can perform sedentary desk work.', trapWarning: 'Describe concrete daily functional limitations accurately without exaggeration.', response: 'As documented in the vocational assessment in Exhibit B, my service-connected symptoms require unscheduled rest periods and prevent reliable attendance in any full-time sedentary role.', exhibits: ['Ex. B'], readiness: 'Ready for Court' }
            ],
            directExam: [
              { id: 'DX-1', section: '1. Service History & Functional Impact', visualCue: 'yellow-highlight', movesToAdmit: true, question: 'How do your service-connected conditions affect your daily ability to maintain employment?', answer: 'They cause daily functional limitations documented in Exhibit B that prevent sustained concentration or regular work attendance.', exhibitLabel: 'Ex. B' }
            ],
            witnesses: [
              { id: 'W-1', name: 'Benefit Appellant', role: 'Claimant', callStatus: 'will-call', minutes: 45, scope: 'In-service onset, daily functional impact, and occupational history.' }
            ],
            agenda: [
              { id: 'AG-1', topic: 'Effective Date Preservation (Ex. A)', questionForCounsel: 'Confirm that our February 10, 2029 Intent to File locks in the retroactive effective date.', counselGuidance: 'Confirmed under 38 C.F.R. § 3.155(b).', status: 'Aligned' }
            ],
            calculators: {
              vaRatings: '60, 40, 20',
              vaMonthlyBaseline: 4000
            }
          }),
          employment: createBlankMatter({
            id: 'EXAMPLE-EMPLOYMENT',
            isExample: true,
            title: 'Employee Claimant v. Employer Corp. — Workplace Accommodation Claim',
            docketNumber: '2030-EMP-9040',
            practiceArea: 'Employment & Wage Protection',
            areaOfLaw: 'Employment & Wage Protection',
            forum: 'Office of Administrative Courts — Civil Rights Division',
            framework: '42 U.S.C. § 12112(b)(5)(A) ADA Reasonable Accommodation',
            hearingDate: '2030-11-05',
            hearingMinutes: 180,
            clientName: 'Employee Claimant',
            clientRole: 'Claimant',
            opposingParty: 'Employer Corp.',
            counselName: 'Civil Rights Counsel',
            summary: 'ADA reasonable accommodation interactive process proof, performance evaluations, and back-pay mitigation ledger.',
            goals: [
              { id: 'GOAL-1', title: 'Reinstatement with Approved Ergonomic / Remote Accommodation', requestedOrder: 'Order reinstatement with the physician-recommended accommodation and back-pay award.', rationale: 'Claimant performed all essential job functions with "Exceeds Expectations" reviews prior to revocation.' }
            ],
            timeline: [
              { id: 'TL-1', date: '2029-11-04', title: 'Annual Performance Evaluation ("Exceeds Expectations")', description: 'Supervisor rated Claimant 4.9/5.0 on all essential duties.', exhibitLabel: 'Ex. A' },
              { id: 'TL-2', date: '2030-02-10', title: 'Written Medical Accommodation Request Submitted', description: 'Submitted physician certification requesting hybrid schedule accommodation.', exhibitLabel: 'Ex. B' }
            ],
            exhibits: [
              { id: 'EX-1', label: 'Ex. A', party: 'Claimant', title: '2028–2029 Performance Evaluations & Job Description', category: 'Employment Record', foundation: 'FRE 803(6) Business Record', purpose: 'Proves qualification and full performance of essential job functions.', visualNotes: '4 pages: Supervisor signature & 4.9/5.0 rating on essential duties.', status: 'Stipulated' },
              { id: 'EX-2', label: 'Ex. B', party: 'Claimant', title: 'Physician Accommodation Request & HR Email Thread', category: 'Medical / HR Record', foundation: 'FRE 801(d)(2) Opposing Party Admission', purpose: 'Proves Employer terminated interactive process without undue-hardship analysis.', visualNotes: '5 pages: HR email dated 02/18/2030 denying request without interactive meeting.', status: 'Admitted' }
            ],
            claims: [
              { id: 'CLM-1', statute: '42 U.S.C. § 12112(b)(5)(A)', status: 'corroborated', statement: 'Claimant is a qualified individual who requested a reasonable accommodation that imposed zero undue hardship.', exhibits: ['Ex. A', 'Ex. B'] }
            ],
            ruleExceptions: [
              { id: 'EXC-1', rule: '42 U.S.C. § 12112(b)(5)(A) Reasonable Accommodation Mandate', type: 'Statutory Policy Override', effect: 'Overrides neutral on-site attendance policy unless Employer proves concrete undue hardship under § 12111(10).' }
            ],
            traps: [
              { id: 'TRAP-1', title: 'Essential Function Presence Claim', allegation: 'Employer may argue physical presence 5 days a week is an essential job function.', trapWarning: 'Point to actual remote performance metrics in Ex. A rather than general opinions.', response: 'Exhibit A documents that our team operated on a hybrid schedule throughout 2029, during which I completed 100% of my assigned duties with a 4.9 out of 5 rating.', exhibits: ['Ex. A', 'Ex. B'], readiness: 'Ready for Court' }
            ],
            directExam: [
              { id: 'DX-1', section: '1. Essential Duties & Accommodation Request', visualCue: 'yellow-highlight', movesToAdmit: true, question: 'What accommodation did your physician recommend in Exhibit B, and how did HR respond?', answer: 'My physician recommended a two-day remote schedule in Exhibit B, which matched our existing hybrid workflow, and HR denied it within 48 hours without holding an interactive meeting.', exhibitLabel: 'Ex. B' }
            ],
            witnesses: [
              { id: 'W-1', name: 'Employee Claimant', role: 'Claimant', callStatus: 'will-call', minutes: 45, scope: 'Job duties, 4.9/5.0 evaluations (Ex. A), and interactive process (Ex. B).' }
            ],
            agenda: [
              { id: 'AG-1', topic: 'Back-Pay Mitigation Ledger', questionForCounsel: 'Should we include Q2 job search logs with our pre-hearing exchange?', counselGuidance: 'Yes—stipulated as supplemental pages to Exhibit A.', status: 'Aligned' }
            ]
          }),
          consumer: createBlankMatter({
            id: 'EXAMPLE-CONSUMER',
            isExample: true,
            title: 'Consumer Respondent v. Debt Portfolio Buyer LLC — Chain of Title & FDCPA Defense',
            docketNumber: '2030-CON-9050',
            practiceArea: 'Consumer, Debt & Small Claims',
            areaOfLaw: 'Consumer, Debt & Small Claims',
            forum: 'County Civil Court — Small Claims & Consumer Division',
            framework: '15 U.S.C. § 1692g (FDCPA), UCC § 2-714 & FRE 803(6)/901',
            hearingDate: '2030-11-12',
            hearingMinutes: 90,
            clientName: 'Consumer Respondent',
            clientRole: 'Respondent / Counter-Claimant',
            opposingParty: 'Debt Portfolio Buyer LLC',
            counselName: 'Consumer Law Clinic Counsel',
            summary: 'Enforcement of strict chain-of-title authentication (FRE 901), hearsay exclusion of unverified third-party spreadsheets (FRE 803(6)), and statutory FDCPA validation defense.',
            goals: [
              { id: 'GOAL-1', title: 'Dismissal with Prejudice for Lack of Standing & Chain of Title', requestedOrder: 'Dismiss collection complaint with prejudice and award statutory costs under 15 U.S.C. § 1692k.', rationale: 'Plaintiff produced only a redacted bill-of-sale cover page with zero schedule of accounts linking Respondent.' }
            ],
            timeline: [
              { id: 'TL-1', date: '2030-03-04', title: 'Timely Written Debt Validation Demand Sent', description: 'Delivered 15 U.S.C. § 1692g(b) dispute and validation demand within 30 days.', exhibitLabel: 'Ex. A' },
              { id: 'TL-2', date: '2030-06-19', title: 'Plaintiff Disclosures Omit Account Schedule & Original Contract', description: 'Discovery response confirmed Plaintiff lacks original signed cardholder agreement.', exhibitLabel: 'Ex. B' }
            ],
            exhibits: [
              { id: 'EX-1', label: 'Ex. A', party: 'Respondent', title: 'Certified 15 U.S.C. § 1692g Written Validation Demand & Receipt', category: 'Statutory Notice', foundation: 'FRE 901(b)(1) / Certified Mail', purpose: 'Proves timely statutory dispute requiring verification before collection.', visualNotes: '3 pages: Signed demand letter + postal tracking confirmation.', status: 'Stipulated' },
              { id: 'EX-2', label: 'Ex. B', party: 'Respondent', title: 'Plaintiff Discovery Responses & Unreferenced Bill of Sale', category: 'Discovery Admission', foundation: 'FRE 801(d)(2) Opposing Party Admission', purpose: 'Establishes absence of unbroken chain of assignment from original creditor.', visualNotes: '4 pages: Bill of sale references "Exhibit 1 Schedule" which is missing.', status: 'Admitted' }
            ],
            claims: [
              { id: 'CLM-1', statute: 'FRE 803(6) & FRE 901 Chain of Assignment', status: 'corroborated', statement: 'Third-party debt buyer lacks a qualified witness with personal knowledge of the original creditor’s record-keeping system and an unbroken chain of title.', exhibits: ['Ex. A', 'Ex. B'] }
            ],
            ruleExceptions: [
              { id: 'EXC-1', rule: 'FRE 803(6) Third-Party Incorporation Limit', type: 'Evidentiary Hearsay Bar', effect: 'A debt buyer cannot authenticate an original creditor’s statements merely by placing downloaded files into its own folders without independent verification.' }
            ],
            traps: [
              { id: 'TRAP-1', title: 'Attempt to Shift Burden via Silence', allegation: 'Collector may ask whether you ever held a credit card with the bank years ago.', trapWarning: 'Do not speculate about account numbers or balances; require strict documentary proof of the specific account and assignment.', response: 'I timely requested written verification of this alleged account and chain of assignment in Exhibit A, and no original contract or itemized statement has ever been provided.', exhibits: ['Ex. A', 'Ex. B'], readiness: 'Ready for Court' }
            ],
            directExam: [
              { id: 'DX-1', section: '1. Timely Statutory Validation Request', visualCue: 'yellow-highlight', movesToAdmit: true, question: 'What action did you take upon receiving the initial collection notice in March 2030?', answer: 'Within ten days, I sent the written validation request in Exhibit A by certified mail asking for the original contract, itemized accounting, and chain of assignment.', exhibitLabel: 'Ex. A' }
            ],
            witnesses: [
              { id: 'W-1', name: 'Consumer Respondent', role: 'Respondent', callStatus: 'will-call', minutes: 25, scope: 'Authentication of timely § 1692g validation demand (Ex. A) and discovery record (Ex. B).' }
            ],
            agenda: [
              { id: 'AG-1', topic: 'FRE 803(6) Motion in Limine', questionForCounsel: 'Will we object to the collector’s affidavit before witness testimony starts?', counselGuidance: 'Yes—we will move to exclude the unverified spreadsheet under FRE 803(6) and FRE 901 at the start of Plaintiff’s case.', status: 'Aligned' }
            ]
          }),
          commercial: createBlankMatter({
            id: 'EXAMPLE-COMMERCIAL',
            isExample: true,
            title: 'Member-Manager v. Operating Entity LLC — Fiduciary Accounting & Contract Remedies',
            docketNumber: '2030-COM-9030',
            practiceArea: 'Civil Litigation & Probate',
            areaOfLaw: 'Civil Litigation & Probate',
            forum: 'Metropolitan Superior Court — Commercial & Fiduciary Docket',
            framework: 'Restatement (Second) of Contracts § 347, UCC Article 2 & Uniform Trust/Entity Code',
            hearingDate: '2030-11-19',
            hearingMinutes: 240,
            clientName: 'Claimant Member / Beneficiary',
            clientRole: 'Plaintiff / Petitioner',
            opposingParty: 'Managing Counterparty LLC',
            counselName: 'Commercial & Fiduciary Litigation Counsel',
            summary: 'Enforcement of operating agreement inspection rights, K-1 pass-through reconciliation, and expectation damages under Restatement (Second) § 347.',
            goals: [
              { id: 'GOAL-1', title: 'Judgment for Verified Contract & Distribution Shortfall', requestedOrder: 'Enter judgment for $50,000.00 in withheld pass-through distributions and order a full independent CPA audit.', rationale: 'Certified K-1 schedules and bank ledgers prove distributions were earned and improperly diverted.' }
            ],
            timeline: [
              { id: 'TL-1', date: '2028-01-15', title: 'Operating & Licensing Agreement Executed', description: 'Parties executed Operating Agreement § 8.2 requiring pro-rata quarterly distributions.', exhibitLabel: 'Ex. A' },
              { id: 'TL-2', date: '2030-04-15', title: 'CPA Reconciliation Exposes $50,000 Distribution Shortfall', description: 'Schedule K-1 vs. operating bank ledger audit confirmed unpaid allocation.', exhibitLabel: 'Ex. B' }
            ],
            exhibits: [
              { id: 'EX-1', label: 'Ex. A', party: 'Claimant', title: 'Executed Operating Agreement & IP License (§ 8.2 Distribution Clause)', category: 'Contract Instrument', foundation: 'FRE 901(b)(1) / Stipulated Instrument', purpose: 'Establishes mandatory quarterly distribution formula and inspection rights.', visualNotes: '14 pages: § 8.2 highlighted on p. 9; signatures on p. 14.', status: 'Stipulated' },
              { id: 'EX-2', label: 'Ex. B', party: 'Claimant', title: 'CPA Forensic K-1 & Bank Ledger Reconciliation Schedule', category: 'Financial / Expert Summary', foundation: 'FRE 1006 Voluminous Record Summary', purpose: 'Quantifies exact $50,000.00 shortfall from underlying bank statements.', visualNotes: '6 pages: Tie-out table linking monthly bank statements to K-1 Box 1.', status: 'Admitted' }
            ],
            claims: [
              { id: 'CLM-1', statute: 'Restatement (Second) of Contracts § 347 & Operating Agreement § 8.2', status: 'corroborated', statement: 'Claimant performed all contractual obligations and is entitled to $50,000.00 in expectation damages per the FRE 1006 ledger summary.', exhibits: ['Ex. A', 'Ex. B'] }
            ],
            ruleExceptions: [
              { id: 'EXC-1', rule: 'DGCL § 144 / Entire Fairness Fiduciary Burden Shift', type: 'Fiduciary Burden Shift', effect: 'Where a managing fiduciary stands on both sides of a self-dealing transaction, the business judgment presumption is overridden and the fiduciary bears the burden of proving entire fairness.' }
            ],
            traps: [
              { id: 'TRAP-1', title: 'Unapproved Working-Capital Reserve Defense', allegation: 'Counterparty may claim funds were held back as an informal working-capital reserve.', trapWarning: 'Cite the explicit written consent requirement in § 8.2 of Exhibit A.', response: 'Section 8.2 of Exhibit A requires written supermajority approval to withhold reserves, and Exhibit B shows the funds were transferred to a related entity rather than held in company reserves.', exhibits: ['Ex. A', 'Ex. B'], readiness: 'Ready for Court' }
            ],
            directExam: [
              { id: 'DX-1', section: '1. Operating Agreement & CPA Tie-Out', visualCue: 'yellow-highlight', movesToAdmit: true, question: 'What does Section 8.2 of the Operating Agreement in Exhibit A require, and what did the reconciliation in Exhibit B show?', answer: 'Section 8.2 requires pro-rata quarterly distributions, and the reconciliation in Exhibit B shows $50,000.00 of our earned share was withheld without written consent.', exhibitLabel: 'Ex. B' }
            ],
            witnesses: [
              { id: 'W-1', name: 'Claimant Member-Manager', role: 'Plaintiff', callStatus: 'will-call', minutes: 45, scope: 'Contract execution (Ex. A) and governance correspondence.' },
              { id: 'W-2', name: 'Forensic Accounting Expert (CPA)', role: 'Expert Witness', callStatus: 'will-call', minutes: 40, scope: 'FRE 1006 K-1 and bank statement reconciliation (Ex. B).' }
            ],
            agenda: [
              { id: 'AG-1', topic: 'FRE 1006 Underlying Bank Statements', questionForCounsel: 'Confirm that all underlying bank statements for Exhibit B were produced 30 days before trial.', counselGuidance: 'Confirmed—served with our FRE 1006 Notice on August 1.', status: 'Aligned' }
            ]
          })
        };
      }

      const TEMPLATES = buildStarterTemplates();
      const EXAMPLE_LIST = [
        TEMPLATES.family,
        TEMPLATES.housing,
        TEMPLATES.veterans,
        TEMPLATES.employment,
        TEMPLATES.consumer,
        TEMPLATES.commercial
      ];

      function getExampleById(idOrKey) {
        if (!idOrKey) return null;
        if (TEMPLATES[idOrKey]) return JSON.parse(JSON.stringify(TEMPLATES[idOrKey]));
        const found = EXAMPLE_LIST.find(ex => ex.id === idOrKey);
        return found ? JSON.parse(JSON.stringify(found)) : null;
      }

      function getExampleMatterForArea(areaOfLaw) {
        const area = String(areaOfLaw || '').toLowerCase();
        if (area.includes('hous') || area.includes('tenant')) return TEMPLATES.housing;
        if (area.includes('veteran') || area.includes('admin')) return TEMPLATES.veterans;
        if (area.includes('employ') || area.includes('wage')) return TEMPLATES.employment;
        if (area.includes('consum') || area.includes('debt')) return TEMPLATES.consumer;
        if (area.includes('civil') || area.includes('probate') || area.includes('commerc')) return TEMPLATES.commercial;
        return TEMPLATES.family;
      }

      function loadWorkspace() {
        try {
          const raw = localStorage.getItem(WORKSPACE_KEY);
          if (raw) {
            const parsed = JSON.parse(raw);
            if (parsed && Array.isArray(parsed.matters)) {
              parsed.matters = parsed.matters
                .filter(m => m && !m.isExample && !m.isUnsavedDraft && !String(m.id || '').startsWith('EXAMPLE-'))
                .map(normalizeMatter);
              parsed.activeMatterId = parsed.activeMatterId || '';
              return parsed;
            }
          }
        } catch (e) {}
        return {
          activeMatterId: '',
          matters: []
        };
      }

      let workspace = loadWorkspace();

      function saveWorkspace() {
        try {
          workspace.matters = (workspace.matters || []).filter(m => m && !m.isExample && !m.isUnsavedDraft && !String(m.id || '').startsWith('EXAMPLE-'));
          localStorage.setItem(WORKSPACE_KEY, JSON.stringify(workspace));
        } catch (e) {}
        updateGlobalHeaderMatter();
      }

      function setActiveMatterId(id) {
        workspace = loadWorkspace();
        workspace.activeMatterId = id || '';
        saveWorkspace();
      }

      function copyExampleToSavedMatters(idOrKey) {
        const ex = getExampleById(idOrKey) || TEMPLATES.family;
        const copy = JSON.parse(JSON.stringify(ex));
        delete copy.isExample;
        delete copy.isUnsavedDraft;
        copy.id = 'MATTER-' + Date.now().toString(36).toUpperCase();
        if (!copy.title.includes('(My Saved Copy)')) {
          copy.title = copy.title + ' (My Saved Copy)';
        }
        workspace = loadWorkspace();
        workspace.matters.push(normalizeMatter(copy));
        workspace.activeMatterId = copy.id;
        saveWorkspace();
        return copy;
      }

      function updateActiveMatter(matter) {
        if (!matter) return;
        normalizeMatter(matter);
        workspace = loadWorkspace();
        if (matter.isUnsavedDraft || matter.isExample || String(matter.id || '').startsWith('EXAMPLE-') || matter.id === 'DRAFT-NEW') {
          const wasExample = Boolean(matter.isExample || String(matter.id || '').startsWith('EXAMPLE-'));
          delete matter.isUnsavedDraft;
          delete matter.isExample;
          matter.id = 'MATTER-' + Date.now().toString(36).toUpperCase();
          if (wasExample && !matter.title.includes('(My Saved Copy)')) {
            matter.title = matter.title + ' (My Saved Copy)';
          }
        }
        const idx = workspace.matters.findIndex(m => m.id === matter.id);
        if (idx >= 0) {
          workspace.matters[idx] = matter;
        } else {
          workspace.matters.push(matter);
        }
        workspace.activeMatterId = matter.id;
        saveWorkspace();
      }

      function getActiveMatter() {
        workspace = loadWorkspace();
        if (workspace.activeMatterId) {
          if (workspace.activeMatterId === 'DRAFT-NEW') {
            return null;
          }
          const saved = workspace.matters.find(m => m.id === workspace.activeMatterId);
          if (saved) return normalizeMatter(saved);
          const example = getExampleById(workspace.activeMatterId);
          if (example) return normalizeMatter(example);
        }
        if (workspace.matters.length > 0) {
          workspace.activeMatterId = workspace.matters[0].id;
          return normalizeMatter(workspace.matters[0]);
        }
        return null;
      }

      function ensureActiveMatter() {
        let m = getActiveMatter();
        if (!m) {
          m = createBlankMatter({
            id: 'DRAFT-NEW',
            isUnsavedDraft: true,
            title: '',
            docketNumber: '',
            summary: ''
          });
        }
        return m;
      }

      function buildMatterSelectOptionsHtml(currentMatter) {
        const ws = loadWorkspace();
        const curId = currentMatter ? currentMatter.id : (ws.activeMatterId || 'DRAFT-NEW');
        const savedOptions = ws.matters.map(x =>
          `<option value="${escapeHtml(x.id)}" ${x.id === curId ? 'selected' : ''}>★ ${escapeHtml(x.title || 'Untitled Matter')} (${escapeHtml(x.docketNumber || 'Saved')})</option>`
        ).join('');
        const draftOption = `<option value="DRAFT-NEW" ${(curId === 'DRAFT-NEW' || (currentMatter && currentMatter.isUnsavedDraft)) ? 'selected' : ''}>${ws.matters.length === 0 ? '✨ New Blank Matter (Unsaved Draft)' : '+ Start New Blank Matter Draft'}</option>`;
        const exampleOptions = EXAMPLE_LIST.map(ex =>
          `<option value="${escapeHtml(ex.id)}" ${ex.id === curId ? 'selected' : ''}>📘 Example (${escapeHtml(ex.areaOfLaw)}): ${escapeHtml(ex.title)}</option>`
        ).join('');
        return `
          <optgroup label="📁 My Saved Matters (${ws.matters.length})">
            ${savedOptions}
            ${draftOption}
          </optgroup>
          <optgroup label="📘 Reference Examples (Preview Only — Not Saved)">
            ${exampleOptions}
          </optgroup>
        `;
      }

      function updateGlobalHeaderMatter() {
        const sub = document.getElementById('global-header-sub');
        const sel = document.getElementById('global-matter-select');
        const m = getActiveMatter();
        if (sub) {
          if (m && m.isExample) {
            sub.textContent = `📘 Previewing Reference Example: ${m.title} (${m.areaOfLaw || m.practiceArea}) — Not in your Saved Matters`;
          } else if (m) {
            sub.textContent = `★ Saved Matter: ${m.title || 'Untitled Matter'}${m.areaOfLaw ? ' · ' + m.areaOfLaw : ''}${m.forum ? ' · ' + m.forum : ''}`;
          } else {
            sub.textContent = '0 Saved Matters · Start Your New Matter or Explore a Reference Example Below';
          }
        }
        if (sel) {
          sel.innerHTML = buildMatterSelectOptionsHtml(m || { id: 'DRAFT-NEW', isUnsavedDraft: true });
        }
      }
      updateGlobalHeaderMatter();

      const globalSelEl = document.getElementById('global-matter-select');
      if (globalSelEl) {
        globalSelEl.addEventListener('change', () => {
          if (globalSelEl.value) {
            setActiveMatterId(globalSelEl.value);
            window.location.reload();
          }
        });
      }
      const globalSaveBtn = document.getElementById('btn-global-save-json');
      if (globalSaveBtn) {
        globalSaveBtn.addEventListener('click', () => {
          const cur = ensureActiveMatter();
          exportMatterJson(cur);
        });
      }

      document.addEventListener('click', (ev) => {
        const startBlankBtn = ev.target.closest('[data-action-start-blank]');
        if (startBlankBtn) {
          setActiveMatterId('DRAFT-NEW');
          window.location.reload();
          return;
        }
        const previewExBtn = ev.target.closest('[data-action-preview-example]');
        if (previewExBtn) {
          const exId = previewExBtn.getAttribute('data-action-preview-example') || 'EXAMPLE-FAMILY';
          setActiveMatterId(exId);
          window.location.reload();
          return;
        }
        const copyExBtn = ev.target.closest('[data-action-copy-example]');
        if (copyExBtn) {
          const exId = copyExBtn.getAttribute('data-action-copy-example') || 'EXAMPLE-FAMILY';
          copyExampleToSavedMatters(exId);
          window.location.reload();
          return;
        }
      });

      function renderStepExampleDrawer(stepId, exMatter) {
        if (!exMatter) return '';
        const area = exMatter.areaOfLaw || 'Family & Parenting Law';
        const goals = (exMatter.reliefGoals || exMatter.goals || []).slice(0, 2);
        const tl = (exMatter.timeline || []).slice(0, 2);
        const exs = (exMatter.exhibits || []).slice(0, 2);
        const claims = (exMatter.claims || []).slice(0, 2);
        const excs = (exMatter.ruleExceptions || []).slice(0, 1);
        const traps = (exMatter.traps || []).slice(0, 1);
        const dxs = (exMatter.directExam || []).slice(0, 2);
        const wits = (exMatter.witnesses || []).slice(0, 2);
        const ags = (exMatter.agenda || []).slice(0, 1);

        let bodyHtml = '';
        if (stepId === 'client-step-1' || stepId === 'counsel-step-1') {
          bodyHtml = `
            <p style="margin:4px 0 8px;"><strong>How this step works in our ${escapeHtml(area)} Example (<code>${escapeHtml(exMatter.docketNumber)}</code>):</strong><br>
            Notice how the example states a clear case summary and defines specific, enforceable court orders rather than broad requests:</p>
            <div style="display:grid;gap:8px;">
              ${goals.map((g, i) => `
                <div style="padding:8px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--stipulated);">
                  <strong>Example Goal ${i + 1} (${escapeHtml(g.title)}):</strong> "${escapeHtml(g.requestedOrder)}"<br>
                  <span style="font-size:0.8rem;color:var(--muted);"><em>Why It Works:</em> ${escapeHtml(g.rationale)}</span>
                </div>
              `).join('')}
            </div>
          `;
        } else if (stepId === 'client-step-2') {
          bodyHtml = `
            <p style="margin:4px 0 8px;"><strong>How Timeline &amp; Exhibits work together in our ${escapeHtml(area)} Example:</strong><br>
            Each timeline event records an observable date and links to an Exhibit label (<code>Ex. A</code>, <code>Ex. B</code>) with page callouts:</p>
            <div style="display:grid;gap:8px;">
              ${tl.map(ev => `
                <div style="padding:7px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--accent);">
                  <strong>📅 ${escapeHtml(ev.date)} — ${escapeHtml(ev.title)}</strong> ${ev.exhibitId ? `<span class="exhibit-pill">${escapeHtml(ev.exhibitId)}</span>` : ''}<br>
                  <span style="font-size:0.8rem;color:var(--muted);">${escapeHtml(ev.description)}</span>
                </div>
              `).join('')}
              ${exs.map(e => `
                <div style="padding:7px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--stipulated);">
                  <strong>📎 ${escapeHtml(e.label || e.id)}: ${escapeHtml(e.title)}</strong><br>
                  <span style="font-size:0.8rem;color:var(--muted);"><strong>Proves:</strong> ${escapeHtml(e.purpose)} ${e.visualNotes ? ` · <strong>Page Callout:</strong> ${escapeHtml(String(e.visualNotes))}` : ''}</span>
                </div>
              `).join('')}
            </div>
          `;
        } else if (stepId === 'client-step-3' || stepId === 'court-step-1') {
          const t = traps[0];
          bodyHtml = t ? `
            <p style="margin:4px 0 8px;"><strong>How Cross-Examination Preparation works in our ${escapeHtml(area)} Example:</strong><br>
            Instead of arguing when asked a hostile question, pause, avoid the emotional trap, and pivot calmly to the written exhibit:</p>
            <div style="padding:10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--warning);">
              <div><strong>🎯 Example Hostile Question (${escapeHtml(t.title)}):</strong> "${escapeHtml(t.question)}"</div>
              <div style="margin-top:4px;color:var(--danger);"><strong>⛔ Trap to Avoid:</strong> ${escapeHtml(t.avoid)}</div>
              <div style="margin-top:4px;color:var(--stipulated);"><strong>✅ Calm Witness Answer:</strong> "${escapeHtml(t.response)}" ${t.exhibitId ? `<span class="exhibit-pill">${escapeHtml(t.exhibitId)}</span>` : ''}</div>
              ${t.rule106Context ? `<div style="margin-top:4px;font-size:0.8rem;color:var(--accent);"><strong>📜 FRE 106 Full Context:</strong> ${escapeHtml(t.rule106Context)}</div>` : ''}
            </div>
          ` : '';
        } else if (stepId === 'client-step-4' || stepId === 'court-step-2') {
          bodyHtml = `
            <p style="margin:4px 0 8px;"><strong>How Direct Examination Q&amp;As work in our ${escapeHtml(area)} Example:</strong><br>
            Direct questions are open-ended (<em>Who, What, When, How</em>) and cue when to offer an exhibit into evidence:</p>
            <div style="display:grid;gap:8px;">
              ${dxs.map(d => `
                <div style="padding:8px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--stipulated);">
                  <div><span class="badge info">${escapeHtml(d.chapter || 'Direct')}</span> ${d.movesToAdmit ? `<span class="badge stip">📎 Move to Admit ${escapeHtml(d.exhibitId || '')}</span>` : ''}</div>
                  <div style="margin-top:4px;"><strong>Q:</strong> ${escapeHtml(d.question)}</div>
                  <div style="margin-top:2px;color:var(--muted);"><strong>A:</strong> "${escapeHtml(d.answer)}"</div>
                </div>
              `).join('')}
            </div>
          `;
        } else if (stepId === 'counsel-step-2') {
          const c = claims[0];
          const ex = excs[0];
          const prop = c ? compileClaimProposition(c) : null;
          bodyHtml = `
            <p style="margin:4px 0 8px;"><strong>How Statutory Claims &amp; Rule Exceptions work in our ${escapeHtml(area)} Example:</strong></p>
            ${c ? `
              <div style="padding:8px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--stipulated);margin-bottom:6px;">
                <strong>Example Claim (<code>${escapeHtml(c.statute)}</code>):</strong> ${escapeHtml(c.statement)}<br>
                <span style="font-size:0.8rem;color:var(--stipulated);"><strong>Compiled Court Finding:</strong> ${escapeHtml(prop.text)}</span>
              </div>
            ` : ''}
            ${ex ? `
              <div style="padding:8px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--accent);">
                <strong>Example Statutory Exception (<code>${escapeHtml(ex.rule || ex.statute)}</code>):</strong> ${escapeHtml(ex.effect)}
              </div>
            ` : ''}
          `;
        } else if (stepId === 'counsel-step-3') {
          const w = wits[0];
          const d = dxs[0];
          bodyHtml = `
            <p style="margin:4px 0 8px;"><strong>How Witness Budgeting &amp; Examination Scripts work in our ${escapeHtml(area)} Example:</strong></p>
            ${w ? `<div style="padding:7px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--accent);margin-bottom:6px;"><strong>Example Witness Allocation:</strong> ${escapeHtml(w.name)} (${escapeHtml(w.role)} · <strong>${w.minutes} min</strong>) — ${escapeHtml(w.scope)}</div>` : ''}
            ${d ? `<div style="padding:7px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--stipulated);"><strong>Example Direct Script Cue:</strong> Q: "${escapeHtml(d.question)}" → A: "${escapeHtml(d.answer)}" (${d.movesToAdmit ? '📎 Move to Admit ' + escapeHtml(d.exhibitId) : 'Testimony'})</div>` : ''}
          `;
        } else if (stepId === 'counsel-step-4' || stepId === 'court-step-3') {
          bodyHtml = `
            <p style="margin:4px 0 8px;"><strong>How Exhibit Foundations &amp; Visual Callouts work in our ${escapeHtml(area)} Example:</strong></p>
            <div style="display:grid;gap:6px;">
              ${exs.map(e => `
                <div style="padding:7px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--stipulated);">
                  <strong>${escapeHtml(e.label || e.id)} — ${escapeHtml(e.title)}</strong> (Foundation: <code>${escapeHtml(e.foundation || 'FRE 901')}</code> · Status: <strong>${escapeHtml(e.status)}</strong>)<br>
                  <span style="font-size:0.8rem;color:var(--muted);"><strong>Proves:</strong> ${escapeHtml(e.purpose)} ${e.visualNotes ? ` · <strong>Visual Forensics:</strong> ${escapeHtml(String(e.visualNotes))}` : ''}</span>
                </div>
              `).join('')}
            </div>
          `;
        } else {
          const a = ags[0];
          bodyHtml = a ? `
            <p style="margin:4px 0 8px;"><strong>How Client–Attorney Alignment &amp; Export work in our ${escapeHtml(area)} Example:</strong></p>
            <div style="padding:8px 10px;border-radius:6px;background:var(--surface);border-left:3px solid var(--accent);">
              <strong>Topic (${escapeHtml(a.topic)}):</strong><br>
              • <em>Client Question:</em> "${escapeHtml(a.questionForCounsel)}"<br>
              • <em>Attorney Guidance:</em> "${escapeHtml(a.counselGuidance)}"
            </div>
          ` : '';
        }

        return `
          <details class="pedagogy-details" style="margin-top:8px;">
            <summary>📘 See Example From a Sample ${escapeHtml(area)} Case: How to Complete This Step ▾</summary>
            ${bodyHtml}
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;padding-top:8px;border-top:1px dashed var(--border);">
              <button type="button" class="btn" data-action-preview-example="${escapeHtml(exMatter.id)}" style="padding:3px 10px;font-size:0.78rem;">👁️ Preview Full ${escapeHtml(area)} Example (Read-Only)</button>
              <button type="button" class="btn" data-action-copy-example="${escapeHtml(exMatter.id)}" style="padding:3px 10px;font-size:0.78rem;">📋 Save a Copy of This Example to My Matters</button>
            </div>
          </details>
        `;
      }

      function renderPedagogyBanner(stepId) {
        const guides = (DATA && DATA.pedagogyGuides) ? DATA.pedagogyGuides : [];
        const g = guides.find(x => x.stepId === stepId);
        if (!g) return '';
        const curMatter = ensureActiveMatter();
        const exMatter = getExampleMatterForArea(curMatter ? curMatter.areaOfLaw : 'Family & Parenting Law');

        let modeNotice = '';
        if (curMatter && curMatter.isExample) {
          modeNotice = `
            <div class="card" style="margin-bottom:12px;padding:12px 16px;background:rgba(3,105,161,0.08);border:2px solid var(--accent);display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;">
              <div>
                <span class="badge info">📘 Reference Example Preview (Not in Your Saved Matters)</span>
                <strong style="margin-left:6px;">${escapeHtml(curMatter.title)}</strong>
                <div style="font-size:0.84rem;color:var(--muted);margin-top:2px;">You are exploring this example case to see how PrismLegal works. It is not saved in your workspace unless you choose to save a copy.</div>
              </div>
              <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <button type="button" class="btn primary" data-action-start-blank="1">+ Start My Own Blank Matter</button>
                <button type="button" class="btn" data-action-copy-example="${escapeHtml(curMatter.id)}">📋 Save a Copy to My Matters</button>
              </div>
            </div>
          `;
        } else if (curMatter && curMatter.isUnsavedDraft) {
          modeNotice = `
            <div class="card" style="margin-bottom:12px;padding:10px 14px;background:var(--surface-alt);border-left:4px solid var(--stipulated);display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;">
              <div style="font-size:0.86rem;">
                <span class="badge stip">✨ New Unsaved Matter Draft</span>
                <strong>Your workspace has no pre-saved default cases.</strong> Enter your specific case facts or documents below so the workspace can build bespoke strategy, claims, and examination scripts from your intake.
              </div>
              <button type="button" class="btn" data-action-preview-example="${escapeHtml(exMatter.id)}" style="padding:4px 10px;font-size:0.78rem;">👁️ Preview ${escapeHtml(exMatter.areaOfLaw)} Example</button>
            </div>
          `;
        }

        return `
          ${modeNotice}
          <aside class="pedagogy-banner" aria-label="Contextual Legal Guidance">
            <div class="pedagogy-banner-top">
              <div>
                <span class="badge stip">💡 Guided Coaching</span>
                <strong>${escapeHtml(g.heading)}</strong>
              </div>
              <span class="badge info">${escapeHtml(g.pole.toUpperCase())}</span>
            </div>
            <p class="pedagogy-tip">${escapeHtml(g.coachingTip)}</p>
            <details class="pedagogy-details">
              <summary>Why Judges Look for This &amp; Governing Legal Rule Context ▾</summary>
              <p style="margin:6px 0 4px;"><strong>Why It Matters in Court:</strong> ${escapeHtml(g.whyItMatters)}</p>
              <p style="margin:0;"><strong>Governing Legal Standard:</strong> <code>${escapeHtml(g.ruleContext)}</code></p>
            </details>
            ${renderStepExampleDrawer(stepId, exMatter)}
          </aside>
        `;
      }

      // In-Browser Intake Classifiers & Per-Node Attention Extrapolation Engine (Zero Defaults · 100% Bespoke to Intake)
      const DOMAIN_AREAS = [
        'Family & Parenting Law',
        'Housing & Tenant Rights',
        'Veterans & Administrative Appeals',
        'Employment & Wage Protection',
        'Consumer, Debt & Small Claims',
        'Civil Litigation & Probate'
      ];

      function intakeVectorEnergy(features) {
        return (features || []).reduce((acc, v) => acc + Math.max(0, Number(v) || 0), 0);
      }

      function intakeDot(xs, ws) {
        let sum = 0;
        const len = Math.min(xs.length, ws.length);
        for (let i = 0; i < len; i++) {
          sum += (Number(xs[i]) || 0) * (Number(ws[i]) || 0);
        }
        return sum;
      }

      function intakeAttend(query, features) {
        const out = [];
        const len = Math.min(query.length, features.length);
        for (let i = 0; i < len; i++) {
          out.push((Number(query[i]) || 0) * (Number(features[i]) || 0));
        }
        return out;
      }

      function intakeRequant(m, shift, bias, x) {
        const div = Math.max(1, Number(shift) || 64);
        const q = Math.floor(((Number(x) + Number(bias)) * Number(m)) / div);
        return Math.max(0, Math.min(255, q));
      }

      function intakeScoreKeys(attended, keys, biases, m, shift) {
        return (keys || []).map((kVec, idx) =>
          intakeRequant(m, shift, (biases && biases[idx]) || 0, intakeDot(attended, kVec))
        );
      }

      function intakeArgmax(scores) {
        let bestVal = 0;
        let bestIdx = -1;
        for (let i = 0; i < (scores || []).length; i++) {
          const val = Number(scores[i]) || 0;
          if (val > bestVal) {
            bestVal = val;
            bestIdx = i;
          }
        }
        return bestIdx;
      }

      const CLASSIFIER_DISPLAY_LABELS = {
        // HEAD-01 / Domain Classifiers
        'DOM-FAM-103': 'Domestic Relations § 14-10-124 & § 14-10-115 (Best Interests & Shared Support)',
        'DOM-HOU-URLTA': 'URLTA § 2.104 & § 4.104 (Implied Warranty of Habitability & Escrow Defense)',
        'DOM-VET-38CFR': '38 U.S.C. § 1110 & 38 C.F.R. §§ 3.102, 4.16, 4.25 (Veterans Benefits & TDIU)',
        'DOM-EMP-ADA': '42 U.S.C. § 12112(b)(5)(A) & 29 U.S.C. § 207 (ADA Accommodation & Wage Act)',
        'DOM-COM-UCC': 'U.C.C. §§ 2-601, 2-608, 2-712 & 15 U.S.C. § 1692g (Commercial & Debt Validation)',
        'DOM-BIZ-DGCL': '8 Del. C. § 144 & RULLCA §§ 408–409 (Fiduciary Accounting & Entire Fairness)',
        // HEAD-02 / Relief Goal Classifiers
        'relief-parenting-and-guideline-support': 'Equal Parenting Schedule & Guideline Support Order (§ 14-10-124)',
        'relief-habitability-repairs-and-abatement': 'Habitability Repair Order, Rent Abatement & Escrow Release (URLTA § 4.104)',
        'relief-schedular-tdiu-and-effective-date': '100% TDIU Rating & Earlier Effective Date Grant (38 C.F.R. § 4.16)',
        'relief-accommodation-and-wage-remedy': 'Workplace Accommodation & Statutory Back-Pay Order (42 U.S.C. § 12112)',
        'relief-contract-rejection-or-validation': 'Nonconforming Goods Rejection & Debt Dismissal Order (U.C.C. § 2-608 / FDCPA)',
        'relief-fiduciary-accounting-and-distributions': 'Books-and-Records Accounting & Pro-Rata Distribution Order (RULLCA § 408)',
        // HEAD-03 / Timeline Event Classifiers
        'event-caregiving-and-schedule-compliance': 'Verified Caregiving & Parenting Schedule Compliance Log',
        'event-repair-notice-and-escrow-deposit': 'Written Habitability Defect Notice & Court Escrow Deposit',
        'event-claim-filing-and-medical-opinion': 'Service Filing & Nexus Medical Examination Record',
        'event-accommodation-request-and-response': 'Accommodation Request & Interactive Process Record',
        'event-notice-of-dispute-or-nonconformity': 'Written Notice of Nonconformity & Debt Validation Demand',
        'event-agreement-execution-and-audit': 'Operating Agreement Execution & Ledger Reconciliation Audit',
        // HEAD-04 / Exhibit Foundation Classifiers
        'fre-901-authenticated-log': 'FRE 901(b)(1) Authenticated Record & Contemporaneous Log',
        'fre-803-6-business-record': 'FRE 803(6) Certified Business & Financial Record',
        'fre-801d2-opposing-admission': 'FRE 801(d)(2) Opposing Party Statement & Admission',
        'fre-106-completeness-context': 'FRE 106 Rule of Completeness Full Context Document',
        'frcp-26e-disclosure-audit': 'FRCP 26(e) / Rule 16.2 Mandatory Financial Disclosure Record',
        'fre-1006-voluminous-summary': 'FRE 1006 Voluminous Financial Ledger Summary & Tie-Out',
        // HEAD-05 / Statutory Claim Classifiers
        'claim-best-interests-allocation': 'Domestic Relations § 14-10-124 & § 14-10-115 Best-Interests & Support Allocation',
        'claim-warranty-habitability-breach': 'URLTA § 2.104 & § 4.104 Implied Warranty of Habitability & Rent Abatement',
        'claim-tdiu-service-connection': '38 C.F.R. § 4.16(a) & § 3.102 Service-Connected TDIU & Benefit of the Doubt',
        'claim-ada-reasonable-accommodation': '42 U.S.C. § 12112(b)(5)(A) Reasonable Accommodation & Interactive Process',
        'claim-ucc-or-fdcpa-compliance': 'U.C.C. § 2-608 Revocation of Acceptance & 15 U.S.C. § 1692g Debt Validation',
        'claim-fiduciary-duty-accounting': '8 Del. C. § 144 & RULLCA § 409 Fiduciary Accounting & Entire Fairness',
        // HEAD-06 / Witness Roster Classifiers
        'witness-coparent-and-corroborator': 'Co-Parent & Corroborating Caregiving Witness Scope',
        'witness-tenant-and-code-inspector': 'Tenant & Municipal Building Code Inspector Scope',
        'witness-claimant-and-medical-examiner': 'Veteran Claimant & Independent Medical Nexus Examiner Scope',
        'witness-employee-and-hr-representative': 'Employee & Workplace HR Compliance Witness Scope',
        'witness-contract-party-and-custodian': 'Contracting Party & Account Records Custodian Scope',
        'witness-member-and-forensic-accountant': 'Managing Member & Forensic Accounting Witness Scope',
        // HEAD-07 / Trap & Rebuttal Classifiers
        'documentary-impeachment': 'Documentary Impeachment via Authenticated Exhibit',
        'statutory-factor-deduction': 'Statutory Factor Deduction & Element Tie-Out',
        'stipulated-anchor-lock': 'Pretrial Stipulation Anchor & Burden Lock',
        'calm-opening-pivot': 'Calm Fact-Anchored Affirmative Pivot',
        'fre-106-completeness-restoration': 'FRE 106 Rule of Completeness Context Restoration',
        'affirmative-cure-and-mitigation': 'Affirmative Cure, Escrow Compliance & Mitigation Proof',
        // HEAD-08 / Direct Exam Classifiers
        'dx-parenting-and-financial-walkthrough': 'Parenting Routine & Verified Financial Disclosure Walkthrough',
        'dx-habitability-notice-and-escrow': 'Written Defect Notice, Code Citation & Rent Escrow Walkthrough',
        'dx-service-history-and-functional-limits': 'In-Service Event, Medical Nexus & Functional Limitation Walkthrough',
        'dx-essential-duties-and-accommodation': 'Essential Job Functions & Accommodation Request Walkthrough',
        'dx-contract-terms-and-validation-demand': 'Contract Specifications, Nonconformity Notice & Validation Walkthrough',
        'dx-governance-instrument-and-ledger-audit': 'Operating Agreement Authority & General Ledger Audit Walkthrough',
        // HEAD-09 / Visual Forensics Classifiers
        'vis-schedule-log-and-notebook-completeness': 'Custody Calendar & FRE 106 Full Notebook Callout',
        'vis-inspection-citation-and-escrow-receipts': 'Municipal Inspection Citation & Bank Escrow Receipt Callout',
        'vis-rating-code-sheet-and-nexus-opinion': 'VA Rating Code Sheet & Medical Nexus Rationale Callout',
        'vis-evaluation-metrics-and-hr-thread': 'Performance Evaluation Metrics & HR Correspondence Callout',
        'vis-validation-letter-and-assignment-gap': 'Written Dispute Notice & Chain-of-Assignment Gap Callout',
        'vis-operating-clause-and-k1-reconciliation': 'Operating Agreement Clause & Schedule K-1 Tie-Out Callout',
        // HEAD-10 / Calculator Classifiers
        'calc-family-305-shared-support': 'Shared-Custody § 305 Child Support & 1.5× Cross-Credit Calculator',
        'calc-housing-urlta-rent-abatement': 'URLTA Habitability Rent Abatement & Escrow Offset Calculator',
        'calc-veterans-38cfr-combined-rating': '38 C.F.R. § 4.25 Combined Disability & § 4.16 TDIU Threshold Calculator',
        'calc-employment-backpay-and-damages': 'Lost Wages, Mitigation Offset & Statutory Damages Calculator',
        'calc-commercial-ucc-cover-damages': 'U.C.C. § 2-712 Cover Damages & Offset Calculator',
        'calc-fiduciary-disgorgement-surcharge': 'Fiduciary Disgorgement & Pro-Rata Distribution Surcharge Calculator',
        // HEAD-11 / Hearing Clock Classifiers
        'clock-evidentiary-Custody-hearing': 'Domestic Relations Evidentiary Hearing Clock Allocation',
        'clock-housing-abatement-hearing': 'Habitability & Rent Escrow Evidentiary Hearing Clock Allocation',
        'clock-administrative-review-hearing': 'Administrative & Veterans Appeal Hearing Clock Allocation',
        'clock-workplace-remedy-hearing': 'Employment & Accommodation Evidentiary Hearing Clock Allocation',
        'clock-commercial-dispute-hearing': 'Commercial Contract & Debt Validation Hearing Clock Allocation',
        'clock-fiduciary-accounting-hearing': 'Fiduciary Accounting & Governance Hearing Clock Allocation',
        // HEAD-12 / Agenda Classifiers
        'agenda-stipulations-and-disclosure-audit': 'Pretrial Stipulations & Rule 16.2 Financial Disclosure Alignment',
        'agenda-escrow-release-and-inspection': 'Municipal Inspection Admission & Escrow Disbursement Alignment',
        'agenda-effective-date-and-nexus': 'Earlier Effective Date & Medical Nexus Corroboration Alignment',
        'agenda-interactive-process-and-mitigation': 'Interactive Process Timeline & Wage Mitigation Alignment',
        'agenda-chain-of-title-and-hearsay-motion': 'Chain-of-Title Foundation & Business Record Objection Alignment',
        'agenda-fre1006-summary-and-audit-scope': 'FRE 1006 Voluminous Ledger Summary & Audit Scope Alignment',
        // HEAD-19 / Multi-Modal Upload Classifiers
        'modality-pleading-or-court-order': 'FRE 901(b)(7) / 902 Certified Pleading or Municipal/Court Order',
        'modality-financial-ledger-or-tax-csv': 'FRE 803(6) & FRE 1006 Financial Ledger, Escrow Receipt or Tax Schedule',
        'modality-visual-photo-or-premises-media': 'FRE 901(b)(1) Authenticated Photographic or Visual Inspection Evidence',
        'modality-handwritten-notebook-or-scan': 'FRE 106 & FRE 803(5) Contemporaneous Log or Scanned Notebook',
        'modality-digital-message-or-email-thread': 'FRE 901(b)(4) & FRE 801(d)(2) Authenticated Written Correspondence Thread',
        'modality-official-certificate-or-medical-record': 'FRE 803(4) & FRE 902 Official Agency Certificate or Medical Record',
        // HEAD-20 / Jural Posture Classifiers
        'jural-enforceable-claim-right-and-duty': 'Enforceable Claim-Right & Correlative Statutory Duty',
        'jural-joint-governance-authority': 'Joint Decision-Making Authority & Equal Governance Liberty',
        'jural-statutory-benefit-immunity': 'Statutory Benefit Protection & Income Imputation Shield',
        'jural-disclosure-reopening-remedy': 'Mandatory Disclosure Reopening Power & Omitted-Asset Remedy',
        'jural-completeness-restoration-right': 'FRE 106 Contemporaneous Completeness Restoration Right',
        'jural-fiduciary-accounting-entitlement': 'Books-and-Records Inspection Right & Fiduciary Accounting Duty',
        // HEAD-21 / Filing Artifact Classifiers
        'filing-parenting-and-support-position-statement': 'Verified Domestic Relations Position Statement & Parenting Plan',
        'filing-habitability-abatement-and-escrow-motion': 'Verified Motion for Habitability Rent Abatement & Escrow Release',
        'filing-veterans-tdiu-and-nexus-brief': 'Claimant Appellate Brief for 100% TDIU & Earlier Effective Date',
        'filing-workplace-accommodation-and-remedy-brief': 'Pretrial Memorandum on Reasonable Accommodation & Wage Remedies',
        'filing-commercial-validation-and-rejection-brief': 'Trial Brief on Revocation of Acceptance & Statutory Debt Validation',
        'filing-fiduciary-accounting-and-audit-petition': 'Verified Petition for Fiduciary Accounting & Pro-Rata Distribution',
        // HEAD-22 / Filing Deadline Classifiers
        'deadline-mandatory-financial-and-exhibit-disclosures': 'Rule 16.2 Mandatory Financial Affidavit & Pretrial Exhibit Exchange Schedule',
        'deadline-municipal-inspection-and-escrow-notice': 'URLTA § 4.104 Written Notice, Escrow Deposit & Inspection Filing Schedule',
        'deadline-administrative-record-and-medical-submission': '38 C.F.R. Supplemental Nexus Submission & Hearing Brief Schedule',
        'deadline-interactive-process-and-pretrial-exchange': 'Pretrial Witness, Exhibit & Accommodation Record Exchange Schedule',
        'deadline-statutory-validation-and-cure-window': '15 U.S.C. § 1692g 30-Day Validation Window & Pretrial Filing Schedule',
        'deadline-books-and-records-and-summary-tieout': 'FRE 1006 Voluminous Summary Notice & Accounting Exchange Schedule'
      };

      function formatClassifierLabel(rawLabel) {
        if (!rawLabel) return '';
        const key = String(rawLabel).trim();
        if (CLASSIFIER_DISPLAY_LABELS[key]) {
          return CLASSIFIER_DISPLAY_LABELS[key];
        }
        return key
          .replace(/-/g, ' ')
          .replace(/\b(fre|frcp|ucc|urlta|ada|tdiu|cfr|usc|dgcl|rullca|fdcpa)\b/gi, m => m.toUpperCase())
          .replace(/\b\w/g, c => c.toUpperCase());
      }

      function evalIntakeNode(head, features) {
        const energy = intakeVectorEnergy(features);
        if (energy <= 0) {
          return {
            headId: head.id,
            nodeId: head.nodeId,
            schemaId: head.schemaId,
            valid: false,
            energy: 0,
            classIndex: -1,
            classLabel: '',
            rawClassLabel: '',
            scores: [0, 0, 0, 0, 0, 0],
            inductiveRelation: '',
            deductiveStrategy: ''
          };
        }
        const attended = intakeAttend(head.query || [4, 4, 4, 4, 4, 4, 2, 2], features);
        const scores = intakeScoreKeys(attended, head.keys || [], head.biases || [0, 0, 0, 0, 0, 0], head.multiplier || 1, head.shift || 64);
        const classIdx = intakeArgmax(scores);
        const labels = head.classLabels || [];
        if (classIdx < 0) {
          return {
            headId: head.id,
            nodeId: head.nodeId,
            schemaId: head.schemaId,
            valid: false,
            energy: energy,
            classIndex: -1,
            classLabel: '',
            rawClassLabel: '',
            scores: scores,
            inductiveRelation: '',
            deductiveStrategy: ''
          };
        }
        const rawCls = labels[classIdx] || '';
        return {
          headId: head.id,
          nodeId: head.nodeId,
          schemaId: head.schemaId,
          valid: true,
          energy: energy,
          classIndex: classIdx,
          classLabel: formatClassifierLabel(rawCls),
          rawClassLabel: rawCls,
          scores: scores,
          inductiveRelation: head.inductiveRelation || '',
          deductiveStrategy: formatClassifierLabel(head.deductiveStrategy || '')
        };
      }

      function extractIntakeFeatureVector(matter, extraText) {
        const cfg = (DATA && DATA.intakeClassifier) ? DATA.intakeClassifier : {};
        const channels = cfg.featureChannels || [];
        const m = matter || {};
        const corpusParts = [
          m.title || '',
          m.summary || '',
          m.forum || '',
          m.docketNumber || '',
          m.clientName || '',
          m.opposingParty || '',
          extraText || ''
        ];
        (m.reliefGoals || m.goals || []).forEach(g => {
          corpusParts.push(g.title || '', g.requestedOrder || '', g.rationale || '');
        });
        (m.timeline || []).forEach(ev => {
          corpusParts.push(ev.date || '', ev.title || '', ev.description || '', ev.exhibitId || '');
        });
        (m.exhibits || []).forEach(ex => {
          corpusParts.push(ex.title || '', ex.purpose || '', ex.foundation || '');
        });
        (m.claims || []).forEach(c => {
          corpusParts.push(c.statute || '', c.statement || '');
        });
        (m.traps || []).forEach(t => {
          corpusParts.push(t.title || '', t.question || '', t.response || '');
        });
        const corpus = corpusParts.join(' ').trim().toLowerCase();

        // Zero baseline: empty intake must produce [0, 0, 0, 0, 0, 0, 0, 0]
        const vec = [0, 0, 0, 0, 0, 0, 0, 0];
        if (!corpus) {
          return vec;
        }

        channels.forEach((ch, idx) => {
          if (idx >= 8) return;
          let hits = 0;
          (ch.keywords || []).forEach(kw => {
            if (kw && corpus.includes(String(kw).toLowerCase())) {
              hits += 1;
            }
          });
          vec[idx] += hits * 42;
        });

        // If user explicitly selected an areaOfLaw AND provided substantive intake text/items, weight that domain channel
        const areaBoostIdx = DOMAIN_AREAS.findIndex(a =>
          String(m.areaOfLaw || '').toLowerCase().includes(a.split(' ')[0].toLowerCase())
        );
        if (areaBoostIdx >= 0 && areaBoostIdx < 6 && corpus.length > 0) {
          vec[areaBoostIdx] += 64;
        }

        // Documentary and contestation channels from actual user items or text tokens
        const docTokens = (corpus.match(/\b(exhibit|ex\.|record|receipt|statement|contract|agreement|notice|report|inspection|ledger|bank|email|letter|log|photo|certificate|order)\b/g) || []).length;
        const contestTokens = (corpus.match(/\b(dispute|contest|deny|denied|omitted|conceal|imput|restrict|alleg|object|hearsay|incomplete|excerpt|breach|violation)\b/g) || []).length;
        vec[6] += ((m.exhibits || []).length * 36) + ((m.timeline || []).length * 24) + (docTokens * 28);
        vec[7] += ((m.traps || []).length * 36) + ((m.claims || []).length * 24) + (contestTokens * 28);

        // If the user entered bespoke prose that didn't hit a predefined keyword, still project its token energy onto the active domain & documentary channels
        const totalSoFar = intakeVectorEnergy(vec);
        if (totalSoFar === 0 && corpus.length >= 3) {
          const domIdx = areaBoostIdx >= 0 ? areaBoostIdx : (corpus.charCodeAt(0) % 6);
          vec[domIdx] = Math.min(255, corpus.length * 4);
          vec[6] = Math.min(255, corpus.length * 3);
        }

        return vec.map(v => Math.max(0, Math.min(255, Math.round(v))));
      }

      function classifyMatterIntake(matter, extraText) {
        const cfg = (DATA && DATA.intakeClassifier) ? DATA.intakeClassifier : {};
        const heads = cfg.attentionHeads || [];
        const schemas = cfg.schemaClassifiers || [];
        const features = extractIntakeFeatureVector(matter, extraText);
        const energy = intakeVectorEnergy(features);
        if (energy <= 0) {
          return {
            valid: false,
            energy: 0,
            features,
            domainIndex: -1,
            inferredArea: '',
            nodeResults: {},
            schemaResults: {}
          };
        }
        const nodeResults = {};
        const schemaResults = {};
        heads.forEach(h => {
          const res = evalIntakeNode(h, features);
          nodeResults[h.nodeId] = res;
          if (!schemaResults[h.schemaId]) {
            schemaResults[h.schemaId] = res;
          }
        });
        schemas.forEach(sc => {
          if (!schemaResults[sc.id] && nodeResults['node-case-meta']) {
            schemaResults[sc.id] = nodeResults['node-case-meta'];
          }
        });
        const primary = nodeResults['node-case-meta'] || { valid: false, classIndex: -1, classLabel: '' };
        const inferredArea = (primary.classIndex >= 0 && DOMAIN_AREAS[primary.classIndex])
          ? DOMAIN_AREAS[primary.classIndex]
          : ((matter && matter.areaOfLaw) || '');
        return {
          valid: true,
          energy,
          features,
          domainIndex: primary.classIndex,
          inferredArea,
          nodeResults,
          schemaResults
        };
      }

      function classifyExhibitIntake(ex, matter) {
        if (!ex) return ex;
        const rawTitle = String(ex.title || '').trim();
        const rawPurpose = String(ex.purpose || '').trim();
        const rawFoundation = String(ex.foundation || '').trim();
        if (!rawTitle && !rawPurpose) {
          return ex;
        }
        const text = `${rawTitle} ${rawPurpose} ${rawFoundation} ${ex.category || ''}`.toLowerCase();
        const cfg = (DATA && DATA.intakeClassifier) ? DATA.intakeClassifier : {};
        const heads = cfg.attentionHeads || [];
        const exHead = heads.find(h => h.id === 'HEAD-04') || heads[3];
        const features = extractIntakeFeatureVector(matter, text);
        if (text.includes('bank') || text.includes('tax') || text.includes('certified') || text.includes('medical') || text.includes('invoice') || text.includes('inspection') || text.includes('pay') || text.includes('statement') || text.includes('receipt') || text.includes('agency') || text.includes('report')) {
          features[6] = Math.max(features[6], 240);
        }
        if (text.includes('journal') || text.includes('diary') || text.includes('log') || text.includes('excerpt') || text.includes('selective') || text.includes('message') || text.includes('text') || text.includes('email') || text.includes('thread')) {
          features[7] = Math.max(features[7], 235);
        }
        const nodeEval = exHead ? evalIntakeNode(exHead, features) : { valid: false, classIndex: -1, classLabel: '' };
        const clsLabel = nodeEval.classLabel || '';

        const dateMatch = (rawTitle + ' ' + rawPurpose).match(/\b(\d{4}-\d{2}-\d{2}|\d{1,2}\/\d{1,2}\/\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}|\b20\d{2}\b)/i);
        const moneyMatch = (rawTitle + ' ' + rawPurpose).match(/\$[0-9,]+(?:\.\d{2})?/);
        const pageMatch = (rawTitle + ' ' + rawPurpose).match(/\b(?:p\.|pp\.|page|pages|§|sec\.|section)\s*[0-9A-Za-z.\-–]+/i);

        if (!rawFoundation) {
          ex.foundation = clsLabel || 'FRE 901(b)(1) Authenticated Record';
        }
        if (!rawPurpose) {
          const partyRef = (matter && matter.clientName) ? ` for ${matter.clientName}` : '';
          const dateRef = dateMatch ? ` dated ${dateMatch[0]}` : '';
          const moneyRef = moneyMatch ? ` quantifying ${moneyMatch[0]}` : '';
          ex.purpose = `Establishes the facts recorded in ${rawTitle}${dateRef}${moneyRef}${partyRef} under ${ex.foundation}.`;
        }
        if (!ex.visualNotes) {
          const calloutParts = [];
          if (dateMatch) calloutParts.push(`Dated entry (${dateMatch[0]})`);
          if (moneyMatch) calloutParts.push(`figure callout (${moneyMatch[0]})`);
          if (pageMatch) calloutParts.push(`reference (${pageMatch[0]})`);
          ex.visualNotes = calloutParts.length > 0
            ? `${rawTitle}: verify ${calloutParts.join(', ')} under ${ex.foundation}.`
            : `${rawTitle}: verify operative text and authentication markings under ${ex.foundation}.`;
        }
        if (!ex.pivotIntent) {
          ex.pivotIntent = `Offers ${rawTitle || ex.label || 'exhibit'} (${ex.foundation}) to prove: ${ex.purpose}`;
        }
        return ex;
      }

      function parseIntakeClauses(text) {
        if (!text || !String(text).trim()) return [];
        const protectedText = String(text)
          .replace(/\b(No|Nos|Sec|Secs|Ex|Exs|v|vs|p|pp|Inc|Co|Corp|LLC|Dept|Dr|Mr|Ms|Mrs|Jr|Sr)\.\s+/gi, '$1\u00A0')
          .replace(/\b(U\.S\.C|C\.F\.R|Del\.\s*C)\.\s+/gi, '$1\u00A0');
        return protectedText
          .split(/(?:[\n\r]+|(?<=[.?!;])\s+)/)
          .map(s => s.replace(/\u00A0/g, '. ').replace(/^(?:Case\s+No\.\s*[0-9A-Za-z\-]+\.?\s*)/i, '').trim())
          .filter(s => s.length >= 8 && !/^[0-9]{2,4}-[A-Z]{2,5}-[0-9]{3,6}\.?$/i.test(s));
      }

      function extrapolateCaseFromIntake(matter, options) {
        if (!matter || matter.isExample) return matter;
        normalizeMatter(matter);

        // 1. Evaluate intake feature vector & 18 node attention heads.
        // Zero-default invariant: if the intake has zero feature energy, output NOTHING.
        const rawText = `${matter.title || ''} ${matter.summary || ''}`.trim();
        const classification = classifyMatterIntake(matter, rawText);
        if (!classification.valid || classification.energy <= 0) {
          return matter;
        }

        const cfg = (DATA && DATA.intakeClassifier) ? DATA.intakeClassifier : {};
        const heads = cfg.attentionHeads || [];
        const findHead = (id) => heads.find(h => h.id === id) || heads[0];

        // 2. Infer Area of Law & Governing Statutory Framework from HEAD-01 & positive keyword hits
        const chs = cfg.featureChannels || [];
        let bestCh = -1;
        let bestHits = 0;
        const lowerIntake = `${rawText} ${(matter.reliefGoals || []).map(g => g.title + ' ' + g.requestedOrder).join(' ')} ${(matter.exhibits || []).map(e => e.title + ' ' + e.purpose).join(' ')}`.toLowerCase();
        for (let i = 0; i < 6; i++) {
          const kws = (chs[i] && chs[i].keywords) ? chs[i].keywords : [];
          let hits = 0;
          kws.forEach(k => { if (k && lowerIntake.includes(String(k).toLowerCase())) hits++; });
          if (hits > bestHits) {
            bestHits = hits;
            bestCh = i;
          }
        }
        if (bestCh >= 0 && bestHits > 0) {
          matter.areaOfLaw = DOMAIN_AREAS[bestCh];
          matter.practiceArea = matter.areaOfLaw;
        } else if (!matter.areaOfLaw && classification.inferredArea) {
          matter.areaOfLaw = classification.inferredArea;
          matter.practiceArea = matter.areaOfLaw;
        }

        const head01Res = classification.nodeResults['node-case-meta'] || evalIntakeNode(findHead('HEAD-01'), classification.features);
        const head05Res = classification.nodeResults['node-statutory-matrix'] || evalIntakeNode(findHead('HEAD-05'), classification.features);
        if (!matter.framework && head05Res && head05Res.classLabel) {
          matter.framework = head05Res.classLabel;
        }

        // Parse bespoke clauses, dates, monetary amounts, and quantities from the user's intake
        const clauses = parseIntakeClauses(`${matter.summary || ''}\n${matter.title || ''}`);
        const allIntakeText = [
          matter.title || '',
          matter.summary || '',
          ...(matter.reliefGoals || []).map(g => `${g.title || ''} ${g.requestedOrder || ''} ${g.rationale || ''}`),
          ...(matter.timeline || []).map(t => `${t.date || ''} ${t.title || ''} ${t.description || ''}`),
          ...(matter.exhibits || []).map(e => `${e.title || ''} ${e.purpose || ''}`)
        ].join(' ');

        const extractedMoney = (allIntakeText.match(/\$[0-9,]+(?:\.\d{2})?(?:\/mo|\/month|\/yr|\/year)?/gi) || []);
        const extractedPcts = (allIntakeText.match(/\b\d{1,3}(?:\.\d+)?%\b|\b50\/50\b/g) || []);
        const clientLabel = (matter.clientName || '').trim();
        const opposingLabel = (matter.opposingParty || '').trim();
        const partyPrefix = clientLabel ? clientLabel : (matter.clientRole || 'Proponent');

        // Synthesize bespoke summary ONLY if summary is blank and user entered other substantive fields
        if (!matter.summary && (matter.title || (matter.reliefGoals && matter.reliefGoals.length) || (matter.exhibits && matter.exhibits.length))) {
          const goalPhrases = (matter.reliefGoals || []).map(g => g.requestedOrder || g.title).filter(Boolean);
          const exPhrases = (matter.exhibits || []).map(e => `${e.label || e.id}: ${e.title}`).filter(Boolean);
          const parts = [];
          if (matter.title) parts.push(`${partyPrefix} matter in ${matter.title}`);
          if (opposingLabel) parts.push(`opposing ${opposingLabel}`);
          if (matter.framework) parts.push(`governed by ${matter.framework}`);
          if (goalPhrases.length) parts.push(`seeking ${goalPhrases.join('; ')}`);
          if (exPhrases.length) parts.push(`corroborated by ${exPhrases.join(', ')}`);
          matter.summary = parts.join(' — ') + '.';
        }

        // 3. Bespoke Relief Goals (HEAD-02: node-relief-posture) synthesized directly from intake clauses or exhibits
        matter.reliefGoals = matter.reliefGoals || [];
        if (matter.reliefGoals.length === 0 && clauses.length > 0) {
          const head02 = findHead('HEAD-02');
          clauses.slice(0, 4).forEach((clause, idx) => {
            const cFeat = extractIntakeFeatureVector(matter, clause);
            const h2 = evalIntakeNode(head02, cFeat);
            const postureTag = (h2 && h2.classLabel) ? h2.classLabel : 'Requested Relief Order';
            matter.reliefGoals.push({
              id: 'GOAL-' + String(idx + 1).padStart(2, '0'),
              title: `${postureTag} (${idx + 1})`,
              requestedOrder: clause,
              rationale: `Grounded in ${partyPrefix}'s intake factual proposition${matter.framework ? ' under ' + matter.framework : ''}.`
            });
          });
        } else if (matter.reliefGoals.length === 0 && (matter.exhibits || []).length > 0) {
          const head02 = findHead('HEAD-02');
          matter.exhibits.slice(0, 3).forEach((ex, idx) => {
            const cFeat = extractIntakeFeatureVector(matter, `${ex.title} ${ex.purpose}`);
            const h2 = evalIntakeNode(head02, cFeat);
            const postureTag = (h2 && h2.classLabel) ? h2.classLabel : 'Evidentiary Relief Order';
            matter.reliefGoals.push({
              id: 'GOAL-' + String(idx + 1).padStart(2, '0'),
              title: `${postureTag} — ${ex.label || ex.id}`,
              requestedOrder: `Enter order granting relief established by ${ex.title} (${ex.label || ex.id}): ${ex.purpose || ex.title}`,
              rationale: `Directly corroborated by ${ex.label || ex.id} (${ex.foundation || 'Authenticated Record'}).`
            });
          });
        }
        matter.goals = matter.reliefGoals;

        // 4. Bespoke Exhibits (HEAD-04: node-exhibit-admission) — only extracted when intake clauses or timeline mention records/documents
        matter.exhibits = matter.exhibits || [];
        matter.timeline = matter.timeline || [];
        const docRegex = /\b(exhibit\s+[a-z0-9-]+|ex\.\s*[a-z0-9-]+|agreement|contract|lease|notice|inspection|report|receipt|escrow|statement|ledger|worksheet|return|w-2|k-1|1099|evaluation|review|rating|nexus|email|message|thread|log|journal|certificate|order|record|invoice|bill of sale)\b/i;

        if (matter.exhibits.length === 0) {
          clauses.forEach(clause => {
            const match = clause.match(docRegex);
            if (match && matter.exhibits.length < 6) {
              const idx = matter.exhibits.length;
              const lbl = `Ex. ${String.fromCharCode(65 + idx)}`;
              const matchedWord = match[0];
              const cleanTitle = clause.length <= 78 ? clause : `${matchedWord.charAt(0).toUpperCase() + matchedWord.slice(1)} — ${clause.slice(0, 64).trim()}…`;
              const dateInClause = clause.match(/\b(\d{4}-\d{2}-\d{2}|\d{1,2}\/\d{1,2}\/\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}|\b20\d{2}\b)/i);
              matter.exhibits.push(classifyExhibitIntake({
                id: `Ex-${String.fromCharCode(65 + idx)}`,
                label: lbl,
                party: partyPrefix,
                title: cleanTitle,
                date: dateInClause ? dateInClause[0] : '',
                purpose: clause,
                status: 'Ready to Offer'
              }, matter));
            }
          });
        }

        // Classify any existing user exhibits so their bespoke foundations/callouts are populated from their own text
        matter.exhibits = matter.exhibits.map(ex => classifyExhibitIntake(ex, matter));

        // Cross-link timeline events that reference an exhibit label not yet in matter.exhibits
        matter.timeline.forEach(ev => {
          const refLbl = (ev.exhibitId || ev.exhibitLabel || '').trim();
          if (refLbl && !matter.exhibits.some(e => (e.label || e.id) === refLbl)) {
            matter.exhibits.push(classifyExhibitIntake({
              id: refLbl.replace(/[^A-Za-z0-9_-]/g, '-'),
              label: refLbl,
              party: partyPrefix,
              title: `${ev.title}${ev.date ? ' (' + ev.date + ')' : ''}`,
              date: ev.date || '',
              purpose: ev.description || ev.title,
              status: 'Ready to Offer'
            }, matter));
          }
        });

        // 5. Bespoke Chronological Timeline (HEAD-03: node-chronology) — only created when actual dates exist in intake clauses or dated exhibits
        if (matter.timeline.length === 0) {
          const dateRegex = /\b(\d{4}-\d{2}-\d{2}|\d{1,2}\/\d{1,2}\/\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}|\b(?:19|20)\d{2}\b)/i;
          clauses.forEach((clause) => {
            const dm = clause.match(dateRegex);
            if (dm) {
              const linkedEx = matter.exhibits.find(e => e.purpose === clause || (e.date && e.date === dm[0]));
              const exLbl = linkedEx ? (linkedEx.label || linkedEx.id) : '';
              matter.timeline.push({
                id: 'TL-' + String(matter.timeline.length + 1).padStart(2, '0'),
                date: dm[0],
                title: clause.length <= 64 ? clause : (clause.slice(0, 60).trim() + '…'),
                description: clause,
                exhibitId: exLbl,
                exhibitLabel: exLbl
              });
            }
          });
          matter.exhibits.forEach(ex => {
            if (ex.date && !matter.timeline.some(t => t.date === ex.date && t.exhibitId === (ex.label || ex.id))) {
              matter.timeline.push({
                id: 'TL-' + String(matter.timeline.length + 1).padStart(2, '0'),
                date: ex.date,
                title: ex.title,
                description: ex.purpose || ex.title,
                exhibitId: ex.label || ex.id,
                exhibitLabel: ex.label || ex.id
              });
            }
          });
        }

        // 6. Bespoke Statutory Claims (HEAD-05) & Controlling Rule Overrides (HEAD-13..HEAD-16)
        const availExLabels = matter.exhibits.map(e => e.label || e.id).filter(Boolean);
        matter.claims = matter.claims || [];
        if (matter.claims.length === 0) {
          const head05 = findHead('HEAD-05');
          const sourceItems = matter.reliefGoals.length > 0
            ? matter.reliefGoals.map(g => ({ text: `${g.title}: ${g.requestedOrder}`, rationale: g.rationale }))
            : clauses.map(c => ({ text: c, rationale: '' }));
          sourceItems.slice(0, 4).forEach((item, idx) => {
            const cFeat = extractIntakeFeatureVector(matter, item.text);
            const h5 = evalIntakeNode(head05, cFeat);
            const statuteLabel = (h5 && h5.classLabel) ? h5.classLabel : (matter.framework || 'Governing Statutory Element');
            const linkedExs = availExLabels.length > 0 ? [availExLabels[idx % availExLabels.length]] : [];
            matter.claims.push({
              id: 'CLM-' + String(matter.claims.length + 1).padStart(2, '0'),
              statute: statuteLabel,
              status: linkedExs.length > 0 ? 'corroborated' : 'contested',
              statement: item.text,
              exhibits: linkedExs
            });
          });
        } else if (availExLabels.length > 0) {
          matter.claims.forEach((c, idx) => {
            if (!Array.isArray(c.exhibits) || c.exhibits.length === 0) {
              c.exhibits = [availExLabels[idx % availExLabels.length]];
            }
          });
        }

        matter.ruleExceptions = matter.ruleExceptions || [];
        if (matter.ruleExceptions.length === 0 && (clauses.length > 0 || matter.claims.length > 0)) {
          const head15 = findHead('HEAD-15');
          const head16 = findHead('HEAD-16');
          const h15Res = evalIntakeNode(head15, classification.features);
          const h16Res = evalIntakeNode(head16, classification.features);
          if (h15Res && h15Res.valid && h15Res.classLabel) {
            const anchorStatement = matter.claims[0] ? matter.claims[0].statement : (clauses[0] || '');
            if (anchorStatement) {
              matter.ruleExceptions.push({
                id: 'EXC-01',
                statute: h15Res.classLabel,
                rule: h15Res.classLabel,
                type: (h16Res && h16Res.classLabel) ? h16Res.classLabel : 'Controlling Statutory Override',
                generalRule: opposingLabel ? `Opposing posture asserted by ${opposingLabel}` : 'General statutory baseline',
                effect: `Applies ${h15Res.classLabel} to ${anchorStatement}`,
                exhibitId: availExLabels[0] || ''
              });
            }
          }
        }

        // 7. Bespoke Direct Examination Q&As (HEAD-08 & HEAD-17)
        matter.directExam = matter.directExam || [];
        if (matter.directExam.length === 0) {
          const head08 = findHead('HEAD-08');
          matter.reliefGoals.forEach((g, idx) => {
            const gFeat = extractIntakeFeatureVector(matter, `${g.title} ${g.requestedOrder}`);
            const h8 = evalIntakeNode(head08, gFeat);
            const chLabel = (h8 && h8.classLabel) ? h8.classLabel : 'Requested Relief & Factual Basis';
            const qText = `What specific order are you requesting regarding ${g.title}, and what facts in this matter support it?`;
            matter.directExam.push({
              id: 'DX-' + String(matter.directExam.length + 1).padStart(2, '0'),
              chapter: chLabel,
              section: chLabel,
              visualCue: idx === 0 ? 'yellow-highlight' : 'standard',
              movesToAdmit: false,
              question: qText,
              answer: `${g.requestedOrder}${g.rationale ? ' — ' + g.rationale : ''}`,
              exhibitId: availExLabels[idx] || '',
              exhibitLabel: availExLabels[idx] || '',
              coachingNote: `State the requested order (${g.title}) clearly and anchor to the record.`
            });
          });
        }
        matter.exhibits.forEach(ex => {
          const lbl = ex.label || ex.id;
          if (lbl && !matter.directExam.some(d => (d.exhibitId === lbl || d.exhibitLabel === lbl))) {
            matter.directExam.push({
              id: 'DX-' + String(matter.directExam.length + 1).padStart(2, '0'),
              chapter: 'Exhibit Authentication & Foundation',
              section: 'Exhibit Authentication & Foundation',
              visualCue: 'yellow-highlight',
              movesToAdmit: true,
              question: `Showing you ${lbl} (${ex.title}), how do you recognize this document and what does it establish?`,
              answer: `I recognize ${lbl} as ${ex.title}. It is an accurate record that establishes: ${ex.purpose}`,
              exhibitId: lbl,
              exhibitLabel: lbl,
              counselPrompt: `Move to admit ${lbl} (${ex.title}) pursuant to ${ex.foundation || 'FRE 901'}.`,
              coachingNote: `Identify ${lbl} (${ex.title}) and pause while it is offered into evidence.`
            });
          }
        });

        // 8. Bespoke Cross-Examination Flashcards & FRE 106 Context (HEAD-07 & HEAD-09)
        matter.traps = matter.traps || [];
        if (matter.traps.length === 0 && (matter.claims.length > 0 || matter.exhibits.length > 0)) {
          const head07 = findHead('HEAD-07');
          const pivotSources = matter.claims.length > 0
            ? matter.claims.slice(0, 2).map(c => ({ title: c.statute, fact: c.statement, ex: (c.exhibits && c.exhibits[0]) || availExLabels[0] || '' }))
            : matter.exhibits.slice(0, 2).map(e => ({ title: e.title, fact: e.purpose, ex: e.label || e.id }));
          pivotSources.forEach((src) => {
            const tFeat = extractIntakeFeatureVector(matter, `${src.title} ${src.fact}`);
            const h7 = evalIntakeNode(head07, tFeat);
            const trapTheme = (h7 && h7.classLabel) ? h7.classLabel : src.title;
            matter.traps.push({
              id: 'TRAP-' + String(matter.traps.length + 1).padStart(2, '0'),
              title: `${trapTheme}`,
              question: `If ${opposingLabel || 'opposing counsel'} challenges "${src.fact}", how do you respond?`,
              allegation: `If ${opposingLabel || 'opposing counsel'} challenges "${src.fact}", how do you respond?`,
              avoid: `Do not speculate beyond the written record${src.ex ? ' in ' + src.ex : ''}.`,
              trapWarning: `Do not speculate beyond the written record${src.ex ? ' in ' + src.ex : ''}.`,
              response: `The written record${src.ex ? ' in ' + src.ex : ''} directly establishes that ${src.fact}`,
              rule106Context: src.ex ? `Under FRE 106, request that the complete text of ${src.ex} be read in full context.` : '',
              exhibitId: src.ex,
              exhibits: src.ex ? [src.ex] : [],
              readiness: 'Ready for Hearing'
            });
          });
        }

        // 9. Bespoke Witness Roster (HEAD-06 & HEAD-11) — only created when parties or exhibits exist in intake
        matter.witnesses = matter.witnesses || [];
        if (matter.witnesses.length === 0 && (clientLabel || opposingLabel || availExLabels.length > 0)) {
          const totalMins = Number(matter.hearingMinutes) || 180;
          if (clientLabel || availExLabels.length > 0) {
            matter.witnesses.push({
              id: 'W-01',
              name: clientLabel || partyPrefix,
              role: `${matter.clientRole || 'Proponent'} (Direct Testimony)`,
              status: 'will-call',
              callStatus: 'will-call',
              minutes: Math.max(20, Math.round(totalMins * 0.25)),
              scope: `Testifies to ${matter.reliefGoals.map(g => g.title).join(', ') || matter.title || 'intake facts'}${availExLabels.length ? ' and authenticates ' + availExLabels.join(', ') : ''}.`
            });
          }
          if (opposingLabel) {
            matter.witnesses.push({
              id: 'W-' + String(matter.witnesses.length + 1).padStart(2, '0'),
              name: opposingLabel,
              role: 'Adverse Party (Cross-Examination)',
              status: 'adverse-cross',
              callStatus: 'adverse-cross',
              minutes: Math.max(15, Math.round(totalMins * 0.20)),
              scope: `Cross-examination anchored to ${availExLabels.join(', ') || 'the documentary record'} regarding ${matter.title || 'disputed elements'}.`
            });
          }
        }

        // 10. Bespoke Calculator Extraction (HEAD-10) — strictly from numbers in the user's intake (never defaults)
        matter.calculators = matter.calculators || {};
        if (extractedMoney.length > 0) {
          const numericDollars = extractedMoney
            .map(s => Number(String(s).replace(/[^0-9.]/g, '')))
            .filter(n => !isNaN(n) && n > 0);
          if (numericDollars.length >= 2 && (matter.areaOfLaw || '').toLowerCase().includes('family')) {
            if (matter.calculators.supportParty1Income === undefined) matter.calculators.supportParty1Income = numericDollars[0];
            if (matter.calculators.supportParty2Income === undefined) matter.calculators.supportParty2Income = numericDollars[1];
            if (matter.calculators.supportParty2Nights === undefined && lowerIntake.includes('50/50')) {
              matter.calculators.supportParty2Nights = 182.5;
            }
          } else if (numericDollars.length >= 1) {
            if (matter.calculators.civilContractRate === undefined) matter.calculators.civilContractRate = numericDollars[0];
          }
        }
        if (extractedPcts.length > 0 && (matter.areaOfLaw || '').toLowerCase().includes('veteran')) {
          const pctNums = extractedPcts.map(s => parseInt(s, 10)).filter(n => !isNaN(n) && n > 0 && n <= 100);
          if (pctNums.length > 0 && !matter.calculators.vaRatings) {
            matter.calculators.vaRatings = pctNums.join(', ');
          }
        }

        // 11. Bespoke Client–Counsel Alignment Agenda (HEAD-12)
        matter.agenda = matter.agenda || [];
        if (matter.agenda.length === 0 && (availExLabels.length > 0 || matter.claims.length > 0)) {
          const focusTarget = availExLabels.length > 0 ? availExLabels.join(', ') : (matter.claims[0] ? matter.claims[0].statute : matter.title);
          matter.agenda.push({
            id: 'AG-01',
            topic: `Evidentiary Stipulations & Proof Alignment (${focusTarget})`,
            questionForCounsel: `How should we sequence ${focusTarget} during the hearing to establish our requested orders efficiently?`,
            counselGuidance: `Introduce ${focusTarget} under ${matter.exhibits[0] ? matter.exhibits[0].foundation : (matter.framework || 'governing evidence rules')} and link directly to Claim ${matter.claims[0] ? matter.claims[0].id : 'CLM-01'}.`,
            status: 'Aligned'
          });
        }

        normalizeMatter(matter);
        return matter;
      }

      function compileClaimProposition(claim) {
        const exs = Array.isArray(claim.exhibits) ? claim.exhibits.filter(Boolean) : [];
        if (exs.length === 0) {
          const label = 'Evidentiary Refusal Guard Active';
          return {
            ok: false,
            admissible: false,
            label,
            statusLabel: label,
            text: `Refused for Proposed Court Findings: Claim ${claim.id} (${claim.statute || 'Unanchored'}) has zero linked exhibits. Link at least one documentary exhibit in Step 2 or Step 4 before offering as a proposed finding of fact.`
          };
        }
        const postureWord = claim.status === 'stipulated'
          ? 'Pursuant to pretrial stipulation'
          : (claim.status === 'corroborated' ? 'Upon preponderance of the corroborated record' : 'On the contested evidentiary record');
        const label = 'Compiled Proposed Finding of Fact (' + (claim.statute || 'Statute') + ')';
        return {
          ok: true,
          admissible: true,
          label,
          statusLabel: label,
          text: `${postureWord} and admitted Exhibits ${exs.join(', ')}, the Court finds under ${claim.statute || 'governing law'} that: ${claim.statement}`
        };
      }

      function computeHearingClockStages(totalMinutes, witnesses) {
        const total = Math.max(30, Number(totalMinutes) || 180);
        const openingMins = Math.round(total * 0.10);
        const directMins = Math.round(total * 0.45);
        const crossMins = Math.round(total * 0.30);
        const closingGateMins = Math.max(10, total - openingMins - directMins - crossMins);
        const usedWitnessMins = (witnesses || []).reduce((acc, w) => acc + (Number(w.minutes) || 0), 0);
        const evidentiaryPool = directMins + crossMins;
        const gateProtected = usedWitnessMins <= evidentiaryPool;
        return {
          total,
          openingMins,
          directMins,
          crossMins,
          closingGateMins,
          evidentiaryPool,
          availableExamPool: evidentiaryPool,
          usedWitnessMins,
          usedWitnessMinutes: usedWitnessMins,
          gateProtected,
          overBudget: !gateProtected,
          stages: [
            { name: 'Stage 1: Opening Posture', pct: 10, minutes: openingMins, note: 'Relief goals & stipulations' },
            { name: 'Stage 2: Direct Exam', pct: 45, minutes: directMins, note: 'Affirmative statutory proof' },
            { name: 'Stage 3: Cross & Redirect', pct: 30, minutes: crossMins, note: 'Impeachment & Rule 106 context' },
            { name: 'Stage 4: Protected Closing Gate', pct: 15, minutes: closingGateMins, note: gateProtected ? 'Protected for final orders' : '⚠️ Witness roster exceeds exam pool' }
          ]
        };
      }

      function auditMatterConsistency(matter) {
        const m = normalizeMatter(matter || {});
        const checks = [];
        const goalsCount = (m.reliefGoals || []).length;
        const exs = m.exhibits || [];
        const claims = m.claims || [];
        const traps = m.traps || [];
        const dxs = m.directExam || [];

        checks.push({
          title: 'Relief Goals & Requested Court Orders',
          label: 'Relief Goals & Requested Court Orders',
          ok: goalsCount > 0,
          detail: goalsCount > 0 ? `${goalsCount} specific relief order(s) defined.` : 'No relief goals defined yet in Step 1.'
        });

        const unbackedClaims = claims.filter(c => !c.exhibits || c.exhibits.length === 0);
        checks.push({
          title: 'Statutory Claims Backed by Exhibits',
          label: 'Statutory Claims Backed by Exhibits',
          ok: claims.length > 0 && unbackedClaims.length === 0,
          detail: claims.length === 0
            ? 'No statutory claims mapped yet in Attorney Step 2.'
            : (unbackedClaims.length === 0
              ? `All ${claims.length} statutory claim(s) are backed by exhibits.`
              : `${unbackedClaims.length} claim(s) (${unbackedClaims.map(x => x.id).join(', ')}) lack a supporting exhibit.`)
        });

        const referencedLabels = new Set();
        (m.timeline || []).forEach(t => { if (t.exhibitId) referencedLabels.add(t.exhibitId.trim()); });
        claims.forEach(c => (c.exhibits || []).forEach(x => referencedLabels.add(x.trim())));
        traps.forEach(t => (t.exhibits || []).forEach(x => referencedLabels.add(x.trim())));
        dxs.forEach(d => { if (d.exhibitId) referencedLabels.add(d.exhibitId.trim()); });
        const unrefEx = exs.filter(e => !referencedLabels.has((e.label || e.id || '').trim()));
        checks.push({
          title: 'Exhibit Integration Across Timeline, Claims & Testimony',
          label: 'Exhibit Integration Across Timeline, Claims & Testimony',
          ok: exs.length > 0 && unrefEx.length === 0,
          detail: exs.length === 0
            ? 'No exhibits logged yet.'
            : (unrefEx.length === 0
              ? `All ${exs.length} exhibit(s) are actively referenced in your timeline, claims, or testimony.`
              : `${unrefEx.length} exhibit(s) (${unrefEx.map(e => e.label || e.id).join(', ')}) are listed in Step 2/4 but not yet referenced in testimony or claims.`)
        });

        const unrehearsed = traps.filter(t => !String(t.readiness || '').toLowerCase().includes('ready'));
        checks.push({
          title: 'Cross-Examination Flashcard Readiness',
          label: 'Cross-Examination Flashcard Readiness',
          ok: traps.length > 0 && unrehearsed.length === 0,
          detail: traps.length === 0
            ? 'No cross-examination flashcards added yet in Step 3.'
            : (unrehearsed.length === 0
              ? `All ${traps.length} tough question(s) marked Ready for Court.`
              : `${unrehearsed.length} of ${traps.length} tough question(s) still need practice in Step 3.`)
        });

        return checks;
      }

      function applySavedPrefs() {
        const btnTheme = document.getElementById('btn-theme');
        const btnStand = document.getElementById('btn-stand-mode');
        try {
          const th = localStorage.getItem(THEME_KEY) || 'light';
          document.documentElement.setAttribute('data-theme', th);
          if (btnTheme) {
            btnTheme.setAttribute('aria-pressed', String(th === 'dark'));
            btnTheme.textContent = th === 'dark' ? 'Light Theme' : 'Dark Theme';
          }
          const st = localStorage.getItem(STAND_KEY) === 'true';
          document.documentElement.setAttribute('data-stand-mode', String(st));
          if (btnStand) btnStand.setAttribute('aria-pressed', String(st));
        } catch (e) {}
      }
      applySavedPrefs();

      const btnThemeEl = document.getElementById('btn-theme');
      if (btnThemeEl) {
        btnThemeEl.addEventListener('click', () => {
          const cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
          document.documentElement.setAttribute('data-theme', cur);
          try { localStorage.setItem(THEME_KEY, cur); } catch (e) {}
          applySavedPrefs();
        });
      }
      const btnStandEl = document.getElementById('btn-stand-mode');
      if (btnStandEl) {
        btnStandEl.addEventListener('click', () => {
          const cur = document.documentElement.getAttribute('data-stand-mode') === 'true';
          document.documentElement.setAttribute('data-stand-mode', String(!cur));
          try { localStorage.setItem(STAND_KEY, String(!cur)); } catch (e) {}
          applySavedPrefs();
        });
      }

      function setupJourneyStepper() {
        const tabs = Array.from(document.querySelectorAll('.step-tab'));
        const secs = Array.from(document.querySelectorAll('.workspace-section'));
        function activateStep(secId) {
          tabs.forEach(t => t.setAttribute('aria-selected', String(t.dataset.target === secId)));
          secs.forEach(s => s.classList.toggle('active', s.id === secId));
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        tabs.forEach(t => t.addEventListener('click', () => activateStep(t.dataset.target)));
        document.querySelectorAll('[data-goto-step]').forEach(btn => {
          btn.addEventListener('click', () => activateStep(btn.dataset.gotoStep));
        });
        return activateStep;
      }

      function exportMatterJson(matter) {
        if (!matter) return;
        const payload = {
          spec: 'prism-legal/matter/2',
          exportedAt: new Date().toISOString(),
          matter: matter
        };
        const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const slug = (matter.docketNumber || matter.title || 'matter').toLowerCase().replace(/[^a-z0-9]+/g, '-');
        a.download = `${slug}.prismlegal.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }

      function importMatterFromFile(file, onDone) {
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          try {
            const parsed = JSON.parse(String(reader.result));
            const m = parsed.matter || (parsed.id && parsed.title ? parsed : null);
            if (m) {
              const clean = createBlankMatter(m);
              const existingIdx = workspace.matters.findIndex(x => x.id === clean.id);
              if (existingIdx >= 0) workspace.matters[existingIdx] = clean;
              else workspace.matters.push(clean);
              workspace.activeMatterId = clean.id;
              saveWorkspace();
              if (onDone) onDone(clean);
            }
          } catch (e) {}
        };
        reader.readAsText(file);
      }

      function downloadMatterMarkdown(matter, mode) {
        if (!matter) return;
        const isBrief = mode === 'brief';
        const lines = [
          `# ${isBrief ? 'TRIAL BRIEF & EXAMINATION BOOK' : 'CASE PREPARATION & HEARING PACKET'}: ${matter.title}`,
          '',
          `- **Docket / Case No.:** ${matter.docketNumber}`,
          `- **Practice Area:** ${matter.practiceArea}`,
          `- **Representation Scope:** ${matter.representationScope || 'Full-Scope Trial Representation'}`,
          `- **Court / Forum:** ${matter.forum}`,
          `- **Governing Legal Framework:** ${matter.framework}`,
          `- **Hearing Date:** ${matter.hearingDate} (${matter.hearingMinutes || 180} min allocated)`,
          `- **Client Party:** ${matter.clientName} (${matter.clientRole})`,
          `- **Opposing Party:** ${matter.opposingParty}`,
          `- **Engaged Counsel:** ${matter.counselName}`,
          '',
          '## 1. Core Relief Goals & Theory of the Case',
          ''
        ];
        if ((matter.goals || []).length === 0) {
          lines.push('_No relief goals recorded yet._', '');
        } else {
          matter.goals.forEach((g, idx) => {
            lines.push(`### Goal ${idx + 1}: ${g.title}`, `- **Requested Order:** ${g.requestedOrder}`, `- **Supporting Rationale:** ${g.rationale}`, '');
          });
        }
        lines.push('## 2. Chronological Timeline of Key Events', '');
        if ((matter.timeline || []).length === 0) {
          lines.push('_No timeline events recorded yet._', '');
        } else {
          lines.push('| Date | Event | Supporting Document | Details |', '| :--- | :--- | :--- | :--- |');
          matter.timeline.slice().sort((a, b) => String(a.date).localeCompare(String(b.date))).forEach(ev => {
            lines.push(`| ${ev.date} | **${ev.title}** | ${ev.exhibitLabel || '—'} | ${ev.description} |`);
          });
          lines.push('');
        }
        lines.push('## 3. Statutory Elements, Compiled Findings & Controlling Exceptions', '');
        if ((matter.claims || []).length === 0) {
          lines.push('_No statutory claims recorded yet._', '');
        } else {
          lines.push('| ID | Statute / Legal Element | Status | Supporting Exhibits | Compiled Proposed Finding / Refusal Guard |', '| :--- | :--- | :--- | :--- | :--- |');
          matter.claims.forEach(c => {
            const prop = compileClaimProposition(c);
            lines.push(`| ${c.id} | \`${c.statute}\` | **${c.status}** | ${(c.exhibits || []).join(', ') || '—'} | ${prop.text} |`);
          });
          lines.push('');
        }
        if ((matter.ruleExceptions || []).length > 0) {
          lines.push('### Controlling Statutory Exceptions & Rule Overrides', '');
          matter.ruleExceptions.forEach(ex => {
            lines.push(`- **${ex.rule || ex.statute || 'Statutory Exception'}** (${ex.type || 'Override'}): ${ex.effect || ex.exceptionRule || ''}`);
          });
          lines.push('');
        }
        lines.push('## 4. Exhibit Register, Evidentiary Foundations & Visual Annotations', '');
        if ((matter.exhibits || []).length === 0) {
          lines.push('_No exhibits recorded yet._', '');
        } else {
          lines.push('| Label | Offering Party | Title | Foundation / Rule | Purpose & Visual / Trial Intent | Status |', '| :--- | :--- | :--- | :--- | :--- | :--- |');
          matter.exhibits.forEach(ex => {
            const extra = [ex.purpose, ex.visualNotes ? `Visual Details: ${ex.visualNotes}` : '', ex.pivotIntent ? `Intent: ${ex.pivotIntent}` : ''].filter(Boolean).join(' — ');
            lines.push(`| **${ex.label}** | ${ex.party} | ${ex.title} | \`${ex.foundation || 'FRE 901'}\` | ${extra} | ${ex.status || 'Marked'} |`);
          });
          lines.push('');
        }
        lines.push('## 5. Direct Examination Script & Visual Cues', '');
        if ((matter.directExam || []).length === 0) {
          lines.push('_No direct examination questions recorded yet._', '');
        } else {
          matter.directExam.forEach((dx, i) => {
            const cueBadge = dx.visualCue === 'yellow-highlight' ? '[⭐ KEY HIGHLIGHT] ' : (dx.visualCue === 'red-strikethrough' ? '[🚫 SKIP UNLESS OPENED ON CROSS] ' : '');
            const admitBadge = dx.movesToAdmit ? ' [📎 MOVE TO ADMIT]' : '';
            lines.push(`### Q${i + 1} (${dx.section || 'Direct'}) ${cueBadge}— Exhibit: ${dx.exhibitLabel || 'None'}${admitBadge}`, `**Q:** ${dx.question}`, `**A:** "${dx.answer}"`, '');
          });
        }
        lines.push('## 6. Cross-Examination Preparation, Rule 106 Context & Calm Responses', '');
        if ((matter.traps || []).length === 0) {
          lines.push('_No cross-examination items recorded yet._', '');
        } else {
          matter.traps.forEach((t, i) => {
            lines.push(`### Topic ${i + 1}: ${t.title}`, `- **Anticipated Question / Claim:** ${t.allegation}`, `- **Avoid:** ${t.trapWarning}`, `- **Calm Fact-Based Response:** "${t.response}"`, ...(t.rule106Context ? [`- **FRE 106 Full Completeness Context:** ${t.rule106Context}`] : []), `- **Supporting Exhibits:** ${(t.exhibits || []).join(', ') || '—'}`, '');
          });
        }
        if ((matter.witnesses || []).length > 0) {
          lines.push('## 7. Witness Roster & Hearing Clock Allocation', '');
          matter.witnesses.forEach(w => {
            lines.push(`- **${w.id}: ${w.name}** (${w.role} · \`${w.status}\` · **${w.minutes} min**): ${w.scope}`);
          });
          lines.push('');
        }
        if ((matter.agenda || []).length > 0) {
          lines.push('## 8. Client–Counsel Alignment Notes', '');
          matter.agenda.forEach(a => {
            lines.push(`- **${a.topic}** [${a.status || 'Open'}] — *Client Question:* ${a.questionForCounsel} | *Attorney Guidance:* ${a.counselGuidance}`);
          });
          lines.push('');
        }
        const blob = new Blob([lines.join('\\n')], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const slug = (matter.docketNumber || matter.title || 'matter').toLowerCase().replace(/[^a-z0-9]+/g, '-');
        a.download = `${slug}-${isBrief ? 'trial-brief' : 'case-packet'}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }

      function buildTimelineSvg(matter) {
        const events = (matter && matter.timeline ? matter.timeline : []).slice().sort((a, b) => String(a.date).localeCompare(String(b.date)));
        if (events.length === 0) {
          return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 110" role="img" aria-label="Empty Chronological Timeline"><rect width="860" height="110" rx="10" fill="#f1f5f9" stroke="#cbd5e1"/><text x="430" y="60" text-anchor="middle" font-family="Inter, sans-serif" font-size="14" fill="#334155">Add key dates below to generate your visual chronological timeline automatically.</text></svg>`;
        }
        const width = Math.max(860, events.length * 190);
        const step = (width - 140) / Math.max(1, events.length - 1);
        const nodes = events.map((ev, idx) => {
          const x = events.length === 1 ? width / 2 : 70 + idx * step;
          const yTop = idx % 2 === 0;
          const cy = 95;
          const labelY = yTop ? 42 : 148;
          const dateY = yTop ? 24 : 166;
          const shortTitle = String(ev.title || '').slice(0, 24);
          return `<g>
            <line x1="${x}" y1="${cy}" x2="${x}" y2="${yTop ? 54 : 132}" stroke="#1e3a8a" stroke-width="2"/>
            <circle cx="${x}" cy="${cy}" r="8" fill="#14532d" stroke="#ffffff" stroke-width="2"/>
            <text x="${x}" y="${dateY}" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#1e3a8a">${escapeHtml(ev.date)} ${ev.exhibitLabel ? '(' + escapeHtml(ev.exhibitLabel) + ')' : ''}</text>
            <text x="${x}" y="${labelY}" text-anchor="middle" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="#0f172a">${escapeHtml(shortTitle)}</text>
          </g>`;
        }).join('');
        return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} 190" role="img" aria-label="Matter Chronological Timeline">
          <rect width="${width}" height="190" rx="12" fill="#f8fafc" stroke="#cbd5e1"/>
          <line x1="50" y1="95" x2="${width - 50}" y2="95" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>
          ${nodes}
        </svg>`;
      }

      // ============================================================================
      // Multi-Modal Evidence Intake Parser, Jural Posture Classifier, Adaptive
      // Neuromorphic Strategy Scheduler, Procedural Deadlines & Filing Generator
      // ============================================================================

      function classifyJuralPosture(claim, matter) {
        if (!claim || (!claim.statute && !claim.statement)) {
          return { valid: false, label: '', Correlative: '', energy: 0 };
        }
        const cfg = (DATA && DATA.intakeClassifier) ? DATA.intakeClassifier : {};
        const heads = cfg.attentionHeads || [];
        const head20 = heads.find(h => h.id === 'HEAD-20') || heads.find(h => h.nodeId === 'node-jural-posture');
        const text = `${claim.statute || ''} ${claim.statement || ''}`.trim();
        const feat = extractIntakeFeatureVector(matter, text);
        const low = text.toLowerCase();
        if (low.includes('exempt') || low.includes('38 u.s.c.') || low.includes('bar') || low.includes('shield') || low.includes('cannot be imputed')) {
          feat[2] = Math.max(feat[2], 220);
        }
        if (low.includes('106') || low.includes('complete') || low.includes('context') || low.includes('remainder')) {
          feat[7] = Math.max(feat[7], 235);
        }
        if (low.includes('26(e)') || low.includes('16.2') || low.includes('omitted') || low.includes('disclos') || low.includes('escrow')) {
          feat[6] = Math.max(feat[6], 230);
          feat[7] = Math.max(feat[7], 210);
        }
        const res = head20 ? evalIntakeNode(head20, feat) : { valid: false, energy: 0, classIndex: -1, classLabel: '' };
        if (!res.valid) {
          return { valid: false, label: '', correlative: '', energy: res.energy || 0 };
        }
        const rawLabel = res.classLabel || 'Right <-> Duty (Enforceable Claim-Right)';
        const friendlyMap = {
          'Right <-> Duty (Enforceable Claim-Right)': 'Enforceable Claim-Right & Duty',
          'Privilege <-> No-Right (Equal Governance Liberty)': 'Equal Governance Authority',
          'Immunity <-> Disability (Statutory Benefit Shield)': 'Statutory Benefit Exemption',
          'Power <-> Liability (Mandatory Disclosure Reopening)': 'Mandatory Disclosure Remedy',
          'Right <-> Duty (FRE 106 Completeness Demand)': 'FRE 106 Completeness Right',
          'Right <-> Duty (Fiduciary Accounting Entitlement)': 'Fiduciary Accounting Right'
        };
        return {
          valid: true,
          label: friendlyMap[rawLabel] || rawLabel,
          correlative: rawLabel,
          energy: res.energy
        };
      }

      function computeAdaptiveStrategySchedule(matter) {
        const m = normalizeMatter(matter || {});
        const claims = m.claims || [];
        const exs = m.exhibits || [];
        const excs = m.ruleExceptions || [];
        const traps = m.traps || [];
        const dxs = m.directExam || [];
        const hasIntake = claims.length > 0 || exs.length > 0 || (m.reliefGoals || []).length > 0;
        if (!hasIntake) {
          return [];
        }
        const clampW = (w) => Math.max(1, Math.min(16, Math.round(w)));
        const backedClaims = claims.filter(c => Array.isArray(c.exhibits) && c.exhibits.length > 0);
        const stipClaims = claims.filter(c => c.status === 'stipulated');
        const hashedExs = exs.filter(e => Boolean(e.sha256 || e.foundation));
        const r106Traps = traps.filter(t => Boolean(t.rule106Context || t.exhibitId));

        // Bounded neuromorphic weight adaptation rule: W_INIT = 8, RAISE = +2 per corroborated signal, LOWER = -1 per gap
        const s1Weight = clampW(8 + (backedClaims.length * 2) + (stipClaims.length * 1) - Math.max(0, claims.length - backedClaims.length));
        const s2Weight = clampW(8 + (hashedExs.length * 2) + (dxs.filter(d => d.movesToAdmit).length * 1) - (exs.length === 0 ? 3 : 0));
        const s3Weight = clampW(8 + (excs.length * 3) + (claims.filter(c => /305|1781|4\.25|4\.16|1692|144|4\.104/i.test(c.statute || '')).length * 2));
        const s4Weight = clampW(8 + (r106Traps.length * 2) + (traps.filter(t => String(t.readiness || '').toLowerCase().includes('ready')).length * 1));

        const strategies = [
          {
            id: 'STRAT-01',
            title: 'Affirmative Statutory Elements & Requested Orders',
            weight: s1Weight,
            maxWeight: 16,
            focus: backedClaims.length > 0
              ? `Lead with ${backedClaims.slice(0, 3).map(c => c.id + ' (' + c.statute + ')').join(', ')}`
              : 'Anchor relief goals to statutory elements in Step 2',
            rationale: `${backedClaims.length} of ${claims.length} statutory claim(s) corroborated by exhibits`
          },
          {
            id: 'STRAT-02',
            title: 'Authenticated Documentary & Multi-Modal Record Tie-Out',
            weight: s2Weight,
            maxWeight: 16,
            focus: exs.length > 0
              ? `Offer ${exs.slice(0, 4).map(e => (e.label || e.id) + ' [' + (e.foundation || 'FRE 901') + ']').join(', ')}`
              : 'Upload or log documentary exhibits in Step 2 / Step 4',
            rationale: `${exs.length} exhibit(s) registered (${hashedExs.length} with verified foundation/custody)`
          },
          {
            id: 'STRAT-03',
            title: 'Controlling Statutory Exceptions & Benefit Protections',
            weight: s3Weight,
            maxWeight: 16,
            focus: excs.length > 0
              ? `Invoke ${excs.map(x => x.rule || x.statute).join(', ')} to bar opposing baseline assumptions`
              : 'Enforce statutory exemptions and burden-shifting rules',
            rationale: `${excs.length} controlling statutory override(s) active`
          },
          {
            id: 'STRAT-04',
            title: 'FRE 106 Rule of Completeness & Cross-Examination Pivots',
            weight: s4Weight,
            maxWeight: 16,
            focus: traps.length > 0
              ? `Deploy ${traps.slice(0, 3).map(t => t.id + ': ' + t.title).join('; ')}`
              : 'Prepare calm fact-anchored responses to anticipated cross-exam challenges',
            rationale: `${r106Traps.length} completeness/rebuttal pivot card(s) anchored to exhibits`
          }
        ];
        return strategies.sort((a, b) => b.weight - a.weight);
      }

      async function computeBufferSha256Hex(buffer) {
        try {
          if (typeof crypto !== 'undefined' && crypto.subtle && crypto.subtle.digest) {
            const hashBuf = await crypto.subtle.digest('SHA-256', buffer);
            return Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2, '0')).join('');
          }
        } catch (e) {}
        // Deterministic fallback digest if WebCrypto is unavailable in non-HTTPS test harness
        const bytes = new Uint8Array(buffer || []);
        let h1 = 0x811c9dc5;
        let h2 = 0x01000193;
        for (let i = 0; i < bytes.length; i++) {
          h1 ^= bytes[i];
          h1 = Math.imul(h1, 0x01000193) >>> 0;
          h2 ^= (bytes[i] + (i & 0xff));
          h2 = Math.imul(h2, 0x85ebca6b) >>> 0;
        }
        const base = (h1.toString(16).padStart(8, '0') + h2.toString(16).padStart(8, '0'));
        return (base.repeat(4)).slice(0, 64);
      }

      async function decompressBytesInBrowser(compressedBytes, format) {
        try {
          if (typeof DecompressionStream === 'undefined' || typeof Response === 'undefined' || typeof Blob === 'undefined') {
            return null;
          }
          const ds = new DecompressionStream(format);
          const stream = new Blob([compressedBytes]).stream().pipeThrough(ds);
          const ab = await new Response(stream).arrayBuffer();
          return new Uint8Array(ab);
        } catch (e) {
          return null;
        }
      }

      function decodePdfLiteralString(rawLiteral) {
        let out = '';
        for (let i = 0; i < rawLiteral.length; i++) {
          const ch = rawLiteral[i];
          if (ch === '\\' && i + 1 < rawLiteral.length) {
            const next = rawLiteral[i + 1];
            if (next === 'n') { out += '\n'; i++; }
            else if (next === 'r') { out += ' '; i++; }
            else if (next === 't') { out += ' '; i++; }
            else if (next === '(' || next === ')' || next === '\\') { out += next; i++; }
            else if (/[0-7]/.test(next)) {
              const oct = rawLiteral.slice(i + 1, i + 4).match(/^[0-7]{1,3}/)[0];
              out += String.fromCharCode(parseInt(oct, 8));
              i += oct.length;
            } else {
              out += next;
              i++;
            }
          } else {
            out += ch;
          }
        }
        return out.replace(/[^\x20-\x7E\n]/g, ' ').replace(/\s+/g, ' ').trim();
      }

      function decodePdfHexString(hexRaw) {
        const clean = hexRaw.replace(/[^0-9A-Fa-f]/g, '');
        if (clean.length < 4) return '';
        const bytes = [];
        for (let i = 0; i + 1 < clean.length; i += 2) {
          bytes.push(parseInt(clean.slice(i, i + 2), 16));
        }
        if (bytes.length >= 2 && bytes[0] === 0xFE && bytes[1] === 0xFF) {
          let u16 = '';
          for (let j = 2; j + 1 < bytes.length; j += 2) {
            const code = (bytes[j] << 8) | bytes[j + 1];
            if (code >= 32 && code <= 126) u16 += String.fromCharCode(code);
            else if (code === 10 || code === 13) u16 += ' ';
          }
          return u16.replace(/\s+/g, ' ').trim();
        }
        return bytes
          .map(b => (b >= 32 && b <= 126) ? String.fromCharCode(b) : ' ')
          .join('')
          .replace(/\s+/g, ' ')
          .trim();
      }

      function extractTextOperatorsFromPdfStream(streamStr) {
        const chunks = [];
        const filterNoise = (s) => s.length >= 3 && /[A-Za-z0-9]{2,}/.test(s) && !/^(Identity-H|Adobe|MacRomanEncoding|WinAnsiEncoding|Times-Roman|Times-Bold|Helvetica|Courier|FontDescriptor|BaseFont|Subtype|Page|Pages|Catalog|FlateDecode)$/i.test(s);

        // Parse TJ arrays: [(Hello ) -15 (World)] TJ
        const tjArrayRe = /\[([^\[\]]{2,2000})\]\s*TJ\b/g;
        let m;
        while ((m = tjArrayRe.exec(streamStr)) !== null && chunks.length < 180) {
          const inner = m[1];
          const parts = [];
          const tokenRe = /\((?:\\.|[^()\\])*?\)|<([0-9A-Fa-f\s]{4,})>/g;
          let tm;
          while ((tm = tokenRe.exec(inner)) !== null) {
            if (tm[0].startsWith('(')) {
              const dec = decodePdfLiteralString(tm[0].slice(1, -1));
              if (dec) parts.push(dec);
            } else if (tm[1]) {
              const dec = decodePdfHexString(tm[1]);
              if (dec) parts.push(dec);
            }
          }
          const joined = parts.join('').replace(/\s+/g, ' ').trim();
          if (filterNoise(joined)) chunks.push(joined);
        }

        // Parse single literal Tj / ' / " operators
        const singleTjRe = /\(((?:\\.|[^()\\]){2,400})\)\s*(?:Tj|'|")\b/g;
        while ((m = singleTjRe.exec(streamStr)) !== null && chunks.length < 220) {
          const dec = decodePdfLiteralString(m[1]);
          if (filterNoise(dec)) chunks.push(dec);
        }

        // Parse hex string <...> Tj operators
        const hexTjRe = /<([0-9A-Fa-f\s]{6,800})>\s*Tj\b/g;
        while ((m = hexTjRe.exec(streamStr)) !== null && chunks.length < 240) {
          const dec = decodePdfHexString(m[1]);
          if (filterNoise(dec)) chunks.push(dec);
        }

        return chunks;
      }

      async function extractPdfStructureAndTextInBrowser(bytes) {
        const scanLen = Math.min(bytes.length, 1048576);
        const raw = new TextDecoder('latin1').decode(bytes.slice(0, scanLen));
        const pageMatches = raw.match(/\/Type\s*\/Page\b/g);
        const countMatches = Array.from(raw.matchAll(/\/Count\s+(\d+)/g)).map(m => parseInt(m[1], 10)).filter(n => n > 0);
        const pageCount = countMatches.length ? Math.max(...countMatches) : (pageMatches ? Math.max(1, pageMatches.length) : 1);

        const metaParts = [];
        const infoKeys = ['Title', 'Subject', 'Author', 'Keywords'];
        infoKeys.forEach(k => {
          const km = raw.match(new RegExp('\\/' + k + '\\s*\\(((?:\\\\.|[^()\\\\]){2,200})\\)'));
          if (km && km[1]) {
            const val = decodePdfLiteralString(km[1]);
            if (val && val.length >= 3) metaParts.push(`${k}: ${val}`);
          }
        });
        const xmpTitle = raw.match(/<dc:title[^>]*>[\s\S]*?<rdf:li[^>]*>([\s\S]*?)<\/rdf:li>/i);
        if (xmpTitle && xmpTitle[1]) {
          const cleanXmp = xmpTitle[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
          if (cleanXmp) metaParts.push(cleanXmp);
        }

        const extractedSegments = [...metaParts];
        // Decompress /FlateDecode content streams in browser
        const streamRe = /stream\r?\n/g;
        let sm;
        let streamCount = 0;
        while ((sm = streamRe.exec(raw)) !== null && streamCount < 28) {
          streamCount++;
          const dataStart = sm.index + sm[0].length;
          const endIdx = raw.indexOf('endstream', dataStart);
          if (endIdx < 0 || endIdx - dataStart > 524288) continue;
          const headerWindow = raw.slice(Math.max(0, sm.index - 320), sm.index);
          if (/\/DCTDecode|\/JPXDecode|\/CCITTFaxDecode|\/Subtype\s*\/Image/i.test(headerWindow)) {
            continue;
          }
          let endTrim = endIdx;
          if (raw[endTrim - 1] === '\n') endTrim--;
          if (raw[endTrim - 1] === '\r') endTrim--;
          const streamBytes = bytes.slice(dataStart, endTrim);

          if (/\/FlateDecode/i.test(headerWindow)) {
            let decomp = await decompressBytesInBrowser(streamBytes, 'deflate');
            if (!decomp && streamBytes.length > 2) {
              decomp = await decompressBytesInBrowser(streamBytes.slice(2), 'deflate-raw');
            }
            if (decomp && decomp.length > 0) {
              const decompStr = new TextDecoder('latin1').decode(decomp);
              const ops = extractTextOperatorsFromPdfStream(decompStr);
              ops.forEach(op => {
                if (!extractedSegments.includes(op)) extractedSegments.push(op);
              });
            }
          } else {
            const plainStream = raw.slice(dataStart, endTrim);
            const ops = extractTextOperatorsFromPdfStream(plainStream);
            ops.forEach(op => {
              if (!extractedSegments.includes(op)) extractedSegments.push(op);
            });
          }
        }

        // Also scan top-level uncompressed literal strings if streams were sparse
        if (extractedSegments.length < 6) {
          const topOps = extractTextOperatorsFromPdfStream(raw);
          topOps.forEach(op => {
            if (!extractedSegments.includes(op)) extractedSegments.push(op);
          });
          const litRegex = /\(((?:\\.|[^()\\]){4,220})\)/g;
          let lm;
          while ((lm = litRegex.exec(raw)) !== null && extractedSegments.length < 60) {
            const clean = decodePdfLiteralString(lm[1]);
            if (clean.length >= 4 && /[A-Za-z]{3,}/.test(clean) && !/^(Identity|Adobe|MacRoman|WinAnsi|Times|Helvetica|Courier|Font|Type|Page|Catalog|Parent|Resources|ProcSet|MediaBox)/i.test(clean)) {
              if (!extractedSegments.includes(clean)) extractedSegments.push(clean);
            }
          }
        }

        return {
          pageCount,
          metadataSummary: metaParts.join(' · '),
          extractedText: extractedSegments.join('. ')
        };
      }

      function extractPngChunksMetadata(bytes) {
        if (!bytes || bytes.length < 24 || bytes[0] !== 0x89 || bytes[1] !== 0x50 || bytes[2] !== 0x4E || bytes[3] !== 0x47) {
          return null;
        }
        const readU32 = (off) => ((bytes[off] << 24) | (bytes[off + 1] << 16) | (bytes[off + 2] << 8) | bytes[off + 3]) >>> 0;
        let offset = 8;
        let width = 0;
        let height = 0;
        let bitDepth = 8;
        let dpi = 0;
        const textChunks = [];

        while (offset + 12 <= bytes.length) {
          const len = readU32(offset);
          const type = String.fromCharCode(bytes[offset + 4], bytes[offset + 5], bytes[offset + 6], bytes[offset + 7]);
          const dataStart = offset + 8;
          if (dataStart + len > bytes.length) break;

          if (type === 'IHDR' && len >= 9) {
            width = readU32(dataStart);
            height = readU32(dataStart + 4);
            bitDepth = bytes[dataStart + 8];
          } else if (type === 'pHYs' && len >= 9) {
            const ppuX = readU32(dataStart);
            const unit = bytes[dataStart + 8];
            if (unit === 1 && ppuX > 0) {
              dpi = Math.round(ppuX * 0.0254);
            }
          } else if ((type === 'tEXt' || type === 'iTXt') && len > 2 && len < 16384) {
            const rawChunk = new TextDecoder('utf-8', { fatal: false }).decode(bytes.slice(dataStart, dataStart + len));
            const parts = rawChunk.split('\0').map(s => s.replace(/[^\x20-\x7E]/g, ' ').trim()).filter(Boolean);
            if (parts.length >= 2) {
              const key = parts[0];
              const val = parts[parts.length - 1];
              if (!/^(Software|XML:com\.adobe\.xmp)$/i.test(key) && val.length >= 3) {
                textChunks.push(`${key}: ${val}`);
              }
            } else if (parts.length === 1 && parts[0].length >= 4) {
              textChunks.push(parts[0]);
            }
          } else if (type === 'IEND') {
            break;
          }
          offset = dataStart + len + 4;
        }

        const summaryParts = [];
        if (width && height) summaryParts.push(`${width}×${height}px (${bitDepth}-bit PNG${dpi ? ', ' + dpi + ' DPI' : ''})`);
        if (textChunks.length) summaryParts.push(textChunks.slice(0, 2).join(' · '));
        return {
          dimensions: (width && height) ? { width, height } : null,
          dpi,
          extractedText: textChunks.join('. '),
          exifSummary: summaryParts.join(' · ')
        };
      }

      function extractJpegExifMetadata(bytes) {
        if (!bytes || bytes.length < 4 || bytes[0] !== 0xFF || bytes[1] !== 0xD8) {
          return null;
        }
        let offset = 2;
        let width = 0;
        let height = 0;
        const exifTags = {};
        const comments = [];

        const parseTiffIfd = (tiffStart, ifdOffset, littleEndian, maxLen) => {
          const readU16 = (pos) => littleEndian ? (bytes[pos] | (bytes[pos + 1] << 8)) : ((bytes[pos] << 8) | bytes[pos + 1]);
          const readU32 = (pos) => littleEndian
            ? ((bytes[pos] | (bytes[pos + 1] << 8) | (bytes[pos + 2] << 16) | (bytes[pos + 3] << 24)) >>> 0)
            : (((bytes[pos] << 24) | (bytes[pos + 1] << 16) | (bytes[pos + 2] << 8) | bytes[pos + 3]) >>> 0);

          const dirStart = tiffStart + ifdOffset;
          if (dirStart + 2 > tiffStart + maxLen || dirStart + 2 > bytes.length) return 0;
          const numEntries = readU16(dirStart);
          let subIfdOffset = 0;
          const tagNames = {
            0x010E: 'ImageDescription',
            0x010F: 'CameraMake',
            0x0110: 'CameraModel',
            0x0131: 'Software',
            0x0132: 'DateTime',
            0x9003: 'DateTimeOriginal',
            0x9004: 'CreateDate',
            0x9286: 'UserComment'
          };

          for (let i = 0; i < Math.min(numEntries, 64); i++) {
            const entryPos = dirStart + 2 + i * 12;
            if (entryPos + 12 > bytes.length || entryPos + 12 > tiffStart + maxLen) break;
            const tag = readU16(entryPos);
            const fieldType = readU16(entryPos + 2);
            const count = readU32(entryPos + 4);
            if (tag === 0x8769) {
              subIfdOffset = readU32(entryPos + 8);
              continue;
            }
            if ((fieldType === 2 || fieldType === 7) && tagNames[tag] && count > 1 && count < 512) {
              const valPos = count <= 4 ? (entryPos + 8) : (tiffStart + readU32(entryPos + 8));
              if (valPos >= tiffStart && valPos + count <= bytes.length) {
                let rawStr = new TextDecoder('utf-8', { fatal: false }).decode(bytes.slice(valPos, valPos + count));
                rawStr = rawStr.replace(/^ASCII\0+/i, '').replace(/\0+/g, '').replace(/[^\x20-\x7E]/g, ' ').trim();
                if (rawStr.length >= 2) {
                  if ((tag === 0x0132 || tag === 0x9003 || tag === 0x9004) && /^\d{4}:\d{2}:\d{2}/.test(rawStr)) {
                    rawStr = rawStr.slice(0, 10).replace(/:/g, '-') + rawStr.slice(10);
                  }
                  exifTags[tagNames[tag]] = rawStr;
                }
              }
            }
          }
          return subIfdOffset;
        };

        while (offset + 4 <= bytes.length && bytes[offset] === 0xFF) {
          const marker = bytes[offset + 1];
          if (marker === 0xD9 || marker === 0xDA) break;
          if (marker === 0xFF) { offset++; continue; }
          const segLen = (bytes[offset + 2] << 8) | bytes[offset + 3];
          if (segLen < 2 || offset + 2 + segLen > bytes.length) break;

          if ((marker === 0xC0 || marker === 0xC1 || marker === 0xC2) && segLen >= 7) {
            height = (bytes[offset + 5] << 8) | bytes[offset + 6];
            width = (bytes[offset + 7] << 8) | bytes[offset + 8];
          } else if (marker === 0xFE && segLen > 3) {
            const com = new TextDecoder('utf-8', { fatal: false }).decode(bytes.slice(offset + 4, offset + 2 + segLen)).trim();
            if (com) comments.push(com);
          } else if (marker === 0xE1 && segLen > 14) {
            const hdr = String.fromCharCode(bytes[offset + 4], bytes[offset + 5], bytes[offset + 6], bytes[offset + 7]);
            if (hdr === 'Exif' && bytes[offset + 8] === 0 && bytes[offset + 9] === 0) {
              const tiffStart = offset + 10;
              const endian = String.fromCharCode(bytes[tiffStart], bytes[tiffStart + 1]);
              const little = endian === 'II';
              if (little || endian === 'MM') {
                const ifd0Off = little
                  ? ((bytes[tiffStart + 4] | (bytes[tiffStart + 5] << 8) | (bytes[tiffStart + 6] << 16) | (bytes[tiffStart + 7] << 24)) >>> 0)
                  : (((bytes[tiffStart + 4] << 24) | (bytes[tiffStart + 5] << 16) | (bytes[tiffStart + 6] << 8) | bytes[tiffStart + 7]) >>> 0);
                const subOff = parseTiffIfd(tiffStart, ifd0Off, little, segLen - 8);
                if (subOff > 0) {
                  parseTiffIfd(tiffStart, subOff, little, segLen - 8);
                }
              }
            }
          }
          offset += 2 + segLen;
        }

        const textParts = [];
        if (exifTags.ImageDescription) textParts.push(exifTags.ImageDescription);
        if (exifTags.UserComment) textParts.push(exifTags.UserComment);
        if (exifTags.DateTimeOriginal || exifTags.DateTime) textParts.push(`Captured ${exifTags.DateTimeOriginal || exifTags.DateTime}`);
        comments.forEach(c => textParts.push(c));

        const exifSummaryParts = [];
        if (width && height) exifSummaryParts.push(`${width}×${height}px JPEG`);
        if (exifTags.CameraMake || exifTags.CameraModel) exifSummaryParts.push(`Device: ${[exifTags.CameraMake, exifTags.CameraModel].filter(Boolean).join(' ')}`);
        if (exifTags.DateTimeOriginal || exifTags.DateTime) exifSummaryParts.push(`EXIF Timestamp: ${exifTags.DateTimeOriginal || exifTags.DateTime}`);

        return {
          dimensions: (width && height) ? { width, height } : null,
          exifTags,
          extractedText: textParts.join('. '),
          exifSummary: exifSummaryParts.join(' · ')
        };
      }

      function renderImagePreviewThumbnail(file, ext, bytes) {
        return new Promise((resolve) => {
          if (ext === 'svg' && bytes && bytes.length > 0 && bytes.length <= 65536) {
            try {
              const svgStr = new TextDecoder('utf-8', { fatal: false }).decode(bytes);
              const encoded = 'data:image/svg+xml;utf8,' + encodeURIComponent(svgStr);
              resolve({ dimensions: null, previewDataUrl: encoded });
              return;
            } catch (e) {}
          }
          if (typeof Image === 'undefined' || typeof URL === 'undefined' || !URL.createObjectURL || typeof document === 'undefined') {
            resolve({ dimensions: null, previewDataUrl: '' });
            return;
          }
          const url = URL.createObjectURL(file);
          const img = new Image();
          const timer = setTimeout(() => {
            URL.revokeObjectURL(url);
            resolve({ dimensions: null, previewDataUrl: '' });
          }, 1500);
          img.onload = () => {
            clearTimeout(timer);
            const w = img.naturalWidth || img.width || 0;
            const h = img.naturalHeight || img.height || 0;
            let previewDataUrl = '';
            try {
              if (w > 0 && h > 0) {
                const scale = Math.min(1, 260 / w, 170 / h);
                const cw = Math.max(1, Math.round(w * scale));
                const ch = Math.max(1, Math.round(h * scale));
                const canvas = document.createElement('canvas');
                canvas.width = cw;
                canvas.height = ch;
                const ctx = canvas.getContext('2d');
                if (ctx) {
                  ctx.fillStyle = '#ffffff';
                  ctx.fillRect(0, 0, cw, ch);
                  ctx.drawImage(img, 0, 0, cw, ch);
                  previewDataUrl = canvas.toDataURL('image/jpeg', 0.78);
                }
              }
            } catch (e) {}
            URL.revokeObjectURL(url);
            resolve({ dimensions: (w && h) ? { width: w, height: h } : null, previewDataUrl });
          };
          img.onerror = () => {
            clearTimeout(timer);
            URL.revokeObjectURL(url);
            resolve({ dimensions: null, previewDataUrl: '' });
          };
          img.src = url;
        });
      }

      async function extractZipXmlTextInBrowser(bytes, ext) {
        if (!bytes || bytes.length < 30 || bytes[0] !== 0x50 || bytes[1] !== 0x4B || bytes[2] !== 0x03 || bytes[3] !== 0x04) {
          return '';
        }
        const readU16 = (p) => bytes[p] | (bytes[p + 1] << 8);
        const readU32 = (p) => ((bytes[p] | (bytes[p + 1] << 8) | (bytes[p + 2] << 16) | (bytes[p + 3] << 24)) >>> 0);
        let pos = 0;
        const texts = [];
        while (pos + 30 <= bytes.length && bytes[pos] === 0x50 && bytes[pos + 1] === 0x4B && bytes[pos + 2] === 0x03 && bytes[pos + 3] === 0x04) {
          const method = readU16(pos + 8);
          const compSize = readU32(pos + 18);
          const nameLen = readU16(pos + 26);
          const extraLen = readU16(pos + 28);
          const nameStart = pos + 30;
          const dataStart = nameStart + nameLen + extraLen;
          if (dataStart + compSize > bytes.length) break;
          const entryName = new TextDecoder('utf-8', { fatal: false }).decode(bytes.slice(nameStart, nameStart + nameLen));
          if (/(word\/document\.xml|xl\/sharedStrings\.xml|content\.xml)$/i.test(entryName)) {
            const compBytes = bytes.slice(dataStart, dataStart + compSize);
            let xmlBytes = null;
            if (method === 0) {
              xmlBytes = compBytes;
            } else if (method === 8) {
              xmlBytes = await decompressBytesInBrowser(compBytes, 'deflate-raw');
            }
            if (xmlBytes && xmlBytes.length > 0) {
              const xmlStr = new TextDecoder('utf-8', { fatal: false }).decode(xmlBytes);
              const stripped = xmlStr
                .replace(/<\/(?:w:p|p|row|si|text:p)>/gi, '. ')
                .replace(/<[^>]+>/g, ' ')
                .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
                .replace(/\s+/g, ' ')
                .trim();
              if (stripped) texts.push(stripped);
            }
          }
          pos = dataStart + compSize;
        }
        return texts.join('. ');
      }

      function extractRtfTextInBrowser(bytes) {
        const raw = new TextDecoder('latin1').decode(bytes.slice(0, Math.min(bytes.length, 131072)));
        return raw
          .replace(/\\par\b/g, '. ')
          .replace(/\\'[0-9a-fA-F]{2}/g, ' ')
          .replace(/\\[a-zA-Z]+-?\d*\s?/g, ' ')
          .replace(/[{}]/g, ' ')
          .replace(/\s+/g, ' ')
          .trim();
      }

      function extractEmlTextInBrowser(rawText) {
        const parts = String(rawText || '').split(/\r?\n\r?\n/);
        const headerBlock = parts[0] || '';
        const bodyBlock = parts.slice(1).join('. ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
        const subj = (headerBlock.match(/^Subject:\s*(.+)$/im) || [])[1] || '';
        const from = (headerBlock.match(/^From:\s*(.+)$/im) || [])[1] || '';
        const date = (headerBlock.match(/^Date:\s*(.+)$/im) || [])[1] || '';
        return [
          subj ? `Subject: ${subj.trim()}` : '',
          from ? `From: ${from.trim()}` : '',
          date ? `Date: ${date.trim()}` : '',
          bodyBlock
        ].filter(Boolean).join('. ');
      }

      async function parseMultiModalFileInBrowser(file, matter) {
        if (!file) return null;
        const fileName = String(file.name || 'uploaded-evidence').trim();
        const mimeType = String(file.type || '').toLowerCase();
        const ext = (fileName.includes('.') ? fileName.split('.').pop() : '').toLowerCase();
        const byteSize = Number(file.size) || 0;

        let buffer;
        if (typeof file.arrayBuffer === 'function') {
          buffer = await file.arrayBuffer();
        } else {
          buffer = await new Promise((resolve) => {
            const r = new FileReader();
            r.onload = () => resolve(r.result || new ArrayBuffer(0));
            r.onerror = () => resolve(new ArrayBuffer(0));
            r.readAsArrayBuffer(file);
          });
        }
        const bytes = new Uint8Array(buffer);
        const sha256 = await computeBufferSha256Hex(buffer);

        let modality = 'Structured Document';
        let extractedText = '';
        let pageCount = 1;
        let dimensions = null;
        let previewDataUrl = '';
        let exifSummary = '';

        const isPdf = mimeType.includes('pdf') || ext === 'pdf' || (bytes.length >= 4 && bytes[0] === 0x25 && bytes[1] === 0x50 && bytes[2] === 0x44 && bytes[3] === 0x46);
        const isPng = mimeType === 'image/png' || ext === 'png' || (bytes.length >= 8 && bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4E && bytes[3] === 0x47);
        const isJpeg = mimeType === 'image/jpeg' || ['jpg', 'jpeg'].includes(ext) || (bytes.length >= 3 && bytes[0] === 0xFF && bytes[1] === 0xD8 && bytes[2] === 0xFF);
        const isImage = isPng || isJpeg || mimeType.startsWith('image/') || ['png', 'jpg', 'jpeg', 'webp', 'gif', 'svg', 'bmp', 'tif', 'tiff'].includes(ext);
        const isOfficeZip = ['docx', 'xlsx', 'odt'].includes(ext) || (bytes.length >= 4 && bytes[0] === 0x50 && bytes[1] === 0x4B && bytes[2] === 0x03 && bytes[3] === 0x04);
        const isRtf = ext === 'rtf' || mimeType.includes('rtf');
        const isAudioVideo = mimeType.startsWith('audio/') || mimeType.startsWith('video/') || ['mp3', 'wav', 'm4a', 'ogg', 'mp4', 'webm', 'mov'].includes(ext);
        const isSpreadsheet = ['csv', 'tsv'].includes(ext) || mimeType.includes('csv') || mimeType.includes('spreadsheet');

        if (isPdf) {
          modality = 'PDF Documentary Record';
          const pdfInfo = await extractPdfStructureAndTextInBrowser(bytes);
          pageCount = pdfInfo.pageCount;
          extractedText = pdfInfo.extractedText;
          if (pdfInfo.metadataSummary) exifSummary = pdfInfo.metadataSummary;
        } else if (isImage) {
          modality = ext === 'svg' ? 'Visual Diagram / Inspection Graphic (SVG)' : 'Photographic / Scanned Visual Evidence';
          if (ext === 'svg') {
            const svgText = new TextDecoder('utf-8', { fatal: false }).decode(bytes);
            const textMatches = Array.from(svgText.matchAll(/<(?:text|title|desc)[^>]*>([\s\S]*?)<\/(?:text|title|desc)>/gi))
              .map(m => m[1].replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').trim())
              .filter(Boolean);
            extractedText = textMatches.join('. ');
          } else if (isPng) {
            const pngMeta = extractPngChunksMetadata(bytes);
            if (pngMeta) {
              dimensions = pngMeta.dimensions;
              extractedText = pngMeta.extractedText || '';
              exifSummary = pngMeta.exifSummary || '';
            }
          } else if (isJpeg) {
            const jpgMeta = extractJpegExifMetadata(bytes);
            if (jpgMeta) {
              dimensions = jpgMeta.dimensions;
              extractedText = jpgMeta.extractedText || '';
              exifSummary = jpgMeta.exifSummary || '';
            }
          }
          const thumbInfo = await renderImagePreviewThumbnail(file, ext, bytes);
          if (!dimensions && thumbInfo.dimensions) dimensions = thumbInfo.dimensions;
          if (thumbInfo.previewDataUrl) previewDataUrl = thumbInfo.previewDataUrl;
        } else if (isOfficeZip) {
          modality = ext === 'xlsx' ? 'Financial / Tabular Workbook (XLSX)' : 'Word Processing Pleading / Record (DOCX)';
          extractedText = await extractZipXmlTextInBrowser(bytes, ext);
          pageCount = Math.max(1, Math.ceil((extractedText.length || 1200) / 2200));
        } else if (isRtf) {
          modality = 'Rich Text Pleading / Record (RTF)';
          extractedText = extractRtfTextInBrowser(bytes);
          pageCount = Math.max(1, Math.ceil((extractedText.length || 1200) / 2200));
        } else if (isAudioVideo) {
          modality = 'Audio / Video Recording';
        } else if (isSpreadsheet) {
          modality = 'Financial / Tabular Ledger (CSV/TSV)';
          const rawCsv = new TextDecoder('utf-8', { fatal: false }).decode(bytes.slice(0, Math.min(bytes.length, 65536)));
          const rows = rawCsv.split(/\r?\n/).filter(r => r.trim().length > 0);
          pageCount = Math.max(1, Math.ceil(rows.length / 35));
          const dataRows = rows.length > 1 ? rows.slice(1) : rows;
          extractedText = dataRows.map(r => r.split(/[,\t]/).map(c => c.trim()).filter(Boolean).join(' · ')).join('. ');
        } else {
          const rawUtf = new TextDecoder('utf-8', { fatal: false }).decode(bytes.slice(0, Math.min(bytes.length, 65536)));
          if (ext === 'eml' || (/^From:\s+/im.test(rawUtf) && /^Subject:\s+/im.test(rawUtf))) {
            modality = 'Electronic Correspondence (EML)';
            extractedText = extractEmlTextInBrowser(rawUtf);
          } else if (ext === 'html' || ext === 'htm') {
            modality = 'Electronic Web / Portal Record (HTML)';
            extractedText = rawUtf.replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
          } else {
            modality = 'Written Document / Statement';
            extractedText = rawUtf;
          }
          pageCount = Math.max(1, Math.ceil(extractedText.length / 2200));
        }

        const cleanName = fileName
          .replace(/\.[a-z0-9]{1,5}$/i, '')
          .replace(/[_-]+/g, ' ')
          .replace(/\s+/g, ' ')
          .trim();

        const combinedCorpus = `${cleanName}. ${extractedText}`.trim();
        const dates = Array.from(new Set(
          (combinedCorpus.match(/\b(\d{4}-\d{2}-\d{2}|\d{1,2}\/\d{1,2}\/\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b/gi) || [])
        ));
        const moneyAmounts = Array.from(new Set(
          (combinedCorpus.match(/\$[0-9,]+(?:\.\d{2})?(?:\/mo|\/month|\/yr|\/year)?/gi) || [])
        ));
        const percentages = Array.from(new Set(
          (combinedCorpus.match(/\b\d{1,3}(?:\.\d+)?%\b|\b50\/50\b/g) || [])
        ));
        const docketMatch = combinedCorpus.match(/\b(?:Case\s*(?:No\.?|Number)?|Docket\s*(?:No\.?)?)\s*[:#]?\s*([0-9]{2,4}-[A-Z]{2,5}-[0-9]{3,6})\b/i)
          || combinedCorpus.match(/\b([0-9]{4}-[A-Z]{2,5}-[0-9]{3,6})\b/);
        const sectionRefs = Array.from(new Set(
          (combinedCorpus.match(/\b(?:§+\s*[0-9A-Za-z.\-()]+|Rule\s+[0-9A-Za-z.\-()]+|FRE\s+[0-9A-Za-z.\-()]+|FRCP\s+[0-9A-Za-z.\-()]+|38\s+U\.S\.C\.\s*§\s*[0-9A-Za-z.\-()]+|38\s+C\.F\.R\.\s*§\s*[0-9A-Za-z.\-()]+|15\s+U\.S\.C\.\s*§\s*[0-9A-Za-z.\-()]+|42\s+U\.S\.C\.\s*§\s*[0-9A-Za-z.\-()]+)\b/gi) || [])
        ));

        // Run HEAD-19 (node-multimodal-upload) and HEAD-04 (node-exhibit-admission)
        const cfg = (DATA && DATA.intakeClassifier) ? DATA.intakeClassifier : {};
        const heads = cfg.attentionHeads || [];
        const head19 = heads.find(h => h.id === 'HEAD-19') || heads.find(h => h.nodeId === 'node-multimodal-upload');
        const head04 = heads.find(h => h.id === 'HEAD-04') || heads.find(h => h.nodeId === 'node-exhibit-admission');
        const feat = extractIntakeFeatureVector(matter, combinedCorpus);
        if (isSpreadsheet || moneyAmounts.length > 0 || /bank|escrow|tax|ledger|pay|invoice|k-1|w-2/i.test(combinedCorpus)) {
          feat[6] = Math.max(feat[6], 245);
        }
        if (/message|email|thread|log|diary|journal|excerpt|recording|transcript/i.test(combinedCorpus)) {
          feat[7] = Math.max(feat[7], 240);
        }
        if (isImage || /photo|inspection|diagram|chart|map/i.test(combinedCorpus)) {
          feat[1] = Math.max(feat[1], 160);
          feat[6] = Math.max(feat[6], 210);
        }

        const h19Res = head19 ? evalIntakeNode(head19, feat) : { valid: false, classLabel: '' };
        const h04Res = head04 ? evalIntakeNode(head04, feat) : { valid: false, classLabel: '' };

        const foundation = h04Res.classLabel || h19Res.classLabel || 'FRE 901(b)(1) Authenticated Record';
        const clauses = parseIntakeClauses(extractedText).slice(0, 6);
        const summarySentence = clauses[0]
          ? (clauses[0].length <= 160 ? clauses[0] : clauses[0].slice(0, 155).trim() + '…')
          : `Authenticated ${modality.toLowerCase()} (${cleanName})${dates[0] ? ' dated ' + dates[0] : ''}${moneyAmounts[0] ? ' documenting ' + moneyAmounts.join(', ') : ''}.`;

        const visualParts = [
          `${modality} (${pageCount} p., ${(byteSize / 1024).toFixed(1)} KB)`,
          `SHA-256: ${sha256.slice(0, 16)}…`
        ];
        if (exifSummary) visualParts.push(exifSummary);
        else if (dimensions && dimensions.width) visualParts.push(`Dimensions: ${dimensions.width}×${dimensions.height}px`);
        if (dates.length) visualParts.push(`Dates: ${dates.slice(0, 3).join(', ')}`);
        if (moneyAmounts.length) visualParts.push(`Figures: ${moneyAmounts.slice(0, 3).join(', ')}`);
        if (sectionRefs.length) visualParts.push(`Citations: ${sectionRefs.slice(0, 3).join(', ')}`);

        return {
          fileName,
          cleanTitle: cleanName || fileName,
          title: cleanName || fileName,
          date: dates[0] || 'Record',
          purpose: summarySentence,
          pivotIntent: `Offer (${modality}) under ${foundation} to establish ${summarySentence}`,
          mimeType: mimeType || ext || 'application/octet-stream',
          byteSize,
          sha256,
          modality,
          modalityClass: h19Res.classLabel || modality,
          foundation,
          pageCount,
          dimensions,
          exifSummary,
          previewDataUrl,
          dates,
          moneyAmounts,
          percentages,
          docketNumber: docketMatch ? docketMatch[1] : '',
          sectionRefs,
          clauses,
          summarySentence,
          visualNotes: visualParts.join(' · '),
          extractedText
        };
      }

      async function ingestMultiModalUploadsIntoMatter(matter, fileList, onComplete) {
        if (!matter) return { parsedFiles: [], matter };
        if (matter.isExample) {
          // If the user drops files while viewing a read-only example, start a fresh saved matter for their uploads
          matter = createBlankMatter({
            areaOfLaw: matter.areaOfLaw || 'Family & Parenting Law',
            practiceArea: matter.areaOfLaw || 'Family & Parenting Law'
          });
        }
        if (matter.isUnsavedDraft) {
          delete matter.isUnsavedDraft;
          if (!matter.id || matter.id === 'DRAFT-NEW') {
            matter.id = 'MATTER-' + Date.now();
          }
        }

        const files = Array.from(fileList || []);
        const parsedFiles = [];
        for (let i = 0; i < files.length; i++) {
          const item = files[i];
          const pf = (item && item.sha256 && item.cleanTitle) ? item : await parseMultiModalFileInBrowser(item, matter);
          if (pf) parsedFiles.push(pf);
        }

        matter.exhibits = matter.exhibits || [];
        matter.timeline = matter.timeline || [];

        parsedFiles.forEach((pf) => {
          const existingIdx = matter.exhibits.findIndex(e => e.sha256 === pf.sha256 || e.title === pf.cleanTitle);
          const nextIdx = existingIdx >= 0 ? existingIdx : matter.exhibits.length;
          const letter = nextIdx < 26 ? String.fromCharCode(65 + nextIdx) : String(nextIdx + 1);
          const exLabel = existingIdx >= 0 ? (matter.exhibits[existingIdx].label || `Ex. ${letter}`) : `Ex. ${letter}`;

          const exObj = classifyExhibitIntake({
            id: `Ex-${letter}`,
            label: exLabel,
            party: matter.clientName || matter.clientRole || 'Proponent',
            title: pf.cleanTitle,
            date: pf.dates[0] || 'Verified Upload',
            modality: pf.modality,
            fileName: pf.fileName,
            byteSize: pf.byteSize,
            pageCount: pf.pageCount,
            sha256: pf.sha256,
            previewDataUrl: pf.previewDataUrl || '',
            exifSummary: pf.exifSummary || '',
            foundation: pf.foundation,
            purpose: pf.summarySentence,
            visualNotes: pf.visualNotes,
            pivotIntent: `Offer ${exLabel} (${pf.fileName}, SHA-256 ${pf.sha256.slice(0, 12)}…) under ${pf.foundation} to establish: ${pf.summarySentence}`,
            status: 'Ready to Offer'
          }, matter);

          if (existingIdx >= 0) {
            matter.exhibits[existingIdx] = exObj;
          } else {
            matter.exhibits.push(exObj);
          }

          // Auto-populate front-matter fields if blank and present in the uploaded evidence
          if (!matter.docketNumber && pf.docketNumber) {
            matter.docketNumber = pf.docketNumber;
          }
          if (!matter.title && pf.cleanTitle) {
            matter.title = `${pf.cleanTitle} Proceeding`;
          }

          // Extract dated events from the uploaded document and link them to this exhibit
          pf.dates.slice(0, 3).forEach((dt) => {
            const matchingClause = pf.clauses.find(c => c.includes(dt)) || pf.summarySentence;
            const alreadyInTimeline = matter.timeline.some(ev => ev.date === dt && (ev.exhibitId === exLabel || ev.title === pf.cleanTitle));
            if (!alreadyInTimeline) {
              matter.timeline.push({
                id: 'TL-' + String(matter.timeline.length + 1).padStart(2, '0'),
                date: dt,
                title: pf.cleanTitle,
                description: matchingClause,
                exhibitId: exLabel,
                exhibitLabel: exLabel
              });
            }
          });

          // Append key extracted clauses to matter.summary if summary was empty or brief
          if (pf.clauses.length > 0 && (!matter.summary || matter.summary.length < 240)) {
            const snippet = pf.clauses.slice(0, 2).join(' ');
            if (!String(matter.summary || '').includes(snippet)) {
              matter.summary = [matter.summary, snippet].filter(Boolean).join(' ').trim();
            }
          }
        });

        // Run the 22-head intake extrapolation engine to synthesize/update goals, claims, rule exceptions, direct exam Q&As, cross traps, and calculators
        extrapolateCaseFromIntake(matter, { inferArea: true });
        updateActiveMatter(matter);

        if (typeof onComplete === 'function') {
          onComplete(matter, parsedFiles);
        }
        return { parsedFiles, matter };
      }

      function renderCourtCaptionMastheadHtml(matter) {
        const m = normalizeMatter(matter || {});
        const forum = m.forum || 'IN THE TRIAL COURT / ADJUDICATIVE FORUM OF RECORD';
        const area = m.areaOfLaw || m.practiceArea || 'General Civil & Statutory Proceeding';
        const client = m.clientName || 'Proponent / Client Party';
        const role = m.clientRole || 'Respondent / Claimant';
        const opposing = m.opposingParty || 'Adverse / Opposing Party';
        const docket = m.docketNumber || 'PENDING ASSIGNMENT';
        const hearing = m.hearingDate || 'To Be Scheduled';
        const mins = Number(m.hearingMinutes) || 180;
        const counsel = m.counselName || m.representationScope || 'Counsel of Record / Self-Represented';
        const summary = m.summary || 'Open the Matter Details drawer below or upload documentary/visual evidence files (.pdf, .png, .jpg, .docx, .csv, .eml) to populate your case caption, relief posture, timeline, and statutory claims.';
        return `
          <div class="court-caption-masthead" role="region" aria-label="Formal Case Caption Masthead">
            <div class="court-caption-header">
              <span>⚖️ ${escapeHtml(forum)}</span>
              <span class="badge info" style="margin:0;">${escapeHtml(area)}</span>
            </div>
            <div class="court-caption-grid">
              <div class="court-caption-parties">
                <div style="font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--muted);font-family:var(--sans);font-weight:700;">In the Matter of:</div>
                <div style="margin-top:4px;font-weight:800;">${escapeHtml(client)},</div>
                <div style="font-size:0.84rem;color:var(--muted);font-style:italic;margin-bottom:4px;">${escapeHtml(role)},</div>
                <div style="font-weight:700;margin:2px 0;">v.</div>
                <div style="font-weight:800;margin-top:4px;">${escapeHtml(opposing)},</div>
                <div style="font-size:0.84rem;color:var(--muted);font-style:italic;">Adverse Party.</div>
              </div>
              <div class="court-caption-docket">
                <div><strong>CASE / DOCKET NO.:</strong> ${escapeHtml(docket)}</div>
                <div><strong>HEARING DATE:</strong>      ${escapeHtml(hearing)} (${mins} min)</div>
                <div><strong>COUNSEL / SCOPE:</strong>   ${escapeHtml(counsel)}</div>
                <div><strong>RECORD COUNTS:</strong>     ${(m.exhibits || []).length} Ex. · ${(m.claims || []).length} Claims · ${(m.directExam || []).length} Q&amp;As</div>
              </div>
            </div>
            <div class="court-caption-theme">
              <strong>Core Theory &amp; Posture:</strong> ${escapeHtml(summary)}
            </div>
          </div>
        `;
      }

      function computeFilingDeadlines(matter) {
        const m = normalizeMatter(matter || {});
        const rawDate = String(m.hearingDate || '').trim();
        const parsedMs = rawDate ? Date.parse(rawDate) : NaN;
        const hasValidDate = !isNaN(parsedMs);
        const baseDate = hasValidDate ? new Date(parsedMs) : null;

        const fmtDate = (offsetDays) => {
          if (!baseDate) return `T-${offsetDays} Days Before Hearing`;
          const d = new Date(baseDate.getTime() - offsetDays * 86400000);
          return d.toISOString().slice(0, 10);
        };

        const exs = m.exhibits || [];
        const claims = m.claims || [];
        const backedClaims = claims.filter(c => Array.isArray(c.exhibits) && c.exhibits.length > 0);
        const wits = m.witnesses || [];
        const dxs = m.directExam || [];
        const traps = m.traps || [];

        const milestones = [
          {
            id: 'DL-01',
            offsetDays: 42,
            dueDate: fmtDate(42),
            title: 'Mandatory Initial & Financial Disclosures',
            rule: 'FRCP 26(a)(1) & Mandatory Sworn Disclosure Rule',
            artifactType: 'disclosure-statement',
            ready: exs.length >= 1,
            statusLabel: exs.length >= 1 ? '✓ Ready (${exs.length} Exhibit(s) Logged)'.replace('${exs.length}', String(exs.length)) : '⚠️ Upload / Log Disclosure Records'
          },
          {
            id: 'DL-02',
            offsetDays: 28,
            dueDate: fmtDate(28),
            title: 'Discovery, Subpoena & Inspection Cutoff',
            rule: 'FRCP 34 & FRCP 45 Documentary Production',
            artifactType: 'exhibit-index',
            ready: exs.some(e => Boolean(e.sha256 || e.foundation)),
            statusLabel: exs.some(e => Boolean(e.sha256 || e.foundation)) ? '✓ Foundations & SHA-256 Verified' : '⚠️ Verify Exhibit Foundations'
          },
          {
            id: 'DL-03',
            offsetDays: 14,
            dueDate: fmtDate(14),
            title: 'Joint Pretrial Position Statement & Stipulations',
            rule: 'FRCP 16 Pretrial Management Order',
            artifactType: 'position-statement',
            ready: (m.reliefGoals || []).length > 0 && claims.length > 0,
            statusLabel: ((m.reliefGoals || []).length > 0 && claims.length > 0) ? '✓ Relief Posture & Claims Mapped' : '⚠️ Define Relief Goals & Claims'
          },
          {
            id: 'DL-04',
            offsetDays: 7,
            dueDate: fmtDate(7),
            title: 'Final Witness List, Exhibit Register & Trial Brief',
            rule: 'Pretrial Order Witness & Exhibit Exchange',
            artifactType: 'witness-list',
            ready: wits.length > 0 && dxs.length > 0,
            statusLabel: (wits.length > 0 && dxs.length > 0) ? `✓ ${wits.length} Witness(es) & ${dxs.length} Q&As Ready` : '⚠️ Complete Witness & Exam Script'
          },
          {
            id: 'DL-05',
            offsetDays: 3,
            dueDate: fmtDate(3),
            title: 'FRE 1006 Summaries & FRE 106 Completeness Notice',
            rule: 'FRE 1006 Voluminous Records & FRE 106 Context',
            artifactType: 'exhibit-index',
            ready: traps.length > 0 && exs.length > 0,
            statusLabel: (traps.length > 0 && exs.length > 0) ? `✓ ${traps.length} Context / Rebuttal Card(s) Ready` : '⚠️ Add Cross-Exam Context Cards'
          },
          {
            id: 'DL-06',
            offsetDays: 0,
            dueDate: fmtDate(0),
            title: 'Evidentiary Hearing & Proposed Findings Submission',
            rule: 'Admissible Proposed Findings of Fact & Conclusions of Law',
            artifactType: 'proposed-findings',
            ready: claims.length > 0 && backedClaims.length === claims.length,
            statusLabel: (claims.length > 0 && backedClaims.length === claims.length) ? `✓ All ${backedClaims.length} Findings Admissible` : '⚠️ Link Exhibits to All Claims'
          }
        ];

        return {
          hasValidDate,
          hearingDate: rawDate || 'TBD (Set Hearing Date in Step 1)',
          milestones
        };
      }

      function downloadDeadlinesIcs(matter) {
        const dl = computeFilingDeadlines(matter);
        const slug = ((matter && (matter.docketNumber || matter.title)) || 'legal-matter').toLowerCase().replace(/[^a-z0-9]+/g, '-');
        const lines = [
          'BEGIN:VCALENDAR',
          'VERSION:2.0',
          'PRODID:-//PrismLegal//On-Time Filing Schedule//EN',
          'CALSCALE:GREGORIAN'
        ];
        dl.milestones.forEach((ms) => {
          const dtRaw = /^\d{4}-\d{2}-\d{2}$/.test(ms.dueDate) ? ms.dueDate.replace(/-/g, '') : '20300918';
          lines.push(
            'BEGIN:VEVENT',
            `UID:${ms.id}-${slug}@prismlegal.local`,
            `DTSTART;VALUE=DATE:${dtRaw}`,
            `SUMMARY:[${(matter && matter.docketNumber) || 'Case Filing'}] ${ms.title}`,
            `DESCRIPTION:${ms.rule} - Status: ${ms.statusLabel}`,
            'END:VEVENT'
          );
        });
        lines.push('END:VCALENDAR');
        const blob = new Blob([lines.join('\r\n')], { type: 'text/calendar' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${slug}-filing-deadlines.ics`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }

      function generateFilingArtifact(matter, artifactType) {
        const m = normalizeMatter(matter || {});
        const forum = (m.forum || 'IN THE TRIAL COURT OF RECORD').toUpperCase();
        const docket = m.docketNumber || 'CASE NO. [PENDING]';
        const client = m.clientName || 'PROPONENT PARTY';
        const role = m.clientRole || 'Respondent / Claimant';
        const opposing = m.opposingParty || 'OPPOSING PARTY';
        const counsel = m.counselName || 'Pro Se / Trial Counsel of Record';
        const hearingDate = m.hearingDate || 'Scheduled Evidentiary Hearing';
        const framework = m.framework || m.areaOfLaw || 'Governing Statutory Framework';
        const goals = m.reliefGoals || [];
        const exs = m.exhibits || [];
        const claims = m.claims || [];
        const excs = m.ruleExceptions || [];
        const wits = m.witnesses || [];
        const clock = computeHearingClockStages(m.hearingMinutes, wits);
        const strategies = computeAdaptiveStrategySchedule(m);

        const captionBlock = [
          '==============================================================================',
          `  ${forum}`,
          '==============================================================================',
          `  In re the Matter of:`,
          `  ${client} (${role}),`,
          `  and`,
          `  ${opposing} (Adverse Party).`,
          `  ----------------------------------------------------------------------------`,
          `  DOCKET / CASE NO.: ${docket}`,
          `  HEARING DATE:      ${hearingDate} (${clock.total} Minutes Allocated)`,
          `  GOVERNING LAW:     ${framework}`,
          '==============================================================================',
          ''
        ];

        if (artifactType === 'exhibit-index') {
          const body = [
            ...captionBlock,
            '  JOINT PRETRIAL EXHIBIT INDEX, ADMISSIBILITY FOUNDATIONS & CUSTODY REGISTER',
            '==============================================================================',
            '',
            `Comes now ${client}, by and through ${counsel}, and submits this authenticated Exhibit Register for the hearing on ${hearingDate}:`,
            ''
          ];
          if (exs.length === 0) {
            body.push('  [No exhibits logged yet. Upload multi-modal evidence files or add records in Step 2/4.]', '');
          } else {
            exs.forEach((ex, i) => {
              body.push(
                `${i + 1}. EXHIBIT ${ex.label || ex.id}: ${ex.title}`,
                `   - Offering Party:       ${ex.party || client}`,
                `   - Modality / Source:    ${ex.modality || 'Documentary Record'}${ex.fileName ? ' (' + ex.fileName + ')' : ''}`,
                `   - Evidentiary Rule:     ${ex.foundation || 'FRE 901(b)(1)'}`,
                `   - SHA-256 Custody Hash: ${ex.sha256 || 'Verified Local Record'}`,
                `   - Fact Established:     ${ex.purpose || 'Corroborates chronological timeline'}`,
                `   - Visual / Page Notes:  ${typeof ex.visualNotes === 'string' ? ex.visualNotes : 'Operative pages marked for admission'}`,
                `   - Pretrial Posture:     ${ex.status || 'Ready to Offer'}`,
                ''
              );
            });
          }
          body.push(
            '------------------------------------------------------------------------------',
            `Respectfully submitted by: ${counsel} on behalf of ${client}`,
            `Dated: ${new Date().toISOString().slice(0, 10)}`
          );
          return { title: 'Joint Exhibit Index & Chain-of-Custody Register', slug: 'exhibit-index', content: body.join('\n') };
        }

        if (artifactType === 'witness-list') {
          const body = [
            ...captionBlock,
            '  TRIAL WITNESS LIST & STAGE-BY-STAGE HEARING CLOCK ALLOCATION',
            '==============================================================================',
            '',
            'I. STAGE-BY-STAGE HEARING CLOCK BUDGET:',
            ...clock.stages.map(s => `   - ${s.name}: ${s.minutes} min (${s.pct}%) — ${s.note}`),
            `   - Total Witness Exam Pool Used: ${clock.usedWitnessMinutes} / ${clock.availableExamPool} min (${clock.gateProtected ? 'Closing Gate Protected' : 'Warning: Exceeds Pool'})`,
            '',
            'II. DESIGNATED WITNESS ROSTER & SCOPE OF TESTIMONY:'
          ];
          if (wits.length === 0) {
            body.push('   [No witnesses designated yet. Add witnesses or run intake extrapolation.]', '');
          } else {
            wits.forEach((w, i) => {
              body.push(
                `   ${i + 1}. ${w.id}: ${w.name} (${w.role})`,
                `      - Call Status:        ${w.status || 'will-call'}`,
                `      - Allocated Time:     ${w.minutes} minutes`,
                `      - Scope of Testimony: ${w.scope}`,
                ''
              );
            });
          }
          body.push(
            '------------------------------------------------------------------------------',
            `Respectfully submitted by: ${counsel} on behalf of ${client}`,
            `Dated: ${new Date().toISOString().slice(0, 10)}`
          );
          return { title: 'Trial Witness List & Hearing Time Allocation', slug: 'witness-list', content: body.join('\n') };
        }

        if (artifactType === 'disclosure-statement') {
          const body = [
            ...captionBlock,
            '  MANDATORY EVIDENTIARY & FINANCIAL DISCLOSURE COMPLIANCE STATEMENT',
            '==============================================================================',
            '',
            'I. CERTIFICATION OF COMPLETE MANDATORY DISCLOSURES (FRCP 26(a)/(e)):',
            `   ${client} certifies that all documentary exhibits, financial records, and statutory calculation inputs relied upon in this proceeding have been disclosed and authenticated with chain-of-custody verification:`,
            ''
          ];
          if (exs.length === 0) {
            body.push('   - [Upload or register disclosure records in Step 1, Step 2, or Step 4.]', '');
          } else {
            exs.forEach((e) => {
              body.push(`   - [${e.label || e.id}] ${e.title} (${e.foundation || 'FRE 901'})${e.sha256 ? ' · SHA-256: ' + e.sha256.slice(0, 16) + '…' : ''} — ${e.purpose}`);
            });
            body.push('');
          }
          if (excs.length > 0) {
            body.push('II. CONTROLLING STATUTORY EXEMPTIONS & DISCLOSURE AUDITS:');
            excs.forEach((ex) => {
              body.push(`   - ${ex.rule || ex.statute}: ${ex.effect}`);
            });
            body.push('');
          }
          body.push(
            '------------------------------------------------------------------------------',
            `Certified by: ${client} & ${counsel}`,
            `Dated: ${new Date().toISOString().slice(0, 10)}`
          );
          return { title: 'Mandatory Disclosure Compliance Statement', slug: 'disclosure-statement', content: body.join('\n') };
        }

        if (artifactType === 'proposed-findings') {
          const body = [
            ...captionBlock,
            '  PROPOSED FINDINGS OF FACT, JURAL POSTURE & CONCLUSIONS OF LAW',
            '==============================================================================',
            '',
            'I. PROPOSED FINDINGS OF FACT (ANCHORED TO ADMITTED EXHIBITS):',
            ''
          ];
          if (claims.length === 0) {
            body.push('   [No statutory claims mapped yet. Populate intake facts or add claims in Step 2.]', '');
          } else {
            claims.forEach((c, idx) => {
              const prop = compileClaimProposition(c);
              const jural = classifyJuralPosture(c, m);
              body.push(
                `   Finding ${idx + 1} [${c.id} · ${c.statute}] (${jural.label || 'Enforceable Claim'}):`,
                `   ${prop.text}`,
                ''
              );
            });
          }
          body.push('II. PROPOSED CONCLUSIONS OF LAW & FINAL ORDERS:');
          if (goals.length === 0) {
            body.push('   [Define requested court orders in Step 1.]', '');
          } else {
            goals.forEach((g, idx) => {
              body.push(
                `   Order ${idx + 1} (${g.title}):`,
                `   IT IS HEREBY ORDERED that ${g.requestedOrder}`,
                `   Basis: ${g.rationale}`,
                ''
              );
            });
          }
          body.push(
            '------------------------------------------------------------------------------',
            `Submitted by: ${counsel} on behalf of ${client}`,
            `Dated: ${new Date().toISOString().slice(0, 10)}`
          );
          return { title: 'Proposed Findings of Fact & Conclusions of Law', slug: 'proposed-findings', content: body.join('\n') };
        }

        // Default: 'position-statement'
        const body = [
          ...captionBlock,
          '  PRETRIAL POSITION STATEMENT, RELIEF MOTION & CASE STRATEGY SUMMARY',
          '==============================================================================',
          '',
          'I. EXECUTIVE SUMMARY & OPENING POSTURE:',
          `   ${m.summary || 'Specify case summary or upload intake documents in Step 1.'}`,
          '',
          'II. SPECIFIC RELIEF ORDERS REQUESTED FROM THE COURT:'
        ];
        if (goals.length === 0) {
          body.push('   [No relief orders specified yet.]', '');
        } else {
          goals.forEach((g, i) => {
            body.push(`   ${i + 1}. ${g.title}: ${g.requestedOrder} (${g.rationale})`);
          });
          body.push('');
        }
        if (strategies.length > 0) {
          body.push('III. PRIORITIZED TRIAL STRATEGY & PROOF SEQUENCE:');
          strategies.forEach((s, i) => {
            body.push(`   Priority #${i + 1} [Score ${s.weight}/${s.maxWeight}] ${s.title}: ${s.focus} (${s.rationale})`);
          });
          body.push('');
        }
        body.push(
          '------------------------------------------------------------------------------',
          `Respectfully submitted by: ${counsel} on behalf of ${client}`,
          `Dated: ${new Date().toISOString().slice(0, 10)}`
        );
        return { title: 'Pretrial Position Statement & Relief Motion', slug: 'position-statement', content: body.join('\n') };
      }

      function downloadFilingArtifact(matter, artifactType) {
        const art = generateFilingArtifact(matter, artifactType);
        const slug = ((matter && (matter.docketNumber || matter.title)) || 'matter').toLowerCase().replace(/[^a-z0-9]+/g, '-');
        const blob = new Blob([art.content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${slug}-${art.slug}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }

      function renderMultiModalDropzoneHtml(prefix, subtitle) {
        return `
          <div class="intake-dropzone" id="${prefix}-dropzone" role="region" aria-label="Multi-Modal Evidence Intake Dropzone">
            <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;">
              <div style="flex:1;min-width:260px;">
                <span class="badge stip">📎 Multi-Modal Evidence Intake &amp; Auto-Linker</span>
                <span class="badge info">100% Local Browser Parsing · SHA-256 Chain of Custody</span>
                <h4 style="margin:6px 0 4px;">Drop Documentary, Visual, Financial, or Media Evidence Files Here</h4>
                <p style="margin:0;font-size:0.85rem;color:var(--muted);">${escapeHtml(subtitle || 'Upload PDFs (with FlateDecode stream extraction), images/scans (.png/.jpg/.webp/.svg with EXIF/PNG chunk inspection & visual preview), Office pleadings (.docx/.xlsx/.rtf), financial ledgers (.csv/.tsv), correspondence (.eml/.txt), or recordings. Each file is hashed (SHA-256), classified for FRE admissibility, and linked to your timeline, claims, and testimony.')}</p>
                <div class="format-chip-row" aria-label="Supported Evidence Formats">
                  <span class="format-chip">PDF (Stream &amp; Text)</span>
                  <span class="format-chip">PNG · JPG · WEBP · SVG (EXIF + Preview)</span>
                  <span class="format-chip">DOCX · XLSX · RTF</span>
                  <span class="format-chip">CSV · TSV Ledgers</span>
                  <span class="format-chip">EML · TXT · MD · HTML</span>
                  <span class="format-chip">MP3 · WAV · MP4</span>
                </div>
              </div>
              <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;">
                <label class="btn primary" style="cursor:pointer;margin:0;">
                  📂 Select Evidence Files From Device
                  <input type="file" id="${prefix}-file-input" multiple accept=".pdf,.png,.jpg,.jpeg,.webp,.gif,.bmp,.svg,.tif,.tiff,.docx,.xlsx,.odt,.rtf,.csv,.tsv,.txt,.md,.json,.eml,.html,.htm,.log,.mp3,.wav,.m4a,.ogg,.mp4,.webm,.mov,application/pdf,image/*,text/*,audio/*,video/*" style="display:none;">
                </label>
              </div>
            </div>
            <div id="${prefix}-upload-feedback" style="display:none;margin-top:10px;"></div>
          </div>
        `;
      }

      function bindMultiModalDropzoneEvents(prefix, getMatterFn, onUpdatedFn) {
        const dz = document.getElementById(`${prefix}-dropzone`);
        const inp = document.getElementById(`${prefix}-file-input`);
        const fb = document.getElementById(`${prefix}-upload-feedback`);
        if (!dz) return;

        const handleFiles = async (fileList) => {
          if (!fileList || !fileList.length) return;
          const curMatter = getMatterFn();
          if (fb) {
            fb.style.display = 'block';
            fb.className = 'finding-box';
            fb.innerHTML = `⏳ Parsing ${fileList.length} evidence file(s) locally in your browser &amp; linking to case record…`;
          }
          const res = await ingestMultiModalUploadsIntoMatter(curMatter, fileList, (updatedMatter, parsedFiles) => {
            if (fb) {
              fb.style.display = 'block';
              fb.className = 'finding-box';
              fb.innerHTML = `
                <strong>✓ Ingested &amp; Linked ${parsedFiles.length} Multi-Modal Evidence File(s):</strong>
                <div style="display:grid;gap:6px;margin-top:6px;">
                  ${parsedFiles.map(pf => `
                    <div style="display:flex;flex-wrap:wrap;align-items:center;gap:10px;">
                      ${pf.previewDataUrl ? `<img src="${escapeHtml(pf.previewDataUrl)}" alt="${escapeHtml(pf.cleanTitle)}" style="width:56px;height:40px;object-fit:cover;border-radius:4px;border:1px solid var(--border);">` : ''}
                      <div>
                        <span class="modality-badge">${escapeHtml(pf.modality)}</span>
                        <strong>${escapeHtml(pf.fileName)}</strong> (${pf.pageCount} p.)
                        → Classified under <code>${escapeHtml(pf.foundation)}</code>
                        · SHA-256: <code>${escapeHtml(pf.sha256.slice(0, 16))}…</code>
                        ${pf.exifSummary ? ` · <span>${escapeHtml(pf.exifSummary)}</span>` : ''}
                        ${pf.dates.length ? ` · Linked Date(s): <strong>${escapeHtml(pf.dates.slice(0, 2).join(', '))}</strong>` : ''}
                        ${pf.moneyAmounts.length ? ` · Quantified: <strong>${escapeHtml(pf.moneyAmounts.slice(0, 2).join(', '))}</strong>` : ''}
                      </div>
                    </div>
                  `).join('')}
                </div>
              `;
            }
            if (typeof onUpdatedFn === 'function') {
              onUpdatedFn(updatedMatter, parsedFiles);
            }
          });
          return res;
        };

        dz.addEventListener('dragover', (ev) => {
          ev.preventDefault();
          dz.classList.add('drag-active');
        });
        dz.addEventListener('dragleave', () => {
          dz.classList.remove('drag-active');
        });
        dz.addEventListener('drop', (ev) => {
          ev.preventDefault();
          dz.classList.remove('drag-active');
          if (ev.dataTransfer && ev.dataTransfer.files && ev.dataTransfer.files.length) {
            handleFiles(ev.dataTransfer.files);
          }
        });
        if (inp) {
          inp.addEventListener('change', () => {
            if (inp.files && inp.files.length) {
              handleFiles(inp.files);
              inp.value = '';
            }
          });
        }
      }

      function renderFilingCenterHtml(matter, prefix) {
        const dl = computeFilingDeadlines(matter);
        const defaultArt = generateFilingArtifact(matter, 'position-statement');
        return `
          <div class="card" style="border-left:6px solid var(--accent);">
            <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:8px;">
              <div>
                <span class="badge stip">📅 On-Time Procedural Filing Schedule &amp; Court Artifact Generator</span>
                <h3 style="margin:4px 0 0;">Backward-Scheduled Statutory Deadlines (Anchored to Hearing: ${escapeHtml(dl.hearingDate)})</h3>
              </div>
              <button type="button" class="btn" id="${prefix}-btn-dl-ics">📅 Export Deadlines to Calendar (.ics)</button>
            </div>
            <p style="margin:0 0 10px;font-size:0.86rem;color:var(--muted);">Stay on time with mandatory disclosures, pretrial stipulations, and exhibit exchanges. Each milestone below checks your current matter readiness and links directly to its court-captioned filing artifact:</p>
            <div class="deadline-grid">
              ${dl.milestones.map(ms => `
                <div class="deadline-card ${ms.ready ? 'ready' : 'urgent'}">
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:4px;">
                    <span class="badge ${ms.ready ? 'stip' : 'warn'}">T-${ms.offsetDays}d · ${escapeHtml(ms.dueDate)}</span>
                    <button type="button" class="btn ${prefix}-select-art-btn" data-art="${escapeHtml(ms.artifactType)}" style="padding:2px 8px;font-size:0.73rem;">Preview Filing</button>
                  </div>
                  <div style="font-weight:800;font-size:0.88rem;margin:6px 0 2px;">${escapeHtml(ms.title)}</div>
                  <div style="font-size:0.76rem;color:var(--muted);">${escapeHtml(ms.rule)}</div>
                  <div style="font-size:0.78rem;font-weight:700;margin-top:6px;color:${ms.ready ? 'var(--stipulated)' : 'var(--warning)'};">${escapeHtml(ms.statusLabel)}</div>
                </div>
              `).join('')}
            </div>

            <div style="margin-top:16px;padding-top:14px;border-top:1px solid var(--border);">
              <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;">
                <div>
                  <span class="badge info">📜 Court-Captioned Filing Artifact Generator</span>
                  <strong style="margin-left:4px;">Select Pleading / Filing Packet to Generate from Your Active Matter:</strong>
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:6px;" role="group" aria-label="Filing Artifact Selector">
                  <button type="button" class="btn primary ${prefix}-art-tab" data-art="position-statement">1. Pretrial Position Statement</button>
                  <button type="button" class="btn ${prefix}-art-tab" data-art="exhibit-index">2. Exhibit &amp; SHA-256 Index</button>
                  <button type="button" class="btn ${prefix}-art-tab" data-art="witness-list">3. Witness &amp; Clock Roster</button>
                  <button type="button" class="btn ${prefix}-art-tab" data-art="disclosure-statement">4. Mandatory Disclosures</button>
                  <button type="button" class="btn ${prefix}-art-tab" data-art="proposed-findings">5. Proposed Findings of Fact</button>
                </div>
              </div>
              <pre id="${prefix}-pleading-preview" class="pleading-preview" aria-label="Generated Court Filing Preview">${escapeHtml(defaultArt.content)}</pre>
              <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;">
                <button type="button" class="btn primary" id="${prefix}-btn-dl-art" data-active-art="position-statement">📄 Download Selected Court Filing (.md)</button>
                <button type="button" class="btn" id="${prefix}-btn-copy-art">📋 Copy Filing Text to Clipboard</button>
              </div>
            </div>
          </div>
        `;
      }

      function bindFilingCenterEvents(prefix, getMatterFn) {
        const icsBtn = document.getElementById(`${prefix}-btn-dl-ics`);
        const dlArtBtn = document.getElementById(`${prefix}-btn-dl-art`);
        const copyArtBtn = document.getElementById(`${prefix}-btn-copy-art`);
        const previewEl = document.getElementById(`${prefix}-pleading-preview`);

        const switchArtifact = (artType) => {
          const m = getMatterFn();
          const art = generateFilingArtifact(m, artType);
          if (previewEl) previewEl.textContent = art.content;
          if (dlArtBtn) dlArtBtn.setAttribute('data-active-art', artType);
          document.querySelectorAll(`.${prefix}-art-tab`).forEach(b => {
            b.classList.toggle('primary', b.getAttribute('data-art') === artType);
          });
        };

        document.querySelectorAll(`.${prefix}-art-tab, .${prefix}-select-art-btn`).forEach(btn => {
          btn.addEventListener('click', () => {
            switchArtifact(btn.getAttribute('data-art') || 'position-statement');
          });
        });

        if (icsBtn) {
          icsBtn.addEventListener('click', () => downloadDeadlinesIcs(getMatterFn()));
        }
        if (dlArtBtn) {
          dlArtBtn.addEventListener('click', () => {
            const artType = dlArtBtn.getAttribute('data-active-art') || 'position-statement';
            downloadFilingArtifact(getMatterFn(), artType);
          });
        }
        if (copyArtBtn && previewEl) {
          copyArtBtn.addEventListener('click', () => {
            if (navigator.clipboard && navigator.clipboard.writeText) {
              navigator.clipboard.writeText(previewEl.textContent || '');
              copyArtBtn.textContent = '✓ Copied to Clipboard';
              setTimeout(() => { copyArtBtn.textContent = '📋 Copy Filing Text to Clipboard'; }, 2000);
            }
          });
        }
      }

      window.PrismLegalStore = {
        createBlankMatter,
        normalizeMatter,
        getActiveMatter,
        ensureActiveMatter,
        updateActiveMatter,
        extractIntakeFeatureVector,
        classifyMatterIntake,
        classifyExhibitIntake,
        classifyJuralPosture,
        computeAdaptiveStrategySchedule,
        extrapolateCaseFromIntake,
        extractPdfStructureAndTextInBrowser,
        extractPngChunksMetadata,
        extractJpegExifMetadata,
        parseMultiModalFileInBrowser,
        ingestMultiModalUploadsIntoMatter,
        computeFilingDeadlines,
        generateFilingArtifact,
        compileClaimProposition,
        computeHearingClockStages,
        auditMatterConsistency
      };
"""


def render_index_html(payload):
    """`view/index.html` — Clean, User-Centered Service Home & Matter Workspace Launcher."""
    payload_json = json.dumps(payload, ensure_ascii=False)
    commit_sha = html.escape(payload.get("commit", ""))
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="prism-legal-commit" content="{commit_sha}">
  <title>PrismLegal — Legal Case Preparation &amp; Trial Readiness Service</title>
  <style>{_shared_css()}</style>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to service content</a>
  {_shared_header_html("index.html")}

  <main id="main-content" class="container" role="main">
    <!-- Section 1: Clear Role-Based Entry & Guided 5-Step Service Overview -->
    <section class="card" style="border-left:6px solid var(--accent);">
      <span class="badge stip">Free Public-Benefit Legal Service</span>
      <span class="badge info">100% Private Local Browser Workspace</span>
      <h2 style="margin:6px 0 6px;">Organize Your Facts, Prepare Your Testimony, and Build Your Trial Brief</h2>
      <p style="margin:0 0 18px;color:var(--muted);max-width:920px;">PrismLegal guides clients and attorneys through a structured 5-step preparation workflow. Everything you enter stays locally in your browser until you choose to save or share a matter file (<code>.prismlegal.json</code>) or printable summary packet.</p>

      <div class="grid-3">
        <article class="card" style="margin-bottom:0;background:var(--surface-alt);border-top:5px solid var(--stipulated);">
          <span class="badge stip">5-Step Guided Client Journey</span>
          <h3>👤 For Clients &amp; Self-Represented Litigants</h3>
          <p style="font-size:0.9rem;color:var(--muted);margin:4px 0 10px;">Prepare calmly for your hearing and organize everything your attorney or judge needs:</p>
          <ol style="font-size:0.86rem;padding-left:20px;margin:0 0 16px;">
            <li><strong>My Matter &amp; Goals:</strong> State what you are asking the court to order.</li>
            <li><strong>Timeline &amp; Documents:</strong> Log key dates and supporting exhibits.</li>
            <li><strong>Tough Questions:</strong> Practice calm responses with flashcards.</li>
            <li><strong>Direct Testimony:</strong> Rehearse your testimony step-by-step.</li>
            <li><strong>Counsel Packet:</strong> List questions for your lawyer &amp; export your file.</li>
          </ol>
          <a href="client.html" class="btn primary">Open Client Case Preparation →</a>
        </article>

        <article class="card" style="margin-bottom:0;background:var(--surface-alt);border-top:5px solid var(--accent);">
          <span class="badge info">5-Step Guided Attorney Journey</span>
          <h3>⚖️ For Attorneys &amp; Legal Aid Clinics</h3>
          <p style="font-size:0.9rem;color:var(--muted);margin:4px 0 10px;">Turn a client's facts and documents into a structured evidentiary proof matrix and trial book:</p>
          <ol style="font-size:0.86rem;padding-left:20px;margin:0 0 16px;">
            <li><strong>Matter Intake &amp; Theory:</strong> Open a client file or create a new docket.</li>
            <li><strong>Elements &amp; Proof Matrix:</strong> Map statutory claims to exhibits &amp; spot gaps.</li>
            <li><strong>Witness Examinations:</strong> Script direct/cross exams &amp; budget time.</li>
            <li><strong>Exhibits &amp; Calculators:</strong> Audit foundations &amp; run statutory worksheets.</li>
            <li><strong>Trial Brief &amp; Handoff:</strong> Answer client notes &amp; export the trial brief.</li>
          </ol>
          <a href="lawyer.html" class="btn primary">Open Attorney Workbench →</a>
        </article>

        <article class="card" style="margin-bottom:0;background:var(--surface-alt);border-top:5px solid var(--warning);">
          <span class="badge warn">Day-of-Hearing Companion</span>
          <h3>🏛️ For the Witness Stand &amp; Counsel Table</h3>
          <p style="font-size:0.9rem;color:var(--muted);margin:4px 0 10px;">Distraction-free, large-type reference built directly from your active matter during live proceedings:</p>
          <ul style="font-size:0.86rem;padding-left:20px;margin:0 0 16px;">
            <li><strong>Live Hearing Clock:</strong> Track remaining minutes across hearing stages.</li>
            <li><strong>Instant Pivot Responder:</strong> One-click calm responses to opposing claims.</li>
            <li><strong>Direct Testimony Checklist:</strong> Check off questions as they are asked.</li>
            <li><strong>Live Exhibit Tracker:</strong> Mark exhibits Offered, Admitted, or Objected.</li>
          </ul>
          <a href="courtroom.html" class="btn primary">Open Hearing Companion →</a>
        </article>
      </div>
    </section>

    <!-- Section 2: Start Your New Legal Matter OR Open Your Workspace Matters -->
    <section class="grid-2">
      <div class="card" style="border-top:5px solid var(--stipulated);margin-bottom:0;">
        <span class="badge stip">Quick Start · New Matter</span>
        <h2>+ Start a New Legal Matter</h2>
        <p style="margin:0 0 12px;font-size:0.9rem;color:var(--muted);">Enter a title and area of law to launch your workspace immediately. You can add or refine court and party details at any time:</p>

        <div class="form-grid">
          <label class="field-label">Case / Matter Title
            <input type="text" id="new-title" class="search-input" value="" aria-label="Case or Matter Title">
          </label>
          <label class="field-label">Area of Law
            <select id="new-area" class="btn">
              <option value="Family &amp; Parenting Law">Family &amp; Parenting Law</option>
              <option value="Housing &amp; Tenant Rights">Housing &amp; Tenant Rights</option>
              <option value="Veterans &amp; Administrative Appeals">Veterans &amp; Administrative Appeals</option>
              <option value="Employment &amp; Wage Protection">Employment &amp; Wage Protection</option>
              <option value="Consumer, Debt &amp; Small Claims">Consumer, Debt &amp; Small Claims</option>
              <option value="Civil Litigation &amp; Probate">Civil Litigation &amp; Probate</option>
            </select>
          </label>
        </div>

        <div style="display:flex;flex-wrap:wrap;gap:10px;margin:12px 0;">
          <button type="button" class="btn primary" id="btn-create-go-client">Create &amp; Start in Client Workspace →</button>
          <button type="button" class="btn" id="btn-create-go-lawyer">Create &amp; Start in Counsel Workbench →</button>
        </div>

        <div id="home-multimodal-intake"></div>

        <details class="action-drawer">
          <summary>Optional: Add Court, Docket Number, Party Names &amp; Hearing Date</summary>
          <div class="form-grid">
            <label class="field-label">Court, Agency, or Forum
              <input type="text" id="new-forum" class="search-input" value="" aria-label="Court or Forum">
            </label>
            <label class="field-label">Case / Docket Number (if assigned)
              <input type="text" id="new-docket" class="search-input" value="" aria-label="Docket Number">
            </label>
            <label class="field-label">Your Name / Party Designation
              <input type="text" id="new-client" class="search-input" value="" aria-label="Your Name or Party Designation">
            </label>
            <label class="field-label">Your Role in the Case
              <select id="new-role" class="btn">
                <option value="Respondent / Defendant">Respondent / Defendant</option>
                <option value="Petitioner / Plaintiff / Claimant">Petitioner / Plaintiff / Claimant</option>
                <option value="Appellant / Applicant">Appellant / Applicant</option>
                <option value="Tenant / Household">Tenant / Household</option>
              </select>
            </label>
            <label class="field-label">Opposing Party
              <input type="text" id="new-opposing" class="search-input" value="" aria-label="Opposing Party">
            </label>
            <label class="field-label">Next Hearing or Filing Date
              <input type="date" id="new-date" class="search-input" value="" aria-label="Hearing Date">
            </label>
          </div>
          <label class="field-label">Brief Summary of What This Matter Is About
            <input type="text" id="new-summary" class="search-input" value="" aria-label="Brief Summary">
          </label>
        </details>
      </div>

      <div class="card" style="border-top:5px solid var(--accent);margin-bottom:0;">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px;">
          <div>
            <span class="badge info">Your Local Workspace</span>
            <h2 style="margin:4px 0 0;">My Saved Legal Matters</h2>
          </div>
          <label class="btn" style="cursor:pointer;">
            📂 Open Matter File (.json)
            <input type="file" id="inp-open-matter" accept=".json" style="display:none;">
          </label>
        </div>
        <p style="margin:0 0 12px;font-size:0.88rem;color:var(--muted);">Only matters that you create, save, or import appear here. Reference examples are kept separate below so your workspace stays clean:</p>

        <div id="workspace-matters-list"></div>
      </div>
    </section>

    <!-- Section 3: Reference Example Matters for Pedagogical Learning -->
    <section class="card" id="example-matters-section" style="margin-top:18px;">
      <span class="badge info">📘 Reference Example Matters (Learn by Example Across 6 Practice Areas)</span>
      <h3>Explore Reference Example Matters to See How Each Part of PrismLegal Works</h3>
      <p style="margin:0 0 14px;font-size:0.88rem;color:var(--muted);">These 6 reference cases show how relief goals, timelines, exhibits, statutory claims, and testimony scripts work in practice. <strong>Previewing an example does not add it to your Saved Matters</strong>—or click <em>Save a Copy</em> if you want to customize one in your workspace:</p>
      <div class="grid-3" id="templates-grid">
        <div class="card" style="margin-bottom:0;background:var(--surface-alt);">
          <span class="badge stip">📘 Example · Family &amp; Parenting Law</span>
          <h4>Parenting Plan &amp; Guideline Support Benchmark (30 Exhibits · 36 Q&amp;As)</h4>
          <p style="font-size:0.86rem;color:var(--muted);margin:4px 0 12px;">Complete trial benchmark with 6 relief pillars, 16 timeline milestones, 30 exhibits with visual annotations, 24 statutory claims, 16 cross-exam flashcards, and 36 direct Q&amp;As.</p>
          <div style="display:flex;flex-wrap:wrap;gap:6px;">
            <button type="button" class="btn primary" data-preview-example="EXAMPLE-FAMILY">👁️ Preview Example</button>
            <button type="button" class="btn" data-load-template="family">📋 Save a Copy</button>
          </div>
        </div>
        <div class="card" style="margin-bottom:0;background:var(--surface-alt);">
          <span class="badge stip">📘 Example · Housing &amp; Tenant Rights</span>
          <h4>Warranty of Habitability &amp; Rent Escrow Proceeding</h4>
          <p style="font-size:0.86rem;color:var(--muted);margin:4px 0 12px;">Includes repair notice timeline, municipal code inspection exhibit, court rent-escrow receipts, and 40% rent abatement worksheet.</p>
          <div style="display:flex;flex-wrap:wrap;gap:6px;">
            <button type="button" class="btn primary" data-preview-example="EXAMPLE-HOUSING">👁️ Preview Example</button>
            <button type="button" class="btn" data-load-template="housing">📋 Save a Copy</button>
          </div>
        </div>
        <div class="card" style="margin-bottom:0;background:var(--surface-alt);">
          <span class="badge info">📘 Example · Veterans &amp; Administrative Appeals</span>
          <h4>Service-Connected Disability &amp; Unemployability (TDIU) Appeal</h4>
          <p style="font-size:0.86rem;color:var(--muted);margin:4px 0 12px;">Includes 38 C.F.R. §§ 4.25 &amp; 4.16 combined rating claim, independent medical nexus exhibit, and administrative hearing testimony script.</p>
          <div style="display:flex;flex-wrap:wrap;gap:6px;">
            <button type="button" class="btn primary" data-preview-example="EXAMPLE-VETERANS">👁️ Preview Example</button>
            <button type="button" class="btn" data-load-template="veterans">📋 Save a Copy</button>
          </div>
        </div>
        <div class="card" style="margin-bottom:0;background:var(--surface-alt);">
          <span class="badge info">📘 Example · Employment &amp; Wage Protection</span>
          <h4>Workplace Reasonable Accommodation Proceeding</h4>
          <p style="font-size:0.86rem;color:var(--muted);margin:4px 0 12px;">Includes performance evaluation timeline, physician accommodation request exhibit, interactive-process claim matrix, and testimony script.</p>
          <div style="display:flex;flex-wrap:wrap;gap:6px;">
            <button type="button" class="btn primary" data-preview-example="EXAMPLE-EMPLOYMENT">👁️ Preview Example</button>
            <button type="button" class="btn" data-load-template="employment">📋 Save a Copy</button>
          </div>
        </div>
        <div class="card" style="margin-bottom:0;background:var(--surface-alt);">
          <span class="badge warn">📘 Example · Consumer, Debt &amp; Small Claims</span>
          <h4>Chain of Assignment &amp; FDCPA Debt Validation Defense</h4>
          <p style="font-size:0.86rem;color:var(--muted);margin:4px 0 12px;">Includes 15 U.S.C. § 1692g validation demand, FRE 803(6) third-party hearsay objection, and chain-of-title proof matrix.</p>
          <div style="display:flex;flex-wrap:wrap;gap:6px;">
            <button type="button" class="btn primary" data-preview-example="EXAMPLE-CONSUMER">👁️ Preview Example</button>
            <button type="button" class="btn" data-load-template="consumer">📋 Save a Copy</button>
          </div>
        </div>
        <div class="card" style="margin-bottom:0;background:var(--surface-alt);">
          <span class="badge warn">📘 Example · Civil Litigation &amp; Probate</span>
          <h4>Contract Performance &amp; Fiduciary Accounting Proceeding</h4>
          <p style="font-size:0.86rem;color:var(--muted);margin:4px 0 12px;">Includes Operating Agreement distribution clause, CPA FRE 1006 ledger tie-out, and expectation damages worksheet.</p>
          <div style="display:flex;flex-wrap:wrap;gap:6px;">
            <button type="button" class="btn primary" data-preview-example="EXAMPLE-COMMERCIAL">👁️ Preview Example</button>
            <button type="button" class="btn" data-load-template="commercial">📋 Save a Copy</button>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer" role="contentinfo">
    <strong>PrismLegal — Free Public-Benefit Legal Case Preparation &amp; Trial Readiness Service</strong><br>
    Open-Source Public-Benefit Release (MIT / Apache-2.0) · 100% Local Browser Workspace
  </footer>

  <script id="case-model-data" type="application/json">{payload_json}</script>
  <script>
    (function() {{
      {_shared_js_helpers()}

      const mattersList = document.getElementById('workspace-matters-list');

      function renderMattersList() {{
        workspace = loadWorkspace();
        const active = getActiveMatter();
        if (workspace.matters.length === 0) {{
          mattersList.innerHTML = `
            <div class="empty-state" style="text-align:left;padding:18px;">
              <span class="badge info">0 Saved Matters</span>
              <h3 style="margin:6px 0 4px;">You haven't saved any legal matters yet.</h3>
              <p style="margin:0 0 12px;font-size:0.88rem;color:var(--muted);">PrismLegal does not pre-fill your workspace with default cases. Matters only appear here when you create and save your own case, or when you open a <code>.prismlegal.json</code> file.</p>
              <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <button type="button" class="btn primary" id="btn-focus-new-matter">+ Start My New Matter on the Left</button>
                <a href="#example-matters-section" class="btn">📘 Explore Example Matters Below</a>
              </div>
            </div>
          `;
          const focusBtn = document.getElementById('btn-focus-new-matter');
          if (focusBtn) {{
            focusBtn.addEventListener('click', () => {{
              const inp = document.getElementById('new-title');
              if (inp) {{ inp.focus(); inp.select(); }}
            }});
          }}
          return;
        }}
        mattersList.innerHTML = workspace.matters.map(m => {{
          const isAct = active && active.id === m.id;
          return `
            <article class="card" style="margin-bottom:10px;padding:14px;background:var(--surface-alt);${{isAct ? 'border:2px solid var(--stipulated);' : ''}}">
              <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px;margin-bottom:6px;">
                <div>
                  ${{m.practiceArea ? `<span class="badge stip">${{escapeHtml(m.practiceArea)}}</span>` : ''}}
                  ${{m.docketNumber ? `<span class="badge info">${{escapeHtml(m.docketNumber)}}</span>` : ''}}
                  ${{isAct ? '<span class="badge stip">★ Active Saved Matter</span>' : ''}}
                </div>
                <button type="button" class="btn danger-btn del-matter-btn" data-mid="${{escapeHtml(m.id)}}">Remove</button>
              </div>
              <h3 style="margin:4px 0;">${{escapeHtml(m.title || 'Untitled Matter')}}</h3>
              <div style="font-size:0.83rem;color:var(--muted);margin-bottom:6px;">
                <strong>Court:</strong> ${{escapeHtml(m.forum || '—')}} · <strong>Hearing:</strong> ${{escapeHtml(m.hearingDate || '—')}}<br>
                <strong>Counts:</strong> ${{(m.goals || []).length}} Goals · ${{(m.timeline || []).length}} Events · ${{(m.exhibits || []).length}} Exhibits · ${{(m.directExam || []).length}} Direct Q&amp;As · ${{(m.traps || []).length}} Cross Topics
              </div>
              <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;">
                <button type="button" class="btn primary open-client-btn" data-mid="${{escapeHtml(m.id)}}">👤 Open as Client</button>
                <button type="button" class="btn open-lawyer-btn" data-mid="${{escapeHtml(m.id)}}">⚖️ Open as Attorney</button>
                <button type="button" class="btn open-court-btn" data-mid="${{escapeHtml(m.id)}}">🏛️ Courtroom Mode</button>
                <button type="button" class="btn export-matter-btn" data-mid="${{escapeHtml(m.id)}}">💾 Export .json</button>
              </div>
            </article>
          `;
        }}).join('');

        mattersList.querySelectorAll('.open-client-btn').forEach(b => {{
          b.addEventListener('click', () => {{
            workspace.activeMatterId = b.dataset.mid;
            saveWorkspace();
            window.location.href = 'client.html';
          }});
        }});
        mattersList.querySelectorAll('.open-lawyer-btn').forEach(b => {{
          b.addEventListener('click', () => {{
            workspace.activeMatterId = b.dataset.mid;
            saveWorkspace();
            window.location.href = 'lawyer.html';
          }});
        }});
        mattersList.querySelectorAll('.open-court-btn').forEach(b => {{
          b.addEventListener('click', () => {{
            workspace.activeMatterId = b.dataset.mid;
            saveWorkspace();
            window.location.href = 'courtroom.html';
          }});
        }});
        mattersList.querySelectorAll('.export-matter-btn').forEach(b => {{
          b.addEventListener('click', () => {{
            const found = workspace.matters.find(x => x.id === b.dataset.mid);
            if (found) exportMatterJson(found);
          }});
        }});
        mattersList.querySelectorAll('.del-matter-btn').forEach(b => {{
          b.addEventListener('click', () => {{
            workspace.matters = workspace.matters.filter(x => x.id !== b.dataset.mid);
            if (workspace.activeMatterId === b.dataset.mid) {{
              workspace.activeMatterId = workspace.matters[0] ? workspace.matters[0].id : '';
            }}
            saveWorkspace();
            renderMattersList();
          }});
        }});
      }}
      renderMattersList();

      function createFromFormAndGo(targetUrl) {{
        const m = createBlankMatter({{
          title: (document.getElementById('new-title').value || '').trim(),
          practiceArea: document.getElementById('new-area').value,
          areaOfLaw: document.getElementById('new-area').value,
          forum: (document.getElementById('new-forum').value || '').trim(),
          docketNumber: (document.getElementById('new-docket').value || '').trim(),
          clientName: (document.getElementById('new-client').value || '').trim(),
          clientRole: document.getElementById('new-role').value,
          opposingParty: (document.getElementById('new-opposing').value || '').trim(),
          hearingDate: (document.getElementById('new-date').value || '').trim(),
          summary: (document.getElementById('new-summary').value || '').trim()
        }});
        extrapolateCaseFromIntake(m, {{ inferArea: true }});
        workspace.matters.push(m);
        workspace.activeMatterId = m.id;
        saveWorkspace();
        window.location.href = targetUrl;
      }}

      document.getElementById('btn-create-go-client').addEventListener('click', () => createFromFormAndGo('client.html'));
      document.getElementById('btn-create-go-lawyer').addEventListener('click', () => createFromFormAndGo('lawyer.html'));

      const homeMmWrap = document.getElementById('home-multimodal-intake');
      if (homeMmWrap) {{
        homeMmWrap.innerHTML = renderMultiModalDropzoneHtml('home-mm', 'Drop notices, orders, financial CSVs, PDFs, or photos here to auto-create your matter and populate your timeline, claims, and testimony.');
        bindMultiModalDropzoneEvents('home-mm', () => {{
          let cur = getActiveMatter();
          if (!cur || cur.isExample) {{
            cur = createBlankMatter({{
              title: (document.getElementById('new-title').value || '').trim(),
              practiceArea: document.getElementById('new-area').value,
              areaOfLaw: document.getElementById('new-area').value,
              forum: (document.getElementById('new-forum').value || '').trim(),
              docketNumber: (document.getElementById('new-docket').value || '').trim(),
              clientName: (document.getElementById('new-client').value || '').trim(),
              clientRole: document.getElementById('new-role').value,
              opposingParty: (document.getElementById('new-opposing').value || '').trim(),
              hearingDate: (document.getElementById('new-date').value || '').trim(),
              summary: (document.getElementById('new-summary').value || '').trim()
            }});
          }}
          return cur;
        }}, (updatedMatter) => {{
          if (updatedMatter.title && !document.getElementById('new-title').value) {{
            document.getElementById('new-title').value = updatedMatter.title;
          }}
          if (updatedMatter.docketNumber && !document.getElementById('new-docket').value) {{
            document.getElementById('new-docket').value = updatedMatter.docketNumber;
          }}
          renderMattersList();
        }});
      }}

      document.getElementById('inp-open-matter').addEventListener('change', (ev) => {{
        const file = ev.target.files && ev.target.files[0];
        importMatterFromFile(file, () => renderMattersList());
      }});

      document.querySelectorAll('[data-preview-example]').forEach(btn => {{
        btn.addEventListener('click', () => {{
          const exId = btn.getAttribute('data-preview-example');
          setActiveMatterId(exId);
          window.location.href = 'client.html';
        }});
      }});

      document.querySelectorAll('[data-load-template]').forEach(btn => {{
        btn.addEventListener('click', () => {{
          const key = btn.dataset.loadTemplate;
          copyExampleToSavedMatters(key);
          renderMattersList();
        }});
      }});
    }})();
  </script>
</body>
</html>
"""


def render_client_html(payload):
    """`view/client.html` — Five-Step Guided Client Case Preparation Journey."""
    payload_json = json.dumps(payload, ensure_ascii=False)
    commit_sha = html.escape(payload.get("commit", ""))
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="prism-legal-commit" content="{commit_sha}">
  <title>Client Case Preparation — PrismLegal Public-Benefit Legal Platform</title>
  <style>{_shared_css()}</style>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to Client Case Preparation</a>
  {_shared_header_html("client.html")}

  <main id="main-content" class="container" role="main">
    <!-- Active Matter Selector & File Controls -->
    <div class="matter-bar" aria-label="Active Matter Controls">
      <div class="matter-bar-left">
        <span class="badge info">👤 Client Case Preparation</span>
        <label style="font-size:0.86rem;font-weight:700;display:flex;align-items:center;gap:6px;">
          Active Matter:
          <select id="client-matter-select" class="btn" aria-label="Select Active Matter"></select>
        </label>
        <span id="client-matter-meta" style="font-size:0.82rem;color:var(--muted);"></span>
      </div>
      <div class="matter-bar-right">
        <a href="index.html" class="btn">+ New or Switch Matter</a>
        <label class="btn" style="cursor:pointer;margin:0;">
          📂 Open File (.json)
          <input type="file" id="client-import-file" accept=".json,application/json" style="display:none;">
        </label>
        <button type="button" class="btn primary" id="btn-client-export-json">💾 Save Matter (.json)</button>
      </div>
    </div>

    <!-- 5-Step Guided Client Journey Stepper -->
    <nav class="journey-stepper" aria-label="Client 5-Step Case Preparation Journey">
      <button type="button" class="step-tab" aria-selected="true" data-target="client-step-1">
        <span class="step-num">1</span>
        <span>
          <span class="step-title">My Matter &amp; Goals</span>
          <span class="step-sub">What You Ask the Court to Order</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="client-step-2">
        <span class="step-num">2</span>
        <span>
          <span class="step-title">Timeline &amp; Documents</span>
          <span class="step-sub">Key Dates &amp; Supporting Records</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="client-step-3">
        <span class="step-num">3</span>
        <span>
          <span class="step-title">Tough Questions</span>
          <span class="step-sub">Flashcard Rehearsal &amp; Calm Pivots</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="client-step-4">
        <span class="step-num">4</span>
        <span>
          <span class="step-title">My Direct Testimony</span>
          <span class="step-sub">Question-by-Question Walkthrough</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="client-step-5">
        <span class="step-num">5</span>
        <span>
          <span class="step-title">Counsel Notes &amp; Export</span>
          <span class="step-sub">Questions for Lawyer &amp; Case Packet</span>
        </span>
      </button>
    </nav>

    <!-- STEP 1: ORIENTATION — MY MATTER & RELIEF GOALS -->
    <section id="client-step-1" class="workspace-section active">
      <div id="client-pedagogy-1"></div>

      <div class="card" style="border-left:6px solid var(--accent);">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-start;gap:12px;">
          <div>
            <span class="badge info">Step 1 of 5 · Matter Overview &amp; Relief Posture</span>
            <h2 id="cm-summary-heading" style="margin:4px 0 4px;">Your Legal Matter Overview</h2>
            <p id="cm-summary-sub" style="margin:0;color:var(--muted);font-size:0.9rem;"></p>
          </div>
          <span id="cm-save-status" style="font-size:0.84rem;color:var(--stipulated);font-weight:700;"></span>
        </div>
        <div id="cm-summary-box" style="margin-top:10px;margin-bottom:8px;"></div>
        <div id="client-step1-multimodal"></div>

        <details class="action-drawer">
          <summary>✏️ Edit Matter Title, Area of Law, Court, Docket &amp; Party Names</summary>
          <div class="form-grid" style="margin-bottom:12px;">
            <div class="form-field">
              <label for="cm-title">Matter Title</label>
              <input type="text" id="cm-title" class="search-input">
            </div>
            <div class="form-field">
              <label for="cm-area">Area of Law</label>
              <select id="cm-area" class="btn" style="width:100%;">
                <option value="Family &amp; Parenting Law">Family &amp; Parenting Law</option>
                <option value="Housing &amp; Tenant Rights">Housing &amp; Tenant Rights</option>
                <option value="Veterans &amp; Administrative Appeals">Veterans &amp; Administrative Appeals</option>
                <option value="Employment &amp; Wage Protection">Employment &amp; Wage Protection</option>
                <option value="Consumer, Debt &amp; Small Claims">Consumer, Debt &amp; Small Claims</option>
                <option value="Civil Litigation &amp; Probate">Civil Litigation &amp; Probate</option>
              </select>
            </div>
            <div class="form-field">
              <label for="cm-forum">Court, Board, or Agency Forum</label>
              <input type="text" id="cm-forum" class="search-input">
            </div>
            <div class="form-field">
              <label for="cm-docket">Case / Docket Number</label>
              <input type="text" id="cm-docket" class="search-input">
            </div>
            <div class="form-field">
              <label for="cm-date">Scheduled Hearing or Filing Date</label>
              <input type="text" id="cm-date" class="search-input">
            </div>
            <div class="form-field">
              <label for="cm-client">Your Name / Party Role</label>
              <input type="text" id="cm-client" class="search-input">
            </div>
            <div class="form-field">
              <label for="cm-opposing">Opposing Party</label>
              <input type="text" id="cm-opposing" class="search-input">
            </div>
            <div class="form-field">
              <label for="cm-counsel">Your Attorney / Clinic (Optional)</label>
              <input type="text" id="cm-counsel" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:12px;">
            <label for="cm-summary">Core Opening Theme &amp; Matter Summary (2–3 Calm Sentences)</label>
            <textarea id="cm-summary" class="search-input" style="height:76px;"></textarea>
          </div>
          <button type="button" class="btn primary" id="btn-save-cm-meta">💾 Save Matter Details</button>
        </details>
      </div>

      <div class="card">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px;">
          <div>
            <span class="badge stip">Your Relief Goals</span>
            <h3 style="margin:4px 0 0;">Specific Orders You Are Requesting from the Decision-Maker</h3>
          </div>
          <button type="button" class="btn" id="btn-add-domain-goals">✨ Auto-Complete Strategy, Claims &amp; Testimony from My Case Details</button>
        </div>
        <div id="client-goals-list" class="grid-3" style="margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Add a Custom Relief Goal</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="goal-title-in">Goal Category (e.g., Parenting Schedule, Rent Abatement, Service Connection)</label>
              <input type="text" id="goal-title-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="goal-req-in">Exact Order Requested</label>
              <input type="text" id="goal-req-in" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="goal-rat-in">Why This Order Is Fair &amp; Supported by the Record</label>
            <input type="text" id="goal-rat-in" class="search-input">
          </div>
          <button type="button" class="btn primary" id="btn-add-goal">+ Save Relief Goal</button>
        </details>

        <div class="step-footer">
          <a href="index.html" class="btn">← Back to Overview &amp; Matters</a>
          <button type="button" class="btn primary" data-goto-step="client-step-2">Continue to Step 2: Timeline &amp; Documents →</button>
        </div>
      </div>
    </section>

    <!-- STEP 2: SUBSTANCE — TIMELINE & SUPPORTING DOCUMENTS -->
    <section id="client-step-2" class="workspace-section">
      <div id="client-pedagogy-2"></div>

      <div class="card" style="border-left:6px solid var(--stipulated);">
        <span class="badge stip">Step 2 of 5 · Factual Timeline &amp; Supporting Documents</span>
        <h2>Build Your Chronological Timeline &amp; Organize Your Exhibits</h2>
        <p style="margin:0 0 12px;color:var(--muted);">Clear dates and organized documents make your story easy to verify. Add each key event in chronological order and log the records that prove it.</p>
        <div id="client-timeline-svg" class="svg-frame" style="margin-bottom:14px;"></div>
        <div id="client-timeline-list" style="margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Add a Chronological Event to Timeline</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="tl-date-in">Date (YYYY-MM-DD or Month/Year)</label>
              <input type="text" id="tl-date-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="tl-title-in">Event Headline</label>
              <input type="text" id="tl-title-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="tl-ex-in">Supporting Document / Exhibit Label</label>
              <input type="text" id="tl-ex-in" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="tl-desc-in">What Happened &amp; Why It Matters</label>
            <input type="text" id="tl-desc-in" class="search-input">
          </div>
          <button type="button" class="btn primary" id="btn-add-tl">+ Save Timeline Event</button>
        </details>
      </div>

      <div class="card">
        <span class="badge info">Supporting Documents &amp; Records</span>
        <h3>Your Document &amp; Exhibit Checklist</h3>
        <div id="client-step2-multimodal"></div>
        <div id="client-exhibits-list" class="grid-2" style="margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Add a Supporting Document or Exhibit</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="cex-label-in">Exhibit Label (e.g., Ex. A, Ex. 1)</label>
              <input type="text" id="cex-label-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="cex-title-in">Document Title</label>
              <input type="text" id="cex-title-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="cex-date-in">Document Date</label>
              <input type="text" id="cex-date-in" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="cex-purpose-in">What Fact Does This Document Prove?</label>
            <input type="text" id="cex-purpose-in" class="search-input">
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="cex-file-in">Attach Document, PDF, or Image File from Device (Optional — Computes SHA-256 &amp; Extracts Dates/Preview)</label>
            <input type="file" id="cex-file-in" class="search-input" accept=".pdf,.png,.jpg,.jpeg,.webp,.gif,.bmp,.svg,.docx,.xlsx,.rtf,.csv,.tsv,.txt,.md,.eml">
          </div>
          <button type="button" class="btn primary" id="btn-add-cex">+ Save Supporting Document</button>
        </details>

        <div class="step-footer">
          <button type="button" class="btn" data-goto-step="client-step-1">← Previous: Step 1 (My Matter &amp; Goals)</button>
          <button type="button" class="btn primary" data-goto-step="client-step-3">Continue to Step 3: Tough Questions →</button>
        </div>
      </div>
    </section>

    <!-- STEP 3: CHALLENGE — TOUGH QUESTIONS & FLASHCARD REHEARSAL -->
    <section id="client-step-3" class="workspace-section">
      <div id="client-pedagogy-3"></div>

      <div class="card" style="border-left:6px solid var(--warning);">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px;">
          <div>
            <span class="badge warn">Step 3 of 5 · Cross-Examination &amp; Rule 106 Context Rehearsal</span>
            <h2 style="margin:4px 0 0;">Practice Answering Difficult Questions Calmly &amp; Factually</h2>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;">
            <label style="font-size:0.86rem;font-weight:700;display:flex;align-items:center;gap:6px;cursor:pointer;">
              <input type="checkbox" id="chk-blind-drill" checked> Hide Answer First (Self-Test Mode)
            </label>
            <button type="button" class="btn" id="btn-prev-card">← Previous</button>
            <span id="flashcard-counter" style="font-weight:700;font-size:0.9rem;">0 / 0</span>
            <button type="button" class="btn primary" id="btn-next-card">Next →</button>
          </div>
        </div>
        <div id="flashcard-stage"></div>
      </div>

      <div class="card">
        <h3>All Anticipated Tough Questions &amp; Planned Responses</h3>
        <div id="client-traps-list" class="grid-2" style="margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Add a Tough Question or Out-of-Context Quote to Prepare For</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="tr-title-in">Topic / Issue Name</label>
              <input type="text" id="tr-title-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="tr-ex-in">Supporting Exhibit Label</label>
              <input type="text" id="tr-ex-in" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="tr-q-in">Anticipated Hostile Question or Allegation</label>
            <input type="text" id="tr-q-in" class="search-input">
          </div>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="tr-avoid-in">Mistake / Trap to Avoid</label>
              <input type="text" id="tr-avoid-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="tr-say-in">Your Calm, Factual Answer</label>
              <input type="text" id="tr-say-in" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="tr-r106-in">Rule of Completeness (FRE 106) Full Context (Optional: if opposing side quotes a text/email/journal out of context)</label>
            <input type="text" id="tr-r106-in" class="search-input">
          </div>
          <button type="button" class="btn primary" id="btn-add-trap">+ Save Tough Question Card</button>
        </details>

        <div class="step-footer">
          <button type="button" class="btn" data-goto-step="client-step-2">← Previous: Step 2 (Timeline &amp; Documents)</button>
          <button type="button" class="btn primary" data-goto-step="client-step-4">Continue to Step 4: My Direct Testimony →</button>
        </div>
      </div>
    </section>

    <!-- STEP 4: PROOF — MY DIRECT TESTIMONY WALKTHROUGH -->
    <section id="client-step-4" class="workspace-section">
      <div id="client-pedagogy-4"></div>

      <div class="card" style="border-left:6px solid var(--accent);">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px;">
          <div>
            <span class="badge info">Step 4 of 5 · Direct Testimony Walkthrough</span>
            <h2 style="margin:4px 0 0;">Rehearse Your Direct Examination Questions &amp; Answers</h2>
          </div>
          <button type="button" class="btn" id="btn-gen-dx-from-goals">⚡ + Generate Foundational Questions from My Goals &amp; Exhibits</button>
        </div>
        <p style="margin:0 0 14px;color:var(--muted);">Review each question your attorney will ask on direct examination (or the points you will present in your statement to the court) and refine your answers so they are clear, truthful, and tied to your exhibits.</p>

        <div id="client-dx-list" class="grid-2" style="margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Add a Direct Testimony Question &amp; Planned Answer</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="dx-ch-in">Topic / Chapter</label>
              <input type="text" id="dx-ch-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="dx-ex-in">Exhibit to Introduce or Reference</label>
              <input type="text" id="dx-ex-in" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="dx-q-in">Direct Examination Question</label>
            <input type="text" id="dx-q-in" class="search-input">
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="dx-a-in">Your Planned Answer on the Stand</label>
            <textarea id="dx-a-in" class="search-input" style="height:68px;"></textarea>
          </div>
          <button type="button" class="btn primary" id="btn-add-dx">+ Save Direct Testimony Q&amp;A</button>
        </details>

        <div class="step-footer">
          <button type="button" class="btn" data-goto-step="client-step-3">← Previous: Step 3 (Tough Questions)</button>
          <button type="button" class="btn primary" data-goto-step="client-step-5">Continue to Step 5: Counsel Notes &amp; Export →</button>
        </div>
      </div>
    </section>

    <!-- STEP 5: RESOLUTION — COUNSEL NOTES & EXPORT CASE PACKET -->
    <section id="client-step-5" class="workspace-section">
      <div id="client-pedagogy-5"></div>

      <div class="card" style="border-left:6px solid var(--stipulated);">
        <span class="badge stip">Step 5 of 5 · Readiness Summary, Consistency Check &amp; Export</span>
        <h2>Your Hearing Readiness &amp; Portable Case Packet</h2>
        <div id="client-readiness-kpis" class="kpi-strip" style="margin-top:12px;"></div>
        <div id="client-consistency-audit" class="grid-2" style="margin-bottom:14px;"></div>

        <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:14px;">
          <button type="button" class="btn primary" id="btn-step5-export-json">💾 Download Matter File for My Lawyer (.prismlegal.json)</button>
          <button type="button" class="btn" id="btn-step5-export-md">📄 Download Printable Case Packet (.md)</button>
          <button type="button" class="btn" id="btn-step5-print">🖨️ Print Summary</button>
          <a href="courtroom.html" class="btn">🏛️ Open Courtroom Mode →</a>
        </div>
      </div>

      <div id="client-step5-filing-center"></div>

      <div class="card">
        <span class="badge info">Client ↔ Attorney Strategy Agenda</span>
        <h3>Questions &amp; Notes for Your Attorney</h3>
        <p style="margin:0 0 12px;color:var(--muted);">Log questions here as you prepare. When you export your matter file and share it with your lawyer, these questions appear directly in their Counsel Workbench.</p>
        <div id="client-agenda-list" style="margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Add a Question or Note for Your Lawyer</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="ag-topic-in">Related Topic or Exhibit</label>
              <input type="text" id="ag-topic-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="ag-q-in">Your Question for Counsel</label>
              <input type="text" id="ag-q-in" class="search-input">
            </div>
          </div>
          <button type="button" class="btn primary" id="btn-add-agenda">+ Save Question for Counsel</button>
        </details>

        <div class="step-footer">
          <button type="button" class="btn" data-goto-step="client-step-4">← Previous: Step 4 (My Direct Testimony)</button>
          <a href="lawyer.html" class="btn primary">Open in Counsel Workbench →</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer" role="contentinfo">
    <strong>PrismLegal — Client Case Preparation Journey</strong> · Free Open-Source Legal Preparation Service · 100% Private Browser Storage
  </footer>

  <script id="case-model-data" type="application/json">{payload_json}</script>
  <script>
    (function() {{
      {_shared_js_helpers()}
      const goToStep = setupJourneyStepper();

      let matter = ensureActiveMatter();
      let cardIdx = 0;
      let cardRevealed = false;

      const matterSelect = document.getElementById('client-matter-select');
      const matterMeta = document.getElementById('client-matter-meta');

      function refreshMatterSelector() {{
        matter = ensureActiveMatter();
        matterSelect.innerHTML = buildMatterSelectOptionsHtml(matter);
        const modeTag = matter.isExample ? '📘 Reference Example Preview' : (matter.isUnsavedDraft ? '✨ Unsaved Draft' : '★ Saved Matter');
        matterMeta.textContent = `${{modeTag}} · ${{matter.areaOfLaw || ''}} · ${{matter.docketNumber || 'No docket'}}`;
      }}

      matterSelect.addEventListener('change', () => {{
        setActiveMatterId(matterSelect.value);
        matter = ensureActiveMatter();
        cardIdx = 0;
        cardRevealed = false;
        renderAll();
      }});

      document.getElementById('btn-client-export-json').addEventListener('click', () => exportMatterJson(matter));
      document.getElementById('btn-step5-export-json').addEventListener('click', () => exportMatterJson(matter));
      document.getElementById('btn-step5-export-md').addEventListener('click', () => downloadMatterMarkdown(matter));
      document.getElementById('btn-step5-print').addEventListener('click', () => window.print());

      const importFile = document.getElementById('client-import-file');
      importFile.addEventListener('change', () => {{
        if (importFile.files && importFile.files[0]) {{
          importMatterFromFile(importFile.files[0], (imported) => {{
            matter = imported;
            renderAll();
          }});
        }}
      }});

      function renderStep1() {{
        document.getElementById('client-pedagogy-1').innerHTML = renderPedagogyBanner('client-step-1');
        document.getElementById('cm-title').value = matter.title || '';
        document.getElementById('cm-area').value = matter.areaOfLaw || 'Family & Parenting Law';
        document.getElementById('cm-forum').value = matter.forum || '';
        document.getElementById('cm-docket').value = matter.docketNumber || '';
        document.getElementById('cm-date').value = matter.hearingDate || '';
        document.getElementById('cm-client').value = matter.clientName || '';
        document.getElementById('cm-opposing').value = matter.opposingParty || '';
        document.getElementById('cm-counsel').value = matter.counselName || '';
        document.getElementById('cm-summary').value = matter.summary || '';

        document.getElementById('cm-summary-heading').textContent = matter.title || 'Untitled Legal Matter';
        document.getElementById('cm-summary-sub').textContent =
          `${{matter.areaOfLaw || 'Family & Parenting Law'}} · Forum: ${{matter.forum || 'Trial Court'}} · Docket: ${{matter.docketNumber || 'Pending'}} · Hearing: ${{matter.hearingDate || 'TBD'}} · Parties: ${{matter.clientName || 'Client'}} vs. ${{matter.opposingParty || 'Opposing Party'}}`;
        document.getElementById('cm-summary-box').innerHTML = renderCourtCaptionMastheadHtml(matter);

        const mm1 = document.getElementById('client-step1-multimodal');
        if (mm1 && !mm1.dataset.bound) {{
          mm1.innerHTML = renderMultiModalDropzoneHtml('client-mm1', 'Drop your court notices, financial statements (.csv/.pdf), emails (.eml/.txt), or inspection photos (.png/.jpg/.svg) here. The workspace will extract dates, figures, and clauses and link them across your goals, timeline, and testimony.');
          bindMultiModalDropzoneEvents('client-mm1', () => matter, (updated) => {{
            matter = updated;
            refreshMatterSelector();
            renderAll();
          }});
          mm1.dataset.bound = '1';
        }}

        const goalsList = document.getElementById('client-goals-list');
        const goals = matter.reliefGoals || [];
        if (!goals.length) {{
          goalsList.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">No relief goals added yet. Click <strong>"⚡ + Add Standard Statutory Goals for My Area of Law"</strong> above or open <strong>"+ Add a Custom Relief Goal"</strong> below.</div>`;
        }} else {{
          goalsList.innerHTML = goals.map((g, idx) => `
            <article class="card" style="margin-bottom:0;background:var(--surface-alt);border-top:4px solid var(--stipulated);display:flex;flex-direction:column;justify-content:space-between;">
              <div>
                <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">
                  <span class="badge stip">Goal ${{idx + 1}} · ${{escapeHtml(g.title)}}</span>
                  <button type="button" class="btn btn-del-goal" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.74rem;">Remove</button>
                </div>
                <h4 style="margin:8px 0 4px;">${{escapeHtml(g.requestedOrder)}}</h4>
                <p style="font-size:0.86rem;color:var(--muted);margin:0;">${{escapeHtml(g.rationale)}}</p>
              </div>
            </article>
          `).join('');
          goalsList.querySelectorAll('.btn-del-goal').forEach(btn => {{
            btn.addEventListener('click', () => {{
              matter.reliefGoals.splice(Number(btn.dataset.idx), 1);
              updateActiveMatter(matter);
              renderStep1();
              renderStep5();
            }});
          }});
        }}
      }}

      document.getElementById('btn-add-domain-goals').addEventListener('click', () => {{
        extrapolateCaseFromIntake(matter, {{ inferArea: true, seedStarterIntake: true }});
        updateActiveMatter(matter);
        refreshMatterSelector();
        renderAll();
      }});

      document.getElementById('btn-save-cm-meta').addEventListener('click', () => {{
        matter.title = document.getElementById('cm-title').value.trim();
        matter.areaOfLaw = document.getElementById('cm-area').value;
        matter.forum = document.getElementById('cm-forum').value.trim();
        matter.docketNumber = document.getElementById('cm-docket').value.trim();
        matter.hearingDate = document.getElementById('cm-date').value.trim();
        matter.clientName = document.getElementById('cm-client').value.trim();
        matter.opposingParty = document.getElementById('cm-opposing').value.trim();
        matter.counselName = document.getElementById('cm-counsel').value.trim();
        matter.summary = document.getElementById('cm-summary').value.trim();
        extrapolateCaseFromIntake(matter, {{ inferArea: true, seedStarterIntake: true }});
        updateActiveMatter(matter);
        refreshMatterSelector();
        renderAll();
        const st = document.getElementById('cm-save-status');
        st.textContent = '✓ Saved & Case Strategy Extrapolated';
        setTimeout(() => {{ st.textContent = ''; }}, 2500);
      }});

      document.getElementById('btn-add-goal').addEventListener('click', () => {{
        const title = document.getElementById('goal-title-in').value.trim();
        const requestedOrder = document.getElementById('goal-req-in').value.trim();
        const rationale = document.getElementById('goal-rat-in').value.trim();
        if (!title && !requestedOrder) return;
        matter.reliefGoals = matter.reliefGoals || [];
        matter.reliefGoals.push({{
          id: 'GOAL-' + String(matter.reliefGoals.length + 1).padStart(2, '0'),
          title: title || 'Requested Relief',
          requestedOrder: requestedOrder || title,
          rationale
        }});
        document.getElementById('goal-title-in').value = '';
        document.getElementById('goal-req-in').value = '';
        document.getElementById('goal-rat-in').value = '';
        extrapolateCaseFromIntake(matter, {{ inferArea: false, seedStarterIntake: false }});
        updateActiveMatter(matter);
        renderAll();
      }});

      function renderStep2() {{
        document.getElementById('client-pedagogy-2').innerHTML = renderPedagogyBanner('client-step-2');
        document.getElementById('client-timeline-svg').innerHTML = buildTimelineSvg(matter);
        const tlList = document.getElementById('client-timeline-list');
        const tl = matter.timeline || [];
        if (!tl.length) {{
          tlList.innerHTML = `<div class="empty-state">No timeline events recorded yet. Open <strong>"+ Add a Chronological Event to Timeline"</strong> below to add your first key date.</div>`;
        }} else {{
          tlList.innerHTML = `<table class="data-table">
            <thead><tr><th>Date</th><th>Event</th><th>Details &amp; Relevance</th><th>Supporting Record</th><th>Action</th></tr></thead>
            <tbody>
              ${{tl.map((ev, idx) => `
                <tr>
                  <td><strong>${{escapeHtml(ev.date)}}</strong></td>
                  <td><strong>${{escapeHtml(ev.title)}}</strong></td>
                  <td>${{escapeHtml(ev.description)}}</td>
                  <td>${{ev.exhibitId ? `<span class="exhibit-pill">${{escapeHtml(ev.exhibitId)}}</span>` : '—'}}</td>
                  <td><button type="button" class="btn btn-del-tl" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.74rem;">Remove</button></td>
                </tr>
              `).join('')}}
            </tbody>
          </table>`;
          tlList.querySelectorAll('.btn-del-tl').forEach(btn => {{
            btn.addEventListener('click', () => {{
              matter.timeline.splice(Number(btn.dataset.idx), 1);
              updateActiveMatter(matter);
              renderStep2();
              renderStep5();
            }});
          }});
        }}

        const mm2 = document.getElementById('client-step2-multimodal');
        if (mm2 && !mm2.dataset.bound) {{
          mm2.innerHTML = renderMultiModalDropzoneHtml('client-mm2', 'Upload PDFs, financial spreadsheets (.csv), messages (.txt/.eml), or photos (.png/.jpg/.svg) to automatically log exhibits, extract dates into your timeline, and verify SHA-256 chain of custody.');
          bindMultiModalDropzoneEvents('client-mm2', () => matter, (updated) => {{
            matter = updated;
            refreshMatterSelector();
            renderAll();
          }});
          mm2.dataset.bound = '1';
        }}

        const exList = document.getElementById('client-exhibits-list');
        const exs = matter.exhibits || [];
        if (!exs.length) {{
          exList.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">No supporting documents logged yet. Drop evidence files above or open <strong>"+ Add a Supporting Document or Exhibit"</strong> below.</div>`;
        }} else {{
          exList.innerHTML = exs.map((e, idx) => `
            <article class="card" style="margin-bottom:0;background:var(--surface-alt);">
              <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;flex-wrap:wrap;">
                <div>
                  <span class="badge stip">${{escapeHtml(e.label || e.id)}}</span>
                  <span class="badge info">${{escapeHtml(e.party || e.date || 'Record')}}</span>
                  ${{e.modality ? `<span class="modality-badge">${{escapeHtml(e.modality)}}</span>` : ''}}
                  ${{e.foundation ? `<code>${{escapeHtml(e.foundation)}}</code>` : ''}}
                </div>
                <button type="button" class="btn btn-del-cex" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.74rem;">Remove</button>
              </div>
              <h4 style="margin:6px 0 4px;">${{escapeHtml(e.title)}}</h4>
              ${{e.previewDataUrl ? `<div class="exhibit-thumb"><img src="${{escapeHtml(e.previewDataUrl)}}" alt="${{escapeHtml(e.title)}}"><span style="font-size:0.76rem;color:var(--muted);">${{escapeHtml(e.exifSummary || e.modality || 'Visual Preview')}}</span></div>` : ''}}
              <p style="font-size:0.86rem;margin:0;color:var(--muted);"><strong>Proves:</strong> ${{escapeHtml(e.purpose)}}</p>
              ${{e.sha256 ? `<div style="margin-top:4px;font-size:0.75rem;color:var(--stipulated);"><strong>🔐 SHA-256 Custody Digest:</strong> <code>${{escapeHtml(e.sha256.slice(0, 24))}}…</code></div>` : ''}}
              ${{(e.visualNotes || e.pivotIntent) ? `
                <details class="pedagogy-details" style="margin-top:8px;">
                  <summary>🔍 Visual Details, Page Callouts &amp; Trial Intent ▾</summary>
                  ${{e.visualNotes ? `<p style="margin:4px 0;"><strong>Visual &amp; Page Annotations:</strong> ${{escapeHtml(e.visualNotes)}}</p>` : ''}}
                  ${{e.pivotIntent ? `<p style="margin:4px 0 0;"><strong>Trial Intent / Pivot:</strong> ${{escapeHtml(e.pivotIntent)}}</p>` : ''}}
                </details>
              ` : ''}}
            </article>
          `).join('');
          exList.querySelectorAll('.btn-del-cex').forEach(btn => {{
            btn.addEventListener('click', () => {{
              matter.exhibits.splice(Number(btn.dataset.idx), 1);
              updateActiveMatter(matter);
              renderStep2();
              renderStep5();
            }});
          }});
        }}
      }}

      document.getElementById('btn-add-tl').addEventListener('click', () => {{
        const date = document.getElementById('tl-date-in').value.trim();
        const title = document.getElementById('tl-title-in').value.trim();
        const exhibitId = document.getElementById('tl-ex-in').value.trim();
        const description = document.getElementById('tl-desc-in').value.trim();
        if (!title) return;
        matter.timeline = matter.timeline || [];
        matter.timeline.push({{
          id: 'TL-' + String(matter.timeline.length + 1).padStart(2, '0'),
          date: date || 'Key Date',
          title,
          description,
          exhibitId
        }});
        document.getElementById('tl-date-in').value = '';
        document.getElementById('tl-title-in').value = '';
        document.getElementById('tl-ex-in').value = '';
        document.getElementById('tl-desc-in').value = '';
        extrapolateCaseFromIntake(matter, {{ inferArea: false, seedStarterIntake: false }});
        updateActiveMatter(matter);
        renderAll();
      }});

      document.getElementById('btn-add-cex').addEventListener('click', async () => {{
        const label = document.getElementById('cex-label-in').value.trim();
        let title = document.getElementById('cex-title-in').value.trim();
        let date = document.getElementById('cex-date-in').value.trim();
        let purpose = document.getElementById('cex-purpose-in').value.trim();
        const fileEl = document.getElementById('cex-file-in');
        const fileObj = (fileEl && fileEl.files && fileEl.files[0]) ? fileEl.files[0] : null;
        if (!title && !fileObj) return;
        let parsed = null;
        if (fileObj) {{
          parsed = await parseMultiModalFileInBrowser(fileObj, matter);
          if (!title) title = parsed.title;
          if (!date) date = parsed.date;
          if (!purpose) purpose = parsed.purpose;
        }}
        matter.exhibits = matter.exhibits || [];
        const nextNum = matter.exhibits.length + 1;
        const id = label ? label.replace(/[^A-Za-z0-9_-]/g, '-') : ('Ex-' + nextNum);
        const exProf = classifyExhibitIntake({{ title, purpose }});
        matter.exhibits.push({{
          id,
          label: label || ('Ex. ' + nextNum),
          party: 'Client',
          title,
          date: date || 'Record',
          purpose,
          modality: parsed ? parsed.modality : '',
          sha256: parsed ? parsed.sha256 : '',
          previewDataUrl: parsed ? (parsed.previewDataUrl || '') : '',
          exifSummary: parsed ? (parsed.exifSummary || '') : '',
          foundation: parsed ? parsed.foundation : exProf.foundation,
          visualNotes: parsed ? parsed.visualNotes : exProf.visualNotes,
          pivotIntent: parsed ? parsed.pivotIntent : exProf.pivotIntent,
          status: 'Ready to Offer'
        }});
        document.getElementById('cex-label-in').value = '';
        document.getElementById('cex-title-in').value = '';
        document.getElementById('cex-date-in').value = '';
        document.getElementById('cex-purpose-in').value = '';
        if (fileEl) fileEl.value = '';
        extrapolateCaseFromIntake(matter, {{ inferArea: false, seedStarterIntake: false }});
        updateActiveMatter(matter);
        renderAll();
      }});

      function renderStep3() {{
        document.getElementById('client-pedagogy-3').innerHTML = renderPedagogyBanner('client-step-3');
        const traps = matter.traps || [];
        const counter = document.getElementById('flashcard-counter');
        const stage = document.getElementById('flashcard-stage');
        const chkBlind = document.getElementById('chk-blind-drill');

        if (!traps.length) {{
          counter.textContent = '0 / 0';
          stage.innerHTML = `<div class="empty-state">No tough questions added yet. Open <strong>"+ Add a Tough Question or Out-of-Context Quote to Prepare For"</strong> below so you can practice calm, factual answers.</div>`;
        }} else {{
          if (cardIdx >= traps.length) cardIdx = 0;
          const t = traps[cardIdx];
          counter.textContent = `${{cardIdx + 1}} / ${{traps.length}}`;
          const showAnswer = !chkBlind.checked || cardRevealed;
          stage.innerHTML = `
            <div class="card" style="margin-bottom:0;background:var(--surface-alt);border:2px solid var(--border);">
              <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px;">
                <div>
                  <span class="badge info">${{escapeHtml(t.id)}}</span>
                  <span class="badge stip">Readiness: ${{escapeHtml(t.readiness || 'Practice Needed')}}</span>
                  <strong style="font-size:1.05rem;">${{escapeHtml(t.title)}}</strong>
                </div>
                <div>${{t.exhibitId ? `<span class="exhibit-pill">${{escapeHtml(t.exhibitId)}}</span>` : ''}}</div>
              </div>
              <p style="font-size:1.02rem;margin:8px 0;"><strong>🎯 Anticipated Question / Challenge:</strong><br>${{escapeHtml(t.question)}}</p>
              ${{!showAnswer ? `
                <div style="margin:14px 0;">
                  <button type="button" class="btn primary" id="btn-reveal-card">👁️ Reveal Trap to Avoid &amp; Calm Response</button>
                </div>
              ` : `
                <div class="trap-dont"><strong>⛔ Trap to Avoid:</strong> ${{escapeHtml(t.avoid)}}</div>
                ${{t.rule106Context ? `<div class="quote-box" style="margin-top:8px;font-size:0.88rem;"><strong>📖 Rule 106 Full Context (Remainder of Writing):</strong> ${{escapeHtml(t.rule106Context)}}</div>` : ''}}
                <div class="pivot-say" style="font-size:1.02rem;"><strong>✅ Your Calm Response:</strong><br>"${{escapeHtml(t.response)}}"</div>
                <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:8px;">
                  <button type="button" class="btn card-ready-btn" data-status="Ready for Hearing">✅ Mark Ready for Hearing</button>
                  <button type="button" class="btn card-ready-btn" data-status="Needs More Practice">🔄 Practice Again</button>
                  <button type="button" class="btn card-ready-btn" data-status="Review with Lawyer">❓ Flag for My Lawyer</button>
                </div>
              `}}
            </div>
          `;
          const revBtn = document.getElementById('btn-reveal-card');
          if (revBtn) revBtn.addEventListener('click', () => {{ cardRevealed = true; renderStep3(); }});
          stage.querySelectorAll('.card-ready-btn').forEach(b => {{
            b.addEventListener('click', () => {{
              t.readiness = b.dataset.status;
              if (b.dataset.status === 'Review with Lawyer') {{
                matter.agenda = matter.agenda || [];
                matter.agenda.push({{
                  id: 'AG-' + String(matter.agenda.length + 1).padStart(2, '0'),
                  topic: t.title,
                  questionForCounsel: 'Please review my planned response to: ' + t.question,
                  counselGuidance: 'Pending attorney review.',
                  status: 'Open'
                }});
              }}
              updateActiveMatter(matter);
              renderStep3();
              renderStep5();
            }});
          }});
        }}

        const listEl = document.getElementById('client-traps-list');
        if (!traps.length) {{
          listEl.innerHTML = '';
        }} else {{
          listEl.innerHTML = traps.map((t, idx) => `
            <article class="card" style="margin-bottom:0;">
              <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">
                <div><span class="badge info">${{escapeHtml(t.id)}}</span> <span class="badge stip">${{escapeHtml(t.readiness || 'Practice Needed')}}</span></div>
                <button type="button" class="btn btn-del-trap" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.74rem;">Remove</button>
              </div>
              <h4 style="margin:6px 0 4px;">${{escapeHtml(t.title)}}</h4>
              <p style="font-size:0.88rem;margin:4px 0;"><strong>Q:</strong> ${{escapeHtml(t.question)}}</p>
              <div class="trap-dont"><strong>⛔ Avoid:</strong> ${{escapeHtml(t.avoid)}}</div>
              ${{t.rule106Context ? `<div style="font-size:0.82rem;color:var(--muted);margin-top:6px;"><strong>📖 Rule 106 Context:</strong> ${{escapeHtml(t.rule106Context)}}</div>` : ''}}
              <div class="pivot-say"><strong>✅ Say:</strong> "${{escapeHtml(t.response)}}"</div>
            </article>
          `).join('');
          listEl.querySelectorAll('.btn-del-trap').forEach(btn => {{
            btn.addEventListener('click', () => {{
              matter.traps.splice(Number(btn.dataset.idx), 1);
              updateActiveMatter(matter);
              renderStep3();
              renderStep5();
            }});
          }});
        }}
      }}

      document.getElementById('chk-blind-drill').addEventListener('change', () => {{ cardRevealed = false; renderStep3(); }});
      document.getElementById('btn-prev-card').addEventListener('click', () => {{
        const len = (matter.traps || []).length;
        if (!len) return;
        cardIdx = (cardIdx - 1 + len) % len;
        cardRevealed = false;
        renderStep3();
      }});
      document.getElementById('btn-next-card').addEventListener('click', () => {{
        const len = (matter.traps || []).length;
        if (!len) return;
        cardIdx = (cardIdx + 1) % len;
        cardRevealed = false;
        renderStep3();
      }});

      document.getElementById('btn-add-trap').addEventListener('click', () => {{
        const title = document.getElementById('tr-title-in').value.trim();
        const exhibitId = document.getElementById('tr-ex-in').value.trim();
        const question = document.getElementById('tr-q-in').value.trim();
        const avoid = document.getElementById('tr-avoid-in').value.trim();
        const response = document.getElementById('tr-say-in').value.trim();
        const rule106Context = document.getElementById('tr-r106-in').value.trim();
        if (!question || !response) return;
        matter.traps = matter.traps || [];
        matter.traps.push({{
          id: 'TRAP-' + String(matter.traps.length + 1).padStart(2, '0'),
          title: title || 'Cross-Examination Topic',
          question,
          avoid: avoid || 'Do not argue or speculate.',
          response,
          rule106Context,
          exhibitId,
          readiness: 'Practice Needed'
        }});
        document.getElementById('tr-title-in').value = '';
        document.getElementById('tr-ex-in').value = '';
        document.getElementById('tr-q-in').value = '';
        document.getElementById('tr-avoid-in').value = '';
        document.getElementById('tr-say-in').value = '';
        document.getElementById('tr-r106-in').value = '';
        updateActiveMatter(matter);
        renderStep3();
        renderStep5();
      }});

      function renderStep4() {{
        document.getElementById('client-pedagogy-4').innerHTML = renderPedagogyBanner('client-step-4');
        const dxList = document.getElementById('client-dx-list');
        const rows = matter.directExam || [];
        if (!rows.length) {{
          dxList.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">No direct examination questions added yet. Click <strong>"⚡ + Generate Foundational Questions from My Goals &amp; Exhibits"</strong> above or open <strong>"+ Add a Direct Testimony Question"</strong> below.</div>`;
        }} else {{
          dxList.innerHTML = rows.map((d, idx) => `
            <article class="card" style="margin-bottom:0;${{d.visualCue === 'yellow-highlight' ? 'border-left:5px solid #d97706;' : (d.visualCue === 'red-strikethrough' ? 'opacity:0.78;border-left:5px solid var(--danger);' : '')}}">
              <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:6px;flex-wrap:wrap;">
                <div>
                  <span class="badge info">${{escapeHtml(d.id)}}</span>
                  <span class="badge stip">${{escapeHtml(d.chapter || 'Direct Testimony')}}</span>
                  ${{d.visualCue === 'yellow-highlight' ? '<span class="badge warn">⭐ Key Highlight</span>' : ''}}
                  ${{d.visualCue === 'red-strikethrough' ? '<span class="badge danger">🚫 Skip Unless Opened on Cross</span>' : ''}}
                  ${{d.exhibitId ? `<span class="exhibit-pill">${{escapeHtml(d.exhibitId)}}</span>` : ''}}
                  ${{d.movesToAdmit ? '<span class="badge stip">📎 Move to Admit</span>' : ''}}
                </div>
                <button type="button" class="btn btn-del-dx" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.74rem;">Remove</button>
              </div>
              <h4 style="margin:6px 0;${{d.visualCue === 'red-strikethrough' ? 'text-decoration:line-through;' : ''}}">Q: ${{escapeHtml(d.question)}}</h4>
              <div class="pivot-say"><strong>✅ Planned Answer:</strong> "${{escapeHtml(d.answer)}}"</div>
              ${{d.coachingNote ? `<div style="margin-top:6px;font-size:0.8rem;color:var(--muted);"><strong>💡 Witness Coaching Note:</strong> ${{escapeHtml(d.coachingNote)}}</div>` : ''}}
            </article>
          `).join('');
          dxList.querySelectorAll('.btn-del-dx').forEach(btn => {{
            btn.addEventListener('click', () => {{
              matter.directExam.splice(Number(btn.dataset.idx), 1);
              updateActiveMatter(matter);
              renderStep4();
              renderStep5();
            }});
          }});
        }}
      }}

      document.getElementById('btn-gen-dx-from-goals').addEventListener('click', () => {{
        matter.directExam = matter.directExam || [];
        (matter.reliefGoals || []).forEach(g => {{
          const qText = `What specific order are you requesting regarding ${{g.title}}, and why is it supported by the record?`;
          if (!matter.directExam.some(d => d.question === qText)) {{
            matter.directExam.push({{
              id: 'DX-' + String(matter.directExam.length + 1).padStart(2, '0'),
              chapter: 'Requested Relief & Case Theory',
              question: qText,
              answer: `${{g.requestedOrder}} ${{g.rationale || ''}}`.trim(),
              exhibitId: ''
            }});
          }}
        }});
        (matter.exhibits || []).forEach(ex => {{
          const lbl = ex.label || ex.id;
          const qText = `Showing you what has been marked as ${{lbl}} (${{ex.title}}), how do you recognize this document and what does it establish?`;
          if (!matter.directExam.some(d => d.exhibitId === lbl)) {{
            matter.directExam.push({{
              id: 'DX-' + String(matter.directExam.length + 1).padStart(2, '0'),
              chapter: 'Exhibit Foundation & Proof',
              question: qText,
              answer: `I recognize ${{lbl}} as ${{ex.title}}. It is a true and accurate copy of the record, and it establishes that ${{ex.purpose || 'the facts in our timeline are corroborated'}}.`,
              exhibitId: lbl
            }});
          }}
        }});
        updateActiveMatter(matter);
        renderStep4();
        renderStep5();
      }});

      document.getElementById('btn-add-dx').addEventListener('click', () => {{
        const chapter = document.getElementById('dx-ch-in').value.trim();
        const exhibitId = document.getElementById('dx-ex-in').value.trim();
        const question = document.getElementById('dx-q-in').value.trim();
        const answer = document.getElementById('dx-a-in').value.trim();
        if (!question || !answer) return;
        matter.directExam = matter.directExam || [];
        matter.directExam.push({{
          id: 'DX-' + String(matter.directExam.length + 1).padStart(2, '0'),
          chapter: chapter || 'Direct Examination',
          question,
          answer,
          exhibitId
        }});
        document.getElementById('dx-ch-in').value = '';
        document.getElementById('dx-ex-in').value = '';
        document.getElementById('dx-q-in').value = '';
        document.getElementById('dx-a-in').value = '';
        updateActiveMatter(matter);
        renderStep4();
        renderStep5();
      }});

      function renderStep5() {{
        document.getElementById('client-pedagogy-5').innerHTML = renderPedagogyBanner('client-step-5');
        const kpis = document.getElementById('client-readiness-kpis');
        const goalsCount = (matter.reliefGoals || []).length;
        const exCount = (matter.exhibits || []).length;
        const trapCount = (matter.traps || []).length;
        const dxCount = (matter.directExam || []).length;
        kpis.innerHTML = `
          <div class="kpi-card stip"><div class="kpi-label">Relief Goals Defined</div><div class="kpi-val">${{goalsCount}}</div><div class="kpi-note">Step 1 · Specific Court Orders</div></div>
          <div class="kpi-card info"><div class="kpi-label">Supporting Exhibits</div><div class="kpi-val">${{exCount}}</div><div class="kpi-note">Step 2 · Documentary Proof</div></div>
          <div class="kpi-card warn"><div class="kpi-label">Tough Questions Rehearsed</div><div class="kpi-val">${{trapCount}}</div><div class="kpi-note">Step 3 · Cross-Exam Flashcards</div></div>
          <div class="kpi-card stip"><div class="kpi-label">Direct Exam Q&amp;As</div><div class="kpi-val">${{dxCount}}</div><div class="kpi-note">Step 4 · Testimony Script</div></div>
        `;

        const auditEl = document.getElementById('client-consistency-audit');
        const checks = auditMatterConsistency(matter);
        auditEl.innerHTML = checks.map(ch => `
          <div class="${{ch.ok ? 'finding-box' : 'refusal-box'}}" style="margin-top:0;">
            <strong>${{ch.ok ? '✓ Ready:' : '⚠️ Action Recommended:'}} ${{escapeHtml(ch.title)}}</strong><br>
            <span>${{escapeHtml(ch.detail)}}</span>
          </div>
        `).join('');

        const fcWrap = document.getElementById('client-step5-filing-center');
        if (fcWrap) {{
          fcWrap.innerHTML = renderFilingCenterHtml(matter, 'client-fc');
          bindFilingCenterEvents('client-fc', () => matter);
        }}

        const agWrap = document.getElementById('client-agenda-list');
        const ag = matter.agenda || [];
        if (!ag.length) {{
          agWrap.innerHTML = `<div class="empty-state">No questions logged for counsel yet. Open <strong>"+ Add a Question or Note for Your Lawyer"</strong> below to add any strategy notes.</div>`;
        }} else {{
          agWrap.innerHTML = ag.map((a, idx) => `
            <div class="card" style="margin-bottom:10px;padding:14px;">
              <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
                <div><span class="badge info">${{escapeHtml(a.id)}}</span> <strong>${{escapeHtml(a.topic)}}</strong></div>
                <div style="display:flex;gap:6px;align-items:center;">
                  <span class="badge stip">${{escapeHtml(a.status || 'Open')}}</span>
                  <button type="button" class="btn btn-del-ag" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.74rem;">Remove</button>
                </div>
              </div>
              <p style="margin:6px 0;"><strong>Your Question:</strong> ${{escapeHtml(a.questionForCounsel)}}</p>
              <div class="pivot-say"><strong>⚖️ Attorney Response / Guidance:</strong> ${{escapeHtml(a.counselGuidance || 'Pending attorney review.')}}</div>
            </div>
          `).join('');
          agWrap.querySelectorAll('.btn-del-ag').forEach(btn => {{
            btn.addEventListener('click', () => {{
              matter.agenda.splice(Number(btn.dataset.idx), 1);
              updateActiveMatter(matter);
              renderStep5();
            }});
          }});
        }}
      }}

      document.getElementById('btn-add-agenda').addEventListener('click', () => {{
        const topic = document.getElementById('ag-topic-in').value.trim();
        const questionForCounsel = document.getElementById('ag-q-in').value.trim();
        if (!questionForCounsel) return;
        matter.agenda = matter.agenda || [];
        matter.agenda.push({{
          id: 'AG-' + String(matter.agenda.length + 1).padStart(2, '0'),
          topic: topic || 'Case Strategy',
          questionForCounsel,
          counselGuidance: 'Saved for review in Attorney Workbench.',
          status: 'Open'
        }});
        document.getElementById('ag-topic-in').value = '';
        document.getElementById('ag-q-in').value = '';
        updateActiveMatter(matter);
        renderStep5();
      }});

      function renderAll() {{
        refreshMatterSelector();
        renderStep1();
        renderStep2();
        renderStep3();
        renderStep4();
        renderStep5();
      }}
      renderAll();
    }})();
  </script>
</body>
</html>
"""


def render_lawyer_html(payload):
    """`view/lawyer.html` — Five-Step Guided Attorney Case Workbench Journey."""
    payload_json = json.dumps(payload, ensure_ascii=False)
    commit_sha = html.escape(payload.get("commit", ""))
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="prism-legal-commit" content="{commit_sha}">
  <title>Attorney Workbench — PrismLegal Public-Benefit Legal Platform</title>
  <style>{_shared_css()}</style>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to Attorney Workbench</a>
  {_shared_header_html("lawyer.html")}

  <main id="main-content" class="container" role="main">
    <!-- Active Matter Selector & File Controls -->
    <div class="matter-bar" aria-label="Active Matter Controls">
      <div class="matter-bar-left">
        <span class="badge stip">⚖️ Attorney Case Workbench</span>
        <label style="font-size:0.86rem;font-weight:700;display:flex;align-items:center;gap:6px;">
          Active Matter:
          <select id="lawyer-matter-select" class="btn" aria-label="Select Active Matter"></select>
        </label>
        <span id="lawyer-matter-meta" style="font-size:0.82rem;color:var(--muted);"></span>
      </div>
      <div class="matter-bar-right">
        <a href="index.html" class="btn">+ New or Switch Matter</a>
        <label class="btn" style="cursor:pointer;margin:0;">
          📂 Import Client File (.json)
          <input type="file" id="lawyer-import-file" accept=".json,application/json" style="display:none;">
        </label>
        <button type="button" class="btn primary" id="btn-lawyer-export-json">💾 Export Matter (.json)</button>
      </div>
    </div>

    <!-- Live Evidentiary Proof Health Strip -->
    <div id="lawyer-health-strip" class="kpi-strip"></div>

    <!-- 5-Step Guided Attorney Journey Stepper -->
    <nav class="journey-stepper" aria-label="Attorney 5-Step Case Workbench Journey">
      <button type="button" class="step-tab" aria-selected="true" data-target="lawyer-step-1">
        <span class="step-num">1</span>
        <span>
          <span class="step-title">Intake &amp; Case Theory</span>
          <span class="step-sub">Forum, Scope &amp; Relief Posture</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="lawyer-step-2">
        <span class="step-num">2</span>
        <span>
          <span class="step-title">Statutory Proof Matrix</span>
          <span class="step-sub">Elements, Claims &amp; Gap Audit</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="lawyer-step-3">
        <span class="step-num">3</span>
        <span>
          <span class="step-title">Witnesses &amp; Exams</span>
          <span class="step-sub">Clock Budget, Direct &amp; Cross</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="lawyer-step-4">
        <span class="step-num">4</span>
        <span>
          <span class="step-title">Exhibits &amp; Calculators</span>
          <span class="step-sub">Foundations &amp; Guideline Math</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="lawyer-step-5">
        <span class="step-num">5</span>
        <span>
          <span class="step-title">Trial Brief &amp; Handoff</span>
          <span class="step-sub">Client Q&amp;A &amp; Brief Export</span>
        </span>
      </button>
    </nav>

    <!-- STEP 1: ORIENTATION — MATTER INTAKE, REPRESENTATION SCOPE & CASE THEORY -->
    <section id="lawyer-step-1" class="workspace-section active">
      <div id="lawyer-pedagogy-1"></div>

      <div class="card" style="border-left:6px solid var(--accent);">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-start;gap:12px;">
          <div>
            <span class="badge info">Step 1 of 5 · Matter Intake, Scope &amp; Case Theory</span>
            <h2 id="lm-posture-heading" style="margin:4px 0 4px;">Matter Posture &amp; Representation Scope</h2>
            <p id="lm-posture-sub" style="margin:0;color:var(--muted);font-size:0.9rem;"></p>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;">
            <button type="button" class="btn" id="btn-scaffold-domain">✨ Auto-Complete Case Theory, Proof Matrix, Exams &amp; Brief from Intake</button>
            <span id="lm-save-status" style="font-size:0.84rem;color:var(--stipulated);font-weight:700;"></span>
          </div>
        </div>
        <div id="lm-posture-box" style="margin-top:10px;margin-bottom:8px;"></div>
        <div id="lawyer-step1-multimodal"></div>

        <details class="action-drawer">
          <summary>✏️ Edit Matter Caption, Forum, Representation Scope (Rule 1.2(c)) &amp; Hearing Budget</summary>
          <div class="form-grid" style="margin-bottom:12px;">
            <div class="form-field">
              <label for="lm-title">Matter Title / Caption</label>
              <input type="text" id="lm-title" class="search-input">
            </div>
            <div class="form-field">
              <label for="lm-area">Practice Area / Governing Framework</label>
              <select id="lm-area" class="btn" style="width:100%;">
                <option value="Family &amp; Parenting Law">Family &amp; Parenting Law</option>
                <option value="Housing &amp; Tenant Rights">Housing &amp; Tenant Rights</option>
                <option value="Veterans &amp; Administrative Appeals">Veterans &amp; Administrative Appeals</option>
                <option value="Employment &amp; Wage Protection">Employment &amp; Wage Protection</option>
                <option value="Consumer, Debt &amp; Small Claims">Consumer, Debt &amp; Small Claims</option>
                <option value="Civil Litigation &amp; Probate">Civil Litigation &amp; Probate</option>
              </select>
            </div>
            <div class="form-field">
              <label for="lm-scope">Representation Scope (ABA Model Rule 1.2(c))</label>
              <select id="lm-scope" class="btn" style="width:100%;">
                <option value="Full-Scope Trial Representation">Full-Scope Trial Representation</option>
                <option value="Limited-Scope: Hearing &amp; Trial Brief Coaching (Rule 1.2(c))">Limited-Scope: Hearing &amp; Trial Brief Coaching (Rule 1.2(c))</option>
                <option value="Legal Aid Clinic / Pro Bono Advisory">Legal Aid Clinic / Pro Bono Advisory</option>
                <option value="Self-Represented Litigant Preparation">Self-Represented Litigant Preparation</option>
              </select>
            </div>
            <div class="form-field">
              <label for="lm-forum">Adjudicative Forum / Division</label>
              <input type="text" id="lm-forum" class="search-input">
            </div>
            <div class="form-field">
              <label for="lm-docket">Docket / Case Number</label>
              <input type="text" id="lm-docket" class="search-input">
            </div>
            <div class="form-field">
              <label for="lm-date">Hearing / Trial Date</label>
              <input type="text" id="lm-date" class="search-input">
            </div>
            <div class="form-field">
              <label for="lm-mins">Total Hearing Budget (Minutes)</label>
              <input type="number" id="lm-mins" class="search-input">
            </div>
            <div class="form-field">
              <label for="lm-client">Client Name &amp; Procedural Role</label>
              <input type="text" id="lm-client" class="search-input">
            </div>
            <div class="form-field">
              <label for="lm-counsel">Lead / Consulting Counsel</label>
              <input type="text" id="lm-counsel" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:12px;">
            <label for="lm-summary">Opening Statement Theory of the Case</label>
            <textarea id="lm-summary" class="search-input" style="height:76px;"></textarea>
          </div>
          <button type="button" class="btn primary" id="btn-save-lm-meta">💾 Save Matter Posture</button>
        </details>
      </div>

      <div class="card">
        <span class="badge stip">Requested Relief Orders</span>
        <h3>Relief Posture &amp; Proposed Court Orders</h3>
        <div id="lawyer-goals-list" class="grid-3"></div>

        <div class="step-footer">
          <a href="index.html" class="btn">← Back to Overview &amp; Matters</a>
          <button type="button" class="btn primary" data-goto-step="lawyer-step-2">Continue to Step 2: Statutory Proof Matrix →</button>
        </div>
      </div>
    </section>

    <!-- STEP 2: SUBSTANCE — STATUTORY ELEMENTS, PROPOSED FINDINGS & RULE EXCEPTIONS -->
    <section id="lawyer-step-2" class="workspace-section">
      <div id="lawyer-pedagogy-2"></div>

      <div class="card" style="border-left:6px solid var(--stipulated);">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px;">
          <div>
            <span class="badge stip">Step 2 of 5 · Statutory Elements, Proposed Findings &amp; Refusal Guard</span>
            <h2 style="margin:4px 0 0;">Map Every Legal Claim to Statutory Authority &amp; Backing Exhibits</h2>
          </div>
          <button type="button" class="btn" id="btn-add-preset-claims">✨ Synthesize Statutory Claims &amp; Exceptions from My Intake</button>
        </div>
        <p style="margin:0 0 14px;color:var(--muted);">Each claim backed by exhibits automatically compiles into a <strong>Controlled-English Proposed Court Finding</strong>. Claims without an assigned exhibit trigger the <strong>Evidentiary Refusal Guard</strong> until documentary proof is linked.</p>

        <div id="lawyer-claims-list" class="grid-2" style="margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Add a Statutory Claim or Legal Element</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="lclm-stat-in">Statute / Rule Citation</label>
              <input type="text" id="lclm-stat-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="lclm-status-in">Evidentiary Posture</label>
              <select id="lclm-status-in" class="btn" style="width:100%;">
                <option value="stipulated">stipulated</option>
                <option value="corroborated" selected>corroborated</option>
                <option value="contested">contested</option>
              </select>
            </div>
            <div class="form-field">
              <label for="lclm-ex-in">Backing Exhibits (comma-separated)</label>
              <input type="text" id="lclm-ex-in" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="lclm-stmt-in">Declarative Legal &amp; Factual Proposition</label>
            <input type="text" id="lclm-stmt-in" class="search-input">
          </div>
          <button type="button" class="btn primary" id="btn-lawyer-add-claim">+ Save Statutory Claim</button>
        </details>
      </div>

      <div class="card">
        <span class="badge info">Statutory Exceptions, Immunities &amp; Rule Overrides</span>
        <h3>Controlling Statutory Exceptions &amp; Affirmative Defenses</h3>
        <p style="margin:0 0 12px;color:var(--muted);">When opposing counsel relies on a general rule (such as wage imputation, summary eviction, or schedular rating caps), pair it with the controlling statutory exception or immunity that overrides it.</p>
        <div id="lawyer-exceptions-list" class="grid-2" style="margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Add a Controlling Statutory Exception or Rule Override</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="lexc-stat-in">Controlling Statute / Rule Exception</label>
              <input type="text" id="lexc-stat-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="lexc-ex-in">Supporting Exhibit Label</label>
              <input type="text" id="lexc-ex-in" class="search-input">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="lexc-gen-in">Opposing General Rule Claimed</label>
            <input type="text" id="lexc-gen-in" class="search-input">
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="lexc-ov-in">Controlling Statutory Override / Immunity</label>
            <input type="text" id="lexc-ov-in" class="search-input">
          </div>
          <button type="button" class="btn primary" id="btn-add-exception">+ Save Statutory Exception</button>
        </details>

        <div class="step-footer">
          <button type="button" class="btn" data-goto-step="lawyer-step-1">← Previous: Step 1 (Intake &amp; Case Theory)</button>
          <button type="button" class="btn primary" data-goto-step="lawyer-step-3">Continue to Step 3: Witnesses &amp; Exams →</button>
        </div>
      </div>
    </section>

    <!-- STEP 3: CHALLENGE — WITNESS EXAMINATIONS, OBJECTIONS & CLOCK BUDGET -->
    <section id="lawyer-step-3" class="workspace-section">
      <div id="lawyer-pedagogy-3"></div>

      <div class="card" style="border-left:6px solid var(--accent);">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px;">
          <div>
            <span class="badge info">Step 3 of 5 · Stage-by-Stage Hearing Clock &amp; Witness Roster</span>
            <h2 style="margin:4px 0 0;">Regulate Hearing Stage Budgets &amp; Witness Time Allocations</h2>
          </div>
          <span id="lawyer-clock-badge" class="badge stip" style="font-size:0.9rem;padding:6px 12px;"></span>
        </div>

        <div id="lawyer-stage-clock-strip" class="kpi-strip" style="margin-bottom:14px;"></div>
        <div id="lawyer-witness-list" class="grid-3" style="margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Add a Witness to the Hearing Roster</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="lwit-name-in">Witness Name</label>
              <input type="text" id="lwit-name-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="lwit-role-in">Role / Relationship</label>
              <input type="text" id="lwit-role-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="lwit-status-in">Call Status</label>
              <select id="lwit-status-in" class="btn" style="width:100%;">
                <option value="will-call">will-call</option>
                <option value="may-call">may-call</option>
                <option value="adverse-cross">adverse-cross</option>
              </select>
            </div>
            <div class="form-field">
              <label for="lwit-mins-in">Allocated Minutes</label>
              <input type="number" id="lwit-mins-in" class="search-input" value="25">
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="lwit-scope-in">Scope of Testimony &amp; Exhibits Authenticated</label>
            <input type="text" id="lwit-scope-in" class="search-input">
          </div>
          <button type="button" class="btn primary" id="btn-add-witness">+ Save Witness</button>
        </details>
      </div>

      <div class="grid-2">
        <div class="card">
          <span class="badge stip">Direct Examination Script</span>
          <h3>Direct Examination Q&amp;As &amp; Admission Cues</h3>
          <div id="lawyer-dx-list" style="margin-bottom:12px;"></div>
          <details class="action-drawer">
            <summary>+ Add a Direct Examination Question &amp; Admission Cue</summary>
            <div class="form-grid" style="margin-bottom:10px;">
              <div class="form-field">
                <label for="ldx-chap-in">Chapter / Examination Topic</label>
                <input type="text" id="ldx-chap-in" class="search-input">
              </div>
              <div class="form-field">
                <label for="ldx-ex-in">Exhibit to Authenticate / Offer</label>
                <input type="text" id="ldx-ex-in" class="search-input">
              </div>
              <div class="form-field">
                <label for="ldx-cue-in">Script Visual Cue</label>
                <select id="ldx-cue-in" class="btn" style="width:100%;">
                  <option value="standard">Standard Direct Question</option>
                  <option value="highlight">⭐ Key Highlight / Must-Ask</option>
                  <option value="strikethrough">🚫 Skip Unless Opened on Cross</option>
                </select>
              </div>
              <div class="form-field">
                <label for="ldx-admit-in">Move to Admit Exhibit?</label>
                <select id="ldx-admit-in" class="btn" style="width:100%;">
                  <option value="no">No — Testimony Only</option>
                  <option value="yes">Yes — Move to Admit into Evidence</option>
                </select>
              </div>
            </div>
            <div class="form-field" style="margin-bottom:10px;">
              <label for="ldx-q-in">Non-Leading Direct Question</label>
              <input type="text" id="ldx-q-in" class="search-input">
            </div>
            <div class="form-field" style="margin-bottom:10px;">
              <label for="ldx-a-in">Target Fact-Anchored Testimony &amp; Page Callout</label>
              <input type="text" id="ldx-a-in" class="search-input">
            </div>
            <button type="button" class="btn primary" id="btn-lawyer-add-dx">+ Save Direct Exam Question</button>
          </details>
        </div>
        <div class="card">
          <span class="badge warn">Cross-Examination, Rule 106 Context &amp; Objections</span>
          <h3>Opposing Lines, Objections &amp; Redirect Pivots</h3>
          <div id="lawyer-traps-list" style="margin-bottom:12px;"></div>
          <details class="action-drawer">
            <summary>+ Add a Cross-Examination / Redirect Card</summary>
            <div class="form-grid" style="margin-bottom:10px;">
              <div class="form-field">
                <label for="ltr-title-in">Topic / Impeachment Theme</label>
                <input type="text" id="ltr-title-in" class="search-input">
              </div>
              <div class="form-field">
                <label for="ltr-ex-in">Rehabilitating Exhibit Label</label>
                <input type="text" id="ltr-ex-in" class="search-input">
              </div>
            </div>
            <div class="form-field" style="margin-bottom:10px;">
              <label for="ltr-q-in">Anticipated Hostile Question or Selective Quote</label>
              <input type="text" id="ltr-q-in" class="search-input">
            </div>
            <div class="form-field" style="margin-bottom:10px;">
              <label for="ltr-resp-in">Disciplined Witness Response / Redirect Pivot</label>
              <input type="text" id="ltr-resp-in" class="search-input">
            </div>
            <div class="form-field" style="margin-bottom:10px;">
              <label for="ltr-r106-in">Rule of Completeness (FRE 106) Full Surrounding Context</label>
              <input type="text" id="ltr-r106-in" class="search-input">
            </div>
            <button type="button" class="btn primary" id="btn-lawyer-add-trap">+ Save Cross-Exam / Redirect Card</button>
          </details>
        </div>
      </div>

      <div class="card">
        <div class="step-footer" style="margin-top:0;padding-top:0;border-top:none;">
          <button type="button" class="btn" data-goto-step="lawyer-step-2">← Previous: Step 2 (Statutory Proof Matrix)</button>
          <button type="button" class="btn primary" data-goto-step="lawyer-step-4">Continue to Step 4: Exhibits &amp; Calculators →</button>
        </div>
      </div>
    </section>

    <!-- STEP 4: PROOF — EXHIBIT FOUNDATIONS & MULTI-DOMAIN STATUTORY CALCULATORS -->
    <section id="lawyer-step-4" class="workspace-section">
      <div id="lawyer-pedagogy-4"></div>

      <div class="card" style="border-left:6px solid var(--stipulated);">
        <span class="badge stip">Step 4 of 5 · Master Exhibit Register &amp; Admissibility Foundations</span>
        <h2>Verify Evidentiary Foundations, Chain of Custody &amp; Admission Status</h2>
        <div id="lawyer-step4-multimodal"></div>
        <div id="lawyer-exhibits-table" style="overflow-x:auto;margin-bottom:12px;"></div>

        <details class="action-drawer">
          <summary>+ Register Exhibit &amp; Admissibility Foundation</summary>
          <div class="form-grid" style="margin-bottom:10px;">
            <div class="form-field">
              <label for="lex-label-in">Exhibit Label (e.g., Ex. A)</label>
              <input type="text" id="lex-label-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="lex-title-in">Document Title</label>
              <input type="text" id="lex-title-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="lex-found-in">Evidentiary Rule Foundation (e.g., FRE 803(6), 901)</label>
              <input type="text" id="lex-found-in" class="search-input">
            </div>
            <div class="form-field">
              <label for="lex-status-in">Admission Status</label>
              <select id="lex-status-in" class="btn" style="width:100%;">
                <option value="Stipulated">Stipulated</option>
                <option value="Ready to Offer" selected>Ready to Offer</option>
                <option value="Admitted">Admitted</option>
                <option value="Objected / Contested">Objected / Contested</option>
              </select>
            </div>
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="lex-purp-in">Evidentiary Purpose &amp; Fact Established</label>
            <input type="text" id="lex-purp-in" class="search-input">
          </div>
          <div class="form-field" style="margin-bottom:10px;">
            <label for="lex-file-in">Attach Exhibit File (.pdf, .png, .jpg, .docx, .csv, .eml — Optional)</label>
            <input type="file" id="lex-file-in" class="search-input" accept=".pdf,.png,.jpg,.jpeg,.webp,.gif,.bmp,.svg,.docx,.xlsx,.rtf,.csv,.tsv,.txt,.md,.eml">
          </div>
          <button type="button" class="btn primary" id="btn-lawyer-add-ex">+ Save Exhibit</button>
        </details>

        <details class="action-drawer">
          <summary>🔐 Verify Local Document File Integrity (Compute SHA-256 Chain-of-Custody Digest)</summary>
          <p style="margin:0 0 10px;font-size:0.86rem;color:var(--muted);">Select any PDF, image, or document file on your device to compute its cryptographic SHA-256 fingerprint locally in your browser (the file never leaves your device) and attach it to an exhibit's authentication note:</p>
          <div class="form-grid" style="align-items:end;">
            <div class="form-field">
              <label for="coc-ex-select">Target Exhibit</label>
              <select id="coc-ex-select" class="btn" style="width:100%;"></select>
            </div>
            <div class="form-field">
              <label for="coc-file-in">Select Local Document File</label>
              <input type="file" id="coc-file-in" class="search-input">
            </div>
          </div>
          <div id="coc-hash-out" class="finding-box" style="display:none;"></div>
        </details>
      </div>

      <!-- Focused Tabbed Multi-Domain Statutory Calculators -->
      <div class="card">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px;">
          <div>
            <span class="badge info">Statutory &amp; Guideline Remedy Calculators</span>
            <h3 style="margin:4px 0 0;">Domain-Specific Remedy &amp; Worksheet Calculator</h3>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:6px;" role="tablist" aria-label="Select Domain Calculator">
            <button type="button" class="btn calc-tab-btn primary" data-calc-tab="calc-tab-family">Family Support (§ 305)</button>
            <button type="button" class="btn calc-tab-btn" data-calc-tab="calc-tab-va">Veterans Rating (38 C.F.R. § 4.25)</button>
            <button type="button" class="btn calc-tab-btn" data-calc-tab="calc-tab-civil">Housing &amp; Civil (§ 4.104 / § 2-714)</button>
          </div>
        </div>

        <!-- Calculator 1: Family Support Guidelines -->
        <div id="calc-tab-family" class="calc-pane card" style="margin-bottom:0;background:var(--surface-alt);">
          <span class="badge stip">Family Law · Support Guidelines (§ 305)</span>
          <h4>Shared Parenting Support Worksheet</h4>
          <div class="form-grid">
            <div class="form-field">
              <label for="calc-p1-inc">Party A Monthly Gross Income ($)</label>
              <input type="number" id="calc-p1-inc" class="search-input">
            </div>
            <div class="form-field">
              <label for="calc-p2-inc">Party B Monthly Gross Income ($)</label>
              <input type="number" id="calc-p2-inc" class="search-input">
            </div>
            <div class="form-field">
              <label for="calc-p2-nights">Party B Annual Overnights (0–365)</label>
              <input type="number" id="calc-p2-nights" class="search-input" step="0.5">
            </div>
            <div class="form-field">
              <label for="calc-addons">Direct Childcare / Medical Add-On ($/mo)</label>
              <input type="number" id="calc-addons" class="search-input">
            </div>
          </div>
          <div id="calc-support-out" class="pivot-say" style="font-size:0.9rem;"></div>
        </div>

        <!-- Calculator 2: Veterans 38 CFR 4.25 Combined Rating -->
        <div id="calc-tab-va" class="calc-pane card" style="display:none;margin-bottom:0;background:var(--surface-alt);">
          <span class="badge info">Veterans Law · 38 C.F.R. §§ 4.25 &amp; 4.16</span>
          <h4>Combined Rating &amp; TDIU Calculator</h4>
          <div class="form-grid">
            <div class="form-field">
              <label for="calc-va-ratings">Individual Ratings (%, comma-separated)</label>
              <input type="text" id="calc-va-ratings" class="search-input">
            </div>
            <div class="form-field">
              <label for="calc-va-comp">Monthly Compensation Baseline ($)</label>
              <input type="number" id="calc-va-comp" class="search-input">
            </div>
          </div>
          <div id="calc-va-out" class="pivot-say" style="font-size:0.9rem;"></div>
        </div>

        <!-- Calculator 3: Housing & Civil Abatement / Damages -->
        <div id="calc-tab-civil" class="calc-pane card" style="display:none;margin-bottom:0;background:var(--surface-alt);">
          <span class="badge warn">Housing &amp; Civil · URLTA § 4.104 / UCC § 2-714</span>
          <h4>Rent Abatement &amp; Diminution Calculator</h4>
          <div class="form-grid">
            <div class="form-field">
              <label for="calc-civ-rate">Monthly Contract / Lease Rate ($)</label>
              <input type="number" id="calc-civ-rate" class="search-input">
            </div>
            <div class="form-field">
              <label for="calc-civ-mos">Impaired Duration (Months)</label>
              <input type="number" id="calc-civ-mos" class="search-input">
            </div>
            <div class="form-field">
              <label for="calc-civ-dim">Diminution in Value (%)</label>
              <input type="number" id="calc-civ-dim" class="search-input">
            </div>
          </div>
          <div id="calc-civ-out" class="pivot-say" style="font-size:0.9rem;"></div>
        </div>

        <div class="step-footer">
          <button type="button" class="btn" data-goto-step="lawyer-step-3">← Previous: Step 3 (Witnesses &amp; Exams)</button>
          <button type="button" class="btn primary" data-goto-step="lawyer-step-5">Continue to Step 5: Trial Brief &amp; Handoff →</button>
        </div>
      </div>
    </section>

    <!-- STEP 5: RESOLUTION — CONSISTENCY AUDIT, PRIORITY SCHEDULE, CLIENT Q&A & TRIAL BRIEF -->
    <section id="lawyer-step-5" class="workspace-section">
      <div id="lawyer-pedagogy-5"></div>

      <div class="card" style="border-left:6px solid var(--stipulated);">
        <span class="badge stip">Step 5 of 5 · Automated Consistency Audit &amp; Priority Examination Schedule</span>
        <h2>Verify Record Completeness &amp; Examination Priority Order</h2>
        <div id="lawyer-consistency-audit" class="grid-2" style="margin-bottom:14px;"></div>
        <div id="lawyer-priority-schedule" class="card" style="margin-bottom:0;background:var(--surface-alt);"></div>
      </div>

      <div id="lawyer-step5-filing-center"></div>

      <div class="card" style="border-left:6px solid var(--accent);">
        <span class="badge info">Client–Counsel Alignment &amp; Trial Brief Generation</span>
        <h3>Respond to Client Questions &amp; Export the Compiled Trial Brief</h3>
        <p style="margin:0 0 14px;color:var(--muted);">Provide written guidance on your client's flagged questions below, then export the updated <code>.prismlegal.json</code> matter file or download the formatted Markdown Trial Brief.</p>

        <div id="lawyer-agenda-wrap" style="margin-bottom:16px;"></div>

        <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:14px;">
          <button type="button" class="btn primary" id="btn-lawyer-export-md">📄 Download Compiled Trial Brief (.md)</button>
          <button type="button" class="btn" id="btn-step5-lawyer-json">💾 Export Updated Matter File for Client (.prismlegal.json)</button>
          <button type="button" class="btn" id="btn-lawyer-print">🖨️ Print Trial Brief View</button>
          <a href="courtroom.html" class="btn primary">🏛️ Launch Courtroom Mode →</a>
        </div>

        <div class="step-footer">
          <button type="button" class="btn" data-goto-step="lawyer-step-4">← Previous: Step 4 (Exhibits &amp; Calculators)</button>
          <a href="courtroom.html" class="btn primary">Proceed to Courtroom Mode →</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer" role="contentinfo">
    <strong>PrismLegal — Attorney Case Workbench Journey</strong> · Free Open-Source Legal Preparation Service · 100% Private Browser Storage
  </footer>

  <script id="case-model-data" type="application/json">{payload_json}</script>
  <script>
    (function() {{
      {_shared_js_helpers()}
      setupJourneyStepper();

      let matter = ensureActiveMatter();
      const matterSelect = document.getElementById('lawyer-matter-select');
      const matterMeta = document.getElementById('lawyer-matter-meta');

      function refreshMatterSelector() {{
        matter = ensureActiveMatter();
        matterSelect.innerHTML = buildMatterSelectOptionsHtml(matter);
        const modeTag = matter.isExample ? '📘 Reference Example Preview' : (matter.isUnsavedDraft ? '✨ Unsaved Draft' : '★ Saved Matter');
        matterMeta.textContent = `${{modeTag}} · ${{matter.areaOfLaw || ''}} · ${{matter.docketNumber || 'No docket'}}`;
      }}

      matterSelect.addEventListener('change', () => {{
        setActiveMatterId(matterSelect.value);
        matter = ensureActiveMatter();
        renderAll();
      }});

      document.getElementById('btn-lawyer-export-json').addEventListener('click', () => exportMatterJson(matter));
      document.getElementById('btn-step5-lawyer-json').addEventListener('click', () => exportMatterJson(matter));
      document.getElementById('btn-lawyer-export-md').addEventListener('click', () => downloadMatterMarkdown(matter));
      document.getElementById('btn-lawyer-print').addEventListener('click', () => window.print());

      const importFile = document.getElementById('lawyer-import-file');
      importFile.addEventListener('change', () => {{
        if (importFile.files && importFile.files[0]) {{
          importMatterFromFile(importFile.files[0], (imported) => {{
            matter = imported;
            renderAll();
          }});
        }}
      }});

      function renderHealthStrip() {{
        const claims = matter.claims || [];
        const backed = claims.filter(c => c.exhibits && c.exhibits.length > 0);
        const exs = matter.exhibits || [];
        const wits = matter.witnesses || [];
        const usedMins = wits.reduce((s, w) => s + (Number(w.minutes) || 0), 0);
        const budget = Number(matter.hearingMinutes) || 180;
        const openAg = (matter.agenda || []).filter(a => a.status !== 'Aligned').length;
        document.getElementById('lawyer-health-strip').innerHTML = `
          <div class="kpi-card ${{backed.length === claims.length && claims.length > 0 ? 'stip' : 'warn'}}">
            <div class="kpi-label">Statutory Proof Coverage</div>
            <div class="kpi-val">${{backed.length}} / ${{claims.length}} Claims</div>
            <div class="kpi-note">${{claims.length - backed.length === 0 ? 'All claims backed by exhibits' : (claims.length - backed.length) + ' claim(s) missing exhibit link'}}</div>
          </div>
          <div class="kpi-card info">
            <div class="kpi-label">Registered Exhibits</div>
            <div class="kpi-val">${{exs.length}} Exhibits</div>
            <div class="kpi-note">With evidentiary foundations</div>
          </div>
          <div class="kpi-card ${{usedMins <= budget ? 'stip' : 'warn'}}">
            <div class="kpi-label">Hearing Clock Budget</div>
            <div class="kpi-val">${{usedMins}} / ${{budget}} min</div>
            <div class="kpi-note">${{wits.length}} Witness(es) on roster</div>
          </div>
          <div class="kpi-card info">
            <div class="kpi-label">Client Strategy Notes</div>
            <div class="kpi-val">${{(matter.agenda || []).length}} Note(s)</div>
            <div class="kpi-note">${{openAg}} awaiting counsel response</div>
          </div>
        `;
      }}

      function renderStep1() {{
        const ped1 = document.getElementById('lawyer-pedagogy-1');
        if (ped1) ped1.innerHTML = renderPedagogyBanner('counsel-step-1');

        document.getElementById('lm-title').value = matter.title || '';
        document.getElementById('lm-area').value = matter.areaOfLaw || 'Family & Parenting Law';
        document.getElementById('lm-scope').value = matter.representationScope || 'Full-Scope Representation';
        document.getElementById('lm-forum').value = matter.forum || '';
        document.getElementById('lm-docket').value = matter.docketNumber || '';
        document.getElementById('lm-date').value = matter.hearingDate || '';
        document.getElementById('lm-mins').value = Number(matter.hearingMinutes) || 180;
        document.getElementById('lm-client').value = matter.clientName || '';
        document.getElementById('lm-counsel').value = matter.counselName || '';
        document.getElementById('lm-summary').value = matter.summary || '';

        const pHead = document.getElementById('lm-posture-heading');
        if (pHead) pHead.textContent = (matter.title || 'Active Matter') + ' · ' + (matter.areaOfLaw || 'Legal Matter');
        const pSub = document.getElementById('lm-posture-sub');
        if (pSub) pSub.textContent = [matter.forum, matter.docketNumber ? ('Docket: ' + matter.docketNumber) : '', matter.hearingDate ? ('Hearing: ' + matter.hearingDate) : '', (Number(matter.hearingMinutes) || 180) + ' min budget', matter.representationScope || 'Full-Scope Representation'].filter(Boolean).join(' · ');
        const pBox = document.getElementById('lm-posture-box');
        if (pBox) pBox.innerHTML = renderCourtCaptionMastheadHtml(matter);

        const lmm1 = document.getElementById('lawyer-step1-multimodal');
        if (lmm1 && !lmm1.dataset.bound) {{
          lmm1.innerHTML = renderMultiModalDropzoneHtml('lawyer-mm1', 'Drop client discovery files, PDFs, financial CSV ledgers, notices, emails (.eml/.txt), or inspection graphics (.png/.jpg/.svg) here. Each upload is SHA-256 hashed, classified for FRE admissibility, and linked into your proof matrix and examination scripts.');
          bindMultiModalDropzoneEvents('lawyer-mm1', () => matter, (updated) => {{
            matter = updated;
            refreshMatterSelector();
            renderAll();
          }});
          lmm1.dataset.bound = '1';
        }}

        const goalsList = document.getElementById('lawyer-goals-list');
        const goals = matter.reliefGoals || [];
        if (!goals.length) {{
          goalsList.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">No relief goals defined yet. Click "+ Load Standard Practice-Area Elements &amp; Relief Goals" above or add relief goals in Client Step 1.</div>`;
        }} else {{
          goalsList.innerHTML = goals.map((g, idx) => `
            <article class="card" style="margin-bottom:0;background:var(--surface-alt);border-top:4px solid var(--stipulated);">
              <span class="badge stip">Relief Order ${{idx + 1}} · ${{escapeHtml(g.title)}}</span>
              <h4 style="margin:8px 0 4px;">${{escapeHtml(g.requestedOrder)}}</h4>
              <p style="font-size:0.86rem;color:var(--muted);margin:0;">${{escapeHtml(g.rationale)}}</p>
            </article>
          `).join('');
        }}
      }}

      const btnScaffoldDomain = document.getElementById('btn-scaffold-domain');
      if (btnScaffoldDomain) {{
        btnScaffoldDomain.addEventListener('click', () => {{
          extrapolateCaseFromIntake(matter, {{ inferArea: true, seedStarterIntake: true }});
          updateActiveMatter(matter);
          refreshMatterSelector();
          renderAll();
        }});
      }}

      document.getElementById('btn-save-lm-meta').addEventListener('click', () => {{
        matter.title = document.getElementById('lm-title').value.trim();
        matter.areaOfLaw = document.getElementById('lm-area').value;
        matter.representationScope = document.getElementById('lm-scope').value;
        matter.forum = document.getElementById('lm-forum').value.trim();
        matter.docketNumber = document.getElementById('lm-docket').value.trim();
        matter.hearingDate = document.getElementById('lm-date').value.trim();
        matter.hearingMinutes = Number(document.getElementById('lm-mins').value) || 180;
        matter.clientName = document.getElementById('lm-client').value.trim();
        matter.counselName = document.getElementById('lm-counsel').value.trim();
        matter.summary = document.getElementById('lm-summary').value.trim();
        extrapolateCaseFromIntake(matter, {{ inferArea: true, seedStarterIntake: true }});
        updateActiveMatter(matter);
        refreshMatterSelector();
        renderAll();
        const st = document.getElementById('lm-save-status');
        st.textContent = '✓ Saved & Case Model Extrapolated';
        setTimeout(() => {{ st.textContent = ''; }}, 2500);
      }});

      function renderStep2() {{
        const ped2 = document.getElementById('lawyer-pedagogy-2');
        if (ped2) ped2.innerHTML = renderPedagogyBanner('counsel-step-2');

        const listEl = document.getElementById('lawyer-claims-list');
        const claims = matter.claims || [];
        if (!claims.length) {{
          listEl.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">No statutory claims mapped yet. Enter your case facts in Step 1 and click "✨ Synthesize Statutory Claims &amp; Exceptions from My Intake" above, or add a custom element below.</div>`;
        }} else {{
          listEl.innerHTML = claims.map((c, idx) => {{
            const prop = compileClaimProposition(c);
            const jural = classifyJuralPosture(c, matter);
            const hasEx = prop.admissible;
            return `
              <article class="card" style="margin-bottom:0;background:var(--surface-alt);border-left:4px solid ${{hasEx ? 'var(--stipulated)' : 'var(--danger)'}};">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:6px;flex-wrap:wrap;">
                  <div>
                    <span class="badge info">${{escapeHtml(c.id)}}</span>
                    <code>${{escapeHtml(c.statute)}}</code>
                    ${{jural.valid ? `<span class="jural-pill" title="Enforceable Legal Posture">⚖️ ${{escapeHtml(jural.label)}}</span>` : ''}}
                  </div>
                  <div style="display:flex;gap:6px;align-items:center;">
                    <select class="btn lclm-status-sel" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.76rem;">
                      <option value="stipulated" ${{c.status === 'stipulated' ? 'selected' : ''}}>stipulated</option>
                      <option value="corroborated" ${{c.status === 'corroborated' ? 'selected' : ''}}>corroborated</option>
                      <option value="contested" ${{c.status === 'contested' ? 'selected' : ''}}>contested</option>
                    </select>
                    <button type="button" class="btn btn-del-lclm" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.74rem;">Remove</button>
                  </div>
                </div>
                <textarea class="search-input lclm-stmt-edit" data-idx="${{idx}}" style="width:100%;height:54px;margin-bottom:6px;">${{escapeHtml(c.statement)}}</textarea>
                <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;font-size:0.84rem;">
                  <div>
                    <strong>Exhibits:</strong>
                    ${{hasEx ? c.exhibits.map(x => `<span class="exhibit-pill">${{escapeHtml(x)}}</span>`).join(' ') : `<span class="badge danger">⚠️ Proof Gap: No Exhibit Linked</span>`}}
                  </div>
                </div>
                <div class="${{hasEx ? 'finding-box' : 'refusal-box'}}">
                  <strong>${{escapeHtml(prop.statusLabel)}}:</strong> ${{escapeHtml(prop.text)}}
                </div>
              </article>
            `;
          }}).join('');

          listEl.querySelectorAll('.lclm-status-sel').forEach(sel => {{
            sel.addEventListener('change', () => {{
              matter.claims[Number(sel.dataset.idx)].status = sel.value;
              updateActiveMatter(matter);
              renderStep2();
              renderHealthStrip();
            }});
          }});
          listEl.querySelectorAll('.lclm-stmt-edit').forEach(ta => {{
            ta.addEventListener('change', () => {{
              matter.claims[Number(ta.dataset.idx)].statement = ta.value.trim();
              updateActiveMatter(matter);
              renderStep2();
            }});
          }});
          listEl.querySelectorAll('.btn-del-lclm').forEach(btn => {{
            btn.addEventListener('click', () => {{
              matter.claims.splice(Number(btn.dataset.idx), 1);
              updateActiveMatter(matter);
              renderStep2();
              renderHealthStrip();
            }});
          }});
        }}

        const excWrap = document.getElementById('lawyer-exceptions-list');
        if (excWrap) {{
          const excs = matter.ruleExceptions || [];
          if (!excs.length) {{
            excWrap.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">No statutory exceptions, affirmative defenses, or rule overrides recorded yet.</div>`;
          }} else {{
            excWrap.innerHTML = excs.map((ex, idx) => `
              <article class="card" style="margin-bottom:0;background:var(--surface-alt);border-left:4px solid var(--accent);">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:4px;">
                  <div>
                    <span class="badge info">${{escapeHtml(ex.type || 'Statutory Exception')}}</span>
                    <code>${{escapeHtml(ex.statute || ex.rule)}}</code>
                    ${{ex.exhibitId ? `<span class="exhibit-pill">${{escapeHtml(ex.exhibitId)}}</span>` : ''}}
                  </div>
                  <button type="button" class="btn btn-del-exc" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.74rem;">Remove</button>
                </div>
                ${{ex.generalRule ? `<div style="font-size:0.82rem;color:var(--muted);margin-bottom:4px;"><strong>General Rule Claimed:</strong> ${{escapeHtml(ex.generalRule)}}</div>` : ''}}
                <p style="margin:4px 0 0;font-size:0.86rem;"><strong>Controlling Exception / Override:</strong> ${{escapeHtml(ex.effect || ex.exceptionRule || '')}}</p>
              </article>
            `).join('');
            excWrap.querySelectorAll('.btn-del-exc').forEach(btn => {{
              btn.addEventListener('click', () => {{
                matter.ruleExceptions.splice(Number(btn.dataset.idx), 1);
                updateActiveMatter(matter);
                renderStep2();
              }});
            }});
          }}
        }}
      }}

      const btnAddPresetClaims = document.getElementById('btn-add-preset-claims');
      if (btnAddPresetClaims) {{
        btnAddPresetClaims.addEventListener('click', () => {{
          extrapolateCaseFromIntake(matter, {{ inferArea: true, seedStarterIntake: true }});
          updateActiveMatter(matter);
          renderAll();
        }});
      }}

      const btnAddException = document.getElementById('btn-add-exception');
      if (btnAddException) {{
        btnAddException.addEventListener('click', () => {{
          const statEl = document.getElementById('lexc-stat-in');
          const exEl = document.getElementById('lexc-ex-in');
          const genEl = document.getElementById('lexc-gen-in');
          const ovEl = document.getElementById('lexc-ov-in');
          const rule = statEl ? statEl.value.trim() : '';
          const exhibitId = exEl ? exEl.value.trim() : '';
          const generalRule = genEl ? genEl.value.trim() : '';
          const effect = ovEl ? ovEl.value.trim() : '';
          if (!rule || !effect) return;
          matter.ruleExceptions = matter.ruleExceptions || [];
          matter.ruleExceptions.push({{
            id: 'EXC-' + String(matter.ruleExceptions.length + 1).padStart(2, '0'),
            statute: rule,
            rule,
            type: 'Statutory Exception / Override',
            generalRule,
            effect,
            exhibitId
          }});
          if (statEl) statEl.value = '';
          if (exEl) exEl.value = '';
          if (genEl) genEl.value = '';
          if (ovEl) ovEl.value = '';
          updateActiveMatter(matter);
          renderStep2();
        }});
      }}

      document.getElementById('btn-lawyer-add-claim').addEventListener('click', () => {{
        const statute = document.getElementById('lclm-stat-in').value.trim() || 'Governing Statute';
        const status = document.getElementById('lclm-status-in').value;
        const exhibits = document.getElementById('lclm-ex-in').value.split(',').map(s => s.trim()).filter(Boolean);
        const statement = document.getElementById('lclm-stmt-in').value.trim();
        if (!statement) return;
        matter.claims = matter.claims || [];
        matter.claims.push({{
          id: 'CLM-' + String(matter.claims.length + 1).padStart(2, '0'),
          statute,
          status,
          statement,
          exhibits
        }});
        document.getElementById('lclm-stat-in').value = '';
        document.getElementById('lclm-ex-in').value = '';
        document.getElementById('lclm-stmt-in').value = '';
        updateActiveMatter(matter);
        renderStep2();
        renderHealthStrip();
      }});

      function renderStep3() {{
        const ped3 = document.getElementById('lawyer-pedagogy-3');
        if (ped3) ped3.innerHTML = renderPedagogyBanner('counsel-step-3');

        const wits = matter.witnesses || [];
        const budget = Number(matter.hearingMinutes) || 180;
        const clock = computeHearingClockStages(budget, wits);
        const badge = document.getElementById('lawyer-clock-badge');
        badge.className = 'badge ' + (clock.overBudget ? 'danger' : 'stip');
        badge.textContent = `Witness Time: ${{clock.usedWitnessMinutes}} / ${{clock.availableExamPool}} min exam pool (${{clock.total}} min total)`;

        const stageStrip = document.getElementById('lawyer-stage-clock-strip');
        if (stageStrip) {{
          stageStrip.innerHTML = clock.stages.map(st => `
            <div class="kpi-card ${{clock.overBudget ? 'warn' : 'stip'}}">
              <div class="kpi-label">${{escapeHtml(st.name)}} (${{st.pct}}%)</div>
              <div class="kpi-val">${{st.minutes}} min</div>
              <div class="kpi-note">${{escapeHtml(st.note)}}</div>
            </div>
          `).join('');
        }}

        const wList = document.getElementById('lawyer-witness-list');
        if (!wits.length) {{
          wList.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">No witnesses listed yet. Open the "+ Add Witness to Roster" drawer below.</div>`;
        }} else {{
          wList.innerHTML = wits.map((w, idx) => `
            <article class="card" style="margin-bottom:0;background:var(--surface-alt);">
              <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:6px;">
                <div><span class="badge info">${{escapeHtml(w.id)}}</span> <span class="badge stip">${{escapeHtml(w.status || 'will-call')}}</span></div>
                <div style="display:flex;align-items:center;gap:4px;">
                  <label style="font-size:0.76rem;font-weight:700;">Min:
                    <input type="number" class="search-input lwit-min-edit" data-idx="${{idx}}" style="width:60px;padding:2px 6px;" value="${{Number(w.minutes) || 20}}">
                  </label>
                  <button type="button" class="btn btn-del-lwit" data-idx="${{idx}}" style="padding:2px 6px;font-size:0.72rem;">✕</button>
                </div>
              </div>
              <h4 style="margin:6px 0 2px;">${{escapeHtml(w.name)}}</h4>
              <div style="font-size:0.8rem;color:var(--muted);margin-bottom:6px;">${{escapeHtml(w.role)}}</div>
              <p style="font-size:0.86rem;margin:0;">${{escapeHtml(w.scope)}}</p>
            </article>
          `).join('');
          wList.querySelectorAll('.lwit-min-edit').forEach(inp => {{
            inp.addEventListener('change', () => {{
              matter.witnesses[Number(inp.dataset.idx)].minutes = Number(inp.value) || 0;
              updateActiveMatter(matter);
              renderStep3();
              renderHealthStrip();
            }});
          }});
          wList.querySelectorAll('.btn-del-lwit').forEach(btn => {{
            btn.addEventListener('click', () => {{
              matter.witnesses.splice(Number(btn.dataset.idx), 1);
              updateActiveMatter(matter);
              renderStep3();
              renderHealthStrip();
            }});
          }});
        }}

        const dxWrap = document.getElementById('lawyer-dx-list');
        const dxs = matter.directExam || [];
        dxWrap.innerHTML = dxs.length ? dxs.map(d => {{
          const cue = d.visualCue || 'standard';
          const isHighlight = cue === 'highlight' || cue === 'yellow-highlight';
          const isStrike = cue === 'strikethrough' || cue === 'red-strikethrough';
          return `
          <div class="card" style="margin-bottom:8px;padding:12px;background:var(--surface-alt);border-left:4px solid ${{isHighlight ? 'var(--stipulated)' : isStrike ? 'var(--muted)' : 'var(--accent)'}};${{isStrike ? 'opacity:0.78;' : ''}}">
            <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;">
              <span class="badge info">${{escapeHtml(d.id)}}</span>
              <span class="badge stip">${{escapeHtml(d.chapter)}}</span>
              ${{isHighlight ? `<span class="badge stip">⭐ Key Highlight</span>` : ''}}
              ${{isStrike ? `<span class="badge warn">🚫 Skip Unless Opened on Cross</span>` : ''}}
              ${{d.movesToAdmit ? `<span class="badge info">📎 Move to Admit</span>` : ''}}
              ${{d.exhibitId ? `<span class="exhibit-pill">${{escapeHtml(d.exhibitId)}}</span>` : ''}}
            </div>
            <div style="font-weight:700;margin:4px 0;${{isStrike ? 'text-decoration:line-through;' : ''}}">Q: ${{escapeHtml(d.question)}}</div>
            <div style="font-size:0.88rem;color:var(--muted);">A: "${{escapeHtml(d.answer)}}"</div>
            ${{(d.counselPrompt || d.coachingNote) ? `<div style="margin-top:4px;font-size:0.78rem;color:var(--accent);"><strong>📋 Script Note:</strong> ${{escapeHtml(d.counselPrompt || d.coachingNote)}}</div>` : ''}}
          </div>
          `;
        }}).join('') : `<div class="empty-state">No direct examination questions added yet.</div>`;

        const trWrap = document.getElementById('lawyer-traps-list');
        const trs = matter.traps || [];
        trWrap.innerHTML = trs.length ? trs.map(t => `
          <div class="card" style="margin-bottom:8px;padding:12px;background:var(--surface-alt);">
            <div><span class="badge warn">${{escapeHtml(t.id)}}</span> <strong>${{escapeHtml(t.title)}}</strong> ${{t.exhibitId ? `<span class="exhibit-pill">${{escapeHtml(t.exhibitId)}}</span>` : ''}}</div>
            <div style="font-size:0.86rem;margin:4px 0;"><strong>Challenge:</strong> ${{escapeHtml(t.question)}}</div>
            <div class="pivot-say" style="font-size:0.86rem;margin:4px 0 0;"><strong>Redirect / Response:</strong> "${{escapeHtml(t.response)}}"</div>
            ${{t.rule106Context ? `<div style="margin-top:6px;font-size:0.8rem;color:var(--accent);"><strong>📜 FRE 106 Full Context:</strong> ${{escapeHtml(t.rule106Context)}}</div>` : ''}}
          </div>
        `).join('') : `<div class="empty-state">No cross-examination topics added yet.</div>`;
      }}

      const btnLawyerAddDx = document.getElementById('btn-lawyer-add-dx');
      if (btnLawyerAddDx) {{
        btnLawyerAddDx.addEventListener('click', () => {{
          const chapter = document.getElementById('ldx-chap-in').value.trim() || 'Direct Testimony';
          const exhibitId = document.getElementById('ldx-ex-in').value.trim();
          const visualCue = document.getElementById('ldx-cue-in').value || 'standard';
          const movesToAdmit = document.getElementById('ldx-admit-in').value === 'yes';
          const question = document.getElementById('ldx-q-in').value.trim();
          const answer = document.getElementById('ldx-a-in').value.trim();
          if (!question || !answer) return;
          matter.directExam = matter.directExam || [];
          matter.directExam.push({{
            id: 'DX-' + String(matter.directExam.length + 1).padStart(2, '0'),
            chapter,
            question,
            answer,
            exhibitId,
            visualCue,
            movesToAdmit,
            counselPrompt: movesToAdmit && exhibitId ? `Counsel moves to admit ${{exhibitId}} into evidence.` : ''
          }});
          document.getElementById('ldx-chap-in').value = '';
          document.getElementById('ldx-ex-in').value = '';
          document.getElementById('ldx-q-in').value = '';
          document.getElementById('ldx-a-in').value = '';
          updateActiveMatter(matter);
          renderStep3();
        }});
      }}

      const btnLawyerAddTrap = document.getElementById('btn-lawyer-add-trap');
      if (btnLawyerAddTrap) {{
        btnLawyerAddTrap.addEventListener('click', () => {{
          const title = document.getElementById('ltr-title-in').value.trim() || 'Cross-Exam Challenge';
          const exhibitId = document.getElementById('ltr-ex-in').value.trim();
          const question = document.getElementById('ltr-q-in').value.trim();
          const response = document.getElementById('ltr-resp-in').value.trim();
          const rule106Context = document.getElementById('ltr-r106-in').value.trim();
          if (!question || !response) return;
          matter.traps = matter.traps || [];
          matter.traps.push({{
            id: 'T-' + String(matter.traps.length + 1).padStart(2, '0'),
            title,
            question,
            avoid: 'Do not argue, speculate, or accept selective out-of-context premises.',
            response,
            exhibitId,
            rule106Context
          }});
          document.getElementById('ltr-title-in').value = '';
          document.getElementById('ltr-ex-in').value = '';
          document.getElementById('ltr-q-in').value = '';
          document.getElementById('ltr-resp-in').value = '';
          document.getElementById('ltr-r106-in').value = '';
          updateActiveMatter(matter);
          renderStep3();
        }});
      }}

      document.getElementById('btn-add-witness').addEventListener('click', () => {{
        const name = document.getElementById('lwit-name-in').value.trim();
        const role = document.getElementById('lwit-role-in').value.trim();
        const status = document.getElementById('lwit-status-in').value;
        const minutes = Number(document.getElementById('lwit-mins-in').value) || 20;
        const scope = document.getElementById('lwit-scope-in').value.trim();
        if (!name) return;
        matter.witnesses = matter.witnesses || [];
        matter.witnesses.push({{
          id: 'W-' + String(matter.witnesses.length + 1).padStart(2, '0'),
          name,
          role: role || 'Fact Witness',
          status,
          minutes,
          scope
        }});
        document.getElementById('lwit-name-in').value = '';
        document.getElementById('lwit-role-in').value = '';
        document.getElementById('lwit-scope-in').value = '';
        updateActiveMatter(matter);
        renderStep3();
        renderHealthStrip();
      }});

      function renderStep4() {{
        const ped4 = document.getElementById('lawyer-pedagogy-4');
        if (ped4) ped4.innerHTML = renderPedagogyBanner('counsel-step-4');

        const lmm4 = document.getElementById('lawyer-step4-multimodal');
        if (lmm4 && !lmm4.dataset.bound) {{
          lmm4.innerHTML = renderMultiModalDropzoneHtml('lawyer-mm4', 'Batch-upload exhibit files (.pdf, .csv, .txt, .eml, .png, .jpg, .svg) to compute SHA-256 chain-of-custody digests, classify FRE foundations, and cross-link into your statutory claims and direct examination script.');
          bindMultiModalDropzoneEvents('lawyer-mm4', () => matter, (updated) => {{
            matter = updated;
            refreshMatterSelector();
            renderAll();
          }});
          lmm4.dataset.bound = '1';
        }}

        const exTable = document.getElementById('lawyer-exhibits-table');
        const exs = matter.exhibits || [];
        if (!exs.length) {{
          exTable.innerHTML = `<div class="empty-state">No exhibits registered yet. Drop multi-modal evidence files above or add exhibits below.</div>`;
        }} else {{
          exTable.innerHTML = `<table class="data-table">
            <thead><tr><th>Exhibit</th><th>Title, Modality &amp; Date</th><th>Evidentiary Purpose &amp; Visual Forensics</th><th>Admissibility Foundation</th><th>Status</th><th>Action</th></tr></thead>
            <tbody>
              ${{exs.map((e, idx) => {{
                const vNotesStr = typeof e.visualNotes === 'string' ? e.visualNotes.trim() : '';
                const pIntentStr = typeof e.pivotIntent === 'string' ? e.pivotIntent.trim() : '';
                const vNotesArr = Array.isArray(e.visualNotes) ? e.visualNotes : [];
                const pIntentArr = Array.isArray(e.pivotIntent) ? e.pivotIntent : [];
                const hasForensics = Boolean(vNotesStr || pIntentStr || vNotesArr.length || pIntentArr.length);
                return `
                <tr>
                  <td><span class="exhibit-pill">${{escapeHtml(e.label || e.id)}}</span></td>
                  <td>
                    <strong>${{escapeHtml(e.title)}}</strong>
                    ${{e.previewDataUrl ? `<div class="exhibit-thumb" style="margin:4px 0;"><img src="${{escapeHtml(e.previewDataUrl)}}" alt="${{escapeHtml(e.title)}}"></div>` : ''}}
                    ${{e.modality ? `<div style="margin-top:2px;"><span class="modality-badge">${{escapeHtml(e.modality)}}</span></div>` : ''}}
                    <span style="font-size:0.78rem;color:var(--muted);">${{escapeHtml(e.date || '')}}</span>
                    ${{e.sha256 ? `<div style="font-size:0.72rem;color:var(--stipulated);">🔐 SHA-256: <code>${{escapeHtml(e.sha256.slice(0, 16))}}…</code></div>` : ''}}
                  </td>
                  <td>
                    <div>${{escapeHtml(e.purpose)}}</div>
                    ${{hasForensics ? `
                      <details style="margin-top:6px;padding:6px 8px;border-radius:6px;background:var(--surface);border:1px solid var(--border);font-size:0.79rem;">
                        <summary style="cursor:pointer;font-weight:700;color:var(--accent);">🔍 Visual Forensics &amp; Trial Intent ▾</summary>
                        ${{vNotesStr ? `<div style="margin-top:4px;"><strong>Visual Callout:</strong> ${{escapeHtml(vNotesStr)}}</div>` : ''}}
                        ${{pIntentStr ? `<div style="margin-top:4px;color:var(--stipulated);"><strong>Trial Intent:</strong> ${{escapeHtml(pIntentStr)}}</div>` : ''}}
                        ${{vNotesArr.map(vn => `<div style="margin-top:4px;">• <strong>[${{escapeHtml(vn.pageRef)}}]</strong> ${{escapeHtml(vn.observation)}} — <em>${{escapeHtml(vn.intent)}}</em></div>`).join('')}}
                        ${{pIntentArr.map(pi => `<div style="margin-top:4px;color:var(--stipulated);">• <strong>Trial Intent (${{escapeHtml(pi.id)}}):</strong> ${{escapeHtml(pi.shows)}}</div>`).join('')}}
                      </details>
                    ` : ''}}
                  </td>
                  <td><input type="text" class="search-input lex-found-edit" data-idx="${{idx}}" style="width:100%;padding:4px 6px;font-size:0.82rem;" value="${{escapeHtml(e.foundation || 'FRE 901')}}"></td>
                  <td>
                    <select class="btn lex-status-edit" data-idx="${{idx}}" style="padding:3px 6px;font-size:0.78rem;">
                      <option value="Stipulated" ${{e.status === 'Stipulated' ? 'selected' : ''}}>Stipulated</option>
                      <option value="Ready to Offer" ${{e.status === 'Ready to Offer' ? 'selected' : ''}}>Ready to Offer</option>
                      <option value="Admitted" ${{e.status === 'Admitted' ? 'selected' : ''}}>Admitted</option>
                      <option value="Objected / Contested" ${{e.status === 'Objected / Contested' ? 'selected' : ''}}>Objected / Contested</option>
                    </select>
                  </td>
                  <td><button type="button" class="btn btn-del-lex" data-idx="${{idx}}" style="padding:2px 8px;font-size:0.74rem;">Remove</button></td>
                </tr>
                `;
              }}).join('')}}
            </tbody>
          </table>`;
          exTable.querySelectorAll('.lex-found-edit').forEach(inp => {{
            inp.addEventListener('change', () => {{
              matter.exhibits[Number(inp.dataset.idx)].foundation = inp.value.trim();
              updateActiveMatter(matter);
            }});
          }});
          exTable.querySelectorAll('.lex-status-edit').forEach(sel => {{
            sel.addEventListener('change', () => {{
              matter.exhibits[Number(sel.dataset.idx)].status = sel.value;
              updateActiveMatter(matter);
            }});
          }});
          exTable.querySelectorAll('.btn-del-lex').forEach(btn => {{
            btn.addEventListener('click', () => {{
              matter.exhibits.splice(Number(btn.dataset.idx), 1);
              updateActiveMatter(matter);
              renderStep4();
              renderHealthStrip();
            }});
          }});
        }}

        const cocSel = document.getElementById('coc-ex-select');
        if (cocSel) {{
          cocSel.innerHTML = exs.length
            ? exs.map((e, idx) => `<option value="${{idx}}">${{escapeHtml(e.label || e.id)}} — ${{escapeHtml(e.title)}}</option>`).join('')
            : `<option value="">No exhibits registered yet</option>`;
        }}

        // Auto-select calculator tab matching matter.areaOfLaw
        const areaLower = (matter.areaOfLaw || '').toLowerCase();
        const defaultCalcTab = areaLower.includes('veteran') ? 'calc-tab-va' : (areaLower.includes('family') || areaLower.includes('parent') ? 'calc-tab-family' : 'calc-tab-civil');
        activateCalcTab(defaultCalcTab);

        // Initialize Calculators from matter.calculators (zero defaults; bespoke values only)
        matter.calculators = matter.calculators || {{}};
        const c = matter.calculators;
        document.getElementById('calc-p1-inc').value = c.supportParty1Income !== undefined ? c.supportParty1Income : '';
        document.getElementById('calc-p2-inc').value = c.supportParty2Income !== undefined ? c.supportParty2Income : '';
        document.getElementById('calc-p2-nights').value = c.supportParty2Nights !== undefined ? c.supportParty2Nights : '';
        document.getElementById('calc-addons').value = c.supportAddons !== undefined ? c.supportAddons : '';
        document.getElementById('calc-va-ratings').value = c.vaRatings !== undefined ? c.vaRatings : '';
        document.getElementById('calc-va-comp').value = c.vaMonthlyBaseline !== undefined ? c.vaMonthlyBaseline : '';
        document.getElementById('calc-civ-rate').value = c.civilContractRate !== undefined ? c.civilContractRate : '';
        document.getElementById('calc-civ-mos').value = c.civilImpairedMonths !== undefined ? c.civilImpairedMonths : '';
        document.getElementById('calc-civ-dim').value = c.civilDiminutionPct !== undefined ? c.civilDiminutionPct : '';
        recomputeCalculators(false);
      }}

      const cocFileIn = document.getElementById('coc-file-in');
      if (cocFileIn) {{
        cocFileIn.addEventListener('change', async (ev) => {{
          const file = ev.target.files && ev.target.files[0];
          if (!file) return;
          const buf = await file.arrayBuffer();
          const hashBuf = await crypto.subtle.digest('SHA-256', buf);
          const hex = Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2, '0')).join('');
          const shortHex = hex.slice(0, 16) + '…' + hex.slice(-8);
          const cocSel = document.getElementById('coc-ex-select');
          const exIdx = cocSel && cocSel.value !== '' ? Number(cocSel.value) : -1;
          const out = document.getElementById('coc-hash-out');
          if (exIdx >= 0 && matter.exhibits && matter.exhibits[exIdx]) {{
            const curFound = matter.exhibits[exIdx].foundation || 'FRE 901';
            const cleanFound = curFound.replace(/ · SHA-256: [0-9a-f…]+/i, '');
            matter.exhibits[exIdx].foundation = `${{cleanFound}} · SHA-256: ${{shortHex}}`;
            matter.exhibits[exIdx].sha256 = hex;
            updateActiveMatter(matter);
            renderStep4();
            if (out) {{
              out.style.display = 'block';
              out.innerHTML = `<strong>✓ Verified File Integrity (${{escapeHtml(file.name)}}):</strong> <code>${{hex}}</code> attached to <strong>${{escapeHtml(matter.exhibits[exIdx].label || matter.exhibits[exIdx].id)}}</strong>.`;
            }}
          }} else if (out) {{
            out.style.display = 'block';
            out.innerHTML = `<strong>✓ File SHA-256 (${{escapeHtml(file.name)}}):</strong> <code>${{hex}}</code>`;
          }}
        }});
      }}

      function activateCalcTab(targetId) {{
        document.querySelectorAll('.calc-tab-btn').forEach(b => b.classList.toggle('primary', b.getAttribute('data-calc-tab') === targetId));
        ['calc-tab-family', 'calc-tab-va', 'calc-tab-civil'].forEach(pid => {{
          const el = document.getElementById(pid);
          if (el) el.style.display = pid === targetId ? 'block' : 'none';
        }});
      }}

      document.querySelectorAll('.calc-tab-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          activateCalcTab(btn.getAttribute('data-calc-tab'));
        }});
      }});

      function recomputeCalculators(persist) {{
        matter.calculators = matter.calculators || {{}};
        const c = matter.calculators;
        const p1Val = Number(document.getElementById('calc-p1-inc').value) || 0;
        const p2Val = Number(document.getElementById('calc-p2-inc').value) || 0;
        const nightsVal = Math.max(0, Math.min(365, Number(document.getElementById('calc-p2-nights').value) || 0));
        const addonsVal = Number(document.getElementById('calc-addons').value) || 0;
        if (persist) {{
          c.supportParty1Income = p1Val;
          c.supportParty2Income = p2Val;
          c.supportParty2Nights = nightsVal;
          c.supportAddons = addonsVal;
        }}

        const comb = p1Val + p2Val;
        if (comb <= 0) {{
          document.getElementById('calc-support-out').innerHTML = `<span style="color:var(--muted);">Enter party income figures above or include monthly income/overnights in your Step 1 intake to compute support.</span>`;
        }} else {{
          const p1Share = p1Val / comb;
          const p2Share = p2Val / comb;
          const p1Nights = 365 - nightsVal;
          const basic = Math.max(1000, comb * 0.155);
          if (nightsVal >= 93) {{
            const mult = basic * 1.5;
            const p2Oblig = mult * p2Share * (p1Nights / 365) + addonsVal * p2Share;
            const p1Oblig = mult * p1Share * (nightsVal / 365);
            const net = p1Oblig - p2Oblig;
            document.getElementById('calc-support-out').innerHTML = net >= 0
              ? `<strong>Shared Schedule Result:</strong> Party A pays Party B <strong>$${{net.toFixed(2)}}/mo</strong> (Combined: $${{comb.toLocaleString()}}/mo).`
              : `<strong>Shared Schedule Result:</strong> Party B pays Party A <strong>$${{Math.abs(net).toFixed(2)}}/mo</strong>.`;
          }} else {{
            const net = (basic + addonsVal) * p2Share;
            document.getElementById('calc-support-out').innerHTML = `<strong>Standard Worksheet:</strong> Party B pays Party A <strong>$${{net.toFixed(2)}}/mo</strong>.`;
          }}
        }}

        const vaRatingsStr = document.getElementById('calc-va-ratings').value;
        const vaCompVal = Number(document.getElementById('calc-va-comp').value) || 0;
        if (persist) {{
          c.vaRatings = vaRatingsStr;
          c.vaMonthlyBaseline = vaCompVal;
        }}
        const ratings = (vaRatingsStr || '').split(',').map(s => Math.max(0, Math.min(100, Number(s.trim()) || 0))).filter(n => n > 0).sort((a, b) => b - a);
        if (!ratings.length) {{
          document.getElementById('calc-va-out').innerHTML = `<span style="color:var(--muted);">Enter comma-separated disability ratings above or include percentage ratings in your Step 1 intake to compute 38 C.F.R. § 4.25 combined rating.</span>`;
        }} else {{
          let eff = 100;
          ratings.forEach(r => {{ eff = eff * (1 - r / 100); }});
          const rawComb = 100 - eff;
          const roundComb = Math.min(100, Math.round(rawComb / 10) * 10);
          const maxSingle = ratings[0];
          const tdiu = (maxSingle >= 60) || (roundComb >= 70 && ratings.length >= 2);
          document.getElementById('calc-va-out').innerHTML =
            `<strong>38 C.F.R. § 4.25 Combined:</strong> ${{rawComb.toFixed(1)}}% → <strong>${{roundComb}}%</strong><br>` +
            `<strong>§ 4.16(a) TDIU:</strong> ${{tdiu ? '✅ Eligible' + (vaCompVal > 0 ? ' ($' + vaCompVal.toLocaleString() + '/mo)' : '') : '⚠️ Below schedular threshold'}}`;
        }}

        const civRateVal = Number(document.getElementById('calc-civ-rate').value) || 0;
        const civMosVal = Number(document.getElementById('calc-civ-mos').value) || 0;
        const civDimVal = Math.max(0, Math.min(100, Number(document.getElementById('calc-civ-dim').value) || 0));
        if (persist) {{
          c.civilContractRate = civRateVal;
          c.civilImpairedMonths = civMosVal;
          c.civilDiminutionPct = civDimVal;
        }}
        const gross = civRateVal * civMosVal;
        if (gross <= 0) {{
          document.getElementById('calc-civ-out').innerHTML = `<span style="color:var(--muted);">Enter monthly contract/lease rate and impaired months above or include figures in your Step 1 intake to compute damages.</span>`;
        }} else {{
          const abate = gross * (civDimVal / 100);
          document.getElementById('calc-civ-out').innerHTML =
            `<strong>Gross Contract:</strong> $${{gross.toLocaleString()}}<br>` +
            `<strong>Abatement / Damages (${{civDimVal}}%):</strong> <strong>$${{abate.toFixed(2)}}</strong> (Net: $${{(gross - abate).toFixed(2)}})`;
        }}

        if (persist) updateActiveMatter(matter);
      }}

      ['calc-p1-inc', 'calc-p2-inc', 'calc-p2-nights', 'calc-addons', 'calc-va-ratings', 'calc-va-comp', 'calc-civ-rate', 'calc-civ-mos', 'calc-civ-dim'].forEach(id => {{
        document.getElementById(id).addEventListener('input', () => recomputeCalculators(true));
      }});

      document.getElementById('btn-lawyer-add-ex').addEventListener('click', async () => {{
        const label = document.getElementById('lex-label-in').value.trim();
        let title = document.getElementById('lex-title-in').value.trim();
        const foundationIn = document.getElementById('lex-found-in').value.trim();
        const status = document.getElementById('lex-status-in').value;
        let purpose = document.getElementById('lex-purp-in').value.trim();
        const fileEl = document.getElementById('lex-file-in');
        const fileObj = (fileEl && fileEl.files && fileEl.files[0]) ? fileEl.files[0] : null;
        if (!title && !fileObj) return;
        let parsed = null;
        if (fileObj) {{
          parsed = await parseMultiModalFileInBrowser(fileObj, matter);
          if (!title) title = parsed.title;
          if (!purpose) purpose = parsed.purpose;
        }}
        matter.exhibits = matter.exhibits || [];
        const nextNum = matter.exhibits.length + 1;
        const id = label ? label.replace(/[^A-Za-z0-9_-]/g, '-') : ('Ex-' + nextNum);
        const exProf = classifyExhibitIntake({{ title, purpose, foundation: foundationIn }});
        matter.exhibits.push({{
          id,
          label: label || ('Ex. ' + nextNum),
          party: 'Client',
          title,
          date: parsed ? parsed.date : 'Record',
          purpose,
          modality: parsed ? parsed.modality : '',
          sha256: parsed ? parsed.sha256 : '',
          previewDataUrl: parsed ? (parsed.previewDataUrl || '') : '',
          exifSummary: parsed ? (parsed.exifSummary || '') : '',
          foundation: foundationIn || (parsed ? parsed.foundation : exProf.foundation),
          visualNotes: parsed ? parsed.visualNotes : exProf.visualNotes,
          pivotIntent: parsed ? parsed.pivotIntent : exProf.pivotIntent,
          status
        }});
        document.getElementById('lex-label-in').value = '';
        document.getElementById('lex-title-in').value = '';
        document.getElementById('lex-found-in').value = '';
        document.getElementById('lex-purp-in').value = '';
        if (fileEl) fileEl.value = '';
        extrapolateCaseFromIntake(matter, {{ inferArea: false, seedStarterIntake: false }});
        updateActiveMatter(matter);
        renderAll();
      }});

      function renderStep5() {{
        const ped5 = document.getElementById('lawyer-pedagogy-5');
        if (ped5) ped5.innerHTML = renderPedagogyBanner('counsel-step-5');

        const auditEl = document.getElementById('lawyer-consistency-audit');
        if (auditEl) {{
          const checks = auditMatterConsistency(matter);
          auditEl.innerHTML = checks.map(ch => `
            <div class="kpi-card ${{ch.ok ? 'stip' : 'warn'}}">
              <div class="kpi-label">${{ch.ok ? '✓ Ready' : '⚠️ Attention'}} · ${{escapeHtml(ch.label)}}</div>
              <div class="kpi-note" style="margin-top:4px;font-size:0.84rem;color:var(--ink);">${{escapeHtml(ch.detail)}}</div>
            </div>
          `).join('');
        }}

        const schedEl = document.getElementById('lawyer-priority-schedule');
        if (schedEl) {{
          const claims = matter.claims || [];
          const strategies = computeAdaptiveStrategySchedule(matter);
          const clock = computeHearingClockStages(matter.hearingMinutes, matter.witnesses);
          const directPool = clock.stages[1] ? clock.stages[1].minutes : 60;
          if (!claims.length && !strategies.length) {{
            schedEl.innerHTML = `<div class="empty-state">Add statutory claims in Step 2 or upload multi-modal evidence in Step 1/4 to generate your prioritized examination schedule.</div>`;
          }} else {{
            const stratHtml = strategies.length ? `
              <div style="margin-bottom:14px;">
                <span class="badge stip">⚡ Adaptive Strategy Priority Ranking (Bounded Weight Schedule 1..16)</span>
                <div class="kpi-strip" style="margin-top:8px;margin-bottom:8px;">
                  ${{strategies.map((st, idx) => `
                    <div class="kpi-card ${{idx === 0 ? 'stip' : 'info'}}">
                      <div class="kpi-label">Rank #${{idx + 1}} · Score ${{st.weight}}/${{st.maxWeight}}</div>
                      <div class="kpi-val" style="font-size:0.95rem;">${{escapeHtml(st.title)}}</div>
                      <div class="kpi-note"><strong>Focus:</strong> ${{escapeHtml(st.focus)}}<br><em>${{escapeHtml(st.rationale)}}</em></div>
                    </div>
                  `).join('')}}
                </div>
              </div>
            ` : '';
            const perClaimMin = claims.length ? Math.max(5, Math.round(directPool / claims.length)) : 0;
            const tableHtml = claims.length ? `<table class="data-table">
              <thead><tr><th>Priority Rank</th><th>Statutory Element &amp; Legal Posture</th><th>Evidentiary Status</th><th>Supporting Exhibits</th><th>Target Direct Exam Window</th></tr></thead>
              <tbody>
                ${{claims.map((c, i) => {{
                  const hasEx = Array.isArray(c.exhibits) && c.exhibits.length > 0;
                  const jural = classifyJuralPosture(c, matter);
                  return `
                    <tr>
                      <td><span class="badge ${{i === 0 ? 'stip' : 'info'}}">Priority #${{i + 1}}</span></td>
                      <td>
                        <code>${{escapeHtml(c.statute)}}</code>
                        ${{jural.valid ? `<span class="jural-pill">⚖️ ${{escapeHtml(jural.label)}}</span>` : ''}}
                        <br><span style="font-size:0.82rem;color:var(--muted);">${{escapeHtml(c.statement)}}</span>
                      </td>
                      <td><span class="badge ${{hasEx ? 'stip' : 'danger'}}">${{hasEx ? escapeHtml(c.status || 'corroborated') : 'Proof Gap'}}</span></td>
                      <td>${{hasEx ? c.exhibits.map(x => `<span class="exhibit-pill">${{escapeHtml(x)}}</span>`).join(' ') : '<em>None</em>'}}</td>
                      <td><strong>${{perClaimMin}} min</strong></td>
                    </tr>
                  `;
                }}).join('')}}
              </tbody>
            </table>` : '';
            schedEl.innerHTML = stratHtml + tableHtml;
          }}
        }}

        const lfcWrap = document.getElementById('lawyer-step5-filing-center');
        if (lfcWrap) {{
          lfcWrap.innerHTML = renderFilingCenterHtml(matter, 'lawyer-fc');
          bindFilingCenterEvents('lawyer-fc', () => matter);
        }}

        const agWrap = document.getElementById('lawyer-agenda-wrap');
        const ag = matter.agenda || [];
        if (!ag.length) {{
          agWrap.innerHTML = `<div class="empty-state">No client questions logged yet. Questions added in Client Step 5 appear here for attorney response.</div>`;
          return;
        }}
        agWrap.innerHTML = ag.map((a, idx) => `
          <div class="card" style="margin-bottom:10px;padding:14px;background:var(--surface-alt);">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:6px;">
              <div><span class="badge info">${{escapeHtml(a.id)}}</span> <strong>${{escapeHtml(a.topic)}}</strong></div>
              <span class="badge stip">${{escapeHtml(a.status || 'Open')}}</span>
            </div>
            <p style="margin:6px 0;font-size:0.92rem;"><strong>Client Question:</strong> ${{escapeHtml(a.questionForCounsel)}}</p>
            <label style="font-size:0.84rem;font-weight:700;display:block;">Attorney Guidance / Trial Plan:<br>
              <input type="text" class="search-input law-ag-edit" data-idx="${{idx}}" style="width:100%;margin-top:4px;" value="${{escapeHtml(a.counselGuidance || '')}}">
            </label>
          </div>
        `).join('');
        agWrap.querySelectorAll('.law-ag-edit').forEach(inp => {{
          inp.addEventListener('change', () => {{
            const i = Number(inp.dataset.idx);
            matter.agenda[i].counselGuidance = inp.value.trim();
            matter.agenda[i].status = 'Aligned';
            updateActiveMatter(matter);
            renderStep5();
            renderHealthStrip();
          }});
        }});
      }}

      function renderAll() {{
        refreshMatterSelector();
        renderHealthStrip();
        renderStep1();
        renderStep2();
        renderStep3();
        renderStep4();
        renderStep5();
      }}
      renderAll();
    }})();
  </script>
</body>
</html>
"""


def render_courtroom_html(payload):
    """`view/courtroom.html` — High-Legibility Live Hearing Companion driven by the Active Matter."""
    payload_json = json.dumps(payload, ensure_ascii=False)
    commit_sha = html.escape(payload.get("commit", ""))
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light" data-stand-mode="true">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="prism-legal-commit" content="{commit_sha}">
  <title>Hearing Companion — PrismLegal Public-Benefit Legal Platform</title>
  <style>{_shared_css()}</style>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to Hearing Companion</a>
  {_shared_header_html("courtroom.html")}

  <main id="main-content" class="container" role="main">
    <!-- Active Matter Selector & Live Hearing Clock Bar -->
    <div class="matter-bar" aria-label="Active Matter &amp; Hearing Clock">
      <div class="matter-bar-left">
        <span class="badge stip">🏛️ Live Hearing Companion</span>
        <label style="font-size:0.86rem;font-weight:700;display:flex;align-items:center;gap:6px;">
          Active Matter:
          <select id="court-matter-select" class="btn" aria-label="Select Active Matter"></select>
        </label>
        <span id="court-matter-meta" style="font-size:0.84rem;color:var(--muted);"></span>
      </div>
      <div class="matter-bar-right">
        <select id="court-stage-sel" class="btn" aria-label="Active Hearing Stage">
          <option value="Stage 1: Opening Statement &amp; Relief Posture">Stage 1: Opening Statement &amp; Relief Posture</option>
          <option value="Stage 2: Case-in-Chief &amp; Direct Testimony" selected>Stage 2: Case-in-Chief &amp; Direct Testimony</option>
          <option value="Stage 3: Cross-Examination &amp; Redirect">Stage 3: Cross-Examination &amp; Redirect</option>
          <option value="Stage 4: Closing Arguments &amp; Final Orders">Stage 4: Closing Arguments &amp; Final Orders</option>
        </select>
        <div id="court-timer-readout" style="font-family:var(--mono);font-size:1.3rem;font-weight:800;padding:5px 12px;background:var(--surface-alt);border-radius:8px;border:2px solid var(--stipulated);">03:00:00</div>
        <button type="button" class="btn primary" id="btn-timer-toggle">▶ Start Clock</button>
        <button type="button" class="btn" id="btn-timer-reset">↺ Reset</button>
      </div>
    </div>

    <!-- High-Legibility 3-Tab Hearing Stepper -->
    <nav class="journey-stepper" aria-label="Hearing Companion Reference Modes" style="grid-template-columns:repeat(3,minmax(0,1fr));">
      <button type="button" class="step-tab" aria-selected="true" data-target="court-step-1">
        <span class="step-num">1</span>
        <span>
          <span class="step-title">Instant Cross-Exam Responder</span>
          <span class="step-sub">One-Click Calm Answers on the Stand</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="court-step-2">
        <span class="step-num">2</span>
        <span>
          <span class="step-title">Direct Testimony Checklist</span>
          <span class="step-sub">Question-by-Question Live Script</span>
        </span>
      </button>
      <button type="button" class="step-tab" aria-selected="false" data-target="court-step-3">
        <span class="step-num">3</span>
        <span>
          <span class="step-title">Exhibit Admission Tracker</span>
          <span class="step-sub">Live Offer &amp; Admissibility Status</span>
        </span>
      </button>
    </nav>

    <!-- Relief Goals Banner -->
    <section id="court-goals-strip" class="kpi-strip" aria-label="Requested Relief Summary"></section>

    <!-- TAB 1: INSTANT CROSS-EXAMINATION PIVOT RESPONDER -->
    <section id="court-step-1" class="workspace-section active">
      <div id="court-pedagogy-1"></div>
      <div class="card" style="border-left:6px solid var(--stipulated);">
        <span class="badge stip">Mode 1 · Instant Cross-Examination Responder</span>
        <h2 style="margin:4px 0 6px;">Select Any Topic for Your Immediate Calm Response &amp; Supporting Exhibit</h2>
        <div id="court-trap-buttons" style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px;"></div>
        <div id="court-trap-display"></div>
      </div>
    </section>

    <!-- TAB 2: DIRECT TESTIMONY LIVE CHECKLIST -->
    <section id="court-step-2" class="workspace-section">
      <div id="court-pedagogy-2"></div>
      <div class="card" style="border-left:6px solid var(--accent);">
        <span class="badge info">Mode 2 · Direct Testimony Live Script</span>
        <h2 style="margin:4px 0 6px;">Check Off Each Direct Examination Question as Covered</h2>
        <div class="search-bar" style="flex-wrap:wrap;gap:8px;">
          <label for="court-dx-search" style="font-weight:700;font-size:0.86rem;align-self:center;">Filter Direct Questions:</label>
          <input type="search" id="court-dx-search" class="search-input" aria-label="Search direct exam questions" style="flex:1;min-width:180px;">
          <div style="display:flex;flex-wrap:wrap;gap:6px;" role="group" aria-label="Quick Script Filters">
            <button type="button" class="btn primary court-dx-filter" data-filter="all">All Questions</button>
            <button type="button" class="btn court-dx-filter" data-filter="highlight">⭐ Key Highlights</button>
            <button type="button" class="btn court-dx-filter" data-filter="admit">📎 Exhibit Admissions</button>
            <button type="button" class="btn court-dx-filter" data-filter="active">Hide Stricken</button>
          </div>
        </div>
        <div id="court-dx-grid" class="grid-2"></div>
      </div>
    </section>

    <!-- TAB 3: LIVE EXHIBIT ADMISSION TRACKER -->
    <section id="court-step-3" class="workspace-section">
      <div id="court-pedagogy-3"></div>
      <div class="card" style="border-left:6px solid var(--stipulated);">
        <span class="badge stip">Mode 3 · Live Exhibit Admission Tracker</span>
        <h2 style="margin:4px 0 6px;">Track Offered &amp; Admitted Exhibits During the Hearing</h2>
        <div class="search-bar">
          <label for="court-ex-search" style="font-weight:700;font-size:0.86rem;align-self:center;">Filter Exhibits:</label>
          <input type="search" id="court-ex-search" class="search-input" aria-label="Filter exhibits">
        </div>
        <div id="court-ex-grid" class="grid-3"></div>
      </div>
    </section>
  </main>

  <footer class="site-footer" role="contentinfo">
    <strong>PrismLegal — High-Legibility Hearing Companion</strong> · Free Open-Source Legal Preparation Service · 100% Private Browser Storage
  </footer>

  <script id="case-model-data" type="application/json">{payload_json}</script>
  <script>
    (function() {{
      {_shared_js_helpers()}
      setupJourneyStepper();

      let matter = ensureActiveMatter();
      let activeTrapIdx = 0;
      let remainingSeconds = (Number(matter.hearingMinutes) || 180) * 60;
      let timerInterval = null;

      const matterSelect = document.getElementById('court-matter-select');
      const matterMeta = document.getElementById('court-matter-meta');
      const timerReadout = document.getElementById('court-timer-readout');
      const btnTimerToggle = document.getElementById('btn-timer-toggle');
      const btnTimerReset = document.getElementById('btn-timer-reset');

      function formatSeconds(sec) {{
        const h = Math.floor(sec / 3600);
        const m = Math.floor((sec % 3600) / 60);
        const s = sec % 60;
        return String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
      }}

      function refreshMatterSelector() {{
        matter = ensureActiveMatter();
        matterSelect.innerHTML = buildMatterSelectOptionsHtml(matter);
        matterMeta.textContent = `${{matter.forum || ''}} · ${{matter.docketNumber || ''}}`;
        remainingSeconds = (Number(matter.hearingMinutes) || 180) * 60;
        timerReadout.textContent = formatSeconds(remainingSeconds);
      }}

      matterSelect.addEventListener('change', () => {{
        setActiveMatterId(matterSelect.value);
        matter = ensureActiveMatter();
        activeTrapIdx = 0;
        renderAll();
      }});

      btnTimerToggle.addEventListener('click', () => {{
        if (timerInterval) {{
          clearInterval(timerInterval);
          timerInterval = null;
          btnTimerToggle.textContent = '▶ Resume Clock';
        }} else {{
          btnTimerToggle.textContent = '⏸ Pause Clock';
          timerInterval = setInterval(() => {{
            if (remainingSeconds > 0) remainingSeconds--;
            timerReadout.textContent = formatSeconds(remainingSeconds);
          }}, 1000);
        }}
      }});

      btnTimerReset.addEventListener('click', () => {{
        if (timerInterval) {{ clearInterval(timerInterval); timerInterval = null; }}
        remainingSeconds = (Number(matter.hearingMinutes) || 180) * 60;
        timerReadout.textContent = formatSeconds(remainingSeconds);
        btnTimerToggle.textContent = '▶ Start Clock';
      }});

      function renderGoalsStrip() {{
        const goals = matter.reliefGoals || [];
        const strip = document.getElementById('court-goals-strip');
        if (!goals.length) {{
          strip.innerHTML = '';
          return;
        }}
        strip.innerHTML = goals.map((g, idx) => `
          <div class="kpi-card stip">
            <div class="kpi-label">Relief Goal ${{idx + 1}} · ${{escapeHtml(g.title)}}</div>
            <div class="kpi-val" style="font-size:1rem;">${{escapeHtml(g.requestedOrder)}}</div>
            <div class="kpi-note">${{escapeHtml(g.rationale)}}</div>
          </div>
        `).join('');
      }}

      function renderResponder() {{
        const ped1 = document.getElementById('court-pedagogy-1');
        if (ped1) ped1.innerHTML = renderPedagogyBanner('court-step-1');

        const btnsWrap = document.getElementById('court-trap-buttons');
        const dispWrap = document.getElementById('court-trap-display');
        const traps = matter.traps || [];
        if (!traps.length) {{
          btnsWrap.innerHTML = '';
          dispWrap.innerHTML = `<div class="empty-state">No cross-examination topics added to this matter yet. Add tough questions in Client Step 3 or Attorney Step 3.</div>`;
          return;
        }}
        if (activeTrapIdx >= traps.length) activeTrapIdx = 0;
        btnsWrap.innerHTML = traps.map((t, idx) => `
          <button type="button" class="btn ${{idx === activeTrapIdx ? 'primary' : ''}}" data-idx="${{idx}}">${{escapeHtml(t.id)}}: ${{escapeHtml(t.title)}}</button>
        `).join('');
        btnsWrap.querySelectorAll('button').forEach(b => {{
          b.addEventListener('click', () => {{
            activeTrapIdx = Number(b.dataset.idx);
            renderResponder();
          }});
        }});
        const t = traps[activeTrapIdx];
        dispWrap.innerHTML = `
          <div class="card" style="margin-bottom:0;background:var(--surface-alt);border:2px solid var(--accent);">
            <div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;">
              <div><span class="badge info">${{escapeHtml(t.id)}}</span> <strong style="font-size:1.1rem;">${{escapeHtml(t.title)}}</strong></div>
              <div>${{t.exhibitId ? `<span class="exhibit-pill">${{escapeHtml(t.exhibitId)}}</span>` : ''}}</div>
            </div>
            <p style="font-size:1.02rem;margin:8px 0;"><strong>Hostile Question / Challenge:</strong> ${{escapeHtml(t.question)}}</p>
            <div class="trap-dont" style="margin-top:10px;"><strong>⛔ DO NOT FALL FOR THIS TRAP:</strong> ${{escapeHtml(t.avoid)}}</div>
            <div class="pivot-say" style="font-size:1.08rem;"><strong>✅ SAY THIS CALMLY ON THE STAND:</strong><br>"${{escapeHtml(t.response)}}"</div>
            ${{t.rule106Context ? `<div style="margin-top:8px;padding:8px 12px;border-radius:6px;background:rgba(3,105,161,0.08);border-left:3px solid var(--accent);font-size:0.9rem;"><strong>📜 Rule of Completeness (FRE 106) Full Context:</strong> ${{escapeHtml(t.rule106Context)}}</div>` : ''}}
          </div>
        `;
      }}

      const dxSearch = document.getElementById('court-dx-search');
      let activeDxFilter = 'all';
      document.querySelectorAll('.court-dx-filter').forEach(btn => {{
        btn.addEventListener('click', () => {{
          activeDxFilter = btn.getAttribute('data-filter') || 'all';
          document.querySelectorAll('.court-dx-filter').forEach(b => b.classList.toggle('primary', b === btn));
          renderCourtDx();
        }});
      }});

      function renderCourtDx() {{
        const ped2 = document.getElementById('court-pedagogy-2');
        if (ped2) ped2.innerHTML = renderPedagogyBanner('court-step-2');

        const grid = document.getElementById('court-dx-grid');
        const q = (dxSearch.value || '').toLowerCase().trim();
        const rows = (matter.directExam || []).filter(d => {{
          const cue = d.visualCue || 'standard';
          const isHighlight = cue === 'highlight' || cue === 'yellow-highlight';
          const isStrike = cue === 'strikethrough' || cue === 'red-strikethrough';
          if (q && !JSON.stringify(d).toLowerCase().includes(q)) return false;
          if (activeDxFilter === 'highlight' && !isHighlight) return false;
          if (activeDxFilter === 'admit' && !d.movesToAdmit) return false;
          if (activeDxFilter === 'active' && isStrike) return false;
          return true;
        }});
        if (!rows.length) {{
          grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">No direct examination questions match your filter.</div>`;
          return;
        }}
        grid.innerHTML = rows.map(d => {{
          const cue = d.visualCue || 'standard';
          const isHighlight = cue === 'highlight' || cue === 'yellow-highlight';
          const isStrike = cue === 'strikethrough' || cue === 'red-strikethrough';
          return `
          <article class="card" style="margin-bottom:0;padding:14px;border-left:5px solid ${{isHighlight ? 'var(--stipulated)' : isStrike ? 'var(--muted)' : 'var(--accent)'}};${{isStrike ? 'opacity:0.78;' : ''}}">
            <label style="display:flex;gap:10px;align-items:flex-start;cursor:pointer;">
              <input type="checkbox" style="margin-top:4px;width:18px;height:18px;">
              <div style="flex:1;">
                <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;">
                  <span class="badge info">${{escapeHtml(d.id)}}</span>
                  <span class="badge stip">${{escapeHtml(d.chapter || 'Direct Exam')}}</span>
                  ${{isHighlight ? `<span class="badge stip">⭐ Key Highlight</span>` : ''}}
                  ${{isStrike ? `<span class="badge warn">🚫 Skip Unless Opened</span>` : ''}}
                  ${{d.movesToAdmit ? `<span class="badge info">📎 Move to Admit</span>` : ''}}
                  ${{d.exhibitId ? `<span class="exhibit-pill">${{escapeHtml(d.exhibitId)}}</span>` : ''}}
                </div>
                <div style="font-weight:700;margin:6px 0 4px;${{isStrike ? 'text-decoration:line-through;' : ''}}">Q: ${{escapeHtml(d.question)}}</div>
                <div class="pivot-say" style="margin-top:4px;font-size:0.95rem;"><strong>✅ Say:</strong> "${{escapeHtml(d.answer)}}"</div>
                ${{d.coachingNote ? `<div style="margin-top:6px;font-size:0.84rem;color:var(--accent);"><strong>💡 Witness Cue:</strong> ${{escapeHtml(d.coachingNote)}}</div>` : ''}}
              </div>
            </label>
            ${{d.movesToAdmit && d.exhibitId ? `
              <div style="margin-top:8px;padding-top:8px;border-top:1px dashed var(--border);display:flex;justify-content:space-between;align-items:center;gap:8px;">
                <span style="font-size:0.8rem;color:var(--muted);"><strong>Evidentiary Offer:</strong> Authenticate &amp; offer <code>${{escapeHtml(d.exhibitId)}}</code></span>
                <button type="button" class="btn primary btn-court-admit-ex" data-ex="${{escapeHtml(d.exhibitId)}}" style="padding:3px 10px;font-size:0.78rem;">📎 Mark ${{escapeHtml(d.exhibitId)}} Admitted</button>
              </div>
            ` : ''}}
          </article>
          `;
        }}).join('');
        grid.querySelectorAll('.btn-court-admit-ex').forEach(btn => {{
          btn.addEventListener('click', () => {{
            const exRef = btn.getAttribute('data-ex') || '';
            const firstToken = exRef.split(',')[0].trim();
            (matter.exhibits || []).forEach(ex => {{
              if (ex.id === firstToken || ex.label === firstToken) {{
                ex.status = 'Admitted';
              }}
            }});
            updateActiveMatter(matter);
            btn.textContent = '✓ Admitted in Record';
            renderCourtExhibits();
          }});
        }});
      }}
      dxSearch.addEventListener('input', renderCourtDx);

      const exSearch = document.getElementById('court-ex-search');
      function renderCourtExhibits() {{
        const ped3 = document.getElementById('court-pedagogy-3');
        if (ped3) ped3.innerHTML = renderPedagogyBanner('court-step-3');
        const grid = document.getElementById('court-ex-grid');
        const q = (exSearch.value || '').toLowerCase().trim();
        const exs = (matter.exhibits || []).filter(e => !q || JSON.stringify(e).toLowerCase().includes(q));
        if (!exs.length) {{
          grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">No exhibits match your filter.</div>`;
          return;
        }}
        grid.innerHTML = exs.map((e, idx) => {{
          const vNotesStr = typeof e.visualNotes === 'string' ? e.visualNotes.trim() : '';
          const pIntentStr = typeof e.pivotIntent === 'string' ? e.pivotIntent.trim() : '';
          const vNotesArr = Array.isArray(e.visualNotes) ? e.visualNotes : [];
          const pIntentArr = Array.isArray(e.pivotIntent) ? e.pivotIntent : [];
          const hasForensics = Boolean(vNotesStr || pIntentStr || vNotesArr.length || pIntentArr.length);
          return `
          <article class="card" style="margin-bottom:0;padding:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">
              <div><span class="badge stip">${{escapeHtml(e.label || e.id)}}</span> <strong>${{escapeHtml(e.title)}}</strong></div>
              <select class="btn court-ex-status" data-idx="${{idx}}" style="padding:2px 6px;font-size:0.76rem;">
                <option value="Stipulated" ${{e.status === 'Stipulated' ? 'selected' : ''}}>Stipulated</option>
                <option value="Ready to Offer" ${{e.status === 'Ready to Offer' ? 'selected' : ''}}>Ready to Offer</option>
                <option value="Offered at Hearing" ${{e.status === 'Offered at Hearing' ? 'selected' : ''}}>Offered at Hearing</option>
                <option value="Admitted" ${{e.status === 'Admitted' ? 'selected' : ''}}>Admitted</option>
                <option value="Objected / Contested" ${{e.status === 'Objected / Contested' ? 'selected' : ''}}>Objected / Contested</option>
              </select>
            </div>
            <p style="font-size:0.86rem;margin:6px 0;"><strong>Proves:</strong> ${{escapeHtml(e.purpose)}}</p>
            ${{e.previewDataUrl ? `<div class="exhibit-thumb" style="margin:6px 0;"><img src="${{escapeHtml(e.previewDataUrl)}}" alt="${{escapeHtml(e.title)}}"><span style="font-size:0.75rem;color:var(--muted);">${{escapeHtml(e.exifSummary || e.modality || '')}}</span></div>` : ''}}
            <div style="font-size:0.78rem;color:var(--muted);"><strong>Foundation:</strong> <code>${{escapeHtml(e.foundation || 'FRE 901')}}</code></div>
            ${{hasForensics ? `
              <details style="margin-top:8px;padding:6px 8px;border-radius:6px;background:var(--surface-alt);border:1px solid var(--border);font-size:0.8rem;">
                <summary style="cursor:pointer;font-weight:700;color:var(--accent);">🔍 Page Callouts &amp; Trial Intent ▾</summary>
                ${{vNotesStr ? `<div style="margin-top:4px;"><strong>Visual Callout:</strong> ${{escapeHtml(vNotesStr)}}</div>` : ''}}
                ${{pIntentStr ? `<div style="margin-top:4px;color:var(--stipulated);"><strong>Trial Intent:</strong> ${{escapeHtml(pIntentStr)}}</div>` : ''}}
                ${{vNotesArr.map(vn => `<div style="margin-top:4px;">• <strong>[${{escapeHtml(vn.pageRef)}}]</strong> ${{escapeHtml(vn.observation)}} — <em>${{escapeHtml(vn.intent)}}</em></div>`).join('')}}
                ${{pIntentArr.map(pi => `<div style="margin-top:4px;color:var(--stipulated);">• <strong>Trial Intent (${{escapeHtml(pi.id)}}):</strong> ${{escapeHtml(pi.shows)}}</div>`).join('')}}
              </details>
            ` : ''}}
          </article>
          `;
        }}).join('');
        grid.querySelectorAll('.court-ex-status').forEach(sel => {{
          sel.addEventListener('change', () => {{
            matter.exhibits[Number(sel.dataset.idx)].status = sel.value;
            updateActiveMatter(matter);
          }});
        }});
      }}
      exSearch.addEventListener('input', renderCourtExhibits);

      function renderAll() {{
        refreshMatterSelector();
        renderGoalsStrip();
        renderResponder();
        renderCourtDx();
        renderCourtExhibits();
      }}
      renderAll();
    }})();
  </script>
</body>
</html>
"""


def sync_logo():
    LOGO_PATH.parent.mkdir(parents=True, exist_ok=True)
    svg = render_logo_svg()
    changed = not LOGO_PATH.exists() or LOGO_PATH.read_text() != svg
    if changed:
        LOGO_PATH.write_text(svg)
    return {"logo": str(LOGO_PATH.relative_to(ROOT)), "changed": changed}


def check_logo():
    if not LOGO_PATH.exists():
        return {"ok": False, "reason": "site/logo.svg is missing; run `bin/prism-legal api sync`"}
    ok = LOGO_PATH.read_text() == render_logo_svg()
    return {"ok": ok, "reason": None if ok else "site/logo.svg drifted; run `bin/prism-legal api sync`"}


def check_rendered_pages(out_dir=None):
    """Verify that all 4 portal pages exist, implement progressive-disclosure user journeys,
    never auto-seed saved matters, provide contextual step-by-step example drawers,
    contain zero non-production attributes, and contain zero leaked internal meta-taxonomy."""
    from . import sanitize
    out_dir = Path(out_dir) if out_dir else (ROOT / "view")
    pages = ["index.html", "client.html", "lawyer.html", "courtroom.html"]
    for p in pages:
        fp = out_dir / p
        if not fp.exists():
            return {"ok": False, "reason": f"view/{p} missing; run `bin/prism-legal view render`"}
        raw = fp.read_text()
        visible = re.sub(r'<script id="case-model-data".*?</script>', "", raw, flags=re.DOTALL)
        for term in presentationmodel.FORBIDDEN_META_TERMS:
            if term in visible:
                return {"ok": False, "reason": f"Forbidden meta-taxonomy term '{term}' leaked into visible UI of view/{p}"}
        for pterm in sanitize.forbidden_placeholder_terms():
            if pterm in raw.lower():
                return {"ok": False, "reason": f"Forbidden non-production token '{pterm}' found in view/{p}"}
        if "global-matter-select" not in visible or "brand-pill" not in visible:
            return {"ok": False, "reason": f"Production top bar (global-matter-select / brand-pill) missing in view/{p}"}
        if "renderStepExampleDrawer" not in visible:
            return {"ok": False, "reason": f"Contextual step-by-step example drawer helper missing in view/{p}"}
        if "extrapolateCaseFromIntake" not in visible or "classifyMatterIntake" not in visible:
            return {"ok": False, "reason": f"In-browser intake classifier & case extrapolation engine missing in view/{p}"}
        if "parseMultiModalFileInBrowser" not in visible or "ingestMultiModalUploadsIntoMatter" not in visible:
            return {"ok": False, "reason": f"In-browser multi-modal evidence intake parser & linker missing in view/{p}"}
        if "extractPdfStructureAndTextInBrowser" not in visible or "extractJpegExifMetadata" not in visible or "extractPngChunksMetadata" not in visible:
            return {"ok": False, "reason": f"Real binary PDF FlateDecode / JPEG EXIF / PNG chunk parsers missing in view/{p}"}
        if "renderCourtCaptionMastheadHtml" not in visible:
            return {"ok": False, "reason": f"Formal court caption masthead component missing in view/{p}"}
        for sim_tok in ("buildSampleMultiModalFiles", "sample-btn", "Load Sample Multi-Modal"):
            if sim_tok in raw:
                return {"ok": False, "reason": f"Simulated evidence upload token '{sim_tok}' found in view/{p}"}
        if "computeFilingDeadlines" not in visible or "generateFilingArtifact" not in visible:
            return {"ok": False, "reason": f"Procedural filing deadline calculator or court artifact generator missing in view/{p}"}
        if p in ("client.html", "lawyer.html", "courtroom.html"):
            if "journey-stepper" not in visible:
                return {"ok": False, "reason": f"Progressive-disclosure journey-stepper missing in view/{p}"}
            if "renderPedagogyBanner" not in visible:
                return {"ok": False, "reason": f"Pedagogical banner rendering missing in view/{p}"}
        if p in ("index.html", "client.html", "lawyer.html") and "action-drawer" not in visible:
            return {"ok": False, "reason": f"Progressive-disclosure action-drawer missing in view/{p}"}
        if "split('(')" in visible or 'split("(")' in visible:
            return {"ok": False, "reason": f"Ad-hoc label truncation split('(') found in view/{p}"}
    return {"ok": True, "reason": None}


def render_view(out_dir=None):
    out_dir = Path(out_dir) if out_dir else (ROOT / "view")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "sheets").mkdir(parents=True, exist_ok=True)

    payload = build_payload()
    written = []

    def write_artifact(rel_path, content):
        target = out_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        written.append(rel_path)

    write_artifact("logo.svg", render_logo_svg())
    write_artifact("parenting-schedule.svg", render_schedule_svg())
    write_artifact("remedies-waterfall.svg", render_support_svg())
    write_artifact("case-timeline.svg", render_timeline_svg())
    write_artifact("sheets/opening-strategy-compass.md", render_compass_md())
    write_artifact("sheets/client-strategy-and-testimony-guide.md", render_client_guide_md())
    write_artifact("sheets/lawyer-model-tuning-and-trial-brief.md", render_lawyer_tuner_md())
    write_artifact("sheets/statutory-best-interests-matrix.md", render_factors_md())
    write_artifact("sheets/guideline-remedies-and-disclosure-audit.md", render_remedies_md())
    write_artifact("sheets/cross-exam-pivot-cards.md", render_pivots_md())
    write_artifact("sheets/witness-examination-sheets.md", render_witnesses_md())
    write_artifact("sheets/counsel-direct-examination-script.md", render_direct_exam_md())
    write_artifact("sheets/visual-evidence-and-intent-matrix.md", render_visual_evidence_md())
    write_artifact("register.json", json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    write_artifact("tuning.json", json.dumps(tunemodel.load_state(), indent=2, ensure_ascii=False) + "\n")
    write_artifact("standards.json", json.dumps({"standards": standardsmodel.rows()}, indent=2, ensure_ascii=False) + "\n")
    write_artifact(".nojekyll", "")

    index_doc = render_index_html(payload)
    client_doc = render_client_html(payload)
    lawyer_doc = render_lawyer_html(payload)
    courtroom_doc = render_courtroom_html(payload)

    write_artifact("index.html", index_doc)
    write_artifact("client.html", client_doc)
    write_artifact("lawyer.html", lawyer_doc)
    write_artifact("courtroom.html", courtroom_doc)

    # Mirror into `site/` and `docs/` so GitHub Pages works out-of-the-box from `/docs` or `/view`
    for mirror in (ROOT / "site", ROOT / "docs"):
        mirror.mkdir(parents=True, exist_ok=True)
        (mirror / "sheets").mkdir(parents=True, exist_ok=True)
        for rel in written:
            src_f = out_dir / rel
            dst_f = mirror / rel
            dst_f.parent.mkdir(parents=True, exist_ok=True)
            dst_f.write_text(src_f.read_text())

    return {"out": str(out_dir), "written": written, "count": len(written)}
