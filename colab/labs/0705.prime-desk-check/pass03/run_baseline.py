"""Run the pinned prime-desk-pass01 baseline against the pass02 fixtures and check it with the pinned pass02 checker.

  python -I -B run_baseline.py --pack05-03 ABS(source-manifest.json) --pack05-02 ABS(source-manifest.json) --out NEW-ABS

Everything executed is copied from pack05.03 snapshot bytes into <out>/pinned after hash checks.
Raw candidate stdout/stderr/exit are kept per run. Lab code; not product code. Exit 0 when the run completed
(whatever the desk verdict), 2 when refused.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import adapter as A  # noqa: E402

PY = [sys.executable, "-I", "-B"]
EXPECTED_SHA = "d44d237aa77b35b9e5728d5abdf43e705b0f850153a7761536861f55850d8e09"
PIN = {
    "labs/prime-desk-pass01/prime_desk.py": "labs/prime-desk-pass01/prime_desk.py",
    "app/context.py": "app/context.py",
    "colab/labs/0705.prime-desk-check/pass02/build_fixture.py": "colab/labs/0705.prime-desk-check/pass02/build_fixture.py",
    "colab/labs/0705.prime-desk-check/pass02/cases.json": "colab/labs/0705.prime-desk-check/pass02/cases.json",
    "colab/labs/0705.prime-desk-check/pass02/check.py": "colab/labs/0705.prime-desk-check/pass02/check.py",
    "colab/labs/0705.prime-desk-check/pass02/expected.json": "colab/labs/0705.prime-desk-check/pass02/expected.json",
    "colab/labs/0705.prime-desk-check/pass02/manual-checklist.json": "colab/labs/0705.prime-desk-check/pass02/manual-checklist.json",
}
SELECTOR = "00.kernel/00.00.10.work/0401.goal/06.01.md"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def pin_tree(manifest_path: Path, out: Path) -> dict:
    man = json.loads(manifest_path.read_bytes())
    rows = {r["path"]: r for r in man["sources"]}
    ids = {}
    for src, dst in PIN.items():
        r = rows[src]
        b = (manifest_path.parent / r["snapshot"]).read_bytes()
        if sha(b) != r["sha256"] or len(b) != r["bytes"]:
            raise SystemExit(f"refused: snapshot for {src} does not match its pin")
        p = out / "pinned" / dst
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "xb") as f:
            f.write(b)
        ids[src] = r["sha256"]
    return ids


def run(argv, cwd):
    p = subprocess.run(PY + [str(a) for a in argv], capture_output=True, timeout=300, cwd=str(cwd),
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return p


def keep(run_dir: Path, name: str, argv, p) -> dict:
    (run_dir / f"{name}.stdout").write_bytes(p.stdout)
    (run_dir / f"{name}.stderr").write_bytes(p.stderr)
    return {"argv": [Path(sys.executable).name, "-I", "-B"] + [str(a) for a in argv], "exit": p.returncode,
            "stdout_file": f"{name}.stdout", "stdout_sha256": sha(p.stdout), "stdout_bytes": len(p.stdout),
            "stderr_file": f"{name}.stderr", "stderr_sha256": sha(p.stderr)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack05-03", required=True)
    ap.add_argument("--pack05-02", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    out = Path(a.out)
    if not out.is_absolute() or os.path.lexists(out):
        print("refused: --out must be a new absolute path", file=sys.stderr)
        return 2
    out.mkdir()
    ids = pin_tree(Path(a.pack05_03), out)
    pinned = out / "pinned"
    lab02 = pinned / "colab/labs/0705.prime-desk-check/pass02"
    cand = pinned / "labs/prime-desk-pass01/prime_desk.py"
    cand_sha = sha(cand.read_bytes())
    summary = {"schema": "desk-baseline-run/1", "label": "REAL pinned-candidate execution on lab fixtures (SYNTHETIC request artifacts)",
               "python": sys.version.split()[0], "pins": ids, "candidate_sha256": cand_sha,
               "fixture_source_manifest_sha256": sha(Path(a.pack05_02).read_bytes()), "steps": []}
    b = run([lab02 / "build_fixture.py", "--cases", lab02 / "cases.json", "--manifest", a.pack05_02, "--out", out / "fixtures"], out)
    summary["steps"].append({"step": "build fixtures (pinned pass02 builder)", "exit": b.returncode, "stderr": b.stderr.decode("utf-8", "replace")[:400]})
    if b.returncode != 0:
        (out / "baseline-summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
        print("refused: fixture build failed", file=sys.stderr)
        return 2
    exp = json.loads((lab02 / "expected.json").read_bytes())
    snap_sel = None
    man02 = json.loads(Path(a.pack05_02).read_bytes())
    for r in man02["sources"]:
        if r["path"] == SELECTOR:
            snap_sel = (Path(a.pack05_02).parent / r["snapshot"]).read_bytes()
    shadow = A.canonical_snapshot_current_work(snap_sel)
    summary["shadow_selector_rule"] = {"work_ref": shadow, "from": "pinned pack05.02 snapshot of 0401/06.01 (R1); same for every case"}
    obs_dir, trace_dir, conf_dir = out / "observations", out / "mapping-trace", out / "conflicts"
    for d in (obs_dir, trace_dir, conf_dir):
        d.mkdir()
    for case in exp["executable_cases"]:
        fixture = out / "fixtures" / case
        run_dir = out / "runs" / case
        shutil.copytree(fixture / "instance-A", run_dir / "book")
        prep = A.prepare_request(fixture, run_dir / "book", pinned, shadow)
        rec = {"schema": "desk-baseline-run-record/1", "case": case, "candidate_path": "pinned/labs/prime-desk-pass01/prime_desk.py",
               "candidate_sha256": cand_sha, "request_sha256": prep["request_sha256"], "request_label": prep["label"],
               "shadow_selected_work_id": prep["shadow_selected_work_id"],
               "fixture_manifest_sha256": sha((fixture / "fixture-manifest.json").read_bytes()),
               "fixture_catalog_sha256": sha((fixture / "catalog.json").read_bytes())}
        argv_v = [cand, "view", "--request", prep["request_path"], "--json"]
        rec["view"] = keep(run_dir, "view", argv_v, run(argv_v, out))
        try:
            sel = (json.loads((run_dir / "view.stdout").read_bytes()).get("selected") or {}).get("id")
        except (ValueError, UnicodeDecodeError):
            sel = None
        if sel:
            argv_p = [cand, "packet", "--request", prep["request_path"], "--work-id", sel, "--json"]
            rec["packet"] = keep(run_dir, "packet", argv_p, run(argv_p, out))
        if case == "C14":
            rec["view_second"] = keep(run_dir, "view-second", argv_v, run(argv_v, out))
        (run_dir / "run-record.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
        try:
            obs, trace, conf = A.normalize(run_dir, cand_sha, fixture)
            (obs_dir / f"{case}.json").write_text(json.dumps(obs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            (trace_dir / f"{case}.json").write_text(json.dumps(trace, indent=1) + "\n", encoding="utf-8")
            (conf_dir / f"{case}.json").write_text(json.dumps(conf, indent=1) + "\n", encoding="utf-8")
            if case == "C14":
                obs2, trace2, _ = A.normalize(run_dir, cand_sha, fixture, view_key="view_second")
                (obs_dir / "C14.second.json").write_text(json.dumps(obs2, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
                (trace_dir / "C14.second.json").write_text(json.dumps(trace2, indent=1) + "\n", encoding="utf-8")
            summary["steps"].append({"step": f"{case}: view exit {rec['view']['exit']}" + (f", packet exit {rec['packet']['exit']}" if 'packet' in rec else "")
                                     + f"; adapted; conflicts {len(conf['conflicts'])}"})
        except A.AdapterRefused as e:
            summary["steps"].append({"step": f"{case}: adapter refused: {e}"})
    c = run([lab02 / "check.py", "--expected", lab02 / "expected.json", "--expected-sha256", EXPECTED_SHA, "--fixtures", out / "fixtures",
             "--observations", obs_dir, "--manual-checklist", lab02 / "manual-checklist.json", "--json"], out)
    (out / "check-report.json").write_bytes(c.stdout)
    (out / "check.stderr").write_bytes(c.stderr)
    summary["check"] = {"exit": c.returncode, "stdout_sha256": sha(c.stdout)}
    try:
        rep = json.loads(c.stdout)
        summary["check"].update(run_class=rep.get("run_class"), desk_verdict=rep.get("desk_verdict"),
                                assertions=rep.get("assertions"), manual=rep.get("manual", {}).get("by_status"))
    except ValueError:
        summary["check"]["parse"] = "report not JSON"
    (out / "baseline-summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("candidate_sha256", "shadow_selector_rule", "check")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
