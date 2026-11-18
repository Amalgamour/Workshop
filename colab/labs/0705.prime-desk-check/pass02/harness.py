"""Two-process lab harness: build fixtures, then check saved observations twice in separate processes.

  python -I -B harness.py --pack-manifest ABS --out ABS(new) [--observations ABS] [--manual-results ABS]

Without --observations it materializes SYNTHETIC self-test observations. The repeat in a new process is
HARNESS RESTART ONLY: it shows the lab's build/check is reproducible from files. It is not a desk restart.
Exit 0 when both check reports are byte-identical, 1 when they differ, 2 refused.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
PY = [sys.executable, "-I", "-B"]


def run(argv):
    p = subprocess.run(PY + [str(a) for a in argv], capture_output=True, timeout=300, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return {"argv": [str(a) for a in argv], "exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr.decode("utf-8", "replace")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--observations")
    ap.add_argument("--manual-results")
    a = ap.parse_args(argv)
    out = Path(a.out)
    if os.path.lexists(out) or not out.is_absolute():
        print("refused: --out must be a new absolute path", file=sys.stderr)
        return 2
    out.mkdir()
    exp = LAB / "expected.json"
    exp_sha = hashlib.sha256(exp.read_bytes()).hexdigest()
    steps = [run([LAB / "build_fixture.py", "--cases", LAB / "cases.json", "--manifest", a.pack_manifest, "--out", out / "fixtures"])]
    obs = Path(a.observations) if a.observations else out / "obs-synthetic"
    if not a.observations:
        steps.append(run([LAB / "synth_obs.py", "--expected", exp, "--fixtures", out / "fixtures", "--out", obs]))
    chk = [LAB / "check.py", "--expected", exp, "--expected-sha256", exp_sha, "--fixtures", out / "fixtures", "--observations", obs,
           "--manual-checklist", LAB / "manual-checklist.json"] + (["--manual-results", a.manual_results] if a.manual_results else [])
    first, second = run(chk), run(chk)
    steps += [first, second]
    same = first["stdout"] == second["stdout"] and first["exit"] == second["exit"]
    rep = json.loads(first["stdout"]) if first["stdout"].startswith(b"{") else {}
    summary = {"schema": "desk-lab-harness/1", "label": "HARNESS RESTART ONLY" + (" with SYNTHETIC observations" if not a.observations else ""),
               "expected_sha256": exp_sha, "reports_identical": same, "check_exit": first["exit"],
               "run_class": rep.get("run_class"), "desk_verdict": rep.get("desk_verdict"), "blocking": rep.get("blocking"),
               "assertions": rep.get("assertions", {}).get("by_status"),
               "steps": [{"argv": [x.replace(str(out), "<out>") for x in s["argv"]], "exit": s["exit"],
                          "stdout_sha256": hashlib.sha256(s["stdout"]).hexdigest(), "stderr": s["stderr"][:300]} for s in steps]}
    (out / "harness-summary.json").write_bytes((json.dumps(summary, indent=1) + "\n").encode("utf-8"))
    (out / "check-report.json").write_bytes(first["stdout"])
    sys.stdout.buffer.write((json.dumps(summary, indent=1) + "\n").encode("utf-8"))
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
