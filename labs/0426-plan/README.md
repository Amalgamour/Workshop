# Plan: 90.50.10.0426 split-commands (the stable kernel split)

Lead: Claude, acting lead (t562u). 2026-11-23.
Decision: Matthew t565s2260 (Nov 23, 3:17 PM EST) said yes: page 0426, title split-commands, packed right after 0423 is closed and its trial is done, before 0425 and before 0422.05.01.
This folder is a plan, not a packed page.

**Revision 2 (t570u, Nov 23 3:33 PM EST):** Matthew asked for 0426 to be drafted beside the live kernel. So the page now has two passes:
- **05.01, the proof test** (PACK-0426-05.01.txt). The only file it touches is `tests/page_0426.rs`, which no page holds, so it is packed now on today's layout. It pins `wf help` and a full page loop's log and views against a golden copy kept inside the test file. An ignored `regenerate_golden` test refreshes the golden at any start commit.
- **05.02, the move** (PACK-0426-05.02.txt; this was 05.01 in revision 1). It is packed only when Codex reports 0423 closed. It first refreshes the golden at its own start commit and commits that alone, then moves the code, and the test must still pass.

This makes the move checkable without anyone waiting: the proof is written and checked while 0423 is still open. Section 6 below still describes what the proof covers.

**Tools (lead lab work, not a pass):**
- `tools/split_cmd.py` splits `src/cmd.rs` into the group files by function name. It is a move only, and it can be re-run at any start commit. I ran it once in a local scratch worktree and nothing was pushed. It is offered to the 05.02 builder, and to the optional dry run, as a starting point. It is not a substitute for their own check.
- `tools/push_log.ps1` pushes a page log to returns only if the published log is a byte prefix of the local log. It commits only that path.

**Matthew's framing (t565s2260):** this builds a stable kernel that every page pulls from and rarely changes: the shared helpers, the log, the page lock and the router. That lets forks of work run in parallel. Command groups sit on top, in their own files.

## 1. Why

At a823ee28 nearly every command lives in three files:
- `src/cmd.rs`, 984 lines: every command (init_page :181, face_write :233, draft :262, pack :357, claim :435, ret :488, push_log :558, publish_pack :583, intake :605, check :724, signoff :796, close :842, answer :881).
- `src/lib.rs`, 303 lines: the HELP text, the dispatch match, writes(), Args and the page lock.
- `src/page.rs`, 397 lines: KINDS, order() and apply() for every log kind.

So 0408, 0423, 0425, 0409, 0406, 0411, 0412 and 0422.05.01-05.03 all wait one at a time for the same files. Waves 5-10 in docs/plan/GROK-BUILDER-QUEUE.md are a single-file queue on `src/cmd.rs`, so most of the five Grok builders wait.

**Axioms:**
- **1 Authority:** each grant names the part of wf it changes, not a file that everyone needs.
- **2 Fractal:** the code splits along the lines of the work (start, plan, build, sync, check, close, lock). One work order maps to one module.
- **7 Missing:** the move is checked mechanically, so nothing is lost or invented on the way.

## 2. Page number

0426 is the next open 04NN.
- On packs, pages exist for 0400, 0403, 0404, 0407, 0408, 0415, 0416, 0418, 0419, 0422 and 0424.
- Reserved in the queue: 0405, 0406, 0409-0414, 0417, 0420, 0421, 0423, 0425, 0497 and 0498.
- 0401 and 0402 were dropped and are not reused.
- The only earlier mention of 0426 is the withdrawn 0422-0426 five-page split (CLAUDE-LEAD-0422.md:37). No page, pack or reservation uses it.

## 3. Target layout

This is a move, with no behaviour change. Names are this plan's proposal. The builder may adjust a name for a good reason, and must say so in the return.

**Kernel: rarely changes, and every page uses it.**
| File | Holds |
|---|---|
| `src/lib.rs` | Args, the page Lock, writes(), and a small router that sends each command name to its group's `run` |
| `src/cmd/mod.rs` | shared command helpers only: need, nonblank, no_ctrl, why_ref, must_be, not_halted, prime_or_person, tail_is, parse_pass, nn, pass_number_ok, text_arg, fields, repo, system_ref and the like. It declares the group modules. |
| `src/page.rs` | load, the hash-chain check, the Page and Pass types, check_addr, and the order() and apply() frame that calls into the rules |
| `src/page/rules/mod.rs` | the list of kinds (KINDS, PASS_KINDS), built from the rule modules; declares them |
| `src/log.rs`, `src/chars.rs`, `src/git.rs`, `src/addr.rs` | unchanged, and not in this grant |

**Command groups: each in its own file, with its own HELP lines and `run`.**
| File | Commands at a823ee28, plus what 0408 and 0423 add |
|---|---|
| `src/cmd/start.rs` | init_page, set_prime, grant, halt, resume |
| `src/cmd/plan.rs` | face_write, draft, pack, overlap checks; 0408's withdraw |
| `src/cmd/build.rs` | claim, ret, parse_return, ret_change_paths |
| `src/cmd/sync.rs` | merge_into_shared, push_log (with 0423's prefix check), publish_pack, intake |
| `src/cmd/check.rs` | check, check_report, refuse_passed |
| `src/cmd/close.rs` | signoff, close, elevate, answer |
| `src/cmd/lock.rs` | 0423's lockout, try-out, release and override |

**Rules: each kind's order and apply arms go with its group.** These are `src/page/rules/<group>.rs`, for example `start.rs`, `plan.rs`, `build.rs`, `check.rs`, `close.rs` and `lock.rs`.

**Not moved:** `src/render.rs`, `src/status.rs` and `src/board.rs` are held by other pages (0407, 0413, 0414, 0406 and 0424) and are not in this grant. Their calls into `cmd::` or `page::` are kept working through re-exports in `src/cmd/mod.rs` and `src/page.rs`, so those files need no edit. If a re-export cannot do it, the builder stops and raises it.

**After the split, a typical page holds:**
- one group file, plus its rule file, when it changes an existing group;
- `src/lib.rs` (one router line) and `src/cmd/mod.rs` (one `mod` line), when it adds a group;
- `src/page/rules/mod.rs`, when it adds a log kind.

That is why `src/lib.rs`, `src/cmd/mod.rs` and `src/page/rules/mod.rs` must stay small. Lesson 4 of 0705 applies: a new module still needs its parent's declaration.

## 4. Grant

The page grant at `init-page` is the same as the 05.01 may-touch:
- `src/cmd.rs` (deleted)
- `src/cmd/`
- `src/lib.rs`
- `src/page.rs`
- `src/page/`
- `tests/page_0426.rs`

Folder grants work at a823ee28. A grant path that ends in `/` covers every file under it: `g == path || (g.ends_with('/') && path.starts_with(g))` (src/page.rs:83).

**Disjointness.** When 0426 is packed:
- 0408 and 0423 are closed, with their trials done;
- 0425 and 0422.05.01 wait for it (t565s2260);
- 0409, 0406, 0411 and 0412 wait for it as before;
- no other page holds `src/cmd.rs`, `src/lib.rs` or `src/page.rs`.

0407 (`src/render.rs`), 0424 (`src/board.rs`) and 0419.05.02 (`tests/lab_0419.rs`) do not overlap.

## 5. Order

```
0408 closed -> 0423 closed (and its trial)
  -> 0426 split-commands, one pass, one Grok builder, then Grok-Check
  -> 0426 closed (and its trial, tests/lab_0426.rs on 0701)
  -> 0425 (Codex) and 0422.05.01 (Claude). They can now run in parallel if their files differ:
     0422.05.01 holds src/report.rs and src/lib.rs.
     0425 likely holds src/cmd/start.rs and src/page/rules/start.rs, and needs src/lib.rs only if it adds a group.
```

**A risk, raised:** 0425 and 0422.05.01 both need `src/lib.rs` if each adds a command group. Then one waits for the other's one pass, not for a whole page. Under R2, 0425 goes first if it is drafted by then.

## 6. Proof that nothing changed

These are the pack's checks plus the checker's own view (axiom 9):
1. `cargo test --lib` and `cargo test --test page_0426` pass.
2. Every `tests/page_*.rs` and `tests/lab_*.rs` at the start commit passes unchanged on the return. The return lists each one with its result.
3. The `tests/wf.rs` failures on Windows are no worse than at the start commit. The return lists the failing test names before and after.
4. `tests/page_0426.rs` checks:
   - the `wf help` output is byte for byte the text captured from the start commit (embedded in the test);
   - a full page loop gives the same log and views as the start commit, with only times and the hashes that depend on them normalised. The loop is init-page, set-prime, face-write 01/04/08, draft, pack, lockout, claim, return, release, lockout, check, release, signoff, close and verify, run against local bare remotes. The same script runs with the start-commit binary, built from a clean checkout into its own target directory.
5. The checker reads `git diff -M --stat <start> <return>` and `git diff --color-moved=zebra` to confirm the code was moved, not rewritten. Any changed logic line is named in the check.

## 7. What this changes on the 0422 track

The 0422 pass grants are re-pointed to the new paths. Matthew's yes (t565s2260) is the grant change; see labs/0422-plan/README.md, C9. The wf grant record on page 0422 still has the old paths from `init-page`. Matthew records the new grant with `wf grant` once 0426 is closed, before 0422.05.01 is drafted.
