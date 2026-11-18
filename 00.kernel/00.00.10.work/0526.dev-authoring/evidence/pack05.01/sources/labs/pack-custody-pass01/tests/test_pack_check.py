"""Disposable-directory tests for pack_check.py. No shared fixture is modified."""
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
CHECKER = LAB / "pack_check.py"
PY = Path(os.environ.get(
    "PACK_CHECK_PYTHON",
    r"C:\Users\misg\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe",
))
if not PY.is_file():
    PY = Path(shutil.which("python") or "python")
REAL_GIT = shutil.which("git")
SCHEMA = "prime-pack-sources/1"
NOT_CHECKED = {
    "meaning",
    "instruction-sufficiency",
    "approval-release",
    "dependencies",
    "execution-safety",
    "live-source",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run_check(args, env=None):
    merged = os.environ.copy()
    if env:
        merged.update(env)
    result = subprocess.run(
        [str(PY), "-B", str(CHECKER), *args],
        capture_output=True,
        env=merged,
    )
    return result.returncode, result.stdout, result.stderr


def load_json(stdout):
    return json.loads(stdout.decode("utf-8"))


def tsv(rows):
    lines = ["path\tsha256\tbytes"]
    for path, data in rows:
        lines.append(f"{path}\t{digest(data)}\t{len(data)}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def source(path, data, snapshot=None):
    return {
        "path": path,
        "sha256": digest(data),
        "bytes": len(data),
        "snapshot": snapshot or path,
    }


def manifest_json(sources, **extra):
    body = {"schema": SCHEMA, "sources": sources}
    body.update(extra)
    return (json.dumps(body, indent=2) + "\n").encode("utf-8")


def assert_report(test, report, result):
    test.assertEqual(report["schema"], "pack-custody-report/1")
    test.assertEqual(report["result"], result)
    test.assertEqual({item["item"] for item in report["not_checked"]}, NOT_CHECKED)
    test.assertNotIn(b"Traceback", json.dumps(report).encode("utf-8"))


class FilesystemTests(unittest.TestCase):
    def test_tsv_and_json_match(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            inputs = root / "inputs"
            inputs.mkdir()
            payload = b"alpha\n"
            (inputs / "a.txt").write_bytes(payload)
            manifest = root / "source-manifest.tsv"
            manifest.write_bytes(tsv([("a.txt", payload)]))
            code, out, err = run_check([
                "--format", "tsv", "--manifest", str(manifest), "--root", str(inputs), "--json",
            ])
            self.assertEqual(err, b"")
            self.assertEqual(code, 0)
            report = load_json(out)
            assert_report(self, report, "pass")
            self.assertEqual(report["mode"], "filesystem")
            self.assertEqual(report["rows_checked"], 1)
            self.assertEqual(report["manifest_sha256"], digest(manifest.read_bytes()))
            self.assertEqual(report["entries"][0]["result"], "match")
            self.assertIsNone(report["commit"])

            pack = root / "json-pack"
            pack.mkdir()
            (pack / "a.txt").write_bytes(payload)
            body = manifest_json(
                [source("logical/a.txt", payload, "a.txt")],
                repository="example/labels-only",
                commit="not-a-fetch",
            )
            (pack / "source-manifest.json").write_bytes(body)
            code, out, err = run_check([
                "--format", SCHEMA, "--manifest", str(pack / "source-manifest.json"), "--json",
            ])
            self.assertEqual(code, 0, err)
            report = load_json(out)
            assert_report(self, report, "pass")
            self.assertEqual(report["provenance"]["repository"], "example/labels-only")
            self.assertEqual(report["provenance"]["commit"], "not-a-fetch")
            self.assertIsNone(report["commit"])

    def test_hash_length_and_missing(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            data = b"abc"
            (root / "a.txt").write_bytes(data)
            bad = source("a.txt", data)
            bad["sha256"] = "0" * 64
            (root / "m.json").write_bytes(manifest_json([bad]))
            code, out, err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(err, b"")
            self.assertEqual(code, 1)
            report = load_json(out)
            assert_report(self, report, "findings")
            self.assertEqual(report["entries"][0]["result"], "mismatch")
            self.assertEqual(report["entries"][0]["bytes"], 3)

            short = source("a.txt", data)
            short["bytes"] = 2
            (root / "m.json").write_bytes(manifest_json([short]))
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 1)
            self.assertEqual(load_json(out)["entries"][0]["result"], "mismatch")

            missing = source("gone.txt", b"nope")
            (root / "m.json").write_bytes(manifest_json([missing]))
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 1)
            self.assertEqual(load_json(out)["entries"][0]["result"], "missing")

    def test_invalid_manifests_do_not_pass(self):
        cases = {
            "empty": b"",
            "header-only": b"path\tsha256\tbytes\n",
            "truncated": b'{"schema": "prime-pack-sources/1"',
            "malformed": b"{",
            "unknown-schema": manifest_json([source("a.txt", b"a")]).replace(
                b"prime-pack-sources/1", b"other-schema/9"
            ),
            "trailing": manifest_json([source("a.txt", b"a")]) + b"\n[]\n",
            "bom": b"\xef\xbb\xbf" + manifest_json([source("a.txt", b"a")]),
            "bool-length": b'{"schema":"prime-pack-sources/1","sources":[{"path":"a.txt","sha256":"'
            + (b"a" * 64)
            + b'","bytes":true,"snapshot":"a.txt"}]}',
            "upper-sha": manifest_json([source("a.txt", b"a")]).replace(b"sha256", b"sha256", 1),
        }
        upper = source("a.txt", b"a")
        upper["sha256"] = upper["sha256"].upper()
        cases["upper-sha"] = manifest_json([upper])
        duplicate_key = (
            b'{"schema":"prime-pack-sources/1","schema":"prime-pack-sources/1",'
            b'"sources":[{"path":"a.txt","sha256":"' + b"ab" * 32
            + b'","bytes":1,"snapshot":"a.txt"}]}'
        )
        cases["duplicate-key"] = duplicate_key
        extra = manifest_json([source("a.txt", b"a")])
        extra = extra.replace(b"{\n  \"schema\"", b'{\n  "extra": true,\n  "schema"')
        cases["extra-field"] = extra
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            (root / "a.txt").write_bytes(b"a")
            for name, body in cases.items():
                path = root / f"{name}.bin"
                path.write_bytes(body)
                fmt = "tsv" if name in ("empty", "header-only") else SCHEMA
                args = ["--format", fmt, "--manifest", str(path), "--json"]
                if fmt == "tsv":
                    args.extend(["--root", str(root)])
                code, out, err = run_check(args)
                self.assertEqual(code, 2, name)
                self.assertNotIn(b"Traceback", err)
                self.assertNotIn(b"Traceback", out)
                report = load_json(out)
                assert_report(self, report, "invalid")
                self.assertEqual(report["rows_checked"], 0)
                self.assertEqual(report["entries"], [])

    def test_duplicate_and_alias_and_partial_row(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            data = b"z"
            row = source("dir/a.txt", data)
            (root / "m.json").write_bytes(manifest_json([row, dict(row)]))
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 2)
            self.assertIn("duplicate path", load_json(out)["findings"][0]["detail"])

            other = source("Dir/a.txt", data)
            (root / "m.json").write_bytes(manifest_json([row, other]))
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 2)
            self.assertIn("ambiguous path alias", load_json(out)["findings"][0]["detail"])

            good = tsv([("a.txt", data)])
            partial = good + b"not-a-row\n"
            (root / "m.tsv").write_bytes(partial)
            code, out, _err = run_check([
                "--format", "tsv", "--manifest", str(root / "m.tsv"), "--root", str(root), "--json",
            ])
            self.assertEqual(code, 2)
            self.assertEqual(load_json(out)["entries"], [])
            self.assertFalse((root / "a.txt").exists())

    def test_crlf_space_unicode_and_rejected_paths(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            lf = b"line\n"
            crlf = b"line\r\n"
            (root / "a.txt").write_bytes(crlf)
            row = source("a.txt", lf)
            (root / "m.json").write_bytes(manifest_json([row]))
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 1)
            self.assertEqual(load_json(out)["entries"][0]["result"], "mismatch")
            self.assertEqual(load_json(out)["entries"][0]["bytes"], len(crlf))

            row = source("a.txt", crlf)
            (root / "m.json").write_bytes(manifest_json([row]))
            code, _out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 0)

            spaced = root / "my file.txt"
            spaced.write_bytes(b"space")
            (root / "m.json").write_bytes(manifest_json([source("my file.txt", b"space")]))
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 0)
            self.assertEqual(load_json(out)["entries"][0]["result"], "match")

            named = "caf\u00e9.txt"
            (root / named).write_bytes(b"tea")
            (root / "m.json").write_bytes(manifest_json([source(named, b"tea")]))
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 0, out)
            self.assertEqual(load_json(out)["entries"][0]["path"], named)

            for bad in ("../out.txt", "/etc/passwd", "C:/windows/note", "//server/share/a", "a\\b", "a/./b", "a//b"):
                (root / "m.json").write_bytes(manifest_json([source(bad, b"x")]))
                code, out, err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
                self.assertEqual(code, 2, bad)
                self.assertNotIn(b"Traceback", err)
                self.assertEqual(load_json(out)["entries"], [])

    def test_junction_is_not_followed(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            outside = root / "outside"
            pack = root / "pack"
            outside.mkdir()
            pack.mkdir()
            secret = b"secret-bytes\n"
            (outside / "secret.txt").write_bytes(secret)
            link = pack / "jump"
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(outside)],
                check=True, stdout=subprocess.DEVNULL,
            )
            try:
                (pack / "m.json").write_bytes(manifest_json([source("jump/secret.txt", secret)]))
                code, out, err = run_check(["--format", SCHEMA, "--manifest", str(pack / "m.json"), "--json"])
                self.assertEqual(err, b"")
                self.assertEqual(code, 1)
                report = load_json(out)
                self.assertEqual(report["entries"][0]["result"], "linked")
                self.assertIsNone(report["entries"][0]["sha256"])
            finally:
                os.rmdir(link)

    def test_file_symlink_when_privileged(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            target = root / "target.txt"
            target.write_bytes(b"target\n")
            link = root / "linked.txt"
            try:
                os.symlink(target, link)
            except OSError as exc:
                if getattr(exc, "winerror", None) == 1314:
                    self.skipTest("file symlink privilege WinError 1314")
                raise
            (root / "m.json").write_bytes(manifest_json([source("linked.txt", b"target\n")]))
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 1)
            self.assertEqual(load_json(out)["entries"][0]["result"], "linked")

    def test_unreadable_when_feasible(self):
        user = os.environ.get("USERNAME")
        if not user:
            self.skipTest("USERNAME is unset; read-deny not attempted")
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            path = root / "secret.txt"
            path.write_bytes(b"hidden\n")
            denied = subprocess.run(
                ["icacls", str(path), "/deny", f"{user}:(R)"],
                capture_output=True,
            )
            if denied.returncode != 0:
                self.skipTest("icacls could not deny read")
            try:
                (root / "m.json").write_bytes(manifest_json([source("secret.txt", b"hidden\n")]))
                code, out, err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
                self.assertNotIn(b"Traceback", err)
                report = load_json(out)
                if code == 0 and report["entries"][0]["result"] == "match":
                    self.skipTest("read deny did not stick; privilege skip")
                self.assertEqual(code, 1)
                self.assertEqual(report["entries"][0]["result"], "unreadable")
            finally:
                subprocess.run(["icacls", str(path), "/remove:d", user], capture_output=True)

    def test_directory_snapshot_and_decoy_manifest_are_not_loaded(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            (root / "adir").mkdir()
            (root / "m.json").write_bytes(manifest_json([source("adir", b"x")]))
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 1)
            self.assertEqual(load_json(out)["entries"][0]["result"], "not-a-file")

            decoy = {
                "schema": SCHEMA,
                "sources": [source("missing-nested.txt", b"nope")],
            }
            decoy_bytes = (json.dumps(decoy) + "\n").encode("utf-8")
            (root / "decoy.json").write_bytes(decoy_bytes)
            (root / "m.json").write_bytes(manifest_json([
                source("decoy.json", decoy_bytes, "decoy.json"),
            ]))
            marker = root / "RAN"
            (root / "run-me.bat").write_bytes(b"echo ran> RAN\r\n")
            code, out, _err = run_check(["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"])
            self.assertEqual(code, 0, out)
            report = load_json(out)
            self.assertEqual([item["path"] for item in report["entries"]], ["decoy.json"])
            self.assertFalse((root / "missing-nested.txt").exists())
            self.assertFalse(marker.exists())

    def test_filesystem_mode_does_not_invoke_git(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            payload = b"solo\n"
            (root / "a.txt").write_bytes(payload)
            (root / "m.json").write_bytes(manifest_json([source("a.txt", payload)]))
            log = root / "git.log"
            wrap = root / "wrap"
            wrap.mkdir()
            write_wrapper(wrap)
            env = {
                "PATH": str(wrap) + os.pathsep + os.environ.get("PATH", ""),
                "PACK_CHECK_GIT_LOG": str(log),
                "PACK_CHECK_REAL_GIT": REAL_GIT or "",
            }
            code, out, err = run_check(
                ["--format", SCHEMA, "--manifest", str(root / "m.json"), "--json"],
                env=env,
            )
            self.assertEqual(code, 0, err + out)
            self.assertFalse(log.exists())
            self.assertNotIn(b"Traceback", err)


def write_wrapper(directory):
    script = r"""import os, sys, subprocess
log = os.environ.get("PACK_CHECK_GIT_LOG", "")
args = sys.argv[1:]
if log:
    with open(log, "a", encoding="utf-8") as handle:
        handle.write(" ".join(args) + "\n")
        handle.write("LOCKS=" + os.environ.get("GIT_OPTIONAL_LOCKS", "") + "\n")
        handle.write("PROMPT=" + os.environ.get("GIT_TERMINAL_PROMPT", "") + "\n")
index = 0
while index < len(args):
    item = args[index]
    if item == "-C":
        index += 2
        continue
    if item.startswith("-"):
        index += 1
        continue
    break
command = args[index] if index < len(args) else ""
if command not in {"rev-parse", "cat-file"}:
    raise SystemExit(97)
real = os.environ["PACK_CHECK_REAL_GIT"]
raise SystemExit(subprocess.call([real, *args]))
"""
    (directory / "gitwrap.py").write_bytes(script.encode("utf-8"))
    cmd = f'@echo off\r\n"{PY}" -B "%~dp0gitwrap.py" %*\r\n'
    (directory / "git.cmd").write_bytes(cmd.encode("ascii"))


def git(repo, *args, input_bytes=None, check=True):
    result = subprocess.run(
        [REAL_GIT, "-C", str(repo), *args],
        input=input_bytes,
        capture_output=True,
        check=False,
    )
    if check and result.returncode:
        raise AssertionError(result.stderr.decode("utf-8", "replace"))
    return result


def tree_hashes(root):
    found = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        for name in filenames:
            path = Path(dirpath) / name
            if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
                found[str(path)] = "link"
                continue
            found[str(path)] = digest(path.read_bytes())
    git_dir = Path(root) / ".git"
    for dirpath, _dirnames, filenames in os.walk(git_dir):
        for name in filenames:
            path = Path(dirpath) / name
            try:
                found[str(path)] = digest(path.read_bytes())
            except OSError:
                found[str(path)] = "unreadable"
    return found


class GitTests(unittest.TestCase):
    def setUp(self):
        if not REAL_GIT:
            self.skipTest("git is not on PATH")

    def make_repo(self, parent):
        repo = parent / "repo"
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "config", "user.email", "pack@example.invalid")
        git(repo, "config", "user.name", "pack-check")
        return repo

    def commit_all(self, repo, message):
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", message)
        return git(repo, "rev-parse", "HEAD").stdout.decode().strip()

    def test_pinned_commit_ignores_worktree_index_and_head(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            repo = self.make_repo(root)
            payload = b"committed\n"
            (repo / "inputs").mkdir()
            (repo / "inputs" / "a.txt").write_bytes(payload)
            (repo / "source-manifest.tsv").write_bytes(tsv([("a.txt", payload)]))
            good = self.commit_all(repo, "good pack")
            (repo / "inputs" / "a.txt").write_bytes(b"later\n")
            moved = self.commit_all(repo, "move head")
            (repo / "inputs" / "a.txt").write_bytes(b"worktree\n")
            git(repo, "add", "--", "inputs/a.txt")
            (repo / "inputs" / "a.txt").write_bytes(b"unstaged\n")
            self.assertNotEqual(good, moved)
            before = tree_hashes(repo)
            head_before = (repo / ".git" / "HEAD").read_bytes()
            code, out, err = run_check([
                "--format", "tsv", "--git-repo", str(repo), "--rev", good,
                "--manifest", "source-manifest.tsv", "--root", "inputs", "--json",
            ])
            self.assertEqual(err, b"", err)
            self.assertEqual(code, 0, out)
            report = load_json(out)
            assert_report(self, report, "pass")
            self.assertEqual(report["commit"], good)
            self.assertEqual(report["mode"], "git")
            self.assertEqual((repo / ".git" / "HEAD").read_bytes(), head_before)
            self.assertEqual(tree_hashes(repo), before)
            self.assertEqual((repo / "inputs" / "a.txt").read_bytes(), b"unstaged\n")

            (repo / "inputs" / "a.txt").write_bytes(b"bad-commit\n")
            git(repo, "add", "--", "inputs/a.txt")
            # The index currently holds "worktree" from the earlier add, then we
            # rewrote the file and added the bad bytes. Commit that bad snapshot.
            bad = self.commit_all(repo, "bad pack")
            before_bad = tree_hashes(repo)
            code, out, err = run_check([
                "--format", "tsv", "--git-repo", str(repo), "--rev", bad,
                "--manifest", "source-manifest.tsv", "--root", "inputs", "--json",
            ])
            self.assertEqual(err, b"")
            self.assertEqual(code, 1, out)
            report = load_json(out)
            self.assertEqual(report["entries"][0]["result"], "mismatch")
            self.assertEqual(report["commit"], bad)
            self.assertEqual(tree_hashes(repo), before_bad)

            (repo / "source-manifest.tsv").write_bytes(b"not a manifest\n")
            git(repo, "add", "--", "source-manifest.tsv")
            refused = self.commit_all(repo, "refused")
            before_refused = tree_hashes(repo)
            code, out, err = run_check([
                "--format", "tsv", "--git-repo", str(repo), "--rev", refused,
                "--manifest", "source-manifest.tsv", "--root", "inputs", "--json",
            ])
            self.assertEqual(code, 2)
            self.assertNotIn(b"Traceback", out)
            self.assertNotIn(b"Traceback", err)
            report = load_json(out)
            assert_report(self, report, "invalid")
            self.assertEqual(tree_hashes(repo), before_refused)

    def test_long_path_and_no_network_commands(self):
        with tempfile.TemporaryDirectory(prefix="wf0507-") as tmp:
            root = Path(tmp)
            repo = self.make_repo(root)
            payload = b"long-ok\n"
            blob = git(repo, "hash-object", "-w", "--stdin", input_bytes=payload).stdout.decode().strip()
            long_rel = "directory/" * 28 + "file.txt"
            self.assertGreater(len(long_rel), 260)
            manifest = manifest_json([source("logical/file.txt", payload, long_rel)])
            man_blob = git(repo, "hash-object", "-w", "--stdin", input_bytes=manifest).stdout.decode().strip()
            # mktree accepts one path segment per tree. Nest the blob, then
            # attach that tree and the manifest at the root. Nothing is checked out.
            parts = long_rel.split("/")
            oid = blob
            mode, kind = "100644", "blob"
            for name in reversed(parts[1:]):
                listing = f"{mode} {kind} {oid}\t{name}\n".encode("utf-8")
                oid = git(repo, "mktree", input_bytes=listing).stdout.decode().strip()
                mode, kind = "040000", "tree"
            listing = (
                f"040000 tree {oid}\t{parts[0]}\n"
                f"100644 blob {man_blob}\tsource-manifest.json\n"
            ).encode("utf-8")
            tree = git(repo, "mktree", input_bytes=listing).stdout.decode().strip()
            commit = git(
                repo, "commit-tree", tree, "-m", "long",
            ).stdout.decode().strip()
            # Point HEAD at an unrelated empty commit so a worktree read would miss the blob.
            (repo / "README").write_bytes(b"other\n")
            other = self.commit_all(repo, "other head")
            self.assertNotEqual(commit, other)
            log = root / "git.log"
            wrap = root / "wrap"
            wrap.mkdir()
            write_wrapper(wrap)
            before = tree_hashes(repo)
            env = {
                "PATH": str(wrap) + os.pathsep + os.environ.get("PATH", ""),
                "PACK_CHECK_GIT_LOG": str(log),
                "PACK_CHECK_REAL_GIT": REAL_GIT,
            }
            code, out, err = run_check([
                "--format", SCHEMA, "--git-repo", str(repo), "--rev", commit,
                "--manifest", "source-manifest.json", "--json",
            ], env=env)
            self.assertEqual(err, b"", err)
            self.assertEqual(code, 0, out)
            report = load_json(out)
            assert_report(self, report, "pass")
            self.assertEqual(report["commit"], commit)
            self.assertEqual(report["entries"][0]["location"], long_rel)
            self.assertEqual(tree_hashes(repo), before)
            text = log.read_text(encoding="utf-8")
            self.assertIn("cat-file --batch", text)
            self.assertIn("LOCKS=0", text)
            self.assertIn("PROMPT=0", text)
            for banned in ("fetch", "pull", "push", "ls-remote", "clone", "checkout", "show ", " status"):
                self.assertNotIn(banned, text)
            self.assertFalse((repo / "file.txt").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
