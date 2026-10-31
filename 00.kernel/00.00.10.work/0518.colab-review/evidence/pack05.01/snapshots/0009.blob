"""Tests for colab-support-pass02 (exchange layout v2) on disposable repositories,
books and outputs, with the real pinned v1 producer, assembler, checker, capture
helper and inspector. Hooks are private in-process callables.

  python -B -X dev tests/test_colab_support_v2.py -v
"""

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LAB = HERE.parent
REPO_ROOT = LAB.parent.parent
sys.path.insert(0, str(LAB))
import colab_support as cs  # noqa: E402
import handoff_check as hc  # noqa: E402

TOOLS = {
    "assembler": REPO_ROOT / "labs/pack-assembly-pass01/pack_assembly.py",
    "checker": REPO_ROOT / "labs/pack-custody-pass01/pack_check.py",
    "helper": REPO_ROOT / "labs/return-capture-pass01/return_capture.py",
    "inspector": REPO_ROOT / "labs/return-capture-pass01/return_inspect.py",
    "producer_v1": REPO_ROOT / "labs/colab-support-pass01/colab_support.py",
}
FROZEN = {
    "labs/colab-support-pass01/colab_support.py": "33bbe41c52485fc7b2b611d830bae8a15129721ad807a931e8193f17944c467c",
    "labs/colab-support-pass01/README.md": "8b04686131fb00f35987754c10a3b540a02f13b736d99761f033c156b2b12d8e",
    "labs/colab-support-pass01/tests/test_colab_support.py": "f6be57f6bccf9a9aada4e32e0fc2681964cd2ead7bcb4e1f5ff6dc5983212ff8",
    "labs/pack-assembly-pass01/pack_assembly.py": "75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c",
    "labs/pack-custody-pass01/pack_check.py": "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d",
    "labs/return-capture-pass01/return_capture.py": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
    "labs/return-capture-pass01/return_inspect.py": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
}
BOOK = "00.00.10.work"
BASE = "00.kernel/00.00.10.work"
PAGE = (
    "# 01 — Fixture layout\n"
    "\n"
    "## Pass identity\n"
    "body\n"
    "```text\n"
    "## Example heading inside a fence\n"
    "```\n"
    "\n"
    "## Notes\n"
    "a\n"
    "\n"
    "## Notes\n"
    "b\n"
).encode("utf-8")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def frozen_hashes():
    return {rel: sha((REPO_ROOT / rel).read_bytes()) for rel in FROZEN}


def setUpModule():
    assert frozen_hashes() == FROZEN, "a frozen dependency differs before the suite"


def tearDownModule():
    assert frozen_hashes() == FROZEN, "a frozen dependency changed during the suite"


def git(repo, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="f@example.invalid",
               GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="f@example.invalid")
    out = subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, env=env)
    if out.returncode:
        raise RuntimeError(out.stderr.decode("utf-8", "replace"))
    return out.stdout.decode("utf-8").strip()


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))


class Fixture:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="colab2-test-")
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        write(self.repo / BASE / "0411.colab/evidence/layout/CONTRACT.md", PAGE)
        write(self.repo / BASE / "0411.colab/07.md", "# 07\nsource face 07 is data\n")
        write(self.repo / BASE / "0411.colab/02.md", "# 02\nrecords\n")
        write(self.repo / BASE / "0411.colab/evidence/key.md", "# key\nexpected answers\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "A")
        self.commit = git(self.repo, "rev-parse", "HEAD")
        self.config = self.root / "config.json"
        write(self.config, json.dumps({"schema": "colab-config/2", "repositories": {"fixture": str(self.repo)},
                                       "python": sys.executable, **{k: str(v) for k, v in TOOLS.items()}}))
        self.v1config = self.root / "config-v1.json"
        cfg1 = {"schema": "colab-config/1", "repositories": {"fixture": str(self.repo)}, "python": sys.executable,
                **{k: str(v) for k, v in TOOLS.items() if k != "producer_v1"}}
        write(self.v1config, json.dumps(cfg1))
        self.n = 0

    def request(self, **over):
        doc = {
            "schema": "colab-request/2",
            "binding": {"schema": "colab-binding/1",
                        "investigation": {"book": BOOK, "page": "0701.layout-probe", "pass": "05.01"},
                        "targets": [{"id": "T01", "book": BOOK, "page": "0411.colab",
                                     "file": "evidence/layout/CONTRACT.md",
                                     "section": {"kind": "heading", "value": "## Pass identity", "occurrence": None},
                                     "source": {"repository": "fixture", "commit": self.commit,
                                                "path": f"{BASE}/0411.colab/evidence/layout/CONTRACT.md",
                                                "sha256": sha(PAGE)}}]},
            "title": "Fixture layout probe", "date": "2026-10-29", "author": "fixture Prime",
            "recipient": "fixture Colab", "reviewer": "fixture reviewer", "mode": "hostile-read",
            "scoring": {"state": "unscored"}, "context": "Fixture context.", "question": "Does it hold?",
            "why": "Tests need a reason.", "built_state": "Nothing.", "known_gaps": ["gap"],
            "method": "Read.", "cases": [{"id": "C01", "text": "case"}],
            "environment": {"kind": "zip-only", "read": "package", "write": "one file", "execute": "none", "network": "none"},
            "permissions": ["read"], "stop": ["stop on mismatch"], "prior_involvement": "none",
            "required_sources": [{"path": f"{BASE}/0411.colab/07.md", "role": "source face 07 is ordinary data"}],
            "withheld": [], "unavailable": [], "director_replies": [],
            "return_route": {"destination": "return to Prime", "submission_hint": "one file"},
            "preparation_notes": ["note one", "note two\nwith a second line"],
        }
        doc.update(over)
        return doc

    def request_file(self, doc=None, raw=None):
        self.n += 1
        path = self.root / f"req-{self.n}.json"
        write(path, raw if raw is not None else json.dumps(doc if doc is not None else self.request(), ensure_ascii=False))
        return str(path)

    def output(self):
        self.n += 1
        return str(self.root / f"out-{self.n}")


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fx = Fixture()
        cls.status = git(cls.fx.repo, "status", "--porcelain")

    @classmethod
    def tearDownClass(cls):
        assert git(cls.fx.repo, "status", "--porcelain") == cls.status
        cls.fx.tmp.cleanup()

    def preview(self, doc=None, raw=None):
        return cs.preview(self.fx.request_file(doc, raw), str(self.fx.config))

    def refused(self, doc=None, raw=None, code=None):
        body, exit_code = self.preview(doc, raw)
        self.assertEqual(exit_code, 2, body)
        if code:
            self.assertEqual(body["findings"][0]["code"], code, body["findings"])
        return body

    def prepared(self, doc=None):
        request = self.fx.request_file(doc)
        body, code = cs.preview(request, str(self.fx.config))
        self.assertEqual(code, 0, body)
        out = self.fx.output()
        res, code = cs.prepare(request, str(self.fx.config), out, body["digest"])
        self.assertEqual(code, 0, res)
        return request, out, body["digest"]

    def verify_code(self, out):
        return cs.verify(out, str(self.fx.config))


class Names(Base):
    def test_exchange_names_follow_pass(self):
        doc = self.fx.request()
        doc["binding"]["investigation"]["pass"] = "05.03"
        _r, out, _d = self.prepared(doc)
        files = sorted(p.relative_to(Path(out) / "package").as_posix()
                       for p in (Path(out) / "package").rglob("*") if p.is_file())
        for name in ("05.03.pack.md", "06.03.notes.md", "templates/05.03.return.TEMPLATE.md",
                     "templates/06.03.review.TEMPLATE.md", "support/assembler/05.03.md", "support/SUPPORT.md",
                     "ENTRY.md", "binding.json", "colab-request.json", "source-manifest.json"):
            self.assertIn(name, files)
        self.assertNotIn("05.03.md", files)  # legacy draft only under support/
        handoff = json.loads((Path(out) / "handoff.json").read_text(encoding="utf-8"))
        self.assertEqual(handoff["exchange"]["primary_instruction"], "05.03.pack.md")
        self.assertEqual(handoff["not_created"], ["05.03.return.md", "06.03.review.md"])
        self.assertEqual([e["path"] for e in handoff["envelope"] if e["role"] == "pack-primary-instruction"],
                         ["package/05.03.pack.md"])
        self.assertEqual(json.loads((Path(out) / "package/binding.json").read_text())["investigation"]["pass"], "05.03")

    def test_no_return_or_review_before_receipt(self):
        _r, out, _d = self.prepared()
        all_files = [p.name for p in Path(out).rglob("*") if p.is_file()]
        self.assertFalse([n for n in all_files if n.endswith(".return.md") or n.endswith(".review.md")])
        entry = (Path(out) / "package/ENTRY.md").read_text(encoding="utf-8")
        self.assertIn("It is NOT in this package and does not exist yet.", entry)

    def test_fabricated_return_or_review_is_a_defect(self):
        for rel in ("package/05.01.return.md", "06.01.review.md"):
            _r, out, _d = self.prepared()
            write(Path(out) / rel, "Accepted. Looks good.\n")
            body, code = self.verify_code(out)
            self.assertEqual(code, 1, body)
            self.assertIn("fabricated-exchange", [f["code"] for f in body["findings"]])

    def test_missing_misnamed_extra(self):
        _r, out, _d = self.prepared()
        (Path(out) / "package/06.01.notes.md").unlink()
        body, code = self.verify_code(out)
        self.assertEqual(code, 1)
        self.assertIn("package/06.01.notes.md is missing", [f["detail"] for f in body["findings"]])
        _r, out, _d = self.prepared()
        os.rename(Path(out) / "package/05.01.pack.md", Path(out) / "package/05.01.md")
        body, code = self.verify_code(out)
        codes = sorted(f["code"] for f in body["findings"])
        self.assertEqual(code, 1)
        self.assertIn("missing", codes)
        self.assertIn("extra", codes)
        _r, out, _d = self.prepared()
        write(Path(out) / "package/notes-extra.md", "x")
        self.assertEqual(self.verify_code(out)[1], 1)

    def test_source_names_are_data(self):
        body, code = self.preview()
        self.assertEqual(code, 0, body)  # 0411.colab page and a 07.md source are legal sources


class Content(Base):
    def test_notes_and_quotes_exact(self):
        reply = 'Yes review is right that\'s good.\n"quoted" — kept'
        doc = self.fx.request(director_replies=[
            {"id": "D01", "date": "2026-10-29", "source": "chat", "reply": reply, "status": "actual"},
            {"id": "D02", "date": "2026-10-29", "source": "fixture", "reply": "maybe", "status": "hypothetical-fixture"}])
        _r, out, _d = self.prepared(doc)
        notes = (Path(out) / "package/06.01.notes.md").read_text(encoding="utf-8")
        entry = (Path(out) / "package/ENTRY.md").read_text(encoding="utf-8")
        self.assertIn("N01. note one\nN02. note two\nwith a second line", notes)
        quoted = "reply: Yes review is right that's good.\nreply: \"quoted\" — kept"
        self.assertIn(quoted, notes)
        self.assertIn(quoted, entry)
        self.assertIn("not a review", notes)
        self.assertIn("HYPOTHETICAL FIXTURE, not a Director decision", entry)

    def test_template_is_not_review(self):
        _r, out, _d = self.prepared()
        review = (Path(out) / "package/templates/06.01.review.TEMPLATE.md").read_text(encoding="utf-8")
        ret = (Path(out) / "package/templates/05.01.return.TEMPLATE.md").read_text(encoding="utf-8")
        self.assertTrue(review.startswith("# TEMPLATE — 06.01.review.md"))
        self.assertIn("THIS IS A TEMPLATE. No review has happened.", review)
        for heading in ("## Prime assessment", "## Director reply", "## Unresolved questions",
                        "## Dispositions and reasons", "## Route"):
            self.assertIn(heading, review)
        self.assertIn("Never write an approval that was not given.", review)
        self.assertIn("None is chosen by this template.", review)
        self.assertTrue(ret.startswith("# TEMPLATE — 05.01.return.md"))
        for heading in ("## Hostile", "## Factfind", "## Overflow", "## Unprompted"):
            self.assertIn(heading, ret)
        self.assertNotIn("accepted", review.lower().replace("not accepted", ""))

    def test_support_is_declared_not_instruction(self):
        _r, out, _d = self.prepared()
        support = (Path(out) / "package/support/SUPPORT.md").read_text(encoding="utf-8")
        self.assertIn("It is NOT an instruction source. The instruction source is `05.01.pack.md`.", support)
        legacy = (Path(out) / "package/support/assembler/05.01.md").read_text(encoding="utf-8")
        self.assertIn("It is not an instruction source.", legacy)
        for name in ("05.01.md", "request.snapshot", "completion-receipt.json"):
            self.assertEqual((Path(out) / "package/support/assembler" / name).read_bytes(),
                             (Path(out) / "assembler-output" / name).read_bytes())


class Versions(Base):
    def test_wrong_request_versions(self):
        self.refused(self.fx.request(schema="colab-request/1"), code="version")
        self.refused(self.fx.request(schema="colab-request/3"), code="version")
        doc = self.fx.request()
        del doc["preparation_notes"]
        self.refused(doc, code="missing-key")

    def test_wrong_config_version(self):
        cfg = json.loads(self.fx.config.read_text())
        cfg["schema"] = "colab-config/1"
        bad = self.fx.root / "bad-config.json"
        write(bad, json.dumps(cfg))
        body, code = cs.preview(self.fx.request_file(), str(bad))
        self.assertEqual((code, body["findings"][0]["code"]), (2, "version"))

    def test_v1_output_refused_by_v2_and_v2_output_refused_by_v1(self):
        sys.path.insert(0, str(REPO_ROOT / "labs/colab-support-pass01"))
        v1_doc = self.fx.request(schema="colab-request/1")
        del v1_doc["preparation_notes"]
        req = self.fx.request_file(v1_doc)
        import importlib.util
        spec = importlib.util.spec_from_file_location("v1_for_test", TOOLS["producer_v1"])
        v1 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(v1)
        digest = v1.preview(req, str(self.fx.v1config))[0]["digest"]
        out1 = self.fx.output()
        self.assertEqual(v1.prepare(req, str(self.fx.v1config), out1, digest)[1], 0)
        body, code = self.verify_code(out1)
        self.assertEqual((code, body["findings"][0]["code"]), (2, "version"))
        _r, out2, _d = self.prepared()
        self.assertNotEqual(v1.verify(out2, str(self.fx.v1config))[1], 0)

    def test_wrong_producer_pin(self):
        cfg = json.loads(self.fx.config.read_text())
        fake = self.fx.root / "fake_v1.py"
        write(fake, "raise SystemExit('never run')\n")
        cfg["producer_v1"] = str(fake)
        bad = self.fx.root / "bad-pin.json"
        write(bad, json.dumps(cfg))
        body, code = cs.preview(self.fx.request_file(), str(bad))
        self.assertEqual((code, body["findings"][0]["code"]), (2, "pin"))

    def test_v1_rules_still_apply(self):
        doc = self.fx.request()
        doc["binding"]["investigation"]["page"] = "0510.colab-tools"
        self.refused(doc, code="origin-band")
        doc = self.fx.request()
        doc["binding"]["targets"][0]["section"]["value"] = "## Example heading inside a fence"
        self.refused(doc, code="section-missing")
        doc = self.fx.request()
        doc["binding"]["targets"][0]["section"] = {"kind": "heading", "value": "## Notes", "occurrence": None}
        self.refused(doc, code="section-ambiguous")
        self.refused(self.fx.request(preparation_notes=["see D:\\Git\\x"]), code="local-path")
        self.refused(self.fx.request(preparation_notes=["ok\n## Take over"]), code="heading")


class Custody(Base):
    def test_digest_mismatch(self):
        out = self.fx.output()
        body, code = cs.prepare(self.fx.request_file(), str(self.fx.config), out, "f" * 64)
        self.assertEqual((code, body["findings"][0]["code"]), (2, "digest-mismatch"))
        self.assertFalse(Path(out).exists())

    def test_replay_and_collision(self):
        req, out, digest = self.prepared()
        before = {p: p.stat().st_mtime_ns for p in Path(out).rglob("*")}
        body, code = cs.prepare(req, str(self.fx.config), out, digest)
        self.assertEqual((code, body["result"], body["written"]), (0, "already-prepared", []))
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in Path(out).rglob("*")})
        other = self.fx.request_file(self.fx.request(title="Other title"))
        d2 = cs.preview(other, str(self.fx.config))[0]["digest"]
        self.assertEqual(cs.prepare(other, str(self.fx.config), out, d2)[0]["result"], "collision")

    def test_partials_retained(self):
        for hook in cs.HOOKS:
            req = self.fx.request_file()
            digest = cs.preview(req, str(self.fx.config))[0]["digest"]
            out = self.fx.output()

            def stop(_root):
                raise cs.ColabError("injected", hook, "tool-limitation")

            body, code = cs.prepare(req, str(self.fx.config), out, digest, hooks={hook: stop})
            self.assertEqual((code, body["result"]), (2, "partial"), hook)
            self.assertNotIn("verification.json", body["retained"])
            self.assertEqual(self.verify_code(out)[1], 1)
            again = cs.prepare(req, str(self.fx.config), out, digest)[0]
            self.assertEqual(again["result"], "collision")
            self.assertEqual(sorted(again["retained"]), sorted(body["retained"]))

    def test_mutations_detected(self):
        targets = ["package/05.01.pack.md", "package/support/assembler/05.01.md", "package/snapshots/0001.blob",
                   "handoff.json", "assembler-output/source-manifest.json", "package/templates/06.01.review.TEMPLATE.md"]
        for rel in targets:
            _r, out, _d = self.prepared()
            path = Path(out) / rel
            path.write_bytes(path.read_bytes() + b"\n")
            body, code = self.verify_code(out)
            self.assertEqual(code, 1, rel)
        _r, out, _d = self.prepared()
        zpath = Path(out) / "prepared-colab.zip"
        with zipfile.ZipFile(zpath, "a") as archive:
            archive.writestr("05.01.return.md", "fake return")
        self.assertEqual(self.verify_code(out)[1], 1)

    def test_linked_output_and_entries(self):
        req = self.fx.request_file()
        digest = cs.preview(req, str(self.fx.config))[0]["digest"]
        real = self.fx.root / "real-dir"
        real.mkdir()
        link = self.fx.root / "link-out"
        if os.name == "nt":
            if subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(real)], capture_output=True).returncode:
                self.skipTest("junction not available")
        else:
            os.symlink(real, link)
        self.assertEqual(cs.prepare(req, str(self.fx.config), str(link), digest)[1], 2)
        self.assertEqual(list(real.iterdir()), [])
        _r, out, _d = self.prepared()
        inner = Path(out) / "package" / "linked"
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "mklink", "/J", str(inner), str(real)], capture_output=True)
        else:
            os.symlink(real, inner)
        self.assertEqual(self.verify_code(out)[1], 2)

    def test_blind_evaluator_absent_from_package(self):
        doc = self.fx.request(mode="controlled-experiment", scoring={
            "state": "scored", "blind": True, "evaluator_sources": [f"{BASE}/0411.colab/evidence/key.md"]})
        _r, out, digest = self.prepared(doc)
        with zipfile.ZipFile(Path(out) / "prepared-colab.zip") as archive:
            blob = b"".join(archive.read(n) for n in archive.namelist())
            self.assertFalse(any(n.startswith("evaluator") for n in archive.namelist()))
        self.assertNotIn(b"expected answers", blob)
        self.assertTrue((Path(out) / "evaluator/snapshots/0001.blob").exists())
        self.assertEqual(self.verify_code(out)[1], 0)
        self.assertEqual(hc.check(out, digest)[1], 0)


class Handoff(Base):
    def test_standalone_check_and_copy(self):
        _r, out, digest = self.prepared()
        body, code = hc.check(out, digest)
        self.assertEqual((code, body["result"]), (0, "valid"), body)
        dest = self.fx.root / f"copy-{self.fx.n}"
        body, code = hc.copy(out, digest, str(dest))
        self.assertEqual((code, body["result"]), (0, "copied"), body)
        self.assertEqual((dest / "05.01.pack.md").read_bytes(), (Path(out) / "package/05.01.pack.md").read_bytes())
        self.assertEqual(hc.copy(out, digest, str(dest))[1], 2)  # never overwrites
        self.assertEqual(hc.check(out, "0" * 64)[1], 1)
        pack = Path(out) / "package/05.01.pack.md"
        pack.write_bytes(pack.read_bytes() + b"x")
        self.assertEqual(hc.check(out, digest)[1], 1)

    def test_handoff_preimage_recomputes_digest(self):
        _r, out, digest = self.prepared()
        handoff = json.loads((Path(out) / "handoff.json").read_text(encoding="utf-8"))
        self.assertEqual(handoff["digest"], digest)
        self.assertEqual(handoff["layout"], "colab-exchange-layout/2")
        self.assertEqual(handoff["digest_domain"], "colab-package-digest/2")
        self.assertIn({"kind": "text", "value": "package/05.01.pack.md"}, handoff["digest_preimage"])
        mapped = {m["source_path"]: m for m in handoff["source_map"]}
        self.assertEqual(mapped[f"{BASE}/0411.colab/evidence/layout/CONTRACT.md"]["targets"], ["T01"])
        self.assertEqual(mapped[f"{BASE}/0411.colab/07.md"]["role"], "required")
        self.assertNotIn(str(self.fx.repo), json.dumps(handoff))


class Intake(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.book_root = cls.fx.root / "bookroot"
        cls.book = cls.book_root / "00.kernel" / BOOK
        write(cls.book / "0100.band.returns" / "01.md", "# 01\ndoor\n")
        req = cls.fx.request_file()
        digest = cs.preview(req, str(cls.fx.config))[0]["digest"]
        cls.out = cls.fx.output()
        assert cs.prepare(req, str(cls.fx.config), cls.out, digest)[1] == 0
        cls.digest = digest

    def reserve(self, sub, name, page, batch="05.01"):
        out = subprocess.run([sys.executable, "-B", str(TOOLS["helper"]), "reserve", "--book", str(self.book),
                              "--submission", sub, "--name", name, "--origin-book", BOOK, "--origin-page", page,
                              "--origin-batch", batch, "--expected-output", "notes", "--submitter", "SYNTHETIC FIXTURE",
                              "--reviewer", "fixture", "--release", "fixture only"], capture_output=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        return [p.name for p in self.book.iterdir() if p.name.endswith(name)][0]

    def source(self, tag):
        src = self.book_root / f"src-{tag}"
        write(src / "return.md", "# SYNTHETIC FIXTURE return — no model\n\n## Hostile\nnone\n\n## Factfind\nnone\n\n"
                                 "## Overflow\nnone\n\n## Unprompted\nnone\n\n## Director replies\nnone\n")
        write(src / "notes.txt", f"synthetic {tag}\n")
        return src

    def run_intake(self, member, src):
        return cs.intake(self.out, str(self.fx.config), str(self.book), member, str(src / "return.md"),
                         str(src), ["notes.txt|notes"])

    def test_capture_placement_replay_conflict(self):
        member = self.reserve("syn-0701-0501", "syn-layout", "0701.layout-probe")
        src = self.source("a")
        original = (src / "return.md").read_bytes()
        body, code = self.run_intake(member, src)
        self.assertEqual((code, body["result"]), (0, "captured"), body)
        place = body["placement"]
        self.assertEqual(place["schema"], "colab-placement-proposal/2")
        self.assertEqual(place["action"], "proposed; not written")
        self.assertEqual(place["destination"], {"book": BOOK, "page": "0701.layout-probe", "file": "05.01.return.md"})
        self.assertEqual(place["source"]["sha256"], sha(original))
        self.assertEqual((self.book / member / "return.md").read_bytes(), original)  # exact bytes, no injection
        self.assertFalse(list(self.book_root.rglob("05.01.return.md")))
        self.assertFalse(list(self.book_root.rglob("06.01.review.md")))
        again, code = self.run_intake(member, src)
        self.assertEqual((code, again["result"]), (0, "already-captured"))
        write(src / "notes.txt", "changed\n")
        changed, code = self.run_intake(member, src)
        self.assertEqual((code, changed["result"]), (1, "attention"))
        self.assertNotIn("placement", changed)

    def test_wrong_target_origin_refused(self):
        member = self.reserve("syn-target", "syn-target", "0411.colab")
        body, code = self.run_intake(member, self.source("b"))
        self.assertEqual((code, body["result"]), (2, "wrong-origin"))
        self.assertEqual(len(body["runs"]), 1)
        self.assertEqual(sorted(p.name for p in (self.book / member).iterdir()), ["01.md", "reservation.json"])


class Cli(Base):
    def test_cli_no_traceback(self):
        script = str(LAB / "colab_support.py")
        out = subprocess.run([sys.executable, "-B", script, "preview", "--request", self.fx.request_file(raw="{x"),
                              "--config", str(self.fx.config), "--json"], capture_output=True)
        self.assertEqual(out.returncode, 2)
        self.assertNotIn(b"Traceback", out.stderr)
        _r, out_dir, digest = self.prepared()
        out = subprocess.run([sys.executable, "-B", str(LAB / "handoff_check.py"), "check", "--output", out_dir,
                              "--expected-digest", digest, "--json"], capture_output=True)
        self.assertEqual(out.returncode, 0, out.stdout)


if __name__ == "__main__":
    unittest.main()
