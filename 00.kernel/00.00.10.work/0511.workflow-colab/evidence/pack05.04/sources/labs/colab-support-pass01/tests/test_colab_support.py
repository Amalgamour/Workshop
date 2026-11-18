"""Tests for colab_support.py on disposable repositories, books and outputs.

The real pinned assembler, checker, capture helper and inspector are used.
Hooks are private in-process callables, not CLI switches.

  python -B -X dev tests/test_colab_support.py -v
"""

import copy
import hashlib
import io
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

TOOLS = {
    "assembler": REPO_ROOT / "labs/pack-assembly-pass01/pack_assembly.py",
    "checker": REPO_ROOT / "labs/pack-custody-pass01/pack_check.py",
    "helper": REPO_ROOT / "labs/return-capture-pass01/return_capture.py",
    "inspector": REPO_ROOT / "labs/return-capture-pass01/return_inspect.py",
}
BOOK = "00.00.10.work"
BASE = "00.kernel/00.00.10.work"
PAGE_TEXT = (
    "# 01 — Fixture design\n"
    "version: 001\n"
    "state: draft\n"
    "\n"
    "## Purpose\n"
    "Purpose body.\n"
    "\n"
    "```text\n"
    "## Compute\n"
    "a fenced example heading, not a section\n"
    "```\n"
    "\n"
    "## Compute\n"
    "Compute body line.\n"
    "### Detail\n"
    "Nested detail.\n"
    "\n"
    "## Notes\n"
    "first notes\n"
    "\n"
    "## Notes\n"
    "second notes\n"
    "\n"
    "## End\n"
    "end.\n"
).encode("utf-8")
PNG = b"\x89PNG\r\n\x1a\n" + bytes(range(64))


def sha(data):
    return hashlib.sha256(data).hexdigest()


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
    """One disposable Git repository with two commits, plus a config."""

    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="colab-test-")
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        write(self.repo / BASE / "0411.colab/01.md", PAGE_TEXT)
        write(self.repo / BASE / "0411.colab/02.md", "# 02\nrecord groups\n")
        write(self.repo / BASE / "0508.return-capture/05.19.md", "# 05\n## #02 — One proposed source record\nbody\n")
        write(self.repo / BASE / "0411.colab/evidence/figure.png", PNG)
        write(self.repo / BASE / "0411.colab/evidence/rubric-key.md", "# key\nexpected answers\n")
        write(self.repo / BASE / "0411.colab/evidence/rubric-copy.md", "# 02\nrecord groups\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "A")
        self.commit_a = git(self.repo, "rev-parse", "HEAD")
        write(self.repo / BASE / "0411.colab/01.md", PAGE_TEXT.replace(b"## Compute\nCompute", b"## Compute ops\nCompute"))
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "B")
        self.commit_b = git(self.repo, "rev-parse", "HEAD")
        self.page_b = (self.repo / BASE / "0411.colab/01.md").read_bytes()
        self.config = self.root / "config.json"
        write(self.config, json.dumps({
            "schema": "colab-config/1",
            "repositories": {"fixture": str(self.repo)},
            "python": sys.executable,
            **{name: str(path) for name, path in TOOLS.items()},
        }))
        self.counter = 0

    def target(self, tid="T01", file="01.md", page="0411.colab", section=None, commit=None, data=PAGE_TEXT):
        return {
            "id": tid, "book": BOOK, "page": page, "file": file, "section": section,
            "source": {"repository": "fixture", "commit": commit or self.commit_a,
                       "path": f"{BASE}/{page}/{file}", "sha256": sha(data)},
        }

    def request(self, **over):
        doc = {
            "schema": "colab-request/1",
            "binding": {
                "schema": "colab-binding/1",
                "investigation": {"book": BOOK, "page": "0701.desk-state", "pass": "05.01"},
                "targets": [self.target(section={"kind": "heading", "value": "## Compute", "occurrence": None})],
            },
            "title": "Fixture investigation",
            "date": "2026-10-29",
            "author": "fixture Prime",
            "recipient": "fixture Colab",
            "reviewer": "fixture reviewer",
            "mode": "open-design",
            "scoring": {"state": "unscored"},
            "context": "Fixture context.",
            "question": "Does the fixture hold?",
            "why": "Because tests need a reason.",
            "built_state": "Nothing is built.",
            "known_gaps": ["gap one"],
            "method": "Read and say.",
            "cases": [{"id": "C01", "text": "case one"}],
            "environment": {"kind": "zip-only", "read": "package only", "write": "one return file",
                            "execute": "nothing", "network": "none"},
            "permissions": ["read the package"],
            "stop": ["stop on a hash mismatch"],
            "prior_involvement": "none",
            "required_sources": [{"path": f"{BASE}/0411.colab/02.md", "role": "records"}],
            "withheld": [],
            "unavailable": [],
            "director_replies": [],
            "return_route": {"destination": "return to Prime", "submission_hint": "one file"},
        }
        doc.update(over)
        return doc

    def request_file(self, doc=None, raw=None):
        self.counter += 1
        path = self.root / f"request-{self.counter}.json"
        write(path, raw if raw is not None else json.dumps(doc if doc is not None else self.request(), ensure_ascii=False, indent=2))
        return str(path)

    def output(self):
        self.counter += 1
        return str(self.root / f"out-{self.counter}")


def preview_of(fx, doc=None, raw=None):
    return cs.preview(fx.request_file(doc, raw), str(fx.config))


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fx = Fixture()
        cls.status_before = git(cls.fx.repo, "status", "--porcelain")

    @classmethod
    def tearDownClass(cls):
        # No test may change the source repository.
        assert git(cls.fx.repo, "status", "--porcelain") == cls.status_before
        assert git(cls.fx.repo, "rev-parse", "HEAD") == cls.fx.commit_b
        cls.fx.tmp.cleanup()

    def refused(self, doc=None, raw=None, code=None, kind=None):
        body, exit_code = preview_of(self.fx, doc, raw)
        self.assertEqual(exit_code, 2, body)
        self.assertEqual(body["result"], "invalid")
        if code:
            self.assertEqual(body["findings"][0]["code"], code, body["findings"])
        if kind:
            self.assertEqual(body["findings"][0]["kind"], kind)
        return body

    def prepared(self, doc=None):
        request = self.fx.request_file(doc)
        body, code = cs.preview(request, str(self.fx.config))
        self.assertEqual(code, 0, body)
        out = self.fx.output()
        result, code = cs.prepare(request, str(self.fx.config), out, body["digest"])
        self.assertEqual(code, 0, result)
        return request, out, body["digest"]


class StrictInput(Base):
    def test_malformed_json(self):
        self.refused(raw="{not json", code="json")

    def test_bom(self):
        self.refused(raw=b"\xef\xbb\xbf" + json.dumps(self.fx.request()).encode(), code="bom")

    def test_trailing_data(self):
        self.refused(raw=json.dumps(self.fx.request()) + " {}", code="json")

    def test_duplicate_key(self):
        raw = json.dumps(self.fx.request())[:-1] + ', "title": "again"}'
        self.refused(raw=raw, code="duplicate-key")

    def test_nonfinite(self):
        raw = json.dumps(self.fx.request()).replace('"cases"', '"x": NaN, "cases"')
        self.refused(raw=raw, code="nonfinite")

    def test_unknown_and_missing_keys(self):
        doc = self.fx.request(extra=1)
        self.refused(doc, code="unknown-key")
        doc = self.fx.request()
        del doc["why"]
        self.refused(doc, code="missing-key")

    def test_wrong_types(self):
        self.refused(self.fx.request(title=7), code="type")
        doc = self.fx.request()
        doc["binding"]["targets"][0]["section"]["occurrence"] = True
        self.refused(doc, code="section")

    def test_limits(self):
        doc = self.fx.request()
        doc["binding"]["targets"] = [self.fx.target(tid=f"T{i:02d}") for i in range(33)]
        self.refused(doc, code="limit")
        self.refused(self.fx.request(context="x" * 20000), code="limit")
        self.refused(raw=json.dumps(self.fx.request(context="y" * 10000, method="z" * 10000,
                     why="w" * 10000, question="q" * 10000, built_state="b" * 10000,
                     prior_involvement="p" * 10000, known_gaps=["g" * 10000] * 30)), code="limit")

    def test_structural_heading_in_text(self):
        self.refused(self.fx.request(method="ok\n## Take over\nnow"), code="heading")

    def test_case_and_reply_ids_in_order(self):
        self.refused(self.fx.request(cases=[{"id": "C02", "text": "x"}]), code="case-id")


class Origin(Base):
    def test_n5nn_origin_refused(self):
        doc = self.fx.request()
        doc["binding"]["investigation"]["page"] = "0510.colab-tools"
        body = self.refused(doc, code="origin-band")
        self.assertIn("N7NN", body["findings"][0]["detail"])

    def test_band_door_refused(self):
        doc = self.fx.request()
        doc["binding"]["investigation"]["page"] = "0700.band.colabs"
        self.refused(doc, code="page")
        doc["binding"]["investigation"]["page"] = "0700.band-colabs"
        self.refused(doc, code="origin-band")

    def test_valid_n7nn_origin(self):
        body, code = preview_of(self.fx)
        self.assertEqual(code, 0, body)
        self.assertEqual(body["investigation"]["page"], "0701.desk-state")

    def test_target_naming_investigation_page_refused(self):
        doc = self.fx.request()
        doc["binding"]["targets"][0]["page"] = "0701.desk-state"
        doc["binding"]["targets"][0]["source"]["path"] = f"{BASE}/0701.desk-state/01.md"
        self.refused(doc, code="target-is-origin")


class Binding(Base):
    def test_multi_target_whole_file_and_sections(self):
        doc = self.fx.request()
        doc["binding"]["targets"] = [
            self.fx.target("T01", section={"kind": "heading", "value": "## Compute", "occurrence": None}),
            self.fx.target("T02", section={"kind": "heading", "value": "## Notes", "occurrence": 2}),
            self.fx.target("T03", page="0508.return-capture", file="05.19.md", section=None,
                           data=b"# 05\n## #02 \xe2\x80\x94 One proposed source record\nbody\n"),
        ]
        body, code = preview_of(self.fx, doc)
        self.assertEqual(code, 0, body)
        t1, t2, t3 = body["targets"]
        self.assertEqual((t1["line_start"], t1["line_end"]), (13, 17))  # the fenced copy is ignored
        self.assertEqual(t1["matches"], 1)
        self.assertEqual((t2["line_start"], t2["line_end"]), (21, 23))
        self.assertEqual(t3["kind"], "whole-file")
        sources = [p["path"] for p in body["planned"] if p["path"].startswith("package/snapshots/")]
        self.assertEqual(len(sources), 3)  # one file for T01/T02, one for T03, one required source

    def test_duplicate_heading_needs_occurrence(self):
        doc = self.fx.request()
        doc["binding"]["targets"][0]["section"] = {"kind": "heading", "value": "## Notes", "occurrence": None}
        self.refused(doc, code="section-ambiguous")
        doc["binding"]["targets"][0]["section"]["occurrence"] = 3
        self.refused(doc, code="section-missing")

    def test_no_fuzzy_heading(self):
        doc = self.fx.request()
        doc["binding"]["targets"][0]["section"]["value"] = "## compute"
        self.refused(doc, code="section-missing")
        doc["binding"]["targets"][0]["section"]["value"] = "## Comp"
        self.refused(doc, code="section-missing")

    def test_stale_source_and_section(self):
        doc = self.fx.request()
        doc["binding"]["targets"][0]["source"]["sha256"] = sha(self.fx.page_b)
        body = self.refused(doc, code="stale-source")
        self.assertIn(sha(PAGE_TEXT), body["findings"][0]["detail"])  # reported as a fact
        self.assertIn("nothing was retargeted", body["findings"][0]["detail"])
        doc = self.fx.request()
        doc["binding"]["targets"] = [self.fx.target(commit=self.fx.commit_b, data=self.fx.page_b,
                                     section={"kind": "heading", "value": "## Compute", "occurrence": None})]
        self.refused(doc, code="section-missing")  # the heading text moved at the later commit; no retarget

    def test_section_id_unsupported(self):
        doc = self.fx.request()
        doc["binding"]["targets"][0]["section"] = {"kind": "id", "value": "compute", "occurrence": None}
        self.refused(doc, code="unsupported-section-id", kind="tool-limitation")

    def test_duplicate_targets(self):
        doc = self.fx.request()
        doc["binding"]["targets"].append(copy.deepcopy(doc["binding"]["targets"][0]))
        self.refused(doc, code="duplicate-target")
        doc["binding"]["targets"][1]["id"] = "T02"
        self.refused(doc, code="duplicate-target")

    def test_path_consistency(self):
        doc = self.fx.request()
        doc["binding"]["targets"][0]["file"] = "02.md"
        self.refused(doc, code="path-mismatch")

    def test_unsafe_paths(self):
        for bad in ("../x/0411.colab/01.md", "C:/x/0411.colab/01.md", "a\\0411.colab/01.md"):
            doc = self.fx.request()
            doc["binding"]["targets"][0]["source"]["path"] = bad
            self.refused(doc, code="path")
        self.refused(self.fx.request(required_sources=[{"path": "/abs/x", "role": "r"}]), code="path")

    def test_multi_commit_refused(self):
        doc = self.fx.request()
        doc["binding"]["targets"].append(self.fx.target("T02", page="0508.return-capture", file="05.19.md",
                                         commit=self.fx.commit_b, data=b"x"))
        self.refused(doc, code="multi-commit", kind="tool-limitation")

    def test_missing_image_body(self):
        doc = self.fx.request(required_sources=[{"path": f"{BASE}/0411.colab/evidence/missing.png", "role": "figure"}])
        body = self.refused(doc, code="source")
        self.assertIn("absent", body["findings"][0]["detail"])

    def test_committed_image_travels(self):
        doc = self.fx.request(required_sources=[{"path": f"{BASE}/0411.colab/evidence/figure.png", "role": "figure"}])
        _req, out, _digest = self.prepared(doc)
        with zipfile.ZipFile(Path(out) / "prepared-colab.zip") as archive:
            self.assertIn(PNG, [archive.read(n) for n in archive.namelist()])


class Prepare(Base):
    def test_prepare_verify_and_zip_closure(self):
        _req, out, digest = self.prepared()
        body, code = cs.verify(out, str(self.fx.config))
        self.assertEqual(code, 0, body)
        self.assertEqual(body["result"], "intact")
        self.assertEqual(body["digest"], digest)
        self.assertEqual(body["assembler_verify"]["exit"], 0)
        root = Path(out)
        package = {p.relative_to(root / "package").as_posix(): p.read_bytes()
                   for p in (root / "package").rglob("*") if p.is_file()}
        with zipfile.ZipFile(root / "prepared-colab.zip") as archive:
            members = {n: archive.read(n) for n in archive.namelist()}
        self.assertEqual(members, package)
        for name in ("binding.json", "ENTRY.md", "05.01.md", "06.01.md", "RETURN-TEMPLATE.md",
                     "source-manifest.json", "completion-receipt.json", "request.snapshot", "colab-request.json"):
            self.assertIn(name, package)
        self.assertFalse(any(".colab" in n.split("/")[-1][-7:] for n in package))
        entry = package["ENTRY.md"].decode("utf-8")
        self.assertNotIn(str(self.fx.repo), entry)
        self.assertNotIn(str(self.fx.repo), package["binding.json"].decode("utf-8"))
        self.assertIn("state: draft", package["05.01.md"].decode("utf-8"))
        self.assertIn("Release: PENDING.", package["05.01.md"].decode("utf-8"))

    def test_digest_mismatch_writes_nothing(self):
        request = self.fx.request_file()
        out = self.fx.output()
        body, code = cs.prepare(request, str(self.fx.config), out, "0" * 64)
        self.assertEqual(code, 2)
        self.assertEqual(body["findings"][0]["code"], "digest-mismatch")
        self.assertFalse(Path(out).exists())

    def test_replay_is_read_only(self):
        request, out, digest = self.prepared()
        before = {p: p.stat().st_mtime_ns for p in Path(out).rglob("*")}
        body, code = cs.prepare(request, str(self.fx.config), out, digest)
        self.assertEqual((code, body["result"], body["written"]), (0, "already-prepared", []))
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in Path(out).rglob("*")})

    def test_collision_with_other_content(self):
        request = self.fx.request_file()
        digest = cs.preview(request, str(self.fx.config))[0]["digest"]
        out = self.fx.output()
        write(Path(out) / "someone-else.txt", "keep me")
        body, code = cs.prepare(request, str(self.fx.config), out, digest)
        self.assertEqual((code, body["result"]), (2, "collision"))
        self.assertEqual((Path(out) / "someone-else.txt").read_text(), "keep me")

    def test_collision_with_different_package(self):
        _req, out, _digest = self.prepared()
        other = self.fx.request_file(self.fx.request(title="Another title"))
        digest = cs.preview(other, str(self.fx.config))[0]["digest"]
        body, code = cs.prepare(other, str(self.fx.config), out, digest)
        self.assertEqual((code, body["result"]), (2, "collision"))
        self.assertEqual(cs.verify(out, str(self.fx.config))[1], 0)

    def test_partial_is_retained_and_not_completed(self):
        for hook in cs.HOOKS:
            request = self.fx.request_file()
            digest = cs.preview(request, str(self.fx.config))[0]["digest"]
            out = self.fx.output()

            def stop(_root):
                raise cs.ColabError("injected", f"stopped at {hook}", "tool-limitation")

            body, code = cs.prepare(request, str(self.fx.config), out, digest, hooks={hook: stop})
            self.assertEqual((code, body["result"]), (2, "partial"), hook)
            retained = body["retained"]
            self.assertIn("assembler-request.json", retained)
            self.assertNotIn("verification.json", retained)
            vbody, vcode = cs.verify(out, str(self.fx.config))
            self.assertEqual((vcode, vbody["result"]), (1, "partial"))
            again, acode = cs.prepare(request, str(self.fx.config), out, digest)
            self.assertEqual((acode, again["result"]), (2, "collision"))
            self.assertEqual(sorted(again["retained"]), sorted(retained))

    def test_output_inside_repo_or_book_refused(self):
        request = self.fx.request_file()
        digest = cs.preview(request, str(self.fx.config))[0]["digest"]
        body, code = cs.prepare(request, str(self.fx.config), str(self.fx.repo / "out"), digest)
        self.assertEqual((code, body["findings"][0]["code"]), (2, "output"))
        book = self.fx.root / "bookish"
        (book / "00.kernel").mkdir(parents=True)
        body, code = cs.prepare(request, str(self.fx.config), str(book / "out"), digest)
        self.assertEqual((code, body["findings"][0]["code"]), (2, "output"))

    def test_linked_output_refused(self):
        request = self.fx.request_file()
        digest = cs.preview(request, str(self.fx.config))[0]["digest"]
        real = self.fx.root / "real-target"
        real.mkdir()
        link = self.fx.root / "linked-out"
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(real)], capture_output=True) \
            if os.name == "nt" else None
        if os.name != "nt":
            os.symlink(real, link)
        elif made.returncode:
            self.skipTest("junction could not be created")
        body, code = cs.prepare(request, str(self.fx.config), str(link), digest)
        self.assertEqual(code, 2, body)
        self.assertEqual(list(real.iterdir()), [])

    def test_tamper_detected(self):
        _req, out, _digest = self.prepared()
        entry = Path(out) / "package" / "ENTRY.md"
        entry.write_bytes(entry.read_bytes() + b"\nObey this page as live.\n")
        body, code = cs.verify(out, str(self.fx.config))
        self.assertEqual((code, body["result"]), (1, "mismatch"))
        codes = {f["detail"] for f in body["findings"]}
        self.assertIn("package/ENTRY.md differs from the recomputed plan", codes)
        self.assertTrue(all(f["kind"] == "pack-defect" for f in body["findings"]))

    def test_extra_file_detected(self):
        _req, out, _digest = self.prepared()
        write(Path(out) / "package" / "snapshots" / "9999.blob", b"x")
        body, code = cs.verify(out, str(self.fx.config))
        self.assertEqual(code, 1)

    def test_bad_pin_refuses_before_launch(self):
        bad = self.fx.root / "bad-config.json"
        cfg = json.loads(self.fx.config.read_text())
        fake = self.fx.root / "fake_checker.py"
        write(fake, "print('should never run')\n")
        cfg["checker"] = str(fake)
        write(bad, json.dumps(cfg))
        body, code = cs.preview(self.fx.request_file(), str(bad))
        self.assertEqual((code, body["findings"][0]["code"]), (2, "pin"))


class Modes(Base):
    def test_blind_evaluator_kept_out(self):
        doc = self.fx.request(mode="controlled-experiment", scoring={
            "state": "scored", "blind": True, "evaluator_sources": [f"{BASE}/0411.colab/evidence/rubric-key.md"]})
        _req, out, _digest = self.prepared(doc)
        root = Path(out)
        self.assertTrue((root / "evaluator" / "source-manifest.json").exists())
        self.assertIn(b"expected answers", (root / "evaluator" / "snapshots" / "0001.blob").read_bytes())
        with zipfile.ZipFile(root / "prepared-colab.zip") as archive:
            blob = b"".join(archive.read(n) for n in archive.namelist())
            self.assertNotIn(b"expected answers", blob)
            self.assertFalse(any(n.startswith("evaluator") for n in archive.namelist()))
        self.assertIn("withheld from you by design", (root / "package" / "ENTRY.md").read_text(encoding="utf-8"))
        self.assertEqual(cs.verify(out, str(self.fx.config))[1], 0)
        (root / "evaluator" / "snapshots" / "0001.blob").write_bytes(b"changed key")
        self.assertEqual(cs.verify(out, str(self.fx.config))[1], 1)

    def test_blind_evaluator_overlap_refused(self):
        doc = self.fx.request(scoring={"state": "scored", "blind": True,
                                       "evaluator_sources": [f"{BASE}/0411.colab/02.md"]})
        self.refused(doc, code="evaluator-overlap")
        doc["scoring"]["evaluator_sources"] = [f"{BASE}/0411.colab/evidence/rubric-copy.md"]
        self.refused(doc, code="evaluator-overlap")  # same bytes as a candidate input

    def test_blind_rubric_text_not_allowed_in_request(self):
        # The exact request travels in the package, so a blind rubric may live only in evaluator sources.
        doc = self.fx.request(scoring={"state": "scored", "blind": True, "rubric": "SECRET", "meaning": "m",
                                       "evaluator_sources": [f"{BASE}/0411.colab/evidence/rubric-key.md"]})
        self.refused(doc, code="unknown-key")

    def test_unscored_mode(self):
        _req, out, _digest = self.prepared()
        package = Path(out) / "package"
        self.assertIn("Unscored. State the qualitative result. Do not invent a number.",
                      (package / "ENTRY.md").read_text(encoding="utf-8"))
        self.assertNotIn("## Scoring", (package / "RETURN-TEMPLATE.md").read_text(encoding="utf-8"))

    def test_scored_open_rejects_evaluator_files(self):
        doc = self.fx.request(scoring={"state": "scored", "blind": False, "rubric": "r", "meaning": "m",
                                       "evaluator_sources": [f"{BASE}/0411.colab/evidence/rubric-key.md"]})
        self.refused(doc, code="unknown-key")

    def test_scored_open_carries_rubric(self):
        doc = self.fx.request(scoring={"state": "scored", "blind": False, "rubric": "R1 names the path.",
                                       "meaning": "Counts R1 only."})
        _req, out, _digest = self.prepared(doc)
        package = Path(out) / "package"
        self.assertIn("R1 names the path.", (package / "ENTRY.md").read_text(encoding="utf-8"))
        self.assertIn("## Scoring", (package / "RETURN-TEMPLATE.md").read_text(encoding="utf-8"))


class Retention(Base):
    def test_exact_reply_and_overflow_preserved(self):
        reply = 'Ok "quoted" — keep it.\nSecond line with D:\\Git path as data.'
        doc = self.fx.request(director_replies=[
            {"id": "D01", "date": "2026-10-29", "source": "chat", "reply": reply, "status": "actual"},
            {"id": "D02", "date": "2026-10-29", "source": "fixture", "reply": "maybe", "status": "hypothetical-fixture"},
        ])
        _req, out, _digest = self.prepared(doc)
        package = Path(out) / "package"
        entry = (package / "ENTRY.md").read_text(encoding="utf-8")
        sixty = (package / "06.01.md").read_text(encoding="utf-8")
        for text in (entry, sixty):
            self.assertIn('reply: Ok "quoted" — keep it.\nreply: Second line with D:\\Git path as data.', text)
        self.assertIn("HYPOTHETICAL FIXTURE, not a Director decision", entry)
        self.assertIn("[hypothetical-fixture]", sixty)
        template = (package / "RETURN-TEMPLATE.md").read_text(encoding="utf-8")
        for heading in ("## Hostile", "## Factfind", "## Overflow", "## Unprompted", "## Director replies",
                        "## Pack and tool defects"):
            self.assertIn(heading, template)
        self.assertIn("None. This face holds supplied reasons only.", sixty)

    def test_withhold_omission_and_limit_labelled(self):
        doc = self.fx.request(
            withheld=[{"item": "history", "reason": "not needed"}],
            unavailable=[{"item": "adapter", "reason": "not built", "kind": "required-omission"},
                         {"item": "ids", "reason": "no syntax", "kind": "tool-limitation"}])
        _req, out, _digest = self.prepared(doc)
        entry = (Path(out) / "package" / "ENTRY.md").read_text(encoding="utf-8")
        self.assertIn("Withheld on purpose:\n- history: not needed", entry)
        self.assertIn("Required but unavailable (a pack gap, not a design finding):\n- adapter: not built", entry)
        self.assertIn("Tool limitations (not design findings):\n- ids: no syntax", entry)

    def test_zip_only_local_path_refused(self):
        self.refused(self.fx.request(method="Open D:\\Git\\lib-build and read it."), code="local-path")
        self.refused(self.fx.request(context="see /home/x/file"), code="local-path")
        doc = self.fx.request(method="Open D:\\Git\\lib-build and read it.")
        doc["environment"]["kind"] = "local-tools"
        self.assertEqual(preview_of(self.fx, doc)[1], 0)


class Intake(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.book_root = cls.fx.root / "bookroot"
        cls.book = cls.book_root / "00.kernel" / "00.00.10.work"
        (cls.book / "0100.band.returns").mkdir(parents=True)
        write(cls.book / "0100.band.returns" / "01.md", "# 01\nreturns door\n")
        request = cls.fx.request_file()
        digest = cs.preview(request, str(cls.fx.config))[0]["digest"]
        cls.out = cls.fx.output()
        assert cs.prepare(request, str(cls.fx.config), cls.out, digest)[1] == 0
        cls.digest = digest

    def reserve(self, submission, name, page, batch="05.01"):
        out = subprocess.run([sys.executable, "-B", str(TOOLS["helper"]), "reserve", "--book", str(self.book),
                              "--submission", submission, "--name", name, "--origin-book", BOOK,
                              "--origin-page", page, "--origin-batch", batch, "--expected-output", "notes",
                              "--submitter", "synthetic fixture", "--reviewer", "fixture reviewer",
                              "--release", "fixture only; no release"], capture_output=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        return [p.name for p in self.book.iterdir() if p.name.endswith(name)][0]

    def synthetic_return(self, tag, extra=""):
        src = self.book_root / f"src-{tag}"
        write(src / "return.md", "# Return — synthetic, labelled fixture\n\n## Answer\nfixture\n\n## Hostile\nnone\n\n"
              "## Factfind\nF01 none\n\n## Overflow\nnone\n\n## Unprompted\nnone\n\n## Director replies\nnone\n" + extra)
        write(src / "notes.txt", "synthetic notes " + tag + "\n")
        return src

    def run_intake(self, member, src):
        return cs.intake(self.out, str(self.fx.config), str(self.book), member, str(src / "return.md"),
                         str(src), ["notes.txt|notes"])

    def test_capture_replay_and_conflict(self):
        member = self.reserve("synthetic-0701-0501", "synthetic-colab-0701", "0701.desk-state")
        src = self.synthetic_return("a")
        body, code = self.run_intake(member, src)
        self.assertEqual((code, body["result"]), (0, "captured"), body)
        self.assertEqual(body["package_digest"], self.digest)
        self.assertEqual(body["investigation"], {"book": BOOK, "page": "0701.desk-state", "pass": "05.01"})
        self.assertTrue(all(body["return_headings"].values()))
        self.assertIn("not approved; not accepted; not published", body["pointer"])
        self.assertEqual([r["exit"] for r in body["runs"]], [1, 0, 0, 0])
        tree = sorted(p.name for p in (self.book / member).rglob("*"))
        again, code = self.run_intake(member, src)
        self.assertEqual((code, again["result"]), (0, "already-captured"), again)
        self.assertEqual(tree, sorted(p.name for p in (self.book / member).rglob("*")))
        write(src / "notes.txt", "changed bytes\n")
        changed, code = self.run_intake(member, src)
        self.assertEqual((code, changed["result"]), (1, "attention"), changed)
        self.assertEqual(changed["helper_capture"], "refused")
        self.assertEqual(changed["runs"][1]["exit"], 2)

    def test_wrong_target_page_origin_refused(self):
        member = self.reserve("synthetic-target-origin", "synthetic-wrong-origin", "0411.colab")
        src = self.synthetic_return("b")
        body, code = self.run_intake(member, src)
        self.assertEqual((code, body["result"]), (2, "wrong-origin"), body)
        self.assertEqual(len(body["runs"]), 1)  # only the inspector ran; no capture
        self.assertEqual(sorted(p.name for p in (self.book / member).iterdir()), ["01.md", "reservation.json"])

    def test_implementation_batch_origin_refused(self):
        member = self.reserve("synthetic-impl-origin", "synthetic-impl", "0510.colab-tools", "05.02")
        body, code = self.run_intake(member, self.synthetic_return("c"))
        self.assertEqual((code, body["result"]), (2, "wrong-origin"))

    def test_intake_needs_verified_package(self):
        member = self.reserve("synthetic-bad-package", "synthetic-bad-package", "0701.desk-state")
        body, code = cs.intake(str(self.fx.root / "no-such-out"), str(self.fx.config), str(self.book), member,
                               str(self.synthetic_return("d") / "return.md"), str(self.book_root), ["x|notes"])
        self.assertEqual((code, body["result"]), (2, "package-not-verified"))


class Cli(Base):
    def test_cli_exit_codes_and_no_traceback(self):
        script = str(LAB / "colab_support.py")
        bad = self.fx.request_file(raw="{bad")
        out = subprocess.run([sys.executable, "-B", script, "preview", "--request", bad, "--config",
                              str(self.fx.config), "--json"], capture_output=True)
        self.assertEqual(out.returncode, 2)
        self.assertNotIn(b"Traceback", out.stderr)
        self.assertEqual(json.loads(out.stdout)["result"], "invalid")
        good = self.fx.request_file()
        out = subprocess.run([sys.executable, "-B", script, "preview", "--request", good, "--config",
                              str(self.fx.config), "--json"], capture_output=True)
        self.assertEqual(out.returncode, 0, out.stderr)


if __name__ == "__main__":
    unittest.main()
