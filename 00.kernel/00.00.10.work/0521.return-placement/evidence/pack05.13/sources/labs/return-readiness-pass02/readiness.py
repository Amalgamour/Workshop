#!/usr/bin/env python3
"""Coherent read-only return-route readiness.

This wrapper reuses return-readiness-pass01. It does not select a route or
write a file. inspect(..., read_bytes=...) is the unit seam. The command
line has no injection flag.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "return-route-readiness/2"
PASS01_PATH = Path(__file__).resolve().parent.parent / "return-readiness-pass01" / "readiness.py"
CONTRACTS_PATH = Path(__file__).resolve().parent.parent / "return-readiness-pass01" / "contracts.json"
PASS01_PY_SHA = "e9d59040920e06cc2edf0d5d2ebdec8954e83945fa2629b9eae08e5164cfcecf"
PASS01_CONTRACTS_SHA = "0bd74ada28e4828df9fe74feffdbb44af3eba4df9f57c64a9512f93373664cfc"
DISPATCHER_REL = "app/librarian.py"
EXTRA_LIMITS = (
    "Invalid UTF-8 leaves route selection unknown.",
    "One final re-read is not a lock and is not retried.",
    "A completed bounded observation is not a guarantee against changes after the final check.",
)
_PASS01 = None


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pass01():
    global _PASS01
    if _PASS01 is not None:
        return _PASS01
    tool = PASS01_PATH.read_bytes()
    if sha(tool) != PASS01_PY_SHA:
        raise RuntimeError("pass01 readiness bytes changed")
    contracts = CONTRACTS_PATH.read_bytes()
    if sha(contracts) != PASS01_CONTRACTS_SHA:
        raise RuntimeError("pass01 contracts bytes changed")
    spec = importlib.util.spec_from_file_location("return_readiness_pass01", PASS01_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load pass01")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _PASS01 = module
    return module


def annotate(body: dict) -> dict:
    body["schema"] = SCHEMA
    body["decode"] = body.get("decode")
    body["read_error"] = body.get("read_error")
    body["changed_paths"] = body.get("changed_paths", [])
    limits = list(body["limits"])
    for line in EXTRA_LIMITS:
        if line not in limits:
            limits.append(line)
    body["limits"] = limits
    return body


def remember_layout(mod, reads: dict, layout: dict) -> None:
    mod.remember(reads, {
        "bytes": layout.get("bytes"),
        "path": layout.get("path", "return-line-layout.json"),
        "sha256": layout.get("sha256"),
        "state": "file" if layout.get("state") in {"valid", "conflicting", "malformed"} else layout.get("state"),
    }, "book")


def directory_state(mod, root: Path, rel: str) -> str:
    if not mod.safe_rel(rel):
        return "escaping"
    full = os.path.abspath(str(root.joinpath(*rel.split("/"))))
    if not mod.inside(str(root), full):
        return "escaping"
    if not os.path.lexists(full):
        return "missing"
    if mod.is_reparse(full):
        return "linked"
    info = os.lstat(full)
    if not stat.S_ISDIR(info.st_mode):
        return "wrong-type"
    return "present"


def unknown_routes(mod, state: str, selector: str) -> dict:
    routes = {}
    for name in mod.COMMANDS:
        route = mod.blank_route(state)
        route["selector"] = selector
        routes[name] = route
    return routes


def base_observation(mod, code_root: Path, book: Path, code_text: str, book_text: str, dispatcher: dict, routes: dict, door: dict, layout: dict, reads: dict) -> dict:
    body = mod.observation(code_root, book, code_text, book_text, dispatcher, routes, door, layout, reads)
    return annotate(body)


def measure_book(mod, book: Path, read_bytes, reads: dict) -> tuple[dict, dict]:
    pinned = mod.contracts()
    try:
        layout = mod.measure_layout(book, read_bytes)
    except OSError as exc:
        layout = {"book": None, "bytes": None, "path": "return-line-layout.json", "sha256": None, "state": "unreadable", "read_error": type(exc).__name__}
    remember_layout(mod, reads, layout)
    try:
        door = mod.measure_door(book, pinned["door"], read_bytes, reads)
    except OSError as exc:
        door = {"page": None, "state": "unreadable", "read_error": type(exc).__name__}
    return door, layout


def encoding_observation(mod, code_root, book, code_text, book_text, row, exc, read_bytes) -> dict:
    reads = {}
    mod.remember(reads, row, "code")
    door, layout = measure_book(mod, book, read_bytes, reads)
    dispatcher = {
        "bytes": row["bytes"],
        "matches_predecessor_snapshot": False,
        "path": DISPATCHER_REL,
        "predecessor_bytes": mod.contracts()["predecessor_dispatcher"]["bytes"],
        "predecessor_sha256": mod.contracts()["predecessor_dispatcher"]["sha256"],
        "sha256": row["sha256"],
        "sha256_final": row["sha256"],
        "sha256_reread": row["sha256_reread"],
        "state": "malformed",
        "whole_file_hash_is_provenance": True,
    }
    body = base_observation(
        mod, code_root, book, code_text, book_text, dispatcher,
        unknown_routes(mod, "unknown", "unknown"), door, layout, reads,
    )
    body["coherent"] = True
    body["decode"] = {"encoding": "utf-8", "position": exc.start, "reason": exc.reason}
    body["final_check"] = "matched"
    body["read_error"] = None
    return body


def unreadable_observation(mod, code_root, book, code_text, book_text, exc, read_bytes) -> dict:
    reads = {}
    row = {"bytes": None, "path": DISPATCHER_REL, "sha256": None, "state": "unreadable"}
    mod.remember(reads, row, "code")
    door, layout = measure_book(mod, book, read_bytes, reads)
    prior = mod.contracts()["predecessor_dispatcher"]
    dispatcher = {
        "bytes": None,
        "matches_predecessor_snapshot": False,
        "path": DISPATCHER_REL,
        "predecessor_bytes": prior["bytes"],
        "predecessor_sha256": prior["sha256"],
        "sha256": None,
        "sha256_final": None,
        "sha256_reread": None,
        "state": "unreadable",
        "whole_file_hash_is_provenance": True,
    }
    body = base_observation(
        mod, code_root, book, code_text, book_text, dispatcher,
        unknown_routes(mod, "unknown", "unknown"), door, layout, reads,
    )
    body["coherent"] = False
    body["decode"] = None
    body["final_check"] = "not-run"
    body["read_error"] = type(exc).__name__
    return body


def blank_validity(mod, body: dict) -> None:
    body["routes"] = {name: mod.blank_route("unstable") for name in mod.COMMANDS}


def revalidate(mod, body: dict, code_root: Path, book: Path, read_bytes) -> dict:
    changed = []
    final_dispatcher = None
    again_by = {}
    for row in list(body["reads"]):
        root = code_root if row["root"] == "code" else book
        try:
            again = mod.read_identity(root, row["path"], read_bytes)
        except OSError as exc:
            changed.append({
                "after_sha256": None,
                "after_state": "unreadable",
                "before_sha256": row.get("sha256"),
                "before_state": row.get("state"),
                "path": row["path"],
                "read_error": type(exc).__name__,
                "root": row["root"],
            })
            continue
        again_by[(row["root"], row["path"])] = again
        if row["path"] == DISPATCHER_REL and row["root"] == "code":
            final_dispatcher = again
        if again["state"] != row.get("state") or again["sha256"] != row.get("sha256") or again["bytes"] != row.get("bytes"):
            changed.append({
                "after_sha256": again["sha256"],
                "after_state": again["state"],
                "before_sha256": row.get("sha256"),
                "before_state": row.get("state"),
                "path": row["path"],
                "root": row["root"],
            })
    seen_paths = {item["path"] for item in changed}
    for name, route in list(body["routes"].items()):
        if route.get("state") != "selected-valid":
            continue
        spec = mod.contracts()["routes"].get(name, {}).get(route.get("selector"))
        if not isinstance(spec, dict):
            continue
        expected = [spec["facade"], spec["declaration"], *spec["dependencies"]]
        for item in expected:
            if item["path"] in seen_paths:
                continue
            again = again_by.get(("code", item["path"]))
            if again is not None and mod.same_bytes(again, item):
                continue
            changed.append({
                "after_sha256": None if again is None else again.get("sha256"),
                "after_state": "unreadable" if again is None else again.get("state"),
                "before_sha256": item.get("sha256"),
                "before_state": "file",
                "path": item["path"],
                "root": "code",
            })
            seen_paths.add(item["path"])
    door_name = mod.contracts()["door"]
    try:
        door_now = directory_state(mod, book, door_name)
    except OSError as exc:
        door_now = "unreadable"
        changed.append({
            "after_sha256": None,
            "after_state": "unreadable",
            "before_sha256": None,
            "before_state": body["book_declaration"]["door"]["state"],
            "path": door_name,
            "read_error": type(exc).__name__,
            "root": "book",
        })
    if door_now != body["book_declaration"]["door"]["state"]:
        changed.append({
            "after_sha256": None,
            "after_state": door_now,
            "before_sha256": None,
            "before_state": body["book_declaration"]["door"]["state"],
            "path": door_name,
            "root": "book",
        })
        body["book_declaration"]["door"]["state"] = "unstable"
        body["book_declaration"]["door"]["page"] = None
        body["book_declaration"]["declared"] = False
    body["changed_paths"] = changed
    body["dispatcher"]["sha256_final"] = None if final_dispatcher is None else final_dispatcher["sha256"]
    if not changed:
        body["coherent"] = True
        body["decode"] = None
        body["final_check"] = "matched"
        body["read_error"] = None
        return annotate(body)
    if any(item["path"] == DISPATCHER_REL for item in changed):
        body["dispatcher"]["state"] = "unstable"
    if any(item["path"] == "return-line-layout.json" for item in changed):
        body["book_declaration"]["layout"]["state"] = "unstable"
        body["book_declaration"]["declared"] = False
    if any(item["path"] == f"{door_name}/01.md" for item in changed):
        page = body["book_declaration"]["door"].get("page")
        if isinstance(page, dict):
            page["state"] = "unstable"
        body["book_declaration"]["declared"] = False
    blank_validity(mod, body)
    body["coherent"] = False
    body["decode"] = None
    body["final_check"] = "changed"
    body["read_error"] = None
    return annotate(body)


def inspect(code_root: Path, book: Path, *, read_bytes=None, code_text: str | None = None, book_text: str | None = None) -> dict:
    mod = pass01()
    reader = mod.default_read if read_bytes is None else read_bytes
    code_text = str(code_root) if code_text is None else code_text
    book_text = str(book) if book_text is None else book_text
    try:
        pre = mod.read_identity(code_root, DISPATCHER_REL, reader)
    except OSError as exc:
        return unreadable_observation(mod, code_root, book, code_text, book_text, exc, reader)
    if pre["state"] == "file" and isinstance(pre.get("data"), bytes):
        try:
            pre["data"].decode("utf-8")
        except UnicodeDecodeError as exc:
            return encoding_observation(mod, code_root, book, code_text, book_text, pre, exc, reader)
    try:
        body = mod.inspect(code_root, book, read_bytes=reader, code_text=code_text, book_text=book_text)
    except UnicodeDecodeError as exc:
        try:
            again = mod.read_identity(code_root, DISPATCHER_REL, reader)
            if isinstance(again.get("data"), bytes):
                again["data"].decode("utf-8")
        except UnicodeDecodeError as second:
            return encoding_observation(mod, code_root, book, code_text, book_text, again, second, reader)
        except OSError:
            raise exc
        raise
    except OSError as exc:
        return unreadable_observation(mod, code_root, book, code_text, book_text, exc, reader)
    body = revalidate(mod, body, code_root, book, reader)
    if pre["sha256"] != body["dispatcher"].get("sha256_final") and pre["state"] == "file" and body["final_check"] == "matched":
        body["changed_paths"] = body["changed_paths"] + [{
            "after_sha256": body["dispatcher"].get("sha256_final"),
            "after_state": body["dispatcher"]["state"],
            "before_sha256": pre["sha256"],
            "before_state": pre["state"],
            "path": DISPATCHER_REL,
            "root": "code",
        }]
        body["dispatcher"]["state"] = "unstable"
        blank_validity(mod, body)
        body["coherent"] = False
        body["final_check"] = "changed"
    return body


def project_text(body: dict) -> str:
    mod = pass01()
    base = mod.project_text(body)
    return base + f"coherent: {str(body['coherent']).lower()}\nfinal_check: {body['final_check']}\n"


def dump(body: dict) -> str:
    return pass01().dump(body)


def main(argv: list[str] | None = None) -> int:
    try:
        mod = pass01()
    except RuntimeError as exc:
        sys.stderr.buffer.write(f"refuse: {exc}\n".encode("utf-8"))
        return 2
    try:
        chosen = list(sys.argv[1:] if argv is None else argv)
        code_text, book_text, text = mod.parse_args(chosen)
        code_root = mod.require_dir(code_text, "code root")
        book = mod.require_dir(book_text, "book")
        body = inspect(code_root, book, code_text=code_text, book_text=book_text)
        sys.stdout.buffer.write(dump(body).encode("utf-8"))
        if text:
            sys.stdout.buffer.write(project_text(body).encode("utf-8"))
        return 0
    except mod.Refuse as exc:
        sys.stderr.buffer.write(f"refuse: {exc.message}\n".encode("utf-8"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
