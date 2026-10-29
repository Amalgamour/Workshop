"""Assemble one mechanical review packet for one named return.

Custody comes from the pinned inspector and helper. A verified receipt is
custody, not acceptance. This module does not capture, repair, allocate,
route, or decide the next task.
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
from pathlib import Path

HELPER_SHA256 = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
HELPER_BYTES = 45767
INSPECTOR_SHA256 = "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b"
INSPECTOR_BYTES = 11402
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
STATEMENT = (
    "A verified receipt is custody, not acceptance. "
    "Return claims remain claims even when a hash matches. "
    "These checks are not an OS sandbox or a same-user race guarantee."
)
MEMBER_FILE_NAMES = {"return.md", "receipt.json", "manifest.json", "reservation.json"}
PAYLOAD_NAME = re.compile(r"^payload/[0-9]{4}\.blob$")
MEMBER_NAME = re.compile(r"^(\d{4})\.([A-Za-z0-9][A-Za-z0-9._-]{0,63})$")
PASS_NAME = re.compile(r"^05\.\d{2}$")
SOURCE_ID = re.compile(r"^[a-z][a-z0-9-]{0,31}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ROLES = {"builder-claim", "custody", "director-quotation", "supporting"}
CUSTODY_STATUS = {"complete", "reserved", "missing", "incomplete", "refused"}
RESERVED_WINDOWS = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{n}" for n in range(1, 10)),
    *(f"LPT{n}" for n in range(1, 10)),
}
REQUEST_KEYS = {
    "schema",
    "book",
    "member",
    "origin",
    "repo",
    "python",
    "inspector",
    "helper",
    "output",
    "bounds",
    "sources",
}
GIT_BLOB_KEYS = {"id", "kind", "role", "commit", "path", "expect_sha256", "artifact_manifest"}
LIVE_KEYS = {"id", "kind", "role", "path", "expect_sha256", "embed", "artifact_manifest"}
MEMBER_KEYS = {"id", "kind", "role", "name", "expect_sha256", "artifact_manifest"}
TIMEOUT_SECONDS = 60


class Refused(Exception):
    pass


class Partial(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def refuse(message: str) -> None:
    raise Refused(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(value) -> bytes:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
    return (text + "\n").encode("utf-8")


def loads_strict(text: str):
    def reject_constant(name: str):
        refuse(f"nonfinite JSON {name}")

    def pairs(seq):
        obj = {}
        for key, value in seq:
            if not isinstance(key, str):
                refuse("JSON key is not a string")
            if key in obj:
                refuse("duplicate JSON key")
            obj[key] = value
        return obj

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=reject_constant)
    except Refused:
        raise
    except json.JSONDecodeError:
        refuse("invalid JSON")


def is_reparse(path: Path) -> bool:
    info = os.lstat(path)
    attrs = getattr(info, "st_file_attributes", 0) or 0
    if attrs & FILE_ATTRIBUTE_REPARSE_POINT:
        return True
    return stat.S_ISLNK(info.st_mode)


def file_problem(path: Path) -> str | None:
    if not os.path.lexists(path):
        return "missing"
    if is_reparse(path):
        return "link"
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode):
        return "not-regular"
    if info.st_nlink != 1:
        return "link-count"
    return None


def directory_problem(path: Path) -> str | None:
    if not os.path.lexists(path):
        return "missing"
    if is_reparse(path):
        return "link"
    info = os.lstat(path)
    if not stat.S_ISDIR(info.st_mode):
        return "not-directory"
    return None


def exclusive_write(path: Path, data: bytes) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(str(path), flags)
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise OSError("short write")
            view = view[written:]
    finally:
        os.close(fd)


def require_exact(value, keys: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        refuse(f"{label} is not an object")
    got = set(value)
    if got != keys:
        extra = sorted(got - keys)
        missing = sorted(keys - got)
        refuse(f"{label} keys extra={extra} missing={missing}")
    return value


def require_int(value, label: str, low: int, high: int) -> int:
    if type(value) is not int:
        refuse(f"{label} is not an integer")
    if value < low or value > high:
        refuse(f"{label} is outside {low}..{high}")
    return value


def require_text(value, label: str, limit: int = 200) -> str:
    if not isinstance(value, str) or value == "" or len(value) > limit:
        refuse(f"{label} is empty or too long")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        refuse(f"{label} has control characters")
    if "\\" in value or "/" in value:
        refuse(f"{label} has a slash")
    return value


def absolute_path(value, label: str) -> Path:
    if not isinstance(value, str) or not os.path.isabs(value):
        refuse(f"{label} must be absolute")
    path = Path(value)
    if any(part == ".." for part in path.parts):
        refuse(f"{label} has ..")
    return path


def ancestor_link(path: Path) -> str | None:
    if not path.is_absolute():
        refuse("path is not absolute")
    current = Path(path.anchor)
    for part in path.parts[1:]:
        if part in ("", ".", ".."):
            refuse(f"path escape: {path}")
        current = current / part
        if not os.path.lexists(current):
            return None
        try:
            if is_reparse(current):
                return str(current)
        except OSError as exc:
            refuse(f"filesystem: {type(exc).__name__}: {exc.strerror or exc}")
    return None


def relative_problem(value: str) -> str | None:
    if not isinstance(value, str) or value == "" or len(value) > 4096:
        return "path is empty or too long"
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        return "path has control characters"
    if "\\" in value or ":" in value or value.startswith("/"):
        return "path is unsafe"
    for part in value.split("/"):
        if part in ("", ".", "..") or part.endswith(" ") or part.endswith("."):
            return "path has an unsafe segment"
        if part.split(".", 1)[0].upper() in RESERVED_WINDOWS:
            return "path is a reserved windows name"
    return None


def require_relative(value, label: str) -> str:
    problem = relative_problem(value if isinstance(value, str) else "")
    if not isinstance(value, str) or problem:
        refuse(f"{label} {problem or 'is not a string'}")
    return value


def within(child: Path, parent: Path) -> bool:
    try:
        child_abs = os.path.normcase(os.path.abspath(child))
        parent_abs = os.path.normcase(os.path.abspath(parent))
        return os.path.commonpath([child_abs, parent_abs]) == parent_abs
    except ValueError:
        return False


def child_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return env


def run_git(repo: Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    allowed = False
    if args[:3] == ["rev-parse", "--verify", "--end-of-options"] and len(args) == 4:
        allowed = True
    elif args[:3] in (["cat-file", "-t", "--end-of-options"], ["cat-file", "blob", "--end-of-options"]):
        allowed = len(args) == 4
    if not allowed:
        refuse("git command is not a read")
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        check=False,
        env=child_env(),
        shell=False,
        timeout=TIMEOUT_SECONDS,
    )


def commit_exists(repo: Path, commit: str) -> bool:
    probe = run_git(repo, ["rev-parse", "--verify", "--end-of-options", f"{commit}^{{commit}}"])
    if probe.returncode != 0:
        return False
    return probe.stdout.decode("utf-8", "replace").strip() == commit


def read_blob(repo: Path, commit: str, relpath: str) -> tuple[bytes | None, str | None]:
    if not commit_exists(repo, commit):
        return None, "commit-absent"
    kind = run_git(repo, ["cat-file", "-t", "--end-of-options", f"{commit}:{relpath}"])
    if kind.returncode != 0:
        return None, "absent"
    if kind.stdout.strip() != b"blob":
        return None, "not-blob"
    blob = run_git(repo, ["cat-file", "blob", "--end-of-options", f"{commit}:{relpath}"])
    if blob.returncode != 0:
        return None, "unreadable"
    return blob.stdout, None


def pin_tool(path: Path, digest: str, size: int, label: str) -> None:
    problem = file_problem(path)
    if problem:
        refuse(f"{label} is {problem}")
    data = path.read_bytes()
    if len(data) != size or sha256_bytes(data) != digest:
        refuse(f"{label} pin mismatch")


def optional_sha(value, label: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or HEX64.fullmatch(value) is None:
        refuse(f"{label} must be 64 lowercase hex")
    return value


def parse_artifact_request(value) -> dict | None:
    if value is None:
        return None
    body = require_exact(value, {"compare_commit", "compare_live"}, "artifact_manifest")
    commit = body["compare_commit"]
    if commit is not None and (not isinstance(commit, str) or HEX40.fullmatch(commit) is None):
        refuse("compare_commit must be 40 lowercase hex or null")
    if type(body["compare_live"]) is not bool:
        refuse("compare_live must be boolean")
    return {"compare_commit": commit, "compare_live": body["compare_live"]}


def parse_source(value, seen: set[str]) -> dict:
    if not isinstance(value, dict):
        refuse("source is not an object")
    kind = value.get("kind")
    if kind == "git-blob":
        allowed = GIT_BLOB_KEYS
        required = {"id", "kind", "role", "commit", "path"}
    elif kind == "live":
        allowed = LIVE_KEYS
        required = {"id", "kind", "role", "path", "embed"}
    elif kind == "member-file":
        allowed = MEMBER_KEYS
        required = {"id", "kind", "role", "name"}
    else:
        refuse("source kind is not git-blob, live, or member-file")
    got = set(value)
    if not required <= got <= allowed:
        refuse(f"source keys extra={sorted(got - allowed)} missing={sorted(required - got)}")
    source_id = value["id"]
    if not isinstance(source_id, str) or SOURCE_ID.fullmatch(source_id) is None:
        refuse("source id is not a short lowercase id")
    if source_id in seen:
        refuse(f"duplicate source id: {source_id}")
    seen.add(source_id)
    role = value["role"]
    if role not in ROLES:
        refuse("source role is unknown")
    item = {
        "id": source_id,
        "kind": kind,
        "role": role,
        "expect_sha256": optional_sha(value.get("expect_sha256"), "expect_sha256"),
        "artifact_manifest": parse_artifact_request(value.get("artifact_manifest")),
        "live_opened": False,
    }
    if kind == "git-blob":
        commit = value["commit"]
        if not isinstance(commit, str) or HEX40.fullmatch(commit) is None:
            refuse("commit must be 40 lowercase hex")
        item["commit"] = commit
        item["path"] = require_relative(value["path"], "git path")
    elif kind == "live":
        if type(value["embed"]) is not bool:
            refuse("embed must be boolean")
        item["path"] = require_relative(value["path"], "live path")
        item["embed"] = value["embed"]
    else:
        name = value["name"]
        if not isinstance(name, str) or (name not in MEMBER_FILE_NAMES and PAYLOAD_NAME.fullmatch(name) is None):
            refuse("member-file name is not an allowed sealed name")
        item["name"] = name
    return item


def load_request(path_text: str) -> dict:
    path = absolute_path(path_text, "request")
    link = ancestor_link(path)
    if link:
        refuse(f"request ancestor is link: {link}")
    problem = file_problem(path)
    if problem:
        refuse(f"request is {problem}")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse("request has a BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("request is not utf-8")
    value = loads_strict(text)
    body = require_exact(value, REQUEST_KEYS, "request")
    if body["schema"] != "review-packet-request/1":
        refuse("request schema mismatch")
    origin = require_exact(body["origin"], {"book", "page", "pass"}, "origin")
    require_text(origin["book"], "origin book")
    require_text(origin["page"], "origin page")
    if not isinstance(origin["pass"], str) or PASS_NAME.fullmatch(origin["pass"]) is None:
        refuse("origin pass must match 05.NN")
    member = body["member"]
    if not isinstance(member, str) or MEMBER_NAME.fullmatch(member) is None:
        refuse("member path is not a return member")
    bounds = require_exact(
        body["bounds"],
        {"max_sources", "max_source_bytes", "max_total_bytes", "max_output_bytes"},
        "bounds",
    )
    max_sources = require_int(bounds["max_sources"], "max_sources", 0, 64)
    max_source_bytes = require_int(bounds["max_source_bytes"], "max_source_bytes", 1, 2_000_000)
    max_total_bytes = require_int(bounds["max_total_bytes"], "max_total_bytes", 1, 8_000_000)
    max_output_bytes = require_int(bounds["max_output_bytes"], "max_output_bytes", 1, 12_000_000)
    if max_total_bytes < max_source_bytes:
        refuse("max_total_bytes is below max_source_bytes")
    sources = body["sources"]
    if not isinstance(sources, list):
        refuse("sources is not an array")
    if len(sources) > max_sources:
        refuse("source count exceeds max_sources")
    seen: set[str] = set()
    parsed = [parse_source(item, seen) for item in sources]
    book = absolute_path(body["book"], "book")
    repo = absolute_path(body["repo"], "repo")
    python = absolute_path(body["python"], "python")
    inspector = absolute_path(body["inspector"], "inspector")
    helper = absolute_path(body["helper"], "helper")
    output = absolute_path(body["output"], "output")
    for label, candidate in (
        ("book", book),
        ("repo", repo),
        ("python", python),
        ("inspector", inspector),
        ("helper", helper),
        ("output", output),
    ):
        link = ancestor_link(candidate)
        if link:
            refuse(f"{label} ancestor is link: {link}")
    if os.path.lexists(output):
        refuse("output exists")
    parent_problem = directory_problem(output.parent)
    if parent_problem:
        refuse(f"output parent is {parent_problem}")
    member_path = book / member
    if within(output, member_path) or os.path.normcase(str(output)) == os.path.normcase(str(member_path)):
        refuse("output is inside the member")
    if ".git" in {part.casefold() for part in output.parts}:
        refuse("output is inside a Git control path")
    repo_problem = directory_problem(repo)
    if repo_problem:
        refuse(f"repo is {repo_problem}")
    python_problem = file_problem(python)
    if python_problem:
        refuse(f"python is {python_problem}")
    pin_tool(inspector, INSPECTOR_SHA256, INSPECTOR_BYTES, "inspector")
    pin_tool(helper, HELPER_SHA256, HELPER_BYTES, "helper")
    for source in parsed:
        if source["kind"] == "live":
            live_path = repo / source["path"]
            if not within(live_path, repo):
                refuse("live path escapes the repo")
            link = ancestor_link(live_path)
            if link:
                refuse(f"live source ancestor is link: {link}")
            if os.path.lexists(live_path):
                problem = file_problem(live_path)
                if problem and problem != "missing":
                    refuse(f"live source is {problem}: {source['id']}")
        if source["kind"] == "member-file" and os.path.lexists(member_path):
            if is_reparse(member_path):
                refuse("member is link")
            sealed = member_path / source["name"]
            link = ancestor_link(sealed)
            if link:
                refuse(f"member-file ancestor is link: {link}")
            if os.path.lexists(sealed):
                problem = file_problem(sealed)
                if problem and problem != "missing":
                    refuse(f"member-file is {problem}: {source['id']}")
    return {
        "book": str(book),
        "member": member,
        "origin": {"book": origin["book"], "page": origin["page"], "pass": origin["pass"]},
        "repo": str(repo),
        "python": str(python),
        "inspector": str(inspector),
        "helper": str(helper),
        "output": str(output),
        "bounds": {
            "max_sources": max_sources,
            "max_source_bytes": max_source_bytes,
            "max_total_bytes": max_total_bytes,
            "max_output_bytes": max_output_bytes,
        },
        "sources": parsed,
    }


def run_tool(python: str, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [python, "-B", *args],
        capture_output=True,
        check=False,
        env=child_env(),
        shell=False,
        timeout=TIMEOUT_SECONDS,
    )


class Output:
    def __init__(self, root: Path, limit: int) -> None:
        self.root = root
        self.limit = limit
        self.used = 0
        self.files: list[dict] = []

    def emit(self, rel: str, data: bytes) -> None:
        if self.used + len(data) > self.limit:
            raise Partial("output bound")
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        exclusive_write(path, data)
        self.used += len(data)
        self.files.append({"path": rel, "sha256": sha256_bytes(data), "bytes": len(data)})


def take_bytes(data: bytes, bounds: dict, total: int) -> int:
    if len(data) > bounds["max_source_bytes"] or total + len(data) > bounds["max_total_bytes"]:
        raise Partial("source bound")
    return total + len(data)


def blank_source(source: dict, status: str, problems: list[str]) -> dict:
    return {
        "id": source["id"],
        "kind": source["kind"],
        "role": source["role"],
        "status": status,
        "sha256": None,
        "bytes": None,
        "embedded": False,
        "snapshot": None,
        "expect_sha256": source["expect_sha256"],
        "expected_match": None,
        "problems": problems,
        "live_opened": False,
        "artifact_check": None,
        "_bytes": None,
    }


def present_source(source: dict, data: bytes, embedded: bool, snapshot: str | None) -> dict:
    digest = sha256_bytes(data)
    expected = source["expect_sha256"]
    problems = []
    expected_match = None
    if expected is not None:
        expected_match = digest == expected
        if not expected_match:
            problems.append("differs-from-expected")
    return {
        "id": source["id"],
        "kind": source["kind"],
        "role": source["role"],
        "status": "present",
        "sha256": digest,
        "bytes": len(data),
        "embedded": embedded,
        "snapshot": snapshot,
        "expect_sha256": expected,
        "expected_match": expected_match,
        "problems": problems,
        "live_opened": source["kind"] == "live",
        "artifact_check": None,
        "_bytes": data,
    }


def gather_source(source: dict, request: dict, total: int) -> tuple[dict, int]:
    bounds = request["bounds"]
    repo = Path(request["repo"])
    if source["kind"] == "git-blob":
        data, problem = read_blob(repo, source["commit"], source["path"])
        if problem or data is None:
            record = blank_source(
                source,
                "absent",
                [f"git blob is {problem or 'absent'}", "live file was not read"],
            )
            return record, total
        total = take_bytes(data, bounds, total)
        return present_source(source, data, True, None), total
    if source["kind"] == "live":
        path = repo / source["path"]
        if not os.path.lexists(path):
            return blank_source(source, "absent", ["live file is absent"]), total
        problem = file_problem(path)
        if problem:
            return blank_source(source, "rejected", [f"live file is {problem}"]), total
        size = os.lstat(path).st_size
        if size > bounds["max_source_bytes"] or total + size > bounds["max_total_bytes"]:
            raise Partial(f"source bound: {source['id']}")
        data = path.read_bytes()
        if len(data) != size:
            raise Partial(f"source changed while reading: {source['id']}")
        total += len(data)
        embedded = source["embed"]
        record = present_source(source, data, embedded, None)
        if not embedded:
            record["_bytes"] = data
            record["embedded"] = False
        return record, total
    member_path = Path(request["book"]) / request["member"] / source["name"]
    if not os.path.lexists(member_path):
        return blank_source(source, "absent", ["sealed member file is absent"]), total
    problem = file_problem(member_path)
    if problem:
        return blank_source(source, "rejected", [f"sealed member file is {problem}"]), total
    size = os.lstat(member_path).st_size
    if size > bounds["max_source_bytes"] or total + size > bounds["max_total_bytes"]:
        raise Partial(f"source bound: {source['id']}")
    data = member_path.read_bytes()
    if len(data) != size:
        raise Partial(f"source changed while reading: {source['id']}")
    total += len(data)
    return present_source(source, data, True, None), total


def row_commit(row: dict, default: str | None) -> str | None:
    if "commit" not in row:
        return default
    commit = row["commit"]
    if not isinstance(commit, str) or HEX40.fullmatch(commit) is None:
        return ""
    return commit


def classify(historical: str, live: str) -> str:
    if historical == "match" and live == "differs":
        return "changed-live-working-copy"
    if historical == "match" and live == "absent":
        return "live-absent"
    if historical == "match" and live in {"match", "not-requested"}:
        return "historical-match"
    if historical == "mismatch":
        return "historical-mismatch"
    if historical == "absent":
        return "historical-absent"
    if historical == "not-declared" and live == "match":
        return "live-match"
    if historical == "not-declared" and live == "differs":
        return "live-mismatch"
    if historical == "not-declared" and live == "absent":
        return "live-absent"
    return "row-rejected"


def observe_live_row(repo: Path, relpath: str, declared_sha: str, declared_bytes: int, limit: int) -> dict:
    path = repo / relpath
    if not within(path, repo):
        return {"live": "unreadable", "live_sha256": None, "live_bytes": None}
    link = None
    try:
        link = ancestor_link(path)
    except Refused:
        return {"live": "unreadable", "live_sha256": None, "live_bytes": None}
    if link or (os.path.lexists(path) and is_reparse(path)):
        return {"live": "link", "live_sha256": None, "live_bytes": None}
    if not os.path.lexists(path):
        return {"live": "absent", "live_sha256": None, "live_bytes": None}
    problem = file_problem(path)
    if problem:
        return {"live": "not-regular", "live_sha256": None, "live_bytes": None}
    size = os.lstat(path).st_size
    if size > limit:
        return {"live": "oversize", "live_sha256": None, "live_bytes": size}
    data = path.read_bytes()
    digest = sha256_bytes(data)
    state = "match" if digest == declared_sha and len(data) == declared_bytes else "differs"
    return {"live": state, "live_sha256": digest, "live_bytes": len(data)}


def observe_historical_row(repo: Path, commit: str | None, relpath: str, declared_sha: str, declared_bytes: int, limit: int) -> dict:
    if commit is None:
        return {"historical": "not-declared", "historical_sha256": None, "historical_bytes": None, "commit": None}
    if commit == "":
        return {"historical": "unreadable", "historical_sha256": None, "historical_bytes": None, "commit": None}
    data, problem = read_blob(repo, commit, relpath)
    if problem or data is None:
        return {
            "historical": "absent" if problem in {"absent", "commit-absent"} else "unreadable",
            "historical_sha256": None,
            "historical_bytes": None,
            "commit": commit,
        }
    if len(data) > limit:
        return {"historical": "oversize", "historical_sha256": None, "historical_bytes": len(data), "commit": commit}
    digest = sha256_bytes(data)
    state = "match" if digest == declared_sha and len(data) == declared_bytes else "mismatch"
    return {"historical": state, "historical_sha256": digest, "historical_bytes": len(data), "commit": commit}


def check_artifact(source_record: dict, check: dict, repo: Path, limit: int) -> dict:
    if source_record["status"] != "present" or source_record["_bytes"] is None:
        return {
            "source": source_record["id"],
            "result": "not-run",
            "observed_schema": None,
            "rows_interpreted": False,
            "not_interpreted_keys": [],
            "rows": [],
        }
    try:
        text = source_record["_bytes"].decode("utf-8")
        value = loads_strict(text)
    except (UnicodeDecodeError, Refused):
        return {
            "source": source_record["id"],
            "result": "malformed",
            "observed_schema": None,
            "rows_interpreted": False,
            "not_interpreted_keys": [],
            "rows": [],
        }
    if not isinstance(value, dict) or value.get("schema") != "artifact-manifest/1" or not isinstance(value.get("artifacts"), list):
        observed = value.get("schema") if isinstance(value, dict) else None
        result = "malformed" if isinstance(value, dict) and value.get("schema") == "artifact-manifest/1" else "unsupported-schema"
        return {
            "source": source_record["id"],
            "result": result,
            "observed_schema": observed if isinstance(observed, str) else None,
            "rows_interpreted": False,
            "not_interpreted_keys": sorted(key for key in value if key not in {"schema", "artifacts"}) if isinstance(value, dict) else [],
            "rows": [],
        }
    rows = []
    for row in value["artifacts"]:
        if not isinstance(row, dict):
            rows.append({"path": None, "classification": "row-rejected", "problems": ["row is not an object"]})
            continue
        missing = [key for key in ("path", "sha256", "bytes") if key not in row]
        path = row.get("path")
        digest = row.get("sha256")
        size = row.get("bytes")
        path_ok = isinstance(path, str) and relative_problem(path) is None
        digest_ok = isinstance(digest, str) and HEX64.fullmatch(digest) is not None
        size_ok = type(size) is int and size >= 0
        if missing or not path_ok or not digest_ok or not size_ok:
            rows.append(
                {
                    "path": path if isinstance(path, str) else None,
                    "classification": "row-rejected",
                    "problems": ["row fields are incomplete or unsafe"],
                }
            )
            continue
        commit = row_commit(row, check["compare_commit"])
        historical = observe_historical_row(repo, commit, path, digest, size, limit)
        if check["compare_live"]:
            live = observe_live_row(repo, path, digest, size, limit)
        else:
            live = {"live": "not-requested", "live_sha256": None, "live_bytes": None}
        rows.append(
            {
                "path": path,
                "declared_sha256": digest,
                "declared_bytes": size,
                "commit": historical["commit"],
                "historical": historical["historical"],
                "historical_sha256": historical["historical_sha256"],
                "historical_bytes": historical["historical_bytes"],
                "live": live["live"],
                "live_sha256": live["live_sha256"],
                "live_bytes": live["live_bytes"],
                "classification": classify(historical["historical"], live["live"]),
                "not_interpreted_keys": sorted(key for key in row if key not in {"path", "sha256", "bytes", "commit"}),
            }
        )
    return {
        "source": source_record["id"],
        "result": "checked",
        "observed_schema": "artifact-manifest/1",
        "rows_interpreted": True,
        "not_interpreted_keys": sorted(key for key in value if key not in {"schema", "artifacts"}),
        "rows": rows,
    }


def parse_custody(stdout: bytes) -> tuple[dict | None, list[str]]:
    unverified = []
    try:
        value = loads_strict(stdout.decode("utf-8"))
    except (UnicodeDecodeError, Refused):
        return None, ["custody JSON did not parse"]
    if not isinstance(value, dict):
        return None, ["custody JSON was not an object"]
    if value.get("schema") != "return-capture-inspection/1":
        unverified.append("custody schema was not return-capture-inspection/1")
    status = value.get("status")
    if status not in CUSTODY_STATUS:
        unverified.append("custody status was not a known inspection status")
        status = None
    reservation = value.get("reservation") if isinstance(value.get("reservation"), dict) else None
    capture = value.get("capture") if isinstance(value.get("capture"), dict) else None
    problems = value.get("problems") if isinstance(value.get("problems"), list) else []
    problems = [item for item in problems if isinstance(item, str)]
    return {
        "status": status,
        "problems": problems,
        "reservation": reservation,
        "capture": capture,
    }, unverified


def origin_conflicts(requested: dict, reservation: dict | None, status: str | None) -> tuple[list[str], list[str]]:
    conflicts = []
    unverified = []
    if reservation is None:
        if status != "missing":
            unverified.append("reservation origin was not observed")
        return conflicts, unverified
    origin = reservation.get("origin")
    if not isinstance(origin, dict):
        unverified.append("reservation origin was not observed")
        return conflicts, unverified
    pairs = (
        ("book", "book"),
        ("page", "page"),
        ("pass", "batch"),
    )
    for requested_key, reservation_key in pairs:
        got = origin.get(reservation_key)
        want = requested[requested_key]
        if not isinstance(got, str):
            conflicts.append(f"reservation origin {reservation_key} is absent")
        elif got != want:
            conflicts.append(f"requested {requested_key} {want}; reservation {reservation_key} {got}")
    return conflicts, unverified


def public_source(record: dict) -> dict:
    return {
        "id": record["id"],
        "kind": record["kind"],
        "role": record["role"],
        "status": record["status"],
        "sha256": record["sha256"],
        "bytes": record["bytes"],
        "embedded": record["embedded"],
        "snapshot": record["snapshot"],
        "expect_sha256": record["expect_sha256"],
        "expected_match": record["expected_match"],
        "problems": record["problems"],
        "live_opened": record["live_opened"],
    }


def render_packet_md(packet: dict) -> bytes:
    lines = [
        "# Review packet",
        "",
        f"Assembly: {packet['assembly']}",
        f"Member: {packet['member']}",
        f"Book: {packet['book']}",
        "",
        "## Custody observation",
        "",
        f"Status: {packet['custody']['status']}",
        f"Inspector exit: {packet['custody']['exit']}",
        f"Helper verify exit: {packet['custody']['verify_exit']}",
    ]
    problems = packet["custody"]["problems"]
    if problems:
        lines.append("Problems:")
        lines.extend(f"- {item}" for item in problems)
    else:
        lines.append("Problems: none")
    lines.append("")
    lines.append(STATEMENT.split(". ")[0] + ".")
    lines.append("")
    lines.append("Helper verify text, stored exact:")
    lines.append("")
    verify_text = packet["custody"]["verify_text"]
    if verify_text == "":
        lines.append("Verify stdout is empty.")
    else:
        lines.extend(verify_text.splitlines())
    lines.extend(["", "## Builder-reported claims", "", "Return claims remain claims even when a hash matches."])
    claims = [item for item in packet["sources"] if item["role"] == "builder-claim"]
    if not claims:
        lines.append("None.")
    for item in claims:
        lines.append(
            f"- {item['id']}: status {item['status']}; sha256 {item['sha256']}; bytes {item['bytes']}; snapshot {item['snapshot']}"
        )
    lines.extend(["", "## Artifact checks", ""])
    checks = packet["artifact_checks"]
    if not checks:
        lines.append("None.")
    for check in checks:
        lines.append(f"### {check['source']}")
        lines.append("")
        lines.append(f"Schema result: {check['result']}")
        lines.append(f"Observed schema: {check['observed_schema']}")
        lines.append(f"Rows interpreted: {str(check['rows_interpreted']).lower()}")
        if check["not_interpreted_keys"]:
            lines.append("Keys not interpreted: " + ", ".join(check["not_interpreted_keys"]))
        if not check["rows"]:
            lines.append("Rows: none")
        for row in check["rows"]:
            lines.append(
                "- {path}: classification {classification}; historical {historical} sha256 {hsha} bytes {hbytes}; live {live} sha256 {lsha} bytes {lbytes}".format(
                    path=row.get("path"),
                    classification=row.get("classification"),
                    historical=row.get("historical"),
                    hsha=row.get("historical_sha256"),
                    hbytes=row.get("historical_bytes"),
                    live=row.get("live"),
                    lsha=row.get("live_sha256"),
                    lbytes=row.get("live_bytes"),
                )
            )
        lines.append("")
    lines.extend(["## Absent, conflicting, and unverified", ""])
    notes = []
    for item in packet["sources"]:
        if item["status"] != "present":
            notes.append(f"absent or rejected source {item['id']}: {', '.join(item['problems']) or item['status']}")
        elif item["expected_match"] is False:
            notes.append(f"conflicting source {item['id']}: differs-from-expected")
    notes.extend(f"origin conflict: {item}" for item in packet["origin_conflicts"])
    notes.extend(f"unverified: {item}" for item in packet["unverified"])
    for check in checks:
        for row in check["rows"]:
            classification = row.get("classification")
            if classification not in {None, "historical-match", "live-match"}:
                notes.append(f"artifact {row.get('path')}: {classification}")
    if not notes:
        lines.append("None.")
    else:
        lines.extend(f"- {item}" for item in notes)
    lines.extend(["", "## Director quotations", ""])
    quotes = [item for item in packet["sources"] if item["role"] == "director-quotation"]
    if not quotes:
        lines.append("None.")
    for item in quotes:
        lines.append(
            f"- {item['id']}: status {item['status']}; sha256 {item['sha256']}; bytes {item['bytes']}; snapshot {item['snapshot']}"
        )
    lines.append("These quotations are source bytes. They do not confer authority.")
    lines.extend(
        [
            "",
            "## Limits",
            "",
            STATEMENT,
            "This packet does not accept, approve, publish, seat, or name a next task.",
            "",
        ]
    )
    rendered = "\n".join(line.rstrip() for line in lines)
    if not rendered.endswith("\n"):
        rendered += "\n"
    return rendered.encode("utf-8")


def decode_text(data: bytes) -> str:
    return data.decode("utf-8", "replace")


def build(request: dict, out: Path) -> int:
    output = Output(out, request["bounds"]["max_output_bytes"])
    inspect = run_tool(
        request["python"],
        [request["inspector"], "inspect", "--book", request["book"], "--member", request["member"], "--json"],
    )
    verify = run_tool(
        request["python"],
        [request["helper"], "verify", "--book", request["book"], "--member", request["member"]],
    )
    output.emit("custody.json", inspect.stdout)
    output.emit("custody-stderr.txt", inspect.stderr)
    output.emit("helper-verify.txt", verify.stdout)
    output.emit("helper-verify-stderr.txt", verify.stderr)
    observation, unverified = parse_custody(inspect.stdout)
    status = observation["status"] if observation else None
    reservation = observation["reservation"] if observation else None
    conflicts, origin_unverified = origin_conflicts(request["origin"], reservation, status)
    unverified.extend(origin_unverified)
    records = []
    total = 0
    repo = Path(request["repo"])
    for index, source in enumerate(request["sources"], start=1):
        record, total = gather_source(source, request, total)
        if record["embedded"] and record["_bytes"] is not None:
            snapshot = f"sources/{index:04d}-{source['id']}.blob"
            output.emit(snapshot, record["_bytes"])
            record["snapshot"] = snapshot
        if source["artifact_manifest"] is not None:
            record["artifact_check"] = check_artifact(
                record,
                source["artifact_manifest"],
                repo,
                request["bounds"]["max_source_bytes"],
            )
        records.append(record)
    checks = [record["artifact_check"] for record in records if record["artifact_check"] is not None]
    verify_text = decode_text(verify.stdout) if verify.stdout else ""
    packet = {
        "schema": "review-packet/1",
        "assembly": "complete",
        "acceptance": False,
        "approved": False,
        "published": False,
        "seated": False,
        "authority_inferred": False,
        "semantic_review": False,
        "next_task": None,
        "custody_is_acceptance": False,
        "checks_are_not_sandbox": True,
        "statement": STATEMENT,
        "member": request["member"],
        "book": request["book"],
        "origin_requested": request["origin"],
        "origin_conflicts": conflicts,
        "unverified": unverified,
        "tools": {
            "python": request["python"],
            "inspector": request["inspector"],
            "helper": request["helper"],
            "inspector_sha256": INSPECTOR_SHA256,
            "helper_sha256": HELPER_SHA256,
        },
        "custody": {
            "status": status,
            "exit": inspect.returncode,
            "problems": observation["problems"] if observation else [],
            "reservation": reservation,
            "capture": observation["capture"] if observation else None,
            "sha256": sha256_bytes(inspect.stdout),
            "verify_exit": verify.returncode,
            "verify_sha256": sha256_bytes(verify.stdout),
            "verify_text": verify_text,
        },
        "sources": [public_source(record) for record in records],
        "artifact_checks": checks,
    }
    packet_bytes = dump(packet)
    output.emit("packet.json", packet_bytes)
    rendered = render_packet_md(json.loads(packet_bytes.decode("utf-8")))
    output.emit("PACKET.md", rendered)
    manifest = {
        "schema": "review-packet-manifest/1",
        "files": list(output.files),
        "sources": [
            {
                "id": record["id"],
                "sha256": record["sha256"],
                "bytes": record["bytes"],
                "snapshot": record["snapshot"],
                "embedded": record["embedded"],
            }
            for record in records
        ],
    }
    manifest_bytes = dump(manifest)
    output.emit("manifest.json", manifest_bytes)
    status_body = dump(
        {
            "schema": "review-packet-assembly/1",
            "assembly": "complete",
            "reason": None,
            "manifest_sha256": sha256_bytes(manifest_bytes),
        }
    )
    output.emit("assembly-status.json", status_body)
    return 0


def write_partial(out: Path, reason: str, limit: int) -> None:
    status_path = out / "assembly-status.json"
    if os.path.lexists(status_path):
        return
    used = 0
    if out.exists():
        for dirpath, _dirnames, filenames in os.walk(out):
            for name in filenames:
                used += os.lstat(Path(dirpath) / name).st_size
    body = dump(
        {
            "schema": "review-packet-assembly/1",
            "assembly": "partial",
            "reason": reason,
            "manifest_sha256": None,
        }
    )
    if used + len(body) > limit:
        return
    try:
        exclusive_write(status_path, body)
    except OSError:
        return


def assemble_request(path_text: str) -> int:
    request = load_request(path_text)
    out = Path(request["output"])
    try:
        os.mkdir(out)
    except FileExistsError:
        refuse("output exists")
    try:
        return build(request, out)
    except Partial as exc:
        write_partial(out, exc.reason, request["bounds"]["max_output_bytes"])
        return 2
    except (OSError, subprocess.TimeoutExpired) as exc:
        write_partial(out, f"{type(exc).__name__}: {exc}", request["bounds"]["max_output_bytes"])
        return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="review_packet.py")
    sub = parser.add_subparsers(dest="command", required=True)
    assemble = sub.add_parser("assemble")
    assemble.add_argument("--request", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return 2 if code is None else int(code)
    try:
        return assemble_request(args.request)
    except Refused as exc:
        sys.stderr.write(str(exc).rstrip() + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
