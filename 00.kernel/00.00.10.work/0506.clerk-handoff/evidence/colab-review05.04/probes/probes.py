"""Claude's independent probes of the corrected Clerk (schema 2) and show --json (0506/05.05).
Disposable stores under %TEMP% only. python -B probes.py <lab-copy> <out.json>
Assertions are made against the real recorded files (0001/0002/0003/witness bytes), not against the tool's output."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LAB = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
if "lib-build" in str(LAB).lower():
    sys.exit("stop: run only against a disposable copy")
sys.path.insert(0, str(LAB))
import clerk  # noqa: E402

PY = sys.executable
TMP = Path(tempfile.mkdtemp(prefix="cr05-probes-"))
results = []
transcript = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cli(*args):
    r = subprocess.run([PY, "-B", str(LAB / "clerk.py"), *map(str, args)], capture_output=True, text=True,
                       encoding="utf-8", timeout=60)
    transcript.append({"argv": [str(a) for a in args], "exit": r.returncode, "stdout": r.stdout, "stderr": r.stderr})
    return r.returncode, r.stdout, r.stderr


def tree(root: Path):
    return {p.relative_to(root).as_posix(): (sha(p.read_bytes()) if p.is_file() else "dir")
            for p in sorted(root.rglob("*"))}


def note(status, name, detail=""):
    results.append({"status": status, "probe": name, "detail": detail})
    print(f"{status:8} {name} :: {detail}")


def check(name, cond, detail=""):
    note("ok" if cond else "FINDING", name, detail)


def setup(name, outputs=("count.py",)):
    root = TMP / name
    base = root / "base"
    base.mkdir(parents=True)
    task = b"count non-blank lines\n"
    (base / "task.txt").write_bytes(task)
    job = {"job_id": "job-1", "assignee": "builder-b", "reviewer": "codex-prime",
           "instructions": {"path": "task.txt", "sha256": sha(task)}, "release": "fixture release",
           "routed_by": "router-fixture", "expected_outputs": list(outputs)}
    jf = root / "job.json"
    jf.write_text(json.dumps(job), encoding="utf-8")
    return root, base, jf, root / "store"


def returned(name, evidence="scripted fixture"):
    root, base, jf, store = setup(name)
    assert cli("queue", "--store", store, "--job", jf, "--instructions-base", base)[0] == 0
    code, out, _ = cli("claim", "--store", store, "--job", "job-1", "--as", "builder-b", "--instructions-base", base)
    token = next(l.split()[1] for l in out.splitlines() if l.startswith("token "))
    jd = store / "jobs" / "job-1"
    (jd / "outbox" / "count.py").write_bytes(b"def count(t):\n    return sum(1 for l in t.splitlines() if l.strip())\n")
    rc = cli("return", "--store", store, "--job", "job-1", "--as", "builder-b", "--claim", token,
             "--delivery", "d-1", "--evidence", evidence)
    return root, base, store, jd, token, rc


def show_json(store, base=None, job="job-1"):
    args = ["show", "--store", store, "--job", job, "--json"] + (["--instructions-base", base] if base else [])
    before = tree(store) if Path(store).exists() else None
    code, out, err = cli(*args)
    after = tree(store) if Path(store).exists() else None
    try:
        doc = json.loads(out)
        one_doc = out.count("\n") == 1
    except ValueError:
        doc, one_doc = None, False
    return code, doc, err, before == after, one_doc


# R1 fields of a clean returned document against the real files
root, base, store, jd, token, rc = returned("r1")
check("R1 return exit 0", rc[0] == 0, rc[1].splitlines()[0])
q = json.loads((jd / "0001.queued.json").read_text(encoding="utf-8"))
c = json.loads((jd / "0002.claimed.json").read_text(encoding="utf-8"))
r_bytes = (jd / "0003.returned.json").read_bytes()
r = json.loads(r_bytes)
w = json.loads((jd / "0003.witness.json").read_text(encoding="utf-8"))
code, doc, err, ro, one = show_json(store, base)
check("R1 show --json exit 0, one JSON document, no stderr, read-only", code == 0 and one and err == "" and ro, f"exit {code}")
check("R1 job equals the recorded 0001 job object", doc["job"] == q["job"])
check("R1 assignee/reviewer/outputs from the record", (doc["job"]["assignee"], doc["job"]["reviewer"], doc["job"]["expected_outputs"])
      == ("builder-b", "codex-prime", ["count.py"]))
check("R1 claim token and by equal 0002", doc["claim"] == {"by": c["by"], "token": c["claim"]} and c["claim"] == token)
check("R1 returned delivery/evidence/artifacts equal 0003", doc["returned"] == {"by": r["by"], "delivery": r["delivery"],
                                                                                 "evidence": r["evidence"], "artifacts": r["artifacts"]})
art = (jd / "outbox" / "count.py").read_bytes()
check("R1 artifact hash equals the outbox file", r["artifacts"][0]["sha256"] == sha(art) and r["artifacts"][0]["bytes"] == len(art))
check("R1 witness digest equals sha256 of 0003 bytes", w["sha256"] == sha(r_bytes) and w["job_id"] == "job-1")
check("R1 checks all ok with a base", doc["checks"] == {"events": "ok", "completion": "ok", "artifacts": "ok", "instructions": "usable"},
      json.dumps(doc["checks"]))
exposed = json.dumps(doc)
check("R1 JSON exposes no 0003 event digest or witness digest", sha(r_bytes) not in exposed,
      "OBSERVE: a consumer cannot get the returned event's identity from show --json")
code, doc_nb, _, ro, _ = show_json(store)
check("R1b without a base: instructions not-checked, exit 0 (absent check, not verified)",
      doc_nb["checks"]["instructions"] == "not-checked" and code == 0 and ro, f"exit {code}")
code, out, _ = cli("show", "--store", store, "--job", "job-1")
check("R1c human show still prints the claim token (seam replay path)", f"claim {token}" in out)

# R2 isolated completion loss/corruption
cases = {
    "R2a event deleted, witness kept": lambda jd: (jd / "0003.returned.json").unlink(),
    "R2b witness deleted, event kept": lambda jd: (jd / "0003.witness.json").unlink(),
    "R2c one byte changed in 0003": lambda jd: (jd / "0003.returned.json").write_bytes(
        (jd / "0003.returned.json").read_bytes().replace(b"d-1", b"d-2", 1)),
    "R2d witness truncated": lambda jd: (jd / "0003.witness.json").write_bytes((jd / "0003.witness.json").read_bytes()[:10]),
    "R2e witness valid JSON but wrong job_id": lambda jd: (jd / "0003.witness.json").write_bytes(
        clerk.canonical(dict(json.loads((jd / "0003.witness.json").read_text(encoding="utf-8")), job_id="job-2"))),
    "R2f witness with an extra key": lambda jd: (jd / "0003.witness.json").write_bytes(
        clerk.canonical(dict(json.loads((jd / "0003.witness.json").read_text(encoding="utf-8")), extra=1))),
    "R2g 0003 lost only its trailing newline": lambda jd: (jd / "0003.returned.json").write_bytes(
        (jd / "0003.returned.json").read_bytes().rstrip(b"\n")),
    "R2h planted 0004.completion.json": lambda jd: (jd / "0004.completion.json").write_bytes(b"{}"),
}
for i, (name, damage) in enumerate(cases.items()):
    root, base, store, jd, token, rc = returned(f"r2-{i}")
    damage(jd)
    code, doc, err, ro, one = show_json(store, base)
    clean = doc and doc["state"] == "returned" and not doc["problems"]
    check(name + ": not a clean returned document, exit 2, read-only, one JSON",
          not clean and code == 2 and ro and one and doc["returned"] is None and doc["job"] is None,
          f"exit {code} state {doc and doc['state']} completion {doc and doc['checks']['completion']}")
    vcode, vout, _ = cli("verify", "--store", store)
    icode, iout, _ = cli("inbox", "--store", store, "--as", "codex-prime")
    check(name + ": verify exit 2 and reviewer inbox discloses it", vcode == 2 and "section incomplete\nnone" not in iout,
          f"verify {vcode} inbox {icode}")
    before = tree(store)
    rcode, rout, _ = cli("return", "--store", store, "--job", "job-1", "--as", "builder-b", "--claim", token,
                         "--delivery", "d-9", "--evidence", "different")
    check(name + ": a different re-return refuses and writes nothing", rcode == 2 and tree(store) == before, rout.splitlines()[0])

# R3 coherent deletion of both completion files (documented limit, not a finding)
root, base, store, jd, token, rc = returned("r3")
(jd / "0003.returned.json").unlink()
(jd / "0003.witness.json").unlink()
code, doc, err, ro, one = show_json(store, base)
note("LIMIT", "R3 both completion files deleted reads as a clean claim", f"state {doc['state']} exit {code} (documented limit)")

# R4 required fields
root, base, jf, store = setup("r4", outputs=())
code, out, _ = cli("queue", "--store", store, "--job", jf, "--instructions-base", base)
check("R4a empty expected_outputs refused, nothing written", code == 2 and not store.exists(), out.splitlines()[0])
for label, ev in (("R4b blank", "   "), ("R4c tab inside", "line one\tline two"), ("R4d newline inside", "line one\nline two")):
    root, base, jf, store = setup("r4" + label[2])
    cli("queue", "--store", store, "--job", jf, "--instructions-base", base)
    _, out, _ = cli("claim", "--store", store, "--job", "job-1", "--as", "builder-b", "--instructions-base", base)
    token = next(l.split()[1] for l in out.splitlines() if l.startswith("token "))
    (store / "jobs/job-1/outbox/count.py").write_bytes(b"x\n")
    before = tree(store)
    code, out, _ = cli("return", "--store", store, "--job", "job-1", "--as", "builder-b", "--claim", token,
                       "--delivery", "d-1", "--evidence", ev)
    status = "ok" if label.endswith("blank") else "OBSERVE"
    note(status if code == 2 and tree(store) == before else "FINDING", f"{label} evidence refused, nothing written",
         f"exit {code}: {out.splitlines()[0]}")

# R5 stale instructions and changed artifact
root, base, store, jd, token, rc = returned("r5")
(base / "task.txt").write_bytes(b"changed\n")
code, doc, _, ro, _ = show_json(store, base)
check("R5a stale instructions: unusable, exit 1, recorded hash kept", doc["checks"]["instructions"] == "unusable" and code == 1 and ro
      and doc["job"]["instructions"]["sha256"] == sha(b"count non-blank lines\n"), f"exit {code}")
code, doc, _, ro, _ = show_json(store)
check("R5b stale instructions without a base: not-checked, exit 0", doc["checks"]["instructions"] == "not-checked" and code == 0,
      "OBSERVE: exit 0 with an unchecked instruction file")
root, base, store, jd, token, rc = returned("r5c")
(jd / "outbox" / "count.py").write_bytes(b"changed\n")
code, doc, _, ro, _ = show_json(store, base)
check("R5c changed artifact: state returned, checks.artifacts changed, exit 1, recorded hash unchanged",
      doc["state"] == "returned" and doc["checks"]["artifacts"] == "changed" and code == 1 and ro
      and doc["returned"]["artifacts"][0]["sha256"] != sha(b"changed\n"), f"exit {code}")
note("OBSERVE", "R5d no single 'clean' field", "a consumer must combine exit code, state, checks and problems")

# R6 idempotent resend and conflict
root, base, store, jd, token, rc = returned("r6")
before = tree(store)
code, out, _ = cli("return", "--store", store, "--job", "job-1", "--as", "builder-b", "--claim", token,
                   "--delivery", "d-1", "--evidence", "scripted fixture")
check("R6a identical resend: already-recorded, no byte changes", code == 0 and "already-recorded" in out and tree(store) == before)
code, out, _ = cli("return", "--store", store, "--job", "job-1", "--as", "builder-b", "--claim", token,
                   "--delivery", "d-1", "--evidence", "other evidence")
check("R6b same delivery, different evidence: conflict, nothing written", code == 2 and "conflict" in out and tree(store) == before)

# R7 expected read failures (in-process), JSON stays valid and read-only
root, base, store, jd, token, rc = returned("r7")
real_read = Path.read_bytes


def failing(self):
    if self.name == "0003.returned.json":
        raise PermissionError(13, "Permission denied")
    return real_read(self)


before = tree(store)
Path.read_bytes = failing
try:
    res = clerk.show(str(store), "job-1", str(base), as_json=True)
finally:
    Path.read_bytes = real_read
doc = json.loads(res.text)
check("R7a 0003 unreadable: valid JSON, exit 2, not returned, read-only",
      res.code == 2 and doc["state"] != "returned" and doc["returned"] is None and tree(store) == before,
      f"state {doc['state']} problems {doc['problems']}")
real_listdir = os.listdir


def failing_listdir(p):
    if str(p).endswith("job-1"):
        raise PermissionError(13, "Permission denied")
    return real_listdir(p)


os.listdir = failing_listdir
try:
    res = clerk.show(str(store), "job-1", str(base), as_json=True)
finally:
    os.listdir = real_listdir
doc = json.loads(res.text)
check("R7b job directory unreadable: valid JSON, exit 2", res.code == 2 and doc["state"] in ("corrupt", "unknown"), f"state {doc['state']}")

# R8 earlier schema-1 store is named and refused
root, base, store, jd, token, rc = returned("r8")
for name in ("0001.queued.json",):
    p = jd / name
    p.write_bytes(p.read_bytes().replace(b"clerk-handoff-pass02/2", b"clerk-handoff-pass02/1"))
code, doc, _, ro, _ = show_json(store, base)
check("R8 schema-1 event: not clean, exit 2, read-only", code == 2 and doc["state"] != "returned" and ro,
      f"state {doc['state']} detail {doc['problems'][0]['detail'] if doc['problems'] else ''}")

# R9 events check wording when only completion is missing
root, base, store, jd, token, rc = returned("r9")
(jd / "0003.witness.json").unlink()
code, doc, _, _, _ = show_json(store, base)
note("OBSERVE", "R9 witness missing reports checks.events 'broken'", f"events {doc['checks']['events']} completion {doc['checks']['completion']}; 0001/0002 chain is intact")

# R10 CLI syntax error stays argparse; no stdout document
code, out, err = cli("show", "--store", TMP / "nope", "--json", "--bogus")
check("R10 argparse error: exit 2, empty stdout", code == 2 and out == "", err.strip().splitlines()[-1] if err.strip() else "")

shutil.rmtree(TMP, ignore_errors=True)
OUT.write_text(json.dumps({"results": results, "transcript_calls": len(transcript)}, indent=1), encoding="utf-8")
(OUT.parent / "probes-transcript.json").write_text(json.dumps(transcript, indent=1), encoding="utf-8")
print("total", len(results), "findings", sum(r["status"] == "FINDING" for r in results))
