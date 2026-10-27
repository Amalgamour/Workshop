"""Read-only inventory of pinned 05.NN pages.

Classification looks at heading lines. It does not extract a return body for
capture, and a disposition line is a quote, not acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


SCHEMA = "return-capture-inventory/1"
PAGE = re.compile(r"^00\.kernel/00\.00\.10\.work/[^/]+/05\.\d{2}\.md$")
RETURN_HEADING = re.compile(r"^## Return\b")
REVIEW_HEADING = re.compile(r"^## Review\b")


def git_bytes(repo: Path, *args: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise SystemExit(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout


def classify(text: str) -> dict:
    lines = text.splitlines()
    return_at = [index for index, line in enumerate(lines) if RETURN_HEADING.match(line)]
    review_at = [index for index, line in enumerate(lines) if REVIEW_HEADING.match(line)]
    quote = None
    for line in lines:
        if "Disposition:" in line:
            quote = line.strip()
            break
    if len(return_at) == 0 and not review_at:
        label = "pending"
    elif len(return_at) != 1 or review_at:
        label = "needs-prime-classification"
    else:
        start = return_at[0] + 1
        end = len(lines)
        for index in range(start, len(lines)):
            if lines[index].startswith("## "):
                end = index
                break
        body = "\n".join(lines[start:end]).strip()
        label = "pending" if body in ("", "PENDING.") else "return-present"
    return {
        "classification": label,
        "review_in_same_file": bool(review_at),
        "return_heading_count": len(return_at),
        "review_heading_count": len(review_at),
        "disposition_quote": quote,
    }


def inventory(repo: Path, commit: str) -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise SystemExit("commit must be 40 lowercase hex")
    listing = git_bytes(repo, "ls-tree", "-r", "--name-only", commit).decode("utf-8")
    records = []
    for path in listing.splitlines():
        if not PAGE.fullmatch(path):
            continue
        if "/evidence/" in path or "/pack/" in f"/{path}":
            continue
        blob = git_bytes(repo, "cat-file", "blob", f"{commit}:{path}")
        try:
            text = blob.decode("utf-8")
            decoded = True
        except UnicodeDecodeError:
            text = ""
            decoded = False
        row = {
            "path": path,
            "commit": commit,
            "sha256": hashlib.sha256(blob).hexdigest(),
            "bytes": len(blob),
            "utf8": decoded,
        }
        if decoded:
            row.update(classify(text))
        else:
            row.update(
                {
                    "classification": "needs-prime-classification",
                    "review_in_same_file": False,
                    "return_heading_count": 0,
                    "review_heading_count": 0,
                    "disposition_quote": None,
                }
            )
        records.append(row)
    records.sort(key=lambda item: item["path"])
    return {
        "schema": SCHEMA,
        "commit": commit,
        "repository": str(repo),
        "disposition_quote_is_not_acceptance": True,
        "classification_does_not_split_return_bytes": True,
        "sof_excluded": True,
        "records": records,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="inventory.py")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    payload = inventory(Path(args.repo), args.commit)
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    Path(args.out).write_bytes(text.encode("utf-8"))
    counts: dict[str, int] = {}
    for row in payload["records"]:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    sys.stdout.write(
        f"records {len(payload['records'])}\n"
        + "".join(f"{key} {counts[key]}\n" for key in sorted(counts))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
