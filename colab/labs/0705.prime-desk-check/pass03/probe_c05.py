"""SUPPLEMENTARY PROBE (not part of the pass02 oracle run): C05 attribution with a fixture-completed copy.

  python -I -B probe_c05.py --baseline ABS(completed run_baseline --out) --pack05-02 ABS(source-manifest.json) --out NEW-ABS

The pass02 C05 fixture copies only the selector and 0420/06.01, while its catalog lists 0522/05.04, so the candidate
(correctly) reports that file missing, selects nothing and builds no packet (fixture defect FX-01 in pass02).
This probe copies the C05 fixture, ADDS the pack05.02 snapshot bytes of 0522/05.04 (labelled), and runs the same
pinned candidate, adapter and checker. Only C05 rows are meaningful. pass02 files are not changed.
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
from run_baseline import EXPECTED_SHA, keep, run, sha  # noqa: E402

ADD = "00.kernel/00.00.10.work/0522.review-construction/05.04.md"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--pack05-02", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    base, out = Path(a.baseline), Path(a.out)
    if not out.is_absolute() or os.path.lexists(out):
        print("refused: --out must be a new absolute path", file=sys.stderr)
        return 2
    pinned = base / "pinned"
    lab02 = pinned / "colab/labs/0705.prime-desk-check/pass02"
    cand = pinned / "labs/prime-desk-pass01/prime_desk.py"
    cand_sha = sha(cand.read_bytes())
    fixture = base / "fixtures" / "C05"
    man = json.loads(Path(a.pack05_02).read_bytes())
    row = next(r for r in man["sources"] if r["path"] == ADD)
    data = (Path(a.pack05_02).parent / row["snapshot"]).read_bytes()
    assert sha(data) == row["sha256"]
    run_dir = out / "runs" / "C05"
    shutil.copytree(fixture / "instance-A", run_dir / "book")
    target = run_dir / "book" / ADD
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "xb") as f:
        f.write(data)
    shadow = "0522.review-construction/05.04"
    prep = A.prepare_request(fixture, run_dir / "book", pinned, shadow)
    rec = {"schema": "desk-baseline-run-record/1", "case": "C05", "label": "SUPPLEMENTARY PROBE: fixture-completed copy (added 0522/05.04 snapshot bytes)",
           "added_file": {"path": ADD, "sha256": row["sha256"]}, "candidate_sha256": cand_sha, "request_sha256": prep["request_sha256"],
           "fixture_manifest_sha256": sha((fixture / "fixture-manifest.json").read_bytes())}
    argv_v = [cand, "view", "--request", prep["request_path"], "--json"]
    rec["view"] = keep(run_dir, "view", argv_v, run(argv_v, out))
    sel = (json.loads((run_dir / "view.stdout").read_bytes()).get("selected") or {}).get("id")
    if sel:
        argv_p = [cand, "packet", "--request", prep["request_path"], "--work-id", sel, "--json"]
        rec["packet"] = keep(run_dir, "packet", argv_p, run(argv_p, out))
    (run_dir / "run-record.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    obs, trace, conf = A.normalize(run_dir, cand_sha, fixture)
    (out / "observations").mkdir()
    (out / "observations" / "C05.json").write_text(json.dumps(obs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "mapping-trace-C05.json").write_text(json.dumps(trace, indent=1) + "\n", encoding="utf-8")
    c = run([lab02 / "check.py", "--expected", lab02 / "expected.json", "--expected-sha256", EXPECTED_SHA, "--fixtures", base / "fixtures",
             "--observations", out / "observations", "--json"], out)
    (out / "check-report.json").write_bytes(c.stdout)
    rep = json.loads(c.stdout)
    rows = [r for r in rep["rows"] if r["case"] == "C05"]
    q = [x for x in obs["quotes"]]
    summary = {"schema": "desk-supplementary-probe/1", "label": rec["label"], "c05_rows": rows,
               "quotes_mapped": q, "derived_expected_quote_sha256": json.loads((fixture / "fixture-manifest.json").read_bytes())["derived"]["C05_director_quote_sha256"],
               "note": "only C05 rows are meaningful; every other case is not-run here by design"}
    (out / "probe-summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
