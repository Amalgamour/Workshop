#!/usr/bin/env python3
"""0709 pass01: READ-ONLY inventory of the live 01NN capture set (NONPRODUCTION).

Origins come from each capture's stored reservation.json, never from the slug or
number. Routes come from the pinned return_lines.route_for (pure); occupants from
return_lines.occupants (a directory read). Nothing in the live book is written.
usage: inventory.py --out DIR   (DIR must not exist)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CHECKOUT = Path(r"D:\Git\lib-build")
LIVE = CHECKOUT / "00.kernel" / "00.00.10.work"
AUDIT = LIVE / "0417.return-placement" / "evidence" / "audit-corrected.json"
RL = CHECKOUT / "labs" / "return-lines-pass01"
RL_PIN = ("863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a", 100897)
MEMBER = re.compile(r"^01(0[1-9]|[1-9][0-9])\..+$")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_rl():
    data = (RL / "return_lines.py").read_bytes()
    if (sha(data), len(data)) != RL_PIN:
        raise SystemExit("return_lines.py differs from its pin")
    sys.path.insert(0, str(RL))
    import return_lines as rl  # noqa: E402
    return rl


def files_of(root: Path) -> dict[str, dict]:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            b = p.read_bytes()
            out[p.relative_to(root).as_posix()] = {"sha256": sha(b), "bytes": len(b)}
    return out


def audit_hashes(verify_output: str) -> dict[str, str]:
    """verify_output lines: 'reservation H', 'manifest H', 'receipt H', 'payload NAME H'."""
    found = {}
    for line in (verify_output or "").splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0] in ("reservation", "manifest", "receipt"):
            found[f"{parts[0]}.json"] = parts[1]
        elif len(parts) == 3 and parts[0] == "payload":
            found[f"payload/{parts[1]}"] = parts[2]
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    rl = load_rl()
    audit_raw = AUDIT.read_bytes()
    audit = json.loads(audit_raw)
    by_member = {r["old_member"]: r for r in audit["records"]}
    live_names = sorted(e.name for e in os.scandir(LIVE) if e.is_dir(follow_symlinks=False) and MEMBER.match(e.name))
    rows, problems = [], []
    for name in sorted(live_names, key=rl.member_key):
        d = LIVE / name
        files = files_of(d)
        res_raw = (d / "reservation.json").read_bytes() if (d / "reservation.json").is_file() else None
        res = json.loads(res_raw) if res_raw else None
        origin = res.get("origin") if isinstance(res, dict) else None
        rec = by_member.get(name)
        row = {"member": name, "in_audit": rec is not None, "file_count": len(files),
               "reservation_sha256": sha(res_raw) if res_raw else None,
               "origin_from_reservation": origin, "submission": res.get("submission_id") if isinstance(res, dict) else None,
               "has_receipt": (d / "receipt.json").is_file(), "has_return": (d / "return.md").is_file()}
        if rec:
            row["audit_origin"] = rec["origin"]
            row["origin_matches_audit"] = origin == rec["origin"]
            want = audit_hashes(rec.get("verify_output"))
            changed = sorted(k for k, h in want.items() if files.get(k, {}).get("sha256") != h)
            row["audit_hash_entries"] = len(want)
            row["files_changed_since_audit"] = changed
            row["audit_has_receipt"] = rec.get("has_receipt")
            if changed or not row["origin_matches_audit"]:
                problems.append(name)
        if isinstance(origin, dict) and all(isinstance(origin.get(k), str) for k in ("book", "page", "batch")):
            try:
                route = rl.route_for(origin["book"], origin["page"], origin["batch"])
                row["route"] = route.get("route")
                row["intended_target_page"] = route.get("target_page")
                row["intended_return_path"] = route.get("return_path")
                row["intended_custody_dir"] = route.get("custody_dir")
                row["occupants_of_intended_number"] = rl.occupants(str(LIVE), route["target_number"], route["target_page"]) \
                    if route.get("route") == "matched-workflow-return-line" else []
                tail = LIVE / Path(*route["return_path"].split("/"))
                row["intended_tail_exists"] = tail.is_file()
                row["intended_tail_equals_return"] = tail.is_file() and (d / "return.md").is_file() and tail.read_bytes() == (d / "return.md").read_bytes()
            except rl.LineError as exc:
                row["route_error"] = exc.correction if hasattr(exc, "correction") else str(exc)
        row["state"] = "complete" if row["has_receipt"] and row["has_return"] else ("reserved-only" if res_raw and not row["has_receipt"] else "incomplete")
        row["backup_destination"] = f"<backup>/sources/{name}"
        row["lookup"] = {"by_member": name, "by_origin": origin}
        rows.append(row)
    not_live = sorted(set(by_member) - set(live_names))
    occ = sorted({o for r in rows for o in r.get("occupants_of_intended_number", [])})
    body = {
        "schema": "0709-return-inventory/1", "live_book": str(LIVE), "audit_sha256": sha(audit_raw), "audit_bytes": len(audit_raw),
        "live_member_dirs": len(live_names), "door_dirs": [n for n in live_names if n.startswith("0100.")],
        "captures": len([r for r in rows if not r["member"].startswith("0100.")]),
        "in_audit": sum(r["in_audit"] for r in rows), "not_in_audit": [r["member"] for r in rows if not r["in_audit"]],
        "audit_records_not_live": not_live, "records_with_changes_or_origin_mismatch": problems,
        "routes": {k: sum(1 for r in rows if r.get("route") == k) for k in ("matched-workflow-return-line", "page-local-colab")},
        "states": {k: sum(1 for r in rows if r["state"] == k and not r["member"].startswith("0100.")) for k in ("complete", "reserved-only", "incomplete")},
        "occupancy_collisions": occ, "occupancy_collision_count": len(occ),
        "rows": rows,
    }
    (out / "inventory.json").write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["| Old capture | Origin (reservation) | Intended return | State | Collides with | Tail equal |", "|---|---|---|---|---|---|"]
    for r in rows:
        if r["member"].startswith("0100."):
            continue
        o = r.get("origin_from_reservation") or {}
        lines.append(f"| {r['member']} | {o.get('page')}/{o.get('batch')} | {r.get('intended_return_path')} | {r['state']} | "
                     f"{', '.join(r.get('occupants_of_intended_number', [])) or '-'} | {r.get('intended_tail_equals_return')} |")
    (out / "MAP.md").write_text("# Current routing map (read-only, live)\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: body[k] for k in ("live_member_dirs", "door_dirs", "captures", "in_audit", "not_in_audit", "audit_records_not_live",
                                           "records_with_changes_or_origin_mismatch", "routes", "states", "occupancy_collision_count")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
