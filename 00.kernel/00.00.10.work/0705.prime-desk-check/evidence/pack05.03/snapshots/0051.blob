"""SYNTHETIC self-test observations for the 0705 pass02 checker. Not candidate output, not desk evidence.

  python -I -B synth_obs.py --expected ABS --fixtures ABS --out ABS(new dir)

Materializes, for every executable case, a desk-observation/1 that satisfies the frozen assertions
(first branch of each one-of), labelled producer.kind synthetic-self-test and adapter not-connected.
Tests then plant faults in copies. Exit 0 written, 2 refused.
"""
import argparse
import copy
import json
import os
import sys
from pathlib import Path

BASE = {"schema": "desk-observation/1", "case_id": None,
        "producer": {"kind": "synthetic-self-test", "adapter": {"id": "none (synthetic)", "sha256": None, "status": "not-connected"},
                     "raw_outputs": [], "unmapped": []},
        "instance": {"selected": "instance-A"}, "selected": {"work_ref": None, "basis": "unknown", "source": {"path": None, "sha256": None}},
        "parallel": [], "works": [], "attention": {"total": 0, "shown": 0, "overflow_route": None, "items": []},
        "holds": [], "coverage": [], "sources": [], "quotes": [], "workers": [], "refusals": [], "identity_fingerprint": "SYNTHETIC-fingerprint"}


def ref_value(v, fm):
    if isinstance(v, dict) and set(v) == {"fixture_file"}:
        inst, rel = v["fixture_file"]
        return fm["instances"][inst]["files"][rel]
    if isinstance(v, dict) and set(v) == {"fixture_derived"}:
        return fm["derived"][v["fixture_derived"]]
    if isinstance(v, dict):
        return {k: ref_value(x, fm) for k, x in v.items()}
    return v


def put(obs, path, value):
    cur = obs
    for i, step in enumerate(path):
        last = i == len(path) - 1
        if isinstance(step, dict):
            (k, v), = step.items()
            hits = [x for x in cur if isinstance(x, dict) and x.get(k) == v]
            if not hits:
                cur.append({k: v})
                hits = [cur[-1]]
            cur = hits[0]
            if last:
                cur.update(value)
        else:
            nxt = path[i + 1] if not last else None
            if last:
                cur[step] = value
            else:
                if step not in cur or cur[step] is None:
                    cur[step] = [] if isinstance(nxt, dict) else {}
                cur = cur[step]


def satisfy(obs, spec, fm):
    op = spec["op"]
    if op == "one-of":
        return satisfy(obs, spec["any_of"][0], fm)
    path, val = spec["path"], ref_value(spec.get("value"), fm)
    if op in ("eq", "ge"):
        put(obs, path, val)
    elif op == "in":
        put(obs, path, val[0])
    elif op == "null":
        put(obs, path, None)
    elif op == "contains":
        cur = obs
        for i, step in enumerate(path):
            last = i == len(path) - 1
            if isinstance(step, dict):
                (k, v), = step.items()
                hits = [x for x in cur if isinstance(x, dict) and x.get(k) == v]
                if not hits:
                    cur.append({k: v})
                    hits = [cur[-1]]
                cur = hits[0]
            else:
                if step not in cur or cur[step] is None:
                    cur[step] = [] if last else {}
                cur = cur[step]
        cur.append(dict(val))
    elif op == "overflow-consistent":
        att = obs["attention"]
        total = max(att.get("total") or 0, len(att["items"]))
        att["total"] = total
        att["shown"] = len(att["items"])
        att["overflow_route"] = "SYNTHETIC: expand with the attention drill-down" if total > att["shown"] else None
    elif op == "same-as-second":
        pass
    else:
        raise ValueError(op)


def build(expected, fixtures):
    out = {}
    for case in expected["executable_cases"]:
        fm = json.loads((fixtures / case / "fixture-manifest.json").read_bytes())
        obs = copy.deepcopy(BASE)
        obs["case_id"] = case
        specs = [s for s in expected["assertions"] if s["case"] == case]
        for s in sorted(specs, key=lambda s: s["op"] == "overflow-consistent"):
            satisfy(obs, s, fm)
        out[f"{case}.json"] = obs
        if case == "C14":
            out["C14.second.json"] = copy.deepcopy(obs)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--expected", required=True)
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    out = Path(a.out)
    if os.path.lexists(out):
        print(f"refused: {out} exists", file=sys.stderr)
        return 2
    obs = build(json.loads(Path(a.expected).read_bytes()), Path(a.fixtures))
    out.mkdir()
    for name, o in obs.items():
        with open(out / name, "xb") as f:
            f.write((json.dumps(o, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    print(json.dumps({"schema": "synthetic-observations/1", "label": "SYNTHETIC self-test observations; not desk evidence",
                      "out": str(out), "files": sorted(obs)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
