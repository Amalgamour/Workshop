#!/usr/bin/env python3
"""Fixture checks for the read-only batch-observe entry.

Expected refusals are counted apart from passes and from unexpected failures.
An observation is not closure and is not release readiness.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
LIBRARIAN = REPO / "app" / "librarian.py"
READER = REPO / "labs" / "batch-observation-pass01" / "batch_observe.py"
COMMIT = "4cca1d2e9ac845e82a2d44df432f8f7f6584f1e5"
PAGE = "00.kernel/00.00.10.work/0508.return-capture/05.10.md"
BOOK = REPO / "00.kernel" / "00.00.10.work"
REPARSE = 0x400
Z_STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$")
NEEDED = (
    "app/librarian.py",
    "app/batch_tools.py",
    "app/batch-observer.json",
    "labs/batch-observation-pass01/batch_observe.py",
    "labs/prime-support-pass01/prime_support.py",
    "labs/prime-support-pass01/clerk_adapter.py",
    "labs/return-capture-pass01/return_inspect.py",
    "labs/return-capture-pass01/return_capture.py",
)
FROZEN = NEEDED + (
    "app/README.md",
    "app/boot_tools.py",
    "app/prime-boot.json",
    "app/prime_intake.py",
    "app/tests/test_entry.py",
    "app/tests/test_boot_tools.py",
    "app/tests/test_batch_tools.py",
    "labs/batch-observation-pass01/README.md",
    "labs/batch-observation-pass01/tests/test_batch_observe.py",
    "00.kernel/00.00.10.work/0508.return-capture/05.16.md",
    "00.kernel/00.00.10.work/0508.return-capture/06.17.md",
    "00.kernel/00.00.10.work/0508.return-capture/evidence/prime-review05.15/review.md",
    "00.kernel/00.00.10.work/0144.batch-reader-entry-0516/01.md",
    "00.kernel/00.00.10.work/0144.batch-reader-entry-0516/reservation.json",
    "00.kernel/00.00.10.work/0128.pack-assembly-0501/receipt.json",
    "00.kernel/00.00.10.work/0129.assembly-capture-0510/receipt.json",
    PAGE,
)
STAMP_KEYS = ("observation_started_at", "observation_finished_at")


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


def git(real: str, repo: Path, args: list[str], env: dict) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [real, "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
        shell=False,
    )


def require_git(proc: subprocess.CompletedProcess[bytes], label: str) -> None:
    if proc.returncode != 0:
        raise AssertionError(label + " " + proc.stderr.decode("utf-8", "replace"))


def live_bytes() -> dict[str, bytes]:
    return {rel: (REPO / rel).read_bytes() for rel in FROZEN}


def pycache_names() -> list[str]:
    roots = (
        REPO / "app",
        REPO / "labs" / "batch-observation-pass01",
        REPO / "labs" / "prime-support-pass01",
        REPO / "labs" / "return-capture-pass01",
    )
    found = []
    for folder in roots:
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


def copy_code(dest: Path) -> Path:
    for rel in NEEDED:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / rel).read_bytes())
    return dest


def sentinel_bytes(path: Path) -> bytes:
    text = "from pathlib import Path\nPath(%r).write_text('ran', encoding='utf-8')\n" % str(path)
    return text.encode("utf-8")


def assert_stop(proc: subprocess.CompletedProcess[bytes], message: str) -> None:
    text = proc.stderr.decode("utf-8").replace("\r\n", "\n")
    if proc.returncode != 2 or f"stop: {message}" not in text or proc.stdout != b"":
        raise AssertionError((proc.returncode, text, proc.stdout[:200]))


def observe_argv(repo: str, commit: str, path: str, book: str | None = None) -> list[str]:
    argv = [
        "batch-observe",
        "--repo",
        repo,
        "--commit",
        commit,
        "--path",
        path,
        "--json",
    ]
    if book is not None:
        argv[1:1] = ["--members-book", book]
    return argv


def direct_argv(repo: str, commit: str, path: str, book: str | None = None) -> list[str]:
    argv = [PY, "-B", str(READER), "observe", "--repo", repo, "--commit", commit, "--path", path, "--json"]
    if book is not None:
        argv.extend(["--members-book", book])
    return argv


def call_app(librarian: Path, argv: list[str], cwd: Path, env: dict) -> subprocess.CompletedProcess[bytes]:
    return run([PY, "-B", str(librarian), *argv], cwd, env)


def strip_stamps(document: dict) -> dict:
    cloned = json.loads(json.dumps(document))
    for item in cloned["custody"]["observations"]:
        for key in STAMP_KEYS:
            item.pop(key, None)
    return cloned


def live_stamps(document: dict) -> list[str]:
    found = []
    for item in document["custody"]["observations"]:
        for key in STAMP_KEYS:
            value = item.get(key)
            if value is not None:
                found.append(value)
    return found


def main() -> None:
    print("command python -B app/tests/test_batch_tools.py", flush=True)
    print("repo D:/Git/lib-build", flush=True)
    print("python " + PY, flush=True)
    real = shutil.which("git.exe") or shutil.which("git")
    if not real:
        raise SystemExit("git is missing")
    print("git " + real, flush=True)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    before = live_bytes()
    before_cache = pycache_names()
    before_scratch = scratch_names()
    head_before = git(real, REPO, ["rev-parse", "HEAD"], env)
    require_git(head_before, "workshop head")
    workshop_head = head_before.stdout.decode("utf-8").strip()
    print("workshop-head " + workshop_head, flush=True)
    junctions: list[Path] = []
    tmp = tempfile.TemporaryDirectory(prefix="entry0516-")
    root = Path(tmp.name)
    try:
        foreign = root / "foreign-cwd"
        foreign.mkdir()
        repo = root / "fixture-repo"
        repo.mkdir()
        require_git(git(real, repo, ["init"], env), "init")
        require_git(git(real, repo, ["config", "user.email", "fixture@example.invalid"], env), "email")
        require_git(git(real, repo, ["config", "user.name", "Fixture"], env), "name")
        require_git(git(real, repo, ["config", "commit.gpgsign", "false"], env), "gpg")
        require_git(git(real, repo, ["config", "core.autocrlf", "false"], env), "autocrlf")
        page = repo / "pages" / "note.md"
        page.parent.mkdir()
        page_text = (
            "# 05 — café 状态\n"
            "version: 001\n"
            "state: draft\n"
            "\n"
            "## Assignment\n"
            "Executor: café 状态.\n"
            "\n"
            "## Return pointer\n"
            "PENDING.\n"
            "\n"
            "## Review — Codex Prime\n"
            "PENDING.\n"
        )
        page.write_bytes(page_text.encode("utf-8"))
        require_git(git(real, repo, ["add", "pages/note.md"], env), "add")
        require_git(git(real, repo, ["commit", "-m", "fixture"], env), "commit")
        head = git(real, repo, ["rev-parse", "HEAD"], env)
        require_git(head, "head")
        fixture_commit = head.stdout.decode("utf-8").strip()
        fixture_before = page.read_bytes()
        status_before = git(real, repo, ["status", "--porcelain"], env)
        require_git(status_before, "status")
        if status_before.stdout != b"":
            raise AssertionError(status_before.stdout)

        def same_backend(proc: subprocess.CompletedProcess[bytes], direct: subprocess.CompletedProcess[bytes]) -> None:
            if proc.returncode != direct.returncode or proc.stdout != direct.stdout or proc.stderr != direct.stderr:
                raise AssertionError((proc.returncode, direct.returncode, proc.stderr, direct.stderr, proc.stdout[:120], direct.stdout[:120]))

        def check_corpus_bytes() -> None:
            argv = observe_argv(str(REPO), COMMIT, PAGE)
            proc = call_app(LIBRARIAN, argv, foreign, env)
            direct = run(direct_argv(str(REPO), COMMIT, PAGE), foreign, env)
            same_backend(proc, direct)
            if proc.returncode != 1 or proc.stdout == b"":
                raise AssertionError((proc.returncode, proc.stderr, proc.stdout[:160]))
            body = json.loads(proc.stdout.decode("utf-8"))
            if body["schema"] != "batch-observation/1" or body["authority"] != "none":
                raise AssertionError(body["schema"])
            if body["source"]["kind"] != "git-blob" or body["source"]["commit"] != COMMIT:
                raise AssertionError(body["source"])
            for key in ("live_observed_at", *STAMP_KEYS):
                if body["source"][key] is not None:
                    raise AssertionError(body["source"])
            if body["custody"]["package_at_commit"] != "not-established":
                raise AssertionError(body["custody"]["package_at_commit"])
            if body["review"]["binding"] != "unbound":
                raise AssertionError(body["review"]["binding"])
            if "closure" in body or "current_work" in body:
                raise AssertionError(sorted(body))

        def check_members() -> None:
            book = str(BOOK)
            proc = call_app(LIBRARIAN, observe_argv(str(REPO), COMMIT, PAGE, book), foreign, env)
            direct = run(direct_argv(str(REPO), COMMIT, PAGE, book), foreign, env)
            if proc.returncode != 1 or direct.returncode != 1:
                raise AssertionError((proc.returncode, direct.returncode, proc.stderr, direct.stderr))
            app_body = json.loads(proc.stdout.decode("utf-8"))
            direct_body = json.loads(direct.stdout.decode("utf-8"))
            if strip_stamps(app_body) != strip_stamps(direct_body):
                raise AssertionError("members facets differ")
            app_stamps = live_stamps(app_body)
            direct_stamps = live_stamps(direct_body)
            if len(app_stamps) < 2 or len(direct_stamps) < 2:
                raise AssertionError((app_stamps, direct_stamps))
            if app_stamps == direct_stamps or set(app_stamps) & set(direct_stamps):
                raise AssertionError((app_stamps, direct_stamps))
            for stamp in app_stamps + direct_stamps:
                if Z_STAMP.fullmatch(stamp) is None or stamp == COMMIT:
                    raise AssertionError(stamp)
            for body in (app_body, direct_body):
                for key in ("live_observed_at", *STAMP_KEYS):
                    if body["source"][key] is not None:
                        raise AssertionError(body["source"])
                if body["custody"]["primary"] != "0129.assembly-capture-0510":
                    raise AssertionError(body["custody"]["primary"])
                if body["custody"]["package_at_commit"] != "not-established":
                    raise AssertionError(body["custody"])
                if body["review"]["binding"] != "unbound":
                    raise AssertionError(body["review"]["binding"])
                by_member = {item["member"]: item for item in body["custody"]["observations"]}
                primary = by_member["0129.assembly-capture-0510"]
                secondary = by_member["0128.pack-assembly-0501"]
                if primary["role"] != "primary-current-candidate" or primary["inspection"]["status"] != "complete":
                    raise AssertionError(primary["role"])
                if secondary["role"] != "secondary-historical" or secondary["inspection"]["status"] != "complete":
                    raise AssertionError(secondary["role"])
                if "observation_started_at" in primary["inspection"] or "observation_finished_at" in primary["inspection"]:
                    raise AssertionError("stamp moved into the inspection")
            if proc.stderr != direct.stderr:
                raise AssertionError((proc.stderr, direct.stderr))

        def check_utf8() -> None:
            proc = call_app(LIBRARIAN, observe_argv(str(repo), fixture_commit, "pages/note.md"), foreign, env)
            direct = run(direct_argv(str(repo), fixture_commit, "pages/note.md"), foreign, env)
            same_backend(proc, direct)
            if proc.returncode not in (0, 1) or proc.stdout == b"":
                raise AssertionError((proc.returncode, proc.stderr))
            text = proc.stdout.decode("utf-8")
            if "\\u" in text or "状态" not in text or "café" not in text:
                raise AssertionError(text[:400])
            body = json.loads(text)
            if body["source"]["kind"] != "git-blob" or "状态" not in body["assignment"]["executor_raw"]:
                raise AssertionError(body["assignment"])

        def check_missing_blob() -> None:
            proc = call_app(LIBRARIAN, observe_argv(str(repo), fixture_commit, "pages/missing.md"), foreign, env)
            direct = run(direct_argv(str(repo), fixture_commit, "pages/missing.md"), foreign, env)
            same_backend(proc, direct)
            if proc.returncode != 2 or proc.stdout != b"" or b"stop:" in proc.stderr:
                raise AssertionError((proc.returncode, proc.stderr, proc.stdout))
            if b"{" in proc.stdout:
                raise AssertionError(proc.stdout)

        def check_absent_commit() -> None:
            missing = "0123456789abcdef0123456789abcdef01234567"
            proc = call_app(LIBRARIAN, observe_argv(str(repo), missing, "pages/note.md"), foreign, env)
            direct = run(direct_argv(str(repo), missing, "pages/note.md"), foreign, env)
            same_backend(proc, direct)
            if proc.returncode != 2 or proc.stdout != b"" or b"stop:" in proc.stderr:
                raise AssertionError((proc.returncode, proc.stderr, proc.stdout))

        def check_fixture_git() -> None:
            if page.read_bytes() != fixture_before:
                raise AssertionError("fixture page changed")
            again = git(real, repo, ["rev-parse", "HEAD"], env)
            require_git(again, "fixture head")
            if again.stdout.decode("utf-8").strip() != fixture_commit:
                raise AssertionError(again.stdout)
            status = git(real, repo, ["status", "--porcelain"], env)
            require_git(status, "fixture status")
            if status.stdout != b"":
                raise AssertionError(status.stdout)

        def refuse_on_sentinel(name: str, argv: list[str], message: str) -> None:
            code = copy_code(root / name)
            ran = root / (name + "-ran.txt")
            (code / "labs" / "batch-observation-pass01" / "batch_observe.py").write_bytes(sentinel_bytes(ran))
            proc = call_app(code / "app" / "librarian.py", argv, foreign, env)
            assert_stop(proc, message)
            if ran.exists() or b"pinned tool hash" in proc.stderr:
                raise AssertionError((proc.stderr, ran.exists()))

        def check_duplicate_repo() -> None:
            argv = ["batch-observe", "--repo", str(repo), "--repo", str(repo), "--commit", fixture_commit, "--path", "pages/note.md", "--json"]
            refuse_on_sentinel("dup-repo", argv, "repeated --repo")

        def check_duplicate_commit() -> None:
            argv = ["batch-observe", "--repo", str(repo), "--commit", fixture_commit, "--commit", fixture_commit, "--path", "pages/note.md", "--json"]
            refuse_on_sentinel("dup-commit", argv, "repeated --commit")

        def check_duplicate_path() -> None:
            argv = ["batch-observe", "--repo", str(repo), "--commit", fixture_commit, "--path", "pages/note.md", "--path", "pages/note.md", "--json"]
            refuse_on_sentinel("dup-path", argv, "repeated --path")

        def check_duplicate_book() -> None:
            argv = ["batch-observe", "--repo", str(repo), "--commit", fixture_commit, "--path", "pages/note.md", "--members-book", str(BOOK), "--members-book", str(BOOK), "--json"]
            refuse_on_sentinel("dup-book", argv, "repeated --members-book")

        def check_duplicate_json() -> None:
            argv = observe_argv(str(repo), fixture_commit, "pages/note.md") + ["--json"]
            refuse_on_sentinel("dup-json", argv, "repeated --json")

        def check_unknown() -> None:
            argv = observe_argv(str(repo), fixture_commit, "pages/note.md") + ["--model"]
            refuse_on_sentinel("unknown", argv, "unsupported argument")

        def check_live() -> None:
            argv = ["batch-observe", "--repo", str(repo), "--live", "--path", "pages/note.md", "--json"]
            refuse_on_sentinel("live", argv, "live mode is not exposed")

        def check_supplied() -> None:
            argv = ["batch-observe", "--supplied", str(page), "--json"]
            refuse_on_sentinel("supplied", argv, "supplied text is not exposed")

        def check_declaration_flag() -> None:
            argv = observe_argv(str(repo), fixture_commit, "pages/note.md") + ["--declaration", str(page)]
            refuse_on_sentinel("declaration-flag", argv, "declaration override is not exposed")

        def check_missing_repo() -> None:
            argv = ["batch-observe", "--commit", fixture_commit, "--path", "pages/note.md", "--json"]
            refuse_on_sentinel("missing-repo", argv, "missing --repo")

        def check_missing_commit() -> None:
            argv = ["batch-observe", "--repo", str(repo), "--path", "pages/note.md", "--json"]
            refuse_on_sentinel("missing-commit", argv, "missing --commit")

        def check_missing_path() -> None:
            argv = ["batch-observe", "--repo", str(repo), "--commit", fixture_commit, "--json"]
            refuse_on_sentinel("missing-path", argv, "missing --path")

        def check_missing_json() -> None:
            argv = ["batch-observe", "--repo", str(repo), "--commit", fixture_commit, "--path", "pages/note.md"]
            refuse_on_sentinel("missing-json", argv, "missing --json")

        def check_relative_repo() -> None:
            argv = observe_argv("fixture-repo", fixture_commit, "pages/note.md")
            refuse_on_sentinel("relative-repo", argv, "repository path must be absolute")

        def check_relative_book() -> None:
            argv = observe_argv(str(repo), fixture_commit, "pages/note.md", "00.kernel/00.00.10.work")
            refuse_on_sentinel("relative-book", argv, "members book path must be absolute")

        def check_abbrev_commit() -> None:
            argv = observe_argv(str(repo), fixture_commit[:12], "pages/note.md")
            refuse_on_sentinel("abbrev-commit", argv, "commit must be 40 lowercase hex")

        def check_upper_commit() -> None:
            argv = observe_argv(str(repo), fixture_commit.upper(), "pages/note.md")
            refuse_on_sentinel("upper-commit", argv, "commit must be 40 lowercase hex")

        def check_traversal() -> None:
            argv = observe_argv(str(repo), fixture_commit, "../outside.md")
            refuse_on_sentinel("traversal", argv, "path is not a contained relative path")

        def check_nested_traversal() -> None:
            argv = observe_argv(str(repo), fixture_commit, "pages/../../outside.md")
            refuse_on_sentinel("nested-traversal", argv, "path is not a contained relative path")

        def check_absolute_path() -> None:
            argv = observe_argv(str(repo), fixture_commit, str(page))
            refuse_on_sentinel("absolute-path", argv, "path is not a contained relative path")

        def check_normal_run() -> None:
            proc = call_app(LIBRARIAN, ["run"], foreign, env)
            assert_stop(proc, "normal run is not activated")

        def pin_stop(name: str, rel: str, message: str) -> None:
            code = copy_code(root / name)
            ran = root / (name + "-ran.txt")
            target = code / rel
            target.write_bytes(sentinel_bytes(ran))
            proc = call_app(
                code / "app" / "librarian.py",
                observe_argv(str(repo), fixture_commit, "pages/note.md"),
                foreign,
                env,
            )
            assert_stop(proc, message)
            if ran.exists():
                raise AssertionError(name + " ran before the pin check")
            if b"parser pin mismatch" in proc.stderr or b"clerk adapter pin mismatch" in proc.stderr:
                raise AssertionError(proc.stderr)

        def check_reader_pin() -> None:
            pin_stop("pin-reader", "labs/batch-observation-pass01/batch_observe.py", "pinned tool hash does not match: batch_observe")

        def check_support_pin() -> None:
            pin_stop("pin-support", "labs/prime-support-pass01/prime_support.py", "pinned tool hash does not match: prime_support")

        def check_adapter_pin() -> None:
            pin_stop("pin-adapter", "labs/prime-support-pass01/clerk_adapter.py", "pinned tool hash does not match: clerk_adapter")

        def check_inspect_pin() -> None:
            pin_stop("pin-inspect", "labs/return-capture-pass01/return_inspect.py", "pinned tool hash does not match: return_inspect")

        def check_helper_pin() -> None:
            pin_stop("pin-helper", "labs/return-capture-pass01/return_capture.py", "pinned tool hash does not match: return_capture")

        def check_missing_tool() -> None:
            code = copy_code(root / "pin-missing")
            (code / "labs" / "batch-observation-pass01" / "batch_observe.py").unlink()
            proc = call_app(
                code / "app" / "librarian.py",
                observe_argv(str(repo), fixture_commit, "pages/note.md"),
                foreign,
                env,
            )
            assert_stop(proc, "pinned tool is missing: batch_observe")

        def check_decl(name: str, raw: bytes, message: str) -> None:
            code = copy_code(root / name)
            ran = root / (name + "-ran.txt")
            (code / "labs" / "batch-observation-pass01" / "batch_observe.py").write_bytes(sentinel_bytes(ran))
            (code / "app" / "batch-observer.json").write_bytes(raw)
            proc = call_app(
                code / "app" / "librarian.py",
                observe_argv(str(repo), fixture_commit, "pages/note.md"),
                foreign,
                env,
            )
            assert_stop(proc, message)
            if ran.exists():
                raise AssertionError(name + " launched")

        def declaration() -> dict:
            return json.loads((REPO / "app" / "batch-observer.json").read_text(encoding="utf-8"))

        def dump(document: dict) -> bytes:
            return (json.dumps(document, indent=2) + "\n").encode("utf-8")

        def check_decl_bom() -> None:
            check_decl("decl-bom", b"\xef\xbb\xbf" + (REPO / "app" / "batch-observer.json").read_bytes(), "batch observer declaration is not utf-8")

        def check_decl_trailing() -> None:
            check_decl("decl-trailing", (REPO / "app" / "batch-observer.json").read_bytes() + b"\n{}\n", "batch observer declaration is not strict json")

        def check_decl_repeat() -> None:
            raw = b'{"schema":"librarian-batch-observer","schema":"librarian-batch-observer"}\n'
            check_decl("decl-repeat", raw, "batch observer declaration repeats schema")

        def check_decl_unknown() -> None:
            document = declaration()
            document["extra"] = 1
            check_decl("decl-unknown", dump(document), "batch observer declaration has an unknown field: extra")

        def check_decl_schema() -> None:
            document = declaration()
            document["schema"] = "librarian-prime-intake"
            check_decl("decl-schema", dump(document), "batch observer declaration schema is not librarian-batch-observer")

        def check_decl_version() -> None:
            document = declaration()
            document["version"] = 2
            check_decl("decl-version", dump(document), "batch observer declaration version is not 1")

        def check_decl_hash() -> None:
            document = declaration()
            document["tools"]["batch_observe"]["sha256"] = "0" * 64
            check_decl("decl-hash", dump(document), "batch observer declaration does not match the pinned tools")

        def check_decl_escape() -> None:
            document = declaration()
            document["tools"]["batch_observe"]["path"] = "../batch_observe.py"
            check_decl("decl-escape", dump(document), "tool path escapes the code root")

        def check_decl_missing() -> None:
            code = copy_code(root / "decl-missing")
            ran = root / "decl-missing-ran.txt"
            (code / "labs" / "batch-observation-pass01" / "batch_observe.py").write_bytes(sentinel_bytes(ran))
            (code / "app" / "batch-observer.json").unlink()
            proc = call_app(
                code / "app" / "librarian.py",
                observe_argv(str(repo), fixture_commit, "pages/note.md"),
                foreign,
                env,
            )
            assert_stop(proc, "batch observer declaration is missing")
            if ran.exists():
                raise AssertionError("missing declaration launched")

        def check_junction() -> None:
            code = copy_code(root / "pin-junction")
            lab = code / "labs" / "batch-observation-pass01"
            outside = root / "outside-lab"
            shutil.copytree(lab, outside)
            shutil.rmtree(lab)
            made = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(lab), str(outside)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if made.returncode != 0:
                raise AssertionError(made.stderr)
            junctions.append(lab)
            ran = root / "ran-junction.txt"
            (outside / "batch_observe.py").write_bytes(sentinel_bytes(ran))
            proc = call_app(
                code / "app" / "librarian.py",
                observe_argv(str(repo), fixture_commit, "pages/note.md"),
                foreign,
                env,
            )
            assert_stop(proc, "tool path is linked and was not followed")
            if ran.exists():
                raise AssertionError("junction was followed")

        def check_symlink() -> None:
            code = copy_code(root / "pin-symlink")
            tool = code / "labs" / "batch-observation-pass01" / "batch_observe.py"
            outside = root / "linked-reader.py"
            outside.write_bytes(tool.read_bytes())
            tool.unlink()
            try:
                os.symlink(outside, tool)
            except OSError as exc:
                if getattr(exc, "winerror", None) == 1314:
                    raise Skip("file symlink privilege WinError 1314") from exc
                raise
            proc = call_app(
                code / "app" / "librarian.py",
                observe_argv(str(repo), fixture_commit, "pages/note.md"),
                foreign,
                env,
            )
            assert_stop(proc, "tool path is linked and was not followed")

        checks = [
            ("corpus-bytes-match-direct", "pass", check_corpus_bytes),
            ("members-facets-stamps-distinct", "pass", check_members),
            ("utf8-bytes-match-direct", "pass", check_utf8),
            ("missing-blob-preserved", "pass", check_missing_blob),
            ("absent-commit-preserved", "pass", check_absent_commit),
            ("fixture-git-unchanged", "pass", check_fixture_git),
            ("duplicate-repo", "refuse", check_duplicate_repo),
            ("duplicate-commit", "refuse", check_duplicate_commit),
            ("duplicate-path", "refuse", check_duplicate_path),
            ("duplicate-members-book", "refuse", check_duplicate_book),
            ("duplicate-json", "refuse", check_duplicate_json),
            ("unknown-flag", "refuse", check_unknown),
            ("live-not-exposed", "refuse", check_live),
            ("supplied-not-exposed", "refuse", check_supplied),
            ("declaration-not-exposed", "refuse", check_declaration_flag),
            ("missing-repo", "refuse", check_missing_repo),
            ("missing-commit", "refuse", check_missing_commit),
            ("missing-path", "refuse", check_missing_path),
            ("missing-json", "refuse", check_missing_json),
            ("relative-repo", "refuse", check_relative_repo),
            ("relative-members-book", "refuse", check_relative_book),
            ("abbreviated-commit", "refuse", check_abbrev_commit),
            ("uppercase-commit", "refuse", check_upper_commit),
            ("path-traversal", "refuse", check_traversal),
            ("nested-traversal", "refuse", check_nested_traversal),
            ("absolute-path", "refuse", check_absolute_path),
            ("normal-run", "refuse", check_normal_run),
            ("wrong-reader-pin", "refuse", check_reader_pin),
            ("wrong-support-pin", "refuse", check_support_pin),
            ("wrong-adapter-pin", "refuse", check_adapter_pin),
            ("wrong-inspect-pin", "refuse", check_inspect_pin),
            ("wrong-helper-pin", "refuse", check_helper_pin),
            ("missing-reader", "refuse", check_missing_tool),
            ("declaration-bom", "refuse", check_decl_bom),
            ("declaration-trailing", "refuse", check_decl_trailing),
            ("declaration-repeat", "refuse", check_decl_repeat),
            ("declaration-unknown", "refuse", check_decl_unknown),
            ("declaration-schema", "refuse", check_decl_schema),
            ("declaration-version", "refuse", check_decl_version),
            ("declaration-hash", "refuse", check_decl_hash),
            ("declaration-escape", "refuse", check_decl_escape),
            ("declaration-missing", "refuse", check_decl_missing),
            ("junction-pin", "refuse", check_junction),
            ("file-symlink-pin", "refuse", check_symlink),
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
        if not SUITE.failed:
            after = live_bytes()
            if after != before:
                changed = [rel for rel in FROZEN if after[rel] != before[rel]]
                SUITE.fail("frozen-sources")
                print("changed " + " ".join(changed), flush=True)
            elif pycache_names() != before_cache or scratch_names() != before_scratch:
                SUITE.fail("bytecode-or-scratch")
                print(f"cache {pycache_names()} scratch {scratch_names()}", flush=True)
            else:
                head_after = git(real, REPO, ["rev-parse", "HEAD"], env)
                require_git(head_after, "workshop head after")
                if head_after.stdout.decode("utf-8").strip() != workshop_head:
                    SUITE.fail("workshop-head")
                    print(head_after.stdout.decode("utf-8"), flush=True)
                else:
                    SUITE.ok("frozen-sources")
                    for rel in (
                        "app/librarian.py",
                        "app/batch_tools.py",
                        "app/batch-observer.json",
                        "app/README.md",
                        "app/tests/test_batch_tools.py",
                    ):
                        data = (REPO / rel).read_bytes()
                        print(f"hash {rel} {sha256(data)} {len(data)}", flush=True)
    finally:
        for link in junctions:
            if os.path.lexists(link):
                os.rmdir(link)
        tmp.cleanup()
    print(
        f"summary pass {len(SUITE.passed)} expected-refusal {len(SUITE.refusals)} "
        f"skip {len(SUITE.skipped)} fail {len(SUITE.failed)}",
        flush=True,
    )
    if SUITE.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
