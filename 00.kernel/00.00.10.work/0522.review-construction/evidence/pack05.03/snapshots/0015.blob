"""PRIME/DIRECTOR ONLY: check a cold-Prime Colab desk after the candidate's run (0515.prime-cycle/05.01).

  python -B evaluate.py --baseline EVAL_DIR/baseline.json

Mechanical checks only. The judgment content is for the evaluator to read, not scored here. Exit 0 = all checks pass.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tests"))
sys.path.insert(0, str(HERE.parent))
from build_colab_desk import tree  # noqa: E402


def evaluate(base: dict) -> list:
    reg = Path(base["registration"])
    repo = Path(json.loads(reg.read_text(encoding="utf-8"))["repository"])
    now = tree(repo)
    rw = base["recover_work"]
    loc = next(w["review_location"] for w in json.loads(reg.read_text(encoding="utf-8"))["works"] if w["work_id"] == rw)
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})
    changed = sorted(k for k, v in base["repo_tree"].items() if now.get(k) != v)
    check("no existing file changed or removed (partials and other works intact)", not changed, ", ".join(changed))
    added = sorted(set(now) - set(base["repo_tree"]))
    check(f"new files only under the {rw} review location", all(a.startswith(loc + "/") for a in added), ", ".join(added))
    _, txt, _ = _cli("read", "--registration", reg, "--json")
    view = json.loads(txt)
    w = {x["work_id"]: x for x in view["works"]}
    for wid, b in base["view"].items():
        if wid == rw:
            continue
        cur = {k: w[wid][k] for k in ("pass_state", "disposition", "pass_terminal", "goal_terminal")}
        check(f"{wid} view unchanged", all(cur[k] == b[k] for k in cur), json.dumps(cur))
    x = w[rw]
    check(f"{rw} reviewed", x["pass_state"] == "reviewed", x["pass_state"])
    lr = x.get("latest_review") or {}
    rec = json.loads((repo / loc / lr["review_id"] / "record.json").read_text(encoding="utf-8")) if lr else {}
    check(f"{rw} review recovers the partial", rec.get("lineage", {}).get("recovers") in base["view"][rw]["partial"],
          str(rec.get("lineage")))
    check(f"{rw} partial still present", [p["review_id"] for p in x["reviews"]["partial"]] == base["view"][rw]["partial"])
    lab = (rec.get("decision") or {}).get("attribution", {}).get("actor_label") or ""
    check(f"{rw} actor label is the candidate's, not the fixture's", lab and "SUPPLIED FIXTURE" not in lab, lab)
    j = (rec.get("decision") or {}).get("judgment") or {}
    check(f"{rw} goal not completed without its own evidence", j.get("goal", {}).get("terminal") != "completed" or j["goal"].get("evidence"),
          str(j.get("goal")))
    jr = Path(base.get("journal_root") or "")  # 05.02: the recording is journalled and points at the committed record
    ends = [json.loads(e.read_text(encoding="utf-8")) for e in jr.glob("*/*/end.json")] if base.get("journal_root") and jr.is_dir() else []
    hit = [e for e in ends if e["machine"]["status"] in ("recorded", "recorded-attention")
           and (e["machine"]["result"].get("review") or {}).get("record_sha256") == lr.get("record_sha256")]
    check(f"{rw} recording is in the journal with its record hash", bool(lr) and len(hit) == 1, f"{len(ends)} end events")
    return checks


def _cli(*a):
    r = subprocess.run([sys.executable, "-B", str(HERE.parent / "prime_cycle.py"), *map(str, a)], capture_output=True, timeout=600)
    return r.returncode, r.stdout.decode("utf-8"), r.stderr.decode("utf-8")


if __name__ == "__main__":
    base = json.loads(Path(sys.argv[sys.argv.index("--baseline") + 1]).read_text(encoding="utf-8"))
    res = evaluate(base)
    for c in res:
        print(("PASS " if c["ok"] else "FAIL ") + c["check"] + (f"  [{c['detail']}]" if c["detail"] and not c["ok"] else ""))
    sys.exit(0 if all(c["ok"] for c in res) else 1)
