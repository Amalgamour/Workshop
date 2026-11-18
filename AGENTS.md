# AGENTS.md: for any model working with this kit

## Read first
1. In the kit folder (this folder: the one with this file, `src/`, and `docs/`): `docs/AXIOMS.md`: the nine axioms.
2. Same folder: `docs/DESIGN.md`: the page, the faces, the pass, the roles.
3. If you hold a pass: `pages/<page>/05.<NN>/AGENTS.md` and `PROMPT.md`.
   They pin the hash of AXIOMS.md and DESIGN.md. If yours differ, stop and tell Prime.

Check every choice against these axioms:
- **1 Authority**: act only inside what you were granted.
- **5 Frame**: know the goal and why before you start.
- **7 Missing**: a gap is reported, never invented or quietly filled.
- **9 Trial**: your own work is checked by another view, never by you.

## The one rule
Never edit anything under `pages/` by hand. Only `wf` writes there.
A hand edit is caught and refused. Say who you are on every command: `--as <name>`.
A log entry out of the commands' order (for example a close before a return, a claim after a close, a second init, an unknown kind, a pass number outside 01-98) makes the page unreadable: every command names the entry and the rule, exits 1 and writes nothing. Why (axiom 1, authority): a forged or hand-written log must not steer what the tool does next. These order rules are build stage, no Director ruling yet.

## The tool you run
The `wf` you run must be a pinned build of the last merged commit, kept apart from
where builders build. README setup is two steps: build once, then copy the binary.
When you build or test, set your own `CARGO_TARGET_DIR` (for example `target-builder`)
and never build into the pinned copy. A builder build must not overwrite the tool
that judges the work. When an old and a new build share a `CARGO_TARGET_DIR`, run
`cargo clean -p wf` and touch the sources between them, or the new tests may run
against the old binary.

## Your role, and what you may run
| Role | You may run |
|---|---|
| Builder | `claim`, `return`, `elevate --to prime`, `status` |
| Checker | `check`, `status` (never on a pass you built) |
| Observer | `observe`, `observe --record "finding"`, `status` (never if you are Prime) |
| Prime | `face-write 01 02 04 06 08`, `draft [--overlap-ok NN --why "... (ref)"]`, `pack [--overlap-ok NN --why "... (ref)"]` (Director t262u: "sometimes multiple models can sit at this"), `signoff --outcome ... [--cards ...] [--note "... (ref)"]`, `close`, `elevate --to person`, `answer`, `set-prime --ref` |
| Person | `init-page`, `face-write 04 --section responses`, `grant`, `answer`, `set-prime --ref` |

Anyone may run `status`, `observe`, `verify` and `board`.

`wf board [<page>] [--all] [--card NN] [--stall-hours 24]` is read only: it writes no log entry, no view file and no lock, and runs no git. It is built from `log.jsonl` only (the log wins over a hand-edited view, and the board says so). With a page it prints attention first, then one card per 05.NN in the columns Draft, Ready, Working, Waiting check, Checked, Closed; with no page it prints one line per page (an unreadable page is named with its reason). `--card` takes `4`, `04` or `05.04`; other flags are refused. Why: see what needs someone in under a minute (docs/design/WF-BOARD.md). Every log string is escaped like `\u{1b}`. Build stage, pending Director answer (WF-BOARD.md Q1-Q3): tool words as columns with body-shop side labels; STALE after 24 hours with no log entry (`--stall-hours`); the board prints git commands for the evidence instead of running git.

`wf halt <page> --note "why (ref)"`: Prime or the person stops the page (refused while a pass is open); draft, pack and claim then refuse, and status shows who halted it and why.
`wf resume <page> --note "why (ref)"`: Prime or the person lets work go on again.

Pass numbers may be written `1` or `01`. Hashes are sha256; a 12-character prefix is shown.

A pack stores the template version it was printed with. Packs with no version reprint from the v1 (8eb1fdb) text kept in the binary, so a later template change does not rewrite past job boxes (axiom 6). New packs record version 2.

Command flags and pack fields are checked in one place. Refused: every character whose Unicode general category is Cc, Cf, Zl, Zp, Co or Cn, plus the Hangul fillers U+3164, U+115F and U+1160, and a field that is only combining marks. CR is refused everywhere. A newline is kept only in face text (`--file` or `--text`) and in pack field values. Draft field keys are checked too.

Text that came from a builder (return file job lines, notes, elevation items made from them, and changed file names from git) is shown escaped, for example `\u{1b}`, in status, observe and the 05 views when it contains a refused character. A hostile return can still be logged as evidence. The escape is a no-op when the text has no refused character, so past views stay the same.

## As a builder
1. `wf claim <page> <NN> --as <you>`. The first claim wins.
2. Commit on your pass branch, created from the start commit; push only where your setup says.
   The branch is `pass/<page>.05.<NN>`.
3. Touch only the "may touch" files. The return file under `.workshop/returns/` is always
   allowed. The tool takes the changed-file list from git (create, modify, delete); the
   `changed:` line is your summary. Anything outside may touch gets the return refused.
4. Copy `pages/<page>/05.<NN>/RETURN-TEMPLATE.md` to the return path in the prompt.
   Fill every line, in this order:
   - `pack:` the pack hash (already filled)
   - `done:` what you did
   - `changed:` your summary of creates, modifies and deletes; the tool takes the list from git
   - `noticed:` what you noticed
   - one line per job: `w01: done - ...`, `w02: need - ...` or `w02: blocked - ...`
   - `proof:` commits, tests and what they showed
   - `not done:` what you did not do, and why
   - `unprompted:` anything done that was not asked
   - `overflow:` ideas past this job
5. Commit the work and the return file. Push only where your setup says.
6. Ping: `wf return <page> <NN> --branch pass/<page>.05.<NN> --commit <sha> --file <return path> --as <you>`
7. Stuck, or need something outside your frame? Do not fix it. End that job `need`
   or `blocked` and say why. The tool sends it to Prime.

## As a checker
`wf check <page> <NN> --as <you> [--note "..."] [--fail "why"] [--dry-run]`.
`--dry-run` runs the checks and prints the full output, and writes nothing.
The tool runs the pack's checks on the returned commit.
Before you file, read the return file (in the returned commit) and the diff
(from the pack's start commit to the return commit).
"Done when" lives on face 01, and is copied into the pack and the printed job at release.
The check report uses the packed done-when. If face 01 changed since the pack, the report notes the drift.
A filed report is built after the check takes the lock and reloads, so a face 01 change during the check is included.
Judge those lines yourself; add `--fail` if a "done when" line is not met, even when the commands pass.
Then run without `--dry-run` to write your report.

`--why` and `--note` need a reason and a (ref), both non-blank. `set-prime --ref`, `grant --ref` and `answer --text` refuse blank or spaces.
`wf close` re-runs the passed-signoff refusals, and a passed close is refused if face 01 changed after the signoff entry (a note stored for something else does not cover it).

## As an observer
`wf observe <page>` lists signals: many passes, the same blocker again,
two closes in a row that did not pass, no movement for a day, goals changed
under an open pass, unanswered questions. File one finding with evidence:
`wf observe <page> --record "one plain line" --as <you>`. It stops nothing.
