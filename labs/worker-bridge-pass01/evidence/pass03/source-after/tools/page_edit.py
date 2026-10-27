"""Replace one exact, unique block of text on the batch page, keeping its CRLF line endings.

  python -B page_edit.py <page> <old-file> <new-file>

Both blocks are given as LF text files; they are converted to the page's CRLF before matching.
Refuses unless the old block occurs exactly once. Used only for 0503.worker-bridge pages 05.01, 06.01, 05.02 and 06.02.
"""
import sys
from pathlib import Path

page, old, new = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
allowed = {"05.01.md", "06.01.md", "05.02.md", "06.02.md", "05.03.md", "06.03.md"}
if page.name not in allowed or page.parent.name != "0503.worker-bridge":
    sys.exit(f"stop: not an allowed page: {page}")
data = page.read_bytes()
o = old.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
n = new.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
if data.count(o) != 1:
    sys.exit(f"stop: the old block occurs {data.count(o)} times")
page.write_bytes(data.replace(o, n))
print(f"edited {page.name}")
