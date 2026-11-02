"""LexLean lock, check, and Lean 4 kernel verify runner for PrismLegal Public-Benefit Legal Platform."""

import json
import subprocess
from pathlib import Path
from . import ROOT


def lexlean_bin():
    for candidate in ["/home/alex/.local/bin/lexlean", "/usr/local/bin/lexlean"]:
        if Path(candidate).exists():
            return candidate
    return "lexlean"


def prismpm_bin():
    for candidate in ["/home/alex/.local/bin/prismpm", "/usr/local/bin/prismpm"]:
        if Path(candidate).exists():
            return candidate
    return "prismpm"


def _run(cmd, cwd=ROOT, timeout=600):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def lock():
    code, out, err = _run([lexlean_bin(), "--project", str(ROOT / "lexlean.toml"), "lock"], timeout=600)
    return {"ok": code == 0, "output": (out + err).strip()[-400:]}


def _lexlean(args, timeout=900):
    cmd = [lexlean_bin(), "--project", str(ROOT / "lexlean.toml"), *args, "--diagnostic-format", "json"]
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

