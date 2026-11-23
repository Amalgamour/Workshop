"""Split src/cmd.rs into src/cmd/mod.rs plus one file per command group.

Lab tool for page 90.50.10.0426 (split-commands). Claude, 2026-11-23.
It is a MOVE: every top-level item keeps its text. The only edits are:
  - a private `fn` moved into a group file becomes `pub(crate) fn`, so the
    other groups and mod.rs can still call it (visibility only, no logic);
  - each group file starts with `use super::*;`;
  - mod.rs declares the groups and re-exports them, so `cmd::ret` and the
    other paths used by lib.rs, render.rs, status.rs and board.rs still work.

Run from the kit root:  python -I labs/0426-plan/tools/split_cmd.py
Re-run it on any start commit (for example after 0423 lands). An item the
map does not name stays in mod.rs and is listed, so nothing is lost.
"""
import re
import sys
from pathlib import Path

GROUPS = {
    "start": ["halt", "resume", "init_page", "set_prime", "grant"],
    "plan": ["face_write", "pin", "pin05", "draft", "pin_text", "overlap_ok_flag",
             "refuse_overlap", "pack", "withdraw"],
    "build": ["claim", "ret_change_paths", "parse_return", "ret"],
    "sync": ["merge_into_shared", "push_log", "publish_pack", "intake"],
    "check": ["refuse_passed", "check_report", "check"],
    "close": ["signoff", "close", "elevate", "answer"],
    # 0423 adds these; they are placed here once they exist at the start commit.
    "lock": ["lockout", "try_out", "release", "release_override"],
}
ORDER = ["start", "plan", "build", "sync", "check", "close", "lock"]

ITEM = re.compile(r"^(pub(\(crate\))? )?(fn|struct|enum|const|static|impl|mod|type|use)\b")
FN_NAME = re.compile(r"^(?:pub(?:\(crate\))? )?fn (\w+)")


def items(lines):
    """Yield (start, end, first_line_index) for each top-level item, with its
    leading doc comments and attributes."""
    starts = [i for i, l in enumerate(lines) if ITEM.match(l) or l.startswith("#[cfg(test)]")]
    spans = []
    for k, i in enumerate(starts):
        s = i
        while s > 0 and (lines[s - 1].startswith("///") or lines[s - 1].startswith("#[")
                         or lines[s - 1].startswith("//")):
            s -= 1
        spans.append([s, i])
    out = []
    for k, (s, i) in enumerate(spans):
        e = spans[k + 1][0] if k + 1 < len(spans) else len(lines)
        out.append((s, e, i))
    return out


def main():
    root = Path(".")
    src = root / "src" / "cmd.rs"
    lines = src.read_text(encoding="utf-8").split("\n")
    where = {name: g for g, names in GROUPS.items() for name in names}
    keep, moved = [], {g: [] for g in ORDER}
    placed = []
    spans = items(lines)
    # Text before the first item (file docs) stays in mod.rs.
    head_end = spans[0][0] if spans else len(lines)
    keep.extend(lines[:head_end])
    for s, e, i in spans:
        block = lines[s:e]
        m = FN_NAME.match(lines[i])
        g = where.get(m.group(1)) if m else None
        if g is None:
            keep.extend(block)
            continue
        j = i - s
        if block[j].startswith("fn "):
            block[j] = "pub(crate) " + block[j]
        moved[g].extend(block)
        placed.append((m.group(1), i + 1, g))

    used = [g for g in ORDER if moved[g]]
    decl = []
    for g in used:
        decl.append(f"mod {g};")
    for g in used:
        decl.append(f"pub use {g}::*;")
    # Put the declarations after the use lines at the top of mod.rs.
    last_use = max((k for k, l in enumerate(keep) if l.startswith("use ")), default=-1)
    keep = keep[: last_use + 1] + [""] + decl + keep[last_use + 1:]

    out = root / "src" / "cmd"
    out.mkdir(exist_ok=True)
    (out / "mod.rs").write_text("\n".join(keep), encoding="utf-8")
    for g in used:
        body = ["//! " + g + " commands, moved from src/cmd.rs by page 90.50.10.0426 (no behaviour change).",
                "use super::*;", ""] + moved[g]
        text = "\n".join(body).rstrip("\n") + "\n"
        (out / f"{g}.rs").write_text(text, encoding="utf-8")
    src.unlink()

    for name, line, g in placed:
        print(f"{name}\tsrc/cmd.rs:{line}\t-> src/cmd/{g}.rs")
    missing = sorted(n for n in where if n not in {p[0] for p in placed})
    if missing:
        print("not found at this commit (fine if 0423 has not landed):", ", ".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
