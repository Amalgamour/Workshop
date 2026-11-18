#!/usr/bin/env python3
"""Build a disposable book from pinned work-page bytes and print one real view.

The live work book is only read. Copies and the request live under --out.
This demo does not write 00.live, launch a worker, or call Git.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
TOOL = os.path.join(ROOT, "labs", "prime-desk-pass01", "prime_desk.py")
PY = sys.executable

PAGES = [
    "00.kernel/00.00.10.work/0401.goal/01.md",
    "00.kernel/00.00.10.work/0401.goal/06.01.md",
    "00.kernel/00.00.10.work/0408.seats/01.md",
    "00.kernel/00.00.10.work/0416.desk-app/01.003.md",
    "00.kernel/00.00.10.work/0418.desk-operations/01.md",
    "00.kernel/00.00.10.work/0419.work-history/01.md",
    "00.kernel/00.00.10.work/0420.prime-desk/01.md",
    "00.kernel/00.00.10.work/0420.prime-desk/06.01.md",
    "00.kernel/00.00.10.work/0420.prime-desk/06.02.md",
    "00.kernel/00.00.10.work/0412.prime-review/06.02.md",
    "00.kernel/00.00.10.work/0521.return-placement/05.03.md",
    "00.kernel/00.00.10.work/0522.review-construction/05.03.md",
    "00.kernel/00.00.10.work/0522.review-construction/05.04.md",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pin_table() -> tuple[str, dict[str, tuple[str, int, str]]]:
    manifest = os.path.join(
        ROOT, "00.kernel", "00.00.10.work", "0524.prime-desk", "evidence", "pack05.01", "source-manifest.json",
    )
    with open(manifest, "rb") as handle:
        doc = json.loads(handle.read().decode("utf-8"))
    pins = {row["path"]: (row["sha256"], row["bytes"], row["snapshot"]) for row in doc["sources"]}
    return os.path.dirname(manifest), pins


def copy_pages(book: str, pack: str, pins: dict[str, tuple[str, int, str]]) -> tuple[dict[str, dict], list[str]]:
    copied = {}
    drifts = []
    for rel in PAGES:
        expect, size, snapshot = pins[rel]
        src = os.path.join(pack, *snapshot.split("/"))
        with open(src, "rb") as handle:
            data = handle.read()
        got = sha256_bytes(data)
        if got != expect or len(data) != size:
            raise SystemExit(f"snapshot pin mismatch: {rel}")
        live = os.path.join(ROOT, *rel.split("/"))
        with open(live, "rb") as handle:
            live_data = handle.read()
        live_sha = sha256_bytes(live_data)
        if live_sha != expect or len(live_data) != size:
            drifts.append(f"{rel}\nlive {live_sha} {len(live_data)}\npin {expect} {size}\n")
        dest_rel = rel.split("00.kernel/00.00.10.work/", 1)[1]
        dest = os.path.join(book, *dest_rel.split("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as handle:
            handle.write(data)
        copied[dest_rel] = {"path": dest_rel, "sha256": got, "bytes": len(data)}
    return copied, drifts


def pointer(copied: dict[str, dict], rel: str) -> dict:
    return dict(copied[rel])


def book_pointer(book: str, rel: str, body: dict) -> dict:
    path = os.path.join(book, *rel.split("/"))
    data = (json.dumps(body, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)
    return {"path": rel, "sha256": sha256_bytes(data), "bytes": len(data)}


def fingerprint(root: str) -> str:
    rows = []
    for dirpath, _dirs, names in os.walk(root):
        for name in sorted(names):
            path = os.path.join(dirpath, name)
            with open(path, "rb") as handle:
                data = handle.read()
            rel = os.path.relpath(path, root).replace("\\", "/")
            rows.append(f"{rel}\n{sha256_bytes(data)}\n{len(data)}\n")
    return sha256_bytes("".join(sorted(rows)).encode("utf-8"))


def live_fingerprint() -> str:
    rows = []
    for rel in PAGES:
        path = os.path.join(ROOT, *rel.split("/"))
        with open(path, "rb") as handle:
            data = handle.read()
        rows.append(f"{rel}\n{sha256_bytes(data)}\n{len(data)}\n")
    return sha256_bytes("".join(rows).encode("utf-8"))


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--out" or not os.path.isabs(argv[1]):
        sys.stderr.write("usage: python -B labs/prime-desk-pass01/demo.py --out ABS\n")
        return 2
    out = argv[1]
    book = os.path.join(out, "book")
    if os.path.lexists(book):
        sys.stderr.write("demo output book already exists\n")
        return 2
    os.makedirs(out)
    before_live = live_fingerprint()
    pack, pins = pin_table()
    copied, drifts = copy_pages(book, pack, pins)
    with open(os.path.join(out, "live-drift.txt"), "wb") as handle:
        if drifts:
            handle.write(("live files differ from the pack pin. The book copies are the snapshots. The new live bytes were not parsed.\n" + "\n".join(drifts)).encode("utf-8"))
        else:
            handle.write(b"live files matched the pack pins at copy time\n")
    evidence = book_pointer(book, "workers/grok-2.json", {
        "schema": "prime-desk-worker-evidence/1",
        "state": "claimed",
        "note": "recorded claim file written for this disposable copy; not a process check",
    })
    selector = book_pointer(book, "selector.json", {
        "schema": "prime-desk-selector/1",
        "selected_work_id": "work-0522-0504",
        "checkpoint": pointer(copied, "0420.prime-desk/06.02.md"),
        "verified_result": None,
        "next_route": {**pointer(copied, "0420.prime-desk/01.md"), "speaker": "codex-prime"},
    })
    catalog = book_pointer(book, "catalog.json", {
        "schema": "prime-desk-catalog/1",
        "items": [
            {"work_id": "work-0521-0503", "address": "0521.return-placement/05.03", "label": "pinned page index; not the selector"},
        ],
    })
    ops = []
    for name, rel, limitation in (
        ("desk-state", "labs/desk-state-pass01/desk_state.py", "view launches subprocesses; this desk does not call it"),
        ("prime-brief", "labs/prime-brief-pass01/prime_brief.py", "fixture brief; build is not called from this desk"),
        ("state-projection", "labs/state-projection-pass01/state_projection.py", "fixture lifecycle; project and inspect are not called"),
        ("prime-support", "labs/prime-support-pass01/prime_support.py", "status uses Git; this desk does not call it"),
    ):
        full = os.path.join(ROOT, *rel.split("/"))
        with open(full, "rb") as handle:
            data = handle.read()
        ops.append({
            "id": name,
            "name": name,
            "path": rel,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "limitation": limitation,
            "past_tests": "unknown",
            "activation": "unknown",
        })
    request = {
        "schema": "prime-desk-request/1",
        "instance": {"root": book, "book": "00.00.10.work", "role": "prime", "tools_root": ROOT},
        "selector": selector,
        "references": [
            {"id": "goal", "role": "goal", "label": "goal page", **pointer(copied, "0401.goal/01.md")},
            {"id": "scope", "role": "scope", "label": "seats page", **pointer(copied, "0408.seats/01.md")},
            {"id": "authority", "role": "authority", "label": "desk-app direction", **pointer(copied, "0416.desk-app/01.003.md")},
            {"id": "assign", "role": "assignment", "label": "current-assignment record", **pointer(copied, "0401.goal/06.01.md")},
            {"id": "director", "role": "director", "label": "Director approval file, quoted whole", **pointer(copied, "0420.prime-desk/06.01.md")},
            {"id": "model", "role": "model", "label": "Prime coordination note, separate file", **pointer(copied, "0420.prime-desk/06.02.md")},
            {"id": "criteria", "role": "criteria", "label": "deliverable page", **pointer(copied, "0420.prime-desk/01.md")},
            {"id": "review-home", "role": "review-home", "label": "Director-facing review landing", **pointer(copied, "0412.prime-review/06.02.md")},
            {"id": "dependency", "role": "dependency", "label": "desk operations ideas", **pointer(copied, "0418.desk-operations/01.md")},
            {"id": "ret", "role": "return", "label": "no return copied", "path": "missing-return.md", "sha256": "0" * 64, "bytes": 0},
            {"id": "talk", "role": "talk", "label": "work history is talk, not a command", **pointer(copied, "0419.work-history/01.md")},
        ],
        "work": [
            {"id": "work-0522-0504", "address": "0522.review-construction/05.04", **pointer(copied, "0522.review-construction/05.04.md")},
            {"id": "work-0522-0503", "address": "0522.review-construction/05.03", **pointer(copied, "0522.review-construction/05.03.md")},
            {"id": "work-0521-0503", "address": "0521.return-placement/05.03", **pointer(copied, "0521.return-placement/05.03.md")},
        ],
        "workers": [
            {"id": "grok-2", "work_id": "work-0522-0504", "evidence": evidence},
            {"id": "claude", "work_id": "work-0521-0503", "evidence": None},
        ],
        "supplied": [{
            "id": "sup-grok-2",
            "speaker": "codex-prime",
            "about": "grok-2",
            "text": "Director reported Grok-2 working",
            "limit": "recorded report in 0420.prime-desk/06.02.md; not a live process check",
        }],
        "attention": [{
            "id": "hold-placement",
            "kind": "hold",
            "open": True,
            "label": "live return migration is not approved",
            **pointer(copied, "0420.prime-desk/01.md"),
        }],
        "history": [{"id": "hist-0419", **pointer(copied, "0419.work-history/01.md")}],
        "catalog": catalog,
        "operations": ops,
        "legacy": [],
        "foreign": [],
    }
    request_path = os.path.join(out, "request.json")
    with open(request_path, "wb") as handle:
        handle.write((json.dumps(request, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    before_book = fingerprint(book)
    commands = (
        ("view.md", ["view", "--request", request_path]),
        ("view.json", ["view", "--request", request_path, "--json"]),
        ("packet.md", ["packet", "--request", request_path, "--work-id", "work-0522-0504"]),
        ("packet.json", ["packet", "--request", request_path, "--work-id", "work-0522-0504", "--json"]),
    )
    for name, args in commands:
        proc = subprocess.run([PY, "-B", TOOL, *args], cwd=ROOT, capture_output=True)
        with open(os.path.join(out, name), "wb") as handle:
            handle.write(proc.stdout)
        with open(os.path.join(out, name + ".exit"), "wb") as handle:
            handle.write(f"{proc.returncode}\n".encode("utf-8"))
            handle.write(proc.stderr)
        if proc.returncode not in (0, 1):
            sys.stderr.write(proc.stderr.decode("utf-8", "replace"))
            return proc.returncode
    after_book = fingerprint(book)
    after_live = live_fingerprint()
    if before_book != after_book or before_live != after_live:
        sys.stderr.write("fingerprint changed\n")
        return 2
    view = json.loads(open(os.path.join(out, "view.json"), encoding="utf-8").read())
    if view["selected"]["id"] != "work-0522-0504":
        sys.stderr.write("selector was not kept\n")
        return 2
    if view["selected"]["verified_result"]["basis"] != "unknown":
        sys.stderr.write("verification was invented\n")
        return 2
    sys.stdout.write("demo ok\n")
    sys.stdout.write(f"out {out}\n")
    sys.stdout.write(f"selected {view['selected']['id']}\n")
    sys.stdout.write(f"exit {view['exit']}\n")
    sys.stdout.write(f"live-drift {len(drifts)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
