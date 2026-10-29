"""Prime status and intake, fixture lab (0507.prime-support/05.02). Standard library plus read-only Git.

Reads only what a registry names. Never fetches, launches, queues, reviews or accepts.
Contract: 00.kernel/00.00.10.work/0507.prime-support/evidence/build05.02/DESIGN.002.md.
Every field named there is a provisional fixture contract, not workshop law.

Patterns cited, not imported: exclusive-create records with exact keys and a version stamp,
and refusal instead of repair (labs/clerk-handoff-pass02/clerk.py, exclusive_write and validate_job).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clerk_adapter  # noqa: E402  same lab folder; the only Clerk reader (05.04)

REGISTRY_SCHEMA = "prime-support-registry"
INTAKE_SCHEMA = "prime-intake/1"
REPO_KEYS = {"local", "branch", "remote_ref", "worktree", "history_limit"}
LANE_KEYS = {"lane", "project", "owner_label", "repository", "pages", "return_files", "review_sources"}
CANON_KEYS = {"repository", "path", "lane"}
TOP_REQUIRED = {"schema", "version", "repositories", "lanes"}
TOP_OPTIONAL = {"canonical_assignment", "attention_order"}
ATTENTION_KINDS = ["conflict", "missing", "unsupported", "bad-intake", "invalid-review", "clerk-not-clean",
                   "review-needed", "unseen",
                   "history-unknown", "open-finding"]
ASSIGNMENT_KEYS = {"record", "schema", "desk", "book", "workflow_space", "current_work", "pack",
                   "assignment_state", "waits_on", "next", "updated"}
RECORD_KEYS = {"schema", "subject_id", "subject", "observed", "supersedes", "by", "at", "note"}
SUBJECT_KEYS = {"kind", "repository", "path", "revision_id"}
OBSERVED_KEYS = {"source", "commit", "whole_sha256", "execution"}
# 05.04: Clerk returns are a distinct subject kind, stored as prime-intake/2. /1 records are read unchanged.
INTAKE_SCHEMA_2 = "prime-intake/2"
CLERK_SUBJECT_KEYS = {"kind", "store", "job_id", "event_sha256"}
CLERK_OBSERVED_KEYS = {"tool_sha256", "exit", "state", "checks", "problems"}
CLERK_JOB_KEYS = {"store", "job_id", "instructions_base", "reviewer"}
GIT_ALLOWED = {"rev-parse", "show", "ls-tree", "log", "status", "merge-base", "for-each-ref", "cat-file"}
OPEN = {"unresolved", "fix-planned", "director-pending"}
CLOSED = {"verified-fixed", "answered-with-reason", "decided"}
EXECUTION_STATES = {"claimed", "running", "returned", "stopped"}
ELIGIBLE = {"returned", "unknown"}
SEP = " — "
PAGE_FILE = re.compile(r"^05\.\d{2}\.md$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
FINDING_ID = re.compile(r"^[A-Za-z][A-Za-z0-9-]*$")
LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
NOTE = "acknowledged as seen; not reviewed, not accepted"


class Refusal(Exception):
    pass


def refuse(message: str) -> None:
    raise Refusal(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def loads_strict(text: str, label: str):
    def pairs(seq):
        out = {}
        for key, value in seq:
            if key in out:
                refuse(f"{label}: duplicate key {key}")
            out[key] = value
        return out

    def constant(name):
        refuse(f"{label}: nonfinite number {name}")

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except json.JSONDecodeError as exc:
        refuse(f"{label}: invalid JSON ({exc.msg})")


# ---------- registry ----------

def _rel(path, label: str) -> str:
    if not isinstance(path, str) or path == "":
        refuse(f"registry: {label} is not a path")
    if "\\" in path or path.startswith("/") or re.match(r"^[A-Za-z]:", path):
        refuse(f"registry: {label} must be a relative forward-slash path: {path!r}")
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        refuse(f"registry: {label} escapes or is not normal: {path!r}")
    return path


def _text(value, label: str) -> str:
    if not isinstance(value, str) or value.strip() == "" or any(ord(c) < 32 for c in value):
        refuse(f"registry: {label} is not plain text")
    return value


def load_registry(path_text: str) -> tuple[dict, str]:
    path = Path(path_text)
    if not path.is_absolute():
        refuse("registry path must be absolute")
    if not path.is_file():
        refuse("registry is missing")
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("registry: not UTF-8")
    reg = loads_strict(text, "registry")
    if not isinstance(reg, dict):
        refuse("registry: not an object")
    keys = set(reg)
    version = reg.get("version")
    if reg.get("schema") != REGISTRY_SCHEMA or type(version) is not int or version not in (1, 2):
        refuse("registry: unsupported schema or version")
    optional = TOP_OPTIONAL | ({"clerk_tool"} if version == 2 else set())  # 05.04: version 2 adds Clerk jobs
    if not TOP_REQUIRED <= keys or keys - TOP_REQUIRED - optional:
        extra = sorted(keys - TOP_REQUIRED - optional)
        refuse("registry: " + (f"unknown key {extra[0]}" if extra else "missing required key"))
    repos = reg["repositories"]
    if not isinstance(repos, dict) or not repos:
        refuse("registry: repositories must be a non-empty object")
    for name, repo in repos.items():
        if not LABEL.fullmatch(name):
            refuse(f"registry: repository name {name!r} is not a plain label")
        if not isinstance(repo, dict) or set(repo) != REPO_KEYS:
            refuse(f"registry: repository {name} must have exactly {sorted(REPO_KEYS)}")
        if not isinstance(repo["local"], str) or not os.path.isabs(repo["local"]):
            refuse(f"registry: repository {name} local must be absolute")
        _text(repo["branch"], f"{name}.branch")
        if not isinstance(repo["remote_ref"], str) or not repo["remote_ref"].startswith("refs/remotes/"):
            refuse(f"registry: repository {name} remote_ref must start with refs/remotes/")
        if repo["worktree"] not in ("registered-paths", "off"):
            refuse(f"registry: repository {name} worktree must be registered-paths or off")
        limit = repo["history_limit"]
        if type(limit) is not int or not 1 <= limit <= 1000:
            refuse(f"registry: repository {name} history_limit must be an int 1..1000")
    lanes = reg["lanes"]
    if not isinstance(lanes, list) or not lanes:
        refuse("registry: lanes must be a non-empty list")
    seen = set()
    clerk_pairs = set()
    for lane in lanes:
        allowed = LANE_KEYS | ({"clerk_jobs"} if version == 2 else set())
        if not isinstance(lane, dict) or not LANE_KEYS <= set(lane) or set(lane) - allowed:
            refuse(f"registry: each lane must have exactly {sorted(LANE_KEYS)}"
                   + (" (and optionally clerk_jobs)" if version == 2 else ""))
        lane.setdefault("clerk_jobs", [])
        if not isinstance(lane["clerk_jobs"], list):
            refuse(f"registry: lane {lane.get('lane')} clerk_jobs must be a list")
        for job in lane["clerk_jobs"]:
            if not isinstance(job, dict) or set(job) != CLERK_JOB_KEYS:
                refuse(f"registry: each clerk job must have exactly {sorted(CLERK_JOB_KEYS)}")
            for key in ("store", "instructions_base"):
                if not isinstance(job[key], str) or not os.path.isabs(job[key]):
                    refuse(f"registry: clerk job {key} must be absolute")
            for key in ("job_id", "reviewer"):
                if not isinstance(job[key], str) or not clerk_adapter.CLERK_ID.fullmatch(job[key]):
                    refuse(f"registry: clerk job {key} is not a Clerk id")
            pair = (clerk_adapter.canonical_store(job["store"]), job["job_id"].casefold())
            if pair in clerk_pairs:
                refuse(f"registry: clerk job {job['job_id']} is registered twice for one store")
            clerk_pairs.add(pair)
        if not LABEL.fullmatch(str(lane["lane"])) or lane["lane"] in seen:
            refuse(f"registry: lane id {lane['lane']!r} is invalid or repeated")
        seen.add(lane["lane"])
        _text(lane["project"], "project")
        _text(lane["owner_label"], "owner_label")
        if lane["repository"] not in repos:
            refuse(f"registry: lane {lane['lane']} names an unknown repository")
        for key in ("pages", "return_files", "review_sources"):
            if not isinstance(lane[key], list):
                refuse(f"registry: lane {lane['lane']} {key} must be a list")
            for item in lane[key]:
                _rel(item, f"{lane['lane']}.{key}")
    canon = reg.get("canonical_assignment")
    if canon is not None:
        if not isinstance(canon, dict) or set(canon) != CANON_KEYS:
            refuse("registry: canonical_assignment must have repository, path, lane")
        if canon["repository"] not in repos or canon["lane"] not in seen:
            refuse("registry: canonical_assignment names an unknown repository or lane")
        _rel(canon["path"], "canonical_assignment.path")
    tool = reg.get("clerk_tool")
    if clerk_pairs and tool is None:
        refuse("registry: clerk_jobs require clerk_tool")
    if tool is not None:
        if not isinstance(tool, dict) or set(tool) != {"path", "sha256"}:
            refuse("registry: clerk_tool must have exactly path and sha256")
        if not isinstance(tool["path"], str) or not os.path.isabs(tool["path"]):
            refuse("registry: clerk_tool.path must be absolute")
        if not isinstance(tool["sha256"], str) or not HEX64.fullmatch(tool["sha256"]):
            refuse("registry: clerk_tool.sha256 must be 64 hex")
    order = reg.get("attention_order", ATTENTION_KINDS)
    if not isinstance(order, list) or len(set(order)) != len(order) or set(order) - set(ATTENTION_KINDS):
        refuse("registry: attention_order must list distinct known kinds")
    reg["attention_order"] = order + [k for k in ATTENTION_KINDS if k not in order]
    return reg, sha256(raw)


# ---------- git (allowlisted, read-only) ----------

class Git:
    def __init__(self, local: str) -> None:
        self.local = local
        self.calls: list[list[str]] = []

    def run(self, *args: str, ok_codes=(0,)) -> tuple[int, bytes]:
        if not args or args[0] not in GIT_ALLOWED:
            raise AssertionError(f"git subcommand not allowed: {args[:1]}")
        self.calls.append(list(args))
        env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
        proc = subprocess.run(["git", "-C", self.local, *args], capture_output=True, env=env, timeout=60)
        if proc.returncode not in ok_codes:
            raise Refusal(f"git {args[0]} failed in {self.local}: {proc.stderr.decode('utf-8', 'replace').strip()}")
        return proc.returncode, proc.stdout

    def commit(self, ref: str) -> str | None:
        code, out = self.run("rev-parse", "--verify", "--quiet", "--end-of-options", ref + "^{commit}", ok_codes=(0, 1))
        return out.decode().strip() if code == 0 else None

    def shallow(self) -> bool:
        return self.run("rev-parse", "--is-shallow-repository")[1].decode().strip() == "true"

    def ancestor(self, a: str, b: str) -> bool:
        return self.run("merge-base", "--is-ancestor", a, b, ok_codes=(0, 1))[0] == 0

    def blob(self, commit: str, path: str) -> bytes | None:
        code, _ = self.run("cat-file", "-e", f"{commit}:{path}", ok_codes=(0, 1, 128))
        if code != 0:
            return None
        return self.run("show", f"{commit}:{path}")[1]

    def names(self, commit: str, folder: str) -> list[str]:
        out = self.run("ls-tree", "--name-only", commit, folder + "/")[1].decode("utf-8")
        return [line.rsplit("/", 1)[-1] for line in out.splitlines() if line]

    def history(self, refs: list[str], path: str, limit: int) -> list[tuple[str, int]]:
        if not refs:
            return []
        # --topo-order: children before parents. Commit dates are never used for ordering (PSI-02).
        out = self.run("log", "--topo-order", "--format=%H %ct", "-n", str(limit), *refs, "--", path)[1].decode()
        return [(line.split()[0], int(line.split()[1])) for line in out.splitlines() if line.strip()]

    def dirty(self, paths: list[str]) -> list[str]:
        if not paths:
            return []
        out = self.run("status", "--porcelain=v1", "-z", "--untracked-files=all", "--", *paths)[1]
        return [entry.decode("utf-8", "replace") for entry in out.split(b"\0") if entry]


# ---------- structure (PS-01, PS-02) ----------

def _fence_open(line: str):
    stripped = line.lstrip(" ")
    if len(line) - len(stripped) > 3:
        return None
    m = re.match(r"^(`{3,}|~{3,})", stripped)
    return m.group(1) if m else None


def reviewable_bytes(data: bytes, raw_lines: list[bytes], cut: int | None) -> bytes:
    """Bytes before the Review heading line (or the whole file), with trailing blank lines removed and one LF
    added. Appending a Review, and the blank line before it, then leaves the identity unchanged (DESIGN.002 §3)."""
    body = b"\n".join(raw_lines[:cut]) if cut is not None else data
    return body.rstrip(b" \t\r\n") + b"\n"


def parse_source(data: bytes, kind: str) -> dict:
    """kind is page-return or return-file. Returns status ok|no-return|unsupported with identity fields."""
    out = {"status": "ok", "reason": "", "whole": sha256(data), "revision_id": None, "execution": None,
           "review": None}
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return dict(out, status="unsupported", reason="not UTF-8")
    raw_lines = data.split(b"\n")
    lines = [line.rstrip("\r") for line in text.split("\n")]
    fence = None
    returns, reviews = [], []
    for n, line in enumerate(lines):
        if fence:
            stripped = line.strip()
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                fence = None
            continue
        opened = _fence_open(line)
        if opened:
            fence = opened
            continue
        m = re.match(r"^(#{1,6}) (.*)$", line)
        if not m:
            continue
        level, title = len(m.group(1)), m.group(2)
        word = title.casefold()
        if not (word.startswith("return") or word.startswith("review")):
            continue
        if kind == "return-file" and n == 0 and level == 1 and (title == "Return" or title.startswith("Return" + SEP)):
            returns.append(n)
        elif level == 2 and kind == "page-return" and (title == "Return" or title.startswith("Return" + SEP)):
            returns.append(n)
        elif level == 2 and (title == "Review" or title.startswith("Review" + SEP)):
            reviews.append(n)
        else:
            return dict(out, status="unsupported", reason=f"ambiguous heading line {n + 1}")
    if fence:
        return dict(out, status="unsupported", reason="unclosed fence")
    if kind == "return-file" and returns != [0]:
        return dict(out, status="unsupported", reason="return file must start with '# Return'")
    if len(returns) > 1 or len(reviews) > 1:
        return dict(out, status="unsupported", reason="duplicate heading")
    if not returns:
        return dict(out, status="no-return", reason="no Return section")
    if reviews and reviews[0] < returns[0]:
        return dict(out, status="unsupported", reason="Review before Return")
    cut = reviews[0] if reviews else None
    out["revision_id"] = sha256(reviewable_bytes(data, raw_lines, cut))
    body_end = cut if cut is not None else len(lines)
    body = [line for line in lines[returns[0] + 1:body_end] if line.strip()]
    first = body[0] if body else ""
    m = re.fullmatch(r"execution: (\w+)", first)
    if m and m.group(1) in EXECUTION_STATES:
        out["execution"] = m.group(1)
    elif len(body) == 1 and first == "PENDING.":
        out["execution"] = "pending"
    else:
        out["execution"] = "unknown"
    if cut is not None:
        out["review"] = parse_review_lines(lines[cut + 1:])
    return out


def parse_review_lines(lines: list[str]) -> dict:
    review = {"prefix": None, "legacy_whole": None, "target": None, "disposition": None, "findings": [], "bad": []}
    for line in lines:
        m = re.fullmatch(r"reviewed_return_prefix: ([0-9a-f]{64})", line.strip())
        if m:
            review["prefix"] = m.group(1)
            continue
        m = re.fullmatch(r"reviewed_return_path: (\S+)", line.strip())
        if m:
            review["target"] = m.group(1)
            continue
        m = re.search(r"Reviewed return SHA-256: `?([0-9a-f]{64})`?", line)
        if m:
            review["legacy_whole"] = m.group(1)
            continue
        if line.startswith("Disposition: ") and review["disposition"] is None:
            review["disposition"] = line[len("Disposition: "):].strip()
            continue
        if line.startswith("findings:"):
            for item in line[len("findings:"):].split(";"):
                item = item.strip()
                if not item:
                    continue
                if "=" not in item or not FINDING_ID.fullmatch(item.split("=", 1)[0].strip()):
                    review["bad"].append(item)
                    continue
                ident, resolution = (part.strip() for part in item.split("=", 1))
                review["findings"].append((ident, resolution))
    return review


# ---------- evaluation ----------

class Repo:
    def __init__(self, name: str, spec: dict) -> None:
        self.name = name
        self.spec = spec
        self.git = Git(spec["local"])
        self.problem = None
        self.head = self.remote = None
        self.shallow = False
        self.relation = "unknown"
        self._anc: dict[tuple, bool] = {}
        if not Path(spec["local"]).is_dir():
            self.problem = "repository path is missing"
            return
        try:
            self.head = self.git.commit("HEAD")
            self.remote = self.git.commit(spec["remote_ref"])
            self.shallow = self.git.shallow()
        except Refusal as exc:
            self.problem = str(exc)
            return
        if self.head and self.remote:
            if self.head == self.remote:
                self.relation = "same"
            elif self.git.ancestor(self.remote, self.head):
                self.relation = "local ahead of last-observed remote"
            elif self.git.ancestor(self.head, self.remote):
                self.relation = "local behind last-observed remote (stale local)"
            else:
                self.relation = "diverged"
        elif self.head and not self.remote:
            self.relation = "remote ref not present locally"

    @property
    def worktree(self) -> bool:
        return self.spec["worktree"] == "registered-paths"

    def refs(self) -> list[str]:
        return [c for c in dict.fromkeys([self.head, self.remote]) if c]

    def is_ancestor(self, a: str, b: str) -> bool:
        """True when commit a is an ancestor of commit b (a != b). Cached; causal order only (PSI-02)."""
        key = (a, b)
        if key not in self._anc:
            self._anc[key] = a != b and self.git.ancestor(a, b)
        return self._anc[key]

    def observations(self, path: str) -> list[dict]:
        found = []
        for label, commit in (("published", self.remote), ("local", self.head)):
            if commit:
                data = self.git.blob(commit, path)
                if data is not None:
                    found.append({"label": label, "commit": commit, "data": data})
        if self.worktree:
            disk = Path(self.spec["local"]) / path
            if disk.is_file() and not disk.is_symlink():
                found.append({"label": "worktree", "commit": None, "data": disk.read_bytes()})
        return found


DRAFT = "worktree (uncommitted draft)"


def _versions(repo: Repo, path: str, obs: list[dict], hist: list) -> list[tuple]:
    """(topo index, source label, bytes, commit or None). Parents come before children. A worktree copy is
    included only when it differs from HEAD's bytes (or HEAD lacks the file): an identical copy is the same
    observation, not a new one (PSI-02)."""
    out = []
    for i, (commit, _ct) in enumerate(reversed(hist)):
        data = repo.git.blob(commit, path)
        if data is not None:
            out.append((i, f"{path}@{commit}", data, commit))
    head = next((o["data"] for o in obs if o["label"] == "local"), None)
    for o in obs:
        if o["commit"] is None and o["data"] != head:
            out.append((len(hist), f"{path}@{DRAFT}", o["data"], None))
    return out


def _history_state(repo: Repo, hist: list) -> str:
    if repo.shallow or len(hist) >= repo.spec["history_limit"]:
        return "incomplete"
    return "none" if not hist else "complete"


def evaluate_file(repo: Repo, path: str, kind: str, reviews_out: list, packets: list, lineages: dict) -> dict:
    obs = repo.observations(path)
    entry = {"path": path, "kind": kind, "revisions": [], "history": "complete", "status": "ok", "reason": ""}
    if not obs:
        entry.update(status="missing", reason="registered source not found at any observed revision")
        return entry
    hist = repo.git.history(repo.refs(), path, repo.spec["history_limit"])
    entry["history"] = _history_state(repo, hist)
    for o in obs:
        o["parsed"] = parse_source(o["data"], kind)
    versions = [(i, source, parse_source(data, kind), commit) for i, source, data, commit in _versions(repo, path, obs, hist)]
    known = {v[2]["revision_id"] for v in versions if v[2]["revision_id"]}
    known |= {o["parsed"]["revision_id"] for o in obs if o["parsed"]["revision_id"]}
    whole_to_rev = {v[2]["whole"]: v[2]["revision_id"] for v in versions if v[2]["revision_id"]}
    for o in obs:
        if o["parsed"]["revision_id"]:
            whole_to_rev.setdefault(o["parsed"]["whole"], o["parsed"]["revision_id"])
    lineages[path] = {"known": known, "whole": whole_to_rev}
    order_ids = []
    for _, _, parsed, _ in sorted(versions, key=lambda v: v[0]):
        rid = parsed["revision_id"]
        if rid and parsed["execution"] in ELIGIBLE and (not order_ids or order_ids[-1] != rid):
            order_ids.append(rid)
    for _, source, parsed, commit in versions:
        if parsed.get("review"):
            # A page Review's target is always its own page; binding is decided later against `known`.
            reviews_out.append({"source": source, "commit": commit, "target": path, "review": parsed["review"]})
    distinct = []
    for o in obs:
        p = o["parsed"]
        if p["status"] != "ok":
            entry["revisions"].append({"label": o["label"], "commit": o["commit"], "status": p["status"],
                                       "reason": p["reason"], "whole_sha256": p["whole"]})
            continue
        rid = p["revision_id"]
        prev = None
        if rid in order_ids and order_ids.index(rid) > 0:
            prev = order_ids[order_ids.index(rid) - 1]
        elif rid not in order_ids and order_ids:
            prev = order_ids[-1]
        rev = {"label": o["label"], "commit": o["commit"], "status": "ok", "revision_id": rid,
               "whole_sha256": p["whole"], "execution": p["execution"],
               "eligible": p["execution"] in ELIGIBLE, "supersedes": prev}
        entry["revisions"].append(rev)
        if rid not in distinct:
            distinct.append(rid)
    entry["divergent"] = len(distinct) > 1
    if any(r["status"] == "unsupported" for r in entry["revisions"]):
        entry["status"] = "unsupported"
        entry["reason"] = next(r["reason"] for r in entry["revisions"] if r["status"] == "unsupported")
    for r in entry["revisions"]:
        if r["status"] == "ok":
            where = f"{path}@{r['commit']}" if r["commit"] else f"{path}@worktree"
            packets.append(f"{where}#{r['revision_id']}")
    return entry


def evaluate_review_source(repo: Repo, path: str, lane: str, reviews_out: list) -> dict:
    """A review source names its target with `reviewed_return_path:`. It is never inferred (PSI-01)."""
    obs = repo.observations(path)
    entry = {"path": path, "kind": "review-source", "status": "ok", "history": "complete"}
    if not obs:
        entry.update(status="missing")
        return entry
    hist = repo.git.history(repo.refs(), path, repo.spec["history_limit"])
    entry["history"] = _history_state(repo, hist)
    for _, source, data, commit in _versions(repo, path, obs, hist):
        try:
            lines = data.decode("utf-8").split("\n")
        except UnicodeDecodeError:
            entry.update(status="unsupported")
            continue
        review = parse_review_lines([line.rstrip("\r") for line in lines])
        if review["findings"] or review["prefix"] or review["legacy_whole"] or review["target"]:
            reviews_out.append({"source": source, "commit": commit, "target": review["target"], "review": review})
    return entry


def resolve_binding(item: dict, lineages: dict, lane_paths: set) -> tuple[str, str | None]:
    """VALID only when the named revision is a known revision of the declared target (PSI-01)."""
    r = item["review"]
    has_claim = bool(r["prefix"] or r["legacy_whole"] or r["findings"])
    if item["target"] not in lane_paths:
        return ("invalid-target", None) if has_claim else ("unbound", None)
    lineage = lineages.get(item["target"], {"known": set(), "whole": {}})
    if r["prefix"]:
        return ("valid", r["prefix"]) if r["prefix"] in lineage["known"] else ("unknown-hash", None)
    if r["legacy_whole"]:
        rid = lineage["whole"].get(r["legacy_whole"])
        return ("valid", rid) if rid else ("invalid-legacy", None)
    return "unbound", None


def causal_frontier(repo: Repo, records: list[dict]) -> list[dict]:
    """Records whose commit is not an ancestor of another record's commit. Ancestry only; no dates (PSI-02)."""
    commits = {r["commit"] for r in records}
    keep, seen = [], set()
    for r in records:
        if any(repo.is_ancestor(r["commit"], c) for c in commits if c != r["commit"]):
            continue
        key = (r["commit"], r["resolution"], r["source"])
        if key not in seen:
            seen.add(key)
            keep.append(r)
    return keep


def classify(resolution: str) -> str:
    return "open" if resolution in OPEN else "closed" if resolution in CLOSED else "unrecognized"


def lane_findings(repo: Repo, valid: list[dict]) -> dict:
    """Finding identity is (target path, ID) (PSI-01). Committed state comes from the causal frontier.
    Uncommitted drafts are reported beside it and never replace it (PSI-02)."""
    by_key: dict[tuple, list] = {}
    for item in valid:
        for ident, resolution in item["review"]["findings"]:
            by_key.setdefault((item["target"], ident), []).append(
                {"commit": item["commit"], "resolution": resolution, "source": item["source"], "binds": item["binds"]})
    out = {}
    for (target, ident), recs in sorted(by_key.items()):
        committed = [r for r in recs if r["commit"]]
        drafts = sorted({r["resolution"] for r in recs if not r["commit"]})
        front = causal_frontier(repo, committed)
        resolutions = sorted({r["resolution"] for r in front})
        if committed and len(resolutions) == 1:
            resolution, state = resolutions[0], classify(resolutions[0])
        elif committed:
            resolution, state = " | ".join(resolutions), "conflict"
        else:
            resolution, state = " | ".join(drafts), "draft-only"
        out[f"{target}#{ident}"] = {
            "id": ident, "target": target, "resolution": resolution, "state": state,
            "passes": len({r["binds"] for r in committed}),
            "source": ", ".join(sorted({r["source"] for r in front})) if committed else DRAFT,
            "frontier": [{"resolution": r["resolution"], "source": r["source"]} for r in front],
            "draft": " | ".join(drafts) if drafts else None}
    return out


def parse_assignment(data: bytes) -> dict | None:
    fields = {}
    for line in data.decode("utf-8", "replace").splitlines():
        if ": " not in line:
            return None
        key, value = line.split(": ", 1)
        if key in fields:
            return None
        fields[key] = value
    return fields if set(fields) == ASSIGNMENT_KEYS and all(fields.values()) else None


# ---------- intake store ----------

def _inside_git(path: Path) -> bool:
    current = path
    while not current.exists() and current.parent != current:
        current = current.parent
    for ancestor in [current, *current.resolve().parents]:
        if (ancestor / ".git").exists():
            return True
    return False


def store_path(text: str) -> Path:
    path = Path(text)
    if not path.is_absolute():
        refuse("intake store must be an absolute path")
    if _inside_git(path):
        refuse("intake store resolves inside a Git working tree")
    return path


def subject_id(subject: dict) -> str:
    return sha256(canonical(subject))


def load_store(store: Path) -> tuple[dict, list[str]]:
    records, bad = {}, []
    root = store / "subjects"
    if not root.exists():
        return records, bad
    for d in sorted(os.listdir(root)):
        rec_path = root / d / "0001.seen.json"
        extra = sorted(set(os.listdir(root / d)) - {"0001.seen.json"}) if (root / d).is_dir() else ["not a directory"]
        try:
            rec = loads_strict(rec_path.read_bytes().decode("utf-8"), f"intake {d}")
            schema = rec.get("schema") if isinstance(rec, dict) else None
            subject_keys, observed_keys = ((SUBJECT_KEYS, OBSERVED_KEYS) if schema == INTAKE_SCHEMA else
                                           (CLERK_SUBJECT_KEYS, CLERK_OBSERVED_KEYS) if schema == INTAKE_SCHEMA_2 else
                                           (None, None))
            ok = (isinstance(rec, dict) and set(rec) == RECORD_KEYS and subject_keys is not None
                  and isinstance(rec["subject"], dict) and set(rec["subject"]) == subject_keys
                  and (schema == INTAKE_SCHEMA or rec["subject"].get("kind") == "clerk-return")
                  and isinstance(rec["observed"], dict) and set(rec["observed"]) == observed_keys
                  and isinstance(rec["subject_id"], str) and HEX64.fullmatch(rec["subject_id"])
                  and subject_id(rec["subject"]) == rec["subject_id"] and rec["subject_id"][:12] == d
                  and not extra)
        except (Refusal, OSError, UnicodeDecodeError) as exc:
            bad.append(f"bad intake record {d}: {exc}")
            continue
        if not ok:
            bad.append(f"bad intake record {d}: inconsistent identity or schema")
            continue
        records[rec["subject_id"]] = rec
    return records, bad


# ---------- registered Clerk returns (05.04) ----------

def clerk_observations(reg: dict, lane: dict, records: dict, store_text: str | None, report: dict) -> list[dict]:
    """One inspection/2 observation per registered job. Scope: registered jobs only, never an inbox scan."""
    out = []
    for job in lane.get("clerk_jobs", []):
        obs = clerk_adapter.inspect(reg["clerk_tool"], job)
        where = f"lane {lane['lane']}: clerk {job['job_id']} in {job['store']}"
        subject = clerk_adapter.subject_for(obs)
        obs["intake"] = None
        if obs["status"] != "ok":
            report["attention"].append(("unsupported", f"{where}: {obs['reason']}"))
        elif obs["binding"].startswith("mismatch"):
            report["attention"].append(("conflict", f"{where}: registration binding {obs['binding']}; unusable"))
        elif obs["state"] in ("unknown",):
            report["attention"].append(("missing", f"{where}: state unknown: "
                                        + "; ".join(p["detail"] for p in obs["problems"])))
        elif obs["state"] in ("incomplete", "corrupt"):
            report["attention"].append(("clerk-not-clean", f"{where}: state {obs['state']}: "
                                        + "; ".join(p["detail"] for p in obs["problems"])))
        if subject:
            obs["subject_id"] = subject_id(subject)
            obs["intake"] = ("seen" if obs["subject_id"] in records else "unseen") if store_text else "not checked"
            if obs["intake"] == "seen":
                report["attention"].append(("review-needed", f"{where}: event {obs['event_sha256']} seen; review not machine-readable"))
            else:
                report["attention"].append(("unseen", f"{where}: event {obs['event_sha256']}"))
        if obs["status"] == "ok" and obs["state"] == "returned" and not obs["clean"] and not obs["binding"].startswith("mismatch"):
            # Kept after acknowledgement: a seen record never hides a troubled return.
            report["attention"].append(("clerk-not-clean", f"{where}: event {obs['event_sha256']} not clean: checks "
                                        + json.dumps(obs["checks"], sort_keys=True) + " problems "
                                        + json.dumps(obs["problems"], sort_keys=True)))
        out.append(obs)
    return out


# ---------- status ----------

def collect(reg: dict, store_text: str | None) -> dict:
    repos = {name: Repo(name, spec) for name, spec in reg["repositories"].items()}
    records, bad = ({}, [])
    if store_text:
        store = store_path(store_text)
        records, bad = load_store(store)
    report = {"scope": "only registered sources are read; no fetch; remote refs are last observed",
              "repositories": {}, "lanes": [], "conflicts": [], "attention": [], "intake_problems": bad}
    for name, repo in repos.items():
        report["repositories"][name] = {"head": repo.head, "remote_ref": repo.spec["remote_ref"], "remote": repo.remote,
                                        "relation": repo.relation, "shallow": repo.shallow, "problem": repo.problem,
                                        "worktree": repo.spec["worktree"]}
        if repo.problem:
            report["attention"].append(("missing", f"repository {name}: {repo.problem}"))
    lane_files: dict[str, dict] = {}
    for lane in reg["lanes"]:
        repo = repos[lane["repository"]]
        out = {"lane": lane["lane"], "project": lane["project"], "owner_label": lane["owner_label"],
               "repository": repo.name, "files": [], "review_sources": [], "findings": {}, "packets": [],
               "dirty": []}
        report["lanes"].append(out)
        out["clerk"] = clerk_observations(reg, lane, records, store_text, report)
        if repo.problem:
            continue
        reviews: list = []
        lineages: dict = {}
        paths = []
        for folder in lane["pages"]:
            names = set()
            for commit in repo.refs():
                names.update(n for n in repo.git.names(commit, folder) if PAGE_FILE.fullmatch(n))
            disk = Path(repo.spec["local"]) / folder
            if repo.worktree and disk.is_dir():
                names.update(n for n in os.listdir(disk) if PAGE_FILE.fullmatch(n) and (disk / n).is_file())
            if not names:
                out["files"].append({"path": folder, "kind": "page-folder", "status": "missing", "revisions": []})
                report["attention"].append(("missing", f"lane {lane['lane']}: page folder {folder} not found"))
            for name in sorted(names):
                paths.append((f"{folder}/{name}", "page-return"))
        paths += [(p, "return-file") for p in lane["return_files"]]
        for path, kind in paths:
            entry = evaluate_file(repo, path, kind, reviews, out["packets"], lineages)
            out["files"].append(entry)
            lane_files[f"{lane['lane']}:{path}"] = entry
        for path in lane["review_sources"]:
            out["review_sources"].append(evaluate_review_source(repo, path, lane["lane"], reviews))
        if repo.worktree:
            out["dirty"] = repo.git.dirty([*lane["pages"], *lane["return_files"], *lane["review_sources"]])
        lane_paths = {p for p, _ in paths}
        for item in reviews:
            item["status"], item["binds"] = resolve_binding(item, lineages, lane_paths)
            if item["status"] not in ("valid", "unbound") or (
                    item["status"] == "unbound" and (item["review"]["findings"] or item["review"]["disposition"])):
                claimed = item["review"]["prefix"] or item["review"]["legacy_whole"]
                text = "; ".join(f"{i}={r}" for i, r in item["review"]["findings"]) or "no findings"
                report["attention"].append((
                    "invalid-review",
                    f"lane {lane['lane']}: {item['source']}: {item['status']} review"
                    f"{' naming ' + claimed if claimed else ''}{' for ' + str(item['target']) if item['target'] else ''}"
                    f" changes no finding and counts no pass; its text is kept: {text}"))
        valid = [i for i in reviews if i["status"] == "valid"]
        for entry in out["files"]:
            if entry.get("status") == "missing":
                report["attention"].append(("missing", f"lane {lane['lane']}: {entry['path']} missing"))
                continue
            if entry.get("status") == "unsupported":
                report["attention"].append(("unsupported", f"lane {lane['lane']}: {entry['path']}: {entry['reason']}"))
            has_rev = any(r.get("status") == "ok" for r in entry["revisions"])
            if has_rev and entry["history"] != "complete":
                report["attention"].append(("history-unknown",
                                            f"lane {lane['lane']}: {entry['path']}: history {entry['history']}; findings may be missing"))
            for rev in entry["revisions"]:
                if rev.get("status") != "ok":
                    continue
                bound = [b for b in valid if b["target"] == entry["path"] and b["binds"] == rev["revision_id"]]
                committed = [b for b in bound if b["commit"]]
                if committed:
                    front = causal_frontier(repo, [dict(b, resolution=b["review"]["disposition"]) for b in committed])
                    rev["review"] = "reviewed"
                    rev["review_source"] = ", ".join(sorted({b["source"] for b in front}))
                    dispositions = sorted({b["resolution"] for b in front if b["resolution"]})
                    if len(dispositions) == 1:
                        rev["disposition"] = dispositions[0]
                    elif dispositions:
                        rev["disposition"] = " | ".join(dispositions)
                        report["attention"].append(("conflict", f"lane {lane['lane']}: {entry['path']}: incomparable review dispositions {dispositions}"))
                elif bound:
                    rev["review"] = "reviewed-in-uncommitted-draft"
                    rev["review_source"] = bound[0]["source"]
                elif any(b["target"] == entry["path"] for b in valid):
                    rev["review"] = "stale-review"
                else:
                    rev["review"] = "review-needed"
                unbound = [b for b in reviews if b["target"] == entry["path"] and b["status"] != "valid"]
                if unbound:
                    rev["unbound_reviews"] = [b["source"] for b in unbound]
                rev["intake"] = None
                if rev["eligible"]:
                    sid = subject_id({"kind": entry["kind"], "repository": repo.name, "path": entry["path"],
                                      "revision_id": rev["revision_id"]})
                    rev["subject_id"] = sid
                    rev["intake"] = ("seen" if sid in records else "unseen") if store_text else "not checked"
                    if rev["review"] != "reviewed":
                        kind = "review-needed" if rev["intake"] == "seen" else "unseen" if rev["intake"] == "unseen" else "review-needed"
                        report["attention"].append((kind, f"lane {lane['lane']}: {entry['path']} {rev['label']} #{rev['revision_id']}"))
        out["findings"] = lane_findings(repo, valid)
        for key, f in out["findings"].items():
            if f["state"] == "conflict":
                report["attention"].append(("conflict", f"lane {lane['lane']}: {key}: incomparable resolutions "
                                            + "; ".join(f"{r['resolution']} at {r['source']}" for r in f["frontier"])))
            elif f["state"] != "closed":
                report["attention"].append(("open-finding", f"lane {lane['lane']}: {key}={f['resolution']} ({f['state']}, passes {f['passes']})"))
            if f["draft"] is not None and f["state"] != "draft-only" and f["draft"] != f["resolution"]:
                report["attention"].append(("conflict", f"lane {lane['lane']}: {key}: draft differs from committed: "
                                            f"committed {f['resolution']}, uncommitted draft {f['draft']}"))
        for item in reviews:
            for b in item["review"]["bad"]:
                report["attention"].append(("unsupported", f"lane {lane['lane']}: unreadable finding item {b!r} in {item['source']}"))
    for b in bad:
        report["attention"].append(("bad-intake", b))
    canon = reg.get("canonical_assignment")
    if canon:
        repo = repos[canon["repository"]]
        data = None
        if not repo.problem:
            obs = repo.observations(canon["path"])
            data = obs[-1]["data"] if obs else None
        fields = parse_assignment(data) if data is not None else None
        report["canonical"] = {"path": canon["path"], "lane": canon["lane"], "fields": fields,
                               "sha256": sha256(data) if data is not None else None}
        if fields is None:
            report["conflicts"].append(f"canonical record {canon['path']} is missing or not a v1 assignment record")
        else:
            state, work = fields["assignment_state"], fields["current_work"]
            lane = next(l for l in report["lanes"] if l["lane"] == canon["lane"])
            entry = lane_files.get(f"{canon['lane']}:{work}")
            lane_spec = next(l for l in reg["lanes"] if l["lane"] == canon["lane"])
            inside = any(work.startswith(folder + "/") for folder in lane_spec["pages"]) or work in lane_spec["return_files"]
            if entry is None and inside:
                report["conflicts"].append(f"canonical current_work {work} is inside lane {canon['lane']}'s registered pages but not present at any observed revision")
            elif entry is None:
                report["conflicts"].append(f"canonical current_work {work} is not inside lane {canon['lane']}'s registered pages")
            else:
                for rev in entry["revisions"]:
                    ex = rev.get("execution")
                    if state in ("waiting", "released") and ex in ELIGIBLE:
                        report["conflicts"].append(f"canonical says {state} for {work}; {rev['label']} page shows a return (execution {ex})")
                    if state == "returned" and ex not in ELIGIBLE:
                        report["conflicts"].append(f"canonical says returned for {work}; {rev['label']} page execution is {ex or rev.get('status')}")
            if state == "waiting" and lane["dirty"]:
                report["conflicts"].append(f"canonical says waiting; uncommitted changes on lane {canon['lane']} paths: {len(lane['dirty'])}")
    for c in report["conflicts"]:
        report["attention"].insert(0, ("conflict", c))
    order = reg["attention_order"]
    report["attention"].sort(key=lambda a: order.index(a[0]))
    return report


def grouped(revisions: list[dict]) -> list[tuple[str, str, dict]]:
    """One row per distinct revision: labels joined (published=local=worktree), commits listed."""
    rows: dict[tuple, list] = {}
    for rev in revisions:
        key = (rev.get("status"), rev.get("revision_id") or rev.get("whole_sha256"), rev.get("intake"), rev.get("review"))
        rows.setdefault(key, []).append(rev)
    out = []
    for revs in rows.values():
        labels = "=".join(r["label"] for r in revs)
        where = ",".join(dict.fromkeys(r["commit"][:12] if r["commit"] else "worktree" for r in revs))
        out.append((labels, where, revs[0]))
    return out


def render(report: dict, reg_sha: str) -> str:
    lines = [f"prime-support status  registry sha256 {reg_sha}", f"scope: {report['scope']}"]
    for name, r in report["repositories"].items():
        if r["problem"]:
            lines.append(f"repo {name}: MISSING ({r['problem']})")
            continue
        lines.append(f"repo {name}: HEAD {r['head'] or 'none'}  {r['remote_ref']} {r['remote'] or 'absent'} "
                     f"(last observed, not fetched)  {r['relation']}{'  SHALLOW' if r['shallow'] else ''}  worktree {r['worktree']}")
    if "canonical" in report:
        c = report["canonical"]
        f = c["fields"] or {}
        lines.append(f"canonical {c['path']} sha256 {c['sha256']}  lane {c['lane']}  "
                     f"current_work {f.get('current_work', '?')}  state {f.get('assignment_state', '?')}")
    for lane in report["lanes"]:
        lines.append(f"lane {lane['lane']}  ({lane['owner_label']}; {lane['project']})")
        for entry in lane["files"]:
            if entry.get("status") == "missing":
                lines.append(f"  {entry['path']}: MISSING")
                continue
            lines.append(f"  {entry['path']}  [{entry['kind']}]  history {entry['history']}"
                         f"{'  DIVERGENT' if entry.get('divergent') else ''}")
            for labels, where, rev in grouped(entry["revisions"]):
                if rev.get("status") != "ok":
                    lines.append(f"    {labels}  {where}  {rev['status'].upper()}: {rev['reason']}")
                    continue
                extra = f"  disposition {rev['disposition']!r} ({rev['review_source']})" if rev.get("disposition") else ""
                lines.append(f"    {labels}  {where}  revision {rev['revision_id']}  execution {rev['execution']}"
                             f"  review {rev['review']}  intake {rev['intake'] or 'not eligible'}"
                             f"{'  supersedes ' + rev['supersedes'][:12] if rev['supersedes'] else ''}{extra}")
        for src in lane["review_sources"]:
            lines.append(f"  review source {src['path']}: {src['status']}  history {src['history']}")
        for obs in lane.get("clerk", []):
            head = f"  clerk {obs['job_id']}  store {obs['store']}  [registered job; show --json, tool {obs['tool_sha256'][:12]}]"
            if obs["status"] != "ok":
                lines.append(f"{head}  UNSUPPORTED: {obs['reason']}")
                continue
            lines.append(f"{head}  exit {obs['exit']}  state {obs['state']}  binding {obs['binding']}")
            lines.append(f"    checks {json.dumps(obs['checks'], sort_keys=True)}  problems {len(obs['problems'])}"
                         f"  event {obs['event_sha256'] or 'none'}  clean {'yes' if obs['clean'] else 'no'}"
                         f"  intake {obs['intake'] or 'not eligible'}  review {obs['review']}")
            for p in obs["problems"]:
                lines.append(f"    problem {p['kind']}: {p['detail']}")
        if lane["findings"]:
            lines.append("  findings: " + "; ".join(
                f"{v['id']} [{v['target']}]={v['resolution']} ({v['state']}, passes {v['passes']}"
                f"{', draft ' + v['draft'] if v['draft'] else ''})" for _, v in sorted(lane["findings"].items())))
        else:
            lines.append("  findings: none recorded in machine-readable form")
        if lane["dirty"]:
            lines.append(f"  uncommitted on registered paths: {len(lane['dirty'])}")
    for c in report["conflicts"]:
        lines.append(f"CONFLICT {c}")
    for b in report["intake_problems"]:
        lines.append(f"INTAKE {b}")
    if report["attention"]:
        kind, text = report["attention"][0]
        lines.append(f"attention ({kind}; recommendation, not authority): {text}")
        packet = next((l["packets"] + [o["packet"] for o in l.get("clerk", []) if o.get("packet") and o["job_id"] in text]
                       for l in report["lanes"] if f"lane {l['lane']}:" in text), [])
        if packet:
            lines.append("packet: " + ", ".join(dict.fromkeys(packet)))
        lines.append(f"attention items: {len(report['attention'])}")
    else:
        lines.append("attention: none")
    return "\n".join(lines) + "\n"


def _json_ready(report: dict) -> dict:
    out = json.loads(json.dumps(report, default=list))
    out["attention"] = [{"kind": k, "item": t} for k, t in report["attention"]]
    return out


# ---------- commands ----------

def cmd_status(args) -> int:
    reg, reg_sha = load_registry(args.registry)
    report = collect(reg, args.intake)
    if args.json:
        sys.stdout.write(json.dumps({"registry_sha256": reg_sha, **_json_ready(report)}, indent=1, sort_keys=True) + "\n")
    else:
        sys.stdout.write(render(report, reg_sha))
    return 1 if report["attention"] else 0


def cmd_scan(args) -> int:
    reg, reg_sha = load_registry(args.registry)
    report = collect(reg, args.intake)
    rows = []
    for lane in report["lanes"]:
        for entry in lane["files"]:
            for labels, _where, rev in grouped(entry.get("revisions", [])):
                if rev.get("status") != "ok":
                    rows.append(f"{lane['lane']} {entry['path']} {labels} {rev['status']}: {rev['reason']}")
                    continue
                state = rev["intake"] if rev["eligible"] else f"not eligible (execution {rev['execution']})"
                rows.append(f"{lane['lane']} {entry['path']} {labels} revision {rev['revision_id']} "
                            f"{state} review {rev['review']}"
                            f"{' supersedes ' + rev['supersedes'] if rev['supersedes'] else ''}")
        for obs in lane.get("clerk", []):
            if obs["status"] != "ok":
                rows.append(f"{lane['lane']} clerk {obs['job_id']} unsupported: {obs['reason']}")
            elif obs["event_sha256"] and obs["identity"]:
                rows.append(f"{lane['lane']} clerk {obs['job_id']} event {obs['event_sha256']} {obs['intake']} "
                            f"clean {'yes' if obs['clean'] else 'no'} review {obs['review']}")
            else:
                rows.append(f"{lane['lane']} clerk {obs['job_id']} not eligible (state {obs['state']}, binding {obs['binding']})")
    if args.json:
        sys.stdout.write(json.dumps({"registry_sha256": reg_sha, "rows": rows}, indent=1) + "\n")
    else:
        sys.stdout.write("intake scan (read-only)\n" + "\n".join(rows) + "\n")
    pending = any(" unseen " in r for r in rows) or report["intake_problems"]
    return 1 if pending else 0


def cmd_ack(args) -> int:
    reg, _ = load_registry(args.registry)
    if not HEX64.fullmatch(args.revision or ""):
        refuse("--revision must be the full 64-hex revision id")
    if not LABEL.fullmatch(args.actor):
        refuse("--as must be a plain label")
    store = store_path(args.intake)
    lane = next((l for l in reg["lanes"] if l["lane"] == args.lane), None)
    if lane is None:
        refuse("unknown lane")
    report = collect(reg, args.intake)
    if report["intake_problems"]:
        refuse("intake store has bad records; nothing written")
    lane_out = next(l for l in report["lanes"] if l["lane"] == args.lane)
    entry = next((e for e in lane_out["files"] if e["path"] == args.path), None)
    if entry is None:
        refuse("path is not a registered return in that lane")
    rev = next((r for r in entry.get("revisions", []) if r.get("revision_id") == args.revision), None)
    if rev is None:
        refuse("revision is not currently observed for that path")
    if not rev["eligible"]:
        refuse(f"revision is not intake-eligible (execution {rev['execution']})")
    subject = {"kind": entry["kind"], "repository": lane["repository"], "path": args.path, "revision_id": args.revision}
    sid = subject_id(subject)
    directory = store / "subjects" / sid[:12]
    target = directory / "0001.seen.json"
    if target.exists():
        existing = loads_strict(target.read_bytes().decode("utf-8"), "intake")
        if existing.get("subject_id") != sid:
            refuse("abbreviated id collision: a different subject already holds " + sid[:12])
        if existing.get("by") != args.actor:
            refuse("conflicting acknowledgement: this subject was acknowledged by another label")
        sys.stdout.write(f"already-recorded {sid}\n")
        return 0
    record = {"schema": INTAKE_SCHEMA, "subject_id": sid, "subject": subject,
              "observed": {"source": rev["label"], "commit": rev["commit"], "whole_sha256": rev["whole_sha256"],
                           "execution": rev["execution"]},
              "supersedes": rev["supersedes"], "by": args.actor,
              "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "note": NOTE}
    directory.mkdir(parents=True, exist_ok=True)
    with open(target, "xb") as handle:
        handle.write(canonical(record))
    sys.stdout.write(f"seen {sid}\n{NOTE}\n")
    return 0


def cmd_ack_clerk(args) -> int:
    """Freshly inspect one registered Clerk job and record that its exact returned event was seen."""
    reg, _ = load_registry(args.registry)
    if not HEX64.fullmatch(args.event_sha256 or ""):
        refuse("--event-sha256 must be the full 64-hex returned.event_sha256")
    if not LABEL.fullmatch(args.actor):
        refuse("--as must be a plain label")
    store = store_path(args.intake)
    lane = next((l for l in reg["lanes"] if l["lane"] == args.lane), None)
    if lane is None:
        refuse("unknown lane")
    wanted = clerk_adapter.canonical_store(args.store)
    job = next((j for j in lane["clerk_jobs"]
                if clerk_adapter.canonical_store(j["store"]) == wanted and j["job_id"] == args.job), None)
    if job is None:
        refuse("store and job are not a registered Clerk job in that lane")
    resolved = Path(os.path.realpath(store))
    for other in (j for l in reg["lanes"] for j in l["clerk_jobs"]):
        clerk_root = Path(os.path.realpath(other["store"]))
        if resolved == clerk_root or clerk_root in resolved.parents:
            refuse("intake store resolves inside a registered Clerk store")
    records, bad = load_store(store)
    if bad:
        refuse("intake store has bad records; nothing written")
    obs = clerk_adapter.inspect(reg["clerk_tool"], job)
    if obs["status"] != "ok":
        refuse("inspection failed: " + obs["reason"])
    if obs["binding"].startswith("mismatch"):
        refuse("registration binding " + obs["binding"])
    subject = clerk_adapter.subject_for(obs)
    if subject is None:
        refuse(f"no returned-event identity (state {obs['state']}, checks {json.dumps(obs['checks'], sort_keys=True)})")
    if subject["event_sha256"] != args.event_sha256:
        refuse(f"stale event: the job now projects event {subject['event_sha256']}")
    sid = subject_id(subject)
    directory = store / "subjects" / sid[:12]
    target = directory / "0001.seen.json"
    if target.exists():
        existing = loads_strict(target.read_bytes().decode("utf-8"), "intake")
        if existing.get("subject_id") != sid:
            refuse("abbreviated id collision: a different subject already holds " + sid[:12])
        if existing.get("by") != args.actor:
            refuse("conflicting acknowledgement: this subject was acknowledged by another label")
        sys.stdout.write(f"already-recorded {sid}\n")
        return 0
    record = {"schema": INTAKE_SCHEMA_2, "subject_id": sid, "subject": subject,
              "observed": {"tool_sha256": obs["tool_sha256"], "exit": obs["exit"], "state": obs["state"],
                           "checks": obs["checks"], "problems": obs["problems"]},
              "supersedes": None, "by": args.actor,
              "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "note": NOTE}
    directory.mkdir(parents=True, exist_ok=True)
    with open(target, "xb") as handle:
        handle.write(canonical(record))
    sys.stdout.write(f"seen {sid}\nclean {'yes' if obs['clean'] else 'no'}\n{NOTE}\n")
    return 0


def cmd_show(args) -> int:
    store = store_path(args.intake)
    records, bad = load_store(store)
    if args.json:
        sys.stdout.write(json.dumps({"records": list(records.values()), "problems": bad}, indent=1, sort_keys=True) + "\n")
    else:
        lines = [f"intake store {store}  records {len(records)}"]
        for sid, rec in sorted(records.items()):
            s = rec["subject"]
            if s.get("kind") == "clerk-return":
                lines.append(f"{sid}  clerk {s['store']}#{s['job_id']}  event {s['event_sha256']}  by {rec['by']}  at {rec['at']}")
            else:
                lines.append(f"{sid}  {s['repository']}:{s['path']}  revision {s['revision_id']}  by {rec['by']}  at {rec['at']}")
        lines.extend(bad)
        sys.stdout.write("\n".join(lines) + "\n")
    return 1 if bad else 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(prog="prime_support.py")
    sub = parser.add_subparsers(dest="command", required=True)
    st = sub.add_parser("status")
    st.add_argument("--registry", required=True)
    st.add_argument("--intake")
    st.add_argument("--json", action="store_true")
    intake = sub.add_parser("intake")
    isub = intake.add_subparsers(dest="action", required=True)
    sc = isub.add_parser("scan")
    sc.add_argument("--registry", required=True)
    sc.add_argument("--intake")
    sc.add_argument("--json", action="store_true")
    ak = isub.add_parser("ack")
    ak.add_argument("--registry", required=True)
    ak.add_argument("--intake", required=True)
    ak.add_argument("--lane", required=True)
    ak.add_argument("--path", required=True)
    ak.add_argument("--revision", required=True)
    ak.add_argument("--as", dest="actor", required=True)
    ac = isub.add_parser("ack-clerk")
    ac.add_argument("--registry", required=True)
    ac.add_argument("--intake", required=True)
    ac.add_argument("--lane", required=True)
    ac.add_argument("--store", required=True)
    ac.add_argument("--job", required=True)
    ac.add_argument("--event-sha256", dest="event_sha256", required=True)
    ac.add_argument("--as", dest="actor", required=True)
    sh = isub.add_parser("show")
    sh.add_argument("--intake", required=True)
    sh.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "status":
            return cmd_status(args)
        if args.action == "scan":
            return cmd_scan(args)
        if args.action == "ack":
            return cmd_ack(args)
        if args.action == "ack-clerk":
            return cmd_ack_clerk(args)
        return cmd_show(args)
    except Refusal as exc:
        sys.stdout.write(f"refused: {exc}\n")
        return 2
    except OSError as exc:
        sys.stdout.write(f"refused: filesystem error: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
