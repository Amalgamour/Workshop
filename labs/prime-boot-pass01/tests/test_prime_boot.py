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
        self.assertEqual(json.loads(show)["state"], "failed")
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
        self.assertEqual(out, "already-recorded\n")
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
        self.assertIn("prepared; not oriented (no judgement)", out)
        code, out = self.cli("judge", "--attempt", d, "--judgement", self.write_json("j0.json", self.judgement(d)), code=2)
        self.assertIn("needs checked answers", out)
        self.cli("check", "--attempt", d, "--answers", self.write_json("a.json", self.good_answers(d)), code=0)
        _, out = self.cli("show", "--attempt", d, code=0)
        self.assertIn("not oriented (no judgement)", out)
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
        _, out = self.cli("judge", "--attempt", d3, "--judgement", self.write_json("b3.json", bad), code=2)
        self.assertTrue((d3 / "30.judgement.raw").is_file() and not (d3 / "39.outcome.json").exists())

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


if __name__ == "__main__":
    unittest.main()
