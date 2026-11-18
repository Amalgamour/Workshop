#!/usr/bin/env python3
"""Confirm declared source hashes and write a request only when they match.

This helper does not walk a repository, invent task text, or mark a worker
running. A hash mismatch is a revision record, not a corruption finding.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import prime_desk as pd


def pointers(doc: dict):
    yield "tools", doc["workspace"]
    yield "book", doc["assignment"]
    if doc["legacy_selector"] is not None:
        yield "book", doc["legacy_selector"]
    yield "book", doc["catalog"]
    for key in ("references", "work", "attention", "history", "legacy", "attribution"):
        for item in doc[key]:
            yield "book", item
    for item in doc["operations"]:
        yield "tools", item
    for item in doc["workers"]:
        if item["evidence"] is not None:
            yield "book", item["evidence"]


def main(argv: list[str]) -> int:
    if len(argv) < 4 or argv[0] != "--list" or argv[2] != "--out":
        sys.stderr.write("usage: python -B labs/prime-desk-pass02/request_index.py --list ABS --out ABS [--accept REL]\n")
        return 2
    list_path = argv[1]
    out = argv[3]
    accept = set()
    index = 4
    while index < len(argv):
        if argv[index] != "--accept" or index + 1 >= len(argv):
            sys.stderr.write("usage: --accept REL\n")
            return 2
        accept.add(argv[index + 1])
        index += 2
    if not os.path.isabs(list_path) or not os.path.isabs(out):
        sys.stderr.write("list and out must be absolute\n")
        return 2
    if os.path.lexists(out):
        sys.stderr.write("output already exists\n")
        return 2
    status, first, _second = pd.read_twice(list_path)
    if status != "bytes" or first is None:
        sys.stderr.write(f"source list is {status}\n")
        return 2
    try:
        parsed = pd.parse_request(first)
        pd.prepare(parsed["doc"])
    except pd.Problem as exc:
        sys.stderr.write(f"{exc.check}: {exc.message}\n")
        return 2
    doc = parsed["doc"]
    revisions = []
    accepted = []
    for base_name, item in pointers(doc):
        base = parsed["tools"] if base_name == "tools" else parsed["root"]
        rel = item["path"]
        full = os.path.abspath(os.path.join(base, *rel.split("/")))
        if not pd.inside(base, full):
            sys.stderr.write(f"path leaves its root: {rel}\n")
            return 2
        status, data, _again = pd.read_twice(full)
        if status != "bytes" or data is None:
            revisions.append((rel, item["sha256"], None, status))
            continue
        digest = pd.sha256_bytes(data)
        if digest == item["sha256"] and len(data) == item["bytes"]:
            continue
        if rel in accept:
            item["sha256"] = digest
            item["bytes"] = len(data)
            accepted.append((rel, digest, len(data)))
            continue
        revisions.append((rel, item["sha256"], digest, str(len(data))))
    if revisions:
        sys.stdout.write("revision\n")
        for rel, declared, observed, detail in revisions:
            sys.stdout.write(f"{rel}\n")
            sys.stdout.write(f"declared {declared}\n")
            sys.stdout.write(f"observed {observed} {detail}\n")
        sys.stdout.write("This is a revision record, not proof of corruption. The request was not written.\n")
        return 1
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as handle:
        handle.write(pd.dump(doc))
    sys.stdout.write("pinned\n")
    sys.stdout.write(f"request {out}\n")
    for rel, digest, length in accepted:
        sys.stdout.write(f"explicit-accept {rel} {digest} {length}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
