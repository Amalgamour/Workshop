#!/usr/bin/env python3
"""Fixture checks for the read-only prime-status entry.

Expected refusals are counted apart from passes and from unexpected failures.
A status result is not authority and is not release readiness.
"""

from __future__ import annotations

import hashlib
import json
import os
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
TOOL = REPO / "labs" / "prime-support-pass01" / "prime_support.py"
OWNER = "状态 café"
REPARSE = 0x400
NEEDED = (
    "app/librarian.py",
    "app/prime_intake.py",
    "app/prime-intake.json",
    "labs/prime-support-pass01/prime_support.py",
    "labs/prime-support-pass01/clerk_adapter.py",
    "labs/clerk-handoff-pass02/clerk.py",
)
FROZEN = NEEDED + (
    "app/prime_tools.py",
    "app/prime-tools.json",
    "app/context.py",
    "app/README.md",
    "app/tests/test_entry.py",
    "app/tests/test_prime_tools.py",
    "00.kernel/00.00.10.work/0504.app-entry/05.14.md",
    "00.kernel/00.00.10.work/0504.app-entry/06.14.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/CONTRACT.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/before/librarian.py",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/intake05.14/before/README.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.13/review.md",
    "00.kernel/00.00.10.work/0127.prime-intake-0514/reservation.json",
    "00.kernel/00.00.10.work/0127.prime-intake-0514/01.md",
    "labs/return-capture-pass01/return_capture.py",
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


def worktree_hashes(repo: Path) -> dict[str, str]:
    found = {}
    for path in repo.rglob("*"):
        if not path.is_file() or is_reparse(path):
            continue
        relative = path.relative_to(repo)
        if relative.parts and relative.parts[0] == ".git":
            continue
        found[relative.as_posix()] = sha256(path.read_bytes())
    return found


def registry_bytes(local: Path, pages: list[str]) -> bytes:
    document = {
        "schema": "prime-support-registry",
        "version": 1,
        "repositories": {
            "desk": {
                "local": str(local),
                "branch": "fixture",
                "remote_ref": "refs/remotes/origin/workshop",
                "worktree": "off",
                "history_limit": 5,
            }
        },
        "lanes": [
            {
                "lane": "status",
                "project": "fixture",
                "owner_label": OWNER,
                "repository": "desk",
                "pages": pages,
                "return_files": [],
                "review_sources": [],
            }
        ],
    }
    return (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def sentinel_bytes(path: Path) -> bytes:
    text = "from pathlib import Path\nPath(%r).write_text('ran', encoding='utf-8')\n" % str(path)
    return text.encode("utf-8")


def copy_code(dest: Path) -> Path:
    for rel in NEEDED:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / rel).read_bytes())
    return dest


def assert_stop(proc: subprocess.CompletedProcess[bytes], message: str) -> None:
    text = proc.stderr.decode("utf-8").replace("\r\n", "\n")
    if proc.returncode != 2 or f"stop: {message}" not in text or proc.stdout != b"":
        raise AssertionError((proc.returncode, text, proc.stdout))


def live_bytes() -> dict[str, bytes]:
    return {rel: (REPO / rel).read_bytes() for rel in FROZEN}


def pycache_names() -> list[str]:
    found = []
    for folder in (REPO / "app", REPO / "labs" / "prime-support-pass01", REPO / "labs" / "clerk-handoff-pass02"):
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


def main() -> None:
    print("command python -B app/tests/test_prime_intake.py", flush=True)
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
    junctions: list[Path] = []
    tmp = tempfile.TemporaryDirectory(prefix="intake0514-")
    root = Path(tmp.name)
    try:
        foreign = root / "foreign-cwd"
        foreign.mkdir()
        decoy = foreign / "decoy-ran.txt"
        for rel in (
            "labs/prime-support-pass01/prime_support.py",
            "labs/prime-support-pass01/clerk_adapter.py",
            "labs/clerk-handoff-pass02/clerk.py",
        ):
            target = foreign / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(sentinel_bytes(decoy))
        (foreign / "app").mkdir()
        (foreign / "app" / "prime-intake.json").write_bytes(b"{}\n")
        (foreign / "registry.json").write_bytes(b'{"schema":"decoy"}\n')

        repo = root / "fixture-repo"
        repo.mkdir()
        require_git(git(real, repo, ["init"], env), "init")
        require_git(git(real, repo, ["config", "user.email", "fixture@example.invalid"], env), "email")
        require_git(git(real, repo, ["config", "user.name", "Fixture"], env), "name")
        require_git(git(real, repo, ["config", "commit.gpgsign", "false"], env), "gpg")
        (repo / "README").write_bytes(b"fixture\n")
        require_git(git(real, repo, ["add", "README"], env), "add")
        require_git(git(real, repo, ["commit", "-m", "fixture"], env), "commit")
        head = git(real, repo, ["rev-parse", "HEAD"], env)
        require_git(head, "head")
        head_text = head.stdout.decode("utf-8").strip()
        porcelain = git(real, repo, ["status", "--porcelain"], env)
        require_git(porcelain, "status")
        if porcelain.stdout != b"":
            raise AssertionError(porcelain.stdout)
        tree = worktree_hashes(repo)
        print(f"fixture-head {head_text}", flush=True)

        reg_dir = root / "状态"
        reg_dir.mkdir()
        clean_path = reg_dir / "registry-clean.json"
        attention_path = reg_dir / "registry-attention.json"
        malformed_path = reg_dir / "registry-malformed.json"
        missing_path = reg_dir / "registry-missing.json"
        clean_raw = registry_bytes(repo, [])
        attention_raw = registry_bytes(repo, ["absent-pages"])
        malformed_raw = "{".encode("utf-8")
        clean_path.write_bytes(clean_raw)
        attention_path.write_bytes(attention_raw)
        malformed_path.write_bytes(malformed_raw)
        if OWNER.encode("utf-8") not in clean_raw:
            raise AssertionError("registry lost non-ascii bytes")

        store = root / "store"
        store.mkdir()
        marker = store / "marker.txt"
        marker.write_bytes(b"store-marker\n")

        def matched(registry: Path) -> subprocess.CompletedProcess[bytes]:
            direct = run(
                [PY, "-B", str(TOOL), "status", "--registry", str(registry), "--json"],
                foreign,
                env,
            )
            wrapped = run(
                [PY, "-B", str(LIBRARIAN), "prime-status", "--registry", str(registry), "--json"],
                foreign,
                env,
            )
            if wrapped.returncode != direct.returncode or wrapped.stdout != direct.stdout or wrapped.stderr != direct.stderr:
                raise AssertionError((
                    "wrapper", wrapped.returncode, wrapped.stdout, wrapped.stderr,
                    "direct", direct.returncode, direct.stdout, direct.stderr,
                ))
            if b"stop:" in wrapped.stdout or b"stop:" in wrapped.stderr:
                raise AssertionError(wrapped.stderr)
            return wrapped

        def check_clean() -> None:
            proc = matched(clean_path)
            if proc.returncode != 0 or proc.stderr != b"":
                raise AssertionError((proc.returncode, proc.stderr, proc.stdout[:200]))
            report = json.loads(proc.stdout.decode("utf-8"))
            if report["lanes"][0]["owner_label"] != OWNER or report["attention"] or report["lanes"][0]["clerk"] != []:
                raise AssertionError(report["attention"])
            if decoy.exists():
                raise AssertionError("cwd decoy ran")
            print(
                "evidence clean exit 0 attention 0 clerk [] newline "
                + ("crlf" if b"\r\n" in proc.stdout else "lf"),
                flush=True,
            )

        def check_attention() -> None:
            proc = matched(attention_path)
            if proc.returncode != 1 or proc.stderr != b"":
                raise AssertionError((proc.returncode, proc.stderr, proc.stdout[:200]))
            report = json.loads(proc.stdout.decode("utf-8"))
            if not report["attention"] or report["lanes"][0]["owner_label"] != OWNER:
                raise AssertionError(report["attention"])
            kind = report["attention"][0]["kind"]
            if kind != "missing":
                raise AssertionError(kind)
            print(
                "evidence attention exit 1 items "
                + json.dumps(report["attention"], ensure_ascii=False),
                flush=True,
            )

        def check_malformed() -> None:
            proc = matched(malformed_path)
            if proc.returncode != 2 or not proc.stdout.startswith(b"refused:") or proc.stderr != b"":
                raise AssertionError((proc.returncode, proc.stdout, proc.stderr))
            print("evidence malformed exit 2 refused", flush=True)

        def check_missing() -> None:
            proc = matched(missing_path)
            if missing_path.exists():
                raise AssertionError("missing registry was created")
            text = proc.stdout.decode("utf-8").replace("\r\n", "\n")
            if proc.returncode != 2 or text != "refused: registry is missing\n" or proc.stderr != b"":
                raise AssertionError((proc.returncode, proc.stdout, proc.stderr))
            shown = proc.stdout.decode("utf-8").encode("unicode_escape").decode("ascii")
            print("evidence missing exit 2 bytes " + shown, flush=True)

        def check_bytes() -> None:
            if clean_path.read_bytes() != clean_raw or attention_path.read_bytes() != attention_raw:
                raise AssertionError("registry bytes changed")
            if malformed_path.read_bytes() != malformed_raw:
                raise AssertionError("malformed bytes changed")
            if marker.read_bytes() != b"store-marker\n" or [path.name for path in store.iterdir()] != ["marker.txt"]:
                raise AssertionError("store changed")
            later_head = git(real, repo, ["rev-parse", "HEAD"], env)
            require_git(later_head, "head-after")
            later_status = git(real, repo, ["status", "--porcelain"], env)
            require_git(later_status, "status-after")
            if later_head.stdout.decode("utf-8").strip() != head_text or later_status.stdout != b"":
                raise AssertionError("fixture git changed")
            if worktree_hashes(repo) != tree:
                raise AssertionError("fixture worktree changed")
            seen = list(root.rglob("0001.seen.json"))
            if seen or decoy.exists():
                raise AssertionError(seen or decoy)
            print("evidence registry store git worktree unchanged; no ack", flush=True)

        def refuse_live(name: str, argv: list[str], message: str) -> None:
            proc = run(argv, foreign, env)
            assert_stop(proc, message)
            if decoy.exists():
                raise AssertionError("decoy ran")

        def check_missing_json() -> None:
            refuse_live(
                "missing-json",
                [PY, "-B", str(LIBRARIAN), "prime-status", "--registry", str(clean_path)],
                "missing --json",
            )

        def check_missing_registry() -> None:
            refuse_live(
                "missing-registry",
                [PY, "-B", str(LIBRARIAN), "prime-status", "--json"],
                "missing --registry",
            )

        def check_relative() -> None:
            refuse_live(
                "relative",
                [PY, "-B", str(LIBRARIAN), "prime-status", "--registry", "registry.json", "--json"],
                "registry path must be absolute",
            )

        def check_extra() -> None:
            refuse_live(
                "extra",
                [PY, "-B", str(LIBRARIAN), "prime-status", "--registry", str(clean_path), "--json", "extra"],
                "unsupported argument",
            )

        def check_intake() -> None:
            refuse_live(
                "intake",
                [PY, "-B", str(LIBRARIAN), "prime-status", "--registry", str(clean_path), "--json", "--intake", str(store)],
                "intake is not exposed",
            )

        def check_repeated() -> None:
            refuse_live(
                "repeated",
                [PY, "-B", str(LIBRARIAN), "prime-status", "--registry", str(clean_path), "--registry", str(clean_path), "--json"],
                "repeated --registry",
            )

        def check_unknown_flag() -> None:
            refuse_live(
                "unknown-flag",
                [PY, "-B", str(LIBRARIAN), "prime-status", "--registry", str(clean_path), "--json", "--format", "json"],
                "unsupported argument",
            )

        def check_normal_bare() -> None:
            refuse_live("bare", [PY, "-B", str(LIBRARIAN)], "normal run is not activated")

        def check_normal_run() -> None:
            refuse_live("run", [PY, "-B", str(LIBRARIAN), "run"], "normal run is not activated")

        def check_unknown_command() -> None:
            refuse_live("unknown", [PY, "-B", str(LIBRARIAN), "status"], "normal run is not activated")

        def check_support_pin() -> None:
            code = copy_code(root / "pin-support")
            ran = root / "ran-support.txt"
            (code / "labs" / "prime-support-pass01" / "prime_support.py").write_bytes(sentinel_bytes(ran))
            proc = run(
                [PY, "-B", str(code / "app" / "librarian.py"), "prime-status", "--registry", str(clean_path), "--json"],
                foreign,
                env,
            )
            assert_stop(proc, "pinned tool hash does not match: prime_support")
            if ran.exists():
                raise AssertionError("prime_support ran before the pin check")

        def check_adapter_pin() -> None:
            code = copy_code(root / "pin-adapter")
            ran = root / "ran-adapter.txt"
            (code / "labs" / "prime-support-pass01" / "clerk_adapter.py").write_bytes(sentinel_bytes(ran))
            proc = run(
                [PY, "-B", str(code / "app" / "librarian.py"), "prime-status", "--registry", str(clean_path), "--json"],
                foreign,
                env,
            )
            assert_stop(proc, "pinned tool hash does not match: clerk_adapter")
            if ran.exists():
                raise AssertionError("adapter import ran before the pin check")

        def check_clerk_pin() -> None:
            code = copy_code(root / "pin-clerk")
            clerk = code / "labs" / "clerk-handoff-pass02" / "clerk.py"
            raw = bytearray(clerk.read_bytes())
            raw[-1] ^= 1
            clerk.write_bytes(bytes(raw))
            proc = run(
                [PY, "-B", str(code / "app" / "librarian.py"), "prime-status", "--registry", str(clean_path), "--json"],
                foreign,
                env,
            )
            assert_stop(proc, "pinned tool hash does not match: clerk")

        def check_declaration_pin() -> None:
            code = copy_code(root / "pin-declaration")
            ran = root / "ran-declaration.txt"
            (code / "labs" / "prime-support-pass01" / "prime_support.py").write_bytes(sentinel_bytes(ran))
            declaration = code / "app" / "prime-intake.json"
            document = json.loads(declaration.read_text(encoding="utf-8"))
            document["tools"]["prime_support"]["sha256"] = "0" * 64
            declaration.write_bytes((json.dumps(document, indent=2) + "\n").encode("utf-8"))
            proc = run(
                [PY, "-B", str(code / "app" / "librarian.py"), "prime-status", "--registry", str(clean_path), "--json"],
                foreign,
                env,
            )
            assert_stop(proc, "prime intake declaration does not match the pinned tools")
            if ran.exists():
                raise AssertionError("declaration mismatch started the tool")

        def check_args_before_pin() -> None:
            code = copy_code(root / "pin-args")
            ran = root / "ran-args.txt"
            (code / "labs" / "prime-support-pass01" / "prime_support.py").write_bytes(sentinel_bytes(ran))
            proc = run(
                [PY, "-B", str(code / "app" / "librarian.py"), "prime-status", "--registry", "registry.json", "--json"],
                foreign,
                env,
            )
            assert_stop(proc, "registry path must be absolute")
            if ran.exists() or b"pinned tool hash" in proc.stderr:
                raise AssertionError("argument refusal reached the pin")

        def check_junction() -> None:
            code = copy_code(root / "pin-junction")
            lab = code / "labs" / "prime-support-pass01"
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
            (outside / "prime_support.py").write_bytes(sentinel_bytes(ran))
            proc = run(
                [PY, "-B", str(code / "app" / "librarian.py"), "prime-status", "--registry", str(clean_path), "--json"],
                foreign,
                env,
            )
            assert_stop(proc, "tool path is linked and was not followed")
            if ran.exists():
                raise AssertionError("junction was followed")

        def check_symlink() -> None:
            code = copy_code(root / "pin-symlink")
            tool = code / "labs" / "prime-support-pass01" / "prime_support.py"
            outside = root / "linked-support.py"
            outside.write_bytes(tool.read_bytes())
            tool.unlink()
            try:
                os.symlink(outside, tool)
            except OSError as exc:
                if getattr(exc, "winerror", None) == 1314:
                    raise Skip("file symlink privilege WinError 1314") from exc
                raise
            proc = run(
                [PY, "-B", str(code / "app" / "librarian.py"), "prime-status", "--registry", str(clean_path), "--json"],
                foreign,
                env,
            )
            assert_stop(proc, "tool path is linked and was not followed")
            if outside.read_bytes() != (REPO / "labs" / "prime-support-pass01" / "prime_support.py").read_bytes():
                raise AssertionError("symlink target changed")

        checks = [
            ("clean-matches-direct", "pass", check_clean),
            ("attention-matches-direct", "pass", check_attention),
            ("malformed-matches-direct", "pass", check_malformed),
            ("missing-matches-direct", "pass", check_missing),
            ("fixture-bytes-unchanged", "pass", check_bytes),
            ("missing-json", "refuse", check_missing_json),
            ("missing-registry", "refuse", check_missing_registry),
            ("relative-registry", "refuse", check_relative),
            ("extra-argument", "refuse", check_extra),
            ("intake-not-exposed", "refuse", check_intake),
            ("repeated-registry", "refuse", check_repeated),
            ("unknown-flag", "refuse", check_unknown_flag),
            ("normal-bare", "refuse", check_normal_bare),
            ("normal-run", "refuse", check_normal_run),
            ("unknown-command", "refuse", check_unknown_command),
            ("wrong-prime-support-pin", "refuse", check_support_pin),
            ("wrong-adapter-pin", "refuse", check_adapter_pin),
            ("wrong-clerk-pin", "refuse", check_clerk_pin),
            ("declaration-pin", "refuse", check_declaration_pin),
            ("args-before-pin", "refuse", check_args_before_pin),
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
                SUITE.ok("frozen-sources")
                for rel in (
                    "app/librarian.py",
                    "app/prime_intake.py",
                    "app/prime-intake.json",
                    "app/README.md",
                    "app/tests/test_prime_intake.py",
                    "labs/prime-support-pass01/prime_support.py",
                    "labs/prime-support-pass01/clerk_adapter.py",
                    "labs/clerk-handoff-pass02/clerk.py",
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
