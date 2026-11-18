#!/usr/bin/env python3
"""Read-only preflight for the accepted loop pieces (0525.app-dependencies/05.03).

Runs labs/module-dependencies-pass02/depdecl.py. Does not import declared modules,
does not edit the reader, and does not treat a valid set as activation.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
CANONICAL = REPO / "labs" / "app-dependencies-pass03" / "preflight.py"
PIN_FILE = CANONICAL.parent / "reader-pin.json"
READER_REL = "labs/module-dependencies-pass02/depdecl.py"
DOOR = "lib-build:labs/review-instance-binding-pass01/review_loop_tools.py"
PASS05 = "lib-build:labs/workbook-review-pass05/workbook.py"
REPORTER = "lib-build:labs/review-report-hardening-pass01/report.py"
SELECTED = "lib-build:app/librarian.py"
DISCLOSED = (REPORTER, "selected-app-pin")
HOLD = (
    "Hold activation. The declared rows are a preflight of accepted pieces. "
    "Combined workbook W and reporter-on-W are pending. "
    "This report is not closure, compatibility, or release."
)
PENDING = (
    {"bytes": None, "id": "combined-workbook-W", "path": None, "sha256": None, "state": "pending"},
    {"bytes": None, "id": "reporter-on-W", "path": None, "sha256": None, "state": "pending"},
)
UNCOVERED = (
    "v4 through v8 historical door pins except the named v7 and v9 files",
    "pass01 and pass02 workbook fan-out, and the pass03 load of pass02",
    "capacity pass01 and pass02 prime_review pins inside source-capacity-prime-review",
    "the rest of the reporter PINS table",
    "labs/review-report-hardening-pass01/librarian.py",
    "the nested candidate tree under labs/review-source-capacity-pass03/candidate",
    "index and delta commands",
    "Git authentication, custody, app selection, concurrency, power loss, and AR-01",
)
EDGE_FAULTS = {
    "pin-differs",
    "identity-pair-mismatch",
    "identity-conflict",
    "record-missing",
    "digest-differs",
}
INCOMING_FAULTS = {"digest-differs", "pair-differs", "pair-mismatch"}


def refuse(message: str) -> None:
    sys.stderr.write("refused: %s\n" % message)
    raise SystemExit(2)


def canonical_self() -> None:
    here = Path(__file__).resolve()
    if os.path.normcase(str(here)) != os.path.normcase(str(CANONICAL)):
        refuse("preflight is not at its canonical root")


def load_pin() -> dict:
    if not PIN_FILE.is_file():
        refuse("reader pin is missing")
    pin = json.loads(PIN_FILE.read_text(encoding="utf-8"))
    if pin.get("path") != READER_REL or not isinstance(pin.get("sha256"), str) or not isinstance(pin.get("bytes"), int):
        refuse("reader pin is malformed")
    path = REPO / READER_REL
    body = path.read_bytes()
    digest = hashlib.sha256(body).hexdigest()
    if digest != pin["sha256"] or len(body) != pin["bytes"]:
        refuse("reader pin mismatch")
    return {"bytes": len(body), "path": READER_REL, "sha256": digest}


def run_reader(reader: Path, set_path: str, args: list[str]) -> tuple[int, str, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", str(reader), *args, "--set", set_path],
        cwd=str(REPO),
        env=env,
        capture_output=True,
        check=False,
        shell=False,
    )
    out = proc.stdout.decode("utf-8", errors="backslashreplace")
    err = proc.stderr.decode("utf-8", errors="backslashreplace")
    return proc.returncode, out, err


def parse_answer(code: int, out: str) -> dict:
    if code == 2 or out.startswith("refused:") or out.startswith("partial:"):
        refuse(out.strip() or "reader refused")
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        refuse("reader answer is not JSON")


def emit(report: dict, code: int) -> int:
    raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    sys.stdout.buffer.write(raw)
    sys.stderr.write("preflight: hold\n")
    sys.stderr.write("activation_ready: false\n")
    sys.stderr.write("validate: %s\n" % report.get("validate", {}).get("status"))
    sys.stderr.write("measured_faults: %s\n" % len(report.get("measured_faults", [])))
    sys.stderr.write("pending: combined-workbook-W, reporter-on-W\n")
    sys.stderr.write("recommendation: %s\n" % HOLD)
    return code


def base_report(reader: dict, set_path: str) -> dict:
    return {
        "schema": "app-dependency-preflight/1",
        "activation_ready": False,
        "closure": False,
        "compatibility": False,
        "release": False,
        "recommendation": HOLD,
        "report_status": "hold",
        "reader": reader,
        "set": {"path": set_path},
        "pending_slots": [dict(item) for item in PENDING],
        "uncovered": list(UNCOVERED),
        "commit_authenticated": False,
        "note": (
            "Answers cover the declared edges only. "
            "Pending slots stay pending. "
            "Identical fixture bytes are not runtime closure."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace", newline="\n")
    canonical_self()
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] != ["--set"] or len(args) != 2:
        refuse("usage: preflight.py --set ABS")
    set_path = args[1]
    if not os.path.isabs(set_path) or not os.path.isfile(set_path):
        refuse("--set must be an existing absolute file")
    reader = load_pin()
    reader_path = REPO / READER_REL
    report = base_report(reader, set_path)

    code, out, _err = run_reader(reader_path, set_path, ["validate"])
    if code == 2 or out.startswith("refused:"):
        report["reader_refused"] = True
        report["validate"] = {"exit": code, "status": "refused", "text": out.strip()}
        report["measured_faults"] = ["reader-refused:validate"]
        return emit(report, 2)
    validate = parse_answer(code, out)
    report["validate"] = {"exit": code, "status": validate.get("status")}
    report["set"]["sha256"] = validate.get("set", {}).get("sha256")
    report["basis"] = []
    for row in validate.get("records", []):
        basis = row.get("basis") or {}
        report["basis"].append({
            "declaration_id": row.get("declaration_id"),
            "kind": basis.get("kind"),
            "form": basis.get("form"),
            "verification": basis.get("verification"),
            "context_head": basis.get("context_head"),
            "commit": basis.get("commit"),
        })

    code, out, _err = run_reader(reader_path, set_path, ["identity"])
    identity = parse_answer(code, out)
    rows = []
    faults = []
    for row in identity.get("fixtures", []):
        incoming = []
        for item in row.get("incoming_pins", []):
            incoming.append({
                "from": item.get("from"),
                "requirement_id": item.get("requirement_id"),
                "form": item.get("form"),
                "relation": item.get("relation"),
            })
            if (item.get("from"), item.get("requirement_id")) == DISCLOSED and item.get("relation") in INCOMING_FAULTS:
                continue
            if item.get("relation") in INCOMING_FAULTS:
                faults.append("incoming:%s:%s:%s" % (item.get("from"), item.get("requirement_id"), item.get("relation")))
        rows.append({"module": row.get("module"), "result": row.get("result"), "incoming": incoming})
        if row.get("result") != "identical":
            faults.append("identity:%s:%s" % (row.get("module"), row.get("result")))
    report["identity"] = {"exit": code, "status": identity.get("status"), "rows": rows}

    calls = [
        ("requires-instance-door", ["requires", "--transitive", "--module", DOOR]),
        ("requires-instance-door-depth1", ["requires", "--transitive", "--depth", "1", "--module", DOOR]),
        ("explain-instance-door-pass05", ["explain", "--module", DOOR, "--to", PASS05]),
        ("impacted-pass05-depth1", ["impacted", "--depth", "1", "--module", PASS05]),
        ("requires-reporter", ["requires", "--transitive", "--module", REPORTER]),
        ("requires-selected-app", ["requires", "--transitive", "--module", SELECTED]),
    ]
    answers = {}
    command_rows = []
    for name, call in calls:
        code, out, _err = run_reader(reader_path, set_path, call)
        answer = parse_answer(code, out)
        answers[name] = answer
        command_rows.append({
            "command": name,
            "exit": code,
            "status": answer.get("status"),
            "finding_counts": answer.get("finding_counts", {}),
        })
    report["commands"] = command_rows

    edges = []
    environments = []
    disclosed = []
    for name in ("requires-instance-door", "requires-reporter", "requires-selected-app"):
        for edge in answers[name].get("requirements") or []:
            pin_form = edge.get("pin_form")
            resolution = edge.get("resolution")
            origin = edge.get("from")
            rid = edge.get("requirement_id")
            edges.append({
                "command": name,
                "from": origin,
                "requirement_id": rid,
                "pin_form": pin_form,
                "resolution": resolution,
            })
            if (origin, rid) == DISCLOSED and resolution == "pin-differs":
                disclosed.append({
                    "from": origin,
                    "requirement_id": rid,
                    "resolution": resolution,
                    "note": "The reporter pair pin expects the inert hardening dispatcher bytes.",
                })
                continue
            if resolution in EDGE_FAULTS:
                faults.append("edge:%s:%s:%s" % (origin, rid, resolution))
            target = edge.get("target") or {}
            if "environment" in target:
                environments.append(target["environment"].get("name"))
    report["edges"] = edges
    report["disclosed_dispatcher_difference"] = disclosed
    report["unknown_environment"] = sorted({name for name in environments if name})
    depth = answers["requires-instance-door-depth1"]
    names = []
    for edge in depth.get("requirements") or []:
        names.extend(item.get("finding") for item in edge.get("findings") or [])
    report["truncation"] = {
        "depth1_exit": command_rows[1]["exit"],
        "depth_limit": "depth-limit" in names,
        "impacted_status": answers["impacted-pass05-depth1"].get("status"),
        "explain_paths": len(answers["explain-instance-door-pass05"].get("paths") or []),
    }
    report["measured_faults"] = sorted(set(faults))
    return emit(report, 0 if not report["measured_faults"] else 1)


if __name__ == "__main__":
    sys.exit(main())
