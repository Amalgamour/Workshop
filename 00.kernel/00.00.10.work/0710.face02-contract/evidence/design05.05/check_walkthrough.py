#!/usr/bin/env python3
"""0710/05.05 NONPRODUCTION check of the walkthrough and map against the frozen sources.

Proves only: quoted candidate/seat excerpts and Director phrases occur verbatim in their
sources; #NN items are contiguous with a label and an UNANSWERED answer; every seat section
is named in the preservation map; CHANGE-SET identities equal measured bytes; candidates
unchanged. It does not prove semantic preservation.
usage: check_walkthrough.py --out FILE(new)
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PAGE = HERE.parents[1]
ROOT = PAGE.parents[2]
S = PAGE / "evidence/pack05.05/sources/00.kernel"


def text(p):
    return p.read_bytes().decode("utf-8").replace("\r\n", "\n")


def flat(t):
    return re.sub(r"\s+", " ", t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out = Path(ap.parse_args().out)
    if out.exists():
        sys.exit("refused: exists")
    c1 = text(PAGE / "evidence/design05.02/candidates/0001.law.01.005.candidate.md")
    c2 = text(PAGE / "evidence/design05.03/candidates/0002.schema.01.004.candidate.md")
    s1 = text(S / "00.00.01.law/0001.law/01.md")
    s2 = text(S / "00.00.01.law/0002.schema/01.md")
    dec = text(PAGE / "06.02.decisions.md") + "\n" + text(PAGE / "06.03.decisions.md")
    w = text(HERE / "DIRECTOR-WALKTHROUGH.md")
    problems, checks = [], []
    # excerpts: '> ' lines after a 'Proposed (0001' or 'Proposed (0002' marker
    target = None
    for line in w.split("\n"):
        if line.startswith("**Proposed (0001"):
            target = ("0001", c1)
        elif line.startswith("**Proposed (0002"):
            target = ("0002", c2)
        elif line.startswith("> ") and target:
            q = line[2:].strip()
            ok = q in target[1]
            checks.append({"excerpt": q[:60], "candidate": target[0], "verbatim": ok})
            if not ok:
                problems.append(f"excerpt not verbatim in {target[0]}: {q[:80]}")
        elif line.startswith("## #"):
            target = None
    # current-seat quotes
    for m in re.finditer(r'\*\*Current \((0001|0002) seat[^)]*\):\*\* (.*)', w):
        seat = s1 if m.group(1) == "0001" else s2
        for q in re.findall(r'"([^"]+)"', m.group(2)):
            # an ellipsis marks an elision: each piece must be verbatim on its own (fix after check01)
            for part in [p.strip() for p in q.split("…") if p.strip()]:
                ok = part in seat
                checks.append({"seat_quote": part[:60], "seat": m.group(1), "verbatim": ok})
                if not ok:
                    problems.append(f"seat quote not verbatim in {m.group(1)}: {part[:80]}")
    # Director phrases quoted with a decision reference
    for q in re.findall(r'\("([^"]+)"\)', w):
        ok = flat(q) in flat(dec)
        checks.append({"director_phrase": q[:60], "verbatim_whitespace_normalized": ok})
        if not ok:
            problems.append(f"Director phrase not found: {q[:80]}")
    # items
    items = re.findall(r"^## #(\d\d) .*?\[(S|O|T|P)\]", w, flags=re.M)
    nums = [int(n) for n, _ in items]
    if nums != list(range(1, len(nums) + 1)) or len(nums) > 8:
        problems.append(f"#NN not contiguous or >8: {nums}")
    blocks = re.split(r"^## #\d\d ", w, flags=re.M)[1:]
    for i, b in enumerate(blocks, 1):
        if "**Director answer:** UNANSWERED" not in b:
            problems.append(f"#{i:02d} lacks UNANSWERED")
    # map coverage of seat sections
    pm = text(HERE / "PRESERVATION-MAP.md")
    for name, seat in (("0001", s1), ("0002", s2)):
        for h in re.findall(r"^## (.+)$", seat, flags=re.M):
            if not re.search(rf"\| {re.escape(h)}[ :|]", pm):
                problems.append(f"map lacks {name} section {h}")
    # identities
    cs = json.loads((HERE / "CHANGE-SET.json").read_text(encoding="utf-8"))
    for mem in cs["joint_release_members"]:
        for k in ("seat", "candidate"):
            p = ROOT / mem[k]["path"]
            if hashlib.sha256(p.read_bytes()).hexdigest() != mem[k]["sha256"]:
                problems.append(f"identity drift {mem[k]['path']}")
    body = {"schema": "0710-05.05-walkthrough-check/1", "proves": "verbatim quotes, item shape, map section coverage, identities; NOT semantic preservation",
            "items": nums, "checks": checks, "problems": problems}
    out.write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("items", nums, "checks", len(checks), "problems", len(problems))
    for p in problems:
        print("PROBLEM", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
