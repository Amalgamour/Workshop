# AGENTS.md: for any model working with this kit

## Read first
1. `docs/AXIOMS.md`: the nine axioms.
2. `docs/DESIGN.md`: the page, the faces, the pass, the roles.
3. If you hold a pass: `pages/<page>/05.<NN>/AGENTS.md` and `PROMPT.md`.
   They pin the hash of AXIOMS.md and DESIGN.md. If yours differ, stop and tell Prime.

Check every choice against these axioms:
- **1 Authority**: act only inside what you were granted.
- **5 Frame**: know the goal and why before you start.
- **7 Missing**: a gap is reported, never invented or quietly filled.
- **9 Trial**: your own work is checked by another view, never by you.
Before any write, run the cold set `1.7.8`.

## The one rule
Never edit anything under `pages/` by hand. Only `wf` writes there.
A hand edit is caught and refused. Say who you are on every command: `--as <name>`.

## Your role, and what you may run
| Role | You may run |
|---|---|
| Builder | `claim`, `return`, `elevate --to prime`, `status` |
| Checker | `check`, `status` (never on a pass you built) |
| Observer | `observe`, `observe --record "finding"`, `status` (never if you are Prime) |
| Prime | `face-write 01 02 04 06 08`, `draft`, `pack`, `signoff`, `close`, `elevate --to person`, `answer`, `set-prime` |
| Person | `init-page`, `face-write 04 --section responses`, `grant`, `answer`, `set-prime` |

Anyone may run `status`, `observe` and `verify`.

## As a builder
1. `wf claim <page> <NN> --as <you>`. The first claim wins.
2. Work only on branch `pass/<page>.05.<NN>`, from the start commit in the prompt.
3. Touch only the "may touch" files. Anything else gets the return refused.
4. Copy `pages/<page>/05.<NN>/RETURN-TEMPLATE.md` to the return path in the prompt.
   Fill every line, in this order:
   - `pack:` the pack hash (already filled)
   - `done:` what you did
   - `changed:` each file, as `create path` or `modify path`
   - `noticed:` what you noticed
   - one line per job: `w01: done - ...`, `w02: need - ...` or `w02: blocked - ...`
   - `proof:` commits, tests and what they showed
   - `not done:` what you did not do, and why
   - `unprompted:` anything done that was not asked
   - `overflow:` ideas past this job
5. Commit the work and the return file. Push the branch.
6. Ping: `wf return <page> <NN> --branch pass/<page>.05.<NN> --commit <sha> --file <return path> --as <you>`
7. Stuck, or need something outside your frame? Do not fix it. End that job `need`
   or `blocked` and say why. The tool sends it to Prime.

## As a checker
`wf check <page> <NN> --as <you> [--note "..."] [--fail "why"]`.
The tool runs the pack's checks on the returned commit and writes your report.
Add `--fail` if a "done when" line is not met, even when the commands pass.

## As an observer
`wf observe <page>` lists signals: many passes, the same blocker again,
two closes in a row that did not pass, no movement for a day, goals changed
under an open pass, unanswered questions. File one finding with evidence:
`wf observe <page> --record "one plain line" --as <you>`. It stops nothing.
