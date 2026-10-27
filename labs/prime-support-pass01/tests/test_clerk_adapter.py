"""Registered Clerk return intake (0507.prime-support/05.04). Disposable repositories and Clerk stores only.

  python -B -X dev tests/test_clerk_adapter.py -v

queue/claim/return below are FIXTURE SETUP ONLY, run with a copied, hash-checked clerk.py. The adapter under test
only ever runs `show --json`.
"""
import builtins
import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_prime_support as tps  # noqa: E402

ps = tps.ps
ca = ps.clerk_adapter
CLERK_SOURCE = tps.LAB.parent / "clerk-handoff-pass02" / "clerk.py"
TASK = b"Count the non-blank lines.\n"
RESULT = b'{"count":3}'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tree(root: Path):
    if not root.exists():
        return {}
    return {p.relative_to(root).as_posix(): (sha(p.read_bytes()) if p.is_file() else "dir") for p in sorted(root.rglob("*"))}


class ClerkAdapter(tps.Fixture):
    """Reuses the original fixture helpers. Inherited test_ methods are disabled at the bottom of this module."""

    def setUp(self):
        super().setUp()
        self.commit(self.repo, {f"{tps.PAGE}/05.01.md": tps.batch("PENDING.")})
        self.tool = self.tmp / "tool" / "clerk.py"
        self.tool.parent.mkdir()
        data = CLERK_SOURCE.read_bytes()
        self.assertEqual(sha(data), ca.ACCEPTED_CLERK_SHA256, "the copied Clerk is not the accepted inspection/2 code")
        self.tool.write_bytes(data)
        self.cstore = self.tmp / "clerk-store"
        self.base = self.tmp / "base"
        self.base.mkdir()
        (self.base / "task.txt").write_bytes(TASK)

    # ---- fixture setup: the copied Clerk, never the adapter ----
    def clerk(self, *args, check=True):
        r = subprocess.run([sys.executable, "-B", str(self.tool), *map(str, args)], capture_output=True, text=True,
                           encoding="utf-8", timeout=60)
        if check:
            self.assertIn(r.returncode, (0,), r.stdout + r.stderr)
        return r

    def make_job(self, job_id="job-1", reviewer="codex-prime", stage="returned"):
        job = {"job_id": job_id, "assignee": "builder-b", "reviewer": reviewer,
               "instructions": {"path": "task.txt", "sha256": sha(TASK)}, "release": "fixture release",
               "routed_by": "router-fixture", "expected_outputs": ["result.json"]}
        jf = self.tmp / f"{job_id}.json"
        jf.write_text(json.dumps(job), encoding="utf-8")
        self.clerk("queue", "--store", self.cstore, "--job", jf, "--instructions-base", self.base)
        if stage == "queued":
            return None
        out = self.clerk("claim", "--store", self.cstore, "--job", job_id, "--as", "builder-b", "--instructions-base", self.base).stdout
        token = next(line.split()[1] for line in out.splitlines() if line.startswith("token "))
        if stage == "claimed":
            return token
        (self.cstore / "jobs" / job_id / "outbox" / "result.json").write_bytes(RESULT)
        self.clerk("return", "--store", self.cstore, "--job", job_id, "--as", "builder-b", "--claim", token,
                   "--delivery", "d-1", "--evidence", "fixture evidence")
        return token

    def real_event(self, job_id="job-1"):
        jd = self.cstore / "jobs" / job_id
        return sha((jd / "0003.returned.json").read_bytes()), json.loads((jd / "0003.witness.json").read_text(encoding="utf-8"))["sha256"]

    def creg(self, jobs, tool_sha=None, tool_path=None):
        reg = json.loads(self.registry().read_text(encoding="utf-8"))
        reg["version"] = 2
        reg["clerk_tool"] = {"path": str(tool_path or self.tool), "sha256": tool_sha or ca.ACCEPTED_CLERK_SHA256}
        reg["lanes"][0]["clerk_jobs"] = jobs
        path = self.tmp / f"creg-{len(list(self.tmp.glob('creg-*')))}.json"
        path.write_text(json.dumps(reg), encoding="utf-8")
        return path

    def cjob(self, job_id="job-1", reviewer="codex-prime", base=None):
        return {"store": str(self.cstore), "job_id": job_id, "instructions_base": str(base or self.base), "reviewer": reviewer}

    def guarded(self, *args, code=None):
        """Every adapter CLI call: the Clerk store and the fixture repository must be byte-identical afterwards."""
        before = (tree(self.cstore), self.snapshot(self.repo, [f"{tps.PAGE}/05.01.md"]), tree(self.tool.parent))
        result = self.run_tool(*args, code=code)
        self.assertEqual(before, (tree(self.cstore), self.snapshot(self.repo, [f"{tps.PAGE}/05.01.md"]), tree(self.tool.parent)),
                         "an adapter command changed a Clerk store, the tool or the repository")
        return result

    def cstatus(self, reg):
        return json.loads(self.guarded("status", "--registry", reg, "--intake", self.store, "--json")[1])

    def obs(self, rep, job_id="job-1"):
        return next(o for o in rep["lanes"][0]["clerk"] if o["job_id"] == job_id)

    def kinds(self, rep):
        return [a["kind"] for a in rep["attention"]]

    def ack(self, reg, event, actor="codex-prime", job="job-1", code=None):
        return self.guarded("intake", "ack-clerk", "--registry", reg, "--intake", self.store, "--lane", "fixture",
                            "--store", self.cstore, "--job", job, "--event-sha256", event, "--as", actor, code=code)

    # ---- the connection ----
    def test_clean_return_unseen_ack_seen_idempotent(self):
        self.make_job()
        reg = self.creg([self.cjob()])
        event, witness = self.real_event()
        o = self.obs(self.cstatus(reg))
        self.assertEqual((o["state"], o["clean"], o["identity"], o["intake"], o["review"]),
                         ("returned", True, True, "unseen", "not-machine-readable"))
        self.assertEqual(o["event_sha256"], event)
        self.assertEqual(o["event_sha256"], witness)
        code, out = self.guarded("intake", "scan", "--registry", reg, "--intake", self.store)
        self.assertIn(f"clerk job-1 event {event} unseen clean yes", out)
        self.assertIn("seen", self.ack(reg, event, code=0)[1])
        rep = self.cstatus(reg)
        self.assertEqual(self.obs(rep)["intake"], "seen")
        self.assertIn("review-needed", self.kinds(rep))
        self.assertNotIn("clerk-not-clean", self.kinds(rep))
        files = sorted(p for p in self.store.rglob("*") if p.is_file())
        self.assertEqual(len(files), 1)
        rec = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertEqual((rec["schema"], rec["subject"]["kind"], rec["subject"]["event_sha256"]), ("prime-intake/2", "clerk-return", event))
        self.assertEqual(len(rec["subject_id"]), 64)
        self.assertIn("already-recorded", self.ack(reg, event, code=0)[1])
        self.assertIn("conflicting acknowledgement", self.ack(reg, event, actor="other-label", code=2)[1])
        self.assertEqual(files, sorted(p for p in self.store.rglob("*") if p.is_file()))
        code, out = self.guarded("intake", "show", "--intake", self.store)
        self.assertIn(f"clerk {ca.canonical_store(str(self.cstore))}#job-1  event {event}", out)

    def test_queued_and_claimed_have_no_identity(self):
        self.make_job("job-q", stage="queued")
        self.make_job("job-c", stage="claimed")
        reg = self.creg([self.cjob("job-q"), self.cjob("job-c")])
        rep = self.cstatus(reg)
        for job_id, state in (("job-q", "queued"), ("job-c", "claimed")):
            o = self.obs(rep, job_id)
            self.assertEqual((o["state"], o["event_sha256"], o["identity"], o["intake"]), (state, None, False, None))
            self.assertIn("no returned-event identity", self.ack(reg, "a" * 64, job=job_id, code=2)[1])
        self.assertFalse(any("clerk" in a["item"] for a in rep["attention"]))

    def test_changed_artifact_keeps_identity_and_attention_after_ack(self):
        self.make_job()
        reg = self.creg([self.cjob()])
        event, _ = self.real_event()
        self.ack(reg, event, code=0)
        (self.cstore / "jobs/job-1/outbox/result.json").write_bytes(b'{"count":4}')
        rep = self.cstatus(reg)
        o = self.obs(rep)
        self.assertEqual((o["event_sha256"], o["intake"], o["clean"], o["checks"]["artifacts"]), (event, "seen", False, "changed"))
        self.assertTrue(any(a["kind"] == "clerk-not-clean" and "artifact-changed" in a["item"] for a in rep["attention"]))

    def test_stale_and_missing_instruction_base(self):
        self.make_job()
        (self.base / "task.txt").write_bytes(b"stale\n")
        o = self.obs(self.cstatus(self.creg([self.cjob()])))
        self.assertEqual((o["checks"]["instructions"], o["clean"], o["identity"]), ("unusable", False, True))
        o = self.obs(self.cstatus(self.creg([self.cjob(base=self.tmp / "no-such-base")])))
        self.assertEqual((o["checks"]["instructions"], o["clean"]), ("unusable", False))

    def test_unknown_job_and_damaged_pair(self):
        self.make_job()
        rep = self.cstatus(self.creg([self.cjob("job-missing")]))
        o = self.obs(rep, "job-missing")
        self.assertEqual((o["state"], o["identity"]), ("unknown", False))
        self.assertIn("missing", self.kinds(rep))
        (self.cstore / "jobs/job-1/0003.witness.json").unlink()
        reg = self.creg([self.cjob()])
        rep = self.cstatus(reg)
        o = self.obs(rep)
        self.assertEqual((o["state"], o["event_sha256"], o["identity"]), ("incomplete", None, False))
        self.assertIn("clerk-not-clean", self.kinds(rep))
        self.assertIn("no returned-event identity", self.ack(reg, "b" * 64, code=2)[1])

    def test_changed_valid_event_does_not_inherit_seen(self):
        self.make_job()
        reg = self.creg([self.cjob()])
        event, _ = self.real_event()
        self.ack(reg, event, code=0)
        jd = self.cstore / "jobs/job-1"
        # Fixture: a coherent rewrite of both completion files (Clerk's documented limit) yields a new valid event.
        new_bytes = (jd / "0003.returned.json").read_bytes().replace(b"fixture evidence", b"rewritten evidence")
        witness = json.loads((jd / "0003.witness.json").read_text(encoding="utf-8"))
        witness["sha256"] = sha(new_bytes)
        os.remove(jd / "0003.returned.json")
        os.remove(jd / "0003.witness.json")
        (jd / "0003.witness.json").write_bytes((json.dumps(witness, sort_keys=True, separators=(",", ":")) + "\n").encode())
        (jd / "0003.returned.json").write_bytes(new_bytes)
        o = self.obs(self.cstatus(reg))
        self.assertEqual(o["state"], "returned")
        self.assertNotEqual(o["event_sha256"], event)
        self.assertEqual(o["intake"], "unseen")
        self.assertIn("stale event", self.ack(reg, event, code=2)[1])

    def test_reviewer_binding_conflict(self):
        self.make_job()
        reg = self.creg([self.cjob(reviewer="someone-else")])
        rep = self.cstatus(reg)
        o = self.obs(rep)
        self.assertTrue(o["binding"].startswith("mismatch"))
        self.assertEqual((o["identity"], o["clean"], o["intake"]), (False, False, None))
        self.assertTrue(any(a["kind"] == "conflict" and "reviewer" in a["item"] for a in rep["attention"]))
        self.assertIn("registration binding", self.ack(reg, self.real_event()[0], code=2)[1])

    def test_malformed_and_old_schema_projections_are_unsupported(self):
        self.make_job()
        good = subprocess.run(ca.argv_for(str(self.tool), self.cjob()), capture_output=True, text=True, encoding="utf-8")
        doc = json.loads(good.stdout)
        old = dict(doc, schema="clerk-handoff-inspection/1")
        old_returned = dict(doc, returned={k: v for k, v in doc["returned"].items() if k != "event_sha256"})
        variants = {
            "invalid json": (0, "{not json\n", ""),
            "duplicate keys": (0, '{"schema":"a","schema":"b"}\n', ""),
            "not an object": (0, "[1]\n", ""),
            "old schema": (0, json.dumps(old) + "\n", ""),
            "inspection/1 returned shape": (0, json.dumps(old_returned) + "\n", ""),
            "job id mismatch": (0, json.dumps(dict(doc, job_id="job-2")) + "\n", ""),
            "exit 0 with problems": (0, json.dumps(dict(doc, problems=[{"kind": "corrupt", "detail": "x"}])) + "\n", ""),
            "stderr": (0, good.stdout, "warning\n"),
            "two lines": (0, good.stdout + good.stdout, ""),
            "bad enum": (0, json.dumps(dict(doc, checks=dict(doc["checks"], artifacts="fine"))) + "\n", ""),
        }
        tool = {"path": str(self.tool), "sha256": ca.ACCEPTED_CLERK_SHA256}
        for name, reply in variants.items():
            with self.subTest(case=name):
                o = ca.inspect(tool, self.cjob(), runner=lambda argv, r=reply: r)
                self.assertEqual((o["status"], o["identity"], o["event_sha256"]), ("unsupported", False, None), o["reason"])
        o = ca.inspect(tool, self.cjob(), runner=lambda argv: (good.returncode, good.stdout, good.stderr))
        self.assertEqual((o["status"], o["clean"]), ("ok", True))

    def test_wrong_tool_identity_is_never_executed(self):
        self.make_job()
        calls = []
        o = ca.inspect({"path": str(self.tool), "sha256": "c" * 64}, self.cjob(), runner=lambda argv: calls.append(argv))
        self.assertEqual((o["status"], calls), ("unsupported", []))
        marker = self.tmp / "executed.marker"
        planted = self.tmp / "tool2" / "clerk.py"
        planted.parent.mkdir()
        planted.write_bytes(self.tool.read_bytes().replace(b"from __future__ import annotations\n",
                            b"from __future__ import annotations\nopen(%r, 'w').close()\n" % str(marker), 1))
        rep = self.cstatus(self.creg([self.cjob()], tool_path=planted))
        o = self.obs(rep)
        self.assertEqual(o["status"], "unsupported")
        self.assertIn("not the accepted inspection/2 code", o["reason"])
        self.assertFalse(marker.exists())
        code, out = self.run_tool("status", "--registry", self.creg([self.cjob()], tool_sha="d" * 64), "--json")
        self.assertIn("not the accepted inspection/2 code", out)

    def test_ack_stale_event_and_abbreviated_id_refused(self):
        self.make_job()
        reg = self.creg([self.cjob()])
        event, _ = self.real_event()
        self.assertIn("stale event", self.ack(reg, "e" * 64, code=2)[1])
        self.assertIn("full 64-hex", self.ack(reg, event[:12], code=2)[1])
        self.assertFalse(self.store.exists())

    def test_ack_store_deletion_restores_unseen_and_keeps_problems(self):
        self.make_job()
        reg = self.creg([self.cjob()])
        event, _ = self.real_event()
        self.ack(reg, event, code=0)
        (self.cstore / "jobs/job-1/outbox/result.json").write_bytes(b"changed")
        shutil.rmtree(self.store)
        rep = self.cstatus(reg)
        o = self.obs(rep)
        self.assertEqual((o["intake"], o["clean"]), ("unseen", False))
        self.assertIn("clerk-not-clean", self.kinds(rep))
        self.assertNotIn("accepted", json.dumps(rep).replace("not accepted", ""))

    def test_intake_store_inside_a_clerk_store_is_refused(self):
        self.make_job()
        reg = self.creg([self.cjob()])
        inside = self.cstore / "intake"
        code, out = self.guarded("intake", "ack-clerk", "--registry", reg, "--intake", inside, "--lane", "fixture",
                                 "--store", self.cstore, "--job", "job-1", "--event-sha256", self.real_event()[0],
                                 "--as", "codex-prime")
        self.assertEqual(code, 2)
        self.assertIn("inside a registered Clerk store", out)

    def test_adapter_reads_no_store_file_and_runs_only_show_json(self):
        self.make_job()
        reg, _ = ps.load_registry(str(self.creg([self.cjob()])))
        root = os.path.normcase(os.path.realpath(self.cstore))
        touched, argvs = [], []

        def note(p):
            try:
                if os.path.normcase(os.path.realpath(os.fspath(p))).startswith(root):
                    touched.append(os.fspath(p))
            except TypeError:
                pass

        real_open, real_listdir, real_scandir = builtins.open, os.listdir, os.scandir
        real_read_bytes, real_read_text, real_run = Path.read_bytes, Path.read_text, ca.run_show

        def run_spy(argv):
            argvs.append(list(argv))
            return real_run(argv)

        builtins.open = lambda p, *a, **k: (note(p), real_open(p, *a, **k))[1]
        os.listdir = lambda p=".": (note(p), real_listdir(p))[1]
        os.scandir = lambda p=".": (note(p), real_scandir(p))[1]
        Path.read_bytes = lambda self_p: (note(self_p), real_read_bytes(self_p))[1]
        Path.read_text = lambda self_p, *a, **k: (note(self_p), real_read_text(self_p, *a, **k))[1]
        ca.run_show = run_spy
        try:
            report = ps.collect(reg, None)
        finally:
            builtins.open, os.listdir, os.scandir = real_open, real_listdir, real_scandir
            Path.read_bytes, Path.read_text, ca.run_show = real_read_bytes, real_read_text, real_run
        self.assertEqual(touched, [], "the adapter itself opened or listed a Clerk store path")
        self.assertEqual(argvs, [[sys.executable, "-I", "-B", str(self.tool), "show", "--store", str(self.cstore),
                                  "--job", "job-1", "--instructions-base", str(self.base), "--json"]])
        self.assertEqual(report["lanes"][0]["clerk"][0]["state"], "returned")
        source = (tps.LAB / "clerk_adapter.py").read_text(encoding="utf-8")
        # "claim" is a legitimate inspection/2 key, so the subcommand check is the argv assertion above.
        for forbidden in ("0003.returned", "0003.witness", "outbox", "listdir", "scandir", "glob(", "shell=True",
                          '"queue"', '"return"', '"--resume"'):
            self.assertNotIn(forbidden, source)

    def test_registry_versions(self):
        v1 = json.loads(self.registry().read_text(encoding="utf-8"))
        self.assertIn(self.run_tool("status", "--registry", self.registry())[0], (0, 1))  # v1 still valid (not refused)
        cases = {
            "v1 with clerk_tool": dict(v1, clerk_tool={"path": str(self.tool), "sha256": ca.ACCEPTED_CLERK_SHA256}),
            "v1 with clerk_jobs": dict(v1, lanes=[dict(v1["lanes"][0], clerk_jobs=[])]),
            "v2 jobs without tool": dict(v1, version=2, lanes=[dict(v1["lanes"][0], clerk_jobs=[self.cjob()])]),
            "v2 relative store": dict(v1, version=2, clerk_tool={"path": str(self.tool), "sha256": ca.ACCEPTED_CLERK_SHA256},
                                      lanes=[dict(v1["lanes"][0], clerk_jobs=[dict(self.cjob(), store="rel")])]),
            "v2 duplicate job": dict(v1, version=2, clerk_tool={"path": str(self.tool), "sha256": ca.ACCEPTED_CLERK_SHA256},
                                     lanes=[dict(v1["lanes"][0], clerk_jobs=[self.cjob(), self.cjob()])]),
            "v2 extra job key": dict(v1, version=2, clerk_tool={"path": str(self.tool), "sha256": ca.ACCEPTED_CLERK_SHA256},
                                     lanes=[dict(v1["lanes"][0], clerk_jobs=[dict(self.cjob(), extra=1)])]),
            "version 3": dict(v1, version=3),
        }
        for name, reg in cases.items():
            with self.subTest(case=name):
                path = self.tmp / f"bad-{name.replace(' ', '-')}.json"
                path.write_text(json.dumps(reg), encoding="utf-8")
                code, out = self.run_tool("status", "--registry", path)
                self.assertEqual(code, 2, out)
                self.assertIn("refused: registry", out)


for _name in [n for n in vars(tps.Fixture) if n.startswith("test_")]:
    setattr(ClerkAdapter, _name, None)

if __name__ == "__main__":
    unittest.main()
