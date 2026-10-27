"""Fill this batch's PENDING return fields on 0503.worker-bridge/05.01.md, keeping CRLF and every instruction line.

  python -B page_return.py <05.01.md> <return-text-folder>

The folder holds r01.txt..r04.txt (each replaces 'result: PENDING' inside section '## #0N') and
return.txt (replaces the five PENDING lines under '## Return — Claude' after 'Execution state:').
Refuses unless each target occurs exactly once.
"""
import sys
from pathlib import Path

page, folder = Path(sys.argv[1]), Path(sys.argv[2])
if page.name != "05.01.md" or page.parent.name != "0503.worker-bridge":
    sys.exit("stop: not the batch page")
t = page.read_bytes().decode("utf-8")
if "\r\n" not in t:
    sys.exit("stop: expected CRLF")
t = t.replace("\r\n", "\n")


def crlf_free(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n")


for n in range(1, 5):
    head = f"\n## #0{n} "
    i = t.index(head)
    j = t.find("\n## ", i + 1)
    sec = t[i:j]
    if sec.count("result: PENDING") != 1:
        sys.exit(f"stop: section #0{n} has {sec.count('result: PENDING')} pending results")
    t = t[:i] + sec.replace("result: PENDING", crlf_free(folder / f"r0{n}.txt")) + t[j:]
old = ("Execution state: IN PROGRESS\nConnection inventory and recommended next real exchange: PENDING\n"
       "Implemented and demonstrated: PENDING\nTests and retained failures: PENDING\n"
       "Artifacts, evidence and SHA-256 manifest: PENDING\nNot implemented/uncertain: PENDING")
if t.count(old) != 1:
    sys.exit("stop: return block not found exactly once")
t = t.replace(old, crlf_free(folder / "return.txt"))
page.write_bytes(t.replace("\n", "\r\n").encode("utf-8"))
print("return written")
