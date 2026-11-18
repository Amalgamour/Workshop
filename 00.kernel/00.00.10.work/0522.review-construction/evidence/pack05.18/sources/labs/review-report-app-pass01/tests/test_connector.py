#!/usr/bin/env python3
"""Author tests for the staged review-report connector.

These cases are author work. They are not Prime's independent probes.
Prime's future independent probes, not executed here:
- repeat the three-way compare on the two live addresses
- supply a separate disposable book
- apply the dispatcher diff on a copy and show the librarian.py pin refusal
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
LAB = ROOT / "labs" / "review-report-app-pass01"
BOOK = ROOT / "00.kernel" / "00.00.10.work"
KEEP = Path(r"D:\librarian\temp\0512-0507-report")
CONTRACT = ROOT / "00.kernel" / "00.00.10.work" / "0512.prime-review" / "evidence" / "build05.07" / "CONTRACT.md"
CONTRACT_SHA = "a2a915e2ab133eb3fb4536d1c7d50361ea33d9a11dca14654a6aeea3d3cedc08"
CONTRACT_BYTES = 7879
FROZEN_TEST_SHA = "f477fd4e4dac922435fac822a5b85ee34b34d731583a730842b08f5c110e18de"
FROZEN_TEST_BYTES = 32678
LIBRARIAN_SHA = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"
LIBRARIAN_BYTES = 12204
PRIME_FUTURE_PROBES = (
    "repeat the three-way compare on the two live addresses",
    "supply a separate disposable book",
    "apply the dispatcher diff on a copy and show the librarian.py pin refusal",
)
WATCH = (
    "app/librarian.py",
    "app/README.md",
    "app/review-report-v1.json",
    "app/review_report_tools_v1.py",
    "labs/review-report-pass01/report.py",
    "labs/review-report-pass02/report.py",
    "labs/review-report-pass03/report.py",
    "labs/review-report-pass03/PRIME-USE.md",
    "labs/review-report-pass03/tests/test_report.py",
    "00.kernel/00.00.10.work/0512.prime-review/05.06.md",
    "00.kernel/00.00.10.work/0512.prime-review/05.07.md",
    "00.kernel/00.00.10.work/0512.prime-review/06.10.md",
    "00.kernel/00.00.10.work/0512.prime-review/evidence/build05.06/CONTRACT.md",
    "00.kernel/00.00.10.work/0512.prime-review/evidence/build05.07/CONTRACT.md",
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
    ROOT / "labs" / "workbook-review-pass01" / "__pycache__",
    ROOT / "labs" / "workbook-review-pass02" / "__pycache__",
    ROOT / "labs" / "workbook-review-pass03" / "__pycache__",
)
RESULTS: list[dict] = []


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


door = load("review_report_tools_v1_author", ROOT / "app" / "review_report_tools_v1.py")
wb = load("workbook_review_pass03_author_helpers", ROOT / "labs" / "workbook-review-pass03" / "tests" / "test_workbook.py")


def environment() -> dict:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def launch(argv: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", *argv],
        cwd=str(door.installed_root()),
        env=environment(),
        capture_output=True,
        shell=False,
    )


def three(book: str, source: str, pass_id: str) -> tuple:
    root = str(door.installed_root())
    direct = launch([
        str(ROOT / "labs" / "review-report-pass03" / "report.py"),
        "--code-root", root, "--book", book, "--source", source, "--pass", pass_id,
    ])
    tool = launch([
        str(ROOT / "app" / "review_report_tools_v1.py"),
        "--book", book, "--source", source, "--pass", pass_id,
    ])
    invoked = launch([
        str(LAB / "invoke.py"),
        "review-report", "--book", book, "--source", source, "--pass", pass_id,
    ])
    return direct, tool, invoked


def save_command(name: str, runs: tuple) -> None:
    folder = KEEP / "commands" / name
    folder.mkdir(parents=True, exist_ok=True)
    for label, run in zip(("direct", "tool", "invoke"), runs):
        (folder / f"{label}.stdout").write_bytes(run.stdout)
        (folder / f"{label}.stderr").write_bytes(run.stderr)
        (folder / f"{label}.exit").write_bytes(f"{run.returncode}\n".encode("utf-8"))


def save_hostile(name: str, payload: bytes) -> None:
    latest = KEEP / "hostile-latest"
    first = KEEP / "hostile-first"
    latest.mkdir(parents=True, exist_ok=True)
    first.mkdir(parents=True, exist_ok=True)
    (latest / name).write_bytes(payload)
    dest = first / name
    if not dest.exists():
        dest.write_bytes(payload)


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
        caches.extend(f"{path.relative_to(ROOT).as_posix()} {sha256(path.read_bytes())} {path.stat().st_size}" for path in sorted(folder.rglob("*")) if path.is_file())
    return {"caches": caches, "files": files, "trees": trees}


def norm(data: bytes) -> str:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n").decode("utf-8")


def plant(book: Path, source: str, pass_id: str) -> None:
    if book.exists():
        shutil.rmtree(book)
    submission = b"Substantive submission for the connector fixture. It names verification in prose only.\n"
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


def copy_cut(dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    for rel in door.TOOLS:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, target)
    target = dest / "app" / "review-report-v1.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "app" / "review-report-v1.json", target)


def extract(stdout: bytes, code: int) -> dict:
    report = json.loads(stdout.decode("utf-8"))
    artifacts = report["artifacts"]
    counters = {}
    for key in ("addressed_sources", "content_blobs", "physical_files"):
        item = artifacts[key]
        counters[key] = {
            "bytes": item.get("bytes"),
            "count": item.get("count"),
            "provenance": item.get("provenance"),
            "scope": item.get("scope"),
        }
    attention = report.get("attention") if isinstance(report.get("attention"), dict) else {}
    lines = attention.get("lines")
    return {
        "attention_lines": len(lines) if isinstance(lines, list) else None,
        "attention_state": attention.get("state"),
        "counters": counters,
        "custody": report.get("custody"),
        "exit": report.get("exit"),
        "process_exit": code,
        "review_id": report.get("review_id"),
        "schema": report.get("schema"),
        "stale": report.get("stale"),
        "state": report.get("state"),
        "tests_note_in_projection": "tests_note" in str(report.get("projection")),
        "unique_files_absent": "unique_files" not in artifacts,
    }


class ConnectorTests(unittest.TestCase):
    def assert_same(self, runs: tuple) -> None:
        base = runs[0]
        for label, run in zip(("tool", "invoke"), runs[1:]):
            self.assertEqual(run.returncode, base.returncode, label)
            self.assertEqual(run.stdout, base.stdout, label + " stdout")
            self.assertEqual(run.stderr, base.stderr, label + " stderr")

    def assert_report(self, runs: tuple, state: str | None = None) -> dict:
        self.assert_same(runs)
        code = runs[0].returncode
        self.assertIn(code, (0, 1))
        self.assertEqual(runs[0].stderr, b"")
        report = json.loads(runs[0].stdout.decode("utf-8"))
        self.assertEqual(report["schema"], "review-report/3")
        self.assertEqual(report["exit"], code)
        artifacts = report["artifacts"]
        self.assertNotIn("unique_files", artifacts)
        physical = artifacts["physical_files"]
        self.assertIsNone(physical["count"])
        self.assertIsNone(physical["bytes"])
        self.assertEqual(physical["provenance"], "not-established")
        self.assertEqual(physical["scope"], "verified-physical-files")
        if state is not None:
            self.assertEqual(report["state"], state)
            self.assertEqual(code, 1)
        return extract(runs[0].stdout, code)

    def assert_stop(self, proc: subprocess.CompletedProcess, message: str) -> None:
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertEqual(proc.stdout, b"")
        self.assertEqual(norm(proc.stderr), f"stop: {message}\n")

    def test_author_contract_and_dispatcher_stay_put(self) -> None:
        data = CONTRACT.read_bytes()
        self.assertEqual(len(data), CONTRACT_BYTES)
        self.assertEqual(sha256(data), CONTRACT_SHA)
        self.assertNotIn(b"\r", data)
        live = (ROOT / "app" / "librarian.py").read_bytes()
        self.assertEqual(len(live), LIBRARIAN_BYTES)
        self.assertEqual(sha256(live), LIBRARIAN_SHA)
        self.assertNotIn(b'"review-report"', live)
        proposed = (LAB / "librarian.py").read_text(encoding="utf-8")
        self.assertIn("review-report forwards one selected read-only report", proposed)
        self.assertIn('"review-report",', proposed)
        self.assertIn('if command == "review-report":', proposed)
        page = (BOOK / "0512.prime-review" / "05.07.md").read_text(encoding="utf-8")
        self.assertIn("## Return pointer\nPENDING.\n", page)
        self.assertIn("## Review - Codex Prime\nPENDING.\n", page)
        self.assertIn("state: PREPARED; execute on named Director invocation; staged app connector\n", page)
        self.assertEqual((LAB / "PRIME-USE.md").read_bytes(), (BOOK / "0512.prime-review" / "evidence" / "build05.07" / "PRIME-USE.md").read_bytes())
        door.audit_dependencies(door.installed_root())

    def test_author_prime_probes_are_not_this_suite(self) -> None:
        names = [item for item in dir(ConnectorTests) if item.startswith("test_")]
        self.assertTrue(names)
        self.assertTrue(all(item.startswith("test_author_") for item in names))
        self.assertEqual(len(PRIME_FUTURE_PROBES), 3)

    def test_author_mid_observation_evidence_stays_frozen(self) -> None:
        path = ROOT / "labs" / "review-report-pass03" / "tests" / "test_report.py"
        data = path.read_bytes()
        self.assertEqual(len(data), FROZEN_TEST_BYTES)
        self.assertEqual(sha256(data), FROZEN_TEST_SHA)
        self.assertIn(b"def test_author_journal_current_changed_during_read", data)
        self.assertIn(b'result["state"], "held"', data)

    def test_author_live_0512_05_06(self) -> None:
        before = watched()
        runs = three(str(BOOK), "0512.prime-review", "05.06")
        after = watched()
        self.assertEqual(before, after)
        save_command("live-0512-05-06", runs)
        summary = self.assert_report(runs)
        RESULTS.append({"name": "live-0512-05-06", "no_write": True, "summary": summary})

    def test_author_live_0521_05_13(self) -> None:
        before = watched()
        runs = three(str(BOOK), "0521.return-placement", "05.13")
        after = watched()
        self.assertEqual(before, after)
        save_command("live-0521-05-13", runs)
        summary = self.assert_report(runs)
        RESULTS.append({"name": "live-0521-05-13", "no_write": True, "summary": summary})

    def test_author_fixture_missing_review(self) -> None:
        book = KEEP / "books" / "missing"
        source, pass_id = "0592.connector-missing", "05.92"
        plant(book, source, pass_id)
        before = tree_digest(book)
        runs = three(str(book), source, pass_id)
        self.assertEqual(tree_digest(book), before)
        save_command("fixture-missing", runs)
        summary = self.assert_report(runs, "not-recorded")
        self.assertIsNone(summary["stale"])
        RESULTS.append({"name": "fixture-missing", "no_write": True, "summary": summary})

    def test_author_fixture_stale_note(self) -> None:
        book = KEEP / "books" / "stale"
        source, pass_id = "0591.connector-stale", "05.91"
        plant(book, source, pass_id)
        publish(book, source, pass_id)
        (book / "note.md").write_bytes(b"NOTE changed\n")
        before = tree_digest(book)
        runs = three(str(book), source, pass_id)
        self.assertEqual(tree_digest(book), before)
        save_command("fixture-stale", runs)
        summary = self.assert_report(runs, "stale")
        self.assertIs(summary["stale"], True)
        RESULTS.append({"name": "fixture-stale", "no_write": True, "summary": summary})

    def test_author_fixture_digest_held(self) -> None:
        book = KEEP / "books" / "held"
        source, pass_id = "0593.connector-held", "05.93"
        plant(book, source, pass_id)
        review = publish(book, source, pass_id)
        record = book / "workbook-review" / source / pass_id / "reviews" / review / "record.json"
        text = record.read_text(encoding="utf-8")
        self.assertIn("The disposable note is present.", text)
        record.write_text(text.replace("The disposable note is present.", "The disposable note is present!", 1), encoding="utf-8", newline="\n")
        before = tree_digest(book)
        runs = three(str(book), source, pass_id)
        self.assertEqual(tree_digest(book), before)
        save_command("fixture-held", runs)
        summary = self.assert_report(runs, "held")
        RESULTS.append({"name": "fixture-held", "no_write": True, "summary": summary})

    def test_author_hostile_other_root(self) -> None:
        other = KEEP / "other-root"
        other.mkdir(parents=True, exist_ok=True)
        args = ["--book", str(other), "--source", "0594.probe", "--pass", "05.94"]
        before = watched()
        with self.assertRaises(door.Refuse) as caught:
            door.perform(args, other)
        self.assertEqual(watched(), before)
        message = f"copied fixture root {other.resolve()} is not the installed app root {door.installed_root()}"
        self.assertEqual(str(caught.exception), message)
        save_hostile("other-root.txt", (message + "\n").encode("utf-8"))

    def test_author_hostile_second_copy(self) -> None:
        folder = KEEP / "second-copy" / "notapp"
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)
        copy = folder / "review_report_tools_v1.py"
        shutil.copyfile(ROOT / "app" / "review_report_tools_v1.py", copy)
        other = KEEP / "other-root"
        other.mkdir(parents=True, exist_ok=True)
        args = ["--book", str(other), "--source", "0594.probe", "--pass", "05.94"]
        copied = load("copied_review_report_tools_author", copy)
        before = watched()
        with self.assertRaises(copied.Refuse) as caught:
            copied.perform(args, ROOT)
        self.assertEqual(watched(), before)
        message = f"copied fixture root {copy.resolve().parent} is not the installed app root {ROOT.resolve()}"
        self.assertEqual(str(caught.exception), message)
        proc = launch([str(copy), *args])
        seated = copy.resolve().parent.parent
        main_message = f"copied fixture root {copy.resolve().parent} is not the installed app root {seated}"
        self.assert_stop(proc, main_message)
        save_hostile("second-copy.stderr", proc.stderr)
        save_hostile("second-copy.stdout", proc.stdout)

    def test_author_hostile_flags_escape_and_arguments(self) -> None:
        other = KEEP / "other-root"
        other.mkdir(parents=True, exist_ok=True)
        base = ["--book", str(other), "--source", "0594.probe", "--pass", "05.94"]
        before = watched()
        for flag in ("--publish", "--code-root", "--tool", "--record", "--prepare", "--form"):
            proc = launch([str(ROOT / "app" / "review_report_tools_v1.py"), flag, *base])
            self.assert_stop(proc, f"unknown flag {flag}")
            save_hostile(f"flag-{flag[2:]}.stderr", proc.stderr)
        proc = launch([str(ROOT / "app" / "review_report_tools_v1.py"), "--book", str(other), "--book", str(other), "--source", "0594.probe", "--pass", "05.94"])
        self.assert_stop(proc, "repeated --book")
        proc = launch([str(ROOT / "app" / "review_report_tools_v1.py"), "--book", str(other), "--source", "0594.probe", "--pass", "5"])
        self.assert_stop(proc, "pass is not 05.NN")
        proc = launch([str(ROOT / "app" / "review_report_tools_v1.py"), "--book", "labs", "--source", "0594.probe", "--pass", "05.94"])
        self.assert_stop(proc, "book must be an absolute directory and was not followed when linked")
        proc = launch([str(ROOT / "app" / "review_report_tools_v1.py"), "--book", str(other), "--source", "nested/page", "--pass", "05.94"])
        self.assert_stop(proc, "source is a page id")
        proc = launch([str(ROOT / "app" / "review_report_tools_v1.py"), "review-report", *base])
        self.assert_stop(proc, "unknown argument review-report")
        raw = (ROOT / "app" / "review-report-v1.json").read_bytes()
        document = json.loads(raw.decode("utf-8"))
        document["tools"]["../outside.py"] = {"bytes": 1, "sha256": "aa"}
        cooked = json.dumps(document).encode("utf-8")
        with self.assertRaises(door.Refuse) as caught:
            door.assess_declaration(cooked)
        self.assertEqual(str(caught.exception), "tool path escapes the code root")
        self.assertEqual(watched(), before)
        save_hostile("escape.txt", b"tool path escapes the code root\n")

    def test_author_wrong_and_missing_dependency(self) -> None:
        dest = KEEP / "tampered-cut"
        copy_cut(dest)
        rel = "labs/review-report-pass03/report.py"
        path = dest / rel
        data = bytearray(path.read_bytes())
        data[-1] = (data[-1] + 1) % 256
        path.write_bytes(bytes(data))
        got = sha256(path.read_bytes())
        want = door.TOOLS[rel]
        before = watched()
        with self.assertRaises(door.Refuse) as caught:
            door.audit_dependencies(dest)
        message = (
            f"dependency conflict {rel} got {len(data)} bytes sha256 {got} "
            f"want {want['bytes']} bytes sha256 {want['sha256']}"
        )
        self.assertEqual(str(caught.exception), message)
        self.assertIn(want["sha256"], message)
        self.assertIn(got, message)
        self.assertNotEqual(got, want["sha256"])
        live = (ROOT / rel).read_bytes()
        self.assertEqual(len(live), want["bytes"])
        self.assertEqual(sha256(live), want["sha256"])
        save_hostile("dependency.txt", (message + "\n").encode("utf-8"))
        missing = KEEP / "missing-cut"
        copy_cut(missing)
        gone = missing / "app" / "review-loop-v4.json"
        gone.unlink()
        with self.assertRaises(door.Refuse) as caught:
            door.audit_dependencies(missing)
        self.assertEqual(
            str(caught.exception),
            "dependency conflict app/review-loop-v4.json got missing want 2519 bytes sha256 769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723",
        )
        self.assertEqual(watched(), before)

    def test_author_linked_pin_when_available(self) -> None:
        dest = KEEP / "linked-cut"
        copy_cut(dest)
        labs = dest / "labs"
        moved = dest / "labs-real"
        labs.rename(moved)
        proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(labs), str(moved)], capture_output=True, shell=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        with self.assertRaises(door.Refuse) as caught:
            door.audit_dependencies(dest)
        self.assertEqual(
            str(caught.exception),
            "dependency conflict labs/prime-cycle-pass03/prime_cycle.py is linked and was not followed",
        )

    def test_author_routes_do_not_mutate(self) -> None:
        before = watched()
        cases = (
            (["review-loop"], "unknown review-loop command"),
            (["authoring"], "unknown authoring command"),
            (["authoring", "form"], "missing --book"),
            (["return-lines"], "command is not on this door"),
            (["where"], "missing --root"),
        )
        for args, message in cases:
            proc = launch([str(LAB / "invoke.py"), *args])
            self.assert_stop(proc, message)
            save_hostile(f"route-{' '.join(args)}.stderr", proc.stderr)
        self.assertEqual(watched(), before)

    def test_author_direct_lab_dispatcher_is_not_an_install(self) -> None:
        other = KEEP / "other-root"
        other.mkdir(parents=True, exist_ok=True)
        before = watched()
        proc = launch([
            str(LAB / "librarian.py"),
            "review-report",
            "--book", str(other),
            "--source", "0594.probe",
            "--pass", "05.94",
        ])
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, b"")
        self.assertFalse(proc.stdout.lstrip().startswith(b"{"))
        self.assertEqual(watched(), before)
        save_hostile("direct-lab.stderr", proc.stderr)
        save_hostile("direct-lab.stdout", proc.stdout)
        RESULTS.append({"direct_lab_exit": proc.returncode, "name": "direct-lab-dispatcher"})


def tearDownModule() -> None:
    KEEP.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(RESULTS, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (KEEP / "author-results.json").write_bytes(raw)


if __name__ == "__main__":
    unittest.main(verbosity=2)
