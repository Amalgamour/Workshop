"""Independent Colab probes for 0504/05.03. Runs only against a disposable copy.
python -B probes.py <copy-root> <out-file>"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WS = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
if "lib-build" in str(WS).lower().replace("\\", "/").split("/"):
    sys.exit("stop: refusing to probe the shared workspace")
sys.path.insert(0, str(WS / "app" / "tests"))
import test_entry as T  # noqa: E402  REPO resolves to the copy

assert T.REPO == WS, (T.REPO, WS)
PY = sys.executable
LIB = WS / "app" / "librarian.py"
CAND = T.CANDIDATE
log: list[str] = []
results: list[tuple[str, str, str]] = []


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tree() -> dict[str, str]:
    got = {}
    for p in WS.rglob("*"):
        rel = p.relative_to(WS).as_posix()
        if rel.startswith("app/scratch") or "/fixtures/probe-" in rel:
            continue
        if p.is_file():
            got[rel] = sha(p)
    return got


def run(args, cwd=None):
    proc = subprocess.run([PY, "-B", str(LIB), *args], cwd=str(cwd or tempfile.gettempdir()),
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    log.append(f"$ librarian.py {' '.join(args)}\nexit {proc.returncode}\nstdout:\n{proc.stdout}stderr:\n{proc.stderr}")
    return proc


def record(name, proc, want_exit, snippet=""):
    ok = proc.returncode == want_exit and (snippet in (proc.stderr + proc.stdout))
    ok = ok and "Traceback" not in proc.stderr
    results.append((("PASS" if ok else "FAIL"), name, f"exit {proc.returncode}: {(proc.stderr or proc.stdout).strip().splitlines()[-1] if (proc.stderr or proc.stdout).strip() else ''}"))


def junction(link: Path, target: Path) -> bool:
    made = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, text=True)
    return made.returncode == 0 and link.exists()


def marker_payload(root: Path, marker: Path) -> str:
    """Rewrite the planted payload so importing it creates marker. Stamp header kept."""
    page = root / "00.kernel/00.00.01.law/0310.inventory/02.inventory.py"
    text = page.read_text(encoding="utf-8")
    hook = f"\nfrom pathlib import Path as _P\n_P({str(marker)!r}).write_text('imported')\n"
    text = text.replace("from __future__ import annotations\n", "from __future__ import annotations\n" + hook, 1)
    page.write_bytes(text.encode("utf-8"))
    digest = sha(page)
    fx = json.loads((root / "fixture.json").read_text(encoding="utf-8"))
    fx["payload_sha256"] = digest
    (root / "fixture.json").write_bytes(T.lf(json.dumps(fx, indent=2) + "\n"))
    return digest


before = tree()
readme = WS / "app/README.md"
readme_sha = sha(readme)
scratch = WS / "app/scratch"
scratch.mkdir(parents=True, exist_ok=True)
digest = T.sha(T.PAYLOAD)
ext_parent = Path(tempfile.mkdtemp(prefix="colab0504-ext-"))

# P1 original APP-01 probe with a complete fixture tree planted in app/, output README.md
T.make_fixture(WS / "app")
fx = json.loads((WS / "app/fixture.json").read_text(encoding="utf-8"))
fx["output"] = "README.md"
fx["allowed_root"] = "."
(WS / "app/fixture.json").write_bytes(T.lf(json.dumps(fx, indent=2) + "\n"))
p = run(["test-run", "--root", str(WS / "app"), "--candidate", CAND, "--sha256", digest])
record("P1 complete fixture in app/, output README.md", p, 2, "fixture root is not a designated container")
results.append(("PASS" if sha(readme) == readme_sha else "FAIL", "P1 README bytes unchanged", sha(readme)))
for rel in ("fixture.json",):
    (WS / "app" / rel).unlink()
shutil.rmtree(WS / "app/00.kernel")

# P2 sibling prefix of the page fixtures container, and another page's fixtures folder
for name, rel in (("P2a sibling prefix fixtures-x", "00.kernel/00.00.10.work/0504.app-entry/fixtures-x"),
                  ("P2b other page fixtures", "00.kernel/00.00.10.work/0502.workflow-start/fixtures")):
    r = WS / rel
    T.make_fixture(r)
    p = run(["test-run", "--root", str(r), "--candidate", CAND, "--sha256", digest])
    record(name, p, 2, "fixture root is the live workspace")
    shutil.rmtree(r)

# P3 success in app/scratch, from a foreign cwd, with a case-varied root path
ok_root = scratch / "colab-ok"
T.make_fixture(ok_root)
varied = str(ok_root).replace("scratch", "SCRATCH")
p = run(["test-run", "--root", varied, "--candidate", CAND, "--sha256", digest])
record("P3 case-varied root in app/scratch succeeds", p, 0, "result: pass")
got = json.loads((ok_root / "output/inventory.json").read_text(encoding="utf-8"))
results.append(("PASS" if got == json.loads(T.EXPECTED.read_text(encoding="utf-8")) else "FAIL", "P3 inventory equals expected", ""))

# P4 explicit container naming the other designated container
p = run(["test-run", "--root", str(ok_root), "--container", str(WS / "00.kernel/00.00.10.work/0504.app-entry/fixtures"),
         "--candidate", CAND, "--sha256", digest])
record("P4 explicit container mismatch inside workspace", p, 2, "explicit container does not match")
p = run(["test-run", "--root", str(ok_root), "--container", str(scratch), "--candidate", CAND, "--sha256", digest])
record("P4b explicit container equal to the designated one", p, 0, "result: pass")

# P5 external container success, and external fixture root that is a junction into app/
box = ext_parent / "box"
froot = box / "fx"
T.make_fixture(froot)
p = run(["test-run", "--root", str(froot), "--container", str(box), "--candidate", CAND, "--sha256", digest])
record("P5a external container success", p, 0, "result: pass")
p = run(["test-run", "--root", str(froot), "--container", str(froot / "00.kernel"), "--candidate", CAND, "--sha256", digest])
record("P5b fixture root outside the named container", p, 2, "fixture root is outside the named container")
alias = box / "alias-app"
if junction(alias, WS / "app"):
    p = run(["test-run", "--root", str(alias), "--container", str(box), "--candidate", CAND, "--sha256", digest])
    record("P5c external root that is a junction to app/", p, 2, "fixture root is not a designated container")
    os.rmdir(alias)
else:
    results.append(("SKIP", "P5c junction", "mklink failed"))
calias = ext_parent / "alias-ws"
if junction(calias, WS):
    p = run(["test-run", "--root", str(froot), "--container", str(calias), "--candidate", CAND, "--sha256", digest])
    record("P5d named container is a junction to the workspace", p, 2, "")
    os.rmdir(calias)

# P6 output directory junction inside a designated container pointing at app/
jroot = scratch / "colab-junction"
T.make_fixture(jroot)
if junction(jroot / "output", WS / "app"):
    fx = json.loads((jroot / "fixture.json").read_text(encoding="utf-8"))
    fx["output"] = "output/README.md"
    (jroot / "fixture.json").write_bytes(T.lf(json.dumps(fx, indent=2) + "\n"))
    p = run(["test-run", "--root", str(jroot), "--candidate", CAND, "--sha256", digest])
    record("P6 output junction to app/ refused", p, 2, "path escapes the root")
    os.rmdir(jroot / "output")

# P7 refusal before payload import: marker payload at a refused root, and with a broken stamp
marker = ext_parent / "imported.marker"
mroot = WS / "00.kernel/00.00.10.work/0504.app-entry/colab-not-container"
T.make_fixture(mroot)
mdig = marker_payload(mroot, marker)
p = run(["test-run", "--root", str(mroot), "--candidate", CAND, "--sha256", mdig])
record("P7a marker payload at a refused root", p, 2, "")
results.append(("PASS" if not marker.exists() else "FAIL", "P7a payload not imported", str(marker.exists())))
shutil.rmtree(mroot)
sroot = scratch / "colab-stamp"
T.make_fixture(sroot)
pay = sroot / "00.kernel/00.00.01.law/0310.inventory/02.inventory.py"
mdig = marker_payload(sroot, marker)
pay.write_bytes(pay.read_bytes().replace(b"# state: draft\n", b"", 1))
mdig = sha(pay)
fx = json.loads((sroot / "fixture.json").read_text(encoding="utf-8"))
fx["payload_sha256"] = mdig
(sroot / "fixture.json").write_bytes(T.lf(json.dumps(fx, indent=2) + "\n"))
p = run(["test-run", "--root", str(sroot), "--candidate", CAND, "--sha256", mdig])
record("P7b broken stamp refused", p, 2, "")
results.append(("PASS" if not marker.exists() else "FAIL", "P7b payload not imported", str(marker.exists())))
p = run(["test-run", "--root", str(sroot), "--candidate", CAND, "--sha256", digest])
record("P7c CLI hash differs from fixture hash", p, 2, "")
results.append(("PASS" if not marker.exists() else "FAIL", "P7c payload not imported", str(marker.exists())))

# P8 is the payload limited to the reviewed one? A stamped, carded marker payload with matching hashes.
xroot = scratch / "colab-other-payload"
T.make_fixture(xroot)
xdig = marker_payload(xroot, marker)
p = run(["test-run", "--root", str(xroot), "--candidate", CAND, "--sha256", xdig])
results.append(("OBSERVE", "P8 unreviewed stamped payload with caller-supplied hash",
                f"exit {p.returncode}; imported={marker.exists()}; hash {xdig[:12]} vs reviewed {digest[:12]}"))
if marker.exists():
    marker.unlink()

# P9 hard link planted in a designated container at the payload's temporary name
hroot = scratch / "colab-hardlink"
T.make_fixture(hroot)
victim = WS / "app" / "README.md"
victim_before = victim.read_bytes()
(hroot / "output").mkdir()
try:
    os.link(victim, hroot / "output" / "inventory.json.tmp")
    linked = True
except OSError as exc:
    linked = False
    results.append(("SKIP", "P9 hard link", str(exc)))
if linked:
    p = run(["test-run", "--root", str(hroot), "--candidate", CAND, "--sha256", digest])
    changed = victim.read_bytes() != victim_before
    results.append(("FAIL" if changed else "PASS", "P9 hard-linked temp name leaves app/README.md unchanged",
                    f"exit {p.returncode}; README changed={changed}; sha now {sha(victim)[:12]}"))
    victim.write_bytes(victim_before)  # restore the disposable copy

# P10 predecessors in the copy
for rel, want in T.PINNED.items():
    if rel.startswith("00.kernel/00.00.01.law/0302.run/"):
        results.append(("PASS" if sha(WS / rel) == want else "FAIL", f"P10 predecessor pinned {rel}", ""))

after = tree()
diff = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
results.append(("PASS" if not diff else "FAIL", "copy tree outside scratch unchanged after restores", ", ".join(diff[:10])))
shutil.rmtree(ext_parent, ignore_errors=True)
for d in ("colab-ok", "colab-junction", "colab-stamp", "colab-other-payload", "colab-hardlink"):
    shutil.rmtree(scratch / d, ignore_errors=True)

text = "\n".join(f"{s}\t{n}\t{d}" for s, n, d in results)
OUT.write_text(text + "\n\n# log\n" + "\n".join(log), encoding="utf-8")
print(text)
