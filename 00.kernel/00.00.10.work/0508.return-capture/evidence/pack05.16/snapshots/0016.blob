#!/usr/bin/env python3
"""Fixture checks for the recorded-boot app entry.

The accepted boot fixture factory builds disposable repositories. Production code
does not import it. Expected refusals are counted apart from passes.
An orientation result is not authorization.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
LIBRARIAN = REPO / "app" / "librarian.py"
TOOL = REPO / "labs" / "prime-boot-pass01" / "prime_boot.py"
REPARSE = 0x400
AUTH = "none; orientation grants no new work authority"
MARK = "状态"
NEEDED = (
    "app/librarian.py",
    "app/boot_tools.py",
    "app/prime-boot.json",
    "labs/prime-boot-pass01/prime_boot.py",
    "labs/prime-support-pass01/prime_support.py",
    "labs/prime-support-pass01/clerk_adapter.py",
    "labs/book-orientation-pass01/check_book.py",
    "labs/return-capture-pass01/return_capture.py",
    "labs/return-capture-pass01/return_inspect.py",
    "labs/clerk-handoff-pass02/clerk.py",
)
FROZEN = NEEDED + (
    "app/README.md",
    "app/prime_intake.py",
    "app/prime-intake.json",
    "app/prime_tools.py",
    "app/prime-tools.json",
    "app/context.py",
    "app/tests/test_boot_tools.py",
    "app/tests/test_entry.py",
    "app/tests/test_prime_intake.py",
    "app/tests/test_prime_tools.py",
    "labs/prime-boot-pass01/tests/test_prime_boot.py",
    "labs/prime-boot-pass01/README.md",
    "00.kernel/00.00.10.work/0504.app-entry/05.15.md",
    "00.kernel/00.00.10.work/0504.app-entry/06.15.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/CONTRACT.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/before/librarian.py",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/boot-entry05.15/before/README.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.14/review.md",
    "00.kernel/00.00.10.work/0130.boot-entry-0515/reservation.json",
    "00.kernel/00.00.10.work/0130.boot-entry-0515/01.md",
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


def writable_retry(func, path, exc) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def load_factory():
    path = REPO / "labs" / "prime-boot-pass01" / "tests" / "test_prime_boot.py"
    spec = importlib.util.spec_from_file_location("accepted_boot_fixture", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the accepted boot fixture")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(argv: list[str], cwd: Path, env: dict) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False, shell=False, timeout=300,
    )


def text_of(raw: bytes) -> str:
    return raw.decode("utf-8").replace("\r\n", "\n")


def norm(raw: bytes, *paths: Path) -> str:
    value = text_of(raw)
    ordered = sorted((str(path) for path in paths), key=len, reverse=True)
    for path in ordered:
        value = value.replace(path, "<PATH>")
    return value


def assert_stop(proc: subprocess.CompletedProcess[bytes], message: str) -> None:
    text = text_of(proc.stderr)
    if proc.returncode != 2 or f"stop: {message}" not in text or proc.stdout != b"":
        raise AssertionError((proc.returncode, text, proc.stdout[:300]))


def tree_files(root: Path) -> dict[str, str]:
    found = {}
    if not root.exists():
        return found
    for path in root.rglob("*"):
        if not path.is_file() or is_reparse(path):
            continue
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == ".git":
            continue
        found[relative.as_posix()] = sha256(path.read_bytes())
    return found


def file_hashes(root: Path) -> dict[str, str]:
    found = {}
    if not root.exists():
        return found
    for path in sorted(root.iterdir()):
        if path.is_file() and not is_reparse(path):
            found[path.name] = sha256(path.read_bytes())
    return found


def live_bytes() -> dict[str, bytes]:
    return {rel: (REPO / rel).read_bytes() for rel in FROZEN}


def names_under(root: Path) -> list[str]:
    if not root.exists():
        return ["<absent>"]
    return sorted(str(path.relative_to(root)) for path in root.rglob("*"))


def pycache_names() -> list[str]:
    found = []
    roots = [
        REPO / "app",
        REPO / "labs" / "prime-boot-pass01",
        REPO / "labs" / "prime-support-pass01",
        REPO / "labs" / "book-orientation-pass01",
        REPO / "labs" / "return-capture-pass01",
        REPO / "labs" / "clerk-handoff-pass02",
    ]
    for folder in roots:
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


def copy_code(dest: Path) -> Path:
    for rel in NEEDED:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / rel).read_bytes())
    return dest


def stage(attempt: Path, name: str) -> dict:
    return json.loads((attempt / name).read_text(encoding="utf-8"))


def main() -> None:
    print("command python -B app/tests/test_boot_tools.py", flush=True)
    print("repo D:/Git/lib-build", flush=True)
    print("python " + PY, flush=True)
    print("limit subprocess-timeout-seconds 300", flush=True)
    print("limit no-model no-network no-live-install", flush=True)
    print("limit records one named attempt under the explicit root", flush=True)
    factory = load_factory()

    class Holder(factory.Fixture):
        def test_holder(self) -> None:
            return None

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    before = live_bytes()
    before_cache = pycache_names()
    before_scratch = scratch_names()
    before_app = sorted(path.name for path in (REPO / "app").iterdir())
    evidence = REPO / "00.kernel" / "00.00.10.work" / "0504.app-entry" / "evidence" / "boot-entry05.15"
    member = REPO / "00.kernel" / "00.00.10.work" / "0130.boot-entry-0515"
    before_evidence = names_under(evidence)
    before_member = names_under(member)
    cases: list = []
    junctions: list[Path] = []
    foreign_root = tempfile.TemporaryDirectory(prefix="boot0515-")
    foreign = Path(foreign_root.name)
    decoy = foreign / "decoy-ran.txt"

    def open_case():
        case = Holder("test_holder")
        case.setUp()
        cases.append(case)
        renamed = case.tmp.parent / (MARK + "-" + case.records.name)
        case.records.rename(renamed)
        case.records = renamed
        sibling = case.records.parent / ("keep-" + case.records.name)
        sibling.mkdir()
        (sibling / "marker.txt").write_bytes(b"keep\n")
        case.sibling = sibling
        outside = case.tmp / "outside-records"
        outside.mkdir()
        (outside / "marker.txt").write_bytes(b"keep\n")
        case.work_before = tree_files(case.repo)
        return case

    def close_case(case) -> None:
        sibling = getattr(case, "sibling", None)
        try:
            case.tearDown()
        finally:
            if sibling is not None and sibling.exists():
                shutil.rmtree(sibling, onexc=writable_retry)

    def direct(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
        return run([PY, "-B", str(TOOL), *argv], foreign, env)

    def wrapped(command: str, argv: list[str]) -> subprocess.CompletedProcess[bytes]:
        return run([PY, "-B", str(LIBRARIAN), command, *argv], foreign, env)

    def paths_for(*items: Path) -> tuple[Path, ...]:
        return tuple(sorted(items, key=lambda path: len(str(path)), reverse=True))

    def matched(left, right, *paths: Path) -> None:
        if left.returncode != right.returncode or norm(left.stdout, *paths) != norm(right.stdout, *paths) or left.stderr != right.stderr:
            raise AssertionError((
                "direct", left.returncode, text_of(left.stdout)[:500], text_of(left.stderr)[:200],
                "wrapper", right.returncode, text_of(right.stdout)[:500], text_of(right.stderr)[:200],
            ))

    def require_code(proc, code: int) -> None:
        if proc.returncode != code or proc.stderr != b"":
            raise AssertionError((proc.returncode, text_of(proc.stderr)[:300], text_of(proc.stdout)[:400]))

    def watch(case, fn):
        before = {path.name for path in case.tmp.iterdir()}
        proc = fn()
        extra = {path.name for path in case.tmp.iterdir()} - before
        if extra:
            raise AssertionError("wrote outside the attempt: " + " ".join(sorted(extra)))
        return proc

    def records_only(case, attempt: Path) -> None:
        if sorted(path.name for path in case.records.iterdir()) != [attempt.name]:
            raise AssertionError(sorted(path.name for path in case.records.iterdir()))
        if (case.sibling / "marker.txt").read_bytes() != b"keep\n":
            raise AssertionError("sibling marker outside records changed")
        if (case.tmp / "outside-records" / "marker.txt").read_bytes() != b"keep\n":
            raise AssertionError("fixture marker outside records changed")
        if tree_files(case.repo) != case.work_before:
            raise AssertionError("fixture worktree changed")

    def prepare_pair(left_case, right_case):
        left_request = left_case.write_json("req-a1.json", left_case.request())
        right_request = right_case.write_json("req-a1.json", right_case.request())
        left_args = ["--request", str(left_request), "--records", str(left_case.records), "--attempt", "a1"]
        right_args = ["--attempt", "a1", "--records", str(right_case.records), "--request", str(right_request)]
        left = watch(left_case, lambda: direct(["prepare", *left_args]))
        right = watch(right_case, lambda: wrapped("boot-prepare", right_args))
        if MARK.encode("utf-8") not in left.stdout or MARK.encode("utf-8") not in right.stdout:
            raise AssertionError("unicode records path missing from stdout bytes")
        scope = paths_for(left_case.records, right_case.records, left_case.records / "a1", right_case.records / "a1")
        matched(left, right, *scope)
        require_code(left, 0)
        require_code(right, 0)
        left_attempt = left_case.records / "a1"
        right_attempt = right_case.records / "a1"
        if left_attempt == right_attempt or not left_attempt.is_dir() or not right_attempt.is_dir():
            raise AssertionError("prepare did not use two independent attempt directories")
        left_outcome = stage(left_attempt, "19.prepare-outcome.json")
        right_outcome = stage(right_attempt, "19.prepare-outcome.json")
        if left_outcome["status"] != "prepared" or right_outcome["status"] != "prepared":
            raise AssertionError((left_outcome.get("status"), right_outcome.get("status")))
        if left_outcome["authority"] != AUTH or right_outcome["authority"] != AUTH:
            raise AssertionError((left_outcome.get("authority"), right_outcome.get("authority")))
        left_text = {item["path"]: item["text"] for item in stage(left_attempt, "09.packet.json")["refs"]}
        right_text = {item["path"]: item["text"] for item in stage(right_attempt, "09.packet.json")["refs"]}
        if left_text != right_text:
            raise AssertionError("packet ref texts diverged")
        records_only(left_case, left_attempt)
        records_only(right_case, right_attempt)
        return left_attempt, right_attempt

    def check_boundary() -> None:
        tool = (REPO / "app" / "boot_tools.py").read_text(encoding="utf-8")
        entry = (REPO / "app" / "librarian.py").read_text(encoding="utf-8")
        if "importlib" in tool or "test_prime_boot" in tool or "exec_module" in tool:
            raise AssertionError("boot_tools imports the lab or the fixture")
        if "prime_boot" in entry or "importlib.exec_module" in entry:
            raise AssertionError("librarian loads the boot lab itself")
        if decoy.exists():
            raise AssertionError("decoy ran before a command")

    def check_valid() -> None:
        left_case = open_case()
        right_case = open_case()
        left_attempt, right_attempt = prepare_pair(left_case, right_case)
        print("evidence prepare exit 0 prepared authority none unicode path", flush=True)
        left_answers = left_case.write_json("ans-a1.json", left_case.good_answers(left_attempt))
        right_answers = right_case.write_json("ans-a1.json", right_case.good_answers(right_attempt))
        left = watch(left_case, lambda: direct(["check", "--attempt", str(left_attempt), "--answers", str(left_answers)]))
        right = watch(right_case, lambda: wrapped("boot-check", ["--answers", str(right_answers), "--attempt", str(right_attempt)]))
        scope = paths_for(left_attempt, right_attempt, left_case.records, right_case.records, left_case.tmp, right_case.tmp)
        matched(left, right, *scope)
        require_code(left, 0)
        require_code(right, 0)
        if not text_of(left.stdout).startswith("checks ok\n"):
            raise AssertionError(text_of(left.stdout)[:300])
        if stage(left_attempt, "22.checks.json")["status"] != "ok" or stage(right_attempt, "22.checks.json")["status"] != "ok":
            raise AssertionError("checks status diverged")
        print("evidence check exit 0 checks ok", flush=True)
        for attempt in (left_attempt, right_attempt):
            before_hash = file_hashes(attempt)
            case = left_case if attempt is left_attempt else right_case
            if attempt is left_attempt:
                shown = watch(case, lambda: direct(["show", "--attempt", str(attempt)]))
                shown_json = watch(case, lambda: direct(["show", "--attempt", str(attempt), "--json"]))
            else:
                shown = watch(case, lambda: wrapped("boot-show", ["--attempt", str(attempt)]))
                shown_json = watch(case, lambda: wrapped("boot-show", ["--json", "--attempt", str(attempt)]))
            require_code(shown, 0)
            require_code(shown_json, 0)
            if file_hashes(attempt) != before_hash:
                raise AssertionError("show wrote the attempt")
            if MARK.encode("utf-8") not in shown.stdout:
                raise AssertionError("text show lost the unicode path")
            body = json.loads(text_of(shown_json.stdout))
            if body["attempt"] != str(attempt) or body["authority"] != AUTH or body["stage"] != "checked" or body["complete"] is not True:
                raise AssertionError(body)
            if "not oriented" not in body["state"] or "fixture-judge" in body["authority"]:
                raise AssertionError(body)
            if MARK.encode("utf-8") in shown_json.stdout:
                raise AssertionError("json show did not escape the unicode path")
            if "\\u72b6\\u6001" not in text_of(shown_json.stdout):
                raise AssertionError("json show escaped path missing")
        left_show = watch(left_case, lambda: direct(["show", "--attempt", str(left_attempt)]))
        right_show = watch(right_case, lambda: wrapped("boot-show", ["--attempt", str(right_attempt)]))
        matched(left_show, right_show, *scope)
        left_json = json.loads(text_of(watch(left_case, lambda: direct(["show", "--json", "--attempt", str(left_attempt)])).stdout))
        right_json = json.loads(text_of(watch(right_case, lambda: wrapped("boot-show", ["--attempt", str(right_attempt), "--json"])).stdout))
        left_json["attempt"] = "<ATTEMPT>"
        right_json["attempt"] = "<ATTEMPT>"
        if left_json != right_json:
            raise AssertionError((left_json, right_json))
        print("evidence show read-only stage checked authority none", flush=True)
        left_doc = left_case.judgement(left_attempt)
        right_doc = right_case.judgement(right_attempt)
        left_doc["grades"]["O1"] = "wrong"
        right_doc["grades"]["O1"] = "wrong"
        left_judgement = left_case.write_json("jud-a1.json", left_doc)
        right_judgement = right_case.write_json("jud-a1.json", right_doc)
        before_left = file_hashes(left_attempt)
        before_right = file_hashes(right_attempt)
        judged_left = watch(left_case, lambda: direct(["judge", "--attempt", str(left_attempt), "--judgement", str(left_judgement)]))
        judged_right = watch(right_case, lambda: wrapped("boot-judge", ["--judgement", str(right_judgement), "--attempt", str(right_attempt)]))
        matched(judged_left, judged_right, *scope)
        require_code(judged_left, 1)
        require_code(judged_right, 1)
        if "fixture-judge" in text_of(judged_left.stdout) or "fixture-judge" in text_of(judged_right.stdout):
            raise AssertionError("reviewer label leaked into judge stdout")
        for attempt, before_hash in ((left_attempt, before_left), (right_attempt, before_right)):
            outcome = stage(attempt, "39.outcome.json")
            recorded = stage(attempt, "31.judgement.json")
            if outcome["outcome"] != "not-oriented" or outcome["authority"] != AUTH:
                raise AssertionError(outcome)
            if "fixture-judge" in outcome["authority"] or not str(outcome["authority"]).startswith("none"):
                raise AssertionError(outcome["authority"])
            if recorded["reviewer"] != "fixture-judge":
                raise AssertionError(recorded.get("reviewer"))
            if "not authentication or authority" not in recorded["note"]:
                raise AssertionError(recorded.get("note"))
            if file_hashes(attempt) == before_hash:
                raise AssertionError("judge wrote nothing")
        show_left = file_hashes(left_attempt)
        show_right = file_hashes(right_attempt)
        require_code(watch(left_case, lambda: direct(["show", "--attempt", str(left_attempt)])), 0)
        require_code(watch(right_case, lambda: wrapped("boot-show", ["--attempt", str(right_attempt)])), 0)
        if file_hashes(left_attempt) != show_left or file_hashes(right_attempt) != show_right:
            raise AssertionError("show after judge wrote the attempt")
        records_only(left_case, left_attempt)
        records_only(right_case, right_attempt)
        print("evidence judge exit 1 not-oriented authority none reviewer label not authority", flush=True)

    def check_malformed() -> None:
        left_case = open_case()
        right_case = open_case()
        left_attempt, right_attempt = prepare_pair(left_case, right_case)
        left_doc = {"schema": "not-answers", "attempt_id": left_attempt.name, "answers": {}}
        right_doc = {"schema": "not-answers", "attempt_id": right_attempt.name, "answers": {}}
        left_answers = left_case.write_json("ans-a1.json", left_doc)
        right_answers = right_case.write_json("ans-a1.json", right_doc)
        left = watch(left_case, lambda: direct(["check", "--attempt", str(left_attempt), "--answers", str(left_answers)]))
        right = watch(right_case, lambda: wrapped("boot-check", ["--attempt", str(right_attempt), "--answers", str(right_answers)]))
        scope = paths_for(left_attempt, right_attempt, left_case.tmp, right_case.tmp)
        matched(left, right, *scope)
        require_code(left, 1)
        require_code(right, 1)
        if not text_of(left.stdout).startswith("checks failed:"):
            raise AssertionError(text_of(left.stdout)[:300])
        if stage(left_attempt, "22.checks.json")["status"] != "failed" or stage(right_attempt, "22.checks.json")["status"] != "failed":
            raise AssertionError("malformed answers were not recorded as failed")
        records_only(left_case, left_attempt)
        records_only(right_case, right_attempt)
        print("evidence malformed answers exit 1 checks failed", flush=True)

    def check_incomplete() -> None:
        left_case = open_case()
        right_case = open_case()
        left_attempt, right_attempt = prepare_pair(left_case, right_case)

        def plant(case, attempt: Path) -> Path:
            raw = json.dumps(case.good_answers(attempt)).encode("utf-8")
            (attempt / "20.answers.raw").write_bytes(raw)
            return case.write_json("ans-a1.json", raw)

        left_answers = plant(left_case, left_attempt)
        right_answers = plant(right_case, right_attempt)
        before_left = file_hashes(left_attempt)
        before_right = file_hashes(right_attempt)
        left = watch(left_case, lambda: direct(["check", "--answers", str(left_answers), "--attempt", str(left_attempt)]))
        right = watch(right_case, lambda: wrapped("boot-check", ["--attempt", str(right_attempt), "--answers", str(right_answers)]))
        scope = paths_for(left_attempt, right_attempt)
        matched(left, right, *scope)
        require_code(left, 3)
        require_code(right, 3)
        if not text_of(left.stdout).startswith("incomplete:"):
            raise AssertionError(text_of(left.stdout)[:300])
        if file_hashes(left_attempt) != before_left or file_hashes(right_attempt) != before_right:
            raise AssertionError("incomplete replay wrote the attempt")
        if (left_attempt / "22.checks.json").exists() or (right_attempt / "22.checks.json").exists():
            raise AssertionError("incomplete replay wrote checks")
        for attempt, before_hash, channel in (
            (left_attempt, before_left, "direct"),
            (right_attempt, before_right, "wrapper"),
        ):
            case = left_case if channel == "direct" else right_case
            if channel == "direct":
                shown = watch(case, lambda: direct(["show", "--attempt", str(attempt)]))
                shown_json = watch(case, lambda: direct(["show", "--attempt", str(attempt), "--json"]))
            else:
                shown = watch(case, lambda: wrapped("boot-show", ["--attempt", str(attempt)]))
                shown_json = watch(case, lambda: wrapped("boot-show", ["--json", "--attempt", str(attempt)]))
            require_code(shown, 0)
            require_code(shown_json, 0)
            body = json.loads(text_of(shown_json.stdout))
            if body["stage"] != "check-incomplete" or body["complete"] is not False or body["authority"] != AUTH:
                raise AssertionError(body)
            if file_hashes(attempt) != before_hash:
                raise AssertionError("show of an incomplete attempt wrote")
        records_only(left_case, left_attempt)
        records_only(right_case, right_attempt)
        print("evidence incomplete replay exit 3 show read-only check-incomplete", flush=True)

    def check_relative_records() -> None:
        request = foreign / "dummy-request.json"
        request.write_bytes(b"{}\n")
        relative = "relative-records"
        left = direct(["prepare", "--request", str(request), "--records", relative, "--attempt", "a1"])
        right = wrapped("boot-prepare", ["--records", relative, "--attempt", "a1", "--request", str(request)])
        matched(left, right)
        require_code(left, 2)
        require_code(right, 2)
        if not text_of(left.stdout).startswith("refused:"):
            raise AssertionError(text_of(left.stdout)[:300])
        if (foreign / relative).exists() or (REPO / relative).exists():
            raise AssertionError("relative records path created a directory")
        print("evidence relative records exit 2 refused no directory", flush=True)

    def check_not_attempt() -> None:
        empty = foreign / "not-an-attempt"
        empty.mkdir()
        before_hash = file_hashes(empty)
        left = direct(["show", "--attempt", str(empty)])
        right = wrapped("boot-show", ["--json", "--attempt", str(empty)])
        matched(left, right, empty)
        require_code(left, 2)
        if not text_of(left.stdout).startswith("refused:"):
            raise AssertionError(text_of(left.stdout)[:200])
        if file_hashes(empty) != before_hash:
            raise AssertionError("refused show wrote")
        print("evidence not an attempt exit 2 refused", flush=True)

    def check_arguments() -> None:
        code = copy_code(foreign / "pin-args")
        ran = foreign / "ran-args.txt"
        (code / "labs" / "prime-boot-pass01" / "prime_boot.py").write_bytes(sentinel_bytes(ran))
        entry = code / "app" / "librarian.py"
        calls = (
            ("missing --attempt", ["boot-show"]),
            ("repeated --attempt", ["boot-show", "--attempt", str(foreign), "--attempt", str(foreign)]),
            ("unsupported argument", ["boot-show", "positional"]),
            ("missing value for --attempt", ["boot-show", "--attempt", ""]),
            ("missing value for --attempt", ["boot-show", "--attempt", "--json"]),
            ("repeated --json", ["boot-show", "--json", "--json", "--attempt", str(foreign)]),
            ("missing --answers", ["boot-check", "--attempt", str(foreign)]),
            ("missing --judgement", ["boot-judge", "--attempt", str(foreign)]),
            ("missing --records", ["boot-prepare", "--request", str(foreign), "--attempt", "a1"]),
            ("unsupported argument", ["boot-judge", "--attempt", str(foreign), "--judgement", str(foreign), "--json"]),
        )
        for message, argv in calls:
            proc = run([PY, "-B", str(entry), *argv], foreign, env)
            assert_stop(proc, message)
            if b"pinned tool hash" in proc.stderr or ran.exists():
                raise AssertionError("argument refusal reached the pin or the tool")
        print("evidence argument refusals before pin", flush=True)

    def check_clerk_pin() -> None:
        code = copy_code(foreign / "pin-clerk")
        clerk = code / "labs" / "clerk-handoff-pass02" / "clerk.py"
        data = bytearray(clerk.read_bytes())
        data[-1] ^= 0x01
        clerk.write_bytes(bytes(data))
        records = foreign / "records-clerk"
        records.mkdir()
        request = foreign / "clerk-request.json"
        request.write_bytes(b"{}\n")
        proc = run(
            [PY, "-B", str(code / "app" / "librarian.py"), "boot-prepare",
             "--request", str(request), "--records", str(records), "--attempt", "a1"],
            foreign, env,
        )
        assert_stop(proc, "pinned tool hash does not match: clerk")
        if any(records.iterdir()):
            raise AssertionError("clerk pin mismatch started the tool")

    def check_backend_pin() -> None:
        code = copy_code(foreign / "pin-backend")
        ran = foreign / "ran-backend.txt"
        (code / "labs" / "prime-boot-pass01" / "prime_boot.py").write_bytes(sentinel_bytes(ran))
        proc = run(
            [PY, "-B", str(code / "app" / "librarian.py"), "boot-show", "--attempt", str(foreign)],
            foreign, env,
        )
        assert_stop(proc, "pinned tool hash does not match: prime_boot")
        if ran.exists():
            raise AssertionError("backend pin mismatch started the tool")

    def check_declaration() -> None:
        code = copy_code(foreign / "pin-declaration")
        ran = foreign / "ran-declaration.txt"
        (code / "labs" / "prime-boot-pass01" / "prime_boot.py").write_bytes(sentinel_bytes(ran))
        declaration = code / "app" / "prime-boot.json"
        document = json.loads(declaration.read_text(encoding="utf-8"))
        document["tools"]["clerk"]["sha256"] = "0" * 64
        declaration.write_bytes((json.dumps(document, indent=2) + "\n").encode("utf-8"))
        proc = run(
            [PY, "-B", str(code / "app" / "librarian.py"), "boot-show", "--attempt", str(foreign), "--json"],
            foreign, env,
        )
        assert_stop(proc, "prime boot declaration does not match the pinned tools")
        if ran.exists():
            raise AssertionError("declaration mismatch started the tool")

    def check_junction() -> None:
        code = copy_code(foreign / "pin-junction")
        lab = code / "labs" / "prime-boot-pass01"
        outside = foreign / "outside-lab"
        shutil.copytree(lab, outside)
        shutil.rmtree(lab)
        made = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(lab), str(outside)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if made.returncode != 0:
            raise AssertionError(made.stderr)
        junctions.append(lab)
        ran = foreign / "ran-junction.txt"
        (outside / "prime_boot.py").write_bytes(sentinel_bytes(ran))
        proc = run(
            [PY, "-B", str(code / "app" / "librarian.py"), "boot-show", "--attempt", str(foreign)],
            foreign, env,
        )
        assert_stop(proc, "tool path is linked and was not followed")
        if ran.exists():
            raise AssertionError("junction was followed")

    def check_symlink() -> None:
        code = copy_code(foreign / "pin-symlink")
        tool = code / "labs" / "prime-boot-pass01" / "prime_boot.py"
        outside = foreign / "linked-prime-boot.py"
        outside.write_bytes(tool.read_bytes())
        tool.unlink()
        try:
            os.symlink(outside, tool)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                raise Skip("file symlink privilege WinError 1314") from exc
            raise
        proc = run(
            [PY, "-B", str(code / "app" / "librarian.py"), "boot-show", "--attempt", str(foreign)],
            foreign, env,
        )
        assert_stop(proc, "tool path is linked and was not followed")
        if outside.read_bytes() != (REPO / "labs" / "prime-boot-pass01" / "prime_boot.py").read_bytes():
            raise AssertionError("symlink target changed")

    def check_normal(argv: list[str], message: str) -> None:
        proc = run([PY, "-B", str(LIBRARIAN), *argv], foreign, env)
        assert_stop(proc, message)
        if decoy.exists():
            raise AssertionError("foreign decoy ran")

    try:
        (foreign / "labs" / "prime-boot-pass01").mkdir(parents=True)
        (foreign / "labs" / "prime-boot-pass01" / "prime_boot.py").write_bytes(sentinel_bytes(decoy))
        checks = [
            ("production-boundary", "pass", check_boundary),
            ("valid-flow-matches-direct", "pass", check_valid),
            ("malformed-answers-match-direct", "pass", check_malformed),
            ("incomplete-replay-matches-direct", "pass", check_incomplete),
            ("relative-records-match-direct", "pass", check_relative_records),
            ("not-attempt-matches-direct", "pass", check_not_attempt),
            ("arguments-before-pin", "refuse", check_arguments),
            ("wrong-clerk-pin", "refuse", check_clerk_pin),
            ("wrong-backend-pin", "refuse", check_backend_pin),
            ("declaration-pin", "refuse", check_declaration),
            ("junction-pin", "refuse", check_junction),
            ("file-symlink-pin", "refuse", check_symlink),
            ("normal-bare", "refuse", lambda: check_normal([], "normal run is not activated")),
            ("normal-run", "refuse", lambda: check_normal(["run"], "normal run is not activated")),
            ("unknown-command", "refuse", lambda: check_normal(["boot"], "normal run is not activated")),
        ]
        for name, kind, fn in checks:
            if SUITE.failed:
                break
            try:
                fn()
            except Skip as exc:
                SUITE.skip(f"{name} {exc}")
                continue
            except Exception:
                SUITE.fail(name)
                traceback.print_exc()
                break
            if kind == "pass":
                SUITE.ok(name)
            else:
                SUITE.refuse(name)
        if not SUITE.failed and decoy.exists():
            SUITE.fail("foreign-decoy")
            print("decoy ran", flush=True)
        if not SUITE.failed:
            after = live_bytes()
            if after != before:
                changed = [rel for rel in FROZEN if after[rel] != before[rel]]
                SUITE.fail("frozen-sources")
                print("changed " + " ".join(changed), flush=True)
            elif pycache_names() != before_cache or scratch_names() != before_scratch:
                SUITE.fail("bytecode-or-scratch")
                print(f"cache {pycache_names()} scratch {scratch_names()}", flush=True)
            elif sorted(path.name for path in (REPO / "app").iterdir()) != before_app:
                SUITE.fail("app-names")
            elif names_under(evidence) != before_evidence or names_under(member) != before_member:
                SUITE.fail("evidence-or-member-names")
            else:
                SUITE.ok("frozen-sources")
                for rel in (
                    "app/librarian.py",
                    "app/boot_tools.py",
                    "app/prime-boot.json",
                    "app/README.md",
                    "app/tests/test_boot_tools.py",
                ):
                    data = (REPO / rel).read_bytes()
                    print(f"hash {rel} {sha256(data)} {len(data)}", flush=True)
    finally:
        for case in cases:
            try:
                close_case(case)
            except Exception:
                traceback.print_exc()
        for link in junctions:
            if os.path.lexists(link):
                os.rmdir(link)
        foreign_root.cleanup()
    print(
        f"summary pass {len(SUITE.passed)} expected-refusal {len(SUITE.refusals)} "
        f"skip {len(SUITE.skipped)} fail {len(SUITE.failed)}",
        flush=True,
    )
    if SUITE.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
