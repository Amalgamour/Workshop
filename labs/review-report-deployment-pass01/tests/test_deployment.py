#!/usr/bin/env python3
"""Author tests for the deployment-coherent review-report candidate.

These cases are author work. They are not Prime's independent probes.
Prime's future independent probes, not executed here:
- repeat the candidate comparison on a book this author did not plant
- select the candidate dispatcher on the active app
- file 0112.prime-review

The historical 05.07 test that expects a PENDING return pointer is a known
failure retained outside this module. It is not repaired here and it is not
counted as coverage.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
LAB = ROOT / "labs" / "review-report-deployment-pass01"
BOOK = ROOT / "00.kernel" / "00.00.10.work"
PACK = BOOK / "0512.prime-review"
KEEP = Path(r"D:\librarian\temp\0512-0508-report")
CANDIDATE = (KEEP / "candidate").resolve()
PAGE = PACK / "05.08.md"
CONTRACT = PACK / "evidence" / "build05.08" / "CONTRACT.md"
CONTRACT_SHA = "773b65bcb33cf8378beff0786216611a69056a3ae44a3aeb876bb233a387432c"
CONTRACT_BYTES = 6573
BODY_SHA = "63defe4b9c4e0a04ef142eb7c21a02d48e4b7f1b808920f1bb8233f039f5de2b"
OLD_SHA = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"
OLD_BYTES = 12204
NEW_SHA = "d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52"
NEW_BYTES = 12805
V1_SHA = "00489768c33874b282a3732709eb40503d0c3ebfad2826a9b3e8be6d832a5e2c"
V1_BYTES = 13708
README_SHA = "3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920"
README_BYTES = 39687
FROZEN_TEST_SHA = "f477fd4e4dac922435fac822a5b85ee34b34d731583a730842b08f5c110e18de"
FROZEN_TEST_BYTES = 32678
MARKER = "\n## Return pointer\n"
REVIEW = "\n## Review - Codex Prime\n"
RUNTIME_REL = "labs/review-report-deployment-pass01/report.py"
PRIME_FUTURE_PROBES = (
    "repeat the candidate comparison on a book this author did not plant",
    "select the candidate dispatcher on the active app",
    "file 0112.prime-review",
)
WATCH = (
    "app/librarian.py",
    "app/README.md",
    "app/review-report-v1.json",
    "app/review_report_tools_v1.py",
    "app/review-report-v2.json",
    "app/review_report_tools_v2.py",
    "labs/review-report-pass01/report.py",
    "labs/review-report-pass02/report.py",
    "labs/review-report-pass03/report.py",
    "labs/review-report-pass03/PRIME-USE.md",
    "labs/review-report-pass03/tests/test_report.py",
    "labs/review-report-deployment-pass01/report.py",
    "labs/review-report-deployment-pass01/librarian.py",
    "labs/workbook-review-pass03/workbook.py",
    "00.kernel/00.00.10.work/0512.prime-review/05.06.md",
    "00.kernel/00.00.10.work/0512.prime-review/05.07.md",
    "00.kernel/00.00.10.work/0512.prime-review/05.08.md",
    "00.kernel/00.00.10.work/0512.prime-review/06.10.md",
    "00.kernel/00.00.10.work/0512.prime-review/06.12.md",
    "00.kernel/00.00.10.work/0512.prime-review/06.13.md",
    "00.kernel/00.00.10.work/0512.prime-review/evidence/build05.06/CONTRACT.md",
    "00.kernel/00.00.10.work/0512.prime-review/evidence/build05.08/CONTRACT.md",
    "00.kernel/00.00.10.work/0521.return-placement/05.13.md",
)
TREES = (
    BOOK / "workbook-review" / "0512.prime-review" / "05.06",
    BOOK / "workbook-review" / "0521.return-placement" / "05.13",
)
CACHES = (
    ROOT / "app" / "__pycache__",
    ROOT / "labs" / "review-report-pass01" / "__pycache__",
    ROOT / "labs" / "review-report-pass02" / "__pycache__",
    ROOT / "labs" / "review-report-pass03" / "__pycache__",
    ROOT / "labs" / "review-report-pass03" / "tests" / "__pycache__",
    ROOT / "labs" / "review-report-deployment-pass01" / "__pycache__",
    ROOT / "labs" / "review-report-deployment-pass01" / "tests" / "__pycache__",
    ROOT / "labs" / "workbook-review-pass03" / "__pycache__",
)
RESULTS: list[dict] = []


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


door = load("review_report_tools_v2_author", ROOT / "app" / "review_report_tools_v2.py")
runtime = load("review_report_deployment_author", LAB / "report.py")
wb = load("workbook_review_pass03_author_helpers_0508", ROOT / "labs" / "workbook-review-pass03" / "tests" / "test_workbook.py")


def environment() -> dict:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(argv: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", *argv],
        cwd=str(cwd),
        env=environment(),
        capture_output=True,
        shell=False,
    )


def ignore_cache(_directory: str, names: list[str]) -> list[str]:
    return [name for name in names if name == "__pycache__" or name.endswith(".pyc")]


def declaration_paths() -> list[str]:
    found: list[str] = []

    def walk(value) -> None:
        if isinstance(value, dict):
            path = value.get("path")
            if isinstance(path, str):
                found.append(path)
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    for name in ("authoring-v2.json", "return-lines-v2.json", "review-loop-v7.json"):
        walk(json.loads((ROOT / "app" / name).read_text(encoding="utf-8")))
    return found


def copy_rel(dest: Path, rel: str) -> None:
    target = dest / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copyfile(ROOT / rel, target)


def materialize(dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(ROOT / "app", dest / "app", ignore=ignore_cache)
    for rel in runtime.PINS:
        if rel.startswith("labs/"):
            copy_rel(dest, rel)
    copy_rel(dest, RUNTIME_REL)
    for rel in declaration_paths():
        copy_rel(dest, rel)
    shutil.copyfile(LAB / "librarian.py", dest / "app" / "librarian.py")


def norm(data: bytes) -> str:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n").decode("utf-8")


def tree_rows(root: Path) -> list[str]:
    rows = []
    if not root.exists():
        return rows
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            rows.append(f"link {rel}")
            continue
        if path.is_file():
            data = path.read_bytes()
            rows.append(f"file {rel} {sha256(data)} {len(data)}")
    return rows


def tree_digest(root: Path) -> str:
    payload = ("\n".join(tree_rows(root)) + "\n").encode("utf-8")
    return sha256(payload)


def watched() -> dict:
    files = {}
    for rel in WATCH:
        data = (ROOT / rel).read_bytes()
        files[rel] = {"bytes": len(data), "sha256": sha256(data)}
    trees = {path.relative_to(ROOT).as_posix(): tree_digest(path) for path in TREES}
    caches = []
    for folder in CACHES:
        if not folder.exists():
            continue
        caches.extend(
            f"{path.relative_to(ROOT).as_posix()} {sha256(path.read_bytes())} {path.stat().st_size}"
            for path in sorted(folder.rglob("*"))
            if path.is_file()
        )
    return {"caches": caches, "files": files, "trees": trees}


def page_parts(data: bytes) -> tuple[str, str, str]:
    text = data.decode("utf-8")
    if text.count(MARKER) != 1 or text.count(REVIEW) != 1:
        raise AssertionError("lifecycle headings")
    body, rest = text.split(MARKER, 1)
    pointer, review = rest.split(REVIEW, 1)
    if pointer.strip() == "" or review.strip() == "":
        raise AssertionError("empty lifecycle")
    if sha256(body.encode("utf-8")) != BODY_SHA:
        raise AssertionError("task body changed")
    return body, pointer, review


def save_pair(name: str, base: subprocess.CompletedProcess, inst: subprocess.CompletedProcess) -> None:
    folder = KEEP / "commands" / name
    folder.mkdir(parents=True, exist_ok=True)
    for label, item in (("baseline", base), ("installed", inst)):
        (folder / f"{label}.stdout").write_bytes(item.stdout)
        (folder / f"{label}.stderr").write_bytes(item.stderr)
        (folder / f"{label}.exit").write_bytes(f"{item.returncode}\n".encode("utf-8"))


def save_bytes(name: str, payload: bytes) -> None:
    latest = KEEP / "hostile-latest"
    first = KEEP / "hostile-first"
    latest.mkdir(parents=True, exist_ok=True)
    first.mkdir(parents=True, exist_ok=True)
    (latest / name).write_bytes(payload)
    dest = first / name
    if not dest.exists():
        dest.write_bytes(payload)


def plant(book: Path, source: str, pass_id: str) -> None:
    if book.exists():
        shutil.rmtree(book)
    submission = b"Substantive submission for the deployment fixture. It names verification in prose only.\n"
    note = b"NOTE one\n"
    manifest = wb.pretty({"files": [{"bytes": len(note), "path": "note.md", "sha256": wb.sha(note)}], "schema": "example-manifest/1"})
    wb.write(book / "evidence" / "submission.md", submission)
    wb.write(book / "evidence" / "artifact-manifest.json", manifest)
    wb.write(book / "note.md", note)
    pointer = (
        f"Submission: evidence/submission.md sha256 {wb.sha(submission)}, {len(submission)} bytes.\n"
        f"Artifact manifest: evidence/artifact-manifest.json sha256 {wb.sha(manifest)}, {len(manifest)} bytes.\n"
    )
    wb.write(book / source / f"{pass_id}.md", wb.page(pointer))


def publish(book: Path, source: str, pass_id: str) -> str:
    proc, prepared = wb.call(book, "prepare", source=source, pass_=pass_id)
    if proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8", "replace")[:900])
    wb.write(book / "judgment.json", wb.pretty(wb.judgment()))
    proc, recorded = wb.call(
        book, "record", source=source, pass_=pass_id,
        intake=prepared["intake_id"], judgment=str(book / "judgment.json"),
    )
    if proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8", "replace")[:700] + proc.stdout.decode("utf-8", "replace")[:400])
    review = recorded["review_id"]
    proc, _published = wb.call(book, "publish", source=source, pass_=pass_id, review=review)
    if proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8", "replace")[:700] + proc.stdout.decode("utf-8", "replace")[:400])
    return review


def run_pass03(book: str, source: str, pass_id: str) -> subprocess.CompletedProcess:
    return run(
        [
            str(CANDIDATE / "labs" / "review-report-pass03" / "report.py"),
            "--code-root", str(CANDIDATE),
            "--book", book,
            "--source", source,
            "--pass", pass_id,
        ],
        CANDIDATE,
    )


def run_app(book: str, source: str, pass_id: str) -> subprocess.CompletedProcess:
    return run(
        [
            str(CANDIDATE / "app" / "librarian.py"),
            "review-report",
            "--book", book,
            "--source", source,
            "--pass", pass_id,
        ],
        CANDIDATE,
    )


def pair(book: str, source: str, pass_id: str) -> tuple[subprocess.CompletedProcess, subprocess.CompletedProcess]:
    path = CANDIDATE / "app" / "librarian.py"
    previous = path.read_bytes()
    try:
        path.write_bytes((ROOT / "app" / "librarian.py").read_bytes())
        base = run_pass03(book, source, pass_id)
        path.write_bytes((LAB / "librarian.py").read_bytes())
        installed = run_app(book, source, pass_id)
        return base, installed
    finally:
        path.write_bytes(previous)


def summary_of(stdout: bytes, code: int) -> dict:
    report = json.loads(stdout.decode("utf-8"))
    artifacts = report["artifacts"]
    attention = report.get("attention") if isinstance(report.get("attention"), dict) else {}
    lines = attention.get("lines")
    observation = report.get("observation") if isinstance(report.get("observation"), dict) else {}
    publication = report.get("publication") if isinstance(report.get("publication"), dict) else {}
    counters = {}
    for key in ("addressed_sources", "content_blobs", "physical_files"):
        item = artifacts[key]
        counters[key] = {
            "bytes": item.get("bytes"),
            "count": item.get("count"),
            "provenance": item.get("provenance"),
            "scope": item.get("scope"),
        }
    return {
        "accepted": report.get("accepted"),
        "action_released": report.get("action_released"),
        "approved": report.get("approved"),
        "attention_lines": len(lines) if isinstance(lines, list) else None,
        "attention_state": attention.get("state"),
        "authority": report.get("authority"),
        "closes_work": report.get("closes_work"),
        "code_root": report.get("code_root"),
        "counters": counters,
        "custody": report.get("custody"),
        "declared_bytes": artifacts.get("bytes"),
        "declared_count": artifacts.get("count"),
        "disposition": report.get("disposition"),
        "exit": report.get("exit"),
        "hash_match": artifacts.get("hash_match"),
        "hash_mismatch": artifacts.get("hash_mismatch"),
        "measurement": artifacts.get("measurement"),
        "not_verified": artifacts.get("not_verified"),
        "observation_stable": observation.get("stable"),
        "operation": report.get("operation"),
        "process_exit": code,
        "publication_class": publication.get("class"),
        "publication_status": publication.get("status"),
        "releases_action": report.get("releases_action"),
        "review_id": report.get("review_id"),
        "schema": report.get("schema"),
        "stale": report.get("stale"),
        "state": report.get("state"),
        "stdout_bytes": len(stdout),
        "stdout_sha256": sha256(stdout),
        "task_association": report.get("task_association"),
        "tests_note_type": type(report.get("tests_note")).__name__,
        "tests_passed": report.get("tests_passed"),
        "unique_files_absent": "unique_files" not in artifacts,
        "work_complete": report.get("work_complete"),
    }


def setUpModule() -> None:
    KEEP.mkdir(parents=True, exist_ok=True)
    materialize(CANDIDATE)


def tearDownModule() -> None:
    rows = []
    for path in sorted(CANDIDATE.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            rows.append({
                "bytes": len(data),
                "path": path.relative_to(CANDIDATE).as_posix(),
                "sha256": sha256(data),
            })
    index = {"files": rows, "root": str(CANDIDATE), "schema": "review-report-candidate-index/1"}
    (KEEP / "candidate-index.json").write_bytes((json.dumps(index, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    (KEEP / "author-results.json").write_bytes((json.dumps(RESULTS, indent=2, sort_keys=True) + "\n").encode("utf-8"))


class DeploymentTests(unittest.TestCase):
    def assert_stop(self, proc: subprocess.CompletedProcess, message: str) -> None:
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertEqual(proc.stdout, b"")
        self.assertEqual(norm(proc.stderr), f"stop: {message}\n")

    def assert_same_pair(self, base: subprocess.CompletedProcess, inst: subprocess.CompletedProcess) -> dict:
        if base.returncode != inst.returncode or base.stdout != inst.stdout or base.stderr != inst.stderr:
            self.fail(
                f"baseline exit {base.returncode} installed {inst.returncode}\n"
                f"stderr base {base.stderr[:400]!r}\nstderr installed {inst.stderr[:400]!r}\n"
                f"stdout base {len(base.stdout)} installed {len(inst.stdout)}"
            )
        self.assertIn(base.returncode, (0, 1))
        self.assertEqual(base.stderr, b"")
        report = json.loads(base.stdout.decode("utf-8"))
        self.assertEqual(report["schema"], "review-report/3")
        self.assertEqual(report["exit"], base.returncode)
        self.assertIsInstance(report["tests_note"], dict)
        artifacts = report["artifacts"]
        self.assertNotIn("unique_files", artifacts)
        physical = artifacts["physical_files"]
        self.assertIsNone(physical["count"])
        self.assertIsNone(physical["bytes"])
        self.assertEqual(physical["provenance"], "not-established")
        self.assertEqual(report["code_root"], str(CANDIDATE))
        return summary_of(base.stdout, base.returncode)

    def test_author_contract_and_active_app_stay_put(self) -> None:
        data = CONTRACT.read_bytes()
        self.assertEqual(len(data), CONTRACT_BYTES)
        self.assertEqual(sha256(data), CONTRACT_SHA)
        self.assertNotIn(b"\r", data)
        live = (ROOT / "app" / "librarian.py").read_bytes()
        self.assertEqual(len(live), OLD_BYTES)
        self.assertEqual(sha256(live), OLD_SHA)
        self.assertNotIn(b'"review-report"', live)
        v1 = (ROOT / "app" / "review_report_tools_v1.py").read_bytes()
        self.assertEqual(len(v1), V1_BYTES)
        self.assertEqual(sha256(v1), V1_SHA)
        readme = (ROOT / "app" / "README.md").read_bytes()
        self.assertEqual(len(readme), README_BYTES)
        self.assertEqual(sha256(readme), README_SHA)
        candidate = (LAB / "librarian.py").read_bytes()
        self.assertEqual(len(candidate), NEW_BYTES)
        self.assertEqual(sha256(candidate), NEW_SHA)
        self.assertEqual(door.TOOLS["app/librarian.py"]["sha256"], NEW_SHA)
        self.assertEqual(runtime.PINS["app/librarian.py"], (NEW_BYTES, NEW_SHA))
        self.assertNotIn(RUNTIME_REL, runtime.PINS)
        self.assertEqual(door.TOOLS[RUNTIME_REL]["sha256"], sha256((LAB / "report.py").read_bytes()))
        for rel, (size, digest) in runtime.PINS.items():
            item = door.TOOLS[rel]
            self.assertEqual(item["bytes"], size)
            self.assertEqual(item["sha256"], digest)
        declaration = json.loads((ROOT / "app" / "review-report-v2.json").read_text(encoding="utf-8"))
        self.assertEqual(declaration["schema"], "review-report-command/2")
        self.assertEqual(declaration["version"], 2)
        self.assertEqual(set(declaration["tools"]), set(door.TOOLS))
        page_parts(PAGE.read_bytes())
        self.assertEqual((LAB / "PRIME-USE.md").read_bytes(), (PACK / "evidence" / "build05.08" / "PRIME-USE.md").read_bytes())
        self.assertEqual((LAB / "INTEGRATION.md").read_bytes(), (PACK / "evidence" / "build05.08" / "INTEGRATION.md").read_bytes())
        book = KEEP / "arg-book"
        book.mkdir(parents=True, exist_ok=True)
        proc = run(
            [str(ROOT / "app" / "review_report_tools_v2.py"), "--book", str(book), "--source", "0594.probe", "--pass", "05.94"],
            ROOT,
        )
        self.assert_stop(
            proc,
            f"dependency conflict app/librarian.py got {OLD_BYTES} bytes sha256 {OLD_SHA} want {NEW_BYTES} bytes sha256 {NEW_SHA}",
        )
        save_bytes("active-v2-refuses.stderr", proc.stderr)

    def test_author_lifecycle_regions_accept_filing(self) -> None:
        original = PAGE.read_bytes()
        body, pointer, review = page_parts(original)
        pending = (body + MARKER + "PENDING.\n" + REVIEW + "PENDING.\n").encode("utf-8")
        page_parts(pending)
        filled_pointer = "Submission: example sha256 " + ("ab" * 32) + ", 3 bytes.\n"
        filled_review = "authority: none\ncustody: missing\n"
        filled = (body + MARKER + filled_pointer + REVIEW + filled_review).encode("utf-8")
        page_parts(filled)
        changed = ("Q" + body[1:] + MARKER + pointer + REVIEW + review).encode("utf-8")
        with self.assertRaises(AssertionError):
            page_parts(changed)
        self.assertEqual(PAGE.read_bytes(), original)

    def test_author_prime_probes_are_not_this_suite(self) -> None:
        names = [item for item in dir(DeploymentTests) if item.startswith("test_")]
        self.assertTrue(names)
        self.assertTrue(all(item.startswith("test_author_") for item in names))
        self.assertEqual(len(PRIME_FUTURE_PROBES), 3)
        self.assertGreaterEqual(len(names), 16)

    def test_author_historical_modules_and_helper_root_stay(self) -> None:
        tests = (ROOT / "labs" / "review-report-pass03" / "tests" / "test_report.py").read_bytes()
        self.assertEqual(len(tests), FROZEN_TEST_BYTES)
        self.assertEqual(sha256(tests), FROZEN_TEST_SHA)
        helper = (ROOT / runtime.HELPER_MODULE).read_bytes()
        self.assertEqual(len(helper), runtime.PINS[runtime.HELPER_MODULE][0])
        self.assertEqual(sha256(helper), runtime.PINS[runtime.HELPER_MODULE][1])
        self.assertIn(f'REPO = Path(r"{runtime.HELPER_ROOT}")'.encode("utf-8"), helper)
        self.assertEqual(str(runtime.HELPER_ROOT), r"D:\Git\lib-build")

    def test_author_live_0512_05_06(self) -> None:
        before = watched()
        base, inst = pair(str(BOOK), "0512.prime-review", "05.06")
        self.assertEqual(watched(), before)
        save_pair("live-0512-05-06", base, inst)
        summary = self.assert_same_pair(base, inst)
        self.assertEqual(summary["state"], "readable")
        self.assertEqual(summary["process_exit"], 0)
        RESULTS.append({"name": "live-0512-05-06", "no_write": True, "provenance": "author", "same_bytes": True, "summary": summary})

    def test_author_live_0521_05_13(self) -> None:
        before = watched()
        base, inst = pair(str(BOOK), "0521.return-placement", "05.13")
        self.assertEqual(watched(), before)
        save_pair("live-0521-05-13", base, inst)
        summary = self.assert_same_pair(base, inst)
        self.assertEqual(summary["state"], "readable")
        self.assertEqual(summary["process_exit"], 0)
        RESULTS.append({"name": "live-0521-05-13", "no_write": True, "provenance": "author", "same_bytes": True, "summary": summary})

    def test_author_fixture_missing_review(self) -> None:
        book = KEEP / "books" / "missing"
        source, pass_id = "0582.deployment-missing", "05.82"
        plant(book, source, pass_id)
        before = tree_digest(book)
        base, inst = pair(str(book), source, pass_id)
        self.assertEqual(tree_digest(book), before)
        save_pair("fixture-missing", base, inst)
        summary = self.assert_same_pair(base, inst)
        self.assertEqual(summary["state"], "not-recorded")
        self.assertIsNone(summary["stale"])
        RESULTS.append({"name": "fixture-missing", "no_write": True, "provenance": "author", "same_bytes": True, "summary": summary})

    def test_author_fixture_stale_note(self) -> None:
        book = KEEP / "books" / "stale"
        source, pass_id = "0581.deployment-stale", "05.81"
        plant(book, source, pass_id)
        publish(book, source, pass_id)
        (book / "note.md").write_bytes(b"NOTE changed\n")
        before = tree_digest(book)
        base, inst = pair(str(book), source, pass_id)
        self.assertEqual(tree_digest(book), before)
        save_pair("fixture-stale", base, inst)
        summary = self.assert_same_pair(base, inst)
        self.assertEqual(summary["state"], "stale")
        self.assertIs(summary["stale"], True)
        RESULTS.append({"name": "fixture-stale", "no_write": True, "provenance": "author", "same_bytes": True, "summary": summary})

    def test_author_fixture_digest_held(self) -> None:
        book = KEEP / "books" / "held"
        source, pass_id = "0583.deployment-held", "05.83"
        plant(book, source, pass_id)
        review = publish(book, source, pass_id)
        record = book / "workbook-review" / source / pass_id / "reviews" / review / "record.json"
        text = record.read_text(encoding="utf-8")
        self.assertIn("The disposable note is present.", text)
        record.write_text(text.replace("The disposable note is present.", "The disposable note is present!", 1), encoding="utf-8", newline="\n")
        before = tree_digest(book)
        base, inst = pair(str(book), source, pass_id)
        self.assertEqual(tree_digest(book), before)
        save_pair("fixture-held", base, inst)
        summary = self.assert_same_pair(base, inst)
        self.assertEqual(summary["state"], "held")
        RESULTS.append({"name": "fixture-held", "no_write": True, "provenance": "author", "same_bytes": True, "summary": summary})

    def test_author_wrong_app_hash(self) -> None:
        path = CANDIDATE / "app" / "librarian.py"
        original = path.read_bytes()
        book = KEEP / "arg-book"
        book.mkdir(parents=True, exist_ok=True)
        marker = b"deployment connector"
        index = original.index(marker)
        flipped = bytearray(original)
        flipped[index] ^= 0x20
        path.write_bytes(bytes(flipped))
        try:
            got = sha256(path.read_bytes())
            before = watched()
            proc = run_app(str(book), "0594.probe", "05.94")
            message = (
                f"dependency conflict app/librarian.py got {len(flipped)} bytes sha256 {got} "
                f"want {NEW_BYTES} bytes sha256 {NEW_SHA}"
            )
            self.assert_stop(proc, message)
            self.assertEqual(watched(), before)
            save_bytes("wrong-app.stderr", proc.stderr)
        finally:
            path.write_bytes(original)

    def test_author_wrong_transitive_hash(self) -> None:
        rel = "labs/prime-cycle-pass03/prime_cycle.py"
        path = CANDIDATE / rel
        original = path.read_bytes()
        book = KEEP / "arg-book"
        book.mkdir(parents=True, exist_ok=True)
        flipped = bytearray(original)
        flipped[-1] = (flipped[-1] + 1) % 256
        path.write_bytes(bytes(flipped))
        try:
            got = sha256(path.read_bytes())
            want_bytes, want_sha = runtime.PINS[rel]
            direct = run(
                [
                    str(CANDIDATE / "labs" / "review-report-deployment-pass01" / "report.py"),
                    "--code-root", str(CANDIDATE),
                    "--book", str(book),
                    "--source", "0594.probe",
                    "--pass", "05.94",
                ],
                CANDIDATE,
            )
            self.assertEqual(direct.returncode, 2, direct.stderr)
            self.assertTrue(direct.stdout.startswith(b"{"))
            refused = json.loads(direct.stdout.decode("utf-8"))
            self.assertEqual(refused["state"], "refused")
            self.assertEqual(refused["exit"], 2)
            self.assertEqual(refused["observation"]["status"], "not-run")
            self.assertEqual(
                norm(direct.stderr),
                f"refused: dependency conflict {rel} got {len(flipped)} bytes sha256 {got} "
                f"want {want_bytes} bytes sha256 {want_sha}\n",
            )
            proc = run_app(str(book), "0594.probe", "05.94")
            self.assert_stop(
                proc,
                f"dependency conflict {rel} got {len(flipped)} bytes sha256 {got} "
                f"want {want_bytes} bytes sha256 {want_sha}",
            )
            save_bytes("wrong-transitive.stderr", proc.stderr)
            save_bytes("wrong-transitive-runtime.stderr", direct.stderr)
        finally:
            path.write_bytes(original)

    def test_author_malformed_and_repeated_arguments(self) -> None:
        book = KEEP / "arg-book"
        book.mkdir(parents=True, exist_ok=True)
        app = str(CANDIDATE / "app" / "librarian.py")
        before = watched()
        cases = (
            ([app, "review-report", "--publish", "--book", str(book), "--source", "0594.probe", "--pass", "05.94"], "unknown flag --publish"),
            ([app, "review-report", "--code-root", str(CANDIDATE), "--book", str(book), "--source", "0594.probe", "--pass", "05.94"], "unknown flag --code-root"),
            ([app, "review-report", "--book", str(book), "--book", str(book), "--source", "0594.probe", "--pass", "05.94"], "repeated --book"),
            ([app, "review-report", "--book", str(book), "--source", "0594.probe", "--pass", "5"], "pass is not 05.NN"),
            ([app, "review-report", "--book", "labs", "--source", "0594.probe", "--pass", "05.94"], "book must be an absolute directory and was not followed when linked"),
            ([app, "review-report", "--book", str(book), "--source", "nested/page", "--pass", "05.94"], "source is a page id"),
            ([app, "review-report", "--book", str(book), "--pass", "05.94"], "missing --source"),
        )
        for argv, message in cases:
            proc = run(argv, CANDIDATE)
            self.assert_stop(proc, message)
            save_bytes(f"arg-{message.split()[0]}.stderr", proc.stderr)
        raw = (ROOT / "app" / "review-report-v2.json").read_bytes()
        document = json.loads(raw.decode("utf-8"))
        document["tools"]["../outside.py"] = {"bytes": 1, "sha256": "aa"}
        with self.assertRaises(door.Refuse) as caught:
            door.assess_declaration(json.dumps(document).encode("utf-8"))
        self.assertEqual(str(caught.exception), "tool path escapes the code root")
        self.assertEqual(watched(), before)

    def test_author_hostile_historical_chain_refuses_installed_dispatcher(self) -> None:
        book = KEEP / "arg-book"
        book.mkdir(parents=True, exist_ok=True)
        before = watched()
        digest = tree_digest(book)
        direct = run_pass03(str(book), "0594.probe", "05.94")
        self.assertEqual(direct.returncode, 2, direct.stderr)
        self.assertEqual(norm(direct.stderr), "refused: pin mismatch app/librarian.py\n")
        refused = json.loads(direct.stdout.decode("utf-8"))
        self.assertEqual(refused["schema"], "review-report/3")
        self.assertEqual(refused["state"], "refused")
        self.assertEqual(refused["exit"], 2)
        self.assertEqual(refused["observation"]["status"], "not-run")
        v1 = run(
            [str(CANDIDATE / "app" / "review_report_tools_v1.py"), "--book", str(book), "--source", "0594.probe", "--pass", "05.94"],
            CANDIDATE,
        )
        self.assert_stop(
            v1,
            f"dependency conflict app/librarian.py got {NEW_BYTES} bytes sha256 {NEW_SHA} want {OLD_BYTES} bytes sha256 {OLD_SHA}",
        )
        self.assertEqual(tree_digest(book), digest)
        self.assertEqual(watched(), before)
        save_bytes("historical-pass03.stderr", direct.stderr)
        save_bytes("historical-v1.stderr", v1.stderr)
        RESULTS.append({
            "historical_pass03_exit": direct.returncode,
            "historical_v1_exit": v1.returncode,
            "hostile_deployment": True,
            "name": "historical-chain-refuses-installed-dispatcher",
            "provenance": "author",
        })

    def test_author_hostile_swapped_runtime_stops_app_command(self) -> None:
        path = CANDIDATE / RUNTIME_REL
        original = path.read_bytes()
        book = KEEP / "books" / "missing"
        if not book.exists():
            plant(book, "0582.deployment-missing", "05.82")
        before_book = tree_digest(book)
        before = watched()
        flipped = bytearray(original)
        flipped[-1] = (flipped[-1] + 1) % 256
        path.write_bytes(bytes(flipped))
        try:
            got = sha256(path.read_bytes())
            want = door.TOOLS[RUNTIME_REL]
            proc = run_app(str(book), "0582.deployment-missing", "05.82")
            message = (
                f"dependency conflict {RUNTIME_REL} got {len(flipped)} bytes sha256 {got} "
                f"want {want['bytes']} bytes sha256 {want['sha256']}"
            )
            self.assert_stop(proc, message)
            self.assertEqual(tree_digest(book), before_book)
            self.assertEqual(watched(), before)
            save_bytes("swapped-runtime.stderr", proc.stderr)
        finally:
            path.write_bytes(original)
        RESULTS.append({
            "hostile_deployment": True,
            "name": "swapped-runtime-stops-app-command",
            "provenance": "author",
        })

    def test_author_routes_do_not_mutate(self) -> None:
        app = str(CANDIDATE / "app" / "librarian.py")
        before = watched()
        cases = (
            ([app, "review-loop"], "unknown review-loop command"),
            ([app, "authoring"], "unknown authoring command"),
            ([app, "authoring", "form"], "missing --book"),
            ([app, "return-lines"], "command is not on this door"),
            ([app, "where"], "missing --root"),
        )
        for argv, message in cases:
            proc = run(argv, CANDIDATE)
            self.assert_stop(proc, message)
            save_bytes(("route-" + message.replace(" ", "-") + ".stderr"), proc.stderr)
        self.assertEqual(watched(), before)

    def test_author_direct_lab_dispatcher_is_not_an_install(self) -> None:
        book = KEEP / "arg-book"
        book.mkdir(parents=True, exist_ok=True)
        before = watched()
        proc = run(
            [str(LAB / "librarian.py"), "review-report", "--book", str(book), "--source", "0594.probe", "--pass", "05.94"],
            LAB,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, b"")
        self.assertFalse(proc.stdout.lstrip().startswith(b"{"))
        self.assertEqual(watched(), before)
        save_bytes("direct-lab.stderr", proc.stderr)
        RESULTS.append({"direct_lab_exit": proc.returncode, "name": "direct-lab-dispatcher", "provenance": "author"})

    def test_author_unseated_connector_is_refused(self) -> None:
        folder = KEEP / "second-copy" / "notapp"
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)
        copy = folder / "review_report_tools_v2.py"
        shutil.copyfile(ROOT / "app" / "review_report_tools_v2.py", copy)
        book = KEEP / "arg-book"
        book.mkdir(parents=True, exist_ok=True)
        proc = run([str(copy), "--book", str(book), "--source", "0594.probe", "--pass", "05.94"], KEEP)
        seated = copy.resolve().parent.parent
        self.assert_stop(proc, f"copied fixture root {copy.resolve().parent} is not the installed app root {seated}")
        save_bytes("unseated.stderr", proc.stderr)

    def test_author_linked_pin_when_available(self) -> None:
        dest = KEEP / "linked-cut"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(CANDIDATE, dest, ignore=ignore_cache)
        labs = dest / "labs"
        moved = dest / "labs-real"
        if moved.exists():
            shutil.rmtree(moved)
        labs.rename(moved)
        proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(labs), str(moved)], capture_output=True, shell=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        try:
            copied = load("review_report_tools_v2_linked_author", dest / "app" / "review_report_tools_v2.py")
            with self.assertRaises(copied.Refuse) as caught:
                copied.audit_dependencies(dest)
            self.assertEqual(
                str(caught.exception),
                "dependency conflict labs/prime-cycle-pass03/prime_cycle.py is linked and was not followed",
            )
        finally:
            subprocess.run(["cmd", "/c", "rmdir", str(labs)], capture_output=True, shell=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
