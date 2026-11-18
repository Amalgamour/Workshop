#!/usr/bin/env python3
"""Reporter-obligation judge v2 (0707/05.25; Prime 0522/06.40 controlled observations). EQUIPMENT ONLY.

The pass03 judge (labs/loop-convergence-harness-pass03/reporter_judges.py, hash-pinned, unchanged) covers read/recover.
v2 adds the core INSPECT and PREPARE results the reporter must check before advertising a current judgment, using the
real core fields (inspect: exit, current, stale, publication.review_id; prepare: exit, measurement):
  I1  inspect body missing/non-object, exit not an integer or nonzero
  I2  inspect 'current' missing/non-string or different from the read review id   (Prime: inspect_current_differs)
  I3  inspect 'stale' not the boolean False                                       (Prime: inspect_stale)
  P1  prepare exit not an integer, or nonzero while measurement is 'complete'     (Prime: prepare_nonzero)
  P2  prepare measurement not 'complete'
Any v2 anomaly (or a pass03 anomaly) => the report must NOT be 'readable'. Flags, typed envelope and custody rules are
the pass03 rules. Proposed RP-3 for Prime; NOT in the 37 required cases.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

LIVE = Path(r"D:\Git\lib-build")
_REL = "labs/loop-convergence-harness-pass03/reporter_judges.py"
_ROW = {r["path"]: r for r in json.loads((LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.25/source-manifest.json").read_bytes())["files"]}[_REL]
if hashlib.sha256((LIVE / _REL).read_bytes()).hexdigest() != _ROW["sha256"]:
    raise SystemExit("refused: pass03 reporter_judges.py differs from its pack05.25 freeze")
_s = importlib.util.spec_from_file_location("rj_pass03", LIVE / _REL)
RJ = importlib.util.module_from_spec(_s)
_s.loader.exec_module(RJ)
SAFE, STATES = RJ.SAFE, RJ.STATES


def anomalies_v2(read, inspect, prepare) -> list:
    a = []
    if not isinstance(inspect, dict) or not isinstance(inspect.get("body"), dict):
        a.append("core inspect: missing or non-object body")
    else:
        ib = inspect["body"]
        if type(inspect.get("exit")) is not int or inspect["exit"] != 0:
            a.append(f"core inspect: exit {inspect.get('exit')!r} (must be the integer 0)")
        rid = (read.get("body") or {}).get("review_id") if isinstance(read, dict) else None
        if not isinstance(ib.get("current"), str) or not ib["current"]:
            a.append("core inspect: current id missing or not a string")
        elif ib["current"] != rid:
            a.append("core inspect: current id differs from the read review id")
        if ib.get("stale") is not False:
            a.append(f"core inspect: stale {ib.get('stale')!r} (must be the boolean false)")
    if not isinstance(prepare, dict) or not isinstance(prepare.get("body"), dict):
        a.append("core prepare: missing or non-object body")
    else:
        if type(prepare.get("exit")) is not int:
            a.append("core prepare: exit not an integer")
        elif prepare["exit"] != 0 and prepare["body"].get("measurement") == "complete":
            a.append("core prepare: nonzero exit with complete measurement")
        if prepare["body"].get("measurement") != "complete":
            a.append(f"core prepare: measurement {prepare['body'].get('measurement')!r}")
    return a


def guard_v2(read, recover, inspect, prepare, report, kind: str) -> tuple:
    r = []
    rep = report.get("body") if isinstance(report, dict) else None
    if not isinstance(rep, dict):
        return {"report": "object"}, ["report has no JSON body"], "fail"
    for k, v in SAFE.items():
        if k not in rep:
            r.append(f"report field {k} absent")
        elif type(rep[k]) is not type(v) or rep[k] != v:
            r.append(f"report {k}={rep[k]!r} (must be {v!r})")
    st = rep.get("state")
    if st not in STATES:
        r.append(f"report state {st!r} unsupported or absent")
    if st in ("readable", "stale") and not isinstance(rep.get("stale"), bool):
        r.append("report stale absent or not boolean")
    an = RJ.anomalies(read, recover) + anomalies_v2(read, inspect, prepare)
    if an:
        if st == "readable":
            r.append("report claims current despite core anomalies: " + "; ".join(an))
    else:
        if read["exit"] == 0 and read["body"]["stale"] is False:
            if st != "readable" or rep.get("stale") is not False:
                r.append("core current but report not readable/stale false")
            if rep.get("review_id") != read["body"]["review_id"]:
                r.append("report review_id differs from the core")
            if rep.get("judgment") != read["body"].get("judgment"):
                r.append("report judgment differs from the core's current judgment")
        elif st == "readable":
            r.append("core not current but report readable")
    cust = (read.get("body") or {}).get("custody") if isinstance(read, dict) else None
    if rep.get("custody") != cust:
        r.append(f"report custody {rep.get('custody')!r} != core {cust!r}")
    if kind == "N7" and rep.get("custody") != "not-applicable":
        r.append("N7 report custody is not 'not-applicable'")
    if kind == "N5" and rep.get("custody") == "not-applicable":
        r.append("N5 report custody took the N7 value")
    return {"anomalies": an}, r, "pass" if not r else "fail"
