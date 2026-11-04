"""Bind a successful CI browser artifact to its Git tree and pinned SDK.

This is delivery bookkeeping, not a replacement PrismPM attestation. CI calls
pack only after verification and every application test succeeds. Pages also
requires a successful run of the repository's CI workflow before downloading.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def identity(root):
    tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=root, text=True
    ).strip()
    sdk = json.loads((root / "toolchain/prismpm.json").read_text())["revision"]
    if not all(re.fullmatch(r"[0-9a-f]{40}", value) for value in (tree, sdk)):
        raise ValueError("Invalid Git tree or SDK revision")
    return {"tree": tree, "sdk": sdk}


def artifact_name(binding):
    return f"verified-matter-{binding['tree']}-{binding['sdk']}"


def file_hashes(directory):
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("Regular artifact directory required")
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError("Artifact aliases are not permitted")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError("Regular artifact file required")
        result[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def verification_result(path):
    data = json.loads(path.read_text())
    if data.get("schema") != "prismpm/verify-result/1" or not all(
        re.fullmatch(r"[0-9a-f]{64}", str(data.get(key, "")))
        for key in ("build_id", "attestation_id")
    ):
        raise ValueError("Successful PrismPM verification result required")
    return data


def pack(root):
    binding = identity(root)
    result = verification_result(root / "matter-verification.json")
    output = root / "verified-matter"
    output.mkdir()  # A stale artifact must not silently become a fresh release.
    shutil.copytree(root / "matter-site", output / "site")
    shutil.copyfile(root / "matter-verification.json", output / "matter-verification.json")
    receipt = {"schema": "prism-legal/verified-view/1", **binding,
               "build_id": result["build_id"], "files": file_hashes(output)}
    (output / "receipt.json").write_text(json.dumps(receipt, sort_keys=True) + "\n")


def restore(root):
    output = root / "verified-matter"
    receipt_path = output / "receipt.json"
    if receipt_path.is_symlink():
        raise ValueError("Regular receipt required")
    receipt = json.loads(receipt_path.read_text())
    binding = identity(root)
    if receipt.get("schema") != "prism-legal/verified-view/1" or any(
        receipt.get(key) != value for key, value in binding.items()
    ):
        raise ValueError("Verified artifact does not match this source tree and SDK")
    actual = file_hashes(output)
    del actual["receipt.json"]
    if actual != receipt.get("files") or not {"site/index.html", "site/provenance.json"} <= actual.keys():
        raise ValueError("Verified artifact bytes or file set changed")
    result = verification_result(output / "matter-verification.json")
    if result["build_id"] != receipt.get("build_id"):
        raise ValueError("Verified build identity changed")
    shutil.copytree(output / "site", root / "matter-site")


if __name__ == "__main__":
    root = Path.cwd()
    command = sys.argv[1]
    if command == "name":
        print(artifact_name(identity(root)))
    elif command == "pack":
        pack(root)
    elif command == "restore":
        restore(root)
    else:
        raise SystemExit("Expected name, pack, or restore")
