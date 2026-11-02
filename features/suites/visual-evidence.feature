Feature: PrismLegal Handwritten, Visual & 30-Exhibit Content-Meaning / Intent Conformance
  Every handwritten journal entry, visual/scanned exhibit forensic extraction, photo page, and all 30 trial exhibits carry verified content meaning and proponent intent.

  @VIS-01 @Ex-A
  Scenario: VIS-01 (Ex-A · Digital Transit Telemetry Map · 4 pp.)
    Given visual forensic record "VIS-01" in "src/VisualEvidence.lex.tex"
    When exhibit "Ex-A" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-02 @Ex-E
  Scenario: VIS-02 (Ex-E · Official Retirement Board Decision · 8 pp.)
    Given visual forensic record "VIS-02" in "src/VisualEvidence.lex.tex"
    When exhibit "Ex-E" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-03 @Ex-G
  Scenario: VIS-03 (Ex-G · Sworn Financial Statement (Initial) · 7 pp.)
    Given visual forensic record "VIS-03" in "src/VisualEvidence.lex.tex"
    When exhibit "Ex-G" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-04 @Ex-H
  Scenario: VIS-04 (Ex-H · Subpoenaed Bank Statements · 18 pp.)
    Given visual forensic record "VIS-04" in "src/VisualEvidence.lex.tex"
    When exhibit "Ex-H" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-05 @Ex-I
  Scenario: VIS-05 (Ex-I · Photographic Compendium · 11 pp.)
    Given visual forensic record "VIS-05" in "src/VisualEvidence.lex.tex"
    When exhibit "Ex-I" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-06 @Ex-K
  Scenario: VIS-06 (Ex-K · Multimedia & Activity Stills · 9 pp.)
    Given visual forensic record "VIS-06" in "src/VisualEvidence.lex.tex"
    When exhibit "Ex-K" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-07 @Ex-M
  Scenario: VIS-07 (Ex-M · Signed Completion Certificate · 1 pp.)
    Given visual forensic record "VIS-07" in "src/VisualEvidence.lex.tex"
    When exhibit "Ex-M" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-08 @Ex-N
  Scenario: VIS-08 (Ex-N · Signed Court Order & Guideline Worksheet · 12 pp.)
    Given visual forensic record "VIS-08" in "src/VisualEvidence.lex.tex"
    When exhibit "Ex-N" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-09 @OP-Ex-04
  Scenario: VIS-09 (OP-Ex-04 · Commercial Childcare Quote · 5 pp.)
    Given visual forensic record "VIS-09" in "src/VisualEvidence.lex.tex"
    When exhibit "OP-Ex-04" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-10 @OP-Ex-11
  Scenario: VIS-10 (OP-Ex-11 · Handwritten Calendar Annotations · 3 pp.)
    Given visual forensic record "VIS-10" in "src/VisualEvidence.lex.tex"
    When exhibit "OP-Ex-11" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-11 @OP-Ex-13
  Scenario: VIS-11 (OP-Ex-13 · Scanned Homework Study Log (2028-2029) · 21 pp.)
    Given visual forensic record "VIS-11" in "src/VisualEvidence.lex.tex"
    When exhibit "OP-Ex-13" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register

  @VIS-12 @OP-Ex-14
  Scenario: VIS-12 (OP-Ex-14 · Youth Device Message Screenshots · 6 pp.)
    Given visual forensic record "VIS-12" in "src/VisualEvidence.lex.tex"
    When exhibit "OP-Ex-14" is examined under "FRE 106 & Uniform Best-Interests Standard § 402"
    Then its handwritten/visual details and trial pivot are verified in the register
