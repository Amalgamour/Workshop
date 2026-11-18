#!/usr/bin/env python3
"""Hardening runtime for one selected read-only review report.

Contract review-report-hardening/1. This module checks the candidate
dispatcher and the historical dependency cut, then calls the accepted
pass03 observation with envelope and intake guards installed in this
process only. It does not call pass01.check_pins and it does not launch
pass03 main. Exit 0 is not a release.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

CONTRACT = "review-report-hardening/1"
HELPER_ROOT = Path(r"D:\Git\lib-build")
HELPER_MODULE = "labs/workbook-review-pass03/workbook.py"
REPARSE = 0x400
LIBRARIAN_PIN_BYTES = 12804
LIBRARIAN_PIN_SHA = "f1d23d455f20319e3f430d345b2893bda039fd8c84be4f3691b4e4be123b8983"
HEX = set("0123456789abcdef")
ENVELOPE_SUPPORTED = {
    "accepted": False,
    "approved": False,
    "authority": "none",
    "closes_work": False,
    "releases_action": False,
    "task_association": "not-established",
}
ENVELOPE_CURRENT = (
    "accepted",
    "action_released",
    "approved",
    "authority",
    "closes_work",
    "releases_action",
    "task_association",
)
REJECTED_STATUS = {"unstable", "mismatch", "unreadable", "bad"}
REJECTED_SIZE = "negative or bool size is not a valid measurement"
MISSING_SIZE = "a row omits a byte size; this is not a conflict between two int sizes"
PINS = {
    "app/librarian.py": (LIBRARIAN_PIN_BYTES, LIBRARIAN_PIN_SHA),
    "app/review-loop-v4.json": (2519, "769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723"),
    "app/review-loop-v5.json": (1964, "eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3"),
    "app/review-loop-v6.json": (2743, "c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa"),
    "app/review-loop-v7.json": (3515, "bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8"),
    "app/review_loop_tools_v4.py": (13381, "0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296"),
    "app/review_loop_tools_v5.py": (7875, "b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9"),
    "app/review_loop_tools_v6.py": (9175, "e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94"),
    "app/review_loop_tools_v7.py": (10291, "93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d"),
    "labs/prime-cycle-pass03/prime_cycle.py": (76045, "496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c"),
    "labs/prime-review-pass02/prime_review.py": (58560, "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"),
    "labs/return-access-pass01/return_access.py": (26561, "501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5"),
    "labs/review-construction-pass04/construct.py": (42582, "6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20"),
    "labs/review-loop-pass03/review_loop.py": (55474, "47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b"),
    "labs/review-report-deployment-pass01/report.py": (6294, "0f7def8d353506b93c71d130d740cd1262717ce493a868fc356e09ab925f7506"),
    "labs/review-report-pass01/report.py": (42127, "72e9bda15c5f3ca844350be5dae2fcfcf4e7c609c262b8f7e702d64467eb94cc"),
    "labs/review-report-pass02/report.py": (38323, "d13d8d4f54d79cbdb22e1a40fdffb89bd26b85a611bf8620dc36854be9eb852e"),
    "labs/review-report-pass03/report.py": (8091, "70028dfe97bc6178a3497c814cf585476bb0b41650ce67fc79dd3d5b118dfade"),
    "labs/workbook-review-pass01/forms/workbook-review-v1.json": (4532, "152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f"),
    "labs/workbook-review-pass01/workbook.py": (79131, "60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a"),
    "labs/workbook-review-pass02/forms/workbook-review-v1.json": (4532, "66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645"),
    "labs/workbook-review-pass02/workbook.py": (52574, "6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a"),
    "labs/workbook-review-pass03/forms/workbook-review-v1.json": (4532, "4b8cf0e8c81cc421fd0212ae169ba1557998bf526c5f6d87ee170c9d038cbb0b"),
    "labs/workbook-review-pass03/workbook.py": (19533, "9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c"),
}


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


def _load(rel: str, name: str):
    path = Path(__file__).resolve().parents[1] / rel
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p3 = _load("review-report-pass03/report.py", "review_report_pass03_for_hardening_v1")
_PATCHED = p3.finish.__globals__
base_report = _PATCHED["base_report"]
emit = _PATCHED["emit"]
parse_args = _PATCHED["p1"].parse_args
ArgRefuse = _PATCHED["p1"].Refuse
p2 = p3.p2


def _linked(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def check_pins(code_root: Path) -> None:
    root = Path(code_root)
    for rel in PINS:
        want_bytes, want_sha = PINS[rel]
        if "\\" in rel or rel.startswith("/") or any(part in {"", ".", ".."} for part in rel.split("/")):
            raise Refuse("pin path escapes")
        cursor = root
        for part in rel.split("/"):
            cursor = cursor / part
            if _linked(cursor):
                raise Refuse(f"dependency conflict {rel} is linked and was not followed")
        if not cursor.is_file():
            raise Refuse(
                f"dependency conflict {rel} got missing want {want_bytes} bytes sha256 {want_sha}"
            )
        data = cursor.read_bytes()
        got = hashlib.sha256(data).hexdigest()
        if len(data) != want_bytes or got != want_sha:
            raise Refuse(
                f"dependency conflict {rel} got {len(data)} bytes sha256 {got} "
                f"want {want_bytes} bytes sha256 {want_sha}"
            )


def canonical_digest(value) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(char in HEX for char in value)


def envelope_supported(inspect, read, recover) -> bool:
    if not isinstance(inspect, dict):
        return False
    for key, want in ENVELOPE_SUPPORTED.items():
        if key not in inspect:
            return False
        got = inspect[key]
        if type(got) is not type(want) or got != want:
            return False
    same = p2.p1.same
    for other in (read, recover):
        if not isinstance(other, dict):
            return False
        for key in ENVELOPE_SUPPORTED:
            if not same(inspect.get(key), other.get(key)):
                return False
    return True


def rejected(report: dict) -> bool:
    observation = report.get("observation") if isinstance(report.get("observation"), dict) else {}
    # No journal yet: the cut is unreadable and stable stays null. A validated
    # advisory envelope is the not-recorded baseline, not a rejected current cut.
    if report.get("state") == "not-recorded" and observation.get("stable") is not False:
        return False
    status = observation.get("status")
    if status in REJECTED_STATUS:
        return True
    if observation.get("stable") is False:
        return True
    identity = report.get("identity") if isinstance(report.get("identity"), dict) else {}
    return identity.get("selected_by") == "mismatch"


def withhold(report: dict, cause: str) -> None:
    for key in ENVELOPE_CURRENT:
        report[key] = None
    report["envelope_withheld"] = {
        "cause": cause,
        "fields": list(ENVELOPE_CURRENT),
        "provenance": "withheld-current-cut",
        "reason": (
            "source identity was rejected; unknown is not false and these values "
            "are not a current authority or action state"
        ),
    }


def stash_historical(report: dict) -> None:
    if isinstance(report.get("historical_supplied"), dict):
        return
    fresh = base_report(
        {
            "book": report.get("book"),
            "code_root": report.get("code_root"),
            "pass": report.get("pass"),
            "source": report.get("source"),
        },
        report.get("state") if isinstance(report.get("state"), str) else "held",
        report.get("exit") if type(report.get("exit")) is int else 1,
    )
    supplied = {}
    for key in p2.JUDGMENT_KEYS:
        if report.get(key) != fresh.get(key):
            supplied[key] = report.get(key)
    if not supplied:
        return
    report["historical_supplied"] = {
        "fields": supplied,
        "provenance": "historical-supplied",
        "reason": "retained after the current cut was rejected; not a current judgment",
    }


def source_rows(inspect):
    if not isinstance(inspect, dict):
        return None
    form = inspect.get("form") if isinstance(inspect.get("form"), dict) else {}
    bindings = form.get("bindings") if isinstance(form.get("bindings"), dict) else {}
    if "rows" not in bindings or not isinstance(bindings.get("rows"), list):
        return None
    return bindings["rows"]


def size_counts(rows: list) -> dict:
    counts = {"bool": 0, "missing": 0, "negative": 0, "other": 0}
    for row in rows:
        if not isinstance(row, dict):
            continue
        if "bytes" not in row or row.get("bytes") is None:
            counts["missing"] += 1
            continue
        value = row.get("bytes")
        if type(value) is bool:
            counts["bool"] += 1
        elif type(value) is int and value < 0:
            counts["negative"] += 1
        elif type(value) is not int:
            counts["other"] += 1
    return counts


def int_conflict(rows: list) -> bool:
    groups: dict[tuple[str, str], set] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        root = row.get("root") if isinstance(row.get("root"), str) else None
        path = row.get("path") if isinstance(row.get("path"), str) else None
        value = row.get("bytes")
        if root is None or path is None or type(value) is not int or value < 0:
            continue
        groups.setdefault((root, path), set()).add(value)
    return any(len(values) > 1 for values in groups.values())


def clear_bytes(item: dict, reason: str) -> None:
    item["bytes"] = None
    item["bytes_state"] = "unknown"
    item["reason"] = reason


def withhold_totals(body: dict, reason: str) -> None:
    body["bytes"] = None
    body["bytes_state"] = "unknown"
    body["count"] = None
    body["count_state"] = "unknown"
    body["hash_match"] = None
    body["hash_mismatch"] = None
    body["not_verified"] = None
    for key in ("addressed_sources", "content_blobs", "intake_roles", "measured_artifact_rows"):
        item = body.get(key)
        if not isinstance(item, dict):
            continue
        item["bytes"] = None
        item["bytes_state"] = "unknown"
        item["count"] = None
        item["count_state"] = "unknown"
        item["reason"] = reason
        if key == "intake_roles":
            item["hash_match"] = None
            item["hash_mismatch"] = None
            item["not_verified"] = None


def recount_integrity(rows: list) -> tuple[int, int, int]:
    matched = 0
    mismatched = 0
    unverified = 0
    for row in rows:
        declared = row.get("declared_sha256")
        actual = row.get("sha256")
        size = row.get("bytes")
        declared_size = row.get("declared_bytes")
        if not canonical_digest(declared) or not canonical_digest(actual):
            unverified += 1
        elif (
            declared == actual
            and type(size) is int
            and size >= 0
            and type(declared_size) is int
            and declared_size == size
        ):
            matched += 1
        else:
            mismatched += 1
    return matched, mismatched, unverified


def apply_size_guard(body: dict, rows: list, counts: dict) -> None:
    if counts["bool"] == 0 and counts["missing"] == 0 and counts["negative"] == 0 and counts["other"] == 0:
        return
    body["size_observation"] = {
        "bool": counts["bool"],
        "missing": counts["missing"],
        "negative": counts["negative"],
        "other": counts["other"],
        "provenance": "row-byte-field",
    }
    if counts["bool"] or counts["negative"]:
        reason = REJECTED_SIZE
        body["bytes"] = None
        body["bytes_state"] = "unknown"
        for key in ("addressed_sources", "content_blobs", "intake_roles", "measured_artifact_rows"):
            item = body.get(key)
            if isinstance(item, dict):
                clear_bytes(item, reason)
        return
    if int_conflict(rows):
        return
    reason = MISSING_SIZE if counts["other"] == 0 else "a row byte size is not a supported int measurement"
    for key in ("addressed_sources", "content_blobs"):
        item = body.get(key)
        if isinstance(item, dict) and isinstance(item.get("reason"), str) and "do not agree on one int byte size" in item["reason"]:
            item["reason"] = reason


def apply_digest_guard(body: dict, rows: list) -> None:
    dicts = [row for row in rows if isinstance(row, dict)]
    if not any(
        isinstance(row.get(key), str) and not canonical_digest(row.get(key))
        for row in dicts
        for key in ("declared_sha256", "sha256")
    ):
        return
    kept = body.get("rows") if isinstance(body.get("rows"), list) else dicts
    artifacts = [row for row in kept if row.get("role") == "artifact"]
    matched, mismatched, unverified = recount_integrity(artifacts)
    body["hash_match"] = matched
    body["hash_mismatch"] = mismatched
    body["not_verified"] = unverified
    intake = body.get("intake_roles")
    if isinstance(intake, dict):
        in_match, in_mismatch, in_unverified = recount_integrity(kept)
        intake["hash_match"] = in_match
        intake["hash_mismatch"] = in_mismatch
        intake["not_verified"] = in_unverified


def harden_artifacts(inspect):
    body = _artifacts_of(inspect)
    rows = source_rows(inspect)
    if rows is None:
        return body
    invalid = [row for row in rows if not isinstance(row, dict)]
    counts = size_counts(rows)
    if invalid:
        body["invalid_rows"] = {
            "count": len(invalid),
            "dropped": False,
            "provenance": "retained-malformed-intake",
        }
        body["measurement_withheld"] = (
            "malformed intake rows were retained; counters are not a complete measured total"
        )
        body["raw_rows"] = rows
        withhold_totals(body, "malformed intake rows were retained and the total was withheld")
    apply_size_guard(body, rows, counts)
    if not invalid:
        apply_digest_guard(body, rows)
    return body


def install_patches() -> None:
    global _artifacts_of
    _artifacts_of = p2.artifacts_of
    _apply = p2.p1.apply_envelope
    _mark = p2.mark_unstable
    _hold = p2.hold_mismatch
    _set = p2.set_observation
    _projection = p2.projection_of

    def apply_envelope(report, inspect, read, recover) -> bool:
        if not envelope_supported(inspect, read, recover):
            return False
        return _apply(report, inspect, read, recover)

    def mark_unstable(report, bound, recheck, keys) -> None:
        stash_historical(report)
        _mark(report, bound, recheck, keys)
        withhold(report, "unstable")

    def hold_mismatch(report, bound, recheck) -> None:
        _hold(report, bound, recheck)
        withhold(report, "mismatch")

    def set_observation(report, bound, recheck, status, stable) -> None:
        force_cut = False
        bound_ok = isinstance(bound, dict)
        recheck_ok = isinstance(recheck, dict)
        if not bound_ok and not recheck_ok:
            stable = None
            if status not in {"unreadable", "bad", "not-run"}:
                status = "unreadable"
        elif not bound_ok or not recheck_ok:
            if stable is not False:
                stable = False
                force_cut = True
        _set(report, bound, recheck, status, stable)
        if force_cut:
            changed = report["observation"].get("changed")
            if not isinstance(changed, list):
                changed = []
            if "cut" not in changed:
                report["observation"]["changed"] = [*changed, "cut"]

    def projection_of(report) -> str:
        if rejected(report):
            cause = report.get("observation", {}).get("status")
            withhold(report, cause if isinstance(cause, str) else "rejected")
        return _projection(report)

    p2.p1.apply_envelope = apply_envelope
    p2.mark_unstable = mark_unstable
    p2.hold_mismatch = hold_mismatch
    p2.set_observation = set_observation
    p2.artifacts_of = harden_artifacts
    p2.projection_of = projection_of
    p3.artifacts_of = harden_artifacts
    p3.projection_of = projection_of


install_patches()


def main(argv: list[str] | None = None) -> int:
    blank = {"book": None, "code_root": None, "pass": None, "source": None}
    try:
        options = parse_args(argv)
    except ArgRefuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        emit(p3.finish(base_report(blank, "refused", 2)))
        return 2
    try:
        check_pins(options["code_root"])
    except Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        emit(p3.finish(base_report(options, "refused", 2)))
        return 2
    report = p3.finish(p3.observe(options))
    if report["exit"] == 2:
        print("refused: core stdout is not one workbook-review-result/1 object", file=sys.stderr)
    emit(report)
    return int(report["exit"])


if __name__ == "__main__":
    sys.exit(main())
