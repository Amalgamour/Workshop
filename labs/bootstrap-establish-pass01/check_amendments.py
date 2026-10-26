"""Pack B #05: check each amendment draft against its imported source face.

For each amendment: the source line names the exact SHA-256 of `01.md`; every section the notes call
unchanged is byte-identical to the source's section; every changed section is listed in the notes.

  python -B check_amendments.py [--fix-source-hash]
"""
import hashlib, re, sys
from pathlib import Path

LAW = Path(r"D:\Git\lib-build\00.kernel\00.00.01.law")
CASES = {
    "0018.seqaddr/01.011.md": {"changed": {"Walk", "notes"}},
    "0050.band.structure/01.004.md": {"changed": {"Thing", "notes"}},
    "0057.bands/01.003.md": {"changed": {"This book", "Space", "notes"}},
}


def sections(text):
    """Split on '## ' and '### ' headings; repeated headings keep their order as name#n."""
    out, name, buf, seen = {}, "_head", [], {}
    for line in text.split("\n"):
        m = re.match(r"^(#{2,3}) (.+)$", line)
        if m:
            out[name] = "\n".join(buf).rstrip("\n")
            base = m.group(2)
            seen[base] = seen.get(base, 0) + 1
            name = base if seen[base] == 1 else f"{base}#{seen[base]}"
            buf = []
        else:
            buf.append(line)
    out[name] = "\n".join(buf).rstrip("\n")
    return out


def main(fix):
    bad = []
    for rel, spec in CASES.items():
        amend = LAW / rel
        src = amend.parent / "01.md"
        h = hashlib.sha256(src.read_bytes()).hexdigest()
        text = amend.read_text(encoding="utf-8")
        m = re.search(r"sha256 ([0-9a-f]+)", text.split("\n## ")[0])
        if not m or m.group(1) != h:
            if fix and m:
                text = text.replace(f"sha256 {m.group(1)}", f"sha256 {h}", 1)
                amend.write_bytes(text.encode("utf-8"))
                print(f"{rel}: source hash set to {h}")
            else:
                bad.append(f"{rel}: source line names {m.group(1) if m else None}, actual {h}")
        a, s = sections(text), sections(src.read_text(encoding="utf-8"))
        for name, body in s.items():
            if name in ("_head",) or name.split("#")[0] in spec["changed"]:
                continue
            if a.get(name) != body:
                bad.append(f"{rel}: section '{name}' is called unchanged but differs from the source")
        for name in spec["changed"]:
            if name != "notes" and f"| {name} |" not in text and f"| (new) {name} |" not in text and not re.search(rf"\| {re.escape(name)} \(", text):
                bad.append(f"{rel}: changed section '{name}' is not in the amendment notes")
        print(f"{rel}: checked {len(s) - 1} source sections")
    print("\n".join(bad) if bad else "PASS: every unchanged section is byte-identical and every change is noted")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main("--fix-source-hash" in sys.argv))
