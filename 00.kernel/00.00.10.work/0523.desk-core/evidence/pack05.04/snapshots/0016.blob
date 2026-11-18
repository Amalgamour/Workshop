"""JSON command line for python -m app.desk_core."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import (
    assert_done,
    init_book,
    pending,
    record_task,
    recover,
    register,
    retrieve,
    review,
    revise_task,
    show,
    submit_return,
)
from .identity import Refused, loads, require_object
from .pins import verify


def _print(payload: dict[str, object]) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _read_input(path: str) -> dict[str, object]:
    file = Path(path)
    if not file.is_file() or file.is_symlink():
        raise Refused("input", "input file is missing")
    return require_object(loads(file.read_bytes(), path), path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="app.desk_core")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--book", required=True)
    init.add_argument("--label", required=True)

    for name in ("record-task", "register", "review"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--book", required=True)
        cmd.add_argument("--input", required=True)

    revise = sub.add_parser("revise-task")
    revise.add_argument("--book", required=True)
    revise.add_argument("--input", required=True)
    revise.add_argument("--interrupt", action="store_true")

    submit = sub.add_parser("submit-return")
    submit.add_argument("--book", required=True)
    submit.add_argument("--input", required=True)
    submit.add_argument("--interrupt", action="store_true")
    submit.add_argument("--force-line")
    submit.add_argument("--force-pass")

    done = sub.add_parser("assert-done")
    done.add_argument("--book", required=True)
    done.add_argument("--page", required=True)
    done.add_argument("--subject", required=True)
    done.add_argument("--pass", dest="pass_id", required=True)
    done.add_argument("--worker", required=True)

    for name in ("show", "recover", "retrieve"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--book", required=True)
        cmd.add_argument("--page", required=True)
        cmd.add_argument("--subject", required=True)
        cmd.add_argument("--pass", dest="pass_id", required=True)

    waiting = sub.add_parser("pending")
    waiting.add_argument("--book", required=True)

    pins = sub.add_parser("pins")
    pins.add_argument("--repo")

    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            payload = init_book(args.book, args.label)
        elif args.command == "record-task":
            payload = record_task(args.book, _read_input(args.input))
        elif args.command == "register":
            payload = register(args.book, _read_input(args.input))
        elif args.command == "revise-task":
            payload = revise_task(args.book, _read_input(args.input), interrupt=args.interrupt)
        elif args.command == "review":
            payload = review(args.book, _read_input(args.input))
        elif args.command == "submit-return":
            payload = submit_return(
                args.book,
                _read_input(args.input),
                args.interrupt,
                args.force_line,
                args.force_pass,
            )
        elif args.command == "assert-done":
            payload = assert_done(args.book, args.page, args.subject, args.pass_id, args.worker)
        elif args.command == "show":
            payload = show(args.book, args.page, args.subject, args.pass_id)
        elif args.command == "recover":
            payload = recover(args.book, args.page, args.subject, args.pass_id)
        elif args.command == "retrieve":
            payload = retrieve(args.book, args.page, args.subject, args.pass_id)
        elif args.command == "pending":
            payload = pending(args.book)
        elif args.command == "pins":
            root = None if args.repo is None else Path(args.repo)
            payload = verify(root)
        else:
            raise Refused("command", "unknown command")
    except Refused as exc:
        _print(
            {
                "schema": "desk-core-result/1",
                "ok": False,
                "accepted": False,
                "refusal": exc.code,
                "message": exc.message,
                **exc.extra,
            }
        )
        return 2
    except Exception as exc:  # unexpected: surface it, do not pretend success
        _print(
            {
                "schema": "desk-core-result/1",
                "ok": False,
                "accepted": False,
                "refusal": "unexpected",
                "message": f"{type(exc).__name__}: {exc}",
            }
        )
        return 1
    _print(payload)
    if payload.get("interrupted") is True:
        return 3
    return 0
