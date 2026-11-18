#!/usr/bin/env python3
"""0707 pass02: NONPRODUCTION prototypes of two proposed pure functions.

classify_target  - the F8 prepare-time target inspection, reusing the pinned
                   constructor's own locate() and PENDING rule (imported from
                   labs/review-construction-pass02/construct.py, hash-checked,
                   main not run). Read-only.
mechanical_state - the F7 blocker derivation from a CURRENT `read` view. Uses
                   only fields the view already carries; never the supplied
                   next-action text.

usage: proto.py   (checks both against recorded probe and 05.01 outputs;
                   writes evidence/build05.02/probes/proto-check.json)
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CHECKOUT = Path(r"D:\Git\lib-build")
PAGE = CHECKOUT / "00.kernel" / "00.00.10.work" / "0707.app-use-check"
OUT = PAGE / "evidence" / "build05.02" / "probes"
OLD = PAGE / "evidence" / "build05.01" / "runs" / "run1"
CONSTRUCT = CHECKOUT / "labs" / "review-construction-pass02" / "construct.py"
BINDING = re.compile(r"(?m)^task_binding: ([0-9a-f]{64})$")


def load_constructor():
    pins = {r["path"]: r for r in json.loads((PAGE / "evidence/pack05.02/source-manifest.json").read_text(encoding="utf-8"))["files"]}
    data = CONSTRUCT.read_bytes()
    pin = pins["labs/review-construction-pass02/construct.py"]
    if hashlib.sha256(data).hexdigest() != pin["sha256"] or len(data) != pin["bytes"]:
        raise SystemExit("construct.py does not match pack05.02")
    spec = importlib.util.spec_from_file_location("pinned_construct_pass02", CONSTRUCT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = load_constructor()


def classify_target(data: bytes | None, current_binding: str | None) -> dict:
    """Proposed review-target-inspection/1 core. Same rule order as compose()."""
    if data is None:
        return {"state": "absent", "rule": "target file is absent; this entry does not create targets (permit_create false)"}
    try:
        sep = C.newline_of(data)
        _prefix, current, _suffix = C.locate(data, sep)
        text = current.decode("utf-8")
    except C.Refusal as exc:
        return {"state": "unsupported", "rule": exc.message}
    stripped = text.strip()
    if stripped in {"PENDING", "PENDING."}:
        return {"state": "pending", "rule": None}
    match = BINDING.search(text)
    if match and current_binding and match.group(1) == current_binding:
        return {"state": "constructed-same-binding", "rule": "a constructed review for this task binding is present; render is idempotent only if the body is identical",
                "section_sha256": C.sha256_bytes(current), "binding_sha256": match.group(1)}
    return {
        "state": "existing-review",
        "rule": "existing review conflicts; a successor process is required and this review was not overwritten",
        "section_sha256": C.sha256_bytes(current),
        "binding_sha256": match.group(1) if match else None,
    }


def mechanical_state(view: dict) -> dict:
    """Proposed `mechanical` block of review-loop-result/2. Pure function of the view."""
    pass_state = view.get("pass_state")
    render_state = view.get("render_state")
    latest = view.get("latest_review") or {}
    current_token = (view.get("write_token") or {}).get("sha256")
    recorded_token = (latest.get("write_token") or {}).get("sha256")
    if render_state == "conflict":
        return {"blocker": "existing-review-conflict", "route": "none-in-this-entry",
                "text": "The target holds another review. This entry cannot render this judgment; a successor process is required. The committed judgment is kept."}
    if render_state == "pending":
        if current_token is not None and current_token == recorded_token:
            return {"blocker": "render-interrupted", "route": "recover",
                    "text": "Run recover: it retries rendering the same committed review against the unchanged target."}
        return {"blocker": "target-changed-since-record", "route": "none-in-this-entry",
                "text": "The target changed after this judgment was recorded. render and recover will refuse. This entry has no supersession route."}
    if pass_state == "reviewed" and render_state == "rendered":
        return {"blocker": None, "route": None, "text": "The committed review is rendered."}
    if pass_state == "awaiting-review":
        return {"blocker": None, "route": "record", "text": "Supply a typed judgment and supplied_record, then record."}
    return {"blocker": "unknown-state", "route": None, "text": f"Unrecognized state: pass {pass_state}, render {render_state}."}


def main() -> int:
    rows = []
    probes = OUT / "run1"
    a_binding = "a8761262afb9993a459ce26da4e55b722686f43ba842c880d2e55d3a33cbd74c"
    old_books = OLD / "books"
    targets = [
        ("pending (05.01 A before render)", (old_books / "A.after-record" / "0519.desk-app" / "05.01.md").read_bytes(), a_binding, "pending"),
        ("substantive 0519 snapshot (05.01 E)", (old_books / "E.after" / "0519.desk-app" / "05.01.md").read_bytes(), a_binding, "existing-review"),
        ("rendered A, same binding", (old_books / "A.after-render" / "0519.desk-app" / "05.01.md").read_bytes(), a_binding, "constructed-same-binding"),
        ("rendered A, other binding", (old_books / "A.after-render" / "0519.desk-app" / "05.01.md").read_bytes(), "0" * 64, "existing-review"),
        ("no heading", b"# x\n\n## Return pointer\nPENDING.\n", a_binding, "unsupported"),
        ("duplicate heading", b"# x\n\n## Review - Codex Prime\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n", a_binding, "unsupported"),
        ("absent", None, a_binding, "absent"),
        ("PENDING without dot, CRLF", b"# x\r\n\r\n## Review - Codex Prime\r\nPENDING\r\n## Notes\r\nT\r\n", a_binding, "pending"),
    ]
    for name, data, binding, expect in targets:
        got = classify_target(data, binding)
        rows.append({"fn": "classify_target", "case": name, "expect": expect, "observed": got["state"], "rule": got.get("rule"), "ok": got["state"] == expect})

    reads = [
        ("05.01 B before recover", OLD / "09-B-read-before-recover.stdout", "render-interrupted", "recover"),
        ("05.01 D after stale refusal", OLD / "19-D-read.stdout", "target-changed-since-record", "none-in-this-entry"),
        ("05.01 E conflict", OLD / "25-E-read.stdout", "existing-review-conflict", "none-in-this-entry"),
        ("05.01 A reviewed", OLD / "05-A-read.stdout", None, None),
        ("05.02 P2 pending prepare", probes / "08-P2-pending.stdout", None, "record"),
    ]
    for name, path, expect_blocker, expect_route in reads:
        body = json.loads(path.read_bytes().decode("utf-8"))
        view = body["view"]
        got = mechanical_state(view)
        supplied = (view.get("next_action") or {}).get("text")
        rows.append({"fn": "mechanical_state", "case": name, "expect": [expect_blocker, expect_route],
                     "observed": [got["blocker"], got["route"]], "ok": [got["blocker"], got["route"]] == [expect_blocker, expect_route],
                     "current_next_field": body.get("next"), "supplied_next_action": supplied,
                     "mechanical_text_differs_from_supplied": got["text"] != supplied})
    body = {"schema": "0707-proto-check/1", "nonproduction": True, "rows": rows, "all_ok": all(r["ok"] for r in rows)}
    (OUT / "proto-check.json").write_bytes((json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    for r in rows:
        print("OK " if r["ok"] else "NO ", r["fn"], r["case"], r["observed"])
    print("all_ok", body["all_ok"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
