#!/usr/bin/env python3
"""Observation reporter for the pass02 convergence workbook (0522/05.18).

Calls prepare, inspect, read, and recover on the sibling workbook. Exit 0 is
an observation. Flags are copied only after the observed envelope matches the
accepted hardening constants on inspect, read, and recover. An unsupported
envelope, a bad type, or a cross-command identity or currentness disagreement
withholds judgment and every current authority field under state noncurrent.
A malformed core response refuses. This module does not select a route.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HERE = Path(__file__).resolve().parent
WORKBOOK = HERE / "workbook.py"
PY = Path(sys.executable)
SCHEMA = "review-report-convergence/2"
ENVELOPE_SUPPORTED = {
    "accepted": False,
    "approved": False,
    "authority": "none",
    "closes_work": False,
    "releases_action": False,
    "task_association": "not-established",
}
ENVELOPE_CURRENT = (
    "accepted",
    "action_released",
    "approved",
    "authority",
    "closes_work",
    "releases_action",
    "task_association",
)
class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def _run(command: str, book: str, source: str, pass_id: str) -> dict:
    if not WORKBOOK.is_file():
        raise Refuse("workbook pin is missing")
    proc = subprocess.run(
        [str(PY), "-B", str(WORKBOOK), command, "--book", book, "--source", source, "--pass", pass_id],
        cwd=str(HERE),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        shell=False,
        check=False,
    )
    stderr = proc.stderr.decode("utf-8", "replace")
    if "Traceback (most recent call last)" in stderr:
        raise Refuse("workbook crashed")
    body = None
    if proc.stdout:
        try:
            body = json.loads(proc.stdout.decode("utf-8"))
        except json.JSONDecodeError:
            body = None
    if not isinstance(body, dict):
        message = stderr.strip() or "workbook returned no observation"
        raise Refuse(message[:500])
    body["exit"] = proc.returncode
    return body


def _rows(prepare: dict) -> list:
    form = prepare.get("form") if isinstance(prepare.get("form"), dict) else {}
    bindings = form.get("bindings") if isinstance(form.get("bindings"), dict) else {}
    rows = bindings.get("rows")
    return rows if isinstance(rows, list) else []


def _size_counts(rows: list) -> dict:
    counts = {"bool": 0, "missing": 0, "negative": 0, "other": 0}
    for row in rows:
        if not isinstance(row, dict) or "bytes" not in row or row.get("bytes") is None:
            if isinstance(row, dict):
                counts["missing"] += 1
            continue
        value = row.get("bytes")
        if type(value) is bool:
            counts["bool"] += 1
        elif type(value) is int and value < 0:
            counts["negative"] += 1
        elif type(value) is not int:
            counts["other"] += 1
    return counts


def envelope_problem(inspect: dict, read: dict, recover: dict) -> str | None:
    """None when inspect, read, and recover carry the same supported envelope."""
    bodies = (("inspect", inspect), ("read", read), ("recover", recover))
    for label, body in bodies:
        if not isinstance(body, dict):
            return f"{label}-not-object"
        if type(body.get("exit")) is not int:
            return f"{label}-exit-type"
        for key, want in ENVELOPE_SUPPORTED.items():
            if key not in body:
                return f"{label}-missing-{key}"
            got = body[key]
            if type(got) is not type(want) or got != want:
                return f"{label}-unsupported-{key}"
    for key in ENVELOPE_SUPPORTED:
        if read.get(key) != inspect.get(key) or recover.get(key) != inspect.get(key):
            return f"envelope-disagrees-{key}"
    return None


def _review_id(body: dict):
    value = body.get("review_id")
    if value is None:
        return None, True
    if isinstance(value, str) and value != "":
        return value, True
    return None, False


def cross_command_problem(inspect: dict, read: dict, recover: dict) -> str | None:
    """Disagreement about which review is current. A consistent stale or empty cut is not a problem."""
    read_id, read_ok = _review_id(read)
    recover_id, recover_ok = _review_id(recover)
    inspect_id, inspect_ok = _review_id(inspect)
    if not read_ok or not recover_ok or not inspect_ok:
        return "review-id-type"
    if read.get("exit") == 0 and type(read.get("stale")) is not bool:
        return "read-stale-type"
    if recover.get("exit") == 0 and type(recover.get("stale")) is not bool:
        return "recover-stale-type"
    known = [item for item in (read_id, recover_id, inspect_id) if item is not None]
    if len(set(known)) > 1:
        return "review-id-mismatch"
    read_current = read.get("exit") == 0 and read.get("stale") is False
    if read_current:
        if recover.get("exit") != 0:
            return "recover-exit"
        if recover.get("stale") is not False:
            return "recover-stale"
        if read_id is None or recover_id != read_id:
            return "recover-id"
        if inspect_id is not None and inspect_id != read_id:
            return "inspect-id"
        return None
    if read.get("stale") is True and recover.get("exit") == 0 and recover.get("stale") is False:
        return "recover-current-while-read-stale"
    if read_id is not None and recover_id is None and (read_current or read.get("stale") is True):
        return "recover-id-missing"
    return None


def _validated_flags() -> dict:
    flags = dict(ENVELOPE_SUPPORTED)
    flags["action_released"] = False
    flags["work_complete"] = False
    return flags


def _withhold_flags() -> dict:
    flags = {key: None for key in ENVELOPE_CURRENT}
    flags["work_complete"] = None
    return flags


def observe(book: str, source: str, pass_id: str) -> dict:
    prepare = _run("prepare", book, source, pass_id)
    inspect = _run("inspect", book, source, pass_id)
    read = _run("read", book, source, pass_id)
    recover = _run("recover", book, source, pass_id)
    measurement = prepare.get("measurement")
    envelope = envelope_problem(inspect, read, recover)
    crossed = None if envelope else cross_command_problem(inspect, read, recover)
    rows = _rows(prepare)
    invalid = [row for row in rows if not isinstance(row, dict)]
    counts = _size_counts(rows)
    problem = envelope or crossed
    if problem:
        state = "noncurrent"
        stale = None
    elif measurement != "complete" or bool(invalid) or any(counts.values()):
        state = "held"
        stale = read.get("stale") if isinstance(read.get("stale"), bool) else None
    elif read.get("exit") == 0 and read.get("stale") is False:
        state = "readable"
        stale = False
    elif read.get("stale") is True:
        state = "stale"
        stale = True
    elif read.get("exit") == 2:
        state = "not-recorded"
        stale = True if read.get("stale") is True else None
    else:
        state = "held"
        stale = read.get("stale") if isinstance(read.get("stale"), bool) else None
    body = {
        "schema": SCHEMA,
        "command": "review-report",
        "exit": 0,
        "state": state,
        "stale": stale,
        "review_id": read.get("review_id"),
        "recover_review_id": recover.get("review_id"),
        "inspect_review_id": inspect.get("review_id"),
        "custody": read.get("custody"),
        "exchange": prepare.get("exchange") if isinstance(prepare.get("exchange"), dict) else None,
        "measurement": measurement,
        "kind": prepare.get("kind"),
        "page": prepare.get("page"),
        "pass": prepare.get("pass"),
        "instance_id": prepare.get("instance_id"),
        "identity": "agreed" if not problem else problem,
        "read_exit": read.get("exit"),
        "recover_exit": recover.get("exit"),
        "inspect_exit": inspect.get("exit"),
        "current_applicability": read.get("current_applicability"),
        "instance_applicability": read.get("instance_applicability") or prepare.get("instance_applicability"),
        "unknowns": prepare.get("unknowns"),
        "envelope_problem": envelope,
    }
    if problem:
        body.update(_withhold_flags())
        body["judgment"] = None
        body["next_action"] = None
        body["envelope_withheld"] = {
            "cause": problem,
            "fields": list(ENVELOPE_CURRENT) + ["judgment", "next_action", "work_complete"],
            "provenance": "withheld-current-cut",
            "reason": "the observed envelope or cross-command currentness is not a current authority or action state",
        }
        supplied_envelope = {key: read.get(key) for key in ENVELOPE_CURRENT if key in read}
        body["historical_supplied"] = {
            "envelope": supplied_envelope,
            "judgment": read.get("judgment"),
            "next_action": read.get("next_action"),
            "provenance": "historical-supplied",
            "reason": "retained after the current cut was rejected; not a current judgment",
        }
    else:
        body.update(_validated_flags())
        if state == "readable":
            body["judgment"] = read.get("judgment")
            body["next_action"] = read.get("next_action")
        else:
            body["judgment"] = None
            body["next_action"] = None
            supplied = read.get("judgment")
            if supplied is not None:
                body["historical_supplied"] = {
                    "judgment": supplied,
                    "next_action": read.get("next_action"),
                    "provenance": "historical-supplied",
                    "reason": "retained after the current cut was rejected; not a current judgment",
                }
            body["envelope_withheld"] = {
                "cause": state,
                "fields": ["judgment", "next_action"],
                "provenance": "withheld-current-cut",
                "reason": "the current cut is not a current judgment; validated safety flags stay on a consistent observation",
            }
    if invalid:
        body["raw_rows"] = rows
        body["invalid_rows"] = {"count": len(invalid), "dropped": False, "provenance": "retained-malformed-intake"}
        body["measurement_withheld"] = "malformed intake rows were retained; counters are not a complete measured total"
    if any(counts.values()):
        body["size_observation"] = {**counts, "provenance": "row-byte-field"}
    return body


def emit(body: dict) -> None:
    sys.stdout.buffer.write((json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 6 or args[0::2] != ["--book", "--source", "--pass"]:
        print("refused: usage: report --book ABS --source PAGE --pass 05.NN", file=sys.stderr)
        return 2
    try:
        emit(observe(args[1], args[3], args[5]))
    except Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
