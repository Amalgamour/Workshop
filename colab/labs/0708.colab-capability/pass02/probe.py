"""Allocate one evidence-preserving probe run.

The evidence root and the scratch root are explicit. This process creates one
new slot under each, or it refuses an occupied evidence slot before writing.
It does not delete a directory and it has no default output path.

Exit 0: status complete. Exit 1: this process recorded a failure. Exit 2: refused
before creating an evidence slot.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
import traceback
from pathlib import Path

SCHEMA_COMMAND = "colab-probe-command/0502"
SCHEMA_INPUTS = "colab-probe-inputs/0502"
SCHEMA_RUN = "colab-probe-run/0502"
PRODUCER_SHA256 = "2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b"
PRODUCER_BYTES = 53892
REPORT_SCHEMA = "colab-support-report/2"
OK_BYTES = b"minimal-ok\n"
PARTIAL_BYTES = b"partial-output\n"
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
CHILD_OK = """import pathlib, sys
pathlib.Path(sys.argv[1]).write_bytes(b"minimal-ok\\n")
raise SystemExit(0)
"""
CHILD_FAIL = """import pathlib, sys
pathlib.Path(sys.argv[1]).write_bytes(b"partial-output\\n")
raise SystemExit(1)
"""


class Refuse(Exception):
    """A refusal before an evidence slot exists."""


def dump(body: dict) -> bytes:
    return (json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _binary_flags(*flags: int) -> int:
    value = 0
    for flag in flags:
        value |= flag
    if hasattr(os, "O_BINARY"):
        value |= os.O_BINARY
    return value


def _fsync(fd: int) -> None:
    os.fsync(fd)


def write_bytes(path: Path, data: bytes) -> None:
    # Read/write is required so Windows FlushFileBuffers accepts the handle.
    fd = os.open(str(path), _binary_flags(os.O_RDWR, os.O_CREAT, os.O_EXCL))
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise OSError(f"short write to {path}")
            view = view[written:]
        _fsync(fd)
    finally:
        os.close(fd)


def replace_bytes(path: Path, data: bytes) -> None:
    temporary = path.with_name(path.name + ".tmp")
    write_bytes(temporary, data)
    os.replace(temporary, path)
    fd = os.open(str(path), _binary_flags(os.O_RDWR))
    try:
        _fsync(fd)
    finally:
        os.close(fd)


def write_json(path: Path, body: dict) -> None:
    write_bytes(path, dump(body))


def replace_json(path: Path, body: dict) -> None:
    replace_bytes(path, dump(body))


def require_directory(label: str, text: str) -> Path:
    path = Path(text)
    if not path.is_absolute():
        raise Refuse(f"{label} is not absolute")
    if not path.is_dir():
        raise Refuse(f"{label} is not an existing directory")
    return path.resolve()


def inside(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return child != parent


def valid_run_id(value: str) -> bool:
    return bool(RUN_ID.fullmatch(value)) and ".." not in value


def require_file(label: str, text: str) -> Path:
    path = Path(text)
    if not path.is_absolute() or not path.is_file():
        raise Refuse(f"{label} is not an absolute file")
    return path.resolve()


def running_body(run_id: str) -> dict:
    return {
        "checks": [],
        "detail": "started",
        "interruption": None,
        "run_id": run_id,
        "schema": SCHEMA_RUN,
        "status": "running",
    }


def failed_body(run_id: str, detail: str, checks: list, child_exit: int | None) -> dict:
    body = {
        "checks": checks,
        "detail": detail,
        "interruption": "caught-failure",
        "run_id": run_id,
        "schema": SCHEMA_RUN,
        "status": "failed",
    }
    if child_exit is not None:
        body["child_exit"] = child_exit
    return body


def complete_body(run_id: str, detail: str, checks: list, child_exit: int) -> dict:
    return {
        "checks": checks,
        "child_exit": child_exit,
        "detail": detail,
        "interruption": "none",
        "run_id": run_id,
        "schema": SCHEMA_RUN,
        "status": "complete",
    }


def decide_ok(run_id: str, child_exit: int, output: bytes | None) -> dict:
    checks = [
        {"matched": child_exit == 0, "name": "child-exit", "observed": child_exit},
        {
            "matched": output == OK_BYTES,
            "name": "child-out",
            "observed": None if output is None else sha256(output),
        },
    ]
    if all(item["matched"] for item in checks):
        return complete_body(run_id, "ok checks passed", checks, child_exit)
    return failed_body(run_id, "ok checks failed", checks, child_exit)


def decide_fail(run_id: str, child_exit: int, output: bytes | None) -> dict:
    checks = [
        {"matched": child_exit == 1, "name": "child-exit", "observed": child_exit},
        {
            "matched": output == PARTIAL_BYTES,
            "name": "partial-output",
            "observed": None if output is None else sha256(output),
        },
    ]
    if all(item["matched"] for item in checks):
        detail = "fail mode recorded a caught failure"
    else:
        detail = "fail mode did not match the expected caught failure"
    return failed_body(run_id, detail, checks, child_exit)


def accept_preview(stdout: bytes, code: int) -> tuple[bool, str, str | None]:
    if code != 0:
        return False, f"preview exit {code}", None
    try:
        body = json.loads(stdout.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        return False, f"preview stdout is not json: {exc}", None
    if not isinstance(body, dict):
        return False, "preview stdout is not an object", None
    if body.get("schema") != REPORT_SCHEMA:
        return False, "preview schema is not colab-support-report/2", None
    if body.get("command") != "preview" or body.get("result") != "preview":
        return False, "preview result is not preview", None
    digest = body.get("digest")
    if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
        return False, "preview digest is missing", None
    return True, "preview checks passed", digest


def decide_preview(run_id: str, child_exit: int, stdout: bytes) -> dict:
    matched, detail, digest = accept_preview(stdout, child_exit)
    checks = [
        {"matched": matched, "name": "preview-report", "observed": digest},
    ]
    if matched:
        return complete_body(run_id, detail, checks, child_exit)
    return failed_body(run_id, detail, checks, child_exit)


def file_row(role: str, path: Path) -> dict:
    data = path.read_bytes()
    return {"bytes": len(data), "path": str(path), "role": role, "sha256": sha256(data)}


def claim_evidence(root: Path, run_id: str | None) -> tuple[Path, str]:
    if run_id is not None:
        slot = root / run_id
        try:
            os.mkdir(slot)
        except FileExistsError as exc:
            raise Refuse("occupied evidence destination") from exc
        except OSError as exc:
            raise Refuse(f"evidence slot was not created: {exc.strerror or exc}") from exc
        return slot, run_id
    for _ in range(8):
        candidate = time.strftime("run-%Y%m%dT%H%M%S-") + secrets.token_hex(4)
        if not valid_run_id(candidate):
            continue
        slot = root / candidate
        try:
            os.mkdir(slot)
        except FileExistsError:
            continue
        except OSError as exc:
            raise Refuse(f"evidence slot was not created: {exc.strerror or exc}") from exc
        return slot, candidate
    raise Refuse("could not allocate a unique run id")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="probe.py")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--evidence-root", required=True)
    run.add_argument("--scratch-root", required=True)
    run.add_argument("--run-id")
    run.add_argument("--mode", required=True, choices=("ok", "fail", "hold", "preview"))
    run.add_argument("--request")
    run.add_argument("--config")
    run.add_argument("--producer")
    run.add_argument("--hold-seconds", type=int)
    return parser.parse_args(argv)


def validate(opts: argparse.Namespace) -> tuple[Path, Path, int | None]:
    evidence = require_directory("evidence root", opts.evidence_root)
    scratch = require_directory("scratch root", opts.scratch_root)
    if evidence == scratch or inside(evidence, scratch) or inside(scratch, evidence):
        raise Refuse("evidence root and scratch root must be separate directories")
    if opts.run_id is not None and not valid_run_id(opts.run_id):
        raise Refuse("run id must be one path segment")
    if opts.mode == "hold":
        seconds = 30 if opts.hold_seconds is None else opts.hold_seconds
        if not 1 <= seconds <= 120:
            raise Refuse("hold seconds must be from 1 to 120")
    elif opts.hold_seconds is not None:
        raise Refuse("hold seconds is only valid for hold mode")
    else:
        seconds = None
    if opts.mode == "preview":
        for label, value in (("request", opts.request), ("config", opts.config), ("producer", opts.producer)):
            if not value:
                raise Refuse(f"preview requires --{label}")
            require_file(label, value)
    elif any((opts.request, opts.config, opts.producer)):
        raise Refuse("request, config, and producer are only valid for preview")
    return evidence, scratch, seconds


def command_body(opts: argparse.Namespace, evidence: Path, scratch: Path, slot: Path, scratch_slot: Path, run_id: str) -> dict:
    return {
        "argv": sys.argv,
        "evidence_root": str(evidence),
        "evidence_slot": str(slot),
        "mode": opts.mode,
        "probe_cwd": os.getcwd(),
        "python": sys.executable,
        "python_version": sys.version,
        "run_id": run_id,
        "schema": SCHEMA_COMMAND,
        "scratch_root": str(scratch),
        "scratch_slot": str(scratch_slot),
    }


def synthetic_inputs(mode: str) -> dict:
    return {"files": [], "mode": mode, "schema": SCHEMA_INPUTS}


def preview_inputs(opts: argparse.Namespace) -> tuple[dict, bool]:
    producer = require_file("producer", opts.producer)
    request = require_file("request", opts.request)
    config = require_file("config", opts.config)
    producer_row = file_row("producer", producer)
    producer_row["pin_match"] = (
        producer_row["sha256"] == PRODUCER_SHA256 and producer_row["bytes"] == PRODUCER_BYTES
    )
    body = {
        "files": [
            producer_row,
            file_row("request", request),
            file_row("config", config),
        ],
        "mode": "preview",
        "schema": SCHEMA_INPUTS,
    }
    return body, producer_row["pin_match"]


def child_env() -> dict:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_child(slot: Path, scratch_slot: Path, argv: list[str]) -> tuple[int, bytes]:
    proc = subprocess.run(
        argv,
        cwd=str(scratch_slot),
        capture_output=True,
        check=False,
        shell=False,
        env=child_env(),
    )
    write_bytes(slot / "child.stdout", proc.stdout)
    write_bytes(slot / "child.stderr", proc.stderr)
    write_bytes(slot / "child.exit", f"{proc.returncode}\n".encode("ascii"))
    return proc.returncode, proc.stdout


def read_optional(path: Path) -> bytes | None:
    if path.is_file():
        return path.read_bytes()
    return None


def finish(slot: Path, body: dict) -> int:
    replace_json(slot / "status.json", body)
    status = body["status"]
    if status == "failed":
        print(f"failed: {body['detail']}", file=sys.stderr)
    print(f"status {status}")
    sys.stdout.flush()
    return 0 if status == "complete" else 1


def record_exception(slot: Path, exc: BaseException) -> None:
    path = slot / "error.txt"
    if path.exists():
        return
    text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    try:
        write_bytes(path, text.encode("utf-8", "replace"))
    except OSError:
        return


def open_scratch(slot: Path, scratch_slot: Path, run_id: str) -> int | None:
    try:
        os.mkdir(scratch_slot)
    except FileExistsError:
        return finish(slot, failed_body(run_id, "occupied scratch destination", [], None))
    except OSError as exc:
        detail = f"scratch slot was not created: {exc.strerror or exc}"
        return finish(slot, failed_body(run_id, detail, [], None))
    return None


def run_claimed(opts: argparse.Namespace, evidence: Path, scratch: Path, slot: Path, run_id: str, hold_seconds: int | None) -> int:
    scratch_slot = scratch / run_id
    write_json(slot / "status.json", running_body(run_id))
    write_json(slot / "command.json", command_body(opts, evidence, scratch, slot, scratch_slot, run_id))
    print(f"run {run_id}")
    sys.stdout.flush()
    if opts.mode == "preview":
        inputs, pin_match = preview_inputs(opts)
        write_json(slot / "inputs.json", inputs)
        if not pin_match:
            return finish(slot, failed_body(run_id, "producer pin mismatch", [], None))
    else:
        write_json(slot / "inputs.json", synthetic_inputs(opts.mode))
    scratch_code = open_scratch(slot, scratch_slot, run_id)
    if scratch_code is not None:
        return scratch_code
    if opts.mode == "ok":
        child_exit, _stdout = run_child(
            slot,
            scratch_slot,
            [sys.executable, "-B", "-c", CHILD_OK, str(scratch_slot / "child-out.txt")],
        )
        return finish(slot, decide_ok(run_id, child_exit, read_optional(scratch_slot / "child-out.txt")))
    if opts.mode == "fail":
        child_exit, _stdout = run_child(
            slot,
            scratch_slot,
            [sys.executable, "-B", "-c", CHILD_FAIL, str(scratch_slot / "partial.txt")],
        )
        return finish(slot, decide_fail(run_id, child_exit, read_optional(scratch_slot / "partial.txt")))
    if opts.mode == "hold":
        time.sleep(hold_seconds or 30)
        return finish(
            slot,
            failed_body(run_id, "hold window elapsed without termination", [], None),
        )
    child_exit, stdout = run_child(
        slot,
        scratch_slot,
        [
            sys.executable,
            "-B",
            str(require_file("producer", opts.producer)),
            "preview",
            "--request",
            str(require_file("request", opts.request)),
            "--config",
            str(require_file("config", opts.config)),
            "--json",
        ],
    )
    return finish(slot, decide_preview(run_id, child_exit, stdout))


def execute(opts: argparse.Namespace) -> int:
    evidence, scratch, hold_seconds = validate(opts)
    slot, run_id = claim_evidence(evidence, opts.run_id)
    try:
        return run_claimed(opts, evidence, scratch, slot, run_id, hold_seconds)
    except Refuse:
        raise
    except Exception as exc:
        record_exception(slot, exc)
        try:
            replace_json(
                slot / "status.json",
                failed_body(run_id, f"caught {type(exc).__name__}: {exc}", [], None),
            )
        except Exception:
            print(f"failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 1
        print(f"failed: caught {type(exc).__name__}: {exc}", file=sys.stderr)
        print("status failed")
        return 1


def main(argv: list[str] | None = None) -> int:
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        opts = parse_args(sys.argv[1:] if argv is None else argv)
        if opts.command != "run":
            raise Refuse("unknown command")
        return execute(opts)
    except Refuse as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
