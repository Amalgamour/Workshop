#!/usr/bin/env python3
"""Bounded Prime benchmark harness, rules 2: sealed trials, input checks, commitments, costs.

Standard library only. No model call, no session launch, no network, no Git.
A coordinator seals a whole trial before any answer, starts fresh sessions by hand,
and collects what they said. Deterministic checks are string checks. Rubric scores and
action dispositions are supplied judgment; code checks only their shape and bindings.

  python -B prime_bench.py validate [--json]
  python -B prime_bench.py manifest
  python -B prime_bench.py seal         --plan ABS --investigation ABS --dest ABS
  python -B prime_bench.py check-inputs --run-dir ABS
  python -B prime_bench.py collect      --run-dir ABS --expect-run ID --expect-condition C --status S ...
  python -B prime_bench.py event        --run-dir ABS --kind K --text TEXT [--attachment ABS]
  python -B prime_bench.py assess       --run-dir ABS
  python -B prime_bench.py review       --run-dir ABS --record ABS
  python -B prime_bench.py actions      --run-dir ABS --record ABS
  python -B prime_bench.py rerun        --trial ABS --supersedes ID --run-id ID --reason TEXT
  python -B prime_bench.py compare      --trial ABS
  python -B prime_bench.py export       --trial ABS --dest ABS

Contract: 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.02/CONTRACT.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

LAB = Path(os.path.abspath(__file__)).parent
REPO = LAB.parents[1]

SCHEMA_BENCH = "prime-bench/1"
SCHEMA_CONDITIONS = "prime-bench-conditions/1"
SCHEMA_KEY = "prime-bench-key/1"
SCHEMA_RUBRIC = "prime-bench-rubric/1"
SCHEMA_COMMITMENTS = "prime-bench-commitments/1"
SCHEMA_MEASURES = "prime-bench-measures/1"
SCHEMA_META = "prime-bench-case-meta/1"
SCHEMA_INVESTIGATION = "prime-bench-investigation/1"
SCHEMA_PLAN = "prime-bench-plan/1"
SCHEMA_SEAL = "prime-bench-seal/1"
SCHEMA_AMENDMENT = "prime-bench-amendment/1"
SCHEMA_RUN = "prime-bench-run/2"
SCHEMA_RUN_LEGACY = "prime-bench-run/1"
SCHEMA_COLLECTION = "prime-bench-collection/2"
SCHEMA_INPUT_CHECK = "prime-bench-input-check/1"
SCHEMA_EVENT = "prime-bench-event/1"
SCHEMA_TOOL_EVENT = "prime-bench-tool-event/1"
SCHEMA_ASSESSMENT = "prime-bench-assessment/1"
SCHEMA_REVIEW = "prime-bench-review/1"
SCHEMA_ACTIONS = "prime-bench-action-assessment/1"
SCHEMA_COSTS = "prime-bench-costs/1"
SCHEMA_COMPARISON = "prime-bench-comparison/2"
RULES = "prime-bench-rules/2"
BENCH_REVISION = 2

FAMILIES = ("correction", "false-completion", "design-fork", "complete")
VARIANTS = ("a", "b")
CONDITIONS = ("baseline", "assisted")
OUTCOMES = ("continue", "director-input", "develop", "complete")
CAPABILITY = ("supported", "unsupported", "unknown")
CAPABILITY_KEYS = ("fresh_session", "workspace_confined", "tool_log", "usage")
STATUSES = ("completed", "failed", "abandoned")
ISOLATION_USED = ("fresh", "shared", "unknown")
EVENT_KINDS = ("correction", "intervention", "note")
COMMITMENT_KINDS = ("required-action", "hold", "prohibited", "no-further-edit")
DISPOSITIONS = ("present", "contradicted", "absent")
AMORTIZATION = ("not-amortized", "equal-split-over-planned-runs")
CACHE_STATES = ("cold", "warm", "unknown")
USAGE_KEYS = ("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens", "total_tokens")
COST_COUNTS = ("launch_order", "tool_operations", "failed_tool_calls", "request_repairs", "repair_minutes",
               "correction_loops", "correction_minutes", "director_attention_events", "director_attention_minutes")
COST_KEYS = ("schema", "run_id", "observer", *COST_COUNTS, "cache_state", "prior_involvement")
WORK_DIR = "work"
PROMPT_DIFFERENCE = "PROMPT.md#tools-paragraph-and-run-id"

MAX_JSON = 262144
MAX_RESPONSE = 1048576
MAX_TOOL_LOG = 8388608
MAX_TEXT = 4000
MAX_EVENTS = 9999
MAX_RUNS = 200

_RUN_ID = re.compile(r"r[0-9]{4}")
_TRIAL_ID = re.compile(r"t[0-9]{4}")
_PAIR_ID = re.compile(r"p[0-9]{2,4}")
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
ASSISTED_COPIES = tuple(item["copy_to"] for item in SUPPORT if item["role"] == "assisted")
ALLOWED_DIFFERENCES = (PROMPT_DIFFERENCE, *ASSISTED_COPIES)

PROMPT = """# Prime review run {run_id}

Work only inside this folder. Read TASK.md, then everything in sources/.
This must be a fresh session with no earlier context. Do not open any other folder or repository.
No one will help or answer questions during this run.
Do not change, add or delete anything outside work/. Put any notes you want to keep in work/.
If you run Python, use `python -B`.

## Tools
{tools}

## Response
Your final message is saved exactly as your answer. It must start with this line:

Run: {run_id}

The next line is `Outcome: <continue|director-input|develop|complete>`.
Then give your findings, the reasons and evidence for each, and one proposed next action.
"""

COORDINATOR = """# Coordinator steps for run {run_id}

Trial {trial_id}, pair {pair_id}, planned order {order}{late}.
Case {case_id} revision {revision}, condition {condition}. Model label {model}, effort label {effort}.
Candidate folder: {candidate}
Declared: fresh-session {fresh_session}, workspace-confined {workspace_confined}, tool-log {tool_log}, usage {usage}.

1. Before the first launch of the trial, send the seal digest to Prime. Never edit the trial after that.
2. Check the inputs: python -B {module} check-inputs --run-dir "{run_dir}"
   It must say intact. If it says drift, do not repair it: record the run as failed and use rerun.
3. Start one new session with no earlier context, confined to the candidate folder only. It must not
   be able to read this run folder, other candidates, the bench lab or the repository.
4. Paste PROMPT.md from the candidate folder as the first message (session start). Record the time.
5. Do not help, hint, repair or answer questions. Any help is an intervention and must be recorded.
6. Save the final message exactly (session stop). Record the time. Export the tool log and usage if
   the surface offers them. Fill a prime-bench-costs/1 record; unknown fields stay null.
7. Never reuse this session for another run, case or condition.
8. Collect:

python -B {module} collect --run-dir "{run_dir}" --expect-run {run_id} --expect-condition {condition} --status completed --label ACTUAL --session-label LABEL --isolation-used fresh|shared|unknown --response ABS [--tool-log ABS] [--tool-events ABS] [--usage ABS] [--costs ABS] --started ISO --finished ISO [--intervention TEXT]

A failed or abandoned run is collected with --status failed|abandoned --reason TEXT. It stays in the trial.
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
            out.append((Path(folder) / name).relative_to(base).as_posix())
    return sorted(out)


def _file_row(path: Path, rel: str) -> dict:
    data = read_regular(path, rel, MAX_JSON)
    return {"path": rel, "sha256": sha256(data), "bytes": len(data)}


def manifest_object() -> dict:
    """The bench.json object the files on disk describe now."""
    cases = []
    for case_id in _case_dirs():
        if not _CASE_ID.fullmatch(case_id):
            raise Refused("bench-drift", f"case folder name is unusable: {case_id}")
        files = []
        for rel in _case_files(case_id):
            need_rel(rel, f"case file {case_id}/{rel}")
            files.append(_file_row(LAB / "cases" / case_id / rel, rel))
        meta = strict_json(read_regular(LAB / "cases" / case_id / "coordinator" / "meta.json", "meta", MAX_JSON), "meta")
        revision = meta.get("revision") if isinstance(meta, dict) else None
        cases.append({"case_id": case_id, "revision": revision, "files": files})
    return {
        "schema": SCHEMA_BENCH,
        "bench_id": "prime-bench-pass01",
        "revision": BENCH_REVISION,
        "rules": RULES,
        "conditions": _file_row(LAB / "conditions.json", "conditions.json"),
        "measures": _file_row(LAB / "measures.json", "measures.json"),
        "support": [{k: item[k] for k in ("role", "path", "copy_to", "sha256", "bytes")} for item in SUPPORT],
        "cases": cases,
    }


REQUIRED_CASE_FILES = ("candidate/TASK.md", "evaluator/key.json", "evaluator/rubric.json",
                       "evaluator/commitments.json", "coordinator/meta.json")


def _check_case_records(case_id: str, revision: object, files: set[str]) -> list[str]:
    problems = []
    for rel in REQUIRED_CASE_FILES:
        if rel not in files:
            problems.append(f"{case_id}: {rel} is missing")
    if not any(rel.startswith("candidate/sources/") for rel in files):
        problems.append(f"{case_id}: no candidate sources")
    for rel in files:
        if rel.split("/")[0] not in ("candidate", "evaluator", "coordinator"):
            problems.append(f"{case_id}: {rel} is outside the three case trees")
    if problems:
        return problems
    if revision != BENCH_REVISION:
        return [f"{case_id}: revision {revision} is not bench revision {BENCH_REVISION}"]
    base = LAB / "cases" / case_id
    key = load_key(base, case_id, revision)
    load_rubric(base, case_id, revision)
    commitments = load_commitments(base, case_id, revision)
    meta = exact_keys(strict_json(read_regular(base / "coordinator/meta.json", "meta", MAX_JSON), "meta"),
                      ("schema", "case_id", "revision", "family", "variant", "matched_with", "label",
                       "decisive_evidence", "ambiguity", "provenance"), f"{case_id} meta")
    if meta["schema"] != SCHEMA_META or meta["case_id"] != case_id or meta["revision"] != revision:
        problems.append(f"{case_id}: meta identity differs")
    if meta["family"] not in FAMILIES or meta["variant"] not in VARIANTS:
        problems.append(f"{case_id}: family or variant is unknown")
    if meta["label"] != "SYNTHETIC":
        problems.append(f"{case_id}: meta label is not SYNTHETIC")
    if meta["family"] == "complete" and not any(i["kind"] == "no-further-edit" for i in commitments["items"]):
        problems.append(f"{case_id}: a complete case needs a no-further-edit commitment")
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


def load_commitments(base: Path, case_id: str, revision: object) -> dict:
    com = exact_keys(strict_json(read_regular(base / "evaluator/commitments.json", "commitments", MAX_JSON),
                                 "commitments"), ("schema", "case_id", "revision", "items"), f"{case_id} commitments")
    if com["schema"] != SCHEMA_COMMITMENTS or com["case_id"] != case_id or com["revision"] != revision:
        raise Refused("malformed", f"{case_id} commitments identity differs")
    if not isinstance(com["items"], list) or not com["items"]:
        raise Refused("malformed", f"{case_id} commitments are empty")
    ids = []
    for item in com["items"]:
        exact_keys(item, ("id", "kind", "text"), f"{case_id} commitment")
        need_label(item["id"], "commitment id")
        need_choice(item["kind"], COMMITMENT_KINDS, "commitment kind")
        need_text(item["text"], "commitment text")
        ids.append(item["id"])
    if len(set(ids)) != len(ids):
        raise Refused("malformed", f"{case_id} commitment ids repeat")
    return com


def load_measures() -> dict:
    measures = exact_keys(strict_json(read_regular(LAB / "measures.json", "measures.json", MAX_JSON), "measures"),
                          ("schema", "operation_unit", "session_start", "session_stop", "preparation_timing",
                           "fields", "amortization", "unknown"), "measures")
    if measures["schema"] != SCHEMA_MEASURES:
        raise Refused("malformed", "measures schema differs")
    names = [f.get("field") for f in measures["fields"] if isinstance(f, dict)]
    if names != [*COST_COUNTS, "cache_state", "prior_involvement"]:
        raise Refused("malformed", "measures fields differ from the costs record")
    return measures


def validate() -> dict:
    """Re-hash the bench against bench.json and the support pins."""
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
        wanted = list(ASSISTED_COPIES) if name == "assisted" else []
        if entry["support"] != wanted:
            drift.append(f"condition {name} support differs from the pinned copy list")
    load_measures()
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
        if meta["matched_with"] != families.get((family, "b" if variant == "a" else "a")):
            drift.append(f"{case_id}: matched_with is not its other variant")
    drift.extend(candidate_leaks(current, canaries))
    return {
        "schema": "prime-bench-validation/1",
        "result": "valid" if not drift else "drift",
        "bench_version": sha256(raw),
        "rules": RULES,
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


def _secret_material(manifest: dict, canaries: dict[str, str]) -> list[tuple[str, bytes]]:
    secret = [(f"canary of {cid}", c.encode("utf-8")) for cid, c in canaries.items()]
    for other in manifest["cases"]:
        for f in other["files"]:
            if not f["path"].startswith("candidate/"):
                secret.append((f"{other['case_id']}/{f['path']}",
                               read_regular(LAB / "cases" / other["case_id"] / f["path"], f["path"], MAX_JSON)))
    return secret


# ---------------------------------------------------------------- investigation and plan

def load_investigation(raw: str) -> tuple[dict, bytes]:
    path = need_abs(raw, "investigation")
    data = read_regular(path, "investigation", MAX_JSON)
    return parse_investigation(data), data


def parse_investigation(data: bytes) -> dict:
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
    return inv


def parse_plan(data: bytes, inv_sha: str, case_ids: list[str]) -> dict:
    plan = exact_keys(strict_json(data, "plan"),
                      ("schema", "trial_id", "investigation_sha256", "capabilities", "allowed_differences",
                       "preparation", "runs"), "plan")
    if plan["schema"] != SCHEMA_PLAN:
        raise Refused("malformed", "plan schema differs")
    if not isinstance(plan["trial_id"], str) or not _TRIAL_ID.fullmatch(plan["trial_id"]):
        raise Refused("malformed", "trial id is not t followed by four digits")
    if need_hex(plan["investigation_sha256"], "plan investigation sha256") != inv_sha:
        raise Refused("mixed-investigation", "plan names a different investigation file")
    caps = exact_keys(plan["capabilities"], CAPABILITY_KEYS, "plan capabilities")
    for key in CAPABILITY_KEYS:
        need_choice(caps[key], CAPABILITY, f"capability {key}")
    if plan["allowed_differences"] != list(ALLOWED_DIFFERENCES):
        raise Refused("malformed", f"allowed_differences must be exactly {list(ALLOWED_DIFFERENCES)}")
    prep = exact_keys(plan["preparation"], ("owner", "reusable_setup_minutes", "per_run_setup_minutes", "amortization"),
                      "plan preparation")
    need_label(prep["owner"], "preparation owner")
    need_count(prep["reusable_setup_minutes"], "reusable_setup_minutes")
    need_count(prep["per_run_setup_minutes"], "per_run_setup_minutes")
    need_choice(prep["amortization"], AMORTIZATION, "amortization")
    runs = plan["runs"]
    if not isinstance(runs, list) or not runs or len(runs) > MAX_RUNS:
        raise Refused("malformed", f"plan runs is not a list of 1 to {MAX_RUNS}")
    pairs: dict[str, list[dict]] = {}
    for run in runs:
        exact_keys(run, ("run_id", "pair_id", "case_id", "condition", "order", "model_label", "effort_label"), "plan run")
        if not isinstance(run["run_id"], str) or not _RUN_ID.fullmatch(run["run_id"]):
            raise Refused("malformed", "plan run id is not r followed by four digits")
        if not isinstance(run["pair_id"], str) or not _PAIR_ID.fullmatch(run["pair_id"]):
            raise Refused("malformed", "plan pair id is not p followed by two to four digits")
        if run["case_id"] not in case_ids:
            raise Refused("malformed", f"plan case is not in the bench: {run['case_id']}")
        need_choice(run["condition"], CONDITIONS, "plan condition")
        need_count(run["order"], "plan order", nullable=False)
        need_label(run["model_label"], "model label")
        need_label(run["effort_label"], "effort label")
        pairs.setdefault(run["pair_id"], []).append(run)
    ids = [r["run_id"] for r in runs]
    if len(set(ids)) != len(ids):
        raise Refused("duplicate", "plan run ids repeat")
    if sorted(r["order"] for r in runs) != list(range(1, len(runs) + 1)):
        raise Refused("malformed", "plan orders must be exactly 1..N")
    for pair_id, members in pairs.items():
        if len(members) != 2 or {m["condition"] for m in members} != set(CONDITIONS):
            raise Refused("incomplete-pair", f"pair {pair_id} needs exactly one baseline and one assisted run")
        if len({m["case_id"] for m in members}) != 1:
            raise Refused("incomplete-pair", f"pair {pair_id} mixes cases")
        if len({(m["model_label"], m["effort_label"]) for m in members}) != 1:
            raise Refused("incomplete-pair", f"pair {pair_id} mixes model or effort labels")
    return plan


# ---------------------------------------------------------------- kits and parity

def kit_files(base: Path, case: dict, condition: str, run_id: str, tools: str) -> dict[str, bytes]:
    """Every file delivered to one candidate, by relative path."""
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
    files["PROMPT.md"] = PROMPT.format(run_id=run_id, tools=tools).encode("utf-8")
    return files


def pair_parity(kits: dict[str, dict[str, bytes]], runs: dict[str, dict], tools: dict[str, str]) -> dict:
    """Byte parity inside one pair, except the declared allowed differences."""
    by_cond = {runs[rid]["condition"]: rid for rid in kits}
    base_id, asst_id = by_cond["baseline"], by_cond["assisted"]
    base, asst = kits[base_id], kits[asst_id]
    problems = []
    extra = sorted(set(asst) - set(base))
    if extra != sorted(ASSISTED_COPIES):
        problems.append(f"assisted-only files are {extra}, not the allowed support files")
    missing_in_assisted = sorted(set(base) - set(asst))
    if missing_in_assisted:
        problems.append(f"missing from assisted: {missing_in_assisted}")
    compared = 0
    for rel in sorted(set(base) & set(asst)):
        if rel == "PROMPT.md":
            continue
        compared += 1
        if base[rel] != asst[rel]:
            problems.append(f"decisive bytes differ: {rel}")
    for rid in (base_id, asst_id):
        want = PROMPT.format(run_id=rid, tools=tools[runs[rid]["condition"]]).encode("utf-8")
        if kits[rid].get("PROMPT.md") != want:
            problems.append(f"{rid} PROMPT.md is not the fixed template for its condition")
    decisive = sorted(rel for rel in base if rel == "TASK.md" or rel.startswith("sources/"))
    reach = all(rel in base for rel in decisive) and bool(decisive)
    return {"baseline": base_id, "assisted": asst_id, "compared_files": compared, "decisive_files": decisive,
            "baseline_reach": "all decisive files delivered to baseline" if reach else "incomplete",
            "parity": "identical-except-allowed" if not problems else "fail", "problems": problems}


def delivery_rows(files: dict[str, bytes]) -> list[dict]:
    return [{"path": p, "sha256": sha256(d), "bytes": len(d)} for p, d in sorted(files.items())]


def check_inputs(run: dict) -> dict:
    """Recheck the candidate folder against its sealed delivery manifest. Ignores work/."""
    cand = Path(run["candidate_dir"])
    out = {"schema": SCHEMA_INPUT_CHECK, "run_id": run["run_id"], "candidate_dir": str(cand), "kind": "mechanical"}
    if not cand.is_dir() or is_linked(cand):
        out.update({"result": "drift", "problems": ["unavailable: candidate folder is missing or linked"]})
        return out
    delivered = {row["path"]: row for row in run["delivery"]}
    problems = []
    seen = set()
    work = cand / WORK_DIR
    if is_linked(work):
        problems.append("linked: work/")
    for folder, dirs, files in os.walk(cand):
        here = Path(folder)
        rel_dir = here.relative_to(cand).as_posix()
        if rel_dir == WORK_DIR or rel_dir.startswith(WORK_DIR + "/"):
            dirs[:] = []
            continue
        for name in sorted(dirs):
            path = here / name
            rel = (path.relative_to(cand)).as_posix()
            if is_linked(path):
                problems.append(f"linked: {rel}/")
        dirs[:] = [d for d in sorted(dirs) if not is_linked(here / d)]
        for name in sorted(files):
            path = here / name
            rel = path.relative_to(cand).as_posix()
            if rel not in delivered:
                problems.append(f"extra: {rel}")
                continue
            seen.add(rel)
            st = os.lstat(path)
            if is_linked(path) or not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
                problems.append(f"linked: {rel}")
                continue
            with open(path, "rb") as handle:
                data = handle.read(MAX_TOOL_LOG + 1)
            if sha256(data) != delivered[rel]["sha256"] or len(data) != delivered[rel]["bytes"]:
                problems.append(f"changed: {rel}")
    for rel in sorted(set(delivered) - seen):
        if not any(p.endswith(f": {rel}") for p in problems):
            problems.append(f"missing: {rel}")
    out.update({"result": "intact" if not problems else "drift", "problems": sorted(problems)})
    return out


# ---------------------------------------------------------------- seal

def _run_record(trial_id: str, plan_run: dict, version: str, inv: dict, inv_sha: str, case: dict, cand: Path,
                caps: dict, files: dict[str, bytes], late: bool, supersedes: str | None) -> dict:
    base = LAB / "cases" / case["case_id"]
    return {
        "schema": SCHEMA_RUN,
        "trial_id": trial_id,
        "run_id": plan_run["run_id"],
        "pair_id": plan_run["pair_id"],
        "order": plan_run["order"],
        "late": late,
        "supersedes": supersedes,
        "bench_version": version,
        "investigation_sha256": inv_sha,
        "investigation": {"page": inv["page"], "pass": inv["pass"]},
        "case_id": case["case_id"],
        "case_revision": case["revision"],
        "condition": plan_run["condition"],
        "model_label": plan_run["model_label"],
        "effort_label": plan_run["effort_label"],
        "capabilities": caps,
        "candidate_dir": str(cand),
        "pins": {
            "task_sha256": sha256(files["TASK.md"]),
            "key_sha256": sha256(read_regular(base / "evaluator/key.json", "key", MAX_JSON)),
            "rubric_sha256": sha256(read_regular(base / "evaluator/rubric.json", "rubric", MAX_JSON)),
            "commitments_sha256": sha256(read_regular(base / "evaluator/commitments.json", "commitments", MAX_JSON)),
            "measures_sha256": sha256(read_regular(LAB / "measures.json", "measures", MAX_JSON)),
        },
        "delivery": delivery_rows(files),
        "working_dir": WORK_DIR,
        "prepared_at": utc_now(),
    }


def _coordinator_text(run: dict, run_dir: Path) -> bytes:
    return COORDINATOR.format(
        run_id=run["run_id"], trial_id=run["trial_id"], pair_id=run["pair_id"], order=run["order"],
        late=f" (LATE, supersedes {run['supersedes']}; not part of the pre-answer seal)" if run["late"] else "",
        case_id=run["case_id"], revision=run["case_revision"], condition=run["condition"], model=run["model_label"],
        effort=run["effort_label"], candidate=run["candidate_dir"], module=Path(os.path.abspath(__file__)),
        run_dir=run_dir, **run["capabilities"]).encode("utf-8")


def _write_kit(writer: Writer, cand: Path, files: dict[str, bytes]) -> None:
    writer.mkdir(cand)
    for rel, data in sorted(files.items()):
        writer.file(cand.joinpath(*rel.split("/")), data)
    writer.mkdir(cand / WORK_DIR)
    for rel, data in files.items():
        if read_regular(cand.joinpath(*rel.split("/")), rel, 1 << 22) != data:
            raise OSError(f"candidate file differs after write: {rel}")


def seal(args: argparse.Namespace) -> dict:
    started = time.monotonic()
    seal_started_at = utc_now()
    inv, inv_bytes = load_investigation(args.investigation)
    inv_sha = sha256(inv_bytes)
    plan_bytes = read_regular(need_abs(args.plan, "plan"), "plan", MAX_JSON)
    manifest, version, canaries = bench_state()
    cases = {c["case_id"]: c for c in manifest["cases"]}
    plan = parse_plan(plan_bytes, inv_sha, sorted(cases))
    dest = fresh_dest(args.dest, "trial folder")
    if inside(dest, LAB):
        raise Refused("unsafe-path", "a trial folder cannot sit inside the bench lab")
    cond = strict_json(read_regular(LAB / "conditions.json", "conditions.json", MAX_JSON), "conditions")
    tools = {name: cond[name]["tools"] for name in CONDITIONS}
    secret = _secret_material(manifest, canaries)
    runs = {r["run_id"]: r for r in plan["runs"]}
    kits: dict[str, dict[str, bytes]] = {}
    for rid, run in runs.items():
        kits[rid] = kit_files(LAB / "cases" / run["case_id"], cases[run["case_id"]], run["condition"], rid,
                              tools[run["condition"]])
        leaks = leak_hits(sorted(kits[rid].items()), secret)
        if leaks:
            raise Refused("evaluator-leakage", f"{rid}: " + "; ".join(leaks))
    pairs = {}
    for rid, run in runs.items():
        pairs.setdefault(run["pair_id"], {})[rid] = kits[rid]
    parity = {}
    for pair_id, members in sorted(pairs.items()):
        result = pair_parity(members, runs, tools)
        if result["parity"] != "identical-except-allowed" or result["baseline_reach"] != "all decisive files delivered to baseline":
            raise Refused("parity-fail", f"pair {pair_id}: " + "; ".join(result["problems"] or [result["baseline_reach"]]))
        parity[pair_id] = result
    records = {}
    for rid, run in runs.items():
        cand = dest / "candidates" / rid
        records[rid] = _run_record(plan["trial_id"], run, version, inv, inv_sha, cases[run["case_id"]], cand,
                                   plan["capabilities"], kits[rid], False, None)
    assessment = {}
    for case_id in sorted({r["case_id"] for r in runs.values()}):
        base = LAB / "cases" / case_id
        assessment[case_id] = {
            "revision": cases[case_id]["revision"],
            "key_sha256": sha256(read_regular(base / "evaluator/key.json", "key", MAX_JSON)),
            "rubric_sha256": sha256(read_regular(base / "evaluator/rubric.json", "rubric", MAX_JSON)),
            "commitments_sha256": sha256(read_regular(base / "evaluator/commitments.json", "commitments", MAX_JSON)),
        }
    run_bytes = {rid: dumps(rec) for rid, rec in records.items()}
    writer = Writer()
    sealed: dict = {}

    def write_all() -> None:
        writer.mkdir(dest)
        writer.file(dest / "plan.json", plan_bytes)
        writer.file(dest / "investigation.json", inv_bytes)
        writer.mkdir(dest / "candidates")
        writer.mkdir(dest / "runs")
        for rid in sorted(runs):
            _write_kit(writer, dest / "candidates" / rid, kits[rid])
            run_dir = dest / "runs" / rid
            writer.mkdir(run_dir)
            writer.file(run_dir / "COORDINATOR.md", _coordinator_text(records[rid], run_dir))
            writer.file(run_dir / "run.json", run_bytes[rid])
        sealed.update({
            "schema": SCHEMA_SEAL,
            "trial_id": plan["trial_id"],
            "plan_sha256": sha256(plan_bytes),
            "investigation_sha256": inv_sha,
            "bench_version": version,
            "rules": RULES,
            "harness": {"prime_bench.py": sha256(read_regular(Path(os.path.abspath(__file__)), "harness", 1 << 22)),
                        "conditions.json": sha256(read_regular(LAB / "conditions.json", "conditions", MAX_JSON)),
                        "measures.json": sha256(read_regular(LAB / "measures.json", "measures", MAX_JSON))},
            "support": [{"path": s["path"], "sha256": s["sha256"]} for s in SUPPORT],
            "allowed_differences": list(ALLOWED_DIFFERENCES),
            "assessment": assessment,
            "runs": [{"run_id": rid, "pair_id": runs[rid]["pair_id"], "order": runs[rid]["order"],
                      "case_id": runs[rid]["case_id"], "condition": runs[rid]["condition"],
                      "run_json_sha256": sha256(run_bytes[rid]),
                      "delivery_sha256": sha256(dumps(records[rid]["delivery"]))}
                     for rid in sorted(runs, key=lambda r: runs[r]["order"])],
            "pairs": parity,
            "preparation": plan["preparation"],
            "capabilities": plan["capabilities"],
            "seal_started_at": seal_started_at,
            "sealed_at": utc_now(),
            "preparation_machine_seconds": round(time.monotonic() - started, 3),
        })
        writer.file(dest / "seal.json", dumps(sealed))

    guarded(writer, "seal", write_all)
    return {"result": "sealed", "trial_id": plan["trial_id"], "dest": str(dest), "runs": len(runs),
            "pairs": len(pairs), "seal_sha256": sha256(dumps(sealed)), "bench_version": version}


# ---------------------------------------------------------------- run loading

def load_run(run_dir: Path) -> dict:
    path = run_dir / "run.json"
    if not os.path.lexists(path):
        raise Refused("partial-present", f"run folder has no run.json (unprepared or partial): {run_dir}")
    obj = strict_json(read_regular(path, "run.json", MAX_JSON), "run.json")
    if isinstance(obj, dict) and obj.get("schema") == SCHEMA_RUN_LEGACY:
        raise Refused("legacy-run", "run was prepared under rules 1 without a trial seal; it cannot satisfy rules 2")
    run = exact_keys(obj, ("schema", "trial_id", "run_id", "pair_id", "order", "late", "supersedes", "bench_version",
                           "investigation_sha256", "investigation", "case_id", "case_revision", "condition",
                           "model_label", "effort_label", "capabilities", "candidate_dir", "pins", "delivery",
                           "working_dir", "prepared_at"), "run.json")
    if run["schema"] != SCHEMA_RUN or not isinstance(run["run_id"], str) or not _RUN_ID.fullmatch(run["run_id"]):
        raise Refused("malformed", "run.json identity is unusable")
    need_choice(run["condition"], CONDITIONS, "run condition")
    need_hex(run["bench_version"], "run bench version")
    need_hex(run["investigation_sha256"], "run investigation sha256")
    exact_keys(run["capabilities"], CAPABILITY_KEYS, "run capabilities")
    exact_keys(run["pins"], ("task_sha256", "key_sha256", "rubric_sha256", "commitments_sha256", "measures_sha256"),
               "run pins")
    for row in run["delivery"]:
        exact_keys(row, ("path", "sha256", "bytes"), "delivery row")
        need_rel(row["path"], "delivery path")
    return run


def trial_of(run_dir: Path) -> Path:
    return run_dir.parent.parent


def seal_check(run_dir: Path, run: dict) -> dict:
    """Is this run.json the one the trial sealed (or a recorded late amendment)?"""
    trial = trial_of(run_dir)
    run_sha = sha256(read_regular(run_dir / "run.json", "run.json", MAX_JSON))
    seal_path = trial / "seal.json"
    if not os.path.lexists(seal_path):
        return {"result": "unsealed", "kind": "mechanical", "detail": "trial has no seal.json"}
    sealed = strict_json(read_regular(seal_path, "seal.json", MAX_JSON), "seal.json")
    for row in sealed.get("runs", []):
        if row.get("run_id") == run["run_id"]:
            ok = row.get("run_json_sha256") == run_sha
            return {"result": "sealed" if ok else "mismatch", "kind": "mechanical",
                    "detail": "run.json equals the sealed bytes" if ok else "run.json differs from the sealed bytes"}
    for amendment in load_amendments(trial):
        if amendment.get("run_id") == run["run_id"]:
            ok = amendment.get("run_json_sha256") == run_sha
            return {"result": "late" if ok else "mismatch", "kind": "mechanical",
                    "detail": "prepared after the seal by amendment" if ok else "run.json differs from its amendment"}
    return {"result": "mismatch", "kind": "mechanical", "detail": "run is neither sealed nor amended in this trial"}


def load_amendments(trial: Path) -> list[dict]:
    folder = trial / "amendments"
    if not folder.is_dir():
        return []
    out = []
    for name in sorted(os.listdir(folder)):
        if re.fullmatch(r"[0-9]{4}\.json", name):
            out.append(strict_json(read_regular(folder / name, name, MAX_JSON), name))
    return out


# ---------------------------------------------------------------- collect

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


def as_time(raw: str) -> datetime:
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


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


def parse_costs(data: bytes, run_id: str) -> dict:
    costs = exact_keys(strict_json(data, "costs"), COST_KEYS, "costs")
    if costs["schema"] != SCHEMA_COSTS:
        raise Refused("malformed", "costs schema differs")
    if costs["run_id"] != run_id:
        raise Refused("wrong-identity", f"costs name run {costs['run_id']}, not {run_id}")
    need_label(costs["observer"], "costs observer")
    for key in COST_COUNTS:
        need_count(costs[key], f"costs {key}")
    need_choice(costs["cache_state"], CACHE_STATES, "cache_state")
    if costs["prior_involvement"] is not None:
        need_text(costs["prior_involvement"], "prior_involvement")
    return costs


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
    if started and finished and as_time(finished) < as_time(started):
        raise Refused("malformed", "finished is before started")

    inputs: dict[str, tuple[str, bytes] | None] = {}
    for name, raw, limit, out in (("response", args.response, MAX_RESPONSE, "response.txt"),
                                  ("tool_log", args.tool_log, MAX_TOOL_LOG, "tool-log.raw"),
                                  ("tool_events", args.tool_events, MAX_TOOL_LOG, "tool-events.jsonl"),
                                  ("usage", args.usage, MAX_JSON, "usage.json"),
                                  ("costs", args.costs, MAX_JSON, "costs.json")):
        if raw is None:
            inputs[name] = None
            continue
        path = need_abs(raw, name)
        if inside(path, run_dir):
            raise Refused("unsafe-path", f"{name} is inside the run folder")
        if inside(path, Path(run["candidate_dir"])):
            raise Refused("unsafe-path", f"{name} is inside the candidate folder")
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
    costs = parse_costs(inputs["costs"][1], run["run_id"]) if inputs["costs"] else None
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
        "times_source": "declared by the coordinator",
        "intervention": intervention,
        "identity": identity,
        "leakage": leakage,
        "input_check": check_inputs(run),
        "seal_check": seal_check(run_dir, run),
        "files": {name: (None if item is None else {"path": f"collected/{item[0]}", "sha256": sha256(item[1]),
                                                    "bytes": len(item[1])}) for name, item in inputs.items()},
        "tool_event_count": tool_event_count,
        "usage": usage,
        "costs": costs,
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
            "leakage": leakage, "input_check": record["input_check"]["result"],
            "seal_check": record["seal_check"]["result"], "collection_sha256": sha256(record_bytes)}


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


def collected_response(run_dir: Path, col: dict | None) -> str | None:
    if col is None or col["files"]["response"] is None:
        return None
    rel = col["files"]["response"]["path"]
    return read_regular(run_dir.joinpath(*rel.split("/")), rel, MAX_RESPONSE).decode("utf-8", errors="replace")


# ---------------------------------------------------------------- events

def load_events(run_dir: Path) -> list[dict]:
    folder = run_dir / "events"
    if not os.path.lexists(folder):
        return []
    out = []
    for name in sorted(os.listdir(folder)):
        if re.fullmatch(r"[0-9]{4}\.json", name):
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

def pinned_case(run: dict) -> tuple[dict, dict, dict]:
    base = LAB / "cases" / run["case_id"]
    if not _CASE_ID.fullmatch(run["case_id"]) or not base.is_dir():
        raise Refused("key-changed", f"case {run['case_id']} is not in the bench")
    pins = run["pins"]
    for rel, pin, code in (("evaluator/key.json", pins["key_sha256"], "key-changed"),
                           ("evaluator/rubric.json", pins["rubric_sha256"], "rubric-changed"),
                           ("evaluator/commitments.json", pins["commitments_sha256"], "commitments-changed"),
                           ("candidate/TASK.md", pins["task_sha256"], "key-changed")):
        if not os.path.lexists(base / rel) or sha256(read_regular(base / rel, rel, MAX_JSON)) != pin:
            raise Refused(code, f"{run['case_id']} {rel} differs from the pin taken at seal; "
                                "no post-answer grading change")
    if sha256(read_regular(LAB / "measures.json", "measures", MAX_JSON)) != pins["measures_sha256"]:
        raise Refused("measures-changed", "measures.json differs from the pin taken at seal")
    return (load_key(base, run["case_id"], run["case_revision"]),
            load_rubric(base, run["case_id"], run["case_revision"]),
            load_commitments(base, run["case_id"], run["case_revision"]))


def assess_run(run_dir: Path) -> dict:
    run = load_run(run_dir)
    key, _rubric, _com = pinned_case(run)
    loaded = load_collection(run_dir)
    out = {"schema": SCHEMA_ASSESSMENT, "run_id": run["run_id"], "case_id": run["case_id"],
           "case_revision": run["case_revision"], "condition": run["condition"],
           "kind": "deterministic string checks; not a semantic or action verdict"}
    response = collected_response(run_dir, loaded[0] if loaded else None)
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
    out.update({"response": "present", "checks": checks, "deterministic_pass": passed,
                "quotes_preserved": all(c["pass"] for c in checks["must_quote"]) if checks["must_quote"] else None})
    return out


# ---------------------------------------------------------------- supplied records

def _store_once(run_dir: Path, name: str, data: bytes, same_code: str) -> None:
    target = run_dir / name
    if os.path.lexists(target):
        same = read_regular(target, name, MAX_JSON) == data
        raise Refused(same_code if same else "conflict",
                      f"run already has this {name}; nothing was written" if same
                      else f"run already has a different {name}; nothing was written")
    writer = Writer()
    guarded(writer, name, lambda: writer.file(target, data))


def review(args: argparse.Namespace) -> dict:
    run_dir = existing_dir(args.run_dir, "run folder")
    run = load_run(run_dir)
    _key, rubric, _com = pinned_case(run)
    if load_collection(run_dir) is None:
        raise Refused("not-collected", "a review follows a collection; collect first")
    data = read_regular(need_abs(args.record, "review record"), "review record", MAX_JSON)
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
    _store_once(run_dir, "review.json", data, "already-reviewed")
    return {"result": "reviewed", "run_id": run["run_id"], "review_sha256": sha256(data)}


def actions(args: argparse.Namespace) -> dict:
    run_dir = existing_dir(args.run_dir, "run folder")
    run = load_run(run_dir)
    _key, _rubric, com = pinned_case(run)
    loaded = load_collection(run_dir)
    if loaded is None:
        raise Refused("not-collected", "an action assessment follows a collection; collect first")
    response = collected_response(run_dir, loaded[0])
    data = read_regular(need_abs(args.record, "action record"), "action record", MAX_JSON)
    rec = exact_keys(strict_json(data, "action record"),
                     ("schema", "run_id", "case_id", "case_revision", "commitments_sha256", "assessor_label",
                      "blind_to_condition", "dispositions", "notes"), "action record")
    if rec["schema"] != SCHEMA_ACTIONS:
        raise Refused("malformed", "action record schema differs")
    if rec["run_id"] != run["run_id"] or rec["case_id"] != run["case_id"] or rec["case_revision"] != run["case_revision"]:
        raise Refused("wrong-identity", "action record names another run, case or revision")
    if need_hex(rec["commitments_sha256"], "commitments sha256") != run["pins"]["commitments_sha256"]:
        raise Refused("commitments-changed", "action record was made against different commitments")
    need_label(rec["assessor_label"], "assessor label")
    if rec["blind_to_condition"] not in (True, False, None):
        raise Refused("malformed", "blind_to_condition is not true, false or null")
    if rec["notes"] is not None:
        need_text(rec["notes"], "action notes")
    if not isinstance(rec["dispositions"], list):
        raise Refused("malformed", "dispositions is not a list")
    wanted = [item["id"] for item in com["items"]]
    seen = []
    for disp in rec["dispositions"]:
        exact_keys(disp, ("commitment", "status", "evidence"), "disposition")
        if disp["commitment"] not in wanted or disp["commitment"] in seen:
            raise Refused("malformed", f"commitment is unknown or repeated: {disp['commitment']}")
        need_choice(disp["status"], DISPOSITIONS, "disposition status")
        if disp["status"] == "absent":
            if disp["evidence"] is not None:
                raise Refused("malformed", f"{disp['commitment']}: absent takes no evidence")
        else:
            need_text(disp["evidence"], f"{disp['commitment']} evidence")
            if response is None or disp["evidence"] not in response:
                raise Refused("evidence-not-in-response",
                              f"{disp['commitment']}: evidence is not an exact part of the collected response")
        seen.append(disp["commitment"])
    if sorted(seen) != sorted(wanted):
        raise Refused("malformed", "dispositions do not cover every commitment exactly once")
    _store_once(run_dir, "actions.json", data, "already-assessed")
    return {"result": "assessed", "run_id": run["run_id"], "actions_sha256": sha256(data)}


def load_supplied(run_dir: Path, name: str) -> dict | None:
    path = run_dir / name
    if not os.path.lexists(path):
        return None
    return strict_json(read_regular(path, name, MAX_JSON), name)


# ---------------------------------------------------------------- rerun

def rerun(args: argparse.Namespace) -> dict:
    trial = existing_dir(args.trial, "trial folder")
    reason = need_text(args.reason, "reason")
    if not isinstance(args.run_id, str) or not _RUN_ID.fullmatch(args.run_id):
        raise Refused("malformed", "run id is not r followed by four digits")
    sealed = load_seal(trial)
    original_dir = trial / "runs" / args.supersedes
    original = load_run(existing_dir(str(original_dir), "original run folder"))
    if seal_check(original_dir, original)["result"] != "sealed":
        raise Refused("malformed", "only a sealed run of this trial can be superseded")
    taken = {r["run_id"] for r in sealed["runs"]} | {a.get("run_id") for a in load_amendments(trial)}
    if args.run_id in taken or os.path.lexists(trial / "runs" / args.run_id):
        raise Refused("duplicate", f"run id {args.run_id} is already used in this trial")
    manifest, version, canaries = bench_state()
    if version != original["bench_version"]:
        raise Refused("mixed-version", "the bench changed since the seal; plan a new trial")
    case = next(c for c in manifest["cases"] if c["case_id"] == original["case_id"])
    inv_bytes = read_regular(trial / "investigation.json", "investigation", MAX_JSON)
    inv = parse_investigation(inv_bytes)
    cond = strict_json(read_regular(LAB / "conditions.json", "conditions.json", MAX_JSON), "conditions")
    files = kit_files(LAB / "cases" / case["case_id"], case, original["condition"], args.run_id,
                      cond[original["condition"]]["tools"])
    leaks = leak_hits(sorted(files.items()), _secret_material(manifest, canaries))
    if leaks:
        raise Refused("evaluator-leakage", "; ".join(leaks))
    old = {row["path"]: row["sha256"] for row in original["delivery"]}
    new = {p: sha256(d) for p, d in files.items()}
    differ = sorted(p for p in set(old) | set(new) if p != "PROMPT.md" and old.get(p) != new.get(p))
    if differ:
        raise Refused("parity-fail", f"replacement kit differs from the original delivery: {differ}")
    plan_run = {"run_id": args.run_id, "pair_id": original["pair_id"], "order": original["order"],
                "condition": original["condition"], "model_label": original["model_label"],
                "effort_label": original["effort_label"]}
    cand = trial / "candidates" / args.run_id
    if os.path.lexists(cand):
        raise Refused("occupied", f"candidate folder already exists: {cand}")
    record = _run_record(original["trial_id"], plan_run, version, inv, original["investigation_sha256"], case, cand,
                         original["capabilities"], files, True, original["run_id"])
    run_bytes = dumps(record)
    seq = len(load_amendments(trial)) + 1
    amendment = {"schema": SCHEMA_AMENDMENT, "seq": seq, "trial_id": original["trial_id"], "run_id": args.run_id,
                 "supersedes": original["run_id"], "reason": reason, "run_json_sha256": sha256(run_bytes),
                 "prepared_at": record["prepared_at"],
                 "note": "Late run: prepared after the seal. It is reported, never clean; a clean replacement needs a new sealed trial."}
    writer = Writer()

    def write_all() -> None:
        _write_kit(writer, cand, files)
        run_dir = trial / "runs" / args.run_id
        writer.mkdir(run_dir)
        writer.file(run_dir / "COORDINATOR.md", _coordinator_text(record, run_dir))
        writer.file(run_dir / "run.json", run_bytes)
        if not (trial / "amendments").is_dir():
            writer.mkdir(trial / "amendments")
        writer.file(trial / "amendments" / f"{seq:04d}.json", dumps(amendment))

    guarded(writer, "rerun", write_all)
    return {"result": "prepared-late", "run_id": args.run_id, "supersedes": original["run_id"], "amendment": seq}


# ---------------------------------------------------------------- compare

def load_seal(trial: Path) -> dict:
    path = trial / "seal.json"
    if not os.path.lexists(path):
        raise Refused("unsealed", "trial has no seal.json; nothing was sealed, so nothing can be compared")
    sealed = strict_json(read_regular(path, "seal.json", MAX_JSON), "seal.json")
    if not isinstance(sealed, dict) or sealed.get("schema") != SCHEMA_SEAL or sealed.get("rules") != RULES:
        raise Refused("malformed", "seal.json schema or rules differ")
    if sha256(read_regular(trial / "plan.json", "plan.json", MAX_JSON)) != sealed["plan_sha256"]:
        raise Refused("tampered", "plan.json differs from the seal")
    if sha256(read_regular(trial / "investigation.json", "investigation.json", MAX_JSON)) != sealed["investigation_sha256"]:
        raise Refused("tampered", "investigation.json differs from the seal")
    return sealed


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


def _elapsed(col: dict) -> float | None:
    if not col.get("started") or not col.get("finished"):
        return None
    return (as_time(col["finished"]) - as_time(col["started"])).total_seconds()


def _cost_view(costs: dict | None) -> dict:
    if costs is None:
        return {"supplied": False, "complete": False, "missing": [*COST_COUNTS, "cache_state", "prior_involvement"],
                "values": None, "kind": "declared"}
    missing = [k for k in COST_COUNTS if costs[k] is None]
    if costs["cache_state"] == "unknown":
        missing.append("cache_state")
    values = {k: costs[k] for k in (*COST_COUNTS, "cache_state", "prior_involvement")}
    return {"supplied": True, "complete": not missing, "missing": missing, "values": values,
            "observer": costs["observer"], "kind": "declared"}


def compare_trial(raw_trial: str) -> dict:
    trial = existing_dir(raw_trial, "trial folder")
    sealed = load_seal(trial)
    sealed_at = as_time(sealed["sealed_at"])
    meta_cache: dict[str, dict] = {}
    rows = []
    entries = [(r["run_id"], False) for r in sealed["runs"]]
    entries += [(a["run_id"], True) for a in load_amendments(trial)]
    loaded = []
    for run_id, late_entry in entries:
        run_dir = trial / "runs" / run_id
        if not os.path.lexists(run_dir / "run.json"):
            loaded.append((run_id, run_dir, None, None))
            continue
        run = load_run(run_dir)
        pinned_case(run)
        lc = load_collection(run_dir)
        loaded.append((run_id, run_dir, run, lc[0] if lc else None))
    sessions: dict[str, list[str]] = {}
    for run_id, _d, run, col in loaded:
        if col is not None:
            sessions.setdefault(col["session_label"], []).append(run_id)
    sealed_rows = {r["run_id"]: r for r in sealed["runs"]}
    for run_id, run_dir, run, col in loaded:
        planned = sealed_rows.get(run_id)
        if run is None:
            rows.append({"run_id": run_id, "status": "missing", "clean": False, "late": planned is None,
                         "pair_id": planned["pair_id"] if planned else None,
                         "condition": planned["condition"] if planned else None,
                         "case_id": planned["case_id"] if planned else None,
                         "not_clean_reasons": ["run folder or run.json is missing"]})
            continue
        if run["case_id"] not in meta_cache:
            meta_cache[run["case_id"]] = strict_json(read_regular(
                LAB / "cases" / run["case_id"] / "coordinator/meta.json", "meta", MAX_JSON), "meta")
        meta = meta_cache[run["case_id"]]
        assessment = assess_run(run_dir)
        rev = load_supplied(run_dir, "review.json")
        act = load_supplied(run_dir, "actions.json")
        events = load_events(run_dir)
        seal_now = seal_check(run_dir, run)
        input_now = check_inputs(run)
        reasons = []
        if run["late"] or seal_now["result"] == "late":
            reasons.append(f"late-prepared after the seal (supersedes {run['supersedes']})")
        elif seal_now["result"] != "sealed":
            reasons.append(f"seal {seal_now['result']}: {seal_now['detail']}")
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
                reasons.append("shared session: " + ", ".join(sorted(sessions[col["session_label"]])))
            if col["intervention"] is not None or any(e.get("kind") == "intervention" for e in events):
                reasons.append("intervention")
            if col["leakage"]:
                reasons.append("evaluator-leakage")
            if col["status"] == "completed" and col["identity"] != "matched":
                reasons.append(f"identity {col['identity']}")
            if col["input_check"]["result"] != "intact":
                reasons.append("input drift at collection: " + ", ".join(col["input_check"]["problems"]))
            if col["seal_check"]["result"] not in ("sealed", "late"):
                reasons.append(f"seal {col['seal_check']['result']} at collection")
            if col["started"] and as_time(col["started"]) < sealed_at:
                reasons.append("declared start is before the seal")
        if input_now["result"] != "intact" and not (
                col is not None and col["input_check"]["problems"] == input_now["problems"]):
            reasons.append("input drift at compare: " + ", ".join(input_now["problems"]))
        cost = _cost_view(col["costs"] if col else None)
        planned_order = run["order"]
        launch_order = cost["values"]["launch_order"] if cost["values"] else None
        action_view = None
        if act is not None:
            com = load_commitments(LAB / "cases" / run["case_id"], run["case_id"], run["case_revision"])
            kinds = {i["id"]: i["kind"] for i in com["items"]}
            action_view = {"assessor_label": act["assessor_label"], "blind_to_condition": act["blind_to_condition"],
                           "dispositions": [{"commitment": d["commitment"], "kind": kinds[d["commitment"]],
                                             "status": d["status"]} for d in act["dispositions"]],
                           "kind": "supplied judgment"}
        rows.append({
            "run_id": run_id,
            "pair_id": run["pair_id"],
            "order": planned_order,
            "launch_order": launch_order,
            "late": run["late"],
            "supersedes": run["supersedes"],
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
            "input_check_collect": None if col is None else col["input_check"]["result"],
            "input_check_now": input_now["result"],
            "seal_check": seal_now["result"],
            "deterministic_pass": assessment["deterministic_pass"],
            "quotes_preserved": assessment.get("quotes_preserved"),
            "outcome_found": (assessment["checks"] or {}).get("outcome", {}).get("found"),
            "assessment": assessment,
            "actions": action_view,
            "review": None if rev is None else {
                "reviewer_label": rev["reviewer_label"], "blind_to_condition": rev["blind_to_condition"],
                "scores": {s["item"]: s["score"] for s in rev["scores"]},
                "reviewer_minutes": rev["reviewer_minutes"],
                "director_attention_events": rev["director_attention_events"], "kind": "supplied judgment"},
            "costs": cost,
            "elapsed_seconds": None if col is None else _elapsed(col),
            "tool_events": None if col is None else col["tool_event_count"],
            "usage": None if col is None else col["usage"],
            "records": record_hashes(run_dir),
            "corrections": sum(1 for e in events if e.get("kind") == "correction"),
            "interventions": sum(1 for e in events if e.get("kind") == "intervention")
            + (1 if col is not None and col["intervention"] is not None else 0),
        })
    by_id = {r["run_id"]: r for r in rows}
    pairs = []
    for pair_id, parity in sorted(sealed["pairs"].items()):
        members = [by_id[parity["baseline"]], by_id[parity["assisted"]]]
        why = [f"{m['run_id']} not clean" for m in members if not m["clean"]]
        pairs.append({"pair_id": pair_id, "case_id": members[0]["case_id"], "baseline": parity["baseline"],
                      "assisted": parity["assisted"], "parity": parity["parity"],
                      "baseline_reach": parity["baseline_reach"], "readable": not why, "not_readable": why,
                      "assisted_first": sealed_rows[parity["assisted"]]["order"] < sealed_rows[parity["baseline"]]["order"]})
    counts = {}
    for cond in CONDITIONS:
        mine = [r for r in rows if r.get("condition") == cond and not r.get("late")]
        clean = [r for r in mine if r["clean"]]
        items: dict[str, dict] = {}
        tallies: dict[str, dict] = {}
        for r in clean:
            if r.get("review"):
                for item, score in r["review"]["scores"].items():
                    slot = items.setdefault(item, {"reviewed_clean_runs": 0, "score_sum": 0})
                    slot["reviewed_clean_runs"] += 1
                    slot["score_sum"] += score
            if r.get("actions"):
                for d in r["actions"]["dispositions"]:
                    slot = tallies.setdefault(d["kind"], {s: 0 for s in DISPOSITIONS})
                    slot[d["status"]] += 1
        counts[cond] = {
            "planned_runs": len(mine),
            "by_status": {s: sum(1 for r in mine if r["status"] == s) for s in (*STATUSES, "uncollected", "missing")},
            "clean": len(clean),
            "clean_deterministic_pass": sum(1 for r in clean if r.get("deterministic_pass")),
            "clean_with_action_record": sum(1 for r in clean if r.get("actions")),
            "commitments_by_kind": dict(sorted(tallies.items())),
            "rubric_items": dict(sorted(items.items())),
            "cost_complete": sum(1 for r in mine if r.get("costs", {}).get("complete")),
        }
    prep = sealed["preparation"]
    planned = len(sealed["runs"])
    share = None
    if prep["amortization"] == "equal-split-over-planned-runs" and prep["reusable_setup_minutes"] is not None:
        share = round(prep["reusable_setup_minutes"] / planned, 2)
    trial_summary = {
        "trial_id": sealed["trial_id"],
        "seal_sha256": sha256(read_regular(trial / "seal.json", "seal.json", MAX_JSON)),
        "sealed_at": sealed["sealed_at"],
        "planned_runs": planned,
        "collected_planned_runs": sum(1 for r in rows if not r.get("late") and r["status"] not in ("uncollected", "missing")),
        "late_runs": sum(1 for r in rows if r.get("late")),
        "pairs": len(pairs),
        "readable_pairs": sum(1 for p in pairs if p["readable"]),
        "assisted_first_pairs": sum(1 for p in pairs if p["assisted_first"]),
        "preparation": {**prep, "machine_seconds": sealed["preparation_machine_seconds"],
                        "machine_seconds_kind": "mechanical", "minutes_kind": "declared",
                        "reusable_setup_share_per_planned_run": share},
    }
    trial_summary["complete"] = (trial_summary["collected_planned_runs"] == planned
                                 and trial_summary["readable_pairs"] == len(pairs))
    inv = parse_investigation(read_regular(trial / "investigation.json", "investigation.json", MAX_JSON))
    result = {
        "schema": SCHEMA_COMPARISON,
        "rules": RULES,
        "bench_version": sealed["bench_version"],
        "investigation_sha256": sealed["investigation_sha256"],
        "investigation": {"page": inv["page"], "pass": inv["pass"]},
        "trial": trial_summary,
        "synthetic": any(r.get("label") == "SYNTHETIC" for r in rows),
        "pairs": pairs,
        "rows": rows,
        "counts": counts,
        "not_computed": ["ratios between conditions", "time or token savings", "rankings", "a pass score",
                         "subscription or provider cost conversion"],
    }
    markdown = render(result)
    result["markdown"] = markdown
    result["markdown_sha256"] = sha256(markdown.encode("utf-8"))
    return result


def _cell(value: object) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, float):
        return f"{value:g}"
    return str(value).replace("|", "\\|")


def render(result: dict) -> str:
    t = result["trial"]
    lines = ["# Prime bench comparison", ""]
    if result["synthetic"]:
        lines += ["**SYNTHETIC.** At least one run is labelled SYNTHETIC. These records demonstrate the harness and "
                  "its report format. They show no model performance.", ""]
    inv = result["investigation"]
    lines += [f"Rules `{result['rules']}`. Bench version `{result['bench_version']}`. Investigation {inv['page']} "
              f"pass {inv['pass']}. Trial {t['trial_id']}, seal `{t['seal_sha256']}`, sealed {t['sealed_at']} "
              "(machine clock).", ""]
    status = "complete" if t["complete"] else "INCOMPLETE"
    lines += [f"**Trial {status}.** Planned runs {t['planned_runs']}; collected {t['collected_planned_runs']}; "
              f"late runs {t['late_runs']} (reported, never clean). Pairs {t['pairs']}; readable {t['readable_pairs']}; "
              f"assisted first in {t['assisted_first_pairs']}. A trial is complete only when every planned run is "
              "collected and every pair is readable.", ""]
    lines += ["## Kinds of fact",
              "- **mechanical**: computed by the harness: hashes, pair parity, baseline reach, input checks, seal "
              "binding, record bindings, string checks, the seal's own clock.",
              "- **declared**: supplied by people: session times, isolation and confinement, tool events, usage, "
              "costs, launch order, cache state.",
              "- **supplied judgment**: rubric scores and action dispositions. Code checked only their shape, "
              "identity and that action evidence occurs in the response.",
              "- Hashes do not prove when a session started or what else it could see.", ""]
    lines += ["## What is counted",
              "- A run is clean only when it was sealed before answers, its inputs were intact at collection and at "
              "compare, it completed, isolation was declared supported and used fresh, its session was used by no "
              "other run, there was no intervention or leakage, its run line matched, and its declared start is not "
              "before the seal.",
              "- A pair is readable only when both its runs are clean.",
              "- String checks: run line, outcome label, mentions, exact quotes, forbidden patterns, canary. They are "
              "not a semantic or action verdict. Quote preservation is reported on its own.",
              "- Action commitments: per kind, the count of present, contradicted and absent dispositions among clean "
              "runs with a supplied record. No universal score.",
              "- Unknown values are shown as `unknown`, never 0. A cost record is complete only when every field is "
              "known.", ""]
    lines += ["## Pairs", "", "| pair | case | baseline | assisted | parity | baseline reach | readable |",
              "|---|---|---|---|---|---|---|"]
    for p in result["pairs"]:
        lines.append(f"| {p['pair_id']} | {p['case_id']} | {p['baseline']} | {p['assisted']} | {p['parity']} "
                     f"| {p['baseline_reach']} | {'yes' if p['readable'] else 'no: ' + '; '.join(p['not_readable'])} |")
    lines += ["", "## Runs", "",
              "| run | pair | order (plan / launch) | case | condition | label | status | clean | inputs (collect / now) "
              "| outcome | string checks | quotes | actions | review | elapsed s | costs |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in result["rows"]:
        if r["status"] == "missing":
            lines.append(f"| {r['run_id']} | {_cell(r['pair_id'])} | | {_cell(r['case_id'])} | {_cell(r['condition'])} "
                         "| | missing | no | | | | | | | | |")
            continue
        acts = "unknown" if r["actions"] is None else ", ".join(
            f"{d['commitment']}={d['status']}" for d in r["actions"]["dispositions"])
        review = "unknown" if r["review"] is None else ", ".join(
            f"{k}={v}" for k, v in sorted(r["review"]["scores"].items()))
        cost = r["costs"]
        cost_cell = "not supplied" if not cost["supplied"] else (
            "complete" if cost["complete"] else "incomplete: " + ", ".join(cost["missing"]))
        quotes = "n/a" if r["quotes_preserved"] is None else ("kept" if r["quotes_preserved"] else "not kept")
        lines.append(
            f"| {r['run_id']}{' (late)' if r['late'] else ''} | {r['pair_id']} | {r['order']} / {_cell(r['launch_order'])} "
            f"| {r['case_id']} r{r['case_revision']} | {r['condition']} | {_cell(r['label'])} | {r['status']} "
            f"| {'yes' if r['clean'] else 'no'} | {_cell(r['input_check_collect'])} / {r['input_check_now']} "
            f"| {_cell(r['outcome_found'])} | {'pass' if r['deterministic_pass'] else 'fail'} | {quotes} | {acts} "
            f"| {review} | {_cell(r['elapsed_seconds'])} | {cost_cell} |")
    lines += ["", "## Costs (declared unless marked)", "",
              "| run | tool ops | failed calls | repairs (n / min) | corrections (n / min) | Director (n / min) "
              "| cache | tool events | usage |", "|---|---|---|---|---|---|---|---|---|"]
    for r in result["rows"]:
        if r["status"] == "missing":
            continue
        v = r["costs"]["values"] or {}
        usage = "unknown" if r["usage"] is None else ", ".join(
            f"{k}={val}" for k, val in sorted(r["usage"].items()) if k != "source")
        lines.append(
            f"| {r['run_id']} | {_cell(v.get('tool_operations'))} | {_cell(v.get('failed_tool_calls'))} "
            f"| {_cell(v.get('request_repairs'))} / {_cell(v.get('repair_minutes'))} "
            f"| {_cell(v.get('correction_loops'))} / {_cell(v.get('correction_minutes'))} "
            f"| {_cell(v.get('director_attention_events'))} / {_cell(v.get('director_attention_minutes'))} "
            f"| {_cell(v.get('cache_state'))} | {_cell(r['tool_events'])} | {usage} |")
    prep = t["preparation"]
    lines += ["", f"Preparation: owner {prep['owner']}; seal took {prep['machine_seconds']} s (mechanical); reusable "
              f"setup {_cell(prep['reusable_setup_minutes'])} min and per-run setup {_cell(prep['per_run_setup_minutes'])} "
              f"min (declared); amortization {prep['amortization']}"
              + (f", reusable share per planned run {prep['reusable_setup_share_per_planned_run']} min."
                 if prep["reusable_setup_share_per_planned_run"] is not None else "."), ""]
    lines += ["## Counts by condition (planned runs; late runs excluded)", ""]
    for cond, c in result["counts"].items():
        status_text = ", ".join(f"{k} {v}" for k, v in c["by_status"].items())
        lines.append(f"- **{cond}**: {c['planned_runs']} planned ({status_text}); clean {c['clean']}; clean with "
                     f"string checks passing {c['clean_deterministic_pass']}; clean with an action record "
                     f"{c['clean_with_action_record']}; cost records complete {c['cost_complete']}.")
        for kind, slot in c["commitments_by_kind"].items():
            lines.append(f"  - {kind}: present {slot['present']}, contradicted {slot['contradicted']}, "
                         f"absent {slot['absent']}.")
        for item, slot in c["rubric_items"].items():
            lines.append(f"  - rubric {item}: {slot['reviewed_clean_runs']} clean reviewed runs, score sum "
                         f"{slot['score_sum']}.")
    lines += ["", "## Not clean, failed, late or missing (kept, not dropped)", ""]
    unclean = [r for r in result["rows"] if not r["clean"]]
    lines += [f"- {r['run_id']} ({_cell(r.get('condition'))}): {'; '.join(r['not_clean_reasons'])}"
              for r in unclean] or ["- none"]
    lines += ["", "## Corrections and interventions (separate from the original runs)", ""]
    extra = [r for r in result["rows"] if r.get("corrections") or r.get("interventions")]
    lines += [f"- {r['run_id']}: corrections {r['corrections']}, interventions {r['interventions']}"
              for r in extra] or ["- none"]
    lines += ["", "## Not computed", "",
              "No ratio between conditions, no time or token saving, no ranking, no pass score and no provider or "
              "subscription cost conversion. One trial of fixed cases cannot establish general productivity.", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- export

def export(args: argparse.Namespace) -> dict:
    result = compare_trial(args.trial)
    trial = existing_dir(args.trial, "trial folder")
    dest = fresh_dest(args.dest, "export folder")
    inv = result["investigation"]
    nn = inv["pass"].split(".")[1]
    files: dict[str, bytes] = {
        "comparison.md": result["markdown"].encode("utf-8"),
        "comparison.json": dumps({k: v for k, v in result.items() if k != "markdown"}),
        "seal.json": read_regular(trial / "seal.json", "seal.json", MAX_JSON),
        "plan.json": read_regular(trial / "plan.json", "plan.json", MAX_JSON),
        "investigation.json": read_regular(trial / "investigation.json", "investigation.json", MAX_JSON),
    }
    for amendment in sorted(os.listdir(trial / "amendments")) if (trial / "amendments").is_dir() else []:
        files[f"amendments/{need_rel(amendment, 'amendment')}"] = read_regular(
            trial / "amendments" / amendment, amendment, MAX_JSON)
    for row in result["rows"]:
        run_dir = trial / "runs" / row["run_id"]
        for rel in row.get("records", {}):
            files[f"runs/{row['run_id']}/{rel}"] = read_regular(run_dir.joinpath(*rel.split("/")), rel, MAX_TOOL_LOG)
    template = (
        f"# 05.{nn}.return.md — TEMPLATE for the bench coordinator\n\n"
        f"Investigation {inv['page']}, pass 05.{nn}. Trial {result['trial']['trial_id']}, seal "
        f"{result['trial']['seal_sha256']}.\n"
        "This is a TEMPLATE. The coordinator writes every section in their own words before capture.\n"
        "Nothing below is a completed return or a review.\n\n"
        "## Did\nTEMPLATE: trial sealed, runs launched and collected, records supplied; exact commands.\n\n"
        "## Blocked\nTEMPLATE: anything that stopped a run, an input check or a review.\n\n"
        "## Need\nTEMPLATE: the Director or Prime choices needed next.\n\n"
        "## Records\n"
        f"comparison.md sha256 {sha256(files['comparison.md'])}\n"
        f"comparison.json sha256 {sha256(files['comparison.json'])}\n"
        f"seal.json sha256 {sha256(files['seal.json'])}\n")
    files[f"05.{nn}.return.TEMPLATE.md"] = template.encode("utf-8")
    artifacts = ["comparison.md", "comparison.json", "seal.json"]
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
        "4. Prime places the captured return into the N7NN page with the reviewed workflow. Run records under runs/, "
        "plan.json, investigation.json and amendments/ stay in this export folder, bound by comparison.json and "
        "seal.json.\n")
    files["CAPTURE.txt"] = capture.encode("utf-8")
    writer = Writer()

    def write_all() -> None:
        writer.mkdir(dest)
        for rel, data in sorted(files.items()):
            writer.file(dest.joinpath(*rel.split("/")), data)

    guarded(writer, "export", write_all)
    return {"result": "exported", "dest": str(dest), "files": len(files),
            "comparison_sha256": sha256(files["comparison.md"]), "trial_complete": result["trial"]["complete"]}


# ---------------------------------------------------------------- cli

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prime_bench.py", description="Bounded Prime benchmark harness, rules 2.")
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name: str, required: tuple[str, ...], optional: tuple[str, ...] = (), multi: tuple[str, ...] = ()):
        p = sub.add_parser(name)
        for flag in required:
            p.add_argument(flag, required=True)
        for flag in optional:
            p.add_argument(flag)
        p.add_argument("--json", action="store_true")
        return p

    add("validate", ())
    sub.add_parser("manifest")
    add("seal", ("--plan", "--investigation", "--dest"))
    add("check-inputs", ("--run-dir",))
    add("collect", ("--run-dir", "--expect-run", "--expect-condition", "--status", "--label", "--session-label",
                    "--isolation-used"),
        ("--reason", "--response", "--tool-log", "--tool-events", "--usage", "--costs", "--started", "--finished",
         "--intervention"))
    add("event", ("--run-dir", "--kind", "--text"), ("--attachment",))
    add("assess", ("--run-dir",))
    add("review", ("--run-dir", "--record"))
    add("actions", ("--run-dir", "--record"))
    add("rerun", ("--trial", "--supersedes", "--run-id", "--reason"))
    add("compare", ("--trial",))
    add("export", ("--trial", "--dest"))
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
        if args.command == "check-inputs":
            result = check_inputs(load_run(existing_dir(args.run_dir, "run folder")))
            emit(result, as_json, f"{result['run_id']} inputs {result['result']}\n"
                 + "".join(f"  {p}\n" for p in result["problems"]))
            return 0 if result["result"] == "intact" else 1
        if args.command == "assess":
            result = assess_run(existing_dir(args.run_dir, "run folder"))
            emit(result, as_json, f"{result['run_id']} string checks "
                 f"{'pass' if result['deterministic_pass'] else 'fail'}\n")
            return 0
        if args.command == "compare":
            result = compare_trial(args.trial)
            emit(result, as_json, result["markdown"])
            return 0
        handler = {"seal": seal, "collect": collect, "event": event, "review": review, "actions": actions,
                   "rerun": rerun, "export": export}
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
