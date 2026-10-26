"""Pack B #04: every quoted reply on 0409.decisions appears verbatim in its named source file."""
import re, sys
from pathlib import Path
LB = Path(r"D:\Git\lib-build")
text = (LB / "00.kernel/00.00.10.work/0409.decisions/01.md").read_text(encoding="utf-8")
src, bad, n = None, [], 0
blocks = re.split(r"\n(?=### |- `#)", text)
for b in blocks:
    m = re.match(r"### `([^`]+)`", b)
    if m:
        src = (LB / m.group(1)).read_text(encoding="utf-8")
        continue
    if src is None or not b.startswith("- `#"):
        continue
    q = "\n".join(l[2:] if l.startswith("> ") else "" for l in b.split("\n") if l.startswith(">"))
    if q.strip():
        n += 1
        if q not in src:
            bad.append(b.split("\n")[0])
print(f"checked {n} quoted replies; not verbatim: {len(bad)}")
for x in bad:
    print("  " + x)
sys.exit(1 if bad else 0)
