"""`prism-legal`: Mechanized PrismPM / LexLean CLI for the Open-Source Public-Benefit Legal Platform."""

import argparse
import json
import sys
from pathlib import Path

from . import (
    ROOT,
    apimodel,
    archmodel,
    auditmodel,
    casemodel,
    checks,
    convertmodel,
    directexammodel,
    discover_rust,
    discoverymodel,
    engine_rust,
    enginemodel,
    intakemodel,
    legalmetamodel,
    lexicon,
    observermodel,
    portalmodel,
    presentationmodel,
    prismmodel,
    production,
    sanitize,
    sequencemodel,
    site,
    standardsmodel,
    supportmodel,
    tunemodel,
    visualmodel,
)


def out(args, data, text):
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(text)


def cmd_brief(args):
    meta = casemodel.CASE_META
    fl = casemodel.FINANCIAL_LEDGER
    lines = [
        f"=== PRISM-LEGAL REFERENCE BENCHMARK: CASE NO. {meta['caseNumber']} — {meta['hearingTitle'].upper()} ===",
        f"Court:      {meta['court']} (Division {meta['division']})",
        f"Hearing:    {meta['hearingTitle']} — {meta['hearingDate']} at {meta['hearingTime']}",
        f"Children:   " + ", ".join(f"{c['name']} (age {c['age']})" for c in casemodel.CHILDREN),
        "",
        "OPENING STATEMENT PILLARS:",
    ]
    for p in casemodel.OPENING_PILLARS:
        lines.append(f"  {p['id']} [{p['theme']}]: {p['title']}")
        lines.append(f"      Quote: \"{p['verbatimQuote']}\"")
    lines += [
        "",
        "DISPUTED ISSUES & RELIEF TARGETS:",
        f"  1. Parenting Time (Fam. Code § 103(1)(a)): Equal 50/50 2-2-5-5 schedule (182.5 overnights each, Ex. L) vs. Counterparty's 90 overnights.",
        f"  2. Decision-Making (Fam. Code § 103(2)): Joint Major Decisions with mediation first (Ex. L) vs. Counterparty's sole decision-making.",
        f"  3. Support & Remedies (Fam. Code § 204): Guideline Worksheet (Ex. N) on stipulated incomes ($8,000/mo Counterparty, $5,000/mo Client) -> Counterparty owes Client ${fl['fatherProposal']['netMonthlyTransfer']:.2f}/mo.",
    ]
    out(args, {"caseMeta": meta, "pillars": casemodel.OPENING_PILLARS, "financial": fl}, "\n".join(lines))


def cmd_claim(args):
    c = next((x for x in casemodel.CLAIMS if x["id"].lower() == args.id.lower()), None)
    if not c:
        print(f"PRISM1001: Unknown claim ID '{args.id}'", file=sys.stderr)
        sys.exit(1)
    dependents = [x["id"] for x in casemodel.CLAIMS if c["id"] in x["depends"]]
    data = {**c, "dependents": dependents}
    text = (
        f"{c['id']} [{c['status'].upper()}] ({c['category']} · {c['statutory']})\n"
        f"  Statement:  {c['statement']}\n"
        f"  Exhibits:   {', '.join(c['exhibits'])}\n"
        f"  Depends on: {', '.join(c['depends']) or 'none'}\n"
        f"  Supports:   {', '.join(dependents) or 'none'}"
    )
    out(args, data, text)


def cmd_exhibit(args):
    q = args.id.lower().replace(".", "").replace(" ", "-")
    all_ex = [{**e, "party": "respondent"} for e in casemodel.RESPONDENT_EXHIBITS] + [
        {**e, "party": "petitioner"} for e in casemodel.PETITIONER_EXHIBITS
    ]
    e = next(
        (
            x
            for x in all_ex
            if x["id"].lower() == args.id.lower()
            or x["id"].lower() == q
            or x["label"].lower() == args.id.lower()
        ),
        None,
    )
    if not e:
        print(f"PRISM1001: Unknown exhibit ID '{args.id}'", file=sys.stderr)
        sys.exit(1)
    if e["party"] == "respondent":
        text = f"{e['id']} ({e['label']}) — {e['title']}\n  Category: {e['category']} ({e['statutory']})\n  File:     {e['file']}\n  Purpose:  {e['purpose']}"
    else:
        text = f"{e['id']} ({e['label']}) — {e['title']}\n  Category:     {e['category']}\n  File:         {e['file']}\n  Opposing Use: {e['motherUse']}\n  Client Pivot: {e['fatherPivot']}"
    out(args, e, text)


def cmd_witness(args):
    w = next((x for x in casemodel.WITNESSES if x["id"].lower() == args.id.lower() or args.id.lower() in x["name"].lower()), None)
    if not w:
        print(f"PRISM1001: Unknown witness '{args.id}'", file=sys.stderr)
        sys.exit(1)
    text = (
        f"{w['id']}: {w['name']} ({w['relationship']}) [{w['callStatus']} · {w['party']}]\n"
        f"  Scope: {w['scope']}\n  Key Examination Points:\n"
        + "\n".join(f"    - {pt}" for pt in w["keyPoints"])
    )
    out(args, w, text)


def cmd_audit(args):
    rows = auditmodel.TRAPS
    if getattr(args, "status", None):
        rows = [t for t in rows if t["status"] == args.status]
    lines = [f"=== OPPOSING ALLEGATION & CROSS-EXAMINATION AUDIT ({len(rows)} Traps) ==="]
    for t in rows:
        lines += [
            f"\n{t['id']} [{t['status']}] — {t['title']} ({t['statutoryAnchor']})",
            f"  Allegation: {t['allegation']}",
            f"  Rebuttal:   {', '.join(t['rebuttalExhibits'])}",
            f"  WARNING:    {t['trapWarning']}",
            f"  PIVOT:      \"{t['openingAlignedPivot']}\"",
        ]
    out(args, {"traps": rows}, "\n".join(lines))


def cmd_tune(args):
    action = getattr(args, "action", None) or "status"
    if action == "reset":
        state = tunemodel.default_state()
        tunemodel.TUNING_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
        out(args, state, "Reset model/tuning.json to baseline Client-Lawyer tuning state.")
        return
    if action == "apply":
        if not getattr(args, "file", None):
            print("PRISM4001: `bin/prism-legal tune apply --file <patch.json>` requires --file", file=sys.stderr)
            sys.exit(1)
        state = tunemodel.apply_patch(Path(args.file))
        out(args, state, f"Applied Client-Lawyer tuning patch from {args.file} into model/tuning.json")
        return
    state = tunemodel.load_state()
    if action == "export":
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return
    lines = [
        f"=== CLIENT & LAWYER MODEL-TUNING WORKBENCH ({len(state['dimensions'])} Dimensions) ===",
    ]
    for d in state["dimensions"]:
        lines.append(f"  • {d['id']} [{d['owner']} ↔ {d['collaborator']}] ({d['targetModule']}): {d['title']}")
    lines.append(f"\n=== CLIENT-LAWYER STRATEGY CO-DESIGN AGENDA ({len(state['agenda'])} Items) ===")
    for item in state["agenda"]:
        lines += [
            f"  {item['id']} [{item['status']}] ({item['targetId']} · {item['category']}) — Raised by {item['author']}",
            f"    Question / Focus: {item['questionForLawyer']}",
            f"    Lawyer Guidance:  {item['lawyerGuidance']}",
        ]
    out(args, state, "\n".join(lines))


def cmd_meta(args):
    sec = getattr(args, "section", None) or "all"
    data = {
        "hohfeldRelations": legalmetamodel.HOHFELD_RELATIONS,
        "legalRules": legalmetamodel.LEGAL_RULES,
        "superiorityOverrides": legalmetamodel.SUPERIORITY_OVERRIDES,
        "arguments": legalmetamodel.ARGUMENTS,
        "attacks": legalmetamodel.ATTACKS,
        "aknDocuments": legalmetamodel.AKN_DOCUMENTS,
        "chainOfCustody": legalmetamodel.CHAIN_OF_CUSTODY,
    }
    lines = ["=== FORMAL LEGAL META-THEORY & INTERNATIONAL COMPLIANCE ENGINE (src/LegalMeta.lex.tex) ==="]
    if sec in ("all", "hohfeld"):
        lines.append(f"\n1. HOHFELDIAN FUNDAMENTAL LEGAL CONCEPTIONS ({len(legalmetamodel.HOHFELD_RELATIONS)} Jural Relations):")
        for r in legalmetamodel.HOHFELD_RELATIONS:
            lines.append(
                f"  • {r['id']} [{r['orderKind']}]: {r['dominantPosition']} <-> {r['correlativePosition']} (Opposite: {r['oppositePosition']}) — {r['title']} ({r['statutoryAuthority']})"
            )
    if sec in ("all", "rules"):
        lines.append(f"\n2. OASIS LEGALRULEML v1.0 DEFEASIBLE DEONTIC RULES ({len(legalmetamodel.LEGAL_RULES)} Rules, {len(legalmetamodel.SUPERIORITY_OVERRIDES)} Overrides):")
        for r in legalmetamodel.LEGAL_RULES:
            lines.append(f"  • {r['id']} [{r['strength']} · {r['deonticModality']}]: {r['statutorySource']} -> {r['consequent']}")
        for sup in legalmetamodel.SUPERIORITY_OVERRIDES:
            lines.append(f"  • {sup['id']}: {sup['superiorRuleId']} > {sup['inferiorRuleId']} ({sup['authority']}) — {sup['rationale']}")
    if sec in ("all", "arguments"):
        lines.append(f"\n3. DUNG (1995) / ASPIC+ STRUCTURED ARGUMENTATION ({len(legalmetamodel.ATTACKS)} Grounded Rebuttals):")
        for atk in legalmetamodel.ATTACKS:
            lines.append(
                f"  • {atk['id']}: {atk['attackerId']} {atk['attackKind']} {atk['targetId']} via {atk['statutoryBasis']} ({', '.join(atk['winningExhibits'])})"
            )
    if sec in ("all", "akn"):
        lines.append(f"\n4. OASIS AKOMA NTOSO v1.0 FRBR DOCUMENT MANIFEST ({len(legalmetamodel.AKN_DOCUMENTS)} Documents):")
        for d in legalmetamodel.AKN_DOCUMENTS:
            lines.append(f"  • {d['id']} [{d['docType']}]: {d['workUri']} — {d['title']}")
    if sec in ("all", "coc"):
        lines.append(f"\n5. ISO 15489-1:2016 & ISO/IEC 27037:2012 CHAIN OF CUSTODY ({len(legalmetamodel.CHAIN_OF_CUSTODY)} Records):")
        for c in legalmetamodel.CHAIN_OF_CUSTODY:
            lines.append(f"  • {c['id']} ({c['exhibitId']}): {c['iso15489Class']} — {c['creFoundation']}")
    out(args, data, "\n".join(lines))


def cmd_portal(args):
    action = getattr(args, "action", None) or "status"
    port = int(getattr(args, "port", 8780) or 8780)
    if action == "serve":
        import http.server
        import socketserver

        out_dir = ROOT / "view"
        if not (out_dir / "index.html").exists():
            site.render_view(out_dir)

        class PortalHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *h_args, **h_kwargs):
                super().__init__(*h_args, directory=str(out_dir), **h_kwargs)

            def log_message(self, fmt, *log_args):
                sys.stderr.write(f"[prism-legal-portal] {self.address_string()} - {fmt % log_args}\n")

        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("127.0.0.1", port), PortalHandler) as httpd:
            print(f"PrismLegal User Portal serving locally at http://127.0.0.1:{port}/ (root: {out_dir})", flush=True)
            httpd.serve_forever()
        return

    data = {
        "publicBenefitCharter": portalmodel.PUBLIC_BENEFIT_CHARTER,
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
    }
    lines = [
        "=== PRISM-LEGAL PRODUCTION PLATFORM & PUBLIC-BENEFIT PORTAL (src/Portal.lex.tex) ===",
        f"Public-Benefit Charter: {portalmodel.PUBLIC_BENEFIT_CHARTER['name']} ({portalmodel.PUBLIC_BENEFIT_CHARTER['license']})",
        f"Auth Providers ({len(portalmodel.AUTH_PROVIDERS)}): " + ", ".join(f"{a['id']} ({a['protocol']})" for a in portalmodel.AUTH_PROVIDERS),
        f"Share Grants ({len(portalmodel.SHARE_GRANTS)}):   " + ", ".join(f"{g['id']} ({g['scope']})" for g in portalmodel.SHARE_GRANTS),
        f"Firms/Clinics ({len(portalmodel.FIRMS)}):  " + ", ".join(f"{f['id']} ({f['name']})" for f in portalmodel.FIRMS),
        f"Courts ({len(portalmodel.COURTS)}):         " + ", ".join(f"{c['id']} ({c['name']})" for c in portalmodel.COURTS),
        f"Frameworks ({len(portalmodel.LEGAL_FRAMEWORKS)}):     " + ", ".join(f"{fw['id']} ({fw['domain']})" for fw in portalmodel.LEGAL_FRAMEWORKS),
        f"Clients ({len(portalmodel.CLIENTS)}):        " + ", ".join(f"{c['id']} ({c['name']})" for c in portalmodel.CLIENTS),
        f"Lawyers ({len(portalmodel.LAWYERS)}):        " + ", ".join(f"{l['id']} ({l['name']})" for l in portalmodel.LAWYERS),
        f"Cases ({len(portalmodel.CASES)}):          " + ", ".join(f"{k['id']} ({k['docketNumber']} · {k['domain']})" for k in portalmodel.CASES),
        "\nM:N ENGAGEMENTS (ABA Model Rules 1.2 & 1.16 — Zero Lawyer Lock-In):",
    ]
    for e in portalmodel.ENGAGEMENTS:
        lines.append(
            f"  • {e['id']}: {e['clientId']} <-> {e['caseId']} <-> {e['lawyerId']} [{e['role']}] (portableExitRight={e['portableExitRight']})"
        )
    lines.append("\nSTRICTLY SEPARATED PORTAL VIEWS (Client vs. Lawyer):")
    for v in portalmodel.PORTAL_VIEWS:
        lines.append(f"  • {v['id']} [{v['persona'].upper()} PORTAL ONLY]: {v['title']}")
    out(args, data, "\n".join(lines))


def cmd_convert(args):
    rows = convertmodel.compiled_fixtures()
    qid = getattr(args, "id", None)
    if qid:
        rows = [r for r in rows if r["id"].lower() == qid.lower()]
        if not rows:
            print(f"PRISM1001: Unknown proposition/refusal fixture '{qid}'", file=sys.stderr)
            sys.exit(1)
    lines = [
        f"=== COMPILED CONTROLLED-ENGLISH LEGAL PROPOSITION ENGINE (src/Convert.lex.tex · {len(rows)} Fixtures · Zero External LLM) ==="
    ]
    for r in rows:
        tag = "OK" if r["verdict"] == "statement" else "REFUSED"
        lines.append(f"  • {r['id']} [{tag}] (claim={r['claimId'] or 'refusal'}): {r['controlledEnglish']}")
    out(args, {"fixtures": rows, "lexiconPackage": "prism.legal@1.0.0", "externalLlm": False}, "\n".join(lines))


def cmd_engine(args):
    action = getattr(args, "action", None) or "status"
    committed = enginemodel.load_committed_table()
    schedules = [
        {"family": fam, "applicable": app, "ordered": enginemodel.Mirror.schedule(committed, fam, app)}
        for fam, app in enginemodel.FIXTURE_SCHEDULES
    ]
    rust_verified = None
    if action == "rust":
        rust_sched = engine_rust.schedule_batch(committed, enginemodel.FIXTURE_SCHEDULES)
        rust_learn = engine_rust.learn_batch(enginemodel.initial_table(), enginemodel.FIXTURE_OUTCOMES)
        rust_verified = {
            "schedulesMatchMirror": rust_sched == [s["ordered"] for s in schedules],
            "learnAllMatchesCommitted": rust_learn == committed,
            "binary": str(engine_rust.BIN.relative_to(ROOT)),
        }
    data = {
        "spec": "prism/engine/1",
        "bounds": {"wMin": enginemodel.W_MIN, "wMax": enginemodel.W_MAX, "wInit": enginemodel.W_INIT, "raise": enginemodel.RAISE, "lower": enginemodel.LOWER},
        "portfolio": enginemodel.PORTFOLIO,
        "families": enginemodel.FAMILIES,
        "stages": [{"phase": p, "budgetMinutes": b, "isGate": g} for p, b, g in enginemodel.WORKLOAD["stages"]],
        "tickLimitMinutes": enginemodel.WORKLOAD["tickBudget"],
        "timeoutMinutes": enginemodel.WORKLOAD["timeoutMinutes"],
        "committedWeights": [{"strategy": s, "family": f, "value": v} for s, f, v in committed],
        "schedules": schedules,
        "rust": rust_verified,
    }
    lines = [
        "=== COMPILED NEUROMORPHIC STRATEGY ENGINE & HOMEOSTATIC TRIAL CLOCK (src/Engine.lex.tex) ===",
        f"Plasticity Bounds: w in [{enginemodel.W_MIN}, {enginemodel.W_MAX}], w_init={enginemodel.W_INIT}, raise=+{enginemodel.RAISE}, lower=-{enginemodel.LOWER}",
        f"Homeostatic Trial Clock ({enginemodel.WORKLOAD['tickBudget']} min total / {enginemodel.WORKLOAD['timeoutMinutes']} min ceiling): "
        + ", ".join(f"{p}={b}m" for p, b, _ in enginemodel.WORKLOAD["stages"]),
        "\nWEIGHT-ORDERED STRATEGY SCHEDULES:",
    ]
    for s in schedules:
        lines.append(f"  • {s['family']}: {' > '.join(s['ordered'])}")
    if rust_verified:
        lines.append(
            f"\nCERTIFIED RUST ENGINE ({rust_verified['binary']}): schedulesMatch={rust_verified['schedulesMatchMirror']}, learnAllMatches={rust_verified['learnAllMatchesCommitted']}"
        )
    out(args, data, "\n".join(lines))


def cmd_discover(args):
    action = getattr(args, "action", None) or "status"
    seq_data = sequencemodel.load()
    fx = discoverymodel.fixtures(seq_data)
    rust_verified = None
    if action == "rust":
        idx, bases = discoverymodel.index_of(seq_data), discoverymodel.bases_of(seq_data)
        r_rels = discover_rust.find_relations(discoverymodel.FIXTURE_WIDTH, bases, fx["specs"])
        r_recs = discover_rust.find_recurrences([r["bits"] for r in fx["recurrences"]])
        rust_verified = {
            "relationsMatchMirror": r_rels == fx["relations"],
            "recurrencesMatchMirror": r_recs == [r["found"] for r in fx["recurrences"]],
            "binary": str(discover_rust.BIN.relative_to(ROOT)),
        }
    rel_descriptions = []
    for mask in fx["relations"]:
        cols = [discoverymodel.FIXTURE_COLUMNS[i] for i, bit in enumerate(mask) if bit]
        rel_descriptions.append({"mask": mask, "columns": cols, "xorEquation": " XOR ".join(cols) + " = 0"})
    data = {
        "window": seq_data["window"],
        "fixtureWidth": discoverymodel.FIXTURE_WIDTH,
        "sequences": seq_data["sequence"],
        "discoveredRelations": rel_descriptions,
        "registerClaimRelations": [
            {"claimId": cid, "columns": cols, "equation": " XOR ".join(cols) + " = 0"}
            for cid, cols in discoverymodel.REGISTER_CLAIM_RELATIONS
        ],
        "recurrences": [
            {"name": r["name"], "column": r["column"], "connectionPolynomial": r["found"], "expected": r["expected"]}
            for r in fx["recurrences"]
        ],
        "rust": rust_verified,
    }
    lines = [
        f"=== COMPILED EVIDENTIARY F_2 RELATION & RECURRENCE DISCOVERY ENGINE (src/Discovery.lex.tex · {len(seq_data['sequence'])} Sequences) ===",
        "\nDISCOVERED F_2 PARITY INVARIANTS (RelationSearch / Gaussian Elimination):",
    ]
    for r in rel_descriptions:
        lines.append(f"  • {r['xorEquation']}")
    lines.append("\nBERLEKAMP-MASSEY MINIMAL CONNECTION POLYNOMIALS (RecurrenceSearch):")
    for r in fx["recurrences"]:
        lines.append(f"  • {r['name']} ({r['column']}): c(D) = {r['found']} (degree {len(r['found']) - 1})")
    if rust_verified:
        lines.append(
            f"\nCERTIFIED RUST DISCOVERY ({rust_verified['binary']}): relationsMatch={rust_verified['relationsMatchMirror']}, recurrencesMatch={rust_verified['recurrencesMatchMirror']}"
        )
    out(args, data, "\n".join(lines))


def cmd_intake(args):
    action = getattr(args, "action", None) or "status"
    fixture_results = []
    for fx in intakemodel.INTAKE_FIXTURES:
        dom_cls = intakemodel.Mirror.eval_head(intakemodel.NODE_ATTENTION_HEADS[0], fx["features"])
        head_cls = intakemodel.Mirror.classify_all_heads(fx["features"])
        fixture_results.append(
            {
                **fx,
                "classifiedDomain": dom_cls,
                "headClassifications": head_cls,
                "matchesExpected": dom_cls == fx["expectedClass"],
            }
        )
    data = {
        "spec": "prism-legal/intake/1",
        "featureDim": intakemodel.FEATURE_DIM,
        "maxChannel": intakemodel.MAX_CHANNEL,
        "numDomainClasses": intakemodel.NUM_DOMAIN_CLASSES,
        "featureChannels": intakemodel.FEATURE_CHANNELS,
        "schemaClassifiers": intakemodel.SCHEMA_CLASSIFIERS,
        "attentionHeads": intakemodel.NODE_ATTENTION_HEADS,
        "fixtures": fixture_results,
    }
    lines = [
        f"=== COMPILED IN-BROWSER INTAKE CLASSIFIERS & PER-NODE ATTENTION HEADS (src/Intake.lex.tex · {len(intakemodel.SCHEMA_CLASSIFIERS)} Schema Classifiers · {len(intakemodel.NODE_ATTENTION_HEADS)} Node Heads) ===",
    ]
    if action in ("status", "schemas"):
        lines.append("\n1. SCHEMA ELEMENT CLASSIFIERS (Every Schema Element in the Model):")
        for sc in intakemodel.SCHEMA_CLASSIFIERS:
            lines.append(f"  • {sc['id']} ({sc['schemaElement']} -> {sc['headId']}): {sc['title']}")
    if action in ("status", "heads"):
        lines.append("\n2. PER-NODE ATTENTION HEADS (Every Node in the Model):")
        for h in intakemodel.NODE_ATTENTION_HEADS:
            lines.append(
                f"  • {h['id']} [{h['nodeId']} -> {h['schemaId']}]: inductive=\"{h['inductiveRelation']}\" · deductive=\"{h['deductiveStrategy']}\""
            )
    if action in ("status", "fixtures"):
        lines.append("\n3. VERIFIED INTAKE CLASSIFICATION FIXTURES:")
        for r in fixture_results:
            lines.append(
                f"  • {r['name']} ({r['domainId']}): class={r['classifiedDomain']} (expected={r['expectedClass']}) · all18Heads={r['headClassifications']}"
            )
    out(args, data, "\n".join(lines))


def cmd_exam(args):
    flt = (getattr(args, "filter", None) or "all").lower()
    chapters = directexammodel.DIRECT_EXAM_CHAPTERS
    qs = directexammodel.DIRECT_EXAM_QUESTIONS
    if flt == "highlights":
        qs = [q for q in qs if q["visualCue"] == "yellow-highlight"]
    elif flt == "admissions":
        qs = [q for q in qs if q["movesToAdmit"]]
    elif flt == "stricken":
        qs = [q for q in qs if q["visualCue"] == "red-strikethrough"]
    elif flt != "all":
        qs = [
            q
            for q in qs
            if q["id"].lower() == flt
            or q["chapterId"].lower() == flt
            or q["exhibitId"].lower() == flt
        ]
    lines = [
        f"=== LEAD TRIAL COUNSEL'S INTENDED DIRECT EXAMINATION OF RESPONDENT (src/DirectExam.lex.tex · {len(chapters)} Chapters · {len(qs)} Questions Shown) ==="
    ]
    for q in qs:
        cue = f" [{q['visualCue'].upper()}]" if q["visualCue"] != "standard" else ""
        adm = f" [MOVE TO ADMIT {q['exhibitId']}]" if q["movesToAdmit"] else ""
        lines += [
            f"\n{q['id']} (p. {q['page']} · {q['chapterId']} · {q['pillarId']} · {q['statutoryId']} · {q['exhibitId']}){cue}{adm}",
            f"  Q (Lead Trial Counsel): {q['question']}",
            f"  Script Prompt:  {q['counselPrompt']}",
            f"  Full Answer:    \"{q['fullTestimony']}\"",
            f"  Coaching Note:  {q['coachingNote']}",
        ]
    out(args, {"chapters": chapters, "questions": qs}, "\n".join(lines))


def cmd_visual(args):
    sec = (getattr(args, "section", None) or "all").lower()
    data = {
        "diaryEntries": visualmodel.HANDWRITTEN_DIARY_ENTRIES,
        "visualForensics": visualmodel.VISUAL_FORENSIC_RECORDS,
        "photoPages": visualmodel.PHOTO_PAGE_CATALOG,
        "semanticMappings": visualmodel.EXHIBIT_SEMANTIC_MAPPINGS,
    }
    lines = [
        "=== HANDWRITTEN, VISUAL & 30-EXHIBIT CONTENT-MEANING / INTENT REGISTER (src/VisualEvidence.lex.tex) ==="
    ]
    if sec in ("all", "forensics"):
        lines.append(f"\n1. VISUAL & SCANNED EXHIBIT FORENSIC EXTRACTIONS ({len(visualmodel.VISUAL_FORENSIC_RECORDS)} Records):")
        for v in visualmodel.VISUAL_FORENSIC_RECORDS:
            lines.append(f"  • {v['id']} ({v['exhibitId']} · {v['modality']} · {v['pageCount']} pp.): {v['handwrittenDetails']}")
            lines.append(f"    Trial Pivot: {v['trialPivot']}")
    if sec in ("all", "diary"):
        lines.append(f"\n2. OP EX. 13 HANDWRITTEN DIARY FRE 106 COMPLETENESS ({len(visualmodel.HANDWRITTEN_DIARY_ENTRIES)} Entries):")
        for d in visualmodel.HANDWRITTEN_DIARY_ENTRIES:
            lines.append(f"  • {d['id']} ({d['entryDate']} · {d['pageRange']}): \"{d['handwrittenExcerpt']}\"")
            lines.append(f"    FRE 106 Rebuttal: {d['fullContextRebuttal']}")
    if sec in ("all", "photos"):
        lines.append(f"\n3. PHOTOGRAPHIC PAGE CATALOG ({len(visualmodel.PHOTO_PAGE_CATALOG)} Photos across Ex. I & Ex. O):")
        for p in visualmodel.PHOTO_PAGE_CATALOG:
            lines.append(f"  • {p['id']} ({p['exhibitId']} p. {p['pageNumber']} — {p['subjects']} @ {p['setting']}): {p['visualDescription']}")
    if sec in ("all", "mappings"):
        lines.append(f"\n4. 30-EXHIBIT CONTENT-MEANING & INTENT MATRIX ({len(visualmodel.EXHIBIT_SEMANTIC_MAPPINGS)} Exhibits):")
        for m in visualmodel.EXHIBIT_SEMANTIC_MAPPINGS:
            lines.append(f"  • {m['id']} ({m['exhibitId']} · {m['proponent']} · {m['modality']}): {m['contextualMeaning']}")
    out(args, data, "\n".join(lines))


def cmd_sanitize(args):
    res = sanitize.check()
    text = (
        f"Zero-PII & Case-Sanitization Audit: PASS ({res['scannedFiles']} files scanned, 0 private case tokens, 0 raw PDF/audio attachments)"
        if res["ok"]
        else f"Zero-PII & Case-Sanitization Audit FAILED: {res['reason']}"
    )
    out(args, res, text)
    if not res["ok"]:
        sys.exit(1)


def cmd_api(args):
    if args.sub == "production":
        res = production.build(verify=False)
        text = (
            "LexLean production Rust emission: PASS (.lexlean/production/rust-core & .lexlean/production/rust-std)"
            if res["ok"]
            else f"LexLean production build FAILED: {json.dumps(res)}"
        )
        out(args, res, text)
        if not res["ok"]:
            sys.exit(1)
        return
    if args.sub == "sync":
        lx = lexicon.sync_domain_lexicon()
        t = tunemodel.sync()
        a = apimodel.sync()
        r = casemodel.sync()
        c = supportmodel.sync()
        h = archmodel.sync()
        u = auditmodel.sync()
        cv = convertmodel.sync()
        dx = directexammodel.sync()
        ve = visualmodel.sync()
        en = enginemodel.sync()
        sq = sequencemodel.sync()
        ds = discoverymodel.sync()
        ik = intakemodel.sync()
        lm = legalmetamodel.sync()
        pt = portalmodel.sync()
        p = presentationmodel.sync()
        o = observermodel.sync()
        s = standardsmodel.sync()
        pr = production.sync()
        m = prismmodel.sync()
        g = site.sync_logo()
        pages = site.render_view()
        locked = checks.lock()
        data = {
            "lexicon": lx,
            "tuning": t,
            "api": a,
            "register": r,
            "support": c,
            "architecture": h,
            "audit": u,
            "convert": cv,
            "directExam": dx,
            "visualEvidence": ve,
            "engine": en,
            "sequences": sq,
            "discovery": ds,
            "intake": ik,
            "legalMeta": lm,
            "portal": pt,
            "presentation": p,
            "observer": o,
            "standards": s,
            "production": pr,
            "model": m,
            "logo": g,
            "pages": pages,
            "locked": locked,
        }
        state = lambda x: " (rewritten)" if x["changed"] else " (current)"
        text = "\n".join(
            [
                f"language/{lx['package']}: {lx['entries']} domain lexicon entries{state(lx)}",
                f"{t['file']}: {t['dimensions']} tuning dimensions{state(t)}",
                f"{a['module']}: {a['commands']} commands{state(a)}",
                f"{r['module']}: {r['claims']} claims, {r['exhibits']} exhibits, {r['witnesses']} witnesses, {r['factors']} statutory factors, {r['timeline']} timeline events{state(r)}",
                f"{c['module']}: {c['worksheets']} support worksheets, {c['taxYears']} tax years{state(c)}",
                f"{h['module']}: {h['stakeholders']} stakeholders, {h['concerns']} concerns, {h['viewpoints']} viewpoints, {h['risks']} risks, {h['tuningParameters']} tuning params{state(h)}",
                f"{u['module']}: {u['traps']} cross-exam traps{state(u)}",
                f"{cv['module']}: {cv['fixtures']} controlled-English proposition & refusal fixtures{state(cv)}",
                f"{dx['module']}: {dx['chapters']} direct-exam chapters, {dx['questions']} direct-exam Q&A blocks{state(dx)}",
                f"{ve['module']}: {ve['diaryEntries']} diary entries, {ve['visualForensics']} visual forensics, {ve['photos']} photos, {ve['semanticMappings']} exhibit semantic/intent mappings{state(ve)}",
                f"{en['module']}: {en['strategies']} strategies, {en['families']} statutory families, {en['weights']} synaptic weights{state(en)}",
                f"{sq['module']}: {sq['sequences']} evidentiary bit-vector sequences{state(sq)}",
                f"{ds['module']}: {ds['relations']} F_2 claim relations & Berlekamp-Massey recurrences{state(ds)}",
                f"{ik['module']}: {ik['schemaClassifiers']} schema classifiers, {ik['attentionHeads']} node attention heads{state(ik)}",
                f"{lm['module']}: {lm['hohfeld']} Hohfeld relations, {lm['rules']} LegalRuleML rules, {lm['attacks']} ASPIC+ attacks, {lm['akn']} Akoma Ntoso URIs, {lm['coc']} chain-of-custody records{state(lm)}",
                f"{pt['module']}: {pt['shareGrants']} share grants, {pt['firms']} firms, {pt['courts']} courts, {pt['frameworks']} frameworks, {pt['clients']} clients, {pt['lawyers']} lawyers, {pt['cases']} cases, {pt['engagements']} M:N engagements{state(pt)}",
                f"{p['module']} & {p['application']}: {p['panels']} panels, {p['journeys']} journeys, {p['artifacts']} artifacts, {p['tokens']} design tokens{state(p)}",
                f"{o['module']}: {o['quadruples']} observer quadruples{state(o)}",
                f"{s['module']}: {s['standards']} legal & technical standards{state(s)}",
                f"{pr['request']}: certified Rust production request{state(pr)}",
                f"{m['model']}: {m['registers']} registers, schemas & suites{state(m)}",
                f"{g['logo']}{state(g)}",
                f"view/ + site/ + docs/: {pages['count']} artifacts rendered across view/, site/, and docs/",
            ]
        )
        out(args, data, text)
        if not locked["ok"]:
            print("PRISM3001: lexlean lock failed:\n" + locked["output"], file=sys.stderr)
            sys.exit(1)
    else:
        results = {
            "sanitization": sanitize.check(),
            "tuning": tunemodel.check(),
            "api": apimodel.check(),
            "register": casemodel.check(),
            "support": supportmodel.check(),
            "architecture": archmodel.check(),
            "audit": auditmodel.check(),
            "convert": convertmodel.check(),
            "directExam": directexammodel.check(),
            "visualEvidence": visualmodel.check(),
            "engine": enginemodel.check(),
            "sequences": sequencemodel.check(),
            "discovery": discoverymodel.check(),
            "intake": intakemodel.check(),
            "legalMeta": legalmetamodel.check(),
            "portal": portalmodel.check(),
            "presentation": presentationmodel.check(),
            "observer": observermodel.check(),
            "standards": standardsmodel.check(),
            "production": production.check(),
            "model": prismmodel.check(),
            "logo": site.check_logo(),
            "pages": site.check_rendered_pages(),
        }
        ok = all(v["ok"] for v in results.values())
        text = "\n".join(f"{k}: {'OK' if v['ok'] else v['reason']}" for k, v in results.items())
        out(args, results, text)
        if not ok:
            sys.exit(1)


def cmd_check(args):
    res = checks.check()
    text = "LexLean static check: PASS" if res["ok"] else ("LexLean check FAILED:\n" + "\n".join(res["diagnostics"]))
    out(args, res, text)
    if not res["ok"]:
        sys.exit(1)


def cmd_verify(args):
    res = checks.verify()
    text = (
        f"Lean 4 Kernel Verification: PASS (attestation: {res.get('attestation') or 'verified'})"
        if res["ok"]
        else ("Lean 4 Kernel Verification FAILED:\n" + "\n".join(res["diagnostics"]))
    )
    out(args, res, text)
    if not res["ok"]:
        sys.exit(1)


def cmd_view(args):
    out_dir = Path(args.out) if getattr(args, "out", None) else (ROOT / "view")
    res = site.render_view(out_dir)
    out(args, res, f"{res['out']}: generated {res['count']} mechanized portal & GitHub Pages artifacts across view/, site/, and docs/")


def build_parser():
    p = argparse.ArgumentParser(prog="prism-legal", description="PrismLegal Open-Source Public-Benefit Legal Platform CLI")
    p.add_argument("--json", action="store_true", help="Emit JSON output")
    sub = p.add_subparsers(dest="cmd", required=True)

    s_brief = sub.add_parser("brief", help="Print courtroom trial brief for reference benchmark")
    s_brief.set_defaults(func=cmd_brief)

    s_claim = sub.add_parser("claim", help="Inspect a case claim (CLM-01 to CLM-24)")
    s_claim.add_argument("id")
    s_claim.set_defaults(func=cmd_claim)

    s_ex = sub.add_parser("exhibit", help="Inspect an exhibit (Ex-A to Ex-O or OP-Ex-01 to OP-Ex-15)")
    s_ex.add_argument("id")
    s_ex.set_defaults(func=cmd_exhibit)

    s_wit = sub.add_parser("witness", help="Inspect a witness (W-01 to W-10)")
    s_wit.add_argument("id")
    s_wit.set_defaults(func=cmd_witness)

    s_aud = sub.add_parser("audit", help="Inspect opposing allegations and cross-exam pivots")
    s_aud.add_argument("--status", default=None)
    s_aud.set_defaults(func=cmd_audit)

    s_tune = sub.add_parser("tune", help="Inspect, export, or apply Lawyer & Client model-tuning patches")
    s_tune.add_argument("action", nargs="?", default="status", choices=["status", "export", "apply", "reset"])
    s_tune.add_argument("--file", default=None, help="Path to tuning patch JSON file for `apply`")
    s_tune.set_defaults(func=cmd_tune)

    s_meta = sub.add_parser("meta", help="Inspect formal Legal Meta-Theory & International Standards (Hohfeld, LegalRuleML, ASPIC+, Akoma Ntoso, ISO 15489/27037)")
    s_meta.add_argument("section", nargs="?", default="all", choices=["all", "hohfeld", "rules", "arguments", "akn", "coc"])
    s_meta.set_defaults(func=cmd_meta)

    s_portal = sub.add_parser("portal", help="Inspect or serve the Multi-Client, Multi-Case, Multi-Lawyer User Portal")
    s_portal.add_argument("action", nargs="?", default="status", choices=["status", "serve"])
    s_portal.add_argument("--port", type=int, default=8780, help="Local port for `portal serve` (default: 8780)")
    s_portal.set_defaults(func=cmd_portal)

    s_conv = sub.add_parser("convert", help="Compile formal legal propositions into controlled English (src/Convert.lex.tex)")
    s_conv.add_argument("id", nargs="?", default=None, help="Optional fixture ID (e.g. PROP-01 or REF-13)")
    s_conv.set_defaults(func=cmd_convert)

    s_eng = sub.add_parser("engine", help="Run compiled neuromorphic strategy engine & homeostatic trial clock (src/Engine.lex.tex)")
    s_eng.add_argument("action", nargs="?", default="status", choices=["status", "schedule", "learn", "rust"])
    s_eng.set_defaults(func=cmd_engine)

    s_disc = sub.add_parser("discover", help="Run compiled F_2 relation & Berlekamp-Massey recurrence discovery engine (src/Discovery.lex.tex)")
    s_disc.add_argument("action", nargs="?", default="status", choices=["status", "relations", "recurrences", "rust"])
    s_disc.set_defaults(func=cmd_discover)

    s_intk = sub.add_parser("intake", help="Run compiled in-browser intake classifiers & per-node attention heads (src/Intake.lex.tex)")
    s_intk.add_argument("action", nargs="?", default="status", choices=["status", "heads", "schemas", "fixtures"])
    s_intk.set_defaults(func=cmd_intake)

    s_exam = sub.add_parser("exam", help="Inspect Lead Counsel's Intended Direct Examination of Client (src/DirectExam.lex.tex)")
    s_exam.add_argument("filter", nargs="?", default="all", help="all | highlights | admissions | stricken | <DX-ID or CH-ID>")
    s_exam.set_defaults(func=cmd_exam)

    s_vis = sub.add_parser("visual", help="Inspect handwritten diary, visual forensics, photos & 30-exhibit Content-Meaning/Intent Matrix (src/VisualEvidence.lex.tex)")
    s_vis.add_argument("section", nargs="?", default="all", choices=["all", "mappings", "diary", "forensics", "photos"])
    s_vis.set_defaults(func=cmd_visual)

    s_san = sub.add_parser("sanitize", help="Verify zero private case tokens or raw attachments in repository")
    s_san.set_defaults(func=cmd_sanitize)

    s_api = sub.add_parser("api", help="Sync, check, or emit production Rust packages for all LexLean modules")
    api_sub = s_api.add_subparsers(dest="sub", required=True)
    api_sync = api_sub.add_parser("sync")
    api_sync.set_defaults(func=cmd_api)
    api_chk = api_sub.add_parser("check")
    api_chk.set_defaults(func=cmd_api)
    api_prod = api_sub.add_parser("production")
    api_prod.set_defaults(func=cmd_api)

    s_chk = sub.add_parser("check", help="Run lexlean check and sanitization audit on all modules")
    s_chk.set_defaults(func=cmd_check)

    s_ver = sub.add_parser("verify", help="Run full Lean 4 kernel verification (lexlean verify)")
    s_ver.set_defaults(func=cmd_verify)

    s_view = sub.add_parser("view", help="Render browser interface and GitHub Pages bundle (view/, site/, docs/)")
    view_sub = s_view.add_subparsers(dest="sub", required=True)
    v_render = view_sub.add_parser("render")
    v_render.add_argument("--out", default=str(ROOT / "view"))
    v_render.set_defaults(func=cmd_view)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
