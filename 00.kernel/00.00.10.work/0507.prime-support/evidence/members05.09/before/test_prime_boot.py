"""Fixture tests for prime_boot.py (0507.prime-support/05.07). Every repository is a disposable `git init` with a
local bare origin under the system temp directory; every records root is a separate temp directory outside Git.
The pinned tools are the lab files next to this lab (prime-support-pass01, book-orientation-pass01,
return-capture-pass01), run read-only. Nothing touches a shared checkout; no model is called.

  python -B -X dev tests/test_prime_boot.py -v
"""
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

LAB = Path(__file__).resolve().parents[1]
LABS = LAB.parent
TOOL = LAB / "prime_boot.py"
sys.path.insert(0, str(LAB))
import prime_boot as pb  # noqa: E402

TOOLS = {"prime_support": str(LABS / "prime-support-pass01" / "prime_support.py"),
         "check_book": str(LABS / "book-orientation-pass01" / "check_book.py"),
         "return_capture": str(LABS / "return-capture-pass01" / "return_capture.py")}
ENV = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@local", GIT_COMMITTER_NAME="fixture",
           GIT_COMMITTER_EMAIL="fixture@local", GIT_OPTIONAL_LOCKS="0", GIT_CONFIG_NOSYSTEM="1")
EM = "—"
BOOK = "00.kernel/00.00.10.work"
PAGE = f"{BOOK}/0599.fixture-lane"
ROLE = f"{BOOK}/0408.seats/01.md"
ASSIGN = f"{BOOK}/0401.goal/06.01.md"
CONTENTS = """# 01

## Pages

| Page | Faces and files |
|---|---|
| `0011.contents` | `01.001.md` |
| `0401.goal` | `06.01.md` |
| `0408.seats` | `01.md` |
| `0599.fixture-lane` | `01.md`, `05.01.md`, `05.02.md` |

Book files: `00.md`.

## Other books
Syntax: `../00.00.00.syntax/00.001.md`. Law: `../00.00.01.law/00.001.md`. Each lists what it holds.
"""


def batch(ret, review=None):
    text = (f"# 05 {EM} fixture batch\nstate: draft\n\n## Assignment\nRelease: fixture release.\n\n"
            f"## #01 {EM} Do it\nWrite out.txt.\n\n## Return {EM} fixture-builder\n{ret}\n")
    if review is not None:
        text += f"\n## Review {EM} Codex Prime\n{review}\n"
    return text


def assignment(state="released", work=f"{PAGE}/05.02.md"):
    keys = {"record": "assignment", "schema": "v1", "desk": "00.kernel", "book": BOOK, "workflow_space": "0599",
            "current_work": work, "pack": "fixture", "assignment_state": state, "waits_on": "builder",
            "next": "return", "updated": "2026-10-27"}
    return "".join(f"{k}: {v}\n" for k, v in keys.items())


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, env=ENV, check=True).stdout.decode().strip()


def tree_digest(root: Path, skip=()):
    out = {}
    for p in sorted(root.rglob("*")):
        if any(str(p).startswith(str(s)) for s in skip):
            continue
        if p.is_file():
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def writable_retry(func, path, exc):
    """Git object files are read-only on Windows; clear the flag and retry once."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pb-" + self._testMethodName[5:25] + "-"))
        self.records = Path(tempfile.mkdtemp(prefix="pb-records-"))
        self.assertFalse(pb.inside_git(self.records))
        self.repo = self.tmp / "work"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        bare = self.tmp / "work-origin.git"
        subprocess.run(["git", "init", "-q", "--bare", str(bare)], env=ENV, check=True, capture_output=True)
        git(self.repo, "remote", "add", "origin", str(bare))
        self.files = {
            f"{BOOK}/00.md": "00.00.10.work: the fixture work book; contents in 0011.contents/01.001.md.\n",
            f"{BOOK}/0011.contents/01.001.md": CONTENTS,
            ASSIGN: assignment(),
            ROLE: "# 01 seats\nPrime: draft role for a fixture exercise; not seated.\n",
            f"{PAGE}/01.md": "# 01 fixture lane\nA lane for the boot fixture.\n",
            f"{PAGE}/05.01.md": batch("Claim: builder one.\nexecution: returned\nDid: wrote it.", "Review: accepted."),
            f"{PAGE}/05.02.md": batch("Claim: builder two.\nExecution: IN PROGRESS"),
            "00.kernel/00.00.00.syntax/00.001.md": "syntax\n",
            "00.kernel/00.00.01.law/00.001.md": "law\n",
        }
        self.head = self.commit(self.files)

    def tearDown(self):
        for root in (self.tmp, self.records):
            shutil.rmtree(root, onexc=writable_retry)

    def commit(self, files, msg="c"):
        for rel, text in files.items():
            p = self.repo / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(text.encode("utf-8"))
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", msg)
        git(self.repo, "push", "-q", "origin", "main")
        return git(self.repo, "rev-parse", "HEAD")

    def registry(self, canonical=None, lanes=None, version=1, raw=None):
        reg = {"schema": "prime-support-registry", "version": version,
               "repositories": {"work": {"local": str(self.repo), "branch": "main", "remote_ref": "refs/remotes/origin/main",
                                         "worktree": "registered-paths", "history_limit": 50}},
               "lanes": lanes or [{"lane": "fixture", "project": "workshop", "owner_label": "builder", "repository": "work",
                                   "pages": [PAGE], "return_files": [], "review_sources": []}]}
        if canonical:
            reg["canonical_assignment"] = canonical
        data = raw if raw is not None else json.dumps(reg).encode("utf-8")
        path = self.tmp / f"registry-{len(list(self.tmp.glob('registry-*')))}.json"
        path.write_bytes(data)
        return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest()}

    def request(self, **over):
        req = {"schema": "prime-boot-request/1", "boot_id": "fixture-boot", "attempt": 1, "previous_attempt": None,
               "workspace": str(self.repo), "branch": "main", "commit": self.head, "role": "Prime", "model": "fixture-model",
               "book": BOOK, "role_record": ROLE, "assignment_record": ASSIGN, "registry": self.registry(),
               "tools": dict(TOOLS), "members": [], "members_book": None,
               "packet": [f"{PAGE}/05.01.md", f"{PAGE}/05.02.md"], "limits": {"max_refs": 12, "max_bytes": 131072}}
        req.update(over)
        return req

    def write_json(self, name, value):
        path = self.tmp / name
        path.write_bytes(value if isinstance(value, bytes) else json.dumps(value).encode("utf-8"))
        return path

    def cli(self, *args, code=None):
        r = subprocess.run([sys.executable, "-B", str(TOOL), *map(str, args)], capture_output=True, text=True,
                           encoding="utf-8", timeout=300)
        self.assertEqual(r.stderr, "", r.stderr)
        if code is not None:
            self.assertEqual(r.returncode, code, r.stdout)
        return r.returncode, r.stdout

    def prepare(self, req, attempt="a1", code=None):
        path = self.write_json(f"req-{attempt}.json", req)
        code_, out = self.cli("prepare", "--request", path, "--records", self.records, "--attempt", attempt, code=code)
        return self.records / attempt, code_, out

    def stage(self, attempt_dir, name):
        return json.loads((attempt_dir / name).read_text(encoding="utf-8"))

    def ref(self, attempt_dir, path):
        return next(r for r in self.stage(attempt_dir, "09.packet.json")["refs"] if r["path"] == path)

    def good_answers(self, attempt_dir, target=f"{PAGE}/05.02.md", conflicts=()):
        r = {x["path"]: x["id"] for x in self.stage(attempt_dir, "09.packet.json")["refs"]}
        page = r[f"{PAGE}/05.01.md"]
        return {"schema": "prime-boot-answers/1", "attempt_id": attempt_dir.name, "answers": {
            "O1": {"target": target, "citations": [r[target]], "conflicts_seen": list(conflicts), "text": "work next here"},
            "O2": {"fields": {"release": {"value": "Release: fixture release.", "citation": page},
                              "claim": {"value": "Claim: builder one.", "citation": page},
                              "execution": {"value": "execution: returned", "citation": page},
                              "review": {"value": "Review: accepted.", "citation": page}}, "text": "fields"},
            "O3": {"citations": [r[ROLE]], "text": "role is a draft"},
            "O4": {"citations": [r[ASSIGN]], "text": "assignment record"},
            "O5": {"none_found": True, "text": "nothing missing in this packet"},
            "O6": {"citations": [r[f"{BOOK}/00.md"]], "text": "orientation is not authority"}}}

    def judgement(self, attempt_dir, grade="pass", **over):
        qs = ["O1", "O2", "O3", "O4", "O5", "O6"]
        doc = {"schema": "prime-boot-judgement/1", "attempt_id": attempt_dir.name, "reviewer": "fixture-judge",
               "grades": {q: grade for q in qs}, "reasons": {q: "fixture" for q in qs}, "remediation": []}
        doc.update(over)
        return doc

    def run_all(self, attempt_dir, answers, judgement):
        a = self.write_json(f"ans-{attempt_dir.name}.json", answers)
        j = self.write_json(f"jud-{attempt_dir.name}.json", judgement)
        c1 = self.cli("check", "--attempt", attempt_dir, "--answers", a)
        c2 = self.cli("judge", "--attempt", attempt_dir, "--judgement", j)
        return c1, c2


class TestPrimeBoot(Fixture):
    # content and citation checks, clean path, PB-05 packet text
    def test_01_clean_boot_oriented_with_exact_committed_text(self):
        d, code, out = self.prepare(self.request(), code=0)
        self.assertIn("prepare prepared", out)
        self.assertTrue((d / "00.request.raw").is_file() and (d / "00.intent.json").is_file())
        refs = self.stage(d, "09.packet.json")["refs"]
        self.assertEqual([r["path"] for r in refs][:4],
                         [f"{BOOK}/00.md", f"{BOOK}/0011.contents/01.001.md", ROLE, ASSIGN])
        for r in refs:
            committed = subprocess.run(["git", "-C", str(self.repo), "show", f"{self.head}:{r['path']}"], capture_output=True).stdout
            self.assertEqual(r["text"].encode("utf-8"), committed)
            self.assertEqual(r["sha256"], hashlib.sha256(committed).hexdigest())
            self.assertEqual((r["kind"], r["live"], r["commit"]), ("commit-blob", "same", self.head))
        self.assertEqual(self.stage(d, "05.book.json")["checker_exit"], 0)
        self.assertEqual(self.stage(d, "06.records.json")["assignment_parse"], "v1")
        (c_code, c_out), (j_code, j_out) = self.run_all(d, self.good_answers(d), self.judgement(d))
        self.assertEqual(c_code, 0, c_out)
        self.assertEqual((j_code, self.stage(d, "39.outcome.json")["outcome"]), (0, "oriented"))
        self.assertTrue(self.stage(d, "39.outcome.json")["authority"].startswith("none"))
        self.assertIn("authority none", j_out)

    def test_02_bad_citations_and_field_values_fail_checks(self):
        d, _, _ = self.prepare(self.request(), code=0)
        ans = self.good_answers(d)
        ans["answers"]["O3"]["citations"] = ["R99"]
        ans["answers"]["O2"]["fields"]["claim"]["value"] = "Claim: someone else."
        ans["answers"]["O1"]["citations"] = [ans["answers"]["O3"]["citations"][0]]
        code, out = self.cli("check", "--attempt", d, "--answers", self.write_json("bad.json", ans), code=1)
        res = self.stage(d, "22.checks.json")["results"]
        self.assertEqual(res["O3"]["status"], "fail")
        self.assertIn("value does not occur", " ".join(res["O2"]["errors"]))
        self.assertIn("must cite a packet ref whose path is the target", " ".join(res["O1"]["errors"]))
        self.assertEqual((res["O4"]["status"], res["O5"]["status"]), ("ok", "ok"))
        self.cli("judge", "--attempt", d, "--judgement", self.write_json("j.json", self.judgement(d)), code=1)
        self.assertEqual(self.stage(d, "39.outcome.json")["outcome"], "not-oriented")

    # known conflicts must be acknowledged; attention order is advice (PB-02)
    def test_03_known_conflict_must_be_acknowledged(self):
        self.head = self.commit({ASSIGN: assignment(state="waiting", work=f"{PAGE}/05.01.md")})
        req = self.request(registry=self.registry(canonical={"repository": "work", "path": ASSIGN, "lane": "fixture"}))
        d, _, _ = self.prepare(req, code=0)
        status = self.stage(d, "07.status.json")
        self.assertTrue(any("canonical says waiting" in c for c in status["conflicts"]), status["conflicts"])
        n = len(status["conflicts"])
        self.cli("check", "--attempt", d, "--answers", self.write_json("a.json", self.good_answers(d)), code=1)
        self.assertIn("acknowledge every reported conflict", " ".join(self.stage(d, "22.checks.json")["results"]["O1"]["errors"]))
        d2, _, _ = self.prepare(dict(req, attempt=2, previous_attempt=str(d)), attempt="a2", code=0)
        self.cli("check", "--attempt", d2, "--answers", self.write_json("a2.json", self.good_answers(d2, conflicts=range(n))), code=0)

    def test_04_non_first_valid_target_and_out_of_scope_target(self):
        d, _, _ = self.prepare(self.request(), code=0)
        scope = self.stage(d, "07.status.json")["scope_paths"]
        self.assertIn(f"{PAGE}/05.02.md", scope)
        self.assertNotEqual(scope[0], f"{PAGE}/05.02.md", "the fixture should make 05.02 a non-first target")
        attention = self.stage(d, "07.status.json")["attention_advice"]
        self.cli("check", "--attempt", d, "--answers", self.write_json("a.json", self.good_answers(d)), code=0)
        d2, _, _ = self.prepare(self.request(), attempt="a2", code=0)
        bad = self.good_answers(d2)
        bad["answers"]["O1"]["target"] = "elsewhere/05.01.md"
        self.cli("check", "--attempt", d2, "--answers", self.write_json("b.json", bad), code=1)
        self.assertIn("not inside the declared scope", " ".join(self.stage(d2, "22.checks.json")["results"]["O1"]["errors"]))
        self.assertIsInstance(attention, list)

    # PB-03
    def test_05_no_missing_dependency_and_absence_evidence(self):
        d, _, _ = self.prepare(self.request(packet=[f"{PAGE}/05.01.md", f"{PAGE}/05.02.md", f"{PAGE}/05.09.md"]), code=0)
        packet = self.stage(d, "09.packet.json")
        self.assertEqual(packet["absences"], [{"id": "A01", "path": f"{PAGE}/05.09.md", "commit": self.head, "absent": True}])
        self.assertNotIn(f"{PAGE}/05.09.md", [r["path"] for r in packet["refs"]])
        ans = self.good_answers(d)
        ans["answers"]["O5"] = {"citations": ["A01"], "text": "05.09 is absent at the commit"}
        self.cli("check", "--attempt", d, "--answers", self.write_json("a.json", ans), code=0)
        d2, _, _ = self.prepare(self.request(), attempt="a2", code=0)
        none = self.good_answers(d2)
        self.cli("check", "--attempt", d2, "--answers", self.write_json("n.json", none), code=0)
        self.assertIn("note", self.stage(d2, "22.checks.json")["results"]["O5"])
        empty = self.good_answers(d2)
        d3, _, _ = self.prepare(self.request(), attempt="a3", code=0)
        empty["attempt_id"] = "a3"
        empty["answers"]["O5"] = {"citations": [], "text": "x"}
        self.cli("check", "--attempt", d3, "--answers", self.write_json("e.json", empty), code=1)

    def test_06_wrong_or_missing_tool_pin_never_launches(self):
        alt = self.tmp / "alt-ps"
        alt.mkdir()
        shutil.copy(TOOLS["prime_support"], alt / "prime_support.py")
        shutil.copy(Path(TOOLS["prime_support"]).parent / "clerk_adapter.py", alt / "clerk_adapter.py")
        with open(alt / "clerk_adapter.py", "ab") as h:
            h.write(b"\n# drift\n")
        d, code, out = self.prepare(self.request(tools=dict(TOOLS, prime_support=str(alt / "prime_support.py"))), code=2)
        t = self.stage(d, "03.tools.json")
        self.assertEqual(t["status"], "failed")
        self.assertIn("clerk_adapter", t["reason"])
        self.assertFalse((d / "04.git.json").exists())
        self.assertEqual(self.stage(d, "19.prepare-outcome.json")["stage"], "tools")
        d2, _, _ = self.prepare(self.request(tools=dict(TOOLS, check_book=str(self.tmp / "absent.py"))), attempt="a2", code=2)
        self.assertIn("check_book None", self.stage(d2, "03.tools.json")["reason"])
        # a direct launch with a wrong pin raises before any subprocess
        with mock.patch.object(pb.subprocess, "run") as run:
            with self.assertRaises(pb.StageFailure):
                pb.run_tool(TOOLS["check_book"], "0" * 64, ["--help"])
            run.assert_not_called()

    # PB-04
    def test_07_dirty_bytes_are_observed_apart_from_committed_bytes(self):
        page = self.repo / PAGE / "05.02.md"
        committed = page.read_bytes()
        page.write_bytes(committed + b"Did: uncommitted line.\n")
        (self.repo / PAGE / "05.03.md").write_bytes(b"untracked\n")
        d, _, _ = self.prepare(self.request(), code=0)
        ref = self.ref(d, f"{PAGE}/05.02.md")
        self.assertEqual(ref["text"].encode("utf-8"), committed)
        self.assertEqual(ref["live"], "differs")
        self.assertEqual(ref["live_sha256"], hashlib.sha256(page.read_bytes()).hexdigest())
        self.assertNotIn("uncommitted line", json.dumps(self.stage(d, "09.packet.json")))
        dirty = self.stage(d, "04.git.json")["dirty_paths"]
        self.assertTrue(any("05.02.md" in p for p in dirty) and any("05.03.md" in p for p in dirty), dirty)
        page.unlink()
        d2, _, _ = self.prepare(self.request(), attempt="a2", code=0)
        self.assertEqual(self.ref(d2, f"{PAGE}/05.02.md")["live"], "absent")

    def test_08_head_or_ref_change(self):
        old = self.head
        self.commit({f"{PAGE}/01.md": "# 01 fixture lane\nchanged\n"})
        d, _, _ = self.prepare(self.request(commit=old), code=0)
        g = self.stage(d, "04.git.json")
        self.assertEqual((g["requested_commit"], g["head_is_commit"], g["branch_is_commit"]), (old, False, False))
        self.assertEqual(self.ref(d, ASSIGN)["live"], "same")
        # a change during preparation: identities differ at the stability re-read
        req_path = self.write_json("req-s.json", self.request())
        real = pb.identities
        calls = []

        def moving(req):
            ids = real(req)
            calls.append(1)
            if len(calls) > 2:
                ids = dict(ids, head="f" * 40)
            return ids

        with mock.patch.object(pb, "identities", moving), mock.patch.object(sys, "stdout", new=io.StringIO()):
            code = pb.prepare(str(req_path), str(self.records), "s1")
        self.assertEqual(code, 1)
        st = self.stage(self.records / "s1", "10.stability.json")
        self.assertEqual((st["stable"], st["changed"]), (False, ["head"]))
        self.assertEqual(self.stage(self.records / "s1", "19.prepare-outcome.json")["status"], "partial")
        s1 = self.records / "s1"
        self.run_all(s1, self.good_answers(s1), self.judgement(s1))
        self.assertNotEqual(self.stage(s1, "39.outcome.json")["outcome"], "oriented")
        d3, code3, _ = self.prepare(self.request(commit="e" * 40), attempt="a3", code=2)
        self.assertIn("does not exist", self.stage(d3, "04.git.json")["reason"])

    def test_09_packet_overflow_is_recorded_not_truncated(self):
        d, code, out = self.prepare(self.request(limits={"max_refs": 3, "max_bytes": 131072}), code=1)
        p = self.stage(d, "09.packet.json")
        self.assertEqual(len(p["refs"]), 3)
        self.assertEqual([o["reason"] for o in p["omitted"]], ["max_refs reached"] * 3)
        self.assertTrue(all("text" not in o and len(o["sha256"]) == 64 for o in p["omitted"]))
        self.assertEqual(self.stage(d, "19.prepare-outcome.json")["status"], "partial")
        d2, _, _ = self.prepare(self.request(limits={"max_refs": 12, "max_bytes": 200}), attempt="a2", code=1)
        p2 = self.stage(d2, "09.packet.json")
        self.assertLessEqual(p2["raw_bytes"], 200)
        self.assertTrue(any(o["reason"] == "max_bytes would be exceeded" for o in p2["omitted"]))
        for r in p2["refs"]:
            self.assertEqual(hashlib.sha256(r["text"].encode("utf-8")).hexdigest(), r["sha256"])
        self.run_all(d2, {"x": 1}, self.judgement(d2))
        self.assertNotEqual(self.stage(d2, "39.outcome.json")["outcome"], "oriented")
        for lim in ({"max_refs": 13, "max_bytes": 1}, {"max_refs": 1, "max_bytes": 131073}, {"max_refs": True, "max_bytes": 1}):
            d3, _, _ = self.prepare(self.request(limits=lim), attempt=f"l{lim['max_refs']}{lim['max_bytes']}", code=2)
            self.assertEqual(self.stage(d3, "01.request.json")["status"], "failed")

    def test_10_malformed_or_duplicate_inputs(self):
        cases = {
            "dup": b'{"schema": "prime-boot-request/1", "schema": "prime-boot-request/1"}',
            "nan": b'{"attempt": NaN}',
            "notjson": b"{not json",
            "bom": b"\xef\xbb\xbf{}",
            "extra": json.dumps(dict(self.request(), extra=1)).encode(),
            "duppacket": json.dumps(self.request(packet=[f"{PAGE}/05.01.md", f"{PAGE}/05.01.md"])).encode(),
            "escape": json.dumps(self.request(packet=["../outside.md"])).encode(),
            "shortcommit": json.dumps(self.request(commit=self.head[:12])).encode(),
            "relreg": json.dumps(self.request(registry={"path": "registry.json", "sha256": "0" * 64})).encode(),
        }
        for name, raw in cases.items():
            d, code, out = self.prepare(raw, attempt=name, code=2)
            self.assertEqual((d / "00.request.raw").read_bytes(), raw, name)
            self.assertEqual(self.stage(d, "01.request.json")["status"], "failed", name)
            self.assertEqual(self.stage(d, "19.prepare-outcome.json")["stage"], "request", name)
        reg = self.registry(raw=b'{"schema": "prime-support-registry", "version": 1, "version": 1}')
        d, _, _ = self.prepare(self.request(registry=reg), attempt="dupreg", code=2)
        self.assertIn("duplicate key", self.stage(d, "07.status.json")["reason"])
        d, _, _ = self.prepare(self.request(registry=dict(self.registry(), sha256="1" * 64)), attempt="regsha", code=2)
        self.assertIn("do not match", self.stage(d, "07.status.json")["reason"])
        d, _, _ = self.prepare(self.request(), attempt="good", code=0)
        dup = b'{"schema": "prime-boot-answers/1", "attempt_id": "good", "attempt_id": "good", "answers": {}}'
        self.cli("check", "--attempt", d, "--answers", self.write_json("dup.json", dup), code=1)
        self.assertIn("duplicate key", self.stage(d, "22.checks.json")["reason"])
        self.assertFalse((d / "21.answers.json").exists())

    def test_11_invalid_linked_or_occupied_destinations(self):
        req = self.write_json("r.json", self.request())
        inside = self.repo / "records"
        inside.mkdir()
        for root in (inside, self.tmp / "missing", Path("relative-records")):
            code, out = self.cli("prepare", "--request", req, "--records", root, "--attempt", "x", code=2)
            self.assertIn("record store unusable", out)
            self.assertIn("nothing was recorded", out)
        self.assertEqual(list(inside.iterdir()), [])
        self.cli("prepare", "--request", req, "--records", self.records, "--attempt", "../up", code=2)
        self.prepare(self.request(), attempt="occ", code=0)
        before = tree_digest(self.records / "occ")
        code, out = self.cli("prepare", "--request", req, "--records", self.records, "--attempt", "occ", code=2)
        self.assertIn("already exists", out)
        self.assertEqual(tree_digest(self.records / "occ"), before)
        d, _, _ = self.prepare(self.request(attempt=2, previous_attempt=str(self.tmp / "nope")), attempt="l1", code=2)
        self.assertEqual(self.stage(d, "02.links.json")["status"], "failed")
        d, _, _ = self.prepare(self.request(attempt=1, previous_attempt=str(self.records / "occ")), attempt="l2", code=2)
        self.assertIn("does not follow", self.stage(d, "02.links.json")["reason"])

    # PB-01
    def test_12_failed_preparation_is_kept_and_a_retry_links_it(self):
        d, code, out = self.prepare(self.request(book="00.kernel/absent.book"), code=2)
        self.assertIn("prepare failed at book", out)
        names = sorted(p.name for p in d.iterdir())
        self.assertEqual(names, ["00.intent.json", "00.request.raw", "01.request.json", "02.links.json", "03.tools.json",
                                 "04.git.json", "05.book.json", "19.prepare-outcome.json"])
        _, show = self.cli("show", "--attempt", d, "--json", code=0)
        self.assertEqual((json.loads(show)["state"], json.loads(show)["stage"]), ("failed at book; not oriented", "prepare-failed"))
        code, out = self.cli("check", "--attempt", d, "--answers", self.write_json("a.json", {}), code=2)
        self.assertIn("nothing to check", out)
        before = tree_digest(d)
        d2, _, _ = self.prepare(self.request(attempt=2, previous_attempt=str(d)), attempt="a2", code=0)
        link = self.stage(d2, "02.links.json")
        self.assertEqual((link["previous_attempt_id"], link["previous_attempt_number"]), ("a1", 1))
        self.assertEqual(tree_digest(d), before)

    def test_13_stage_interruption_is_retained(self):
        req_path = self.write_json("req-i.json", self.request())
        with mock.patch.object(pb, "stage_status", side_effect=KeyboardInterrupt), \
                mock.patch.object(sys, "stdout", new=io.StringIO()):
            with self.assertRaises(KeyboardInterrupt):
                pb.prepare(str(req_path), str(self.records), "i1")
        d = self.records / "i1"
        self.assertTrue((d / "06.records.json").is_file())
        self.assertFalse((d / "07.status.json").exists() or (d / "19.prepare-outcome.json").exists())
        _, out = self.cli("show", "--attempt", d, code=0)
        self.assertIn("interrupted after 06.records.json; not oriented", out)
        self.cli("check", "--attempt", d, "--answers", self.write_json("a.json", {}), code=2)

    def test_14_immutable_retry_and_conflict(self):
        d, _, _ = self.prepare(self.request(), code=0)
        a = self.write_json("a.json", self.good_answers(d))
        self.cli("check", "--attempt", d, "--answers", a, code=0)
        before = tree_digest(d)
        _, out = self.cli("check", "--attempt", d, "--answers", a, code=0)
        self.assertEqual(out, "already-recorded: checks ok\n")
        other = self.good_answers(d)
        other["answers"]["O1"]["text"] = "different"
        _, out = self.cli("check", "--attempt", d, "--answers", self.write_json("b.json", other), code=2)
        self.assertIn("conflict", out)
        self.assertEqual(tree_digest(d), before)
        j = self.write_json("j.json", self.judgement(d))
        self.cli("judge", "--attempt", d, "--judgement", j, code=0)
        self.cli("judge", "--attempt", d, "--judgement", j, code=0)
        _, out = self.cli("judge", "--attempt", d, "--judgement", self.write_json("k.json", self.judgement(d, grade="gap")), code=2)
        self.assertIn("conflict", out)
        self.assertEqual(self.stage(d, "39.outcome.json")["outcome"], "oriented")

    def test_15_no_orientation_without_judgement_and_grades_shape_outcome(self):
        d, _, _ = self.prepare(self.request(), code=0)
        _, out = self.cli("show", "--attempt", d, code=0)
        self.assertIn("state prepared; awaiting answers; not oriented", out)
        code, out = self.cli("judge", "--attempt", d, "--judgement", self.write_json("j0.json", self.judgement(d)), code=2)
        self.assertIn("needs checked answers", out)
        self.cli("check", "--attempt", d, "--answers", self.write_json("a.json", self.good_answers(d)), code=0)
        _, out = self.cli("show", "--attempt", d, code=0)
        self.assertIn("state prepared; checks ok; awaiting judgement; not oriented", out)
        self.cli("judge", "--attempt", d, "--judgement", self.write_json("j.json", self.judgement(
            d, grade="gap", remediation=[{"kind": "question", "detail": "which lane owns 05.02?"}])), code=1)
        out39 = self.stage(d, "39.outcome.json")
        self.assertEqual((out39["outcome"], out39["dependent_execution"]), ("partial", "blocked"))
        d2, _, _ = self.prepare(self.request(attempt=2, previous_attempt=str(d)), attempt="a2", code=0)
        self.run_all(d2, self.good_answers(d2), self.judgement(d2, grade="wrong"))
        self.assertEqual(self.stage(d2, "39.outcome.json")["outcome"], "not-oriented")
        d3, _, _ = self.prepare(self.request(attempt=3, previous_attempt=str(d2)), attempt="a3", code=0)
        self.cli("check", "--attempt", d3, "--answers", self.write_json("a3.json", self.good_answers(d3)), code=0)
        bad = self.judgement(d3)
        bad["grades"]["O1"] = "excellent"
        # 05.08 (PB-06): an invalid grade is now a recorded failure, not an unrecorded refusal
        _, out = self.cli("judge", "--attempt", d3, "--judgement", self.write_json("b3.json", bad), code=1)
        self.assertTrue((d3 / "30.judgement.raw").is_file())
        self.assertEqual((self.stage(d3, "31.judgement.json")["status"], self.stage(d3, "39.outcome.json")["outcome"],
                          self.stage(d3, "39.outcome.json")["judgement"]), ("failed", "not-oriented", "invalid"))

    def test_16_clerk_jobs_unsupported(self):
        lanes = [{"lane": "fixture", "project": "workshop", "owner_label": "builder", "repository": "work", "pages": [PAGE],
                  "return_files": [], "review_sources": [],
                  "clerk_jobs": [{"store": str(self.tmp / "store"), "job_id": "job1", "return_id": "r1"}]}]
        d, _, out = self.prepare(self.request(registry=self.registry(lanes=lanes, version=2)), code=2)
        self.assertIn("unsupported", self.stage(d, "07.status.json")["reason"])

    def test_17_members_integrity_only(self):
        d, _, _ = self.prepare(self.request(members=["0198.not-there"], members_book=str(self.tmp)), code=0)
        m = self.stage(d, "08.members.json")["members"][0]
        self.assertEqual((m["integrity"], m["structured"]), ("not verified", "unavailable: return_inspect.py is unaccepted"))
        self.assertNotEqual(m["verify_exit"], 0)
        self.assertNotIn("return_inspect", TOOL.read_text(encoding="utf-8").replace("return_inspect.py is unaccepted", ""))

    def test_18_sources_and_git_metadata_unchanged_no_writes_outside_records(self):
        (self.repo / PAGE / "05.02.md").write_bytes(b"dirty\n")
        snap = lambda: (git(self.repo, "rev-parse", "HEAD"), git(self.repo, "for-each-ref"),
                        git(self.repo, "status", "--porcelain=v1", "-uall"), tree_digest(self.repo),
                        tree_digest(LABS, skip=[LABS / "book-orientation-pass01" / "scratch"]))
        before = snap()
        tmp_before = sorted(p.name for p in self.tmp.iterdir())
        d, _, _ = self.prepare(self.request(), code=0)
        self.run_all(d, self.good_answers(d), self.judgement(d))
        self.cli("show", "--attempt", d, "--json", code=0)
        tmp_after = sorted(p.name for p in self.tmp.iterdir())
        self.assertEqual(snap(), before)
        self.assertEqual(set(tmp_after) - set(tmp_before), {"registry-0.json", "req-a1.json", "ans-a1.json", "jud-a1.json"})
        self.assertEqual([p.name for p in self.records.iterdir()], ["a1"])
        self.assertFalse(any(p.suffix == ".pyc" for p in LAB.rglob("*")))


# ---------- 05.08: PB-06 nested validation, PB-07 stage-aware replay ----------

def set_path(doc, path, value):
    target = doc
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return doc


ANSWER_VARIANTS = [  # (path under answers, wrong-shaped value)
    *[(("O1", "citations"), v) for v in (None, 5, "R01", {}, [None], [["R01"]], [{}])],
    *[(("O1", "target"), v) for v in (None, 1, [], {})],
    *[(("O1", "conflicts_seen"), v) for v in (None, "0", {}, [True], [None], [0.0], [[0]])],
    *[(("O1", "text"), v) for v in (None, 1, [], {})],
    *[(("O2", "fields"), v) for v in (None, "x", [], {"release": {}})],
    *[(("O2", "fields", "claim"), v) for v in (None, "x", [], {})],
    *[(("O2", "fields", "claim", "value"), v) for v in (None, 1, [], {})],
    *[(("O2", "fields", "claim", "citation"), v) for v in (None, 1, [], {})],
    *[(("O3", "citations"), v) for v in (None, "R01", [None], [{}])],
    *[(("O4",), v) for v in (None, "x", [], 1)],
    *[(("O5",), v) for v in (None, [], {"none_found": None, "text": "x"}, {"none_found": True, "text": None},
                             {"citations": None, "text": "x"}, {"citations": [{}], "text": "x"})],
    *[(("O6", "text"), v) for v in (None, [], {})],
]
ENVELOPE_VARIANTS = [b"null", b"[]", b'"answers"', b"1", b'{"schema": "prime-boot-answers/1"}',
                     b'{"schema": "prime-boot-answers/1", "attempt_id": "%s", "answers": null}',
                     b'{"schema": "prime-boot-answers/1", "attempt_id": "%s", "answers": []}',
                     b'{"schema": "prime-boot-answers/1", "attempt_id": ["x"], "answers": {}}',
                     b'{"schema": {}, "attempt_id": "%s", "answers": {}}']
JUDGEMENT_VARIANTS = [
    *[(("grades", "O1"), v) for v in ({}, [], None, 1, "excellent", ["pass"])],
    *[(("grades",), v) for v in (None, [], "pass", {"O1": "pass"})],
    *[(("reasons", "O2"), v) for v in (None, {}, [], 1)],
    *[(("reasons",), v) for v in (None, [])],
    *[(("reviewer",), v) for v in (None, {}, [], 1, "not a label!")],
    *[(("remediation",), v) for v in (None, {}, "x", [None], [{"kind": {}, "detail": "x"}],
                                      [{"kind": "question", "detail": None}], [{"kind": "other", "detail": "x"}],
                                      [{"kind": "question"}])],
    *[(("attempt_id",), v) for v in (None, [], {})],
]
JUDGEMENT_RAW_VARIANTS = [b"null", b"[]", b"{not json", b'{"schema": "a", "schema": "b"}', b'{"grades": NaN}']


class TestValidationAndReplay(Fixture):
    def setUp(self):
        super().setUp()
        self.base, _, _ = self.prepare(self.request(), attempt="base", code=0)

    def clone(self, name, checked=False):
        """A copy of one real prepared attempt; for judge variants, checked with good answers first."""
        d = self.records / name
        shutil.copytree(self.base, d)
        if checked:
            ans = self.good_answers(d)
            self.cli("check", "--attempt", d, "--answers", self.write_json(f"ok-{name}.json", ans), code=0)
        return d

    def show_json(self, d):
        return json.loads(self.cli("show", "--attempt", d, "--json", code=0)[1])

    def test_19_exact_prime_probes(self):
        d = self.clone("probe1")
        ans = self.good_answers(d)
        ans["answers"]["O1"]["citations"] = None
        f = self.write_json("probe1.json", ans)
        code, out = self.cli("check", "--attempt", d, "--answers", f, code=1)
        self.assertIn("O1 fail: O1 citations must be a list of strings", out)
        self.assertEqual((d / "20.answers.raw").read_bytes(), f.read_bytes())
        self.assertEqual(self.stage(d, "22.checks.json")["status"], "failed")
        self.assertEqual(self.cli("check", "--attempt", d, "--answers", f, code=1)[1], "already-recorded: checks failed\n")
        self.assertEqual(self.show_json(d)["state"], "prepared; checks failed; awaiting judgement; not oriented")
        d2 = self.clone("probe2", checked=True)
        j = self.judgement(d2)
        j["grades"]["O1"] = {}
        g = self.write_json("probe2.json", j)
        _, out = self.cli("judge", "--attempt", d2, "--judgement", g, code=1)
        self.assertIn("judgement invalid: judgement grades.O1 must be one of pass, gap, wrong", out)
        self.assertEqual((d2 / "30.judgement.raw").read_bytes(), g.read_bytes())
        self.assertEqual(self.stage(d2, "39.outcome.json")["outcome"], "not-oriented")
        self.assertNotIn("grades", self.stage(d2, "39.outcome.json"))
        _, out = self.cli("judge", "--attempt", d2, "--judgement", g, code=1)
        self.assertEqual(out.splitlines()[0], "already-recorded: outcome not-oriented")
        self.assertEqual(self.show_json(d2)["state"], "not-oriented; judgement invalid")

    def test_20_nested_answer_variants_fail_in_a_controlled_way(self):
        for i, (path, value) in enumerate(ANSWER_VARIANTS):
            with self.subTest(path=path, value=value):
                d = self.clone(f"av{i:02d}")
                ans = self.good_answers(d)
                set_path(ans["answers"], path, value)
                f = self.write_json(f"av{i:02d}.json", ans)
                self.cli("check", "--attempt", d, "--answers", f, code=1)
                self.assertEqual((d / "20.answers.raw").read_bytes(), f.read_bytes())
                checks = self.stage(d, "22.checks.json")
                self.assertEqual(checks["status"], "failed")
                self.assertEqual(checks["results"][path[0]]["status"], "fail")
                self.assertEqual(checks["results"][path[0]].get("phase"), "shape")
                before = tree_digest(d)
                self.cli("check", "--attempt", d, "--answers", f, code=1)
                self.assertEqual(tree_digest(d), before)
                self.assertEqual(self.show_json(d)["stage"], "checked")
                self.cli("judge", "--attempt", d, "--judgement", self.write_json(f"aj{i:02d}.json", self.judgement(d)), code=1)
                self.assertEqual(self.stage(d, "39.outcome.json")["outcome"], "not-oriented")

    def test_21_answer_envelope_variants(self):
        for i, raw in enumerate(ENVELOPE_VARIANTS):
            with self.subTest(raw=raw):
                d = self.clone(f"ev{i:02d}")
                data = raw.replace(b"%s", d.name.encode()) if b"%s" in raw else raw
                f = self.write_json(f"ev{i:02d}.json", data)
                _, out = self.cli("check", "--attempt", d, "--answers", f, code=1)
                self.assertTrue(out.startswith("checks failed: "), out)
                self.assertEqual((d / "20.answers.raw").read_bytes(), data)
                self.assertEqual(self.stage(d, "22.checks.json")["status"], "failed")
                self.assertFalse((d / "21.answers.json").exists())
                self.assertEqual(self.cli("check", "--attempt", d, "--answers", f, code=1)[1], "already-recorded: checks failed\n")

    def test_22_judgement_variants_record_invalid_and_never_orient(self):
        variants = [(p, v, None) for p, v in JUDGEMENT_VARIANTS] + [(None, None, raw) for raw in JUDGEMENT_RAW_VARIANTS]
        for i, (path, value, raw) in enumerate(variants):
            with self.subTest(path=path, value=value, raw=raw):
                d = self.clone(f"jv{i:02d}", checked=True)
                data = raw if raw is not None else json.dumps(set_path(self.judgement(d), path, value)).encode()
                g = self.write_json(f"jv{i:02d}.json", data)
                _, out = self.cli("judge", "--attempt", d, "--judgement", g, code=1)
                self.assertTrue(out.startswith("judgement invalid: "), out)
                self.assertEqual((d / "30.judgement.raw").read_bytes(), data)
                self.assertEqual(self.stage(d, "31.judgement.json")["status"], "failed")
                outcome = self.stage(d, "39.outcome.json")
                self.assertEqual((outcome["outcome"], outcome["judgement"], outcome["dependent_execution"]),
                                 ("not-oriented", "invalid", "blocked"))
                self.assertTrue(outcome["authority"].startswith("none"))
                before = tree_digest(d)
                self.assertEqual(self.cli("judge", "--attempt", d, "--judgement", g, code=1)[1].splitlines()[0],
                                 "already-recorded: outcome not-oriented")
                self.assertEqual(tree_digest(d), before)
                self.cli("judge", "--attempt", d, "--judgement", self.write_json(f"jg{i:02d}.json", self.judgement(d)), code=2)
                self.assertEqual(tree_digest(d), before)

    def test_23_inspected_registry_and_report_shapes(self):
        cases = {"list": b"[]", "scalar": b"7", "lanes-object": b'{"lanes": {}}', "lanes-scalar": b'{"lanes": 3}',
                 "lane-scalar": b'{"lanes": [1]}', "lane-list": b'{"lanes": [[]]}',
                 "clerk-jobs-object": b'{"lanes": [{"clerk_jobs": {}}]}', "clerk-jobs-string": b'{"lanes": [{"clerk_jobs": "j"}]}'}
        for name, raw in cases.items():
            with self.subTest(case=name):
                d, _, out = self.prepare(self.request(registry=self.registry(raw=raw)), attempt=f"rg-{name}", code=2)
                st = self.stage(d, "07.status.json")
                self.assertEqual(st["status"], "failed")
                self.assertIn("registry shape", st["reason"])
                self.assertEqual(self.show_json(d)["state"], "failed at status; not oriented")
        real = pb.run_tool
        reports = {"status-list": ("prime_support", "[]"), "status-files": ("prime_support", '{"lanes": [{"files": [1]}]}'),
                   "status-path": ("prime_support", '{"lanes": [{"files": [{"path": 1}]}]}'),
                   "status-conflicts": ("prime_support", '{"lanes": [], "conflicts": [{}]}'),
                   "status-attention": ("prime_support", '{"lanes": [], "attention": {}}'),
                   "book-findings": ("check_book", '{"findings": {}}'), "book-finding": ("check_book", '{"findings": [1]}')}
        for name, (tool, stdout) in reports.items():
            with self.subTest(report=name):
                def fake(path, pin, args, tool=tool, stdout=stdout):
                    if pin == pb.PINS[tool]:
                        return {"argv": [path, *args], "exit": 0, "stdout": stdout, "stderr": ""}
                    return real(path, pin, args)
                req = self.write_json(f"req-{name}.json", self.request())
                with mock.patch.object(pb, "run_tool", fake), mock.patch.object(sys, "stdout", new=io.StringIO()):
                    self.assertEqual(pb.prepare(str(req), str(self.records), f"rp-{name}"), 2)
                stage = "07.status.json" if tool == "prime_support" else "05.book.json"
                rec = self.stage(self.records / f"rp-{name}", stage)
                self.assertEqual(rec["status"], "failed")
                self.assertIn("shape", rec["reason"])

    def interrupt(self, name, fn, command, path):
        d = self.records / name
        with mock.patch.object(pb, fn, side_effect=KeyboardInterrupt), mock.patch.object(sys, "stdout", new=io.StringIO()):
            with self.assertRaises(KeyboardInterrupt):
                (pb.check if command == "check" else pb.judge)(str(d), str(path))
        return d

    def test_24_missing_or_partial_check_record_replays_as_incomplete(self):
        d, _, _ = self.prepare(self.request(), attempt="ci", code=0)  # a real attempt, so the later link names it
        good = self.write_json("ci.json", self.good_answers(d))
        self.interrupt("ci", "check_answers", "check", good)
        self.assertTrue((d / "20.answers.raw").is_file() and not (d / "22.checks.json").exists())
        before = tree_digest(d)
        _, out = self.cli("check", "--attempt", d, "--answers", good, code=3)
        self.assertIn("incomplete: answers recorded without a check result", out)
        self.assertIn("start a new linked attempt", out)
        self.assertEqual(tree_digest(d), before)
        other = self.good_answers(d)
        other["answers"]["O6"]["text"] = "other"
        self.assertIn("conflict", self.cli("check", "--attempt", d, "--answers", self.write_json("ci2.json", other), code=2)[1])
        self.assertIn("check stage incomplete", self.cli("judge", "--attempt", d, "--judgement",
                                                         self.write_json("cij.json", self.judgement(d)), code=2)[1])
        state = self.show_json(d)
        self.assertEqual((state["stage"], state["complete"]), ("check-incomplete", False))
        self.assertIn("not oriented", state["state"])
        self.assertEqual(tree_digest(d), before)
        for name, partial in {"truncated": b'{"status": "ok"', "unknown-status": b'{"status": "maybe"}', "list": b"[]"}.items():
            with self.subTest(partial=name):
                p = self.clone(f"cp-{name}")
                f = self.write_json(f"cp-{name}.json", self.good_answers(p))
                (p / "20.answers.raw").write_bytes(f.read_bytes())
                (p / "22.checks.json").write_bytes(partial)
                snap = tree_digest(p)
                self.cli("check", "--attempt", p, "--answers", f, code=3)
                self.assertEqual(tree_digest(p), snap)
                self.assertEqual(self.show_json(p)["stage"], "check-incomplete")
                self.cli("judge", "--attempt", p, "--judgement", self.write_json(f"cpj-{name}.json", self.judgement(p)), code=2)
                self.assertFalse((p / "39.outcome.json").exists())
        d2, _, _ = self.prepare(self.request(attempt=2, previous_attempt=str(d)), attempt="ci-next", code=0)
        self.assertEqual(self.stage(d2, "02.links.json")["previous_attempt_id"], "ci")

    def test_25_missing_or_partial_outcome_never_orients_from_raw_bytes(self):
        d = self.clone("ji", checked=True)
        passing = self.write_json("ji.json", self.judgement(d))
        self.interrupt("ji", "judgement_problem", "judge", passing)
        self.assertTrue((d / "30.judgement.raw").is_file())
        self.assertFalse((d / "31.judgement.json").exists() or (d / "39.outcome.json").exists())
        before = tree_digest(d)
        _, out = self.cli("judge", "--attempt", d, "--judgement", passing, code=3)
        self.assertIn("incomplete: judgement recorded without an outcome", out)
        self.assertNotIn("oriented\n", out)
        self.assertEqual(tree_digest(d), before)
        self.assertIn("conflict", self.cli("judge", "--attempt", d, "--judgement",
                                           self.write_json("ji2.json", self.judgement(d, grade="gap")), code=2)[1])
        state = self.show_json(d)
        self.assertEqual((state["stage"], state["complete"]), ("judgement-incomplete", False))
        self.assertNotIn("oriented;", state["state"].replace("not oriented", ""))
        self.assertEqual(tree_digest(d), before)
        for name, partial in {"truncated": b'{"outcome": "oriented"', "no-outcome": b'{"authority": "none"}', "list": b"[]"}.items():
            with self.subTest(partial=name):
                p = self.clone(f"jp-{name}", checked=True)
                g = self.write_json(f"jp-{name}.json", self.judgement(p))
                (p / "30.judgement.raw").write_bytes(g.read_bytes())
                (p / "39.outcome.json").write_bytes(partial)
                snap = tree_digest(p)
                _, out = self.cli("judge", "--attempt", p, "--judgement", g, code=3)
                self.assertTrue(out.startswith("incomplete"), out)
                self.assertEqual(tree_digest(p), snap)
                self.assertEqual(self.show_json(p)["stage"], "judgement-incomplete")

    def test_26_completed_replays_report_their_recorded_state(self):
        d = self.clone("ok", checked=True)
        g = self.write_json("ok-j.json", self.judgement(d))
        self.cli("judge", "--attempt", d, "--judgement", g, code=0)
        before = tree_digest(d)
        _, out = self.cli("judge", "--attempt", d, "--judgement", g, code=0)
        self.assertEqual(out.splitlines()[0], "already-recorded: outcome oriented")
        a = self.write_json("ok-a.json", self.good_answers(d))
        self.assertEqual(self.cli("check", "--attempt", d, "--answers", a, code=0)[1], "already-recorded: checks ok\n")
        self.assertEqual(tree_digest(d), before)
        self.assertEqual((self.show_json(d)["stage"], self.show_json(d)["state"]), ("outcome", "oriented"))
        p = self.clone("gap", checked=True)
        gg = self.write_json("gap-j.json", self.judgement(p, grade="gap"))
        self.cli("judge", "--attempt", p, "--judgement", gg, code=1)
        self.assertEqual(self.cli("judge", "--attempt", p, "--judgement", gg, code=1)[1].splitlines()[0],
                         "already-recorded: outcome partial")


if __name__ == "__main__":
    unittest.main()
