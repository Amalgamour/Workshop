#!/usr/bin/env python3
"""Focused authoring successor checks for 0526.dev-authoring/05.03.

Importing this file writes nothing. The suite runs only as __main__.
It does not run the pass01 suite and it does not write authoring05.02.
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
import threading
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LIB = ROOT / "app" / "librarian.py"
PREVIEW = ROOT / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "evidence" / "authoring05.02"
PAGE = ROOT / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "05.03.md"
SET = ROOT / "labs" / "app-dependencies-pass02" / "set.json"
REL = [
    "00.kernel/00.00.10.work/0423.dev-authoring/01.md",
    "00.kernel/00.00.10.work/0423.dev-authoring/06.01.md",
    "00.kernel/00.00.10.work/0423.dev-authoring/06.02.md",
    "00.kernel/00.00.10.work/0423.dev-authoring/templates/build-pack-v1.draft.md",
    "00.kernel/00.00.10.work/0526.dev-authoring/01.md",
]
NOTE_A = "00.kernel/00.00.10.work/0423.dev-authoring/06.01.md"
NOTE_B = "00.kernel/00.00.10.work/0423.dev-authoring/06.02.md"
FIXTURE_NOTE = "00.kernel/00.00.10.work/0491.fixture-source/06.01.md"
ZEROS = "0" * 64
HELP = "labs/pack-authoring-pass02/PRIME-USE.md"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_app(args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run([str(PY), "-B", str(LIB), *args], cwd=ROOT, capture_output=True, env=env)


def write_json(path: Path, value: object) -> None:
    path.write_bytes(json.dumps(value, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def snapshot(directory: Path) -> dict:
    found = {}
    if not directory.exists():
        return found
    for path in sorted(directory.iterdir()):
        if path.is_file():
            raw = path.read_bytes()
            found[path.name] = {"sha256": digest(raw), "bytes": len(raw)}
    return found


def seed_live_profile(book: Path, occupant: bool) -> None:
    for rel in REL:
        dest = book / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((ROOT / rel).read_bytes())
    if occupant:
        (book / "00.kernel" / "00.00.10.work" / "0126.boot-members-0509").mkdir()


def intent() -> dict:
    return {
        "goal": "Check the typed form and the review binding.",
        "scope": {
            "included": "two items and a prepared page in this disposable book",
            "excluded": "release, return filing, and the live checkout",
            "allowed_writes": "this disposable book only",
        },
        "finish": "Freeze writes the final reviewed bytes",
        "executor": "Grok-1",
        "reviewer": "Codex Prime",
    }


def item(title: str, purpose: str, note: str) -> dict:
    return {
        "title": title,
        "purpose": purpose,
        "requirements": ["The caller does not choose the item number."],
        "interfaces": [],
        "acceptance": ["Inspect shows this purpose under the computed number."],
        "note_refs": [note] if note else [],
        "open_choices": [],
        "dependency_refs": [],
        "relationship": None,
        "condition": None,
    }


class Suite:
    def __init__(self) -> None:
        self.cases: list[dict] = []
        self.first: dict | None = None

    def add(self, name: str, ok: bool, detail: str) -> None:
        row = {"name": name, "ok": bool(ok), "detail": detail}
        self.cases.append(row)
        if not ok and self.first is None:
            self.first = row
        print(("PASS " if ok else "FAIL ") + name)
        if not ok:
            print(detail[:1500])

    def expect(self, name: str, result: subprocess.CompletedProcess, code: int, text: str = "") -> dict | None:
        err = result.stderr.decode("utf-8", "replace")
        out = result.stdout.decode("utf-8", "replace")
        ok = result.returncode == code and (text in err if code else text in out or text == "")
        if code != 0:
            ok = ok and out == ""
        self.add(name, ok, f"exit {result.returncode} expected {code}\n{err}\n{out[:700]}")
        if result.returncode == 0 and out.strip().startswith("{"):
            return json.loads(out)
        return None


def is_junction(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return bool(getattr(info, "st_file_attributes", 0) & 0x400)


def remove_junction(path: Path) -> None:
    if is_junction(path):
        os.rmdir(path)


def work_of(book: Path, home: str) -> Path:
    return book / home


def dispatcher(suite: Suite) -> None:
    result = run_app(["where"])
    err = result.stderr.decode("utf-8", "replace")
    suite.add(
        "where missing root",
        result.returncode == 2 and result.stdout == b"" and err.startswith("stop: missing --root"),
        err,
    )


def pins(suite: Suite) -> None:
    declaration = json.loads((ROOT / "app" / "review-loop-v4.json").read_text(encoding="utf-8"))
    ok = True
    detail = []
    for name, spec in declaration["tools"].items():
        raw = (ROOT / spec["path"]).read_bytes()
        match = digest(raw) == spec["sha256"] and len(raw) == spec["bytes"]
        ok = ok and match
        if not match:
            detail.append(name)
    text = (ROOT / "app" / "librarian.py").read_text(encoding="utf-8")
    ok = ok and "review_loop_tools_v4.py" in text and "librarian_review_loop_tools_v4" in text
    ok = ok and 'authoring_tools_v2.py", "librarian_authoring_tools_v2"' in text
    suite.add("review-loop v4 pins unchanged", ok, ",".join(detail) or "matched")
    door = json.loads((ROOT / "app" / "authoring-v2.json").read_text(encoding="utf-8"))
    pinned = True
    missing = []
    for key in ("module", "form", "predecessor", "dependency_reader", "dependency_set", "pack_checker"):
        spec = door[key]
        raw = (ROOT / spec["path"]).read_bytes()
        if digest(raw) != spec["sha256"] or len(raw) != spec["bytes"]:
            pinned = False
            missing.append(key)
    for spec in door["profiles"].values():
        raw = (ROOT / spec["path"]).read_bytes()
        if digest(raw) != spec["sha256"] or len(raw) != spec["bytes"]:
            pinned = False
            missing.append(spec["path"])
    previous = (ROOT / "app" / "authoring_tools.py").read_bytes()
    previous_decl = (ROOT / "app" / "authoring.json").read_bytes()
    previous_test = (ROOT / "app" / "tests" / "test_authoring_entry.py").read_bytes()
    pinned = pinned and digest(previous) == "13cbc91f880c13dfd5b07afe9284092d16bba01afe1a0d5c06b7b3ff35f3ab54"
    pinned = pinned and len(previous) == 7817
    pinned = pinned and digest(previous_decl) == "8a59bbd93086ac88c37e1e7a44f7db4b6f3d77fe1294aa67ce559d3550885816"
    pinned = pinned and len(previous_decl) == 1864
    pinned = pinned and digest(previous_test) == "ff326f3180aa61357299b8f14bf51b8496eeda6beedcbb8f9c53c4948351c205"
    pinned = pinned and len(previous_test) == 34908
    suite.add("v2 pins and pass01 door unchanged", pinned, ",".join(missing) or "matched")


def junction(suite: Suite, door) -> None:
    base = Path(tempfile.mkdtemp(prefix="author-v2-junction-"))
    try:
        target = base / "target"
        (target / "book").mkdir(parents=True)
        alias = base / "alias"
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(alias), str(target)], capture_output=True)
        suite.add("junction created", made.returncode == 0 and is_junction(alias), made.stderr.decode("utf-8", "replace"))
        called = {"value": False}

        def boom(*_args, **_kwargs):
            called["value"] = True
            raise AssertionError("launched")

        previous = door.subprocess.run
        door.subprocess.run = boom
        try:
            try:
                door.perform(
                    ["form", "--book", str(alias / "book"), "--profile", "0423-to-0526", "--json"],
                    ROOT,
                )
                message = ""
            except door.Refuse as exc:
                message = str(exc)
        finally:
            door.subprocess.run = previous
        suite.add(
            "ancestor junction does not launch",
            (not called["value"]) and message == "book root ancestor is linked and was not followed",
            message,
        )
        banned = {"value": False}

        def boom_banned(*_args, **_kwargs):
            banned["value"] = True
            raise AssertionError("launched")

        door.subprocess.run = boom_banned
        try:
            try:
                door.perform(
                    ["form", "--book", str(target / "book"), "--profile", "0423-to-0526", "--template", "x"],
                    ROOT,
                )
                banned_message = ""
            except door.Refuse as exc:
                banned_message = str(exc)
        finally:
            door.subprocess.run = previous
        suite.add(
            "template override does not launch",
            (not banned["value"]) and banned_message == "caller tool override is refused",
            banned_message,
        )
        direct = base / "direct-book"
        subprocess.run(["cmd", "/c", "mklink", "/J", str(direct), str(target)], capture_output=True)
        direct_cli = run_app(["authoring", "inspect", "--book", str(direct), "--profile", "0423-to-0526", "--json"])
        direct_err = direct_cli.stderr.decode("utf-8", "replace")
        suite.add(
            "direct junction refused",
            direct_cli.returncode == 2 and direct_cli.stdout == b"" and "book root is not a directory" in direct_err,
            direct_err,
        )
        link_file = base / "file-link"
        source_file = base / "file.txt"
        source_file.write_text("x", encoding="utf-8")
        try:
            os.symlink(source_file, link_file)
            suite.add("file symlink skip", False, "created; this host allowed a file symlink")
        except OSError as exc:
            suite.add("file symlink skip", getattr(exc, "winerror", None) == 1314, f"WinError {getattr(exc, 'winerror', None)}")
    finally:
        for name in ("alias", "direct-book"):
            remove_junction(base / name)
        shutil.rmtree(base, ignore_errors=True)


def interrupt(suite: Suite, author) -> None:
    base = Path(tempfile.mkdtemp(prefix="author-v2-interrupt-"))
    try:
        record = base / "record.json"
        original = b'{"schema":"authoring-record/1","marker":"previous"}\n'
        record.write_bytes(original)

        def boom(src, dst):
            raise OSError(5, "injected")

        try:
            author.base.commit_record(
                record,
                {"schema": "authoring-record/1", "marker": "next"},
                "op-interrupt",
                replace=boom,
            )
            suite.add("interrupted replace", False, "replace returned")
        except author.base.Partial as exc:
            partial = base / "record.json.partial-op-interrupt"
            suite.add(
                "interrupted replace",
                record.read_bytes() == original and partial.is_file() and b"next" in partial.read_bytes(),
                str(exc),
            )
    finally:
        shutil.rmtree(base, ignore_errors=True)


def reserve_race(suite: Suite, author, temps: list[Path]) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-v2-reserve-"))
    temps.append(book)
    work = book / "work"
    work.mkdir()
    found: list[str] = []
    errors: list[str] = []

    def once() -> None:
        try:
            name, _slot = author.base.reserve_pass(work)
            found.append(name)
        except Exception as exc:
            errors.append(str(exc))

    threads = [threading.Thread(target=once) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    suite.add("two reserves differ", not errors and sorted(found) == ["05.01", "05.02"], f"{found} {errors}")


def typed(suite: Suite, temps: list[Path]) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-v2-typed-"))
    temps.append(book)
    seed_live_profile(book, occupant=False)
    folder = book / "in"
    folder.mkdir()
    evidence = book / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "evidence"
    base_intent = intent()
    cases = {
        "absent": {key: value for key, value in base_intent.items() if key != "goal"},
        "null": dict(base_intent, goal=None),
        "empty": dict(base_intent, goal=""),
        "wrong-type": dict(base_intent, goal=1),
        "extra": dict(base_intent, candidate_sha256=ZEROS),
    }
    for state, payload in cases.items():
        path = folder / f"{state}.json"
        write_json(path, payload)
        result = run_app(
            [
                "authoring",
                "start",
                "--book",
                str(book),
                "--profile",
                "0423-to-0526",
                "--operation",
                f"typed-{state}",
                "--input",
                str(path),
                "--json",
            ]
        )
        err = result.stderr.decode("utf-8", "replace")
        suite.add(
            f"typed start state {state}",
            result.returncode == 2
            and result.stdout == b""
            and f"state {state}" in err
            and HELP in err
            and not evidence.exists(),
            err,
        )


def call(book: Path, profile: str, args: list[str]) -> subprocess.CompletedProcess:
    return run_app(["authoring", args[0], "--book", str(book), "--profile", profile, *args[1:]])


def happy(suite: Suite, temps: list[Path], run_dir: Path) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-v2-happy-"))
    temps.append(book)
    seed_live_profile(book, occupant=True)
    folder = book / "in"
    folder.mkdir()
    profile = "0423-to-0526"
    evidence = book / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "evidence"
    formed = call(book, profile, ["form", "--json"])
    form_body = suite.expect("source-only form", formed, 0)
    declaration = json.loads((ROOT / "labs" / "pack-authoring-pass02" / "forms" / "build-pack-v1.json").read_text(encoding="utf-8"))
    form_ok = bool(form_body) and form_body["schema"] == "authoring-form/1" and form_body["kind"] == "intent"
    form_ok = form_ok and form_body["fields"] == declaration["forms"]["intent"]["fields"]
    form_ok = form_ok and form_body["declaration_sha256"] == "b3d18c26699674d7aa0607e491210664b31e90a63dba13860befb5409b0416ab"
    form_ok = form_ok and form_body["draft_status"]["state"] == "absent"
    form_ok = form_ok and form_body["profile_id"] == profile
    form_ok = form_ok and form_body["example_input"] == declaration["forms"]["intent"]["example_input"]
    form_ok = form_ok and "Show the source form" not in formed.stdout.decode("utf-8")
    form_ok = form_ok and not evidence.exists()
    suite.add("form is the declaration and writes nothing", form_ok, "form mismatch" if form_body else "no form")
    asked = call(book, profile, ["form", "--kind", "review", "--json"])
    asked_body = suite.expect("explicit review form", asked, 0)
    suite.add(
        "requested form writes nothing",
        bool(asked_body) and asked_body["kind"] == "review" and asked_body["fields"] == declaration["forms"]["review"]["fields"] and not evidence.exists(),
        str(asked_body and asked_body.get("kind")),
    )
    if form_body:
        (run_dir / "form.json").write_bytes(formed.stdout)
    write_json(folder / "intent.json", intent())
    started = call(book, profile, ["start", "--operation", "start-01", "--input", str(folder / "intent.json"), "--json"])
    start_body = suite.expect("filled start", started, 0)
    suite.add(
        "start returns the item form",
        bool(start_body)
        and start_body["schema"] == "authoring-result/2"
        and start_body["next_form"] == "item"
        and start_body["form"]["fields"] == declaration["forms"]["item"]["fields"]
        and start_body["pass"] == "05.01"
        and start_body["final_sha256"] is None
        and start_body["candidate_sha256"] == start_body["draft_sha256"],
        str(start_body and start_body.get("next_form")),
    )
    if not start_body:
        return
    slot = Path(start_body["record"]).parent
    planted = slot / "draft.md.conflict-planted"
    planted.write_bytes(b"planted\n")
    write_json(
        folder / "item-01.json",
        item("Caller form check", "Caller form check. Compute assigns the number.", NOTE_A),
    )
    write_json(
        folder / "item-01-other.json",
        item("Different title", "Different purpose under the same operation.", NOTE_A),
    )
    write_json(
        folder / "item-02.json",
        item("Second meaning", "Second meaning stays in its own item. Mark \u0394.", NOTE_B),
    )
    added = call(book, profile, ["add-item", "--operation", "item-01", "--input", str(folder / "item-01.json"), "--json"])
    item_body = suite.expect("first item", added, 0)
    replay = call(book, profile, ["add-item", "--operation", "item-01", "--input", str(folder / "item-01.json"), "--json"])
    suite.add(
        "exact item retry",
        replay.returncode == 0 and replay.stdout == added.stdout and item_body is not None and item_body["derived_history"] is True and item_body["derived_conflict"] is False,
        replay.stderr.decode()[:400],
    )
    conflict = call(book, profile, ["add-item", "--operation", "item-01", "--input", str(folder / "item-01-other.json"), "--json"])
    suite.expect("conflicting item", conflict, 2, "conflicting operation")
    second = call(book, profile, ["add-item", "--operation", "item-02", "--input", str(folder / "item-02.json"), "--json"])
    second_body = suite.expect("second item", second, 0)
    record = json.loads(Path(start_body["record"]).read_text(encoding="utf-8"))
    suite.add(
        "restarted record has two items",
        bool(second_body)
        and len(record["items"]) == 2
        and record["items"][0]["id"] == "01"
        and record["items"][1]["id"] == "02"
        and "\u0394" in second_body["draft_text"],
        str(len(record["items"])),
    )
    suite.add(
        "ordinary history is not a conflict",
        (slot / "draft.md.history-item-01").is_file()
        and planted.read_bytes() == b"planted\n"
        and not any(path.name.startswith("draft.md.conflict-") and path.name != "draft.md.conflict-planted" for path in slot.iterdir()),
        " ".join(path.name for path in slot.iterdir()),
    )
    saved = Path(start_body["record"]).read_bytes()
    stripped = json.loads(saved)
    del stripped["form_binding"]
    Path(start_body["record"]).write_bytes(json.dumps(stripped).encode("utf-8") + b"\n")
    preserved = call(book, profile, ["add-item", "--operation", "preserve-01", "--input", str(folder / "item-02.json"), "--json"])
    suite.expect("pass01 record is preserved", preserved, 2, "pass01 record is preserved")
    Path(start_body["record"]).write_bytes(saved)
    empty_rel = item("Empty relationship", "This object should be refused.", NOTE_A)
    empty_rel["relationship"] = {}
    write_json(folder / "empty-rel.json", empty_rel)
    suite.expect(
        "empty relationship refused",
        call(book, profile, ["add-item", "--operation", "item-empty", "--input", str(folder / "empty-rel.json"), "--json"]),
        2,
        "state empty",
    )
    extra = item("Extra field", "This field should be refused.", NOTE_A)
    extra["pass"] = "05.99"
    write_json(folder / "extra.json", extra)
    suite.expect(
        "extra field refused",
        call(book, profile, ["add-item", "--operation", "item-extra", "--input", str(folder / "extra.json"), "--json"]),
        2,
        "state extra",
    )
    write_json(folder / "note.json", {"text": "A note.", "attribution": "Grok-1", "source": "check", "mark": None})
    suite.expect(
        "null mark refused",
        call(book, profile, ["add-note", "--operation", "note-null", "--input", str(folder / "note.json"), "--json"]),
        2,
        "state null",
    )
    write_json(folder / "bad-unresolved.json", {"disposition": "unresolved"})
    write_json(folder / "bad-why.json", {"disposition": "deferred"})
    write_json(folder / "bad-extra-why.json", {"disposition": "integrated", "item": "01", "why": "present"})
    suite.expect(
        "unresolved is not a submitted disposition",
        call(book, profile, ["revise", "--operation", "disp-bad-1", "--target", "disposition", "--note", NOTE_A, "--input", str(folder / "bad-unresolved.json"), "--json"]),
        2,
        "state wrong-type",
    )
    suite.expect(
        "deferred why absent",
        call(book, profile, ["revise", "--operation", "disp-bad-2", "--target", "disposition", "--note", NOTE_A, "--input", str(folder / "bad-why.json"), "--json"]),
        2,
        "state absent",
    )
    suite.expect(
        "integrated why is extra",
        call(book, profile, ["revise", "--operation", "disp-bad-3", "--target", "disposition", "--note", NOTE_A, "--input", str(folder / "bad-extra-why.json"), "--json"]),
        2,
        "state extra",
    )
    write_json(folder / "disp-01.json", {"disposition": "integrated", "item": "01"})
    write_json(folder / "disp-02.json", {"disposition": "deferred", "why": "Supplied check: the note is deferred and the draft stays unreleased."})
    suite.expect(
        "integrate first note",
        call(book, profile, ["revise", "--operation", "disp-01", "--target", "disposition", "--note", NOTE_A, "--input", str(folder / "disp-01.json"), "--json"]),
        0,
    )
    suite.expect(
        "defer second note",
        call(book, profile, ["revise", "--operation", "disp-02", "--target", "disposition", "--note", NOTE_B, "--input", str(folder / "disp-02.json"), "--json"]),
        0,
    )
    waiting = suite.expect("form needed is review", call(book, profile, ["form", "--json"]), 0)
    suite.add(
        "review form selected",
        bool(waiting) and waiting["kind"] == "review" and waiting["fields"] == declaration["forms"]["review"]["fields"],
        str(waiting and waiting.get("kind")),
    )
    inspected = suite.expect("inspect candidate", call(book, profile, ["inspect", "--json"]), 0)
    if not inspected:
        return
    candidate = inspected["candidate_sha256"]
    text_hash = digest(inspected["draft_text"].encode("utf-8"))
    suite.add(
        "candidate is the rendered draft",
        inspected["schema"] == "authoring-result/2"
        and inspected["final_sha256"] is None
        and candidate == inspected["draft_sha256"] == text_hash
        and candidate not in inspected["draft_text"]
        and inspected["selected_review"] is None
        and inspected["face_status"] == "matches-record"
        and inspected["return_intent"]["intended"] == "0126.dev-authoring"
        and inspected["return_intent"]["status"] == "occupied"
        and inspected["return_intent"]["occupants"] == ["0126.boot-members-0509"]
        and inspected["return_intent"]["readiness"] == "blocked"
        and "complete_claim: false" in inspected["draft_text"],
        inspected["return_intent"]["status"],
    )
    review = {
        "assessment": "The inspected candidate has two items and one deferred note. This judgment is not release.",
        "unresolved_issues": "Return readiness stays blocked.",
        "stop_conditions": "A changed candidate or a changed source stops the freeze.",
    }
    write_json(folder / "review.json", review)
    write_json(folder / "review-other.json", dict(review, assessment="A different judgment."))
    suite.expect(
        "review requires the candidate",
        call(book, profile, ["review", "--operation", "review-01", "--input", str(folder / "review.json"), "--json"]),
        2,
        "candidate identity is required",
    )
    before_stale = digest(Path(start_body["record"]).read_bytes())
    suite.expect(
        "stale candidate is not stored",
        call(book, profile, ["review", "--operation", "review-01", "--input", str(folder / "review.json"), "--draft-sha256", ZEROS, "--json"]),
        2,
        "stale candidate",
    )
    suite.add("stale review left the record", digest(Path(start_body["record"]).read_bytes()) == before_stale, "record changed")
    reviewed_proc = call(
        book,
        profile,
        ["review", "--operation", "review-01", "--input", str(folder / "review.json"), "--draft-sha256", candidate, "--json"],
    )
    reviewed = suite.expect("review binds the candidate", reviewed_proc, 0)
    suite.add(
        "candidate stays and final is separate",
        bool(reviewed)
        and reviewed["candidate_sha256"] == candidate
        and reviewed["final_sha256"]
        and reviewed["final_sha256"] != candidate
        and reviewed["draft_sha256"] == reviewed["final_sha256"]
        and reviewed["selected_review"]["assessment"] == review["assessment"]
        and candidate not in reviewed["draft_text"]
        and reviewed["final_sha256"] not in reviewed["draft_text"],
        str(reviewed and reviewed.get("final_sha256")),
    )
    if not reviewed:
        return
    replay = call(
        book,
        profile,
        ["review", "--operation", "review-01", "--input", str(folder / "review.json"), "--draft-sha256", candidate, "--json"],
    )
    suite.add(
        "exact review retry",
        replay.returncode == 0 and replay.stdout == reviewed_proc.stdout,
        replay.stderr.decode()[:400],
    )
    suite.expect(
        "conflicting review",
        call(book, profile, ["review", "--operation", "review-01", "--input", str(folder / "review-other.json"), "--draft-sha256", candidate, "--json"]),
        2,
        "conflicting operation",
    )
    final_proc = call(book, profile, ["inspect", "--json"])
    final_view = suite.expect("inspect final document", final_proc, 0)
    final_sha = reviewed["final_sha256"]
    suite.add(
        "final inspect keeps both identities",
        bool(final_view)
        and final_view["candidate_sha256"] == candidate
        and final_view["final_sha256"] == final_sha
        and final_view["draft_sha256"] == final_sha
        and final_view["review_valid"] is True
        and final_view["selected_review"]["candidate_sha256"] == candidate
        and final_view["selected_review"]["final_sha256"] == final_sha
        and final_view["next_form"] is None
        and "freeze with the final sha256" in final_view["next"],
        str(final_view and final_view.get("review_valid")),
    )
    if not final_view:
        return
    (run_dir / "inspect-final.json").write_bytes(final_proc.stdout)
    record_path = Path(start_body["record"])
    good_record = record_path.read_bytes()
    page = book / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "05.01.md"
    suite.expect(
        "candidate hash is not the final document",
        call(book, profile, ["freeze", "--operation", "freeze-01", "--draft-sha256", candidate, "--json"]),
        2,
        "final document identity does not match",
    )
    suite.add(
        "mismatched freeze wrote nothing",
        not page.exists() and record_path.read_bytes() == good_record,
        str(page.exists()),
    )
    changed = json.loads(good_record)
    changed["form_binding"]["sha256"] = ZEROS
    record_path.write_bytes(json.dumps(changed).encode("utf-8") + b"\n")
    suite.expect(
        "changed form",
        call(book, profile, ["freeze", "--operation", "freeze-form", "--draft-sha256", final_sha, "--json"]),
        2,
        "changed form",
    )
    suite.add("changed form wrote no page", not page.exists(), str(page.exists()))
    record_path.write_bytes(good_record)
    restored = suite.expect("review valid after form restore", call(book, profile, ["inspect", "--json"]), 0)
    suite.add(
        "restored review still valid",
        bool(restored) and restored["review_valid"] is True and restored["candidate_sha256"] == candidate,
        str(restored and restored.get("review_valid")),
    )
    source = book / REL[0]
    source_bytes = source.read_bytes()
    source.write_bytes(source_bytes + b"\n")
    drifted = suite.expect("inspect source drift", call(book, profile, ["inspect", "--json"]), 0)
    suite.add(
        "source drift visible",
        bool(drifted) and drifted["live"]["source_drift"] is True and drifted["review_valid"] is False,
        str(drifted and drifted.get("live")),
    )
    suite.expect(
        "source drift refuses freeze",
        call(book, profile, ["freeze", "--operation", "freeze-source", "--draft-sha256", final_sha, "--json"]),
        2,
        "source-drift",
    )
    suite.add("source drift wrote no page", not page.exists(), str(page.exists()))
    source.write_bytes(source_bytes)
    record_path.write_bytes(good_record)
    clean = suite.expect("source restored", call(book, profile, ["inspect", "--json"]), 0)
    suite.add(
        "restored source matches",
        bool(clean) and clean["live"]["source_drift"] is False and clean["review_valid"] is True,
        str(clean and clean.get("live")),
    )
    draft_path = slot / "draft.md"
    draft_path.write_bytes(b"divergent face\n")
    diverged = suite.expect("inspect divergence", call(book, profile, ["inspect", "--json"]), 0)
    suite.add(
        "divergent face is not ordinary history",
        bool(diverged)
        and diverged["face_status"] == "divergence"
        and diverged["derived_divergence"] is True
        and diverged["derived_conflict"] is True,
        str(diverged and diverged.get("face_status")),
    )
    freeze_proc = call(book, profile, ["freeze", "--operation", "freeze-01", "--draft-sha256", final_sha, "--json"])
    frozen = suite.expect("freeze final document", freeze_proc, 0)
    page_bytes = page.read_bytes() if page.is_file() else b""
    draft_bytes = draft_path.read_bytes() if draft_path.is_file() else b""
    suite.add(
        "frozen page matches the final document",
        bool(frozen)
        and frozen["state"] == "frozen"
        and page_bytes == draft_bytes
        and digest(page_bytes) == final_sha
        and b"approval: false" in page_bytes
        and b"release: false" in page_bytes
        and b"complete_claim: false" in page_bytes
        and "\u0394".encode("utf-8") in page_bytes
        and candidate.encode("ascii") not in page_bytes
        and final_sha.encode("ascii") not in page_bytes
        and planted.read_bytes() == b"planted\n"
        and (slot / "draft.md.divergence-freeze-01").is_file(),
        frozen["state"] if frozen else freeze_proc.stderr.decode()[:500],
    )
    if page_bytes:
        (run_dir / "draft.md").write_bytes(draft_bytes)
        (run_dir / "05.01.md").write_bytes(page_bytes)
    replay_freeze = call(book, profile, ["freeze", "--operation", "freeze-01", "--draft-sha256", final_sha, "--json"])
    suite.add(
        "exact freeze retry",
        replay_freeze.returncode == 0 and replay_freeze.stdout == freeze_proc.stdout and page.read_bytes() == page_bytes,
        replay_freeze.stderr.decode()[:400],
    )
    suite.expect(
        "conflicting freeze",
        call(book, profile, ["freeze", "--operation", "freeze-01", "--draft-sha256", ZEROS, "--json"]),
        2,
        "conflicting operation",
    )
    suite.add("conflict left the page", page.read_bytes() == page_bytes, "page changed")
    after = suite.expect("inspect after freeze", call(book, profile, ["inspect", "--json"]), 0)
    suite.add(
        "later inspect matches the record",
        bool(after) and after["face_status"] == "matches-record" and after["page_matches_draft"] is True,
        str(after and after.get("face_status")),
    )


def seed_fixture(book: Path) -> None:
    base = book / "00.kernel" / "00.00.10.work"
    source = base / "0491.fixture-source"
    (source / "templates").mkdir(parents=True)
    (source / "raw").mkdir()
    (source / "01.md").write_text("fixture source\n", encoding="utf-8")
    (source / "06.01.md").write_text("fixture note\n", encoding="utf-8")
    (source / "templates" / "build-pack-v1.draft.md").write_text("fixture template\n", encoding="utf-8")
    (source / "raw" / "blob.bin").write_bytes(b"\xff\x00raw")
    work = base / "0591.fixture-authoring"
    work.mkdir()
    (work / "01.md").write_text("fixture work\n", encoding="utf-8")
    dep = book / "dependency"
    dep.mkdir()
    (dep / "set.json").write_bytes(SET.read_bytes())


def fixture(suite: Suite, temps: list[Path]) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-v2-fixture-"))
    temps.append(book)
    seed_fixture(book)
    folder = book / "in"
    folder.mkdir()
    write_json(folder / "intent.json", intent())
    started = call(book, "fixture-authoring", ["start", "--operation", "f-start", "--input", str(folder / "intent.json"), "--json"])
    body = suite.expect("fixture start", started, 0)
    suite.add(
        "raw source stays raw",
        bool(body) and "utf8 false" in body["draft_text"] and body["return_intent"]["status"] == "unfiled" and body["return_intent"]["readiness"] == "blocked",
        str(body and body.get("return_intent")),
    )
    related = item("Relationship stays unresolved", "Compute records the relationship and does not write the set.", "")
    related["note_refs"] = []
    related["relationship"] = {
        "target_repository": "lib-build",
        "target_path": "app/librarian.py",
        "meaning": "The relationship is asserted and left unresolved.",
    }
    write_json(folder / "related.json", related)
    added = call(book, "fixture-authoring", ["add-item", "--operation", "f-item", "--input", str(folder / "related.json"), "--json"])
    added_body = suite.expect("relationship item", added, 0)
    suite.add(
        "relationship stays unresolved-not-in-set",
        bool(added_body) and "unresolved-not-in-set" in added_body["draft_text"],
        "missing state",
    )
    empty = dict(related)
    empty["relationship"] = {}
    write_json(folder / "empty.json", empty)
    suite.expect(
        "fixture empty relationship refused",
        call(book, "fixture-authoring", ["add-item", "--operation", "f-empty", "--input", str(folder / "empty.json"), "--json"]),
        2,
        "state empty",
    )
    dep = book / "dependency" / "set.json"
    dep.write_bytes(dep.read_bytes() + b"\n")
    inspected = suite.expect("fixture inspect", call(book, "fixture-authoring", ["inspect", "--json"]), 0)
    suite.add("stale set visible", bool(inspected) and inspected["live"]["set_drift"] is True, str(inspected and inspected.get("live")))
    suite.expect(
        "stale set refuses freeze",
        call(book, "fixture-authoring", ["freeze", "--operation", "f-freeze", "--draft-sha256", ZEROS, "--json"]),
        2,
        "stale dependency set",
    )


def dependencies(suite: Suite, temps: list[Path]) -> None:
    missing_book = Path(tempfile.mkdtemp(prefix="author-v2-missing-"))
    temps.append(missing_book)
    seed_live_profile(missing_book, occupant=False)
    folder = missing_book / "in"
    folder.mkdir()
    missing_item = item("Missing dependency", "The lookup stays a finding.", NOTE_A)
    missing_item["dependency_refs"] = [{"repository": "lib-build", "path": "labs/not-a-declared-module.py"}]
    write_json(folder / "intent.json", intent())
    write_json(folder / "item.json", missing_item)
    write_json(folder / "disp.json", {"disposition": "integrated", "item": "01"})
    write_json(folder / "disp2.json", {"disposition": "deferred", "why": "The other note is deferred for this check."})
    write_json(
        folder / "review.json",
        {"assessment": "Review with a missing ref.", "unresolved_issues": "The missing module stays missing.", "stop_conditions": "Freeze stops."},
    )
    call(missing_book, "0423-to-0526", ["start", "--operation", "m-start", "--input", str(folder / "intent.json"), "--json"])
    added = call(missing_book, "0423-to-0526", ["add-item", "--operation", "m-item", "--input", str(folder / "item.json"), "--json"])
    added_body = json.loads(added.stdout.decode("utf-8")) if added.returncode == 0 and added.stdout.strip().startswith(b"{") else {}
    suite.add("missing dependency labelled", added.returncode == 0 and "labels missing" in added_body.get("draft_text", ""), added.stderr.decode()[:500] or added_body.get("draft_text", "")[-300:])
    call(missing_book, "0423-to-0526", ["revise", "--operation", "m-a", "--target", "disposition", "--note", NOTE_A, "--input", str(folder / "disp.json"), "--json"])
    call(missing_book, "0423-to-0526", ["revise", "--operation", "m-b", "--target", "disposition", "--note", NOTE_B, "--input", str(folder / "disp2.json"), "--json"])
    inspected = call(missing_book, "0423-to-0526", ["inspect", "--json"])
    inspected_body = json.loads(inspected.stdout.decode("utf-8")) if inspected.returncode == 0 else {}
    reviewed = call(
        missing_book,
        "0423-to-0526",
        ["review", "--operation", "m-review", "--input", str(folder / "review.json"), "--draft-sha256", inspected_body.get("candidate_sha256", ZEROS), "--json"],
    )
    reviewed_body = json.loads(reviewed.stdout.decode("utf-8")) if reviewed.returncode == 0 else {}
    refused = call(
        missing_book,
        "0423-to-0526",
        ["freeze", "--operation", "m-freeze", "--draft-sha256", reviewed_body.get("final_sha256", ZEROS), "--json"],
    )
    err = refused.stderr.decode("utf-8", "replace")
    suite.add("missing dependency refuses freeze", refused.returncode == 2 and refused.stdout == b"" and "is missing" in err, err)

    stale_book = Path(tempfile.mkdtemp(prefix="author-v2-stale-"))
    temps.append(stale_book)
    seed_live_profile(stale_book, occupant=False)
    folder = stale_book / "in"
    folder.mkdir()
    stale_item = item("Stale claim", "The claimed digest is not the measured file.", NOTE_A)
    stale_item["dependency_refs"] = [{"repository": "lib-build", "path": "app/librarian.py", "claimed_sha256": ZEROS}]
    write_json(folder / "intent.json", intent())
    write_json(folder / "item.json", stale_item)
    write_json(folder / "disp.json", {"disposition": "integrated", "item": "01"})
    write_json(folder / "disp2.json", {"disposition": "deferred", "why": "Deferred for the stale check."})
    write_json(
        folder / "review.json",
        {"assessment": "Review with a stale claim.", "unresolved_issues": "The claim does not match.", "stop_conditions": "Freeze stops."},
    )
    call(stale_book, "0423-to-0526", ["start", "--operation", "s-start", "--input", str(folder / "intent.json"), "--json"])
    added = call(stale_book, "0423-to-0526", ["add-item", "--operation", "s-item", "--input", str(folder / "item.json"), "--json"])
    added_body = json.loads(added.stdout.decode("utf-8")) if added.returncode == 0 and added.stdout.strip().startswith(b"{") else {}
    suite.add("stale claim labelled", added.returncode == 0 and "stale" in added_body.get("draft_text", ""), added.stderr.decode()[:500] or added_body.get("draft_text", "")[-400:])
    call(stale_book, "0423-to-0526", ["revise", "--operation", "s-a", "--target", "disposition", "--note", NOTE_A, "--input", str(folder / "disp.json"), "--json"])
    call(stale_book, "0423-to-0526", ["revise", "--operation", "s-b", "--target", "disposition", "--note", NOTE_B, "--input", str(folder / "disp2.json"), "--json"])
    inspected = call(stale_book, "0423-to-0526", ["inspect", "--json"])
    inspected_body = json.loads(inspected.stdout.decode("utf-8")) if inspected.returncode == 0 else {}
    reviewed = call(
        stale_book,
        "0423-to-0526",
        ["review", "--operation", "s-review", "--input", str(folder / "review.json"), "--draft-sha256", inspected_body.get("candidate_sha256", ZEROS), "--json"],
    )
    reviewed_body = json.loads(reviewed.stdout.decode("utf-8")) if reviewed.returncode == 0 else {}
    refused = call(
        stale_book,
        "0423-to-0526",
        ["freeze", "--operation", "s-freeze", "--draft-sha256", reviewed_body.get("final_sha256", ZEROS), "--json"],
    )
    err = refused.stderr.decode("utf-8", "replace")
    suite.add("stale claim refuses freeze", refused.returncode == 2 and refused.stdout == b"" and "is stale" in err, err)


def boundaries(suite: Suite) -> None:
    outside = run_app(["authoring", "form", "--book", str(ROOT), "--profile", "fixture-authoring", "--json"])
    suite.expect("fixture profile refuses the checkout", outside, 2, "book root must stay outside")
    live = run_app(
        ["authoring", "freeze", "--book", str(ROOT), "--profile", "0423-to-0526", "--operation", "live-freeze", "--draft-sha256", ZEROS, "--json"]
    )
    suite.expect("live freeze refused", live, 2, "freeze on the live checkout is outside this slice")


def main() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = ROOT / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "evidence" / "build05.03" / "runs" / stamp
    run_dir.mkdir(parents=True)
    suite = Suite()
    preview_before = snapshot(PREVIEW)
    page_before = digest(PAGE.read_bytes())
    set_before = SET.read_bytes()
    expected_names = {
        "draft.md",
        "draft.md.conflict-prime-disp-01",
        "draft.md.conflict-prime-disp-02",
        "draft.md.conflict-prime-intent-01",
        "draft.md.conflict-prime-item-01",
        "draft.md.conflict-prime-item-02",
        "record.json",
    }
    suite.add("preview names", set(preview_before) == expected_names, " ".join(sorted(preview_before)))
    temps: list[Path] = []
    try:
        author = load_module("pack_author_v2_under_test", ROOT / "labs" / "pack-authoring-pass02" / "pack_author.py")
        door = load_module("authoring_tools_v2_under_test", ROOT / "app" / "authoring_tools_v2.py")
        suite.add("import wrote no preview change", snapshot(PREVIEW) == preview_before, "preview")
        dispatcher(suite)
        pins(suite)
        junction(suite, door)
        interrupt(suite, author)
        reserve_race(suite, author, temps)
        typed(suite, temps)
        happy(suite, temps, run_dir)
        fixture(suite, temps)
        dependencies(suite, temps)
        boundaries(suite)
    except Exception:
        suite.add("suite crashed", False, traceback.format_exc())
    finally:
        for temp in temps:
            shutil.rmtree(temp, ignore_errors=True)
        suite.add("preview bytes unchanged", snapshot(PREVIEW) == preview_before, "changed")
        suite.add("pack page unchanged", digest(PAGE.read_bytes()) == page_before, page_before)
        suite.add("code-root set unchanged", SET.read_bytes() == set_before, "set")
        summary = {
            "schema": "authoring-entry-run/1",
            "pack": "0526.dev-authoring/05.03",
            "stamp": stamp,
            "cases": len(suite.cases),
            "failed": sum(1 for case in suite.cases if not case["ok"]),
            "first_failure": suite.first,
            "preview": preview_before,
        }
        (run_dir / "summary.json").write_bytes(json.dumps(summary, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
        (run_dir / "cases.json").write_bytes(json.dumps(suite.cases, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
        print(f"run {run_dir}")
        print(f"failed {summary['failed']}")
    return 0 if suite.first is None else 1


if __name__ == "__main__":
    sys.exit(main())

