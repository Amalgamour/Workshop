#!/usr/bin/env python3
"""Bounded Prime benchmark harness: fixed cases, run folders, collection, checks, comparison.

Standard library only. No model call, no session launch, no network, no Git.
A coordinator prepares runs, starts fresh sessions by hand, and collects what they said.
Deterministic checks are string checks. Semantic quality is a supplied reviewer record.

  python -B prime_bench.py validate [--json]
  python -B prime_bench.py manifest
  python -B prime_bench.py prepare --investigation ABS --run-id ID --case ID --condition C ... --run-dir ABS --candidate-dir ABS
  python -B prime_bench.py collect --run-dir ABS --expect-run ID --expect-condition C --status S ...
  python -B prime_bench.py event   --run-dir ABS --kind K --text TEXT [--attachment ABS]
  python -B prime_bench.py assess  --run-dir ABS [--json]
  python -B prime_bench.py review  --run-dir ABS --record ABS [--json]
  python -B prime_bench.py compare --run-dir ABS [...] [--json]
  python -B prime_bench.py export  --run-dir ABS [...] --investigation ABS --dest ABS

Contract: 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/CONTRACT.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

LAB = Path(os.path.abspath(__file__)).parent
REPO = LAB.parents[1]

SCHEMA_BENCH = "prime-bench/1"
SCHEMA_CONDITIONS = "prime-bench-conditions/1"
SCHEMA_KEY = "prime-bench-key/1"
SCHEMA_RUBRIC = "prime-bench-rubric/1"
SCHEMA_META = "prime-bench-case-meta/1"
SCHEMA_INVESTIGATION = "prime-bench-investigation/1"
SCHEMA_RUN = "prime-bench-run/1"
SCHEMA_COLLECTION = "prime-bench-collection/1"
SCHEMA_EVENT = "prime-bench-event/1"
SCHEMA_TOOL_EVENT = "prime-bench-tool-event/1"
SCHEMA_ASSESSMENT = "prime-bench-assessment/1"
SCHEMA_REVIEW = "prime-bench-review/1"
SCHEMA_COMPARISON = "prime-bench-comparison/1"
RULES = "prime-bench-rules/1"

FAMILIES = ("correction", "false-completion", "design-fork", "complete")
VARIANTS = ("a", "b")
CONDITIONS = ("baseline", "assisted")
OUTCOMES = ("continue", "director-input", "develop", "complete")
CAPABILITY = ("supported", "unsupported", "unknown")
CAPABILITY_KEYS = ("fresh_session", "workspace_confined", "tool_log", "usage")
STATUSES = ("completed", "failed", "abandoned")
ISOLATION_USED = ("fresh", "shared", "unknown")
EVENT_KINDS = ("correction", "intervention", "note")
USAGE_KEYS = ("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens", "total_tokens")

MAX_JSON = 262144
MAX_RESPONSE = 1048576
MAX_TOOL_LOG = 8388608
MAX_TEXT = 4000
MAX_EVENTS = 9999

_RUN_ID = re.compile(r"r[0-9]{4}")
_CASE_ID = re.compile(r"[a-z][a-z0-9-]{0,40}")
_SEGMENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}")
_HEX64 = re.compile(r"[0-9a-f]{64}")
_PAGE = re.compile(r"07(0[1-9]|[1-9][0-9])\.[a-z0-9][a-z0-9-]{0,60}")
_PASS = re.compile(r"05\.[0-9]{2}")
_RUN_LINE = re.compile(r"Run:\s*(\S+)\s*")
_OUTCOME_LINE = re.compile(r"(?m)^[ \t*_`#>-]*Outcome:[ \t*_`]*([A-Za-z-]+)")
_REPARSE = 0x400

# Reviewed modules, pinned. Copied for the assisted condition or named for coordinator custody.
SUPPORT = (
    {"role": "assisted", "path": "labs/prime-review-pass01/prime_review.py", "copy_to": "support/prime_review.py",
     "sha256": "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0", "bytes": 58324},
    {"role": "assisted", "path": "labs/prime-review-pass01/README.md", "copy_to": "support/README.md",
     "sha256": "44b6b0c5b33700f058c2e8859d99f33c41643cc00baf6b4242270f366b5ee806", "bytes": 1899},
    {"role": "assisted", "path": "00.kernel/00.00.10.work/0512.prime-review/evidence/build05.01/CONTRACT.md",
     "copy_to": "support/CONTRACT.md",
     "sha256": "4235ff83966ea28a0264f03cfb57ccf98891203dbd2b73eb476aa0e6495f478b", "bytes": 14017},
    {"role": "custody", "path": "labs/return-capture-pass01/return_capture.py", "copy_to": None,
     "sha256": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac", "bytes": 45767},
    {"role": "custody", "path": "labs/return-capture-pass01/return_inspect.py", "copy_to": None,
     "sha256": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b", "bytes": 11402},
)

PROMPT = """# Prime review run {run_id}

Work only inside this folder. Read TASK.md, then everything in sources/.
This must be a fresh session with no earlier context. Do not open any other folder or repository.
No one will help or answer questions during this run.

## Tools
{tools}

## Response
Your final message is saved exactly as your answer. It must start with this line:

Run: {run_id}

The next line is `Outcome: <continue|director-input|develop|complete>`.
Then give your findings, the reasons and evidence for each, and one proposed next action.
"""

COORDINATOR = """# Coordinator steps for run {run_id}

Case {case_id} revision {revision}, condition {condition}. Model label {model}, effort label {effort}.
Candidate folder: {candidate}
Declared: fresh-session {fresh_session}, workspace-confined {workspace_confined}, tool-log {tool_log}, usage {usage}.

1. Start one new session with no earlier context. Confine it to the candidate folder only; it must not
   be able to read this run folder, the bench lab or the repository. If you cannot, record that below.
2. Paste PROMPT.md from the candidate folder as the first message. Record the start time.
3. Do not help, hint, repair or answer questions. Any help is an intervention and must be recorded.
4. Save the final message exactly, byte for byte, to a file outside the candidate folder. Export the
   tool log and usage if the surface offers them. Record the finish time.
5. Never reuse this session for another run, case or condition.
6. Collect:

python -B {module} collect --run-dir "{run_dir}" --expect-run {run_id} --expect-condition {condition} --status completed --label ACTUAL --session-label LABEL --isolation-used fresh|shared|unknown --response ABS [--tool-log ABS] [--tool-events ABS] [--usage ABS] --started ISO --finished ISO [--intervention TEXT]

A failed or abandoned run is collected with --status failed|abandoned --reason TEXT. It stays in the dataset.
"""


class Refused(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class Partial(Exception):
    def __init__(self, detail: str, written: list[str]) -> None:
        super().__init__(detail)
        self.detail = detail
        self.written = written


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dumps(obj: object) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def strict_json(data: bytes, what: str, limit: int = MAX_JSON) -> object:
    if len(data) > limit:
        raise Refused("too-large", f"{what} is over {limit} bytes")

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise Refused("malformed", f"{what} has a duplicate key: {key}")
            out[key] = value
        return out

    def constant(name):
        raise Refused("malformed", f"{what} has a non-finite number: {name}")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused("malformed", f"{what} is not UTF-8") from None
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except json.JSONDecodeError as exc:
        raise Refused("malformed", f"{what} is not JSON: {exc.msg}") from None


def exact_keys(obj: object, keys: tuple[str, ...] | set[str], what: str) -> dict:
    if not isinstance(obj, dict):
        raise Refused("malformed", f"{what} is not an object")
    if set(obj) != set(keys):
        missing = sorted(set(keys) - set(obj))
        extra = sorted(set(obj) - set(keys))
        raise Refused("malformed", f"{what} keys differ: missing {missing}, unknown {extra}")
    return obj


def need_text(value: object, what: str, limit: int = MAX_TEXT) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise Refused("malformed", f"{what} is not non-blank text up to {limit} characters")
    if any(ord(ch) < 32 and ch not in "\n\t" for ch in value):
        raise Refused("malformed", f"{what} has control characters")
    return value


def need_label(value: object, what: str) -> str:
    if not isinstance(value, str) or not (1 <= len(value) <= 80) or not value.isprintable() or value != value.strip():
        raise Refused("malformed", f"{what} is not a printable label of 1 to 80 characters")
    return value


def need_choice(value: object, choices: tuple[str, ...], what: str) -> str:
    if not isinstance(value, str) or value not in choices:
        raise Refused("malformed", f"{what} must be one of {', '.join(choices)}")
    return value


def need_hex(value: object, what: str) -> str:
    if not isinstance(value, str) or not _HEX64.fullmatch(value):
        raise Refused("malformed", f"{what} is not a lowercase sha256")
    return value


def need_count(value: object, what: str, nullable: bool = True) -> int | None:
    if value is None and nullable:
        return None
    if type(value) is not int or value < 0:
        raise Refused("malformed", f"{what} is not a non-negative integer")
    return value


def need_rel(value: object, what: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 240:
        raise Refused("unsafe-path", f"{what} is not a usable relative path")
    if "\\" in value or value.startswith("/") or ":" in value:
        raise Refused("unsafe-path", f"{what} is not a relative forward-slash path: {value}")
    for part in value.split("/"):
        if part in ("", ".", "..") or not _SEGMENT.fullmatch(part):
            raise Refused("unsafe-path", f"{what} has an unsafe segment: {value}")
    return value


def is_linked(path: Path) -> bool:
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(st.st_mode):
        return True
    return bool(getattr(st, "st_file_attributes", 0) & _REPARSE)


def need_abs(raw: str, what: str) -> Path:
    if not isinstance(raw, str) or not raw or any(ord(ch) < 32 for ch in raw):
        raise Refused("unsafe-path", f"{what} is not a usable path")
    if raw.startswith("\\\\") or raw.startswith("//"):
        raise Refused("unsafe-path", f"{what} is a UNC path")
    if not os.path.isabs(raw) or (os.name == "nt" and not re.match(r"[A-Za-z]:[\\/]", raw)):
        raise Refused("unsafe-path", f"{what} is not absolute")
    if any(part == ".." for part in re.split(r"[\\/]", raw)):
        raise Refused("unsafe-path", f"{what} has a parent segment")
    path = Path(os.path.normpath(raw))
    for item in [path, *path.parents]:
        if is_linked(item):
            raise Refused("unsafe-path", f"{what} has a link, junction or reparse point: {item}")
    return path


def read_regular(path: Path, what: str, limit: int) -> bytes:
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        raise Refused("missing", f"{what} is missing: {path}") from None
    if is_linked(path) or not stat.S_ISREG(st.st_mode):
        raise Refused("unsafe-path", f"{what} is not a regular file: {path}")
    if st.st_nlink != 1:
        raise Refused("unsafe-path", f"{what} has more than one hard link: {path}")
    if st.st_size > limit:
        raise Refused("too-large", f"{what} is over {limit} bytes")
    with open(path, "rb") as handle:
        data = handle.read(limit + 1)
    if len(data) > limit:
        raise Refused("too-large", f"{what} is over {limit} bytes")
    return data


def inside(child: Path, parent: Path) -> bool:
    a = os.path.normcase(os.path.abspath(child))
    b = os.path.normcase(os.path.abspath(parent))
    try:
        return os.path.commonpath([a, b]) == b
    except ValueError:
        return False


def fresh_dest(raw: str, what: str) -> Path:
    path = need_abs(raw, what)
    if os.path.lexists(path):
        raise Refused("occupied", f"{what} already exists: {path}")
    parent = path.parent
    if not parent.is_dir():
        raise Refused("unsafe-path", f"{what} parent is not an existing folder: {parent}")
    if inside(path, REPO):
        raise Refused("unsafe-path", f"{what} is inside the repository: {path}")
    return path


def existing_dir(raw: str, what: str) -> Path:
    path = need_abs(raw, what)
    if not path.is_dir():
        raise Refused("missing", f"{what} is not an existing folder: {path}")
    return path


def _write_file(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o644)
    try:
        view = memoryview(data)
        while view:
            done = os.write(fd, view)
            view = view[done:]
    finally:
        os.close(fd)


class Writer:
    """Exclusive creates only. Remembers what it wrote; never deletes."""

    def __init__(self) -> None:
        self.written: list[str] = []

    def mkdir(self, path: Path) -> None:
        os.mkdir(path)
        self.written.append(str(path))

    def file(self, path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.written.append(str(path))
        _write_file(path, data)


def guarded(writer: Writer, what: str, action) -> None:
    try:
        action()
    except Refused:
        raise
    except OSError as exc:
        retained = [w for w in writer.written if os.path.lexists(w)]
        raise Partial(f"{what} stopped after a write failure: {exc.strerror or exc}", retained) from None


# ---------------------------------------------------------------- bench

def _case_dirs() -> list[str]:
    root = LAB / "cases"
    if not root.is_dir():
        raise Refused("bench-drift", "cases folder is missing")
    return sorted(entry.name for entry in os.scandir(root))


def _case_files(case_id: str) -> list[str]:
    base = LAB / "cases" / case_id
    out = []
    for folder, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            full = Path(folder) / name
            rel = full.relative_to(base).as_posix()
            out.append(rel)
    return sorted(out)


def manifest_object() -> dict:
    """The bench.json object the files on disk describe now."""
    cases = []
    for case_id in _case_dirs():
        if not _CASE_ID.fullmatch(case_id):
            raise Refused("bench-drift", f"case folder name is unusable: {case_id}")
        files = []
        for rel in _case_files(case_id):
            need_rel(rel, f"case file {case_id}/{rel}")
            data = read_regular(LAB / "cases" / case_id / rel, f"case file {case_id}/{rel}", MAX_JSON)
            files.append({"path": rel, "sha256": sha256(data), "bytes": len(data)})
        meta = strict_json(read_regular(LAB / "cases" / case_id / "coordinator" / "meta.json", "meta", MAX_JSON), "meta")
        revision = meta.get("revision") if isinstance(meta, dict) else None
        cases.append({"case_id": case_id, "revision": revision, "files": files})
    cond = read_regular(LAB / "conditions.json", "conditions.json", MAX_JSON)
    return {
        "schema": SCHEMA_BENCH,
        "bench_id": "prime-bench-pass01",
        "rules": RULES,
        "conditions": {"path": "conditions.json", "sha256": sha256(cond), "bytes": len(cond)},
        "support": [{k: item[k] for k in ("role", "path", "copy_to", "sha256", "bytes")} for item in SUPPORT],
        "cases": cases,
    }


def _check_case_records(case_id: str, revision: object, files: set[str]) -> list[str]:
    problems = []
    for rel in ("candidate/TASK.md", "evaluator/key.json", "evaluator/rubric.json", "coordinator/meta.json"):
        if rel not in files:
            problems.append(f"{case_id}: {rel} is missing")
    if not any(rel.startswith("candidate/sources/") for rel in files):
        problems.append(f"{case_id}: no candidate sources")
    for rel in files:
        if rel.split("/")[0] not in ("candidate", "evaluator", "coordinator"):
            problems.append(f"{case_id}: {rel} is outside the three case trees")
    if problems:
        return problems
    base = LAB / "cases" / case_id
    key = load_key(base, case_id, revision)
    load_rubric(base, case_id, revision)
    meta = exact_keys(strict_json(read_regular(base / "coordinator/meta.json", "meta", MAX_JSON), "meta"),
                      ("schema", "case_id", "revision", "family", "variant", "matched_with", "label",
                       "decisive_evidence", "ambiguity", "provenance"), f"{case_id} meta")
    if meta["schema"] != SCHEMA_META or meta["case_id"] != case_id or meta["revision"] != revision:
        problems.append(f"{case_id}: meta identity differs")
    if meta["family"] not in FAMILIES or meta["variant"] not in VARIANTS:
        problems.append(f"{case_id}: family or variant is unknown")
    if meta["label"] != "SYNTHETIC":
        problems.append(f"{case_id}: meta label is not SYNTHETIC")
    if not isinstance(meta["provenance"], list) or not meta["provenance"]:
        problems.append(f"{case_id}: provenance is empty")
    else:
        for item in meta["provenance"]:
            exact_keys(item, ("path", "sha256", "rule"), f"{case_id} provenance")
            need_rel(item["path"], f"{case_id} provenance path")
            need_hex(item["sha256"], f"{case_id} provenance sha256")
            need_text(item["rule"], f"{case_id} provenance rule")
    if not key["canary"]:
        problems.append(f"{case_id}: canary is empty")
    return problems


def load_key(base: Path, case_id: str, revision: object) -> dict:
    key = exact_keys(strict_json(read_regular(base / "evaluator/key.json", "key", MAX_JSON), "key"),
                     ("schema", "case_id", "revision", "canary", "outcomes", "must_mention", "must_quote", "must_not"),
                     f"{case_id} key")
    if key["schema"] != SCHEMA_KEY or key["case_id"] != case_id or key["revision"] != revision:
        raise Refused("malformed", f"{case_id} key identity differs")
    need_label(key["canary"], f"{case_id} canary")
    if not isinstance(key["outcomes"], list) or not key["outcomes"] or any(o not in OUTCOMES for o in key["outcomes"]):
        raise Refused("malformed", f"{case_id} key outcomes are unusable")
    if not isinstance(key["must_mention"], list) or not all(
            isinstance(g, list) and g and all(isinstance(s, str) and s for s in g) for g in key["must_mention"]):
        raise Refused("malformed", f"{case_id} must_mention is unusable")
    if not isinstance(key["must_quote"], list) or not all(isinstance(s, str) and s for s in key["must_quote"]):
        raise Refused("malformed", f"{case_id} must_quote is unusable")
    if not isinstance(key["must_not"], list):
        raise Refused("malformed", f"{case_id} must_not is unusable")
    for pattern in key["must_not"]:
        try:
            re.compile(pattern)
        except (re.error, TypeError):
            raise Refused("malformed", f"{case_id} must_not has an unusable pattern") from None
    return key


def load_rubric(base: Path, case_id: str, revision: object) -> dict:
    rubric = exact_keys(strict_json(read_regular(base / "evaluator/rubric.json", "rubric", MAX_JSON), "rubric"),
                        ("schema", "case_id", "revision", "scale", "items"), f"{case_id} rubric")
    if rubric["schema"] != SCHEMA_RUBRIC or rubric["case_id"] != case_id or rubric["revision"] != revision:
        raise Refused("malformed", f"{case_id} rubric identity differs")
    if not isinstance(rubric["scale"], list) or not rubric["scale"] or any(type(v) is not int for v in rubric["scale"]):
        raise Refused("malformed", f"{case_id} rubric scale is unusable")
    ids = []
    if not isinstance(rubric["items"], list) or not rubric["items"]:
        raise Refused("malformed", f"{case_id} rubric items are empty")
    for item in rubric["items"]:
        exact_keys(item, ("id", "text"), f"{case_id} rubric item")
        need_label(item["id"], "rubric item id")
        need_text(item["text"], "rubric item text")
        ids.append(item["id"])
    if len(set(ids)) != len(ids):
        raise Refused("malformed", f"{case_id} rubric item ids repeat")
    return rubric


def validate() -> dict:
    """Re-hash the bench against bench.json and the support pins. Refusals are malformed bench files."""
    raw = read_regular(LAB / "bench.json", "bench.json", MAX_JSON)
    recorded = strict_json(raw, "bench.json")
    current = manifest_object()
    drift = []
    if recorded != current:
        rec = recorded if isinstance(recorded, dict) else {}
        for key in sorted(set(rec) | set(current)):
            if rec.get(key) != current.get(key):
                drift.append(f"bench.json {key} differs from the files on disk")
    for item in SUPPORT:
        try:
            data = read_regular(REPO / item["path"], item["path"], 1 << 22)
        except Refused as exc:
            drift.append(f"support {item['path']}: {exc.detail}")
            continue
        if sha256(data) != item["sha256"] or len(data) != item["bytes"]:
            drift.append(f"support {item['path']} differs from its pin")
    cond = exact_keys(strict_json(read_regular(LAB / "conditions.json", "conditions.json", MAX_JSON), "conditions"),
                      ("schema", "baseline", "assisted"), "conditions")
    if cond["schema"] != SCHEMA_CONDITIONS:
        drift.append("conditions schema differs")
    for name in CONDITIONS:
        entry = exact_keys(cond[name], ("tools", "support"), f"condition {name}")
        need_text(entry["tools"], f"{name} tools")
        wanted = [s["copy_to"] for s in SUPPORT if s["role"] == "assisted"] if name == "assisted" else []
        if entry["support"] != wanted:
            drift.append(f"condition {name} support differs from the pinned copy list")
    families: dict[tuple[str, str], str] = {}
    canaries = {}
    for case in current["cases"]:
        files = {f["path"] for f in case["files"]}
        problems = _check_case_records(case["case_id"], case["revision"], files)
        drift.extend(problems)
        if problems:
            continue
        base = LAB / "cases" / case["case_id"]
        meta = strict_json(read_regular(base / "coordinator/meta.json", "meta", MAX_JSON), "meta")
        families[(meta["family"], meta["variant"])] = case["case_id"]
        canaries[case["case_id"]] = load_key(base, case["case_id"], case["revision"])["canary"]
    for family in FAMILIES:
        for variant in VARIANTS:
            if (family, variant) not in families:
                drift.append(f"family {family} variant {variant} has no case")
    for (family, variant), case_id in families.items():
        meta = strict_json(read_regular(LAB / "cases" / case_id / "coordinator/meta.json", "meta", MAX_JSON), "meta")
        other = families.get((family, "b" if variant == "a" else "a"))
        if meta["matched_with"] != other:
            drift.append(f"{case_id}: matched_with is not its other variant")
    leaks = candidate_leaks(current, canaries)
    drift.extend(leaks)
    return {
        "schema": "prime-bench-validation/1",
        "result": "valid" if not drift else "drift",
        "bench_version": sha256(raw),
        "cases": [c["case_id"] for c in current["cases"]],
        "drift": drift,
    }


def candidate_leaks(manifest: dict, canaries: dict[str, str]) -> list[str]:
    """Any canary or evaluator/coordinator bytes inside any case's candidate files."""
    secret: list[tuple[str, bytes]] = [(f"canary of {cid}", c.encode("utf-8")) for cid, c in canaries.items()]
    candidates: list[tuple[str, bytes]] = []
    for case in manifest["cases"]:
        base = LAB / "cases" / case["case_id"]
        for f in case["files"]:
            data = read_regular(base / f["path"], f["path"], MAX_JSON)
            if f["path"].startswith("candidate/"):
                candidates.append((f"{case['case_id']}/{f['path']}", data))
            else:
                secret.append((f"{case['case_id']}/{f['path']}", data))
    return leak_hits(candidates, secret)


def leak_hits(candidates: list[tuple[str, bytes]], secret: list[tuple[str, bytes]]) -> list[str]:
    hits = []
    for name, data in candidates:
        for label, needle in secret:
            if needle and needle in data:
                hits.append(f"evaluator-leakage: {label} appears in {name}")
    return hits


def bench_state() -> tuple[dict, str, dict[str, str]]:
    result = validate()
    if result["result"] != "valid":
        raise Refused("bench-drift", "; ".join(result["drift"]))
    manifest = manifest_object()
    canaries = {c["case_id"]: load_key(LAB / "cases" / c["case_id"], c["case_id"], c["revision"])["canary"]
                for c in manifest["cases"]}
    return manifest, result["bench_version"], canaries


def all_canaries() -> list[str]:
    """Canaries of the bench as it is now, read without requiring a clean bench."""
    out = []
    root = LAB / "cases"
    for case_id in _case_dirs():
        try:
            key = strict_json(read_regular(root / case_id / "evaluator/key.json", "key", MAX_JSON), "key")
        except Refused:
            continue
        if isinstance(key, dict) and isinstance(key.get("canary"), str) and key["canary"]:
            out.append(key["canary"])
    return out


# ---------------------------------------------------------------- investigation

def load_investigation(raw: str) -> tuple[dict, bytes]:
    path = need_abs(raw, "investigation")
    data = read_regular(path, "investigation", MAX_JSON)
    inv = exact_keys(strict_json(data, "investigation"),
                     ("schema", "page", "pass", "question", "director_replies", "sources", "coordinator_label"),
                     "investigation")
    if inv["schema"] != SCHEMA_INVESTIGATION:
        raise Refused("malformed", "investigation schema differs")
    if not isinstance(inv["page"], str) or not _PAGE.fullmatch(inv["page"]):
        raise Refused("malformed", "investigation page is not 07NN.slug in 0701-0799")
    if not isinstance(inv["pass"], str) or not _PASS.fullmatch(inv["pass"]):
        raise Refused("malformed", "investigation pass is not 05.NN")
    need_text(inv["question"], "investigation question")
    need_label(inv["coordinator_label"], "coordinator label")
    if not isinstance(inv["director_replies"], list) or len(inv["director_replies"]) > 24:
        raise Refused("malformed", "director_replies is not a list of up to 24")
    for reply in inv["director_replies"]:
        exact_keys(reply, ("reply", "source_path", "source_sha256"), "director reply")
        if not isinstance(reply["reply"], str) or not reply["reply"] or len(reply["reply"]) > MAX_TEXT:
            raise Refused("malformed", "director reply is not kept text")
        need_rel(reply["source_path"], "director reply source")
        need_hex(reply["source_sha256"], "director reply source sha256")
    if not isinstance(inv["sources"], list) or len(inv["sources"]) > 64:
        raise Refused("malformed", "investigation sources is not a list of up to 64")
    for source in inv["sources"]:
        exact_keys(source, ("path", "sha256"), "investigation source")
        need_rel(source["path"], "investigation source path")
        need_hex(source["sha256"], "investigation source sha256")
    return inv, data


# ---------------------------------------------------------------- prepare

def prepare(args: argparse.Namespace) -> dict:
    run_id = args.run_id
    if not isinstance(run_id, str) or not _RUN_ID.fullmatch(run_id):
        raise Refused("malformed", "run id is not r followed by four digits")
    condition = need_choice(args.condition, CONDITIONS, "condition")
    model = need_label(args.model_label, "model label")
    effort = need_label(args.effort_label, "effort label")
    caps = {
        "fresh_session": need_choice(args.fresh_session, CAPABILITY, "fresh-session"),
        "workspace_confined": need_choice(args.workspace_confined, CAPABILITY, "workspace-confined"),
        "tool_log": need_choice(args.tool_log, CAPABILITY, "tool-log"),
        "usage": need_choice(args.usage, CAPABILITY, "usage"),
    }
    inv, inv_bytes = load_investigation(args.investigation)
    run_dir = fresh_dest(args.run_dir, "run folder")
    cand_dir = fresh_dest(args.candidate_dir, "candidate folder")
    if inside(run_dir, cand_dir) or inside(cand_dir, run_dir):
        raise Refused("unsafe-path", "run and candidate folders must not contain each other")
    if inside(run_dir, LAB) or inside(cand_dir, LAB):
        raise Refused("unsafe-path", "a run folder cannot sit inside the bench lab")
    manifest, version, canaries = bench_state()
    case = next((c for c in manifest["cases"] if c["case_id"] == args.case), None)
    if case is None:
        raise Refused("malformed", f"case is not in the bench: {args.case}")
    base = LAB / "cases" / case["case_id"]
    cond = strict_json(read_regular(LAB / "conditions.json", "conditions.json", MAX_JSON), "conditions")[condition]

    files: dict[str, bytes] = {}
    for f in case["files"]:
        if f["path"].startswith("candidate/"):
            files[f["path"][len("candidate/"):]] = read_regular(base / f["path"], f["path"], MAX_JSON)
    if condition == "assisted":
        for item in SUPPORT:
            if item["role"] != "assisted":
                continue
            data = read_regular(REPO / item["path"], item["path"], 1 << 22)
            if sha256(data) != item["sha256"]:
                raise Refused("bench-drift", f"support {item['path']} differs from its pin")
            files[item["copy_to"]] = data
    files["PROMPT.md"] = PROMPT.format(run_id=run_id, tools=cond["tools"]).encode("utf-8")

    secret = [(f"canary of {cid}", c.encode("utf-8")) for cid, c in canaries.items()]
    for other in manifest["cases"]:
        for f in other["files"]:
            if not f["path"].startswith("candidate/"):
                secret.append((f"{other['case_id']}/{f['path']}",
                               read_regular(LAB / "cases" / other["case_id"] / f["path"], f["path"], MAX_JSON)))
    leaks = leak_hits(sorted(files.items()), secret)
    if leaks:
        raise Refused("evaluator-leakage", "; ".join(leaks))

    pins = {
        "task_sha256": sha256(files["TASK.md"]),
        "key_sha256": sha256(read_regular(base / "evaluator/key.json", "key", MAX_JSON)),
        "rubric_sha256": sha256(read_regular(base / "evaluator/rubric.json", "rubric", MAX_JSON)),
        "candidate_files": [{"path": p, "sha256": sha256(d), "bytes": len(d)} for p, d in sorted(files.items())],
    }
    run = {
        "schema": SCHEMA_RUN,
        "run_id": run_id,
        "bench_version": version,
        "investigation_sha256": sha256(inv_bytes),
        "investigation": {"page": inv["page"], "pass": inv["pass"]},
        "case_id": case["case_id"],
        "case_revision": case["revision"],
        "condition": condition,
        "model_label": model,
        "effort_label": effort,
        "capabilities": caps,
        "candidate_dir": str(cand_dir),
        "pins": pins,
        "prepared_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    coordinator = COORDINATOR.format(
        run_id=run_id, case_id=case["case_id"], revision=case["revision"], condition=condition, model=model,
        effort=effort, candidate=cand_dir, module=Path(os.path.abspath(__file__)), run_dir=run_dir, **caps)

    writer = Writer()

    def write_all() -> None:
        writer.mkdir(cand_dir)
        for rel, data in sorted(files.items()):
            target = cand_dir.joinpath(*rel.split("/"))
            writer.file(target, data)
        for rel, data in files.items():
            if read_regular(cand_dir.joinpath(*rel.split("/")), rel, 1 << 22) != data:
                raise OSError(f"candidate file differs after write: {rel}")
        writer.mkdir(run_dir)
        writer.file(run_dir / "COORDINATOR.md", coordinator.encode("utf-8"))
        writer.file(run_dir / "run.json", dumps(run))

    guarded(writer, "prepare", write_all)
    return {"result": "prepared", "run_id": run_id, "case_id": case["case_id"], "condition": condition,
            "run_dir": str(run_dir), "candidate_dir": str(cand_dir), "candidate_files": len(files),
            "bench_version": version}


# ---------------------------------------------------------------- collect

def load_run(run_dir: Path) -> dict:
    path = run_dir / "run.json"
    if not os.path.lexists(path):
        raise Refused("partial-present", f"run folder has no run.json (unprepared or partial): {run_dir}")
    run = exact_keys(strict_json(read_regular(path, "run.json", MAX_JSON), "run.json"),
                     ("schema", "run_id", "bench_version", "investigation_sha256", "investigation", "case_id",
                      "case_revision", "condition", "model_label", "effort_label", "capabilities", "candidate_dir",
                      "pins", "prepared_at"), "run.json")
    if run["schema"] != SCHEMA_RUN or not isinstance(run["run_id"], str) or not _RUN_ID.fullmatch(run["run_id"]):
        raise Refused("malformed", "run.json identity is unusable")
    need_choice(run["condition"], CONDITIONS, "run condition")
    need_hex(run["bench_version"], "run bench version")
    need_hex(run["investigation_sha256"], "run investigation sha256")
    exact_keys(run["capabilities"], CAPABILITY_KEYS, "run capabilities")
    exact_keys(run["pins"], ("task_sha256", "key_sha256", "rubric_sha256", "candidate_files"), "run pins")
    return run


def parse_time(raw: str | None, what: str) -> str | None:
    if raw is None:
        return None
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        raise Refused("malformed", f"{what} is not ISO-8601") from None
    if value.tzinfo is None:
        raise Refused("malformed", f"{what} has no UTC offset")
    return raw


def run_line(response: bytes) -> str | None:
    text = response.decode("utf-8", errors="replace")
    for line in text.splitlines():
        if line.strip():
            match = _RUN_LINE.fullmatch(line.strip().strip("*`"))
            return match.group(1) if match else None
    return None


def parse_tool_events(data: bytes) -> int:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused("malformed", "tool events are not UTF-8") from None
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    for number, line in enumerate(lines, 1):
        item = exact_keys(strict_json(line.encode("utf-8"), f"tool event line {number}"),
                          ("schema", "tool", "at"), f"tool event line {number}")
        if item["schema"] != SCHEMA_TOOL_EVENT:
            raise Refused("malformed", f"tool event line {number} schema differs")
        need_label(item["tool"], f"tool event line {number} tool")
        if item["at"] is not None:
            parse_time(item["at"], f"tool event line {number} time")
    return len(lines)


def parse_usage(data: bytes) -> dict:
    usage = strict_json(data, "usage")
    if not isinstance(usage, dict) or "source" not in usage:
        raise Refused("malformed", "usage needs a source")
    unknown = sorted(set(usage) - set(USAGE_KEYS) - {"source"})
    if unknown:
        raise Refused("malformed", f"usage has unknown keys: {unknown}")
    need_label(usage["source"], "usage source")
    for key in USAGE_KEYS:
        if key in usage:
            need_count(usage[key], f"usage {key}", nullable=False)
    return usage


def collect(args: argparse.Namespace) -> dict:
    run_dir = existing_dir(args.run_dir, "run folder")
    run = load_run(run_dir)
    if args.expect_run != run["run_id"] or args.expect_condition != run["condition"]:
        raise Refused("wrong-identity",
                      f"run folder holds {run['run_id']} {run['condition']}, not {args.expect_run} {args.expect_condition}")
    status = need_choice(args.status, STATUSES, "status")
    label = need_choice(args.label, ("SYNTHETIC", "ACTUAL"), "label")
    session = need_label(args.session_label, "session label")
    isolation = need_choice(args.isolation_used, ISOLATION_USED, "isolation used")
    reason = None if args.reason is None else need_text(args.reason, "reason")
    intervention = None if args.intervention is None else need_text(args.intervention, "intervention")
    if status == "completed" and args.response is None:
        raise Refused("malformed", "a completed run needs --response")
    if status == "completed" and reason is not None:
        raise Refused("malformed", "a completed run takes no --reason")
    if status != "completed" and reason is None:
        raise Refused("malformed", f"a {status} run needs --reason")
    started = parse_time(args.started, "started")
    finished = parse_time(args.finished, "finished")
    if started and finished and datetime.fromisoformat(finished.replace("Z", "+00:00")) < datetime.fromisoformat(
            started.replace("Z", "+00:00")):
        raise Refused("malformed", "finished is before started")

    inputs: dict[str, tuple[str, bytes] | None] = {}
    for name, raw, limit, out in (("response", args.response, MAX_RESPONSE, "response.txt"),
                                  ("tool_log", args.tool_log, MAX_TOOL_LOG, "tool-log.raw"),
                                  ("tool_events", args.tool_events, MAX_TOOL_LOG, "tool-events.jsonl"),
                                  ("usage", args.usage, MAX_JSON, "usage.json")):
        if raw is None:
            inputs[name] = None
            continue
        path = need_abs(raw, name)
        if inside(path, run_dir):
            raise Refused("unsafe-path", f"{name} is inside the run folder")
        inputs[name] = (out, read_regular(path, name, limit))

    identity = "unavailable"
    if inputs["response"] is not None:
        found = run_line(inputs["response"][1])
        if found is None:
            identity = "missing"
        elif found != run["run_id"]:
            raise Refused("wrong-identity", f"response names run {found}, not {run['run_id']}")
        else:
            identity = "matched"
    tool_event_count = parse_tool_events(inputs["tool_events"][1]) if inputs["tool_events"] else None
    usage = parse_usage(inputs["usage"][1]) if inputs["usage"] else None
    scanned = b"".join(item[1] for key, item in inputs.items() if item and key in ("response", "tool_log"))
    leakage = any(c.encode("utf-8") in scanned for c in all_canaries())

    record = {
        "schema": SCHEMA_COLLECTION,
        "run_id": run["run_id"],
        "condition": run["condition"],
        "status": status,
        "reason": reason,
        "label": label,
        "session_label": session,
        "isolation_used": isolation,
        "started": started,
        "finished": finished,
        "times_source": "coordinator-supplied",
        "intervention": intervention,
        "identity": identity,
        "leakage": leakage,
        "files": {name: (None if item is None else {"path": f"collected/{item[0]}", "sha256": sha256(item[1]),
                                                    "bytes": len(item[1])}) for name, item in inputs.items()},
        "tool_event_count": tool_event_count,
        "usage": usage,
    }
    record_bytes = dumps(record)
    existing = run_dir / "collection.json"
    if os.path.lexists(existing):
        same = read_regular(existing, "collection.json", MAX_JSON) == record_bytes and all(
            item is None or read_regular(run_dir / "collected" / item[0], item[0], MAX_TOOL_LOG) == item[1]
            for item in inputs.values())
        raise Refused("already-collected" if same else "conflict",
                      "run is already collected; nothing was written" if same
                      else "run is already collected with different content; nothing was written")
    if os.path.lexists(run_dir / "collected"):
        raise Refused("partial-present", "collected/ exists without collection.json; it is kept as found")

    writer = Writer()

    def write_all() -> None:
        writer.mkdir(run_dir / "collected")
        for item in inputs.values():
            if item is not None:
                writer.file(run_dir / "collected" / item[0], item[1])
        writer.file(existing, record_bytes)

    guarded(writer, "collect", write_all)
    return {"result": "collected", "run_id": run["run_id"], "status": status, "identity": identity,
            "leakage": leakage, "collection_sha256": sha256(record_bytes)}


def load_collection(run_dir: Path) -> tuple[dict, bytes] | None:
    path = run_dir / "collection.json"
    if not os.path.lexists(path):
        return None
    data = read_regular(path, "collection.json", MAX_JSON)
    col = strict_json(data, "collection.json")
    if not isinstance(col, dict) or col.get("schema") != SCHEMA_COLLECTION:
        raise Refused("malformed", "collection.json schema differs")
    for name, item in col["files"].items():
        if item is None:
            continue
        rel = need_rel(item["path"], f"collected {name}")
        got = read_regular(run_dir.joinpath(*rel.split("/")), rel, MAX_TOOL_LOG)
        if sha256(got) != item["sha256"]:
            raise Refused("tampered", f"collected {name} differs from collection.json")
    return col, data


# ---------------------------------------------------------------- events

def load_events(run_dir: Path) -> list[dict]:
    folder = run_dir / "events"
    if not os.path.lexists(folder):
        return []
    out = []
    for name in sorted(os.listdir(folder)):
        if not re.fullmatch(r"[0-9]{4}\.json", name):
            continue
        out.append(strict_json(read_regular(folder / name, name, MAX_JSON), name))
    return out


def event(args: argparse.Namespace) -> dict:
    run_dir = existing_dir(args.run_dir, "run folder")
    run = load_run(run_dir)
    loaded = load_collection(run_dir)
    if loaded is None:
        raise Refused("not-collected", "events follow a collection; collect first")
    _col, col_bytes = loaded
    kind = need_choice(args.kind, EVENT_KINDS, "event kind")
    text = need_text(args.text, "event text")
    attachment = None
    if args.attachment is not None:
        path = need_abs(args.attachment, "attachment")
        if inside(path, run_dir):
            raise Refused("unsafe-path", "attachment is inside the run folder")
        attachment = read_regular(path, "attachment", MAX_RESPONSE)
    folder = run_dir / "events"
    seq = len([n for n in (os.listdir(folder) if folder.is_dir() else []) if re.fullmatch(r"[0-9]{4}\.json", n)]) + 1
    if seq > MAX_EVENTS:
        raise Refused("too-large", "event limit reached")
    record = {
        "schema": SCHEMA_EVENT,
        "run_id": run["run_id"],
        "seq": seq,
        "kind": kind,
        "text": text,
        "follows_collection_sha256": sha256(col_bytes),
        "attachment": None if attachment is None else {"path": f"events/{seq:04d}.attachment",
                                                       "sha256": sha256(attachment), "bytes": len(attachment)},
    }
    writer = Writer()

    def write_all() -> None:
        if not folder.is_dir():
            writer.mkdir(folder)
        if attachment is not None:
            writer.file(folder / f"{seq:04d}.attachment", attachment)
        writer.file(folder / f"{seq:04d}.json", dumps(record))

    guarded(writer, "event", write_all)
    return {"result": "recorded", "run_id": run["run_id"], "seq": seq, "kind": kind}


# ---------------------------------------------------------------- assess

def pinned_case(run: dict) -> tuple[dict, dict]:
    base = LAB / "cases" / run["case_id"]
    if not _CASE_ID.fullmatch(run["case_id"]) or not base.is_dir():
        raise Refused("key-changed", f"case {run['case_id']} is not in the bench")
    pins = run["pins"]
    for rel, pin, what in (("evaluator/key.json", pins["key_sha256"], "key"),
                           ("evaluator/rubric.json", pins["rubric_sha256"], "rubric"),
                           ("candidate/TASK.md", pins["task_sha256"], "task")):
        if sha256(read_regular(base / rel, rel, MAX_JSON)) != pin:
            raise Refused("key-changed" if what != "rubric" else "rubric-changed",
                          f"{run['case_id']} {what} differs from the pin taken at prepare; no post-answer grading change")
    return load_key(base, run["case_id"], run["case_revision"]), load_rubric(base, run["case_id"], run["case_revision"])


def assess_run(run_dir: Path) -> dict:
    run = load_run(run_dir)
    key, _rubric = pinned_case(run)
    loaded = load_collection(run_dir)
    out = {"schema": SCHEMA_ASSESSMENT, "run_id": run["run_id"], "case_id": run["case_id"],
           "case_revision": run["case_revision"], "condition": run["condition"], "kind": "deterministic string checks"}
    response = None
    if loaded is not None and loaded[0]["files"]["response"] is not None:
        rel = loaded[0]["files"]["response"]["path"]
        response = read_regular(run_dir.joinpath(*rel.split("/")), rel, MAX_RESPONSE).decode("utf-8", errors="replace")
    if response is None:
        out.update({"response": "unavailable", "deterministic_pass": False, "checks": None})
        return out
    lowered = response.casefold()
    found = _OUTCOME_LINE.search(response)
    outcome = found.group(1).lower() if found else None
    checks = {
        "run_line": "matched" if run_line(response.encode("utf-8")) == run["run_id"] else "missing",
        "outcome": {"found": outcome, "pass": outcome in key["outcomes"]},
        "must_mention": [{"any_of": group, "pass": any(s.casefold() in lowered for s in group)}
                         for group in key["must_mention"]],
        "must_quote": [{"quote": q, "pass": q in response} for q in key["must_quote"]],
        "must_not": [{"pattern": p, "pass": re.search(p, response) is None} for p in key["must_not"]],
        "canary_absent": key["canary"] not in response,
    }
    passed = (checks["run_line"] == "matched" and checks["outcome"]["pass"] and checks["canary_absent"]
              and all(c["pass"] for c in checks["must_mention"] + checks["must_quote"] + checks["must_not"]))
    out.update({"response": "present", "checks": checks, "deterministic_pass": passed})
    return out


# ---------------------------------------------------------------- review

def review(args: argparse.Namespace) -> dict:
    run_dir = existing_dir(args.run_dir, "run folder")
    run = load_run(run_dir)
    _key, rubric = pinned_case(run)
    if load_collection(run_dir) is None:
        raise Refused("not-collected", "a review follows a collection; collect first")
    path = need_abs(args.record, "review record")
    data = read_regular(path, "review record", MAX_JSON)
    rec = exact_keys(strict_json(data, "review record"),
                     ("schema", "run_id", "case_id", "case_revision", "rubric_sha256", "reviewer_label",
                      "blind_to_condition", "scores", "reviewer_minutes", "director_attention_events", "notes"),
                     "review record")
    if rec["schema"] != SCHEMA_REVIEW:
        raise Refused("malformed", "review schema differs")
    if rec["run_id"] != run["run_id"] or rec["case_id"] != run["case_id"] or rec["case_revision"] != run["case_revision"]:
        raise Refused("wrong-identity", "review names another run, case or revision")
    if need_hex(rec["rubric_sha256"], "review rubric sha256") != run["pins"]["rubric_sha256"]:
        raise Refused("rubric-changed", "review was made against a different rubric")
    need_label(rec["reviewer_label"], "reviewer label")
    if rec["blind_to_condition"] not in (True, False, None):
        raise Refused("malformed", "blind_to_condition is not true, false or null")
    need_count(rec["reviewer_minutes"], "reviewer_minutes")
    need_count(rec["director_attention_events"], "director_attention_events")
    if rec["notes"] is not None:
        need_text(rec["notes"], "review notes")
    if not isinstance(rec["scores"], list):
        raise Refused("malformed", "scores is not a list")
    wanted = [item["id"] for item in rubric["items"]]
    seen = []
    for score in rec["scores"]:
        exact_keys(score, ("item", "score", "note"), "score")
        if score["item"] not in wanted or score["item"] in seen:
            raise Refused("malformed", f"score item is unknown or repeated: {score['item']}")
        if type(score["score"]) is not int or score["score"] not in rubric["scale"]:
            raise Refused("malformed", f"score for {score['item']} is not in the scale")
        if score["note"] is not None:
            need_text(score["note"], "score note")
        seen.append(score["item"])
    if sorted(seen) != sorted(wanted):
        raise Refused("malformed", "scores do not cover every rubric item exactly once")
    target = run_dir / "review.json"
    if os.path.lexists(target):
        same = read_regular(target, "review.json", MAX_JSON) == data
        raise Refused("already-reviewed" if same else "conflict",
                      "run already has this review; nothing was written" if same
                      else "run already has a different review; nothing was written")
    writer = Writer()
    guarded(writer, "review", lambda: writer.file(target, data))
    return {"result": "reviewed", "run_id": run["run_id"], "review_sha256": sha256(data)}


def load_review(run_dir: Path) -> dict | None:
    path = run_dir / "review.json"
    if not os.path.lexists(path):
        return None
    return strict_json(read_regular(path, "review.json", MAX_JSON), "review.json")


# ---------------------------------------------------------------- compare

def _elapsed(col: dict) -> float | None:
    if not col.get("started") or not col.get("finished"):
        return None
    a = datetime.fromisoformat(col["started"].replace("Z", "+00:00"))
    b = datetime.fromisoformat(col["finished"].replace("Z", "+00:00"))
    return (b - a).total_seconds()


def record_hashes(run_dir: Path) -> dict:
    """sha256 of every record file in a run folder, so a comparison binds the records it read."""
    out = {}
    for sub in ("", "collected", "events"):
        folder = run_dir / sub if sub else run_dir
        if not folder.is_dir():
            continue
        for name in sorted(os.listdir(folder)):
            path = folder / name
            if path.is_file():
                rel = f"{sub}/{name}" if sub else name
                out[rel] = sha256(read_regular(path, rel, MAX_TOOL_LOG))
    return out


def compare_runs(raw_dirs: list[str]) -> dict:
    if not raw_dirs:
        raise Refused("malformed", "compare needs at least one run folder")
    dirs = [existing_dir(raw, "run folder") for raw in raw_dirs]
    normal = [os.path.normcase(os.path.abspath(d)) for d in dirs]
    if len(set(normal)) != len(normal):
        raise Refused("duplicate", "a run folder is given twice")
    runs = [load_run(d) for d in dirs]
    ids = [r["run_id"] for r in runs]
    if len(set(ids)) != len(ids):
        raise Refused("duplicate", "two run folders carry the same run id")
    if len({r["bench_version"] for r in runs}) != 1:
        raise Refused("mixed-version", "runs were prepared from different bench versions")
    if len({r["investigation_sha256"] for r in runs}) != 1:
        raise Refused("mixed-investigation", "runs are bound to different investigations")
    metas = {}
    rows = []
    sessions: dict[str, list[str]] = {}
    for run_dir, run in zip(dirs, runs):
        loaded = load_collection(run_dir)
        col = loaded[0] if loaded else None
        if col is not None:
            if col["run_id"] != run["run_id"] or col["condition"] != run["condition"]:
                raise Refused("wrong-identity", f"{run_dir} collection names another run or condition")
            sessions.setdefault(col["session_label"], []).append(run["run_id"])
        if run["case_id"] not in metas:
            metas[run["case_id"]] = strict_json(read_regular(
                LAB / "cases" / run["case_id"] / "coordinator/meta.json", "meta", MAX_JSON), "meta")
        rows.append((run_dir, run, col))
    out_rows = []
    for run_dir, run, col in rows:
        assessment = assess_run(run_dir)
        rev = load_review(run_dir)
        events = load_events(run_dir)
        reasons = []
        if col is None:
            reasons.append("uncollected")
        else:
            if col["status"] != "completed":
                reasons.append(col["status"])
            if run["capabilities"]["fresh_session"] != "supported":
                reasons.append(f"fresh-session {run['capabilities']['fresh_session']}")
            if run["capabilities"]["workspace_confined"] != "supported":
                reasons.append(f"workspace-confined {run['capabilities']['workspace_confined']}")
            if col["isolation_used"] != "fresh":
                reasons.append(f"isolation used {col['isolation_used']}")
            if len(sessions.get(col["session_label"], [])) > 1:
                reasons.append("shared session: " + ", ".join(sessions[col["session_label"]]))
            if col["intervention"] is not None or any(e.get("kind") == "intervention" for e in events):
                reasons.append("intervention")
            if col["leakage"]:
                reasons.append("evaluator-leakage")
            if col["status"] == "completed" and col["identity"] != "matched":
                reasons.append(f"identity {col['identity']}")
        meta = metas[run["case_id"]]
        out_rows.append({
            "run_id": run["run_id"],
            "case_id": run["case_id"],
            "case_revision": run["case_revision"],
            "family": meta["family"],
            "variant": meta["variant"],
            "condition": run["condition"],
            "model_label": run["model_label"],
            "effort_label": run["effort_label"],
            "label": None if col is None else col["label"],
            "status": "uncollected" if col is None else col["status"],
            "clean": not reasons,
            "not_clean_reasons": reasons,
            "deterministic_pass": assessment["deterministic_pass"],
            "outcome_found": (assessment["checks"] or {}).get("outcome", {}).get("found"),
            "assessment": assessment,
            "review": None if rev is None else {
                "reviewer_label": rev["reviewer_label"], "blind_to_condition": rev["blind_to_condition"],
                "scores": {s["item"]: s["score"] for s in rev["scores"]},
                "reviewer_minutes": rev["reviewer_minutes"],
                "director_attention_events": rev["director_attention_events"]},
            "elapsed_seconds": None if col is None else _elapsed(col),
            "tool_events": None if col is None else col["tool_event_count"],
            "usage": None if col is None else col["usage"],
            "records": record_hashes(run_dir),
            "corrections": sum(1 for e in events if e.get("kind") == "correction"),
            "interventions": sum(1 for e in events if e.get("kind") == "intervention")
            + (1 if col is not None and col["intervention"] is not None else 0),
        })
    counts = {}
    for cond in CONDITIONS:
        mine = [r for r in out_rows if r["condition"] == cond]
        clean = [r for r in mine if r["clean"]]
        items: dict[str, dict] = {}
        for r in clean:
            if r["review"]:
                for item, score in r["review"]["scores"].items():
                    slot = items.setdefault(item, {"reviewed_clean_runs": 0, "score_sum": 0})
                    slot["reviewed_clean_runs"] += 1
                    slot["score_sum"] += score
        counts[cond] = {
            "runs": len(mine),
            "by_status": {s: sum(1 for r in mine if r["status"] == s) for s in (*STATUSES, "uncollected")},
            "clean": len(clean),
            "clean_deterministic_pass": sum(1 for r in clean if r["deterministic_pass"]),
            "rubric_items": dict(sorted(items.items())),
        }
    inv = runs[0]["investigation"]
    result = {
        "schema": SCHEMA_COMPARISON,
        "bench_version": runs[0]["bench_version"],
        "investigation_sha256": runs[0]["investigation_sha256"],
        "investigation": inv,
        "synthetic": any(r["label"] == "SYNTHETIC" for r in out_rows),
        "rows": out_rows,
        "counts": counts,
        "not_computed": ["ratios between conditions", "time or token savings", "rankings", "a pass score"],
    }
    markdown = render(result)
    result["markdown"] = markdown
    result["markdown_sha256"] = sha256(markdown.encode("utf-8"))
    return result


def _cell(value: object) -> str:
    if value is None:
        return "unavailable"
    if isinstance(value, float):
        return f"{value:g}"
    return str(value).replace("|", "\\|")


def render(result: dict) -> str:
    lines = ["# Prime bench comparison", ""]
    if result["synthetic"]:
        lines += ["**SYNTHETIC.** At least one run is labelled SYNTHETIC. These records demonstrate the harness and "
                  "its report format. They show no model performance.", ""]
    inv = result["investigation"]
    lines += [f"Bench version `{result['bench_version']}`. Investigation {inv['page']} pass {inv['pass']} "
              f"(`{result['investigation_sha256']}`). Runs: {len(result['rows'])}.", ""]
    lines += ["## What is counted",
              "- A run is clean only when it completed, fresh-session and workspace-confined were declared supported, "
              "the session was fresh and used by no other run here, no intervention, no evaluator leakage, and the run "
              "line matched.",
              "- Deterministic pass: the run line, the outcome label, the decisive mentions, the exact quotes, the "
              "forbidden claims and the canary, all as string checks. It is not a judgment that the review is right.",
              "- Reviewer scores are supplied records, summed per rubric item over clean reviewed runs, with the count.",
              "- Elapsed time uses coordinator-supplied start and finish. Tool events and usage are as supplied. "
              "Missing values are `unavailable`, never 0.", ""]
    lines += ["## Runs", "",
              "| run | case | family/variant | condition | model / effort | label | status | clean | outcome | "
              "deterministic | review | elapsed s | tool events | usage |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in result["rows"]:
        review = "unavailable" if r["review"] is None else ", ".join(
            f"{k}={v}" for k, v in sorted(r["review"]["scores"].items()))
        usage = "unavailable" if r["usage"] is None else ", ".join(
            f"{k}={v}" for k, v in sorted(r["usage"].items()) if k != "source")
        lines.append(
            f"| {r['run_id']} | {r['case_id']} r{r['case_revision']} | {r['family']}/{r['variant']} | {r['condition']} "
            f"| {_cell(r['model_label'])} / {_cell(r['effort_label'])} | {_cell(r['label'])} | {r['status']} "
            f"| {'yes' if r['clean'] else 'no'} | {_cell(r['outcome_found'])} "
            f"| {'pass' if r['deterministic_pass'] else 'fail'} | {review} | {_cell(r['elapsed_seconds'])} "
            f"| {_cell(r['tool_events'])} | {usage} |")
    lines += ["", "## Counts by condition", ""]
    for cond, c in result["counts"].items():
        status = ", ".join(f"{k} {v}" for k, v in c["by_status"].items())
        lines.append(f"- **{cond}**: {c['runs']} runs ({status}); clean {c['clean']}; "
                     f"clean with deterministic pass {c['clean_deterministic_pass']}.")
        for item, slot in c["rubric_items"].items():
            lines.append(f"  - {item}: {slot['reviewed_clean_runs']} clean reviewed runs, score sum {slot['score_sum']}.")
    lines += ["", "## Not clean, failed or uncollected (kept, not dropped)", ""]
    unclean = [r for r in result["rows"] if not r["clean"]]
    lines += [f"- {r['run_id']} ({r['condition']}): {'; '.join(r['not_clean_reasons'])}" for r in unclean] or ["- none"]
    lines += ["", "## Corrections and interventions (separate from the original runs)", ""]
    extra = [r for r in result["rows"] if r["corrections"] or r["interventions"]]
    lines += [f"- {r['run_id']}: corrections {r['corrections']}, interventions {r['interventions']}" for r in extra] or ["- none"]
    lines += ["", "## Not computed", "",
              "No ratio between conditions, no time or token saving, no ranking and no pass score. "
              "A small fixed bench cannot establish general productivity.", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- export

def export(args: argparse.Namespace) -> dict:
    result = compare_runs(args.run_dir)
    inv, inv_bytes = load_investigation(args.investigation)
    if sha256(inv_bytes) != result["investigation_sha256"]:
        raise Refused("mixed-investigation", "investigation file differs from the one the runs are bound to")
    dest = fresh_dest(args.dest, "export folder")
    nn = inv["pass"].split(".")[1]
    files: dict[str, bytes] = {
        "comparison.md": result["markdown"].encode("utf-8"),
        "comparison.json": dumps({k: v for k, v in result.items() if k != "markdown"}),
        "investigation.json": inv_bytes,
    }
    for raw in args.run_dir:
        run_dir = existing_dir(raw, "run folder")
        run = load_run(run_dir)
        for rel in ("run.json", "COORDINATOR.md", "collection.json", "review.json"):
            if os.path.lexists(run_dir / rel):
                files[f"runs/{run['run_id']}/{rel}"] = read_regular(run_dir / rel, rel, MAX_JSON)
        for sub in ("collected", "events"):
            folder = run_dir / sub
            if folder.is_dir():
                for name in sorted(os.listdir(folder)):
                    need_rel(name, f"{sub} file")
                    files[f"runs/{run['run_id']}/{sub}/{name}"] = read_regular(folder / name, name, MAX_TOOL_LOG)
    template = (
        f"# 05.{nn}.return.md — TEMPLATE for the bench coordinator\n\n"
        f"Investigation {inv['page']}, pass 05.{nn}. Bench version {result['bench_version']}.\n"
        "This is a TEMPLATE. The coordinator writes every section in their own words before capture.\n"
        "Nothing below is a completed return or a review.\n\n"
        "## Did\nTEMPLATE: runs prepared, collected and reviewed; exact commands; what comparison.md shows.\n\n"
        "## Blocked\nTEMPLATE: anything that stopped a run or a review.\n\n"
        "## Need\nTEMPLATE: the Director or Prime choices needed next.\n\n"
        "## Records\n"
        f"comparison.md sha256 {sha256(files['comparison.md'])}\n"
        f"comparison.json sha256 {sha256(files['comparison.json'])}\n"
        f"investigation.json sha256 {sha256(inv_bytes)}\n")
    files[f"05.{nn}.return.TEMPLATE.md"] = template.encode("utf-8")
    artifacts = ["comparison.md", "comparison.json", "investigation.json"]
    capture = (
        "Coordinator custody (N1NN). Not run by this harness.\n"
        f"1. Write {dest}\\05.{nn}.return.md from the TEMPLATE, starting Did, Blocked, Need.\n"
        "2. Prime reserves a member whose expected outputs are exactly, in this order:\n"
        + "".join(f"   {a}\n" for a in artifacts)
        + "3. Capture and freshly verify from the repository root:\n\n"
        f"python -B labs/return-capture-pass01/return_capture.py capture --book \"ABS-BOOK\" --submission SUBMISSION-ID "
        f"--return-file \"{dest}\\05.{nn}.return.md\" --source-root \"{dest}\" "
        + " ".join(f"--artifact \"{a}|{a}\"" for a in artifacts) + "\n"
        "python -B labs/return-capture-pass01/return_capture.py verify --book \"ABS-BOOK\" --member RESERVED-MEMBER\n\n"
        "4. Prime places the captured return into the N7NN page with the reviewed workflow. "
        "Run records under runs/ stay in this export folder, bound by comparison.json.\n")
    files["CAPTURE.txt"] = capture.encode("utf-8")
    writer = Writer()

    def write_all() -> None:
        writer.mkdir(dest)
        for rel, data in sorted(files.items()):
            writer.file(dest.joinpath(*rel.split("/")), data)

    guarded(writer, "export", write_all)
    return {"result": "exported", "dest": str(dest), "files": len(files),
            "comparison_sha256": sha256(files["comparison.md"])}


# ---------------------------------------------------------------- cli

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prime_bench.py", description="Bounded Prime benchmark harness.")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("validate")
    p.add_argument("--json", action="store_true")
    sub.add_parser("manifest")
    p = sub.add_parser("prepare")
    for name in ("--investigation", "--run-id", "--case", "--condition", "--model-label", "--effort-label",
                 "--fresh-session", "--workspace-confined", "--tool-log", "--usage", "--run-dir", "--candidate-dir"):
        p.add_argument(name, required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("collect")
    for name in ("--run-dir", "--expect-run", "--expect-condition", "--status", "--label", "--session-label",
                 "--isolation-used"):
        p.add_argument(name, required=True)
    for name in ("--reason", "--response", "--tool-log", "--tool-events", "--usage", "--started", "--finished",
                 "--intervention"):
        p.add_argument(name)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("event")
    for name in ("--run-dir", "--kind", "--text"):
        p.add_argument(name, required=True)
    p.add_argument("--attachment")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("assess")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("review")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--record", required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("compare")
    p.add_argument("--run-dir", action="append", required=True)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("export")
    p.add_argument("--run-dir", action="append", required=True)
    p.add_argument("--investigation", required=True)
    p.add_argument("--dest", required=True)
    p.add_argument("--json", action="store_true")
    return parser


def emit(obj: dict, as_json: bool, text: str | None = None) -> None:
    out = dumps(obj) if as_json or text is None else text.encode("utf-8")
    sys.stdout.buffer.write(out)
    sys.stdout.buffer.flush()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    as_json = getattr(args, "json", False)
    try:
        if args.command == "validate":
            result = validate()
            emit(result, as_json, f"{result['result']} {result['bench_version']}\n"
                 + "".join(f"drift {d}\n" for d in result["drift"]))
            return 0 if result["result"] == "valid" else 1
        if args.command == "manifest":
            sys.stdout.buffer.write(dumps(manifest_object()))
            return 0
        if args.command == "assess":
            result = assess_run(existing_dir(args.run_dir, "run folder"))
            emit(result, as_json, f"{result['run_id']} deterministic {'pass' if result['deterministic_pass'] else 'fail'}\n")
            return 0
        if args.command == "compare":
            result = compare_runs(args.run_dir)
            emit(result, as_json, result["markdown"])
            return 0
        handler = {"prepare": prepare, "collect": collect, "event": event, "review": review, "export": export}
        result = handler[args.command](args)
        emit(result, as_json, " ".join(f"{k}={v}" for k, v in result.items()) + "\n")
        return 0
    except Refused as exc:
        emit({"result": "refused", "code": exc.code, "detail": exc.detail}, as_json,
             f"refused {exc.code}: {exc.detail}\n")
        return 2
    except Partial as exc:
        emit({"result": "partial", "detail": exc.detail, "retained": exc.written}, as_json,
             f"partial: {exc.detail}\n" + "".join(f"retained {w}\n" for w in exc.written))
        return 1


if __name__ == "__main__":
    sys.exit(main())
