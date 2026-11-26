# Fire sale prototypes, Thu Nov 26 2026 (jobs 10-14)

Written by the Prima fire-sale worker, 12:42 AM EST (jobs 10-12); jobs 13-14 added 12:49 AM EST. Corrected 1:00 AM EST (job 20): H4 and H7 said "R16" for the held overflow item; it is kernel/CONFLICTS.md D1 (R16 is the dictionary `03.00` door, docs/spec/DIRECTOR-RULINGS.md:65). Samples only. None of this is a pass return.

## Where it lives

- Scratch worktree: `/workspace/firesale-notes/proto`, made by `git worktree add /workspace/firesale-notes/proto -b firesale/proto-2026-11-26 build` (base 8994afd).
- Branch: `firesale/proto-2026-11-26`. **Local only. Never pushed, never merged.**
- Commits on the scratch branch:
  - `fd453dd`: job 10, `crates/seqaddr-core/tests/page_0418.rs`
  - `4a0c361`: job 11, `firesale-proto/golden-norm/` (a standalone crate with its own `[workspace]`, not a member of the repo workspace)
  - `07cd904`: job 13, `crates/seqaddr-core/tests/hostile.rs`
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

The repo-wide `cargo test --workspace --offline` did not run then: other crates need `async-trait`, which wasn't in the box's offline cargo cache. Job 14 below fetched it and ran the whole workspace.

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

## Job 13: hostile test pass on seqaddr-core

Scratch commit `07cd904` on `firesale/proto-2026-11-26` adds `crates/seqaddr-core/tests/hostile.rs`. It has 40 cases and adds no dependencies (the fuzz uses a hand-written xorshift, not proptest).

What it covers:
- **R9 counters.** `00` and `99` are refused with rule R9 on every route: full, short, leading dot, with a tail, with a card, on the door page. `01` and `98` parse and round-trip, with every counter tail. `counter_role` bounds hold at 0, 1, 98, 99 and 255. Faces `00` and `99` still parse as faces (seqAddr 5.1).
- **Edge addresses.** `00.00.00.0000`, `99.99.99.9999` and `00`/`99.99.99` containers. Short forms read right to left (seqAddr 2.1, 2.2). Four ancestors are refused, two page groups are refused, and `0000.timer` is refused (A2.8). `sentinel` is checked at widths 2, 3 and 4, and `page_kind` at all 18 range edges (seqAddr 6). Bands and sets are checked too (6.1, R18).
- **Malformed tails (seqAddr 4, 8).** Counter tails on a page or a bare face, `retired` with a counter, two tails, a tail then a title, a counter after a tail, tails on containers, and a title between a page and its face (A2.2). Cards and brands: 000 and 999 are refused, a bare brand is refused, and so are a 2-digit brand, two brands, two cards, and a tail word as a card.
- **Words (seqAddr 3).** Capitals, `_`, a leading `-` and a leading digit are refused. `t-` and `a--b` are accepted, which the spec allows.
- **Unicode and whitespace (seqAddr 3, R4).** All of these are refused: full-width digits, Arabic-Indic digits, accented letters, zero-width space, BOM, NBSP, a combining accent, a `ﬁ` ligature, U+2028, an RTL override, tab and newline, and empty groups.
- **Very long input.** A 100,000-character title, 50,000 groups, 50,000 faces and 100,000 digits run without a panic.
- **Round trip.** 524 generated addresses (4 ancestor forms × 7 pages × 19 endings, less the illegal `0000.title` ones), plus active-relative addresses and containers: print(parse(s)) == s and parse(print(parse(s))) == parse(s).
- **Fuzz.** 200,000 random strings over `0-9 . a d e i n o p r t v w x -`. No panic. Every accepted string prints back byte-identical.
- **Also checked:** `BookId::parse` strictness, `parse_full_page`, `expand` (missing gives 404, several active pages are elevated), and log timestamps (leap years, 24:00, missing Z, full-width digit). `BookLog` refuses non-ASCII, `\u2014` and `\u0000` escapes, and bad headers.
- **State level.** A counter on uncounted face 01 is refused (A4.4). A seat at plain 05 is refused. 06.01-06.98 can be written, but 06.99 has no address.

**Result: 40 of 40 pass. No parser bug was found.** The parser holds against every hostile input above.

Spec mismatches. The code follows the rulings; the spec text was not updated (`docs/spec/seqAddr.md`, same on build and the scratch branch):

| id | where in seqAddr.md | spec says | code does | severity |
|---|---|---|---|---|
| H1 | 1.4 table, line 53 | `FF.00` is a counted face's board | parse refuses `FF.00` (R9) | Medium |
| H2 | 5.7, lines 197-199, example line 209 | "A face is counted if and only if `FF.00` exists"; `1523.05.00 board` | counted = 05, 06 and `Policy.extra_counted`; `FF.00` cannot be written | Medium |
| H3 | 5.7, line 202 (t511/t512) | "Plain `05` is the seat"; "The board of the passes stays `05.00`" | state.rs:459-460 refuses a put at plain 05 (A4.4); `05.00` is refused at parse. Same as P1 and the red page_0418 case | High (blocks 0418) |
| H4 | 7.1, line 262; 7, line 259 | once `FF.98` exists, `FF.99` points to the next page | `FF.99` refused at parse (R9). A 99th pass or note has no address at all; what follows counter 98 is held `7` (kernel/CONFLICTS.md:148, D1) | Medium |
| H5 | 8 grammar, line 282; rules, lines 293-294 | `counter = 2DIGIT ; 00 board, 01-98, 99 continuation`; "A counter requires its face's `00` board"; "write it as `FF.00`" | 01-98 only; the rule is now "counters only on counted faces" (A4.4) | Medium |
| H6 | 1.2 table, lines 29-31 | `01-09` reserved "on every axis" | faces 01-09 are the ordinary faces (5.1); R9 says faces have no sentinels. The table should say which axes it covers | Low |

Code notes (not spec):
- **H7 (Low).** Dead code at state.rs:426-433 (`if nn == 99`). It can never run, because line 417 refuses 99 first. Keep it, remove it, or mark it for D1; that choice belongs to whoever takes D1.
- **H8 (Low).** The printers don't check what they print. `PageAddr` and `FacePart` are pub structs, so a hand-built value can print text that reads back differently, or not at all. Desk set with no shelf prints `10.21.4442`, which reads back as shelf 10. Counter 0 prints `.05.00`, which is refused. parse never builds either value. Code that builds addresses by hand (compute, wf) should go through parse, or there should be a checked constructor.
- **H9 (Low, for the compute).** Titles have no length limit. A 100,000-character title is accepted. The spec sets none (seqAddr 3), but an HTTP compute should cap input size before it parses.

## Job 14: full workspace test run

`cargo fetch --locked` in the scratch worktree reached crates.io over the network without credentials. `Cargo.lock` was unchanged. Then `CARGO_TARGET_DIR=/workspace/firesale-notes/target cargo test --workspace --locked --no-fail-fast`. The build finished in 19.5 s with 0 warnings. Full output is in `/workspace/firesale-notes/proto-workspace-test-full.txt` (box only).

| crate | test binaries | passed | failed | ignored |
|---|---|---|---|---|
| ask | solve 10 | 10 | 0 | 0 |
| compute | lib 1, ask 3, clock 2, contract_delivery 1, delivery 11, host 2, http 15, r5 4, restart 6 | 45 | 0 | 0 |
| seqaddr-core | grammar 79, hostile 40 (job 13), log_format 35, page_0418 4+1 fail (job 10), repo_books 1, resolve_validate 75, tails 56 | 290 | 1 | 0 |
| seqpage | cli 3, corrupt 37, face00 9, golden 6, round_trip 4 | 59 | 0 | 0 |
| trial-compute | binary 2, crash 2, findings 15, held 14 | 33 | 0 | 0 |
| trial-core | grammar_hostile 8, log_hostile 10, rules_hostile 20 | 38 | 0 | 2 |
| **total** | doc tests: 0 in all 6 crates | **475** | **1** | **2** |

- The one failure is `page_0418::seat_at_plain_05_is_accepted`, the expected red case from job 10 (H3). It isn't in build's code; it's in the scratch test file.
- Without the two scratch files (hostile.rs, page_0418.rs), the build tree is **431 passed, 0 failed, 2 ignored**.
- The 2 ignored tests are in trial-core `rules_hostile`: `a_kernel_draft_counter_is_not_inherited` (finding 6) and `back_link_must_be_live_not_a_draft` (finding 12). Both are marked "raised 7, see Fix pass", so they are known held items and not new.
- This was a Linux run only. The Windows sync_dir failures (0701 baseline) are not covered here.

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
