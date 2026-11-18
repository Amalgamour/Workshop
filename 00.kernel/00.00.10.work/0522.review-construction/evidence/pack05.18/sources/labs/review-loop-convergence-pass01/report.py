#!/usr/bin/env python3
"""Observation reporter for the convergence workbook (0522/05.17).

Calls prepare, read, and recover on the canonical convergence workbook.
Exit 0 is an observation. Safety flags stay none/false. An unstable cut
withholds judgment and next_action and keeps a historical copy when one
was read. Malformed intake rows are retained. This module does not select
a route and does not grant authority.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
WORKBOOK = REPO / "labs" / "review-loop-convergence-pass01" / "workbook.py"
PY = Path(sys.executable)
SCHEMA = "review-report-convergence/1"
FLAGS = {
    "accepted": False,
    "action_released": False,
    "approved": False,
    "authority": "none",
    "closes_work": False,
    "releases_action": False,
    "task_association": "not-established",
    "work_complete": False,
}
WITHHELD = ("judgment", "next_action")


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def _run(command: str, book: str, source: str, pass_id: str) -> dict:
    proc = subprocess.run(
        [str(PY), "-B", str(WORKBOOK), command, "--book", book, "--source", source, "--pass", pass_id],
        cwd=str(REPO),
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


def observe(book: str, source: str, pass_id: str) -> dict:
    prepare = _run("prepare", book, source, pass_id)
    read = _run("read", book, source, pass_id)
    recover = _run("recover", book, source, pass_id)
    measurement = prepare.get("measurement")
    if measurement != "complete":
        state = "held"
    elif read.get("exit") == 0 and read.get("stale") is False:
        state = "readable"
    elif read.get("stale") is True:
        state = "stale"
    elif read.get("exit") == 2:
        state = "not-recorded"
    else:
        state = "held"
    stale = read.get("stale") if isinstance(read.get("stale"), bool) else None
    if state == "readable":
        stale = False
    elif state == "stale":
        stale = True
    rows = _rows(prepare)
    invalid = [row for row in rows if not isinstance(row, dict)]
    counts = _size_counts(rows)
    unstable = state != "readable" or bool(invalid) or any(counts.values())
    read_id = read.get("review_id")
    recover_id = recover.get("review_id")
    identity = "agreed"
    if isinstance(read_id, str) and isinstance(recover_id, str) and read_id != recover_id:
        identity = "mismatch"
        unstable = True
    exchange = prepare.get("exchange") if isinstance(prepare.get("exchange"), dict) else None
    body = {
        "schema": SCHEMA,
        "command": "review-report",
        "exit": 0,
        "state": state,
        "stale": stale,
        "review_id": read_id,
        "recover_review_id": recover_id,
        "custody": read.get("custody"),
        "exchange": exchange,
        "measurement": measurement,
        "kind": prepare.get("kind"),
        "page": prepare.get("page"),
        "pass": prepare.get("pass"),
        "instance_id": prepare.get("instance_id"),
        "identity": identity,
        "read_exit": read.get("exit"),
        "recover_exit": recover.get("exit"),
        "current_applicability": read.get("current_applicability"),
        "instance_applicability": read.get("instance_applicability") or prepare.get("instance_applicability"),
        "unknowns": prepare.get("unknowns"),
    }
    body.update(FLAGS)
    if unstable:
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
            "cause": state if identity == "agreed" else "mismatch",
            "fields": list(WITHHELD),
            "provenance": "withheld-current-cut",
            "reason": "the current cut is not a current authority or action state; safety flags stay none/false",
        }
    else:
        body["judgment"] = read.get("judgment")
        body["next_action"] = read.get("next_action")
    if invalid:
        body["raw_rows"] = rows
        body["invalid_rows"] = {"count": len(invalid), "dropped": False, "provenance": "retained-malformed-intake"}
        body["measurement_withheld"] = "malformed intake rows were retained; counters are not a complete measured total"
    if any(counts.values()):
        body["size_observation"] = {**counts, "provenance": "row-byte-field"}
    return body


def emit(body: dict) -> None:
    sys.stdout.buffer.write((json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8"))
