"""LexLean lock, check, and Lean 4 kernel verify runner for PrismLegal Public-Benefit Legal Platform."""

import json
import shutil
import subprocess
from . import ROOT


def lexlean_bin():
    return shutil.which("lexlean")


def prismpm_bin():
    return shutil.which("prismpm")


def _run(cmd, cwd=ROOT, timeout=600):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def lock():
    b = lexlean_bin()
    if not b:
        return {"ok": False, "output": "LexLean is required on PATH; an existing lockfile is not verification."}
    code, out, err = _run([b, "--project", str(ROOT / "lexlean.toml"), "lock"], timeout=600)
    return {"ok": code == 0, "output": (out + err).strip()[-400:]}


def _lexlean(args, timeout=900):
    b = lexlean_bin()
    if not b:
        return {"ok": False, "diagnostics": ["LexLean is required on PATH. No compiler or kernel verification was performed."], "attestation": None}
    cmd = [b, "--project", str(ROOT / "lexlean.toml"), *args, "--diagnostic-format", "json"]
    code, out, err = _run(cmd, timeout=timeout)
    try:
        data = json.loads(out.strip().splitlines()[-1]) if out.strip() else {}
    except json.JSONDecodeError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    diags = []
    for d in data.get("diagnostics", []):
        where = d.get("primary") or {}
        loc = f"{where.get('path', '?')}:{where.get('line_start', '?')}"
        notes = "; ".join(n.get("message", "")[:200] for n in d.get("notes", [])[:2])
        diags.append(f"{d.get('code')} {loc}: {d.get('message', '')[:400]}" + (f" [{notes}]" if notes else ""))
    if code != 0 and not diags:
        diags.append((err or out).strip()[-800:])
    success = (
        code == 0
        and data.get("spec") == "lexlean/command-result/1"
        and data.get("command") == args[0]
        and data.get("exit_code") == 0
        and data.get("success") is True
    )
    attestation = data.get("attestation_id")
    if args[0] == "verify":
        success = success and (
            isinstance(attestation, str)
            and len(attestation) == 64
            and all(character in "0123456789abcdef" for character in attestation)
        )
    if not success and not diags:
        diags.append("LexLean did not return a valid successful result with the required verification evidence.")
    return {
        "ok": success,
        "diagnostics": diags,
        "attestation": attestation if success else None,
    }


def check(modules=None):
    return _lexlean(["check", *(modules or [])], timeout=600)


def verify(modules=None):
    return _lexlean(["verify", *(modules or [])], timeout=1800)
