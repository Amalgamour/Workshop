"""Check saved desk observations against the frozen 0705 pass02 expected manifest.

  python -I -B check.py --expected ABS --expected-sha256 HEX --fixtures ABS --observations ABS
                        [--manual-checklist ABS] [--manual-results ABS] [--json]

Consumes saved observation files (<case>.json, plus C14.second.json) written by an adapter or by the
lab's synthetic self-tests. It never runs a desk tool. See the lab CONTRACT (0705 evidence/return05.02).
Exit 0 only when desk_verdict is pass; 1 for any other completed report; 2 for refused or checker-error.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

STATUSES = ["pass", "wrong", "missing", "unsupported", "needs-human-assessment", "not-run", "checker-error"]
OBS_KEYS = {"schema", "case_id", "producer", "instance", "selected", "parallel", "works", "attention", "holds",
            "coverage", "sources", "quotes", "workers", "refusals", "identity_fingerprint"}
_MISSING = object()


class Refused(Exception):
    pass


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def strict_load(path: Path):
    def pairs(items):
        keys = [k for k, _ in items]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate key")
        return dict(items)
    return json.loads(path.read_bytes().decode("utf-8"), object_pairs_hook=pairs)


def resolve(obj, path):
    cur = obj
    for step in path:
        if isinstance(step, dict):
            if not isinstance(cur, list):
                return _MISSING
            (k, v), = step.items()
            hits = [x for x in cur if isinstance(x, dict) and x.get(k) == v]
            if len(hits) != 1:
                return _MISSING
            cur = hits[0]
        else:
            if not isinstance(cur, dict) or step not in cur:
                return _MISSING
            cur = cur[step]
    return cur


def unmapped(obs, path):
    prefixes = (obs.get("producer") or {}).get("unmapped") or []
    flat = [s if isinstance(s, str) else next(iter(s)) for s in path or []]
    for p in prefixes:
        pp = p if isinstance(p, list) else [p]
        if flat[:len(pp)] == pp:
            return True
    return False


def ref_value(v, fm):
    if isinstance(v, dict) and set(v) == {"fixture_file"}:
        inst, rel = v["fixture_file"]
        return fm["instances"][inst]["files"][rel]
    if isinstance(v, dict) and set(v) == {"fixture_derived"}:
        return fm["derived"][v["fixture_derived"]]
    if isinstance(v, dict):
        return {k: ref_value(x, fm) for k, x in v.items()}
    return v


def evaluate(spec, obs, fm, second):
    """Return (status, detail) for one assertion on one parsed observation."""
    op = spec["op"]
    if op == "one-of":
        subs = [evaluate(s, obs, fm, second) for s in spec["any_of"]]
        if any(s == "pass" for s, _ in subs):
            return "pass", "a branch passed"
        if all(s == "unsupported" for s, _ in subs):
            return "unsupported", "all branches unmapped"
        if any(s == "wrong" for s, _ in subs):
            return "wrong", "; ".join(d for _, d in subs)
        return "missing", "; ".join(d for _, d in subs)
    path = spec["path"]
    if unmapped(obs, path):
        return "unsupported", f"path {path} is declared unmapped by the adapter"
    got = resolve(obs, path)
    if got is _MISSING:
        return "missing", f"path {path} does not resolve"
    want = ref_value(spec.get("value"), fm)
    if op == "eq":
        return ("pass", "") if got == want else ("wrong", f"got {got!r}, want {want!r}")
    if op == "ne":
        return ("pass", "") if got != want else ("wrong", f"got {got!r}, must differ")
    if op == "in":
        return ("pass", "") if got in want else ("wrong", f"got {got!r}, want one of {want!r}")
    if op == "ge":
        return ("pass", "") if isinstance(got, (int, float)) and not isinstance(got, bool) and got >= want else ("wrong", f"got {got!r}, want >= {want!r}")
    if op == "null":
        return ("pass", "") if got is None else ("wrong", f"got {got!r}, want null")
    if op == "present":
        return ("pass", "") if got is not None else ("wrong", "null")
    if op == "contains":
        if not isinstance(got, list):
            return "wrong", "not a list"
        ok = any(isinstance(x, dict) and all(x.get(k, _MISSING) == v for k, v in want.items()) for x in got)
        return ("pass", "") if ok else ("wrong", f"no item matching {want!r}")
    if op == "overflow-consistent":
        if not isinstance(got, dict) or not all(isinstance(got.get(k), int) for k in ("total", "shown")):
            return "wrong", "attention total/shown missing or not integers"
        hidden = got["total"] - got["shown"]
        items = got.get("items") or []
        if hidden < 0 or len(items) != got["shown"]:
            return "wrong", f"shown={got['shown']} items={len(items)} total={got['total']}"
        if hidden > 0 and not got.get("overflow_route"):
            return "wrong", f"{hidden} items hidden without an overflow route"
        return "pass", f"hidden {hidden}"
    if op == "same-as-second":
        if second is None:
            return "not-run", "second observation absent"
        other = resolve(second, path)
        if other is _MISSING:
            return "missing", "path absent in second observation"
        return ("pass", "") if other == got else ("wrong", f"first {got!r} != second {other!r}")
    raise Refused(f"unknown op {op}")


def load_obs(path: Path):
    if not path.is_file():
        return None, "absent"
    try:
        o = strict_load(path)
    except (ValueError, UnicodeDecodeError) as e:
        return None, f"malformed: {e}"
    if not isinstance(o, dict) or set(o) != OBS_KEYS or o.get("schema") != "desk-observation/1":
        return None, "malformed: not a desk-observation/1 object with exact keys"
    return o, "ok"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--expected", required=True)
    ap.add_argument("--expected-sha256", required=True)
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--observations", required=True)
    ap.add_argument("--manual-checklist")
    ap.add_argument("--manual-results")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        exp_bytes = Path(a.expected).read_bytes()
        if sha(exp_bytes) != a.expected_sha256:
            raise Refused(f"expected manifest sha256 {sha(exp_bytes)} is not the pinned {a.expected_sha256}")
        exp = strict_load(Path(a.expected))
        fixtures, obs_dir = Path(a.fixtures), Path(a.observations)
        rows, producers, adapters, obs_state = [], set(), set(), {}
        for case in exp["executable_cases"]:
            fm_path = fixtures / case / "fixture-manifest.json"
            fm = strict_load(fm_path) if fm_path.is_file() else None
            obs, state = load_obs(obs_dir / f"{case}.json")
            second = None
            if case == "C14":
                second, s2 = load_obs(obs_dir / "C14.second.json")
            obs_state[case] = state if obs is None else "observed"
            if obs is not None:
                producers.add((obs["producer"] or {}).get("kind"))
                adapters.add(((obs["producer"] or {}).get("adapter") or {}).get("status"))
            for spec in [x for x in exp["assertions"] if x["case"] == case]:
                if fm is None:
                    st, d = "checker-error", f"fixture manifest missing: {fm_path}"
                elif obs is None:
                    st, d = ("not-run", "observation absent") if state == "absent" else ("wrong", state)
                elif obs.get("case_id") != case:
                    st, d = "wrong", f"observation case_id {obs.get('case_id')!r}"
                else:
                    try:
                        st, d = evaluate(spec, obs, fm, second)
                    except (KeyError, TypeError, ValueError) as e:
                        st, d = "checker-error", f"{type(e).__name__}: {e}"
                rows.append({"id": spec["id"], "case": case, "status": st, "detail": d, "mandatory": spec["mandatory"]})
        manual_rows = []
        if a.manual_checklist:
            items = strict_load(Path(a.manual_checklist))["items"]
            answers = {}
            if a.manual_results:
                for r in strict_load(Path(a.manual_results)).get("items", []):
                    answers[r.get("id")] = r
            for it in items:
                r = answers.get(it["id"])
                if not r or not r.get("by") or not r.get("date"):
                    st = "needs-human-assessment"
                else:
                    st = "pass" if r.get("answer") == "yes" else "wrong"
                manual_rows.append({"id": it["id"], "status": st, "by": (r or {}).get("by"), "answer": (r or {}).get("answer")})
    except (Refused, OSError, ValueError, KeyError) as e:
        report = {"schema": "desk-check-report/1", "result": "checker-error", "detail": f"{type(e).__name__}: {e}"}
        sys.stdout.buffer.write((json.dumps(report, indent=1) + "\n").encode("utf-8"))
        return 2
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in STATUSES}
    mcounts = {s: sum(1 for r in manual_rows if r["status"] == s) for s in STATUSES}
    synthetic = producers == {"synthetic-self-test"}
    blocking = []
    if not producers:
        blocking.append("no observation was supplied")
    if "synthetic-self-test" in producers:
        blocking.append("synthetic-only or mixed observations: not desk evidence")
    if any(x != "connected" for x in adapters) or not adapters:
        blocking.append("adapter-not-connected")
    nr = [c for c, s in obs_state.items() if s != "observed"]
    if nr:
        blocking.append("cases not observed: " + ",".join(nr))
    for s in STATUSES[1:]:
        ids = [r["id"] for r in rows if r["status"] == s and r["mandatory"]]
        if ids:
            blocking.append(f"{s}: " + ",".join(ids))
    if not a.manual_checklist:
        blocking.append("manual checklist not supplied")
    elif any(r["status"] != "pass" for r in manual_rows):
        blocking.append("manual: " + ",".join(f"{r['id']}={r['status']}" for r in manual_rows if r["status"] != "pass"))
    if synthetic:
        verdict = "not-applicable (synthetic self-test)"
    else:
        verdict = "pass" if not blocking else "not-passed"
    report = {"schema": "desk-check-report/1",
              "run_class": "synthetic-self-test" if synthetic else ("candidate" if producers == {"candidate"} else "mixed-or-empty"),
              "desk_verdict": verdict, "blocking": blocking,
              "expected_sha256": a.expected_sha256,
              "cases": {"executable_defined": len(exp["executable_cases"]), "manual_defined": len(exp["manual_cases"]),
                        "observed": sum(1 for s in obs_state.values() if s == "observed"), "observation_state": obs_state},
              "assertions": {"defined": len(exp["assertions"]), "evaluated": len(rows), "by_status": counts},
              "manual": {"defined": len(manual_rows), "by_status": mcounts},
              "rows": rows, "manual_rows": manual_rows,
              "limits": "checks normalized facts only; forbidden inferences and readability are manual items; not a semantic judge"}
    sys.stdout.buffer.write((json.dumps(report, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
