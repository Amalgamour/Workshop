#!/usr/bin/env python3
"""Orchestrate a described return into a full in-page Prime review.

Calls the pinned constructor, the pass02 cycle, and the pass02 report tool
as separate processes. It does not edit those tools. It does not approve,
release, close, allocate, or establish custody. A rendered review is not approval.
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
CONTRACT = "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.03/CONTRACT.md"
CONSTRUCT = ROOT / "labs" / "review-construction-pass01" / "construct.py"
CONSTRUCT_SHA = "8b9d4a6eda460f594404042f7ee232a7ac55fcc09af38905de364defa189ea8a"
CONSTRUCT_BYTES = 35956
REVIEW01 = ROOT / "labs" / "prime-review-pass01" / "prime_review.py"
REVIEW01_SHA = "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0"
REVIEW01_BYTES = 58324
REVIEW02 = ROOT / "labs" / "prime-review-pass02" / "prime_review.py"
REVIEW02_SHA = "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"
REVIEW02_BYTES = 58560
CYCLE = ROOT / "labs" / "prime-cycle-pass02" / "prime_cycle.py"
CYCLE_SHA = "689d63d26b0dfb59363563effa50acbd69856ffcc2ee728b7f54615f16fabd50"
CYCLE_BYTES = 58448
BOOK = "00.00.10.work"
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
        "prime_cycle_pass02": pin_file(CYCLE, CYCLE_SHA, CYCLE_BYTES, "prime_cycle_pass02"),
        "review_loop": {
            "path": "labs/review-loop-pass01/review_loop.py",
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
    full = view.get("template") is not None and view.get("pass_state") == "awaiting-review"
    result = wrap("prepare", sha(raw), view, full_success=full, exit_code=0 if view.get("template") or view.get("pass_state") else 0)
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
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 2
    root = None
    try:
        pin_set()
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
