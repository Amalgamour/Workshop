#!/usr/bin/env python3
"""Rehearse staged migration on a disposable copy of the audited captures.

The live work book is read in order to make the copy. It is not modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import return_lines as rl

AUDIT = os.path.join(
    rl.repo_root(), "00.kernel", "00.00.10.work",
    "0417.return-placement", "evidence", "audit-corrected.json",
)
KNOWN_OCCUPANTS = {
    "0102.prime-support-0501",
    "0104.app-entry-0508",
    "0105.prime-clerk-0504",
    "0106.entry-regression-0509",
    "0107.clerk-types-0505",
    "0108.backfill-plan-0503",
    "0109.clerk-seam-0510",
    "0110.return-inspection-0504",
    "0111.prime-boot-design-0506",
    "0112.seam-io-0511",
    "0113.prime-boot-0507",
    "0114.inspection-range-0505",
    "0115.observer-pilot-0501",
    "0116.backfill-run-0506",
    "0117.bridge-parent-0512",
    "0118.workflow-start-0501",
    "0119.app-entry-0503",
    "0120.backfill-run-0507",
}


def say(text: str) -> None:
    sys.stderr.write(text + "\n")
    sys.stderr.flush()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def copy_tree(src: str, dest: str) -> int:
    count = 0
    for rel in rl.walk_files(src):
        data = rl.read_exact(os.path.join(src, *rel.split("/")))
        rl.write_new(os.path.join(dest, *rel.split("/")), data)
        count += 1
    return count


def fingerprint(live: str, names: list[str], tails: list[str]) -> str:
    rows = []
    for name in names:
        root = os.path.join(live, name)
        for rel in rl.walk_files(root):
            data = rl.read_exact(os.path.join(root, *rel.split("/")))
            rows.append(f"{name}/{rel} {sha(data)} {len(data)}")
    for rel in tails:
        data = rl.read_exact(os.path.join(live, *rel.split("/")))
        rows.append(f"tail {rel} {sha(data)} {len(data)}")
    return sha(("\n".join(rows) + "\n").encode("utf-8"))


def member_names(live: str) -> list[str]:
    found = []
    with os.scandir(live) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False) and entry.name[:2] == "01" and len(entry.name) > 4 and entry.name[4] == ".":
                found.append(entry.name)
    return sorted(found)


def write_json(path: str, body: object) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(rl.dump(body))


def occupants_of(book: str, records: list[dict]) -> list[str]:
    found = []
    for record in records:
        route = rl.route_for(record["origin"]["book"], record["origin"]["page"], record["origin"]["batch"])
        found.extend(rl.occupants(book, route["target_number"], route["target_page"]))
    return sorted(set(found))


def cleanup(root: str) -> None:
    for dirpath, dirnames, filenames in os.walk(root, topdown=False, followlinks=False):
        for name in filenames:
            os.remove(os.path.join(dirpath, name))
        for name in dirnames:
            os.rmdir(os.path.join(dirpath, name))
    os.rmdir(root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args(argv)
    live = rl.live_book_path()
    work = os.path.abspath(args.work_root)
    if rl.within(live, work) or rl.norm(work) == rl.norm(live):
        say("refusing to rehearse inside the live work book")
        return 2
    audit, audit_sha, audit_bytes = rl.load_audit(AUDIT)
    records = sorted(
        (record for record in audit["records"] if isinstance(record, dict)),
        key=lambda record: rl.member_key(str(record.get("old_member"))),
    )
    names = [record["old_member"] for record in records]
    tails = [record["target_return"] for record in records if record.get("route") == "page-local-colab"]
    say(f"fingerprint {len(names)} members")
    before = fingerprint(live, names, tails)
    before_dirs = member_names(live)
    book = os.path.join(work, "book")
    backup = os.path.join(work, "backup")
    if os.path.exists(work):
        say(f"work root already exists: {work}")
        return 2
    os.makedirs(book)
    say("copy members")
    copied = 0
    for name in names:
        copied += copy_tree(os.path.join(live, name), os.path.join(book, name))
    for rel in tails:
        data = rl.read_exact(os.path.join(live, *rel.split("/")))
        rl.write_new(os.path.join(book, *rel.split("/")), data)
        copied += 1
    say(f"copied {copied} files")
    opened = rl.init_run(book, "00.00.10.work")
    write_json(os.path.join(args.evidence, "rehearsal-init.json"), opened)
    if opened["exit"] != 0:
        return opened["exit"]
    say("stage interrupt")
    interrupted = rl.stage_run(book, backup, AUDIT, interrupt_after=1)
    write_json(os.path.join(args.evidence, "rehearsal-stage-interrupt.json"), interrupted)
    if interrupted["exit"] != 3:
        say("interrupt did not stop the stage")
        return interrupted["exit"] or 2
    say("stage resume")
    resumed = rl.stage_run(book, backup, AUDIT, resume=True)
    write_json(os.path.join(args.evidence, "rehearsal-stage-resume.json"), resumed)
    if resumed["exit"] != 0:
        say("stage resume failed")
        return resumed["exit"] or 2
    discovered = occupants_of(book, records)
    if set(discovered) != KNOWN_OCCUPANTS:
        say("occupants differ: " + " ".join(discovered))
        write_json(os.path.join(args.evidence, "rehearsal-occupants.json"), {"discovered": discovered, "known": sorted(KNOWN_OCCUPANTS)})
        return 2
    for name in discovered:
        if not os.path.isdir(os.path.join(book, name)):
            say(f"occupant missing before adopt: {name}")
            return 2
    say("adopt")
    adopted = rl.adopt_run(book, backup, AUDIT)
    write_json(os.path.join(args.evidence, "rehearsal-adopt.json"), adopted)
    if adopted["exit"] != 0:
        say("adopt failed")
        return adopted["exit"] or 2
    problems = []
    for record in records:
        origin = record["origin"]
        route = rl.route_for(origin["book"], origin["page"], origin["batch"])
        by_member = rl.lookup_run(book, member=record["old_member"])
        by_origin = rl.lookup_run(book, page=origin["page"], batch=origin["batch"])
        backup_return = os.path.join(backup, "sources", record["old_member"], "return.md")
        tail = os.path.join(book, *route["return_path"].split("/"))
        if not os.path.lexists(backup_return):
            if by_member["descriptor"]["state"] != "incomplete" or os.path.lexists(tail):
                problems.append(record["old_member"])
            continue
        original = rl.read_exact(backup_return)
        if not os.path.lexists(tail) or rl.read_exact(tail) != original:
            problems.append(record["old_member"] + " tail")
        if by_member["exit"] != 0 or by_origin["exit"] != 0:
            problems.append(record["old_member"] + " lookup")
        elif by_member["descriptor"]["return_sha256"] != sha(original) or by_origin["descriptor"]["return_sha256"] != sha(original):
            problems.append(record["old_member"] + " hash")
        custody_res = os.path.join(book, route["custody_dir"], "reservation.json")
        source_res = os.path.join(backup, "sources", record["old_member"], "reservation.json")
        if rl.read_exact(custody_res) != rl.read_exact(source_res):
            problems.append(record["old_member"] + " reservation")
    write_json(os.path.join(args.evidence, "lookup-0101.json"), rl.lookup_run(book, member="0101.app-entry-0506"))
    write_json(os.path.join(args.evidence, "lookup-0101-origin.json"), rl.lookup_run(book, page="0504.app-entry", batch="05.06"))
    write_json(os.path.join(args.evidence, "lookup-0154.json"), rl.lookup_run(book, member="0154.colab-support-first-0501"))
    write_json(os.path.join(args.evidence, "lookup-0165.json"), rl.lookup_run(book, member="0165.bench-method-colab-0501"))
    if problems:
        say("lookup or byte problems: " + ", ".join(problems[:20]))
        write_json(os.path.join(args.evidence, "rehearsal-problems.json"), {"problems": problems})
        return 2
    retired = sorted(os.listdir(os.path.join(backup, "retired")))
    if set(retired) != KNOWN_OCCUPANTS:
        say("retired set differs")
        return 2
    say("rollback")
    rolled = rl.rollback_adopt_run(book, backup)
    write_json(os.path.join(args.evidence, "rehearsal-rollback.json"), rolled)
    if rolled["exit"] != 0:
        return rolled["exit"] or 2
    for name in KNOWN_OCCUPANTS:
        if not os.path.isdir(os.path.join(book, name)):
            say(f"occupant was not restored: {name}")
            return 2
    say("adopt again")
    again = rl.adopt_run(book, backup, AUDIT)
    write_json(os.path.join(args.evidence, "rehearsal-adopt-again.json"), again)
    if again["exit"] != 0:
        return again["exit"] or 2
    note = os.path.join(work, "note.md")
    ret = os.path.join(work, "return.md")
    with open(note, "wb") as handle:
        handle.write(b"SYNTHETIC NEW WORK\n")
    with open(ret, "wb") as handle:
        handle.write(b"SYNTHETIC RETURN\n")
    request = {
        "artifact": "note.md",
        "batch": "05.21",
        "page": "0504.app-entry",
        "return": "SYNTHETIC RETURN\n",
        "submission": "grok-1-0521-0503-synthetic",
    }
    write_json(os.path.join(args.evidence, "synthetic-request.json"), request)
    reserved = rl.reserve_run(
        book, "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic",
        ["note.md"], "grok-1", "codex-prime", "prepared", None,
    )
    captured = rl.capture_run(
        book, "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic", ret, [("note.md", note)],
    )
    write_json(os.path.join(args.evidence, "synthetic-result.json"), captured)
    if captured["exit"] != 0 or captured.get("descriptor") is None:
        say("synthetic capture failed")
        return captured["exit"] or 2
    write_json(os.path.join(args.evidence, "synthetic-descriptor.json"), captured["descriptor"])
    historical = rl.lookup_run(book, page="0504.app-entry", batch="05.06")
    if historical["exit"] != 0:
        say("historical pass missing after synthetic capture")
        return 2
    pages = [name for name in os.listdir(book) if name.startswith("0104.")]
    if pages != ["0104.app-entry"]:
        say("synthetic pass took another page: " + " ".join(pages))
        return 2
    after = fingerprint(live, names, tails)
    after_dirs = member_names(live)
    report = {
        "adopt_retired_count": adopted["detail"]["retired_count"],
        "after_fingerprint": after,
        "audit_bytes": audit_bytes,
        "audit_sha256": audit_sha,
        "before_fingerprint": before,
        "copied_files": copied,
        "fingerprint_unchanged": before == after,
        "incomplete_member": "0154.colab-support-first-0501",
        "live_dirs_unchanged": before_dirs == after_dirs,
        "live_member_count": len(before_dirs),
        "occupants": sorted(KNOWN_OCCUPANTS),
        "problems": problems,
        "records": len(records),
        "reserved_exit": reserved["exit"],
        "schema": "return-line-rehearsal/1",
        "source_count": resumed["detail"]["source_count"],
        "synthetic_state": captured["descriptor"]["state"],
        "tails": tails,
    }
    write_json(os.path.join(args.evidence, "rehearsal-report.json"), report)
    if not report["fingerprint_unchanged"] or not report["live_dirs_unchanged"] or report["records"] != 83:
        say("live book changed or record count was not 83")
        return 2
    if os.path.lexists(os.path.join(live, "return-line-layout.json")):
        say("live layout was written")
        return 2
    say("cleanup disposable copy")
    cleanup(work)
    say("rehearsal ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
