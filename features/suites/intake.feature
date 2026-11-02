Feature: PrismLegal In-Browser Intake Classifiers & Per-Node Attention Extrapolation Conformance
  Every schema element in the model has a verified classifier and every node is an attention head whose inductive and deductive outputs extrapolate the completion of a legal matter in the browser without leaking internal meta-jargon.

  @schema-case-meta @HEAD-01
  Scenario: schema-case-meta — Case Front Matter & Jurisdiction Classifier
    Given the schema classifier "schema-case-meta" for schema element "caseMeta" in "src/Intake.lex.tex"
    When node attention head "HEAD-01" scores an 8-channel intake feature vector
    Then it classifies into DOM-FAM-103, DOM-HOU-URLTA, DOM-VET-38CFR and extrapolates the matter completion

  @schema-relief-goal @HEAD-02
  Scenario: schema-relief-goal — Relief Goals & Requested Judicial Orders Classifier
    Given the schema classifier "schema-relief-goal" for schema element "reliefGoals" in "src/Intake.lex.tex"
    When node attention head "HEAD-02" scores an 8-channel intake feature vector
    Then it classifies into relief-parenting-and-guideline-support, relief-habitability-repairs-and-abatement, relief-schedular-tdiu-and-effective-date and extrapolates the matter completion

  @schema-timeline-event @HEAD-03
  Scenario: schema-timeline-event — Chronological Event & Fact Intake Classifier
    Given the schema classifier "schema-timeline-event" for schema element "timeline" in "src/Intake.lex.tex"
    When node attention head "HEAD-03" scores an 8-channel intake feature vector
    Then it classifies into event-caregiving-and-schedule-compliance, event-repair-notice-and-escrow-deposit, event-claim-filing-and-medical-opinion and extrapolates the matter completion

  @schema-exhibit @HEAD-04
  Scenario: schema-exhibit — Documentary & Visual Evidence Intake Classifier
    Given the schema classifier "schema-exhibit" for schema element "exhibits" in "src/Intake.lex.tex"
    When node attention head "HEAD-04" scores an 8-channel intake feature vector
    Then it classifies into fre-901-authenticated-log, fre-803-6-business-record, fre-801d2-opposing-admission and extrapolates the matter completion

  @schema-claim @HEAD-05
  Scenario: schema-claim — Statutory Propositions & Proof Matrix Classifier
    Given the schema classifier "schema-claim" for schema element "claims" in "src/Intake.lex.tex"
    When node attention head "HEAD-05" scores an 8-channel intake feature vector
    Then it classifies into claim-best-interests-allocation, claim-warranty-habitability-breach, claim-tdiu-service-connection and extrapolates the matter completion

  @schema-witness @HEAD-06
  Scenario: schema-witness — Witness Roster & Examination Scope Classifier
    Given the schema classifier "schema-witness" for schema element "witnesses" in "src/Intake.lex.tex"
    When node attention head "HEAD-06" scores an 8-channel intake feature vector
    Then it classifies into witness-coparent-and-corroborator, witness-tenant-and-code-inspector, witness-claimant-and-medical-examiner and extrapolates the matter completion

  @schema-trap @HEAD-07
  Scenario: schema-trap — Cross-Examination Trap & FRE 106 Rebuttal Classifier
    Given the schema classifier "schema-trap" for schema element "traps" in "src/Intake.lex.tex"
    When node attention head "HEAD-07" scores an 8-channel intake feature vector
    Then it classifies into documentary-impeachment, statutory-factor-deduction, stipulated-anchor-lock and extrapolates the matter completion

  @schema-direct-exam @HEAD-08
  Scenario: schema-direct-exam — Direct Examination Q&A Script Classifier
    Given the schema classifier "schema-direct-exam" for schema element "directExam" in "src/Intake.lex.tex"
    When node attention head "HEAD-08" scores an 8-channel intake feature vector
    Then it classifies into dx-parenting-and-financial-walkthrough, dx-habitability-notice-and-escrow, dx-service-history-and-functional-limits and extrapolates the matter completion

  @schema-visual-forensics @HEAD-09
  Scenario: schema-visual-forensics — Visual Evidence Callout & Proponent Intent Classifier
    Given the schema classifier "schema-visual-forensics" for schema element "visualForensics" in "src/Intake.lex.tex"
    When node attention head "HEAD-09" scores an 8-channel intake feature vector
    Then it classifies into vis-schedule-log-and-notebook-completeness, vis-inspection-citation-and-escrow-receipts, vis-rating-code-sheet-and-nexus-opinion and extrapolates the matter completion

  @schema-calculator @HEAD-10
  Scenario: schema-calculator — Statutory & Financial Remedy Calculator Classifier
    Given the schema classifier "schema-calculator" for schema element "calculators" in "src/Intake.lex.tex"
    When node attention head "HEAD-10" scores an 8-channel intake feature vector
    Then it classifies into calc-family-305-shared-support, calc-housing-urlta-rent-abatement, calc-veterans-38cfr-combined-rating and extrapolates the matter completion

  @schema-hearing-stage @HEAD-11
  Scenario: schema-hearing-stage — Homeostatic Hearing Clock Stage Classifier
    Given the schema classifier "schema-hearing-stage" for schema element "hearingStages" in "src/Intake.lex.tex"
    When node attention head "HEAD-11" scores an 8-channel intake feature vector
    Then it classifies into clock-evidentiary-Custody-hearing, clock-housing-abatement-hearing, clock-administrative-review-hearing and extrapolates the matter completion

  @schema-agenda @HEAD-12
  Scenario: schema-agenda — Client–Counsel Strategy Co-Design Agenda Classifier
    Given the schema classifier "schema-agenda" for schema element "agenda" in "src/Intake.lex.tex"
    When node attention head "HEAD-12" scores an 8-channel intake feature vector
    Then it classifies into agenda-stipulations-and-disclosure-audit, agenda-escrow-release-and-inspection, agenda-effective-date-and-nexus and extrapolates the matter completion

  @schema-multimodal-upload @HEAD-19
  Scenario: schema-multimodal-upload — Multi-Modal Evidence Upload Parser & Case Linker Classifier
    Given the schema classifier "schema-multimodal-upload" for schema element "multimodalUploads" in "src/Intake.lex.tex"
    When node attention head "HEAD-19" scores an 8-channel intake feature vector
    Then it classifies into modality-pleading-or-court-order, modality-financial-ledger-or-tax-csv, modality-visual-photo-or-premises-media and extrapolates the matter completion

  @schema-jural-posture @HEAD-20
  Scenario: schema-jural-posture — Enforceable Legal Right, Duty, Power & Immunity Classifier
    Given the schema classifier "schema-jural-posture" for schema element "juralPosture" in "src/Intake.lex.tex"
    When node attention head "HEAD-20" scores an 8-channel intake feature vector
    Then it classifies into jural-enforceable-claim-right-and-duty, jural-joint-governance-authority, jural-statutory-benefit-immunity and extrapolates the matter completion

  @schema-filing-artifact @HEAD-21
  Scenario: schema-filing-artifact — Court-Ready Filing Packet & Pleading Generator Classifier
    Given the schema classifier "schema-filing-artifact" for schema element "filingArtifacts" in "src/Intake.lex.tex"
    When node attention head "HEAD-21" scores an 8-channel intake feature vector
    Then it classifies into filing-parenting-and-support-position-statement, filing-habitability-abatement-and-escrow-motion, filing-veterans-tdiu-and-nexus-brief and extrapolates the matter completion

  @schema-filing-deadline @HEAD-22
  Scenario: schema-filing-deadline — Procedural Timeline & On-Time Filing Schedule Classifier
    Given the schema classifier "schema-filing-deadline" for schema element "filingDeadlines" in "src/Intake.lex.tex"
    When node attention head "HEAD-22" scores an 8-channel intake feature vector
    Then it classifies into deadline-mandatory-financial-and-exhibit-disclosures, deadline-municipal-inspection-and-escrow-notice, deadline-administrative-record-and-medical-submission and extrapolates the matter completion
