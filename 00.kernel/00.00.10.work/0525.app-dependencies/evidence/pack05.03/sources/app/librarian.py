#!/usr/bin/env python3
"""Development entry. where and validate resolve context and do not execute a candidate.

test-run executes one fixture payload through the pinned runner candidate.
bridge-test, bridge-status, and bridge-recover are the fixture-only worker exchange.
clerk-deliver copies one collected fixture delivery into the caller's claimed Clerk job.
pack-check, pack-preview, pack-assemble, and pack-verify call the pinned pack tools.
prime-status calls the pinned read-only Prime status tool on a caller-supplied registry.
prime-review, prime-guard, and prime-check-next call the pinned read-only Prime review tool on one explicit input.
review-loop forwards workbook prepare, form, record, inspect, publish, read, and recover to the pinned v7 door. The v4 fixture commands stay on the pinned v4 door. reproduce is not an app command.
authoring forwards form, start, add-note, add-item, revise, inspect, review, and freeze to the pinned authoring v2 door.
return-lines forwards status, lookup, and verify to the pinned return-access adapter, and reserve and capture to the pinned pass03 door.
boot-prepare, boot-check, boot-judge, and boot-show forward explicit arguments to the pinned recorded-boot tool.
batch-observe calls the pinned read-only batch observation tool on one explicit commit and path.
capture-return calls the pinned capture handoff on one absolute binding. It does not launch a worker.
The writable container is designated before fixture metadata is read.
run is refused. A --test flag does not authorize a fixture root.
A clean pack check is not release readiness.
A status result is not release readiness.
A review result is not a release.
An orientation result is not authorization.
An observation is not closure.
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
    if not args or args[0] not in (
        "where",
        "validate",
        "test-run",
        "bridge-test",
        "bridge-status",
        "bridge-recover",
        "clerk-deliver",
        "pack-check",
        "pack-preview",
        "pack-assemble",
        "pack-verify",
        "prime-status",
        "prime-review",
        "prime-guard",
        "prime-check-next",
        "boot-prepare",
        "boot-check",
        "boot-judge",
        "boot-show",
        "batch-observe",
        "capture-return",
        "review-loop",
        "authoring",
        "return-lines",
    ):
        stop("normal run is not activated")
    command = args.pop(0)
    code_root = Path(__file__).resolve().parent.parent
    if command == "review-loop":
        door = load_module(Path(__file__).resolve().parent / "review_loop_tools_v7.py", "librarian_review_loop_tools_v7")
        try:
            code = door.perform(args, code_root)
        except door.Refuse as exc:
            stop(str(exc))
        if type(code) is not int:
            stop("pinned review loop returned no exit code")
        raise SystemExit(code)
    if command == "authoring":
        door = load_module(Path(__file__).resolve().parent / "authoring_tools_v2.py", "librarian_authoring_tools_v2")
        try:
            code = door.perform(args, code_root)
        except door.Refuse as exc:
            stop(str(exc))
        if type(code) is not int:
            stop("pinned authoring tool returned no exit code")
        raise SystemExit(code)
    if command == "return-lines":
        door = load_module(Path(__file__).resolve().parent / "return_line_tools_v2.py", "librarian_return_line_tools_v2")
        try:
            code = door.perform(args, code_root)
        except door.Refuse as exc:
            stop(str(exc))
        if type(code) is not int:
            stop("pinned return line tool returned no exit code")
        raise SystemExit(code)
    if command in ("boot-prepare", "boot-check", "boot-judge", "boot-show"):
        boot = load_module(Path(__file__).resolve().parent / "boot_tools.py", "librarian_boot_tools")
        try:
            code = boot.perform(command, args, code_root)
        except boot.Refuse as exc:
            stop(str(exc))
        if type(code) is not int:
            stop("pinned boot tool returned no exit code")
        raise SystemExit(code)
    if command == "prime-status":
        intake = load_module(Path(__file__).resolve().parent / "prime_intake.py", "librarian_prime_intake")
        try:
            code = intake.perform(args, code_root)
        except intake.Refuse as exc:
            stop(str(exc))
        if type(code) is not int:
            stop("pinned status tool returned no exit code")
        raise SystemExit(code)
    if command in ("prime-review", "prime-guard", "prime-check-next"):
        door = load_module(Path(__file__).resolve().parent / "prime_review_tools.py", "librarian_prime_review_tools")
        try:
            code = door.perform(command, args, code_root)
        except door.Refuse as exc:
            stop(str(exc))
        if type(code) is not int:
            stop("pinned review tool returned no exit code")
        raise SystemExit(code)
    if command == "batch-observe":
        door = load_module(Path(__file__).resolve().parent / "batch_tools.py", "librarian_batch_tools")
        try:
            code = door.perform(args, code_root)
        except door.Refuse as exc:
            stop(str(exc))
        if type(code) is not int:
            stop("pinned observation tool returned no exit code")
        raise SystemExit(code)
    if command == "capture-return":
        door = load_module(Path(__file__).resolve().parent / "handoff_tools.py", "librarian_handoff_tools")
        try:
            code = door.perform(args, code_root)
        except door.Refuse as exc:
            stop(str(exc))
        if type(code) is not int:
            stop("pinned handoff tool returned no exit code")
        raise SystemExit(code)
    if command in ("pack-check", "pack-preview", "pack-assemble", "pack-verify"):
        tools = load_module(Path(__file__).resolve().parent / "prime_tools.py", "librarian_prime_tools")
        try:
            code = tools.perform(command, args, code_root)
        except tools.Refuse as exc:
            stop(str(exc))
        raise SystemExit(code)
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
        if command in ("bridge-test", "bridge-status", "bridge-recover"):
            if "--test" in args:
                args.remove("--test")
            root = directory(take(args, "--root"))
            explicit = take(args, "--container") if "--container" in args else None
            job = delivery = recovery = None
            if command == "bridge-test":
                job = take(args, "--job")
            elif command == "bridge-status":
                delivery = take(args, "--delivery")
            else:
                delivery = take(args, "--delivery")
                recovery = take(args, "--recovery-request")
            if args:
                stop("unknown argument")
            bridge = load_module(Path(__file__).resolve().parent / "worker_bridge.py", "librarian_worker_bridge")
            report = bridge.perform(
                context,
                command,
                code_root,
                root,
                job_rel=job,
                delivery=delivery,
                recovery_rel=recovery,
                explicit=explicit,
            )
            sys.stdout.write(report.text)
            if report.code != 0:
                raise SystemExit(report.code)
            return
        if command == "clerk-deliver":
            root = directory(take(args, "--root"))
            explicit = take(args, "--container") if "--container" in args else None
            link = take(args, "--link")
            actor = take(args, "--as")
            instructions = take(args, "--instructions-base")
            if args:
                stop("unknown argument")
            seam = load_module(Path(__file__).resolve().parent / "clerk_seam.py", "librarian_clerk_seam")
            result = seam.perform(
                context,
                code_root,
                root,
                link_rel=link,
                actor=actor,
                instructions_base=instructions,
                explicit=explicit,
            )
            sys.stdout.write(result.text)
            if result.code != 0:
                raise SystemExit(result.code)
            return
        test_flag = "--test" in args
        if test_flag:
            args.remove("--test")
        root = directory(take(args, "--root"))
        candidate = take(args, "--candidate")
        payload_sha256 = take(args, "--sha256").lower()
        explicit = take(args, "--container") if "--container" in args else None
        if args:
            stop("unknown argument")
        del test_flag  # present or absent, it does not designate a container
        config = context.load_config(code_root / "app" / "development-workspace.json")
        if context.is_filesystem_root(root):
            stop("fixture container is a filesystem root")
        if context.overlaps_live(root, code_root, config):
            stop("fixture root is the live workspace")
        container = context.select_container(root, code_root, explicit)
        context.guard_workspace_path(root, code_root)
        fixture = context.load_fixture(root / "fixture.json")
        fixture["designated_container"] = str(container)
        context.check_allowed_root(root, fixture)
        if not context.HEX64.fullmatch(payload_sha256):
            stop("payload hash is not sha256")
        payload = context.resolve_under(root, candidate)
        output = context.resolve_under(root, fixture["output"])
        context.guard_workspace_path(payload, code_root)
        context.guard_workspace_path(output, code_root)
        context.validate_context(root, config, execute=True, runner_root=code_root)
        runner_path = context.resolve_under(code_root, config["runner"]["path"])
        if context.sha256_file(runner_path) != config["runner"]["sha256"]:
            stop("runner hash does not match")
        runner = load_module(runner_path, "librarian_runner_003")
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
