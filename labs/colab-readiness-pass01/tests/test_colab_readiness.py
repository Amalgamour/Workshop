"""Checker tests and one disposable frozen-tool demonstration.

The demonstration copies pack snapshots and one committed parser blob.
It does not import or read the live prime-cycle tree.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(LAB))

import colab_readiness as checker  # noqa: E402


PYTHON = sys.executable
SNAPSHOTS = ROOT / "00.kernel/00.00.10.work/0516.colab-readiness/evidence/pack05.01/snapshots"
CUT = "b876c7a9e8a27df58c0a5a0815a53f653d929332"
TOOL_COPIES = {
    "0009.blob": "labs/prime-cycle-pass01/prime_cycle.py",
    "0010.blob": "labs/batch-observation-pass01/batch_observe.py",
    "0011.blob": "labs/prime-support-pass01/clerk_adapter.py",
    "0012.blob": "labs/return-capture-pass01/return_capture.py",
    "0013.blob": "labs/return-capture-pass01/return_inspect.py",
    "0014.blob": "labs/prime-review-pass01/prime_review.py",
    "0015.blob": "labs/review-packet-pass01/review_packet.py",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(checker.canonical(value))


def run_check(request: dict, directory: Path) -> tuple[int, dict | None, str]:
    request_path = directory / "request.json"
    write_json(request_path, request)
    code = checker.main(["check", "--request", str(request_path)])
    output = Path(request["output"])
    report_path = output / "readiness.json"
    report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.is_file() else None
    return code, report, output.as_posix() if False else ""


def base_surface() -> dict:
    return {
        "kind": "local-fixture",
        "os": "windows",
        "interpreter": "python",
        "network": "denied",
        "install": "denied",
        "secrets": "none",
        "read_roots": [],
        "write_roots": [],
    }


def policy() -> dict:
    return {
        "declared": True,
        "retain_first_failure": True,
        "diagnostic": "one read-only diagnostic of the first failing file",
        "dependency_check": "one named hash check of the declared dependency",
        "manual_fallback": "manual fallback is labelled and is not assisted success",
    }


def supplied_row(request: dict, dep_id: str, path: str) -> dict:
    row = next(item for item in request["transport"] if item["path"] == path)
    return {
        "id": dep_id,
        "path": path,
        "sha256": row["sha256"],
        "bytes": row["bytes"],
        "role": "subject-runtime",
        "required": True,
        "needed_by": [],
        "invokes": [],
        "supply": "supplied",
        "condition": None,
        "withhold_reason": None,
    }


def categories(default_refs: list[str] | None = None) -> list[dict]:
    rows = []
    for name in checker.CATEGORIES:
        rows.append(
            {
                "category": name,
                "applicability": "not-applicable",
                "reason": f"{name} is not applicable to this fixture",
                "refs": [],
            }
        )
    if default_refs is not None:
        rows[0] = {
            "category": "task-criteria",
            "applicability": "required",
            "reason": "the declared task file",
            "refs": default_refs,
        }
    return rows


def read_only_smoke() -> dict:
    return {
        "status": "not-applicable",
        "reason": "this method does not execute a return",
        "command": None,
        "child_exit": None,
        "wrapper_exit": None,
        "expected_state": None,
        "observed_state": None,
        "cutoff": "",
        "in_flight": [],
        "manual_fallback": False,
        "label": "none",
        "page_sha256": None,
        "receipt_sha256": None,
        "pass_state_before": None,
        "pass_state_after": None,
        "custody": None,
        "judgment_label": None,
        "journal_operations": [],
    }


def passed_smoke(**overrides) -> dict:
    smoke = {
        "status": "passed",
        "reason": "SYNTHETIC recorded route",
        "command": "read --registration registration.json",
        "child_exit": 0,
        "wrapper_exit": 0,
        "expected_state": "reviewed",
        "observed_state": "reviewed",
        "cutoff": "after re-read",
        "in_flight": [],
        "manual_fallback": False,
        "label": "synthetic",
        "page_sha256": "a" * 64,
        "receipt_sha256": "b" * 64,
        "pass_state_before": "awaiting-review",
        "pass_state_after": "reviewed",
        "custody": "complete",
        "judgment_label": "synthetic",
        "journal_operations": ["read", "record", "read"],
    }
    smoke.update(overrides)
    return smoke


def delivery_with(root: Path, files: dict[str, bytes]) -> None:
    for rel, data in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def manifest_for(files: dict[str, bytes]) -> dict:
    return {
        "schema": "artifact-manifest/1",
        "artifacts": [
            {"path": rel, "sha256": sha256(data), "bytes": len(data)}
            for rel, data in files.items()
        ],
    }


def request_for(root: Path, output: Path, files: dict[str, bytes], **overrides) -> dict:
    body = manifest_for(files)
    manifest_bytes = checker.canonical(body)
    files = dict(files)
    files["manifest.json"] = manifest_bytes
    delivery_with(root, files)
    entry = next(iter(files))
    entry_bytes = files[entry]
    body = {
        "schema": checker.SCHEMA_REQUEST,
        "purpose": {
            "statement": "Check a declared read-only delivery.",
            "mode": "read-only",
            "question": "Do the declared bytes support the method?",
            "role": "checker",
            "method": "hash declared files and record the smoke object",
            "finish_boundary": "report only",
        },
        "surface": base_surface(),
        "delivery_root": str(root),
        "output": str(output),
        "transport": [
            {"path": rel, "sha256": sha256(data), "bytes": len(data)} for rel, data in files.items()
        ],
        "entry_points": [{"id": "entry", "path": entry}],
        "dependencies": [
            {
                "id": "entry",
                "path": entry,
                "sha256": sha256(entry_bytes),
                "bytes": len(entry_bytes),
                "role": "subject-runtime",
                "required": True,
                "needed_by": [],
                "invokes": [],
                "supply": "supplied",
                "condition": None,
                "withhold_reason": None,
            }
        ],
        "evidence": categories(["files"]),
        "references": [
            {
                "id": "files",
                "format": "artifact-manifest/1",
                "path": "manifest.json",
                "follow_nested": True,
            }
        ],
        "withholds": [],
        "smoke": read_only_smoke(),
        "failure_policy": policy(),
        "independent_checks": [],
        "bounds": {"max_files": 40, "max_file_bytes": 2000000, "max_total_bytes": 8000000},
    }
    # The task category is required, and the other eight stay not-applicable.
    # Point task-criteria at the manifest, which lists the entry bytes.
    body["evidence"][0]["refs"] = ["files"]
    body.update(overrides)
    return body


class CheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="colab-ready-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.delivery = self.root / "delivery"
        self.output = self.root / "out"
        self.delivery.mkdir()

    def check(self, request: dict) -> tuple[int, dict | None]:
        code, report, _ignored = run_check(request, self.root)
        return code, report

    def test_read_only_ready_keeps_sufficiency_open(self) -> None:
        files = {"task.txt": b"declared task\n"}
        code, report = self.check(request_for(self.delivery, self.output, files))
        self.assertEqual(code, 0)
        self.assertTrue(report["ready_for_declared_method"])
        self.assertTrue(report["transport_valid"])
        self.assertTrue(report["runtime_dependencies_resolved"])
        self.assertTrue(report["evidence_references_resolved"])
        self.assertTrue(report["minimum_evidence_satisfied"])
        self.assertEqual(report["smoke_result"], "not-applicable")
        self.assertEqual(report["semantic_sufficiency"], "not-established")
        self.assertEqual(report["independent_proof"], "not-established")
        self.assertEqual(report["surface_authorization"], "not-established")
        self.assertFalse(report["facets"]["smoke"]["command_executed"])
        self.assertIn("independent checks are empty", report["limits"])
        text = (self.output / "READINESS.md").read_text(encoding="utf-8")
        self.assertIn("## Transport", text)
        self.assertLess(text.index("## Transport"), text.index("## Runtime dependencies"))
        self.assertLess(text.index("## Smoke"), text.index("## Ready for declared method"))
        self.assertLess(text.index("## Ready for declared method"), text.index("## Limits"))

    def test_import_text_is_not_executed(self) -> None:
        source = b"import missing_module_that_is_not_installed\n"
        code, report = self.check(request_for(self.delivery, self.output, {"entry.py": source}))
        self.assertEqual(code, 0, report)
        self.assertTrue(report["ready_for_declared_method"])
        self.assertFalse((self.delivery / "missing_module_that_is_not_installed.py").exists())

    def test_smoke_not_run_does_not_make_transport_green_into_ready(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["purpose"]["mode"] = "return-review"
        request["smoke"] = {
            **passed_smoke(),
            "status": "not-run",
            "reason": "no smoke was run",
            "command": None,
            "child_exit": None,
            "wrapper_exit": None,
            "label": "none",
            "judgment_label": None,
            "page_sha256": None,
            "receipt_sha256": None,
            "pass_state_before": None,
            "pass_state_after": None,
            "custody": None,
            "expected_state": None,
            "observed_state": None,
            "journal_operations": [],
        }
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertTrue(report["transport_valid"])
        self.assertEqual(report["smoke_result"], "not-run")
        self.assertFalse(report["ready_for_declared_method"])

    def test_missing_adapter_fails_runtime(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["dependencies"].append(
            {
                "id": "adapter",
                "path": "clerk_adapter.py",
                "sha256": "a" * 64,
                "bytes": 4,
                "role": "reviewer-assistance",
                "required": True,
                "needed_by": [],
                "invokes": [],
                "supply": "supplied",
                "condition": None,
                "withhold_reason": None,
            }
        )
        request["entry_points"][0]["path"] = "task.txt"
        request["dependencies"][0]["invokes"] = ["adapter"]
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertFalse(report["runtime_dependencies_resolved"])
        self.assertFalse(report["ready_for_declared_method"])
        self.assertTrue(any("adapter" in item for item in report["problems"]))

    def test_missing_support_file_fails_runtime(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["dependencies"].append(
            {
                "id": "support-review",
                "path": "support/prime_review.py",
                "sha256": "b" * 64,
                "bytes": 8,
                "role": "subject-runtime",
                "required": True,
                "needed_by": ["entry"],
                "invokes": [],
                "supply": "supplied",
                "condition": None,
                "withhold_reason": None,
            }
        )
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertFalse(report["runtime_dependencies_resolved"])
        self.assertFalse(report["ready_for_declared_method"])

    def test_changed_pinned_bytes_fail_transport(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["transport"][0]["sha256"] = "c" * 64
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertFalse(report["transport_valid"])
        self.assertFalse(report["ready_for_declared_method"])

    def test_missing_nested_snapshot_fails_even_when_parent_matches(self) -> None:
        nested = {
            "schema": "artifact-manifest/1",
            "artifacts": [{"path": "nested/item.bin", "sha256": sha256(b"item"), "bytes": 4}],
        }
        nested_bytes = checker.canonical(nested)
        pack = {
            "schema": "prime-pack-sources/1",
            "sources": [
                {
                    "path": "not-opened.txt",
                    "snapshot": "snapshots/top.json",
                    "sha256": sha256(nested_bytes),
                    "bytes": len(nested_bytes),
                }
            ],
        }
        files = {"snapshots/top.json": nested_bytes, "pack.json": checker.canonical(pack)}
        delivery_with(self.delivery, files)
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        # request_for already wrote its own files; add the pack beside them.
        delivery_with(self.delivery, files)
        request["transport"].append(
            {"path": "pack.json", "sha256": sha256(files["pack.json"]), "bytes": len(files["pack.json"])}
        )
        request["transport"].append(
            {
                "path": "snapshots/top.json",
                "sha256": sha256(nested_bytes),
                "bytes": len(nested_bytes),
            }
        )
        request["references"] = [
            {
                "id": "pack",
                "format": "prime-pack-sources/1",
                "path": "pack.json",
                "follow_nested": True,
            }
        ]
        request["evidence"] = categories(["pack"])
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        self.assertFalse(report["evidence_references_resolved"])
        self.assertFalse(report["minimum_evidence_satisfied"])
        self.assertFalse(report["ready_for_declared_method"])
        joined = "\n".join(report["problems"])
        self.assertIn("nested/item.bin", joined)
        self.assertNotIn("not-opened.txt", joined)

    def test_null_source_binding_fails(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["dependencies"][0]["sha256"] = None
        request["dependencies"][0]["bytes"] = None
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertFalse(report["runtime_dependencies_resolved"])
        self.assertTrue(any("null source binding" in item for item in report["problems"]))

    def test_observation_failed_cannot_pass(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["purpose"]["mode"] = "return-review"
        request["smoke"] = passed_smoke(
            expected_state="observation-failed",
            observed_state="observation-failed",
        )
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertEqual(report["smoke_result"], "failed")
        self.assertFalse(report["ready_for_declared_method"])

    def test_no_return_cannot_pass(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["purpose"]["mode"] = "return-review"
        request["smoke"] = passed_smoke(expected_state="no-return", observed_state="no-return")
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertEqual(report["smoke_result"], "failed")

    def test_missing_category_is_refused(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["evidence"] = request["evidence"][:-1]
        code, report = self.check(request)
        self.assertEqual(code, 2)
        self.assertIsNone(report)
        self.assertFalse(self.output.exists())

    def test_unsupported_format_is_not_success(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["references"][0]["format"] = "prime-entry-pin-artifact-manifest/1"
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertEqual(report["evidence_references_resolved"], "unsupported")
        self.assertFalse(report["ready_for_declared_method"])

    def test_unsafe_path_is_refused(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["transport"][0]["path"] = "../secret.txt"
        code, report = self.check(request)
        self.assertEqual(code, 2)
        self.assertIsNone(report)
        self.assertFalse(self.output.exists())

    def test_linked_path_is_refused(self) -> None:
        target = self.delivery / "task.txt"
        target.write_bytes(b"task\n")
        link = self.delivery / "linked.txt"
        try:
            os.symlink(target, link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest("symlink creation failed: WinError 1314")
            raise
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        data = link.read_bytes() if False else target.read_bytes()
        del data
        request["transport"].append(
            {"path": "linked.txt", "sha256": sha256(b"task\n"), "bytes": len(b"task\n")}
        )
        code, report = self.check(request)
        self.assertEqual(code, 2)
        self.assertIsNone(report)
        self.assertFalse(self.output.exists())

    def test_duplicate_key_is_refused(self) -> None:
        raw = self.root / "request.json"
        raw.write_text('{"schema": "colab-readiness-request/1", "schema": "other"}\n', encoding="utf-8")
        code = checker.main(["check", "--request", str(raw)])
        self.assertEqual(code, 2)

    def test_malformed_json_is_refused(self) -> None:
        raw = self.root / "request.json"
        raw.write_text("{", encoding="utf-8")
        self.assertEqual(checker.main(["check", "--request", str(raw)]), 2)

    def test_occupied_output_is_not_modified(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        marker = self.output / "marker.txt"
        marker.write_text("keep\n", encoding="utf-8")
        before = (self.output / "readiness.json").read_bytes()
        code, report = self.check(request)
        self.assertEqual(code, 2)
        self.assertEqual((self.output / "readiness.json").read_bytes(), before)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep\n")

    def test_partial_bound_is_retained(self) -> None:
        request = request_for(
            self.delivery,
            self.output,
            {"one.txt": b"one\n", "two.txt": b"two\n"},
        )
        request["bounds"]["max_files"] = 1
        code, report = self.check(request)
        self.assertEqual(code, 2)
        self.assertEqual(report["assembly"], "partial")
        self.assertFalse(report["ready_for_declared_method"])
        self.assertTrue((self.output / "readiness.json").is_file())
        self.assertTrue((self.output / "READINESS.md").is_file())

    def test_required_withhold_fails_and_optional_assistance_does_not(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["withholds"] = [{"path": "optional-adapter.py", "reason": "assistance not used"}]
        request["dependencies"].append(
            {
                "id": "optional-adapter",
                "path": "optional-adapter.py",
                "sha256": None,
                "bytes": None,
                "role": "reviewer-assistance",
                "required": False,
                "needed_by": [],
                "invokes": [],
                "supply": "withheld",
                "condition": None,
                "withhold_reason": "assistance not used",
            }
        )
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        self.assertTrue(report["runtime_dependencies_resolved"])
        self.assertTrue(report["ready_for_declared_method"])
        request["output"] = str(self.root / "out-required")
        request["dependencies"][1]["required"] = True
        request["dependencies"][1]["needed_by"] = ["entry"]
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertFalse(report["runtime_dependencies_resolved"])

    def test_preinstalled_dependency_stays_unknown(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["dependencies"][0]["supply"] = "preinstalled-verified"
        request["dependencies"][0]["sha256"] = None
        request["dependencies"][0]["bytes"] = None
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertEqual(report["runtime_dependencies_resolved"], "unknown")
        self.assertFalse(report["ready_for_declared_method"])

    def test_allowed_network_does_not_authorize(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["surface"]["network"] = "allowed"
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertEqual(report["surface_authorization"], "not-established")
        self.assertFalse(report["ready_for_declared_method"])

    def test_manual_fallback_is_not_assisted_success(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["purpose"]["mode"] = "return-review"
        request["smoke"] = passed_smoke(manual_fallback=True)
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertEqual(report["smoke_result"], "failed")
        self.assertFalse(report["ready_for_declared_method"])

    def test_exit_layers_stay_distinct(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["purpose"]["mode"] = "return-review"
        request["smoke"] = passed_smoke(child_exit=2, wrapper_exit=1)
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertTrue(report["exit_layers_differ"])
        self.assertEqual(report["smoke_result"], "partial")
        self.assertFalse(report["ready_for_declared_method"])

    def test_undeclared_failure_policy_blocks_ready(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["failure_policy"]["declared"] = False
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertFalse(report["ready_for_declared_method"])

    def test_cycle_and_unexercised_condition_and_outside_closure(self) -> None:
        files = {"a.py": b"a\n", "b.py": b"b\n", "c.py": b"c\n"}
        request = request_for(self.delivery, self.output, files)
        request["entry_points"] = [{"id": "a", "path": "a.py"}]
        digest = {rel: (sha256(data), len(data)) for rel, data in files.items()}
        request["dependencies"] = [
            {
                "id": name,
                "path": rel,
                "sha256": digest[rel][0],
                "bytes": digest[rel][1],
                "role": "subject-runtime",
                "required": True,
                "needed_by": [],
                "invokes": invokes,
                "supply": "supplied",
                "condition": condition,
                "withhold_reason": None,
            }
            for name, rel, invokes, condition in (
                ("a", "a.py", ["b"], None),
                ("b", "b.py", ["a"], None),
                (
                    "c",
                    "c.py",
                    [],
                    {"text": "only when the bench support tree is mounted", "exercised": False},
                ),
            )
        ]
        code, report = self.check(request)
        self.assertEqual(code, 0)
        self.assertFalse(report["runtime_dependencies_resolved"])
        joined = "\n".join(report["problems"])
        self.assertIn("dependency cycle", joined)
        self.assertIn("outside the entry closure", joined)

    def test_shared_component_can_be_ready_without_independent_proof(self) -> None:
        files = {"task.txt": b"task\n", "review_packet.py": b"packet\n"}
        request = request_for(self.delivery, self.output, files)
        packet = request["transport"][1]
        request["dependencies"].append(
            {
                "id": "packet",
                "path": "review_packet.py",
                "sha256": packet["sha256"],
                "bytes": packet["bytes"],
                "role": "shared-subject-and-assistance",
                "required": False,
                "needed_by": [],
                "invokes": [],
                "supply": "supplied",
                "condition": {"text": "packet command", "exercised": False},
                "withhold_reason": None,
            }
        )
        request["independent_checks"] = [
            {"id": "hash", "text": "the file hash matched the declaration", "status": "present"}
        ]
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        self.assertTrue(report["shared_component"])
        self.assertTrue(report["ready_for_declared_method"])
        self.assertEqual(report["independent_proof"], "not-established")
        self.assertTrue(any("shared subject" in item for item in report["limits"]))

    def test_entry_points_must_be_accounted(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        self.assertEqual(request["dependencies"][0]["invokes"], [])
        self.assertTrue(report["facets"]["runtime"]["entries"][0]["accounted"])
        self.assertTrue(report["runtime_dependencies_resolved"])
        self.assertTrue(report["ready_for_declared_method"])

        files = {"a.py": b"a\n", "b.py": b"b\n"}
        both = request_for(self.delivery, self.root / "out-both", files)
        both["entry_points"] = [{"id": "a", "path": "a.py"}, {"id": "b", "path": "b.py"}]
        both["dependencies"] = [supplied_row(both, "a", "a.py"), supplied_row(both, "b", "b.py")]
        code, report = self.check(both)
        self.assertEqual(code, 0, report)
        self.assertTrue(report["ready_for_declared_method"])
        self.assertEqual([row["accounted"] for row in report["facets"]["runtime"]["entries"]], [True, True])

        missing = request_for(self.delivery, self.root / "out-missing-root", files)
        missing["entry_points"] = [{"id": "a", "path": "a.py"}, {"id": "b", "path": "b.py"}]
        missing["dependencies"] = [supplied_row(missing, "a", "a.py")]
        code, report = self.check(missing)
        self.assertEqual(code, 0, report)
        self.assertFalse(report["runtime_dependencies_resolved"])
        self.assertTrue(report["transport_valid"])
        self.assertTrue(report["evidence_references_resolved"])
        self.assertFalse(report["ready_for_declared_method"])
        self.assertIn("entry point has no dependency record: b", report["problems"])

        empty = request_for(self.delivery, self.root / "out-empty-deps", {"task.txt": b"task\n"})
        empty["dependencies"] = []
        code, report = self.check(empty)
        self.assertEqual(code, 0, report)
        self.assertFalse(report["runtime_dependencies_resolved"])
        self.assertTrue(report["transport_valid"])
        self.assertFalse(report["ready_for_declared_method"])
        self.assertIn("entry point has no dependency record: entry", report["problems"])

    def test_matching_failed_exits_are_not_a_passed_reread(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["purpose"]["mode"] = "return-review"
        request["smoke"] = passed_smoke(child_exit=2, wrapper_exit=2)
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        self.assertFalse(report["exit_layers_differ"])
        self.assertEqual(report["smoke_result"], "failed")
        self.assertFalse(report["ready_for_declared_method"])
        self.assertTrue(report["transport_valid"])
        self.assertTrue(report["runtime_dependencies_resolved"])
        self.assertTrue(report["evidence_references_resolved"])
        self.assertTrue(report["minimum_evidence_satisfied"])
        smoke = report["facets"]["smoke"]
        self.assertEqual(smoke["final_stage"], "reviewed-reread")
        self.assertEqual(smoke["success_exit"], 0)
        self.assertEqual(smoke["child_exit"], 2)
        self.assertEqual(smoke["wrapper_exit"], 2)
        self.assertFalse(smoke["command_executed"])
        self.assertIn("reviewed-reread exits are not the successful exit 0", "\n".join(report["problems"]))

    def test_empty_command_cannot_pass(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["purpose"]["mode"] = "return-review"
        request["smoke"] = passed_smoke(command="  ")
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        self.assertEqual(report["smoke_result"], "failed")
        self.assertFalse(report["ready_for_declared_method"])
        self.assertIn("smoke command text is empty", report["problems"])

    def test_evidence_root_must_be_the_transported_file(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        request["transport"] = [row for row in request["transport"] if row["path"] != "manifest.json"]
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        self.assertTrue(report["transport_valid"])
        self.assertTrue(report["runtime_dependencies_resolved"])
        self.assertFalse(report["evidence_references_resolved"])
        self.assertFalse(report["minimum_evidence_satisfied"])
        self.assertFalse(report["ready_for_declared_method"])
        self.assertIn("reference root is not transported", "\n".join(report["problems"]))

        changed = request_for(self.delivery, self.root / "out-changed-root", {"task.txt": b"task\n"})
        for row in changed["transport"]:
            if row["path"] == "manifest.json":
                row["sha256"] = "d" * 64
        code, report = self.check(changed)
        self.assertEqual(code, 0, report)
        self.assertFalse(report["transport_valid"])
        self.assertFalse(report["evidence_references_resolved"])
        self.assertFalse(report["ready_for_declared_method"])
        self.assertIn("reference root does not match the transported declaration", "\n".join(report["problems"]))

    def test_empty_required_manifest_supplies_no_material(self) -> None:
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        empty = checker.canonical({"schema": "artifact-manifest/1", "artifacts": []})
        (self.delivery / "manifest.json").write_bytes(empty)
        for row in request["transport"]:
            if row["path"] == "manifest.json":
                row["sha256"] = sha256(empty)
                row["bytes"] = len(empty)
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        self.assertTrue(report["transport_valid"])
        self.assertTrue(report["evidence_references_resolved"])
        self.assertFalse(report["minimum_evidence_satisfied"])
        self.assertFalse(report["ready_for_declared_method"])
        self.assertIn("resolved no evidence material", "\n".join(report["problems"]))
        task = report["facets"]["minimum"]["categories"][0]
        self.assertEqual(task["members"], [])

    def test_nonempty_nested_evidence_resolves_members(self) -> None:
        item = b"item"
        nested = {
            "schema": "artifact-manifest/1",
            "artifacts": [{"path": "nested/item.bin", "sha256": sha256(item), "bytes": len(item)}],
        }
        nested_bytes = checker.canonical(nested)
        pack = {
            "schema": "prime-pack-sources/1",
            "sources": [
                {
                    "path": "not-opened.txt",
                    "snapshot": "snapshots/top.json",
                    "sha256": sha256(nested_bytes),
                    "bytes": len(nested_bytes),
                }
            ],
        }
        pack_bytes = checker.canonical(pack)
        request = request_for(self.delivery, self.output, {"task.txt": b"task\n"})
        delivery_with(
            self.delivery,
            {
                "snapshots/top.json": nested_bytes,
                "nested/item.bin": item,
                "pack.json": pack_bytes,
            },
        )
        request["transport"].append({"path": "pack.json", "sha256": sha256(pack_bytes), "bytes": len(pack_bytes)})
        request["transport"].append(
            {"path": "snapshots/top.json", "sha256": sha256(nested_bytes), "bytes": len(nested_bytes)}
        )
        request["transport"].append({"path": "nested/item.bin", "sha256": sha256(item), "bytes": len(item)})
        request["references"] = [
            {"id": "pack", "format": "prime-pack-sources/1", "path": "pack.json", "follow_nested": True}
        ]
        request["evidence"] = categories(["pack"])
        code, report = self.check(request)
        self.assertEqual(code, 0, report)
        self.assertTrue(report["evidence_references_resolved"])
        self.assertTrue(report["minimum_evidence_satisfied"])
        self.assertTrue(report["ready_for_declared_method"])
        self.assertEqual(report["facets"]["evidence"]["references"][0]["members"], ["nested/item.bin"])

    def test_checker_source_does_not_launch_commands(self) -> None:
        text = (LAB / "colab_readiness.py").read_text(encoding="utf-8")
        self.assertNotIn("subprocess", text)
        self.assertNotIn("os.system", text)


def tool(script: Path, args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, "-B", str(script), *args],
        cwd=cwd,
        capture_output=True,
        timeout=60,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
    )


def copy_frozen_tools(repo: Path) -> dict[str, bytes]:
    files = {}
    for snapshot, rel in TOOL_COPIES.items():
        data = (SNAPSHOTS / snapshot).read_bytes()
        files[rel] = data
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    parser = subprocess.check_output(
        ["git", "-C", str(ROOT), "cat-file", "blob", f"{CUT}:labs/prime-support-pass01/prime_support.py"]
    )
    rel = "labs/prime-support-pass01/prime_support.py"
    files[rel] = parser
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(parser)
    expected = {
        "labs/prime-cycle-pass01/prime_cycle.py": "dd5319a46a88e05020ee7b0715b8edca26031066c3f2ee867f590a6056581338",
        "labs/batch-observation-pass01/batch_observe.py": "8bea18171b723650e8c0b07f5de334d2c5fd004c5d65c4fa8c4b85cf0bc830d4",
        "labs/prime-support-pass01/clerk_adapter.py": "2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4",
        "labs/prime-support-pass01/prime_support.py": "700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70",
        "labs/return-capture-pass01/return_capture.py": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
        "labs/return-capture-pass01/return_inspect.py": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
        "labs/prime-review-pass01/prime_review.py": "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0",
        "labs/review-packet-pass01/review_packet.py": "f658cbe48a3a76b908e5af0bcf0b7a68abc90571d983ca785e36667268f6ee72",
    }
    for rel, digest in expected.items():
        if sha256(files[rel]) != digest:
            raise AssertionError(f"frozen copy drifted: {rel}")
    return files


def run_synthetic_route(root: Path) -> dict:
    repo = root / "repo"
    book = repo / "00.kernel/00.00.10.work"
    lane = book / "0799.synthetic-readiness"
    evidence = lane / "evidence"
    evidence.mkdir(parents=True)
    files = copy_frozen_tools(repo)
    (repo / "note.txt").write_text("synthetic artifact\n", encoding="utf-8")
    (repo / "return.md").write_text(
        "Did\nThe disposable fixture captured a synthetic return.\n\nBlocked\nNone.\n\nNeed\nNone.\n",
        encoding="utf-8",
    )
    capture = repo / "labs/return-capture-pass01/return_capture.py"
    cycle = repo / "labs/prime-cycle-pass01/prime_cycle.py"
    reserved = tool(
        capture,
        [
            "reserve",
            "--book",
            str(book),
            "--submission",
            "synthetic-readiness-01",
            "--name",
            "synthetic-readiness",
            "--origin-book",
            "00.00.10.work",
            "--origin-page",
            "0799.synthetic-readiness",
            "--origin-batch",
            "05.01",
            "--expected-output",
            "note.txt",
            "--submitter",
            "Grok Builder 1",
            "--reviewer",
            "Codex Prime",
            "--release",
            "synthetic fixture; not a Director release",
        ],
        repo,
    )
    if reserved.returncode != 0:
        raise AssertionError(reserved.stderr.decode("utf-8", "replace") + reserved.stdout.decode("utf-8", "replace"))
    member = reserved.stdout.decode("utf-8").splitlines()[0].split(" ", 1)[1]
    captured = tool(
        capture,
        [
            "capture",
            "--book",
            str(book),
            "--submission",
            "synthetic-readiness-01",
            "--return-file",
            str(repo / "return.md"),
            "--source-root",
            str(repo),
            "--artifact",
            "note.txt|note.txt",
        ],
        repo,
    )
    if captured.returncode != 0:
        raise AssertionError(captured.stderr.decode("utf-8", "replace") + captured.stdout.decode("utf-8", "replace"))
    receipt_bytes = (book / member / "receipt.json").read_bytes()
    receipt = sha256(receipt_bytes)
    page_rel = "00.kernel/00.00.10.work/0799.synthetic-readiness/05.01.md"
    page_path = repo / page_rel
    page_path.write_text(
        "\n".join(
            [
                "# Synthetic readiness",
                "",
                "state: draft",
                "",
                "## Return pointer",
                "Execution: returned.",
                f"Member: {member}",
                f"Receipt: {receipt}",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    output_root = root / "cycle-output"
    journal = root / "journal"
    templates = output_root / "templates"
    output_root.mkdir()
    registration = {
        "schema": "prime-cycle-registration/1",
        "repository": str(repo),
        "book": "00.kernel/00.00.10.work",
        "book_label": "00.00.10.work",
        "source": {"kind": "live-file", "commit": None},
        "members_book": str(book),
        "output_root": str(output_root),
        "bounds": {"max_works": 1, "max_page_bytes": 262144, "max_output_bytes": 2097152},
        "works": [
            {
                "work_id": "synthetic-readiness",
                "page": page_rel,
                "pass": "05.01",
                "member": member,
                "goal": {
                    "goal_id": "fixture-goal",
                    "statement": "Show a dependency-complete frozen route can be read, recorded, and re-read.",
                },
                "agreement": {
                    "goal": "Show a dependency-complete frozen route can be read, recorded, and re-read.",
                    "scope": "One synthetic page in a disposable tree. No kernel change.",
                    "prime_discretion": "Prime may label the judgment synthetic and leave the goal open.",
                    "director_required": "No Director decision is required inside this fixture.",
                    "finish_criteria": [
                        {"id": "route", "text": "The route records awaiting-review and then reviewed."}
                    ],
                    "recorded_decisions": [],
                },
                "review_location": "00.kernel/00.00.10.work/0799.synthetic-readiness/evidence/reviews",
            }
        ],
    }
    registration_path = root / "registration.json"
    write_json(registration_path, registration)
    first = tool(
        cycle,
        [
            "read",
            "--registration",
            str(registration_path),
            "--json",
            "--templates",
            str(templates),
            "--journal-root",
            str(journal),
            "--caller",
            "readiness-fixture",
            "--note",
            "synthetic first read",
        ],
        repo,
    )
    if first.returncode not in (0, 1):
        raise AssertionError(
            f"first read exit {first.returncode}\n"
            + first.stdout.decode("utf-8", "replace")[-2000:]
            + first.stderr.decode("utf-8", "replace")[-2000:]
        )
    first_view = json.loads(first.stdout.decode("utf-8"))
    work = first_view["works"][0]
    if work["pass_state"] != "awaiting-review":
        raise AssertionError(json.dumps(work, indent=2)[:2000])
    template = json.loads((templates / "template-synthetic-readiness.json").read_text(encoding="utf-8"))
    template["attribution"]["actor_label"] = "Codex Prime"
    template["attribution"]["evidence"] = "SYNTHETIC fixture judgment. Not a Director release and not acceptance."
    judgment = template["judgment"]
    judgment["outcome"] = "continue"
    judgment["disposition"] = "accepted"
    judgment["pass_terminal"] = "finished"
    judgment["goal"]["terminal"] = "open"
    judgment["goal"]["evidence"] = []
    judgment["finding"] = "SYNTHETIC judgment for the readiness fixture."
    judgment["reasons"] = ["SYNTHETIC fixture judgment."]
    judgment["source_refs"] = ["synthetic page"]
    judgment["next_action"] = {
        "action_id": "note-only",
        "text": "SYNTHETIC: no further change.",
        "authorized_in_grant": False,
    }
    judgment["semantic_conflict"] = False
    judgment["sections"]["return_result"] = "SYNTHETIC captured return is present."
    judgment["sections"]["prime_finding"] = "SYNTHETIC finding for the readiness fixture."
    judgment["sections"]["within_direction"] = "SYNTHETIC judgment stays inside the fixture direction."
    judgment["sections"]["next_bounded_action"] = "SYNTHETIC: no further change."
    decision_path = root / "decision.json"
    write_json(decision_path, template)
    recorded = tool(
        cycle,
        [
            "record",
            "--registration",
            str(registration_path),
            "--decision",
            str(decision_path),
            "--journal-root",
            str(journal),
            "--caller",
            "readiness-fixture",
            "--note",
            "SYNTHETIC judgment",
        ],
        repo,
    )
    if recorded.returncode not in (0, 1):
        raise AssertionError(
            f"record exit {recorded.returncode}\n"
            + recorded.stdout.decode("utf-8", "replace")[-2000:]
            + recorded.stderr.decode("utf-8", "replace")[-2000:]
        )
    second = tool(
        cycle,
        [
            "read",
            "--registration",
            str(registration_path),
            "--json",
            "--journal-root",
            str(journal),
            "--caller",
            "readiness-fixture",
            "--note",
            "synthetic re-read",
        ],
        repo,
    )
    if second.returncode not in (0, 1):
        raise AssertionError(
            f"re-read exit {second.returncode}\n"
            + second.stdout.decode("utf-8", "replace")[-2000:]
            + second.stderr.decode("utf-8", "replace")[-2000:]
        )
    second_view = json.loads(second.stdout.decode("utf-8"))
    after = second_view["works"][0]
    if after["pass_state"] != "reviewed":
        raise AssertionError(json.dumps(after, indent=2)[:2000])
    ops = []
    ends = []
    for day in sorted(path for path in journal.iterdir() if path.is_dir()):
        for op in sorted(path for path in day.iterdir() if path.is_dir()):
            start = json.loads((op / "start.json").read_text(encoding="utf-8"))
            end_path = op / "end.json"
            end = json.loads(end_path.read_text(encoding="utf-8")) if end_path.is_file() else None
            ops.append(start["operation"])
            ends.append(None if end is None else end["machine"]["exit"])
    if ops != ["read", "record", "read"]:
        raise AssertionError(f"journal operations {ops}")
    if ends[-1] != second.returncode:
        # Keep both numbers. The checker will refuse to hide a difference.
        pass
    page_bytes = page_path.read_bytes()
    route = {
        "member": member,
        "receipt_sha256": receipt,
        "page_sha256": sha256(page_bytes),
        "page_bytes": page_bytes,
        "pass_state_before": work["pass_state"],
        "pass_state_after": after["pass_state"],
        "custody_role": after["custody"]["role"],
        "journal_operations": ops,
        "child_exit": ends[-1],
        "wrapper_exit": second.returncode,
        "first_exit": first.returncode,
        "record_exit": recorded.returncode,
        "end_exits": ends,
        "files": files,
        "registration": registration,
        "decision": template,
        "receipt_file": receipt_bytes,
        "contract": (SNAPSHOTS / "0007.blob").read_bytes(),
    }
    return route


def build_route_request(root: Path, route: dict) -> tuple[dict, Path]:
    delivery = root / "route-delivery"
    if delivery.exists():
        shutil.rmtree(delivery)
    files = dict(route["files"])
    files["evidence/page.md"] = route["page_bytes"]
    files["evidence/receipt.json"] = route["receipt_file"]
    files["evidence/task.md"] = b"Synthetic task: read, record, and re-read one frozen route.\n"
    files["evidence/director.txt"] = (
        b"Fixture constraint: The Director authorizes this bounded build. "
        b"This disposable page is not a second release.\n"
    )
    files["evidence/contract.md"] = route["contract"]
    files["evidence/route-log.json"] = checker.canonical(
        {
            "first_exit": route["first_exit"],
            "record_exit": route["record_exit"],
            "child_exit": route["child_exit"],
            "wrapper_exit": route["wrapper_exit"],
            "end_exits": route["end_exits"],
            "journal_operations": route["journal_operations"],
            "pass_state_before": route["pass_state_before"],
            "pass_state_after": route["pass_state_after"],
        }
    )
    files["evidence/capabilities.txt"] = (
        b"The route can read, record, and re-read with the frozen tools. "
        b"It cannot authorize work or prove the judgment true.\n"
    )
    files["evidence/fallback.txt"] = (
        b"Preserve the first failure. One read-only diagnostic and one named dependency check. "
        b"Manual fallback is not assisted success.\n"
    )
    files["evidence/return-route.txt"] = (
        f"Member: {route['member']}\nReceipt: {route['receipt_sha256']}\n".encode("utf-8")
    )
    listed = {
        rel: files[rel]
        for rel in (
            "evidence/page.md",
            "evidence/receipt.json",
            "evidence/task.md",
            "evidence/director.txt",
            "evidence/contract.md",
            "evidence/route-log.json",
            "evidence/capabilities.txt",
            "evidence/fallback.txt",
            "evidence/return-route.txt",
        )
    }
    artifact = manifest_for(listed)
    files["evidence/artifacts.json"] = checker.canonical(artifact)
    sources = {
        "schema": "prime-pack-sources/1",
        "sources": [
            {
                "path": rel,
                "snapshot": rel,
                "sha256": sha256(data),
                "bytes": len(data),
            }
            for rel, data in route["files"].items()
        ],
    }
    files["sources.json"] = checker.canonical(sources)
    delivery_with(delivery, files)
    output = root / "route-out"

    def dep(dep_id, rel, role, required, invokes, condition=None):
        data = files[rel]
        return {
            "id": dep_id,
            "path": rel,
            "sha256": sha256(data),
            "bytes": len(data),
            "role": role,
            "required": required,
            "needed_by": [],
            "invokes": invokes,
            "supply": "supplied",
            "condition": condition,
            "withhold_reason": None,
        }

    evidence_rows = []
    for name in checker.CATEGORIES:
        evidence_rows.append(
            {
                "category": name,
                "applicability": "required",
                "reason": f"{name} is bound in this synthetic route",
                "refs": ["artifacts"] if name != "source-index" else ["sources"],
            }
        )
    request = {
        "schema": checker.SCHEMA_REQUEST,
        "purpose": {
            "statement": "A dependency-complete frozen return-review route.",
            "mode": "return-review",
            "question": "Did the declared route reach reviewed with the frozen tools?",
            "role": "checker",
            "method": "read, synthetic judgment, record, reviewed re-read",
            "finish_boundary": "one synthetic fixture; no kernel change",
        },
        "surface": base_surface(),
        "delivery_root": str(delivery),
        "output": str(output),
        "transport": [
            {"path": rel, "sha256": sha256(data), "bytes": len(data)} for rel, data in sorted(files.items())
        ],
        "entry_points": [{"id": "cycle", "path": "labs/prime-cycle-pass01/prime_cycle.py"}],
        "dependencies": [
            dep("cycle", "labs/prime-cycle-pass01/prime_cycle.py", "subject-runtime", True, ["reader", "review"]),
            dep("reader", "labs/batch-observation-pass01/batch_observe.py", "subject-runtime", True, ["adapter", "parser", "inspector", "helper"]),
            dep("review", "labs/prime-review-pass01/prime_review.py", "subject-runtime", True, []),
            dep("adapter", "labs/prime-support-pass01/clerk_adapter.py", "reviewer-assistance", True, []),
            dep("parser", "labs/prime-support-pass01/prime_support.py", "reviewer-assistance", True, []),
            dep("inspector", "labs/return-capture-pass01/return_inspect.py", "subject-runtime", True, []),
            dep("helper", "labs/return-capture-pass01/return_capture.py", "subject-runtime", True, []),
            dep(
                "packet",
                "labs/review-packet-pass01/review_packet.py",
                "shared-subject-and-assistance",
                False,
                [],
                {"text": "packet command was not used on this route", "exercised": False},
            ),
        ],
        "evidence": evidence_rows,
        "references": [
            {
                "id": "artifacts",
                "format": "artifact-manifest/1",
                "path": "evidence/artifacts.json",
                "follow_nested": True,
            },
            {
                "id": "sources",
                "format": "prime-pack-sources/1",
                "path": "sources.json",
                "follow_nested": True,
            },
        ],
        "withholds": [],
        "smoke": passed_smoke(
            reason="SYNTHETIC frozen route reached reviewed",
            command="prime_cycle.py read --registration registration.json --json",
            child_exit=route["child_exit"],
            wrapper_exit=route["wrapper_exit"],
            page_sha256=route["page_sha256"],
            receipt_sha256=route["receipt_sha256"],
            pass_state_before=route["pass_state_before"],
            pass_state_after=route["pass_state_after"],
            journal_operations=route["journal_operations"],
            cutoff="after the reviewed re-read; no further operation was started",
        ),
        "failure_policy": policy(),
        "independent_checks": [
            {
                "id": "frozen-hashes",
                "text": "tool bytes matched the frozen snapshots before the route",
                "status": "present",
            },
            {
                "id": "packet-tests",
                "text": "review_packet tests were not rerun on this route",
                "status": "not-established",
            },
        ],
        "bounds": {"max_files": 80, "max_file_bytes": 2000000, "max_total_bytes": 8000000},
    }
    return request, delivery


class SyntheticRouteTests(unittest.TestCase):
    def test_frozen_route_is_ready_without_semantic_proof(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="colab-route-")
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        route = run_synthetic_route(root)
        self.assertEqual(route["pass_state_before"], "awaiting-review")
        self.assertEqual(route["pass_state_after"], "reviewed")
        self.assertEqual(route["custody_role"], "primary-current-candidate")
        self.assertEqual(route["journal_operations"], ["read", "record", "read"])
        request, _delivery = build_route_request(root, route)
        code, report, _ignored = run_check(request, root)
        self.assertEqual(code, 0, report)
        self.assertTrue(report["transport_valid"])
        self.assertTrue(report["runtime_dependencies_resolved"])
        self.assertTrue(report["evidence_references_resolved"])
        self.assertTrue(report["minimum_evidence_satisfied"])
        self.assertEqual(report["smoke_result"], "passed")
        self.assertTrue(report["ready_for_declared_method"])
        self.assertEqual(report["semantic_sufficiency"], "not-established")
        self.assertEqual(report["independent_proof"], "not-established")
        self.assertTrue(report["shared_component"])
        self.assertFalse(report["facets"]["smoke"]["command_executed"])
        self.assertFalse(report["exit_layers_differ"])
        self.assertIn(route["first_exit"], (0, 1))
        self.assertEqual(route["child_exit"], 0)
        self.assertEqual(route["wrapper_exit"], 0)
        self.assertEqual(report["facets"]["smoke"]["final_stage"], "reviewed-reread")
        self.assertEqual(report["facets"]["smoke"]["success_exit"], 0)
        self.assertEqual(report["facets"]["smoke"]["child_exit"], 0)
        self.assertEqual(report["facets"]["smoke"]["wrapper_exit"], 0)
        self.assertTrue(report["minimum_evidence_satisfied"])
        self.assertTrue(any(row["accounted"] for row in report["facets"]["runtime"]["entries"]))
        export = os.environ.get("COLAB_READINESS_SAMPLE")
        if export:
            target = Path(export)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(checker.canonical(report))
            log = target.with_name("route-log.json")
            log.write_bytes(
                checker.canonical(
                    {key: route[key] for key in (
                        "member",
                        "receipt_sha256",
                        "page_sha256",
                        "pass_state_before",
                        "pass_state_after",
                        "custody_role",
                        "journal_operations",
                        "child_exit",
                        "wrapper_exit",
                        "first_exit",
                        "record_exit",
                        "end_exits",
                    )}
                )
            )


if __name__ == "__main__":
    unittest.main()
