# PrismLegal — Open-Source Public-Benefit Legal Platform

**Repository:** `https://github.com/afflom/prism-legal` · **Live GitHub Pages Deployment:** `https://afflom.github.io/prism-legal/`

**PrismLegal (`prism-legal`)** is a free, open-source, local-first legal preparation and trial engineering service built with **PrismPM v0.4.0** and verified in the **Lean 4** kernel via **LexLean v0.4.0** with certified **Rust** inference and rule-discovery crates.

It empowers **clients, self-represented (*pro se*) litigants, legal aid clinics, solo practitioners, and trial counsel** to organize timelines, ingest multi-modal evidence (PDFs, images, spreadsheets, correspondence), build exhibit-backed statutory proof matrices, rehearse testimony, generate court filing artifacts, and run live hearings across 6 legal practice domains—100% locally in the browser (`localStorage`) with portable `.prismlegal.json` and Markdown Trial Brief exports.

---

## GitHub Actions Pages Deployment & Continuous Verification

PrismLegal is configured for **GitHub Actions deployment to GitHub Pages** (`src/Application.lex.tex` → `GitHubPagesPublication`):

- **[`.github/workflows/pages.yml`](.github/workflows/pages.yml)** — Runs `./bin/prism-legal check` and `./bin/prism-legal view render --out view`, packages `./view` via `actions/upload-pages-artifact@v3`, deploys to GitHub Pages via `actions/deploy-pages@v4`, and runs a live post-deploy verification job confirming HTTP 200 across `index.html`, `client.html`, `lawyer.html`, `courtroom.html`, and `register.json` as well as verifying that the deployed `register.json` embeds `"commit": "$GITHUB_SHA"`.
- **[`.github/workflows/ci.yml`](.github/workflows/ci.yml)** — Runs the full static, schema, sanitization, and Lean 4 kernel verification gate on every push and pull request.

---

## Real Client-Side Multi-Modal Evidence Intake & 22-Head Neuromorphic Inference

All evidence parsing, cryptographic hashing, and legal extrapolation run **100% client-side in the browser** with zero server uploads and zero simulated features:

- **Binary PDF Parsing & FlateDecode Stream Decompression (`extractPdfStructureAndTextInBrowser`)**: Inspects `%PDF-1.x` headers, page counts (`/Type /Page`), `/Info` and XMP metadata, and decompresses `/FlateDecode` streams via the browser's native `DecompressionStream('deflate')` / `'deflate-raw'` API to extract `BT ... ET` (`Tj` / `TJ`) text operators, dates, dollar figures, and statutory citations.
- **Image Forensics, EXIF Extraction & Visual Thumbnails (`extractPngChunksMetadata`, `extractJpegExifMetadata`, `renderImagePreviewThumbnail`)**: Parses PNG `IHDR` dimensions/bit-depth, `pHYs` DPI, and `tEXt`/`iTXt` embedded OCR text; parses JPEG `SOF0`/`SOF2` dimensions and `APP1` EXIF TIFF IFD tags (`CameraMake`, `CameraModel`, `DateTimeOriginal`, `ImageDescription`, `UserComment`); and renders visual thumbnail previews via HTML5 `<canvas>` alongside WebCrypto **SHA-256** chain-of-custody digests.
- **Office, Tabular & Correspondence Parsing**: Decompresses ZIP-based XML containers (`.docx`, `.xlsx`, `.odt`) in-browser, strips `.rtf` control words, parses `.eml` RFC-822 headers (`From`, `To`, `Subject`, `Date`), and computes numeric column sums on `.csv`/`.tsv` financial ledgers.
- **22-Head Neuromorphic Attention & Legal Meta-Theory (`IntakeClassifier.lex.tex`)**: Following the discrete cellular-automata and neuromorphic classifier pattern of `afflom/rule30`, 22 schema-element attention heads with 8-token n-gram feature hashing (`D = 64`), Rule-30 chaotic reservoir mixing, and integer ReLU scoring classify intake text and uploaded evidence across Hohfeldian jural relations, Toulmin argumentation warrants, Wigmorean evidentiary inference chains, FRE admissibility foundations (`FRE 901`, `FRE 803(6)`, `FRE 106`, `FRE 1006`), statutory calculators, and procedural filing deadlines—emitting **zero defaults** when intake is blank.

---

## Progressive-Disclosure User Journeys & Live Browser Portal

The complete client-side User Portal is statically generated into `view/`, `site/`, and `docs/`:

- **[`view/index.html`](view/index.html)** — **Service Home & Matter Launcher**: Unified production header with instant active-matter switching (`#global-matter-select`), Guided Case Intake Assistant with real multi-modal evidence dropzone, role-based onboarding for Clients and Attorneys, **"My Saved Legal Matters"** workspace (`localStorage` + `.prismlegal.json` import/export—starting clean with 0 pre-saved matters until the user explicitly creates, edits, or imports a matter), and **Reference Example Matters** across all 6 legal domains (`👁️ Preview Example` or `📋 Save a Copy`).
- **[`view/client.html`](view/client.html)** — **5-Step Guided Client Journey** (each step includes a contextual **`📘 See Example From a Sample Case: How to Complete This Step ▾`** pedagogical drawer):
  1. **Step 1 (Case Summary & Relief Goals)**: Formal pleading caption masthead, multi-modal evidence dropzone, and concrete court orders requested.
  2. **Step 2 (Chronological Timeline & Exhibits)**: Date-anchored timeline and exhibit register with visual thumbnails, **Visual Details, Page Callouts & Trial Intent** (`VisualEvidence.lex.tex`), and local WebCrypto **SHA-256** document integrity verification.
  3. **Step 3 (Cross-Examination Preparation)**: Practice calm, exhibit-backed responses to anticipated hostile questions with **FRE 106 Rule of Completeness** context.
  4. **Step 4 (Direct Testimony Rehearsal)**: Rehearse chapter-by-chapter direct examination Q&As (`DirectExam.lex.tex`) with **⭐ Key Highlight** cues, **🚫 Skip Unless Opened on Cross** warnings, and **📎 Move to Admit** prompts.
  5. **Step 5 (Filing Deadlines, Court Artifacts & Export)**: Compute rules-based filing deadlines, generate court-ready markdown artifacts (Declaration, Exhibit Index, Pre-Hearing Statement, Proposed Order), log questions for counsel, and export a `.prismlegal.json` package.
- **[`view/lawyer.html`](view/lawyer.html)** — **5-Step Attorney Case Workbench**:
  1. **Step 1 (Intake & Case Theory)**: Formal court caption masthead, representation scope (Full-Scope, Limited-Scope / Unbundled per ABA Model Rule 1.2(c), Legal Aid Clinic, or Pro Se Coaching), and multi-modal discovery intake.
  2. **Step 2 (Statutory Proof Matrix & Refusal Guard)**: Map every claim to governing statutes, Hohfeldian jural relations, and backing exhibits, automatically compiling **Controlled-English Proposed Court Findings** (`Conversion.lex.tex`) or triggering the **Evidentiary Refusal Guard** when proof is missing, alongside controlling **Statutory Rule Exceptions** (`RuleDiscovery.lex.tex`).
  3. **Step 3 (Hearing Clock, Witness Roster & Exam Scripts)**: Regulate stage-by-stage hearing time budgets (`Hearing.lex.tex`), witness allocations, Direct Examination scripts with admission cues, and Cross-Examination / FRE 106 redirect cards.
  4. **Step 4 (Master Exhibit Register & Statutory Calculators)**: Manage evidentiary foundations (`FRE 901`, `FRE 803(6)`), visual thumbnails, EXIF/PDF forensics, SHA-256 chain-of-custody digests, and focused tabbed statutory calculators (Family Support Guidelines § 305, Veterans 38 C.F.R. §§ 4.25 & 4.16 TDIU, and Housing/Civil Rent Abatement & Diminution).
  5. **Step 5 (Consistency Audit, Priority Schedule, Filing Center & Trial Brief)**: Run an automated 6-point evidentiary readiness audit, review the priority-ranked examination schedule, generate court filings, respond to client questions, and download the compiled Markdown Trial Brief.
- **[`view/courtroom.html`](view/courtroom.html)** — **High-Legibility Live Hearing Companion**:
  1. **Mode 1 (Instant Cross-Exam Responder)**: 1-click access to calm witness responses, trap warnings, supporting exhibits, and FRE 106 completeness context.
  2. **Mode 2 (Direct Testimony Checklist)**: Live check-off script with 1-click filters (`All Questions`, `⭐ Key Highlights`, `📎 Exhibit Admissions`, `Hide Stricken`) and inline `📎 Mark Admitted` buttons that update the exhibit record in real time.
  3. **Mode 3 (Live Exhibit Admission Tracker)**: Track `Stipulated`, `Ready to Offer`, `Offered at Hearing`, and `Admitted` status with visual exhibit previews and page/paragraph callouts at the podium.

---

## Mechanized Verification & CLI Reference

Every layer of PrismLegal is declaratively specified in literate Lean 4 (`src/*.lex.tex`), validated against PrismPM TOML/JSON schemas (`model/*.toml`, `schemas/*.schema.json`), and compiled into certified Rust artifacts (`production/`):

| Command | Description |
| :--- | :--- |
| `./bin/prism-legal brief` | Print executive summary of the platform and reference benchmark |
| `./bin/prism-legal portal status` | Verify `M:N` Client-Lawyer-Firm-Court-Framework non-conflation |
| `./bin/prism-legal portal serve --port 8780` | Serve the multi-page User Portal locally at `http://127.0.0.1:8780` |
| `./bin/prism-legal view render --out view` | Render the complete static portal and `register.json` into `view/` |
| `./bin/prism-legal convert` | Compile 16 S-expression propositions & refusal guards to Controlled Legal English |
| `./bin/prism-legal engine [--rust]` | Run stratified Horn forward-chaining inference (Python & certified Rust parity) |
| `./bin/prism-legal discover [--rust]` | Run bounded Depth<=3 rule-discovery & trap-pruning synthesizer |
| `./bin/prism-legal exam` | Inspect the 6-chapter, 36-Q&A Direct Examination script & visual annotations |
| `./bin/prism-legal visual` | Inspect handwritten diary transcriptions, visual forensics, & 30-exhibit intent |
| `./bin/prism-legal audit` | Run all 16 structural & strategic traps (`TRAP-01`..`TRAP-16`) |
| `./bin/prism-legal sanitize` | Run automated Zero-PII & Case-Sanitization audit across the repository |
| `./bin/prism-legal api sync` | Regenerate all `src/*.lex.tex`, `model/*.toml`, `.github/workflows/`, `view/`, `site/`, and `docs/` |
| `./bin/prism-legal api check` | Verify zero drift across all 22 mechanized models, workflows, and sanitization gate |
| `./bin/prism-legal check` | Run all static, schema, workflow, and sanitization checks |
| `./bin/prism-legal verify` | Compile and run the 21-module Lean 4 kernel verification executable |
| `./bin/prism-legal api production` | Emit certified Rust production crates via the LexLean API |

---

## Public-Benefit Charter & Zero-PII Production Guarantee

PrismLegal models legal matters using synthetic fictional domains (`Alderbrook`, `pinecrest`, ` Birchwood`, `Cedarhurst`, `Maplewood`, `ironwood`), statutory dockets (`2030-FAM-9010`, `2030-ADM-9020`, `2030-COM-9030`, `2030-EMP-9040`, `2030-CON-9050`, `2030-HSG-9060`), and cryptographic vault URIs (`vault://exhibits/...`). An automated sanitization gate (`./bin/prism-legal sanitize`) enforces zero personal data, zero simulated features, and zero placeholder content across every file in the repository.
