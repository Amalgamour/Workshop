"""Bounded read-only rehearsal harness (0507.prime-support/05.14). Retained evidence, not an installed runtime.

  python -B 00.kernel/00.00.10.work/0507.prime-support/evidence/realbrief05.14/rehearse.py

Runs the accepted, pinned reader once per page named in realbrief-input05.14/source-spec.json, at its exact commit,
feeds the unchanged reports plus the exact Prime-supplied coordination into the pinned prime brief, and writes only
results.json and brief.txt beside this file. No HEAD discovery, queue, capture, model call or dispatch.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

WS = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / "realbrief-input05.14"
PACK = HERE.parent / "pack05.14" / "source-manifest.json"
BOOK_DIR = WS / "00.kernel" / "00.00.10.work"
READER = WS / "labs/batch-observation-pass01/batch_observe.py"
BRIEF = WS / "labs/prime-brief-pass01/prime_brief.py"
FROM_PACK = ["labs/batch-observation-pass01/batch_observe.py", "labs/prime-support-pass01/prime_support.py",
             "labs/prime-support-pass01/clerk_adapter.py", "labs/return-capture-pass01/return_inspect.py",
             "labs/return-capture-pass01/return_capture.py", "labs/state-projection-pass01/state_projection.py"]
BRIEF_SHA256 = "302ed832d2fa955a591420f13d3b22ce91e4a7669c69a778d443fc82627580d7"  # the repaired brief (05.14)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def main() -> int:
    errors = []
    manifest = json.loads(PACK.read_bytes())
    pinned = {s["path"]: s["sha256"] for s in manifest["sources"]}
    pins = {p: {"expected": pinned[p], "live": sha((WS / p).read_bytes())} for p in FROM_PACK}
    pins["labs/prime-brief-pass01/prime_brief.py"] = {"expected": BRIEF_SHA256, "live": sha(BRIEF.read_bytes())}
    for p, v in pins.items():
        v["match"] = v["expected"] == v["live"]
    if not all(v["match"] for v in pins.values()):
        print("refused: a pinned tool does not match; nothing was launched")
        print(json.dumps(pins, indent=1))
        return 2
    raw_inputs = {n: (INPUTS / n).read_bytes() for n in ("source-spec.json", "coordination.json", "coordination-provenance.json")}
    spec = json.loads(raw_inputs["source-spec.json"])
    coordination = json.loads(raw_inputs["coordination.json"])
    calls, observations = [], []
    for page in spec["pages"]:
        argv = [sys.executable, "-B", str(READER), "observe", "--json", "--repo", str(WS), "--commit", spec["commit"],
                "--path", page["path"], "--members-book", str(BOOK_DIR)]
        started = now()
        p = subprocess.run(argv, capture_output=True, timeout=300)
        finished = now()
        call = {"page": page["path"], "batch_id": page["batch_id"], "expected": page["expected"], "argv": argv, "exit": p.returncode,
                "started_at": started, "finished_at": finished, "stdout_text": p.stdout.decode("utf-8"), "stdout_sha256": sha(p.stdout),
                "stdout_bytes": len(p.stdout), "stderr_text": p.stderr.decode("utf-8", "replace"), "stderr_sha256": sha(p.stderr)}
        calls.append(call)
        if p.returncode in (0, 1) and p.stdout:
            report = json.loads(p.stdout)
            observations.append({"label": "SUPPLIED", "note": f"unchanged report of the pinned reader run by rehearse.py at {started}; stdout sha256 {call['stdout_sha256']}",
                                 "observation": report})
        else:
            errors.append(f"reader refused {page['path']} (exit {p.returncode})")
    adapter_input = {"schema": "prime-brief-input/1", "scope": {"book": spec["book"], "lanes": spec["lanes"]},
                     "members_book": str(BOOK_DIR), "observations": observations, "coordination": coordination}
    adapter_bytes = json.dumps(adapter_input, ensure_ascii=False, indent=1).encode("utf-8")
    runs = {}
    with tempfile.TemporaryDirectory(prefix="realbrief-0514-") as tmp:
        path = Path(tmp) / "adapter-input.json"
        path.write_bytes(adapter_bytes)
        for mode, extra in (("json", ["--json"]), ("text", [])):
            argv = [sys.executable, "-B", str(BRIEF), "brief", "--input", str(path), "--inspect", *extra]
            started = now()
            p = subprocess.run(argv, capture_output=True, timeout=600)
            runs[mode] = {"argv": [a if a != str(path) else "<temp>/adapter-input.json" for a in argv], "exit": p.returncode,
                          "started_at": started, "finished_at": now(), "stdout_sha256": sha(p.stdout), "stdout_text": p.stdout.decode("utf-8"),
                          "stderr_text": p.stderr.decode("utf-8", "replace")}
    brief_json = json.loads(runs["json"]["stdout_text"]) if runs["json"]["stdout_text"].startswith("{") else None
    outcomes = []
    if brief_json:
        where = {}
        for key, items in brief_json["brief"].items():
            for it in items:
                where[it["id"]] = (key, it.get("lifecycle"), it["reason"], it.get("followup"))
        for page in spec["pages"]:
            got = where.get(page["batch_id"])
            outcomes.append({"batch_id": page["batch_id"], "expected": page["expected"], "list": got and got[0], "lifecycle": got and got[1],
                             "reason": got and got[2], "followup": got and got[3]})
    results = {"schema": "realbrief-rehearsal-results/1", "batch": "0507.prime-support/05.14", "who": "claude-opus-5-5",
               "note": "a bounded read-only rehearsal; the pinned reader was actually run by this harness, and its reports are "
                       "labelled SUPPLIED at the adapter boundary; coordination is Prime's supplied interpretation, not authentication",
               "workspace": str(WS), "source_commit": spec["commit"], "pins": pins,
               "inputs": {n: {"sha256": sha(b), "bytes": len(b), "text": b.decode("utf-8")} for n, b in raw_inputs.items()},
               "reader_calls": calls,
               "adapter_input": {"sha256": sha(adapter_bytes), "bytes": len(adapter_bytes), "text": adapter_bytes.decode("utf-8")},
               "brief_runs": runs, "brief": brief_json, "outcomes": outcomes, "errors": errors}
    (HERE / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (HERE / "brief.txt").write_text(runs["text"]["stdout_text"].replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    for o in outcomes:
        print(f"{o['batch_id']}: {o['list']} {o['lifecycle']} | expected: {o['expected']}")
    print("errors:", errors)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
