"""Release reuse must never substitute stale or changed bytes for verification."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.ci import changed, verified_view as view
from tools.case import presentationmodel


class VerifiedView(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        self.binding = {"tree": "1" * 40, "sdk": "2" * 40}
        identity = patch.object(view, "identity", return_value=self.binding)
        identity.start()
        self.addCleanup(identity.stop)
        site = self.root / "matter-site"
        site.mkdir()
        (site / "index.html").write_text("test artifact, not application acceptance")
        (site / "provenance.json").write_text("{}")
        (site / "app.wasm").write_bytes(b"test transport bytes")
        self.result = {"schema": "prismpm/verify-result/1", "build_id": "3" * 64,
                       "attestation_id": "4" * 64, "verified_root": ".prism/verified/fixture"}
        (self.root / "matter-verification.json").write_text(json.dumps(self.result))

    def packed(self):
        view.pack(self.root)
        shutil.rmtree(self.root / "matter-site")
        return self.root / "verified-matter"

    def test_exact_artifact_round_trip(self):
        before = view.file_hashes(self.root / "matter-site")
        self.packed()
        view.restore(self.root)
        self.assertEqual(view.file_hashes(self.root / "matter-site"), before)

    def test_source_or_sdk_change_refuses_reuse(self):
        self.packed()
        for key in ("tree", "sdk"):
            with self.subTest(key=key), patch.object(view, "identity", return_value={**self.binding, key: "5" * 40}):
                with self.assertRaisesRegex(ValueError, "source tree and SDK"):
                    view.restore(self.root)
                self.assertFalse((self.root / "matter-site").exists())

    def test_changed_added_and_missing_files_refuse_reuse(self):
        artifact = self.packed()
        target = artifact / "site/app.wasm"
        original = target.read_bytes()
        for mutation in ("changed", "added", "deleted"):
            with self.subTest(mutation=mutation):
                if mutation == "changed": target.write_bytes(b"modified")
                elif mutation == "added": (artifact / "unexpected").write_text("extra")
                else: target.unlink()
                with self.assertRaisesRegex(ValueError, "bytes or file set"):
                    view.restore(self.root)
                target.write_bytes(original)
                (artifact / "unexpected").unlink(missing_ok=True)

    def test_symlink_refused(self):
        artifact = self.packed()
        (artifact / "site/alias").symlink_to(artifact / "site/index.html")
        with self.assertRaisesRegex(ValueError, "aliases"):
            view.restore(self.root)

    def test_attestation_and_build_binding_required(self):
        artifact = self.packed()
        receipt = json.loads((artifact / "receipt.json").read_text())
        receipt["build_id"] = "6" * 64
        (artifact / "receipt.json").write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValueError, "build identity"):
            view.restore(self.root)
        for result in ({}, {**self.result, "schema": "prismpm/build-result/1"},
                       {**self.result, "attestation_id": ""}):
            (self.root / "matter-verification.json").write_text(json.dumps(result))
            with self.assertRaisesRegex(ValueError, "verification result"):
                view.pack(self.root)

    def test_stale_pack_destination_refused(self):
        view.pack(self.root)
        with self.assertRaises(FileExistsError):
            view.pack(self.root)


class WorkflowPolicy(unittest.TestCase):
    def test_only_explanatory_docs_skip_application_work(self):
        self.assertFalse(changed.needs_application(list(changed.DOCS_ONLY), "pull_request"))
        for path in ("src/Matter.lex.tex", "docs/index.html", "docs/new-guide.md",
                     "tools/ci/changed.py", "tests/matter/core_runtime.mjs", "toolchain/prismpm.json",
                     ".github/workflows/ci.yml", "README.md\nsource"):
            self.assertTrue(changed.needs_application(["README.md", path], "pull_request"))
        self.assertTrue(changed.needs_application([], "workflow_dispatch"))

    def test_real_git_diff_detects_document_to_source_rename(self):
        script = Path(changed.__file__).resolve()
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL)
            git("init", "-q")
            git("config", "user.name", "CI policy test")
            git("config", "user.email", "fixture@example.invalid")
            (root / "README.md").write_text("initial")
            git("add", ".")
            git("commit", "-qm", "fixture initial")
            (root / "README.md").write_text("changed")
            git("commit", "-qam", "fixture docs")
            def scope(event):
                return subprocess.check_output(["python3", str(script)], cwd=root, text=True,
                    env={**os.environ, "GITHUB_EVENT_NAME": event}).strip()
            self.assertEqual(scope("pull_request"), "application=false")
            self.assertEqual(scope("workflow_dispatch"), "application=true")
            git("mv", "README.md", "model.lex.tex")
            git("commit", "-qm", "fixture rename")
            self.assertEqual(scope("pull_request"), "application=true")

    def test_workflows_match_authoritative_generator(self):
        self.assertEqual(presentationmodel.CI_WORKFLOW.read_text(), presentationmodel.render_ci_workflow_yml())
        self.assertEqual(presentationmodel.PAGES_WORKFLOW.read_text(), presentationmodel.render_pages_workflow_yml())

    def test_deployment_is_not_canceled_by_pr_concurrency(self):
        ci = presentationmodel.render_ci_workflow_yml()
        pages = presentationmodel.render_pages_workflow_yml()
        self.assertIn("group: prism-legal-ci-", ci)
        self.assertIn("cancel-in-progress: ${{ github.event_name == 'pull_request' }}", ci)
        self.assertIn("group: pages\n  cancel-in-progress: false", pages)
        self.assertIn("needs: validate", ci)
        self.assertIn("  pull-requests: read\n", pages)
        # CI and Pages must agree on the only paths that avoid application work.
        ignored = pages.split("    paths-ignore:\n", 1)[1].split("  workflow_dispatch:", 1)[0]
        self.assertEqual({line.strip()[2:] for line in ignored.splitlines()}, changed.DOCS_ONLY)

    def test_one_build_and_proof_owner_and_all_runtime_checks_remain(self):
        root = Path(__file__).resolve().parents[1]
        script = (root / "tools/verify_matter.sh").read_text()
        self.assertEqual(script.count('"$prism_sdk" --project . --json verify'), 1)
        self.assertNotIn('"$prism_sdk" --project . --json build', script)
        for check in ("./bin/prism-legal check", "cargo test --locked --offline", "holistic_runtime.mjs",
                      "core_runtime.mjs", "run_browser.mjs", "verified_view.py pack"):
            self.assertIn(check, script)
        self.assertNotIn("actions/lexlean", presentationmodel.render_ci_workflow_yml())


if __name__ == "__main__":
    unittest.main()
