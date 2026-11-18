#!/usr/bin/env python3
"""Reporter-obligation judge (0707/05.24; 0522/06.38 controlled-response findings). EQUIPMENT ONLY. NONPRODUCTION.

Judges a reporter's output against the core read/recover responses it observed. Proposed later case RP-3 for Prime;
NOT added to the required registry (callback/reporter contracts unchanged). A real test needs a supplied, reviewed
reporter that can be driven with controlled core responses; this judge is tested only with scripted observations.

Uses only the existing reporter contract fields (05.22 CONTRACT): state, stale, authority, accepted, work_complete,
action_released, releases_action, review_id, custody, judgment. No new display string is required.
Rules:
  F  flags are always safe: authority 'none'; accepted/work_complete/action_released/releases_action false.
  T  report envelope typed: state in {readable, stale, held, refused}; stale bool (or null when held/refused).
  A  anomalies in the core responses: missing/non-object body; read exit not int or stale not bool; exit/stale
     disagreement (exit 0 with stale true, nonzero with stale false); recover stale disagreeing with read; missing,
     non-string or mismatched read/recover review ids; core carrying unsupported authority or accepted flags.
     Any anomaly => the report must NOT be 'readable' (no current claim).
  C  no anomaly and the core is current => report 'readable', stale false, the same review_id, judgment equal.
  S  separation: a non-current report never pairs a judgment with state 'readable' (historical stays historical).
  K  custody equals the core's; N7 'not-applicable'; N5 never 'not-applicable'.
"""

from __future__ import annotations

SAFE = {"authority": "none", "accepted": False, "work_complete": False, "action_released": False, "releases_action": False}
STATES = {"readable", "stale", "held", "refused"}


def anomalies(read, recover) -> list:
    a = []
    for nm, r in (("read", read), ("recover", recover)):
        if not isinstance(r, dict) or not isinstance(r.get("body"), dict):
            a.append(f"core {nm}: missing or non-object body")
    if a:
        return a
    rb, cb = read["body"], recover["body"]
    if type(read.get("exit")) is not int:
        a.append("core read: exit not an integer")
    if not isinstance(rb.get("stale"), bool):
        a.append("core read: stale not boolean")
    elif type(read.get("exit")) is int and ((read["exit"] == 0) == rb["stale"]):
        a.append("core read: exit and stale disagree")
    if isinstance(cb.get("stale"), bool) and isinstance(rb.get("stale"), bool) and cb["stale"] != rb["stale"]:
        a.append("core recover: stale disagrees with read")
    ids = (rb.get("review_id"), cb.get("review_id"))
    if not all(isinstance(x, str) and x for x in ids):
        a.append("core read/recover: review id missing or not a string")
    elif ids[0] != ids[1]:
        a.append("core read/recover: review ids differ")
    for k in ("authority", "accepted"):
        for nm, b in (("read", rb), ("recover", cb)):
            if k in b and b[k] != SAFE[k]:
                a.append(f"core {nm}: unsupported {k}={b[k]!r}")
    return a


def guard(read, recover, report, kind: str) -> tuple:
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
    an = anomalies(read, recover)
    if an:
        if st == "readable":
            r.append("report claims current despite core anomalies: " + "; ".join(an))
    else:
        cur = read["exit"] == 0 and read["body"]["stale"] is False
        if cur:
            if st != "readable" or rep.get("stale") is not False:
                r.append("core current but report not readable/stale false")
            if rep.get("review_id") != read["body"]["review_id"]:
                r.append("report review_id differs from the core")
            if rep.get("judgment") != read["body"].get("judgment"):
                r.append("report judgment differs from the core's current judgment")
        elif st == "readable":
            r.append("core not current but report readable")
    if st == "readable" and an and "judgment" in rep:
        r.append("separation: a judgment is presented as current while the core is anomalous")
    cust = (read.get("body") or {}).get("custody") if isinstance(read, dict) else None
    if rep.get("custody") != cust:
        r.append(f"report custody {rep.get('custody')!r} != core {cust!r}")
    if kind == "N7" and rep.get("custody") != "not-applicable":
        r.append("N7 report custody is not 'not-applicable'")
    if kind == "N5" and rep.get("custody") == "not-applicable":
        r.append("N5 report custody took the N7 value")
    return {"anomalies": an, "rules": "F T A C S K"}, r, "pass" if not r else "fail"
