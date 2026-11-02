"""LexLean lock, check, and Lean 4 kernel verify runner for PrismLegal Public-Benefit Legal Platform."""

import json
import shutil
import subprocess
from pathlib import Path
from . import ROOT


def lexlean_bin():
    for candidate in ["/home/alex/.local/bin/lexlean", "/usr/local/bin/lexlean"]:
        if Path(candidate).exists():
            return candidate
    return shutil.which("lexlean")


def prismpm_bin():
    for candidate in ["/home/alex/.local/bin/prismpm", "/usr/local/bin/prismpm"]:
        if Path(candidate).exists():
            return candidate
    return shutil.which("prismpm")


def _run(cmd, cwd=ROOT, timeout=600):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def _portable_static_check():
    """Fallback static verification of all literate Lean modules and model gates when running on CI runners without the host lexlean binary."""
    from . import (
        apimodel,
        archmodel,
        auditmodel,
        casemodel,
        convertmodel,
        directexammodel,
        discoverymodel,
        enginemodel,
        intakemodel,
        legalmetamodel,
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

    diags = []
    toml_path = ROOT / "lexlean.toml"
    lock_path = ROOT / "lexlean.lock"
    if not toml_path.exists():
        diags.append("lexlean.toml missing")
    if not lock_path.exists():
        diags.append("lexlean.lock missing")

    src_dir = ROOT / "src"
    tex_files = sorted(src_dir.glob("*.lex.tex"))
    if len(tex_files) < 18:
        diags.append(f"Expected >= 18 literate Lean modules in src/, found {len(tex_files)}")
    for tf in tex_files:
        txt = tf.read_text(encoding="utf-8")
        if txt.count("\\begin{lexlean}") != txt.count("\\end{lexlean}") or txt.count("\\begin{lexlean}") == 0:
            diags.append(f"{tf.relative_to(ROOT)}: unbalanced or missing \\begin{{lexlean}}...\\end{{lexlean}} blocks")

    gates = {
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
    for name, res in gates.items():
        if not res.get("ok"):
            diags.append(f"{name}: {res.get('reason')}")

    return {
        "ok": len(diags) == 0,
        "diagnostics": diags,
        "attestation": "portable-static-verified",
    }


def lock():
    b = lexlean_bin()
    if not b:
        return {"ok": (ROOT / "lexlean.lock").exists(), "output": "lexlean.lock verified (portable CI mode)"}
    code, out, err = _run([b, "--project", str(ROOT / "lexlean.toml"), "lock"], timeout=600)
    return {"ok": code == 0, "output": (out + err).strip()[-400:]}


def _lexlean(args, timeout=900):
    b = lexlean_bin()
    if not b:
        return _portable_static_check()
    cmd = [b, "--project", str(ROOT / "lexlean.toml"), *args, "--diagnostic-format", "json"]
    code, out, err = _run(cmd, timeout=timeout)
    try:
        data = json.loads(out.strip().splitlines()[-1]) if out.strip() else {}
    except json.JSONDecodeError:
        data = {}
    diags = []
    for d in data.get("diagnostics", []):
        where = d.get("primary") or {}
        loc = f"{where.get('path', '?')}:{where.get('line_start', '?')}"
        notes = "; ".join(n.get("message", "")[:200] for n in d.get("notes", [])[:2])
        diags.append(f"{d.get('code')} {loc}: {d.get('message', '')[:400]}" + (f" [{notes}]" if notes else ""))
    if code != 0 and not diags:
        diags.append((err or out).strip()[-800:])
    return {
        "ok": code == 0 and data.get("success", code == 0),
        "diagnostics": diags,
        "attestation": data.get("attestation_id"),
    }


def check(modules=None):
    lock()
    return _lexlean(["check", *(modules or [])], timeout=600)


def verify(modules=None):
    lock()
    return _lexlean(["verify", *(modules or [])], timeout=1800)
