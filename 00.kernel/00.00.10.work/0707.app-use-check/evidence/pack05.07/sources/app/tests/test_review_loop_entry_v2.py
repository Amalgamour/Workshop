#!/usr/bin/env python3
"""Focused app-entry checks for the reviewed review loop.

Calls go through app/librarian.py. Importing this file does not write evidence.
Executing it writes evidence/build05.05/suite.log and commands.json. It does not
run test_construct.py, test_entry.py, the pass02 __main__ writer, or AR-01.
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
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LIBRARIAN = ROOT / "app" / "librarian.py"
DOOR = ROOT / "app" / "review_loop_tools_v2.py"
LINES = ROOT / "labs" / "return-lines-pass01" / "return_lines.py"
LIVE_BOOK = ROOT / "00.kernel" / "00.00.10.work"
LIVE_MEMBER = LIVE_BOOK / "0182.desk-app-integration-design-0501"
LIVE_PAGE = LIVE_BOOK / "0519.desk-app" / "05.01.md"
LAYOUT = LIVE_BOOK / "return-line-layout.json"
EVIDENCE = LIVE_BOOK / "0522.review-construction" / "evidence"
LOG: list[dict] = []

ASSIGNMENT = b"Synthetic assignment. Write one piece.\n"
NOTE = b"NOTE\n"
RETURN = "Did.\nThe disposable capture returned one note.\n"
NEXT = "Pack one bounded correction for the disposable capture."
OUTSIDE = "OUTSIDE-\u0394-TOKEN"
TAIL = "TAIL-\u0394-TOKEN"
SUBMISSION = "sub-0505"
SECTION_KEYS = [
    "affected", "assumptions", "consequences", "exploration", "findings_account",
    "finish_assessments", "for_model", "issue", "learning", "limits",
    "next_bounded_action", "open_questions", "options", "outcome_evidence",
    "preservation", "prime_finding", "proposed_plan", "question", "recommendation",
    "remaining_choices", "return_result", "tests_note", "tests_passed", "within_direction",
]
PINS = {
    "labs/review-loop-pass02/review_loop.py": ("8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7", 47189),
    "labs/prime-cycle-pass03/prime_cycle.py": ("496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c", 76045),
    "labs/review-construction-pass02/construct.py": ("b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc", 36188),
    "labs/prime-review-pass02/prime_review.py": ("80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e", 58560),
    "labs/prime-review-pass01/prime_review.py": ("805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0", 58324),
    "labs/return-lines-pass01/return_lines.py": ("863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a", 100897),
    "labs/return-placement-pass01/return_placement.py": ("db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754", 66097),
    "labs/return-capture-pass01/return_inspect.py": ("947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b", 11402),
    "app/review_loop_tools.py": ("b77617c81e073449147c1171aa09bd3c9d4378ff737704ccceec2e3b0bfcecea", 6417),
    "app/review-loop.json": ("bd3e917fc57ffcc435467cd90e6fa2d13fcf07e8233d1462772cc324365e2aae", 1089),
}
RECEIPT_SHA = "f4fd548fb83e33c9d0b21ed997089c4b9c7b9f628c1177432b6a9aeff3713401"
RETURN_SHA = "73e928719064c6d2e6a8b0761d9769c9a147c92f8d2ca9abcbfd952fc10f5464"

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
        "script": script.name,
        "args": args[:2],
        "exit": proc.returncode,
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
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = sorted(name for name in dirnames if not (Path(dirpath) / name).is_symlink())
        for name in sorted(filenames):
            item = Path(dirpath) / name
            if item.is_symlink() or not item.is_file():
                continue
            found[item.relative_to(path).as_posix()] = sha(item.read_bytes())
    return found


def load_door():
    spec = importlib.util.spec_from_file_location("review_loop_tools_v2_under_test", DOOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the v2 door")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Book:
    def __init__(self, page_id: str = "0599.synth-lab", kind: str = "N5NN", body: str = "PENDING.\n", submission: str = SUBMISSION):
        self.root = Path(tempfile.mkdtemp(prefix="rc0505-"))
        self.page_id = page_id
        self.kind = kind
        self.pass_id = "05.01"
        self.submission = submission
        self.return_text = RETURN
        if kind == "N5NN":
            space, nn, subject = page_id[0], page_id[2:4], page_id.split(".", 1)[1]
            self.member = f"{space}1{nn}.{subject}"
            self.target = f"{page_id}/{self.pass_id}.md"
            self.kernel = f"00.kernel/00.00.10.work/{page_id}/{self.pass_id}.md"
        else:
            self.member = None
            self.target = f"{page_id}/06.01.review.md"
            self.kernel = f"00.kernel/00.00.10.work/{page_id}/{self.pass_id}.pack.md"
        self.page = self.root / self.target
        self.page.parent.mkdir(parents=True)
        self.page.write_bytes(page_bytes(body))
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
            "source_kind": self.kind,
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
        sources = [
            source_page("assignment.txt", (self.root / "assignment.txt").read_bytes()),
            source_text("note.md", (self.root / "note.md").read_bytes()),
        ]
        if self.kind == "N5NN":
            sources.append(source_capture(
                self.descriptor["return_path"], return_bytes, self.member, self.page_id, receipt_sha, self.submission,
            ))
        else:
            sources.append(source_text(self.descriptor["return_path"], return_bytes))
        return {
            "schema": "prime-review-record/1",
            "attribution": {
                "actor_label": "Codex Prime (SUPPLIED)",
                "role": "prime",
                "evidence": "SUPPLIED demonstration judgment. The label is not authentication.",
            },
            "sources": sources,
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
            "disposition": "accepted",
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
            "next_action": {"action_id": "pack-correction", "text": supplied["next_action"], "authorized_in_grant": False},
            "unresolved": [],
            "semantic_conflict": supplied["semantic_conflict"],
            "design_fork": supplied["design_fork"],
            "holds": record["holds"],
            "answers": record["answers"],
            "sections": supplied["sections"],
        }

    def decide(self, name: str) -> dict:
        proc, view = self.call(f"{name}-prepare", "prepare")
        if proc.returncode != 0 or view.get("view", {}).get("template") is None:
            raise AssertionError(proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        decision = deepcopy(view["view"]["template"])
        record = self.record_body()
        decision["attribution"] = record["attribution"]
        decision["judgment"] = self.judgment_for(record)
        decision["supplied_record"] = record
        write_json(self.root / "decision.json", decision)
        self.prepared = view
        return decision

    def copy(self) -> Path:
        dest = Path(tempfile.mkdtemp(prefix="rc0505-copy-"))
        shutil.rmtree(dest)
        return Path(shutil.copytree(self.root, dest))

    def close(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


class ReviewLoopEntryTests(unittest.TestCase):
    def test_core_pins_and_old_facade_stay(self) -> None:
        for rel, (digest, size) in PINS.items():
            data = (ROOT / rel).read_bytes()
            self.assertEqual(len(data), size, rel)
            self.assertEqual(sha(data), digest, rel)
        librarian = (ROOT / "app" / "librarian.py").read_bytes()
        self.assertIn(b"review-loop", librarian)
        self.assertNotEqual(sha(librarian), "939484f152c9227482e857f9ce88eaf40649f433a57d6c9d213a07bde16baee5")
        self.assertFalse(os.path.lexists(LAYOUT))

    def test_bad_arguments_refuse_before_the_loop(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="rc0505-arg-"))
        try:
            cases = [
                (["review-loop"], "unknown review-loop command"),
                (["review-loop", "reproduce"], "reproduce is a lab command and is not an app command"),
                (["review-loop", "run"], "run is not a review-loop command"),
                (["review-loop", "capture"], "caller tool override is refused"),
                (["review-loop", "nope"], "unknown review-loop command"),
                (["review-loop", "prepare", "--fixture-root", str(outside), "--request", "request.json", "--tool", "x"], "caller tool override is refused"),
                (["review-loop", "prepare", "--fixture-root", str(outside), "--request", "request.json", "--dest", "x"], "caller tool override is refused"),
                (["review-loop", "prepare", "--fixture-root", str(outside), "--request", "request.json", "--destination", "x"], "caller tool override is refused"),
                (["review-loop", "prepare", "--fixture-root", str(outside), "--request", "request.json", "--capture", "x"], "caller tool override is refused"),
                (["review-loop", "prepare", "--fixture-root", str(outside), "--request", "request.json", "--reserve", "x"], "caller tool override is refused"),
                (["review-loop", "prepare", "--request", "request.json"], "missing --fixture-root"),
                (["review-loop", "prepare", "--fixture-root", str(outside), "--request", "request.json", "--request", "other.json"], "repeated --request"),
                (["review-loop", "prepare", "--fixture-root", str(outside), "--request", "--request"], "missing value for --request"),
                (["review-loop", "prepare", "--fixture-root", str(outside), "--request", "request.json", "--json"], "unknown argument"),
                (["review-loop", "prepare", "--fixture-root", str(ROOT / "app"), "--request", "request.json"], "fixture root must stay outside D:\\Git\\lib-build"),
                (["review-loop", "prepare", "--fixture-root", str(LIVE_BOOK), "--request", "request.json"], "fixture root must stay outside D:\\Git\\lib-build"),
                (["review-loop", "prepare", "--fixture-root", str(outside / "missing"), "--request", "request.json"], "fixture root is not a directory"),
                (["review-loop", "prepare", "--fixture-root", str(outside / "down" / ".." / "down"), "--request", "request.json"], "unsafe path fixture root"),
                (["review-loop", "prepare", "--fixture-root", "\\\\server\\share", "--request", "request.json"], "UNC path fixture root"),
                (["review-loop", "describe-legacy", "--book", str(LIVE_BOOK), "--member", "a/b"], "unsafe path member"),
            ]
            for args, text in cases:
                with self.subTest(args=args):
                    proc = run("arg", LIBRARIAN, args)
                    self.assertEqual(proc.returncode, 2, proc.stderr.decode()[:400])
                    err = proc.stderr.decode("utf-8", "replace")
                    self.assertIn("stop:", err)
                    self.assertIn(text, err)
                    self.assertNotIn("refused:", err)
                    self.assertEqual(proc.stdout, b"")
            self.assertFalse((outside / "trace").exists())
            self.assertFalse(os.path.lexists(LAYOUT))
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    def test_unrelated_commands_keep_their_dispatch(self) -> None:
        bare = run("bare", LIBRARIAN, [])
        self.assertEqual(bare.returncode, 2)
        self.assertIn("stop: normal run is not activated", bare.stderr.decode())
        top = run("top-run", LIBRARIAN, ["run"])
        self.assertEqual(top.returncode, 2)
        self.assertIn("stop: normal run is not activated", top.stderr.decode())
        where = run("where", LIBRARIAN, ["where"])
        self.assertEqual(where.returncode, 2)
        self.assertIn("stop: missing --root", where.stderr.decode())
        prime = run("prime", LIBRARIAN, ["prime-review"])
        self.assertEqual(prime.returncode, 2)
        err = prime.stderr.decode()
        self.assertIn("stop: missing --input", err)
        self.assertNotIn("normal run is not activated", err)

    def test_pin_conflicts_refuse_before_launch(self) -> None:
        door = load_door()
        real = json.loads((ROOT / "app" / "review-loop-v2.json").read_text(encoding="utf-8"))
        outside = Path(tempfile.mkdtemp(prefix="rc0505-pinfix-"))
        code = Path(tempfile.mkdtemp(prefix="rc0505-pincode-"))
        try:
            app = code / "app"
            app.mkdir()
            mismatched = deepcopy(real)
            mismatched["tools"]["review_loop"]["sha256"] = "0" * 64
            write_json(app / "review-loop-v2.json", mismatched)
            with self.assertRaises(door.Refuse) as caught:
                door.perform(["prepare", "--fixture-root", str(outside), "--request", "request.json"], code)
            self.assertIn("review loop declaration does not match the pinned tools", str(caught.exception))

            wrong_path = deepcopy(real)
            wrong_path["tools"]["review_loop"]["path"] = "labs/review-loop-pass02/other.py"
            write_json(app / "review-loop-v2.json", wrong_path)
            with self.assertRaises(door.Refuse) as caught:
                door.perform(["prepare", "--fixture-root", str(outside), "--request", "request.json"], code)
            self.assertIn("review loop declaration does not match the pinned tools", str(caught.exception))

            wrong_schema = deepcopy(real)
            wrong_schema["schema"] = "review-loop-pins/1"
            write_json(app / "review-loop-v2.json", wrong_schema)
            with self.assertRaises(door.Refuse) as caught:
                door.perform(["prepare", "--fixture-root", str(outside), "--request", "request.json"], code)
            self.assertIn("review loop declaration schema is not review-loop-pins/2", str(caught.exception))

            write_json(app / "review-loop-v2.json", real)
            planted = code / "labs" / "review-loop-pass02"
            planted.mkdir(parents=True)
            (planted / "review_loop.py").write_bytes(b"not the reviewed loop\n")
            with self.assertRaises(door.Refuse) as caught:
                door.perform(["prepare", "--fixture-root", str(outside), "--request", "request.json"], code)
            self.assertIn("pinned tool hash does not match: review_loop", str(caught.exception))
            self.assertFalse((outside / "trace").exists())
            self.assertFalse((code / "labs" / "prime-cycle-pass03").exists())
        finally:
            shutil.rmtree(outside, ignore_errors=True)
            shutil.rmtree(code, ignore_errors=True)

    def test_linked_declaration_is_not_followed(self) -> None:
        door = load_door()
        code = Path(tempfile.mkdtemp(prefix="rc0505-link-"))
        outside = Path(tempfile.mkdtemp(prefix="rc0505-linkfix-"))
        try:
            app = code / "app"
            app.mkdir()
            real = app / "real.json"
            real.write_bytes((ROOT / "app" / "review-loop-v2.json").read_bytes())
            link = app / "review-loop-v2.json"
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

    def test_live_legacy_read_writes_nothing(self) -> None:
        before_member = tree_fingerprint(LIVE_MEMBER)
        before_page = sha(LIVE_PAGE.read_bytes())
        self.assertFalse(os.path.lexists(LAYOUT))
        proc = run("live-legacy", LIBRARIAN, [
            "review-loop", "describe-legacy", "--book", str(LIVE_BOOK), "--member", "0182.desk-app-integration-design-0501",
        ])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800])
        described = as_json(proc)
        self.assertEqual(tree_fingerprint(LIVE_MEMBER), before_member)
        self.assertEqual(sha(LIVE_PAGE.read_bytes()), before_page)
        self.assertFalse(os.path.lexists(LAYOUT))
        self.assertEqual(described["schema"], "review-loop-legacy-description/1")
        self.assertEqual(described["state"], "complete")
        self.assertFalse(described["accepted"])
        self.assertFalse(described["filing_claimed"])
        self.assertFalse(described["full_success"])
        self.assertEqual(described["custody"], "not-established")
        self.assertEqual(described["task_association"], "not-established")
        self.assertTrue(described["placement_pending"])
        descriptor = described["descriptor"]
        self.assertEqual(descriptor["schema"], "return-line-descriptor/2")
        self.assertEqual(descriptor["custody_format"], "legacy-in-place/1")
        self.assertEqual(descriptor["state"], "complete")
        self.assertEqual(descriptor["route"], "matched-workflow-return-line")
        self.assertEqual(descriptor["target_page"], "0182.desk-app-integration-design-0501")
        self.assertEqual(descriptor["origin"], {"book": "00.00.10.work", "page": "0519.desk-app", "batch": "05.01"})
        self.assertEqual(descriptor["submission_id"], "claude-0519-0501")
        self.assertEqual(descriptor["placement"]["status"], "pending")
        self.assertEqual(descriptor["placement"]["intended_target_page"], "0119.desk-app")
        self.assertEqual(descriptor["receipt_sha256"], RECEIPT_SHA)
        self.assertEqual(descriptor["return_sha256"], RETURN_SHA)
        self.assertEqual(descriptor["return_bytes"], 3187)
        self.assertIsNone(descriptor["placement"]["relocation_record_path"])

    def test_real_producer_round_trip_through_the_app(self) -> None:
        self.assertFalse(os.path.lexists(LAYOUT))
        book = Book()
        try:
            book.capture("zero")
            self.assertEqual(book.descriptor["schema"], "return-line-descriptor/1")
            self.assertEqual(book.descriptor["target_page"], "0199.synth-lab")
            self.assertNotEqual(book.descriptor["target_page"], book.target)
            self.assertTrue((book.root / book.descriptor["custody_path"]).is_dir())
            self.assertNotIn("0184", book.descriptor["target_page"])
            layout = json.loads((book.root / "return-line-layout.json").read_text(encoding="utf-8"))
            self.assertFalse(layout["sequential_allocation"])
            decision = book.decide("zero")
            self.assertFalse(book.prepared["full_success"])
            self.assertEqual(book.prepared["pass_state"], "awaiting-review")
            self.assertEqual(book.prepared["observation"]["task_association"], "not-established")
            self.assertFalse(book.prepared["accepted"])
            self.assertEqual(book.prepared["custody"], "not-established")
            recorded, record_view = book.call("zero-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode()[:800])
            self.assertEqual(record_view["record"]["result"], "recorded")
            self.assertFalse(record_view["accepted"])
            rendered, render_view = book.call("zero-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:800] + rendered.stdout.decode()[:400])
            self.assertTrue(render_view["full_success"])
            self.assertFalse(render_view["accepted"])
            self.assertFalse(render_view["observation"]["filing_claimed"])
            text = book.page.read_text(encoding="utf-8")
            self.assertIn(OUTSIDE, text)
            self.assertIn(TAIL, text)
            self.assertIn(NEXT, text)
            self.assertIn(decision["binding"]["task_binding_sha256"], text)
            fresh, fresh_view = book.call("zero-read", "read")
            self.assertEqual(fresh.returncode, 0)
            self.assertEqual(fresh_view["pass_state"], "reviewed")
            self.assertTrue(fresh_view["full_success"])
            self.assertFalse(fresh_view["accepted"])
            self.assertEqual(fresh_view["observation"]["task_association"], "not-established")
            self.assertEqual((book.root / "descriptor.json").read_bytes(), book.descriptor_bytes)
            self.assertFalse(os.path.lexists(LAYOUT))
        finally:
            book.close()

    def test_changed_evidence_stays_stale(self) -> None:
        book = Book()
        try:
            book.capture("stale")
            book.decide("stale")
            self.assertEqual(book.call("stale-record", "record", "--decision", "decision.json")[0].returncode, 0)
            self.assertEqual(book.call("stale-render", "render")[0].returncode, 0)
            record_hash = sha((book.root / "cycle" / "05.01-r1" / "record.json").read_bytes())
            copy = book.copy()
            try:
                (copy / "note.md").write_bytes(b"NOTE revised\n")
                proc = run("stale-evidence", LIBRARIAN, ["review-loop", "read", "--fixture-root", str(copy), "--request", "request.json"])
                view = as_json(proc)
                self.assertEqual(view["pass_state"], "review-stale", view.get("observation"))
                self.assertFalse(view["current"]["current"])
                self.assertEqual(view["observation"]["task_association"], "not-established")
                self.assertEqual(sha((copy / "cycle" / "05.01-r1" / "record.json").read_bytes()), record_hash)
            finally:
                shutil.rmtree(copy, ignore_errors=True)
        finally:
            book.close()

    def test_duplicate_partial_and_existing_section(self) -> None:
        book = Book()
        try:
            book.capture("dup")
            book.decide("dup")
            first, _first_view = book.call("dup-record", "record", "--decision", "decision.json")
            self.assertEqual(first.returncode, 0, first.stderr.decode()[:600])
            digest = sha((book.root / "cycle" / "05.01-r1" / "record.json").read_bytes())
            replay, replay_view = book.call("dup-replay", "record", "--decision", "decision.json")
            self.assertEqual(replay.returncode, 0)
            self.assertEqual(replay_view["record"]["result"], "already-recorded")
            revised = json.loads((book.root / "decision.json").read_text(encoding="utf-8"))
            revised["judgment"]["finding"] = "A different finding."
            revised["supplied_record"]["judgment"]["finding"] = "A different finding."
            write_json(book.root / "decision-conflict.json", revised)
            refused = run("dup-conflict", LIBRARIAN, [
                "review-loop", "record", "--fixture-root", str(book.root), "--request", "request.json",
                "--decision", "decision-conflict.json",
            ])
            self.assertEqual(refused.returncode, 2)
            self.assertIn("conflict: a different review is already committed", refused.stderr.decode())
            self.assertIn("refused:", refused.stderr.decode())
            self.assertEqual(sha((book.root / "cycle" / "05.01-r1" / "record.json").read_bytes()), digest)
            rendered, _render_view = book.call("dup-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:600])
            page_hash = sha(book.page.read_bytes())
            (book.root / "cycle" / "05.01-r1" / "rendered.json").unlink()
            interrupted = run("dup-interrupt", LIBRARIAN, [
                "review-loop", "recover", "--fixture-root", str(book.root), "--request", "request.json",
            ])
            self.assertEqual(interrupted.returncode, 2)
            body = as_json(interrupted)
            self.assertEqual(body["schema"], "review-loop-refusal/1")
            self.assertIn("write token changed since read", interrupted.stderr.decode())
            self.assertIn("refused:", interrupted.stderr.decode())
            self.assertEqual(sha(book.page.read_bytes()), page_hash)
            self.assertEqual(sha((book.root / "cycle" / "05.01-r1" / "record.json").read_bytes()), digest)
        finally:
            book.close()
        conflict = Book(body="A different substantive review.\n")
        try:
            conflict.capture("section")
            conflict.decide("section")
            self.assertEqual(conflict.call("section-record", "record", "--decision", "decision.json")[0].returncode, 0)
            before = sha(conflict.page.read_bytes())
            first = run("section-recover", LIBRARIAN, [
                "review-loop", "recover", "--fixture-root", str(conflict.root), "--request", "request.json",
            ])
            view = as_json(first)
            self.assertEqual(first.returncode, 2, first.stdout.decode()[:500])
            self.assertEqual(view["render"]["result"], "render-conflict")
            self.assertTrue(view["render"]["apply_called"])
            self.assertNotIn("refused:", first.stderr.decode())
            partials = list((conflict.root / "partial").glob("*.md"))
            self.assertEqual(len(partials), 1)
            second = run("section-again", LIBRARIAN, [
                "review-loop", "recover", "--fixture-root", str(conflict.root), "--request", "request.json",
            ])
            again = as_json(second)
            self.assertEqual(second.returncode, 2)
            self.assertFalse(again["render"]["apply_called"])
            self.assertEqual(list((conflict.root / "partial").glob("*.md")), partials)
            self.assertEqual(sha(conflict.page.read_bytes()), before)
        finally:
            conflict.close()

    def test_nonzero_and_n7_through_prepare_record_render_read(self) -> None:
        nonzero = Book(page_id="1599.synth-lab")
        try:
            nonzero.capture("nonzero")
            self.assertEqual(nonzero.member, "1199.synth-lab")
            self.assertEqual(nonzero.descriptor["target_page"], "1199.synth-lab")
            decision = nonzero.decide("nonzero")
            self.assertEqual(decision["binding"]["member"], "1199.synth-lab")
            recorded, _view = nonzero.call("nonzero-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode()[:800])
            rendered, render_view = nonzero.call("nonzero-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:800] + rendered.stdout.decode()[:500])
            self.assertTrue(render_view["full_success"])
            self.assertNotIn("bad member", rendered.stderr.decode())
            self.assertNotIn("bad member", rendered.stdout.decode())
            self.assertIn(NEXT, nonzero.page.read_text(encoding="utf-8"))
            fresh, read_view = nonzero.call("nonzero-read", "read")
            self.assertEqual(fresh.returncode, 0)
            self.assertEqual(read_view["pass_state"], "reviewed")
        finally:
            nonzero.close()
        local = Book(page_id="1799.synth-colab", kind="N7NN")
        try:
            local.capture("local")
            self.assertEqual(local.descriptor["target_page"], "1799.synth-colab")
            self.assertEqual(local.descriptor["route"], "page-local-colab")
            self.assertTrue(str(local.page).endswith("06.01.review.md"))
            local.decide("local")
            recorded, _view = local.call("local-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode()[:800])
            rendered, render_view = local.call("local-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:800] + rendered.stdout.decode()[:500])
            self.assertTrue(render_view["full_success"])
            self.assertFalse(render_view["accepted"])
            text = local.page.read_text(encoding="utf-8")
            self.assertIn(NEXT, text)
            self.assertIn(OUTSIDE, text)
            self.assertIn(TAIL, text)
            fresh, read_view = local.call("local-read", "read")
            self.assertEqual(fresh.returncode, 0)
            self.assertEqual(read_view["current"]["next_action"]["text"], NEXT)
            self.assertEqual(read_view["observation"]["task_association"], "not-established")
        finally:
            local.close()


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReviewLoopEntryTests)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    out = EVIDENCE / "build05.05"
    out.mkdir(parents=True, exist_ok=True)
    (out / "suite.log").write_bytes(stream.getvalue().encode("utf-8"))
    (out / "commands.json").write_bytes(json.dumps(LOG, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    skipped = [item[0] for item in result.skipped] if hasattr(result, "skipped") else []
    (out / "skips.txt").write_bytes(("\n".join(str(item) for item in skipped) + ("\n" if skipped else "")).encode("utf-8"))
    raise SystemExit(0 if result.wasSuccessful() else 1)
