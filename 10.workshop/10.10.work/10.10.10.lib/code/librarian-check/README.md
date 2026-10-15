# librarian-check

Drift linter for a Librarian kernel desk. Python 3.11+ standard library only. The default run never writes inside the desk.

    python3 lcheck.py <desk>                 # report: reworked pages listed in full, pending pages as counts
    python3 lcheck.py <desk> --all           # list everything, including info and pending pages
    python3 lcheck.py <desk> --brief         # short model-facing card: reworked errors only
    python3 lcheck.py <desk> --md r.md --json r.json
    python3 lcheck.py <desk> --write-moves new-moves.toml   # derive a moves ledger from stale NNNN.title pointers
    python3 lcheck.py <desk> --fix-sentinel                 # build a missing book 00.md, then lint
    python3 sentinel.py <desk>                              # the same build, without the lint
    python3 sentinel.py <desk> --dry-run                    # print the sentinel, write nothing

Exit code 1 when a reworked page has an error. That is how it gates a commit or a pack.

## Files
- `rules.toml`: scope (`reworked_max_page = 30`, history and work faces), plus one block per rule giving its severity (error, warn, info, off), the kernel page it comes from, and a summary.
- `moves.toml`: moves ledger. Each entry names a number, the title it used to hold, and where that title lives now. Edit it by hand.
- `pre-commit`: git hook.
- `report.md`, `report_all.md`, `report_brief.txt`, `report.json`: output from the run on the 2026-10-08 kernel draft.

## Tiers
- **reworked**: law pages 0000-0030, the whole syntax book, and desk furniture. Listed in full.
- **pending**: law pages above 0030. Counted only. After the rework, raise `reworked_max_page`.
- **history**: the notes book and face 06. Pointer rules are skipped. Face 05 is work, so its pointer findings drop to info. Struck text (~~ ~~) and `### notes` blocks are skipped everywhere.

## Rules (each cites the kernel page it comes from)
| rule | default | source |
|---|---|---|
| face-name | error | law 0018 Envelope/Seat, law 0001 Face name, law 0005: FF / FF.VVV / FF.VVV.09 / 05.NN, FF 01-08 |
| face-00-on-page | error | law 0000 face 01 |
| face-07-filled | warn | law 0007 face 01: a filled face 07 is a halt |
| live-needs-01 | error | law 0001 live |
| stamp-missing / stamp-mismatch | warn / error | law 0000 face 02 stamp, law 0024 (no version line cannot be ranked) |
| status-vocab, status-header-state, status-footer | error/warn/error | axioms Marks: draft < signed < approved < lock |
| seat-is-draft | error | law 0021/0022: onto the seat only by approve |
| draft-version | error | law 0024 Number |
| stale-draft | warn | law 0021/0022: approve renames, it does not copy; old seat becomes FF.VVV.09 |
| same-version-differs | error | law 0024, law 0021 patch; axiom 8 Record |
| cite-format | error | axioms Chain |
| dangling-page | error | axiom 7 Missing (a required absence is a defect) |
| stale-address | error (NNNN.title or moves-ledger hit) / info (heuristic) | law 0018 (title unique under parent), axiom 6 Lineage |
| reassigned-number | warn, error if the old title is on the same line | axiom 6 + moves ledger |
| carry-terms | error | law 0036 face 01 Overflow/Unprompted, law 0040, law 0006 |
| twin-heading | info | law 0001 twin, law 0004 ("not required") |
| register / order / sentinel | error / warn / error | syntax 0014 (00.REG.md, 00.md), law 00.order |
| work-file-name | info | law 0005 (05.plan.md is a convention the law doesn't name) |

## Stable IDs (light proposal)
Law 0018 already says a title is unique under its parent, so `NNNN.title` is a natural stable key.
1. Always cite with the title (`0036.colab`, not `0036`). Then the linter can prove a pointer is right.
2. Keep `moves.toml`, or a `was` column in the register. When a title moves, record its old number and new home. Never drop a row.
3. Optional later step: add an `id:` line to each page's face 01 stamp (for example `id: colab`, or a short random code) that never changes. Pointers would carry it, and the linter would resolve the id instead of the number.

## Workflow
- **Before every pack** (law 0037 check step): run `--brief`. Put the card on the pack door, so the sleeve knows which pointers are known-stale and doesn't report them as factfinds.
- **After a return, before the prime writes** (law 0036 Temp): run it again. New errors mean the pass broke something.
- **Before approve or promote** (law 0022/0023): require exit 0 for the pages being seated.
- **Git pre-commit**: `cp pre-commit .git/hooks/` and set `LCHECK`/`DESK`.
- **Model-facing**: the brief card follows the kernel's card style and says it is "not a write. not permission". A model reads it as findings, not as instructions.

## Missing book sentinel
Syntax page `0014`, face `02`, card `00.md`, says a cold boot can build the file. The three lines are what this is, the first page, and what this is not. Law page `0054`, section Job, says `00.md` proves the book. If the file is missing, the container is not real.

A sentinel finding names that card. `sentinel.py` reads the card on the desk being checked. Law page `0056`, band, says a band door ends in 0 and is not a member, and that work starts at `1000` with that door left open. When the book has a `1000` door, the first live section is the first page at `1001` or after. Pages before that door are reserved and are not chosen. A book with no `1000` door still takes the first live row of `00.REG.md` or `REG.md`, else the first line of `00.order.md`, else the lowest page folder. It writes `BOOK/00.md` only when that file is absent. It does not overwrite a sentinel, and it does not write `00.start`, a register, or a page file. If the card or the first page cannot be opened, it stops and writes nothing. `--fix-sentinel` is that build, then the lint.
