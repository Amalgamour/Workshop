"""Fill batch 05.02's PENDING return fields on 0503.worker-bridge/05.02.md, keeping CRLF and every instruction line.

  python -B page_return_0502.py <05.02.md> <return-text-folder>

The folder holds r01.txt..r04.txt (each replaces 'result: PENDING' inside section '## #0N') and return.txt
(replaces 'Execution: IN PROGRESS' and the three PENDING lines that follow it under '## Return — Claude').
The Prime's review section is not touched. Refuses unless each target occurs exactly once.
"""
import sys
from pathlib import Path

page, folder = Path(sys.argv[1]), Path(sys.argv[2])
if page.name != "05.02.md" or page.parent.name != "0503.worker-bridge":
    sys.exit("stop: not batch 05.02")
raw = page.read_bytes().decode("utf-8")
if "\r\n" not in raw:
    sys.exit("stop: expected CRLF")
t = raw.replace("\r\n", "\n")


def text(name):
    return (folder / name).read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n")


for n in range(1, 5):
    i = t.index(f"\n## #0{n} ")
    j = t.find("\n## ", i + 1)
    sec = t[i:j]
    if sec.count("result: PENDING") != 1:
        sys.exit(f"stop: section #0{n} has {sec.count('result: PENDING')} pending results")
    t = t[:i] + sec.replace("result: PENDING", text(f"r0{n}.txt")) + t[j:]
old = "Execution: IN PROGRESS\nCorrections and original-probe outcomes: PENDING\nTests/evidence/hashes: PENDING\nRemaining limitations: PENDING"
if t.count(old) != 1:
    sys.exit("stop: return block not found exactly once")
t = t.replace(old, text("return.txt"))
page.write_bytes(t.replace("\n", "\r\n").encode("utf-8"))
print("return written")
