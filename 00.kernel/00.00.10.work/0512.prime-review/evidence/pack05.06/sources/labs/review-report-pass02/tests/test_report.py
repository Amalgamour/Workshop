#!/usr/bin/env python3
"""Author cases for review-report-pass02. Not an independent run.

Known pass01 reproductions are labeled in the test names. The two cases named
hostile are new author cases, not independent coverage.
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

ROOT = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LAB = ROOT / "labs" / "review-report-pass02"
sys.path.insert(0, str(LAB))
import report  # noqa: E402

KEEP = Path(r"D:\librarian\temp\0512-0505-report")
KNOWN = KEEP / "known-failures"
WORK = ROOT / "00.kernel" / "00.00.10.work"
PAGE = "0599.probe"
PASS = "05.01"
REVIEW = "rev-bound"
SENTINEL = "UNVERIFIED SECOND-CUT ATTENTION"
MANIFEST = WORK / "0512.prime-review" / "evidence" / "pack05.05" / "source-manifest.json"
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
LIVE_PATHS = [
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/intake.json",
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/journal.json",
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/reviews/w4c5ae945c250d823/judgment.json",
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/reviews/w4c5ae945c250d823/record.json",
    "00.kernel/00.00.10.work/workbook-review/0522.review-construction/05.13/reviews/w4c5ae945c250d823/rendered.md",
    "00.kernel/00.00.10.work/workbook-review/0512.prime-review/05.04/intake.json",
    "00.kernel/00.00.10.work/workbook-review/0512.prime-review/05.04/journal.json",
    "00.kernel/00.00.10.work/workbook-review/0512.prime-review/05.04/reviews/weffe9a51780b52b3/judgment.json",
    "00.kernel/00.00.10.work/workbook-review/0512.prime-review/05.04/reviews/weffe9a51780b52b3/record.json",
    "00.kernel/00.00.10.work/workbook-review/0512.prime-review/05.04/reviews/weffe9a51780b52b3/rendered.md",
    "labs/review-report-pass01/report.py",
    "labs/review-report-pass01/tests/test_report.py",
    "labs/review-report-pass01/README.md",
    "labs/review-report-pass01/PRIME-USE.md",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def tree_hashes(root: Path) -> dict[str, str]:
    found = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            path = Path(dirpath) / name
            found[str(path)] = file_sha(path)
    return found


def judgment(finding: str = "The disposable note is present.", disposition: str = "accepted", tests_passed=True, tests_note: str = "bounded note") -> dict:
    return {
        "answers": [],
        "disposition": disposition,
        "finding": finding,
        "findings": [],
        "gaps": [],
        "goal_terminal": "open",
        "next_action": "Hand back.",
        "operation": "continue",
        "pass_terminal": "finished",
        "reasons": ["The return names the note."],
        "sections": {"limits": None, "tests_note": tests_note, "tests_passed": tests_passed},
    }


def record_body(attention, body: dict, rendered: str = "tests_passed: true\n") -> dict:
    return {
        "attention": attention,
        "custody": "missing",
        "director_text": None,
        "eligible_for_custody_completion": False,
        "holds": [],
        "judgment": body,
        "prime_review_effective": "attention",
        "rendered": rendered,
        "successor_of": None,
    }


def publication(status: str = "published") -> dict:
    return {
        "after_sha256": "aa",
        "before_sha256": "bb",
        "rendered_sha256": "cc",
        "review_id": REVIEW,
        "status": status,
        "target": f"{PAGE}/{PASS}.md",
    }


def journal_body(record_sha: str, status: str = "published", current: str = REVIEW) -> dict:
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


def run(args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(args, cwd=str(ROOT), env=env, capture_output=True, shell=False)


def save_raw(name: str, payload: bytes) -> None:
    first = KEEP / "hostile-first" / name
    if not first.exists():
        write(first, payload)
    write(KEEP / "hostile-latest" / name, payload)


class ReportPass02(unittest.TestCase):
    def setUp(self) -> None:
        self.books: list[Path] = []
        self.core = report.core_call

    def tearDown(self) -> None:
        report.core_call = self.core
        KEEP.mkdir(parents=True, exist_ok=True)
        for path in self.books:
            dest = KEEP / path.name
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(path, dest, dirs_exist_ok=True)
            shutil.rmtree(path, ignore_errors=True)

    def book(self, name: str) -> Path:
        path = Path(tempfile.mkdtemp(prefix=f"rr0505-{name}-"))
        self.books.append(path)
        return path

    def plant(self, book: Path, body: dict, digest: str | None = None, status: str = "published") -> str:
        raw = pretty(body)
        digest = sha(raw) if digest is None else digest
        root = book / "workbook-review" / PAGE / PASS
        write(root / "journal.json", pretty(journal_body(digest, status)))
        write(root / "reviews" / REVIEW / "record.json", raw)
        return digest

    def stub(self, body: dict, commands: list[str], mutate=None, **fields) -> None:
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
                "exit": fields.get("exit", 0),
                "findings": fields.get("findings", []),
                "form": {"bindings": {"rows": fields.get("rows", [])}},
                "instance_id": "inst-1",
                "judgment": body,
                "measurement": fields.get("measurement", "complete"),
                "page": PAGE,
                "pass": PASS,
                "publication": {
                    "rendered_sha256": "cc",
                    "review_id": REVIEW,
                    "status": fields.get("status", "published"),
                },
                "releases_action": False,
                "rendered_ok": True,
                "review_id": REVIEW,
                "schema": "workbook-review-result/1",
                "stale": fields.get("stale", False),
                "target_state": fields.get("target_state", "verified"),
                "task_association": "not-established",
                "unknowns": [],
            }
            return subprocess.CompletedProcess([], payload["exit"], pretty(payload), b"")

        report.core_call = core_call

    def options(self, book: Path) -> dict:
        return {"book": str(book), "code_root": ROOT, "pass": PASS, "source": PAGE}

    def observe(self, book: Path) -> dict:
        return report.finish(report.observe(self.options(book)))

    def test_known_failure_files_record_pass01(self) -> None:
        saved = json.loads((KNOWN / "p1-pass01-result.json").read_text(encoding="utf-8"))
        counted = json.loads((KNOWN / "p2-pass01-result.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["result"], "ok")
        self.assertTrue(saved["second_cut_exposed"])
        self.assertEqual(saved["attention"], [SENTINEL])
        self.assertTrue(saved["constructed_second_matches_disclosed_hash"])
        self.assertEqual(counted["count"], 4)
        self.assertEqual(counted["bytes"], 64)
        self.assertTrue(counted["matches_disclosed_count"])

    def test_expected_digest_mismatch_is_rejected_before_the_record(self) -> None:
        saved = json.loads((KNOWN / "p1-pass01-result.json").read_text(encoding="utf-8"))
        book = KNOWN / "p1-book"
        got, why = report.checked_record(
            str(book), "0599.probe", "05.01", "w4c5ae945c250d823",
            saved["first_expected_hash"], {"judgment": {}}, {"judgment": {}},
        )
        self.assertIsNone(got)
        self.assertEqual(why, "digest-mismatch")
        fresh = self.book("digest")
        root = fresh / "workbook-review" / PAGE / PASS
        write(root / "journal.json", pretty(journal_body("b" * 64)))
        got, why = report.checked_record(
            str(fresh), PAGE, PASS, REVIEW, "a" * 64, {"judgment": {}}, {"judgment": {}},
        )
        self.assertIsNone(got)
        self.assertEqual(why, "digest-mismatch")
        self.assertFalse((root / "reviews" / REVIEW / "record.json").exists())
        write(root / "journal.json", pretty(journal_body(1)))  # type: ignore[arg-type]
        journal = json.loads((root / "journal.json").read_text(encoding="utf-8"))
        journal["reviews"][0]["record_sha256"] = 1
        write(root / "journal.json", pretty(journal))
        got, why = report.checked_record(
            str(fresh), PAGE, PASS, REVIEW, "a" * 64, {"judgment": {}}, {"judgment": {}},
        )
        self.assertIsNone(got)
        self.assertEqual(why, "digest-mismatch")
        journal["reviews"][0].pop("record_sha256")
        write(root / "journal.json", pretty(journal))
        _got, why = report.checked_record(
            str(fresh), PAGE, PASS, REVIEW, "a" * 64, {"judgment": {}}, {"judgment": {}},
        )
        self.assertEqual(why, "digest-mismatch")
        matched = sha(b"record-bytes")
        write(root / "journal.json", pretty(journal_body(matched)))
        _got, why = report.checked_record(
            str(fresh), PAGE, PASS, REVIEW, matched, {"judgment": {}}, {"judgment": {}},
        )
        self.assertEqual(why, "record-mismatch")

    def test_coherent_cut_before_observation_is_reported(self) -> None:
        book = self.book("newcut")
        body = judgment()
        attention = ["FIRST CUT"]
        digest = self.plant(book, record_body(attention, body))
        commands: list[str] = []
        before = tree_hashes(book)
        self.stub(body, commands, rows=[{
            "bytes": 4,
            "declared_bytes": 4,
            "declared_sha256": "d" * 64,
            "path": "payload.txt",
            "role": "artifact",
            "root": "book",
            "sha256": "d" * 64,
        }])
        result = self.observe(book)
        self.assertEqual(commands, ["inspect", "read", "recover"])
        self.assertEqual(before, tree_hashes(book))
        self.assertEqual(result["state"], "readable")
        self.assertEqual(result["exit"], 0)
        self.assertEqual(result["attention"]["lines"], attention)
        self.assertEqual(result["observation"]["status"], "coherent")
        self.assertTrue(result["observation"]["stable"])
        self.assertEqual(result["observation"]["bound"]["record_sha256"], digest)
        self.assertEqual(result["identity"]["selected_by"], "journal-current")
        self.assertTrue(result["judgment_recorded"])
        self.assertEqual(result["custody"], "missing")
        self.assertFalse(result["work_complete"])
        self.assertFalse(result["action_released"])
        self.assertEqual(result["authority"], "none")
        self.assertEqual(result["artifacts"]["count"], 1)
        self.assertIn("detail: reasons, findings, gaps", result["projection"])
        self.assertNotIn("brief", result["projection"])

    def test_journal_current_changed_during_read(self) -> None:
        book = self.book("current")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))
        other = book / "workbook-review" / PAGE / PASS / "reviews" / "other-id" / "record.json"
        write(other, b"OTHER ATTENTION\n")

        def mutate(command: str) -> None:
            if command != "read":
                return
            path = book / "workbook-review" / PAGE / PASS / "journal.json"
            journal = json.loads(path.read_text(encoding="utf-8"))
            journal["current"] = "other-id"
            write(path, pretty(journal))

        self.stub(body, [], mutate=mutate)
        result = self.observe(book)
        raw = pretty(result)
        save_raw("current-changed.json", raw)
        self.assertEqual(result["state"], "held")
        self.assertFalse(result["observation"]["stable"])
        self.assertIn("journal_current", result["observation"]["changed"])
        self.assertEqual(result["review_id"], REVIEW)
        self.assertEqual(result["observation"]["recheck"]["journal_current"], "other-id")
        self.assertNotIn(b"OTHER ATTENTION", raw)
        self.assertNotIn(b"FIRST CUT", raw)
        self.assertEqual(result["attention"]["state"], "not-exposed")

    def test_publication_identity_changed_during_read(self) -> None:
        book = self.book("publication")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))

        def mutate(command: str) -> None:
            if command != "read":
                return
            path = book / "workbook-review" / PAGE / PASS / "journal.json"
            journal = json.loads(path.read_text(encoding="utf-8"))
            journal["publication"]["status"] = "recorded"
            journal["published_target"]["status"] = "recorded"
            write(path, pretty(journal))

        self.stub(body, [], mutate=mutate)
        result = self.observe(book)
        raw = pretty(result)
        self.assertEqual(result["state"], "held")
        self.assertFalse(result["observation"]["stable"])
        self.assertIn("publication", result["observation"]["changed"])
        self.assertEqual(result["observation"]["bound"]["journal_current"], REVIEW)
        self.assertEqual(result["observation"]["bound"]["publication"]["publication"]["status"], "published")
        self.assertEqual(result["observation"]["recheck"]["publication"]["publication"]["status"], "recorded")
        self.assertEqual(result["publication"]["class"], "unknown")
        self.assertNotIn(b"FIRST CUT", raw)
        self.assertIsNone(result["disposition"])

    def test_record_metadata_changed_during_observation(self) -> None:
        book = self.book("metadata")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))

        def mutate(command: str) -> None:
            if command != "read":
                return
            path = book / "workbook-review" / PAGE / PASS / "reviews" / REVIEW / "record.json"
            write(path, pretty(record_body(["METADATA CHANGED"], body)))

        self.stub(body, [], mutate=mutate)
        result = self.observe(book)
        raw = pretty(result)
        self.assertEqual(result["state"], "held")
        self.assertFalse(result["observation"]["stable"])
        self.assertIn("record_file_sha256", result["observation"]["changed"])
        self.assertNotIn(b"METADATA CHANGED", raw)
        self.assertEqual(result["attention"]["state"], "not-exposed")

    def test_four_role_counterexample(self) -> None:
        disclosed = json.loads((
            WORK / "0512.prime-review" / "evidence" / "prime-review05.04" / "independent-artifact-count.json"
        ).read_bytes().decode("utf-8"))
        counted = report.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": disclosed["observed"]["rows"]}},
            "measurement": "complete",
        })
        self.assertEqual(counted["count"], 1)
        self.assertEqual(counted["bytes"], 4)
        self.assertEqual(counted["count_state"], "declared")
        self.assertEqual(counted["scope"], "manifest-declared-artifact-entries")
        self.assertEqual(counted["measured_artifact_rows"]["count"], 1)
        self.assertEqual(counted["measured_artifact_rows"]["bytes"], 4)
        self.assertEqual(counted["unique_files"]["count"], 4)
        self.assertEqual(counted["unique_files"]["bytes"], 64)
        self.assertEqual(counted["intake_roles"]["count"], 4)
        self.assertEqual(counted["intake_roles"]["bytes"], 64)
        self.assertEqual(counted["intake_roles"]["label"], "intake role rows; not a declared artifact total")
        self.assertEqual(counted["hash_match"], 1)
        self.assertEqual(counted["not_verified"], 0)
        self.assertEqual(counted["intake_roles"]["not_verified"], 3)
        self.assertEqual([row["role"] for row in counted["rows"]], [
            "assignment", "submission", "artifact-manifest", "artifact",
        ])
        book = self.book("four")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))
        self.stub(body, [], rows=disclosed["observed"]["rows"])
        result = self.observe(book)
        self.assertIn("declared_artifacts: count 1, bytes 4, provenance declared", result["projection"])
        self.assertIn("intake_role_rows: count 4, bytes 64, provenance current-measured", result["projection"])
        self.assertIn("unique_files: count 4, bytes 64, provenance current-measured", result["projection"])

    def test_overlapping_roles_count_one_unique_file(self) -> None:
        rows = []
        for role, path in (("assignment", "a.txt"), ("artifact", "a.txt"), ("submission", "alias/a.txt")):
            row = {
                "bytes": 4,
                "declared_bytes": 4 if role == "artifact" else None,
                "declared_sha256": "a" * 64 if role == "artifact" else None,
                "path": path,
                "role": role,
                "root": "book",
                "sha256": "a" * 64,
            }
            rows.append(row)
        counted = report.artifacts_of({"findings": [], "form": {"bindings": {"rows": rows}}, "measurement": "complete"})
        self.assertEqual(counted["unique_files"]["count"], 1)
        self.assertEqual(counted["unique_files"]["bytes"], 4)
        self.assertEqual(counted["intake_roles"]["count"], 3)
        self.assertEqual(counted["intake_roles"]["bytes"], 12)
        self.assertEqual(counted["measured_artifact_rows"]["count"], 1)
        self.assertEqual(counted["count"], 1)
        self.assertEqual(len(counted["rows"]), 3)

    def test_missing_submission_is_not_a_missing_payload(self) -> None:
        artifact = {
            "bytes": 4,
            "declared_bytes": 4,
            "declared_sha256": "d" * 64,
            "path": "payload.txt",
            "role": "artifact",
            "root": "book",
            "sha256": "d" * 64,
        }
        submission_only = report.artifacts_of({
            "findings": [{"code": "submission-missing", "path": "return.md"}],
            "form": {"bindings": {"rows": [artifact]}},
            "measurement": "complete",
        })
        self.assertEqual(submission_only["missing"], [])
        self.assertEqual(submission_only["count"], 1)
        self.assertEqual(report.p1.evidence_of(submission_only)["state"], "not-recorded")
        mixed = report.artifacts_of({
            "findings": [
                {"code": "submission-missing", "path": "return.md"},
                {"code": "artifact-missing", "path": "payload.txt"},
            ],
            "form": {"bindings": {"rows": [{
                "bytes": 10,
                "declared_bytes": None,
                "declared_sha256": None,
                "path": "page.md",
                "role": "assignment",
                "root": "book",
                "sha256": "b" * 64,
            }]}},
            "measurement": "complete",
        })
        self.assertEqual(mixed["missing"], [{"code": "artifact-missing", "path": "payload.txt"}])
        self.assertIsNone(mixed["count"])
        self.assertEqual(mixed["count_state"], "unknown")
        self.assertEqual(report.p1.evidence_of(mixed)["state"], "missing-referenced")
        book = self.book("missing")
        body = judgment(finding="HISTORICAL FINDING", disposition="correction-required", tests_passed=None, tests_note=None)
        self.plant(book, record_body(["historical attention"], body))
        self.stub(
            body,
            [],
            rows=[],
            findings=[{"code": "artifact-missing", "path": "payload.txt"}],
            stale=True,
        )
        result = self.observe(book)
        self.assertEqual(result["state"], "stale")
        self.assertEqual(result["exit"], 1)
        self.assertEqual(result["disposition"], "correction-required")
        self.assertEqual(result["finding"], "HISTORICAL FINDING")
        self.assertTrue(result["observation"]["stable"])
        self.assertEqual(result["tests_passed"]["state"], "unknown")
        self.assertEqual(result["artifacts"]["count_state"], "unknown")
        self.assertEqual(result["intake_findings"][0]["code"], "artifact-missing")
        self.assertFalse((book / "payload.txt").exists())
        self.assertIn("disposition: correction-required", result["projection"])
        self.assertIn("detail: reasons, findings", result["projection"])
        self.assertIn(report.p1.HISTORICAL, result["projection"])

    def test_null_counts_stay_unknown(self) -> None:
        blank = report.artifacts_of(None)
        self.assertIsNone(blank["count"])
        self.assertEqual(blank["count_state"], "unknown")
        self.assertIsNone(blank["rows"])
        partial = report.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": [{
                "bytes": None,
                "path": "payload.txt",
                "role": "artifact",
                "root": "book",
                "sha256": "c" * 64,
            }]}},
            "measurement": "complete",
        })
        self.assertEqual(partial["measured_artifact_rows"]["count"], 1)
        self.assertIsNone(partial["measured_artifact_rows"]["bytes"])
        self.assertEqual(partial["measured_artifact_rows"]["bytes_state"], "unknown")
        self.assertIsNone(partial["count"])
        incomplete = report.artifacts_of({
            "findings": [{"code": "artifact-missing", "path": "missing.bin"}],
            "form": {"bindings": {"rows": [{"bytes": 4, "path": "a", "role": "assignment", "root": "book", "sha256": "e" * 64}]}},
            "measurement": "incomplete",
        })
        self.assertIsNone(incomplete["intake_roles"]["count"])
        self.assertEqual(incomplete["rows"][0]["role"], "assignment")
        self.assertEqual(incomplete["missing"], [{"code": "artifact-missing", "path": "missing.bin"}])

    def test_finish_rechecks_before_the_projection(self) -> None:
        book = self.book("finish")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))
        self.stub(body, [])
        observed = report.observe(self.options(book))
        self.assertEqual(observed["attention"]["lines"], ["FIRST CUT"])
        path = book / "workbook-review" / PAGE / PASS / "journal.json"
        journal = json.loads(path.read_text(encoding="utf-8"))
        journal["publication"]["target"] = "other.md"
        journal["published_target"]["target"] = "other.md"
        write(path, pretty(journal))
        finished = report.finish(observed)
        raw = pretty(finished)
        self.assertEqual(finished["state"], "held")
        self.assertFalse(finished["observation"]["stable"])
        self.assertNotIn(b"FIRST CUT", raw)
        self.assertIn("attention: not exposed", finished["projection"])
        self.assertIn("observation_limit:", finished["projection"])

    def test_hostile_newer_folder_is_not_selected(self) -> None:
        book = self.book("newer")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))
        write(
            book / "workbook-review" / PAGE / PASS / "reviews" / "zzz-newer" / "record.json",
            b"NEWER FOLDER WINS\n",
        )
        self.stub(body, [])
        result = self.observe(book)
        raw = pretty(result)
        save_raw("newer-folder.json", raw)
        self.assertEqual(result["review_id"], REVIEW)
        self.assertEqual(result["state"], "readable")
        self.assertNotIn(b"NEWER FOLDER WINS", raw)
        self.assertEqual(result["attention"]["lines"], ["FIRST CUT"])

    def test_hostile_rebaseline_during_observation_is_not_adopted(self) -> None:
        book = self.book("rebaseline")
        body = judgment()
        self.plant(book, record_body(["FIRST CUT"], body))
        root = book / "workbook-review" / PAGE / PASS

        def mutate(command: str) -> None:
            if command != "inspect":
                return
            replacement = record_body(["SECOND CUT ADOPTED"], body)
            raw = pretty(replacement)
            journal = json.loads((root / "journal.json").read_text(encoding="utf-8"))
            journal["reviews"][0]["record_sha256"] = sha(raw)
            write(root / "journal.json", pretty(journal))
            write(root / "reviews" / REVIEW / "record.json", raw)

        self.stub(body, [], mutate=mutate)
        result = self.observe(book)
        raw = pretty(result)
        save_raw("rebaseline.json", raw)
        self.assertEqual(result["state"], "held")
        self.assertFalse(result["observation"]["stable"])
        self.assertEqual(result["observation"]["status"], "unstable")
        self.assertNotIn(b"SECOND CUT ADOPTED", raw)
        self.assertNotIn(b"FIRST CUT", raw)
        self.assertNotEqual(
            result["observation"]["bound"]["record_sha256"],
            result["observation"]["recheck"]["record_sha256"],
        )

    def test_usage_pin_and_non_json(self) -> None:
        proc = run([str(PY), "-B", str(LAB / "report.py")])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"refused:", proc.stderr)
        payload = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(payload["schema"], "review-report/2")
        self.assertEqual(payload["state"], "refused")
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

        def core_call(*_args):
            return subprocess.CompletedProcess([], 2, b"nope", b"")

        report.core_call = core_call
        book = self.book("nonjson")
        self.plant(book, record_body(["FIRST CUT"], judgment()))
        result = self.observe(book)
        self.assertEqual(result["exit"], 2)
        self.assertEqual(result["state"], "refused")


class LiveReads(unittest.TestCase):
    def test_live_reads_match_and_do_not_write(self) -> None:
        frozen = {row["path"]: row["sha256"] for row in json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]}
        before = {rel: file_sha(ROOT / rel) for rel in LIVE_PATHS}
        for rel, digest in before.items():
            self.assertEqual(digest, frozen[rel], rel)
        readme_before = file_sha(ROOT / "app" / "README.md")
        first = run([
            str(PY), "-B", str(LAB / "report.py"),
            "--code-root", str(ROOT),
            "--book", str(WORK),
            "--source", "0522.review-construction",
            "--pass", "05.13",
        ])
        second = run([
            str(PY), "-B", str(LAB / "report.py"),
            "--code-root", str(ROOT),
            "--book", str(WORK),
            "--source", "0522.review-construction",
            "--pass", "05.13",
        ])
        observed = run([
            str(PY), "-B", str(LAB / "report.py"),
            "--code-root", str(ROOT),
            "--book", str(WORK),
            "--source", "0512.prime-review",
            "--pass", "05.04",
        ])
        after = {rel: file_sha(ROOT / rel) for rel in LIVE_PATHS}
        self.assertEqual(before, after)
        self.assertEqual(readme_before, file_sha(ROOT / "app" / "README.md"))
        self.assertEqual(first.returncode, second.returncode)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.stderr, b"")
        payload = json.loads(first.stdout.decode("utf-8"))
        correction = json.loads(observed.stdout.decode("utf-8"))
        out = WORK / "0512.prime-review" / "evidence" / "build05.05" / "current-review"
        write(out / "report.json", first.stdout)
        write(out / "report-second.stdout", second.stdout)
        write(out / "correction-required.json", observed.stdout)
        write(out / "readme-sha256.txt", (readme_before + "\n").encode("utf-8"))
        self.assertEqual(payload["schema"], "review-report/2")
        self.assertEqual(payload["review_id"], "w4c5ae945c250d823")
        self.assertEqual(payload["disposition"], "accepted")
        self.assertEqual(payload["custody"], "missing")
        self.assertEqual(payload["authority"], "none")
        self.assertFalse(payload["work_complete"])
        self.assertFalse(payload["action_released"])
        self.assertEqual(payload["tests_note"]["text"], LIVE_NOTE)
        self.assertEqual(payload["tests_passed"]["value"], True)
        self.assertFalse(payload["tests_passed"]["proof_of_all_tests"])
        self.assertEqual(payload["claims"]["state"], "not-recorded")
        self.assertEqual(payload["claims"]["rows"], [])
        self.assertEqual(payload["attention"]["lines"], LIVE_ATTENTION)
        for line in LIVE_ATTENTION:
            self.assertIn(line, payload["projection"])
        self.assertIn(LIVE_NOTE, payload["projection"])
        self.assertEqual(payload["artifacts"]["scope"], "manifest-declared-artifact-entries")
        self.assertEqual(payload["artifacts"]["intake_roles"]["scope"], "full-intake-role-rows")
        self.assertEqual(correction["review_id"], "weffe9a51780b52b3")
        self.assertEqual(correction["disposition"], "correction-required")
        self.assertIn("selected-record digest coherence", correction["finding"])
        self.assertEqual(correction["custody"], "missing")
        self.assertFalse(correction["work_complete"])
        self.assertFalse(correction["action_released"])
        self.assertIn(correction["state"], {"readable", "stale", "held"})
        if correction["judgment_recoverable"]:
            self.assertTrue(correction["judgment_recorded"])
        write(out / "05.04-observation.txt", b"product_pass: false\n")
        if payload["stale"]:
            self.assertEqual(payload["state"], "stale")
            self.assertEqual(payload["exit"], 1)
        else:
            self.assertEqual(payload["state"], "readable")
            self.assertEqual(payload["exit"], 0)
            self.assertTrue(payload["observation"]["stable"])


if __name__ == "__main__":
    unittest.main()
