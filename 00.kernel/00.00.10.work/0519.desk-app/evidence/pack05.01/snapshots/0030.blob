"""Registered Clerk return intake demonstration (0507.prime-support/05.04). Scope: REGISTERED JOBS ONLY.

  python -B demo_clerk.py --out <new absolute dir outside Git> --clerk D:\\Git\\lib-build\\labs\\clerk-handoff-pass02\\clerk.py

The given clerk.py is copied into --out and must hash to the accepted inspection/2 code. queue/claim/return are
fixture setup with that copy. Every prime_support.py call is a separate process. The Clerk store is snapshotted around
each adapter call. transcript.json keeps argv, exit codes and stdout.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
TOOL = LAB / "prime_support.py"
sys.path.insert(0, str(LAB))
import clerk_adapter  # noqa: E402

transcript, checks = [], []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tree(root):
    return {p.relative_to(root).as_posix(): (sha(p.read_bytes()) if p.is_file() else "dir") for p in sorted(root.rglob("*"))}


def run(step, argv, setup=False):
    r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", timeout=120)
    transcript.append({"step": step, "role": "fixture setup" if setup else "adapter", "argv": argv,
                       "exit": r.returncode, "stdout": r.stdout, "stderr": r.stderr})
    return r


def expect(name, cond, detail=""):
    checks.append({"check": name, "ok": bool(cond), "detail": detail})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--clerk", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    if not out.is_absolute() or out.exists():
        sys.exit("stop: --out must be a new absolute directory")
    probe = out.parent
    while probe != probe.parent:
        if (probe / ".git").exists():
            sys.exit("stop: --out must be outside every Git working tree")
        probe = probe.parent
    out.mkdir(parents=True)
    data = Path(a.clerk).read_bytes()
    if sha(data) != clerk_adapter.ACCEPTED_CLERK_SHA256:
        sys.exit("stop: --clerk is not the accepted inspection/2 code")
    tool = out / "tool" / "clerk.py"
    tool.parent.mkdir()
    tool.write_bytes(data)
    store, base, intake = out / "clerk-store", out / "base", out / "intake-store"
    base.mkdir()
    (base / "task.txt").write_bytes(b"Count the non-blank lines.\n")
    job = {"job_id": "demo-0001", "assignee": "builder-b", "reviewer": "codex-prime",
           "instructions": {"path": "task.txt", "sha256": sha(b"Count the non-blank lines.\n")},
           "release": "fixture release", "routed_by": "router-fixture", "expected_outputs": ["result.json"]}
    (out / "job.json").write_text(json.dumps(job), encoding="utf-8")
    clerk = [sys.executable, "-B", str(tool)]
    run("S1 queue", clerk + ["queue", "--store", str(store), "--job", str(out / "job.json"), "--instructions-base", str(base)], True)
    r = run("S2 claim", clerk + ["claim", "--store", str(store), "--job", "demo-0001", "--as", "builder-b", "--instructions-base", str(base)], True)
    token = next(line.split()[1] for line in r.stdout.splitlines() if line.startswith("token "))
    (store / "jobs/demo-0001/outbox/result.json").write_bytes(b'{"count":3}')
    run("S3 return", clerk + ["return", "--store", str(store), "--job", "demo-0001", "--as", "builder-b", "--claim", token,
                              "--delivery", "d-1", "--evidence", "demo fixture"], True)
    real = sha((store / "jobs/demo-0001/0003.returned.json").read_bytes())
    witness = json.loads((store / "jobs/demo-0001/0003.witness.json").read_text(encoding="utf-8"))["sha256"]
    repo = out / "work"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True, capture_output=True)
    registry = out / "registry.json"
    registry.write_text(json.dumps({
        "schema": "prime-support-registry", "version": 2,
        "repositories": {"work": {"local": str(repo), "branch": "main", "remote_ref": "refs/remotes/origin/main",
                                  "worktree": "off", "history_limit": 50}},
        "clerk_tool": {"path": str(tool), "sha256": clerk_adapter.ACCEPTED_CLERK_SHA256},
        "lanes": [{"lane": "clerk", "project": "workshop (fixture)", "owner_label": "builder-b", "repository": "work",
                   "pages": [], "return_files": [], "review_sources": [],
                   "clerk_jobs": [{"store": str(store), "job_id": "demo-0001", "instructions_base": str(base),
                                   "reviewer": "codex-prime"}]}]}, indent=1), encoding="utf-8")
    ps = [sys.executable, "-B", str(TOOL)]

    def adapter(step, args):
        before = tree(store)
        r = run(step, ps + args)
        expect(f"{step}: Clerk store byte-identical", tree(store) == before)
        return r

    def status(step):
        r = adapter(step, ["status", "--registry", str(registry), "--intake", str(intake), "--json"])
        rep = json.loads(r.stdout)
        return rep, rep["lanes"][0]["clerk"][0]

    adapter("A0 status text", ["status", "--registry", str(registry), "--intake", str(intake)])
    rep, o = status("A1 status json")
    expect("A1 returned, clean, unseen; event = sha256(0003) = witness",
           (o["state"], o["clean"], o["intake"]) == ("returned", True, "unseen") and o["event_sha256"] == real == witness, o["event_sha256"])
    adapter("A2 scan", ["intake", "scan", "--registry", str(registry), "--intake", str(intake)])
    r = adapter("A3 ack-clerk", ["intake", "ack-clerk", "--registry", str(registry), "--intake", str(intake), "--lane", "clerk",
                                 "--store", str(store), "--job", "demo-0001", "--event-sha256", o["event_sha256"], "--as", "codex-prime"])
    expect("A3 ack written", r.returncode == 0 and r.stdout.startswith("seen "), r.stdout.splitlines()[0])
    rep, o = status("A4 status after ack")
    expect("A4 seen, review not machine-readable, attention review-needed",
           o["intake"] == "seen" and o["review"] == "not-machine-readable"
           and any(x["kind"] == "review-needed" for x in rep["attention"]))
    r = adapter("A5 ack again", ["intake", "ack-clerk", "--registry", str(registry), "--intake", str(intake), "--lane", "clerk",
                                 "--store", str(store), "--job", "demo-0001", "--event-sha256", o["event_sha256"], "--as", "codex-prime"])
    expect("A5 idempotent", r.returncode == 0 and "already-recorded" in r.stdout)
    (store / "jobs/demo-0001/outbox/result.json").write_bytes(b'{"count":4}')  # fixture: a later artifact change
    rep, o2 = status("A6 artifact changed after ack")
    expect("A6 same event, still seen, not clean, attention kept",
           o2["event_sha256"] == o["event_sha256"] and o2["intake"] == "seen" and not o2["clean"]
           and any(x["kind"] == "clerk-not-clean" for x in rep["attention"]))
    for p in sorted(intake.rglob("*"), reverse=True):
        p.unlink() if p.is_file() else p.rmdir()
    intake.rmdir()
    rep, o3 = status("A7 acknowledgements deleted")
    expect("A7 unseen again, problems still visible",
           o3["intake"] == "unseen" and any(x["kind"] == "clerk-not-clean" for x in rep["attention"]))
    (out / "transcript.json").write_text(json.dumps(transcript, indent=1), encoding="utf-8")
    (out / "checks.json").write_text(json.dumps(checks, indent=1), encoding="utf-8")
    failed = [c for c in checks if not c["ok"]]
    for c in checks:
        print(("ok   " if c["ok"] else "FAIL ") + c["check"])
    adapter_calls = sum(1 for t in transcript if t["role"] == "adapter")
    print(f"scope: registered jobs only  processes {len(transcript)} (setup {len(transcript) - adapter_calls}, adapter {adapter_calls})"
          f"  checks {len(checks)}  failed {len(failed)}")
    print("demo ok" if not failed else "demo FAILED")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
