#!/usr/bin/env python3
"""05.14 staged successor of labs/review-loop-pass03/review_loop.py.

The live pass03 file stays unchanged. This copy pins the 05.14 prime_cycle
successor. An N7 registration whose derived review file is absent may commit,
and render creates that one file through the pinned constructor. A file that
appears after the read is left in place.

Orchestrate a described return into a full in-page Prime review.

Successor of labs/review-loop-pass02/review_loop.py
sha256 8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7, 47189 bytes.
Uses pinned constructor pass04 for inspect, apply, show, and the pre-apply
bind. The unchanged cycle still calls constructor pass02 for its own bind.
This module does not edit those tools. It does not approve, release, close,
allocate, or establish custody. prepare may exit 0 with full_success false.
A rendered review is not approval. describe-legacy only reads. reproduce is
outside this slice and delegates to the pinned pass02 loop.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
CONTRACT = "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.08/CONTRACT.md"
CONSTRUCT = ROOT / "labs" / "review-construction-pass04" / "construct.py"
CONSTRUCT_SHA = "6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20"
CONSTRUCT_BYTES = 42582
LOOP02 = ROOT / "labs" / "review-loop-pass02" / "review_loop.py"
LOOP02_SHA = "8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7"
LOOP02_BYTES = 47189
REVIEW01 = ROOT / "labs" / "prime-review-pass01" / "prime_review.py"
REVIEW01_SHA = "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0"
REVIEW01_BYTES = 58324
REVIEW02 = ROOT / "labs" / "prime-review-pass02" / "prime_review.py"
REVIEW02_SHA = "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"
REVIEW02_BYTES = 58560
CYCLE = ROOT / "labs" / "n7-first-review-pass01" / "prime_cycle.py"
CYCLE_SHA = "b664c2c989a132108aa236ea6885e2503cf0dca266a12538ebe0b26cf9dba81d"
CYCLE_BYTES = 77501
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
BOOK = "00.00.10.work"
LIVE_BOOK = ROOT / "00.kernel" / "00.00.10.work"
EVIDENCE = LIVE_BOOK / "0522.review-construction" / "evidence" / "build05.08"
REPARSE = 0x400


class Refusal(Exception):
    def __init__(self, message: str, code: str | None = None, extra: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.extra = extra or {}


def need(cond: bool, message: str) -> None:
    if not cond:
        raise Refusal(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


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


def logical_path(value: str, where: str) -> str:
    need(isinstance(value, str) and value.strip() != "", f"empty path {where}")
    need("\\" not in value and not value.startswith("/") and not value.startswith("//"), f"unsafe path {where}")
    need(re.match(r"^[A-Za-z]:", value) is None, f"unsafe path {where}")
    parts = value.split("/")
    need(all(part not in ("", ".", "..") for part in parts), f"unsafe path {where}")
    return value


def under(root: Path, text: str, where: str) -> Path:
    logical_path(text, where)
    resolved = (root / Path(text)).resolve()
    need(is_inside(resolved, root.resolve()), f"path escapes fixture root {where}")
    return resolved


def read_regular(path: Path, where: str) -> bytes:
    need(os.path.lexists(path), f"missing file {where}")
    need(not is_link(path), f"symlink refused {where}")
    need(path.is_file(), f"not a regular file {where}")
    return path.read_bytes()


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


def pin_file(path: Path, digest: str, size: int, label: str) -> dict:
    data = path.read_bytes()
    need(len(data) == size and sha(data) == digest, f"pinned tool hash does not match: {label}")
    return {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": digest, "bytes": size}


def pin_set() -> dict:
    self_bytes = Path(__file__).read_bytes()
    return {
        "construct": pin_file(CONSTRUCT, CONSTRUCT_SHA, CONSTRUCT_BYTES, "construct"),
        "prime_review_pass01": pin_file(REVIEW01, REVIEW01_SHA, REVIEW01_BYTES, "prime_review_pass01"),
        "prime_review_pass02": pin_file(REVIEW02, REVIEW02_SHA, REVIEW02_BYTES, "prime_review_pass02"),
        "prime_cycle_pass03": pin_file(CYCLE, CYCLE_SHA, CYCLE_BYTES, "prime_cycle_pass03"),
        "return_lines": pin_file(LINES, LINES_SHA, LINES_BYTES, "return_lines"),
        "return_placement": pin_file(PLACEMENT, PLACEMENT_SHA, PLACEMENT_BYTES, "return_placement"),
        "return_inspect": pin_file(INSPECT, INSPECT_SHA, INSPECT_BYTES, "return_inspect"),
        "review_loop": {
            "path": "labs/n7-first-review-pass01/review_loop.py",
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


def load_request(root: Path, rel: str) -> tuple[dict, dict, bytes]:
    raw_bytes = read_regular(under(root, rel, "request"), "request")
    raw = strict_json(raw_bytes, "request")
    need(isinstance(raw, dict) and set(raw) == {"schema", "registration_path"}, "request keys are not review-loop-request/1")
    need(raw["schema"] == "review-loop-request/1", "bad request schema")
    logical_path(raw["registration_path"], "registration_path")
    registration = strict_json(
        read_regular(under(root, raw["registration_path"], "registration"), "registration"),
        "registration",
    )
    return raw, registration, raw_bytes


def cycle_call(root: Path, args: list[str]) -> tuple[int, dict, str]:
    proc = run_tool(CYCLE, [*args, "--fixture-root", str(root)])
    text = proc.stdout.decode("utf-8", "replace")
    try:
        payload = json.loads(text) if text.strip() else {}
    except json.JSONDecodeError:
        payload = {"schema": "prime-cycle-refusal/1", "rule": "cycle stdout is not json"}
    err = proc.stderr.decode("utf-8", "replace").strip()
    return proc.returncode, payload, err


def construct_call(root: Path, args: list[str]) -> subprocess.CompletedProcess:
    return run_tool(CONSTRUCT, [*args, "--fixture-root", str(root)])


def flags(view: dict) -> dict:
    return {
        "custody": "not-established",
        "allocated": False,
        "closes_work": False,
        "releases_action": False,
        "authenticates_actor": False,
        "authority": "none",
        "accepted": False,
    }


def supplied_action(view: dict) -> dict | None:
    action = None
    if isinstance(view, dict):
        action = view.get("next_action")
        if not isinstance(action, dict) and isinstance(view.get("historical"), dict):
            action = view["historical"].get("next_action")
    if not isinstance(action, dict):
        return None
    return {
        "action_id": action.get("action_id"),
        "text": action.get("text"),
        "authorized_in_grant": action.get("authorized_in_grant"),
    }


def wrap(command: str, request_sha: str, view: dict, *, full_success: bool, exit_code: int, extra: dict | None = None) -> dict:
    latest = view.get("latest_review") if isinstance(view, dict) else None
    supplied = extra or {}
    guide = supplied.get("mechanical") if isinstance(supplied.get("mechanical"), dict) else None
    payload = {
        "schema": "review-loop-result/2",
        "command": command,
        "full_success": full_success,
        "exit_code": exit_code,
        "request_sha256": request_sha,
        "pins": pin_set(),
        "contract": CONTRACT,
        "observation": view.get("observation") if isinstance(view, dict) else None,
        "supplied_judgment": None,
        "current": {
            "pass_state": view.get("pass_state") if isinstance(view, dict) else None,
            "render_state": view.get("render_state") if isinstance(view, dict) else None,
            "current": view.get("current") if isinstance(view, dict) else False,
            "interpretation": view.get("interpretation") if isinstance(view, dict) else None,
            "task_binding_sha256": view.get("task_binding_sha256") if isinstance(view, dict) else None,
            "write_token": view.get("write_token") if isinstance(view, dict) else None,
            "next_action": view.get("next_action") if isinstance(view, dict) else None,
            "next_action_label": "supplied",
            "questions": view.get("questions") if isinstance(view, dict) else [],
            "director_replies": view.get("director_replies") if isinstance(view, dict) else [],
            "latest_review": latest,
        },
        "historical": view.get("historical") if isinstance(view, dict) else None,
        "supplied_next_action": supplied_action(view),
        "mechanical": guide,
        "next": guide.get("text") if isinstance(guide, dict) else None,
        "pass_state": view.get("pass_state") if isinstance(view, dict) else None,
        "view": view,
    }
    payload.update(flags(view))
    if extra:
        payload.update(extra)
        guide = payload.get("mechanical") if isinstance(payload.get("mechanical"), dict) else None
        payload["next"] = guide.get("text") if isinstance(guide, dict) else None
        payload["supplied_next_action"] = supplied_action(view)
    return payload


def receipt_of(reg: dict, descriptor: dict) -> dict:
    if reg["source_kind"] == "N5NN":
        page_id = reg["page_id"]
        match = re.fullmatch(r"([0-9])5(\d\d)\.([a-z0-9][a-z0-9-]*)", page_id)
        need(match is not None, "page does not match N5NN")
        member = f"{match.group(1)}1{match.group(2)}.{match.group(3)}"
        placement = "n5nn-matching-line"
        page_local = None
    else:
        member = None
        placement = "n7nn-page-local"
        page_local = f"05.{reg['pass'].split('.', 1)[1]}.return.md"
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


def refuse(code: str, detail: str) -> None:
    raise Refusal(f"{code}: {detail}", code=code)


def supplied_state_of(decision: dict) -> dict:
    judgment = decision.get("judgment") if isinstance(decision, dict) else None
    if not isinstance(judgment, dict):
        refuse("supplied-state", "committed decision has no judgment object")
    goal = judgment.get("goal") if isinstance(judgment.get("goal"), dict) else {}
    return {
        "schema": "supplied-review-state/1",
        "source": "cycle decision judgment",
        "disposition": judgment.get("disposition"),
        "pass_terminal": judgment.get("pass_terminal"),
        "goal_terminal": goal.get("terminal"),
        "outcome": judgment.get("outcome"),
    }


def build_envelope(root: Path, reg: dict, record: dict, expect: str, decision: dict) -> dict:
    descriptor = strict_json(
        read_regular(under(root, reg["descriptor_path"], "descriptor"), "descriptor"),
        "descriptor",
    )
    return {
        "schema": "review-construction/2",
        "source_kind": reg["source_kind"],
        "page": reg["kernel_page"],
        "pass": reg["pass"],
        "target": reg["target"],
        "expect_sha256": expect,
        "permit_create": False,
        "review_identity": reg["review_identity"],
        "task": {"task_id": reg["task_id"], "assignment_path": reg["assignment_path"]},
        "evidence": reg["evidence"],
        "agreement": reg["agreement"],
        "receipt": receipt_of(reg, descriptor),
        "record": record,
        "supplied_review_state": supplied_state_of(decision),
    }


def write_scratch(root: Path, name: str, payload: dict) -> str:
    scratch = root / "scratch"
    scratch.mkdir(exist_ok=True)
    rel = f"scratch/{name}"
    under(root, rel, name).write_bytes(canonical(payload))
    return rel


def read_cycle(root: Path, registration: str) -> dict:
    code, view, err = cycle_call(root, ["read", "--registration", registration])
    if code != 0:
        rule = view.get("rule") if isinstance(view, dict) else None
        raise Refusal(rule or err or "cycle read refused")
    return view


def page_hash(root: Path, target: str) -> tuple[str, int]:
    blob = read_regular(under(root, target, "target"), "target")
    return sha(blob), len(blob)


def parse_tool(proc: subprocess.CompletedProcess, code: str, label: str) -> dict:
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        if detail.startswith("refused: "):
            detail = detail[len("refused: "):]
        refuse(code, detail or f"{label} refused")
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refusal(f"{code}: {label} stdout is not json", code=code) from exc
    if not isinstance(payload, dict):
        refuse(code, f"{label} stdout is not an object")
    return payload


def binding_for(view: dict) -> str | None:
    latest = view.get("latest_review") if isinstance(view, dict) else None
    if isinstance(latest, dict) and isinstance(latest.get("task_binding_sha256"), str):
        return latest["task_binding_sha256"]
    template = view.get("template") if isinstance(view, dict) else None
    if isinstance(template, dict) and isinstance(template.get("binding"), dict):
        digest = template["binding"].get("task_binding_sha256")
        if isinstance(digest, str):
            return digest
    if isinstance(view, dict) and isinstance(view.get("task_binding_sha256"), str):
        return view["task_binding_sha256"]
    return None


def inspect_target(root: Path, target: str, binding: str | None) -> dict:
    args = ["inspect", "--target", target]
    if isinstance(binding, str) and binding:
        args.extend(["--binding", binding])
    payload = parse_tool(construct_call(root, args), "target-inspection", "constructor inspect")
    if payload.get("schema") != "review-target-inspection/1":
        refuse("target-inspection", "constructor inspect returned an unexpected schema")
    return payload


def bind_envelope(root: Path, rel: str) -> str:
    payload = parse_tool(construct_call(root, ["bind", "--input", rel]), "binding", "constructor bind")
    if payload.get("schema") != "review-task-binding/2" or payload.get("target_read") is not False:
        refuse("binding", "constructor bind returned an unexpected result")
    digest = payload.get("binding_sha256")
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        refuse("binding", "constructor bind returned no task binding")
    return digest


def review_directory(root: Path, reg: dict, view: dict) -> str | None:
    latest = view.get("latest_review") if isinstance(view, dict) else None
    if isinstance(latest, dict) and isinstance(latest.get("directory"), str):
        return latest["directory"]
    expected = f"{reg['review_location']}/{reg['pass']}-{reg['review_identity']}"
    path = under(root, expected, "review directory")
    if os.path.lexists(path):
        return expected
    return None


def load_coded(root: Path, rel: str, code: str):
    path = under(root, rel, rel)
    if not os.path.lexists(path):
        refuse(code, f"missing {rel}")
    try:
        data = read_regular(path, rel)
        value = strict_json(data, rel)
    except Refusal as exc:
        raise Refusal(f"{code}: {exc.message}", code=code) from exc
    return data, value


def witness_envelope(root: Path) -> dict | None:
    path = root / "scratch" / "envelope.json"
    if not os.path.lexists(path):
        return None
    _data, value = load_coded(root, "scratch/envelope.json", "downgrade")
    if not isinstance(value, dict):
        refuse("downgrade", "scratch envelope witness is not an object")
    return value


def classify_supplied(envelope: dict, decision: dict, witness: dict | None) -> str:
    schema = envelope.get("schema")
    if schema == "review-construction/2":
        if envelope.get("supplied_review_state") != supplied_state_of(decision):
            refuse("supplied-state", "envelope supplied_review_state differs from the hash-verified committed decision")
        if witness is not None and (
            witness.get("schema") != "review-construction/2"
            or witness.get("supplied_review_state") != envelope.get("supplied_review_state")
        ):
            refuse("downgrade", "scratch witness does not agree with the stored /2 envelope")
        return "verified-against-committed-record"
    if schema == "review-construction/1":
        if "supplied_review_state" in envelope:
            refuse("downgrade", "a /1 envelope still carries supplied review state")
        if witness is not None and (
            witness.get("schema") != "review-construction/1" or "supplied_review_state" in witness
        ):
            refuse(
                "downgrade",
                "a newly recorded /2 envelope does not become legacy when supplied state is removed",
            )
        return "legacy-/1-envelope: no supplied state is rendered"
    refuse("envelope", "unknown envelope schema")
    return "not-established"


def assert_measured(measured: str, committed: str, view_hash) -> None:
    if measured != committed or (isinstance(view_hash, str) and measured != view_hash):
        refuse("source-change", "measured task binding does not match the hash-verified committed decision")


def verify_committed(root: Path, reg: dict, view: dict, directory: str) -> dict:
    record_bytes, record = load_coded(root, f"{directory}/record.json", "record-hash")
    _marker_bytes, committed = load_coded(root, f"{directory}/COMMITTED.json", "record-hash")
    _envelope_bytes, envelope = load_coded(root, f"{directory}/envelope.json", "envelope-record")
    if not isinstance(record, dict) or not isinstance(committed, dict) or not isinstance(envelope, dict):
        refuse("record-hash", "committed review files are not objects")
    digest = sha(record_bytes)
    if committed.get("record_sha256") != digest:
        refuse("record-hash", "record.json does not hash to COMMITTED.json")
    latest = view.get("latest_review") if isinstance(view, dict) else None
    if not isinstance(latest, dict) or latest.get("record_sha256") != digest:
        refuse("record-hash", "record.json is not the record the cycle read names")
    decision = record.get("decision") if isinstance(record.get("decision"), dict) else {}
    expected_id = f"{reg['pass']}-{reg['review_identity']}"
    if envelope.get("review_identity") != reg.get("review_identity"):
        refuse("review-identity", "envelope review_identity differs from the registration")
    if not (
        record.get("review_id") == decision.get("review_id") == latest.get("review_id") == expected_id
    ):
        refuse("review-identity", f"record, decision and cycle read do not all name {expected_id}")
    decision_binding = decision.get("binding") if isinstance(decision.get("binding"), dict) else {}
    committed_hash = decision_binding.get("task_binding_sha256")
    if committed_hash != latest.get("task_binding_sha256"):
        refuse("binding", "committed decision binding differs from the cycle read's latest review")
    view_hash = view.get("task_binding_sha256") if isinstance(view, dict) else None
    if isinstance(view_hash, str) and view_hash != committed_hash:
        refuse("binding", "current cycle view task binding differs from the committed decision")
    if envelope.get("record") != decision.get("supplied_record"):
        refuse("envelope-record", "envelope record is not the committed supplied record")
    if (envelope.get("target"), envelope.get("pass")) != (reg.get("target"), reg.get("pass")):
        refuse("envelope-target", "envelope target or pass differs from the registration")
    state = classify_supplied(envelope, decision, witness_envelope(root))
    measured = bind_envelope(root, f"{directory}/envelope.json")
    task = envelope.get("task") if isinstance(envelope.get("task"), dict) else {}
    if task.get("task_id") != reg.get("task_id") or task.get("assignment_path") != reg.get("assignment_path"):
        refuse("task-identity", "envelope task identity differs from the registration")
    if envelope.get("agreement") != reg.get("agreement"):
        refuse("agreement", "envelope agreement differs from the registration")
    if envelope.get("evidence") != reg.get("evidence"):
        refuse("evidence", "envelope evidence differs from the registration")
    descriptor = strict_json(
        read_regular(under(root, reg["descriptor_path"], "descriptor"), "descriptor"),
        "descriptor",
    )
    if envelope.get("receipt") != receipt_of(reg, descriptor):
        refuse("receipt", "envelope receipt differs from the registration")
    assert_measured(measured, committed_hash, view_hash)
    return {
        "verified": True,
        "record_sha256": digest,
        "review_id": expected_id,
        "supplied_state": state,
        "measured_binding_sha256": measured,
        "not_established": ["Director acceptance", "release", "authenticated identity"],
    }


def mechanical(view: dict, inspection: dict | None, failed: Refusal | None = None) -> dict:
    pass_state = view.get("pass_state") if isinstance(view, dict) else None
    render_state = view.get("render_state") if isinstance(view, dict) else None
    latest = view.get("latest_review") if isinstance(view, dict) and isinstance(view.get("latest_review"), dict) else {}
    current = (view.get("write_token") or {}).get("sha256") if isinstance(view, dict) and isinstance(view.get("write_token"), dict) else None
    recorded = (latest.get("write_token") or {}).get("sha256") if isinstance(latest.get("write_token"), dict) else None
    target = (inspection or {}).get("state") if isinstance(inspection, dict) else None

    def out(state: str, route: str, text: str, blocker: str | None = None, extra: dict | None = None) -> dict:
        body = {"state": state, "blocker": blocker, "route": route, "text": text, "target": target}
        if extra:
            body.update(extra)
        return body

    if failed is not None:
        return out(
            "committed-record-mismatch",
            "none-in-this-entry",
            "The committed record is not established.",
            failed.code,
            {"detail": failed.message},
        )
    if pass_state == "awaiting-review":
        if target == "pending":
            return out("awaiting-review", "record", "Supply the typed judgment, then record.")
        if target in {"existing-review", "unsupported", "constructed-same-binding"}:
            return out(
                "awaiting-review",
                "record-then-blocked",
                "Recording preserves the judgment; rendering into this target will be refused.",
                f"target-{target}",
            )
        if target == "absent":
            token = view.get("write_token") if isinstance(view.get("write_token"), dict) else {}
            if token.get("state") == "absent-create":
                return out(
                    "awaiting-review",
                    "record",
                    "Supply the typed judgment, then record. The declared review file stays absent until authorized render.",
                )
            return out(
                "awaiting-review",
                "none-in-this-entry",
                "No judgment is recorded. The target is absent, so this entry does not commit one.",
                "target-absent",
            )
        return out("unknown-state", "none-in-this-entry", "The mechanical state is not established.", "target-not-inspected")
    if render_state == "conflict":
        return out(
            "existing-review-conflict",
            "none-in-this-entry",
            "The judgment is retained. The existing review was not overwritten.",
            "existing-review",
        )
    if render_state == "pending":
        live_token = view.get("write_token") if isinstance(view.get("write_token"), dict) else {}
        recorded_token = latest.get("write_token") if isinstance(latest.get("write_token"), dict) else {}
        if (
            live_token.get("state") == "absent-create"
            and recorded_token.get("state") == "absent-create"
            and live_token.get("path") == recorded_token.get("path")
        ):
            if target == "absent":
                return out(
                    "create-pending",
                    "recover",
                    "Run recover: it creates the declared review file while that file is still absent.",
                )
            return out(
                "target-changed-since-record",
                "none-in-this-entry",
                "The judgment is retained. The target appeared after record, so this entry does not write.",
                "write-token-changed",
            )
        if current is not None and current == recorded:
            if target == "pending":
                return out(
                    "render-interrupted",
                    "recover",
                    "Run recover: it retries rendering the same committed review into the unchanged target.",
                )
            if target in {"existing-review", "unsupported"}:
                return out(
                    "render-blocked",
                    "none-in-this-entry",
                    "The judgment is retained. Rendering into this target is refused.",
                    f"target-{target}",
                )
            return out(
                "unknown-state",
                "none-in-this-entry",
                "The mechanical state is not established.",
                f"unchanged target classified {target}",
            )
        if (
            target == "constructed-same-binding"
            and isinstance(inspection, dict)
            and inspection.get("binding_sha256") == latest.get("task_binding_sha256")
        ):
            return out(
                "rendered-marker-missing",
                "none-in-this-entry",
                "The judgment is retained. A matching task binding is not body equality and is not permission to write. This entry does not clear the missing marker.",
                "page-holds-this-binding",
            )
        return out(
            "target-changed-since-record",
            "none-in-this-entry",
            "The judgment is retained. The target changed after record, so this entry does not write.",
            "write-token-changed",
        )
    if pass_state == "reviewed" and render_state == "rendered":
        return out("rendered", "read", "Read the rendered review.")
    return out(
        "unknown-state",
        "none-in-this-entry",
        "The mechanical state is not established.",
        f"pass {pass_state} render {render_state}",
    )


def enrich(view: dict, inspection: dict | None, exc: Refusal) -> Refusal:
    if "mechanical" not in exc.extra:
        exc.extra["mechanical"] = mechanical(view, inspection, exc)
    if "committed_check" not in exc.extra:
        exc.extra["committed_check"] = {
            "verified": False,
            "rule": exc.code,
            "detail": exc.message,
            "supplied_state": "not-established",
            "not_established": ["Director acceptance", "release", "authenticated identity"],
        }
    return exc


def derived_n7_target(reg: dict) -> str | None:
    if reg.get("source_kind") != "N7NN":
        return None
    page = reg.get("page_id")
    pass_id = reg.get("pass")
    if not isinstance(page, str) or not isinstance(pass_id, str) or "." not in pass_id:
        return None
    tail = pass_id.split(".", 1)[1]
    return f"{page}/06.{tail}.review.md"


def absent_create_token(reg: dict, token) -> bool:
    return (
        isinstance(token, dict)
        and token.get("schema") == "review-write-token/1"
        and token.get("state") == "absent-create"
        and token.get("sha256") is None
        and token.get("bytes") is None
        and token.get("path") == reg.get("target")
        and reg.get("target") == derived_n7_target(reg)
    )


def prepare(root: Path, request_rel: str) -> dict:
    _request, reg, raw = load_request(root, request_rel)
    view = read_cycle(root, _request["registration_path"])
    inspection = inspect_target(root, reg["target"], binding_for(view))
    guide = mechanical(view, inspection, None)
    result = wrap(
        "prepare",
        sha(raw),
        view,
        full_success=False,
        exit_code=0,
        extra={"target": inspection, "mechanical": guide},
    )
    result["supplied_judgment"] = None
    result["_exit"] = 0
    return result


def record(root: Path, request_rel: str, decision_rel: str) -> dict:
    request, reg, raw = load_request(root, request_rel)
    decision_path = under(root, decision_rel, "decision")
    decision_bytes = read_regular(decision_path, "decision")
    decision = strict_json(decision_bytes, "decision")
    need(isinstance(decision.get("supplied_record"), dict), "supplied record is missing")
    preview = read_cycle(root, request["registration_path"])
    target_path = under(root, reg["target"], "target")
    creating = absent_create_token(reg, preview.get("write_token"))
    if creating:
        if os.path.lexists(target_path):
            refuse("target-absent", "target appeared after read")
        expect = "absent"
    elif not os.path.lexists(target_path):
        refuse("target-absent", "target file is absent; the cycle did not commit this decision")
    else:
        digest, _size = page_hash(root, reg["target"])
        expect = digest
    envelope = build_envelope(root, reg, decision["supplied_record"], expect, decision)
    envelope_rel = write_scratch(root, "envelope.json", envelope)
    code, payload, err = cycle_call(
        root,
        ["record", "--registration", request["registration_path"], "--decision", decision_rel, "--envelope", envelope_rel],
    )
    if decision_path.read_bytes() != decision_bytes:
        refuse("target-absent", "record changed the supplied decision file")
    view = read_cycle(root, request["registration_path"]) if code in {0, 1} else {}
    if code == 2:
        rule = payload.get("rule") if isinstance(payload, dict) else err
        raise Refusal(rule or err or "cycle record refused")
    inspection = inspect_target(root, reg["target"], binding_for(view)) if view else None
    guide = mechanical(view, inspection, None)
    full = code == 0 and payload.get("result") in {"recorded", "already-recorded"}
    result = wrap(
        "record",
        sha(raw),
        view,
        full_success=full,
        exit_code=code,
        extra={"record": payload, "target": inspection, "mechanical": guide},
    )
    result["supplied_judgment"] = decision.get("judgment")
    result["_exit"] = code
    return result


def show_binding(root: Path, target: str) -> dict:
    proc = construct_call(root, ["show", "--target", target])
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise Refusal(detail or "constructor show refused")
    return json.loads(proc.stdout.decode("utf-8"))


def finish_render(root: Path, reg: dict, view: dict, proc: subprocess.CompletedProcess, applied: bool) -> dict:
    err = proc.stderr.decode("utf-8", "replace").strip()
    latest = view.get("latest_review") or {}
    directory = latest.get("directory")
    if proc.returncode != 0:
        if "bad member" in err:
            return {
                "result": "render-pending",
                "apply_called": applied,
                "rule": "constructor refused: bad member",
                "next": "a constructor successor must pin labs/prime-review-pass02/prime_review.py before a nonzero page can render",
                "full_success": False,
                "exit_code": 1,
            }
        if "existing review conflicts" in err:
            partial = None
            marker = "partial evidence:"
            if marker in err:
                partial = err.split(marker, 1)[1].strip().splitlines()[0].strip()
            conflict = {
                "schema": "review-loop-render-conflict/1",
                "review_id": latest.get("review_id"),
                "partial": partial,
                "rule": "existing review conflicts; a successor process is required and this review was not overwritten",
            }
            if directory:
                under(root, f"{directory}/render-conflict.json", "render conflict").write_bytes(canonical(conflict))
            return {
                "result": "render-conflict",
                "apply_called": applied,
                "rule": conflict["rule"],
                "partial": partial,
                "next": "a successor process is required; this review was not overwritten",
                "full_success": False,
                "exit_code": 2,
            }
        if err.startswith("refused: "):
            err = err[len("refused: "):]
        raise Refusal(err or "constructor apply refused")
    payload = json.loads(proc.stdout.decode("utf-8"))
    digest, size = page_hash(root, reg["target"])
    need(digest == payload.get("target_sha256_after"), "target hash changed after render")
    shown = show_binding(root, reg["target"])
    need(shown.get("binding_sha256") == view.get("task_binding_sha256"), "rendered review binding does not match the committed task")
    rendered = {
        "schema": "review-loop-rendered/1",
        "review_id": latest.get("review_id"),
        "task_binding_sha256": view.get("task_binding_sha256"),
        "target_sha256": digest,
        "target_bytes": size,
        "section_sha256": shown.get("section_sha256"),
        "prime_review_exit": payload.get("prime_review_exit"),
        "constructor_result": payload.get("result"),
    }
    if directory:
        under(root, f"{directory}/rendered.json", "rendered").write_bytes(canonical(rendered))
    return {
        "result": "rendered",
        "apply_called": applied,
        "rendered": rendered,
        "next": "read the review in a new process",
        "full_success": payload.get("prime_review_exit") in {0, None},
        "exit_code": 0 if payload.get("prime_review_exit") in {0, None} else int(payload.get("prime_review_exit") or 0),
    }


def render_committed(root: Path, reg: dict, view: dict) -> dict:
    latest = view.get("latest_review")
    directory = review_directory(root, reg, view)
    if not isinstance(latest, dict) or not isinstance(directory, str):
        refuse("record-hash", "no committed review")
    if latest.get("schema") != "prime-cycle-review/3":
        refuse("record-hash", "the committed review is not a /3 record")
    check = verify_committed(root, reg, view, directory)
    conflict_path = under(root, f"{directory}/render-conflict.json", "render conflict")
    if conflict_path.is_file():
        conflict = strict_json(read_regular(conflict_path, "render conflict"), "render conflict")
        return {
            "result": "render-conflict",
            "apply_called": False,
            "rule": conflict.get("rule"),
            "partial": conflict.get("partial"),
            "committed_check": check,
            "full_success": False,
            "exit_code": 2,
        }
    rendered_path = under(root, f"{directory}/rendered.json", "rendered")
    token = latest.get("write_token") or {}
    creating = absent_create_token(reg, token)
    target_path = under(root, reg["target"], "target")

    def already(digest: str) -> dict | None:
        if not rendered_path.is_file():
            return None
        rendered = strict_json(read_regular(rendered_path, "rendered"), "rendered")
        if rendered.get("target_sha256") != digest:
            raise Refusal("write token changed since read")
        shown = show_binding(root, reg["target"])
        if shown.get("binding_sha256") != check.get("measured_binding_sha256"):
            refuse("binding", "rendered review binding does not match the measured committed task")
        if shown.get("binding_sha256") != rendered.get("task_binding_sha256"):
            refuse("binding", "rendered review binding does not match the committed task")
        return {
            "result": "already-rendered",
            "apply_called": False,
            "rendered": rendered,
            "committed_check": check,
            "full_success": True,
            "exit_code": 0,
        }

    if creating:
        if os.path.lexists(target_path):
            if is_link(target_path) or not target_path.is_file():
                raise Refusal("target is not a regular file; it was not replaced")
            digest, _size = page_hash(root, reg["target"])
            found = already(digest)
            if found is not None:
                return found
            raise Refusal("target appeared after read")
        digest = "absent"
    else:
        digest, _size = page_hash(root, reg["target"])
        found = already(digest)
        if found is not None:
            return found
        if digest != token.get("sha256"):
            raise Refusal("write token changed since read")
    _stored, envelope = load_coded(root, f"{directory}/envelope.json", "envelope-record")
    if not isinstance(envelope, dict):
        refuse("envelope-record", "stored envelope is not an object")
    if creating:
        if reg.get("target") != derived_n7_target(reg):
            refuse("target-absent", "absent-target creation is only the declared N7 destination")
        envelope["expect_sha256"] = "absent"
        envelope["permit_create"] = True
    else:
        envelope["expect_sha256"] = digest
        envelope["permit_create"] = False
    rel = write_scratch(root, "render-input.json", envelope)
    again = bind_envelope(root, rel)
    assert_measured(again, check["measured_binding_sha256"], check["measured_binding_sha256"])
    proc = construct_call(root, ["apply", "--input", rel])
    outcome = finish_render(root, reg, view, proc, True)
    outcome["committed_check"] = check
    return outcome


def command_view(root: Path, request_rel: str, command: str) -> dict:
    request, reg, raw = load_request(root, request_rel)
    view = read_cycle(root, request["registration_path"])
    inspection = inspect_target(root, reg["target"], binding_for(view))
    failed = None
    check = None
    directory = review_directory(root, reg, view)
    if directory is not None or isinstance(view.get("latest_review"), dict):
        try:
            if not isinstance(directory, str):
                refuse("record-hash", "the cycle read names a review without a directory")
            check = verify_committed(root, reg, view, directory)
        except Refusal as exc:
            failed = exc
    else:
        check = {
            "verified": False,
            "supplied_state": "not-recorded",
            "rule": None,
            "not_established": ["Director acceptance", "release", "authenticated identity"],
        }
    guide = mechanical(view, inspection, failed)
    if command == "read":
        full = failed is None and view.get("pass_state") == "reviewed" and view.get("render_state") == "rendered"
        result = wrap(
            "read",
            sha(raw),
            view,
            full_success=full,
            exit_code=2 if failed is not None else 0,
            extra={"target": inspection, "mechanical": guide, "committed_check": check if failed is None else {
                "verified": False,
                "rule": failed.code,
                "detail": failed.message,
                "supplied_state": "not-established",
                "not_established": ["Director acceptance", "release", "authenticated identity"],
            }},
        )
        if failed is not None:
            result["rule"] = failed.message
        result["_exit"] = 2 if failed is not None else 0
        return result
    try:
        outcome = render_committed(root, reg, view)
    except Refusal as exc:
        raise enrich(view, inspection, exc)
    fresh = read_cycle(root, request["registration_path"])
    fresh_inspection = inspect_target(root, reg["target"], binding_for(fresh))
    guide = mechanical(fresh, fresh_inspection, None)
    result = wrap(
        command,
        sha(raw),
        fresh,
        full_success=outcome["full_success"],
        exit_code=outcome["exit_code"],
        extra={
            "render": {key: value for key, value in outcome.items() if key not in {"full_success", "exit_code"}},
            "target": fresh_inspection,
            "mechanical": guide,
            "committed_check": outcome.get("committed_check"),
        },
    )
    if outcome.get("rule"):
        result["rule"] = outcome["rule"]
    result["_exit"] = outcome["exit_code"]
    return result


def render(root: Path, request_rel: str) -> dict:
    return command_view(root, request_rel, "render")


def recover(root: Path, request_rel: str) -> dict:
    return command_view(root, request_rel, "recover")


def read_back(root: Path, request_rel: str) -> dict:
    return command_view(root, request_rel, "read")


def run_all(root: Path, request_rel: str, decision_rel: str) -> dict:
    prepared = prepare(root, request_rel)
    need(prepared.get("view", {}).get("template") is not None, prepared.get("next") or "no decision template")
    recorded = record(root, request_rel, decision_rel)
    if recorded["_exit"] == 2:
        return recorded
    rendered = render(root, request_rel)
    rendered["prepared_pass_state"] = prepared.get("pass_state")
    rendered["record"] = recorded.get("record")
    rendered["command"] = "run"
    return rendered


def trace(root: Path, payload: dict) -> None:
    directory = root / "trace"
    directory.mkdir(exist_ok=True)
    body = {key: value for key, value in payload.items() if key != "_exit"}
    line = canonical(body) + b"\n"
    with (directory / "trace.jsonl").open("ab") as handle:
        handle.write(line)
    count = len(list(directory.glob("*.json")))
    (directory / f"{payload.get('command', 'op')}-{count}.json").write_bytes(
        json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    )


def preserved(root: Path, request_rel: str | None) -> list[str]:
    found = []
    if request_rel:
        found.append(request_rel)
    for name in ("scratch", "partial", "trace"):
        if (root / name).exists():
            found.append(name)
    return found


def emit(payload: dict) -> None:
    body = {key: value for key, value in payload.items() if key != "_exit"}
    data = (json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        buffer.write(data)
    else:
        sys.stdout.write(data.decode("utf-8"))


def file_measure(path: Path) -> tuple[str | None, int | None]:
    if not os.path.lexists(path) or is_link(path) or not path.is_file():
        return None, None
    data = path.read_bytes()
    if b"\x00" in data:
        return None, None
    return sha(data), len(data)


def read_only_book(text: str) -> Path:
    need(isinstance(text, str) and text.strip() != "", "book is empty")
    need(not text.startswith("\\\\") and not text.startswith("//"), "UNC path book")
    path = Path(text)
    need(path.is_absolute(), "book must be absolute")
    need(".." not in path.parts, "unsafe path book")
    need(path.exists() and path.is_dir() and not is_link(path), "book is not a directory")
    return path


def destination_of(text: str) -> Path:
    need(isinstance(text, str) and text.strip() != "", "destination is empty")
    need(not text.startswith("\\\\") and not text.startswith("//"), "UNC path destination")
    path = Path(text)
    need(path.is_absolute(), "destination must be absolute")
    need(".." not in path.parts, "unsafe path destination")
    inside_checkout = is_inside(path, ROOT)
    inside_evidence = is_inside(path, EVIDENCE)
    if inside_checkout and not inside_evidence:
        raise Refusal("destination inside the checkout must be evidence/build05.08")
    if is_inside(path, LIVE_BOOK) and not inside_evidence:
        raise Refusal("destination must not be the live work book")
    if path.exists():
        need(path.is_dir() and not is_link(path), "destination is not a directory")
    else:
        path.mkdir(parents=True)
    return path


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


def dump_json(path: Path, payload: dict) -> None:
    path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def describe_legacy(book: Path, member: str) -> dict:
    pin_file(INSPECT, INSPECT_SHA, INSPECT_BYTES, "return_inspect")
    pin_file(PLACEMENT, PLACEMENT_SHA, PLACEMENT_BYTES, "return_placement")
    pin_file(LINES, LINES_SHA, LINES_BYTES, "return_lines")
    code, inspected, stderr = tool_json(
        INSPECT, ["inspect", "--book", str(book), "--member", member, "--json"]
    )
    status = None
    problems: list = []
    reservation = None
    if isinstance(inspected, dict):
        status = inspected.get("status")
        if isinstance(inspected.get("problems"), list):
            problems = inspected["problems"]
        if isinstance(inspected.get("reservation"), dict):
            reservation = inspected["reservation"]
    origin = reservation.get("origin") if isinstance(reservation, dict) else None
    route = None
    route_error = None
    if isinstance(origin, dict) and all(isinstance(origin.get(key), str) for key in ("book", "page", "batch")):
        route_code, route_body, route_err = tool_json(
            PLACEMENT,
            ["route", "--book", origin["book"], "--page", origin["page"], "--batch", origin["batch"]],
        )
        if route_code != 0 or route_body is None:
            route_error = route_err.strip() or "unsupported route"
        else:
            route = route_body
    else:
        route_error = "reservation origin is absent" if status != "refused" else None
    safe_member = (
        isinstance(member, str)
        and member != ""
        and "/" not in member
        and "\\" not in member
        and member not in {".", ".."}
    )
    material = {
        "receipt_sha256": None,
        "receipt_bytes": None,
        "return_sha256": None,
        "return_bytes": None,
        "manifest_sha256": None,
        "manifest_bytes": None,
    }
    if safe_member:
        receipt_sha, receipt_len = file_measure(book / member / "receipt.json")
        return_sha, return_len = file_measure(book / member / "return.md")
        manifest_sha, manifest_len = file_measure(book / member / "manifest.json")
        material.update(
            receipt_sha256=receipt_sha,
            receipt_bytes=receipt_len,
            return_sha256=return_sha,
            return_bytes=return_len,
            manifest_sha256=manifest_sha,
            manifest_bytes=manifest_len,
        )
    joined = " ".join(str(item) for item in problems)
    descriptor = None
    if not safe_member:
        state = "unsupported"
        reason = "unsupported member prefix"
    elif status == "refused" and (
        "outside the return band" in joined or "not a return member" in joined or "member path is not" in joined
    ):
        state = "unsupported"
        reason = "unsupported member prefix: " + (problems[0] if problems else str(status))
    elif route is None:
        state = "unsupported"
        reason = route_error or (problems[0] if problems else "unsupported route")
        if stderr.strip() and reason == "unsupported route":
            reason = stderr.strip()
    else:
        state = {"complete": "complete", "reserved": "reserved", "incomplete": "incomplete", "missing": "missing"}.get(
            status, "conflict"
        )
        reason = None if state == "complete" else f"pinned inspector: {status}"
        evidence_path = f"{member}/receipt.json" if material["receipt_sha256"] else f"{member}/reservation.json"
        descriptor = {
            "schema": "return-line-descriptor/2",
            "origin": {"book": origin["book"], "page": origin["page"], "batch": origin["batch"]},
            "route": route.get("route"),
            "target_page": member,
            "return_path": f"{member}/return.md",
            "custody_path": member,
            "receipt_path": f"{member}/receipt.json",
            "manifest_path": f"{member}/manifest.json",
            "submission_id": reservation.get("submission_id") if isinstance(reservation, dict) else None,
            "custody_format": "legacy-in-place/1",
            "receipt_sha256": material["receipt_sha256"],
            "return_sha256": material["return_sha256"],
            "return_bytes": material["return_bytes"],
            "state": state if state in {"complete", "reserved", "incomplete", "conflict"} else "incomplete",
            "verification": {
                "tool_path": INSPECT_PATH,
                "tool_sha256": INSPECT_SHA,
                "result": status,
                "evidence_path": evidence_path,
            },
            "placement": {
                "status": "pending",
                "intended_target_page": route.get("target_page"),
                "intended_return_path": route.get("return_path"),
                "relocation_record_path": None,
                "occupancy": None,
            },
        }
    return {
        "schema": "review-loop-legacy-description/1",
        "book": str(book),
        "member": member,
        "placement_pending": True,
        "final_filing": False,
        "filing_claimed": False,
        "state": state,
        "reason": reason,
        "descriptor": descriptor,
        "inspection": inspected,
        "route": route,
        "material": material,
        "task_association": "not-established",
        "task_association_reason": "custody records do not name the review task",
        "custody": "not-established",
        "allocated": False,
        "closes_work": False,
        "releases_action": False,
        "authenticates_actor": False,
        "authority": "none",
        "accepted": False,
        "full_success": False,
        "exit_code": 0,
    }


def reproduce(destination_text: str, decision_text: str) -> dict:
    """Outside L1. Pass02 keeps this command; pass03 does not reimplement it."""
    pin_file(LOOP02, LOOP02_SHA, LOOP02_BYTES, "review_loop_pass02")
    proc = run_tool(LOOP02, ["reproduce", "--destination", destination_text, "--decision", decision_text])
    text = proc.stdout.decode("utf-8", "replace")
    try:
        payload = json.loads(text) if text.strip() else {}
    except json.JSONDecodeError:
        payload = {
            "schema": "review-loop-refusal/1",
            "rule": "pass02 reproduce stdout is not json",
            "full_success": False,
        }
    if not isinstance(payload, dict):
        payload = {
            "schema": "review-loop-refusal/1",
            "rule": "pass02 reproduce stdout is not an object",
            "full_success": False,
        }
    payload["exit_code"] = proc.returncode
    payload["delegated_to"] = "labs/review-loop-pass02/review_loop.py"
    if proc.returncode == 2 and not str(payload.get("rule") or "").strip():
        payload["rule"] = proc.stderr.decode("utf-8", "replace").strip() or "reproduce refused"
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="review_loop.py")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "render", "read", "recover"):
        command = sub.add_parser(name)
        command.add_argument("--fixture-root", required=True)
        command.add_argument("--request", required=True)
    record_cmd = sub.add_parser("record")
    record_cmd.add_argument("--fixture-root", required=True)
    record_cmd.add_argument("--request", required=True)
    record_cmd.add_argument("--decision", required=True)
    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("--fixture-root", required=True)
    run_cmd.add_argument("--request", required=True)
    run_cmd.add_argument("--decision", required=True)
    legacy_cmd = sub.add_parser("describe-legacy")
    legacy_cmd.add_argument("--book", required=True)
    legacy_cmd.add_argument("--member", required=True)
    repro_cmd = sub.add_parser("reproduce")
    repro_cmd.add_argument("--destination", required=True)
    repro_cmd.add_argument("--decision", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 2
    root = None
    try:
        pin_set()
        if args.command == "describe-legacy":
            result = describe_legacy(read_only_book(args.book), args.member)
            emit(result)
            return int(result.get("exit_code") or 0)
        if args.command == "reproduce":
            result = reproduce(args.destination, args.decision)
            code = int(result.get("exit_code") or 0)
            emit(result)
            if code == 2:
                print(f"refused: {result.get('rule') or 'reproduce refused'}", file=sys.stderr)
            return code
        root = fixture_root(args.fixture_root)
        if args.command == "prepare":
            result = prepare(root, args.request)
        elif args.command == "record":
            result = record(root, args.request, args.decision)
        elif args.command == "render":
            result = render(root, args.request)
        elif args.command == "read":
            result = read_back(root, args.request)
        elif args.command == "recover":
            result = recover(root, args.request)
        else:
            result = run_all(root, args.request, args.decision)
        trace(root, result)
        code = int(result.get("_exit") or 0)
        emit(result)
        render_body = result.get("render") if isinstance(result.get("render"), dict) else {}
        if code == 2 and result.get("rule") and render_body.get("result") != "render-conflict":
            print(f"refused: {result['rule']}", file=sys.stderr)
        return code
    except Refusal as exc:
        payload = {
            "schema": "review-loop-refusal/1",
            "command": getattr(args, "command", None),
            "rule": exc.message,
            "contract": CONTRACT,
            "request_sha256": None,
            "pins": None,
            "observation": None,
            "supplied_judgment": None,
            "current": None,
            "historical": None,
            "preserved": preserved(root, getattr(args, "request", None)) if root is not None else [],
            "next": exc.message,
            "full_success": False,
            "custody": "not-established",
            "allocated": False,
            "closes_work": False,
            "releases_action": False,
            "authenticates_actor": False,
            "authority": "none",
            "accepted": False,
        }
        for key in ("mechanical", "committed_check", "target"):
            if key in exc.extra:
                payload[key] = exc.extra[key]
        guide = payload.get("mechanical")
        if isinstance(guide, dict) and isinstance(guide.get("text"), str):
            payload["next"] = guide["text"]
        try:
            payload["pins"] = pin_set()
        except Refusal:
            payload["pins"] = None
        if root is not None and getattr(args, "request", None):
            try:
                raw = read_regular(under(root, args.request, "request"), "request")
                payload["request_sha256"] = sha(raw)
            except Refusal:
                pass
        if root is not None:
            try:
                trace(root, payload)
            except OSError:
                pass
        emit(payload)
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
