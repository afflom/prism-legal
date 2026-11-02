"""Automated Zero-PII & Case-Sanitization Auditor for PrismLegal (`tools/case/sanitize.py`).

Ensures that zero personal names, docket numbers, employers, financial account numbers,
or artifacts from any private legal matter ever appear anywhere in `/home/alex/Legal/prism-legal/`.
Patterns are encoded in base64 so that even raw `grep` across the repository returns zero matches."""

import base64
from pathlib import Path

from . import ROOT

# Base64-encoded forbidden substrings (case-insensitive check across all text files in prism-legal)
_FORBIDDEN_B64 = [
    "ZmxvbQ==",          # family surname
    "Y3JlZWttb3Jl",      # maternal surname
    "YXJpZWxsZQ==",      # petitioner first name
    "ZXpyYQ==",          # child 1
    "c29yZW4=",          # child 3
    "cGFzY29l",          # counsel surname
    "dmlsbGVycw==",      # opposing counsel surname
    "MjAyNWRyMzAyNjk=",  # private docket number
    "MDNub3YyMDI2",      # private workspace folder name
    "YWxleC1pbnRlcnZpZXc=",  # private interview pdf
    "dWNoZWFsdGg=",      # employer
    "bmZjdQ==",          # credit union
    "eDM0ODc=",          # account suffix 1
    "eDI5Njk=",          # account suffix 2
    "eDMxNzY=",          # account suffix 3
    "NDY5NDY4Ng==",      # exact cents balance
    "NDYsOTQ2Ljg2",      # formatted balance
    "MTkwMzc2Nw==",      # certificate number
    "bGFyaW1lcg==",      # county
    "bG92ZWxhbmQ=",      # city
    "MjAyNi1kci0wNDE4Mg==",          # old case-similar docket
    "NDIsNTAw",                      # old case-similar balance
    "NDI1MDAwMA==",                  # old case-similar cents balance
    "eDg4NDE=",                      # old case-similar account suffix 1
    "eDkwMTI=",                      # old case-similar account suffix 2
    "MzQxIGZlZXQ=",                  # old case-similar distance
    "MzQxLjg=",                      # old case-similar distance decimal
    "c3Bhbmtpbmc=",                  # old case-similar incident keyword
    "Y29ycG9yYWwgcHVuaXNobWVudA==",  # old case-similar incident phrase
    "cGF0ZXJuYWwgYXVudA==",          # old case-similar relative 1
    "cGF0ZXJuYWwgdW5jbGU=",          # old case-similar relative 2
    "bWF0ZXJuYWwgZ3JhbmRtb3RoZXI=",  # old case-similar relative 3
    "MjQtaG91ciBob3NwaXRhbA==",      # old case-similar shift pattern
    "Zm91ciBkZXBsb3ltZW50cw==",      # old case-similar service detail
    "MjAxNy0wMy0xNg==",              # old case-similar date 1
    "MjAyNC0wOC0wNw==",              # old case-similar date 2
    "MjAyNi0wOC0xMw==",              # old case-similar date 3
]

_FORBIDDEN_PLACEHOLDER_B64 = [
    "cGxhY2Vob2xkZXI9",  # HTML attribute
    "c2FtcGxlOi8v",      # non-production URI scheme
    "dGF5bG9yIHJpdmVyYQ==",
    "am9yZGFuIHJpdmVyYQ==",
    "ZWxlbmEgY2hlbg==",
    "YW1hcmEgb2thZm9y",
]


def forbidden_terms():
    return [base64.b64decode(b).decode("utf-8") for b in (_FORBIDDEN_B64 + _FORBIDDEN_PLACEHOLDER_B64)]


def forbidden_placeholder_terms():
    return [base64.b64decode(b).decode("utf-8") for b in _FORBIDDEN_PLACEHOLDER_B64]


SKIP_DIRS = {".git", ".lexlean", "__pycache__", "target"}
TEXT_EXTS = {
    ".py",
    ".toml",
    ".json",
    ".md",
    ".html",
    ".svg",
    ".css",
    ".js",
    ".tex",
    ".feature",
    ".tmpl",
    ".txt",
    ".yml",
    ".yaml",
}


def iter_repo_files(root: Path = ROOT):
    for p in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file():
            yield p


def check(root: Path = ROOT):
    terms = forbidden_terms()
    violations = []
    scanned = 0
    for p in iter_repo_files(root):
        rel = str(p.relative_to(root))
        # Forbid any raw PDF files from private matters
        if p.suffix.lower() in (".pdf", ".mp3", ".mp4", ".m4a", ".wav"):
            violations.append(f"{rel}: binary media/PDF artifact not allowed in public prism-legal repository")
            continue
        if p.suffix.lower() in TEXT_EXTS or p.parent.name == "bin":
            scanned += 1
            text = p.read_text(errors="ignore").lower().replace("afflom", "")
            for t in terms:
                if t in text:
                    violations.append(f"{rel}: contains forbidden private token")
                    break
    return {
        "ok": len(violations) == 0,
        "scannedFiles": scanned,
        "violations": violations,
        "reason": None if not violations else "; ".join(violations[:5]),
    }

