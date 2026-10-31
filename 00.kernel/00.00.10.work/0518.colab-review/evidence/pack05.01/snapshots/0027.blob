"""Disposable local capture, retrospective fixtures, and one local publication.

The publication repository is separate from the sealed book. This script may
call Git. return_capture.py does not.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import return_capture as rc

PIN = "e6d6eb75538732c7eedbc840042242d386b25c2f"
SNAPSHOTS = {
    "0007.blob": (
        "51332cea6913d812c940574432a891f05c4b2667719f465b4a613dbea0a62cf6",
        13251,
    ),
    "0008.blob": (
        "0c91acfe02943770c25950670bbcfc5b6fe732a747707185f7d40bf00968c983",
        17634,
    ),
    "0009.blob": (
        "fb30c940ea36b62b9e673d124834702c3be4ce260730f46aa0883077b1a7c943",
        3632,
    ),
}


def outside_git(path: Path) -> bool:
    current = path.resolve()
    while True:
        if (current / ".git").exists():
            return False
        if current.parent == current:
            return True
        current = current.parent


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True)
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace")
        raise SystemExit(f"{' '.join(cmd)} failed\n{detail}")
    return proc


def copy_bytes(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for dirpath, dirnames, filenames in os.walk(src):
        base = Path(dirpath)
        target = dst / base.relative_to(src)
        target.mkdir(parents=True, exist_ok=True)
        for name in dirnames:
            path = base / name
            if path.is_symlink():
                raise SystemExit(f"refusing to copy a link: {path}")
        for name in filenames:
            path = base / name
            if path.is_symlink():
                raise SystemExit(f"refusing to copy a link: {path}")
            (target / name).write_bytes(path.read_bytes())


def member_files(root: Path) -> list[Path]:
    found = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            found.append(Path(dirpath) / name)
    return sorted(found)


def write_json(path: Path, payload: dict) -> None:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    path.write_bytes(text.encode("utf-8"))


def require_snapshot(directory: Path, name: str) -> bytes:
    data = (directory / name).read_bytes()
    digest, size = SNAPSHOTS[name]
    if sha256_bytes(data) != digest or len(data) != size:
        raise SystemExit(f"snapshot {name} does not match the pin")
    return data


def capture_publication(parent: Path, log: list[str]) -> dict:
    book = parent / "publication-book"
    source = parent / "publication-source"
    book.mkdir()
    source.mkdir()
    if not outside_git(book):
        raise SystemExit("publication book is inside Git")
    return_file = parent / "publication-return.md"
    return_file.write_bytes(b"Did.\nLocal capture before publication.\n")
    (source / "note.txt").write_bytes(b"publication note\n")
    reserved = rc.reserve(
        str(book),
        "pub-demo",
        "demo",
        "0508.return-capture",
        "05.01.md",
        "05.01",
        ["note.txt"],
        "Grok Builder 2",
        "Codex Prime",
        "Director 2026-10-27",
    )
    if reserved.code != 0:
        raise SystemExit(reserved.text)
    captured = rc.capture(
        str(book),
        "pub-demo",
        str(return_file),
        str(source),
        ["note.txt|note.txt"],
    )
    if captured.code != 0:
        raise SystemExit(captured.text)
    verified = rc.verify(str(book), "0101.demo")
    if verified.code != 0:
        raise SystemExit(verified.text)
    member = book / "0101.demo"
    sealed_before = {path.relative_to(member).as_posix(): path.read_bytes() for path in member_files(member)}
    receipt_before = sealed_before["receipt.json"]
    repo = parent / "publication-repo"
    repo.mkdir()
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "return-capture demo"
    env["GIT_AUTHOR_EMAIL"] = "return-capture@example.invalid"
    env["GIT_COMMITTER_NAME"] = "return-capture demo"
    env["GIT_COMMITTER_EMAIL"] = "return-capture@example.invalid"
    run(["git", "init"], repo, env)
    run(["git", "config", "user.email", "return-capture@example.invalid"], repo, env)
    run(["git", "config", "user.name", "return-capture demo"], repo, env)
    run(["git", "config", "core.autocrlf", "false"], repo, env)
    (repo / ".gitattributes").write_bytes(b"* -text\n")
    copy_bytes(member, repo / "0101.demo")
    run(["git", "add", "--", ".gitattributes", "0101.demo"], repo, env)
    run(["git", "commit", "-m", "publish sealed return copy"], repo, env)
    commit = run(["git", "rev-parse", "HEAD"], repo, env).stdout.decode().strip()
    blobs = []
    for rel, data in sorted(sealed_before.items()):
        spec = f"HEAD:0101.demo/{rel}"
        object_id = run(["git", "rev-parse", spec], repo, env).stdout.decode().strip()
        stored = run(["git", "cat-file", "blob", object_id], repo, env).stdout
        blobs.append(
            {
                "path": rel,
                "sha256": sha256_bytes(data),
                "git_object": object_id,
                "match": stored == data,
            }
        )
        if stored != data:
            raise SystemExit(f"published blob differs: {rel}")
    receipt_after = (member / "receipt.json").read_bytes()
    if receipt_after != receipt_before:
        raise SystemExit("sealed receipt changed during publication")
    published_verify = subprocess.run(
        [sys.executable, "-B", str(Path(rc.__file__)), "verify", "--book", str(repo), "--member", "0101.demo"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if published_verify.returncode != 0:
        raise SystemExit(published_verify.stdout + published_verify.stderr)
    log.append(f"publication commit {commit}")
    log.append("sealed receipt unchanged")
    log.append(published_verify.stdout.strip())
    return {
        "schema": "return-capture-publication/1",
        "member": "0101.demo",
        "commit": commit,
        "repository": str(repo),
        "sealed_book": str(book),
        "sealed_receipt_sha256": sha256_bytes(receipt_before),
        "published_receipt_sha256": sha256_bytes(receipt_after),
        "receipt_unchanged": True,
        "blobs": blobs,
        "pushed": False,
        "approved": False,
        "accepted": False,
        "published": True,
    }


def capture_retrospective(parent: Path, snapshots: Path, log: list[str]) -> dict:
    book = parent / "retrospective-book"
    source = parent / "retrospective-source"
    book.mkdir()
    source.mkdir()
    if not outside_git(book):
        raise SystemExit("retrospective book is inside Git")
    first = require_snapshot(snapshots, "0007.blob")
    second = require_snapshot(snapshots, "0008.blob")
    review = require_snapshot(snapshots, "0009.blob")
    first_return = parent / "0504-05.06.md"
    second_return = parent / "0507-05.01.md"
    first_return.write_bytes(first)
    second_return.write_bytes(second)
    (source / "review.md").write_bytes(review)
    subjects = [
        {
            "submission": "0504-05-06-pinned",
            "name": "app-entry-0506",
            "origin_book": "0504.app-entry",
            "origin_page": "05.06.md",
            "origin_batch": "05.06",
            "expected": [],
            "return_file": first_return,
            "artifacts": [],
            "snapshot": "snapshots/0007.blob",
            "proposed_member": "0101",
            "review_bytes": "the whole batch file contains the return and the Prime review",
            "payloads": [],
            "gaps": ["no separate pristine return; the whole pinned batch file is the submission"],
        },
        {
            "submission": "0507-05-01-pinned",
            "name": "prime-support-0501",
            "origin_book": "0507.prime-support",
            "origin_page": "05.01.md",
            "origin_batch": "05.01",
            "expected": ["prime-review05.01/review.md"],
            "return_file": second_return,
            "artifacts": ["review.md|prime-review05.01/review.md"],
            "snapshot": "snapshots/0008.blob",
            "proposed_member": "0102",
            "review_bytes": "the whole batch file contains the return and the Prime review; the payload is the separate review.md snapshot and is not the submission body",
            "payloads": [
                {
                    "snapshot": "snapshots/0009.blob",
                    "logical": "prime-review05.01/review.md",
                    "sha256": SNAPSHOTS["0009.blob"][0],
                    "role": "prime-review bytes, not the submission body",
                }
            ],
            "gaps": ["no separate pristine return; the whole pinned batch file is the submission"],
        },
    ]
    demonstrated = []
    for subject in subjects:
        reserved = rc.reserve(
            str(book),
            subject["submission"],
            subject["name"],
            subject["origin_book"],
            subject["origin_page"],
            subject["origin_batch"],
            subject["expected"],
            "historical snapshot",
            "Codex Prime",
            "pinned commit " + PIN,
        )
        if reserved.code != 0:
            raise SystemExit(reserved.text)
        captured = rc.capture(
            str(book),
            subject["submission"],
            str(subject["return_file"]),
            str(source),
            subject["artifacts"],
            retrospective=True,
            source_commit=PIN,
            return_includes_prime_review=True,
        )
        if captured.code != 0:
            raise SystemExit(captured.text)
        folder = f"{subject['proposed_member']}.{subject['name']}"
        verified = subprocess.run(
            [sys.executable, "-B", str(Path(rc.__file__)), "verify", "--book", str(book), "--member", folder],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if verified.returncode != 0:
            raise SystemExit(verified.stdout + verified.stderr)
        member = book / folder
        manifest = json.loads((member / "manifest.json").read_text(encoding="utf-8"))
        if manifest["captured_at"].startswith("2026-10-2") is False and len(manifest["captured_at"]) < 20:
            raise SystemExit("captured_at is missing")
        if manifest["source_commit"] != PIN or manifest["retrospective"] is not True:
            raise SystemExit("retrospective flags were not recorded")
        if (member / "return.md").read_bytes() != subject["return_file"].read_bytes():
            raise SystemExit("return bytes differ from the snapshot")
        demonstrated.append(
            {
                "proposed_real_member": subject["proposed_member"],
                "proposed_real_name": subject["name"],
                "disposable_member": folder,
                "submission_id": subject["submission"],
                "origin": {
                    "book": subject["origin_book"],
                    "page": subject["origin_page"],
                    "batch": subject["origin_batch"],
                },
                "snapshot": subject["snapshot"],
                "snapshot_sha256": sha256_bytes(subject["return_file"].read_bytes()),
                "return_includes_prime_review": True,
                "review_bytes": subject["review_bytes"],
                "payloads": subject["payloads"],
                "gaps": subject["gaps"],
                "retrospective": True,
                "source_commit": PIN,
                "captured_at": manifest["captured_at"],
                "captured_at_policy": "now, not a historical file time",
                "receipt_sha256": sha256_bytes((member / "receipt.json").read_bytes()),
                "real_book_allocated": False,
            }
        )
        log.append(f"retrospective {folder} captured_at {manifest['captured_at']}")
        log.append(verified.stdout.strip())
    return {
        "schema": "return-capture-backfill/1",
        "source_commit": PIN,
        "real_members_allocated": False,
        "acceptance_inferred": False,
        "proposed": demonstrated,
        "remaining": "Remaining published returns are captured later from an explicitly reviewed list.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="demo.py")
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--snapshots", required=True)
    args = parser.parse_args(argv)
    evidence = Path(args.evidence)
    evidence.mkdir(parents=True, exist_ok=True)
    parent = Path(tempfile.mkdtemp(prefix="rc-demo-"))
    log: list[str] = []
    try:
        if not outside_git(parent):
            raise SystemExit("demo parent is inside Git")
        publication = capture_publication(parent, log)
        backfill = capture_retrospective(parent, Path(args.snapshots), log)
        write_json(evidence / "publication.json", publication)
        write_json(evidence / "backfill.json", backfill)
        write_json(
            evidence / "retrospective.json",
            {
                "schema": "return-capture-retrospective/1",
                "source_commit": PIN,
                "snapshots_are_not_original_time_drops": True,
                "subjects": backfill["proposed"],
            },
        )
    finally:
        shutil.rmtree(parent, ignore_errors=True)
    text = "\n".join(log) + "\n"
    (evidence / "demo.txt").write_bytes(text.encode("utf-8"))
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
