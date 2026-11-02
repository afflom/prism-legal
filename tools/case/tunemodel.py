"""Interactive strategy tuning state (`model/tuning.json`) for PrismLegal."""

import copy
import json
from pathlib import Path
from . import ROOT, archmodel

TUNING_JSON = ROOT / "model" / "tuning.json"
TUNING_FILE = TUNING_JSON

DEFAULT_STATE = {
    "spec": "prism-legal/tuning/1",
    "activeMatterId": "CASE-2030-FAM-9010",
    "activeRole": "client",
    "dimensions": archmodel.TUNING_PARAMETERS,
    "overrides": {
        "claims": {},
        "traps": {
            "TRAP-01": {"clientReadiness": "Ready for Stand"},
            "TRAP-04": {"clientReadiness": "Ready for Stand"},
            "TRAP-06": {"clientReadiness": "Ready for Stand"},
            "TRAP-12": {"clientReadiness": "Ready for Stand"},
        },
        "witnesses": {
            "W-01": {"examMinutes": 60},
            "W-02": {"examMinutes": 60},
            "W-03": {"examMinutes": 20},
            "W-04": {"examMinutes": 15},
            "W-05": {"examMinutes": 15},
            "W-06": {"examMinutes": 15},
            "W-07": {"examMinutes": 15},
            "W-08": {"examMinutes": 10},
            "W-09": {"examMinutes": 10},
            "W-10": {"examMinutes": 15},
        },
    },
    "agenda": [
        {
            "id": "AGENDA-01",
            "author": "Client Litigant (Respondent)",
            "targetId": "Ex-L / SF-01",
            "category": "Parenting Schedule & Exchanges",
            "status": "aligned",
            "questionForLawyer": "Confirm Wednesday school drop-off/pick-up transition language in Ex. L.",
            "lawyerGuidance": "Confirmed (Lead Trial Counsel): Ex. L § 2.3 specifies Wednesday school transitions so all exchanges occur seamlessly at school.",
        },
        {
            "id": "AGENDA-02",
            "author": "Client Litigant (Respondent)",
            "targetId": "Ex-G / Ex-H / CLM-13",
            "category": "Rule 16.2 Financial Impeachment",
            "status": "aligned",
            "questionForLawyer": "Verify sequence for introducing Ex. G (Initial SFS) and Ex. H ($30,000.00 Escrow Bank Statements).",
            "lawyerGuidance": "Confirmed: Lock in Initial SFS omission first, then admit Ex. H and cite Temporary Orders Ex. N ¶¶ 24-26.",
        },
        {
            "id": "AGENDA-03",
            "author": "Lead Trial Counsel",
            "targetId": "OP-Ex-13 / TRAP-12",
            "category": "FRE 106 Rule of Completeness",
            "status": "aligned",
            "questionForLawyer": "Rehearse calm reading of page 6 lines 15-28 of the 2028 study log if opposing counsel raises OP Ex. 13.",
            "lawyerGuidance": "Invoke FRE 106 immediately so the full October 14, 2028 positive reinforcement checklist is read into the record.",
        },
    ],
}


def default_state():
    return copy.deepcopy(DEFAULT_STATE)


def load_state():
    if TUNING_JSON.exists():
        data = json.loads(TUNING_JSON.read_text())
        data.setdefault("dimensions", archmodel.TUNING_PARAMETERS)
        return data
    return default_state()


def apply_patch(patch_path: Path):
    state = load_state()
    patch = json.loads(patch_path.read_text())
    for k, v in patch.items():
        state[k] = v
    TUNING_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    return state


def sync():
    TUNING_JSON.parent.mkdir(parents=True, exist_ok=True)
    txt = json.dumps(DEFAULT_STATE, indent=2, ensure_ascii=False) + "\n"
    changed = not TUNING_JSON.exists() or TUNING_JSON.read_text() != txt
    if changed:
        TUNING_JSON.write_text(txt)
    return {"file": "model/tuning.json", "dimensions": len(DEFAULT_STATE["dimensions"]), "changed": changed}


def check():
    expected = json.dumps(DEFAULT_STATE, indent=2, ensure_ascii=False) + "\n"
    if not TUNING_JSON.exists() or TUNING_JSON.read_text() != expected:
        return {"ok": False, "reason": "model/tuning.json drifted; run `bin/prism-legal api sync`"}
    return {"ok": True, "reason": None}
