#!/usr/bin/env python3
"""Development entry. where and validate resolve context and do not execute a candidate.

test-run executes one fixture payload through the pinned runner candidate.
run is refused. A --test flag does not authorize the live work book.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stop(message: str) -> None:
    print(f"stop: {message}", file=sys.stderr)
    raise SystemExit(2)


def take(args: list[str], flag: str) -> str:
    count = args.count(flag)
    if count == 0:
        stop(f"missing {flag}")
    if count != 1:
        stop(f"repeated {flag}")
    index = args.index(flag)
    if index + 1 >= len(args) or args[index + 1].startswith("--"):
        stop(f"missing value for {flag}")
    value = args[index + 1]
    del args[index : index + 2]
    return value


def directory(text: str) -> Path:
    path = Path(text)
    if not path.is_dir():
        stop("root is missing")
    return path.resolve()


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] not in ("where", "validate", "test-run"):
        stop("normal run is not activated")
    command = args.pop(0)
    code_root = Path(__file__).resolve().parent.parent
    context = load_module(Path(__file__).resolve().parent / "context.py", "librarian_context")
    try:
        if command in ("where", "validate"):
            root = directory(take(args, "--root"))
            if args:
                stop("unknown argument")
            config = context.load_config(root / "app" / "development-workspace.json")
            resolved = context.validate_context(root, config, execute=False)
            lines = context.report_lines(resolved)
            if command == "validate":
                lines.append("validate: pass")
            sys.stdout.write("\n".join(lines) + "\n")
            return
        test_flag = "--test" in args
        if test_flag:
            args.remove("--test")
        root = directory(take(args, "--root"))
        candidate = take(args, "--candidate")
        payload_sha256 = take(args, "--sha256").lower()
        if args:
            stop("unknown argument")
        del test_flag  # present or absent, the live root stays refused
        config = context.load_config(code_root / "app" / "development-workspace.json")
        if context.overlaps_live(root, code_root, config):
            stop("fixture root is the live workspace")
        fixture = context.load_fixture(root / "fixture.json")
        context.check_allowed_root(root, fixture)
        if not context.HEX64.fullmatch(payload_sha256):
            stop("payload hash is not sha256")
        context.validate_context(root, config, execute=True, runner_root=code_root)
        runner_path = context.resolve_under(code_root, config["runner"]["path"])
        if context.sha256_file(runner_path) != config["runner"]["sha256"]:
            stop("runner hash does not match")
        runner = load_module(runner_path, "librarian_runner_002")
        runner.perform(
            context,
            code_root=code_root,
            fixture_root=root,
            candidate=candidate,
            payload_sha256=payload_sha256,
            config=config,
            fixture=fixture,
        )
    except context.Stop as exc:
        stop(str(exc))


if __name__ == "__main__":
    main()
