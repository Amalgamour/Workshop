"""Fixture tests for prime_support.py (0507.prime-support/05.02). Every repository is a disposable
`git init` under the system temp directory, with a local bare origin. Nothing touches a shared checkout.

  python -B -X dev tests/test_prime_support.py -v
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
TOOL = LAB / "prime_support.py"
sys.path.insert(0, str(LAB))
import prime_support as ps  # noqa: E402

ENV = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@local", GIT_COMMITTER_NAME="fixture",
           GIT_COMMITTER_EMAIL="fixture@local", GIT_OPTIONAL_LOCKS="0", GIT_CONFIG_NOSYSTEM="1")
EM = "—"
PAGE = "00.kernel/00.00.10.work/0599.fixture-lane"


def batch(ret: str, review: str | None = None, extra: str = "") -> str:
    text = (f"# 05 {EM} fixture batch\nstate: draft; awaiting Director release\n\n## Assignment\nRelease: fixture.\n"
            f"{extra}\n## #01 {EM} Do it\nWrite out.txt.\n\n## Return {EM} fixture-builder\n{ret}\n")
    if review is not None:
        text += f"\n## Review {EM} Codex Prime\n{review}\n"
    return text


def prefix(text: str) -> str:
    return ps.parse_source(text.encode("utf-8"), "page-return")["revision_id"]


def by_id(findings: dict) -> dict:
    """05.03: finding keys are scoped as '<target path>#<ID>'. Fixtures here use one return per lane."""
    return {v["id"]: v for v in findings.values()}


def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, env=ENV, check=check).stdout.decode().strip()


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="ps-" + self._testMethodName[:20] + "-"))
        self.repo = self.make_repo("work")
        self.store = self.tmp / "intake-store"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def make_repo(self, name, branch="main"):
        repo = self.tmp / name
        repo.mkdir()
        git(repo, "init", "-q", "-b", branch)
        bare = self.tmp / f"{name}-origin.git"
        subprocess.run(["git", "init", "-q", "--bare", str(bare)], env=ENV, check=True, capture_output=True)
        git(repo, "remote", "add", "origin", str(bare))
        return repo

    def write(self, repo, rel, text):
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))

    def commit(self, repo, files, msg="c", push=True, branch="main"):
        for rel, text in files.items():
            self.write(repo, rel, text)
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", msg)
        if push:
            git(repo, "push", "-q", "origin", branch)
        return git(repo, "rev-parse", "HEAD")

    def registry(self, lanes=None, canonical=None, repos=None, **extra):
        reg = {"schema": "prime-support-registry", "version": 1,
               "repositories": repos or {"work": {"local": str(self.repo), "branch": "main",
                                                  "remote_ref": "refs/remotes/origin/main",
                                                  "worktree": "registered-paths", "history_limit": 50}},
               "lanes": lanes or [{"lane": "fixture", "project": "workshop", "owner_label": "builder", "repository": "work",
                                   "pages": [PAGE], "return_files": [], "review_sources": []}]}
        if canonical:
            reg["canonical_assignment"] = canonical
        reg.update(extra)
        path = self.tmp / f"registry-{len(list(self.tmp.glob('registry-*')))}.json"
        path.write_text(json.dumps(reg), encoding="utf-8")
        return path

    def run_tool(self, *args, code=None):
        r = subprocess.run([sys.executable, "-B", str(TOOL), *map(str, args)], capture_output=True, text=True,
                           encoding="utf-8", timeout=120)
        self.assertEqual(r.stderr, "", r.stderr)
        if code is not None:
            self.assertEqual(r.returncode, code, r.stdout)
        return r.returncode, r.stdout

    def status_json(self, reg, store=True):
        args = ["status", "--registry", reg, "--json"] + (["--intake", self.store] if store else [])
        return json.loads(self.run_tool(*args)[1])

    def snapshot(self, repo, files=()):
        idx = repo / ".git" / "index"
        return (git(repo, "rev-parse", "HEAD"), hashlib.sha256(idx.read_bytes()).hexdigest() if idx.exists() else None,
                git(repo, "for-each-ref"), git(repo, "status", "--porcelain=v1", "-uall"),
                tuple(hashlib.sha256((repo / f).read_bytes()).hexdigest() for f in files))

    def file_entry(self, report, lane, path):
        lane_out = next(l for l in report["lanes"] if l["lane"] == lane)
        return next(e for e in lane_out["files"] if e["path"] == path)

    def ack(self, reg, path, revision, actor="codex-prime", lane="fixture", code=None):
        return self.run_tool("intake", "ack", "--registry", reg, "--intake", self.store, "--lane", lane, "--path", path,
                             "--revision", revision, "--as", actor, code=code)

    # 1 three lanes, exact facts, read-only
    def test_01_three_lanes_read_only(self):
        self.commit(self.repo, {f"{PAGE}/05.01.md": batch("execution: returned\nDid: wrote it."),
                                "00.kernel/00.00.10.work/0598.other/05.01.md": batch("PENDING.")})
        sof = self.make_repo("sof", branch="sof/gm-kit")
        self.commit(sof, {"returns/sof-gm-kit-pass01.md": "# Return — sof-fixture\n\nDid\n\n- wrote a thing\n\n## Files\n- a\n"},
                    branch="sof/gm-kit")
        reg = self.registry(
            repos={"work": {"local": str(self.repo), "branch": "main", "remote_ref": "refs/remotes/origin/main",
                            "worktree": "registered-paths", "history_limit": 50},
                   "sof": {"local": str(sof), "branch": "sof/gm-kit", "remote_ref": "refs/remotes/origin/sof/gm-kit",
                           "worktree": "off", "history_limit": 50}},
            lanes=[{"lane": "fixture", "project": "workshop", "owner_label": "b1", "repository": "work", "pages": [PAGE],
                    "return_files": [], "review_sources": []},
                   {"lane": "other", "project": "workshop", "owner_label": "b2", "repository": "work",
                    "pages": ["00.kernel/00.00.10.work/0598.other"], "return_files": [], "review_sources": []},
                   {"lane": "sof", "project": "SoF", "owner_label": "sof builder", "repository": "sof", "pages": [],
                    "return_files": ["returns/sof-gm-kit-pass01.md"], "review_sources": []}])
        before = [self.snapshot(self.repo, [f"{PAGE}/05.01.md"]), self.snapshot(sof, ["returns/sof-gm-kit-pass01.md"])]
        code, text = self.run_tool("status", "--registry", reg)
        self.assertEqual(code, 1)
        for needle in ("lane fixture", "lane other", "lane sof", "execution returned", "execution pending",
                       "[return-file]", "(last observed, not fetched)", "only registered sources are read",
                       "worktree off", "recommendation, not authority"):
            self.assertIn(needle, text)
        rep = self.status_json(reg, store=False)
        sof_rev = self.file_entry(rep, "sof", "returns/sof-gm-kit-pass01.md")["revisions"][0]
        self.assertEqual((sof_rev["execution"], sof_rev["review"], sof_rev["eligible"]), ("unknown", "review-needed", True))
        self.assertEqual([r["label"] for r in self.file_entry(rep, "sof", "returns/sof-gm-kit-pass01.md")["revisions"]],
                         ["published", "local"])  # worktree off: the checkout is not read
        self.assertEqual(before, [self.snapshot(self.repo, [f"{PAGE}/05.01.md"]), self.snapshot(sof, ["returns/sof-gm-kit-pass01.md"])])
        self.assertFalse(self.store.exists())

    # 2 canonical versus page, every shape
    def test_02_canonical_conflicts(self):
        canon = "00.kernel/00.00.10.work/0401.goal/06.01.md"

        def record(state, work):
            keys = dict(record="current-assignment", schema="s", desk="00.kernel", book="00.00.10.work", workflow_space="0",
                        current_work=work, pack=work, assignment_state=state, waits_on="w", next="n", updated="2026-10-27")
            return "".join(f"{k}: {v}\n" for k, v in keys.items())

        page = f"{PAGE}/05.01.md"
        self.commit(self.repo, {page: batch("execution: returned\nDid."), canon: record("waiting", page)})
        reg = self.registry(canonical={"repository": "work", "path": canon, "lane": "fixture"})
        rep = self.status_json(reg)
        self.assertTrue(any("canonical says waiting" in c and "shows a return" in c for c in rep["conflicts"]), rep["conflicts"])
        self.commit(self.repo, {page: batch("PENDING."), canon: record("returned", page)})
        rep = self.status_json(reg)
        self.assertTrue(any("canonical says returned" in c for c in rep["conflicts"]))
        self.commit(self.repo, {canon: record("waiting", "00.kernel/00.00.10.work/0001.elsewhere/05.01.md")})
        rep = self.status_json(reg)
        self.assertTrue(any("not inside lane" in c for c in rep["conflicts"]))
        self.commit(self.repo, {canon: record("waiting", page)})
        self.write(self.repo, f"{PAGE}/06.09.md", "local note\n")
        rep = self.status_json(reg)
        self.assertTrue(any("uncommitted changes" in c for c in rep["conflicts"]))
        self.assertEqual(rep["attention"][0]["kind"], "conflict")

    # 3 and 12: published, local, worktree are separate revisions
    def test_03_published_local_worktree(self):
        page = f"{PAGE}/05.01.md"
        self.commit(self.repo, {page: batch("execution: returned\nv1")})
        self.commit(self.repo, {page: batch("execution: returned\nv2")}, push=False)
        self.write(self.repo, page, batch("execution: returned\nv3"))
        rep = self.status_json(self.registry())
        entry = self.file_entry(rep, "fixture", page)
        self.assertTrue(entry["divergent"])
        ids = {r["label"]: r["revision_id"] for r in entry["revisions"]}
        self.assertEqual(set(ids), {"published", "local", "worktree"})
        self.assertEqual(len(set(ids.values())), 3)
        self.assertEqual(rep["repositories"]["work"]["relation"], "local ahead of last-observed remote")

    # 4 identity under review and amendment; Prime's review is not re-queued
    def test_04_identity_review_amend(self):
        page = f"{PAGE}/05.01.md"
        v1 = batch("execution: returned\nDid v1.")
        self.commit(self.repo, {page: v1})
        reg = self.registry()
        rid = prefix(v1)
        self.ack(reg, page, rid, code=0)
        reviewed = batch("execution: returned\nDid v1.", f"reviewed_return_prefix: {rid}\nDisposition: REPAIR REQUIRED.\nfindings: FX-01=unresolved")
        self.assertEqual(prefix(reviewed), rid)
        self.commit(self.repo, {page: reviewed})
        rep = self.status_json(reg)
        revs = self.file_entry(rep, "fixture", page)["revisions"]
        self.assertTrue(all(r["revision_id"] == rid and r["intake"] == "seen" and r["review"] == "reviewed" for r in revs))
        self.assertFalse(any(a["kind"] in ("unseen", "review-needed") for a in rep["attention"]))
        amended = batch("execution: returned\nDid v1.\nAmendment: fixed FX-01.", f"reviewed_return_prefix: {rid}\nfindings: FX-01=unresolved")
        self.commit(self.repo, {page: amended})
        rep = self.status_json(reg)
        rev = self.file_entry(rep, "fixture", page)["revisions"][0]
        self.assertNotEqual(rev["revision_id"], rid)
        self.assertEqual((rev["intake"], rev["review"], rev["supersedes"]), ("unseen", "stale-review", rid))

    # 5 incomplete returns are not eligible
    def test_05_incomplete_not_eligible(self):
        for body in ("execution: claimed\nworking", "execution: running\nworking", "PENDING.", "execution: stopped\nhalt"):
            with self.subTest(body=body.split()[0]):
                page = f"{PAGE}/05.01.md"
                self.commit(self.repo, {page: batch(body)})
                rep = self.status_json(self.registry())
                rev = self.file_entry(rep, "fixture", page)["revisions"][0]
                self.assertFalse(rev["eligible"])
                code, out = self.ack(self.registry(), page, rev["revision_id"])
                self.assertEqual(code, 2)
                self.assertIn("not intake-eligible", out)

    # 6 ack idempotent, conflicting ack refused, refusals write nothing
    def test_06_ack_rules(self):
        page = f"{PAGE}/05.01.md"
        text = batch("execution: returned\nDid.")
        self.commit(self.repo, {page: text})
        reg = self.registry()
        rid = prefix(text)
        self.assertIn("seen", self.ack(reg, page, rid, code=0)[1])
        tree = sorted((p.relative_to(self.store).as_posix(), p.read_bytes()) for p in self.store.rglob("*") if p.is_file())
        self.assertEqual(len(tree), 1)
        self.assertIn("already-recorded", self.ack(reg, page, rid, code=0)[1])
        self.assertIn("conflicting acknowledgement", self.ack(reg, page, rid, actor="someone-else", code=2)[1])
        self.assertIn("full 64-hex", self.ack(reg, page, rid[:12], code=2)[1])
        self.assertIn("not currently observed", self.ack(reg, page, "0" * 64, code=2)[1])
        after = sorted((p.relative_to(self.store).as_posix(), p.read_bytes()) for p in self.store.rglob("*") if p.is_file())
        self.assertEqual(tree, after)
        rec = json.loads(tree[0][1])
        self.assertEqual(len(rec["subject_id"]), 64)
        self.assertEqual(tree[0][0], f"subjects/{rec['subject_id'][:12]}/0001.seen.json")
        inside = self.repo / "store-inside"
        code, out = self.run_tool("intake", "ack", "--registry", reg, "--intake", inside, "--lane", "fixture",
                                  "--path", page, "--revision", rid, "--as", "codex-prime")
        self.assertEqual(code, 2)
        self.assertIn("inside a Git working tree", out)
        self.assertFalse(inside.exists())

    # abbreviated id collision and inconsistent stored identity
    def test_06b_collision_and_inconsistent_identity(self):
        page = f"{PAGE}/05.01.md"
        text = batch("execution: returned\nDid.")
        self.commit(self.repo, {page: text})
        reg = self.registry()
        rid = prefix(text)
        subject = {"kind": "page-return", "repository": "work", "path": page, "revision_id": rid}
        sid = ps.subject_id(subject)
        other = dict(subject, path=f"{PAGE}/05.02.md")
        planted = {"schema": ps.INTAKE_SCHEMA, "subject_id": sid[:12] + ps.subject_id(other)[12:], "subject": other,
                   "observed": {"source": "local", "commit": None, "whole_sha256": "0" * 64, "execution": "returned"},
                   "supersedes": None, "by": "codex-prime", "at": "2026-10-27T00:00:00Z", "note": ps.NOTE}
        d = self.store / "subjects" / sid[:12]
        d.mkdir(parents=True)
        (d / "0001.seen.json").write_bytes(ps.canonical(planted))
        code, out = self.ack(reg, page, rid)
        self.assertEqual(code, 2)
        self.assertIn("bad records", out)
        code, out = self.run_tool("intake", "show", "--intake", self.store)
        self.assertEqual(code, 1)
        self.assertIn("inconsistent identity", out)
        rep = self.status_json(reg)
        self.assertTrue(any(a["kind"] == "bad-intake" for a in rep["attention"]))

    # 7 review binding (prefix and legacy whole hash), findings and passes
    def test_07_review_binding_findings(self):
        page = f"{PAGE}/05.01.md"
        v1 = batch("Did. legacy return without execution line.")
        self.commit(self.repo, {page: v1})
        whole = hashlib.sha256(v1.encode()).hexdigest()
        legacy = batch("Did. legacy return without execution line.",
                       f"Date: x. Reviewed return SHA-256: `{whole}`.\nDisposition: REPAIR REQUIRED, LG-01.\nfindings: LG-01=unresolved; LG-02=fix-planned")
        self.commit(self.repo, {page: legacy})
        rep = self.status_json(self.registry())
        rev = self.file_entry(rep, "fixture", page)["revisions"][0]
        self.assertEqual((rev["execution"], rev["review"]), ("unknown", "reviewed"))
        self.assertEqual(rev["disposition"], "REPAIR REQUIRED, LG-01.")
        lane = rep["lanes"][0]
        self.assertEqual({k: v["state"] for k, v in by_id(lane["findings"]).items()}, {"LG-01": "open", "LG-02": "open"})
        rid1 = rev["revision_id"]
        v2 = batch("Did. legacy return without execution line.\nAmended.",
                   f"reviewed_return_prefix: {prefix(batch('Did. legacy return without execution line.' + chr(10) + 'Amended.'))}\n"
                   "findings: LG-01=verified-fixed; LG-02=director-pending")
        self.commit(self.repo, {page: v2})
        rep = self.status_json(self.registry())
        f = by_id(rep["lanes"][0]["findings"])
        self.assertEqual((f["LG-01"]["state"], f["LG-01"]["passes"]), ("closed", 2))
        self.assertEqual((f["LG-02"]["resolution"], f["LG-02"]["passes"]), ("director-pending", 2))
        self.assertNotEqual(self.file_entry(rep, "fixture", page)["revisions"][0]["revision_id"], rid1)

    # 8 and PS-03: acknowledgement loss and a removed old Review cannot hide a finding
    def test_08_ps03_lineage_survives(self):
        page = f"{PAGE}/05.01.md"
        v1 = batch("execution: returned\nv1")
        self.commit(self.repo, {page: v1})
        reg = self.registry()
        rid1 = prefix(v1)
        self.ack(reg, page, rid1, code=0)
        self.commit(self.repo, {page: batch("execution: returned\nv1", f"reviewed_return_prefix: {rid1}\nDisposition: REPAIR REQUIRED.\nfindings: SY-01=unresolved")})
        v2 = batch("execution: returned\nv2 answers SY-01")  # the amended page no longer carries the old Review
        self.commit(self.repo, {page: v2})
        shutil.rmtree(self.store)
        rep = self.status_json(reg)
        f = by_id(rep["lanes"][0]["findings"])
        self.assertEqual(f["SY-01"]["state"], "open")
        rev = self.file_entry(rep, "fixture", page)["revisions"][0]
        self.assertEqual((rev["intake"], rev["review"], rev["supersedes"]), ("unseen", "stale-review", rid1))
        self.assertNotIn("accepted", json.dumps(rep).replace("not accepted", ""))
        self.assertTrue(any(a["kind"] == "open-finding" and "SY-01" in a["item"] for a in rep["attention"]))

    # missing legacy history is unknown, not zero findings
    def test_08b_missing_history_is_unknown(self):
        page = f"{PAGE}/05.01.md"
        v1 = batch("execution: returned\nv1")
        self.commit(self.repo, {page: v1})
        self.commit(self.repo, {page: batch("execution: returned\nv1", f"reviewed_return_prefix: {prefix(v1)}\nfindings: OLD-1=unresolved")})
        self.commit(self.repo, {page: batch("execution: returned\nv2")})
        reg = self.registry(repos={"work": {"local": str(self.repo), "branch": "main", "remote_ref": "refs/remotes/origin/main",
                                            "worktree": "registered-paths", "history_limit": 1}})
        rep = self.status_json(reg)
        self.assertEqual(self.file_entry(rep, "fixture", page)["history"], "incomplete")
        self.assertTrue(any(a["kind"] == "history-unknown" for a in rep["attention"]))
        self.assertNotIn("OLD-1", by_id(rep["lanes"][0]["findings"]))  # not seen within the limit, and reported as unknown
        untracked = f"{PAGE}/05.02.md"
        self.write(self.repo, untracked, batch("execution: returned\nlocal only"))
        rep = self.status_json(self.registry())
        self.assertEqual(self.file_entry(rep, "fixture", untracked)["history"], "none")

    # 9 missing sources stay visible
    def test_09_missing_sources(self):
        self.commit(self.repo, {f"{PAGE}/05.01.md": batch("execution: returned\nx")})
        reg = self.registry(lanes=[{"lane": "fixture", "project": "w", "owner_label": "b", "repository": "work",
                                    "pages": [PAGE, "00.kernel/00.00.10.work/0597.gone"],
                                    "return_files": ["returns/absent.md"], "review_sources": ["notes/absent.md"]}])
        rep = self.status_json(reg)
        missing = [a["item"] for a in rep["attention"] if a["kind"] == "missing"]
        self.assertTrue(any("0597.gone" in m for m in missing))
        self.assertTrue(any("returns/absent.md" in m for m in missing))
        self.assertEqual(rep["lanes"][0]["review_sources"][0]["status"], "missing")

    # 10 an unregistered decoy return is never read
    def test_10_no_crawl(self):
        decoy = "00.kernel/00.00.10.work/0596.decoy/05.01.md"
        self.commit(self.repo, {f"{PAGE}/05.01.md": batch("execution: returned\nx"), decoy: batch("execution: returned\nDECOY"),
                                f"{PAGE}/evidence/05.01.md": batch("execution: returned\ncopy")})
        reg_path = self.registry()
        reg, _ = ps.load_registry(str(reg_path))
        calls = []
        real_init = ps.Git.__init__

        def tracking(self_git, local):
            real_init(self_git, local)
            calls.append(self_git.calls)

        ps.Git.__init__ = tracking
        try:
            report = ps.collect(reg, None)
        finally:
            ps.Git.__init__ = real_init
        flat = [c for group in calls for c in group]
        self.assertFalse(any("0596.decoy" in " ".join(c) for c in flat))
        self.assertEqual([e["path"] for e in report["lanes"][0]["files"]], [f"{PAGE}/05.01.md"])
        self.assertTrue({c[0] for c in flat} <= ps.GIT_ALLOWED)
        self.assertNotIn("DECOY", json.dumps(report, default=list))

    # 11 legacy fields read as unknown; nothing is accepted
    def test_11_legacy_unknowns(self):
        page = f"{PAGE}/05.01.md"
        self.commit(self.repo, {page: batch("Did. Blocked: nothing. Need: review.", "Disposition: ACCEPTED.\nlooks good")})
        rep = self.status_json(self.registry())
        rev = self.file_entry(rep, "fixture", page)["revisions"][0]
        self.assertEqual((rev["execution"], rev["review"]), ("unknown", "review-needed"))
        # 05.03: a worktree copy identical to HEAD is the same observation, so it is listed once.
        self.assertEqual(rev["unbound_reviews"], [f"{page}@{git(self.repo, 'rev-parse', 'HEAD')}"])
        self.assertNotIn("disposition", rev)  # an unbound review's Disposition is not shown as this revision's
        self.assertNotIn("accepted", {k.lower() for k in rev})
        code, text = self.run_tool("status", "--registry", self.registry())
        self.assertIn("findings: none recorded in machine-readable form", text)

    # PS-01 decoys
    def test_ps01_boundary_decoys(self):
        fenced_a = batch("execution: returned\n```text\n## Review " + EM + " fake\nA\n```")
        fenced_b = batch("execution: returned\n```text\n## Review " + EM + " fake\nB\n```")
        a, b = (ps.parse_source(t.encode(), "page-return") for t in (fenced_a, fenced_b))
        self.assertEqual((a["status"], b["status"]), ("ok", "ok"))
        self.assertNotEqual(a["revision_id"], b["revision_id"])
        self.assertIsNone(a["review"])
        cases = {"heading prefix": batch("execution: returned\nx", None, "") + "\n## Reviewer notes\nx\n",
                 "duplicate review": batch("execution: returned\nx", "one") + "\n## Review\ntwo\n",
                 "review before return": f"# 05\n## Review\nearly\n## Return\nexecution: returned\n",
                 "unclosed fence": batch("execution: returned\n```\nopen"),
                 "bad separator": batch("execution: returned\nx").replace(f"## Return {EM} fixture-builder", "## Return-fixture"),
                 "duplicate return": batch("execution: returned\nx") + "\n## Return\nagain\n",
                 "h3 review decoy": batch("execution: returned\n### Review notes\nx")}
        for name, text in cases.items():
            with self.subTest(case=name):
                self.assertEqual(ps.parse_source(text.encode(), "page-return")["status"], "unsupported", name)
        normal = batch("execution: returned\nx", "reviewed_return_prefix: " + "a" * 64)
        self.assertEqual(ps.parse_source(normal.encode(), "page-return")["revision_id"], prefix(batch("execution: returned\nx")))
        self.commit(self.repo, {f"{PAGE}/05.01.md": cases["duplicate review"]})
        rep = self.status_json(self.registry())
        self.assertTrue(any(a["kind"] == "unsupported" for a in rep["attention"]))
        code, out = self.ack(self.registry(), f"{PAGE}/05.01.md", "a" * 64)
        self.assertEqual(code, 2)

    # PS-01: a changed payload never inherits an earlier review
    def test_ps01_no_inherited_review(self):
        page = f"{PAGE}/05.01.md"
        v1 = batch("execution: returned\nv1")
        rid = prefix(v1)
        changed = batch("execution: returned\nv1", f"reviewed_return_prefix: {rid}\nDisposition: ACCEPTED.",
                        extra="depends_on: x\n")  # metadata before the Return changed
        self.commit(self.repo, {page: changed})
        rep = self.status_json(self.registry())
        rev = self.file_entry(rep, "fixture", page)["revisions"][0]
        self.assertNotEqual(rev["revision_id"], rid)
        self.assertNotEqual(rev["review"], "reviewed")
        self.assertNotIn("disposition", rev)

    # PS-02 SoF return-file shape
    def test_ps02_return_file_shape(self):
        sof_text = ("# Return — sof-gm-kit-pass01\n\nDid\n\n- wrote notes\n\nBlocked\n\n- nothing\n\nNeed\n\n- review\n\n"
                    "## Files\n\n- a\n\n## Notes account\n\nN1.\n")
        p = ps.parse_source(sof_text.encode(), "return-file")
        self.assertEqual((p["status"], p["execution"], p["review"]), ("ok", "unknown", None))
        self.assertEqual(p["revision_id"], hashlib.sha256(sof_text.encode()).hexdigest())
        self.assertEqual(ps.parse_source(b"# Notes\n\nDid\n", "return-file")["status"], "unsupported")
        self.assertEqual(ps.parse_source(sof_text.encode(), "page-return")["status"], "unsupported")
        reviewed = sof_text + f"\n## Review {EM} Codex Prime\nreviewed_return_prefix: {p['revision_id']}\nfindings: SOF-1=unresolved\n"
        self.assertEqual(ps.parse_source(reviewed.encode(), "return-file")["revision_id"], p["revision_id"])

    # invalid registry and path escape
    def test_invalid_registry(self):
        base = json.loads(self.registry().read_text(encoding="utf-8"))
        variants = {
            "unknown key": dict(base, extra=1),
            "path escape": dict(base, lanes=[dict(base["lanes"][0], pages=["00.kernel/../x"])]),
            "absolute": dict(base, lanes=[dict(base["lanes"][0], return_files=["/etc/x"])]),
            "backslash": dict(base, lanes=[dict(base["lanes"][0], review_sources=["a\\b"])]),
            "relative local": dict(base, repositories={"work": dict(base["repositories"]["work"], local="rel")}),
            "bad attention": dict(base, attention_order=["conflict", "nope"]),
            "unknown repository": dict(base, lanes=[dict(base["lanes"][0], repository="nope")]),
        }
        for name, reg in variants.items():
            with self.subTest(case=name):
                path = self.tmp / f"bad-{name.replace(' ', '-')}.json"
                path.write_text(json.dumps(reg), encoding="utf-8")
                code, out = self.run_tool("status", "--registry", path)
                self.assertEqual(code, 2, out)
                self.assertIn("refused: registry", out)
        dup = self.tmp / "dup.json"
        dup.write_text('{"schema": "prime-support-registry", "schema": "x"}', encoding="utf-8")
        self.assertEqual(self.run_tool("status", "--registry", dup)[0], 2)
        nan = self.tmp / "nan.json"
        nan.write_text(json.dumps(base).replace('"history_limit": 50', '"history_limit": NaN'), encoding="utf-8")
        self.assertIn("nonfinite", self.run_tool("status", "--registry", nan)[1])
        self.assertIn("must be absolute", self.run_tool("status", "--registry", "relative.json")[1])

    # no network: the runner refuses anything outside the allowlist
    def test_git_allowlist(self):
        g = ps.Git(str(self.repo))
        for sub in ("fetch", "pull", "push", "ls-remote", "remote", "clone", "commit", "add"):
            with self.subTest(sub=sub):
                with self.assertRaises(AssertionError):
                    g.run(sub)
        source = TOOL.read_text(encoding="utf-8")
        self.assertNotIn('"fetch"', source.split("GIT_ALLOWED")[0])

    # scan and show are read-only; ack writes only its selected store
    def test_scan_show_read_only(self):
        page = f"{PAGE}/05.01.md"
        text = batch("execution: returned\nx")
        self.commit(self.repo, {page: text})
        reg = self.registry()
        before = self.snapshot(self.repo, [page])

        def outside_store():
            return {p.relative_to(self.tmp).as_posix(): p.read_bytes() for p in self.tmp.rglob("*")
                    if p.is_file() and self.store not in p.parents}

        files_before = outside_store()
        code, out = self.run_tool("intake", "scan", "--registry", reg, "--intake", self.store)
        self.assertEqual(code, 1)
        self.assertIn("unseen", out)
        self.assertFalse(self.store.exists())
        self.ack(reg, page, prefix(text), code=0)
        self.assertEqual(self.run_tool("intake", "show", "--intake", self.store)[0], 0)
        self.run_tool("status", "--registry", reg, "--intake", self.store)
        self.assertEqual(before, self.snapshot(self.repo, [page]))
        self.assertEqual(files_before, outside_store())  # status, scan and show wrote nothing; ack wrote only the store
        self.assertEqual(len([p for p in self.store.rglob("*") if p.is_file()]), 1)


if __name__ == "__main__":
    unittest.main()
