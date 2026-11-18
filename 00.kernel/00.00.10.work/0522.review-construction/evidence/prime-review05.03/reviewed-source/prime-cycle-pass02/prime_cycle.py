#!/usr/bin/env python3
"""Focused successor of labs/prime-cycle-pass01/prime_cycle.py.

Base sha256 19ede9c2125307595d0be867bae1a3cb71bf3db0515ad83e7c04d3333e17861d, 77846 bytes.
Delta: registration/2, decision/3, and review/3. A /3 fingerprint is the
review-task-binding/2 digest plus origin, member, direction, and goal.
The review-home hash is a write token and is outside that fingerprint.
/1 stays legacy. /2 keeps the historical whole-page rule and is not upgraded.
Packet, day, and live return observation are not copied. This module does not
call return_capture.py. It does not approve, release, close, or allocate.
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
CONSTRUCT = ROOT / "labs" / "review-construction-pass01" / "construct.py"
CONSTRUCT_SHA = "8b9d4a6eda460f594404042f7ee232a7ac55fcc09af38905de364defa189ea8a"
CONSTRUCT_BYTES = 35956
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
    self_bytes = Path(__file__).read_bytes()
    return {
        "construct": {"path": "labs/review-construction-pass01/construct.py", "sha256": CONSTRUCT_SHA, "bytes": CONSTRUCT_BYTES},
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
        "prime_cycle_pass02": {
            "path": "labs/prime-cycle-pass02/prime_cycle.py",
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
        route = "page-local-colab"
    need(reg["target"] == destination, "target is not the derived review destination")
    return {
        "book": BOOK,
        "page": page_id,
        "pass": pass_id,
        "member": member,
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
        exact(raw, DESC_KEYS, "descriptor")
        need(raw["schema"] == "return-line-descriptor/1", "bad descriptor schema")
        exact(raw["origin"], {"book", "page", "batch"}, "origin")
        exact(raw["verification"], {"tool_path", "tool_sha256", "result", "evidence_path"}, "verification")
    except Refusal as exc:
        obs = failed_observation(exc.message)
        obs["member"] = address["member"]
        return obs
    obs = failed_observation(None)
    obs["descriptor_state"] = raw["state"]
    obs["origin"] = raw["origin"]
    obs["member"] = address["member"]
    obs["route"] = raw["route"]
    obs["submission_id"] = raw["submission_id"] if isinstance(raw["submission_id"], str) else None
    if raw["state"] not in {"complete", "reserved", "incomplete", "conflict"}:
        obs["reason"] = "descriptor state is not a known state"
        return obs
    if raw["route"] not in {"matched-workflow-return-line", "page-local-colab"}:
        obs["reason"] = "descriptor route is not a known route"
        return obs
    if raw["custody_format"] not in {"return-line-capture/1", "legacy-relocated/1"}:
        obs["reason"] = "descriptor custody_format is not a known format"
        return obs
    reasons = []
    if raw["route"] != address["route"]:
        reasons.append("route does not match the source")
    origin = raw["origin"]
    if origin.get("book") != BOOK or origin.get("page") != address["page"] or origin.get("batch") != address["pass"]:
        reasons.append("origin does not match the source")
    if raw["target_page"] != address["destination"]:
        reasons.append("target_page is not the derived review destination")
    if raw["submission_id"] != reg["submission_id"]:
        reasons.append("submission_id does not match the registration")
    measured = null_measure()
    receipt_sha, receipt_len, receipt_err = hash_or_none(under(root, raw["receipt_path"], "receipt"))
    return_sha, return_len, return_err = hash_or_none(under(root, raw["return_path"], "return"))
    manifest_sha, manifest_len, manifest_err = hash_or_none(under(root, raw["manifest_path"], "manifest"))
    custody_sha, _custody_len, custody_err = hash_or_none(under(root, raw["custody_path"], "custody"))
    evidence_path = raw["verification"]["evidence_path"]
    evidence_err = None
    if isinstance(evidence_path, str) and evidence_path != "":
        try:
            logical_path(evidence_path, "verification.evidence_path")
            _e_sha, _e_len, evidence_err = hash_or_none(under(root, evidence_path, "verification evidence"))
        except Refusal as exc:
            evidence_err = exc.message
    else:
        evidence_err = "absent"
    measured.update(
        receipt_sha256=receipt_sha,
        receipt_bytes=receipt_len,
        return_sha256=return_sha,
        return_bytes=return_len,
        manifest_sha256=manifest_sha,
        manifest_bytes=manifest_len,
        custody_present=custody_err is None,
        verification_present=evidence_err is None,
    )
    obs["measured"] = measured
    obs["receipt_sha256"] = receipt_sha
    obs["return_sha256"] = return_sha
    obs["return_bytes"] = return_len
    obs["manifest_sha256"] = manifest_sha
    obs["manifest_bytes"] = manifest_len
    if reasons:
        obs["state"] = "conflict"
        obs["reason"] = reasons[0]
        return obs
    if raw["state"] == "reserved":
        obs["state"] = "reserved"
        obs["reason"] = "descriptor state is reserved"
        return obs
    if raw["state"] == "incomplete":
        obs["state"] = "incomplete"
        obs["reason"] = "descriptor state is incomplete"
        return obs
    if raw["state"] == "conflict":
        obs["state"] = "conflict"
        obs["reason"] = "descriptor state is conflict"
        return obs
    byte_reasons = []
    if receipt_err or receipt_sha != raw["receipt_sha256"]:
        byte_reasons.append("receipt bytes do not match the descriptor")
    if return_err or return_sha != raw["return_sha256"] or return_len != raw["return_bytes"]:
        byte_reasons.append("return bytes do not match the descriptor")
    if manifest_err:
        byte_reasons.append("manifest bytes are not a regular file")
    if custody_err:
        byte_reasons.append("custody path is not a regular file")
    if evidence_err:
        byte_reasons.append("verification evidence is not a regular file")
    if byte_reasons:
        obs["state"] = "conflict"
        obs["reason"] = byte_reasons[0]
        obs["receipt_sha256"] = receipt_sha
        return obs
    obs["state"] = "complete"
    obs["reason"] = None
    return obs


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
