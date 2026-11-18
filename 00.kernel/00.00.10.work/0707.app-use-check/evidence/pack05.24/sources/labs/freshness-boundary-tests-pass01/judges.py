#!/usr/bin/env python3
"""Pure judges for the independent freshness-boundary tests (0707/05.23). NONPRODUCTION. No I/O.

Supported meanings (no invented display strings are required):
  current      read exit 0 and 'stale' is the boolean False
  not current  'stale' is the boolean True, OR a clean refusal (integer nonzero exit, no Python traceback)
  crash        a traceback in stderr: neither current nor a hold; always a failure
Every mutation case requires its OWN pre-change read to be current, so a candidate that refuses everything fails.
Missing or wrongly typed fields fail with a named reason.
"""

from __future__ import annotations

TB = "Traceback (most recent call last)"


def _int(x) -> bool:
    return type(x) is int


def crashed(r) -> bool:
    return isinstance(r, dict) and TB in str(r.get("stderr", ""))


def is_current(r) -> bool:
    return isinstance(r, dict) and r.get("exit") == 0 and _int(r.get("exit")) and r.get("stale") is False and not crashed(r)


def clean_refusal(r) -> bool:
    return isinstance(r, dict) and _int(r.get("exit")) and r["exit"] != 0 and not crashed(r)


def not_current(r) -> bool:
    if not isinstance(r, dict) or crashed(r):
        return False
    return r.get("stale") is True or clean_refusal(r)


def _verdict(reasons):
    return "pass" if not reasons else "fail"


def _pub_held(obs, reasons, where="publish"):
    p = obs.get("publish")
    if not clean_refusal(p):
        reasons.append(f"{where} not refused cleanly (exit {None if not isinstance(p, dict) else p.get('exit')})")
    if obs.get("destination_created") is not False:
        reasons.append(f"{where}: a destination appeared or was not checked")


def _history(obs, judgment, reasons):
    rd, rc = obs.get("after_read") or {}, obs.get("after_recover") or {}
    if rd.get("judgment") == judgment or rc.get("judgment") == judgment:
        return
    if clean_refusal(rd) and str(rd.get("message", "")).strip():
        return
    reasons.append("historical judgment neither returned (read/recover) nor a clean refusal with a message naming the limit")


# ------------------------------------------------------------------ A. missing comparison intake
def missing(obs: dict, variant: str, judgment) -> tuple:
    """variant: M0 (control, intake intact) | M1 (moved + changed) | M2 (moved, unchanged) | M3 (non-object + changed)
    | M4 (malformed + changed) | M5 (new unreviewed book)."""
    r = []
    if variant == "M5":
        if obs.get("prepare_measurement") != "complete":
            r.append("fixture control: the new pair does not prepare complete")
        if not not_current(obs.get("after_read")):
            r.append("an unreviewed book reads current")
        _pub_held(obs, r)
        return {"read": "not current", "publish": "refused"}, r, _verdict(r)
    if obs.get("record_exit") != 0:
        r.append("fixture: record did not succeed")
    if not is_current(obs.get("control_read")):
        r.append("pre-change read is not current (fixture invalid or the candidate refuses everything)")
    after = obs.get("after_read")
    if not not_current(after):
        r.append(f"after {variant}: read is not held/stale/refused (it reads current or crashed)")
    _pub_held(obs, r)
    if variant in ("M1", "M2", "M3", "M4"):
        _history(obs, judgment, r)
    if variant == "M1":
        if not is_current(obs.get("restored_read")):
            r.append("after restoring the moved intake and the artifact, the review does not read current again (history not recoverable)")
    return {"control": "current", "after": "not current", "publish": "refused", "history": "kept or clean refusal"}, r, _verdict(r)


# ------------------------------------------------------------------ B. N7 pack region
def region(obs: dict, expect: str) -> tuple:
    """expect: 'current' (a permitted Review-only edit) or 'not-current' (a meaningful change)."""
    r = []
    if obs.get("reached") is not True:
        return {"expect": expect}, ["fixture did not reach record/publish; kept as not-reached, never credited"], "not-reached"
    if not is_current(obs.get("pre_read")):
        r.append("pre-edit read is not current (fixture invalid or the candidate refuses everything)")
    post = obs.get("post_read")
    if expect == "current":
        if not is_current(post):
            r.append("a permitted Review-only edit made the review non-current")
    elif expect == "not-current":
        if not not_current(post):
            r.append("a meaningful change kept the review current (freshness exemption granted)")
    else:
        r.append(f"unknown expectation {expect!r}")
    return {"pre": "current", "post": expect}, r, _verdict(r)


# ------------------------------------------------------------------ C. composition
def instance(obs: dict) -> tuple:
    r = []
    if not is_current(obs.get("a_read_before")):
        r.append("original not current before copy (fixture)")
    if not not_current(obs.get("b_read")):
        r.append("the byte-copied book reads the foreign review current")
    if not is_current(obs.get("a_read_after")):
        r.append("original not current after the copy checks")
    if obs.get("a_unchanged") is not True:
        r.append("original bytes changed")
    return {"copy": "not current", "original": "current, unchanged"}, r, _verdict(r)


def n7_body(obs: dict) -> tuple:
    r = []
    if not is_current(obs.get("pre_read")):
        r.append("pre-edit read is not current")
    if not is_current(obs.get("review_edit_read")):
        r.append("a Review-only edit made the N7 review non-current")
    if not not_current(obs.get("task_edit_read")):
        r.append("a task-body edit kept the N7 review current")
    return {"review_edit": "current", "task_edit": "not current"}, r, _verdict(r)


def row_change(obs: dict) -> tuple:
    r = []
    if not is_current(obs.get("pre_read")):
        r.append("pre-change read is not current")
    post = obs.get("post_read")
    if not (isinstance(post, dict) and post.get("stale") is True) and not not_current(post):
        r.append("an ordinary source-row change kept the review current")
    return {"post": "stale"}, r, _verdict(r)
