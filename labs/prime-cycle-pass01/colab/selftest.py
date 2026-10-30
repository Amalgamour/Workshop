"""PRIME/DIRECTOR ONLY: check the Colab builder and evaluator themselves on disposable desks (no model).

  python -B -X dev selftest.py

1. A simulated correct recovery of W5 passes every evaluator check.
2. A simulated run that edits the W5 partial and the W2 page fails the matching checks.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tests"))
sys.path.insert(0, str(HERE.parent))
import fixture as F  # noqa: E402
import prime_cycle as pc  # noqa: E402
import build_colab_desk as B  # noqa: E402
import evaluate as E  # noqa: E402


def recover(base, actor="Cold Prime (SIMULATED by selftest)"):
    reg = Path(base["registration"])
    _, txt, _ = E._cli("read", "--registration", reg, "--json")
    w = next(x for x in json.loads(txt)["works"] if x["work_id"] == "W5")
    d = F.fill(w["template"], "accept-finished-open", actor=actor)
    d["recovers"] = base["view"]["W5"]["partial"][0]
    p = Path(base["desk"]) / "sim-decision.json"  # outside the repository, beside the registration
    p.write_text(json.dumps(d), encoding="utf-8")
    return pc.record(reg, p)


def run():
    results = {}
    for case in ("correct", "edits-partial-and-other-page"):
        ev = Path(tempfile.mkdtemp(prefix="pcy-colab-eval-")) / "eval"
        base = B.build(ev)
        try:
            v0 = base["view"]
            assert [v0[k]["pass_state"] for k in ("W1", "W2", "W3", "W4", "W5")] == \
                ["awaiting-review", "reviewed", "reviewed", "reviewed", "awaiting-review"], v0
            assert (v0["W2"]["goal_terminal"], v0["W3"]["goal_terminal"], v0["W4"]["disposition"]) == ("open", "completed", "held"), v0
            assert len(v0["W5"]["partial"]) == 1, v0
            repo = Path(json.loads(Path(base["registration"]).read_text(encoding="utf-8"))["repository"])
            if case != "correct":
                part = next(repo.rglob(f"{v0['W5']['partial'][0]}/REVIEW.md"))
                part.write_bytes(part.read_bytes() + b"finished by hand\n")
                page = repo / F.BOOK / "0592.colab-w2" / "05.01.md"
                page.write_bytes(page.read_bytes() + b"edited\n")
            code, out = recover(base)
            checks = E.evaluate(base)
            results[case] = {"record_exit": code, "failed": [c["check"] for c in checks if not c["ok"]], "count": len(checks)}
        finally:
            shutil.rmtree(base["desk"], onexc=F.writable_retry)
            shutil.rmtree(ev.parent, onexc=F.writable_retry)
    print(json.dumps(results, indent=1))
    ok = results["correct"]["failed"] == [] and \
        {"no existing file changed or removed (partials and other works intact)", "W2 view unchanged"} <= set(results["edits-partial-and-other-page"]["failed"]) \
        if results["edits-partial-and-other-page"]["record_exit"] is not None else False
    return ok


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
