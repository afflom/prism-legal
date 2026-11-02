"""LexLean production emission request (`production/request.json`) for PrismLegal Reference Matter (Case No. 2030-FAM-9010)."""

import json
import subprocess

from . import ROOT, apimodel, checks, discoverymodel, enginemodel, intakemodel

REQUEST = ROOT / "production" / "request.json"
OUT = ROOT / ".lexlean" / "production"

TARGET_DIGESTS = {
    "rust-core": "b120ca1bfec593473116198fb21e7c9c1b625cbcc858a0e4cfd92fbe4aeb6757",
    "rust-std": "e3db2e96823c5f2c710fdace992d11e5fbb6b63b1500045eff45f85eedf94027",
}

REMEDIES_ROOTS = {
    "stipulatedBaselineCents": {"effects": ["overflow"], "targets": ["rust-core", "rust-std"]},
    "guidelineNetTransferCents": {"effects": ["overflow"], "targets": ["rust-core", "rust-std"]},
    "respondentStipulatedDisabilityCents": {"effects": ["overflow"], "targets": ["rust-core", "rust-std"]},
    "petitionerStipulatedMonthlyCents": {"effects": ["overflow"], "targets": ["rust-core", "rust-std"]},
    "undisclosedReserveBalanceCents": {"effects": ["overflow"], "targets": ["rust-core", "rust-std"]},
    "sharedParentingAdjustedCents": {"effects": ["overflow"], "targets": ["rust-core", "rust-std"]},
    "worksheets": {"effects": ["allocation"], "targets": ["rust-std"]},
}


def _snake(s):
    out = []
    for i, ch in enumerate(s):
        if ch.isupper() and i > 0:
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


def request_doc():
    entries = []
    for name, spec in sorted(apimodel.PRODUCTION_ROOTS.items()):
        entries.append(("PrismLegal.Api", name, spec["targets"]))
    for name, spec in sorted(REMEDIES_ROOTS.items()):
        entries.append(("PrismLegal.RemediesCore", name, spec["targets"]))
    for name, spec in sorted(discoverymodel.PRODUCTION_ROOTS.items()):
        entries.append(("PrismLegal.Discovery", name, spec["targets"]))
    for name, spec in sorted(enginemodel.PRODUCTION_ROOTS.items()):
        entries.append(("PrismLegal.Engine", name, spec["targets"]))
    for name, spec in sorted(intakemodel.PRODUCTION_ROOTS.items()):
        entries.append(("PrismLegal.Intake", name, spec["targets"]))

    roots = []
    for mod, name, targets in entries:
        mod_short = mod.split(".")[-1].lower()
        pkg_name = f"prism_legal_{mod_short}_{_snake(name)}"
        roots.append(
            {
                "package": {"name": pkg_name, "version": "0.1.0"},
                "root": f"{mod}.{name}",
                "targets": [{"digest": TARGET_DIGESTS[tid], "id": tid} for tid in sorted(targets)],
            }
        )
    roots.sort(key=lambda r: r["root"])
    return {
        "roots": roots,
        "spec": "lexlean/production-request/1",
    }


def sync():
    REQUEST.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(request_doc(), indent=2) + "\n"
    changed = not REQUEST.exists() or REQUEST.read_text() != text
    if changed:
        REQUEST.write_text(text)
    return {"request": str(REQUEST.relative_to(ROOT)), "changed": changed}


def check():
    expected = json.dumps(request_doc(), indent=2) + "\n"
    if not REQUEST.exists() or REQUEST.read_text() != expected:
        return {"ok": False, "reason": "production/request.json drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}


def build(verify=False):
    sync()
    checks.lock()
    cmd = [
        checks.lexlean_bin(),
        "production",
        "build",
        "--project",
        str(ROOT / "lexlean.toml"),
        "--request",
        str(REQUEST),
        "--diagnostic-format",
        "json",
    ]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    payload = json.loads(r.stdout) if r.stdout.strip().startswith("{") else {"raw": r.stdout, "stderr": r.stderr}
    return {"ok": r.returncode == 0, "returncode": r.returncode, "result": payload}
