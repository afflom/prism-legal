Feature: PrismLegal User-Centered Service Design & Five-Pole Journey Conformance
  Every portal page enforces progressive disclosure within its cognitive-load budget, separates Client and Attorney workspaces, and walks the five poles (orientation, substance, challenge, proof, resolution) without meta-taxonomy or technical jargon leakage.

  @journey-client-preparation @SH-CLIENT
  Scenario: journey-client-preparation (SH-CLIENT)
    Given the user-centered journey "journey-client-preparation" in "src/Presentation.lex.tex"
    When stakeholder "SH-CLIENT" progresses across poles orientation, substance, challenge, proof, resolution
    Then all 5 steps (client-step-1, client-step-2, client-step-3, client-step-4, client-step-5) resolve to verified workspace panels and artifacts

  @journey-counsel-workbench @SH-LAWYER
  Scenario: journey-counsel-workbench (SH-LAWYER)
    Given the user-centered journey "journey-counsel-workbench" in "src/Presentation.lex.tex"
    When stakeholder "SH-LAWYER" progresses across poles orientation, substance, challenge, proof, resolution
    Then all 5 steps (counsel-step-1, counsel-step-2, counsel-step-3, counsel-step-4, counsel-step-5) resolve to verified workspace panels and artifacts

  @journey-court-bench @SH-COURT
  Scenario: journey-court-bench (SH-COURT)
    Given the user-centered journey "journey-court-bench" in "src/Presentation.lex.tex"
    When stakeholder "SH-COURT" progresses across poles orientation, substance, challenge, proof, resolution
    Then all 5 steps (court-step-1, court-step-2, court-step-3, court-step-4, court-step-5) resolve to verified workspace panels and artifacts

  @journey-beneficiaries-stability @SH-BENEFICIARIES
  Scenario: journey-beneficiaries-stability (SH-BENEFICIARIES)
    Given the user-centered journey "journey-beneficiaries-stability" in "src/Presentation.lex.tex"
    When stakeholder "SH-BENEFICIARIES" progresses across poles orientation, substance, challenge, proof, resolution
    Then all 5 steps (beneficiaries-step-1, beneficiaries-step-2, beneficiaries-step-3, beneficiaries-step-4, beneficiaries-step-5) resolve to verified workspace panels and artifacts

  @journey-counterparty-protocol @SH-COUNTERPARTY
  Scenario: journey-counterparty-protocol (SH-COUNTERPARTY)
    Given the user-centered journey "journey-counterparty-protocol" in "src/Presentation.lex.tex"
    When stakeholder "SH-COUNTERPARTY" progresses across poles orientation, substance, challenge, proof, resolution
    Then all 5 steps (counterparty-step-1, counterparty-step-2, counterparty-step-3, counterparty-step-4, counterparty-step-5) resolve to verified workspace panels and artifacts

  @ped-client-1 @client-step-1
  Scenario: ped-client-1 — Why Courts Ask for Specific Relief Orders First
    Given the contextual pedagogy guide "ped-client-1" for step "client-step-1" in "src/Presentation.lex.tex"
    When a user views pole "orientation" in panel "panel-strategy"
    Then contextual legal guidance grounded in standard "uniform-dom-402" is presented without walls of text

  @ped-client-2 @client-step-2
  Scenario: ped-client-2 — How a Chronological Timeline & Linked Exhibits Build Credibility
    Given the contextual pedagogy guide "ped-client-2" for step "client-step-2" in "src/Presentation.lex.tex"
    When a user views pole "substance" in panel "panel-parenting"
    Then contextual legal guidance grounded in standard "fre-evidence" is presented without walls of text

  @ped-client-3 @client-step-3
  Scenario: ped-client-3 — How to Handle Hostile Questions & Out-of-Context Quotes Calmly
    Given the contextual pedagogy guide "ped-client-3" for step "client-step-3" in "src/Presentation.lex.tex"
    When a user views pole "challenge" in panel "panel-cross-exam"
    Then contextual legal guidance grounded in standard "dung-aspic-arg" is presented without walls of text

  @ped-client-4 @client-step-4
  Scenario: ped-client-4 — How Direct Examination Establishes Your Case-in-Chief
    Given the contextual pedagogy guide "ped-client-4" for step "client-step-4" in "src/Presentation.lex.tex"
    When a user views pole "proof" in panel "panel-evidence"
    Then contextual legal guidance grounded in standard "fre-evidence" is presented without walls of text

  @ped-client-5 @client-step-5
  Scenario: ped-client-5 — How to Review Case Consistency & Share with Counsel
    Given the contextual pedagogy guide "ped-client-5" for step "client-step-5" in "src/Presentation.lex.tex"
    When a user views pole "resolution" in panel "panel-lawyer-tuner"
    Then contextual legal guidance grounded in standard "aba-rpc-webauthn-sharing" is presented without walls of text

  @ped-counsel-1 @counsel-step-1
  Scenario: ped-counsel-1 — Scoping the Engagement, Forum & Theory of the Case
    Given the contextual pedagogy guide "ped-counsel-1" for step "counsel-step-1" in "src/Presentation.lex.tex"
    When a user views pole "orientation" in panel "panel-hub"
    Then contextual legal guidance grounded in standard "aba-rpc-webauthn-sharing" is presented without walls of text

  @ped-counsel-2 @counsel-step-2
  Scenario: ped-counsel-2 — Mapping Statutory Elements, Proposed Findings & Rule Exceptions
    Given the contextual pedagogy guide "ped-counsel-2" for step "counsel-step-2" in "src/Presentation.lex.tex"
    When a user views pole "substance" in panel "panel-parenting"
    Then contextual legal guidance grounded in standard "oasis-legalruleml-1.0" is presented without walls of text

  @ped-counsel-3 @counsel-step-3
  Scenario: ped-counsel-3 — Homeostatic Hearing Clock Budgeting & Examination Scripting
    Given the contextual pedagogy guide "ped-counsel-3" for step "counsel-step-3" in "src/Presentation.lex.tex"
    When a user views pole "challenge" in panel "panel-cross-exam"
    Then contextual legal guidance grounded in standard "fre-evidence" is presented without walls of text

  @ped-counsel-4 @counsel-step-4
  Scenario: ped-counsel-4 — Auditing Admissibility Foundations, Chain of Custody & Guideline Math
    Given the contextual pedagogy guide "ped-counsel-4" for step "counsel-step-4" in "src/Presentation.lex.tex"
    When a user views pole "proof" in panel "panel-financial"
    Then contextual legal guidance grounded in standard "iso-15489-27037" is presented without walls of text

  @ped-counsel-5 @counsel-step-5
  Scenario: ped-counsel-5 — Consistency Audit, Priority Ranking & Trial Brief Handoff
    Given the contextual pedagogy guide "ped-counsel-5" for step "counsel-step-5" in "src/Presentation.lex.tex"
    When a user views pole "resolution" in panel "panel-lawyer-tuner"
    Then contextual legal guidance grounded in standard "hohfeld-1913" is presented without walls of text

  @ped-court-1 @court-step-1
  Scenario: ped-court-1 — Live Witness Stand & Counsel Table Cross-Exam Responder
    Given the contextual pedagogy guide "ped-court-1" for step "court-step-1" in "src/Presentation.lex.tex"
    When a user views pole "orientation" in panel "panel-cross-exam"
    Then contextual legal guidance grounded in standard "dung-aspic-arg" is presented without walls of text

  @ped-court-2 @court-step-2
  Scenario: ped-court-2 — Live Direct Examination Checklist & Foundation Pacing
    Given the contextual pedagogy guide "ped-court-2" for step "court-step-2" in "src/Presentation.lex.tex"
    When a user views pole "substance" in panel "panel-evidence"
    Then contextual legal guidance grounded in standard "fre-evidence" is presented without walls of text

  @ped-court-3 @court-step-3
  Scenario: ped-court-3 — Live Exhibit Offer & Admission Status Tracker
    Given the contextual pedagogy guide "ped-court-3" for step "court-step-3" in "src/Presentation.lex.tex"
    When a user views pole "proof" in panel "panel-evidence"
    Then contextual legal guidance grounded in standard "iso-15489-27037" is presented without walls of text
