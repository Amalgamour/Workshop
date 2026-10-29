"""Bounded desk-state record and derived Prime view (0508.return-capture/05.19).

  python -B desk_state.py view --input ABS [--json] [--out DIR] [--candidate ABS]
  python -B desk_state.py revise --record ABS --expected SHA256 --submission ABS --out ABS

Standard library only. Pinned backends are subprocesses, launched only after pin
checks. This module selects, releases, accepts, completes, and dispatches nothing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "desk-state/1"
VIEW_SCHEMA = "desk-view/1"
AUTHORITY = "none; this view selects, releases, accepts, completes and dispatches nothing"
HANDOFF_KIND = "recorded-prime-intent"

HARD_MAX_SOURCES = 32
HARD_MAX_SOURCE_BYTES = 262144
HARD_MAX_TOTAL_BYTES = 1048576
HARD_MAX_OUTPUT_BYTES = 1048576

LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MEMBER = re.compile(r"^01\d\d\.[a-z0-9][a-z0-9.-]*$")
REL_PATH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
STATUS4 = ("recorded", "pending", "absent", "unknown")
PROTECTED = (
    "00.kernel/00.live.md",
    "00.kernel/00.00.10.work/0401.goal/06.01.md",
)
PINS = {
    "batch_observe": (
        "labs/batch-observation-pass01/batch_observe.py",
        "8bea18171b723650e8c0b07f5de334d2c5fd004c5d65c4fa8c4b85cf0bc830d4",
    ),
    "return_inspect": (
        "labs/return-capture-pass01/return_inspect.py",
        "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
    ),
    "return_capture": (
        "labs/return-capture-pass01/return_capture.py",
        "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
    ),
    "state_projection": (
        "labs/state-projection-pass01/state_projection.py",
        "b349da5cef5178296a069c354002a600ba4e168c2710aa5d87789724d4951ecb",
    ),
    "prime_brief": (
        "labs/prime-brief-pass01/prime_brief.py",
        "302ed832d2fa955a591420f13d3b22ce91e4a7669c69a778d443fc82627580d7",
    ),
}
RECORD_KEYS = {
    "schema", "desk", "book", "goal", "milestone", "lanes", "blockers", "handoff",
    "pages", "members", "coordination", "uninspected", "legacy", "tools", "bounds",
    "roots", "revision", "custody",
}
COORD_KEYS = {
    "label", "batch_id", "source_sha256", "release", "claim", "claim_actor",
    "candidate", "review", "publication",
}
REVIEW_KEYS = {"member", "receipt_sha256", "disposition", "terminal", "reviewer", "followup"}


class Refusal(Exception):
    pass


def need(cond: bool, message: str) -> None:
    if not cond:
        raise Refusal(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(data: bytes, label: str):
    def pairs(seq):
        out = {}
        for key, value in seq:
            need(key not in out, f"{label}: duplicate key {key}")
            out[key] = value
        return out

    def constant(name):
        raise Refusal(f"{label}: nonfinite number {name}")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refusal(f"{label}: not UTF-8") from None
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except Refusal:
        raise
    except json.JSONDecodeError as exc:
        raise Refusal(f"{label}: invalid JSON ({exc.msg})") from None


def is_str(value) -> bool:
    return isinstance(value, str)


def opt_str(value) -> bool:
    return value is None or isinstance(value, str)


def exact(obj, keys: set[str], where: str) -> None:
    need(isinstance(obj, dict), f"{where} must be an object")
    need(set(obj) == keys, f"{where} keys must be exactly {sorted(keys)}")


def bounded_text(value, where: str, limit: int) -> None:
    need(is_str(value) and value != "" and len(value) <= limit, f"{where} must be a non-empty string up to {limit}")


def reparse_point(path: str) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    attrs = getattr(info, "st_file_attributes", 0) or 0
    return bool(attrs & 0x400) or stat.S_ISLNK(info.st_mode)


def reject_reparse_chain(path: str) -> None:
    current = os.path.abspath(path)
    while True:
        if os.path.lexists(current) and reparse_point(current):
            raise Refusal(f"path is a link: {path}")
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent


def plain_file(path: str) -> bytes:
    reject_reparse_chain(path)
    need(os.path.isfile(path), f"not a file: {path}")
    info = os.lstat(path)
    need(stat.S_ISREG(info.st_mode), f"not a regular file: {path}")
    with open(path, "rb") as handle:
        return handle.read()


def plain_dir(path: str, label: str) -> None:
    need(os.path.isabs(path), f"{label} must be absolute")
    need(not path.startswith("\\\\"), f"{label} must not be a UNC path")
    reject_reparse_chain(path)
    need(os.path.isdir(path), f"{label} must be a directory")


def relative_path(value, where: str) -> str:
    need(is_str(value) and REL_PATH.fullmatch(value) is not None, f"{where} is not a safe relative path")
    parts = value.split("/")
    need(".." not in parts and "." not in parts, f"{where} has an unsafe segment")
    return value


def within(root: str, path: str) -> bool:
    root_s = os.path.normcase(os.path.abspath(root))
    path_s = os.path.normcase(os.path.abspath(path))
    try:
        return os.path.commonpath([root_s, path_s]) == root_s
    except ValueError:
        return False


def protected(repository: str, path: str) -> bool:
    if not within(repository, path):
        return False
    rel = os.path.relpath(os.path.abspath(path), os.path.abspath(repository)).replace("\\", "/")
    return rel in PROTECTED


def citation(obj, where: str, repository: str) -> None:
    exact(obj, {"repository", "path", "commit", "sha256", "note"}, where)
    need(obj["repository"] == repository, f"{where}.repository must be the record repository")
    relative_path(obj["path"], f"{where}.path")
    need(isinstance(obj["commit"], str) and HEX40.fullmatch(obj["commit"]) is not None, f"{where}.commit must be 40 hex")
    need(isinstance(obj["sha256"], str) and HEX64.fullmatch(obj["sha256"]) is not None, f"{where}.sha256 must be 64 hex")
    need(is_str(obj["note"]) and len(obj["note"]) <= 400, f"{where}.note must be a string up to 400")


def evidence_list(value, where: str, repository: str) -> None:
    need(isinstance(value, list), f"{where} must be a list")
    for index, item in enumerate(value):
        citation(item, f"{where}[{index}]", repository)


def check_review(review, where: str) -> None:
    if review is None:
        return
    exact(review, REVIEW_KEYS, where)
    need(isinstance(review["member"], str) and MEMBER.fullmatch(review["member"]) is not None, f"{where}.member is not a member name")
    need(isinstance(review["receipt_sha256"], str) and HEX64.fullmatch(review["receipt_sha256"]) is not None, f"{where}.receipt_sha256 is not 64 hex")
    need(review["disposition"] in ("accepted", "held", "correction-required"), f"{where}.disposition is not a known value")
    need(review["terminal"] in ("completed", None), f"{where}.terminal must be completed or null")
    need(isinstance(review["reviewer"], str) and LABEL.fullmatch(review["reviewer"]) is not None, f"{where}.reviewer must be a label")
    need(opt_str(review["followup"]), f"{where}.followup must be a string or null")


def check_coordination(item, where: str) -> None:
    exact(item, COORD_KEYS, where)
    need(item["label"] == "SUPPLIED", f"{where}.label must be SUPPLIED")
    bounded_text(item["batch_id"], f"{where}.batch_id", 200)
    need(isinstance(item["source_sha256"], str) and HEX64.fullmatch(item["source_sha256"]) is not None, f"{where}.source_sha256 must be 64 hex")
    need(item["release"] in STATUS4 and item["claim"] in STATUS4, f"{where} release or claim is not a known value")
    need(opt_str(item["claim_actor"]) and (item["claim_actor"] is None or len(item["claim_actor"]) <= 200), f"{where}.claim_actor is not usable")
    need(item["candidate"] is None or (isinstance(item["candidate"], str) and MEMBER.fullmatch(item["candidate"]) is not None), f"{where}.candidate must be null or a member")
    check_review(item["review"], f"{where}.review")
    pub = item["publication"]
    exact(pub, {"status", "ref", "commit"}, f"{where}.publication")
    need(pub["status"] in ("unknown", "at-ref"), f"{where}.publication.status is not a known value")
    need(opt_str(pub["ref"]) and (pub["ref"] is None or len(pub["ref"]) <= 200), f"{where}.publication.ref is not usable")
    need(pub["commit"] is None or (isinstance(pub["commit"], str) and HEX40.fullmatch(pub["commit"]) is not None), f"{where}.publication.commit must be 40 hex or null")


def validate(doc) -> None:
    exact(doc, RECORD_KEYS, "record")
    need(doc["schema"] == SCHEMA, "record: unsupported schema")
    need(isinstance(doc["desk"], str) and LABEL.fullmatch(doc["desk"]) is not None, "desk must be a label")
    need(isinstance(doc["book"], str) and LABEL.fullmatch(doc["book"]) is not None, "book must be a label")
    exact(doc["goal"], {"statement", "evidence"}, "goal")
    bounded_text(doc["goal"]["statement"], "goal.statement", 2000)
    exact(doc["milestone"], {"statement", "evidence"}, "milestone")
    bounded_text(doc["milestone"]["statement"], "milestone.statement", 2000)
    exact(doc["roots"], {"repository", "tools", "members_book", "output"}, "roots")
    for key in ("repository", "tools", "members_book", "output"):
        plain_dir(doc["roots"][key], f"roots.{key}")
    repository = doc["roots"]["repository"]
    evidence_list(doc["goal"]["evidence"], "goal.evidence", repository)
    evidence_list(doc["milestone"]["evidence"], "milestone.evidence", repository)
    need(isinstance(doc["pages"], list) and doc["pages"], "pages must be a non-empty list")
    need(isinstance(doc["lanes"], list) and doc["lanes"], "lanes must be a non-empty list")
    page_ids = []
    for index, page in enumerate(doc["pages"]):
        exact(page, {"id", "repository", "path", "commit", "observation"}, f"pages[{index}]")
        need(isinstance(page["id"], str) and LABEL.fullmatch(page["id"]) is not None, f"pages[{index}].id must be a label")
        need(page["id"] not in page_ids, f"duplicate page id {page['id']}")
        page_ids.append(page["id"])
        need(page["repository"] == repository, f"pages[{index}].repository must be the record repository")
        relative_path(page["path"], f"pages[{index}].path")
        need(page["observation"] in ("git-blob", "live-file"), f"pages[{index}].observation must be git-blob or live-file")
        if page["observation"] == "git-blob":
            need(isinstance(page["commit"], str) and HEX40.fullmatch(page["commit"]) is not None, f"pages[{index}].commit must be 40 hex")
        else:
            need(page["commit"] is None, f"pages[{index}].commit must be null for a live-file observation")
    for index, lane in enumerate(doc["lanes"]):
        exact(lane, {"id", "page_id", "worker", "task"}, f"lanes[{index}]")
        need(isinstance(lane["id"], str) and LABEL.fullmatch(lane["id"]) is not None, f"lanes[{index}].id must be a label")
        need(lane["page_id"] in page_ids, f"lanes[{index}].page_id is not a declared page")
        need(lane["worker"] is None or (is_str(lane["worker"]) and 0 < len(lane["worker"]) <= 80), f"lanes[{index}].worker must be null or a short label")
        bounded_text(lane["task"], f"lanes[{index}].task", 500)
    need(len({lane["id"] for lane in doc["lanes"]}) == len(doc["lanes"]), "duplicate lane id")
    need(isinstance(doc["blockers"], list), "blockers must be a list")
    blocker_ids = []
    for index, blocker in enumerate(doc["blockers"]):
        exact(blocker, {"id", "statement", "status", "evidence"}, f"blockers[{index}]")
        need(isinstance(blocker["id"], str) and LABEL.fullmatch(blocker["id"]) is not None, f"blockers[{index}].id must be a label")
        need(blocker["id"] not in blocker_ids, f"duplicate blocker id {blocker['id']}")
        blocker_ids.append(blocker["id"])
        bounded_text(blocker["statement"], f"blockers[{index}].statement", 2000)
        need(blocker["status"] in ("unresolved", "recorded"), f"blockers[{index}].status is not a known value")
        evidence_list(blocker["evidence"], f"blockers[{index}].evidence", repository)
    exact(doc["handoff"], {"statement", "author", "evidence"}, "handoff")
    bounded_text(doc["handoff"]["statement"], "handoff.statement", 2000)
    bounded_text(doc["handoff"]["author"], "handoff.author", 80)
    evidence_list(doc["handoff"]["evidence"], "handoff.evidence", repository)
    need(isinstance(doc["members"], list), "members must be a list")
    member_names = []
    for index, member in enumerate(doc["members"]):
        exact(member, {"name", "role"}, f"members[{index}]")
        need(isinstance(member["name"], str) and MEMBER.fullmatch(member["name"]) is not None, f"members[{index}].name is not a member name")
        need(member["role"] in ("declared", "pointer"), f"members[{index}].role is not a known value")
        need(member["name"] not in member_names, f"duplicate member {member['name']}")
        member_names.append(member["name"])
    need(isinstance(doc["coordination"], list), "coordination must be a list")
    batches = []
    for index, item in enumerate(doc["coordination"]):
        check_coordination(item, f"coordination[{index}]")
        need(item["batch_id"] not in batches, f"duplicate coordination for {item['batch_id']}")
        batches.append(item["batch_id"])
    need(isinstance(doc["uninspected"], list), "uninspected must be a list")
    for index, item in enumerate(doc["uninspected"]):
        exact(item, {"label", "reason"}, f"uninspected[{index}]")
        bounded_text(item["label"], f"uninspected[{index}].label", 200)
        bounded_text(item["reason"], f"uninspected[{index}].reason", 400)
    citation(doc["legacy"], "legacy", repository)
    exact(doc["tools"], set(PINS), "tools")
    for name in PINS:
        exact(doc["tools"][name], {"path", "sha256"}, f"tools.{name}")
        need(is_str(doc["tools"][name]["path"]) and os.path.isabs(doc["tools"][name]["path"]), f"tools.{name}.path must be absolute")
        need(isinstance(doc["tools"][name]["sha256"], str) and HEX64.fullmatch(doc["tools"][name]["sha256"]) is not None, f"tools.{name}.sha256 must be 64 hex")
    exact(doc["bounds"], {"max_sources", "max_source_bytes", "max_total_bytes", "max_output_bytes"}, "bounds")
    caps = {
        "max_sources": HARD_MAX_SOURCES,
        "max_source_bytes": HARD_MAX_SOURCE_BYTES,
        "max_total_bytes": HARD_MAX_TOTAL_BYTES,
        "max_output_bytes": HARD_MAX_OUTPUT_BYTES,
    }
    for key, cap in caps.items():
        value = doc["bounds"][key]
        need(type(value) is int and 1 <= value <= cap, f"bounds.{key} must be an integer from 1 through {cap}")
    exact(doc["revision"], {"reason", "authorizing", "predecessor"}, "revision")
    bounded_text(doc["revision"]["reason"], "revision.reason", 2000)
    bounded_text(doc["revision"]["authorizing"], "revision.authorizing", 400)
    pred = doc["revision"]["predecessor"]
    need(pred is None or (isinstance(pred, str) and HEX64.fullmatch(pred) is not None), "revision.predecessor must be null or 64 hex")
    need(doc["custody"] in ("inspect-named-members", "commit-facts-only"), "custody is not a known value")
    declared = len(doc["pages"]) + len(doc["members"]) + len(doc["goal"]["evidence"]) + len(doc["milestone"]["evidence"])
    declared += len(doc["handoff"]["evidence"]) + 1
    for blocker in doc["blockers"]:
        declared += len(blocker["evidence"])
    need(declared <= doc["bounds"]["max_sources"], "declared sources exceed bounds.max_sources")


def check_pins(doc) -> dict[str, str]:
    tools_root = doc["roots"]["tools"]
    paths = {}
    for name, (rel, pin) in PINS.items():
        recorded = doc["tools"][name]
        expected = os.path.abspath(os.path.join(tools_root, *rel.split("/")))
        given = os.path.abspath(recorded["path"])
        need(os.path.normcase(given) == os.path.normcase(expected), f"tools.{name} path is not the pinned path")
        data = plain_file(given)
        got = sha256_bytes(data)
        need(got == pin and got == recorded["sha256"], f"tools.{name} pin mismatch (sha256 {got}); nothing was launched")
        paths[name] = given
    return paths


def source_count_overflow(doc, extra: int = 0) -> None:
    declared = len(doc["pages"]) + len(doc["members"]) + extra
    declared += len(doc["goal"]["evidence"]) + len(doc["milestone"]["evidence"]) + len(doc["handoff"]["evidence"]) + 1
    for blocker in doc["blockers"]:
        declared += len(blocker["evidence"])
    need(declared <= doc["bounds"]["max_sources"], "source count exceeds bounds.max_sources; nothing further was launched")


def run_checked(cmd: list[str], timeout: int) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        return subprocess.run(cmd, capture_output=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        if not isinstance(stdout, bytes):
            stdout = str(stdout).encode("utf-8", "replace")
        if not isinstance(stderr, bytes):
            stderr = str(stderr).encode("utf-8", "replace")
        return subprocess.CompletedProcess(cmd, 124, stdout, stderr + b"\ntimeout\n")


def live_join(root: str, rel: str) -> str:
    return os.path.abspath(os.path.join(root, *rel.split("/")))


def refuse_linked(root: str, rel: str) -> None:
    live = live_join(root, rel)
    need(within(root, live), f"{rel} escapes the repository")
    reject_reparse_chain(live)


def read_citation(item, bounds) -> dict:
    rel = item["path"]
    refuse_linked(item["repository"], rel)
    cmd = ["git", "-C", item["repository"], "cat-file", "blob", "--end-of-options", f"{item['commit']}:{rel}"]
    proc = run_checked(cmd, 30)
    result = {
        "path": rel,
        "commit": item["commit"],
        "expected_sha256": item["sha256"],
        "note": item["note"],
        "command": cmd,
        "exit": proc.returncode,
    }
    if proc.returncode != 0:
        result.update(status="unverified", sha256=None, bytes=None, reason="git cat-file failed")
        return result
    size = len(proc.stdout)
    need(size <= bounds["max_source_bytes"], f"citation {rel} exceeds max_source_bytes")
    digest = sha256_bytes(proc.stdout)
    if digest != item["sha256"]:
        result.update(status="mismatch", sha256=digest, bytes=size, reason="blob hash differs from the record")
        return result
    result.update(status="match", sha256=digest, bytes=size, reason=None)
    return result


def observe_one(doc, page, tool: str) -> dict:
    refuse_linked(page["repository"], page["path"])
    if page["observation"] == "live-file":
        live = live_join(page["repository"], page["path"])
        data = plain_file(live)
        need(len(data) <= doc["bounds"]["max_source_bytes"], f"pages.{page['id']} exceeds max_source_bytes")
        cmd = [sys.executable, "-B", tool, "observe", "--json", "--repo", page["repository"], "--path", page["path"], "--live"]
    else:
        cmd = [sys.executable, "-B", tool, "observe", "--json", "--repo", page["repository"], "--commit", page["commit"], "--path", page["path"]]
    proc = run_checked(cmd, 120)
    shown = [sys.executable, "-B", tool, *cmd[3:]]
    row = {"page_id": page["id"], "command": shown, "exit": proc.returncode, "stderr": proc.stderr.decode("utf-8", "replace")}
    if proc.returncode == 2 or proc.returncode == 124:
        row.update(status="observation-failed", observation=None, reason=row["stderr"].strip() or "reader failed")
        return row
    try:
        observation = strict_json(proc.stdout, f"reader {page['id']}")
    except Refusal as exc:
        row.update(status="observation-failed", observation=None, reason=str(exc))
        return row
    if not isinstance(observation, dict) or observation.get("schema") != "batch-observation/1":
        row.update(status="observation-failed", observation=None, reason="reader output is not batch-observation/1")
        return row
    source = observation.get("source") if isinstance(observation.get("source"), dict) else {}
    size = source.get("bytes")
    need(type(size) is int and size <= doc["bounds"]["max_source_bytes"], f"pages.{page['id']} reader bytes exceed max_source_bytes")
    row.update(status="observed", observation=observation, reason=None)
    return row


def pointer_names(observation) -> list[str]:
    found = []
    if not isinstance(observation, dict):
        return found
    for pointer in observation.get("pointers") or []:
        if not isinstance(pointer, dict):
            continue
        for member in pointer.get("members") or []:
            if isinstance(member, dict) and isinstance(member.get("name"), str) and member["name"] not in found:
                found.append(member["name"])
    return found


def batch_of(observation) -> str | None:
    page = observation.get("page") if isinstance(observation, dict) else None
    if not isinstance(page, dict):
        return None
    if not all(isinstance(page.get(key), str) for key in ("book", "page", "batch")):
        return None
    return f"{page['page']}/{page['batch']}"


def inspect_one(book: str, member: str, tool: str) -> dict:
    cmd = [sys.executable, "-B", tool, "inspect", "--book", book, "--member", member, "--json"]
    proc = run_checked(cmd, 120)
    row = {"member": member, "command": cmd, "exit": proc.returncode, "stderr": proc.stderr.decode("utf-8", "replace")}
    try:
        report = strict_json(proc.stdout, f"inspect {member}")
    except Refusal as exc:
        row.update(status="inspection-failed", report=None, reason=str(exc))
        return row
    if not isinstance(report, dict):
        row.update(status="inspection-failed", report=None, reason="inspector output is not an object")
        return row
    row.update(status="inspected", report=report, reason=None)
    return row


def write_exclusive(path: str, data: bytes) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        handle = os.open(path, flags)
    except FileExistsError:
        raise Refusal(f"output already exists: {path}") from None
    try:
        os.write(handle, data)
    except OSError as exc:
        raise Refusal(f"output write failed: {exc.strerror}") from None
    finally:
        os.close(handle)


def mark_partial(directory: str, reason: str) -> None:
    marker = os.path.join(directory, "PARTIAL.txt")
    try:
        write_exclusive(marker, (reason + "\n").encode("utf-8"))
    except Refusal:
        return


def refuse_existing_outputs(directory: str, candidate: str | None) -> None:
    for name in ("view.json", "PARTIAL.txt"):
        if os.path.lexists(os.path.join(directory, name)):
            raise Refusal(f"output already exists: {name}")
    if candidate and os.path.lexists(candidate):
        raise Refusal(f"output already exists: {candidate}")


def candidate_text(view: dict) -> str:
    lines = [
        "# DERIVED VIEW",
        "",
        "This file is generated from the desk-state record. It is not an input.",
        "A later render reads the record again. Editing this file changes nothing.",
        "",
        f"Record SHA-256: {view['record']['sha256']}",
        f"Record bytes: {view['record']['bytes']}",
        f"Desk: {view['desk']}",
        f"Book: {view['book']}",
        f"Elected current task: none",
        "",
        "## Desk goal",
        "",
        view["goal"]["statement"],
        "",
        "## Milestone",
        "",
        view["milestone"]["statement"],
        "",
        "## Source cuts",
        "",
    ]
    for source in view["sources"]:
        commit = source.get("commit") or "live-file"
        lines.append(f"- {source['path']} {commit} {source.get('sha256') or 'unknown'}")
    lines += ["", "## Live observation times", ""]
    times = view["live_times"]
    lines.append("none" if not times else "\n".join(f"- {item}" for item in times))
    lines += ["", "## Lanes", ""]
    for lane in view["lanes"]:
        worker = "unrecorded" if lane["worker"] is None else lane["worker"]
        follow = f" Follow-up: {lane['followup']}." if lane.get("followup") else ""
        lines.append(f"- {lane['id']}: {lane['lifecycle']}; worker {worker}; {lane['task']}{follow}")
    lines += ["", "## Recorded next step", "", view["handoff"]["statement"], "", "## Unresolved decisions", ""]
    unresolved = [item for item in view["blockers"] if item["status"] == "unresolved"]
    lines.append("none" if not unresolved else "\n".join(f"- {item['id']}: {item['statement']}" for item in unresolved))
    lines += ["", "## Known gaps", ""]
    gaps = view["unknowns"] + [f"{item['label']}: {item['reason']}" for item in view["uninspected"]]
    lines.append("none" if not gaps else "\n".join(f"- {item}" for item in gaps))
    lines += ["", f"Authority: {AUTHORITY}", ""]
    return "\n".join(lines)


def render_text(view: dict) -> str:
    lines = [
        f"Desk {view['desk']}  book {view['book']}",
        f"Record {view['record']['sha256']}",
        "Elected current task: none",
        "",
        "Desk goal",
        view["goal"]["statement"],
        "",
        "Milestone",
        view["milestone"]["statement"],
        "",
        "Lanes",
    ]
    for lane in view["lanes"]:
        worker = "unrecorded" if lane["worker"] is None else f"label {lane['worker']}"
        lines.append(f"- {lane['id']}  {lane['lifecycle']}  worker {worker}")
        lines.append(f"  task: {lane['task']}")
        if lane.get("batch_id"):
            lines.append(f"  batch: {lane['batch_id']}")
        if lane.get("unprojected_reason"):
            lines.append(f"  unknown: {lane['unprojected_reason']}")
        for item in lane.get("attention") or []:
            lines.append(f"  attention: {item}")
        if lane.get("followup"):
            lines.append(f"  followup: {lane['followup']}")
    lines += ["", "Returns"]
    returns = view["returns"]
    if not any(returns.values()):
        lines.append("- none")
    for key, items in returns.items():
        for item in items:
            lines.append(f"- {key}: {item.get('id') or '(no page)'} {item.get('lifecycle') or ''}")
            if item.get("followup"):
                lines.append(f"  followup: {item['followup']}")
            if item.get("reason"):
                lines.append(f"  {item['reason']}")
    lines += ["", "Unresolved decisions"]
    unresolved = [item for item in view["blockers"] if item["status"] == "unresolved"]
    lines.append("- none" if not unresolved else "\n".join(f"- {item['id']}: {item['statement']}" for item in unresolved))
    lines += ["", "Recorded next step", view["handoff"]["statement"], ""]
    lines.append("Unknowns")
    lines.append("- none" if not view["unknowns"] else "\n".join(f"- {item}" for item in view["unknowns"]))
    lines += ["", f"Attention count: {len(view['attention'])}", f"Authority: {AUTHORITY}", ""]
    return "\n".join(lines)


def lane_row(lane, observed, brief_item, unprojected) -> dict:
    worker = lane["worker"]
    row = {
        "id": lane["id"],
        "page_id": lane["page_id"],
        "worker": worker,
        "worker_meaning": "unrecorded" if worker is None else "label",
        "task": lane["task"],
        "batch_id": None,
        "lifecycle": "unknown",
        "unprojected_reason": None,
        "attention": [],
        "followup": None,
        "reader_ambiguities": [],
        "reader_attention": [],
        "release_raw": None,
        "claim_raw": None,
        "source": None,
    }
    if observed is None or observed["status"] != "observed":
        row["lifecycle"] = "observation-failed"
        row["unprojected_reason"] = None if observed is None else observed.get("reason")
        return row
    observation = observed["observation"]
    source = observation.get("source") if isinstance(observation.get("source"), dict) else {}
    row["source"] = {key: source.get(key) for key in ("kind", "path", "commit", "sha256", "bytes")}
    row["reader_ambiguities"] = list(observation.get("ambiguities") or [])
    row["reader_attention"] = list(observation.get("attention") or [])
    assignment = observation.get("assignment") if isinstance(observation.get("assignment"), dict) else {}
    row["release_raw"] = assignment.get("release_raw")
    row["claim_raw"] = assignment.get("claim_raw")
    row["batch_id"] = batch_of(observation)
    if row["batch_id"] is None:
        row["lifecycle"] = "unprojected"
        row["unprojected_reason"] = "page unidentified: reader gives no book/page/batch"
        return row
    if unprojected is not None:
        row["lifecycle"] = "unprojected"
        row["unprojected_reason"] = unprojected.get("reason")
        return row
    if brief_item is not None:
        row["lifecycle"] = brief_item.get("lifecycle") or "unknown"
        row["attention"] = list(brief_item.get("attention") or [])
        row["followup"] = brief_item.get("followup")
        return row
    row["lifecycle"] = "unknown"
    row["unprojected_reason"] = "no brief item for this lane"
    return row


def assemble(doc, record_path: str, record_sha: str, record_bytes: int, observations, inspections, citations, brief, commands, not_applied) -> dict:
    by_page = {row["page_id"]: row for row in observations}
    projected = {}
    projection = (brief or {}).get("projection") if isinstance(brief, dict) else None
    if isinstance(projection, dict):
        for item in projection.get("batches") or []:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                projected[item["id"]] = item
    unprojected = {}
    lists = {key: [] for key in (
        "awaiting_review", "correction_or_held", "completed_fixtures", "conflicts",
        "other_open", "unreleased", "unprojected",
    )}
    if isinstance(brief, dict):
        for key in lists:
            lists[key] = list((brief.get("brief") or {}).get(key) or [])
        for item in lists["unprojected"]:
            if isinstance(item, dict):
                unprojected[item.get("id")] = item
    lanes = []
    for lane in doc["lanes"]:
        observed = by_page.get(lane["page_id"])
        batch_id = batch_of(observed["observation"]) if observed and observed.get("observation") else None
        lanes.append(lane_row(lane, observed, projected.get(batch_id), unprojected.get(batch_id)))
    unknowns = []
    attention = []
    quiet = {"released", "completed"}
    for row in lanes:
        if row["lifecycle"] in ("unprojected", "observation-failed", "unknown") or row["unprojected_reason"]:
            unknowns.append(f"{row['id']}: {row['unprojected_reason'] or row['lifecycle']}")
        if row["lifecycle"] not in quiet:
            attention.append(f"{row['id']}: {row['lifecycle']}")
        attention.extend(f"{row['id']}: {item}" for item in row["attention"])
    for item in lists["unprojected"]:
        if isinstance(item, dict):
            label = item.get("id") or ((item.get("source_ref") or {}).get("path") if isinstance(item.get("source_ref"), dict) else None) or "page"
            unknowns.append(f"{label}: {item.get('reason')}")
    if brief is None:
        for row in observations:
            if row["status"] == "observed" and batch_of(row.get("observation")) is None:
                path = ((row.get("observation") or {}).get("source") or {}).get("path")
                unknowns.append(f"{path}: page unidentified: reader gives no book/page/batch")
    for row in observations:
        if row["status"] != "observed":
            if not any(lane["page_id"] == row["page_id"] for lane in doc["lanes"]):
                unknowns.append(f"{row['page_id']}: {row.get('reason') or 'observation-failed'}")
    for item in citations:
        if item["status"] != "match":
            unknowns.append(f"citation {item['path']}: {item['reason']}")
    for item in not_applied:
        unknowns.append(item)
    named = []
    for row in observations:
        if row["status"] == "observed":
            named.extend(pointer_names(row["observation"]))
    declared = [item["name"] for item in doc["members"]]
    for name in named:
        if MEMBER.fullmatch(name) is None:
            attention.append(f"pointer member outside member form: {name}")
    for name in declared:
        if name not in named:
            attention.append(f"declared member not named by a reader pointer: {name}")
    if doc["custody"] == "commit-facts-only" and declared:
        unknowns.append("declared members were not inspected; custody mode is commit-facts-only")
    for row in inspections:
        report = row.get("report") or {}
        status = report.get("status") if isinstance(report, dict) else None
        if row["status"] != "inspected":
            unknowns.append(f"inspect {row['member']}: {row.get('reason')}")
        elif status != "complete":
            attention.append(f"inspect {row['member']}: {status}")
        else:
            capture = report.get("capture") or {}
            if capture.get("retrospective") is True:
                attention.append(f"inspect {row['member']}: retrospective capture")
    for blocker in doc["blockers"]:
        if blocker["status"] == "unresolved":
            attention.append(f"unresolved {blocker['id']}: {blocker['statement']}")
    live_times = []
    sources = []
    for row in observations:
        observation = row.get("observation") or {}
        source = observation.get("source") if isinstance(observation, dict) else None
        if not isinstance(source, dict):
            sources.append({"page_id": row["page_id"], "path": None, "commit": None, "sha256": None, "kind": None})
            continue
        sources.append({
            "page_id": row["page_id"],
            "path": source.get("path"),
            "commit": source.get("commit"),
            "sha256": source.get("sha256"),
            "kind": source.get("kind"),
            "bytes": source.get("bytes"),
        })
        if source.get("kind") == "live-file":
            live_times.append(f"{source.get('path')} {source.get('live_observed_at')}")
    for row in inspections:
        report = row.get("report") or {}
        capture = report.get("capture") if isinstance(report, dict) else None
        if isinstance(capture, dict) and capture.get("captured_at"):
            live_times.append(f"{row['member']} captured_at {capture.get('captured_at')}")
    view = {
        "schema": VIEW_SCHEMA,
        "authority": AUTHORITY,
        "elected": None,
        "record": {"path": record_path, "sha256": record_sha, "bytes": record_bytes},
        "desk": doc["desk"],
        "book": doc["book"],
        "goal": {"statement": doc["goal"]["statement"], "evidence": citations_for(doc["goal"]["evidence"], citations)},
        "milestone": {"statement": doc["milestone"]["statement"], "evidence": citations_for(doc["milestone"]["evidence"], citations)},
        "lanes": lanes,
        "returns": lists,
        "blockers": [
            {"id": item["id"], "statement": item["statement"], "status": item["status"],
             "evidence": citations_for(item["evidence"], citations)}
            for item in doc["blockers"]
        ],
        "handoff": {
            "kind": HANDOFF_KIND,
            "statement": doc["handoff"]["statement"],
            "author": doc["handoff"]["author"],
            "evidence": citations_for(doc["handoff"]["evidence"], citations),
        },
        "legacy": next((item for item in citations if item["path"] == doc["legacy"]["path"] and item["commit"] == doc["legacy"]["commit"]), None),
        "uninspected": list(doc["uninspected"]),
        "unknowns": list(dict.fromkeys(unknowns)),
        "attention": list(dict.fromkeys(attention)),
        "sources": sources,
        "live_times": live_times,
        "raw": {
            "observations": observations,
            "inspections": inspections,
            "citations": citations,
            "brief": brief,
            "commands": commands,
        },
    }
    return view


def citations_for(wanted, citations) -> list:
    found = []
    for item in wanted:
        match = next((row for row in citations if row["path"] == item["path"] and row["commit"] == item["commit"]), None)
        found.append(match or {"path": item["path"], "commit": item["commit"], "status": "missing"})
    return found


def encode_view(view: dict) -> bytes:
    return (json.dumps(view, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def total_bytes(observations, inspections, citations) -> int:
    total = 0
    for row in observations:
        source = ((row.get("observation") or {}).get("source") or {}) if row.get("observation") else {}
        size = source.get("bytes")
        if type(size) is int:
            total += size
    for row in inspections:
        report = row.get("report")
        if report is not None:
            total += len(json.dumps(report).encode("utf-8"))
    for item in citations:
        size = item.get("bytes")
        if type(size) is int:
            total += size
    return total


def build_view(doc, record_path: str, raw: bytes) -> dict:
    paths = check_pins(doc)
    source_count_overflow(doc)
    commands = []
    citations = []
    groups = [doc["goal"]["evidence"], doc["milestone"]["evidence"], doc["handoff"]["evidence"], [doc["legacy"]]]
    groups.extend(item["evidence"] for item in doc["blockers"])
    for group in groups:
        for item in group:
            citations.append(read_citation(item, doc["bounds"]))
    observations = []
    for page in doc["pages"]:
        observations.append(observe_one(doc, page, paths["batch_observe"]))
        commands.append(observations[-1]["command"])
    pointer_members = []
    for row in observations:
        if row["status"] == "observed":
            for name in pointer_names(row["observation"]):
                if name not in pointer_members:
                    pointer_members.append(name)
    inspect_names = []
    if doc["custody"] == "inspect-named-members":
        for item in doc["members"]:
            inspect_names.append(item["name"])
        for name in pointer_members:
            if MEMBER.fullmatch(name) is not None and name not in inspect_names:
                inspect_names.append(name)
    source_count_overflow(doc, extra=max(0, len(inspect_names) - len(doc["members"])))
    need(total_bytes(observations, [], citations) <= doc["bounds"]["max_total_bytes"], "total source bytes exceed bounds.max_total_bytes")
    inspections = []
    for name in inspect_names:
        inspections.append(inspect_one(doc["roots"]["members_book"], name, paths["return_inspect"]))
        commands.append(inspections[-1]["command"])
    need(total_bytes(observations, inspections, citations) <= doc["bounds"]["max_total_bytes"], "total source bytes exceed bounds.max_total_bytes")
    usable = []
    not_applied = []
    seen_batch = set()
    for row in observations:
        if row["status"] != "observed":
            continue
        observation = row["observation"]
        page = observation.get("page")
        if page is not None and isinstance(page, dict) and page.get("book") not in (None, doc["book"]):
            not_applied.append(f"{row['page_id']}: book {page.get('book')} is outside the record")
            continue
        batch_id = batch_of(observation)
        if batch_id is not None:
            need(batch_id not in seen_batch, f"duplicate observed batch {batch_id}")
            seen_batch.add(batch_id)
        usable.append(row)
    coord_by_batch = {item["batch_id"]: item for item in doc["coordination"]}
    sent_coord = []
    for batch_id, item in coord_by_batch.items():
        if batch_id in seen_batch:
            sent_coord.append(item)
        else:
            not_applied.append(f"coordination for {batch_id} was not applied; that page was not identified")
    brief = None
    identified = [row for row in usable if batch_of(row["observation"]) is not None]
    lanes = []
    for row in identified:
        page = row["observation"]["page"]["page"]
        if page not in lanes:
            lanes.append(page)
    if identified or any(batch_of(row["observation"]) is None for row in usable):
        if not lanes:
            not_applied.append("no identified page; brief was not run")
        else:
            payload = {
                "schema": "prime-brief-input/1",
                "scope": {"book": doc["book"], "lanes": lanes},
                "members_book": doc["roots"]["members_book"] if doc["custody"] == "inspect-named-members" else None,
                "observations": [
                    {"label": "SUPPLIED", "note": "reader stdout at the declared source; not a workflow decision",
                     "observation": row["observation"]}
                    for row in usable
                ],
                "coordination": sent_coord,
            }
            encoded = (json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
            with tempfile.TemporaryDirectory(prefix="desk-state-") as temp:
                target = os.path.join(temp, "brief-input.json")
                with open(target, "wb") as handle:
                    handle.write(encoded)
                cmd = [sys.executable, "-B", paths["prime_brief"], "brief", "--input", target, "--json"]
                if doc["custody"] == "inspect-named-members":
                    cmd.append("--inspect")
                proc = run_checked(cmd, 180)
            shown = [sys.executable, "-B", paths["prime_brief"], "brief", "--input", "<temp>", "--json"]
            if doc["custody"] == "inspect-named-members":
                shown.append("--inspect")
            commands.append(shown)
            text = proc.stdout.decode("utf-8", "replace")
            if proc.returncode == 2 and "not the pinned code" in text:
                raise Refusal(text.strip())
            if proc.returncode == 2:
                not_applied.append("brief refused: " + text.strip())
            else:
                try:
                    brief = strict_json(proc.stdout, "brief")
                except Refusal as exc:
                    not_applied.append(f"brief output unreadable: {exc}")
    view = assemble(
        doc, record_path, sha256_bytes(raw), len(raw), observations, inspections,
        citations, brief, commands, not_applied,
    )
    view["exit"] = 0 if not view["unknowns"] and not view["attention"] else 1
    encoded = encode_view(view)
    need(len(encoded) <= doc["bounds"]["max_output_bytes"], "view exceeds max_output_bytes")
    return view


def output_path(doc, path: str, label: str) -> str:
    need(is_str(path) and os.path.isabs(path), f"{label} must be absolute")
    need(not path.startswith("\\\\"), f"{label} must not be a UNC path")
    need(within(doc["roots"]["output"], path), f"{label} is outside roots.output")
    need(not protected(doc["roots"]["repository"], path), f"{label} is a protected source")
    need(not protected(doc["roots"]["tools"], path), f"{label} is a protected source")
    reject_reparse_chain(path)
    return os.path.abspath(path)


def emit(view: dict, as_json: bool, out_dir: str | None, candidate: str | None, doc) -> int:
    encoded = encode_view(view)
    text = render_text(view).encode("utf-8")
    if out_dir or candidate:
        if out_dir:
            directory = output_path(doc, out_dir, "--out")
            need(os.path.isdir(directory), "--out must be a directory")
        else:
            directory = None
        candidate_abs = output_path(doc, candidate, "--candidate") if candidate else None
        if directory:
            refuse_existing_outputs(directory, candidate_abs)
        elif candidate_abs and os.path.lexists(candidate_abs):
            raise Refusal(f"output already exists: {candidate_abs}")
        if directory:
            try:
                write_exclusive(os.path.join(directory, "view.json"), encoded)
            except Refusal:
                mark_partial(directory, "view.json write failed")
                raise
        if candidate_abs:
            try:
                parent = os.path.dirname(candidate_abs)
                need(os.path.isdir(parent), f"candidate directory is missing: {parent}")
                write_exclusive(candidate_abs, candidate_text(view).encode("utf-8"))
            except Refusal as exc:
                if directory:
                    mark_partial(directory, str(exc))
                raise
    sys.stdout.buffer.write(encoded if as_json else text)
    return view["exit"]


def load_record(path: str) -> tuple[dict, bytes]:
    need(is_str(path) and os.path.isabs(path), "record path must be absolute")
    data = plain_file(path)
    doc = strict_json(data, "record")
    need(isinstance(doc, dict), "record must be an object")
    if doc.get("schema") != SCHEMA:
        raise Refusal("input schema is not desk-state/1")
    validate(doc)
    return doc, data


def cmd_view(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="desk_state.py view", add_help=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("--candidate")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        raise Refusal("view arguments are not usable") from None if code else None
    doc, raw = load_record(args.input)
    view = build_view(doc, os.path.abspath(args.input), raw)
    return emit(view, args.json, args.out, args.candidate, doc)


def cmd_revise(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="desk_state.py revise", add_help=True)
    parser.add_argument("--record", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--submission", required=True)
    parser.add_argument("--out", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        raise Refusal("revise arguments are not usable") from None
    need(HEX64.fullmatch(args.expected or "") is not None, "--expected must be 64 hex")
    current = plain_file(args.record)
    got = sha256_bytes(current)
    need(got == args.expected, "expected hash does not match the record; the record was not written")
    doc, raw = load_record(args.submission)
    need(doc["revision"]["predecessor"] == args.expected, "revision.predecessor must equal the expected record hash")
    check_pins(doc)
    target = output_path(doc, args.out, "--out")
    need(os.path.normcase(os.path.abspath(args.record)) != os.path.normcase(target), "revise will not overwrite the old record")
    need(os.path.normcase(os.path.abspath(args.submission)) != os.path.normcase(target), "revise will not overwrite the submission")
    write_exclusive(target, raw)
    result = {
        "schema": "desk-state-revision/1",
        "wrote": target,
        "sha256": sha256_bytes(raw),
        "predecessor": args.expected,
        "authority": "not a worker command",
    }
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        if not args or args[0] not in ("view", "revise"):
            raise Refusal("command must be view or revise")
        if args[0] == "view":
            return cmd_view(args[1:])
        return cmd_revise(args[1:])
    except Refusal as exc:
        sys.stderr.write(f"refused: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
