#!/usr/bin/env python3
"""STUB matrix for harness self-tests only. Never counted as loop evidence."""

from __future__ import annotations


def s_ok(ctx):
    row = ctx.cli("stub-ok", "ok")
    ctx.check("stub ok exits 0", row["exit"] == 0, row["exit"])
    ctx.check("stub output is labelled stub", (row["json"] or {}).get("stub") is True)


def s_fail(ctx):
    row = ctx.cli("stub-fail", "fail")
    ctx.check("expects exit 0 (stub deliberately exits 3)", row["exit"] == 0, row["exit"])


def s_sleep(ctx):
    pidfile = ctx.run.fixtures / "STUB-grandchild.pid"
    pidfile.parent.mkdir(parents=True, exist_ok=True)
    row = ctx.cli("stub-sleep", "sleep", str(pidfile))
    ctx.check("call returned (timed out)", row["timed_out"], row["timed_out"])


def s_crash(ctx):
    row = ctx.cli("stub-crash", "crash")
    ctx.check("expects exit 0 (stub deliberately crashes)", row["exit"] == 0, row["exit"])


SETS = {
    "pass": [{"id": "S01", "title": "STUB ok", "fn": s_ok}],
    "mixed": [
        {"id": "S01", "title": "STUB ok", "fn": s_ok},
        {"id": "S02", "title": "STUB failing expectation", "fn": s_fail},
        {"id": "S03", "title": "STUB timeout with grandchild", "fn": s_sleep},
        {"id": "S04", "title": "STUB crash keeps traceback", "fn": s_crash},
    ],
}
CASES = SETS["mixed"]
