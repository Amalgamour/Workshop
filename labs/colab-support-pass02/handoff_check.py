#!/usr/bin/env python3
"""Standalone consumer check for a colab-handoff/2 package.

Shows how a later workflow can validate and copy a prepared package from the
machine-readable handoff alone. Standard library only. It imports neither Colab
producer and no workflow code. It needs the expected digest from the launch.

  python -B handoff_check.py check --output ABS --expected-digest HEX --json
  python -B handoff_check.py copy  --output ABS --expected-digest HEX --to ABS --json
"""

import argparse
import hashlib
import io
import json
import os
import sys
import zipfile
from pathlib import Path

HANDOFF_SCHEMA = "colab-handoff/2"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def plain_file(path):
    probe = Path(path)
    return probe.is_file() and not probe.is_symlink()


def check(output, expected):
    root = Path(output)
    problems = []
    try:
        handoff = json.loads((root / "handoff.json").read_bytes().decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"result": "invalid", "problems": [f"handoff.json unreadable: {exc}"]}, 2
    if handoff.get("schema") != HANDOFF_SCHEMA:
        return {"result": "invalid", "problems": [f"handoff schema is {handoff.get('schema')!r}"]}, 2
    if handoff.get("digest") != expected:
        problems.append("handoff digest is not the expected launch digest")
    on_disk = sorted(p.relative_to(root).as_posix() for p in (root / "package").rglob("*") if p.is_file()) \
        if (root / "package").is_dir() else []
    listed = sorted(item["path"] for item in handoff["envelope"])
    if on_disk != listed:
        problems.append("package file set differs from the handoff envelope")
    for item in handoff["envelope"]:
        path = root / item["path"]
        if not plain_file(path):
            problems.append(f"{item['path']} is missing or linked")
            continue
        data = path.read_bytes()
        if sha256(data) != item["sha256"] or len(data) != item["bytes"]:
            problems.append(f"{item['path']} differs from the handoff")
    for name in handoff["not_created"]:
        if list(root.rglob(name)):
            problems.append(f"{name} exists although preparation must not create it")
    zip_path = root / handoff["zip"]["path"]
    try:
        raw = zip_path.read_bytes()
        if sha256(raw) != handoff["zip"]["sha256"]:
            problems.append("ZIP sha256 differs from the handoff")
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            members = {info.filename: archive.read(info.filename) for info in archive.infolist()}
        if sorted(members) != handoff["zip"]["members"]:
            problems.append("ZIP members differ from the handoff")
        for name, data in members.items():
            disk = root / "package" / name
            if not plain_file(disk) or disk.read_bytes() != data:
                problems.append(f"ZIP member {name} differs from package/")
    except (OSError, zipfile.BadZipFile) as exc:
        problems.append(f"ZIP unreadable: {exc}")
    digest = hashlib.sha256()
    for part in handoff["digest_preimage"]:
        if part["kind"] == "file":
            try:
                data = (root / part["value"]).read_bytes()
            except OSError:
                problems.append(f"preimage file {part['value']} is missing")
                data = b""
        else:
            data = part["value"].encode("utf-8")
        digest.update(len(data).to_bytes(8, "big") + data)
    if digest.hexdigest() != expected:
        problems.append("digest recomputed from the preimage is not the expected digest")
    primary = handoff["exchange"]["primary_instruction"]
    roles = [item for item in handoff["envelope"] if item["role"] == "pack-primary-instruction"]
    if [item["path"] for item in roles] != ["package/" + primary]:
        problems.append("the handoff does not name exactly one primary instruction file")
    body = {"result": "valid" if not problems else "invalid", "problems": problems,
            "digest": expected, "exchange": handoff["exchange"], "investigation": handoff["investigation"]}
    return body, (0 if not problems else 1)


def copy(output, expected, to):
    body, code = check(output, expected)
    if code:
        return body, code
    dest = Path(to)
    if dest.exists():
        return {"result": "refused", "problems": ["destination exists; nothing is overwritten"]}, 2
    handoff = json.loads((Path(output) / "handoff.json").read_bytes().decode("utf-8"))
    dest.mkdir(parents=True)
    for item in handoff["envelope"]:
        rel = item["path"][len("package/"):]
        target = dest.joinpath(*rel.split("/"))
        target.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
        fd = os.open(target, flags)
        try:
            os.write(fd, (Path(output) / item["path"]).read_bytes())
        finally:
            os.close(fd)
    for item in handoff["envelope"]:
        data = dest.joinpath(*item["path"][len("package/"):].split("/")).read_bytes()
        if sha256(data) != item["sha256"]:
            return {"result": "copy-mismatch", "problems": [item["path"]]}, 1
    body["result"] = "copied"
    body["copied"] = len(handoff["envelope"])
    return body, 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate or copy a colab-handoff/2 package without producer code.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "copy"):
        item = sub.add_parser(name)
        item.add_argument("--output", required=True)
        item.add_argument("--expected-digest", required=True)
        item.add_argument("--json", action="store_true", required=True)
        if name == "copy":
            item.add_argument("--to", required=True)
    opts = parser.parse_args(argv)
    if opts.command == "check":
        body, code = check(opts.output, opts.expected_digest)
    else:
        body, code = copy(opts.output, opts.expected_digest, opts.to)
    sys.stdout.write(json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
