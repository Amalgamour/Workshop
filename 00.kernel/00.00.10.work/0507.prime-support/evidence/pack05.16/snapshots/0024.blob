"""Registered Clerk returns for Prime intake (0507.prime-support/05.04). Fixture lab, standard library only.

Reads one registered Clerk job through the accepted inspection/2 projection only:
  <python> -I -B <clerk.py> show --store S --job ID --instructions-base BASE --json
The code is pinned by ACCEPTED_CLERK_SHA256 and re-hashed immediately before each run. The adapter never opens or
lists a Clerk store, never parses human output, and never queues, claims, returns or repairs.
Contract: 00.kernel/00.00.10.work/0507.prime-support/evidence/build05.04/DESIGN.004.md.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ACCEPTED_CLERK_SHA256 = "f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c"
INSPECTION_SCHEMA = "clerk-handoff-inspection/2"
TOP_KEYS = {"schema", "job_id", "state", "job", "claim", "returned", "checks", "problems"}
RETURNED_KEYS = {"by", "delivery", "evidence", "artifacts", "event_sha256"}
# Shapes as the pinned Clerk (ACCEPTED_CLERK_SHA256) emits them; not a new producer schema (05.05, CA-01).
JOB_KEYS = {"assignee", "expected_outputs", "instructions", "job_id", "release", "reviewer", "routed_by"}
CLAIM_KEYS = {"by", "token"}
ARTIFACT_KEYS = {"bytes", "path", "sha256"}
STATES = {"queued", "claimed", "returned", "incomplete", "corrupt", "unknown"}
CHECK_ENUMS = {
    "events": {"ok", "unreadable", "broken", "not-applicable"},
    "completion": {"ok", "partial", "missing-event", "missing-witness", "mismatch", "not-applicable"},
    "artifacts": {"ok", "changed", "not-applicable"},
    "instructions": {"usable", "unusable", "not-checked", "not-applicable"},
}
FINDING_KINDS = {"artifact-changed", "instructions-unusable"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
CLERK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
TIMEOUT_S = 60


class ProjectionError(Exception):
    pass


def canonical_store(path: str) -> str:
    return os.path.normcase(os.path.realpath(path))


def tool_problem(path: str, declared: str) -> str | None:
    """None when the file at path is a plain file whose bytes are the accepted inspection/2 code."""
    if declared != ACCEPTED_CLERK_SHA256:
        return "registered clerk_tool.sha256 is not the accepted inspection/2 code"
    try:
        st = os.lstat(path)
    except OSError:
        return "clerk tool is missing"
    attrs = getattr(st, "st_file_attributes", 0) or 0
    if stat.S_ISLNK(st.st_mode) or attrs & 0x400 or not stat.S_ISREG(st.st_mode):
        return "clerk tool is not a plain file"
    with open(path, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    if digest != ACCEPTED_CLERK_SHA256:
        return f"clerk tool bytes are not the accepted inspection/2 code (sha256 {digest})"
    return None


def argv_for(tool: str, job: dict) -> list[str]:
    return [sys.executable, "-I", "-B", tool, "show", "--store", job["store"], "--job", job["job_id"],
            "--instructions-base", job["instructions_base"], "--json"]


def run_show(argv: list[str]) -> tuple[int, str, str]:
    """The one process the adapter launches. Replaced only by tests, never by a caller."""
    env = {k: v for k, v in os.environ.items() if k.upper() in ("SYSTEMROOT", "PATH", "TEMP", "TMP", "COMSPEC")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          cwd=tempfile.gettempdir(), env=env, timeout=TIMEOUT_S)
    return proc.returncode, proc.stdout, proc.stderr


def _strict(text: str):
    def pairs(seq):
        out = {}
        for key, value in seq:
            if key in out:
                raise ProjectionError(f"duplicate key {key}")
            out[key] = value
        return out

    def constant(name):
        raise ProjectionError(f"nonfinite number {name}")

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except json.JSONDecodeError as exc:
        raise ProjectionError(f"invalid JSON ({exc.msg})") from None


def _string(value, label: str) -> str:
    """Type before membership: a list or dict is unhashable, so a set test on it would raise TypeError (CA-01)."""
    if not isinstance(value, str):
        raise ProjectionError(f"{label} is not a string ({type(value).__name__})")
    return value


def _object(value, keys: set, label: str) -> dict:
    if not isinstance(value, dict) or set(value) != keys:
        raise ProjectionError(f"{label} is not the inspection/2 object")
    return value


def _check_shapes(doc: dict) -> None:
    """The fields this adapter reads, typed as the pinned Clerk emits them."""
    if isinstance(doc["job"], dict):
        job = _object(doc["job"], JOB_KEYS, "job")
        for key in ("job_id", "reviewer", "assignee"):
            _string(job[key], f"job.{key}")
    if isinstance(doc["claim"], dict):
        claim = _object(doc["claim"], CLAIM_KEYS, "claim")
        for key in CLAIM_KEYS:
            _string(claim[key], f"claim.{key}")
    if isinstance(doc["returned"], dict):
        ret = _object(doc["returned"], RETURNED_KEYS, "returned")
        for key in ("by", "delivery", "evidence"):
            _string(ret[key], f"returned.{key}")
        if not HEX64.fullmatch(_string(ret["event_sha256"], "returned.event_sha256")):
            raise ProjectionError("returned.event_sha256 is not 64 lowercase hex")
        if not isinstance(ret["artifacts"], list):
            raise ProjectionError("returned.artifacts is not a list")
        for item in ret["artifacts"]:
            item = _object(item, ARTIFACT_KEYS, "returned.artifacts item")
            _string(item["path"], "artifact path")
            if not HEX64.fullmatch(_string(item["sha256"], "artifact sha256")):
                raise ProjectionError("artifact sha256 is not 64 lowercase hex")
            if type(item["bytes"]) is not int or item["bytes"] < 0:
                raise ProjectionError("artifact bytes is not a non-negative integer")


def parse_projection(code: int, stdout: str, stderr: str, job_id: str) -> dict:
    """Strict inspection/2 parse. Raises ProjectionError on anything unexpected."""
    if stderr:
        raise ProjectionError("clerk wrote to stderr: " + stderr.strip().splitlines()[-1][:200])
    if stdout.count("\n") != 1 or not stdout.endswith("\n"):
        raise ProjectionError("stdout is not exactly one JSON line")
    doc = _strict(stdout)
    if not isinstance(doc, dict) or set(doc) != TOP_KEYS:
        raise ProjectionError("projection keys are not the inspection/2 set")
    if _string(doc["schema"], "schema") != INSPECTION_SCHEMA:
        raise ProjectionError(f"unsupported projection schema {doc['schema']!r}")
    if _string(doc["job_id"], "job_id") != job_id:
        raise ProjectionError("projection job_id is not the registered job")
    state = _string(doc["state"], "state")
    if state not in STATES:
        raise ProjectionError(f"unknown state {state!r}")
    checks = doc["checks"]
    if not isinstance(checks, dict) or set(checks) != set(CHECK_ENUMS):
        raise ProjectionError("checks keys are not the inspection/2 set")
    for key, allowed in CHECK_ENUMS.items():
        if _string(checks[key], f"checks.{key}") not in allowed:
            raise ProjectionError(f"checks.{key} has unknown value {checks[key]!r}")
    problems = doc["problems"]
    if not isinstance(problems, list) or any(
            not isinstance(p, dict) or not isinstance(p.get("kind"), str) or not isinstance(p.get("detail"), str)
            for p in problems):
        raise ProjectionError("problems is not a list of {kind, detail} objects")
    clean_phase = state in ("queued", "claimed", "returned")
    if clean_phase != isinstance(doc["job"], dict):
        raise ProjectionError("job presence does not match the state")
    if (state in ("claimed", "returned")) != isinstance(doc["claim"], dict):
        raise ProjectionError("claim presence does not match the state")
    returned = doc["returned"]
    if (state == "returned") != isinstance(returned, dict):
        raise ProjectionError("returned presence does not match the state")
    for key in ("job", "claim", "returned"):
        if doc[key] is not None and not isinstance(doc[key], dict):
            raise ProjectionError(f"{key} is neither null nor an object")
    _check_shapes(doc)
    kinds = {p["kind"] for p in problems}
    if code == 0 and (problems or not clean_phase):
        raise ProjectionError("exit 0 with problems or a damaged state")
    if code == 1 and (not clean_phase or not problems or kinds - FINDING_KINDS):
        raise ProjectionError("exit 1 without only artifact/instruction findings")
    if code == 2 and clean_phase and (not problems or kinds <= FINDING_KINDS):
        raise ProjectionError("exit 2 for an intact phase")
    if code not in (0, 1, 2):
        raise ProjectionError(f"unexpected exit {code}")
    return doc


def inspect(tool: dict, job: dict, runner=None) -> dict:
    """Observe one registered job. Never raises for a bad tool or projection: those become 'unsupported'."""
    runner = runner or run_show
    out = {"store": job["store"], "canonical_store": canonical_store(job["store"]), "job_id": job["job_id"],
           "reviewer": job["reviewer"], "tool_sha256": tool["sha256"], "status": "unsupported", "reason": "",
           "exit": None, "state": None, "checks": None, "problems": [], "event_sha256": None,
           "identity": False, "clean": False, "binding": "unknown", "review": "not-machine-readable"}
    problem = tool_problem(tool["path"], tool["sha256"])
    if problem:
        out["reason"] = "tool identity: " + problem
        return out
    argv = argv_for(tool["path"], job)
    try:
        code, stdout, stderr = runner(argv)
    except (OSError, subprocess.SubprocessError) as exc:
        out["reason"] = f"clerk did not run: {type(exc).__name__}"
        return out
    out["exit"] = code
    try:
        doc = parse_projection(code, stdout, stderr, job["job_id"])
    except ProjectionError as exc:
        out["reason"] = "projection: " + str(exc)
        # The attention item names its exact source even when the projection is unusable (CA-01).
        out["packet"] = (f"clerk:{job['store']}#{job['job_id']}@unsupported via show --json "
                         f"(tool {tool['sha256'][:12]}, exit {code}): {out['reason']}")
        return out
    out.update(status="ok", state=doc["state"], checks=doc["checks"], problems=doc["problems"])
    if isinstance(doc["job"], dict):
        bad = [k for k, want in (("job_id", job["job_id"]), ("reviewer", job["reviewer"])) if doc["job"].get(k) != want]
        out["binding"] = "ok" if not bad else "mismatch: " + ", ".join(f"{k} {doc['job'].get(k)!r}" for k in bad)
    if doc["state"] == "returned":
        out["event_sha256"] = doc["returned"]["event_sha256"]
        out["identity"] = (out["binding"] == "ok" and doc["checks"]["events"] == "ok"
                           and doc["checks"]["completion"] == "ok")
        out["clean"] = (out["identity"] and code == 0 and not doc["problems"]
                        and doc["checks"]["artifacts"] == "ok" and doc["checks"]["instructions"] == "usable")
    out["packet"] = (f"clerk:{job['store']}#{job['job_id']}@{out['event_sha256'] or doc['state']} via show --json "
                     f"(tool {tool['sha256'][:12]}, exit {code})")
    return out


def subject_for(observation: dict) -> dict | None:
    if not observation.get("identity"):
        return None
    return {"kind": "clerk-return", "store": observation["canonical_store"], "job_id": observation["job_id"],
            "event_sha256": observation["event_sha256"]}
