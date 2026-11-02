Feature: PrismLegal Evidentiary Register Conformance
  Every stipulated, corroborated, and contested claim in the reference matter is backed by exhibits and statutory authority.

  @CLM-01 @corroborated
  Scenario: CLM-01 (parenting-time)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-01" is inspected under "Uniform Domestic Relations Act § 402(a)(1)–(11)"
    Then its status is "corroborated" and its exhibits Ex-B, Ex-K, Ex-L, Ex-O resolve in the register

  @CLM-02 @corroborated
  Scenario: CLM-02 (parenting-time)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-02" is inspected under "Uniform Domestic Relations Act § 402(a)(3), (7)"
    Then its status is "corroborated" and its exhibits Ex-B, Ex-K, Ex-O resolve in the register

  @CLM-03 @corroborated
  Scenario: CLM-03 (parenting-time)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-03" is inspected under "Uniform Domestic Relations Act § 402(a)(4)"
    Then its status is "corroborated" and its exhibits Ex-B, Ex-K, Ex-L resolve in the register

  @CLM-04 @stipulated
  Scenario: CLM-04 (parenting-time)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-04" is inspected under "Uniform Domestic Relations Act § 402(a)(4), (8)"
    Then its status is "stipulated" and its exhibits Ex-L, Ex-O resolve in the register

  @CLM-05 @corroborated
  Scenario: CLM-05 (decision-making)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-05" is inspected under "Uniform Domestic Relations Act § 402(b)(1)–(3)"
    Then its status is "corroborated" and its exhibits Ex-A, Ex-B, Ex-D, Ex-L resolve in the register

  @CLM-06 @corroborated
  Scenario: CLM-06 (decision-making)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-06" is inspected under "Uniform Domestic Relations Act § 402(a)(6), (9)"
    Then its status is "corroborated" and its exhibits Ex-D resolve in the register

  @CLM-07 @stipulated
  Scenario: CLM-07 (child-support)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-07" is inspected under "Uniform Support Guidelines § 305(2)"
    Then its status is "stipulated" and its exhibits Ex-E, Ex-I, Ex-N resolve in the register

  @CLM-08 @corroborated
  Scenario: CLM-08 (child-support)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-08" is inspected under "Uniform Support Guidelines § 305(8)"
    Then its status is "corroborated" and its exhibits Ex-E, Ex-N resolve in the register

  @CLM-09 @corroborated
  Scenario: CLM-09 (child-support)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-09" is inspected under "Uniform Support Guidelines § 305(5)(b)"
    Then its status is "corroborated" and its exhibits Ex-E, Ex-I, Ex-N resolve in the register

  @CLM-10 @corroborated
  Scenario: CLM-10 (child-support)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-10" is inspected under "Uniform Support Guidelines § 305(3) & FRE 803(8)"
    Then its status is "corroborated" and its exhibits Ex-I, Ex-N resolve in the register

  @CLM-11 @corroborated
  Scenario: CLM-11 (child-support)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-11" is inspected under "38 U.S.C. § 1781 & Support Guidelines § 305(9)"
    Then its status is "corroborated" and its exhibits Ex-E, Ex-N, OP-Ex-02 resolve in the register

  @CLM-12 @corroborated
  Scenario: CLM-12 (child-support)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-12" is inspected under "Uniform Support Guidelines § 305(9)(a) & § 402(a)(9)"
    Then its status is "corroborated" and its exhibits Ex-E, Ex-L, Ex-N, OP-Ex-02, OP-Ex-08 resolve in the register

  @CLM-13 @corroborated
  Scenario: CLM-13 (financial-disclosure)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-13" is inspected under "FRCP 26(e) & Civil Rule 16.2(e)(10)"
    Then its status is "corroborated" and its exhibits Ex-G, Ex-H, Ex-J, Ex-N resolve in the register

  @CLM-14 @corroborated
  Scenario: CLM-14 (financial-disclosure)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-14" is inspected under "Civil Rule 16.2(e)(10)"
    Then its status is "corroborated" and its exhibits Ex-G, Ex-H, Ex-J, Ex-N, OP-Ex-11 resolve in the register

  @CLM-15 @corroborated
  Scenario: CLM-15 (impeachment)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-15" is inspected under "FRE 106 (Rule of Completeness)"
    Then its status is "corroborated" and its exhibits Ex-D, OP-Ex-13 resolve in the register

  @CLM-16 @corroborated
  Scenario: CLM-16 (impeachment)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-16" is inspected under "FRE 106 & Uniform Act § 402(a)(2), (6)"
    Then its status is "corroborated" and its exhibits Ex-A, Ex-B, OP-Ex-05, OP-Ex-14 resolve in the register

  @CLM-17 @corroborated
  Scenario: CLM-17 (impeachment)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-17" is inspected under "FRE 602 & FRE 802"
    Then its status is "corroborated" and its exhibits Ex-B, Ex-K, Ex-O resolve in the register

  @CLM-18 @corroborated
  Scenario: CLM-18 (protection-order)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-18" is inspected under "FRE 901(b)(9) & Uniform Act § 402(a)(9)"
    Then its status is "corroborated" and its exhibits Ex-F, Ex-L, Ex-M, OP-Ex-06, OP-Ex-07 resolve in the register

  @CLM-19 @stipulated
  Scenario: CLM-19 (protection-order)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-19" is inspected under "Doctrine of Issue Preclusion & Stipulation (Ex. C)"
    Then its status is "stipulated" and its exhibits Ex-C, Ex-F, Ex-L resolve in the register

  @CLM-20 @corroborated
  Scenario: CLM-20 (parenting-time)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-20" is inspected under "Uniform Domestic Relations Act § 402(a)(3), (9)"
    Then its status is "corroborated" and its exhibits Ex-B, Ex-L, OP-Ex-03 resolve in the register

  @CLM-21 @corroborated
  Scenario: CLM-21 (parenting-time)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-21" is inspected under "Uniform Domestic Relations Act § 402(a)(4)"
    Then its status is "corroborated" and its exhibits Ex-K, Ex-L, Ex-O resolve in the register

  @CLM-22 @corroborated
  Scenario: CLM-22 (financial-disclosure)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-22" is inspected under "Uniform Marital Property & Equitable Offset Principles"
    Then its status is "corroborated" and its exhibits Ex-G, Ex-H, Ex-J, Ex-N resolve in the register

  @CLM-23 @corroborated
  Scenario: CLM-23 (decision-making)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-23" is inspected under "Uniform Domestic Relations Act § 408"
    Then its status is "corroborated" and its exhibits Ex-B, Ex-K, Ex-L resolve in the register

  @CLM-24 @contested
  Scenario: CLM-24 (parenting-time)
    Given the verified case register in "src/Register.lex.tex"
    When claim "CLM-24" is inspected under "Uniform Domestic Relations Act § 402(a)(1)–(11)"
    Then its status is "contested" and its exhibits Ex-B, Ex-F, Ex-K, Ex-L, Ex-O, OP-Ex-01 resolve in the register
