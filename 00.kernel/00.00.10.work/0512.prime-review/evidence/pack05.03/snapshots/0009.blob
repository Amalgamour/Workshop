#!/usr/bin/env python3
"""Checks for the pinned Prime review entry.

Expected refusals are counted apart from passes and from unexpected failures.
A report or a hold check is not authority and is not a release.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
LIBRARIAN = REPO / "app" / "librarian.py"
TOOL = REPO / "labs" / "prime-review-pass01" / "prime_review.py"
EXAMPLES = REPO / "labs" / "prime-review-pass01" / "examples"
ACTUAL_INPUT = REPO / "00.kernel/00.00.10.work/0512.prime-review/evidence/prime-review05.01/actual-prime-review-input.json"
ACTUAL_OUTPUT = REPO / "00.kernel/00.00.10.work/0512.prime-review/evidence/prime-review05.01/actual-prime-review-output.json"
PIN = "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0"
REPARSE = 0x400
NEEDED = (
    "app/librarian.py",
    "app/prime_review_tools.py",
    "app/prime-review.json",
    "labs/prime-review-pass01/prime_review.py",
)
FROZEN = NEEDED + (
    "app/prime_tools.py",
    "app/prime-tools.json",
    "app/prime_intake.py",
    "app/prime-intake.json",
    "app/boot_tools.py",
    "app/batch_tools.py",
    "app/handoff_tools.py",
    "labs/prime-review-pass01/README.md",
    "labs/prime-review-pass01/tests/test_prime_review.py",
    "00.kernel/00.00.10.work/0157.prime-review-0501/return.md",
    "00.kernel/00.00.10.work/0158.colab-workflow-repair-0502/return.md",
    "00.kernel/00.00.10.work/0159.colab-exchange-layout-0503/return.md",
    "00.kernel/00.00.10.work/0507.prime-support/05.17.md",
)


class Skip(Exception):
    pass


class Suite:
    def __init__(self) -> None:
        self.passed: list[str] = []
        self.refusals: list[str] = []
        self.skipped: list[str] = []
        self.failed: list[str] = []

    def ok(self, name: str) -> None:
        self.passed.append(name)
        print(f"pass {name}", flush=True)

    def refuse(self, name: str) -> None:
        self.refusals.append(name)
        print(f"expected-refusal {name}", flush=True)

    def skip(self, name: str) -> None:
        self.skipped.append(name)
        print(f"skip {name}", flush=True)

    def fail(self, name: str) -> None:
        self.failed.append(name)
        print(f"fail {name}", flush=True)


SUITE = Suite()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_reparse(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def run(argv: list[str], cwd: Path, env: dict) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
    )


def live_bytes() -> dict[str, bytes]:
    return {rel: (REPO / rel).read_bytes() for rel in FROZEN}


def pycache_names() -> list[str]:
    found = []
    for folder in (REPO / "app", REPO / "labs" / "prime-review-pass01"):
        if not folder.exists():
            continue
        for path in folder.rglob("*"):
            if path.name == "__pycache__" or path.suffix == ".pyc":
                found.append(str(path.relative_to(REPO)))
    return sorted(found)


def scratch_names() -> list[str]:
    scratch = REPO / "app" / "scratch"
    if not scratch.exists():
        return ["<absent>"]
    return sorted(str(path.relative_to(scratch)) for path in scratch.rglob("*"))


def sentinel_bytes(path: Path) -> bytes:
    return ("from pathlib import Path\nPath(%r).write_text('ran', encoding='utf-8')\n" % str(path)).encode("utf-8")


def copy_code(dest: Path) -> None:
    for rel in NEEDED:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / rel).read_bytes())


def assert_stop(proc: subprocess.CompletedProcess[bytes], message: str) -> None:
    text = proc.stderr.decode("utf-8").replace("\r\n", "\n")
    if proc.returncode != 2 or f"stop: {message}" not in text or proc.stdout != b"":
        raise AssertionError((proc.returncode, text, proc.stdout[:400]))


def wrapped(command: str, args: list[str], cwd: Path, env: dict, librarian: Path | None = None) -> subprocess.CompletedProcess[bytes]:
    entry = librarian or LIBRARIAN
    return run([PY, "-B", str(entry), command, *args], cwd, env)


def direct(subcommand: str, args: list[str], cwd: Path, env: dict) -> subprocess.CompletedProcess[bytes]:
    return run([PY, "-B", str(TOOL), subcommand, *args], cwd, env)


def matched(command: str, subcommand: str, args: list[str], cwd: Path, env: dict) -> subprocess.CompletedProcess[bytes]:
    left = direct(subcommand, args, cwd, env)
    right = wrapped(command, args, cwd, env)
    if right.returncode != left.returncode or right.stdout != left.stdout or right.stderr != left.stderr:
        raise AssertionError((
            "wrapper", right.returncode, right.stdout[:400], right.stderr[:400],
            "direct", left.returncode, left.stdout[:400], left.stderr[:400],
        ))
    if b"stop:" in right.stdout or b"stop:" in right.stderr:
        raise AssertionError(right.stderr)
    return right


def load_example(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def write_json(path: Path, document: dict) -> None:
    path.write_bytes((json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


def facts(proc: subprocess.CompletedProcess[bytes]) -> dict:
    return json.loads(proc.stdout.decode("utf-8"))


def main() -> None:
    print("command python -B app/tests/test_prime_review_tools.py", flush=True)
    print("repo D:/Git/lib-build", flush=True)
    print("python " + PY, flush=True)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    before = live_bytes()
    before_cache = pycache_names()
    before_scratch = scratch_names()
    if sha256(before["labs/prime-review-pass01/prime_review.py"]) != PIN:
        raise SystemExit("accepted review module pin drifted before the suite")
    tmp = tempfile.TemporaryDirectory(prefix="review0502-")
    root = Path(tmp.name)
    foreign = root / "foreign-cwd"
    foreign.mkdir()
    decoy = foreign / "decoy-ran.txt"
    decoy_tool = foreign / "labs" / "prime-review-pass01" / "prime_review.py"
    decoy_tool.parent.mkdir(parents=True)
    decoy_tool.write_bytes(sentinel_bytes(decoy))
    junctions: list[Path] = []

    def check(name: str, fn, kind: str) -> None:
        try:
            fn()
        except Skip:
            SUITE.skip(name)
        except Exception:
            traceback.print_exc()
            SUITE.fail(name)
        else:
            if kind == "refusal":
                SUITE.refuse(name)
            else:
                SUITE.ok(name)

    def report_args(path: Path, root_path: Path | None = None, as_json: bool = False) -> list[str]:
        args = ["--input", str(path)]
        if root_path is not None:
            args.extend(["--root", str(root_path)])
        if as_json:
            args.append("--json")
        return args

    def pass_report(name: str, path: Path, expect: str, root_path: Path | None = None) -> None:
        def body() -> None:
            proc = matched("prime-review", "report", report_args(path, root_path, True), foreign, env)
            if proc.returncode != 0 or proc.stderr != b"":
                raise AssertionError((proc.returncode, proc.stderr, proc.stdout[:300]))
            report = facts(proc)
            if report["effective"] != expect or report["closes_work"] or report["releases_action"] or report["authenticates_actor"]:
                raise AssertionError(report["effective"])
            if report["authority"] != "none" or report["tasks_added"] != []:
                raise AssertionError(report["tasks_added"])
            if b"\r\n" in proc.stdout:
                raise AssertionError("stdout gained CR")
            if decoy.exists():
                raise AssertionError("cwd decoy ran")
        check(name, body, "pass")

    try:
        continue_path = EXAMPLES / "continue.json"
        develop_path = EXAMPLES / "develop.json"
        director_path = EXAMPLES / "director-input.json"
        read_path = EXAMPLES / "guard-read-0517.json"
        appoint_path = EXAMPLES / "guard-appoint-0517.json"

        pass_report("continue-json", continue_path, "continue")
        pass_report("develop-json", develop_path, "develop")

        def complete_case() -> None:
            document = load_example("continue.json")
            sections = document["judgment"]["sections"]
            sections["for_model"] = None
            sections.update({
                "outcome_evidence": "SUPPLIED EXAMPLE. The granted typo correction is on the page.",
                "limits": "SUPPLIED EXAMPLE. This account does not close the work.",
                "tests_note": "SUPPLIED EXAMPLE. A green check is evidence, not closure.",
                "tests_passed": True,
                "learning": "SUPPLIED EXAMPLE. Keep the wording repair separate from a new task.",
                "preservation": "SUPPLIED EXAMPLE. Keep the page bytes.",
                "remaining_choices": ["Prime still reads the account."],
                "findings_account": [{"finding_id": "notes/page.md#typo", "status": "accepted"}],
                "finish_assessments": [{"criterion_id": "typo", "assessment": "met"}],
            })
            document["judgment"]["outcome"] = "complete"
            document["judgment"]["finding"] = "SUPPLIED EXAMPLE. The typo correction is accounted."
            document["gaps"] = []
            document["holds"] = []
            path = root / "complete.json"
            write_json(path, document)
            proc = matched("prime-review", "report", report_args(path, as_json=True), foreign, env)
            if proc.returncode != 0 or proc.stderr != b"":
                raise AssertionError((proc.returncode, proc.stderr[:400], proc.stdout[:400]))
            report = facts(proc)
            if report["effective"] != "complete-as-supplied" or report["closes_work"] or report["tasks_added"]:
                raise AssertionError((report["effective"], report["closes_work"], report["tasks_added"]))
            if b"Tests do not close this work." not in proc.stdout:
                raise AssertionError("tests_passed lost its limit")
        check("complete-json", complete_case, "pass")

        def director_case() -> None:
            proc = matched("prime-review", "report", report_args(director_path, as_json=True), foreign, env)
            if proc.returncode != 1 or proc.stderr != b"":
                raise AssertionError((proc.returncode, proc.stderr[:300]))
            report = facts(proc)
            if report["effective"] != "hold" or report["closes_work"] or report["releases_action"]:
                raise AssertionError(report["effective"])
        check("director-hold", director_case, "pass")

        def stale_case() -> None:
            document = load_example("continue.json")
            question = document["sources"][0]["content_sha256"]
            document["holds"] = [{
                "hold_id": "H1",
                "finding_id": "notes/page.md#typo",
                "kind": "director-judgment",
                "question_id": "Q1",
                "question_revision": "r2",
                "question_sha256": question,
                "dependent_scope": ["ship-code"],
            }]
            document["answers"] = [{
                "answer_id": "A1",
                "question_id": "Q1",
                "question_revision": "r1",
                "question_sha256": question,
                "reply": "SUPPLIED EXAMPLE. This reply names the older revision.",
                "provenance": {
                    "actor_label": "Director",
                    "role": "director",
                    "evidence": "SUPPLIED EXAMPLE reply. Not a live Director session.",
                },
                "disposition": "brief-approval",
            }]
            path = root / "stale.json"
            write_json(path, document)
            proc = matched("prime-review", "report", report_args(path, as_json=True), foreign, env)
            if proc.returncode != 1:
                raise AssertionError(proc.returncode)
            report = facts(proc)
            if report["holds"][0]["status"] != "stale" or "answer is stale: A1" not in report["attention"]:
                raise AssertionError(report["holds"][0])
        check("stale-source", stale_case, "pass")

        def guard_case(name: str, path: Path, result: str, code: int) -> None:
            def body() -> None:
                proc = matched("prime-guard", "guard", report_args(path, REPO, True), foreign, env)
                if proc.returncode != code or proc.stderr != b"":
                    raise AssertionError((proc.returncode, proc.stderr[:300], proc.stdout[:300]))
                guard = facts(proc)
                if guard["result"] != result or guard["releases_action"] or guard["closes_work"]:
                    raise AssertionError((guard["result"], guard["releases_action"], guard["closes_work"]))
                other = matched("prime-check-next", "check-next", report_args(path, REPO, True), foreign, env)
                if other.returncode != proc.returncode or other.stdout != proc.stdout or other.stderr != proc.stderr:
                    raise AssertionError("check-next diverged from guard")
            check(name, body, "pass")

        guard_case("independent-read", read_path, "independent-of-holds", 0)
        guard_case("dependent-appoint", appoint_path, "blocked", 1)

        def actual_case() -> None:
            saved = json.loads(ACTUAL_OUTPUT.read_text(encoding="utf-8"))
            proc = matched(
                "prime-review",
                "report",
                report_args(ACTUAL_INPUT, REPO, True),
                foreign,
                env,
            )
            if proc.returncode != saved["exit"] or proc.returncode != 0 or proc.stderr != b"":
                raise AssertionError((proc.returncode, proc.stderr[:300]))
            if facts(proc) != saved["report"]:
                raise AssertionError("actual report facts changed")
            plain = matched("prime-review", "report", report_args(ACTUAL_INPUT, REPO, False), foreign, env)
            if plain.returncode != 0 or b"closes_work: false" not in plain.stdout or b"releases_action: false" not in plain.stdout:
                raise AssertionError(plain.returncode)
            if b"authority: none" not in plain.stdout:
                raise AssertionError("authority line missing")
        check("actual-prime-review", actual_case, "pass")

        def tool_refusal() -> None:
            path = root / "broken.json"
            path.write_bytes(b"{")
            proc = matched("prime-review", "report", report_args(path), foreign, env)
            if proc.returncode != 2 or proc.stdout != b"" or not proc.stderr.startswith(b"refused:"):
                raise AssertionError((proc.returncode, proc.stderr[:300], proc.stdout[:200]))
        check("tool-refusal-propagates", tool_refusal, "refusal")

        def missing_root_for_bind() -> None:
            proc = matched("prime-review", "report", report_args(ACTUAL_INPUT, None, True), foreign, env)
            if proc.returncode != 2 or proc.stdout != b"" or not proc.stderr.startswith(b"refused:"):
                raise AssertionError((proc.returncode, proc.stderr[:300]))
        check("bind-without-root", missing_root_for_bind, "refusal")

        def stop_case(name: str, args: list[str], message: str, command: str = "prime-review") -> None:
            def body() -> None:
                proc = wrapped(command, args, foreign, env)
                assert_stop(proc, message)
                if decoy.exists():
                    raise AssertionError("cwd decoy ran")
            check(name, body, "refusal")

        stop_case("missing-input", [], "missing --input")
        stop_case("repeated-input", ["--input", str(continue_path), "--input", str(continue_path)], "repeated --input")
        stop_case("repeated-json", ["--input", str(continue_path), "--json", "--json"], "repeated --json")
        stop_case("repeated-root", ["--input", str(continue_path), "--root", str(REPO), "--root", str(REPO)], "repeated --root")
        stop_case("missing-input-value", ["--input"], "missing value for --input")
        stop_case("missing-root-value", ["--input", str(continue_path), "--root"], "missing value for --root")
        stop_case("unknown-flag", ["--input", str(continue_path), "--format", "json"], "unsupported argument")
        stop_case("equals-form", ["--input=" + str(continue_path)], "unsupported argument")
        stop_case("relative-input", ["--input", "notes/page.md"], "input path must be absolute")
        stop_case("unc-input", ["--input", "\\\\server\\share\\input.json"], "UNC path input")
        stop_case("dotdot-input", ["--input", str(root / ".." / "input.json")], "unsafe path input")
        stop_case("relative-root", ["--input", str(continue_path), "--root", "notes"], "root path must be absolute")
        stop_case("dotdot-root", ["--input", str(continue_path), "--root", str(root / ".." )], "unsafe path root")
        stop_case("draft-flag", ["--input", str(continue_path), "--dest", str(root / "out.md")], "draft is not exposed")
        stop_case("draft-token", ["draft", "--input", str(continue_path)], "draft is not exposed")
        stop_case("timeout-flag", ["--input", str(continue_path), "--timeout", "1"], "caller timeout is refused")
        stop_case("tool-override", ["--input", str(continue_path), "--tool", str(TOOL)], "caller tool override is refused")
        stop_case("unknown-command", [], "normal run is not activated", "prime-draft")
        stop_case("run-still-refused", [], "normal run is not activated", "run")
        stop_case("prime-status-still-checks-args", [], "missing --registry", "prime-status")
        stop_case("where-still-checks-args", [], "missing --root", "where")

        def bare_entry_fix() -> None:
            proc = run([PY, "-B", str(LIBRARIAN)], foreign, env)
            assert_stop(proc, "normal run is not activated")
        check("bare-entry", bare_entry_fix, "refusal")

        def readonly_case() -> None:
            path = root / "readonly.json"
            raw = continue_path.read_bytes()
            path.write_bytes(raw)
            os.chmod(path, stat.S_IREAD)
            try:
                proc = matched("prime-review", "report", report_args(path, as_json=True), foreign, env)
                if proc.returncode != 0 or path.read_bytes() != raw:
                    raise AssertionError((proc.returncode, path.read_bytes() == raw))
                report = facts(proc)
                if report["closes_work"] or report["releases_action"]:
                    raise AssertionError("readonly run changed the meaning")
            finally:
                os.chmod(path, stat.S_IWRITE)
        check("readonly-input", readonly_case, "pass")

        def nonutf8_case() -> None:
            document = load_example("continue.json")
            document["judgment"]["finding"] = "The café sign stays bound."
            document["judgment"]["sections"]["prime_finding"] = "The café sign stays bound."
            path = root / "cafe.json"
            write_json(path, document)
            local = env.copy()
            local["PYTHONIOENCODING"] = "cp1252"
            local["PYTHONUTF8"] = "0"
            proc = matched("prime-review", "report", report_args(path), foreign, local)
            if proc.returncode != 0 or "café".encode("utf-8") not in proc.stdout:
                raise AssertionError((proc.returncode, proc.stdout[:200]))
            if b"\r\n" in proc.stdout:
                raise AssertionError("non-utf8 host gained CR")
        check("nonutf8-host", nonutf8_case, "pass")

        copy = root / "copy-code"
        copy_code(copy)
        marker = root / "sentinel-ran.txt"

        def hash_mismatch() -> None:
            target = copy / "labs" / "prime-review-pass01" / "prime_review.py"
            target.write_bytes(sentinel_bytes(marker))
            proc = wrapped(
                "prime-review",
                report_args(continue_path, as_json=True),
                foreign,
                env,
                copy / "app" / "librarian.py",
            )
            assert_stop(proc, "pinned tool hash does not match: prime_review")
            if marker.exists():
                raise AssertionError("changed pin launched")
        check("changed-pin-no-launch", hash_mismatch, "refusal")

        def declaration_mismatch() -> None:
            target = copy / "labs" / "prime-review-pass01" / "prime_review.py"
            target.write_bytes((REPO / "labs" / "prime-review-pass01" / "prime_review.py").read_bytes())
            declaration = json.loads((copy / "app" / "prime-review.json").read_text(encoding="utf-8"))
            declaration["tools"]["prime_review"]["sha256"] = "0" * 64
            write_json(copy / "app" / "prime-review.json", declaration)
            proc = wrapped(
                "prime-review",
                report_args(continue_path),
                foreign,
                env,
                copy / "app" / "librarian.py",
            )
            assert_stop(proc, "prime review declaration does not match the pinned tools")
            if marker.exists():
                raise AssertionError("declaration drift launched")
        check("changed-declaration-no-launch", declaration_mismatch, "refusal")

        def linked_input() -> None:
            folder = root / "junction-target"
            folder.mkdir()
            link = root / "junction-input"
            made = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(folder)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                shell=False,
            )
            if made.returncode != 0 or not is_reparse(link):
                raise Skip()
            junctions.append(link)
            proc = wrapped("prime-review", ["--input", str(link)], foreign, env)
            assert_stop(proc, "input path is linked and was not followed")
        check("linked-input", linked_input, "refusal")

        def linked_tool() -> None:
            real = copy / "labs" / "prime-review-pass01"
            aside = root / "tool-aside"
            if real.exists() and not is_reparse(real):
                real.rename(aside)
            planted = root / "planted-tool"
            planted.mkdir()
            (planted / "prime_review.py").write_bytes(sentinel_bytes(marker))
            made = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(real), str(planted)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                shell=False,
            )
            if made.returncode != 0 or not is_reparse(real):
                raise Skip()
            junctions.append(real)
            declaration = {
                "schema": "librarian-prime-review",
                "version": 1,
                "_note": "Development wiring for the accepted read-only Prime review tool. Not kernel law. A report or a hold check is not authority and is not a release.",
                "tools": {
                    "prime_review": {
                        "path": "labs/prime-review-pass01/prime_review.py",
                        "sha256": PIN,
                    }
                },
            }
            write_json(copy / "app" / "prime-review.json", declaration)
            proc = wrapped(
                "prime-review",
                report_args(continue_path),
                foreign,
                env,
                copy / "app" / "librarian.py",
            )
            assert_stop(proc, "tool path is linked and was not followed")
            if marker.exists():
                raise AssertionError("linked tool launched")
        check("linked-tool-no-launch", linked_tool, "refusal")

        if decoy.exists():
            raise SystemExit("foreign decoy ran")
        if live_bytes() != before:
            changed = [rel for rel in FROZEN if live_bytes()[rel] != before[rel]]
            raise SystemExit("frozen bytes changed: " + ", ".join(changed))
        if pycache_names() != before_cache:
            raise SystemExit("pycache changed")
        if scratch_names() != before_scratch:
            raise SystemExit("scratch changed")
    finally:
        for link in junctions:
            if link.exists() or is_reparse(link):
                subprocess.run(
                    ["cmd", "/c", "rmdir", str(link)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                    shell=False,
                )
        tmp.cleanup()

    print(
        f"passed {len(SUITE.passed)} expected-refusal {len(SUITE.refusals)} "
        f"skipped {len(SUITE.skipped)} failed {len(SUITE.failed)}",
        flush=True,
    )
    if SUITE.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
