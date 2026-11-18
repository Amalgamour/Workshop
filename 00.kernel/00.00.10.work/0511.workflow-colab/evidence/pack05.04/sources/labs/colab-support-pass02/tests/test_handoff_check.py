"""Tests for the repaired standalone handoff checker (0510/05.04).

Real packages are prepared by the FROZEN v2 producer on disposable repositories.
Every bad input must refuse or mismatch with no trusted identity and no copy.
For handoff tampering the full producer verify is run too, for comparison.

  python -B -X dev tests/test_handoff_check.py -v
"""

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LAB = HERE.parent
REPO_ROOT = LAB.parent.parent
sys.path.insert(0, str(LAB))
import colab_support as producer  # noqa: E402  (frozen v2 producer, used only to prepare and compare)
import handoff_check as hc  # noqa: E402

FROZEN = {
    "labs/colab-support-pass02/colab_support.py": "2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b",
    "labs/colab-support-pass01/colab_support.py": "33bbe41c52485fc7b2b611d830bae8a15129721ad807a931e8193f17944c467c",
    "labs/pack-assembly-pass01/pack_assembly.py": "75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c",
    "labs/pack-custody-pass01/pack_check.py": "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d",
    "labs/return-capture-pass01/return_capture.py": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
    "labs/return-capture-pass01/return_inspect.py": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
}
BOOK = "00.00.10.work"
BASE = "00.kernel/00.00.10.work"
PAGE = b"# 01\n\n## Pass identity\nbody\n"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def frozen_now():
    return {rel: sha((REPO_ROOT / rel).read_bytes()) for rel in FROZEN}


def setUpModule():
    assert frozen_now() == FROZEN, "frozen dependency differs before the suite"


def tearDownModule():
    assert frozen_now() == FROZEN, "frozen dependency changed during the suite"


def git(repo, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="f", GIT_AUTHOR_EMAIL="f@example.invalid",
               GIT_COMMITTER_NAME="f", GIT_COMMITTER_EMAIL="f@example.invalid")
    out = subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, env=env)
    if out.returncode:
        raise RuntimeError(out.stderr.decode("utf-8", "replace"))
    return out.stdout.decode("utf-8").strip()


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def junction(link, target):
    if os.name == "nt":
        return subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True).returncode == 0
    os.symlink(target, link)
    return True


class Packages:
    """Two frozen-producer packages: unscored and blind-scored."""

    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="hc-test-")
        self.root = Path(self.tmp.name)
        repo = self.root / "repo"
        repo.mkdir()
        git(repo, "init", "-q")
        write(repo / BASE / "0411.colab/evidence/layout/CONTRACT.md", PAGE)
        write(repo / BASE / "0411.colab/07.md", "# 07\ndata\n")
        write(repo / BASE / "0411.colab/evidence/key.md", "# key\nexpected answers\n")
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "A")
        commit = git(repo, "rev-parse", "HEAD")
        self.config = self.root / "config.json"
        write(self.config, json.dumps({
            "schema": "colab-config/2", "repositories": {"fixture": str(repo)}, "python": sys.executable,
            "assembler": str(REPO_ROOT / "labs/pack-assembly-pass01/pack_assembly.py"),
            "checker": str(REPO_ROOT / "labs/pack-custody-pass01/pack_check.py"),
            "helper": str(REPO_ROOT / "labs/return-capture-pass01/return_capture.py"),
            "inspector": str(REPO_ROOT / "labs/return-capture-pass01/return_inspect.py"),
            "producer_v1": str(REPO_ROOT / "labs/colab-support-pass01/colab_support.py")}))
        base = {
            "schema": "colab-request/2",
            "binding": {"schema": "colab-binding/1",
                        "investigation": {"book": BOOK, "page": "0701.layout-probe", "pass": "05.01"},
                        "targets": [{"id": "T01", "book": BOOK, "page": "0411.colab", "file": "evidence/layout/CONTRACT.md",
                                     "section": None,
                                     "source": {"repository": "fixture", "commit": commit,
                                                "path": f"{BASE}/0411.colab/evidence/layout/CONTRACT.md", "sha256": sha(PAGE)}}]},
            "title": "Checker fixture", "date": "2026-10-29", "author": "fixture Prime", "recipient": "fixture Colab",
            "reviewer": "fixture reviewer", "mode": "hostile-read", "scoring": {"state": "unscored"},
            "context": "c", "question": "q", "why": "w", "built_state": "b", "known_gaps": [], "method": "m",
            "cases": [{"id": "C01", "text": "x"}],
            "environment": {"kind": "zip-only", "read": "r", "write": "w", "execute": "e", "network": "n"},
            "permissions": ["p"], "stop": ["s"], "prior_involvement": "none",
            "required_sources": [{"path": f"{BASE}/0411.colab/07.md", "role": "data"}],
            "withheld": [], "unavailable": [], "director_replies": [],
            "return_route": {"destination": "to Prime", "submission_hint": "one file"}, "preparation_notes": ["n"],
        }
        self.plain, self.plain_digest = self.prepare(base, "plain")
        blind = json.loads(json.dumps(base))
        blind["mode"] = "controlled-experiment"
        blind["scoring"] = {"state": "scored", "blind": True, "evaluator_sources": [f"{BASE}/0411.colab/evidence/key.md"]}
        self.blind, self.blind_digest = self.prepare(blind, "blind")
        self.n = 0

    def prepare(self, doc, name):
        req = self.root / f"{name}.json"
        write(req, json.dumps(doc))
        digest = producer.preview(str(req), str(self.config))[0]["digest"]
        out = self.root / name
        body, code = producer.prepare(str(req), str(self.config), str(out), digest)
        assert code == 0, body
        return out, digest

    def clone(self, which="plain"):
        self.n += 1
        dest = self.root / f"case-{self.n}"
        shutil.copytree(self.plain if which == "plain" else self.blind, dest)
        return dest


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pk = Packages()

    @classmethod
    def tearDownClass(cls):
        cls.pk.tmp.cleanup()

    def bad(self, out, digest=None, exit_codes=(1, 2)):
        body, code = hc.check(str(out), digest or self.pk.plain_digest)
        self.assertIn(code, exit_codes, body)
        self.assertNotIn("trusted", body)
        self.assertNotEqual(body["result"], "valid")
        dest = self.pk.root / f"copy-bad-{self.pk.n}"
        cbody, ccode = hc.copy(str(out), digest or self.pk.plain_digest, str(dest))
        self.assertNotEqual(ccode, 0)
        self.assertFalse(dest.exists(), "a bad package must never be copied")
        return body

    def producer_verify(self, out):
        return producer.verify(str(out), str(self.pk.config))[1]

    def edit_handoff(self, out, fn):
        path = Path(out) / "handoff.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        fn(doc)
        path.write_bytes(canonical(doc))


class Valid(Base):
    def test_valid_actual_envelope_checks(self):
        body, code = hc.check(str(self.pk.plain), self.pk.plain_digest)
        self.assertEqual((code, body["result"]), (0, "valid"), body)
        self.assertEqual(body["trusted"]["investigation"]["page"], "0701.layout-probe")
        self.assertEqual(body["trusted"]["exchange"]["primary_instruction"], "05.01.pack.md")
        self.assertIn("not_verified", body)
        self.assertIn("verify", body["unbound_informational"])

    def test_valid_blind_package_checks(self):
        body, code = hc.check(str(self.pk.blind), self.pk.blind_digest)
        self.assertEqual(code, 0, body)
        self.assertEqual(len(body["trusted"]["evaluator"]), 2)

    def test_copy_exact_and_read_only_replay(self):
        out = self.pk.clone()
        before = {p: p.read_bytes() for p in out.rglob("*") if p.is_file()}
        dest = self.pk.root / "copy-valid"
        body, code = hc.copy(str(out), self.pk.plain_digest, str(dest))
        self.assertEqual((code, body["result"]), (0, "copied"), body)
        for p in (out / "package").rglob("*"):
            if p.is_file():
                self.assertEqual((dest / p.relative_to(out / "package")).read_bytes(), p.read_bytes())
        self.assertEqual(before, {p: p.read_bytes() for p in out.rglob("*") if p.is_file()})  # source unchanged
        snapshot = {p: p.stat().st_mtime_ns for p in dest.rglob("*")}
        again, code = hc.copy(str(out), self.pk.plain_digest, str(dest))
        self.assertEqual((code, again["problems"][0]["code"]), (2, "already-copied"))
        self.assertEqual(snapshot, {p: p.stat().st_mtime_ns for p in dest.rglob("*")})

    def test_copy_occupied_and_overlap_refused(self):
        dest = self.pk.root / "occupied"
        write(dest / "keep.txt", "keep")
        body, code = hc.copy(str(self.pk.plain), self.pk.plain_digest, str(dest))
        self.assertEqual((code, body["problems"][0]["code"]), (2, "occupied"))
        self.assertEqual((dest / "keep.txt").read_text(), "keep")
        inside = self.pk.plain / "nested-copy"
        body, code = hc.copy(str(self.pk.plain), self.pk.plain_digest, str(inside))
        self.assertEqual((code, body["problems"][0]["code"]), (2, "destination"))
        self.assertFalse(inside.exists())

    def test_copy_partial_is_retained(self):
        dest = self.pk.root / "copy-partial"
        real_write = os.write
        calls = {"n": 0}

        def failing(fd, data):
            calls["n"] += 1
            if calls["n"] > 2:
                raise OSError(28, "injected disk full")
            return real_write(fd, data)

        with mock.patch.object(hc.os, "write", side_effect=failing):
            body, code = hc.copy(str(self.pk.plain), self.pk.plain_digest, str(dest))
        self.assertEqual((code, body["result"]), (1, "partial"), body)
        self.assertEqual(len(body["written"]), 2)
        self.assertTrue(dest.exists())  # retained, never deleted
        again, code = hc.copy(str(self.pk.plain), self.pk.plain_digest, str(dest))
        self.assertEqual((code, again["problems"][0]["code"]), (2, "occupied"))  # no automatic resume


class HandoffClaims(Base):
    """One claim field at a time. The producer verify must also reject each."""

    def claim(self, fn, exit_codes=(1,)):
        out = self.pk.clone()
        self.edit_handoff(out, fn)
        body = self.bad(out, exit_codes=exit_codes)
        self.assertNotEqual(self.producer_verify(out), 0)
        return body

    def test_hc01_investigation_page(self):
        body = self.claim(lambda h: h["investigation"].__setitem__("page", "0799.wrong-investigation"))
        self.assertEqual(body["problems"][0]["detail"], "handoff.investigation differs from the value derived from bound bytes")
        self.assertNotIn("0799.wrong-investigation", json.dumps(body))

    def test_investigation_book_and_pass(self):
        self.claim(lambda h: h["investigation"].__setitem__("book", "other.book"))
        self.claim(lambda h: h["investigation"].__setitem__("pass", "05.02"))

    def test_binding_and_hash(self):
        self.claim(lambda h: h["binding"]["targets"][0].__setitem__("file", "elsewhere.md"))
        self.claim(lambda h: h.__setitem__("binding_sha256", "0" * 64))

    def test_exchange_names_and_not_created(self):
        self.claim(lambda h: h["exchange"].__setitem__("pack", "06.01.notes.md"))
        self.claim(lambda h: h["exchange"].__setitem__("primary_instruction", "support/assembler/05.01.md"))
        self.claim(lambda h: h.__setitem__("not_created", []))

    def test_envelope_roles_and_hashes(self):
        def swap_role(h):
            for e in h["envelope"]:
                if e["role"] == "pack-primary-instruction":
                    e["role"] = "notes"
        self.claim(swap_role)
        self.claim(lambda h: h["envelope"][0].__setitem__("sha256", "1" * 64))
        self.claim(lambda h: h["envelope"].pop())

    def test_source_map(self):
        self.claim(lambda h: h["source_map"][0].__setitem__("role", "required"))
        self.claim(lambda h: h["source_map"][0].__setitem__("targets", []))
        self.claim(lambda h: h["source_map"][1].__setitem__("snapshot", "package/snapshots/0001.blob"))

    def test_support_zip_layout_domain_digest(self):
        self.claim(lambda h: h["support_projection"][0].__setitem__("assembler_name", "05.01.pack.md"))
        self.claim(lambda h: h["zip"]["members"].pop())
        self.claim(lambda h: h.__setitem__("layout", "colab-exchange-layout/1"))
        self.claim(lambda h: h.__setitem__("digest_domain", "colab-package-digest/1"))
        self.claim(lambda h: h.__setitem__("digest", "2" * 64))

    def test_preimage(self):
        def swap(h):
            p = h["digest_preimage"]
            p[0], p[1] = p[1], p[0]
        self.claim(swap)
        self.claim(lambda h: h["digest_preimage"].append({"kind": "text", "value": "extra"}))
        self.claim(lambda h: h["digest_preimage"][2].__setitem__("kind", "text"))
        body = self.claim(lambda h: h["digest_preimage"][2].__setitem__("kind", "url"), exit_codes=(2,))
        self.assertEqual(body["problems"][0]["code"], "preimage")

    def test_evaluator_claim(self):
        self.claim(lambda h: h["evaluator"].append({"path": "evaluator/x", "sha256": "3" * 64, "bytes": 1}))

    def test_version_and_keys(self):
        body = self.claim(lambda h: h.__setitem__("schema", "colab-handoff/3"), exit_codes=(2,))
        self.assertEqual(body["problems"][0]["code"], "version")
        self.claim(lambda h: h.__setitem__("extra", 1), exit_codes=(2,))
        self.claim(lambda h: h.pop("source_map"), exit_codes=(2,))
        self.claim(lambda h: h.__setitem__("verify", "not an object"), exit_codes=(2,))


class BoundBytes(Base):
    def test_package_byte_tampers(self):
        for rel in ("package/05.01.pack.md", "package/snapshots/0001.blob", "package/support/assembler/completion-receipt.json",
                    "package/templates/06.01.review.TEMPLATE.md", "prepared-colab.zip"):
            out = self.pk.clone()
            path = out / rel
            path.write_bytes(path.read_bytes() + b"\n")
            self.bad(out)
            self.assertNotEqual(self.producer_verify(out), 0, rel)

    def test_consistent_relabel_of_bound_files_fails_digest(self):
        # Rewrite the request, binding, ZIP and handoff consistently: the expected digest still refuses.
        out = self.pk.clone()
        req = json.loads((out / "package/colab-request.json").read_text(encoding="utf-8"))
        req["binding"]["investigation"]["page"] = "0799.wrong-investigation"
        (out / "package/colab-request.json").write_bytes(json.dumps(req).encode())
        (out / "package/binding.json").write_bytes(canonical(req["binding"]))
        body = self.bad(out)
        self.assertNotIn("0799", json.dumps(body))

    def test_noncanonical_binding(self):
        out = self.pk.clone()
        path = out / "package/binding.json"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(self.bad(out)["problems"][0]["code"], "binding")

    def test_missing_extra_and_fabricated(self):
        out = self.pk.clone()
        (out / "package/06.01.notes.md").unlink()
        self.bad(out)
        out = self.pk.clone()
        write(out / "package/notes-extra.md", "x")
        self.assertEqual(self.bad(out)["problems"][0]["code"], "extra")
        for rel in ("package/05.01.return.md", "06.01.review.md"):
            out = self.pk.clone()
            write(out / rel, "Accepted.\n")
            self.assertEqual(self.bad(out)["problems"][0]["code"], "fabricated-exchange")

    def test_duplicate_zip_entry(self):
        out = self.pk.clone()
        zpath = out / "prepared-colab.zip"
        with zipfile.ZipFile(zpath, "a") as archive:
            with self.assertWarns(UserWarning):
                archive.writestr("ENTRY.md", "duplicate")
        self.assertEqual(self.bad(out)["problems"][0]["code"], "zip")

    def test_manifest_commit_and_assembler_request(self):
        out = self.pk.clone()
        path = out / "package/source-manifest.json"
        man = json.loads(path.read_text())
        man["commit"] = "f" * 40
        path.write_bytes(json.dumps(man, indent=2).encode())
        self.bad(out)
        out = self.pk.clone()
        path = out / "package/support/assembler/request.snapshot"
        areq = json.loads(path.read_text(encoding="utf-8"))
        areq["origin"]["page"] = "0799.wrong-investigation"
        path.write_bytes(json.dumps(areq).encode())
        self.assertEqual(self.bad(out)["problems"][0]["code"], "assembler-request")

    def test_wrong_expected_digest(self):
        self.bad(self.pk.plain, digest="4" * 64)
        body, code = hc.check(str(self.pk.plain), "not-hex")
        self.assertEqual((code, body["problems"][0]["code"]), (2, "digest"))

    def test_evaluator_tampers(self):
        out = self.pk.clone("blind")
        (out / "evaluator/snapshots/0001.blob").write_bytes(b"changed key")
        self.bad(out, self.pk.blind_digest)
        out = self.pk.clone("blind")
        shutil.rmtree(out / "evaluator")
        self.bad(out, self.pk.blind_digest)
        out = self.pk.clone()
        write(out / "evaluator/source-manifest.json", "{}")
        self.bad(out)


class Malformed(Base):
    def raw_handoff(self, raw):
        out = self.pk.clone()
        (out / "handoff.json").write_bytes(raw)
        return self.bad(out, exit_codes=(2,))

    def test_strict_json(self):
        good = (self.pk.plain / "handoff.json").read_bytes()
        self.assertEqual(self.raw_handoff(good[:-20])["problems"][0]["code"], "json")
        self.assertEqual(self.raw_handoff(b"\xef\xbb\xbf" + good)["problems"][0]["code"], "bom")
        self.assertEqual(self.raw_handoff(b'{"schema": "colab-handoff/2", "schema": "x"}')["problems"][0]["code"], "duplicate-key")
        self.assertEqual(self.raw_handoff(b'{"schema": NaN}')["problems"][0]["code"], "nonfinite")
        self.assertEqual(self.raw_handoff(b"[]")["problems"][0]["code"], "json")
        self.assertEqual(self.raw_handoff(b'"' + b"x" * (5 * 1024 * 1024) + b'"')["problems"][0]["code"], "limit")

    def test_missing_handoff_and_relative_output(self):
        out = self.pk.clone()
        (out / "handoff.json").unlink()
        self.bad(out, exit_codes=(2,))
        body, code = hc.check("relative/out", self.pk.plain_digest)
        self.assertEqual((code, body["problems"][0]["code"]), (2, "path"))

    def test_preimage_part_shape(self):
        out = self.pk.clone()
        self.edit_handoff(out, lambda h: h["digest_preimage"].__setitem__(0, {"kind": "text"}))
        self.assertEqual(self.bad(out, exit_codes=(2,))["problems"][0]["code"], "preimage")

    def test_unsafe_paths(self):
        for bad in ("../x", "C:/x", "a\\b", "//host/share", "a/./b", "a/b ", ""):
            with self.assertRaises(hc.Refused):
                hc.safe_rel(bad, "probe")


class Links(Base):
    def test_linked_directory_inside_package(self):
        out = self.pk.clone()
        target = self.pk.root / f"elsewhere-{self.pk.n}"
        target.mkdir()
        if not junction(out / "package" / "linked", target):
            self.skipTest("junction not available")
        self.assertEqual(self.bad(out, exit_codes=(2,))["problems"][0]["code"], "linked")

    def test_linked_output_ancestor(self):
        out = self.pk.clone()
        link = self.pk.root / f"link-{self.pk.n}"
        if not junction(link, out):
            self.skipTest("junction not available")
        self.assertEqual(self.bad(link, exit_codes=(2,))["problems"][0]["code"], "linked")

    def test_hardlinked_file(self):
        out = self.pk.clone()
        try:
            os.link(out / "package/ENTRY.md", self.pk.root / f"hard-{self.pk.n}.md")
        except OSError:
            self.skipTest("hard links not available")
        self.assertEqual(self.bad(out, exit_codes=(2,))["problems"][0]["code"], "hardlink")


class Cli(Base):
    def test_cli_exit_codes_no_traceback(self):
        script = str(LAB / "handoff_check.py")
        ok = subprocess.run([sys.executable, "-B", script, "check", "--output", str(self.pk.plain),
                             "--expected-digest", self.pk.plain_digest, "--json"], capture_output=True)
        self.assertEqual(ok.returncode, 0, ok.stdout)
        out = self.pk.clone()
        self.edit_handoff(out, lambda h: h["investigation"].__setitem__("page", "0799.wrong-investigation"))
        bad = subprocess.run([sys.executable, "-B", script, "check", "--output", str(out),
                              "--expected-digest", self.pk.plain_digest, "--json"], capture_output=True)
        self.assertEqual(bad.returncode, 1)
        self.assertNotIn(b"Traceback", bad.stderr)
        self.assertEqual(json.loads(bad.stdout)["result"], "mismatch")


if __name__ == "__main__":
    unittest.main()
