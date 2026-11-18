#!/usr/bin/env python3
"""Author cases for review-report-pass03. Not an independent run.

The identical-file case reloads pass02 and is a known failure, not coverage
of this successor. The other cases are author checks of the counter contract.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LAB = ROOT / "labs" / "review-report-pass03"
sys.path.insert(0, str(LAB))
import report  # noqa: E402

KEEP = Path(r"D:\librarian\temp\0512-0506-report")
KNOWN = KEEP / "known-failures" / "identical-files-pass02.json"
WORK = ROOT / "00.kernel" / "00.00.10.work"
PACK = WORK / "0512.prime-review"
MANIFEST = PACK / "evidence" / "pack05.06" / "source-manifest.json"
CONTRACT = PACK / "evidence" / "build05.06" / "CONTRACT.md"
PAGE = "0599.probe"
PASS = "05.01"
REVIEW = "rev-bound"
CONTRACT_SHA = "e5849352644b63c8f249546d4f5bd7ccad575218d9c2062db2f4814a55babc6c"
LIVE_NOTE = (
    "Bounded reviewer run passed; author six-test suite is attributed evidence, "
    "not independently rerun. Not all 39 independent assertions, new filed successor "
    "behavior or unsupported interruption were exercised."
)
LIVE_ATTENTION = [
    "agreement.goal is unknown",
    "agreement.scope is unknown",
    "agreement.prime_discretion is unknown",
    "agreement.director_required is unknown",
    "agreement.finish_criteria is unknown",
    "agreement.recorded_decisions is unknown",
]
LIVE_FILES = [
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/intake.json",
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/journal.json",
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/reviews/w4c5ae945c250d823/judgment.json",
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/reviews/w4c5ae945c250d823/record.json",
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/reviews/w4c5ae945c250d823/rendered.md",
    "app/README.md",
]
FOUR = PACK / "evidence" / "prime-review05.04" / "independent-artifact-count.json"
FIXTURE = PACK / "evidence" / "prime-review05.05" / "independent-identical-files.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def publication(status: str = "published") -> dict:
    return {
        "after_sha256": "aa",
        "before_sha256": "bb",
        "rendered_sha256": "cc",
        "review_id": REVIEW,
        "status": status,
        "target": f"{PAGE}/{PASS}.md",
    }


def journal_body(record_sha, status: str = "published", current: str = REVIEW) -> dict:
    pub = publication(status)
    return {
        "current": current,
        "publication": dict(pub),
        "published_target": dict(pub),
        "reviews": [{
            "judgment_sha256": "dd",
            "record_sha256": record_sha,
            "review_id": REVIEW,
        }],
        "schema": "workbook-review-journal/1",
    }


def judgment() -> dict:
    return {
        "answers": [],
        "disposition": "accepted",
        "finding": "The disposable note is present.",
        "findings": [],
        "gaps": [],
        "goal_terminal": "open",
        "next_action": "Hand back.",
        "operation": "continue",
        "pass_terminal": "finished",
        "reasons": ["The return names the note."],
        "sections": {"limits": None, "tests_note": "bounded note", "tests_passed": True},
    }


def record_body(attention, body: dict) -> dict:
    return {
        "attention": attention,
        "custody": "missing",
        "director_text": None,
        "eligible_for_custody_completion": False,
        "holds": [],
        "judgment": body,
        "prime_review_effective": "attention",
        "rendered": "tests_passed: true\n",
        "successor_of": None,
    }


def run(args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(args, cwd=str(ROOT), env=env, capture_output=True, shell=False)


def row(path, root="book", digest="a" * 64, size=4, role="assignment", declared=False) -> dict:
    return {
        "bytes": size,
        "declared_bytes": size if declared else None,
        "declared_sha256": digest if declared else None,
        "path": path,
        "role": role,
        "root": root,
        "sha256": digest,
    }


def intake(rows, measurement="complete", findings=None) -> dict:
    return {
        "findings": [] if findings is None else findings,
        "form": {"bindings": {"rows": rows}},
        "measurement": measurement,
    }


class ReportPass03(unittest.TestCase):
    def setUp(self) -> None:
        self.books: list[Path] = []
        self.core = report.core_call

    def tearDown(self) -> None:
        report.core_call = self.core
        report.p2.core_call = self.core
        KEEP.mkdir(parents=True, exist_ok=True)
        for path in self.books:
            dest = KEEP / path.name
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(path, dest, dirs_exist_ok=True)
            shutil.rmtree(path, ignore_errors=True)

    def book(self, name: str) -> Path:
        path = Path(tempfile.mkdtemp(prefix=f"rr0506-{name}-"))
        self.books.append(path)
        return path

    def plant(self, book: Path, body: dict) -> str:
        raw = pretty(body)
        digest = sha(raw)
        root = book / "workbook-review" / PAGE / PASS
        write(root / "journal.json", pretty(journal_body(digest)))
        write(root / "reviews" / REVIEW / "record.json", raw)
        return digest

    def stub(self, body: dict, commands: list[str], mutate=None, rows=None) -> None:
        def core_call(_code_root, _book, _source, _pass_id, command: str):
            commands.append(command)
            if mutate is not None:
                mutate(command)
            payload = {
                "accepted": False,
                "approved": False,
                "authority": "none",
                "closes_work": False,
                "command": command,
                "current": REVIEW,
                "custody": "missing",
                "exit": 0,
                "findings": [],
                "form": {"bindings": {"rows": [] if rows is None else rows}},
                "instance_id": "inst-1",
                "judgment": body,
                "measurement": "complete",
                "page": PAGE,
                "pass": PASS,
                "publication": {
                    "rendered_sha256": "cc",
                    "review_id": REVIEW,
                    "status": "published",
                },
                "releases_action": False,
                "rendered_ok": True,
                "review_id": REVIEW,
                "schema": "workbook-review-result/1",
                "stale": False,
                "target_state": "verified",
                "task_association": "not-established",
                "unknowns": [],
            }
            return subprocess.CompletedProcess([], 0, pretty(payload), b"")

        report.core_call = core_call

    def options(self, book: Path) -> dict:
        return {"book": str(book), "code_root": str(ROOT), "pass": PASS, "source": PAGE}

    def observe(self, book: Path) -> dict:
        return report.finish(report.observe(self.options(book)))

    def assert_freeze(self) -> None:
        manifest = json.loads(MANIFEST.read_bytes().decode("utf-8"))
        for item in manifest["files"]:
            data = (ROOT / item["path"]).read_bytes()
            self.assertEqual(len(data), item["bytes"], item["path"])
            self.assertEqual(sha(data), item["sha256"], item["path"])
        contract = CONTRACT.read_bytes()
        self.assertEqual(len(contract), 12396)
        self.assertEqual(sha(contract), CONTRACT_SHA)
        self.assertEqual(contract.count(b"\r"), 0)

    def test_known_failure_identical_files_are_not_independent_coverage(self) -> None:
        self.assert_freeze()
        saved = json.loads(KNOWN.read_bytes().decode("utf-8"))
        fixture = json.loads(FIXTURE.read_bytes().decode("utf-8"))
        spec = importlib.util.spec_from_file_location(
            "review_report_pass02_known_case",
            ROOT / "labs" / "review-report-pass02" / "report.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        reported = module.unique_files(fixture["fixture"])
        self.assertEqual(reported["count"], 1)
        self.assertEqual(reported["bytes"], 4)
        self.assertEqual(reported["scope"], "unique-physical-files")
        self.assertEqual(reported, saved["unique_files"])
        self.assertTrue(saved["matches_disclosed_report"])
        self.assertEqual(saved["label"], "known-failure reproduction; not independent coverage")
        self.assertEqual(fixture["actual_distinct_paths"], 2)
        self.assertEqual(fixture["actual_total_bytes"], 8)

    def test_author_two_distinct_equal_content_paths(self) -> None:
        fixture = json.loads(FIXTURE.read_bytes().decode("utf-8"))
        counted = report.artifacts_of(intake(fixture["fixture"]))
        addressed = counted["addressed_sources"]
        content = counted["content_blobs"]
        physical = counted["physical_files"]
        self.assertEqual(addressed["count"], 2)
        self.assertEqual(addressed["bytes"], 8)
        self.assertEqual(addressed["scope"], "addressed-source-paths")
        self.assertNotIn("reason", addressed)
        self.assertEqual(content["count"], 1)
        self.assertEqual(content["bytes"], 4)
        self.assertEqual(content["scope"], "content-sha256")
        self.assertIsNone(physical["count"])
        self.assertIsNone(physical["bytes"])
        self.assertEqual(physical["provenance"], "not-established")
        self.assertEqual(physical["reason"], report.REASON_PHYSICAL)
        self.assertEqual(counted["count"], 0)
        self.assertEqual(counted["bytes"], 0)
        self.assertEqual(counted["intake_roles"]["count"], 2)
        self.assertEqual(counted["intake_roles"]["bytes"], 8)
        self.assertNotIn("unique_files", counted)
        book = self.book("two")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))
        self.stub(body, [], rows=fixture["fixture"])
        result = self.observe(book)
        self.assertEqual(result["schema"], "review-report/3")
        self.assertEqual(result["state"], "readable")
        self.assertNotIn("unique_files", result["artifacts"])
        self.assertIn(
            "addressed_sources: count 2, bytes 8, provenance current-measured, scope addressed-source-paths\n",
            result["projection"],
        )
        self.assertIn(
            "content_blobs: count 1, bytes 4, provenance current-measured, scope content-sha256\n",
            result["projection"],
        )
        self.assertIn("physical_files: count unknown, bytes unknown, provenance not-established", result["projection"])
        self.assertIn(report.REASON_PHYSICAL, result["projection"])
        self.assertNotIn("unique_files:", result["projection"])
        self.assertNotIn("unique-physical-files", result["projection"])
        self.assertIn(report.OBSERVATION_LIMIT, result["projection"])

    def test_author_repeated_roles_share_one_address(self) -> None:
        rows = [
            row("a.txt", role="assignment"),
            row("a.txt", role="artifact", declared=True),
        ]
        counted = report.artifacts_of(intake(rows))
        self.assertEqual(counted["addressed_sources"]["count"], 1)
        self.assertEqual(counted["addressed_sources"]["bytes"], 4)
        self.assertEqual(counted["content_blobs"]["count"], 1)
        self.assertEqual(counted["content_blobs"]["bytes"], 4)
        self.assertEqual(counted["intake_roles"]["count"], 2)
        self.assertEqual(counted["intake_roles"]["bytes"], 8)
        self.assertEqual(counted["count"], 1)
        self.assertEqual(counted["bytes"], 4)
        self.assertEqual(counted["measured_artifact_rows"]["count"], 1)

    def test_author_same_relative_path_in_different_roots(self) -> None:
        rows = [row("a.txt", root="book-a"), row("a.txt", root="book-b")]
        counted = report.artifacts_of(intake(rows))
        self.assertEqual(counted["addressed_sources"]["count"], 2)
        self.assertEqual(counted["addressed_sources"]["bytes"], 8)
        self.assertEqual(counted["content_blobs"]["count"], 1)
        self.assertEqual(counted["content_blobs"]["bytes"], 4)
        self.assertIsNone(counted["physical_files"]["count"])

    def test_author_missing_path_identity_blocks_the_addressed_total(self) -> None:
        rows = [
            row("a.txt", digest="a" * 64, size=4),
            {"bytes": 4, "role": "submission", "root": "book", "sha256": "b" * 64},
        ]
        counted = report.artifacts_of(intake(rows))
        self.assertIsNone(counted["addressed_sources"]["count"])
        self.assertIsNone(counted["addressed_sources"]["bytes"])
        self.assertEqual(counted["addressed_sources"]["reason"], report.REASON_ADDRESSED_MISSING)
        self.assertEqual(counted["content_blobs"]["count"], 2)
        self.assertEqual(counted["content_blobs"]["bytes"], 8)
        self.assertEqual(counted["intake_roles"]["count"], 2)
        self.assertEqual(counted["intake_roles"]["bytes"], 8)

    def test_author_identical_hashes_without_paths(self) -> None:
        rows = [
            {"bytes": 4, "role": "assignment", "sha256": "a" * 64},
            {"bytes": 4, "role": "submission", "sha256": "a" * 64},
        ]
        counted = report.artifacts_of(intake(rows))
        self.assertIsNone(counted["addressed_sources"]["count"])
        self.assertEqual(counted["addressed_sources"]["reason"], report.REASON_ADDRESSED_MISSING)
        self.assertEqual(counted["content_blobs"]["count"], 1)
        self.assertEqual(counted["content_blobs"]["bytes"], 4)
        self.assertIsNone(counted["physical_files"]["count"])

    def test_author_distinct_contents(self) -> None:
        rows = [row("a.txt", digest="a" * 64, size=4), row("b.txt", digest="b" * 64, size=8)]
        counted = report.artifacts_of(intake(rows))
        self.assertEqual(counted["addressed_sources"]["count"], 2)
        self.assertEqual(counted["addressed_sources"]["bytes"], 12)
        self.assertEqual(counted["content_blobs"]["count"], 2)
        self.assertEqual(counted["content_blobs"]["bytes"], 12)
        self.assertIsNone(counted["physical_files"]["count"])

    def test_author_null_measurement_and_empty_rows(self) -> None:
        blank = report.artifacts_of(None)
        self.assertIsNone(blank["addressed_sources"]["count"])
        self.assertEqual(blank["addressed_sources"]["reason"], report.REASON_ADDRESSED_MEASUREMENT)
        self.assertEqual(blank["content_blobs"]["reason"], report.REASON_CONTENT_MEASUREMENT)
        self.assertEqual(blank["physical_files"]["reason"], report.REASON_PHYSICAL)
        self.assertIsNone(blank["count"])
        incomplete = report.artifacts_of(intake([row("a.txt")], measurement="incomplete"))
        self.assertIsNone(incomplete["addressed_sources"]["count"])
        self.assertIsNone(incomplete["content_blobs"]["count"])
        self.assertEqual(incomplete["rows"][0]["path"], "a.txt")
        self.assertIsNone(incomplete["intake_roles"]["count"])
        empty = report.artifacts_of(intake([]))
        self.assertEqual(empty["addressed_sources"]["count"], 0)
        self.assertEqual(empty["addressed_sources"]["bytes"], 0)
        self.assertNotIn("reason", empty["addressed_sources"])
        self.assertEqual(empty["content_blobs"]["count"], 0)
        self.assertEqual(empty["content_blobs"]["bytes"], 0)
        self.assertIsNone(empty["physical_files"]["count"])
        self.assertEqual(empty["physical_files"]["reason"], report.REASON_PHYSICAL)

    def test_author_path_strings_are_not_normalized(self) -> None:
        rows = [
            row("a.txt", root="book"),
            row("./a.txt", root="book"),
            row("A.txt", root="book"),
            row("a.txt", root="Book"),
        ]
        counted = report.artifacts_of(intake(rows))
        self.assertEqual(counted["addressed_sources"]["count"], 4)
        self.assertEqual(counted["addressed_sources"]["bytes"], 16)
        self.assertEqual(counted["content_blobs"]["count"], 1)
        self.assertEqual(counted["content_blobs"]["bytes"], 4)
        self.assertIn("no slash folding", counted["addressed_sources"]["assumption"])

    def test_author_size_disagreement_and_boolean_bytes(self) -> None:
        same_path = [row("a.txt", size=4), row("a.txt", size=4)]
        same_path[1]["bytes"] = 5
        counted = report.artifacts_of(intake(same_path))
        self.assertEqual(counted["addressed_sources"]["count"], 1)
        self.assertIsNone(counted["addressed_sources"]["bytes"])
        self.assertEqual(counted["addressed_sources"]["reason"], report.REASON_ADDRESSED_SIZE)
        pair = [row("a.txt", size=4), row("b.txt", size=4)]
        pair[1]["bytes"] = 5
        counted = report.artifacts_of(intake(pair))
        self.assertEqual(counted["addressed_sources"]["count"], 2)
        self.assertEqual(counted["addressed_sources"]["bytes"], 9)
        self.assertEqual(counted["content_blobs"]["count"], 1)
        self.assertIsNone(counted["content_blobs"]["bytes"])
        self.assertEqual(counted["content_blobs"]["reason"], report.REASON_CONTENT_SIZE)
        flagged = row("a.txt", size=4)
        flagged["bytes"] = True
        counted = report.artifacts_of(intake([flagged]))
        self.assertEqual(counted["addressed_sources"]["count"], 1)
        self.assertIsNone(counted["addressed_sources"]["bytes"])
        self.assertEqual(counted["content_blobs"]["count"], 1)
        self.assertIsNone(counted["content_blobs"]["bytes"])

    def test_author_uppercase_hash_blocks_the_content_total(self) -> None:
        rows = [row("a.txt", digest="A" * 64, size=4), row("b.txt", digest="b" * 64, size=4)]
        counted = report.artifacts_of(intake(rows))
        self.assertEqual(counted["addressed_sources"]["count"], 2)
        self.assertEqual(counted["addressed_sources"]["bytes"], 8)
        self.assertIsNone(counted["content_blobs"]["count"])
        self.assertEqual(counted["content_blobs"]["reason"], report.REASON_CONTENT_MISSING)

    def test_author_digest_mismatch_before_missing_record(self) -> None:
        book = self.book("digest")
        root = book / "workbook-review" / PAGE / PASS
        seen: list[str] = []
        original = report.p2.p1.read_regular

        def wrapped(path):
            seen.append(str(path))
            return original(path)

        report.p2.p1.read_regular = wrapped
        try:
            write(root / "journal.json", pretty(journal_body("b" * 64)))
            got, why = report.checked_record(
                str(book), PAGE, PASS, REVIEW, "a" * 64, {"judgment": {}}, {"judgment": {}},
            )
            self.assertIsNone(got)
            self.assertEqual(why, "digest-mismatch")
            journal = json.loads((root / "journal.json").read_bytes().decode("utf-8"))
            journal["reviews"][0]["record_sha256"] = 1
            write(root / "journal.json", pretty(journal))
            _got, why = report.checked_record(
                str(book), PAGE, PASS, REVIEW, "a" * 64, {"judgment": {}}, {"judgment": {}},
            )
            self.assertEqual(why, "digest-mismatch")
            journal["reviews"][0].pop("record_sha256")
            write(root / "journal.json", pretty(journal))
            _got, why = report.checked_record(
                str(book), PAGE, PASS, REVIEW, "a" * 64, {"judgment": {}}, {"judgment": {}},
            )
            self.assertEqual(why, "digest-mismatch")
        finally:
            report.p2.p1.read_regular = original
        self.assertFalse((root / "reviews" / REVIEW / "record.json").exists())
        self.assertTrue(any(item.endswith("journal.json") for item in seen))
        self.assertFalse(any(item.endswith("record.json") for item in seen))

    def test_author_journal_current_changed_during_read(self) -> None:
        book = self.book("current")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))

        def mutate(command: str) -> None:
            if command != "read":
                return
            path = book / "workbook-review" / PAGE / PASS / "journal.json"
            journal = json.loads(path.read_bytes().decode("utf-8"))
            journal["current"] = "other-id"
            write(path, pretty(journal))

        commands: list[str] = []
        self.stub(body, commands, mutate=mutate)
        result = self.observe(book)
        raw = pretty(result)
        write(KEEP / "hostile-latest" / "current-changed.json", raw)
        first = KEEP / "hostile-first" / "current-changed.json"
        if not first.exists():
            write(first, raw)
        self.assertEqual(commands, ["inspect", "read", "recover"])
        self.assertEqual(result["state"], "held")
        self.assertFalse(result["observation"]["stable"])
        self.assertEqual(result["observation"]["status"], "unstable")
        self.assertEqual(result["review_id"], REVIEW)
        self.assertEqual(result["attention"]["state"], "not-exposed")
        self.assertNotIn(b"FIRST CUT", raw)
        self.assertIn("attention: not exposed", result["projection"])

    def test_author_finish_recheck_withholds_attention(self) -> None:
        book = self.book("finish")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))
        self.stub(body, [])
        observed = report.observe(self.options(book))
        self.assertEqual(observed["attention"]["lines"], ["FIRST CUT"])
        path = book / "workbook-review" / PAGE / PASS / "journal.json"
        journal = json.loads(path.read_bytes().decode("utf-8"))
        journal["publication"]["target"] = "other.md"
        journal["published_target"]["target"] = "other.md"
        write(path, pretty(journal))
        finished = report.finish(observed)
        raw = pretty(finished)
        self.assertEqual(finished["state"], "held")
        self.assertFalse(finished["observation"]["stable"])
        self.assertNotIn(b"FIRST CUT", raw)
        self.assertIn("attention: not exposed", finished["projection"])
        self.assertIn(report.OBSERVATION_LIMIT, finished["projection"])

    def test_author_four_role_row_totals_keep_their_scopes(self) -> None:
        disclosed = json.loads(FOUR.read_bytes().decode("utf-8"))
        counted = report.artifacts_of(intake(disclosed["observed"]["rows"]))
        self.assertEqual(counted["count"], 1)
        self.assertEqual(counted["bytes"], 4)
        self.assertEqual(counted["scope"], "manifest-declared-artifact-entries")
        self.assertEqual(counted["measured_artifact_rows"]["count"], 1)
        self.assertEqual(counted["measured_artifact_rows"]["bytes"], 4)
        self.assertEqual(counted["intake_roles"]["count"], 4)
        self.assertEqual(counted["intake_roles"]["bytes"], 64)
        self.assertEqual(counted["intake_roles"]["label"], "intake role rows; not a declared artifact total")
        self.assertEqual(counted["hash_match"], 1)
        self.assertEqual(counted["intake_roles"]["not_verified"], 3)
        self.assertEqual(counted["addressed_sources"]["count"], 4)
        self.assertEqual(counted["addressed_sources"]["bytes"], 64)
        self.assertEqual(counted["addressed_sources"]["scope"], "addressed-source-paths")
        self.assertEqual(counted["content_blobs"]["count"], 4)
        self.assertEqual(counted["content_blobs"]["bytes"], 64)
        self.assertEqual(counted["content_blobs"]["scope"], "content-sha256")
        self.assertIsNone(counted["physical_files"]["count"])
        self.assertNotIn("unique_files", counted)

    def test_author_refusal_does_not_call_the_core(self) -> None:
        proc = run([str(PY), "-B", str(LAB / "report.py")])
        self.assertEqual(proc.returncode, 2)
        self.assertTrue(proc.stderr.startswith(b"refused:"))
        payload = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(payload["schema"], "review-report/3")
        self.assertEqual(payload["state"], "refused")
        self.assertNotIn("unique_files", payload["artifacts"])
        self.assertEqual(payload["artifacts"]["physical_files"]["reason"], report.REASON_PHYSICAL)
        self.assertNotIn("unique_files:", payload["projection"])
        empty = self.book("empty-root")
        proc = run([
            str(PY), "-B", str(LAB / "report.py"),
            "--code-root", str(empty),
            "--book", str(self.book("empty-book")),
            "--source", PAGE,
            "--pass", PASS,
        ])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"pin mismatch", proc.stderr)
        self.assertFalse((empty / "app").exists())

    def test_author_counters_do_not_stat(self) -> None:
        fixture = json.loads(FIXTURE.read_bytes().decode("utf-8"))
        calls: list[str] = []

        def boom(*_args, **_kwargs):
            calls.append("probe")
            raise AssertionError("filesystem probe")

        originals = {
            "stat": os.stat,
            "lstat": os.lstat,
            "listdir": os.listdir,
            "path_stat": Path.stat,
            "open": Path.open,
            "read_bytes": Path.read_bytes,
        }
        os.stat = boom
        os.lstat = boom
        os.listdir = boom
        Path.stat = boom
        Path.open = boom
        Path.read_bytes = boom
        try:
            counted = report.artifacts_of(intake(fixture["fixture"]))
        finally:
            os.stat = originals["stat"]
            os.lstat = originals["lstat"]
            os.listdir = originals["listdir"]
            Path.stat = originals["path_stat"]
            Path.open = originals["open"]
            Path.read_bytes = originals["read_bytes"]
        self.assertEqual(calls, [])
        self.assertEqual(counted["addressed_sources"]["count"], 2)
        self.assertEqual(counted["addressed_sources"]["bytes"], 8)


class LiveReads(unittest.TestCase):
    def test_live_0522_05_13_pair_matches_and_does_not_write(self) -> None:
        before = {rel: sha((ROOT / rel).read_bytes()) for rel in LIVE_FILES}
        readme_before = before["app/README.md"]
        command = [
            str(PY), "-B", str(LAB / "report.py"),
            "--code-root", str(ROOT),
            "--book", str(WORK),
            "--source", "0522.review-construction",
            "--pass", "05.13",
        ]
        first = run(command)
        second = run(command)
        after = {rel: sha((ROOT / rel).read_bytes()) for rel in LIVE_FILES}
        self.assertEqual(before, after)
        self.assertEqual(readme_before, sha((ROOT / "app" / "README.md").read_bytes()))
        manifest = json.loads(MANIFEST.read_bytes().decode("utf-8"))
        for item in manifest["files"]:
            self.assertEqual(sha((ROOT / item["path"]).read_bytes()), item["sha256"], item["path"])
        self.assertEqual(first.returncode, second.returncode)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.stderr, b"")
        self.assertEqual(second.stderr, b"")
        payload = json.loads(first.stdout.decode("utf-8"))
        self.assertEqual(payload["schema"], "review-report/3")
        self.assertEqual(payload["review_id"], "w4c5ae945c250d823")
        self.assertEqual(payload["custody"], "missing")
        self.assertEqual(payload["authority"], "none")
        self.assertFalse(payload["work_complete"])
        self.assertFalse(payload["action_released"])
        self.assertFalse(payload["accepted"])
        self.assertFalse(payload["approved"])
        self.assertFalse(payload["closes_work"])
        self.assertFalse(payload["releases_action"])
        self.assertEqual(payload["tests_note"]["text"], LIVE_NOTE)
        self.assertEqual(payload["tests_passed"]["value"], True)
        self.assertFalse(payload["tests_passed"]["proof_of_all_tests"])
        self.assertFalse(payload["tests_passed"]["proof_of_requirements"])
        self.assertEqual(payload["claims"]["state"], "not-recorded")
        self.assertEqual(payload["claims"]["rows"], [])
        self.assertEqual(payload["attention"]["lines"], LIVE_ATTENTION)
        for line in LIVE_ATTENTION:
            self.assertIn(line, payload["projection"])
        self.assertIn(LIVE_NOTE, payload["projection"])
        self.assertEqual(payload["artifacts"]["scope"], "manifest-declared-artifact-entries")
        self.assertEqual(payload["artifacts"]["intake_roles"]["scope"], "full-intake-role-rows")
        self.assertNotIn("unique_files", payload["artifacts"])
        self.assertNotIn("unique_files:", payload["projection"])
        self.assertNotIn("unique-physical-files", payload["projection"])
        physical = payload["artifacts"]["physical_files"]
        self.assertIsNone(physical["count"])
        self.assertIsNone(physical["bytes"])
        self.assertEqual(physical["reason"], report.REASON_PHYSICAL)
        self.assertEqual(payload["artifacts"]["measurement"], "complete")
        self.assertEqual(payload["artifacts"]["addressed_sources"]["count_state"], "measured")
        self.assertEqual(payload["artifacts"]["content_blobs"]["count_state"], "measured")
        self.assertIn(report.OBSERVATION_LIMIT, payload["projection"])
        if payload["stale"]:
            self.assertEqual(payload["state"], "stale")
            self.assertEqual(payload["exit"], 1)
        else:
            self.assertEqual(payload["state"], "readable")
            self.assertEqual(payload["exit"], 0)
            self.assertFalse(payload["stale"])
            self.assertTrue(payload["observation"]["stable"])
            self.assertEqual(payload["disposition"], "accepted")
        out = KEEP / "current-review"
        write(out / "report.json", first.stdout)
        write(out / "report-second.stdout", second.stdout)
        summary = {
            "exit": payload["exit"],
            "state": payload["state"],
            "stale": payload["stale"],
            "review_id": payload["review_id"],
            "disposition": payload["disposition"],
            "custody": payload["custody"],
            "authority": payload["authority"],
            "work_complete": payload["work_complete"],
            "action_released": payload["action_released"],
            "publication_class": payload["publication"]["class"],
            "publication_status": payload["publication"]["status"],
            "observation_status": payload["observation"]["status"],
            "observation_stable": payload["observation"]["stable"],
            "declared_count": payload["artifacts"]["count"],
            "declared_bytes": payload["artifacts"]["bytes"],
            "measured_count": payload["artifacts"]["measured_artifact_rows"]["count"],
            "measured_bytes": payload["artifacts"]["measured_artifact_rows"]["bytes"],
            "addressed_count": payload["artifacts"]["addressed_sources"]["count"],
            "addressed_bytes": payload["artifacts"]["addressed_sources"]["bytes"],
            "addressed_scope": payload["artifacts"]["addressed_sources"]["scope"],
            "content_count": payload["artifacts"]["content_blobs"]["count"],
            "content_bytes": payload["artifacts"]["content_blobs"]["bytes"],
            "content_scope": payload["artifacts"]["content_blobs"]["scope"],
            "physical_count": payload["artifacts"]["physical_files"]["count"],
            "physical_reason": payload["artifacts"]["physical_files"]["reason"],
            "intake_count": payload["artifacts"]["intake_roles"]["count"],
            "intake_bytes": payload["artifacts"]["intake_roles"]["bytes"],
            "hash_match": payload["artifacts"]["hash_match"],
            "hash_mismatch": payload["artifacts"]["hash_mismatch"],
            "not_verified": payload["artifacts"]["not_verified"],
            "measurement": payload["artifacts"]["measurement"],
        }
        write(out / "summary.json", pretty(summary))


if __name__ == "__main__":
    unittest.main()
