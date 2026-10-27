"""Add-on probes: human show/verify/inbox are read-only on damaged stores; outbox-creation OSError after a claim event.
python -B probes2.py <lab-copy> <out.json>"""
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
    sys.exit("stop: disposable copy only")
sys.path.insert(0, str(LAB))
import clerk  # noqa: E402

PY = sys.executable
TMP = Path(tempfile.mkdtemp(prefix="cr05-probes2-"))
results = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cli(*args):
    r = subprocess.run([PY, "-B", str(LAB / "clerk.py"), *map(str, args)], capture_output=True, text=True, encoding="utf-8", timeout=60)
    return r.returncode, r.stdout, r.stderr


def tree(root):
    return {p.relative_to(root).as_posix(): (sha(p.read_bytes()) if p.is_file() else "dir") for p in sorted(Path(root).rglob("*"))}


def check(name, cond, detail=""):
    results.append({"status": "ok" if cond else "FINDING", "probe": name, "detail": detail})
    print(("ok       " if cond else "FINDING  ") + name + " :: " + detail)


def setup(name):
    root = TMP / name
    base = root / "base"
    base.mkdir(parents=True)
    (base / "task.txt").write_bytes(b"t\n")
    job = {"job_id": "job-1", "assignee": "builder-b", "reviewer": "codex-prime",
           "instructions": {"path": "task.txt", "sha256": sha(b"t\n")}, "release": "r", "routed_by": "x",
           "expected_outputs": ["count.py"]}
    (root / "job.json").write_text(json.dumps(job), encoding="utf-8")
    store = root / "store"
    cli("queue", "--store", store, "--job", root / "job.json", "--instructions-base", base)
    return root, base, store


damages = {
    "event deleted": lambda jd: (jd / "0003.returned.json").unlink(),
    "witness deleted": lambda jd: (jd / "0003.witness.json").unlink(),
    "event byte changed": lambda jd: (jd / "0003.returned.json").write_bytes((jd / "0003.returned.json").read_bytes().replace(b"d-1", b"d-2")),
    "queued event changed": lambda jd: (jd / "0001.queued.json").write_bytes((jd / "0001.queued.json").read_bytes().replace(b'"r"', b'"q"')),
}
for i, (name, damage) in enumerate(damages.items()):
    root, base, store = setup(f"h{i}")
    _, out, _ = cli("claim", "--store", store, "--job", "job-1", "--as", "builder-b", "--instructions-base", base)
    token = next(l.split()[1] for l in out.splitlines() if l.startswith("token "))
    (store / "jobs/job-1/outbox/count.py").write_bytes(b"x\n")
    cli("return", "--store", store, "--job", "job-1", "--as", "builder-b", "--claim", token, "--delivery", "d-1", "--evidence", "e")
    damage(store / "jobs/job-1")
    before = tree(store)
    codes = []
    for args in (["show", "--store", store, "--job", "job-1"], ["show", "--store", store, "--job", "job-1", "--instructions-base", base],
                 ["verify", "--store", store], ["inbox", "--store", store, "--as", "codex-prime"],
                 ["inbox", "--store", store, "--as", "builder-b"], ["show", "--store", store, "--job", "job-1", "--json"]):
        c, o, e = cli(*args)
        codes.append(c)
        if "Traceback" in o + e:
            codes.append("traceback")
    check(f"H {name}: human show/verify/inbox and json are read-only and exit 2 without traceback",
          tree(store) == before and all(c == 2 for c in codes), f"codes {codes}")

# outbox creation fails after the claim event exists (in-process)
root, base, store = setup("ob")
real_mkdir = os.mkdir


def failing_mkdir(p, *a, **k):
    if str(p).endswith("outbox"):
        raise PermissionError(13, "Permission denied")
    return real_mkdir(p, *a, **k)


os.mkdir = failing_mkdir
try:
    res = clerk.claim(str(store), "job-1", "builder-b", str(base))
finally:
    os.mkdir = real_mkdir
claimed = json.loads((store / "jobs/job-1/0002.claimed.json").read_text(encoding="utf-8"))
check("O outbox OSError after claim event: exit 2, names the existing token, no new token",
      res.code == 2 and f"existing token {claimed['claim']}" in res.text and "no new token" in res.text, res.text.replace("\n", " | "))
before = tree(store)
c, o, _ = cli("claim", "--store", store, "--job", "job-1", "--as", "builder-b", "--instructions-base", base, "--resume")
c2, o2, _ = cli("claim", "--store", store, "--job", "job-1", "--as", "builder-b", "--instructions-base", base)
check("O then resume and claim both refuse and write nothing (claim without outbox stays incomplete)",
      c == 2 and c2 == 2 and tree(store) == before, f"{o.splitlines()[0]} / {o2.splitlines()[0]}")

shutil.rmtree(TMP, ignore_errors=True)
OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")
print("total", len(results), "findings", sum(r["status"] == "FINDING" for r in results))
