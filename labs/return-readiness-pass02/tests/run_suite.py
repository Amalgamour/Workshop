#!/usr/bin/env python3
"""Focused cases for the coherent return-route readiness successor.

The suite retains fixture trees under D:\\librarian\\temp\\0521-0511.
It does not select the app, write a layout into the live book, or revise the delta.
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
PASS02 = REPO / "labs" / "return-readiness-pass02" / "readiness.py"
PASS01_TOOL = REPO / "labs" / "return-readiness-pass01" / "readiness.py"
CONTRACTS_PATH = REPO / "labs" / "return-readiness-pass01" / "contracts.json"
MANIFEST_PATH = REPO / "00.kernel" / "00.00.10.work" / "0521.return-placement" / "evidence" / "pack05.11" / "source-manifest.json"
PACK_PATH = REPO / "00.kernel" / "00.00.10.work" / "0521.return-placement" / "05.11.md"
DELTA_PATH = REPO / "00.kernel" / "00.00.10.work" / "0521.return-placement" / "evidence" / "build05.11" / "DELTA.md"
NOTE_PATH = REPO / "00.kernel" / "00.00.10.work" / "0521.return-placement" / "06.22.md"
LIVE_LIB = REPO / "app" / "librarian.py"
REPRO = Path(r"D:\librarian\temp\0521-0511\20261102T224423676416Z-repro")
PASS01_PY_SHA = "e9d59040920e06cc2edf0d5d2ebdec8954e83945fa2629b9eae08e5164cfcecf"
PASS01_CONTRACTS_SHA = "0bd74ada28e4828df9fe74feffdbb44af3eba4df9f57c64a9512f93373664cfc"
CLAIM_TIME_SHA = "b15919adb7664f993373fbc6eaaaf86d66100f396b3401845900734f920248ea"
CLAIM_TIME_BYTES = 12204
PACK_SHA = "1287ccf661907b2b942463199afefee1d9a8f3495dd489502a3b69dc10b3cd46"
PACK_BYTES = 4086
SNAPSHOT_SHA = "826167161000ac3eab78c466ae47e31b37ff435ea33f4104caf7651ecd21436e"
SNAPSHOT_BYTES = 12153
END_SHA = "89c84f3a8a162383da5ab38a74d441a6dc309c5158f5b05d313f6db802e8c270"
T1_SHA = "a8100ae6aa1940d0b663bb31cd466142ebbdbd5187131b92d93818987832eb89"
ADAPTER = "labs/return-access-pass01/return_access.py"
BACKEND = "labs/return-lines-pass03/return_lines.py"
READER = "labs/return-capture-pass01/return_capture.py"
FACADE_OLD = "app/return_line_tools_v2.py"
FACADE_NEW = "app/return_line_tools_v3.py"
DISPATCHER_REL = "app/librarian.py"
OLD_RL = b'parent / "return_line_tools_v2.py"'
NEW_RL = b'parent / "return_line_tools_v3.py"'
OLD_HO = b'parent / "handoff_tools.py"'
NEW_HO = b'parent / "handoff_tools_v2.py"'
COMMANDS = ("return-lines", "capture-return")
ENV = os.environ.copy()
ENV["PYTHONDONTWRITEBYTECODE"] = "1"

STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
SUITE = Path(r"D:\librarian\temp\0521-0511") / f"{STAMP}-suite"


class Fail(Exception):
    pass


class Skip(Exception):
    pass


CLAIMS: list[dict] = []
NOTES: list[dict] = []
INDEX: list[dict] = []
CURRENT = ""
BASELINE_SHA = ""
BASELINE_BYTES = 0
DELTA_SHA = ""
NOTE_SHA = ""


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


def key_of(path: str) -> str:
    return os.path.normcase(os.path.abspath(path))


def tail(rel: str) -> str:
    return os.path.normcase(rel.replace("/", os.sep))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
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
    check(sha(read_bytes(PASS01_TOOL)) == PASS01_PY_SHA, "pass01 readiness.py changed")
    check(sha(read_bytes(CONTRACTS_PATH)) == PASS01_CONTRACTS_SHA, "pass01 contracts.json changed")
    check(sha(read_bytes(DELTA_PATH)) == DELTA_SHA, "DELTA.md changed during the suite")
    check(sha(read_bytes(NOTE_PATH)) == NOTE_SHA, "06.22.md changed during the suite")


def assert_quiet(body: dict) -> None:
    check(body["schema"] == "return-route-readiness/2", "schema")
    check(body["authorization"] is False, "authorization")
    check(body["selection_is_authorization"] is False, "selection_is_authorization")
    check(body["authority"] == "not-assessed", "authority")
    check(body["app_selection_applied"] is False, "app_selection_applied")
    check(body["migration_assessed"] is False, "migration_assessed")
    check(body["approval"] == "not-established", "approval")
    check(body["completion"] == "not-established", "completion")
    check(body["task_association"] == "not-established", "task_association")
    check(body["recognizer"] == "static-ast-pattern", "recognizer")
    check(body["warnings"] == list(PASS01.WARNINGS), f"warnings {body['warnings']}")
    check(body["provenance"] == list(PASS01.PROVENANCE), "provenance")
    check(body["next_checks"] == list(PASS01.NEXT_CHECKS), "next_checks")
    expected_limits = list(PASS01.LIMITS) + list(TOOL.EXTRA_LIMITS)
    check(body["limits"] == expected_limits, f"limits {body['limits']}")
    check("coherent" in body and "final_check" in body and "changed_paths" in body, "coherence fields")
    check("decode" in body and "read_error" in body, "fault fields")
    check("sha256_final" in body["dispatcher"], "sha256_final")
    check("app_selected" in body["historical_status_note"], "historical note")
    check(set(body["routes"]) == set(COMMANDS), f"routes {set(body['routes'])}")
    for line in body["next_checks"]:
        check("python" not in line and not line.startswith("--"), f"next check looks executable: {line}")
    joined = json.dumps(body["reads"])
    check("review_loop" not in joined and "review-loop" not in joined, "a review-loop path was read")


def save_obs(name: str, body: dict) -> None:
    path = SUITE / "observations" / f"{name}.json"
    under_suite(path)
    write_bytes(path, TOOL.dump(body).encode("utf-8"))


def assert_delta(root: Path, before_files: dict[str, str], before_dirs: list[str], allowed_content=(), allowed_new=(), allowed_gone=(), allowed_dirs=()) -> None:
    files, dirs = snap(root)
    new_files = set(files) - set(before_files)
    gone = set(before_files) - set(files)
    check(new_files <= set(allowed_new), f"new files {sorted(new_files)}")
    check(gone <= set(allowed_gone), f"disappeared {sorted(gone)}")
    for rel, digest in files.items():
        if rel in allowed_content or rel in allowed_new:
            continue
        check(before_files.get(rel) == digest, f"unexpected content change {rel}")
    new_dirs = set(dirs) - set(before_dirs)
    check(new_dirs <= set(allowed_dirs), f"new directories {sorted(new_dirs)}")


def observe(name: str, code: Path, book: Path, read_bytes_fn=None, allowed_content=(), allowed_new=(), allowed_gone=(), allowed_dirs=(), book_new=(), book_gone=(), book_dirs=()) -> dict:
    under_suite(code)
    under_suite(book)
    before_code = snap(code)
    before_book = snap(book)
    kwargs = {"code_text": str(code), "book_text": str(book)}
    if read_bytes_fn is not None:
        kwargs["read_bytes"] = read_bytes_fn
    body = TOOL.inspect(code, book, **kwargs)
    assert_delta(code, before_code[0], before_code[1], allowed_content, allowed_new, allowed_gone, allowed_dirs)
    assert_delta(book, before_book[0], before_book[1], (), book_new, book_gone, book_dirs)
    guard_repo()
    assert_quiet(body)
    save_obs(name, body)
    INDEX.append({"book": str(book), "case": name, "code": str(code), "mode": "inspect"})
    NOTES.append({"case": name, "kind": "inspect", "mode": "in-process" if read_bytes_fn is None else "unit-fault-injection"})
    return body


def run_cli(tool: Path, args: list[str]) -> subprocess.CompletedProcess:
    command = [str(PY), "-B", str(tool.relative_to(REPO)).replace("\\", "/"), *args]
    proc = subprocess.run(command, cwd=REPO, env=ENV, capture_output=True, timeout=120)
    NOTES.append({
        "args": args,
        "bytes_stderr": len(proc.stderr),
        "bytes_stdout": len(proc.stdout),
        "exit": proc.returncode,
        "kind": "cli",
        "tool": command[2],
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


def reads_for(selected: dict[str, str]) -> set[str]:
    paths = {DISPATCHER_REL}
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
    check(item["successor_staged"] is True, f"{command} staged")
    check(item["successor_matches_contract"] is True, f"{command} successor pin")


def assert_new_valid(body: dict, command: str) -> None:
    item = body["routes"][command]
    facade = CONTRACTS["routes"][command]["new"]["facade"]["path"]
    check(item["state"] == "selected-valid", f"{command} {item['state']}")
    check(item["selector"] == "new", f"{command} selector")
    check(item["selected_facade"] == facade, f"{command} facade")
    check(item["mismatches"] == [], f"{command} mismatches {item['mismatches']}")
    check(item["successor_staged"] is False, f"{command} staged while selected")
    check(item["predecessor_present"] is True, f"{command} predecessor")


def assert_blank(body: dict, state: str, selector: str) -> None:
    for name in COMMANDS:
        item = body["routes"][name]
        check(item["state"] == state, f"{name} {item['state']}")
        check(item["selector"] == selector, f"{name} selector {item['selector']}")
        check(item["selected_facade"] is None, f"{name} facade kept")
        check(item["mismatches"] == [], f"{name} mismatches kept {item['mismatches']}")
        check(item["dependencies"] == [], f"{name} dependencies kept")


def assert_coherent(body: dict, *, decode_none: bool = True) -> None:
    check(body["coherent"] is True, "coherent")
    check(body["final_check"] == "matched", body["final_check"])
    check(body["changed_paths"] == [], f"changed {body['changed_paths']}")
    if decode_none:
        check(body["decode"] is None, "decode")
    check(body["read_error"] is None, "read_error")
    check(body["dispatcher"]["sha256_final"] == body["dispatcher"]["sha256"], "sha256_final")


def assert_unstable(body: dict) -> None:
    check(body["coherent"] is False, "coherent stayed true")
    check(body["final_check"] == "changed", body["final_check"])
    check(body["changed_paths"], "changed_paths empty")
    assert_blank(body, "unstable", "none")
    check(body["read_error"] is None, "read_error")


def seam_once(actions: dict):
    fired: list[str] = []

    def read_bytes(path: str) -> bytes:
        folded = key_of(path)
        for rel, action in actions.items():
            if folded.endswith(tail(rel)) and rel not in fired:
                fired.append(rel)
                action()
                break
        return PASS01.default_read(path)

    read_bytes.fired = fired
    return read_bytes


def declare_door(book: Path, page: bytes) -> None:
    door = book / "0100.band.returns"
    under_suite(door)
    door.mkdir()
    write_bytes(door / "01.md", page)


def run_case(cid: str, text: str, case: str, limit: str, fn, kind: str) -> None:
    global CURRENT
    CURRENT = case
    try:
        fn()
    except Fail as exc:
        CLAIMS.append({"case": case, "claim": text, "class": kind, "detail": str(exc), "id": cid, "limit": limit, "result": "failed"})
        raise
    except Skip as exc:
        CLAIMS.append({
            "case": case,
            "claim": text,
            "class": kind,
            "detail": str(exc),
            "id": cid,
            "limit": limit,
            "result": "skipped-environment",
        })
        print(f"skip {cid} {case} {exc}", flush=True)
        return
    CLAIMS.append({"case": case, "claim": text, "class": kind, "detail": "", "id": cid, "limit": limit, "result": "passed"})
    print(f"pass {cid} {case}", flush=True)


def case_source() -> None:
    source = read_bytes(PASS02).decode("utf-8")
    check("\r" not in source, "successor source contains CR")
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    allowed = {"__future__", "hashlib", "importlib", "os", "pathlib", "stat", "sys"}
    check(imported <= allowed, f"imports {sorted(imported - allowed)}")
    for banned in ("subprocess", "socket", "review_loop", "except Exception"):
        check(banned not in source, f"tool source contains {banned}")
    check("def recognize" not in source, "successor reimplemented the recognizer")
    check("read_bytes" in source, "fault seam missing")
    for flag in ("--force", "--allow-live", "--reader", "--inject", "--read-bytes"):
        check(flag not in source, f"public flag {flag}")
    check(TOOL.SCHEMA == "return-route-readiness/2", "schema constant")
    check(TOOL.PASS01_PY_SHA == PASS01_PY_SHA, "pass01 pin constant")
    check(TOOL.PASS01_CONTRACTS_SHA == PASS01_CONTRACTS_SHA, "contracts pin constant")


def case_pins() -> None:
    manifest = json.loads(read_bytes(MANIFEST_PATH).decode("utf-8"))
    check(manifest["schema"] == "prime-pack-inputs/1", "manifest schema")
    check(manifest.get("provenance") == "measured working-tree sources, not committed provenance", "manifest provenance")
    mismatches = []
    for row in manifest["files"]:
        live = read_bytes(REPO / row["path"])
        snap_bytes = read_bytes(REPO / row["snapshot"])
        if sha(live) != row["sha256"] or len(live) != row["bytes"] or live != snap_bytes:
            mismatches.append(row["path"])
    check(mismatches == [], f"pin mismatches {mismatches}")
    check(len(manifest["files"]) == 20, f"manifest count {len(manifest['files'])}")
    pred = read_bytes(REPO / CONTRACTS["predecessor_dispatcher"]["path"])
    check(sha(pred) == SNAPSHOT_SHA and len(pred) == SNAPSHOT_BYTES, "predecessor snapshot")
    check(sha(one_new(pred)) == END_SHA, f"return-lines-only end hash {sha(one_new(pred))}")
    sample = PASS01.canonical_layout(CONTRACTS["layout"]["known_book"])
    check(sha(sample) == CONTRACTS["layout"]["known_sha256"] and len(sample) == CONTRACTS["layout"]["known_bytes"], "layout identity")
    saved = {
        "t1-result.json": "8b63afad500f1613f90b747b1455c53e89af5a7497c5b3a069f98caccaab43f6",
        "t1-stderr.txt": "c98afc0abc8edf0d8d6a4131888690b3a955394a0c2b0acee3388f1c6063f017",
        "t2-result.json": "a01e59db99fb506f8a0aa556f6d3d674aaf6466c1d7cfc8fdb23af89b4235036",
    }
    for name, digest in saved.items():
        data = read_bytes(REPRO / name)
        check(sha(data) == digest, f"official {name} hash moved")
    check(read_bytes(REPRO / "t1-stdout.bin") == b"", "official T1 stdout moved")
    check(sha(read_bytes(REPRO / "t1" / "code" / "app" / "librarian.py")) == T1_SHA, "official T1 dispatcher moved")
    check(sha(read_bytes(REPRO / "t2" / "code" / "app" / "librarian.py")) == END_SHA, "official T2 dispatcher moved")
    guard_repo()


def case_pass01_t1() -> None:
    code = make_code("pass01-t1", b"\xff")
    book = make_book("pass01-t1")
    check(sha(read_bytes(code / "app" / "librarian.py")) == T1_SHA, "T1 fixture hash")
    before = snap(code)
    proc = run_cli(PASS01_TOOL, ["--code-root", str(code), "--book", str(book)])
    check(proc.returncode == 1, f"exit {proc.returncode}")
    check(proc.stdout == b"", "stdout was not empty")
    err = proc.stderr.decode("utf-8", "replace")
    check("UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte" in err, err[-400:])
    check("Traceback" in err, "traceback missing")
    check(snap(code) == before, "pass01 T1 created a path")
    write_bytes(SUITE / "pass01-t1.stderr", proc.stderr)
    write_bytes(SUITE / "pass01-t1.stdout", proc.stdout)
    guard_repo()


def case_pass01_t2() -> None:
    code = make_code("pass01-t2", SNAPSHOT)
    book = make_book("pass01-t2")
    mutated = one_new(SNAPSHOT)
    reader = seam_once({FACADE_OLD: lambda: write_dispatcher(code, mutated)})
    before_files, before_dirs = snap(code)
    body = PASS01.inspect(code, book, read_bytes=reader, code_text=str(code), book_text=str(book))
    check(FACADE_OLD in reader.fired, "mutation did not fire")
    check(body["dispatcher"]["state"] == "measured", body["dispatcher"]["state"])
    check(body["dispatcher"]["sha256"] == SNAPSHOT_SHA, body["dispatcher"]["sha256"])
    check(body["routes"]["return-lines"]["state"] == "selected-valid", body["routes"]["return-lines"]["state"])
    check(body["routes"]["capture-return"]["state"] == "selected-valid", body["routes"]["capture-return"]["state"])
    check(body["routes"]["return-lines"]["selector"] == "old", "selector")
    end = sha(read_bytes(code / "app" / "librarian.py"))
    check(end == END_SHA, end)
    assert_delta(code, before_files, before_dirs, allowed_content=(DISPATCHER_REL,))
    guard_repo()
    NOTES.append({"case": "pass01-t2", "end_sha256": end, "kind": "known-failure", "measured_sha256": body["dispatcher"]["sha256"]})


def case_pass02_t1() -> None:
    code = make_code("pass02-t1", b"\xff")
    book = make_book("pass02-t1")
    body = observe("pass02-t1", code, book)
    check(body["dispatcher"]["state"] == "malformed", body["dispatcher"]["state"])
    check(body["dispatcher"]["bytes"] == 1, "byte length")
    check(body["dispatcher"]["sha256"] == T1_SHA, body["dispatcher"]["sha256"])
    check(body["dispatcher"]["sha256_final"] == T1_SHA, "sha256_final")
    check(body["decode"] == {"encoding": "utf-8", "position": 0, "reason": "invalid start byte"}, body["decode"])
    assert_blank(body, "unknown", "unknown")
    assert_coherent(body, decode_none=False)
    check(body["authority"] == "not-assessed", "authority")
    proc = run_cli(PASS02, ["--code-root", str(code), "--book", str(book)])
    check(proc.returncode == 0 and proc.stderr == b"", proc.stderr.decode("utf-8", "replace"))
    check(b"\r" not in proc.stdout, "CR in stdout")
    check(proc.stdout == TOOL.dump(body).encode("utf-8"), "cli observation differs")
    check(b"Traceback" not in proc.stderr, "traceback")


def case_pass02_t2() -> None:
    code = make_code("pass02-t2", SNAPSHOT)
    book = make_book("pass02-t2")
    mutated = one_new(SNAPSHOT)
    reader = seam_once({FACADE_OLD: lambda: write_dispatcher(code, mutated)})
    body = observe("pass02-t2", code, book, reader, allowed_content=(DISPATCHER_REL,))
    check(FACADE_OLD in reader.fired, "mutation did not fire")
    assert_unstable(body)
    check(body["dispatcher"]["state"] == "unstable", body["dispatcher"]["state"])
    check(body["dispatcher"]["sha256"] == SNAPSHOT_SHA, body["dispatcher"]["sha256"])
    check(body["dispatcher"]["sha256_final"] == END_SHA, body["dispatcher"]["sha256_final"])
    row = next(item for item in body["changed_paths"] if item["path"] == DISPATCHER_REL)
    check(row["before_sha256"] == SNAPSHOT_SHA and row["after_sha256"] == END_SHA, row)
    check(sha(read_bytes(code / "app" / "librarian.py")) == END_SHA, "end file")
    check(all(item["state"] != "selected-valid" for item in body["routes"].values()), "selected-valid kept")


def case_late_dependency() -> None:
    code = make_code("late-dependency", SNAPSHOT)
    book = make_book("late-dependency")
    target = code / "labs" / "return-access-pass01" / "return_access.py"
    original = read_bytes(target)

    def mutate() -> None:
        write_bytes(target, original + b"\n")

    reader = seam_once({BACKEND: mutate})
    body = observe("late-dependency", code, book, reader, allowed_content=(ADAPTER,))
    check(BACKEND in reader.fired, "dependency mutation did not fire")
    assert_unstable(body)
    check(body["dispatcher"]["state"] == "measured", body["dispatcher"]["state"])
    row = next(item for item in body["changed_paths"] if item["path"] == ADAPTER)
    check(row["before_state"] == "file" and row["after_state"] == "file", row)
    check(row["before_sha256"] != row["after_sha256"], "adapter hash stayed")
    check(body["book_declaration"]["declared"] is False, "declared")


def case_layout_appears() -> None:
    code = make_code("layout-appears", SNAPSHOT)
    book = make_book("layout-appears")
    layout = PASS01.canonical_layout("00.00.10.work")

    def appear() -> None:
        write_bytes(book / "return-line-layout.json", layout)

    reader = seam_once({FACADE_OLD: appear})
    body = observe("layout-appears", code, book, reader, book_new=("return-line-layout.json",))
    check(FACADE_OLD in reader.fired, "layout mutation did not fire")
    assert_unstable(body)
    check(body["book_declaration"]["layout"]["state"] == "unstable", body["book_declaration"]["layout"]["state"])
    check(body["book_declaration"]["declared"] is False, "declared")
    check(body["dispatcher"]["state"] == "measured", "dispatcher was marked unstable")
    row = next(item for item in body["changed_paths"] if item["path"] == "return-line-layout.json")
    check(row["before_state"] == "missing" and row["after_state"] == "file", row)
    check(row["after_sha256"] == sha(layout), "layout hash")


def case_disappear() -> None:
    code = make_code("disappear", SNAPSHOT)
    book = make_book("disappear")
    target = code.joinpath(*ADAPTER.split("/"))

    def remove() -> None:
        under_suite(target)
        target.unlink()

    reader = seam_once({BACKEND: remove})
    body = observe("disappear", code, book, reader, allowed_gone=(ADAPTER,))
    assert_unstable(body)
    row = next(item for item in body["changed_paths"] if item["path"] == ADAPTER)
    check(row["before_state"] == "file" and row["after_state"] == "missing", row)
    check(all(item["state"] != "selected-valid" for item in body["routes"].values()), "selected-valid")


def case_wrong_type() -> None:
    code = make_code("wrong-type", SNAPSHOT)
    book = make_book("wrong-type")
    target = code.joinpath(*READER.split("/"))

    def replace() -> None:
        under_suite(target)
        target.unlink()
        target.mkdir()

    reader = seam_once({FACADE_NEW: replace})
    body = observe("wrong-type", code, book, reader, allowed_gone=(READER,), allowed_dirs=(READER,))
    assert_unstable(body)
    row = next(item for item in body["changed_paths"] if item["path"] == READER)
    check(row["after_state"] == "wrong-type", row)


def case_hardlink() -> None:
    code = make_code("hardlink", SNAPSHOT)
    book = make_book("hardlink")
    target = code.joinpath(*READER.split("/"))
    extra = target.parent / "return_capture.py.extra-link"
    extra_rel = f"{READER}.extra-link"

    def link() -> None:
        under_suite(extra)
        try:
            os.link(str(target), str(extra))
        except OSError as exc:
            raise Skip(str(exc)) from exc

    reader = seam_once({FACADE_NEW: link})
    body = observe("hardlink", code, book, reader, allowed_new=(extra_rel,))
    assert_unstable(body)
    row = next(item for item in body["changed_paths"] if item["path"] == READER)
    check(row["after_state"] == "linked", row)


def case_stable_old() -> None:
    body = observe("stable-old", OLD_CODE, OLD_BOOK)
    assert_old_valid(body, "return-lines")
    assert_old_valid(body, "capture-return")
    assert_coherent(body)
    check(body["dispatcher"]["state"] == "measured", "dispatcher")
    check(body["dispatcher"]["matches_predecessor_snapshot"] is True, "snapshot")
    check(body["dispatcher"]["sha256"] == SNAPSHOT_SHA, "hash")
    check(body["book_declaration"]["layout"]["state"] == "missing", "layout")
    check(body["book_declaration"]["door"]["state"] == "missing", "door")
    check(body["book_declaration"]["declared"] is False, "declared")
    assert_reads(body, reads_for({"return-lines": "old", "capture-return": "old"}), {"return-line-layout.json"})
    text = TOOL.project_text(body)
    check(text.startswith("\nreturn-route-readiness/2\n"), text[:80])
    check(text.endswith("coherent: true\nfinal_check: matched\n"), text[-80:])
    check("return-lines: selected-valid old app/return_line_tools_v2.py\n" in text, "projection")


def case_stable_new() -> None:
    code = make_code("stable-new", BOTH_NEW)
    book = make_book("stable-new")
    body = observe("stable-new", code, book)
    assert_new_valid(body, "return-lines")
    assert_new_valid(body, "capture-return")
    assert_coherent(body)
    check(body["dispatcher"]["matches_predecessor_snapshot"] is False, "whole-file hash used as a pin")
    check(body["dispatcher"]["sha256"] != SNAPSHOT_SHA, "identity")
    check(body["book_declaration"]["declared"] is False, "selection declared the book")
    assert_reads(body, reads_for({"return-lines": "new", "capture-return": "new"}), {"return-line-layout.json"})


def case_separate() -> None:
    code = make_code("separate", SNAPSHOT)
    book = make_book("separate")
    first = observe("separate-first", code, book)
    assert_old_valid(first, "return-lines")
    check(first["dispatcher"]["matches_predecessor_snapshot"] is True, "first snapshot")
    target = code / "app" / "librarian.py"
    write_bytes(target, SNAPSHOT + b"\n# other branch note\n")
    second = observe("separate-second", code, book)
    assert_old_valid(second, "return-lines")
    assert_old_valid(second, "capture-return")
    assert_coherent(second)
    check(second["dispatcher"]["matches_predecessor_snapshot"] is False, "later hash became a pin")
    check(second["dispatcher"]["sha256"] != first["dispatcher"]["sha256"], "second cut")
    check(second["routes"]["return-lines"]["state"] == "selected-valid", "route invalidated by another inspection")


def case_layouts() -> None:
    code = make_code("layouts", SNAPSHOT)
    missing = make_book("layouts-missing")
    body = observe("layout-missing", code, missing)
    assert_old_valid(body, "return-lines")
    assert_coherent(body)
    check(body["book_declaration"]["layout"]["state"] == "missing", "missing")
    check(body["book_declaration"]["declared"] is False, "missing declared")
    malformed = make_book("layouts-malformed")
    write_bytes(malformed / "return-line-layout.json", b"\xff")
    body = observe("layout-malformed", code, malformed)
    assert_old_valid(body, "return-lines")
    assert_coherent(body)
    check(body["book_declaration"]["layout"]["state"] == "malformed", body["book_declaration"]["layout"]["state"])
    check(body["book_declaration"]["declared"] is False, "malformed declared")
    valid = make_book("layouts-valid")
    write_bytes(valid / "return-line-layout.json", PASS01.canonical_layout("00.00.10.work"))
    declare_door(valid, b"page\n")
    body = observe("layout-valid", code, valid)
    assert_old_valid(body, "return-lines")
    assert_old_valid(body, "capture-return")
    assert_coherent(body)
    check(body["book_declaration"]["layout"]["state"] == "valid", "valid")
    check(body["book_declaration"]["door"]["state"] == "present", "door")
    check(body["book_declaration"]["declared"] is True, "declared")
    check(body["authority"] == "not-assessed", "authority")
    check(body["authorization"] is False, "authorization")
    check("the book has no valid line-pass declaration" not in body["missing_prerequisites"], "declaration prerequisite stayed")
    check("migration and release authority were not assessed" in body["missing_prerequisites"], "authority prerequisite")


def case_bad_declaration() -> None:
    code = make_code("bad-declaration", SNAPSHOT)
    target = code / "app" / "return-lines-v2.json"
    under_suite(target)
    write_bytes(target, b"\xff")
    book = make_book("bad-declaration")
    body = observe("bad-declaration", code, book)
    item = body["routes"]["return-lines"]
    check(item["state"] == "selected-but-invalid", item["state"])
    check("declaration bytes differ" in item["mismatches"], str(item["mismatches"]))
    assert_old_valid(body, "capture-return")
    assert_coherent(body)
    proc = run_cli(PASS02, ["--code-root", str(code), "--book", str(book)])
    check(proc.returncode == 0 and proc.stderr == b"", proc.stderr.decode("utf-8", "replace"))
    check(b"Traceback" not in proc.stdout and b"Traceback" not in proc.stderr, "traceback")


def case_bad_dependency() -> None:
    code = make_code("bad-dependency", SNAPSHOT)
    target = code.joinpath(*ADAPTER.split("/"))
    under_suite(target)
    write_bytes(target, b"\xff")
    body = observe("bad-dependency", code, make_book("bad-dependency"))
    item = body["routes"]["return-lines"]
    check(item["state"] == "selected-but-invalid", item["state"])
    check("dependency bytes differ: adapter" in item["mismatches"], str(item["mismatches"]))
    assert_coherent(body)
    check(item["state"] != "selected-valid", "selected-valid")


def case_door_bytes() -> None:
    code = make_code("door-bytes", SNAPSHOT)
    book = make_book("door-bytes")
    declare_door(book, b"\xff")
    body = observe("door-bytes", code, book)
    assert_old_valid(body, "return-lines")
    assert_coherent(body)
    page = body["book_declaration"]["door"]["page"]
    check(body["book_declaration"]["door"]["state"] == "present", "door")
    check(page["sha256"] == sha(b"\xff") and page["bytes"] == 1, page)
    check(body["book_declaration"]["declared"] is False, "declared")
    proc = run_cli(PASS02, ["--code-root", str(code), "--book", str(book)])
    check(proc.returncode == 0 and proc.stderr == b"", proc.stderr.decode("utf-8", "replace"))


def case_door_disappears() -> None:
    code = make_code("door-disappears", SNAPSHOT)
    book = make_book("door-disappears")
    declare_door(book, b"page\n")
    page = book / "0100.band.returns" / "01.md"

    def remove() -> None:
        under_suite(page)
        page.unlink()

    reader = seam_once({FACADE_OLD: remove})
    body = observe("door-disappears", code, book, reader, book_gone=("0100.band.returns/01.md",))
    assert_unstable(body)
    check(body["book_declaration"]["declared"] is False, "declared")
    check(body["book_declaration"]["door"]["page"]["state"] == "unstable", "page")
    row = next(item for item in body["changed_paths"] if item["path"] == "0100.band.returns/01.md")
    check(row["after_state"] == "missing", row)


def case_syntax() -> None:
    code = make_code("syntax", b"def (\n")
    book = make_book("syntax")
    body = observe("syntax", code, book)
    check(body["dispatcher"]["state"] == "malformed", body["dispatcher"]["state"])
    assert_blank(body, "unsupported", "none")
    assert_coherent(body)
    check(body["decode"] is None, "syntax classified as encoding")
    proc = run_cli(PASS02, ["--code-root", str(code), "--book", str(book)])
    check(proc.returncode == 0 and proc.stderr == b"", proc.stderr.decode("utf-8", "replace"))


def case_missing_dispatcher() -> None:
    code = make_code("missing-dispatcher", SNAPSHOT)
    target = code / "app" / "librarian.py"
    under_suite(target)
    target.unlink()
    body = observe("missing-dispatcher", code, make_book("missing-dispatcher"))
    check(body["dispatcher"]["state"] == "missing", body["dispatcher"]["state"])
    assert_blank(body, "absent", "none")
    assert_coherent(body)


def case_oserror() -> None:
    code = make_code("oserror", SNAPSHOT)
    book = make_book("oserror")

    def read_bytes(path: str) -> bytes:
        if key_of(path).endswith(tail(DISPATCHER_REL)):
            raise FileNotFoundError(path)
        return PASS01.default_read(path)

    body = observe("oserror", code, book, read_bytes)
    assert_blank(body, "unknown", "unknown")
    check(body["coherent"] is False, "coherent")
    check(body["final_check"] == "not-run", body["final_check"])
    check(body["read_error"] == "FileNotFoundError", body["read_error"])
    check(body["dispatcher"]["state"] == "unreadable", body["dispatcher"]["state"])
    check(all(item["state"] != "selected-valid" for item in body["routes"].values()), "selected-valid")


def case_programmer() -> None:
    code = make_code("programmer", SNAPSHOT)
    book = make_book("programmer")

    def read_bytes(path: str) -> bytes:
        raise RuntimeError("programmer fault")

    try:
        TOOL.inspect(code, book, read_bytes=read_bytes, code_text=str(code), book_text=str(book))
    except RuntimeError as exc:
        check(str(exc) == "programmer fault", str(exc))
        guard_repo()
        return
    raise Fail("RuntimeError was swallowed")


def case_pre_gap() -> None:
    code = make_code("pre-gap", SNAPSHOT)
    book = make_book("pre-gap")
    mutated = SNAPSHOT + b"\n# moved between cuts\n"
    seen = {"n": 0}

    def read_bytes(path: str) -> bytes:
        if key_of(path).endswith(tail(DISPATCHER_REL)):
            seen["n"] += 1
            if seen["n"] == 3:
                write_dispatcher(code, mutated)
        return PASS01.default_read(path)

    body = observe("pre-gap", code, book, read_bytes, allowed_content=(DISPATCHER_REL,))
    check(seen["n"] >= 4, f"dispatcher reads {seen['n']}")
    assert_unstable(body)
    check(body["dispatcher"]["state"] == "unstable", body["dispatcher"]["state"])
    row = next(item for item in body["changed_paths"] if item["path"] == DISPATCHER_REL)
    check(row["before_sha256"] == SNAPSHOT_SHA, row)
    check(row["after_sha256"] == sha(mutated), row)
    check(body["dispatcher"]["sha256_final"] == sha(mutated), "sha256_final")


def case_cli() -> None:
    code_s = str(OLD_CODE)
    book_s = str(OLD_BOOK)
    before = (snap(OLD_CODE), snap(OLD_BOOK))
    proc = run_cli(PASS02, ["--code-root", code_s, "--book", book_s, "--text"])
    check(proc.returncode == 0 and proc.stderr == b"", proc.stderr.decode("utf-8", "replace"))
    check(b"\r" not in proc.stdout, "CR in text stdout")
    body = TOOL.inspect(OLD_CODE, OLD_BOOK, code_text=code_s, book_text=book_s)
    expected = (TOOL.dump(body) + TOOL.project_text(body)).encode("utf-8")
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
        (["--inject", "--code-root", code_s, "--book", book_s], "unknown"),
        (["--code-root", code_s, "--code-root", code_s, "--book", book_s], "repeated"),
        (["--text", "--text", "--code-root", code_s, "--book", book_s], "repeated"),
        (["--code-root", str(SUITE / "not-a-directory.txt"), "--book", book_s], "not a directory"),
        (["--code-root", str(SUITE / "absent-root"), "--book", book_s], "absent"),
    ]
    for args, needle in refusals:
        proc = run_cli(PASS02, args)
        check(proc.returncode == 2, f"{args} exit {proc.returncode}")
        check(proc.stdout == b"", f"{args} stdout {proc.stdout!r}")
        err = proc.stderr.decode("utf-8")
        check(err.startswith("refuse: ") and err.count("\n") == 1 and "\r" not in err, err)
        check(needle in err, f"{args} stderr {err}")
    if SYMLINK_OK:
        link = SUITE / "linked-root"
        if not link.exists():
            os.symlink(str(OLD_CODE), str(link), target_is_directory=True)
        proc = run_cli(PASS02, ["--code-root", str(link), "--book", book_s])
        check(proc.returncode == 2 and proc.stdout == b"" and b"linked" in proc.stderr, proc.stderr.decode("utf-8", "replace"))
    else:
        NOTES.append({"kind": "skip", "limit": SYMLINK_ERROR, "name": "linked-root"})


def case_live() -> None:
    before_lib = read_bytes(LIVE_LIB)
    before_page = read_bytes(BOOK_LIVE / "0100.band.returns" / "01.md")
    before_app = sorted(os.listdir(REPO / "app"))
    before_lab = sorted(os.listdir(REPO / "labs" / "return-readiness-pass01"))
    before_pass02 = sorted(os.listdir(REPO / "labs" / "return-readiness-pass02"))
    expected_paths = reads_for({"return-lines": "old", "capture-return": "old"})
    before_hashes = {rel: sha(read_bytes(REPO / rel)) for rel in expected_paths}
    check(not os.path.lexists(BOOK_LIVE / "return-line-layout.json"), "layout before")
    proc = run_cli(PASS02, ["--code-root", str(REPO), "--book", str(BOOK_LIVE), "--text"])
    check(proc.returncode == 0 and proc.stderr == b"", proc.stderr.decode("utf-8", "replace"))
    check(b"\r" not in proc.stdout, "CR in live stdout")
    body = TOOL.inspect(REPO, BOOK_LIVE, code_text=str(REPO), book_text=str(BOOK_LIVE))
    check(proc.stdout == (TOOL.dump(body) + TOOL.project_text(body)).encode("utf-8"), "live cli differs from inspect")
    assert_quiet(body)
    assert_old_valid(body, "return-lines")
    assert_old_valid(body, "capture-return")
    assert_coherent(body)
    check(body["dispatcher"]["sha256"] == BASELINE_SHA, body["dispatcher"]["sha256"])
    check(body["dispatcher"]["bytes"] == BASELINE_BYTES, "dispatcher bytes")
    check(body["dispatcher"]["matches_predecessor_snapshot"] is False, "live hash treated as a pin")
    check(body["dispatcher"]["state"] == "measured", body["dispatcher"]["state"])
    check(body["book_declaration"]["door"]["state"] == "present", "door")
    check(body["book_declaration"]["door"]["page"]["sha256"] == sha(before_page), "door page")
    check(body["book_declaration"]["door"]["page"]["bytes"] == len(before_page), "door bytes")
    check(body["book_declaration"]["layout"]["state"] == "missing", "layout")
    check(body["book_declaration"]["declared"] is False, "declared")
    assert_reads(body, expected_paths, {"return-line-layout.json", "0100.band.returns/01.md"})
    text = proc.stdout.decode("utf-8")
    check("coherent: true\nfinal_check: matched\n" in text, "live coherence lines")
    check("authorization: false\n" in text, "live text")
    after_hashes = {rel: sha(read_bytes(REPO / rel)) for rel in expected_paths}
    check(before_hashes == after_hashes, "a read file changed")
    check(read_bytes(LIVE_LIB) == before_lib, "dispatcher changed")
    check(read_bytes(BOOK_LIVE / "0100.band.returns" / "01.md") == before_page, "door page changed")
    check(sorted(os.listdir(REPO / "app")) == before_app, "app directory changed")
    check(sorted(os.listdir(REPO / "labs" / "return-readiness-pass01")) == before_lab, "pass01 directory changed")
    check(sorted(os.listdir(REPO / "labs" / "return-readiness-pass02")) == before_pass02, "pass02 directory changed")
    check(not os.path.lexists(BOOK_LIVE / "return-line-layout.json"), "layout after")
    write_bytes(SUITE / "live-stdout.txt", proc.stdout)
    write_bytes(SUITE / "live-summary.json", dump_json({
        "authority": body["authority"],
        "authorization": body["authorization"],
        "coherent": body["coherent"],
        "declared": body["book_declaration"]["declared"],
        "claim_time_bytes": CLAIM_TIME_BYTES,
        "claim_time_sha256": CLAIM_TIME_SHA,
        "dispatcher_bytes": body["dispatcher"]["bytes"],
        "dispatcher_sha256": body["dispatcher"]["sha256"],
        "door_bytes": body["book_declaration"]["door"]["page"]["bytes"],
        "door_sha256": body["book_declaration"]["door"]["page"]["sha256"],
        "door": body["book_declaration"]["door"]["state"],
        "final_check": body["final_check"],
        "layout": body["book_declaration"]["layout"]["state"],
        "matches_predecessor_snapshot": body["dispatcher"]["matches_predecessor_snapshot"],
        "read_count": len(body["reads"]),
        "routes": {
            name: {
                "selector": body["routes"][name]["selector"],
                "state": body["routes"][name]["state"],
                "successor_matches_contract": body["routes"][name]["successor_matches_contract"],
                "successor_staged": body["routes"][name]["successor_staged"],
            }
            for name in COMMANDS
        },
        "sha256_final": body["dispatcher"]["sha256_final"],
    }))


def not_run() -> None:
    rows = [
        ("N01", "Prime independent probes", "Prime runs probes later. This suite does not invent them."),
        ("N02", "App selection", "No substitution is applied to the shared dispatcher."),
        ("N03", "Live migration", "No book is migrated and no root is created."),
        ("N04", "Review-loop classification", "The review-loop implementation stays unread and unclassified."),
        ("N05", "Custody filing", "Matching 0121.return-placement stays pending."),
        ("N06", "Historical demo.py and rehearse.py execution", "Those scripts are not started."),
    ]
    for cid, text, limit in rows:
        CLAIMS.append({"case": "", "claim": text, "class": "not-run", "detail": "", "id": cid, "limit": limit, "result": "not-run"})


def finish(code: int, detail: str = "") -> None:
    payload = {
        "claims": CLAIMS,
        "detail": detail,
        "exit": code,
        "failed": sum(1 for item in CLAIMS if item["result"] == "failed"),
        "not_run": sum(1 for item in CLAIMS if item["result"] == "not-run"),
        "passed": sum(1 for item in CLAIMS if item["result"] == "passed"),
        "schema": "return-route-readiness-claims/0511",
        "skipped_environment": sum(1 for item in CLAIMS if item["result"] == "skipped-environment"),
        "suite": str(SUITE),
    }
    write_bytes(SUITE / "claims.json", dump_json(payload))
    write_bytes(SUITE / "commands.json", dump_json(NOTES))
    write_bytes(SUITE / "fixture-index.json", dump_json(INDEX))
    print(json.dumps({
        "exit": code,
        "failed": payload["failed"],
        "passed": payload["passed"],
        "skipped": payload["skipped_environment"],
        "suite": str(SUITE),
    }, sort_keys=True), flush=True)


def prepare() -> None:
    global TOOL, PASS01, CONTRACTS, CLOSURE, SNAPSHOT, BOTH_NEW, OLD_CODE, OLD_BOOK
    global SYMLINK_OK, SYMLINK_ERROR, BASELINE_SHA, BASELINE_BYTES, DELTA_SHA, NOTE_SHA
    SUITE.mkdir(parents=True)
    print(f"suite {SUITE}", flush=True)
    baseline = read_bytes(LIVE_LIB)
    BASELINE_SHA = sha(baseline)
    BASELINE_BYTES = len(baseline)
    DELTA_SHA = sha(read_bytes(DELTA_PATH))
    NOTE_SHA = sha(read_bytes(NOTE_PATH))
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, env=ENV, capture_output=True, timeout=30)
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO, env=ENV, capture_output=True, timeout=30)
    NOTES.append({
        "bytes": BASELINE_BYTES,
        "claim_time_bytes": CLAIM_TIME_BYTES,
        "claim_time_sha256": CLAIM_TIME_SHA,
        "branch": branch.stdout.decode("utf-8", "replace").strip(),
        "head": head.stdout.decode("utf-8", "replace").strip(),
        "kind": "dispatcher-baseline",
        "sha256": BASELINE_SHA,
    })
    TOOL = load_module("return_readiness_pass02", PASS02)
    PASS01 = load_module("return_readiness_pass01_direct", PASS01_TOOL)
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
    check(sha(SNAPSHOT) == SNAPSHOT_SHA and len(SNAPSHOT) == SNAPSHOT_BYTES, "snapshot bytes")
    BOTH_NEW = both_new(SNAPSHOT)
    OLD_CODE = make_code("old-staged", SNAPSHOT)
    OLD_BOOK = make_book("old-staged")
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
            ("K01", "The successor source loads pass01, has no public injection flag, and does not reimplement the recognizer.", "source-audit", "The audit is a source scan.", "author", case_source),
            ("K02", "The pack05.11 rows, the pass01 pins, and the saved known-failure files still match.", "pins", "The manifest is not refreshed.", "author", case_pins),
            ("K03", "Unmodified pass01 still crashes on a stable non-UTF-8 dispatcher.", "pass01-t1", "This is the known failure. The successor is a different command.", "known-failure", case_pass01_t1),
            ("K04", "Unmodified pass01 still reports selected-valid when the dispatcher changes after its adjacent pair.", "pass01-t2", "The return-lines-only substitution is the frozen end hash. Unit seam only.", "known-failure", case_pass01_t2),
            ("A01", "The successor returns an observation for that same non-UTF-8 dispatcher.", "pass02-t1", "Route selection stays unknown. Exit 0 is not approval.", "repair", case_pass02_t1),
            ("A02", "The successor marks both routes unstable when that same late dispatcher change happens.", "pass02-t2", "One final re-read. No lock and no retry.", "repair", case_pass02_t2),
            ("A03", "An earlier dependency that changes during a later read makes the whole observation unstable.", "late-dependency", "Unit seam on a copy. The public command has no injection flag.", "repair", case_late_dependency),
            ("A04", "A layout that is missing and then appears is unstable, not a valid declaration.", "layout-appears", "Unit seam on a copy.", "repair", case_layout_appears),
            ("A05", "A measured dependency that disappears before the final check is unstable.", "disappear", "The first-cut route details are not kept.", "repair", case_disappear),
            ("A06", "A measured file replaced by a directory before the final check is unstable.", "wrong-type", "Wrong-type is explicit.", "repair", case_wrong_type),
            ("A08", "A stable predecessor snapshot still reports both old routes and a matched final check.", "stable-old", "Other branches stay unclassified.", "author", case_stable_old),
            ("A09", "A stable selected successor still reports selected-valid, and the whole-file hash is not a pin.", "stable-new", "The copied dispatcher stays in the suite root.", "author", case_stable_new),
            ("A10", "A later separate inspection can see an other-branch edit and still report selected-valid.", "separate", "An earlier hash does not become a permanent pin.", "author", case_separate),
            ("A11", "Missing, malformed, and valid declarations stay distinct, and a valid declaration is not authority.", "layouts", "declared does not mean the migration ran.", "author", case_layouts),
            ("A12", "A non-UTF-8 selected declaration is selected-but-invalid and the command exits 0.", "bad-declaration", "The bytes are not replaced with an empty file.", "author", case_bad_declaration),
            ("A13", "A non-UTF-8 selected dependency is selected-but-invalid.", "bad-dependency", "The dependency is not executed.", "author", case_bad_dependency),
            ("A14", "A non-UTF-8 door page is recorded and does not crash.", "door-bytes", "The page is not decoded as a route.", "author", case_door_bytes),
            ("A15", "A door page that disappears after it was measured makes the observation unstable.", "door-disappears", "Unit seam on a copy.", "repair", case_door_disappears),
            ("A16", "A syntax error that still decodes stays malformed and unsupported.", "syntax", "Invalid UTF-8 is the encoding case. A syntax error is not reclassified as unknown.", "author", case_syntax),
            ("A17", "A missing dispatcher stays absent.", "missing-dispatcher", "Absent is distinct from unknown.", "author", case_missing_dispatcher),
            ("A18", "An OSError while reading the dispatcher is an explicit unknown observation.", "oserror", "Unit seam. There is no catch-all.", "repair", case_oserror),
            ("A19", "A programmer exception still propagates.", "programmer", "The tool does not report success for an unexpected exception.", "author", case_programmer),
            ("A20", "A dispatcher change between the pre-read and the pass01 cut is not reported as matched.", "pre-gap", "The pre-read is one extra pair, not a lock.", "repair", case_pre_gap),
            ("A21", "The public command projects one observation and refuses every other invocation shape.", "cli", "A linked root is checked only when the process can create a directory symlink.", "author", case_cli),
            ("A22", "The live code root and live book select both old routes, match the final check, and do not authorize migration.", "live", "The read set is the pass01 closure plus the layout path and the door page. The tool creates no file.", "author", case_live),
        ]
        for cid, text, case, limit, kind, fn in cases:
            run_case(cid, text, case, limit, fn, kind)
        run_case(
            "A07",
            "A measured file whose link count changes before the final check is unstable.",
            "hardlink",
            "os.link failure is an environment skip, not a product failure.",
            case_hardlink,
            "repair",
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
