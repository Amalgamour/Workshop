#!/usr/bin/env python3
"""Disposable counterexample for canonical Prime desk selection.

Copies pack05.02 snapshots into two new books. The first book's assignment
record is a disposable v1 record that names 0521/05.03. The second book keeps
the frozen assignment snapshot, which names 0522/05.04. Live files are hashed
for drift and are not parsed when they differ. This demo does not write the
live book, 00.live, or a source record.
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
TOOL = os.path.join(ROOT, "labs", "prime-desk-pass02", "prime_desk.py")
PY = sys.executable
PREFIX = "00.kernel/00.00.10.work/"
PACK_REL = "00.kernel/00.00.10.work/0524.prime-desk/evidence/pack05.02/source-manifest.json"

BOOK_PAGES = [
    "00.kernel/00.00.10.work/0401.goal/01.md",
    "00.kernel/00.00.10.work/0401.goal/06.01.md",
    "00.kernel/00.00.10.work/0408.seats/01.md",
    "00.kernel/00.00.10.work/0412.prime-review/06.02.md",
    "00.kernel/00.00.10.work/0416.desk-app/01.003.md",
    "00.kernel/00.00.10.work/0418.desk-operations/01.md",
    "00.kernel/00.00.10.work/0419.work-history/01.md",
    "00.kernel/00.00.10.work/0420.prime-desk/01.md",
    "00.kernel/00.00.10.work/0420.prime-desk/06.01.md",
    "00.kernel/00.00.10.work/0521.return-placement/05.03.md",
    "00.kernel/00.00.10.work/0522.review-construction/05.03.md",
    "00.kernel/00.00.10.work/0522.review-construction/05.04.md",
]
PASS01 = "labs/prime-desk-pass01/prime_desk.py"
PASS01_SHA = "b047a30324b2a764298ec69daafb9621606bdc10fe5fc45e042105f5c1f10b20"
PASS01_BYTES = 57475
REQUIRED = {
    "app/context.py",
    "app/development-workspace.json",
    "labs/prime-desk-pass01/README.md",
    "labs/prime-desk-pass01/demo.py",
    "labs/prime-desk-pass01/examples/shape.json",
    "labs/prime-desk-pass01/prime_desk.py",
    "labs/prime-desk-pass01/tests/test_prime_desk.py",
    "labs/desk-state-pass01/desk_state.py",
    "labs/prime-brief-pass01/prime_brief.py",
    "labs/state-projection-pass01/state_projection.py",
    "labs/prime-support-pass01/prime_support.py",
}
HEAD_0521 = "# 05 - Return-line writer, reader and staged migration integration"
HEAD_0522 = "# 05 - Real custody into the Prime review loop"
DIRECTOR_SPAN = (111, 403)
MODEL_SPAN = (430, 834)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pin_table() -> tuple[str, dict]:
    manifest = os.path.join(ROOT, *PACK_REL.split("/"))
    with open(manifest, "rb") as handle:
        doc = json.loads(handle.read().decode("utf-8"))
    return os.path.dirname(manifest), {row["path"]: row for row in doc["sources"]}


def snapshot_bytes(pack: str, row: dict) -> bytes:
    path = os.path.join(pack, *row["snapshot"].split("/"))
    with open(path, "rb") as handle:
        data = handle.read()
    if sha256_bytes(data) != row["sha256"] or len(data) != row["bytes"]:
        raise SystemExit(f"snapshot pin mismatch: {row['path']}")
    return data


def live_stat(rel: str) -> tuple[str, int]:
    path = os.path.join(ROOT, *rel.split("/"))
    with open(path, "rb") as handle:
        data = handle.read()
    return sha256_bytes(data), len(data)


def book_rel(full: str) -> str:
    return full.split(PREFIX, 1)[1]


def write_bytes(book: str, rel: str, data: bytes) -> dict:
    path = os.path.join(book, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)
    return {"path": rel, "sha256": sha256_bytes(data), "bytes": len(data)}


def assignment_0521() -> bytes:
    text = (
        "record: current-assignment\n"
        "schema: 00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1\n"
        "desk: 00.kernel\n"
        "book: 00.00.10.work\n"
        "workflow_space: 0\n"
        "current_work: 00.kernel/00.00.10.work/0521.return-placement/05.03.md\n"
        "pack: 00.kernel/00.00.10.work/0521.return-placement/05.03.md\n"
        "assignment_state: returned\n"
        "waits_on: none\n"
        "next: review\n"
        "updated: 2026-11-01\n"
    )
    return text.encode("utf-8")


def copy_book(book: str, pack: str, pins: dict, assignment: bytes | None) -> dict[str, dict]:
    copied = {}
    for full in BOOK_PAGES:
        data = snapshot_bytes(pack, pins[full])
        rel = book_rel(full)
        copied[rel] = write_bytes(book, rel, data)
    if assignment is not None:
        copied["0401.goal/06.01.md"] = write_bytes(book, "0401.goal/06.01.md", assignment)
    copied["checkpoint.md"] = write_bytes(book, "checkpoint.md", b"CHECKPOINT\n")
    copied["verified.md"] = write_bytes(book, "verified.md", b"VERIFIED\n")
    copied["talk.md"] = write_bytes(book, "talk.md", b'python -c "print(987654)"\n')
    return copied


def file_pointer(copied: dict, rel: str) -> dict:
    return dict(copied[rel])


def json_pointer(book: str, rel: str, body: dict) -> dict:
    data = (json.dumps(body, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    return write_bytes(book, rel, data)


def tool_pointer(rel: str) -> dict:
    path = os.path.join(ROOT, *rel.split("/"))
    with open(path, "rb") as handle:
        data = handle.read()
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


def build_request(book: str, copied: dict, canonical_id: str, legacy_id: str, catalog_id: str, workspace: dict) -> dict:
    selector = json_pointer(book, "selector.json", {
        "schema": "prime-desk-selector/1",
        "selected_work_id": legacy_id,
        "checkpoint": None,
        "verified_result": None,
        "next_route": None,
    })
    catalog = json_pointer(book, "catalog.json", {
        "schema": "prime-desk-catalog/2",
        "items": [{
            "work_id": catalog_id,
            "address": "0522.review-construction/05.04",
            "label": "supplied index",
            "provenance": "index note only; not a selection",
        }],
    })
    operations = []
    for name, rel, limitation in (
        ("desk-state", "labs/desk-state-pass01/desk_state.py", "view launches subprocesses; this desk does not call it"),
        ("prime-brief", "labs/prime-brief-pass01/prime_brief.py", "build was not called"),
        ("state-projection", "labs/state-projection-pass01/state_projection.py", "project and inspect were not called"),
        ("prime-support", "labs/prime-support-pass01/prime_support.py", "status uses Git; this desk does not call it"),
    ):
        operations.append({
            "id": name,
            "name": name,
            "limitation": limitation,
            "past_tests": "unknown",
            "activation": "unknown",
            **tool_pointer(rel),
        })
    director = file_pointer(copied, "0420.prime-desk/06.01.md")
    return {
        "schema": "prime-desk-request/2",
        "instance": {"root": book, "book": "00.00.10.work", "role": "prime", "tools_root": ROOT},
        "workspace": workspace,
        "assignment": file_pointer(copied, "0401.goal/06.01.md"),
        "legacy_selector": selector,
        "coverage": "declared-paths",
        "references": [
            {"id": "goal", "role": "goal", "label": "goal page", "binding": {"scope": "desk"}, **file_pointer(copied, "0401.goal/01.md")},
            {"id": "scope", "role": "scope", "label": "seats page", "binding": {"scope": "desk"}, **file_pointer(copied, "0408.seats/01.md")},
            {"id": "authority", "role": "authority", "label": "desk-app direction", "binding": {"scope": "desk"}, **file_pointer(copied, "0416.desk-app/01.003.md")},
            {"id": "policy", "role": "dependency", "label": "reporting policy", "binding": {"scope": "desk"}, **file_pointer(copied, "0412.prime-review/06.02.md")},
            {"id": "crit-0521", "role": "criteria", "label": "0521 task", "binding": {"scope": "work", "work_id": "work-0521-0503"}, **file_pointer(copied, "0521.return-placement/05.03.md")},
            {"id": "crit-0522", "role": "criteria", "label": "0522 task", "binding": {"scope": "work", "work_id": "work-0522-0504"}, **file_pointer(copied, "0522.review-construction/05.04.md")},
            {"id": "ret-0522", "role": "return", "label": "0522 return", "binding": {"scope": "work", "work_id": "work-0522-0504"}, **file_pointer(copied, "0522.review-construction/05.04.md")},
            {"id": "check", "role": "checkpoint", "label": "checkpoint", "binding": {"scope": "work", "work_id": canonical_id}, **file_pointer(copied, "checkpoint.md")},
            {"id": "ver", "role": "verification", "label": "verification", "binding": {"scope": "work", "work_id": canonical_id}, **file_pointer(copied, "verified.md")},
            {"id": "talk", "role": "talk", "label": "quoted command", "binding": {"scope": "desk"}, **file_pointer(copied, "talk.md")},
        ],
        "work": [
            {"id": "work-0521-0503", "address": "0521.return-placement/05.03", **file_pointer(copied, "0521.return-placement/05.03.md")},
            {"id": "work-0522-0504", "address": "0522.review-construction/05.04", **file_pointer(copied, "0522.review-construction/05.04.md")},
            {"id": "work-0522-0503", "address": "0522.review-construction/05.03", **file_pointer(copied, "0522.review-construction/05.03.md")},
        ],
        "workers": [{"id": "grok-2", "work_id": canonical_id, "evidence": None}],
        "supplied": [{
            "id": "sup-grok-2",
            "speaker": "codex-prime",
            "about": "grok-2",
            "text": "Director says the worker is running",
            "limit": "supplied label, not a live process check",
        }],
        "attention": [{
            "id": "hold-live",
            "kind": "hold",
            "open": True,
            "label": "live desk activation is not approved",
            **file_pointer(copied, "0420.prime-desk/01.md"),
        }],
        "history": [{"id": "hist-0419", **file_pointer(copied, "0419.work-history/01.md")}],
        "catalog": catalog,
        "operations": operations,
        "legacy": [],
        "foreign": [],
        "attribution": [
            {"id": "dir", "author": "director", "start": DIRECTOR_SPAN[0], "end": DIRECTOR_SPAN[1], "binding": {"scope": "desk"}, **director},
            {"id": "mod", "author": "model", "start": MODEL_SPAN[0], "end": MODEL_SPAN[1], "binding": {"scope": "desk"}, **director},
        ],
    }


def run_tool(out: str, name: str, args: list[str]) -> int:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([PY, "-B", TOOL, *args], cwd=ROOT, capture_output=True, env=env)
    with open(os.path.join(out, name), "wb") as handle:
        handle.write(proc.stdout)
    with open(os.path.join(out, name + ".exit"), "wb") as handle:
        handle.write(f"{proc.returncode}\n".encode("utf-8"))
        handle.write(proc.stderr)
    return proc.returncode


def load_json(path: str) -> dict:
    with open(path, "rb") as handle:
        return json.loads(handle.read().decode("utf-8"))


def home_section(text: str) -> str:
    return text.split("### Review home")[1].split("### Next routes")[0]


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def check_case(out: str, stem: str, work_id: str, review: str, heading: str, other: str, criteria: list[str], returns: list[str], source: bytes) -> dict:
    suffix = stem[len("view"):]
    doc = load_json(os.path.join(out, stem + ".json"))
    text = read_text(os.path.join(out, stem + ".md"))
    packet_text = read_text(os.path.join(out, "packet" + suffix + ".md"))
    packet = load_json(os.path.join(out, "packet" + suffix + ".json"))
    expect(doc["exit"] == 1, f"{stem} exit {doc['exit']}")
    expect(doc["selected"]["id"] == work_id, f"{stem} selected {doc['selected']}")
    expect(doc["selected"]["rule"] == "assignment-record/v1", f"{stem} rule")
    expect(doc["selected"]["legacy_selector"]["agrees"] is False, f"{stem} legacy agreement")
    expect(doc["catalog"]["used_for_selection"] is False, f"{stem} catalog selection")
    expect(doc["selected"]["review_home"]["address"] == review, f"{stem} review home")
    expect("Pending custody" in doc["selected"]["review_home"]["limit"], f"{stem} custody")
    expect(doc["inspectability"]["fingerprint"] == packet["inspectability"]["fingerprint"], f"{stem} fingerprint")
    expect(heading in packet_text and other not in packet_text, f"{stem} packet heading")
    home = home_section(packet_text)
    expect(review in home and "0412.prime-review/06.02.md" not in home, f"{stem} review section")
    expect([item["id"] for item in packet["packet"]["criteria"]] == criteria, f"{stem} criteria")
    expect([item["id"] for item in packet["packet"]["returns"]] == returns, f"{stem} returns")
    director = packet["packet"]["director"][0]["text"].encode("utf-8")
    model = packet["packet"]["model"][0]["text"].encode("utf-8")
    expect(director == source[DIRECTOR_SPAN[0]:DIRECTOR_SPAN[1]], f"{stem} director span")
    expect(model == source[MODEL_SPAN[0]:MODEL_SPAN[1]], f"{stem} model span")
    expect(director.startswith(b"> I like it."), f"{stem} director opening")
    expect(b"not permission to migrate" not in director, f"{stem} director mixed")
    expect(model.startswith(b"The proposed"), f"{stem} model opening")
    expect("Process activity: unknown." in text, f"{stem} process")
    expect("Association basis supplied." in text, f"{stem} association")
    expect("not a live process check" in text, f"{stem} assignment state")
    expect("Not parsed. Not executable." in text, f"{stem} talk")
    expect("Successor modules were not imported." in text, f"{stem} review loop")
    expect(doc["coverage"]["stale"] == 0 and doc["coverage"]["changed"] == 0, f"{stem} coverage")
    return doc


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--out" or not os.path.isabs(argv[1]):
        sys.stderr.write("usage: python -B labs/prime-desk-pass02/demo.py --out ABS\n")
        return 2
    out = argv[1]
    if os.path.lexists(out):
        sys.stderr.write("demo output already exists\n")
        return 2
    pack, pins = pin_table()
    drifts = []
    blockers = []
    for path, row in pins.items():
        digest, size = live_stat(path)
        if digest == row["sha256"] and size == row["bytes"]:
            continue
        drifts.append(f"{path}\nlive {digest} {size}\npin {row['sha256']} {row['bytes']}\nparsed false\n")
        if path in REQUIRED:
            blockers.append(path)
    pass01 = tool_pointer(PASS01)
    if pass01["sha256"] != PASS01_SHA or pass01["bytes"] != PASS01_BYTES:
        blockers.append(PASS01)
        drifts.append(f"{PASS01}\nlive {pass01['sha256']} {pass01['bytes']}\npin {PASS01_SHA} {PASS01_BYTES}\nparsed false\n")
    os.makedirs(out)
    drift_path = os.path.join(out, "live-drift.txt")
    if blockers:
        with open(drift_path, "wb") as handle:
            handle.write(b"required pin moved. No book was copied. New live bytes were not parsed.\n")
            handle.write("\n".join(drifts).encode("utf-8"))
        sys.stderr.write("required pin moved: " + ", ".join(blockers) + "\n")
        return 2
    with open(drift_path, "wb") as handle:
        if drifts:
            handle.write(b"live files differ from the pack pin. Request books copy the snapshots. New live bytes were not parsed.\n")
            handle.write("\n".join(drifts).encode("utf-8"))
        else:
            handle.write(b"live files matched the pack pins at copy time\n")
    frozen = snapshot_bytes(pack, pins[PREFIX + "0401.goal/06.01.md"])
    if b"current_work: 00.kernel/00.00.10.work/0522.review-construction/05.04.md\n" not in frozen:
        sys.stderr.write("frozen assignment snapshot does not name 0522/05.04\n")
        return 2
    source = snapshot_bytes(pack, pins[PREFIX + "0420.prime-desk/06.01.md"])
    workspace = tool_pointer("app/development-workspace.json")
    book_a = os.path.join(out, "book")
    book_b = os.path.join(out, "book-0522")
    copied_a = copy_book(book_a, pack, pins, assignment_0521())
    copied_b = copy_book(book_b, pack, pins, None)
    note = (
        "book/0401.goal/06.01.md is a disposable assignment-record v1 whose current_work is 0521/05.03.\n"
        "book-0522/0401.goal/06.01.md is the pack snapshot whose current_work is 0522/05.04.\n"
        "The live assignment file was not written.\n"
    )
    with open(os.path.join(out, "books.txt"), "wb") as handle:
        handle.write(note.encode("utf-8"))
    request_a = build_request(book_a, copied_a, "work-0521-0503", "work-0522-0504", "work-0522-0504", workspace)
    request_b = build_request(book_b, copied_b, "work-0522-0504", "work-0521-0503", "work-0522-0504", workspace)
    path_a = os.path.join(out, "request.json")
    path_b = os.path.join(out, "request-0522.json")
    for path, body in ((path_a, request_a), (path_b, request_b)):
        with open(path, "wb") as handle:
            handle.write((json.dumps(body, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    live = os.path.join(ROOT, "00.kernel", "00.live.md")
    with open(live, "rb") as handle:
        live_before = handle.read()
    before = {book_a: fingerprint(book_a), book_b: fingerprint(book_b)}
    commands = (
        ("view.md", ["view", "--request", path_a]),
        ("view.json", ["view", "--request", path_a, "--json"]),
        ("packet.md", ["packet", "--request", path_a, "--work-id", "work-0521-0503"]),
        ("packet.json", ["packet", "--request", path_a, "--work-id", "work-0521-0503", "--json"]),
        ("view-0522.md", ["view", "--request", path_b]),
        ("view-0522.json", ["view", "--request", path_b, "--json"]),
        ("packet-0522.md", ["packet", "--request", path_b, "--work-id", "work-0522-0504"]),
        ("packet-0522.json", ["packet", "--request", path_b, "--work-id", "work-0522-0504", "--json"]),
    )
    for name, args in commands:
        code = run_tool(out, name, args)
        if code not in (0, 1):
            sys.stderr.write(f"{name} exit {code}\n")
            return code
    after = {book_a: fingerprint(book_a), book_b: fingerprint(book_b)}
    with open(live, "rb") as handle:
        live_after = handle.read()
    if before != after or live_before != live_after:
        sys.stderr.write("book or 00.live bytes changed\n")
        return 2
    try:
        left = check_case(out, "view", "work-0521-0503", "0121.return-placement/05.03", HEAD_0521, HEAD_0522, ["crit-0521"], [], source)
        right = check_case(out, "view-0522", "work-0522-0504", "0122.review-construction/05.04", HEAD_0522, HEAD_0521, ["crit-0522"], ["ret-0522"], source)
    except SystemExit as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2
    packet_a = open(os.path.join(out, "packet.md"), encoding="utf-8").read()
    packet_b = open(os.path.join(out, "packet-0522.md"), encoding="utf-8").read()
    if packet_a == packet_b:
        sys.stderr.write("packets are identical\n")
        return 2
    sys.stdout.write("demo ok\n")
    sys.stdout.write(f"out {out}\n")
    sys.stdout.write(f"selected {left['selected']['id']}\n")
    sys.stdout.write(f"selected-0522 {right['selected']['id']}\n")
    sys.stdout.write(f"exit {left['exit']}\n")
    sys.stdout.write(f"exit-0522 {right['exit']}\n")
    sys.stdout.write(f"request {left['inspectability']['request_sha256']}\n")
    sys.stdout.write(f"fingerprint {left['inspectability']['fingerprint']}\n")
    sys.stdout.write(f"observed {left['observed_at']}\n")
    sys.stdout.write(f"live-drift {len(drifts)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
