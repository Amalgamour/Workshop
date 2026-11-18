#!/usr/bin/env python3
"""Focused successor of labs/prime-cycle-pass02/prime_cycle.py.

Base sha256 689d63d26b0dfb59363563effa50acbd69856ffcc2ee728b7f54615f16fabd50, 58448 bytes.
Pass02 itself succeeded pass01 19ede9c2125307595d0be867bae1a3cb71bf3db0515ad83e7c04d3333e17861d.
Delta: custody observation uses the pinned 0521 verify command and the pinned
legacy inspector. target_page is the return-page directory. custody_path is a
directory. The review home stays derived from origin. The constructor pin is
labs/review-construction-pass02/construct.py. A /3 fingerprint is still the
review-task-binding/2 digest plus origin, member, direction, and goal.
The review-home hash is a write token. /1 stays legacy. /2 keeps the historical
whole-page rule. This module does not call return_capture.reserve. It does not
approve, release, close, or allocate. It does not execute a caller tool path.
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

ROOT = Path(r"D:\Git\lib-build")
CONSTRUCT = ROOT / "labs" / "review-construction-pass02" / "construct.py"
CONSTRUCT_SHA = "b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc"
CONSTRUCT_BYTES = 36188
LINES = ROOT / "labs" / "return-lines-pass01" / "return_lines.py"
LINES_SHA = "863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a"
LINES_BYTES = 100897
LINES_PATH = "labs/return-lines-pass01/return_lines.py"
PLACEMENT = ROOT / "labs" / "return-placement-pass01" / "return_placement.py"
PLACEMENT_SHA = "db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754"
PLACEMENT_BYTES = 66097
INSPECT = ROOT / "labs" / "return-capture-pass01" / "return_inspect.py"
INSPECT_SHA = "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b"
INSPECT_BYTES = 11402
INSPECT_PATH = "labs/return-capture-pass01/return_inspect.py"
REVIEW01 = ROOT / "labs" / "prime-review-pass01" / "prime_review.py"
REVIEW01_SHA = "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0"
REVIEW01_BYTES = 58324
REVIEW02 = ROOT / "labs" / "prime-review-pass02" / "prime_review.py"
REVIEW02_SHA = "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"
REVIEW02_BYTES = 58560

BOOK = "00.00.10.work"
LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PASS_ID = re.compile(r"^05\.\d\d$")
N5_ID = re.compile(r"^([0-9])5(\d\d)\.([a-z0-9][a-z0-9-]*)$")
N7_ID = re.compile(r"^([0-9])7(\d\d)\.([a-z0-9][a-z0-9-]*)$")
N5_KERNEL = re.compile(
    r"^00\.kernel/00\.00\.10\.work/([0-9])5(\d\d)\.([a-z0-9][a-z0-9-]*)/(05\.\d\d)\.md$"
)
N7_KERNEL = re.compile(
    r"^00\.kernel/00\.00\.10\.work/([0-9])7(\d\d)\.([a-z0-9][a-z0-9-]*)/(05\.\d\d)\.pack\.md$"
)
DIRECTION_FIELDS = (
    "goal",
    "scope",
    "prime_discretion",
    "director_required",
    "finish_criteria",
    "recorded_decisions",
)
JUDGMENT_KEYS = {
    "outcome",
    "disposition",
    "pass_terminal",
    "goal",
    "finding",
    "reasons",
    "source_refs",
    "next_action",
    "unresolved",
    "semantic_conflict",
    "design_fork",
    "holds",
    "answers",
    "sections",
}
SECTION_KEYS = [
    "return_result",
    "prime_finding",
    "within_direction",
    "next_bounded_action",
    "for_model",
    "issue",
    "consequences",
    "options",
    "recommendation",
    "question",
    "affected",
    "proposed_plan",
    "exploration",
    "assumptions",
    "open_questions",
    "outcome_evidence",
    "limits",
    "tests_note",
    "tests_passed",
    "learning",
    "preservation",
    "remaining_choices",
    "findings_account",
    "finish_assessments",
]
REG_KEYS = {
    "schema",
    "book",
    "work_id",
    "source_kind",
    "page_id",
    "pass",
    "kernel_page",
    "target",
    "descriptor_path",
    "agreement",
    "task_id",
    "assignment_path",
    "evidence",
    "submission_id",
    "receipt_label",
    "review_identity",
    "review_location",
    "goal",
    "bounds",
}
GOAL_KEYS = {"goal_id", "statement", "terminal", "evidence"}
DESC_KEYS = {
    "schema",
    "origin",
    "route",
    "target_page",
    "return_path",
    "custody_path",
    "receipt_path",
    "manifest_path",
    "submission_id",
    "custody_format",
    "receipt_sha256",
    "return_sha256",
    "return_bytes",
    "state",
    "verification",
}
PLACEMENT_KEYS = {
    "status",
    "intended_target_page",
    "intended_return_path",
    "relocation_record_path",
    "occupancy",
}
DESC_STATES = {"complete", "reserved", "incomplete", "conflict"}
NEW_FORMATS = {"return-line-capture/1", "legacy-relocated/1"}
DECISION_KEYS = {
    "schema",
    "review_id",
    "supersedes",
    "recovers",
    "binding",
    "attribution",
    "judgment",
    "supplied_record",
}
BINDING_KEYS = {
    "schema",
    "work_id",
    "page",
    "pass",
    "source",
    "member",
    "origin",
    "receipt_sha256",
    "submission_id",
    "return_sha256",
    "manifest_sha256",
    "agreement_sha256",
    "task_binding_sha256",
    "goal",
    "direction",
    "expected_prior",
    "write_token",
    "fingerprint",
}
RECORD_SCHEMAS = (
    "prime-cycle-review/1",
    "prime-cycle-review/2",
    "prime-cycle-review/3",
)
MAX_DOC = 262144
REPARSE = 0x400


class Refusal(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def need(cond: bool, message: str) -> None:
    if not cond:
        raise Refusal(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def exact(obj, keys: set[str], where: str) -> None:
    need(isinstance(obj, dict), f"{where} must be an object")
    unknown = sorted(set(obj) - keys)
    missing = sorted(keys - set(obj))
    if unknown:
        raise Refusal(f"unknown key {unknown[0]} at {where}")
    if missing:
        raise Refusal(f"missing key {missing[0]} at {where}")


def is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def is_inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return True
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def logical_path(value: str, where: str) -> str:
    need(isinstance(value, str) and value.strip() != "", f"empty path {where}")
    need("\\" not in value and not value.startswith("/") and not value.startswith("//"), f"unsafe path {where}")
    need(re.match(r"^[A-Za-z]:", value) is None, f"unsafe path {where}")
    parts = value.split("/")
    need(all(part not in ("", ".", "..") for part in parts), f"unsafe path {where}")
    return value


def fixture_root(text: str) -> Path:
    need(isinstance(text, str) and text.strip() != "", "fixture root is empty")
    need(not text.startswith("\\\\") and not text.startswith("//"), "UNC path fixture root")
    path = Path(text)
    need(path.is_absolute(), "fixture root must be absolute")
    need(".." not in path.parts, "unsafe path fixture root")
    need(path.exists() and path.is_dir() and not is_link(path), "fixture root is not a directory")
    if is_inside(path, ROOT) or is_inside(ROOT, path):
        raise Refusal("fixture root must stay outside D:\\Git\\lib-build")
    return path


def under(root: Path, text: str, where: str) -> Path:
    logical_path(text, where)
    resolved = (root / Path(text)).resolve()
    need(is_inside(resolved, root.resolve()), f"path escapes fixture root {where}")
    return resolved


def read_regular(path: Path, where: str) -> bytes:
    need(os.path.lexists(path), f"missing file {where}")
    need(not is_link(path), f"symlink refused {where}")
    need(path.is_file(), f"not a regular file {where}")
    data = path.read_bytes()
    need(b"\x00" not in data, f"unsupported byte in {where}")
    return data


def strict_json(data: bytes, where: str):
    need(not data.startswith(b"\xef\xbb\xbf"), f"{where} is not utf-8")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refusal(f"{where} is not utf-8") from exc
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise Refusal(f"{where} is not strict json") from exc
    return value


def pin_file(path: Path, digest: str, size: int, label: str) -> None:
    data = path.read_bytes()
    need(len(data) == size and sha(data) == digest, f"pinned tool hash does not match: {label}")


def pins() -> dict:
    pin_file(CONSTRUCT, CONSTRUCT_SHA, CONSTRUCT_BYTES, "construct")
    pin_file(REVIEW01, REVIEW01_SHA, REVIEW01_BYTES, "prime_review_pass01")
    pin_file(REVIEW02, REVIEW02_SHA, REVIEW02_BYTES, "prime_review_pass02")
    pin_file(LINES, LINES_SHA, LINES_BYTES, "return_lines")
    pin_file(PLACEMENT, PLACEMENT_SHA, PLACEMENT_BYTES, "return_placement")
    pin_file(INSPECT, INSPECT_SHA, INSPECT_BYTES, "return_inspect")
    self_bytes = Path(__file__).read_bytes()
    return {
        "construct": {"path": "labs/review-construction-pass02/construct.py", "sha256": CONSTRUCT_SHA, "bytes": CONSTRUCT_BYTES},
        "prime_review_pass01": {
            "path": "labs/prime-review-pass01/prime_review.py",
            "sha256": REVIEW01_SHA,
            "bytes": REVIEW01_BYTES,
        },
        "prime_review_pass02": {
            "path": "labs/prime-review-pass02/prime_review.py",
            "sha256": REVIEW02_SHA,
            "bytes": REVIEW02_BYTES,
        },
        "return_lines": {"path": LINES_PATH, "sha256": LINES_SHA, "bytes": LINES_BYTES},
        "return_placement": {
            "path": "labs/return-placement-pass01/return_placement.py",
            "sha256": PLACEMENT_SHA,
            "bytes": PLACEMENT_BYTES,
        },
        "return_inspect": {"path": INSPECT_PATH, "sha256": INSPECT_SHA, "bytes": INSPECT_BYTES},
        "prime_cycle_pass03": {
            "path": "labs/prime-cycle-pass03/prime_cycle.py",
            "sha256": sha(self_bytes),
            "bytes": len(self_bytes),
        },
    }


def run_tool(path: Path, args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-B", str(path), *args],
        cwd=str(ROOT),
        capture_output=True,
        env=env,
    )


def goal_sha(goal: dict) -> str:
    need(isinstance(goal.get("statement"), str), "goal.statement must be text")
    return sha(goal["statement"].encode("utf-8"))


def direction_of(reg: dict) -> dict:
    agreement = reg["agreement"]
    return {
        "schema": "prime-cycle-direction/1",
        "agreement_sha256": sha(canonical(agreement)),
        "fields": {key: sha(canonical(agreement.get(key))) for key in DIRECTION_FIELDS},
        "review_location": reg["review_location"],
        "book": reg["book"],
    }


def address_of(reg: dict) -> dict:
    kind = reg["source_kind"]
    page_id = reg["page_id"]
    pass_id = reg["pass"]
    if kind == "N5NN":
        match = N5_ID.fullmatch(page_id)
        need(match is not None, "page does not match N5NN")
        kernel = N5_KERNEL.fullmatch(reg["kernel_page"])
        need(kernel is not None, "kernel page does not match the registration")
        space, nn, subject = match.groups()
        need(kernel.groups() == (space, nn, subject, pass_id), "kernel page does not match the registration")
        destination = f"{page_id}/{pass_id}.md"
        member = f"{space}1{nn}.{subject}"
        return_page = member
        route = "matched-workflow-return-line"
    else:
        need(kind == "N7NN", f"unsupported source kind {kind}")
        match = N7_ID.fullmatch(page_id)
        need(match is not None, "page does not match N7NN")
        kernel = N7_KERNEL.fullmatch(reg["kernel_page"])
        need(kernel is not None, "kernel page does not match the registration")
        space, nn, subject = match.groups()
        need(kernel.groups() == (space, nn, subject, pass_id), "kernel page does not match the registration")
        tail = pass_id.split(".", 1)[1]
        destination = f"{page_id}/06.{tail}.review.md"
        member = None
        return_page = page_id
        route = "page-local-colab"
    need(reg["target"] == destination, "target is not the derived review destination")
    return {
        "book": BOOK,
        "page": page_id,
        "pass": pass_id,
        "member": member,
        "return_page": return_page,
        "return_path": f"{return_page}/{pass_id}.return.md",
        "custody_path": f"{return_page}/{pass_id}.custody",
        "destination": destination,
        "route": route,
        "kind": kind,
    }


def load_registration(root: Path, rel: str) -> dict:
    raw = strict_json(read_regular(under(root, rel, "registration"), "registration"), "registration")
    exact(raw, REG_KEYS, "registration")
    need(raw["schema"] == "prime-cycle-registration/2", "bad registration schema")
    need(raw["book"] == BOOK, "book is not 00.00.10.work")
    need(raw["source_kind"] in {"N5NN", "N7NN"}, "unsupported source kind")
    need(isinstance(raw["pass"], str) and PASS_ID.fullmatch(raw["pass"]) is not None, "bad pass")
    for key in ("work_id", "task_id", "submission_id", "review_identity"):
        need(isinstance(raw[key], str) and LABEL.fullmatch(raw[key]) is not None, f"bad id {key}")
    logical_path(raw["target"], "target")
    logical_path(raw["descriptor_path"], "descriptor_path")
    logical_path(raw["assignment_path"], "assignment_path")
    logical_path(raw["review_location"], "review_location")
    logical_path(raw["kernel_page"], "kernel_page")
    exact(raw["agreement"], set(DIRECTION_FIELDS), "agreement")
    evidence = raw["evidence"]
    need(isinstance(evidence, list), "bad type evidence")
    seen = []
    for index, item in enumerate(evidence):
        exact(item, {"label", "logical_path"}, f"evidence[{index}]")
        need(item["label"] in {"synthetic", "supplied"}, "bad evidence label")
        logical_path(item["logical_path"], f"evidence[{index}]")
        seen.append(item["logical_path"])
    need(len(seen) == len(set(seen)), "duplicate evidence path")
    need(raw["receipt_label"] in {"synthetic", "supplied"}, "bad receipt label")
    exact(raw["goal"], GOAL_KEYS, "goal")
    need(isinstance(raw["goal"]["goal_id"], str) and LABEL.fullmatch(raw["goal"]["goal_id"]) is not None, "bad id goal_id")
    need(raw["goal"]["terminal"] in {"open", "completed"}, "goal.terminal must be open or completed")
    need(isinstance(raw["goal"]["statement"], str) and raw["goal"]["statement"].strip(), "goal.statement must be text")
    need(
        isinstance(raw["goal"]["evidence"], list) and all(isinstance(item, str) and item.strip() for item in raw["goal"]["evidence"]),
        "goal.evidence must be a list of strings",
    )
    exact(raw["bounds"], {"max_output_bytes"}, "bounds")
    limit = raw["bounds"]["max_output_bytes"]
    need(type(limit) is int and limit > 0, "bad max_output_bytes")
    raw["address"] = address_of(raw)
    return raw


def null_measure() -> dict:
    return {
        "receipt_sha256": None,
        "receipt_bytes": None,
        "return_sha256": None,
        "return_bytes": None,
        "manifest_sha256": None,
        "manifest_bytes": None,
        "custody_present": None,
        "verification_present": None,
    }


def failed_observation(reason: str) -> dict:
    return {
        "state": "failed",
        "reason": reason,
        "descriptor_state": None,
        "origin": None,
        "member": None,
        "route": None,
        "submission_id": None,
        "receipt_sha256": None,
        "return_sha256": None,
        "return_bytes": None,
        "manifest_sha256": None,
        "manifest_bytes": None,
        "measured": null_measure(),
        "task_association": "not-established",
        "task_association_reason": "custody records do not name the review task",
        "placement_status": None,
        "filing_claimed": False,
        "custody_verified": False,
        "custody_member": None,
        "validator": None,
    }


def hash_or_none(path: Path) -> tuple[str | None, int | None, str | None]:
    if not os.path.lexists(path):
        return None, None, "absent"
    if is_link(path) or not path.is_file():
        return None, None, "not-a-regular-file"
    data = path.read_bytes()
    if b"\x00" in data:
        return None, None, "unsupported-byte"
    return sha(data), len(data), None


def directory_problem(path: Path) -> str | None:
    if not os.path.lexists(path):
        return "absent"
    if is_link(path):
        return "link"
    if not path.is_dir():
        return "not-a-directory"
    return None


def tool_json(path: Path, args: list[str]) -> tuple[int, dict | None, str]:
    proc = run_tool(path, args)
    stderr = proc.stderr.decode("utf-8", "replace")
    try:
        body = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        return proc.returncode, None, stderr
    if not isinstance(body, dict):
        return proc.returncode, None, stderr
    return proc.returncode, body, stderr


def same_descriptor(left: dict, right: dict) -> bool:
    return canonical(left) == canonical(right)


def load_json_file(path: Path) -> dict | None:
    if directory_problem(path.parent) is not None and not path.is_file():
        return None
    try:
        value = strict_json(read_regular(path, path.name), path.name)
    except Refusal:
        return None
    return value if isinstance(value, dict) else None


def chain_problem(root: Path, raw: dict, custody_format: str) -> str | None:
    try:
        return chain_problem_body(root, raw, custody_format)
    except Refusal as exc:
        return exc.message


def chain_problem_body(root: Path, raw: dict, custody_format: str) -> str | None:
    custody = under(root, raw["custody_path"], "custody")
    problem = directory_problem(custody)
    if problem:
        return "custody path is not a directory" if problem != "absent" else "custody directory is absent"
    receipt_path = under(root, raw["receipt_path"], "receipt")
    manifest_path = under(root, raw["manifest_path"], "manifest")
    return_path = under(root, raw["return_path"], "return")
    receipt = load_json_file(receipt_path)
    manifest = load_json_file(manifest_path)
    if receipt is None or manifest is None:
        return "receipt or manifest is not readable json"
    if custody_format == "return-line-capture/1":
        if receipt.get("schema") != "return-line-capture/1" or receipt.get("kind") != "receipt":
            return "receipt schema is not return-line-capture/1"
        if manifest.get("schema") != "return-line-capture/1" or manifest.get("kind") != "manifest":
            return "manifest schema is not return-line-capture/1"
        reservation_path = custody / "reservation.json"
        reservation = load_json_file(reservation_path)
        if reservation is None or reservation.get("schema") != "return-line-capture/1":
            return "reservation schema is not return-line-capture/1"
        if reservation.get("submission_id") != raw["submission_id"] or receipt.get("submission_id") != raw["submission_id"]:
            return "submission_id does not match the custody records"
        if reservation.get("origin") != raw["origin"]:
            return "origin does not match the reservation"
        reservation_bytes = read_regular(reservation_path, "reservation")
        manifest_bytes = read_regular(manifest_path, "manifest")
        return_bytes = read_regular(return_path, "return")
        custody_return = custody / "return.md"
        if hash_or_none(custody_return)[0] != sha(return_bytes):
            return "page tail does not match the custody return"
        if receipt.get("reservation_sha256") != sha(reservation_bytes) or manifest.get("reservation_sha256") != sha(reservation_bytes):
            return "reservation hash does not match the custody records"
        if receipt.get("manifest_sha256") != sha(manifest_bytes):
            return "manifest hash does not match the custody records"
        if receipt.get("return_sha256") != sha(return_bytes) or receipt.get("return_sha256") != raw["return_sha256"]:
            return "return hash does not match the custody records"
        if receipt.get("approved") is not False or receipt.get("accepted") is not False or receipt.get("published") is not False:
            return "receipt claims acceptance"
        if receipt.get("acceptance") is not None:
            return "receipt claims acceptance"
        sources = manifest.get("sources")
        if not isinstance(sources, list):
            return "manifest payload list is missing"
        for index, source in enumerate(sources, start=1):
            if not isinstance(source, dict):
                return "manifest payload list is missing"
            payload = custody / "payload" / f"{index:04d}.blob"
            digest, _length, error = hash_or_none(payload)
            if error or digest != source.get("sha256"):
                return "payload hash does not match the manifest"
        return None
    if custody_format == "legacy-relocated/1":
        if receipt.get("schema") != "return-capture/1":
            return "receipt schema is not return-capture/1"
        relocation = load_json_file(custody / "relocation.json")
        if relocation is None or relocation.get("schema") != "return-line-relocation/1":
            return "relocation record is missing"
        if relocation.get("custody_format") != "legacy-relocated/1":
            return "relocation record is missing"
        return_bytes = read_regular(return_path, "return")
        if sha(return_bytes) != raw["return_sha256"] or len(return_bytes) != raw["return_bytes"]:
            return "return hash does not match the custody records"
        if sha(read_regular(receipt_path, "receipt")) != raw["receipt_sha256"]:
            return "receipt bytes do not match the descriptor"
        return None
    return "descriptor custody_format is not a known format"


def finish_observed(obs: dict, raw: dict, measured: dict, state: str, reason: str | None, validator: dict) -> dict:
    obs["measured"] = measured
    obs["receipt_sha256"] = measured["receipt_sha256"]
    obs["return_sha256"] = measured["return_sha256"]
    obs["return_bytes"] = measured["return_bytes"]
    obs["manifest_sha256"] = measured["manifest_sha256"]
    obs["manifest_bytes"] = measured["manifest_bytes"]
    obs["state"] = state
    obs["reason"] = reason
    obs["validator"] = validator
    obs["custody_verified"] = state == "complete"
    obs["filing_claimed"] = False
    obs["custody_member"] = raw.get("target_page") if isinstance(raw.get("target_page"), str) else None
    obs["task_association"] = "not-established"
    obs["task_association_reason"] = "custody records do not name the review task"
    if state == "complete" and raw.get("schema") == "return-line-descriptor/2":
        placement = raw.get("placement") if isinstance(raw.get("placement"), dict) else {}
        obs["placement_status"] = placement.get("status")
    elif state == "complete":
        obs["placement_status"] = "final"
    else:
        placement = raw.get("placement") if isinstance(raw.get("placement"), dict) else None
        obs["placement_status"] = placement.get("status") if isinstance(placement, dict) else None
    return obs


def observe_descriptor(root: Path, reg: dict) -> dict:
    address = reg["address"]
    path = under(root, reg["descriptor_path"], "descriptor")
    if not os.path.lexists(path):
        obs = failed_observation("descriptor file is absent")
        obs["state"] = "missing"
        obs["member"] = address["member"]
        obs["route"] = address["route"]
        return obs
    if is_link(path) or not path.is_file():
        obs = failed_observation("descriptor is not a regular file")
        obs["member"] = address["member"]
        return obs
    try:
        raw = strict_json(read_regular(path, "descriptor"), "descriptor")
        need(isinstance(raw, dict), "bad descriptor schema")
        schema = raw.get("schema")
        if schema == "return-line-descriptor/1":
            exact(raw, DESC_KEYS, "descriptor")
        elif schema == "return-line-descriptor/2":
            exact(raw, DESC_KEYS | {"placement"}, "descriptor")
            exact(raw["placement"], PLACEMENT_KEYS, "placement")
        else:
            raise Refusal("unsupported descriptor schema")
        exact(raw["origin"], {"book", "page", "batch"}, "origin")
        exact(raw["verification"], {"tool_path", "tool_sha256", "result", "evidence_path"}, "verification")
    except Refusal as exc:
        obs = failed_observation(exc.message)
        obs["state"] = "unsupported" if exc.message == "unsupported descriptor schema" else "failed"
        obs["member"] = address["member"]
        return obs
    obs = failed_observation(None)
    obs["descriptor_state"] = raw["state"]
    obs["origin"] = raw["origin"]
    obs["member"] = address["member"]
    obs["route"] = raw["route"]
    obs["submission_id"] = raw["submission_id"] if isinstance(raw["submission_id"], str) else None
    measured = null_measure()
    receipt_sha, receipt_len, _receipt_err = hash_or_none(under(root, raw["receipt_path"], "receipt")) if isinstance(raw.get("receipt_path"), str) else (None, None, "absent")
    return_sha, return_len, _return_err = hash_or_none(under(root, raw["return_path"], "return")) if isinstance(raw.get("return_path"), str) else (None, None, "absent")
    manifest_sha, manifest_len, _manifest_err = hash_or_none(under(root, raw["manifest_path"], "manifest")) if isinstance(raw.get("manifest_path"), str) else (None, None, "absent")
    custody_problem = directory_problem(under(root, raw["custody_path"], "custody")) if isinstance(raw.get("custody_path"), str) else "absent"
    measured.update(
        receipt_sha256=receipt_sha,
        receipt_bytes=receipt_len,
        return_sha256=return_sha,
        return_bytes=return_len,
        manifest_sha256=manifest_sha,
        manifest_bytes=manifest_len,
        custody_present=custody_problem is None,
        verification_present=False,
    )
    if raw["state"] not in DESC_STATES:
        return finish_observed(obs, raw, measured, "conflict", "descriptor state is not a known state", None)
    if raw["route"] not in {"matched-workflow-return-line", "page-local-colab"}:
        return finish_observed(obs, raw, measured, "conflict", "descriptor route is not a known route", None)
    reasons = []
    if raw["route"] != address["route"]:
        reasons.append("route does not match the source")
    origin = raw["origin"]
    if origin.get("book") != BOOK or origin.get("page") != address["page"] or origin.get("batch") != address["pass"]:
        reasons.append("origin does not match the source")
    if raw["submission_id"] != reg["submission_id"]:
        reasons.append("submission_id does not match the registration")
    if reasons:
        return finish_observed(obs, raw, measured, "conflict", reasons[0], None)
    custody_format = raw["custody_format"]
    if schema == "return-line-descriptor/2" and custody_format == "staged-seal/1":
        return finish_observed(obs, raw, measured, "unsupported", "staged-seal/1 is not supported in this slice", None)
    if schema == "return-line-descriptor/2" and custody_format == "legacy-in-place/1":
        return observe_legacy_in_place(root, reg, raw, obs, measured)
    if custody_format not in NEW_FORMATS:
        return finish_observed(obs, raw, measured, "unsupported", "descriptor custody_format is not a known format", None)
    if schema == "return-line-descriptor/2":
        placement = raw["placement"]
        if placement["status"] != "final" or placement["intended_target_page"] != raw["target_page"] or placement["intended_return_path"] != raw["return_path"]:
            return finish_observed(obs, raw, measured, "unsupported", "unsupported /2 variant", None)
    if raw["verification"]["tool_path"] != LINES_PATH:
        return finish_observed(obs, raw, measured, "conflict", "verification tool_path is not the pinned validator", None)
    if raw["target_page"] != address["return_page"]:
        return finish_observed(obs, raw, measured, "conflict", "target_page is not the derived return page", None)
    if raw["custody_path"] != address["custody_path"] or raw["return_path"] != address["return_path"]:
        return finish_observed(obs, raw, measured, "conflict", "custody path is not the derived custody directory", None)
    if raw["receipt_path"] != f"{address['custody_path']}/receipt.json" or raw["manifest_path"] != f"{address['custody_path']}/manifest.json":
        return finish_observed(obs, raw, measured, "conflict", "receipt path is not inside the custody directory", None)
    if custody_problem:
        reason = "custody path is not a directory" if custody_problem != "absent" else "custody directory is absent"
        return finish_observed(obs, raw, measured, "conflict", reason, None)
    code, body, stderr = tool_json(LINES, ["verify", "--book", str(root), "--page", address["page"], "--batch", address["pass"]])
    if body is None or not isinstance(body.get("descriptor"), dict):
        obs["state"] = "failed"
        obs["reason"] = stderr.strip() or "pinned validator returned no descriptor"
        obs["measured"] = measured
        return obs
    regenerated = body["descriptor"]
    problems = body.get("detail", {}).get("problems") if isinstance(body.get("detail"), dict) else []
    validator = {
        "tool": LINES_PATH,
        "exit": code,
        "state": body.get("state"),
        "check": body.get("check"),
        "problems": problems if isinstance(problems, list) else [],
    }
    measured["verification_present"] = True
    compared = raw
    if schema == "return-line-descriptor/2":
        compared = {key: raw[key] for key in DESC_KEYS}
        compared["schema"] = "return-line-descriptor/1"
    if not same_descriptor(compared, regenerated):
        detail = validator["problems"][0] if validator["problems"] else body.get("state")
        return finish_observed(obs, raw, measured, "conflict", f"descriptor does not match the pinned validator: {detail}", validator)
    state = regenerated.get("state")
    if state == "complete":
        chain = chain_problem(root, raw, custody_format)
        if chain:
            return finish_observed(obs, raw, measured, "conflict", chain, validator)
        return finish_observed(obs, raw, measured, "complete", None, validator)
    if state in {"reserved", "incomplete", "conflict"}:
        reason = f"descriptor state is {state}"
        if validator["problems"]:
            reason = f"{reason}: {validator['problems'][0]}"
        return finish_observed(obs, raw, measured, state, reason, validator)
    return finish_observed(obs, raw, measured, "conflict", "descriptor state is not a known state", validator)


def observe_legacy_in_place(root: Path, reg: dict, raw: dict, obs: dict, measured: dict) -> dict:
    placement = raw["placement"]
    if raw["verification"]["tool_path"] != INSPECT_PATH:
        return finish_observed(obs, raw, measured, "conflict", "verification tool_path is not the pinned validator", None)
    if placement["status"] != "pending" or placement["relocation_record_path"] is not None:
        return finish_observed(obs, raw, measured, "conflict", "legacy-in-place placement is pending", None)
    member = raw["custody_path"]
    if not isinstance(member, str) or member != raw["target_page"] or "/" in member:
        return finish_observed(obs, raw, measured, "conflict", "custody path is not the original member directory", None)
    if not re.fullmatch(r"01[0-9]{2}\.[A-Za-z0-9][A-Za-z0-9._-]{0,63}", member):
        code, inspected, stderr = tool_json(INSPECT, ["inspect", "--book", str(root), "--member", member, "--json"])
        problem = None
        problems = []
        status = None
        if isinstance(inspected, dict):
            status = inspected.get("status")
            if isinstance(inspected.get("problems"), list):
                problems = inspected["problems"]
                if problems:
                    problem = problems[0]
        reason = "unsupported member prefix" if problem is None else f"unsupported member prefix: {problem}"
        if inspected is None and stderr.strip():
            reason = "unsupported member prefix: " + stderr.strip()
        validator = {"tool": INSPECT_PATH, "exit": code, "state": status, "problems": problems}
        return finish_observed(obs, raw, measured, "unsupported", reason, validator)
    if raw["return_path"] != f"{member}/return.md" or raw["receipt_path"] != f"{member}/receipt.json" or raw["manifest_path"] != f"{member}/manifest.json":
        return finish_observed(obs, raw, measured, "conflict", "legacy paths are not inside the original member", None)
    code, inspected, stderr = tool_json(INSPECT, ["inspect", "--book", str(root), "--member", member, "--json"])
    if inspected is None:
        obs["state"] = "failed"
        obs["reason"] = stderr.strip() or "pinned inspector returned no observation"
        obs["measured"] = measured
        return obs
    status = inspected.get("status")
    reservation = inspected.get("reservation") if isinstance(inspected.get("reservation"), dict) else None
    origin = reservation.get("origin") if isinstance(reservation, dict) else None
    validator = {"tool": INSPECT_PATH, "exit": code, "state": status, "problems": inspected.get("problems") or []}
    measured["verification_present"] = True
    if not isinstance(origin, dict):
        mapped = "reserved" if status == "reserved" else "incomplete" if status == "incomplete" else "conflict"
        if status == "missing":
            mapped = "missing"
        if status == "refused":
            mapped = "unsupported" if "outside the return band" in " ".join(validator["problems"]) else "conflict"
        return finish_observed(obs, raw, measured, mapped, f"pinned inspector: {status}", validator)
    if origin.get("book") != BOOK or origin.get("page") != reg["address"]["page"] or origin.get("batch") != reg["address"]["pass"]:
        return finish_observed(obs, raw, measured, "conflict", "origin does not match the source", validator)
    if reservation.get("submission_id") != raw["submission_id"]:
        return finish_observed(obs, raw, measured, "conflict", "submission_id does not match the custody records", validator)
    route_code, route, route_err = tool_json(
        PLACEMENT,
        ["route", "--book", BOOK, "--page", origin["page"], "--batch", origin["batch"]],
    )
    if route is None:
        return finish_observed(obs, raw, measured, "unsupported", route_err.strip() or "unsupported route", validator)
    if placement["intended_target_page"] != route.get("target_page") or placement["intended_return_path"] != route.get("return_path"):
        return finish_observed(obs, raw, measured, "conflict", "intended placement does not match the source route", validator)
    if placement["occupancy"] is not None:
        return finish_observed(obs, raw, measured, "unsupported", "occupancy is not read in this slice", validator)
    if route_code != 0:
        return finish_observed(obs, raw, measured, "unsupported", "unsupported route", validator)
    if status == "complete":
        chain_receipt = load_json_file(under(root, raw["receipt_path"], "receipt"))
        if chain_receipt is None or chain_receipt.get("schema") != "return-capture/1":
            return finish_observed(obs, raw, measured, "conflict", "receipt schema is not return-capture/1", validator)
        if measured["receipt_sha256"] != raw["receipt_sha256"] or measured["return_sha256"] != raw["return_sha256"]:
            return finish_observed(obs, raw, measured, "conflict", "descriptor does not match the pinned validator: material hash", validator)
        if measured["return_bytes"] != raw["return_bytes"]:
            return finish_observed(obs, raw, measured, "conflict", "descriptor does not match the pinned validator: material hash", validator)
        return finish_observed(obs, raw, measured, "complete", None, validator)
    mapped = {"reserved": "reserved", "incomplete": "incomplete", "missing": "missing"}.get(status, "conflict")
    return finish_observed(obs, raw, measured, mapped, f"pinned inspector: {status}", validator)


def write_token_of(root: Path, reg: dict) -> dict | None:
    path = under(root, reg["target"], "target")
    if not os.path.lexists(path):
        return None
    data = read_regular(path, "target")
    return {
        "schema": "review-write-token/1",
        "path": reg["target"],
        "sha256": sha(data),
        "bytes": len(data),
    }


def stub_record(reg: dict, obs: dict, return_path: str) -> dict:
    address = reg["address"]
    if address["kind"] == "N7NN":
        return {"schema": "prime-review-record/1", "sources": []}
    return {
        "schema": "prime-review-record/1",
        "sources": [
            {
                "kind": "capture",
                "logical_path": return_path,
                "identity": {
                    "schema": "return-capture/1",
                    "member": address["member"],
                    "submission_id": reg["submission_id"],
                    "receipt_sha256": obs["receipt_sha256"],
                    "origin": {
                        "book": BOOK,
                        "page": address["page"],
                        "batch": address["pass"],
                    },
                },
            }
        ],
    }


def constructor_receipt(reg: dict, descriptor: dict) -> dict:
    address = reg["address"]
    if address["kind"] == "N5NN":
        placement = "n5nn-matching-line"
        page_local = None
        member = address["member"]
    else:
        placement = "n7nn-page-local"
        page_local = f"05.{address['pass'].split('.', 1)[1]}.return.md"
        member = None
    return {
        "placement": placement,
        "member": member,
        "page_local": page_local,
        "submission_id": reg["submission_id"],
        "receipt_path": descriptor["receipt_path"],
        "return_path": descriptor["return_path"],
        "manifest_path": descriptor["manifest_path"],
        "status": "complete",
        "label": reg["receipt_label"],
    }


def bind_digest(root: Path, reg: dict, obs: dict) -> str:
    descriptor = strict_json(
        read_regular(under(root, reg["descriptor_path"], "descriptor"), "descriptor"),
        "descriptor",
    )
    envelope = {
        "schema": "review-construction/1",
        "source_kind": reg["source_kind"],
        "page": reg["kernel_page"],
        "pass": reg["pass"],
        "target": reg["target"],
        "expect_sha256": "absent",
        "permit_create": False,
        "review_identity": reg["review_identity"],
        "task": {"task_id": reg["task_id"], "assignment_path": reg["assignment_path"]},
        "evidence": reg["evidence"],
        "agreement": reg["agreement"],
        "receipt": constructor_receipt(reg, descriptor),
        "record": stub_record(reg, obs, descriptor["return_path"]),
    }
    scratch = root / "scratch"
    scratch.mkdir(exist_ok=True)
    rel = "scratch/bind-input.json"
    under(root, rel, "bind input").write_bytes(canonical(envelope))
    proc = run_tool(CONSTRUCT, ["bind", "--fixture-root", str(root), "--input", rel])
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise Refusal(detail or "constructor bind refused")
    payload = json.loads(proc.stdout.decode("utf-8"))
    need(payload.get("schema") == "review-task-binding/2", "constructor bind returned an unexpected schema")
    need(payload.get("target_read") is False, "constructor bind read the review home")
    return payload["binding_sha256"]


def make_binding(reg: dict, obs: dict, task_binding: str, token, prior) -> dict:
    binding = {
        "schema": "prime-cycle-binding/3",
        "work_id": reg["work_id"],
        "page": reg["page_id"],
        "pass": reg["pass"],
        "source": {"book": reg["book"], "page": reg["page_id"], "pass": reg["pass"]},
        "member": obs["member"],
        "origin": obs["origin"],
        "receipt_sha256": obs["receipt_sha256"],
        "submission_id": obs["submission_id"],
        "return_sha256": obs["return_sha256"],
        "manifest_sha256": obs["manifest_sha256"],
        "agreement_sha256": sha(canonical(reg["agreement"])),
        "task_binding_sha256": task_binding,
        "goal": {"goal_id": reg["goal"]["goal_id"], "goal_sha256": goal_sha(reg["goal"])},
        "direction": direction_of(reg),
        "expected_prior": prior,
        "write_token": token,
    }
    finger = {key: value for key, value in binding.items() if key not in {"write_token", "fingerprint"}}
    binding["fingerprint"] = sha(canonical(finger))
    return binding


def review_root(root: Path, reg: dict) -> Path:
    return under(root, reg["review_location"], "review location")


def scan_reviews(root: Path, reg: dict) -> dict:
    base = review_root(root, reg)
    out = {"committed": {}, "partial": [], "invalid": []}
    if not os.path.lexists(base):
        return out
    need(base.is_dir() and not is_link(base), "review location must be a plain directory")
    for entry in sorted(base.iterdir(), key=lambda item: item.name):
        if is_link(entry) or not entry.is_dir() or LABEL.fullmatch(entry.name) is None:
            out["invalid"].append({"review_id": entry.name, "phase": "invalid", "reason": "not a plain review directory"})
            continue
        marker_path = entry / "COMMITTED.json"
        if not marker_path.is_file():
            out["partial"].append({
                "review_id": entry.name,
                "phase": "partial-no-marker",
                "present": sorted(path.name for path in entry.iterdir()),
            })
            continue
        try:
            marker = strict_json(read_regular(marker_path, "marker"), "marker")
            record_bytes = read_regular(entry / "record.json", "record")
            review_bytes = read_regular(entry / "REVIEW.md", "REVIEW.md")
            need(isinstance(marker, dict), "marker: not an object")
            need(marker.get("record_sha256") == sha(record_bytes), "marker hashes do not match the files")
            need(marker.get("review_md_sha256") == sha(review_bytes), "marker hashes do not match the files")
            record = strict_json(record_bytes, "record")
            need(isinstance(record, dict) and record.get("schema") in RECORD_SCHEMAS, "unknown record schema")
        except Refusal as exc:
            phase = "partial-marker-mismatch" if marker_path.is_file() else "invalid"
            bucket = out["partial"] if phase.startswith("partial") else out["invalid"]
            bucket.append({"review_id": entry.name, "phase": phase, "reason": exc.message})
            continue
        out["committed"][entry.name] = {
            "record": record,
            "record_sha256": sha(record_bytes),
            "directory": f"{reg['review_location']}/{entry.name}",
        }
    return out


def prior_of(scan: dict):
    superseded = set()
    for item in scan["committed"].values():
        decision = item["record"].get("decision")
        if isinstance(decision, dict) and isinstance(decision.get("supersedes"), dict):
            superseded.add(decision["supersedes"].get("review_id"))
    heads = [key for key in scan["committed"] if key not in superseded]
    if len(heads) > 1:
        return "fork", heads
    if not heads:
        return None, heads
    head = heads[0]
    return {"review_id": head, "record_sha256": scan["committed"][head]["record_sha256"]}, heads


def empty_judgment(reg: dict) -> dict:
    sections = {key: None for key in SECTION_KEYS}
    return {
        "outcome": None,
        "disposition": None,
        "pass_terminal": None,
        "goal": {
            "terminal": None,
            "goal_id": reg["goal"]["goal_id"],
            "goal_sha256": goal_sha(reg["goal"]),
            "evidence": [],
        },
        "finding": None,
        "reasons": [],
        "source_refs": [],
        "next_action": None,
        "unresolved": [],
        "semantic_conflict": None,
        "design_fork": None,
        "holds": [],
        "answers": [],
        "sections": sections,
    }


def questions_of(decision: dict) -> list[str]:
    found = []
    judgment = decision.get("judgment") if isinstance(decision, dict) else None
    if not isinstance(judgment, dict):
        return found
    for item in judgment.get("unresolved") or []:
        if isinstance(item, str) and item.strip():
            found.append(item)
    sections = judgment.get("sections") if isinstance(judgment.get("sections"), dict) else {}
    question = sections.get("question")
    if isinstance(question, dict) and isinstance(question.get("text"), str) and question["text"].strip():
        found.append(question["text"])
    return found


def replies_of(decision: dict) -> list[str]:
    record = decision.get("supplied_record") if isinstance(decision, dict) else None
    if not isinstance(record, dict):
        return []
    found = []
    for answer in record.get("answers") or []:
        if isinstance(answer, dict) and isinstance(answer.get("reply"), str) and answer["reply"].strip():
            found.append(answer["reply"])
    return found


def next_action_of(decision: dict, review_id: str, record_sha: str):
    judgment = decision.get("judgment") if isinstance(decision, dict) else None
    if not isinstance(judgment, dict):
        return None
    action = judgment.get("next_action")
    if not isinstance(action, dict):
        return None
    attribution = decision.get("attribution") if isinstance(decision.get("attribution"), dict) else {}
    return {
        "action_id": action.get("action_id"),
        "text": action.get("text"),
        "authorized_in_grant": action.get("authorized_in_grant"),
        "author": attribution.get("actor_label"),
        "review_id": review_id,
        "record_sha256": record_sha,
    }


def render_state_of(root: Path, reg: dict, review_id: str, token, task_binding: str) -> str:
    path = review_root(root, reg) / review_id / "rendered.json"
    if not path.is_file():
        return "pending"
    try:
        payload = strict_json(read_regular(path, "rendered"), "rendered")
    except Refusal:
        return "pending"
    if (
        token is not None
        and payload.get("target_sha256") == token["sha256"]
        and payload.get("task_binding_sha256") == task_binding
    ):
        return "rendered"
    return "diverged"


def historical_page_current(reg: dict, obs: dict, token, binding: dict) -> bool:
    source = binding.get("source") if isinstance(binding.get("source"), dict) else {}
    if token is None or source.get("page_sha256") != token["sha256"]:
        return False
    return (
        binding.get("member") == obs["member"]
        and binding.get("receipt_sha256") == obs["receipt_sha256"]
        and binding.get("submission_id") == obs["submission_id"]
        and binding.get("origin") == obs["origin"]
        and binding.get("direction") == direction_of(reg)
    )


def derive(root: Path, reg: dict, obs: dict, token, scan: dict) -> dict:
    prior, heads = prior_of(scan)
    attention = []
    for item in scan["partial"]:
        attention.append(f"partial review {item['review_id']} ({item['phase']}); recover with a new review_id")
    for item in scan["invalid"]:
        attention.append(f"invalid review directory {item['review_id']}: {item['reason']}")
    fork = prior == "fork"
    if fork:
        attention.append(f"lineage-fork: {len(heads)} committed heads; no head is chosen")
        prior_value = None
    else:
        prior_value = prior
    if obs.get("task_association") == "not-established" and obs["state"] == "complete":
        attention.append("task association is not established by the custody records")
    binding = None
    if obs["state"] == "complete" and not fork:
        binding = make_binding(reg, obs, bind_digest(root, reg, obs), token, prior_value)
    elif obs["state"] == "failed":
        attention.append(f"observation-failed: {obs['reason']}")
    elif obs["reason"]:
        attention.append(obs["reason"])
    view = {
        "schema": "prime-cycle-view/4",
        "work_id": reg["work_id"],
        "page": reg["page_id"],
        "pass": reg["pass"],
        "member": obs["member"],
        "pass_state": "observation-failed" if obs["state"] == "failed" else obs["state"],
        "render_state": "not-applicable",
        "interpretation": None,
        "observation": {
            "state": obs["state"],
            "reason": obs["reason"],
            "descriptor_state": obs["descriptor_state"],
            "measured": obs["measured"],
            "task_association": obs.get("task_association"),
            "task_association_reason": obs.get("task_association_reason"),
            "placement_status": obs.get("placement_status"),
            "filing_claimed": False,
            "custody_verified": obs.get("custody_verified"),
            "validator": obs.get("validator"),
            "member": obs.get("member"),
            "custody_member": obs.get("custody_member"),
        },
        "binding": binding,
        "write_token": token,
        "task_binding_sha256": None if binding is None else binding["task_binding_sha256"],
        "template": None,
        "latest_review": None,
        "historical": None,
        "next_action": None,
        "questions": [],
        "director_replies": [],
        "attention": attention,
        "current": False,
        "custody": "not-established",
        "allocated": False,
        "closes_work": False,
        "releases_action": False,
        "authenticates_actor": False,
        "authority": "none",
        "pins": pins(),
    }
    if obs["state"] == "complete" and binding is not None and token is not None and not fork:
        count = len(scan["committed"]) + len(scan["partial"]) + len(scan["invalid"]) + 1
        view["template"] = {
            "schema": "prime-cycle-decision/3",
            "review_id": f"{reg['pass']}-r{count}",
            "supersedes": prior_value,
            "recovers": None,
            "binding": binding,
            "attribution": {"actor_label": None, "role": "prime", "evidence": None},
            "judgment": empty_judgment(reg),
            "supplied_record": None,
        }
    if obs["state"] == "complete" and not heads and not fork:
        view["pass_state"] = "awaiting-review"
        attention.append("awaiting-review: a described return has no recorded review")
    if fork or not heads:
        view["attention"] = attention
        return view
    head_id = heads[0]
    head = scan["committed"][head_id]
    record = head["record"]
    decision = record.get("decision") if isinstance(record.get("decision"), dict) else {}
    schema = record["schema"]
    current = False
    interpretation = None
    reason = None
    if obs["state"] == "failed":
        view["pass_state"] = "observation-failed"
        reason = "observation-failed"
    elif schema == "prime-cycle-review/1":
        view["pass_state"] = "review-unusable"
        interpretation = "legacy-binding"
        reason = "legacy-binding"
    elif schema == "prime-cycle-review/2":
        interpretation = "historical-page-hash"
        stored = decision.get("binding") if isinstance(decision.get("binding"), dict) else {}
        if obs["state"] == "complete" and historical_page_current(reg, obs, token, stored):
            view["pass_state"] = "reviewed"
            current = True
        else:
            view["pass_state"] = "review-stale"
            reason = "review-stale"
    elif schema == "prime-cycle-review/3":
        interpretation = "task-binding"
        stored = decision.get("binding") if isinstance(decision.get("binding"), dict) else {}
        if obs["state"] != "complete" or binding is None:
            view["pass_state"] = obs["state"] if obs["state"] != "failed" else "observation-failed"
            reason = obs["reason"] or view["pass_state"]
        else:
            fresh = make_binding(reg, obs, binding["task_binding_sha256"], token, stored.get("expected_prior"))
            if fresh["fingerprint"] != stored.get("fingerprint"):
                view["pass_state"] = "review-stale"
                reason = "review-stale"
            else:
                current = True
                conflict_path = review_root(root, reg) / head_id / "render-conflict.json"
                if conflict_path.is_file():
                    view["render_state"] = "conflict"
                    view["pass_state"] = "render-conflict"
                    attention.append("render-conflict: the judgment is kept and the existing section was not overwritten")
                else:
                    state = render_state_of(root, reg, head_id, token, stored.get("task_binding_sha256"))
                    view["render_state"] = state
                    view["pass_state"] = "reviewed" if state == "rendered" else "render-pending"
                    if state == "diverged":
                        view["pass_state"] = "reviewed"
                        attention.append("render attestation diverged from the review home; the task binding is unchanged")
    else:
        view["pass_state"] = "review-unusable"
        reason = "unknown record schema"
    action = next_action_of(decision, head_id, head["record_sha256"])
    questions = questions_of(decision)
    replies = replies_of(decision)
    view["interpretation"] = interpretation
    view["latest_review"] = {
        "review_id": head_id,
        "record_sha256": head["record_sha256"],
        "schema": schema,
        "directory": head["directory"],
        "current": current,
        "task_binding_sha256": (decision.get("binding") or {}).get("task_binding_sha256") if isinstance(decision.get("binding"), dict) else None,
        "write_token": (decision.get("binding") or {}).get("write_token") if isinstance(decision.get("binding"), dict) else None,
        "prime_review_exit": record.get("report_exit"),
        "effective": (record.get("report") or {}).get("effective") if isinstance(record.get("report"), dict) else None,
    }
    view["current"] = current
    if current:
        view["next_action"] = action
        view["questions"] = questions
        view["director_replies"] = replies
    else:
        view["historical"] = {
            "review_id": head_id,
            "record_sha256": head["record_sha256"],
            "schema": schema,
            "reason": reason,
            "interpretation": interpretation,
            "next_action": action,
            "questions": questions,
            "director_replies": replies,
        }
        if reason:
            attention.append(f"{view['pass_state']}: {head_id} is historical ({reason})")
    view["attention"] = attention
    return view


def read_view(root: Path, reg_rel: str) -> dict:
    reg = load_registration(root, reg_rel)
    obs = observe_descriptor(root, reg)
    try:
        token = write_token_of(root, reg)
    except Refusal as exc:
        obs = failed_observation(exc.message)
        token = None
    scan = scan_reviews(root, reg)
    return derive(root, reg, obs, token, scan)


def check_judgment(judgment: dict, reg: dict) -> None:
    exact(judgment, JUDGMENT_KEYS, "judgment")
    need(judgment["outcome"] in {"continue", "director-input", "develop", "complete"}, "judgment.outcome must be continue, director-input, develop or complete")
    need(judgment["disposition"] in {"accepted", "held", "correction-required"}, "judgment.disposition must be accepted, held or correction-required")
    need(judgment["pass_terminal"] in {"finished", "open"}, "judgment.pass_terminal must be finished or open")
    goal = judgment["goal"]
    exact(goal, {"terminal", "goal_id", "goal_sha256", "evidence"}, "judgment.goal")
    need(goal["terminal"] in {"open", "completed"}, "judgment.goal.terminal must be open or completed")
    need(
        (goal["goal_id"], goal["goal_sha256"]) == (reg["goal"]["goal_id"], goal_sha(reg["goal"])),
        "judgment.goal must name the registration's current goal_id and goal_sha256",
    )
    need(isinstance(goal["evidence"], list) and all(isinstance(item, str) and item.strip() for item in goal["evidence"]), "judgment.goal.evidence must be a list of strings")
    for key in ("reasons", "source_refs", "unresolved"):
        need(isinstance(judgment[key], list) and all(isinstance(item, str) and item.strip() for item in judgment[key]), f"judgment.{key} must be a list of strings")
    need(isinstance(judgment["finding"], str) and judgment["finding"].strip(), "judgment.finding must be text")
    action = judgment["next_action"]
    if action is not None:
        exact(action, {"action_id", "text", "authorized_in_grant"}, "judgment.next_action")
        need(
            isinstance(action["action_id"], str)
            and LABEL.fullmatch(action["action_id"]) is not None
            and isinstance(action["text"], str)
            and action["text"].strip()
            and action["authorized_in_grant"] in {True, False, None},
            "judgment.next_action has a wrong value",
        )
    need(judgment["semantic_conflict"] is None or isinstance(judgment["semantic_conflict"], bool), "bad type semantic_conflict")
    need(judgment["design_fork"] is None or isinstance(judgment["design_fork"], dict), "bad type design_fork")
    need(isinstance(judgment["holds"], list) and isinstance(judgment["answers"], list), "bad type holds")
    need(isinstance(judgment["sections"], dict), "bad type sections")
    need((judgment["outcome"] == "complete") == (goal["terminal"] == "completed"), "outcome complete if and only if goal.terminal completed")
    if goal["terminal"] == "completed":
        need(judgment["disposition"] == "accepted" and judgment["pass_terminal"] == "finished", "a completed goal needs disposition accepted and pass finished")
        need(goal["evidence"], "a completed goal needs at least one evidence reference")
    if judgment["disposition"] in {"held", "correction-required"}:
        need(judgment["pass_terminal"] == "open" and goal["terminal"] == "open", f"a {judgment['disposition']} review keeps the pass and the goal open")
    if judgment["outcome"] == "director-input":
        need(judgment["disposition"] == "held", "director-input requires disposition held")


def align_supplied(reg: dict, decision: dict) -> None:
    record = decision["supplied_record"]
    need(isinstance(record, dict), "supplied record is missing")
    need(record.get("schema") == "prime-review-record/1", "supplied record schema is not prime-review-record/1")
    need(record.get("agreement") == reg["agreement"], "supplied record does not match the judgment")
    judgment = decision["judgment"]
    supplied = record.get("judgment")
    need(isinstance(supplied, dict), "supplied record does not match the judgment")
    action = judgment["next_action"]["text"] if judgment["next_action"] else None
    pairs = (
        ("outcome", judgment["outcome"], supplied.get("outcome")),
        ("finding", judgment["finding"], supplied.get("finding")),
        ("reasons", judgment["reasons"], supplied.get("reasons")),
        ("sections", judgment["sections"], supplied.get("sections")),
        ("semantic_conflict", judgment["semantic_conflict"], supplied.get("semantic_conflict")),
        ("design_fork", judgment["design_fork"], supplied.get("design_fork")),
        ("next_action", action, supplied.get("next_action")),
    )
    for _name, left, right in pairs:
        need(left == right, "supplied record does not match the judgment")
    sources = record.get("sources")
    need(isinstance(sources, list), "supplied record does not match the measured bytes")
    for source in sources:
        need(isinstance(source, dict) and isinstance(source.get("logical_path"), str), "supplied record does not match the measured bytes")


def measured_files(root: Path, reg: dict) -> dict:
    descriptor = strict_json(read_regular(under(root, reg["descriptor_path"], "descriptor"), "descriptor"), "descriptor")
    rows = {}
    assignment = read_regular(under(root, reg["assignment_path"], "assignment"), "assignment")
    rows[reg["assignment_path"]] = (sha(assignment), len(assignment))
    for item in reg["evidence"]:
        blob = read_regular(under(root, item["logical_path"], item["logical_path"]), item["logical_path"])
        rows[item["logical_path"]] = (sha(blob), len(blob))
    returned = read_regular(under(root, descriptor["return_path"], "return"), "return")
    rows[descriptor["return_path"]] = (sha(returned), len(returned))
    receipt = read_regular(under(root, descriptor["receipt_path"], "receipt"), "receipt")
    return {
        "rows": rows,
        "return_path": descriptor["return_path"],
        "receipt_sha256": sha(receipt),
        "descriptor": descriptor,
    }


def align_sources(root: Path, reg: dict, decision: dict) -> None:
    measured = measured_files(root, reg)
    record = decision["supplied_record"]
    by_path = {}
    for source in record["sources"]:
        by_path[source["logical_path"]] = source
    need(set(by_path) == set(measured["rows"]), "supplied record does not match the measured bytes")
    for path, (digest, size) in measured["rows"].items():
        source = by_path[path]
        need(source.get("content_sha256") == digest and source.get("content_bytes") == size, "supplied record does not match the measured bytes")
    if reg["source_kind"] == "N5NN":
        source = by_path[measured["return_path"]]
        identity = source.get("identity")
        need(source.get("kind") == "capture" and isinstance(identity, dict), "supplied record does not match the measured bytes")
        need(identity.get("schema") == "return-capture/1", "supplied record does not match the measured bytes")
        need(identity.get("member") == reg["address"]["member"], "supplied record does not match the measured bytes")
        need(identity.get("submission_id") == reg["submission_id"], "supplied record does not match the measured bytes")
        need(identity.get("receipt_sha256") == measured["receipt_sha256"], "supplied record does not match the measured bytes")
        origin = identity.get("origin")
        need(
            isinstance(origin, dict)
            and origin.get("book") == BOOK
            and origin.get("page") == reg["page_id"]
            and origin.get("batch") == reg["pass"],
            "origin does not match the source",
        )
    else:
        need(all(item.get("kind") != "capture" for item in record["sources"]), "N7NN must not use an N1NN capture member")


def binding_diff(fresh: dict, stored: dict) -> str | None:
    if fresh["task_binding_sha256"] != stored.get("task_binding_sha256"):
        return "task binding changed since read"
    if fresh["direction"] != stored.get("direction"):
        return "direction changed since read"
    if fresh["goal"] != stored.get("goal"):
        return "goal changed since read"
    keys = (
        "schema",
        "work_id",
        "page",
        "pass",
        "source",
        "member",
        "origin",
        "receipt_sha256",
        "submission_id",
        "return_sha256",
        "manifest_sha256",
        "agreement_sha256",
    )
    changed = [key for key in keys if fresh.get(key) != stored.get(key)]
    if changed:
        return "source changed since read: " + ", ".join(changed)
    if fresh["fingerprint"] != stored.get("fingerprint"):
        return "binding fingerprint does not match the current observation"
    return None


def project_markdown(reg: dict, decision: dict, record_sha: str, report: dict) -> bytes:
    judgment = decision["judgment"]
    action = judgment["next_action"]["text"] if judgment["next_action"] else "none"
    lines = [
        f"# Prime cycle review {decision['review_id']}",
        "",
        f"Readable projection of record.json (sha256 {record_sha}). This file is not the in-page review and it is not approval.",
        "",
        f"- page: {reg['page_id']} pass {reg['pass']}",
        f"- task binding: {decision['binding']['task_binding_sha256']}",
        f"- write token: {decision['binding']['write_token']['sha256']}",
        f"- disposition: {judgment['disposition']}; outcome: {judgment['outcome']}",
        f"- next action: {action}",
        f"- prime_review effective: {report.get('effective')}; closes_work false; authority none",
        "",
    ]
    return ("\n".join(lines)).encode("utf-8")


def record_review(root: Path, reg_rel: str, decision_rel: str, envelope_rel: str) -> dict:
    reg = load_registration(root, reg_rel)
    decision = strict_json(read_regular(under(root, decision_rel, "decision"), "decision"), "decision")
    exact(decision, DECISION_KEYS, "decision")
    need(decision["schema"] == "prime-cycle-decision/3", "decision schema is not prime-cycle-decision/3")
    need(isinstance(decision["review_id"], str) and LABEL.fullmatch(decision["review_id"]) is not None, "review_id must be a label")
    exact(decision["attribution"], {"actor_label", "role", "evidence"}, "attribution")
    need(isinstance(decision["attribution"]["actor_label"], str) and decision["attribution"]["actor_label"].strip(), "attribution.actor_label is required")
    need(decision["attribution"]["role"] == "prime", "attribution.role must be prime")
    exact(decision["binding"], BINDING_KEYS, "binding")
    need(decision["binding"]["schema"] == "prime-cycle-binding/3", "binding schema is not prime-cycle-binding/3")
    check_judgment(decision["judgment"], reg)
    scan = scan_reviews(root, reg)
    target = review_root(root, reg) / decision["review_id"]
    if target.exists() and decision["review_id"] in scan["committed"]:
        stored = scan["committed"][decision["review_id"]]["record"]["decision"]
        need(canonical(stored) == canonical(decision), "conflict: a different review is already committed under this review_id")
        stored_binding = stored.get("binding") if isinstance(stored.get("binding"), dict) else {}
        return {
            "schema": "prime-cycle-record-result/1",
            "result": "already-recorded",
            "review_id": decision["review_id"],
            "record_sha256": scan["committed"][decision["review_id"]]["record_sha256"],
            "prime_review_exit": scan["committed"][decision["review_id"]]["record"].get("report_exit"),
            "already_recorded": True,
            "render_state": render_state_of(
                root,
                reg,
                decision["review_id"],
                write_token_of(root, reg),
                stored_binding.get("task_binding_sha256"),
            ),
            "custody": "not-established",
            "allocated": False,
            "closes_work": False,
            "releases_action": False,
            "authenticates_actor": False,
            "authority": "none",
        }
    if target.exists():
        raise Refusal(f"partial review present at {decision['review_id']}; record under a new review_id with recovers")
    obs = observe_descriptor(root, reg)
    need(obs["state"] == "complete", f"observation is not complete: {obs['state']}" + (f": {obs['reason']}" if obs["reason"] else ""))
    token = write_token_of(root, reg)
    need(token is not None, "review home is absent")
    prior, _heads = prior_of(scan)
    need(prior != "fork", "lineage-fork: more than one committed head")
    need(decision["binding"]["expected_prior"] == prior, "expected_prior does not equal the latest committed review")
    if prior is None:
        need(decision["supersedes"] is None, "supersedes names a review that is not the latest committed review")
    else:
        need(decision["supersedes"] == prior, "a review over an existing one must set supersedes to that review")
    if decision["recovers"] is not None:
        need(any(item["review_id"] == decision["recovers"] for item in scan["partial"]), "recovers must name a partial review directory")
    fresh_digest = bind_digest(root, reg, obs)
    fresh = make_binding(reg, obs, fresh_digest, token, decision["binding"]["expected_prior"])
    diff = binding_diff(fresh, decision["binding"])
    need(diff is None, diff or "binding fingerprint does not match the current observation")
    need(fresh["write_token"] == decision["binding"]["write_token"], "write token changed since read")
    need(decision["binding"]["receipt_sha256"] is not None or decision["judgment"]["disposition"] != "accepted", "an accepted review needs a bound return")
    align_supplied(reg, decision)
    align_sources(root, reg, decision)
    envelope_bytes = read_regular(under(root, envelope_rel, "envelope"), "envelope")
    envelope = strict_json(envelope_bytes, "envelope")
    need(envelope.get("record") == decision["supplied_record"], "envelope record does not match the supplied record")
    need(envelope.get("target") == reg["target"], "target is not the derived review destination")
    record_file = root / "scratch" / "supplied-record.json"
    record_file.parent.mkdir(exist_ok=True)
    record_file.write_bytes(canonical(decision["supplied_record"]))
    proc = run_tool(REVIEW02, ["report", "--input", str(record_file), "--json"])
    if proc.returncode == 2:
        detail = (proc.stderr.decode("utf-8", "replace") + proc.stdout.decode("utf-8", "replace")).strip()
        raise Refusal("prime_review refused the review: " + detail[:600])
    need(proc.returncode in {0, 1}, "prime_review refused the review")
    report = json.loads(proc.stdout.decode("utf-8"))
    if decision["judgment"]["goal"]["terminal"] == "completed":
        need(report.get("effective") == "complete-as-supplied", f"a completed goal needs prime_review effective complete-as-supplied (got {report.get('effective')})")
    summary = {
        "effective": report.get("effective"),
        "holds": report.get("holds"),
        "attention": report.get("attention"),
        "closes_work": False,
        "authority": "none",
    }
    body = {
        "schema": "prime-cycle-review/3",
        "work_id": reg["work_id"],
        "review_id": decision["review_id"],
        "decision": decision,
        "report": summary,
        "report_exit": proc.returncode,
        "tools": pins(),
        "lineage": {"supersedes": decision["supersedes"], "recovers": decision["recovers"]},
        "note": "work-local review record; REVIEW.md is its readable projection; the in-page review is a separate render; COMMITTED.json marks the record usable",
    }
    record_bytes = canonical(body)
    markdown = project_markdown(reg, decision, sha(record_bytes), summary)
    need(len(record_bytes) + len(markdown) + len(envelope_bytes) <= reg["bounds"]["max_output_bytes"], "review is over max_output_bytes")
    base = review_root(root, reg)
    base.mkdir(parents=True, exist_ok=True)
    need(not is_link(base), "review location is a link")
    os.mkdir(target)
    try:
        (target / "record.json").write_bytes(record_bytes)
        (target / "REVIEW.md").write_bytes(markdown)
        (target / "envelope.json").write_bytes(envelope_bytes)
        marker = canonical({"record_sha256": sha(record_bytes), "review_md_sha256": sha(markdown)})
        (target / "COMMITTED.json").write_bytes(marker)
    except OSError as exc:
        raise Refusal(f"write failed in {decision['review_id']}: {type(exc).__name__}: {exc}; files so far are kept") from None
    return {
        "schema": "prime-cycle-record-result/1",
        "result": "recorded",
        "review_id": decision["review_id"],
        "record_sha256": sha(record_bytes),
        "prime_review_exit": proc.returncode,
        "effective": report.get("effective"),
        "already_recorded": False,
        "render_state": "pending",
        "custody": "not-established",
        "allocated": False,
        "closes_work": False,
        "releases_action": False,
        "authenticates_actor": False,
        "authority": "none",
    }


def inspect_reviews(root: Path, reg_rel: str) -> dict:
    reg = load_registration(root, reg_rel)
    scan = scan_reviews(root, reg)
    base = review_root(root, reg)
    rows = []
    if base.exists():
        for entry in sorted(base.iterdir(), key=lambda item: item.name):
            if not entry.is_dir():
                continue
            files = {}
            for path in sorted(entry.iterdir(), key=lambda item: item.name):
                if path.is_file():
                    blob = path.read_bytes()
                    files[path.name] = {"bytes": len(blob), "sha256": sha(blob)}
            if entry.name in scan["committed"]:
                phase = "committed"
            else:
                phase = next((item["phase"] for item in scan["partial"] + scan["invalid"] if item["review_id"] == entry.name), "invalid")
            rows.append({"review_id": entry.name, "phase": phase, "files": files})
    return {
        "schema": "prime-cycle-inspect/1",
        "work_id": reg["work_id"],
        "reviews": rows,
        "recovery": "never edit or delete a partial; record again under a new review_id with recovers set to the partial id",
        "custody": "not-established",
        "allocated": False,
        "closes_work": False,
        "releases_action": False,
        "authenticates_actor": False,
        "authority": "none",
    }


def emit(payload: dict) -> None:
    data = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        buffer.write(data)
    else:
        sys.stdout.write(data.decode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="prime_cycle.py")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("read", "inspect"):
        command = sub.add_parser(name)
        command.add_argument("--fixture-root", required=True)
        command.add_argument("--registration", required=True)
    record = sub.add_parser("record")
    record.add_argument("--fixture-root", required=True)
    record.add_argument("--registration", required=True)
    record.add_argument("--decision", required=True)
    record.add_argument("--envelope", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 2
    try:
        pins()
        root = fixture_root(args.fixture_root)
        if args.command == "read":
            emit(read_view(root, args.registration))
            return 0
        if args.command == "inspect":
            emit(inspect_reviews(root, args.registration))
            return 0
        result = record_review(root, args.registration, args.decision, args.envelope)
        emit(result)
        if result.get("result") == "recorded" and result.get("prime_review_exit") == 1:
            return 1
        return 0
    except Refusal as exc:
        emit({
            "schema": "prime-cycle-refusal/1",
            "rule": exc.message,
            "custody": "not-established",
            "allocated": False,
            "closes_work": False,
            "releases_action": False,
            "authenticates_actor": False,
            "authority": "none",
        })
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
