#!/usr/bin/env python3
"""Orchestrate a described return into a full in-page Prime review.

Successor of labs/review-loop-pass01/review_loop.py
sha256 fac0881d1e7e991b630d1deab688a3e28745e2f7b2075c7eb5148251b8ac5595, 26028 bytes.
Calls the pinned pass02 constructor and the pass03 cycle. It does not edit
those tools. It does not approve, release, close, allocate, or establish
custody. prepare may exit 0 with full_success false. A rendered review is
not approval. describe-legacy only reads. reproduce captures on a disposable
book outside this checkout.
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
CONTRACT = "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.04/CONTRACT.md"
CONSTRUCT = ROOT / "labs" / "review-construction-pass02" / "construct.py"
CONSTRUCT_SHA = "b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc"
CONSTRUCT_BYTES = 36188
REVIEW01 = ROOT / "labs" / "prime-review-pass01" / "prime_review.py"
REVIEW01_SHA = "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0"
REVIEW01_BYTES = 58324
REVIEW02 = ROOT / "labs" / "prime-review-pass02" / "prime_review.py"
REVIEW02_SHA = "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"
REVIEW02_BYTES = 58560
CYCLE = ROOT / "labs" / "prime-cycle-pass03" / "prime_cycle.py"
CYCLE_SHA = "496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c"
CYCLE_BYTES = 76045
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
EVIDENCE = LIVE_BOOK / "0522.review-construction" / "evidence" / "build05.04"
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
            "path": "labs/review-loop-pass02/review_loop.py",
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


def wrap(command: str, request_sha: str, view: dict, *, full_success: bool, exit_code: int, extra: dict | None = None) -> dict:
    latest = view.get("latest_review") if isinstance(view, dict) else None
    judgment = None
    if isinstance(latest, dict):
        judgment = None
    payload = {
        "schema": "review-loop-result/1",
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
            "questions": view.get("questions") if isinstance(view, dict) else [],
            "director_replies": view.get("director_replies") if isinstance(view, dict) else [],
            "latest_review": latest,
        },
        "historical": view.get("historical") if isinstance(view, dict) else None,
        "next": None,
        "pass_state": view.get("pass_state") if isinstance(view, dict) else None,
        "view": view,
    }
    payload.update(flags(view))
    if extra:
        payload.update(extra)
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


def build_envelope(root: Path, reg: dict, record: dict, expect: str) -> dict:
    descriptor = strict_json(
        read_regular(under(root, reg["descriptor_path"], "descriptor"), "descriptor"),
        "descriptor",
    )
    return {
        "schema": "review-construction/1",
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


def prepare(root: Path, request_rel: str) -> dict:
    _request, reg, raw = load_request(root, request_rel)
    view = read_cycle(root, _request["registration_path"])
    result = wrap("prepare", sha(raw), view, full_success=False, exit_code=0)
    result["supplied_judgment"] = None
    result["next"] = "supply a typed judgment and supplied_record, then record" if view.get("template") else view.get("pass_state")
    result["_exit"] = 0
    return result


def record(root: Path, request_rel: str, decision_rel: str) -> dict:
    request, reg, raw = load_request(root, request_rel)
    decision = strict_json(read_regular(under(root, decision_rel, "decision"), "decision"), "decision")
    need(isinstance(decision.get("supplied_record"), dict), "supplied record is missing")
    digest, _size = page_hash(root, reg["target"])
    envelope = build_envelope(root, reg, decision["supplied_record"], digest)
    envelope_rel = write_scratch(root, "envelope.json", envelope)
    code, payload, err = cycle_call(
        root,
        ["record", "--registration", request["registration_path"], "--decision", decision_rel, "--envelope", envelope_rel],
    )
    view = read_cycle(root, request["registration_path"]) if code in {0, 1} else {}
    if code == 2:
        rule = payload.get("rule") if isinstance(payload, dict) else err
        raise Refusal(rule or err or "cycle record refused")
    full = code == 0 and payload.get("result") in {"recorded", "already-recorded"}
    result = wrap("record", sha(raw), view, full_success=full, exit_code=code, extra={"record": payload})
    result["supplied_judgment"] = decision.get("judgment")
    result["next"] = "render the committed review" if payload.get("render_state") == "pending" else "read the current review"
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
    need(isinstance(latest, dict), "no committed review")
    need(latest.get("schema") == "prime-cycle-review/3", "the committed review is not a /3 record")
    directory = latest["directory"]
    conflict_path = under(root, f"{directory}/render-conflict.json", "render conflict")
    if conflict_path.is_file():
        conflict = strict_json(read_regular(conflict_path, "render conflict"), "render conflict")
        return {
            "result": "render-conflict",
            "apply_called": False,
            "rule": conflict.get("rule"),
            "partial": conflict.get("partial"),
            "next": "a successor process is required; this review was not overwritten",
            "full_success": False,
            "exit_code": 2,
        }
    rendered_path = under(root, f"{directory}/rendered.json", "rendered")
    digest, _size = page_hash(root, reg["target"])
    if rendered_path.is_file():
        rendered = strict_json(read_regular(rendered_path, "rendered"), "rendered")
        if rendered.get("target_sha256") == digest:
            shown = show_binding(root, reg["target"])
            need(shown.get("binding_sha256") == rendered.get("task_binding_sha256"), "rendered review binding does not match the committed task")
            return {
                "result": "already-rendered",
                "apply_called": False,
                "rendered": rendered,
                "next": "read the review in a new process",
                "full_success": True,
                "exit_code": 0,
            }
        raise Refusal("write token changed since read")
    token = latest.get("write_token") or {}
    need(digest == token.get("sha256"), "write token changed since read")
    envelope = strict_json(read_regular(under(root, f"{directory}/envelope.json", "envelope"), "envelope"), "envelope")
    envelope["expect_sha256"] = digest
    rel = write_scratch(root, "render-input.json", envelope)
    proc = construct_call(root, ["apply", "--input", rel])
    return finish_render(root, reg, view, proc, True)


def render(root: Path, request_rel: str) -> dict:
    request, reg, raw = load_request(root, request_rel)
    view = read_cycle(root, request["registration_path"])
    outcome = render_committed(root, reg, view)
    fresh = read_cycle(root, request["registration_path"])
    result = wrap(
        "render",
        sha(raw),
        fresh,
        full_success=outcome["full_success"],
        exit_code=outcome["exit_code"],
        extra={"render": {key: value for key, value in outcome.items() if key not in {"full_success", "exit_code"}}},
    )
    result["next"] = outcome.get("next")
    if outcome.get("rule"):
        result["rule"] = outcome["rule"]
    result["_exit"] = outcome["exit_code"]
    return result


def recover(root: Path, request_rel: str) -> dict:
    request, reg, raw = load_request(root, request_rel)
    view = read_cycle(root, request["registration_path"])
    outcome = render_committed(root, reg, view)
    fresh = read_cycle(root, request["registration_path"])
    result = wrap(
        "recover",
        sha(raw),
        fresh,
        full_success=outcome["full_success"],
        exit_code=outcome["exit_code"],
        extra={"render": {key: value for key, value in outcome.items() if key not in {"full_success", "exit_code"}}},
    )
    result["next"] = outcome.get("next")
    if outcome.get("rule"):
        result["rule"] = outcome["rule"]
    result["_exit"] = outcome["exit_code"]
    if outcome["exit_code"] == 2 and outcome.get("result") != "render-conflict":
        raise Refusal(outcome.get("rule") or "recover refused")
    return result


def read_back(root: Path, request_rel: str) -> dict:
    request, _reg, raw = load_request(root, request_rel)
    view = read_cycle(root, request["registration_path"])
    full = view.get("pass_state") == "reviewed" and view.get("render_state") == "rendered"
    result = wrap("read", sha(raw), view, full_success=full, exit_code=0)
    if view.get("next_action"):
        result["next"] = view["next_action"].get("text")
    elif view.get("historical") and (view["historical"].get("next_action") or {}).get("text"):
        result["next"] = "historical next action is not current: " + view["historical"]["next_action"]["text"]
    else:
        result["next"] = view.get("pass_state")
    result["_exit"] = 0
    return result


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
        raise Refusal("destination inside the checkout must be evidence/build05.04")
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


def producer(args: list[str], allowed: set[int]) -> subprocess.CompletedProcess:
    proc = run_tool(LINES, args)
    if proc.returncode not in allowed:
        detail = proc.stderr.decode("utf-8", "replace").strip() or proc.stdout.decode("utf-8", "replace")[:800]
        raise Refusal(detail or f"producer exit {proc.returncode}")
    return proc


def loop_step(book: Path, args: list[str]) -> dict:
    proc = run_tool(Path(__file__).resolve(), [*args, "--fixture-root", str(book)])
    text = proc.stdout.decode("utf-8", "replace")
    try:
        payload = json.loads(text) if text.strip() else {}
    except json.JSONDecodeError:
        payload = {"schema": "review-loop-refusal/1", "rule": "stdout is not json", "full_success": False}
    if not isinstance(payload, dict):
        payload = {"schema": "review-loop-refusal/1", "rule": "stdout is not an object", "full_success": False}
    payload["exit_code"] = proc.returncode
    payload["stderr"] = proc.stderr.decode("utf-8", "replace")
    return payload


def review_page_bytes() -> bytes:
    text = (
        "Intro OUTSIDE-Δ-TOKEN\n\n"
        "## Return pointer\n"
        "PENDING.\n\n"
        "## Review — Codex Prime\n"
        "PENDING.\n"
        "## Notes\n"
        "TAIL-Δ-TOKEN\n"
    )
    return text.encode("utf-8")


def measured_source(path: str, data: bytes, kind: str, identity: dict) -> dict:
    digest = sha(data)
    return {
        "bind": False,
        "content_bytes": len(data),
        "content_sha256": digest,
        "identity": identity,
        "kind": kind,
        "logical_path": path,
        "prior_content_sha256": None,
        "prior_transport_sha256": None,
        "record": data.decode("utf-8"),
        "transport_bytes": len(data),
        "transport_sha256": digest,
    }


def align_supplied_judgment(judgment: dict, record_judgment: dict) -> None:
    action = judgment["next_action"]["text"] if isinstance(judgment.get("next_action"), dict) else None
    pairs = (
        ("outcome", judgment.get("outcome"), record_judgment.get("outcome")),
        ("finding", judgment.get("finding"), record_judgment.get("finding")),
        ("reasons", judgment.get("reasons"), record_judgment.get("reasons")),
        ("sections", judgment.get("sections"), record_judgment.get("sections")),
        ("semantic_conflict", judgment.get("semantic_conflict"), record_judgment.get("semantic_conflict")),
        ("design_fork", judgment.get("design_fork"), record_judgment.get("design_fork")),
        ("next_action", action, record_judgment.get("next_action")),
    )
    for name, left, right in pairs:
        need(left == right, f"supplied record does not match the judgment: {name}")


def reproduce(destination_text: str, decision_text: str) -> dict:
    decision_path = Path(decision_text)
    need(decision_path.is_file() and not is_link(decision_path), "decision file is absent")
    destination = destination_of(destination_text)
    supplied = strict_json(decision_path.read_bytes(), "decision")
    need(isinstance(supplied, dict), "decision file is absent")
    need(supplied.get("schema") == "review-loop-reproduce-decision/1", "decision schema is not review-loop-reproduce-decision/1")
    for key in ("attribution", "agreement", "goal", "judgment", "record_judgment", "return_text", "note_text", "assignment_text", "task_id"):
        need(key in supplied, f"decision is missing {key}")
    need(isinstance(supplied["return_text"], str) and supplied["return_text"] != "", "decision does not name the return text")
    need(isinstance(supplied["note_text"], str), "decision note_text must be text")
    need(isinstance(supplied["assignment_text"], str) and supplied["assignment_text"] != "", "decision assignment_text must be text")
    align_supplied_judgment(supplied["judgment"], supplied["record_judgment"])
    pin_file(LINES, LINES_SHA, LINES_BYTES, "return_lines")
    book = Path(tempfile.mkdtemp(prefix="repro-0504-"))
    if is_inside(book, ROOT) or is_inside(ROOT, book):
        shutil.rmtree(book, ignore_errors=True)
        raise Refusal("disposable book must stay outside D:\\Git\\lib-build")
    steps: list[dict] = []
    try:
        note = book / "note.md"
        assignment = book / "assignment.txt"
        return_file = book / "_inputs" / "return.md"
        artifact = book / "_inputs" / "note.md"
        return_file.parent.mkdir()
        return_file.write_bytes(supplied["return_text"].encode("utf-8"))
        artifact.write_bytes(supplied["note_text"].encode("utf-8"))
        note.write_bytes(supplied["note_text"].encode("utf-8"))
        assignment.write_bytes(supplied["assignment_text"].encode("utf-8"))
        page = book / "0599.synth-lab" / "05.01.md"
        page.parent.mkdir(parents=True)
        page.write_bytes(review_page_bytes())
        producer(["init", "--book", str(book), "--name", BOOK], {0})
        producer(
            [
                "reserve", "--book", str(book), "--page", "0599.synth-lab", "--batch", "05.01",
                "--submission", "repro-0504", "--output", "note.md",
                "--submitter", "grok-1", "--reviewer", "codex-prime", "--release", "prepared",
            ],
            {1},
        )
        producer(
            [
                "capture", "--book", str(book), "--page", "0599.synth-lab", "--batch", "05.01",
                "--submission", "repro-0504", "--return-file", str(return_file),
                "--artifact", "note.md", str(artifact),
            ],
            {0},
        )
        described_proc = producer(
            ["descriptor", "--book", str(book), "--page", "0599.synth-lab", "--batch", "05.01"],
            {0},
        )
        (book / "descriptor.json").write_bytes(described_proc.stdout)
        (destination / "descriptor.json").write_bytes(described_proc.stdout)
        described = json.loads(described_proc.stdout.decode("utf-8"))
        registration = {
            "schema": "prime-cycle-registration/2",
            "book": BOOK,
            "work_id": "repro-0599",
            "source_kind": "N5NN",
            "page_id": "0599.synth-lab",
            "pass": "05.01",
            "kernel_page": "00.kernel/00.00.10.work/0599.synth-lab/05.01.md",
            "target": "0599.synth-lab/05.01.md",
            "descriptor_path": "descriptor.json",
            "agreement": supplied["agreement"],
            "task_id": supplied["task_id"],
            "assignment_path": "assignment.txt",
            "evidence": [{"label": "supplied", "logical_path": "note.md"}],
            "submission_id": "repro-0504",
            "receipt_label": "supplied",
            "review_identity": "r1",
            "review_location": "cycle",
            "goal": supplied["goal"],
            "bounds": {"max_output_bytes": 2097152},
        }
        dump_json(book / "registration.json", registration)
        dump_json(book / "request.json", {"schema": "review-loop-request/1", "registration_path": "registration.json"})
        prepared = loop_step(book, ["prepare", "--request", "request.json"])
        steps.append({"command": "prepare", "payload": prepared})
        template = prepared.get("view", {}).get("template") if isinstance(prepared.get("view"), dict) else None
        if not isinstance(template, dict):
            body = dict(prepared)
            body["command"] = "reproduce"
            body["full_success"] = False
            body["destination"] = str(destination)
            body["descriptor_sha256"] = sha(described_proc.stdout)
            body.pop("stderr", None)
            dump_json(destination / "transcript.json", {"steps": steps, "result": body, "book": str(book)})
            return body
        receipt_bytes = (book / described["receipt_path"]).read_bytes()
        return_bytes = (book / described["return_path"]).read_bytes()
        need(return_bytes == supplied["return_text"].encode("utf-8"), "captured return does not match the supplied return text")
        sources = [
            measured_source("assignment.txt", assignment.read_bytes(), "page", {"schema": "page-bytes/1"}),
            measured_source(
                "note.md",
                note.read_bytes(),
                "supplied-text",
                {"schema": "supplied-text/1", "label": "SUPPLIED"},
            ),
            measured_source(
                described["return_path"],
                return_bytes,
                "capture",
                {
                    "schema": "return-capture/1",
                    "member": described["target_page"],
                    "submission_id": "repro-0504",
                    "receipt_sha256": sha(receipt_bytes),
                    "origin": {"book": BOOK, "page": "0599.synth-lab", "batch": "05.01"},
                },
            ),
        ]
        record = {
            "schema": "prime-review-record/1",
            "attribution": supplied["attribution"],
            "sources": sources,
            "agreement": supplied["agreement"],
            "holds": supplied.get("holds") if isinstance(supplied.get("holds"), list) else [],
            "answers": supplied.get("answers") if isinstance(supplied.get("answers"), list) else [],
            "review_passes": [],
            "gaps": [],
            "judgment": supplied["record_judgment"],
        }
        decision = template
        decision["attribution"] = supplied["attribution"]
        decision["judgment"] = supplied["judgment"]
        decision["supplied_record"] = record
        dump_json(book / "decision.json", decision)
        dump_json(destination / "decision.json", decision)
        recorded = loop_step(book, ["record", "--request", "request.json", "--decision", "decision.json"])
        steps.append({"command": "record", "payload": recorded})
        if recorded.get("exit_code") not in {0, 1}:
            body = dict(recorded)
            body["command"] = "reproduce"
            body["full_success"] = False
            body["destination"] = str(destination)
            body.pop("stderr", None)
            dump_json(destination / "transcript.json", {"steps": steps, "result": body, "book": str(book)})
            return body
        rendered = loop_step(book, ["render", "--request", "request.json"])
        steps.append({"command": "render", "payload": rendered})
        read_back_payload = loop_step(book, ["read", "--request", "request.json"])
        steps.append({"command": "read", "payload": read_back_payload})
        (destination / "sample-review.md").write_bytes(page.read_bytes())
        landed = bool(rendered.get("full_success")) and read_back_payload.get("pass_state") == "reviewed"
        body = dict(read_back_payload)
        body["command"] = "reproduce"
        body["full_success"] = landed
        body["exit_code"] = 0 if landed else int(rendered.get("exit_code") or read_back_payload.get("exit_code") or 1)
        body["destination"] = str(destination)
        body["descriptor_sha256"] = sha(described_proc.stdout)
        body["accepted"] = False
        body["custody"] = "not-established"
        body["filing_claimed"] = False
        body.pop("stderr", None)
        dump_json(destination / "transcript.json", {"steps": steps, "result": body})
        shutil.rmtree(book, ignore_errors=True)
        return body
    except Exception:
        dump_json(destination / "transcript.json", {"steps": steps, "book": str(book)})
        raise


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
