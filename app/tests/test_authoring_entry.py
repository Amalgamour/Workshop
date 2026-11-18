#!/usr/bin/env python3
"""Focused authoring entry checks for 0526.dev-authoring/05.01.

Importing this file writes nothing. The suite runs only as __main__.
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
import threading
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LIB = ROOT / "app" / "librarian.py"
LIVE_PAGE = ROOT / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "05.01.md"
LIVE_SLOT = ROOT / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "evidence" / "authoring05.02"
REL = [
    "00.kernel/00.00.10.work/0423.dev-authoring/01.md",
    "00.kernel/00.00.10.work/0423.dev-authoring/06.01.md",
    "00.kernel/00.00.10.work/0423.dev-authoring/06.02.md",
    "00.kernel/00.00.10.work/0423.dev-authoring/templates/build-pack-v1.draft.md",
    "00.kernel/00.00.10.work/0526.dev-authoring/01.md",
]
NOTE_A = "00.kernel/00.00.10.work/0423.dev-authoring/06.01.md"
NOTE_B = "00.kernel/00.00.10.work/0423.dev-authoring/06.02.md"
ZEROS = "0" * 64
ONES = "1" * 64


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


def seed_live_profile(book: Path, occupant: bool) -> None:
    for rel in REL:
        dest = book / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((ROOT / rel).read_bytes())
    if occupant:
        (book / "00.kernel" / "00.00.10.work" / "0126.boot-members-0509").mkdir()


def intent() -> dict:
    return {
        "goal": "Synthetic disposable authoring check",
        "scope": {
            "included": "two items and a prepared page in this disposable book",
            "excluded": "release, return filing, and the live checkout",
            "allowed_writes": "this disposable book only",
        },
        "finish": "Freeze writes the reviewed draft bytes",
        "executor": "Grok-1",
        "reviewer": "Codex Prime",
    }


def item(title: str, note: str) -> dict:
    return {
        "title": title,
        "purpose": "Supplied test meaning. The tool assigns the number.",
        "requirements": ["The caller does not send a pass, a path, or a hash."],
        "interfaces": ["authoring add-item"],
        "acceptance": ["Inspect shows this title in the draft."],
        "note_refs": [note],
        "open_choices": [],
        "dependency_refs": [],
    }


class Suite:
    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir
        self.cases: list[dict] = []
        self.first: dict | None = None

    def add(self, name: str, ok: bool, detail: str) -> None:
        row = {"name": name, "ok": ok, "detail": detail}
        self.cases.append(row)
        if not ok and self.first is None:
            self.first = row
        print(("PASS " if ok else "FAIL ") + name)
        if not ok:
            print(detail[:1200])

    def expect(self, name: str, result: subprocess.CompletedProcess, code: int, text: str = "") -> dict | None:
        err = result.stderr.decode("utf-8", "replace")
        out = result.stdout.decode("utf-8", "replace")
        ok = result.returncode == code and (text in err if code else True)
        if code != 0:
            ok = ok and out == ""
        detail = f"exit {result.returncode} expected {code}\n{err}\n{out[:500]}"
        self.add(name, ok, detail)
        if result.returncode == 0 and out.strip().startswith("{"):
            return json.loads(out)
        return None


def is_junction(path: Path) -> bool:
    if not path.exists() and not path.is_symlink():
        try:
            os.lstat(path)
        except OSError:
            return False
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return bool(getattr(info, "st_file_attributes", 0) & 0x400)


def remove_junction(path: Path) -> None:
    if is_junction(path):
        os.rmdir(path)


def main() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = (
        ROOT
        / "00.kernel"
        / "00.00.10.work"
        / "0526.dev-authoring"
        / "evidence"
        / "build05.01"
        / "runs"
        / stamp
    )
    run_dir.mkdir(parents=True)
    suite = Suite(run_dir)
    live_before = hashlib.sha256(LIVE_PAGE.read_bytes()).hexdigest()
    suite.add("live slot absent before", not LIVE_SLOT.exists(), str(LIVE_SLOT.exists()))
    author = load_module("pack_author_under_test", ROOT / "labs" / "pack-authoring-pass01" / "pack_author.py")
    door = load_module("authoring_tools_under_test", ROOT / "app" / "authoring_tools.py")
    suite.add("import wrote no live slot", not LIVE_SLOT.exists(), str(LIVE_SLOT.exists()))
    temps: list[Path] = []
    try:
        dispatcher(suite)
        pins(suite)
        junction(suite, door)
        interrupt(suite, author)
        reserve_race(suite, author, temps)
        happy(suite, temps, run_dir)
        collision(suite, temps)
        drift(suite, temps)
        typed(suite, temps)
        fixture(suite, temps)
        start_race(suite, author, temps)
        live_freeze(suite)
    finally:
        for temp in temps:
            shutil.rmtree(temp, ignore_errors=True)
        suite.add("live page unchanged", hashlib.sha256(LIVE_PAGE.read_bytes()).hexdigest() == live_before, live_before)
        suite.add("live slot absent after", not LIVE_SLOT.exists(), str(LIVE_SLOT.exists()))
        summary = {
            "schema": "authoring-entry-run/1",
            "stamp": stamp,
            "cases": len(suite.cases),
            "failed": sum(1 for case in suite.cases if not case["ok"]),
            "first_failure": suite.first,
            "live_page_sha256": live_before,
        }
        (run_dir / "summary.json").write_bytes(json.dumps(summary, indent=2).encode("utf-8") + b"\n")
        (run_dir / "cases.json").write_bytes(json.dumps(suite.cases, indent=2).encode("utf-8") + b"\n")
        print(f"run {run_dir}")
        print(f"failed {summary['failed']}")
    return 0 if suite.first is None else 1


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
        match = hashlib.sha256(raw).hexdigest() == spec["sha256"] and len(raw) == spec["bytes"]
        ok = ok and match
        if not match:
            detail.append(name)
    text = (ROOT / "app" / "librarian.py").read_text(encoding="utf-8")
    ok = ok and "review_loop_tools_v4.py" in text and "librarian_review_loop_tools_v4" in text
    ok = ok and "authoring_tools.py" in text and "librarian_authoring_tools" in text
    suite.add("review-loop v4 pins unchanged", ok, ",".join(detail) or "matched")


def junction(suite: Suite, door) -> None:
    base = Path(tempfile.mkdtemp(prefix="author-junction-"))
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
                    ["start", "--book", str(alias / "book"), "--profile", "0423-to-0526", "--operation", "junction-1"],
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
        cli = run_app(
            ["authoring", "start", "--book", str(alias / "book"), "--profile", "0423-to-0526", "--operation", "junction-1"]
        )
        err = cli.stderr.decode("utf-8", "replace")
        suite.add(
            "ancestor junction cli",
            cli.returncode == 2 and cli.stdout == b"" and "book root ancestor is linked and was not followed" in err,
            err,
        )
        checkout_alias = base / "checkout-alias"
        made_checkout = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(checkout_alias), str(ROOT)], capture_output=True
        )
        suite.add("checkout junction created", made_checkout.returncode == 0 and is_junction(checkout_alias), "created")
        checkout_cli = run_app(
            [
                "authoring",
                "start",
                "--book",
                str(checkout_alias / "labs"),
                "--profile",
                "0423-to-0526",
                "--operation",
                "junction-checkout",
            ]
        )
        checkout_err = checkout_cli.stderr.decode("utf-8", "replace")
        suite.add(
            "checkout alias ancestor refused",
            checkout_cli.returncode == 2
            and checkout_cli.stdout == b""
            and "ancestor is linked" in checkout_err
            and not LIVE_SLOT.exists(),
            checkout_err,
        )
        direct = base / "direct-book"
        subprocess.run(["cmd", "/c", "mklink", "/J", str(direct), str(target)], capture_output=True)
        direct_cli = run_app(
            ["authoring", "inspect", "--book", str(direct), "--profile", "0423-to-0526"]
        )
        direct_err = direct_cli.stderr.decode("utf-8", "replace")
        suite.add(
            "direct junction refused",
            direct_cli.returncode == 2 and "book root is not a directory" in direct_err and direct_cli.stdout == b"",
            direct_err,
        )
        link_file = base / "file-link"
        source_file = base / "file.txt"
        source_file.write_text("x", encoding="utf-8")
        try:
            os.symlink(source_file, link_file)
            suite.add("file symlink skip", False, "created; this host allowed a file symlink")
        except OSError as exc:
            suite.add(
                "file symlink skip",
                getattr(exc, "winerror", None) == 1314,
                f"WinError {getattr(exc, 'winerror', None)}",
            )
    finally:
        for name in ("alias", "checkout-alias", "direct-book"):
            remove_junction(base / name)
        shutil.rmtree(base, ignore_errors=True)


def interrupt(suite: Suite, author) -> None:
    base = Path(tempfile.mkdtemp(prefix="author-interrupt-"))
    try:
        record = base / "record.json"
        original = b'{"schema":"authoring-record/1","marker":"previous"}\n'
        record.write_bytes(original)

        def boom(src, dst):
            raise OSError(5, "injected")

        try:
            author.commit_record(record, {"schema": "authoring-record/1", "marker": "next"}, "op-interrupt", replace=boom)
            suite.add("interrupted replace", False, "replace returned")
        except author.Partial as exc:
            partial = base / "record.json.partial-op-interrupt"
            suite.add(
                "interrupted replace",
                record.read_bytes() == original and partial.is_file() and b"next" in partial.read_bytes(),
                str(exc),
            )
    finally:
        shutil.rmtree(base, ignore_errors=True)


def reserve_race(suite: Suite, author, temps: list[Path]) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-reserve-"))
    temps.append(book)
    work = book / "work"
    work.mkdir()
    found: list[str] = []
    errors: list[str] = []

    def once() -> None:
        try:
            name, _slot = author.reserve_pass(work)
            found.append(name)
        except Exception as exc:
            errors.append(str(exc))

    threads = [threading.Thread(target=once) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    suite.add(
        "two reserves differ",
        not errors and sorted(found) == ["05.01", "05.02"],
        f"{found} {errors}",
    )


def happy(suite: Suite, temps: list[Path], run_dir: Path) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-happy-"))
    temps.append(book)
    seed_live_profile(book, occupant=True)
    folder = book / "inputs"
    folder.mkdir()
    write_json(folder / "intent.json", intent())
    write_json(folder / "item1.json", item("Derive the form", NOTE_A))
    write_json(
        folder / "item1-conflict.json",
        item("Different meaning under the same operation", NOTE_A),
    )
    write_json(folder / "item2.json", item("Preserve \u6587 and \u0394", NOTE_B))
    write_json(folder / "bad-type.json", {"title": 12, "tests_passed": True})
    write_json(
        folder / "note.json",
        {
            "text": "Supplied test note with \u0394",
            "attribution": "test",
            "source": "disposable input",
            "mark": "recorded-decision",
        },
    )
    write_json(
        folder / "disp-a.json",
        {"disposition": "integrated", "item": "01"},
    )
    write_json(
        folder / "disp-b.json",
        {"disposition": "deferred", "why": "Supplied test: the second note stays deferred."},
    )
    write_json(
        folder / "review.json",
        {
            "assessment": "Supplied test review of these exact draft bytes.",
            "unresolved_issues": "Return custody stays blocked.",
            "stop_conditions": "Do not treat this page as a release.",
        },
    )
    (folder / "malformed.json").write_bytes(b"{")

    def call(name: str, args: list[str], code: int = 0, text: str = "") -> dict | None:
        return suite.expect(name, run_app(["authoring", *args, "--json"] if "--json" not in args else ["authoring", *args]), code, text)

    common = ["--book", str(book), "--profile", "0423-to-0526"]
    started = call(
        "first pass start",
        ["start", *common, "--operation", "start-1", "--input", str(folder / "intent.json"), "--json"],
    )
    if not started:
        return
    suite.add("pass is 05.01", started["pass"] == "05.01", started["pass"])
    suite.add(
        "return occupied",
        started["return_intent"]["status"] == "occupied"
        and started["return_intent"]["occupants"] == ["0126.boot-members-0509"]
        and started["return_intent"]["readiness"] == "blocked",
        json.dumps(started["return_intent"]),
    )
    suite.add(
        "conditional and environment preserved",
        "labels conditional" in started["draft_text"] and "environment" in started["draft_text"] and "complete_claim: false" in started["draft_text"],
        "missing labels",
    )
    replay = call(
        "start replay",
        ["start", *common, "--operation", "start-1", "--input", str(folder / "intent.json"), "--json"],
    )
    suite.add("replay keeps pass", bool(replay) and replay["pass"] == "05.01", str(replay and replay["pass"]))
    call(
        "malformed input",
        ["add-item", *common, "--operation", "bad-json", "--input", str(folder / "malformed.json"), "--json"],
        2,
        "not strict json",
    )
    call(
        "typed field",
        ["add-item", *common, "--operation", "bad-type", "--input", str(folder / "bad-type.json"), "--json"],
        2,
        "tests_passed",
    )
    first = call(
        "add item 01",
        ["add-item", *common, "--operation", "item-1", "--input", str(folder / "item1.json"), "--json"],
    )
    suite.add("item 01 assigned", bool(first) and "## #01 - Derive the form" in first["draft_text"], "missing item")
    again = call(
        "item replay",
        ["add-item", *common, "--operation", "item-1", "--input", str(folder / "item1.json"), "--json"],
    )
    suite.add(
        "replay does not add item 02",
        bool(again) and "## #02" not in again["draft_text"] and "## #01 - Derive the form" in again["draft_text"],
        "item count changed",
    )
    call(
        "conflicting retry",
        ["add-item", *common, "--operation", "item-1", "--input", str(folder / "item1-conflict.json"), "--json"],
        2,
        "conflicting operation",
    )
    second = call(
        "add item 02",
        ["add-item", *common, "--operation", "item-2", "--input", str(folder / "item2.json"), "--json"],
    )
    suite.add(
        "utf-8 item",
        bool(second) and "\u6587" in second["draft_text"] and "\u0394" in second["draft_text"],
        "marks missing",
    )
    noted = call(
        "add note",
        ["add-note", *common, "--operation", "note-1", "--input", str(folder / "note.json"), "--json"],
    )
    suite.add(
        "note mark preserved",
        bool(noted) and "mark recorded-decision" in noted["draft_text"] and "d01" in noted["draft_text"],
        "note missing",
    )
    call(
        "freeze before disposition",
        ["freeze", *common, "--operation", "freeze-early", "--draft-sha256", ZEROS, "--json"],
        2,
        "unresolved",
    )
    call(
        "dispose 06.01",
        ["revise", *common, "--operation", "disp-1", "--target", "disposition", "--note", NOTE_A, "--input", str(folder / "disp-a.json"), "--json"],
    )
    call(
        "dispose 06.02",
        ["revise", *common, "--operation", "disp-2", "--target", "disposition", "--note", NOTE_B, "--input", str(folder / "disp-b.json"), "--json"],
    )
    write_json(folder / "disp-d.json", {"disposition": "rejected", "why": "Supplied test rejection."})
    call(
        "dispose draft note",
        ["revise", *common, "--operation", "disp-3", "--target", "disposition", "--note", "d01", "--input", str(folder / "disp-d.json"), "--json"],
    )
    inspected = call("inspect both items", ["inspect", *common, "--json"])
    suite.add(
        "inspect full document",
        bool(inspected)
        and "Derive the form" in inspected["draft_text"]
        and "Preserve \u6587 and \u0394" in inspected["draft_text"]
        and hashlib.sha256(inspected["draft_text"].encode("utf-8")).hexdigest() == inspected["draft_sha256"],
        "inspect mismatch",
    )
    call(
        "review wrong bytes",
        ["review", *common, "--operation", "review-bad", "--input", str(folder / "review.json"), "--draft-sha256", ONES, "--json"],
        2,
        "draft sha256 does not match",
    )
    reviewed = call(
        "review exact bytes",
        ["review", *common, "--operation", "review-1", "--input", str(folder / "review.json"), "--json"],
    )
    if not reviewed:
        return
    local = hashlib.sha256(reviewed["draft_text"].encode("utf-8")).hexdigest()
    suite.add("review binds draft", local == reviewed["draft_sha256"] and "review: present" in reviewed["draft_text"], local)
    frozen = call(
        "freeze prepared page",
        ["freeze", *common, "--operation", "freeze-1", "--draft-sha256", reviewed["draft_sha256"], "--json"],
    )
    if not frozen:
        return
    page = book / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "05.01.md"
    suite.add(
        "page matches reviewed bytes",
        page.is_file() and page.read_bytes() == reviewed["draft_text"].encode("utf-8") and frozen["state"] == "frozen",
        f"state {frozen.get('state')}",
    )
    suite.add(
        "return directory not created",
        not (book / "00.kernel" / "00.00.10.work" / "0126.dev-authoring").exists(),
        "created",
    )
    (run_dir / "happy-draft.md").write_bytes(page.read_bytes())
    call(
        "freeze replay",
        ["freeze", *common, "--operation", "freeze-1", "--draft-sha256", reviewed["draft_sha256"], "--json"],
    )


def collision(suite: Suite, temps: list[Path]) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-collision-"))
    temps.append(book)
    seed_live_profile(book, occupant=False)
    page = book / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "05.01.md"
    page.write_bytes(b"occupied page\n")
    folder = book / "intent.json"
    write_json(folder, intent())
    result = run_app(
        [
            "authoring",
            "start",
            "--book",
            str(book),
            "--profile",
            "0423-to-0526",
            "--operation",
            "collision-1",
            "--input",
            str(folder),
            "--json",
        ]
    )
    body = suite.expect("collision reserves 05.02", result, 0)
    suite.add(
        "occupied page preserved",
        bool(body) and body["pass"] == "05.02" and page.read_bytes() == b"occupied page\n",
        str(body and body["pass"]),
    )


def drift(suite: Suite, temps: list[Path]) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-drift-"))
    temps.append(book)
    seed_live_profile(book, occupant=False)
    folder = book / "in"
    folder.mkdir()
    write_json(folder / "intent.json", intent())
    write_json(folder / "item.json", item("Drift item", NOTE_A))
    write_json(folder / "disp.json", {"disposition": "integrated", "item": "01"})
    write_json(folder / "disp2.json", {"disposition": "deferred", "why": "Not part of this drift check."})
    write_json(
        folder / "review.json",
        {
            "assessment": "Review before the source changes.",
            "unresolved_issues": "none in this check",
            "stop_conditions": "stop on drift",
        },
    )
    common = ["authoring", "--book", str(book), "--profile", "0423-to-0526"]

    def call(args: list[str]) -> subprocess.CompletedProcess:
        return run_app([*common[:1], args[0], *common[1:], *args[1:]])

    call(["start", "--operation", "d-start", "--input", str(folder / "intent.json"), "--json"])
    call(["add-item", "--operation", "d-item", "--input", str(folder / "item.json"), "--json"])
    call(["revise", "--operation", "d-a", "--target", "disposition", "--note", NOTE_A, "--input", str(folder / "disp.json"), "--json"])
    call(["revise", "--operation", "d-b", "--target", "disposition", "--note", NOTE_B, "--input", str(folder / "disp2.json"), "--json"])
    reviewed = call(["review", "--operation", "d-review", "--input", str(folder / "review.json"), "--json"])
    body = json.loads(reviewed.stdout.decode("utf-8")) if reviewed.returncode == 0 else None
    source = book / REL[0]
    source.write_bytes(source.read_bytes() + b"\n")
    inspected = call(["inspect", "--json"])
    live = json.loads(inspected.stdout.decode("utf-8")) if inspected.returncode == 0 else {}
    suite.add(
        "inspect shows source drift",
        bool(live.get("live", {}).get("source_drift")) and live.get("review_valid") is False,
        json.dumps(live.get("live", {}))[:500],
    )
    refused = call(["freeze", "--operation", "d-freeze", "--draft-sha256", body["draft_sha256"] if body else ZEROS, "--json"])
    err = refused.stderr.decode("utf-8", "replace")
    suite.add("source drift refuses freeze", refused.returncode == 2 and refused.stdout == b"" and "source-drift" in err, err)


def typed(suite: Suite, temps: list[Path]) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-typed-"))
    temps.append(book)
    seed_live_profile(book, occupant=False)
    bad = book / "bad.json"
    bad.write_bytes(b'{"title": ["nope"]}\n')
    result = run_app(
        ["authoring", "start", "--book", str(book), "--profile", "0423-to-0526", "--operation", "typed-start", "--input", str(bad), "--json"]
    )
    err = result.stderr.decode("utf-8", "replace")
    work = book / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "evidence"
    suite.add(
        "typed start reserves nothing",
        result.returncode == 2 and result.stdout == b"" and "title" in err and not work.exists(),
        err,
    )


def fixture(suite: Suite, temps: list[Path]) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-fixture-"))
    temps.append(book)
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
    (dep / "set.json").write_bytes((ROOT / "labs" / "app-dependencies-pass02" / "set.json").read_bytes())
    folder = book / "in"
    folder.mkdir()
    write_json(folder / "intent.json", intent())
    started = run_app(
        [
            "authoring",
            "start",
            "--book",
            str(book),
            "--profile",
            "fixture-authoring",
            "--operation",
            "f-start",
            "--input",
            str(folder / "intent.json"),
            "--json",
        ]
    )
    body = suite.expect("fixture start", started, 0)
    suite.add(
        "raw source stays raw",
        bool(body) and "utf8 false" in body["draft_text"] and body["return_intent"]["status"] == "unfiled",
        "raw or return",
    )
    (dep / "set.json").write_bytes((dep / "set.json").read_bytes() + b"\n")
    inspected = run_app(["authoring", "inspect", "--book", str(book), "--profile", "fixture-authoring", "--json"])
    live = json.loads(inspected.stdout.decode("utf-8")) if inspected.returncode == 0 else {}
    suite.add("stale set visible", bool(live.get("live", {}).get("set_drift")), "no drift")
    refused = run_app(
        [
            "authoring",
            "freeze",
            "--book",
            str(book),
            "--profile",
            "fixture-authoring",
            "--operation",
            "f-freeze",
            "--draft-sha256",
            ZEROS,
            "--json",
        ]
    )
    err = refused.stderr.decode("utf-8", "replace")
    suite.add("stale set refuses freeze", refused.returncode == 2 and "stale dependency set" in err, err)
    missing_book = Path(tempfile.mkdtemp(prefix="author-missing-"))
    temps.append(missing_book)
    seed_live_profile(missing_book, occupant=False)
    write_json(missing_book / "intent.json", intent())
    missing_item = item("Missing dependency", NOTE_A)
    missing_item["dependency_refs"] = [{"repository": "lib-build", "path": "labs/not-a-declared-module.py"}]
    write_json(missing_book / "item.json", missing_item)
    write_json(missing_book / "disp.json", {"disposition": "integrated", "item": "01"})
    write_json(missing_book / "disp2.json", {"disposition": "deferred", "why": "The other note is deferred."})
    common = ["authoring", "--book", str(missing_book), "--profile", "0423-to-0526"]
    run_app([*common[:1], "start", *common[1:], "--operation", "m-start", "--input", str(missing_book / "intent.json"), "--json"])
    added = run_app([*common[:1], "add-item", *common[1:], "--operation", "m-item", "--input", str(missing_book / "item.json"), "--json"])
    added_body = json.loads(added.stdout.decode("utf-8")) if added.returncode == 0 else {}
    suite.add("missing dependency labelled", "labels missing" in added_body.get("draft_text", ""), "label")
    run_app(
        [
            *common[:1],
            "revise",
            *common[1:],
            "--operation",
            "m-a",
            "--target",
            "disposition",
            "--note",
            NOTE_A,
            "--input",
            str(missing_book / "disp.json"),
            "--json",
        ]
    )
    run_app(
        [
            *common[:1],
            "revise",
            *common[1:],
            "--operation",
            "m-b",
            "--target",
            "disposition",
            "--note",
            NOTE_B,
            "--input",
            str(missing_book / "disp2.json"),
            "--json",
        ]
    )
    write_json(
        missing_book / "review.json",
        {"assessment": "Review with a missing ref.", "unresolved_issues": "missing", "stop_conditions": "stop"},
    )
    reviewed = run_app(
        [*common[:1], "review", *common[1:], "--operation", "m-review", "--input", str(missing_book / "review.json"), "--json"]
    )
    reviewed_body = json.loads(reviewed.stdout.decode("utf-8")) if reviewed.returncode == 0 else {}
    refused_missing = run_app(
        [
            *common[:1],
            "freeze",
            *common[1:],
            "--operation",
            "m-freeze",
            "--draft-sha256",
            reviewed_body.get("draft_sha256", ZEROS),
            "--json",
        ]
    )
    missing_err = refused_missing.stderr.decode("utf-8", "replace")
    suite.add("missing dependency refuses freeze", refused_missing.returncode == 2 and "missing" in missing_err, missing_err)
    stale_item = item("Stale claim", NOTE_A)
    stale_item["dependency_refs"] = [
        {"repository": "lib-build", "path": "app/librarian.py", "claimed_sha256": ZEROS}
    ]
    stale_book = Path(tempfile.mkdtemp(prefix="author-stale-"))
    temps.append(stale_book)
    seed_live_profile(stale_book, occupant=False)
    write_json(stale_book / "intent.json", intent())
    write_json(stale_book / "item.json", stale_item)
    write_json(stale_book / "disp.json", {"disposition": "integrated", "item": "01"})
    write_json(stale_book / "disp2.json", {"disposition": "deferred", "why": "Deferred for the stale check."})
    write_json(
        stale_book / "review.json",
        {"assessment": "Review with a stale claim.", "unresolved_issues": "stale", "stop_conditions": "stop"},
    )
    common = ["authoring", "--book", str(stale_book), "--profile", "0423-to-0526"]
    run_app([*common[:1], "start", *common[1:], "--operation", "s-start", "--input", str(stale_book / "intent.json"), "--json"])
    added = run_app([*common[:1], "add-item", *common[1:], "--operation", "s-item", "--input", str(stale_book / "item.json"), "--json"])
    added_body = json.loads(added.stdout.decode("utf-8")) if added.returncode == 0 else {}
    suite.add("stale claim labelled", "stale" in added_body.get("draft_text", ""), added_body.get("draft_text", "")[-400:])
    run_app(
        [*common[:1], "revise", *common[1:], "--operation", "s-a", "--target", "disposition", "--note", NOTE_A, "--input", str(stale_book / "disp.json"), "--json"]
    )
    run_app(
        [*common[:1], "revise", *common[1:], "--operation", "s-b", "--target", "disposition", "--note", NOTE_B, "--input", str(stale_book / "disp2.json"), "--json"]
    )
    reviewed = run_app(
        [*common[:1], "review", *common[1:], "--operation", "s-review", "--input", str(stale_book / "review.json"), "--json"]
    )
    reviewed_body = json.loads(reviewed.stdout.decode("utf-8")) if reviewed.returncode == 0 else {}
    refused_stale = run_app(
        [
            *common[:1],
            "freeze",
            *common[1:],
            "--operation",
            "s-freeze",
            "--draft-sha256",
            reviewed_body.get("draft_sha256", ZEROS),
            "--json",
        ]
    )
    stale_err = refused_stale.stderr.decode("utf-8", "replace")
    suite.add("stale claim refuses freeze", refused_stale.returncode == 2 and "stale" in stale_err, stale_err)


def start_race(suite: Suite, author, temps: list[Path]) -> None:
    book = Path(tempfile.mkdtemp(prefix="author-race-"))
    temps.append(book)
    seed_live_profile(book, occupant=False)
    intent_path = book / "intent.json"
    write_json(intent_path, intent())
    codes: list[int] = []
    messages: list[str] = []

    def once(op: str) -> None:
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = author.perform(
                    [
                        "start",
                        "--book",
                        str(book),
                        "--profile",
                        "0423-to-0526",
                        "--operation",
                        op,
                        "--input",
                        str(intent_path),
                        "--json",
                    ],
                    ROOT,
                )
            codes.append(code)
        except author.Refuse as exc:
            codes.append(2)
            messages.append(str(exc))

    threads = [threading.Thread(target=once, args=(f"race-{index}",)) for index in (1, 2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    records = list((book / "00.kernel" / "00.00.10.work" / "0526.dev-authoring" / "evidence").glob("authoring05.*/record.json"))
    suite.add(
        "two starts one session",
        sorted(codes) == [0, 2] and len(records) == 1 and any("open session" in message for message in messages),
        f"codes {codes} records {len(records)} {messages}",
    )


def live_freeze(suite: Suite) -> None:
    result = run_app(
        [
            "authoring",
            "freeze",
            "--book",
            str(ROOT),
            "--profile",
            "0423-to-0526",
            "--operation",
            "live-freeze",
            "--draft-sha256",
            ZEROS,
        ]
    )
    err = result.stderr.decode("utf-8", "replace")
    suite.add(
        "live freeze refused",
        result.returncode == 2
        and result.stdout == b""
        and "freeze on the live checkout is outside this slice" in err
        and not LIVE_SLOT.exists(),
        err,
    )


if __name__ == "__main__":
    sys.exit(main())
