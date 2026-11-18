#!/usr/bin/env python3
"""STUB matrix for pass05 harness self-tests. Never loop evidence."""

from __future__ import annotations


def mk(mode: str, expect_exit=0, needs_pid=False):
    def fn(ctx):
        args = [mode]
        if needs_pid:
            pidfile = ctx.run.fixtures / f"{ctx.id}-grandchild.pid"
            args.append(str(pidfile))
        row = ctx.cli(f"stub-{mode}", *args)
        ctx.check(f"stub {mode} exit {expect_exit}", row["exit"] == expect_exit, row["exit"])
    return fn


SETS = {
    "ok": [{"id": "S01", "title": "STUB ok", "fn": mk("ok")}],
    "fail": [{"id": "S02", "title": "STUB failing expectation", "fn": mk("fail", expect_exit=0)}],
    "crash": [{"id": "S03", "title": "STUB crash", "fn": mk("crash", expect_exit=0)}],
    "flush-sleep": [{"id": "S04", "title": "STUB flushes then times out", "fn": mk("flush-sleep")}],
    "flush-sleep-child": [{"id": "S05", "title": "STUB flushes, leaves a pipe-holding child, times out", "fn": mk("flush-sleep-child", needs_pid=True)}],
    "exit-leave-child": [{"id": "S06", "title": "STUB exits 0 and leaves a detached-stream child", "fn": mk("exit-leave-child", needs_pid=True)}],
    "exit-hold-child": [{"id": "S07", "title": "STUB exits 0 and leaves a pipe-holding child", "fn": mk("exit-hold-child", needs_pid=True)}],
    "crash-leave-child": [{"id": "S08", "title": "STUB leaves a child, then crashes", "fn": mk("crash-leave-child", expect_exit=1, needs_pid=True)}],
}
CASES = SETS["ok"]
