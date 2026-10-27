"""One development-context validator for the app entry and the runner candidate.

This module reads the assignment record and the local development configuration.
It never reads 00.kernel/00.live.md as an input. A path that names that view is refused.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path

SCHEMA = "librarian-development-workspace"
FIXTURE_SCHEMA = "librarian-fixture"
RECORD_SCHEMA = "00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1"
RECORD_KEYS = (
    "record",
    "schema",
    "desk",
    "book",
    "workflow_space",
    "current_work",
    "pack",
    "assignment_state",
    "waits_on",
    "next",
    "updated",
)
STATES = {"waiting", "released", "running", "returned", "accepted", "stopped"}
CONFIG_KEYS = (
    "schema",
    "version",
    "assignment_record",
    "desk",
    "work_book",
    "workflow_space",
    "runtime_book",
    "runtime_space",
    "runner",
)
RUNNER_KEYS = ("path", "sha256")
FIXTURE_KEYS = (
    "schema",
    "version",
    "identity",
    "allowed_root",
    "compute_page",
    "inventory_book",
    "output",
    "required_face",
    "payload_sha256",
)
PAGE_RE = re.compile(r"^(\d{4})\.(.+)$")
RUNNER_NAME_RE = re.compile(r"^02\.[A-Za-z_][A-Za-z0-9_]*\.(\d{3})\.py$")
ACTIVE_NAME_RE = re.compile(r"^02\.[A-Za-z_][A-Za-z0-9_]*\.py$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SEGMENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class Stop(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


def stop(message: str) -> None:
    raise Stop(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(path: Path) -> str:
    return os.path.normcase(os.path.abspath(str(path)))


def is_inside(child: Path, parent: Path) -> bool:
    try:
        child_s = norm(child.resolve())
        parent_s = norm(parent.resolve())
    except OSError:
        stop("path escapes the root")
    if child_s == parent_s:
        return True
    sep = os.path.normcase(os.sep)
    prefix = parent_s if parent_s.endswith(sep) else parent_s + sep
    return child_s.startswith(prefix)


def overlaps_live(fixture_root: Path, code_root: Path, config: dict) -> bool:
    live_book = (code_root / config["desk"] / config["work_book"]).resolve()
    if norm(fixture_root.resolve()) == norm(code_root.resolve()):
        return True
    if is_inside(fixture_root, live_book) or is_inside(live_book, fixture_root):
        return True
    return False


def _pairs(pairs: list) -> dict:
    found = {}
    for key, value in pairs:
        if key in found:
            stop(f"repeats a key: {key}")
        found[key] = value
    return found


def load_json(path: Path, *, kind: str) -> dict:
    if not path.is_file():
        stop(f"missing {kind}")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError:
        stop(f"{kind} is not utf-8")
    if text.startswith("\ufeff"):
        stop(f"{kind} has a BOM")
    try:
        value = json.loads(text, object_pairs_hook=_pairs)
    except Stop:
        raise
    except json.JSONDecodeError:
        stop(f"{kind} is not json")
    if not isinstance(value, dict):
        stop(f"{kind} is not an object")
    return value


def _exact_keys(value: dict, required: tuple[str, ...], kind: str) -> None:
    missing = [key for key in required if key not in value]
    if missing:
        stop(f"{kind} misses keys: {', '.join(missing)}")
    unknown = [key for key in value if key not in required]
    if unknown:
        stop(f"{kind} has an unknown key: {unknown[0]}")


def _string(value: dict, key: str, kind: str) -> str:
    got = value[key]
    if not isinstance(got, str) or isinstance(got, bool):
        stop(f"{kind} field has the wrong type: {key}")
    if got.strip() == "":
        stop(f"{kind} field is empty: {key}")
    return got


def _version(value: dict, kind: str) -> None:
    got = value["version"]
    if isinstance(got, bool) or not isinstance(got, int):
        stop(f"{kind} field has the wrong type: version")
    if got != 1:
        stop(f"{kind} version is not 1")


def _space(text: str, label: str) -> str:
    if not re.fullmatch(r"[0-9]", text):
        stop(f"{label} is not a single digit")
    return text


def _segment(text: str, label: str) -> str:
    if not SEGMENT.fullmatch(text) or "/" in text or "\\" in text:
        stop(f"{label} is not a single folder name")
    return text


def load_config(path: Path) -> dict:
    raw = load_json(path, kind="config")
    _exact_keys(raw, CONFIG_KEYS, "config")
    if raw["schema"] != SCHEMA:
        stop("config schema is not the development workspace")
    _version(raw, "config")
    config = {
        "schema": SCHEMA,
        "version": 1,
        "assignment_record": _string(raw, "assignment_record", "config"),
        "desk": _segment(_string(raw, "desk", "config"), "desk"),
        "work_book": _segment(_string(raw, "work_book", "config"), "work book"),
        "workflow_space": _space(_string(raw, "workflow_space", "config"), "workflow space"),
        "runtime_book": _segment(_string(raw, "runtime_book", "config"), "runtime book"),
        "runtime_space": _space(_string(raw, "runtime_space", "config"), "runtime space"),
    }
    if config["work_book"] == config["runtime_book"]:
        stop("job book and runtime book must differ")
    runner = raw["runner"]
    if not isinstance(runner, dict):
        stop("config field has the wrong type: runner")
    _exact_keys(runner, RUNNER_KEYS, "runner")
    runner_path = _string(runner, "path", "runner")
    runner_hash = _string(runner, "sha256", "runner")
    if not HEX64.fullmatch(runner_hash):
        stop("runner hash is not sha256")
    name = runner_path.replace("\\", "/").split("/")[-1]
    if ACTIVE_NAME_RE.fullmatch(name) and not RUNNER_NAME_RE.fullmatch(name):
        stop("runner is an active name")
    if not RUNNER_NAME_RE.fullmatch(name):
        stop("runner file is not a versioned candidate")
    config["runner"] = {"path": runner_path, "sha256": runner_hash}
    return config


def load_fixture(path: Path) -> dict:
    raw = load_json(path, kind="fixture")
    _exact_keys(raw, FIXTURE_KEYS, "fixture")
    if raw["schema"] != FIXTURE_SCHEMA:
        stop("fixture schema is not the development fixture")
    _version(raw, "fixture")
    identity = _string(raw, "identity", "fixture")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}", identity):
        stop("fixture identity is not explicit")
    payload_hash = _string(raw, "payload_sha256", "fixture")
    if not HEX64.fullmatch(payload_hash):
        stop("payload hash is not sha256")
    compute_page = _string(raw, "compute_page", "fixture")
    if not PAGE_RE.fullmatch(compute_page):
        stop("compute page is not a page folder")
    face = _string(raw, "required_face", "fixture")
    if face != Path(face).name or face in (".", ".."):
        stop("required face is not a file name")
    return {
        "schema": FIXTURE_SCHEMA,
        "version": 1,
        "identity": identity,
        "allowed_root": _string(raw, "allowed_root", "fixture"),
        "compute_page": compute_page,
        "inventory_book": _segment(_string(raw, "inventory_book", "fixture"), "inventory book"),
        "output": _string(raw, "output", "fixture"),
        "required_face": face,
        "payload_sha256": payload_hash,
    }


def parse_assignment(data: bytes) -> dict:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        stop("record is not UTF-8")
    if "\r" in text:
        stop("record has CR line endings")
    if text.startswith("\ufeff"):
        stop("record has a BOM")
    fields = {}
    lines = text.split("\n")
    for number, line in enumerate(lines, 1):
        if line == "" and number == len(lines):
            continue
        if ": " not in line:
            stop(f"record line {number} is not 'key: value'")
        key, value = line.split(": ", 1)
        if key not in RECORD_KEYS:
            stop(f"record has an unknown key: {key}")
        if key in fields:
            stop(f"record repeats a key: {key}")
        if not value.strip():
            stop(f"record key has an empty value: {key}")
        fields[key] = value
    missing = [key for key in RECORD_KEYS if key not in fields]
    if missing:
        stop(f"record misses keys: {', '.join(missing)}")
    if fields["record"] != "current-assignment" or fields["schema"] != RECORD_SCHEMA:
        stop("record is not a version 1 current-assignment record")
    if fields["assignment_state"] not in STATES:
        stop("assignment_state is not a known state")
    if not fields["workflow_space"].isdigit():
        stop("workflow_space is not a number")
    try:
        datetime.strptime(fields["updated"], "%Y-%m-%d")
    except ValueError:
        stop("updated is not a date")
    return fields


def resolve_under(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not rel.strip():
        stop("path escapes the root")
    text = rel.replace("\\", "/")
    if text.startswith("/") or re.match(r"^[A-Za-z]:", text):
        stop("path escapes the root")
    parts = text.split("/")
    for part in parts:
        if part in ("", ".", "..") or part.endswith(" ") or part.endswith("."):
            stop("path escapes the root")
    try:
        root_r = root.resolve()
        resolved = root_r.joinpath(*parts).resolve()
    except OSError:
        stop("path escapes the root")
    if not is_inside(resolved, root_r):
        stop("path escapes the root")
    return resolved


def band_limits(space: str) -> tuple[int, int]:
    digit = _space(space, "runtime space")
    start = int(digit) * 1000 + 300
    return start, start + 99


def band_label(space: str) -> str:
    start, end = band_limits(space)
    return f"{start:04d}-{end:04d}"


def pages_in_band(runtime_book: Path, space: str) -> list[tuple[str, Path]]:
    if not runtime_book.is_dir():
        stop("runtime book is missing")
    start, end = band_limits(space)
    found = []
    for child in runtime_book.iterdir():
        if not child.is_dir():
            continue
        match = PAGE_RE.fullmatch(child.name)
        if not match:
            continue
        number = int(match.group(1))
        if start <= number <= end:
            found.append((match.group(2), child))
    return found


def require_unique_band(runtime_book: Path, space: str) -> None:
    seen = {}
    for keyword, path in pages_in_band(runtime_book, space):
        if keyword in seen:
            stop(f"more than one compute page for {keyword}")
        seen[keyword] = path


def unique_page(runtime_book: Path, space: str, keyword: str) -> Path:
    if not keyword or keyword in (".", "..") or "/" in keyword or "\\" in keyword:
        stop(f"keyword is not a page title: {keyword}")
    hits = [path for name, path in pages_in_band(runtime_book, space) if name == keyword]
    if not hits:
        stop(f"no compute page for {keyword}")
    if len(hits) > 1:
        stop(f"more than one compute page for {keyword}")
    return hits[0]


def _work_file(root: Path, work_book: Path, rel: str, label: str) -> str:
    path = resolve_under(root, rel)
    if not is_inside(path, work_book):
        stop(f"{label} escapes the work book")
    if not path.is_file():
        stop(f"{label} is missing: {rel}")
    return rel.replace("\\", "/")


class Resolved:
    def __init__(self, **kwargs: object) -> None:
        self.__dict__.update(kwargs)


def validate_context(
    root: Path,
    config: dict,
    *,
    execute: bool,
    runner_root: Path | None = None,
) -> Resolved:
    if not root.is_dir():
        stop("root is missing")
    root = root.resolve()
    if runner_root is None:
        runner_root = root
    else:
        if not runner_root.is_dir():
            stop("root is missing")
        runner_root = runner_root.resolve()
    desk = resolve_under(root, config["desk"])
    if not desk.is_dir():
        stop("desk is missing")
    work_dir = resolve_under(desk, config["work_book"])
    if not work_dir.is_dir():
        stop("work book is missing")
    runtime_dir = resolve_under(desk, config["runtime_book"])
    if not runtime_dir.is_dir():
        stop("runtime book is missing")
    record_rel = config["assignment_record"].replace("\\", "/")
    if record_rel.endswith("00.live.md") or Path(record_rel).name == "00.live.md":
        stop("assignment record is the derived view")
    record_path = resolve_under(root, record_rel)
    if not is_inside(record_path, work_dir):
        stop("assignment record escapes the work book")
    if record_path.name == "00.live.md":
        stop("assignment record is the derived view")
    if not record_path.is_file():
        stop("missing assignment record")
    fields = parse_assignment(record_path.read_bytes())
    if fields["desk"] != config["desk"]:
        stop("record desk is not the configured desk")
    if fields["book"] != config["work_book"]:
        stop("record book is not the configured work book")
    if fields["workflow_space"] != config["workflow_space"]:
        stop("workflow space is not the declared space")
    if fields["book"] == config["runtime_book"] or fields["desk"] == config["runtime_book"]:
        stop("job book and runtime book must differ")
    current = _work_file(root, work_dir, fields["current_work"], "work item")
    packs = []
    for piece in fields["pack"].split(" + "):
        piece = piece.strip()
        if not piece:
            stop("pack is empty")
        packs.append(_work_file(root, work_dir, piece, "pack"))
    runner_rel = config["runner"]["path"]
    runner_runtime = resolve_under(resolve_under(runner_root, config["desk"]), config["runtime_book"])
    if not runner_runtime.is_dir():
        stop("runtime book is missing")
    runner_path = resolve_under(runner_root, runner_rel)
    if not is_inside(runner_path, runner_runtime):
        stop("runner is outside the runtime book")
    page_name = runner_path.parent.name
    match = PAGE_RE.fullmatch(page_name)
    start, end = band_limits(config["runtime_space"])
    if not match or not (start <= int(match.group(1)) <= end):
        stop("runner is outside the runtime band")
    if not runner_path.is_file():
        stop("runner is missing")
    digest = sha256_file(runner_path)
    if digest != config["runner"]["sha256"]:
        stop("runner hash does not match")
    require_unique_band(runtime_dir, config["runtime_space"])
    if norm(runner_root) != norm(root):
        require_unique_band(runner_runtime, config["runtime_space"])
    if execute and fields["assignment_state"] != "released":
        stop("assignment is not a fresh execution release")
    return Resolved(
        root=root,
        desk=config["desk"],
        work_book=config["work_book"],
        workflow_space=config["workflow_space"],
        current_work=current,
        pack=" + ".join(packs),
        assignment_state=fields["assignment_state"],
        runtime_book=config["runtime_book"],
        runtime_space=config["runtime_space"],
        band_label=band_label(config["runtime_space"]),
        runner_rel=runner_rel.replace("\\", "/"),
        runner_sha256=digest,
        runtime_dir=runtime_dir,
        work_dir=work_dir,
    )


def report_lines(resolved: Resolved) -> list[str]:
    return [
        f"desk: {resolved.desk}",
        f"work_book: {resolved.work_book}",
        f"workflow_space: {resolved.workflow_space}",
        f"current_work: {resolved.current_work}",
        f"pack: {resolved.pack}",
        f"assignment_state: {resolved.assignment_state}",
        f"runtime_book: {resolved.runtime_book}",
        f"runtime_space: {resolved.runtime_space}",
        f"runtime_band: {resolved.band_label}",
        f"runner: {resolved.runner_rel}",
        f"runner_sha256: {resolved.runner_sha256}",
    ]


def check_allowed_root(fixture_root: Path, fixture: dict) -> None:
    allowed = fixture["allowed_root"]
    if allowed == ".":
        return
    if re.match(r"^[A-Za-z]:", allowed) or allowed.startswith("\\\\"):
        try:
            allowed_path = Path(allowed).resolve()
        except OSError:
            stop("fixture allowed root does not match")
        if norm(allowed_path) != norm(fixture_root.resolve()):
            stop("fixture allowed root does not match")
        return
    stop("fixture allowed root does not match")
