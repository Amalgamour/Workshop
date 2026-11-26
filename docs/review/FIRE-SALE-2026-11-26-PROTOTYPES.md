# Fire sale prototypes, Thu Nov 26 2026 (jobs 10-12)

Written by the Prima fire-sale worker, 12:42 AM EST. Samples only. None of this is a pass return.

## Where it lives

- Scratch worktree: `/workspace/firesale-notes/proto`, made by `git worktree add /workspace/firesale-notes/proto -b firesale/proto-2026-11-26 build` (base 8994afd).
- Branch: `firesale/proto-2026-11-26`. **Local only. Never pushed, never merged.**
- Commits on the scratch branch:
  - `fd453dd`: job 10, `crates/seqaddr-core/tests/page_0418.rs`
  - `4a0c361`: job 11, `firesale-proto/golden-norm/` (a standalone crate with its own `[workspace]`, not a member of the repo workspace)
- Build output: `CARGO_TARGET_DIR=/workspace/firesale-notes/target`.
- wf sandbox for job 12: `/workspace/firesale-notes/wf-sandbox` (a throwaway copy. Not a git repo at the root. `work/` is a fresh `git init` with no remote).
- No wf command ran against a real worktree. Nothing was edited in src/, tests/, .workshop/, pages/ or labs/ on build or packs.

## Job 10: sample test for 0418.05.01 (w02)

What 0418.05.01 says it delivers (packs PACK.md, start c1750c32): plain 05 takes a seat; 05.NN stays a pass; plain 06 is still not a seat; face 06 has no door of its own. Grant file: `crates/seqaddr-core/tests/page_0418.rs`. seqaddr-core is the same at c1750c32 and at build (`git diff c1750c32 build -- crates/seqaddr-core` is empty), so build is a fair base.

The test has 5 cases, one for each claim plus `always_counted(5|6)`. It uses `tests/common` without changing it and has no `std::os::unix`.

Result, `cargo test --no-fail-fast` in crates/seqaddr-core:

| test binary | pass | fail |
|---|---|---|
| grammar | 79 | 0 |
| log_format | 35 | 0 |
| repo_books | 1 | 0 |
| resolve_validate | 75 | 0 |
| tails | 56 | 0 |
| **page_0418 (new)** | **4** | **1** |

- The one fail is `seat_at_plain_05_is_accepted`: `Rejected { rule: "A4.4", "face 05 is counted ... no door of its own (R9)" }` from state.rs:459-460. That is expected. w01 has not been applied, so the test is red before the change and should go green after it. That shows the test can fail.
- The existing 246 tests all pass.

Findings for the builder and Prima:
- **P1 (Medium).** The Done-when line "The board of the passes stays 05.00" can't be checked as an address. `Address::parse("….05.00")` is refused with rule R9 (tests/resolve_validate.rs:147), while seqAddr.md 5.7 says the board "stays `05.00`". The code reads the board as plain `FF`, which t512 now gives to the seat. The builder has to decide how the pass board is read once plain 05 is the seat. That is the "a rule reads two ways" stop-if. Before release, Prima should say which read is meant (for example `05.board`, or a listing call, not an address).
- **P2 (Low).** A note on face 06 can't be made at tail `open` (format 3.3: a counter must be claimed, then moved). A test fixture must create notes at `pack`. My first draft got this wrong, so a builder may too.
- **P3 (Medium, found in job 12).** The pack's Done-when lines come from face 01, not from the draft text. A `done when:` field in the draft file was ignored. So the DW2 fix (a Done-when line that needs page_0418.rs) has to be written to face 01 with face-write before any repack.

## Job 11: golden-output normaliser for 0426.05.01 (DW3)

The problem: wf runs check commands through `cmd /C` on Windows and `sh -c` elsewhere (src/git.rs `run`, at bcf0680e). A golden copy captured on Windows has CRLF line ends and cmd's error text. The packed w02 list normalises only times, hex, the temp root and `\` under the root.

The prototype is `firesale-proto/golden-norm`, three layers, each its own function so a checker can see exactly what is hidden:
1. `newlines`: CRLF and lone CR become LF.
2. `shell_neutral`: cmd's two-line `'X' is not recognized as an internal or external command, / operable program or batch file.` and the sh forms (`sh: 1: X: not found`, `sh: X: command not found`, `sh: line 1: X: command not found`) become `<shell>: X: not found`. Other lines are left alone.
3. `w02`: the packed list exactly (ISO times and `time_s` become `<time>`; 64/40-hex, or 12-hex after hash/head/commit/start, become `<hex>`; the root becomes `<root>`; `\` under the root becomes `/`; `\` outside the root is kept).
- `first_diff` gives the first differing line after normalising.

Result, `cargo test` in golden-norm: **12 passed, 0 failed**. Tests include:
- `w02_alone_does_not_hide_crlf` shows DW3: with only the packed list, a Windows golden fails on the box.
- `live_sh_not_found_equals_canned_cmd_not_found` runs a missing command through `sh -c` on the box, the way wf does, and matches a canned `cmd /C` capture.
- Negative cases: lines with spaces are not touched, a backslash outside the root is kept, an un-keyed 12-hex is kept, and exit codes stay different (the normaliser can't hide ok against fail).
- `normalise_is_idempotent`.

The repo-wide `cargo test --workspace --offline` did not run: other crates need `async-trait`, which isn't in the box's cargo cache offline. Only seqaddr-core and golden-norm were run.

## Job 12: SC1 trial, `wf draft --overlap-ok` after a packed 05.01

Isolation (all of this was met, otherwise the trial would have been skipped):
- Binary: `/workspace/workshop-build/wf-bin-a823/bin/wf` (built from a823ee28, the pinned wf that reads template 4). The older `wf-bin/wf` (a00bc53) refused the page: `unknown template version "4"`.
- Data: only `pages/90.50.10.0418/` copied from the packs worktree (tip c697e035) into the sandbox.
- Env: `env -i PATH=/usr/bin:/bin HOME=<sandbox> WF_ROOT=<sandbox> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`, cwd the sandbox. Read from a823/a00bc53 source: `draft` and `claim` make no git calls; `pack` only reads (`rev-parse`, `remote get-url origin`) from `<root>/work`. The sandbox `work/` has no remote, so the packed `remote` is `""`. Only `publish`/`return` push, and neither was run.
- Proof the real packs worktree is unchanged: the sha256 of its 0418 log.jsonl (0dca7c82…), its `git status` (0 lines) and its HEAD (c697e035) are identical before and after.

Steps and results:

| step | command (in the sandbox) | result |
|---|---|---|
| A | `draft 90.50.10.0418 --file draft-0502.txt` | refused: "05.01 is at 'pack' and not closed" |
| B | same, plus `--overlap-ok 1 --why "sandbox trial …"` (no ref) | **drafted 05.02** (exit 0) |
| C | `pack 90.50.10.0418 2` (no flag) | refused: "may touch overlaps open pass 05.01" (lists all 5 files) |
| D | `pack … 2 --overlap-ok 1 --why "…"` without a (ref) | refused: "--why needs a reason and a (ref)" |
| D2 | same with "(fire-sale SC2)" | **packed 05.02**, entry 8, `overlap_ok: 1` recorded |
| E | `claim … 1 --as Grok-4` | **claimed 05.01** |
| F | `claim … 2 --as Grok-5` | **claimed 05.02** |

What it shows:
- **SC1/SC2 confirmed:** option D (repack beside the held pack with `--overlap-ok`) works in wf a823. A fixed 05.02 can be released without withdrawing 05.01.
- **New risk (High):** after D, **both passes stay claimable and were both claimed**, by two builders on the same five grant files. `--overlap-ok` does not retire, hold or lock 05.01. If option D is chosen, 05.01 has to be closed or withdrawn by a recorded step right after 05.02 is packed, or the 05.02 overview must say "05.01 is dead, do not claim". There is a real chance a builder claims the old pack. Raise this in Monday list M2.
- **Inconsistency (Low):** `draft --overlap-ok` took a `--why` with no (ref); `pack --overlap-ok` demanded one. Worth a wf note.
- **Odd (Low):** 05.02's PROMPT.md says "Read first: pages/…/05.01/AGENTS.md (reused from 05.01)". That's fine for a repack, but the builder of 05.02 is pointed into the old pass's folder.
- P3 above (Done-when comes from face 01) also came from this trial.

## What a real pass would need

0418.05.02 (a repack of 05.01, or the held 05.01 once released):
- Grant: unchanged (state.rs, resolve.rs, validate.rs, face.rs, tests/page_0418.rs).
- Face 01, before the repack, adds: "Done when: tests/page_0418.rs exists and shows: a seat at plain 05 is accepted; 05.NN is still a pass; plain 06 is still not a seat; face 06 has no door of its own. Each case is its own test." Plus: "Done when: page_0418 fails at the start commit and passes after w01 (the builder pastes both runs)."
- It also resolves P1: replace "The board of the passes stays 05.00" with the read Prima picks.
- If option D: a recorded withdraw or close of 05.01 right after 05.02 is packed, and the 05.02 overview says 05.01 must not be claimed.

0426.05.01 (repack, Prime question DW1 still first):
- Grant: unchanged (`tests/page_0426.rs` only). The normaliser lives inside the test file, so golden-norm is a pattern to copy, not a crate to add.
- Change w02's list to add: "CRLF becomes LF; the shell's not-found message (cmd /C or sh -c) becomes one form. Nothing else changes."
- Face 01 adds: "Done when: the golden region is the same whether regenerated on Windows or on the box; the checker regenerates on the box and git diff shows no change." And: "Done when: the normaliser has a unit test that a CRLF cmd /C capture equals the LF sh -c capture, and one that a different exit code is still a difference."
- Stop-if adds: "the capture differs between Windows and the box for any reason other than the normalised ones."
- Better still: keep check-command error text out of the golden (record exit code only). That removes the shell difference at the source.

## Cleanup (for Prima, not done)

- Remove the scratch worktree and branch when done: `git -C /workspace/workshop-build/repo worktree remove /workspace/firesale-notes/proto` then `git branch -D firesale/proto-2026-11-26`. Not run here, because the scratch branch is the evidence.
- `/workspace/firesale-notes/wf-sandbox` and `/workspace/firesale-notes/target` can be deleted freely.
