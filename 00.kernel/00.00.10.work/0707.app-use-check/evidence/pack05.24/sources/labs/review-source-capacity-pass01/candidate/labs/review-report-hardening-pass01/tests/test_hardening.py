#!/usr/bin/env python3
"""Author tests for the hardening review-report candidate.

These cases are author work. They are not Prime's independent probes.
The B-05 and B-01 logs under the keep directory are known reproductions
of the staged 05.08 runtime. They are not counted here.
Prime's future independent probes, not executed here:
- repeat the candidate comparison on a book this author did not plant
- select the candidate dispatcher on the active app
- file 0112.prime-review
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
LAB = ROOT / "labs" / "review-report-hardening-pass01"
BOOK = ROOT / "00.kernel" / "00.00.10.work"
PACK = BOOK / "0512.prime-review"
KEEP = Path(r"D:\librarian\temp\0512-0509-report")
CANDIDATE = (KEEP / "candidate").resolve()
PAGE = PACK / "05.09.md"
CONTRACT = PACK / "evidence" / "build05.09" / "CONTRACT.md"
CONTRACT_SHA = "1ac2b93a03e5a17a38c0deb3046b78324d374e3cec9d6239830d006019917f5b"
CONTRACT_BYTES = 7827
BODY_SHA = "6d12d488cf558b93dd85cbfbab589a49f9c3febb4e551998ea299725645eba6a"
OLD_SHA = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"
OLD_BYTES = 12204
DEPLOY_SHA = "d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52"
DEPLOY_BYTES = 12805
NEW_SHA = "f1d23d455f20319e3f430d345b2893bda039fd8c84be4f3691b4e4be123b8983"
NEW_BYTES = 12804
V1_SHA = "00489768c33874b282a3732709eb40503d0c3ebfad2826a9b3e8be6d832a5e2c"
V1_BYTES = 13708
V2_SHA = "81993c712d74e1d9e5155011fa949731a492ca6a2c626d27c6bebd9591965aab"
V2_BYTES = 13956
README_SHA = "3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920"
README_BYTES = 39687
FROZEN_TEST_SHA = "f477fd4e4dac922435fac822a5b85ee34b34d731583a730842b08f5c110e18de"
FROZEN_TEST_BYTES = 32678
MARKER = "\n## Return pointer\n"
REVIEW = "\n## Review - Codex Prime\n"
RUNTIME_REL = "labs/review-report-hardening-pass01/report.py"
DEPLOY_RUNTIME = "labs/review-report-deployment-pass01/report.py"
PRIME_FUTURE_PROBES = (
    "repeat the candidate comparison on a book this author did not plant",
    "select the candidate dispatcher on the active app",
    "file 0112.prime-review",
)
ENVELOPE = (
    "accepted",
    "action_released",
    "approved",
    "authority",
    "closes_work",
    "releases_action",
    "task_association",
)
WATCH = (
    "app/librarian.py",
    "app/README.md",
    "app/review-report-v1.json",
    "app/review_report_tools_v1.py",
    "app/review-report-v2.json",
    "app/review_report_tools_v2.py",
    "app/review-report-v3.json",
    "app/review_report_tools_v3.py",
    "labs/review-report-pass01/report.py",
    "labs/review-report-pass02/report.py",
    "labs/review-report-pass03/report.py",
    "labs/review-report-pass03/PRIME-USE.md",
    "labs/review-report-pass03/tests/test_report.py",
    "labs/review-report-deployment-pass01/report.py",
    "labs/review-report-deployment-pass01/librarian.py",
    "labs/review-report-hardening-pass01/report.py",
    "labs/review-report-hardening-pass01/librarian.py",
    "labs/workbook-review-pass03/workbook.py",
    "00.kernel/00.00.10.work/0512.prime-review/05.06.md",
    "00.kernel/00.00.10.work/0512.prime-review/05.08.md",
    "00.kernel/00.00.10.work/0512.prime-review/05.09.md",
    "00.kernel/00.00.10.work/0512.prime-review/06.14.md",
    "00.kernel/00.00.10.work/0512.prime-review/06.15.md",
    "00.kernel/00.00.10.work/0512.prime-review/evidence/build05.06/CONTRACT.md",
    "00.kernel/00.00.10.work/0512.prime-review/evidence/build05.08/CONTRACT.md",
    "00.kernel/00.00.10.work/0512.prime-review/evidence/build05.09/CONTRACT.md",
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
    ROOT / "labs" / "review-report-hardening-pass01" / "__pycache__",
    ROOT / "labs" / "review-report-hardening-pass01" / "tests" / "__pycache__",
    ROOT / "labs" / "workbook-review-pass03" / "__pycache__",
)
RESULTS: list[dict] = []


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


door = load("review_report_tools_v3_author", ROOT / "app" / "review_report_tools_v3.py")
runtime = load("review_report_hardening_author", LAB / "report.py")
wb = load("workbook_review_pass03_author_helpers_0509", ROOT / "labs" / "workbook-review-pass03" / "tests" / "test_workbook.py")


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
    submission = b"Substantive submission for the hardening fixture. It names verification in prose only.\n"
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
    for key in ("addressed_sources", "content_blobs", "intake_roles", "physical_files"):
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
        "observation_status": observation.get("status"),
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


def blank_report() -> dict:
    return runtime.base_report(
        {"book": "synthetic", "code_root": "synthetic", "pass": "05.09", "source": "synthetic"},
        "readable",
        0,
    )


def supported_envelope() -> dict:
    return {
        "accepted": False,
        "approved": False,
        "authority": "none",
        "closes_work": False,
        "releases_action": False,
        "task_association": "not-established",
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


class HardeningTests(unittest.TestCase):
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
        self.assertNotIn("envelope_withheld", report)
        self.assertNotIn("invalid_rows", report)
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
        rollback = (PACK / "evidence" / "build05.09" / "rollback-librarian.py").read_bytes()
        self.assertEqual(rollback, live)
        v1 = (ROOT / "app" / "review_report_tools_v1.py").read_bytes()
        self.assertEqual(len(v1), V1_BYTES)
        self.assertEqual(sha256(v1), V1_SHA)
        v2 = (ROOT / "app" / "review_report_tools_v2.py").read_bytes()
        self.assertEqual(len(v2), V2_BYTES)
        self.assertEqual(sha256(v2), V2_SHA)
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
        declaration = json.loads((ROOT / "app" / "review-report-v3.json").read_text(encoding="utf-8"))
        self.assertEqual(declaration["schema"], "review-report-command/2")
        self.assertEqual(declaration["version"], 3)
        self.assertEqual(set(declaration["tools"]), set(door.TOOLS))
        page_parts(PAGE.read_bytes())
        self.assertEqual((LAB / "PRIME-USE.md").read_bytes(), (PACK / "evidence" / "build05.09" / "PRIME-USE.md").read_bytes())
        self.assertEqual((LAB / "INTEGRATION.md").read_bytes(), (PACK / "evidence" / "build05.09" / "INTEGRATION.md").read_bytes())
        deploy = (ROOT / "labs" / "review-report-deployment-pass01" / "librarian.py").read_bytes()
        self.assertEqual(len(deploy), DEPLOY_BYTES)
        self.assertEqual(sha256(deploy), DEPLOY_SHA)
        book = KEEP / "arg-book"
        book.mkdir(parents=True, exist_ok=True)
        proc = run(
            [str(ROOT / "app" / "review_report_tools_v3.py"), "--book", str(book), "--source", "0594.probe", "--pass", "05.94"],
            ROOT,
        )
        self.assert_stop(
            proc,
            f"dependency conflict app/librarian.py got {OLD_BYTES} bytes sha256 {OLD_SHA} want {NEW_BYTES} bytes sha256 {NEW_SHA}",
        )
        save_bytes("active-v3-refuses.stderr", proc.stderr)

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
        names = [item for item in dir(HardeningTests) if item.startswith("test_")]
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
        for rel, digest, size in (
            ("labs/review-report-pass01/report.py", "72e9bda15c5f3ca844350be5dae2fcfcf4e7c609c262b8f7e702d64467eb94cc", 42127),
            ("labs/review-report-pass02/report.py", "d13d8d4f54d79cbdb22e1a40fdffb89bd26b85a611bf8620dc36854be9eb852e", 38323),
            ("labs/review-report-pass03/report.py", "70028dfe97bc6178a3497c814cf585476bb0b41650ce67fc79dd3d5b118dfade", 8091),
            (DEPLOY_RUNTIME, "0f7def8d353506b93c71d130d740cd1262717ce493a868fc356e09ab925f7506", 6294),
        ):
            data = (ROOT / rel).read_bytes()
            self.assertEqual(len(data), size, rel)
            self.assertEqual(sha256(data), digest, rel)

    def test_author_live_0512_05_06(self) -> None:
        before = watched()
        base, inst = pair(str(BOOK), "0512.prime-review", "05.06")
        self.assertEqual(watched(), before)
        save_pair("live-0512-05-06", base, inst)
        summary = self.assert_same_pair(base, inst)
        self.assertEqual(summary["state"], "readable")
        self.assertEqual(summary["process_exit"], 0)
        self.assertEqual(summary["review_id"], "wbf38837cf0fa9c6b")
        self.assertIs(summary["stale"], False)
        self.assertEqual(summary["custody"], "missing")
        self.assertEqual(summary["authority"], "none")
        self.assertEqual(summary["disposition"], "accepted")
        self.assertEqual(summary["operation"], "continue")
        self.assertEqual(summary["publication_status"], "published")
        self.assertEqual(summary["publication_class"], "complete")
        self.assertIs(summary["observation_stable"], True)
        self.assertIs(summary["work_complete"], False)
        self.assertIs(summary["action_released"], False)
        self.assertIs(summary["accepted"], False)
        self.assertIs(summary["approved"], False)
        self.assertIs(summary["closes_work"], False)
        self.assertIs(summary["releases_action"], False)
        self.assertEqual(summary["task_association"], "not-established")
        self.assertEqual(summary["attention_lines"], 5)
        self.assertEqual(summary["declared_count"], 14)
        self.assertEqual(summary["declared_bytes"], 149885)
        self.assertEqual(summary["counters"]["intake_roles"]["count"], 17)
        self.assertEqual(summary["counters"]["intake_roles"]["bytes"], 169310)
        self.assertEqual(summary["counters"]["addressed_sources"]["count"], 16)
        self.assertEqual(summary["counters"]["addressed_sources"]["bytes"], 157007)
        self.assertEqual(summary["counters"]["content_blobs"]["count"], 15)
        self.assertEqual(summary["counters"]["content_blobs"]["bytes"], 127265)
        self.assertEqual(summary["hash_match"], 14)
        self.assertEqual(summary["hash_mismatch"], 0)
        self.assertEqual(summary["not_verified"], 0)
        self.assertIsNone(summary["counters"]["physical_files"]["count"])
        self.assertEqual(summary["tests_note_type"], "dict")
        RESULTS.append({"name": "live-0512-05-06", "no_write": True, "provenance": "author", "same_bytes": True, "summary": summary})

    def test_author_live_0521_05_13(self) -> None:
        before = watched()
        base, inst = pair(str(BOOK), "0521.return-placement", "05.13")
        self.assertEqual(watched(), before)
        save_pair("live-0521-05-13", base, inst)
        summary = self.assert_same_pair(base, inst)
        self.assertEqual(summary["state"], "readable")
        self.assertEqual(summary["process_exit"], 0)
        self.assertEqual(summary["review_id"], "webe8f0a86f3de800")
        self.assertEqual(summary["custody"], "missing")
        self.assertEqual(summary["authority"], "none")
        self.assertIs(summary["work_complete"], False)
        self.assertIs(summary["action_released"], False)
        self.assertIs(summary["observation_stable"], True)
        self.assertEqual(summary["attention_lines"], 6)
        self.assertEqual(summary["declared_count"], 5)
        self.assertEqual(summary["declared_bytes"], 81671)
        self.assertEqual(summary["counters"]["intake_roles"]["count"], 9)
        self.assertEqual(summary["counters"]["intake_roles"]["bytes"], 95759)
        self.assertEqual(summary["counters"]["addressed_sources"]["count"], 7)
        self.assertEqual(summary["counters"]["addressed_sources"]["bytes"], 90980)
        self.assertEqual(summary["counters"]["content_blobs"]["count"], 7)
        self.assertEqual(summary["counters"]["content_blobs"]["bytes"], 90980)
        self.assertEqual(summary["hash_match"], 5)
        self.assertIsNone(summary["counters"]["physical_files"]["count"])
        RESULTS.append({"name": "live-0521-05-13", "no_write": True, "provenance": "author", "same_bytes": True, "summary": summary})

    def test_author_fixture_missing_review(self) -> None:
        book = KEEP / "books" / "missing"
        source, pass_id = "0585.hardening-missing", "05.85"
        plant(book, source, pass_id)
        before = tree_digest(book)
        base, inst = pair(str(book), source, pass_id)
        self.assertEqual(tree_digest(book), before)
        save_pair("fixture-missing", base, inst)
        summary = self.assert_same_pair(base, inst)
        self.assertEqual(summary["state"], "not-recorded")
        self.assertIsNone(summary["stale"])
        self.assertEqual(summary["authority"], "none")
        RESULTS.append({"name": "fixture-missing", "no_write": True, "provenance": "author", "same_bytes": True, "summary": summary})

    def test_author_fixture_stale_note(self) -> None:
        book = KEEP / "books" / "stale"
        source, pass_id = "0584.hardening-stale", "05.84"
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
        self.assertEqual(summary["observation_status"], "coherent")
        self.assertEqual(summary["authority"], "none")
        self.assertIs(summary["action_released"], False)
        RESULTS.append({"name": "fixture-stale", "no_write": True, "provenance": "author", "same_bytes": True, "summary": summary})

    def test_author_fixture_digest_held(self) -> None:
        book = KEEP / "books" / "held"
        source, pass_id = "0586.hardening-held", "05.86"
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
        self.assertEqual(base.returncode, 1, base.stderr)
        self.assertEqual(inst.returncode, 1, inst.stderr)
        base_report = json.loads(base.stdout.decode("utf-8"))
        inst_report = json.loads(inst.stdout.decode("utf-8"))
        self.assertEqual(base_report["state"], "held")
        self.assertEqual(base_report["authority"], "none")
        self.assertIs(base_report["accepted"], False)
        self.assertEqual(inst_report["state"], "held")
        self.assertIs(inst_report["stale"], True)
        self.assertEqual(inst_report["observation"]["status"], "mismatch")
        self.assertIs(inst_report["observation"]["stable"], True)
        for key in ENVELOPE:
            self.assertIsNone(inst_report[key], key)
        self.assertEqual(inst_report["envelope_withheld"]["provenance"], "withheld-current-cut")
        self.assertNotEqual(base.stdout, inst.stdout)
        RESULTS.append({
            "baseline_authority": base_report["authority"],
            "installed_authority": inst_report["authority"],
            "name": "fixture-held",
            "no_write": True,
            "provenance": "author",
            "same_bytes": False,
            "summary": summary_of(inst.stdout, inst.returncode),
        })

    def test_author_wrong_app_hash(self) -> None:
        path = CANDIDATE / "app" / "librarian.py"
        original = path.read_bytes()
        book = KEEP / "arg-book"
        book.mkdir(parents=True, exist_ok=True)
        marker = b"hardening connector"
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
                    str(CANDIDATE / "labs" / "review-report-hardening-pass01" / "report.py"),
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
        raw = (ROOT / "app" / "review-report-v3.json").read_bytes()
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
        v1 = run(
            [str(CANDIDATE / "app" / "review_report_tools_v1.py"), "--book", str(book), "--source", "0594.probe", "--pass", "05.94"],
            CANDIDATE,
        )
        self.assert_stop(
            v1,
            f"dependency conflict app/librarian.py got {NEW_BYTES} bytes sha256 {NEW_SHA} want {OLD_BYTES} bytes sha256 {OLD_SHA}",
        )
        v2 = run(
            [str(CANDIDATE / "app" / "review_report_tools_v2.py"), "--book", str(book), "--source", "0594.probe", "--pass", "05.94"],
            CANDIDATE,
        )
        self.assert_stop(
            v2,
            f"dependency conflict app/librarian.py got {NEW_BYTES} bytes sha256 {NEW_SHA} want {DEPLOY_BYTES} bytes sha256 {DEPLOY_SHA}",
        )
        deployed = run(
            [
                str(CANDIDATE / "labs" / "review-report-deployment-pass01" / "report.py"),
                "--code-root", str(CANDIDATE),
                "--book", str(book),
                "--source", "0594.probe",
                "--pass", "05.94",
            ],
            CANDIDATE,
        )
        self.assertEqual(deployed.returncode, 2, deployed.stderr)
        self.assertTrue(deployed.stdout.startswith(b"{"))
        self.assertIn(f"want {DEPLOY_BYTES} bytes sha256 {DEPLOY_SHA}".encode("utf-8"), deployed.stderr)
        self.assertEqual(tree_digest(book), digest)
        self.assertEqual(watched(), before)
        save_bytes("historical-pass03.stderr", direct.stderr)
        save_bytes("historical-v1.stderr", v1.stderr)
        save_bytes("historical-v2.stderr", v2.stderr)
        save_bytes("historical-deployment.stderr", deployed.stderr)
        RESULTS.append({
            "historical_deployment_exit": deployed.returncode,
            "historical_pass03_exit": direct.returncode,
            "historical_v1_exit": v1.returncode,
            "historical_v2_exit": v2.returncode,
            "hostile_hardening": True,
            "name": "historical-chain-refuses-installed-dispatcher",
            "provenance": "author",
        })

    def test_author_hostile_swapped_runtime_stops_app_command(self) -> None:
        path = CANDIDATE / RUNTIME_REL
        original = path.read_bytes()
        book = KEEP / "books" / "missing"
        if not book.exists():
            plant(book, "0585.hardening-missing", "05.85")
        before_book = tree_digest(book)
        before = watched()
        flipped = bytearray(original)
        flipped[-1] = (flipped[-1] + 1) % 256
        path.write_bytes(bytes(flipped))
        try:
            got = sha256(path.read_bytes())
            want = door.TOOLS[RUNTIME_REL]
            proc = run_app(str(book), "0585.hardening-missing", "05.85")
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
        RESULTS.append({"hostile_hardening": True, "name": "swapped-runtime-stops-app-command", "provenance": "author"})

    def test_author_hostile_malformed_envelope_is_withheld(self) -> None:
        report = blank_report()
        report["authority"] = "Director"
        report["action_released"] = {"x": 1}
        report["releases_action"] = {"x": 1}
        report["accepted"] = False
        report["approved"] = False
        report["disposition"] = "accepted"
        runtime.p2.mark_unstable(
            report,
            {"journal_current": "w-synthetic"},
            {"journal_current": "w-other"},
            ["journal_current"],
        )
        self.assertEqual(report["state"], "held")
        self.assertIsNone(report["authority"])
        self.assertIsNone(report["action_released"])
        self.assertIsNone(report["accepted"])
        self.assertEqual(report["envelope_withheld"]["provenance"], "withheld-current-cut")
        self.assertEqual(report["historical_supplied"]["provenance"], "historical-supplied")
        self.assertEqual(report["historical_supplied"]["fields"]["disposition"], "accepted")
        self.assertIsNone(report["disposition"])
        save_bytes("hostile-envelope.json", (json.dumps({
            "accepted": report["accepted"],
            "action_released": report["action_released"],
            "authority": report["authority"],
            "provenance": "author",
            "state": report["state"],
        }, indent=2, sort_keys=True) + "\n").encode("utf-8"))
        RESULTS.append({
            "hostile_hardening": True,
            "known_reproduction": False,
            "name": "malformed-envelope-is-withheld",
            "provenance": "author",
        })

    def test_author_hostile_invalid_rows_do_not_complete_a_measured_total(self) -> None:
        digest = "a" * 64
        body = runtime.p3.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": [
                {"bytes": 10, "declared_bytes": 10, "declared_sha256": digest, "path": "a.txt", "role": "artifact", "root": "book", "sha256": digest},
                "garbage",
                7,
                None,
            ]}},
            "measurement": "complete",
        })
        self.assertEqual(body["invalid_rows"]["count"], 3)
        self.assertIs(body["invalid_rows"]["dropped"], False)
        self.assertEqual(len(body["raw_rows"]), 4)
        self.assertIsNone(body["intake_roles"]["count"])
        self.assertEqual(body["intake_roles"]["count_state"], "unknown")
        self.assertIsNone(body["count"])
        self.assertIn("measurement_withheld", body)
        save_bytes("hostile-rows.json", (json.dumps({
            "count": body["count"],
            "invalid_rows": body["invalid_rows"],
            "provenance": "author",
        }, indent=2, sort_keys=True) + "\n").encode("utf-8"))
        RESULTS.append({
            "hostile_hardening": True,
            "known_reproduction": False,
            "name": "invalid-rows-do-not-complete-a-measured-total",
            "provenance": "author",
        })

    def test_author_malformed_envelope_types(self) -> None:
        good = supported_envelope()
        report = blank_report()
        self.assertIs(runtime.p2.p1.apply_envelope(report, good, dict(good), dict(good)), True)
        self.assertEqual(report["authority"], "none")
        self.assertIs(report["action_released"], False)
        self.assertNotIn("envelope_withheld", report)
        samples = {
            "accepted": "yes",
            "approved": 1,
            "authority": "Director",
            "closes_work": {"closed": True},
            "releases_action": {"x": 1},
            "task_association": ["task"],
        }
        for key, bad in samples.items():
            payload = dict(good)
            payload[key] = bad
            target = blank_report()
            self.assertIs(runtime.p2.p1.apply_envelope(target, payload, payload, payload), False, key)
            self.assertIsNone(target["authority"], key)
            self.assertIsNone(target[key], key)

    def test_author_each_envelope_field_on_hold_and_mismatch(self) -> None:
        samples = {
            "accepted": "yes",
            "action_released": {"x": 1},
            "approved": 1,
            "authority": "Director",
            "closes_work": {"closed": True},
            "releases_action": {"x": 1},
            "task_association": ["task"],
        }
        for key, bad in samples.items():
            held = blank_report()
            for name, value in supported_envelope().items():
                held[name] = value
            held["action_released"] = False
            held[key] = bad
            runtime.p2.mark_unstable(held, {"journal_current": "a"}, {"journal_current": "b"}, ["journal_current"])
            for name in ENVELOPE:
                self.assertIsNone(held[name], f"{key} {name}")
            self.assertEqual(held["envelope_withheld"]["cause"], "unstable")
            mismatched = blank_report()
            for name, value in supported_envelope().items():
                mismatched[name] = value
            mismatched["action_released"] = False
            mismatched[key] = bad
            runtime.p2.hold_mismatch(mismatched, {"journal_current": "a"}, {"journal_current": "a"})
            for name in ENVELOPE:
                self.assertIsNone(mismatched[name], f"mismatch {key} {name}")
            self.assertEqual(mismatched["observation"]["status"], "mismatch")
            self.assertEqual(mismatched["envelope_withheld"]["cause"], "mismatch")

    def test_author_empty_versus_absent_and_sizes(self) -> None:
        digest = "b" * 64
        empty = runtime.p3.artifacts_of({"findings": [], "form": {"bindings": {"rows": []}}, "measurement": "complete"})
        self.assertEqual(empty["count"], 0)
        self.assertEqual(empty["count_state"], "declared")
        self.assertNotIn("invalid_rows", empty)
        self.assertNotIn("size_observation", empty)
        absent = runtime.p3.artifacts_of({"findings": [], "form": {"bindings": {}}, "measurement": "complete"})
        self.assertIsNone(absent["count"])
        self.assertNotEqual(absent.get("count_state"), "declared")
        null_row = runtime.p3.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": [{"bytes": None, "path": "n.txt", "role": "artifact", "root": "book", "sha256": digest}]}},
            "measurement": "complete",
        })
        missing_row = runtime.p3.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": [{"path": "m.txt", "role": "artifact", "root": "book", "sha256": digest}]}},
            "measurement": "complete",
        })
        self.assertEqual(null_row["size_observation"]["missing"], 1)
        self.assertEqual(missing_row["size_observation"]["missing"], 1)
        self.assertNotIn("do not agree", str(null_row["addressed_sources"].get("reason")))
        self.assertNotIn("do not agree", str(missing_row["addressed_sources"].get("reason")))
        negative = runtime.p3.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": [{"bytes": -3, "path": "n.txt", "role": "artifact", "root": "book", "sha256": digest}]}},
            "measurement": "complete",
        })
        flagged = runtime.p3.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": [{"bytes": True, "path": "n.txt", "role": "artifact", "root": "book", "sha256": digest}]}},
            "measurement": "complete",
        })
        self.assertIsNone(negative["intake_roles"]["bytes"])
        self.assertEqual(negative["size_observation"]["negative"], 1)
        self.assertEqual(negative["intake_roles"]["reason"], "negative or bool size is not a valid measurement")
        self.assertIsNone(flagged["intake_roles"]["bytes"])
        self.assertEqual(flagged["size_observation"]["bool"], 1)
        self.assertNotEqual(flagged["intake_roles"].get("bytes"), 1)
        conflict = runtime.p3.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": [
                {"bytes": 4, "path": "c.txt", "role": "artifact", "root": "book", "sha256": digest},
                {"bytes": 9, "path": "c.txt", "role": "artifact", "root": "book", "sha256": digest},
            ]}},
            "measurement": "complete",
        })
        self.assertIn("do not agree on one int byte size", str(conflict["addressed_sources"].get("reason")))
        self.assertNotIn("size_observation", conflict)

    def test_author_uppercase_and_invalid_digest(self) -> None:
        upper = "C" * 64
        body = runtime.p3.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": [{
                "bytes": 4, "declared_bytes": 4, "declared_sha256": upper, "path": "u.txt",
                "role": "artifact", "root": "book", "sha256": upper,
            }]}},
            "measurement": "complete",
        })
        self.assertEqual(body["rows"][0]["sha256"], upper)
        self.assertEqual(body["hash_match"], 0)
        self.assertEqual(body["not_verified"], 1)
        short = runtime.p3.artifacts_of({
            "findings": [],
            "form": {"bindings": {"rows": [{
                "bytes": 4, "declared_bytes": 4, "declared_sha256": "abcd", "path": "s.txt",
                "role": "artifact", "root": "book", "sha256": "abcd",
            }]}},
            "measurement": "complete",
        })
        self.assertEqual(short["rows"][0]["sha256"], "abcd")
        self.assertEqual(short["hash_match"], 0)
        self.assertEqual(short["not_verified"], 1)

    def test_author_unreadable_cut_is_not_stable(self) -> None:
        report = blank_report()
        runtime.p2.set_observation(report, None, None, "mismatch", True)
        self.assertIsNone(report["observation"]["stable"])
        self.assertEqual(report["observation"]["status"], "unreadable")
        one_sided = blank_report()
        runtime.p2.set_observation(one_sided, None, {"journal_current": "w"}, "mismatch", True)
        self.assertIs(one_sided["observation"]["stable"], False)
        self.assertIn("cut", one_sided["observation"]["changed"])
        book = KEEP / "books" / "unreadable"
        source, pass_id = "0587.hardening-unreadable", "05.87"
        plant(book, source, pass_id)
        publish(book, source, pass_id)
        journal = book / "workbook-review" / source / pass_id / "journal.json"
        journal.unlink()
        journal.mkdir()
        before = tree_digest(book)
        proc = run_app(str(book), source, pass_id)
        self.assertEqual(tree_digest(book), before)
        self.assertNotEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(proc.stdout.startswith(b"{"), proc.stderr)
        body = json.loads(proc.stdout.decode("utf-8"))
        self.assertIsNot(body["observation"]["stable"], True)
        self.assertNotEqual(body.get("authority"), "Director")
        save_pair("fixture-unreadable", proc, proc)
        RESULTS.append({
            "name": "unreadable-cut",
            "observation_stable": body["observation"]["stable"],
            "process_exit": proc.returncode,
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
        copy = folder / "review_report_tools_v3.py"
        shutil.copyfile(ROOT / "app" / "review_report_tools_v3.py", copy)
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
            copied = load("review_report_tools_v3_linked_author", dest / "app" / "review_report_tools_v3.py")
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
