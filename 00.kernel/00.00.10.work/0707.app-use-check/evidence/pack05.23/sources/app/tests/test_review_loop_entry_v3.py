#!/usr/bin/env python3
"""App-boundary checks for the selected review-loop v3 door.

Calls go through app/librarian.py except the labelled declared-pin test,
which calls the door on a disposable code copy. Importing this file does not
write evidence. Executing it writes one new directory under evidence/build05.09/runs.
It does not run the v2 entry test, the 05.08 lab suite, or an old app test main.
A24 stays MANUAL. A planted pin in a disposable copy is not that experiment.
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LIBRARIAN = ROOT / "app" / "librarian.py"
DOOR = ROOT / "app" / "review_loop_tools_v3.py"
DECLARATION = ROOT / "app" / "review-loop-v3.json"
LINES = ROOT / "labs" / "return-lines-pass01" / "return_lines.py"
LIVE_BOOK = ROOT / "00.kernel" / "00.00.10.work"
LIVE_MEMBER = LIVE_BOOK / "0182.desk-app-integration-design-0501"
LIVE_PAGE = LIVE_BOOK / "0519.desk-app" / "05.01.md"
BEFORE = LIVE_BOOK / "0522.review-construction" / "evidence" / "build05.09" / "before"
EVIDENCE = LIVE_BOOK / "0522.review-construction" / "evidence"
LOG: list[dict] = []

ASSIGNMENT = b"Synthetic assignment. Write one piece.\n"
NOTE = b"NOTE\n"
RETURN = "Did.\nThe disposable capture returned one note.\n"
NEXT = "Pack one bounded correction for the disposable capture."
NO_RECORD = "No judgment is recorded. The target is absent, so this entry does not commit one."
OUTSIDE = "OUTSIDE-\u0394-TOKEN"
TAIL = "TAIL-\u0394-TOKEN"
SUBMISSION = "sub-0509"
LOOP_SHA = "47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b"
PASS04_SHA = "6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20"
SECTION_KEYS = [
    "affected", "assumptions", "consequences", "exploration", "findings_account",
    "finish_assessments", "for_model", "issue", "learning", "limits",
    "next_bounded_action", "open_questions", "options", "outcome_evidence",
    "preservation", "prime_finding", "proposed_plan", "question", "recommendation",
    "remaining_choices", "return_result", "tests_note", "tests_passed", "within_direction",
]
OLD = {
    "app/review_loop_tools.py": ("b77617c81e073449147c1171aa09bd3c9d4378ff737704ccceec2e3b0bfcecea", 6417),
    "app/review-loop.json": ("bd3e917fc57ffcc435467cd90e6fa2d13fcf07e8233d1462772cc324365e2aae", 1089),
    "app/review_loop_tools_v2.py": ("e57f7aea3339dad60124f495d974282142902ee078d642230e2315b0c432a408", 11126),
    "app/review-loop-v2.json": ("1a3e12e0b3496a1e14dc07b34efcf0e789b9e38c61c9e6feccb92eac6afb72e3", 1892),
}

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def agreement() -> dict:
    return {
        "director_required": "A design change is not in this grant.",
        "finish_criteria": [{"id": "piece", "text": "The disposable note stays one file."}],
        "goal": "Review one disposable capture.",
        "prime_discretion": "Prime may record a judgment inside that grant.",
        "recorded_decisions": [{
            "id": "D1",
            "source_sha256": sha(b"decision"),
            "text": "The disposable pack was supplied for this lab.",
        }],
        "scope": "The disposable fixture only.",
    }


def goal() -> dict:
    return {
        "goal_id": "g-synth",
        "statement": "Review one disposable capture.",
        "terminal": "open",
        "evidence": [],
    }


def sections() -> dict:
    return {key: None for key in SECTION_KEYS}


def write_json(path: Path, payload: dict) -> None:
    path.write_bytes(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def page_bytes(body: str = "PENDING.\n") -> bytes:
    text = (
        f"Intro {OUTSIDE}\n\n"
        "## Return pointer\n"
        "PENDING.\n\n"
        "## Review - Codex Prime\n"
        f"{body}"
        "## Notes\n"
        f"{TAIL}\n"
    )
    return text.encode("utf-8")


def run(name: str, script: Path, args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [str(PY), "-B", str(script), *args],
        cwd=str(ROOT),
        capture_output=True,
        env=env,
        shell=False,
    )
    LOG.append({
        "name": name,
        "argv": [script.name, *args],
        "exit": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", "replace"),
        "stderr": proc.stderr.decode("utf-8", "replace"),
    })
    return proc


def as_json(proc: subprocess.CompletedProcess) -> dict:
    try:
        body = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError as exc:
        detail = proc.stderr.decode("utf-8", "replace")[:800] + proc.stdout.decode("utf-8", "replace")[:400]
        raise AssertionError(detail) from exc
    if not isinstance(body, dict):
        raise AssertionError("stdout is not an object")
    return body


def authority(body: dict) -> None:
    expected = {
        "accepted": False,
        "authority": "none",
        "custody": "not-established",
        "allocated": False,
        "closes_work": False,
        "releases_action": False,
        "authenticates_actor": False,
    }
    found = {key: body.get(key) for key in expected}
    if found != expected:
        raise AssertionError(json.dumps(found, ensure_ascii=False))


def source_page(path: str, data: bytes) -> dict:
    digest = sha(data)
    return {
        "bind": False,
        "content_bytes": len(data),
        "content_sha256": digest,
        "identity": {"schema": "page-bytes/1"},
        "kind": "page",
        "logical_path": path,
        "prior_content_sha256": None,
        "prior_transport_sha256": None,
        "record": data.decode("utf-8"),
        "transport_bytes": len(data),
        "transport_sha256": digest,
    }


def source_text(path: str, data: bytes) -> dict:
    row = source_page(path, data)
    row["kind"] = "supplied-text"
    row["identity"] = {"schema": "supplied-text/1", "label": "SUPPLIED"}
    return row


def source_capture(path: str, data: bytes, member: str, page_id: str, receipt_sha: str, submission: str) -> dict:
    row = source_page(path, data)
    row["kind"] = "capture"
    row["identity"] = {
        "schema": "return-capture/1",
        "member": member,
        "submission_id": submission,
        "receipt_sha256": receipt_sha,
        "origin": {"book": "00.00.10.work", "page": page_id, "batch": "05.01"},
    }
    return row


def tree_fingerprint(path: Path) -> dict[str, str]:
    found = {}
    if not path.exists():
        return found
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = sorted(name for name in dirnames if not (Path(dirpath) / name).is_symlink())
        for name in sorted(filenames):
            item = Path(dirpath) / name
            if item.is_symlink() or not item.is_file():
                continue
            found[item.relative_to(path).as_posix()] = sha(item.read_bytes())
    return found


def load_door():
    spec = importlib.util.spec_from_file_location("review_loop_tools_v3_under_test", DOOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the v3 door")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def committed_paths(root: Path) -> list[str]:
    found = []
    cycle = root / "cycle"
    if not cycle.exists():
        return found
    for dirpath, dirnames, filenames in os.walk(cycle):
        dirnames[:] = sorted(dirnames)
        for name in sorted(filenames):
            item = Path(dirpath) / name
            found.append(item.relative_to(root).as_posix())
    return found


class Book:
    def __init__(self, page_id: str = "0599.synth-lab", page: bytes | None = None):
        self.root = Path(tempfile.mkdtemp(prefix="rc0509-"))
        self.page_id = page_id
        self.pass_id = "05.01"
        self.submission = SUBMISSION
        self.return_text = RETURN
        space, nn, subject = page_id[0], page_id[2:4], page_id.split(".", 1)[1]
        self.member = f"{space}1{nn}.{subject}"
        self.target = f"{page_id}/{self.pass_id}.md"
        self.kernel = f"00.kernel/00.00.10.work/{page_id}/{self.pass_id}.md"
        self.page = self.root / self.target
        self.page.parent.mkdir(parents=True)
        self.page.write_bytes(page if page is not None else page_bytes())
        (self.root / "assignment.txt").write_bytes(ASSIGNMENT)
        (self.root / "note.md").write_bytes(NOTE)

    def producer(self, name: str, args: list[str], allowed: set[int]) -> subprocess.CompletedProcess:
        proc = run(name, LINES, args)
        if proc.returncode not in allowed:
            raise AssertionError(f"{name} exit {proc.returncode}\n{proc.stdout.decode()[:800]}\n{proc.stderr.decode()[:400]}")
        return proc

    def capture(self, name: str) -> None:
        inputs = self.root / "_inputs"
        inputs.mkdir()
        (inputs / "return.md").write_bytes(self.return_text.encode("utf-8"))
        (inputs / "note.md").write_bytes(NOTE)
        self.producer(f"{name}-init", ["init", "--book", str(self.root), "--name", "00.00.10.work"], {0})
        self.producer(f"{name}-reserve", [
            "reserve", "--book", str(self.root), "--page", self.page_id, "--batch", self.pass_id,
            "--submission", self.submission, "--output", "note.md",
            "--submitter", "grok-1", "--reviewer", "codex-prime", "--release", "prepared",
        ], {1})
        self.producer(f"{name}-capture", [
            "capture", "--book", str(self.root), "--page", self.page_id, "--batch", self.pass_id,
            "--submission", self.submission, "--return-file", str(inputs / "return.md"),
            "--artifact", "note.md", str(inputs / "note.md"),
        ], {0})
        self.save_descriptor(name)

    def save_descriptor(self, name: str) -> None:
        proc = self.producer(f"{name}-descriptor", [
            "descriptor", "--book", str(self.root), "--page", self.page_id, "--batch", self.pass_id,
        ], {0})
        self.descriptor_bytes = proc.stdout
        (self.root / "descriptor.json").write_bytes(proc.stdout)
        self.descriptor = json.loads(proc.stdout.decode("utf-8"))
        self.write_registration()

    def write_registration(self) -> None:
        write_json(self.root / "registration.json", {
            "schema": "prime-cycle-registration/2",
            "book": "00.00.10.work",
            "work_id": "synth-" + self.page_id[:4],
            "source_kind": "N5NN",
            "page_id": self.page_id,
            "pass": self.pass_id,
            "kernel_page": self.kernel,
            "target": self.target,
            "descriptor_path": "descriptor.json",
            "agreement": agreement(),
            "task_id": "synth-task",
            "assignment_path": "assignment.txt",
            "evidence": [{"label": "supplied", "logical_path": "note.md"}],
            "submission_id": self.submission,
            "receipt_label": "supplied",
            "review_identity": "r1",
            "review_location": "cycle",
            "goal": goal(),
            "bounds": {"max_output_bytes": 2097152},
        })
        write_json(self.root / "request.json", {
            "schema": "review-loop-request/1",
            "registration_path": "registration.json",
        })

    def call(self, name: str, command: str, *extra: str) -> tuple[subprocess.CompletedProcess, dict]:
        proc = run(name, LIBRARIAN, [
            "review-loop", command, "--fixture-root", str(self.root), "--request", "request.json", *extra,
        ])
        return proc, as_json(proc)

    def record_body(self) -> dict:
        body = sections()
        body["return_result"] = "The builder returned the disposable note."
        body["prime_finding"] = "The disposable note is present."
        body["within_direction"] = "This stays inside the supplied grant."
        body["next_bounded_action"] = "Hand back one correction pack."
        return_bytes = (self.root / self.descriptor["return_path"]).read_bytes()
        receipt_sha = sha((self.root / self.descriptor["receipt_path"]).read_bytes())
        return {
            "schema": "prime-review-record/1",
            "attribution": {
                "actor_label": "Codex Prime (SUPPLIED)",
                "role": "prime",
                "evidence": "SUPPLIED demonstration judgment. The label is not authentication.",
            },
            "sources": [
                source_page("assignment.txt", (self.root / "assignment.txt").read_bytes()),
                source_text("note.md", (self.root / "note.md").read_bytes()),
                source_capture(
                    self.descriptor["return_path"], return_bytes, self.member,
                    self.page_id, receipt_sha, self.submission,
                ),
            ],
            "agreement": agreement(),
            "holds": [],
            "answers": [],
            "review_passes": [],
            "gaps": [],
            "judgment": {
                "outcome": "continue",
                "finding": "The disposable note is present.",
                "reasons": ["The captured return names the note."],
                "semantic_conflict": False,
                "design_fork": None,
                "next_action": NEXT,
                "sections": body,
            },
        }

    def judgment_for(self, record: dict) -> dict:
        supplied = record["judgment"]
        return {
            "outcome": supplied["outcome"],
            "disposition": "held",
            "pass_terminal": "open",
            "goal": {
                "terminal": "open",
                "goal_id": "g-synth",
                "goal_sha256": sha(goal()["statement"].encode("utf-8")),
                "evidence": [],
            },
            "finding": supplied["finding"],
            "reasons": supplied["reasons"],
            "source_refs": ["assignment.txt"],
            "next_action": {
                "action_id": "pack-correction",
                "text": supplied["next_action"],
                "authorized_in_grant": False,
            },
            "unresolved": [],
            "semantic_conflict": supplied["semantic_conflict"],
            "design_fork": supplied["design_fork"],
            "holds": record["holds"],
            "answers": record["answers"],
            "sections": supplied["sections"],
        }

    def decide(self, name: str) -> dict:
        proc, view = self.call(f"{name}-prepare", "prepare")
        if proc.returncode != 0 or not isinstance(view.get("view", {}).get("template"), dict):
            raise AssertionError(proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        decision = deepcopy(view["view"]["template"])
        record = self.record_body()
        decision["attribution"] = record["attribution"]
        decision["judgment"] = self.judgment_for(record)
        decision["supplied_record"] = record
        write_json(self.root / "decision.json", decision)
        self.prepared = view
        return decision

    def review_dir(self) -> Path:
        return self.root / "cycle" / "05.01-r1"

    def close(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


class ReviewLoopEntryV3Tests(unittest.TestCase):
    def test_selection_preserves_old_doors(self) -> None:
        for rel, (digest, size) in OLD.items():
            data = (ROOT / rel).read_bytes()
            self.assertEqual(len(data), size, rel)
            self.assertEqual(sha(data), digest, rel)
            self.assertEqual((BEFORE / Path(rel).name).read_bytes(), data, rel)
        before_librarian = (BEFORE / "librarian.py").read_text(encoding="utf-8")
        after_librarian = LIBRARIAN.read_text(encoding="utf-8")
        self.assertEqual(
            before_librarian.replace(
                "review_loop_tools_v2.py", "review_loop_tools_v3.py",
            ).replace(
                "librarian_review_loop_tools_v2", "librarian_review_loop_tools_v3",
            ),
            after_librarian,
        )
        self.assertNotIn("review_loop_tools_v2", after_librarian)
        before_readme = (BEFORE / "README.md").read_text(encoding="utf-8")
        after_readme = (ROOT / "app" / "README.md").read_text(encoding="utf-8")
        marker = "`review-loop` calls the reviewed loop"
        self.assertEqual(before_readme.split(marker, 1)[0], after_readme.split(marker, 1)[0])
        self.assertIn("review-loop-v3.json", after_readme)
        self.assertIn(LOOP_SHA, after_readme)
        self.assertIn("construct_pass04", after_readme)
        self.assertIn("construct_pass02", after_readme)
        door = load_door()
        document = json.loads(DECLARATION.read_text(encoding="utf-8"))
        self.assertEqual(document["schema"], "review-loop-pins/2")
        self.assertEqual(document["version"], 1)
        self.assertEqual(set(document["tools"]), set(door.TOOLS))
        for name, expected in door.TOOLS.items():
            item = document["tools"][name]
            self.assertEqual(item["path"], expected["path"], name)
            self.assertEqual(item["sha256"], expected["sha256"], name)
            self.assertEqual(item["bytes"], expected["bytes"], name)
            live = (ROOT / expected["path"]).read_bytes()
            self.assertEqual(len(live), expected["bytes"], name)
            self.assertEqual(sha(live), expected["sha256"], name)
        self.assertEqual(door.TOOLS["review_loop"]["sha256"], LOOP_SHA)
        self.assertEqual(door.TOOLS["construct_pass04"]["sha256"], PASS04_SHA)
        self.assertNotIn("colab_workflow.py", json.dumps(document))

    def test_where_and_validate_stay_read_only(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="rc0509-ctx-"))
        live_before = sha(LIVE_PAGE.read_bytes())
        try:
            for command in ("where", "validate"):
                missing = run(f"{command}-missing", LIBRARIAN, [command])
                self.assertEqual(missing.returncode, 2)
                self.assertEqual(missing.stdout, b"")
                self.assertIn(f"stop: missing --root", missing.stderr.decode())
                self.assertNotIn("review-loop", missing.stderr.decode())
                present = run(f"{command}-empty", LIBRARIAN, [command, "--root", str(outside)])
                self.assertEqual(present.returncode, 2)
                err = present.stderr.decode()
                self.assertIn("stop: missing config", err)
                self.assertNotIn("review_loop", err)
                self.assertEqual(present.stdout, b"")
            self.assertEqual(tree_fingerprint(outside), {})
            self.assertEqual(sha(LIVE_PAGE.read_bytes()), live_before)
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    def test_wrapper_refusals_do_not_launch(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="rc0509-arg-"))
        try:
            cases = [
                (["review-loop", "reproduce"], "reproduce is a lab command and is not an app command"),
                (["review-loop", "run"], "run is not a review-loop command"),
                (["review-loop", "prepare", "--fixture-root", str(ROOT / "app"), "--request", "request.json"], "fixture root must stay outside"),
                (["review-loop", "prepare", "--fixture-root", str(outside), "--request", "request.json", "--executable", "python"], "caller tool override is refused"),
            ]
            for args, text in cases:
                with self.subTest(args=args[:2]):
                    proc = run("wrap", LIBRARIAN, args)
                    self.assertEqual(proc.returncode, 2)
                    err = proc.stderr.decode()
                    self.assertIn("stop:", err)
                    self.assertIn(text, err)
                    self.assertNotIn("refused:", err)
                    self.assertEqual(proc.stdout, b"")
            self.assertFalse((outside / "trace").exists())
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    def test_declared_pin_mismatch_on_a_disposable_copy(self) -> None:
        """Declared-pin mismatch. This is not the A24 altered-file experiment."""
        door = load_door()
        real = json.loads(DECLARATION.read_text(encoding="utf-8"))
        outside = Path(tempfile.mkdtemp(prefix="rc0509-pinfix-"))
        code = Path(tempfile.mkdtemp(prefix="rc0509-pincode-"))
        live_pass04 = sha((ROOT / "labs" / "review-construction-pass04" / "construct.py").read_bytes())
        try:
            app = code / "app"
            app.mkdir()
            mismatched = deepcopy(real)
            mismatched["tools"]["review_loop"]["sha256"] = "0" * 64
            write_json(app / "review-loop-v3.json", mismatched)
            with self.assertRaises(door.Refuse) as caught:
                door.perform(["prepare", "--fixture-root", str(outside), "--request", "request.json"], code)
            self.assertIn("review loop declaration does not match the pinned tools", str(caught.exception))

            write_json(app / "review-loop-v3.json", real)
            loop_dir = code / "labs" / "review-loop-pass03"
            loop_dir.mkdir(parents=True)
            (loop_dir / "review_loop.py").write_bytes(b"not the reviewed loop\n")
            with self.assertRaises(door.Refuse) as caught:
                door.perform(["prepare", "--fixture-root", str(outside), "--request", "request.json"], code)
            self.assertIn("pinned tool hash does not match: review_loop", str(caught.exception))

            (loop_dir / "review_loop.py").write_bytes((ROOT / "labs" / "review-loop-pass03" / "review_loop.py").read_bytes())
            construct_dir = code / "labs" / "review-construction-pass04"
            construct_dir.mkdir(parents=True)
            (construct_dir / "construct.py").write_bytes(b"not pass04\n")
            with self.assertRaises(door.Refuse) as caught:
                door.perform(["prepare", "--fixture-root", str(outside), "--request", "request.json"], code)
            self.assertIn("pinned tool hash does not match: construct_pass04", str(caught.exception))
            self.assertFalse((outside / "trace").exists())
            self.assertFalse((code / "labs" / "prime-cycle-pass03").exists())
            self.assertEqual(
                sha((ROOT / "labs" / "review-construction-pass04" / "construct.py").read_bytes()),
                live_pass04,
            )
            self.assertEqual(live_pass04, PASS04_SHA)
        finally:
            shutil.rmtree(outside, ignore_errors=True)
            shutil.rmtree(code, ignore_errors=True)

    def test_a24_relocated_altered_construct_stays_manual(self) -> None:
        self.assertEqual(sha((ROOT / "labs" / "review-construction-pass04" / "construct.py").read_bytes()), PASS04_SHA)

    def test_linked_declaration_is_not_followed(self) -> None:
        door = load_door()
        code = Path(tempfile.mkdtemp(prefix="rc0509-link-"))
        outside = Path(tempfile.mkdtemp(prefix="rc0509-linkfix-"))
        try:
            app = code / "app"
            app.mkdir()
            real = app / "real.json"
            real.write_bytes(DECLARATION.read_bytes())
            link = app / "review-loop-v3.json"
            try:
                os.symlink(real, link)
            except OSError as exc:
                winerror = getattr(exc, "winerror", None)
                if winerror == 1314 or exc.errno in {1, 13}:
                    self.skipTest(f"symlink privilege unavailable: {exc}")
                raise
            with self.assertRaises(door.Refuse) as caught:
                door.perform(["prepare", "--fixture-root", str(outside), "--request", "request.json"], code)
            self.assertIn("tool path is linked and was not followed", str(caught.exception))
            self.assertFalse((outside / "trace").exists())
        finally:
            shutil.rmtree(code, ignore_errors=True)
            shutil.rmtree(outside, ignore_errors=True)

    def test_describe_legacy_on_a_copied_book_writes_nothing(self) -> None:
        before_member = tree_fingerprint(LIVE_MEMBER)
        before_page = sha(LIVE_PAGE.read_bytes())
        book = Path(tempfile.mkdtemp(prefix="rc0509-legacy-"))
        try:
            shutil.copytree(LIVE_MEMBER, book / LIVE_MEMBER.name)
            before_copy = tree_fingerprint(book)
            proc = run("legacy", LIBRARIAN, [
                "review-loop", "describe-legacy", "--book", str(book), "--member", LIVE_MEMBER.name,
            ])
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800])
            described = as_json(proc)
            self.assertEqual(tree_fingerprint(book), before_copy)
            self.assertEqual(tree_fingerprint(LIVE_MEMBER), before_member)
            self.assertEqual(sha(LIVE_PAGE.read_bytes()), before_page)
            self.assertEqual(described["schema"], "review-loop-legacy-description/1")
            self.assertFalse(described["accepted"])
            self.assertEqual(described["custody"], "not-established")
            self.assertFalse(described["full_success"])
        finally:
            shutil.rmtree(book, ignore_errors=True)

    def test_prepare_record_render_then_separate_process_read(self) -> None:
        book = Book()
        try:
            book.capture("round")
            prepared_proc, prepared = book.call("round-prepare", "prepare")
            self.assertEqual(prepared_proc.returncode, 0, prepared_proc.stderr.decode()[:800])
            self.assertEqual(prepared["schema"], "review-loop-result/2")
            self.assertFalse(prepared["full_success"])
            self.assertEqual(prepared["target"]["state"], "pending")
            self.assertEqual(prepared["mechanical"]["state"], "awaiting-review")
            self.assertEqual(prepared["mechanical"]["route"], "record")
            self.assertEqual(prepared["mechanical"]["text"], "Supply the typed judgment, then record.")
            self.assertIsInstance(prepared["view"]["template"], dict)
            authority(prepared)
            self.assertEqual(prepared["pins"]["review_loop"]["path"], "labs/review-loop-pass03/review_loop.py")
            self.assertEqual(prepared["pins"]["construct"]["path"], "labs/review-construction-pass04/construct.py")
            self.assertEqual(prepared["pins"]["construct"]["sha256"], PASS04_SHA)
            decision = book.decide("round")
            self.assertEqual(decision["judgment"]["disposition"], "held")
            recorded, record_view = book.call("round-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode()[:800])
            self.assertEqual(record_view["record"]["result"], "recorded")
            authority(record_view)
            rendered, render_view = book.call("round-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:800] + rendered.stdout.decode()[:400])
            self.assertTrue(render_view["full_success"])
            authority(render_view)
            text = book.page.read_text(encoding="utf-8")
            self.assertIn(OUTSIDE, text)
            self.assertIn(TAIL, text)
            self.assertIn(NEXT, text)
            self.assertIn(decision["binding"]["task_binding_sha256"], text)
            fresh, fresh_view = book.call("round-read", "read")
            self.assertEqual(fresh.returncode, 0, fresh.stderr.decode()[:800])
            self.assertEqual(fresh_view["pass_state"], "reviewed")
            self.assertEqual(fresh_view["mechanical"]["state"], "rendered")
            self.assertEqual(fresh_view["mechanical"]["text"], "Read the rendered review.")
            self.assertEqual(fresh_view["next"], fresh_view["mechanical"]["text"])
            self.assertEqual(fresh_view["current"]["next_action_label"], "supplied")
            self.assertEqual(fresh_view["supplied_next_action"]["text"], NEXT)
            self.assertNotEqual(fresh_view["next"], fresh_view["supplied_next_action"]["text"])
            authority(fresh_view)
            self.assertEqual((book.root / "descriptor.json").read_bytes(), book.descriptor_bytes)
        finally:
            book.close()

    def test_blocked_render_preserves_the_committed_judgment(self) -> None:
        live_before = sha(LIVE_PAGE.read_bytes())
        book = Book(page=LIVE_PAGE.read_bytes())
        try:
            book.capture("block")
            before = book.page.read_bytes()
            prepared_proc, prepared = book.call("block-prepare", "prepare")
            self.assertEqual(prepared_proc.returncode, 0, prepared_proc.stderr.decode()[:500])
            self.assertEqual(prepared["target"]["state"], "existing-review")
            self.assertEqual(prepared["mechanical"]["route"], "record-then-blocked")
            book.decide("block")
            recorded, record_view = book.call("block-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode()[:800])
            self.assertEqual(record_view["record"]["result"], "recorded")
            rendered_proc, rendered = book.call("block-render", "render")
            self.assertEqual(rendered_proc.returncode, 2)
            self.assertEqual(rendered["render"]["result"], "render-conflict")
            self.assertNotIn("refused:", rendered_proc.stderr.decode())
            self.assertEqual(book.page.read_bytes(), before)
            partials = list((book.root / "partial").glob("*.md"))
            self.assertEqual(len(partials), 1)
            recover_proc, recover = book.call("block-recover", "recover")
            self.assertEqual(recover_proc.returncode, 2)
            self.assertEqual(recover["render"]["result"], "render-conflict")
            self.assertEqual(len(list((book.root / "partial").glob("*.md"))), 1)
            self.assertEqual(book.page.read_bytes(), before)
            read_proc, read_body = book.call("block-read", "read")
            self.assertEqual(read_proc.returncode, 0, read_proc.stderr.decode()[:500])
            self.assertEqual(read_body["mechanical"]["state"], "existing-review-conflict")
            self.assertIn("retained", read_body["mechanical"]["text"])
            stored = json.loads((book.review_dir() / "record.json").read_bytes())
            self.assertEqual(stored["decision"]["judgment"]["disposition"], "held")
            authority(read_body)
            self.assertEqual(sha(LIVE_PAGE.read_bytes()), live_before)
        finally:
            book.close()

    def test_stale_target_refuses_and_keeps_the_record(self) -> None:
        book = Book()
        try:
            book.capture("stale")
            book.decide("stale")
            recorded, _view = book.call("stale-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode()[:800])
            record_bytes = (book.review_dir() / "record.json").read_bytes()
            original = book.page.read_bytes()
            changed = original.replace(OUTSIDE.encode(), "OUTSIDE-\u0394-TOKEX".encode())
            self.assertNotEqual(changed, original)
            book.page.write_bytes(changed)
            proc, body = book.call("stale-render", "render")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("write token changed since read", body.get("rule", "") + proc.stderr.decode())
            self.assertEqual(book.page.read_bytes(), changed)
            self.assertEqual((book.review_dir() / "record.json").read_bytes(), record_bytes)
            read_proc, read_body = book.call("stale-read", "read")
            self.assertEqual(read_proc.returncode, 0, read_proc.stderr.decode()[:600])
            self.assertEqual(read_body["mechanical"]["state"], "target-changed-since-record")
            self.assertIn("retained", read_body["mechanical"]["text"])
            self.assertNotIn(NEXT, read_body["mechanical"]["text"])
            self.assertEqual(read_body["supplied_next_action"]["text"], NEXT)
            self.assertEqual(read_body["next"], read_body["mechanical"]["text"])
            self.assertEqual((book.review_dir() / "record.json").read_bytes(), record_bytes)
        finally:
            book.close()

    def test_read_and_recover_are_idempotent_after_render(self) -> None:
        book = Book()
        try:
            book.capture("again")
            book.decide("again")
            self.assertEqual(book.call("again-record", "record", "--decision", "decision.json")[0].returncode, 0)
            rendered, _render_view = book.call("again-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:800])
            page_hash = sha(book.page.read_bytes())
            first_proc, first = book.call("again-read", "read")
            self.assertEqual(first_proc.returncode, 0)
            recover_proc, recover = book.call("again-recover", "recover")
            self.assertEqual(recover_proc.returncode, 0, recover_proc.stderr.decode()[:800])
            self.assertEqual(recover["render"]["result"], "already-rendered")
            self.assertFalse(recover["render"]["apply_called"])
            authority(recover)
            self.assertEqual(sha(book.page.read_bytes()), page_hash)
            second_proc, second = book.call("again-read-2", "read")
            self.assertEqual(second_proc.returncode, 0)
            self.assertEqual(second["mechanical"]["text"], first["mechanical"]["text"])
            self.assertEqual(second["next"], first["next"])
            self.assertEqual(second["supplied_next_action"]["text"], first["supplied_next_action"]["text"])
            self.assertEqual(second["next"], "Read the rendered review.")
            self.assertEqual(second["supplied_next_action"]["text"], NEXT)
            self.assertNotEqual(second["next"], second["supplied_next_action"]["text"])
            self.assertEqual(sha(book.page.read_bytes()), page_hash)
        finally:
            book.close()

    def test_a22a_absent_before_prepare(self) -> None:
        book = Book()
        try:
            book.capture("a22a")
            book.page.unlink()
            self.assertFalse(book.page.exists())
            self.assertFalse((book.root / "decision.json").exists())
            proc, body = book.call("a22a-prepare", "prepare")
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800])
            self.assertEqual(body["schema"], "review-loop-result/2")
            self.assertEqual(body["target"]["state"], "absent")
            self.assertIsNone(body["view"]["template"])
            self.assertEqual(body["mechanical"]["state"], "awaiting-review")
            self.assertEqual(body["mechanical"]["blocker"], "target-absent")
            self.assertEqual(body["mechanical"]["route"], "none-in-this-entry")
            self.assertEqual(body["mechanical"]["text"], NO_RECORD)
            self.assertNotIn("kept", body["mechanical"]["text"].lower())
            authority(body)
            self.assertFalse(book.page.exists())
            self.assertEqual(committed_paths(book.root), [])
            read_proc, read_body = book.call("a22a-read", "read")
            self.assertEqual(read_proc.returncode, 0, read_proc.stderr.decode()[:800])
            self.assertEqual(read_body["mechanical"]["text"], NO_RECORD)
            self.assertEqual(read_body["mechanical"]["route"], "none-in-this-entry")
            self.assertNotIn(read_body["mechanical"]["route"], {"record", "recover"})
            self.assertFalse(book.page.exists())
            self.assertEqual(committed_paths(book.root), [])
        finally:
            book.close()

    def test_a22b_removed_before_record(self) -> None:
        book = Book()
        try:
            book.capture("a22b")
            prepared_proc, prepared = book.call("a22b-prepare", "prepare")
            self.assertEqual(prepared_proc.returncode, 0, prepared_proc.stderr.decode()[:800])
            self.assertIsInstance(prepared["view"]["template"], dict)
            book.decide("a22b")
            decision_hash = sha((book.root / "decision.json").read_bytes())
            book.page.unlink()
            proc, body = book.call("a22b-record", "record", "--decision", "decision.json")
            self.assertEqual(proc.returncode, 2)
            err = proc.stderr.decode()
            self.assertIn("refused: target-absent: target file is absent; the cycle did not commit this decision", err)
            self.assertEqual(body["schema"], "review-loop-refusal/1")
            self.assertEqual(sha((book.root / "decision.json").read_bytes()), decision_hash)
            self.assertEqual(committed_paths(book.root), [])
            self.assertFalse((book.root / "partial").exists())
            read_proc, read_body = book.call("a22b-read", "read")
            self.assertEqual(read_proc.returncode, 0, read_proc.stderr.decode()[:800])
            self.assertEqual(read_body["mechanical"]["text"], NO_RECORD)
            self.assertEqual(read_body["mechanical"]["route"], "none-in-this-entry")
            self.assertNotIn(read_body["mechanical"]["route"], {"record", "recover"})
            self.assertEqual(sha((book.root / "decision.json").read_bytes()), decision_hash)
            self.assertEqual(committed_paths(book.root), [])
        finally:
            book.close()


if __name__ == "__main__":
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    token = os.urandom(4).hex()
    run_dir = EVIDENCE / "build05.09" / "runs" / f"{stamp}-{token}"
    run_dir.mkdir(parents=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReviewLoopEntryV3Tests)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (run_dir / "suite.txt").write_bytes(stream.getvalue().encode("utf-8"))
    (run_dir / "calls.jsonl").write_bytes(b"".join(
        json.dumps(row, ensure_ascii=False).encode("utf-8") + b"\n" for row in LOG
    ))
    skipped = [f"{item[0]}: {item[1]}" for item in result.skipped] if hasattr(result, "skipped") else []
    (run_dir / "skips.txt").write_bytes(("\n".join(skipped) + ("\n" if skipped else "")).encode("utf-8"))
    summary = {
        "tests": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "exit": 0 if result.wasSuccessful() else 1,
    }
    (run_dir / "summary.json").write_bytes((json.dumps(summary, indent=2) + "\n").encode("utf-8"))
    print(run_dir)
    raise SystemExit(summary["exit"])
