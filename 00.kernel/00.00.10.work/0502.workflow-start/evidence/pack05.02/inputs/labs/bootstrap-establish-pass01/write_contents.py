"""Pack B #04: generate the work book's contents from the folders that actually exist (finding F03).

  python -B write_contents.py [--check]

Writes 00.kernel/00.00.10.work/0011.contents/01.001.md. --check regenerates in memory and compares.
Files inside 0501.bootstrap/pack and 0501.bootstrap/addendum-001 are counted, not listed one by one.
"""
import sys
from pathlib import Path

W = Path(r"D:\Git\lib-build\00.kernel\00.00.10.work")
OUT = W / "0011.contents" / "01.001.md"


def build():
    lines = ["# 01", "", "version: 001", "Authorization: draft — 2026-10-26", "who: claude-opus-5-5",
             "state: draft. Generated from the folders that exist, by labs/bootstrap-establish-pass01/write_contents.py (Pack B #04).",
             "Face: 01", "PPPP: 0011", "book: 00.00.10.work", "keyword: contents",
             "why: Every page of this book, exactly once, with its faces.", "", "## Pages", "", "| Page | Faces and files |", "|---|---|"]
    pages = sorted(p for p in W.iterdir() if p.is_dir())
    for p in pages:
        files = []
        for f in sorted(p.iterdir()):
            if f.is_dir():
                n = sum(1 for x in f.rglob("*") if x.is_file())
                files.append(f"`{f.name}/` ({n} files)")
            else:
                files.append(f"`{f.name}`")
        lines.append(f"| `{p.name}` | {', '.join(files)} |")
    loose = sorted(f.name for f in W.iterdir() if f.is_file())
    lines += ["", f"Book files: {', '.join('`' + x + '`' for x in loose)}.", "",
              "## Other books", "Syntax: `../00.00.00.syntax/00.001.md`. Law: `../00.00.01.law/00.001.md`. Each lists what it holds.", ""]
    return ("\n".join(lines)).encode("utf-8"), [p.name for p in pages]


def main():
    data, pages = build()
    if "--check" in sys.argv:
        ok = OUT.is_file() and OUT.read_bytes() == data
        print(("contents match the folders: " if ok else "contents DIFFER from the folders: ") + f"{len(pages)} pages")
        sys.exit(0 if ok else 2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    print(f"wrote {OUT}: {len(pages)} pages")


if __name__ == "__main__":
    main()
