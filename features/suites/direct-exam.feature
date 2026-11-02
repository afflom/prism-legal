Feature: PrismLegal Lead Counsel Intended Direct Examination Conformance
  Every question in Lead Counsel's Direct Examination script resolves to a chapter, Opening Statement pillar, statutory factor, and exhibit with a full Opening-aligned witness answer.

  @CH-01 @OS-1
  Scenario: CH-01 — Chapter 1: Beneficiaries, Household History & 10-Year Public Service Career (pp. 1-3)
    Given Lead Counsel's Direct Examination script in "src/DirectExam.lex.tex"
    When chapter "CH-01" is conducted under "SF-01"
    Then it advances Opening Statement pillar "OS-1" and admits foundational testimony

  @CH-02 @OS-2
  Scenario: CH-02 — Chapter 2: Equal Caregiving (2020-2027), Sabbatical Solo Care & 2027 Medical Leave (pp. 3-5)
    Given Lead Counsel's Direct Examination script in "src/DirectExam.lex.tex"
    When chapter "CH-02" is conducted under "SF-07"
    Then it advances Opening Statement pillar "OS-2" and admits Ex-C, Ex-E

  @CH-03 @OS-3
  Scenario: CH-03 — Chapter 3: Disability Retirement, Zero-Revenue Civic Writing & 2026-2029 Tax Records (pp. 5-8)
    Given Lead Counsel's Direct Examination script in "src/DirectExam.lex.tex"
    When chapter "CH-03" is conducted under "SF-10"
    Then it advances Opening Statement pillar "OS-3" and admits Ex-B, Ex-D, Ex-F, Ex-H

  @CH-04 @OS-4
  Scenario: CH-04 — Chapter 4: 2029 De-Escalation Videos, Transit Telemetry & Stipulated Dismissal (pp. 8-11)
    Given Lead Counsel's Direct Examination script in "src/DirectExam.lex.tex"
    When chapter "CH-04" is conducted under "SF-09"
    Then it advances Opening Statement pillar "OS-4" and admits Ex-A, Ex-J, Ex-K

  @CH-05 @OS-3
  Scenario: CH-05 — Chapter 5: Townhouse Environment, 90-Day 50/50 Execution & Photo Walkthrough (pp. 11-14)
    Given Lead Counsel's Direct Examination script in "src/DirectExam.lex.tex"
    When chapter "CH-05" is conducted under "SF-04"
    Then it advances Opening Statement pillar "OS-3" and admits Ex-I

  @CH-06 @OS-5
  Scenario: CH-06 — Chapter 6: Early Seminar Completion (Ex. M), 50/50 Plan (Ex. L) & Guideline Support (Ex. N) (pp. 14-17)
    Given Lead Counsel's Direct Examination script in "src/DirectExam.lex.tex"
    When chapter "CH-06" is conducted under "SF-10"
    Then it advances Opening Statement pillar "OS-5" and admits Ex-L, Ex-M, Ex-N, Ex-O
