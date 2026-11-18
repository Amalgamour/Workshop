#!/usr/bin/env python3
"""Focused cases for the read-only return-route readiness tool.

The suite retains fixture trees under D:\\librarian\\temp\\0521-0510.
It does not select the app, write a layout, or revise the contract.
inspect(..., read_bytes=...) is used only as a marked unit fault injection.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
BOOK_LIVE = REPO / "00.kernel" / "00.00.10.work"
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
TOOL = REPO / "labs" / "return-readiness-pass01" / "readiness.py"
CONTRACTS_PATH = REPO / "labs" / "return-readiness-pass01" / "contracts.json"
MANIFEST_PATH = REPO / "00.kernel" / "00.00.10.work" / "0521.return-placement" / "evidence" / "pack05.10" / "source-manifest.json"
PACK_PATH = REPO / "00.kernel" / "00.00.10.work" / "0521.return-placement" / "05.10.md"
LIVE_LIB = REPO / "app" / "librarian.py"
CLAIM_TIME_SHA = "e2d85b1b641d8a1113b0afaa67a9b8203eb58e9f1028308be922a806fffa5f90"
CLAIM_TIME_BYTES = 12204
BASELINE_SHA = ""
BASELINE_BYTES = 0
DOOR_PAGE_SHA = "c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d"
DOOR_PAGE_BYTES = 10206
PACK_SHA = "67067baa88dd0fa9e6c9245125ba8766ac4a2ce30ae9e6334cf1b27ffc981c10"
PACK_BYTES = 7379
MANIFEST_SHA = "fb437e679e32bf3567b9cdce841255aed3b24ac2b1156d30ca6d0619bd3400cc"
MANIFEST_BYTES = 9597
ADAPTER_SHA = "501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5"
ADAPTER_BYTES = 26561
OLD_RL = b'parent / "return_line_tools_v2.py"'
NEW_RL = b'parent / "return_line_tools_v3.py"'
OLD_HO = b'parent / "handoff_tools.py"'
NEW_HO = b'parent / "handoff_tools_v2.py"'
COMMANDS = ("return-lines", "capture-return")
ENV = os.environ.copy()
ENV["PYTHONDONTWRITEBYTECODE"] = "1"

STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
SUITE = Path(r"D:\librarian\temp\0521-0510") / f"{STAMP}-suite"


class Fail(Exception):
    pass


class Skip(Exception):
    pass


CLAIMS: list[dict] = []
NOTES: list[dict] = []
INDEX: list[dict] = []
CURRENT = ""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)


def dump_json(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def under_suite(path: Path) -> None:
    full = os.path.normcase(os.path.abspath(str(path)))
    root = os.path.normcase(os.path.abspath(str(SUITE)))
    if os.path.commonpath([full, root]) != root:
        raise RuntimeError(f"refusing a path outside the suite root: {path}")


def check(cond: bool, detail: str) -> None:
    if not cond:
        raise Fail(detail)


def load_tool():
    spec = importlib.util.spec_from_file_location("return_readiness_pass01", TOOL)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load readiness.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snap(root: Path) -> tuple[dict[str, str], list[str]]:
    files: dict[str, str] = {}
    dirs: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")
        if rel_dir != ".":
            dirs.append(rel_dir)
        for name in filenames:
            rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            files[rel] = sha(read_bytes(Path(dirpath) / name))
    return files, sorted(dirs)


def guard_repo() -> None:
    data = read_bytes(LIVE_LIB)
    check(sha(data) == BASELINE_SHA and len(data) == BASELINE_BYTES, "shared dispatcher bytes changed during the suite")
    check(not os.path.lexists(BOOK_LIVE / "return-line-layout.json"), "live layout appeared")
    check(sha(read_bytes(PACK_PATH)) == PACK_SHA and PACK_PATH.stat().st_size == PACK_BYTES, "pack page changed during the suite")


def assert_quiet(body: dict) -> None:
    check(body["schema"] == "return-route-readiness/1", "schema")
    check(body["authorization"] is False, "authorization")
    check(body["selection_is_authorization"] is False, "selection_is_authorization")
    check(body["authority"] == "not-assessed", "authority")
    check(body["app_selection_applied"] is False, "app_selection_applied")
    check(body["migration_assessed"] is False, "migration_assessed")
    check(body["approval"] == "not-established", "approval")
    check(body["completion"] == "not-established", "completion")
    check(body["task_association"] == "not-established", "task_association")
    check(body["recognizer"] == "static-ast-pattern", "recognizer")
    check(body["warnings"] == list(TOOL_MOD.WARNINGS), f"warnings {body['warnings']}")
    check(body["provenance"] == list(TOOL_MOD.PROVENANCE), "provenance")
    check(body["next_checks"] == list(TOOL_MOD.NEXT_CHECKS), "next_checks")
    check(body["limits"] == list(TOOL_MOD.LIMITS), "limits")
    check("app_selected" in body["historical_status_note"], "historical note")
    check(set(body["routes"]) == set(COMMANDS), f"routes {set(body['routes'])}")
    for line in body["next_checks"]:
        check("python" not in line and not line.startswith("--"), f"next check looks executable: {line}")
    joined = json.dumps(body["reads"])
    check("review_loop" not in joined and "review-loop" not in joined, "a review-loop path was read")


def save_obs(name: str, body: dict) -> None:
    path = SUITE / "observations" / f"{name}.json"
    under_suite(path)
    write_bytes(path, TOOL_MOD.dump(body).encode("utf-8"))


def observe(name: str, code: Path, book: Path, read_bytes_fn=None) -> dict:
    under_suite(code)
    under_suite(book)
    before_code = snap(code)
    before_book = snap(book)
    kwargs = {"code_text": str(code), "book_text": str(book)}
    if read_bytes_fn is not None:
        kwargs["read_bytes"] = read_bytes_fn
    body = TOOL_MOD.inspect(code, book, **kwargs)
    check(snap(code) == before_code, f"{name} code tree changed")
    check(snap(book) == before_book, f"{name} book tree changed")
    guard_repo()
    assert_quiet(body)
    save_obs(name, body)
    INDEX.append({"book": str(book), "case": name, "code": str(code), "mode": "inspect"})
    NOTES.append({"case": name, "kind": "inspect", "mode": "in-process" if read_bytes_fn is None else "unit-fault-injection"})
    return body


def run_cli(args: list[str]) -> subprocess.CompletedProcess:
    command = [str(PY), "-B", "labs/return-readiness-pass01/readiness.py", *args]
    proc = subprocess.run(command, cwd=REPO, env=ENV, capture_output=True, timeout=60)
    NOTES.append({
        "args": args,
        "bytes_stderr": len(proc.stderr),
        "bytes_stdout": len(proc.stdout),
        "exit": proc.returncode,
        "kind": "cli",
    })
    return proc


def copy_closure(code: Path) -> None:
    under_suite(code)
    for rel in CLOSURE:
        write_bytes(code.joinpath(*rel.split("/")), read_bytes(REPO / rel))


def write_dispatcher(code: Path, data: bytes) -> None:
    target = code / "app" / "librarian.py"
    under_suite(target)
    write_bytes(target, data)
    guard_repo()


def make_code(name: str, dispatcher: bytes) -> Path:
    code = SUITE / "cases" / name / "code"
    copy_closure(code)
    write_dispatcher(code, dispatcher)
    return code


def make_book(name: str) -> Path:
    book = SUITE / "cases" / name / "book"
    under_suite(book)
    book.mkdir(parents=True, exist_ok=True)
    return book


def both_new(data: bytes) -> bytes:
    check(data.count(OLD_RL) == 1, "return-lines substitution source is not unique")
    check(data.count(OLD_HO) == 1, "capture-return substitution source is not unique")
    out = data.replace(OLD_RL, NEW_RL, 1).replace(OLD_HO, NEW_HO, 1)
    check(out.count(NEW_RL) == 1 and OLD_RL not in out, "return-lines substitution result")
    check(out.count(NEW_HO) == 1 and OLD_HO not in out, "capture-return substitution result")
    return out


def one_new(data: bytes) -> bytes:
    check(data.count(OLD_RL) == 1 and data.count(OLD_HO) == 1, "one-route source counts")
    out = data.replace(OLD_RL, NEW_RL, 1)
    check(out.count(NEW_RL) == 1 and out.count(OLD_HO) == 1 and OLD_RL not in out, "one-route result")
    return out


def reads_for(selected: dict[str, str], plain: set[str] | None = None) -> set[str]:
    paths = {"app/librarian.py"}
    for command, selector in selected.items():
        sides = CONTRACTS["routes"][command]
        chosen = sides[selector]
        paths.add(chosen["facade"]["path"])
        paths.add(chosen["declaration"]["path"])
        for dep in chosen["dependencies"]:
            paths.add(dep["path"])
        paths.add(sides["new"]["facade"]["path"])
        paths.add(sides["new"]["declaration"]["path"])
        paths.add(sides["old"]["facade"]["path"])
    for command in plain or set():
        new = CONTRACTS["routes"][command]["new"]
        paths.add(new["facade"]["path"])
        paths.add(new["declaration"]["path"])
    return paths


def assert_reads(body: dict, code_paths: set[str], book_paths: set[str]) -> None:
    got = {(row["root"], row["path"]) for row in body["reads"]}
    expected = {("code", rel) for rel in code_paths} | {("book", rel) for rel in book_paths}
    check(got == expected, f"read set differs: {sorted(got ^ expected)}")


def assert_old_valid(body: dict, command: str) -> None:
    item = body["routes"][command]
    facade = CONTRACTS["routes"][command]["old"]["facade"]["path"]
    check(item["state"] == "selected-valid", f"{command} {item['state']}")
    check(item["selector"] == "old", f"{command} selector {item['selector']}")
    check(item["selected_facade"] == facade, f"{command} facade {item['selected_facade']}")
    check(item["mismatches"] == [], f"{command} mismatches {item['mismatches']}")
    check(item["facade_matches_contract"] is True, f"{command} facade pin")
    check(item["declaration_matches_contract"] is True, f"{command} declaration pin")
    check(item["dependencies"] and all(dep["matches_contract"] is True for dep in item["dependencies"]), f"{command} deps")
    check(item["successor_staged"] is True, f"{command} staged")
    check(item["successor_matches_contract"] is True, f"{command} successor pin")
    check(item["successor_path"] == CONTRACTS["routes"][command]["new"]["facade"]["path"], f"{command} successor path")
    check(item["predecessor_present"] is False, f"{command} predecessor flag")
    check(item["staged_notes"] == [], f"{command} staged notes {item['staged_notes']}")


def assert_new_valid(body: dict, command: str) -> None:
    item = body["routes"][command]
    facade = CONTRACTS["routes"][command]["new"]["facade"]["path"]
    check(item["state"] == "selected-valid", f"{command} {item['state']}")
    check(item["selector"] == "new", f"{command} selector")
    check(item["selected_facade"] == facade, f"{command} facade")
    check(item["mismatches"] == [], f"{command} mismatches {item['mismatches']}")
    check(item["facade_matches_contract"] is True and item["declaration_matches_contract"] is True, f"{command} pins")
    check(all(dep["matches_contract"] is True for dep in item["dependencies"]), f"{command} deps")
    check(item["successor_staged"] is False, f"{command} staged while selected")
    check(item["predecessor_present"] is True, f"{command} predecessor missing")
    check(item["predecessor_matches_contract"] is True, f"{command} predecessor pin")


def authority_lines() -> list[str]:
    return [
        "migration and release authority were not assessed",
        "no Director release is recorded by this tool",
    ]


def declare_layout(book: Path, data: bytes) -> None:
    write_bytes(book / "return-line-layout.json", data)


def declare_door(book: Path, page: bytes | None) -> None:
    door = book / "0100.band.returns"
    under_suite(door)
    door.mkdir()
    if page is not None:
        write_bytes(door / "01.md", page)


def run_case(cid: str, text: str, case: str, limit: str, fn) -> None:
    global CURRENT
    CURRENT = case
    try:
        fn()
    except Fail as exc:
        CLAIMS.append({"case": case, "claim": text, "detail": str(exc), "id": cid, "limit": limit, "result": "failed"})
        raise
    except Skip as exc:
        CLAIMS.append({
            "case": case,
            "claim": text,
            "detail": str(exc),
            "id": cid,
            "limit": limit,
            "result": "skipped-environment",
        })
        print(f"skip {cid} {case} {exc}", flush=True)
        return
    CLAIMS.append({"case": case, "claim": text, "detail": "", "id": cid, "limit": limit, "result": "passed"})
    print(f"pass {cid} {case}", flush=True)


def case_source() -> None:
    source = read_bytes(TOOL).decode("utf-8")
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    allowed = {"__future__", "ast", "hashlib", "json", "os", "pathlib", "stat", "sys"}
    check(imported <= allowed, f"imports {sorted(imported - allowed)}")
    for banned in ("subprocess", "importlib", "socket", "review_loop"):
        check(banned not in source, f"tool source contains {banned}")
    check("read_bytes" in source, "fault seam missing")
    for flag in ("--force", "--allow-live", "--reader", "--inject", "--read-bytes"):
        check(flag not in source, f"public flag {flag}")


def case_pins() -> None:
    manifest = json.loads(read_bytes(MANIFEST_PATH).decode("utf-8"))
    check(manifest["schema"] == "prime-pack-inputs/1", "manifest schema")
    check(sha(read_bytes(MANIFEST_PATH)) == MANIFEST_SHA and len(read_bytes(MANIFEST_PATH)) == MANIFEST_BYTES, "manifest hash")
    rows = {}
    mismatches = []
    for row in manifest["files"]:
        live = read_bytes(REPO / row["path"])
        snap_bytes = read_bytes(REPO / row["snapshot"])
        if sha(live) != row["sha256"] or len(live) != row["bytes"] or live != snap_bytes:
            mismatches.append(row["path"])
        rows[row["path"]] = row
    check(mismatches == [], f"pin mismatches {mismatches}")
    check(len(rows) == 29, f"manifest count {len(rows)}")
    adapter = "labs/return-access-pass01/return_access.py"
    check(adapter not in rows, "adapter unexpectedly became a manifest row")
    declaration = json.loads(read_bytes(REPO / "app" / "return-lines-v2.json").decode("utf-8"))
    check(declaration["adapter"]["sha256"] == ADAPTER_SHA and declaration["adapter"]["bytes"] == ADAPTER_BYTES, "adapter declaration")
    adapter_bytes = read_bytes(REPO / adapter)
    check(sha(adapter_bytes) == ADAPTER_SHA and len(adapter_bytes) == ADAPTER_BYTES, "adapter disk")
    adapter_rows = [item for item in CONTRACTS["routes"]["return-lines"]["old"]["dependencies"] if item["role"] == "adapter"]
    check(len(adapter_rows) == 1 and adapter_rows[0]["path"] == adapter, "adapter row")
    check(adapter_rows[0]["sha256"] == ADAPTER_SHA and adapter_rows[0]["bytes"] == ADAPTER_BYTES, "contract adapter")
    pred = CONTRACTS["predecessor_dispatcher"]
    pred_bytes = read_bytes(REPO / pred["path"])
    check(sha(pred_bytes) == pred["sha256"] and len(pred_bytes) == pred["bytes"], "predecessor snapshot")
    check(sha(pred_bytes) != BASELINE_SHA, "snapshot and live dispatcher unexpectedly match")
    sample = TOOL_MOD.canonical_layout(CONTRACTS["layout"]["known_book"])
    check(sha(sample) == CONTRACTS["layout"]["known_sha256"] and len(sample) == CONTRACTS["layout"]["known_bytes"], "layout identity")
    guard_repo()


def case_recognizer() -> None:
    parsed = TOOL_MOD.recognize(SNAPSHOT.decode("utf-8"))
    check(parsed["state"] == "parsed", parsed["state"])
    check(parsed["routes"]["return-lines"] == {"facade": "return_line_tools_v2.py", "state": "recognized"}, "old return-lines")
    check(parsed["routes"]["capture-return"] == {"facade": "handoff_tools.py", "state": "recognized"}, "old capture-return")
    activation = 'if not args or args[0] not in ("return-lines", "capture-return", "other"):\n    raise SystemExit(2)\n'
    activated = TOOL_MOD.recognize(activation)
    check(activated["routes"]["return-lines"]["state"] == "absent", "activation was treated as selection")
    check(activated["routes"]["capture-return"]["state"] == "absent", "activation capture")
    other = 'if command != "return-lines":\n    pass\n'
    other_parsed = TOOL_MOD.recognize(other)
    check(other_parsed["routes"]["return-lines"]["state"] == "unsupported", "other mention")
    orelse = (
        'if command == "return-lines":\n    pass\nelse:\n'
        '    door = load_module(Path(__file__).resolve().parent / "return_line_tools_v2.py", "x")\n'
    )
    check(TOOL_MOD.recognize(orelse)["routes"]["return-lines"]["state"] == "unsupported", "else load")
    doubled = (
        'if command == "return-lines":\n'
        '    door = load_module(Path(__file__).resolve().parent / "return_line_tools_v2.py", "a")\n'
        '    door = load_module(Path(__file__).resolve().parent / "return_line_tools_v3.py", "b")\n'
    )
    check(TOOL_MOD.recognize(doubled)["routes"]["return-lines"]["state"] == "unsupported", "two loads")
    keyword = (
        'if command == "return-lines":\n'
        '    door = load_module(Path(__file__).resolve().parent / "return_line_tools_v2.py", "a", extra=1)\n'
    )
    check(TOOL_MOD.recognize(keyword)["routes"]["return-lines"]["state"] == "unsupported", "keyword load")
    check(TOOL_MOD.recognize("def (\n")["state"] == "malformed", "syntax")


def case_old() -> None:
    body = observe("old-staged", OLD_CODE, OLD_BOOK)
    assert_old_valid(body, "return-lines")
    assert_old_valid(body, "capture-return")
    check(body["dispatcher"]["state"] == "measured", "dispatcher")
    check(body["dispatcher"]["matches_predecessor_snapshot"] is True, "snapshot match")
    check(body["dispatcher"]["whole_file_hash_is_provenance"] is True, "provenance flag")
    check(body["book_declaration"]["declared"] is False, "declared")
    check(body["book_declaration"]["door"]["state"] == "missing", "door")
    check(body["book_declaration"]["layout"]["state"] == "missing", "layout")
    check(body["missing_prerequisites"][0] == "the book has no valid line-pass declaration", "prerequisite")
    assert_reads(body, reads_for({"return-lines": "old", "capture-return": "old"}), {"return-line-layout.json"})
    text = TOOL_MOD.project_text(body)
    check(text.startswith("\nreturn-route-readiness/1\n"), "projection")
    check("authorization: false\n" in text, "projection authority")
    check("return-lines: selected-valid old app/return_line_tools_v2.py\n" in text, "projection route")
    check("An unselected successor does not protect the app." in text, "projection warning")


def case_both_new() -> None:
    code = make_code("both-new", BOTH_NEW)
    book = make_book("both-new")
    body = observe("both-new", code, book)
    assert_new_valid(body, "return-lines")
    assert_new_valid(body, "capture-return")
    check(body["dispatcher"]["matches_predecessor_snapshot"] is False, "hash was used as a pin")
    check(body["dispatcher"]["sha256"] != body["dispatcher"]["predecessor_sha256"], "dispatcher identity")
    check(body["book_declaration"]["declared"] is False, "selection declared the book")
    check("the reviewed successor is not selected on both routes" not in body["missing_prerequisites"], "successor prerequisite")
    check(body["missing_prerequisites"][0] == "the book has no valid line-pass declaration", "declaration prerequisite")
    assert_reads(body, reads_for({"return-lines": "new", "capture-return": "new"}), {"return-line-layout.json"})


def case_one() -> None:
    code = make_code("one-route", ONE_NEW)
    book = make_book("one-route")
    body = observe("one-route", code, book)
    assert_new_valid(body, "return-lines")
    assert_old_valid(body, "capture-return")
    check("the reviewed successor is not selected on both routes" in body["missing_prerequisites"], "partial selection")


def case_missing_facade() -> None:
    code = make_code("missing-facade", SNAPSHOT)
    target = code / "app" / "return_line_tools_v2.py"
    under_suite(target)
    target.unlink()
    book = make_book("missing-facade")
    body = observe("missing-facade", code, book)
    item = body["routes"]["return-lines"]
    check(item["state"] == "selected-but-invalid", item["state"])
    check(item["selector"] == "old", item["selector"])
    check("facade missing" in item["mismatches"], str(item["mismatches"]))
    assert_old_valid(body, "capture-return")
    before_code = snap(code)
    before_book = snap(book)
    proc = run_cli(["--code-root", str(code), "--book", str(book)])
    check(proc.returncode == 0 and proc.stderr == b"", proc.stderr.decode("utf-8", "replace"))
    parsed = json.loads(proc.stdout.decode("utf-8"))
    check(parsed["routes"]["return-lines"]["state"] == "selected-but-invalid", "cli state")
    check(snap(code) == before_code and snap(book) == before_book, "cli created a path")


def case_changed_facade() -> None:
    code = make_code("changed-facade", SNAPSHOT)
    target = code / "app" / "return_line_tools_v2.py"
    under_suite(target)
    data = bytearray(read_bytes(target))
    data[-1] ^= 0x01
    write_bytes(target, bytes(data))
    body = observe("changed-facade", code, make_book("changed-facade"))
    item = body["routes"]["return-lines"]
    check(item["state"] == "selected-but-invalid", item["state"])
    check("facade bytes differ" in item["mismatches"], str(item["mismatches"]))
    check(item["declaration_matches_contract"] is True, "declaration dragged into the facade failure")
    assert_old_valid(body, "capture-return")


def case_changed_dependency() -> None:
    code = make_code("changed-dependency", SNAPSHOT)
    target = code / "labs" / "return-lines-pass01" / "return_lines.py"
    under_suite(target)
    data = bytearray(read_bytes(target))
    data[-1] ^= 0x01
    write_bytes(target, bytes(data))
    body = observe("changed-dependency", code, make_book("changed-dependency"))
    item = body["routes"]["return-lines"]
    check(item["state"] == "selected-but-invalid", item["state"])
    check("dependency bytes differ: pass01" in item["mismatches"], str(item["mismatches"]))
    check(item["declaration_matches_contract"] is True, "declaration")
    check(item["facade_matches_contract"] is True, "facade")
    assert_old_valid(body, "capture-return")


def case_staged_drift() -> None:
    code = make_code("staged-drift", SNAPSHOT)
    target = code / "app" / "return_line_tools_v3.py"
    under_suite(target)
    data = bytearray(read_bytes(target))
    data[-1] ^= 0x01
    write_bytes(target, bytes(data))
    body = observe("staged-drift", code, make_book("staged-drift"))
    assert_old_valid_except_stage(body, "return-lines")
    item = body["routes"]["return-lines"]
    check(item["state"] == "selected-valid", item["state"])
    check("staged facade bytes differ" in item["staged_notes"], str(item["staged_notes"]))
    check(item["successor_matches_contract"] is False, "staged match")
    check(item["successor_staged"] is True, "staged existence")
    assert_old_valid(body, "capture-return")


def assert_old_valid_except_stage(body: dict, command: str) -> None:
    item = body["routes"][command]
    check(item["selector"] == "old" and item["mismatches"] == [], str(item["mismatches"]))
    check(item["facade_matches_contract"] is True and item["declaration_matches_contract"] is True, "pins")


def case_comment() -> None:
    prefix = b"An observation is not closure.\n"
    closing = prefix + b'"""'
    check(SNAPSHOT.count(closing) == 1, "docstring close")
    fake = (
        prefix
        + b"Dead text names return_line_tools_v3.py and is not a load.\n"
        + b'"""\n# comment load_module(Path(__file__).resolve().parent / "return_line_tools_v3.py", "not-a-selection")\n'
    )
    data = SNAPSHOT.replace(closing, fake, 1)
    check(data.count(OLD_RL) == 1, "real load changed")
    check(b"return_line_tools_v3.py" in data, "fake name absent")
    parsed = TOOL_MOD.recognize(data.decode("utf-8"))
    check(parsed["routes"]["return-lines"]["facade"] == "return_line_tools_v2.py", parsed["routes"]["return-lines"])
    code = make_code("comment-docstring", data)
    body = observe("comment-docstring", code, make_book("comment-docstring"))
    assert_old_valid(body, "return-lines")
    assert_old_valid(body, "capture-return")


def case_duplicate() -> None:
    extra = (
        b'\nif command == "return-lines":\n'
        b'    door = load_module(Path(__file__).resolve().parent / "return_line_tools_v3.py", "librarian_return_line_tools_v3")\n'
    )
    data = SNAPSHOT + extra
    check(data.count(b'command == "return-lines"') == 2, "duplicate count")
    code = make_code("duplicate-branch", data)
    body = observe("duplicate-branch", code, make_book("duplicate-branch"))
    item = body["routes"]["return-lines"]
    check(item["state"] == "ambiguous", item["state"])
    check(item["selector"] == "none" and item["selected_facade"] is None, "guessed a duplicate")
    check(item["successor_staged"] is True, "staged report")
    assert_old_valid(body, "capture-return")
    assert_reads(body, reads_for({"capture-return": "old"}, {"return-lines"}), {"return-line-layout.json"})


def case_dynamic() -> None:
    data = SNAPSHOT.replace(OLD_RL, b"parent / filename", 1)
    check(OLD_RL not in data and data.count(OLD_HO) == 1, "dynamic edit")
    code = make_code("dynamic-branch", data)
    body = observe("dynamic-branch", code, make_book("dynamic-branch"))
    item = body["routes"]["return-lines"]
    check(item["state"] == "unsupported", item["state"])
    check(item["selector"] == "none" and item["selected_facade"] is None, "guessed a dynamic load")
    assert_old_valid(body, "capture-return")


def case_unknown() -> None:
    data = SNAPSHOT.replace(OLD_RL, b'parent / "future_tools.py"', 1)
    code = make_code("unknown-route", data)
    body = observe("unknown-route", code, make_book("unknown-route"))
    item = body["routes"]["return-lines"]
    check(item["state"] == "unknown", item["state"])
    check(item["selector"] == "unknown", item["selector"])
    check(item["selected_facade"] == "app/future_tools.py", item["selected_facade"])
    check(item["state"] != "selected-but-invalid", "unknown became invalid")
    check(not os.path.lexists(code / "app" / "future_tools.py"), "unknown file was created")
    names = {row["path"] for row in body["reads"]}
    check("app/future_tools.py" not in names, "unknown path was read")
    assert_old_valid(body, "capture-return")


def case_tampered() -> None:
    code = make_code("tampered-declaration", SNAPSHOT)
    outside = SUITE / "outside.py"
    under_suite(outside)
    write_bytes(outside, b"outside\n")
    before = sha(read_bytes(outside))
    declaration = code / "app" / "return-lines-v2.json"
    under_suite(declaration)
    payload = json.dumps({"adapter": {"path": str(outside)}}).encode("utf-8") + b"\n"
    write_bytes(declaration, payload)
    body = observe("tampered-declaration", code, make_book("tampered-declaration"))
    item = body["routes"]["return-lines"]
    check(item["state"] == "selected-but-invalid", item["state"])
    check("declaration bytes differ" in item["mismatches"], str(item["mismatches"]))
    check(all(row["path"] != str(outside) and ".." not in row["path"] for row in body["reads"]), "escaped read")
    check(sha(read_bytes(outside)) == before, "outside bytes changed")
    assert_old_valid(body, "capture-return")


def case_malformed_dispatcher() -> None:
    code = SUITE / "cases" / "malformed-dispatcher" / "code"
    write_dispatcher(code, b"def (\n")
    body = observe("malformed-dispatcher", code, make_book("malformed-dispatcher"))
    check(body["dispatcher"]["state"] == "malformed", body["dispatcher"]["state"])
    check(all(body["routes"][name]["state"] == "unsupported" for name in COMMANDS), "routes")
    assert_reads(body, {"app/librarian.py"}, {"return-line-layout.json"})


def case_missing_dispatcher() -> None:
    code = SUITE / "cases" / "missing-dispatcher" / "code"
    under_suite(code)
    (code / "app").mkdir(parents=True)
    body = observe("missing-dispatcher", code, make_book("missing-dispatcher"))
    check(body["dispatcher"]["state"] == "missing", body["dispatcher"]["state"])
    check(all(body["routes"][name]["state"] == "absent" for name in COMMANDS), "routes")
    assert_reads(body, {"app/librarian.py"}, {"return-line-layout.json"})


def case_layouts() -> None:
    malformed = make_book("layout-malformed")
    declare_layout(malformed, b"{")
    body = observe("layout-malformed", OLD_CODE, malformed)
    check(body["book_declaration"]["layout"]["state"] == "malformed", body["book_declaration"]["layout"]["state"])
    check(body["book_declaration"]["declared"] is False, "declared")
    assert_old_valid(body, "return-lines")
    duplicate = make_book("layout-duplicate-key")
    declare_layout(duplicate, b'{"schema": "return-line-layout/1", "schema": "other"}\n')
    body = observe("layout-duplicate-key", OLD_CODE, duplicate)
    check(body["book_declaration"]["layout"]["state"] == "malformed", "duplicate key")
    conflicting = make_book("layout-conflicting")
    declare_layout(conflicting, b'{"book": "00.00.10.work", "schema": "return-line-layout/1"}\n')
    body = observe("layout-conflicting", OLD_CODE, conflicting)
    check(body["book_declaration"]["layout"]["state"] == "conflicting", body["book_declaration"]["layout"]["state"])
    check(body["book_declaration"]["declared"] is False, "conflicting declared")
    directory = make_book("layout-directory")
    target = directory / "return-line-layout.json"
    under_suite(target)
    target.mkdir()
    body = observe("layout-directory", OLD_CODE, directory)
    check(body["book_declaration"]["layout"]["state"] == "wrong-type", body["book_declaration"]["layout"]["state"])


def case_door_file() -> None:
    book = make_book("door-file")
    write_bytes(book / "0100.band.returns", b"not a directory\n")
    body = observe("door-file", OLD_CODE, book)
    check(body["book_declaration"]["door"]["state"] == "wrong-type", body["book_declaration"]["door"]["state"])
    check(body["book_declaration"]["door"]["page"] is None, "page")
    check(body["book_declaration"]["declared"] is False, "declared")
    names = {row["path"] for row in body["reads"]}
    check("0100.band.returns/01.md" not in names, "page read on a file door")


def case_valid_book() -> None:
    book = make_book("valid-book")
    page = b"retained page\n"
    declare_door(book, page)
    declare_layout(book, TOOL_MOD.canonical_layout("00.00.10.work"))
    body = observe("valid-book", OLD_CODE, book)
    door = body["book_declaration"]
    check(door["declared"] is True, "declared")
    check(door["door"]["state"] == "present", "door")
    check(door["layout"]["state"] == "valid", "layout")
    check(door["layout"]["book"] == "00.00.10.work", door["layout"]["book"])
    check(door["door"]["page"]["sha256"] == sha(page), "page hash")
    check("the book has no valid line-pass declaration" not in body["missing_prerequisites"], "false missing declaration")
    assert_old_valid(body, "return-lines")
    assert_old_valid(body, "capture-return")
    check(body["authority"] == "not-assessed" and body["authorization"] is False, "declaration became authority")


def case_new_declared() -> None:
    book = make_book("new-and-declared")
    declare_door(book, b"page\n")
    declare_layout(book, TOOL_MOD.canonical_layout("00.00.10.work"))
    body = observe("new-and-declared", NEW_CODE, book)
    assert_new_valid(body, "return-lines")
    assert_new_valid(body, "capture-return")
    check(body["book_declaration"]["declared"] is True, "declared")
    check(body["missing_prerequisites"] == authority_lines(), body["missing_prerequisites"])
    check(body["authorization"] is False and body["authority"] == "not-assessed", "non-authority")
    check(body["warnings"] == list(TOOL_MOD.WARNINGS), "warnings dropped")


def case_bom() -> None:
    book = make_book("bom-layout")
    declare_door(book, b"page\n")
    declare_layout(book, b"\xef\xbb\xbf" + TOOL_MOD.canonical_layout("00.00.10.work"))
    body = observe("bom-layout", OLD_CODE, book)
    check(body["book_declaration"]["layout"]["state"] == "malformed", body["book_declaration"]["layout"]["state"])
    check(body["book_declaration"]["declared"] is False, "bom declared")
    assert_old_valid(body, "return-lines")


def case_fault_dispatcher() -> None:
    calls = {"n": 0}

    def injected(path: str) -> bytes:
        if path.replace("\\", "/").endswith("/app/librarian.py"):
            calls["n"] += 1
            if calls["n"] == 1:
                return SNAPSHOT
            return BOTH_NEW
        with open(path, "rb") as handle:
            return handle.read()

    body = observe("fault-dispatcher", OLD_CODE, OLD_BOOK, injected)
    check(calls["n"] == 2, f"dispatcher reads {calls['n']}")
    check(body["dispatcher"]["state"] == "unstable", body["dispatcher"]["state"])
    check(body["dispatcher"]["sha256"] != body["dispatcher"]["sha256_reread"], "cuts matched")
    for name in COMMANDS:
        item = body["routes"][name]
        check(item["state"] == "unstable", item["state"])
        check(item["selector"] == "none" and item["selected_facade"] is None, "combined cuts")
        check(item["dependencies"] == [], "dependencies from a cut")
    check(all(item["state"] != "selected-valid" for item in body["routes"].values()), "selected-valid from a changing file")


def case_fault_dependency() -> None:
    calls = {"n": 0}
    needle = "/labs/return-access-pass01/return_access.py"

    def injected(path: str) -> bytes:
        with open(path, "rb") as handle:
            data = handle.read()
        if path.replace("\\", "/").endswith(needle):
            calls["n"] += 1
            if calls["n"] >= 2:
                return data + b"x"
        return data

    book = make_book("fault-dependency")
    body = observe("fault-dependency", OLD_CODE, book, injected)
    check(calls["n"] >= 2, f"dependency reads {calls['n']}")
    check(body["dispatcher"]["state"] == "unstable", body["dispatcher"]["state"])
    for name in COMMANDS:
        check(body["routes"][name]["state"] == "unstable", body["routes"][name]["state"])
        check(body["routes"][name]["selected_facade"] is None, "kept a route from the first cut")
    rows = [row for row in body["reads"] if row["path"] == needle[1:]]
    check(len(rows) == 1 and rows[0]["state"] == "unstable", str(rows))


def case_hardlink() -> None:
    code = make_code("hardlink-dependency", SNAPSHOT)
    src = code / "labs" / "return-access-pass01" / "return_access.py"
    dst = code / "labs" / "return-access-pass01" / "return_access-extra.py"
    under_suite(dst)
    try:
        os.link(src, dst)
    except OSError as exc:
        raise Skip(f"os.link failed: {exc}") from exc
    body = observe("hardlink-dependency", code, make_book("hardlink-dependency"))
    item = body["routes"]["return-lines"]
    check(item["state"] == "selected-but-invalid", item["state"])
    check("dependency adapter linked" in item["mismatches"], str(item["mismatches"]))
    assert_old_valid(body, "capture-return")


def case_cli() -> None:
    code_s = str(OLD_CODE)
    book_s = str(OLD_BOOK)
    before = snap(OLD_CODE), snap(OLD_BOOK)
    proc = run_cli(["--code-root", code_s, "--book", book_s, "--text"])
    check(proc.returncode == 0 and proc.stderr == b"", proc.stderr.decode("utf-8", "replace"))
    body = TOOL_MOD.inspect(OLD_CODE, OLD_BOOK, code_text=code_s, book_text=book_s)
    expected = (TOOL_MOD.dump(body) + TOOL_MOD.project_text(body)).encode("utf-8")
    check(proc.stdout == expected, "text projection is not the same observation")
    check(snap(OLD_CODE) == before[0] and snap(OLD_BOOK) == before[1], "cli created a path")
    guard_repo()
    refusals = [
        ([], "missing"),
        (["--code-root", code_s], "missing"),
        (["--code-root", "labs", "--book", book_s], "not absolute"),
        (["--code-root", str(REPO / "app" / ".."), "--book", book_s], "escapes"),
        (["--code-root", code_s, "--book", book_s, "--force"], "unknown"),
        (["--allow-live", "--code-root", code_s, "--book", book_s], "unknown"),
        (["--read-bytes", "x", "--code-root", code_s, "--book", book_s], "unknown"),
        (["--code-root", code_s, "--code-root", code_s, "--book", book_s], "repeated"),
        (["--text", "--text", "--code-root", code_s, "--book", book_s], "repeated"),
        (["--code-root", str(SUITE / "not-a-directory.txt"), "--book", book_s], "not a directory"),
        (["--code-root", str(SUITE / "absent-root"), "--book", book_s], "absent"),
    ]
    write_bytes(SUITE / "not-a-directory.txt", b"file\n")
    for args, needle in refusals:
        proc = run_cli(args)
        check(proc.returncode == 2, f"{args} exit {proc.returncode}")
        check(proc.stdout == b"", f"{args} stdout {proc.stdout!r}")
        err = proc.stderr.decode("utf-8")
        check(err.startswith("refuse: ") and err.count("\n") == 1, err)
        check(needle in err, f"{args} stderr {err}")
    if SYMLINK_OK:
        link = SUITE / "linked-root"
        if not link.exists():
            os.symlink(str(OLD_CODE), str(link), target_is_directory=True)
        proc = run_cli(["--code-root", str(link), "--book", book_s])
        check(proc.returncode == 2 and proc.stdout == b"" and b"linked" in proc.stderr, proc.stderr.decode("utf-8", "replace"))
    else:
        NOTES.append({"kind": "skip", "limit": SYMLINK_ERROR, "name": "linked-root"})


def case_live() -> None:
    before_lib = read_bytes(LIVE_LIB)
    before_page = read_bytes(BOOK_LIVE / "0100.band.returns" / "01.md")
    before_app = sorted(os.listdir(REPO / "app"))
    before_lab = sorted(os.listdir(REPO / "labs" / "return-readiness-pass01"))
    expected_paths = reads_for({"return-lines": "old", "capture-return": "old"})
    before_hashes = {rel: sha(read_bytes(REPO / rel)) for rel in expected_paths}
    check(not os.path.lexists(BOOK_LIVE / "return-line-layout.json"), "layout before")
    proc = run_cli([
        "--code-root", str(REPO),
        "--book", str(BOOK_LIVE),
        "--text",
    ])
    check(proc.returncode == 0 and proc.stderr == b"", proc.stderr.decode("utf-8", "replace"))
    text = proc.stdout.decode("utf-8")
    body = TOOL_MOD.inspect(REPO, BOOK_LIVE, code_text=str(REPO), book_text=str(BOOK_LIVE))
    check(proc.stdout == (TOOL_MOD.dump(body) + TOOL_MOD.project_text(body)).encode("utf-8"), "live cli differs from inspect")
    assert_quiet(body)
    assert_old_valid(body, "return-lines")
    assert_old_valid(body, "capture-return")
    check(body["dispatcher"]["sha256"] == BASELINE_SHA, body["dispatcher"]["sha256"])
    check(body["dispatcher"]["bytes"] == BASELINE_BYTES, "dispatcher bytes")
    check(body["dispatcher"]["matches_predecessor_snapshot"] is False, "live hash treated as a pin")
    check(body["dispatcher"]["state"] == "measured", body["dispatcher"]["state"])
    check(body["book_declaration"]["door"]["state"] == "present", "door")
    check(body["book_declaration"]["door"]["page"]["sha256"] == DOOR_PAGE_SHA, "door page")
    check(body["book_declaration"]["door"]["page"]["bytes"] == DOOR_PAGE_BYTES, "door bytes")
    check(body["book_declaration"]["layout"]["state"] == "missing", "layout")
    check(body["book_declaration"]["declared"] is False, "declared")
    assert_reads(body, expected_paths, {"return-line-layout.json", "0100.band.returns/01.md"})
    check("authorization: false\n" in text, "live text")
    check("warning: Historical direct scripts remain runnable." in text, "live warning")
    after_hashes = {rel: sha(read_bytes(REPO / rel)) for rel in expected_paths}
    check(before_hashes == after_hashes, "a read file changed")
    check(read_bytes(LIVE_LIB) == before_lib, "dispatcher changed")
    check(read_bytes(BOOK_LIVE / "0100.band.returns" / "01.md") == before_page, "door page changed")
    check(sorted(os.listdir(REPO / "app")) == before_app, "app directory changed")
    check(sorted(os.listdir(REPO / "labs" / "return-readiness-pass01")) == before_lab, "lab directory changed")
    check(not os.path.lexists(BOOK_LIVE / "return-line-layout.json"), "layout after")
    check(OLD_RL in before_lib and OLD_HO in before_lib, "live loads")
    check(sha(before_lib) == BASELINE_SHA, "substituted dispatcher was copied onto the app")
    write_bytes(SUITE / "live-stdout.txt", proc.stdout)
    write_bytes(SUITE / "live-summary.json", dump_json({
        "authority": body["authority"],
        "authorization": body["authorization"],
        "declared": body["book_declaration"]["declared"],
        "claim_time_bytes": CLAIM_TIME_BYTES,
        "claim_time_sha256": CLAIM_TIME_SHA,
        "dispatcher_sha256": body["dispatcher"]["sha256"],
        "door": body["book_declaration"]["door"]["state"],
        "layout": body["book_declaration"]["layout"]["state"],
        "matches_predecessor_snapshot": body["dispatcher"]["matches_predecessor_snapshot"],
        "routes": {
            name: {
                "selector": body["routes"][name]["selector"],
                "state": body["routes"][name]["state"],
                "successor_matches_contract": body["routes"][name]["successor_matches_contract"],
                "successor_staged": body["routes"][name]["successor_staged"],
            }
            for name in COMMANDS
        },
    }))


def not_run() -> None:
    rows = [
        ("N01", "Prime independent probes", "Prime runs probes later. This suite does not invent them."),
        ("N02", "App selection", "No substitution is applied to the shared dispatcher."),
        ("N03", "Live migration", "No book is migrated and no root is created."),
        ("N04", "Review-loop classification", "The review-loop implementation stays unread and unclassified."),
        ("N05", "Historical demo.py and rehearse.py execution", "Those scripts are not started."),
    ]
    for cid, text, limit in rows:
        CLAIMS.append({"case": "", "claim": text, "detail": "", "id": cid, "limit": limit, "result": "not-run"})


def finish(code: int, detail: str = "") -> None:
    payload = {
        "claims": CLAIMS,
        "detail": detail,
        "exit": code,
        "passed": sum(1 for item in CLAIMS if item["result"] == "passed"),
        "failed": sum(1 for item in CLAIMS if item["result"] == "failed"),
        "not_run": sum(1 for item in CLAIMS if item["result"] == "not-run"),
        "skipped_environment": sum(1 for item in CLAIMS if item["result"] == "skipped-environment"),
        "schema": "return-route-readiness-claims/0510",
        "suite": str(SUITE),
    }
    write_bytes(SUITE / "claims.json", dump_json(payload))
    write_bytes(SUITE / "commands.json", dump_json(NOTES))
    write_bytes(SUITE / "fixture-index.json", dump_json(INDEX))
    if code != 0 and not (SUITE / "first-failure.txt").exists():
        write_bytes(SUITE / "first-failure.txt", (detail or "failed") .encode("utf-8") + b"\n")
    print(json.dumps({"exit": code, "failed": payload["failed"], "passed": payload["passed"], "suite": str(SUITE)}, sort_keys=True), flush=True)


def prepare() -> None:
    global TOOL_MOD, CONTRACTS, CLOSURE, SNAPSHOT, BOTH_NEW, ONE_NEW, OLD_CODE, OLD_BOOK, NEW_CODE, SYMLINK_OK, SYMLINK_ERROR
    global BASELINE_SHA, BASELINE_BYTES
    SUITE.mkdir(parents=True)
    print(f"suite {SUITE}", flush=True)
    baseline = read_bytes(LIVE_LIB)
    BASELINE_SHA = sha(baseline)
    BASELINE_BYTES = len(baseline)
    NOTES.append({
        "bytes": BASELINE_BYTES,
        "claim_time_bytes": CLAIM_TIME_BYTES,
        "claim_time_sha256": CLAIM_TIME_SHA,
        "kind": "dispatcher-baseline",
        "sha256": BASELINE_SHA,
    })
    TOOL_MOD = load_tool()
    CONTRACTS = json.loads(read_bytes(CONTRACTS_PATH).decode("utf-8"))
    paths = set()
    for sides in CONTRACTS["routes"].values():
        for side in sides.values():
            paths.add(side["facade"]["path"])
            paths.add(side["declaration"]["path"])
            for dep in side["dependencies"]:
                paths.add(dep["path"])
    CLOSURE = sorted(paths)
    SNAPSHOT = read_bytes(REPO / CONTRACTS["predecessor_dispatcher"]["path"])
    BOTH_NEW = both_new(SNAPSHOT)
    ONE_NEW = one_new(SNAPSHOT)
    OLD_CODE = make_code("old-staged", SNAPSHOT)
    OLD_BOOK = make_book("old-staged")
    NEW_CODE = make_code("both-new-base", BOTH_NEW)
    probe = SUITE / "symlink-probe-target"
    probe.mkdir()
    link = SUITE / "symlink-probe"
    try:
        os.symlink(str(probe), str(link), target_is_directory=True)
        SYMLINK_OK = True
        SYMLINK_ERROR = ""
    except OSError as exc:
        SYMLINK_OK = False
        SYMLINK_ERROR = str(exc)
    write_bytes(SUITE / "not-a-directory.txt", b"file\n")
    guard_repo()


def main() -> int:
    try:
        prepare()
        cases = [
            ("C01", "The tool source is a bounded standard-library recognizer with no public injection flag.", "source-audit", "The audit is a source scan, not a proof about every future edit.", case_source),
            ("C02", "Frozen manifest rows and the adapter declaration pin match the disk.", "pin-preflight", "The predecessor snapshot is provenance and is not the live dispatcher.", case_pins),
            ("C03", "The activation guard is not selection, and unsupported shapes are not guessed.", "recognizer-limits", "Matching the static pattern does not prove runtime behavior.", case_recognizer),
            ("C04", "The predecessor snapshot selects both old routes while the reviewed successors are staged.", "old-staged", "Other dispatch branches are not classified.", case_old),
            ("C05", "Both reviewed substitutions select the new routes without using the whole-file hash as a pin.", "both-new", "The copied dispatcher stays in the suite root.", case_both_new),
            ("C06", "One reviewed substitution leaves the other route on its old selector.", "one-route", "A partial selection is not readiness for both routes.", case_one),
            ("C07", "A missing selected facade is selected-but-invalid and the command still exits 0.", "missing-facade", "Exit 0 is an observation, not approval.", case_missing_facade),
            ("C08", "A changed selected facade is selected-but-invalid.", "changed-facade", "The declaration pin is a separate check.", case_changed_facade),
            ("C09", "A changed selected dependency is selected-but-invalid while its declaration hash is unchanged.", "changed-dependency", "Dependency paths come from the versioned contract.", case_changed_dependency),
            ("C10", "Staged successor drift does not invalidate a matching old selection.", "staged-drift", "The staged note is not a mismatch.", case_staged_drift),
            ("C11", "A successor filename in a docstring and a comment is not selection.", "comment-docstring", "The recognizer reads the syntax tree, not comments.", case_comment),
            ("C12", "Two simple branches for one command are ambiguous, including an appended branch.", "duplicate-branch", "Unreachable duplicates still count.", case_duplicate),
            ("C13", "A non-literal load filename is unsupported.", "dynamic-branch", "The other route can still be measured.", case_dynamic),
            ("C14", "A literal outside the reviewed pair stays unknown and is not adopted.", "unknown-route", "There is no rescan and no new contract.", case_unknown),
            ("C15", "A tampered declaration path is not followed outside the code root.", "tampered-declaration", "The tool hashes the contract path and does not parse a destination out of the declaration.", case_tampered),
            ("C16", "A dispatcher that does not parse is malformed, and its routes are unsupported.", "malformed-dispatcher", "A syntax error is not a route result.", case_malformed_dispatcher),
            ("C17", "A missing dispatcher leaves both routes absent.", "missing-dispatcher", "Absent is distinct from selected false.", case_missing_dispatcher),
            ("C18", "Malformed, duplicate-key, conflicting, and wrong-type layouts stay distinct and undeclared.", "layouts", "Duplicate keys are malformed. A parseable non-canonical body is conflicting.", case_layouts),
            ("C19", "A regular file where the band directory is required is a wrong-type door.", "door-file", "The page inside that path is not read.", case_door_file),
            ("C20", "A present door and the canonical layout are a declaration without authority.", "valid-book", "declared does not mean the migration ran.", case_valid_book),
            ("C21", "Selected successors plus a valid declaration still leave authority not-assessed.", "new-and-declared", "The tool does not search for a release.", case_new_declared),
            ("H01", "A dispatcher that changes between the two reads is unstable and the cuts are not combined.", "fault-dispatcher", "Unit fault injection at read_bytes. The public command has no injection flag.", case_fault_dispatcher),
            ("H02", "A canonical layout with a UTF-8 BOM is not valid and does not crash.", "bom-layout", "The BOM is a hostile byte prefix, not a second layout dialect.", case_bom),
            ("H04", "A dependency that changes between its two reads blanks both routes.", "fault-dependency", "Unit fault injection. A stable sibling route is not kept from the first cut.", case_fault_dependency),
        ]
        for cid, text, case, limit, fn in cases:
            run_case(cid, text, case, limit, fn)
        run_case(
            "H03",
            "A selected dependency with link count other than 1 is selected-but-invalid.",
            "hardlink-dependency",
            "os.link failure is an environment skip, not a product failure.",
            case_hardlink,
        )
        run_case(
            "C22",
            "The public command projects one observation and refuses every other invocation shape.",
            "cli",
            "Refusal is exit 2 with empty stdout. A linked root is checked only when the process can create a directory symlink.",
            case_cli,
        )
        run_case(
            "C23",
            "The live code root and live book select both old routes, stage the reviewed successors, and do not authorize migration.",
            "live",
            "The read set is the known old closure plus staged facade and declaration files, the layout path, and the door page. The repository was not walked.",
            case_live,
        )
    except Fail as exc:
        write_bytes(SUITE / "first-failure.txt", f"{CURRENT}\n{exc}\n".encode("utf-8"))
        finish(1, f"{CURRENT}: {exc}")
        return 1
    except Exception:
        detail = traceback.format_exc()
        write_bytes(SUITE / "first-failure.txt", detail.encode("utf-8"))
        finish(1, detail)
        return 1
    not_run()
    guard_repo()
    finish(0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
