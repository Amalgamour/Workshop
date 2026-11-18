#!/usr/bin/env python3
"""Pure judges for the harness successor's required callbacks (0707/05.22). NONPRODUCTION. No I/O.

Each judge takes the OBSERVATIONS a callback collected from real candidate commands and returns
(expected, observed, verdict). Expected values are fixture facts and contract constants written here, never values
computed by the candidate. A missing or wrongly typed field is a failure with a named reason, never a default pass.
An unimplemented candidate operation (no JSON body, unknown command) fails explicitly.
"""

from __future__ import annotations

N7_CUSTODY = "not-applicable"
SAFE_FLAGS = {"authority": "none", "accepted": False, "work_complete": False, "action_released": False, "releases_action": False}
LAB_ONLY = "LAB-ONLY"


def _int(x) -> bool:
    return type(x) is int


def _failed_cleanly(r: dict) -> bool:
    """A refusal: a nonzero integer exit and no Python traceback (a crash is not a refusal)."""
    return isinstance(r, dict) and _int(r.get("exit")) and r["exit"] != 0 and "Traceback (most recent call last)" not in str(r.get("stderr", ""))


def _out(expected, observed, reasons):
    observed = dict(observed)
    observed["judge_reasons"] = reasons
    return expected, observed, "pass" if not reasons else "fail"


# ---------------------------------------------------------------- strict N7 (06.21 H3)
def strict(obs: dict, alternative: tuple | None) -> tuple:
    """Pass only for the strict-grammar reason: malformed-n7-declaration present, the rejected alternative not bound
    in its declared role, intake incomplete, record and publication refused, destination unchanged. A pair mismatch or
    other blocker is not enough. alternative = (roles, path) of the declaration that must NOT bind, or None."""
    r = []
    codes = obs.get("codes")
    if not isinstance(codes, list):
        r.append("codes missing")
    elif "malformed-n7-declaration" not in codes:
        r.append("malformed-n7-declaration reason absent (a different blocker does not prove strict parsing)")
    if obs.get("measurement") != "incomplete":
        r.append(f"measurement {obs.get('measurement')!r} != 'incomplete'")
    rows = obs.get("bound_rows")
    if not isinstance(rows, list):
        r.append("bound rows missing")
    elif alternative:
        roles, path = alternative
        hit = [x for x in rows if isinstance(x, dict) and x.get("role") in roles and isinstance(x.get("path"), str)
               and (x["path"] == path or x["path"].endswith("/" + path))]
        if hit:
            r.append(f"rejected alternative bound: {hit}")
    if not (_int(obs.get("record_exit")) and obs["record_exit"] != 0):
        r.append("record not refused")
    if not (_int(obs.get("publish_exit")) and obs["publish_exit"] != 0):
        r.append("publication not refused")
    if obs.get("destination_unchanged") is not True:
        r.append("destination changed")
    return _out({"codes_include": "malformed-n7-declaration", "alternative_bound": False, "measurement": "incomplete",
                 "record": "refused", "publish": "refused", "destination_unchanged": True}, obs, r)


# ---------------------------------------------------------------- N7-3 not-applicable on record and render
def n7_custody(obs: dict) -> tuple:
    r = []
    if obs.get("record_exit") != 0:
        r.append("N7 record did not record")
    if obs.get("read_custody") != N7_CUSTODY:
        r.append(f"stored N7 record custody {obs.get('read_custody')!r} != {N7_CUSTODY!r}")
    rendered = obs.get("rendered")
    if not isinstance(rendered, str) or not rendered.strip():
        r.append("rendered text missing")
    else:
        if f"custody: {N7_CUSTODY}" not in rendered:
            r.append("rendered text does not state 'custody: not-applicable'")
        if "custody: missing" in rendered:
            r.append("rendered text states 'custody: missing' for N7")
    ex = obs.get("exchange")
    if not isinstance(ex, dict) or ex.get("n1_custody") != N7_CUSTODY:
        r.append("intake exchange n1_custody is not 'not-applicable'")
    if obs.get("n5_control_custody") in (None, N7_CUSTODY):
        r.append(f"N5 control custody {obs.get('n5_control_custody')!r}: an N5 record must carry its own N5 custody value, not none and not N7's")
    return _out({"record_custody": N7_CUSTODY, "render": f"custody: {N7_CUSTODY}", "exchange.n1_custody": N7_CUSTODY,
                 "n5_control": "N5 enum unchanged"}, obs, r)


# ---------------------------------------------------------------- CAP-4 declared source bound and unrelated limits
def cap4(obs: dict, bound: int = 64) -> tuple:
    r = []
    b64, b65, l25, doc = (obs.get(k) or {} for k in ("at_bound", "over_bound", "list25", "doc"))
    if b64.get("harness_count") != bound:
        r.append(f"at-bound fixture is not {bound} sources by the harness count")
    if b64.get("measurement") != "complete":
        r.append("at-bound intake not complete")
    if b64.get("record_exit") != 0:
        r.append(f"{bound}-source judgment not recorded")
    if b64.get("read_exit") != 0 or b64.get("judgment_equal") is not True:
        r.append(f"{bound}-source judgment not read back canonically equal")
    if b65.get("harness_count") != bound + 1:
        r.append(f"over-bound fixture is not {bound + 1} sources")
    if b65.get("measurement") != "complete":
        r.append("over-bound intake not complete (the refusal must come from the source bound, not intake)")
    if not _failed_cleanly(b65):
        r.append(f"{bound + 1}-source record not refused cleanly")
    elif "sources" not in str(b65.get("diagnostic", "")):
        r.append("over-bound refusal has no explicit 'sources' diagnostic")
    if not (_int(l25.get("harness_count")) and l25["harness_count"] <= 24):
        r.append("list-limit fixture must stay within the old 24-source bound")
    if not _failed_cleanly(l25):
        r.append("25-item unrelated list not refused cleanly (MAX_LIST 24 must stay)")
    elif not ("limit" in str(l25.get("diagnostic", "")) and "reasons" in str(l25.get("diagnostic", ""))):
        r.append("unrelated-list refusal does not name the list limit")
    if not (_int(doc.get("harness_count")) and doc["harness_count"] <= 24):
        r.append("document fixture must stay within the old 24-source bound")
    if not (_int(doc.get("judgment_bytes")) and doc["judgment_bytes"] > 262144):
        r.append("document fixture is not over 262144 bytes")
    if not _failed_cleanly(doc):
        r.append("oversize document not refused cleanly")
    elif "262144" not in str(doc.get("diagnostic", "")) and "exceeds" not in str(doc.get("diagnostic", "")):
        r.append("document refusal does not name the document bound")
    return _out({f"{bound}": "record + read equal", f"{bound + 1}": "refused 'sources'", "list 25": "refused 'limit reasons'",
                 "doc > 262144": "refused (document bound)"}, obs, r)


# ---------------------------------------------------------------- RP-1 reporter parity with the core
def _report_ok(rep: dict, where: str, r: list) -> dict | None:
    if not isinstance(rep, dict) or not isinstance(rep.get("body"), dict):
        r.append(f"{where}: reporter gave no JSON body (unimplemented operation; exit {None if not isinstance(rep, dict) else rep.get('exit')})")
        return None
    b = rep["body"]
    for k, v in SAFE_FLAGS.items():
        if k not in b:
            r.append(f"{where}: reporter field {k} missing")
        elif b[k] != v:
            r.append(f"{where}: reporter {k}={b[k]!r} (must be {v!r})")
    return b


def rp1(obs: dict) -> tuple:
    r = []
    want = {"current": ("readable", False), "stale": ("stale", True)}
    for state, (rstate, rstale) in want.items():
        o = obs.get(state) or {}
        core = o.get("core") or {}
        if state == "current" and not (core.get("exit") == 0 and core.get("stale") is False):
            r.append("fixture: core read is not current (cannot test parity)")
        if state == "stale" and core.get("stale") is not True:
            r.append("fixture: core read is not stale (cannot test parity)")
        b = _report_ok(o.get("report"), state, r)
        if b is None:
            continue
        if o["report"].get("exit") != 0:
            r.append(f"{state}: reporter exit {o['report'].get('exit')} (an observation is not a refusal)")
        if b.get("state") != rstate:
            r.append(f"{state}: reporter state {b.get('state')!r} != {rstate!r}")
        if b.get("stale") is not rstale:
            r.append(f"{state}: reporter stale {b.get('stale')!r} != {rstale!r}")
        if b.get("review_id") != core.get("review_id"):
            r.append(f"{state}: reporter review_id differs from the core")
        ex_core, ex_rep = core.get("exchange"), b.get("exchange")
        if not isinstance(ex_rep, dict):
            r.append(f"{state}: reporter has no N7 'exchange' metadata")
        elif not isinstance(ex_core, dict):
            r.append(f"{state}: fixture core has no exchange")
        else:
            for k in ("state", "chronology", "n1_custody"):
                if ex_rep.get(k) != ex_core.get(k):
                    r.append(f"{state}: reporter exchange.{k} {ex_rep.get(k)!r} != core {ex_core.get(k)!r}")
        if b.get("custody") != core.get("custody"):
            r.append(f"{state}: reporter custody {b.get('custody')!r} != core {core.get('custody')!r}")
    o = obs.get("held") or {}
    if (o.get("core") or {}).get("measurement") == "complete":
        r.append("fixture: held core intake is complete (cannot test held)")
    b = _report_ok(o.get("report"), "held", r)
    if b is not None and b.get("state") != "held":
        r.append(f"held: reporter state {b.get('state')!r} != 'held'")
    return _out({"current": "readable/stale false", "stale": "stale/true", "held": "held", "exchange": "equal to core",
                 "flags": SAFE_FLAGS}, obs, r)


# ---------------------------------------------------------------- RP-2 pin refusals and envelope hardening
RP2_PROBES = ("wrong-dispatcher", "wrong-chain-pin", "unknown-flag", "repeated-flag", "relative-book", "bad-pass", "missing-source")


def rp2(obs: dict) -> tuple:
    r = []
    ctl = obs.get("control") or {}
    if not (ctl.get("exit") == 0 and isinstance(ctl.get("body"), dict)):
        r.append(f"positive control: untampered report did not succeed (exit {ctl.get('exit')}); refusals prove nothing without it")
    for k in RP2_PROBES:
        p = obs.get(k)
        if not isinstance(p, dict):
            r.append(f"{k}: not observed")
            continue
        if not _failed_cleanly(p):
            r.append(f"{k}: not refused cleanly (exit {p.get('exit')})")
        elif isinstance(p.get("body"), dict) and p["body"].get("state") not in (None, "refused"):
            r.append(f"{k}: refusal emitted an observation state {p['body'].get('state')!r}")
    return _out({"control": "exit 0", **{k: "refused (nonzero, no traceback)" for k in RP2_PROBES}}, obs, r)


# ---------------------------------------------------------------- IN-2 foreign copied N5 book
def in2(obs: dict, judgment: dict) -> tuple:
    r = []
    a0, a1 = obs.get("a_read_before") or {}, obs.get("a_read_after") or {}
    if obs.get("a_record_exit") != 0:
        r.append("same-book record failed (fixture)")
    for nm, a in (("before", a0), ("after", a1)):
        if not (a.get("exit") == 0 and a.get("stale") is False):
            r.append(f"original book not current {nm} the copy checks")
    if obs.get("a_bytes_unchanged") is not True:
        r.append("original book bytes changed")
    br, bc, bp = obs.get("b_read") or {}, obs.get("b_recover") or {}, obs.get("b_publish") or {}
    for nm, x in (("read", br), ("recover", bc), ("publish", bp)):
        if "Traceback (most recent call last)" in str(x.get("stderr", "")):
            r.append(f"copy {nm} crashed (a crash is not a hold)")
    held = (_int(br.get("exit")) and br["exit"] != 0) or br.get("stale") is True or br.get("applicable") is False
    if not held:
        r.append("copy has no positive hold evidence: it reads current, or gives no correctly typed stale/applicability field")
    if br.get("judgment") != judgment and bc.get("judgment") != judgment:
        r.append("historical judgment not retained in the copy (neither read nor recover returns it)")
    if not _failed_cleanly(bp) or obs.get("b_destination_created") is not False:
        r.append("copy publish not refused, or a destination appeared")
    return _out({"original": "current before/after; bytes unchanged", "copy": "not current (held/stale); judgment retained; publish refused"}, obs, r)
