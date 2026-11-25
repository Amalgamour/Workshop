# Test plan: the draft-page kernel

Builder: Claude. 2026-11-25. Status: `9` (no test here has been run).
These are the tests a later builder pass would write. This lab writes no test code.
The design they test is labs/draft-page/README.md. Section numbers below point there.

## How every test runs

- **The box is Windows**, in PowerShell or from `cargo test`.
- No `std::os::unix`, no `sh`, and no check command that is only `true`, `grep` or `test`. Prima's packs use the same rule (labs/0426-plan/PACK-0426-05.01.txt, the overview line).
- **wf is called as a built binary**, never through `src/` code. So a test still works after 0426 moves the code.
- **Everything happens in a temp folder**: a run folder, a work clone, and a local bare remote. Never the network.
- **Time is fixed** with `WF_NOW`, so logs repeat (src/log.rs:32-34).
- Each test builds into its own `CARGO_TARGET_DIR`. It never builds into the pinned `wf-bin` (AGENTS.md:22-26).
- Each test removes its temp folder at the end, even when it fails. The 0423 trial left `lab0423-*` folders behind (WORK-PAGE-2026-11-25.md:57 @dcdab638).
- **The wf under test must have the 0423 lockout.** Every page write in the steps first takes the matching lockout and releases it after (src/page.rs:369-386).
- Shorthand used in the steps:
  - `L` is the live page, for example a page that edits `src/cmd.rs`.
  - `D` is the draft page, with draft branch `draft/<D>`.
  - "the kernel file" is one file both pages' may-touch names, for example `src/cmd.rs`.

Where the tests could live is a builder choice at pack time. One proposal: one file, `tests/lab_draft_page.rs`, as a lab trial. It is not decided here.

---

## Part 1: the draft sits beside the live kernel

### D1 draft_pack_records_its_draft_branch
- Tests: README section 4.
- Steps:
  1. Start page D with a grant on the kernel file.
  2. Write faces 01 and 06, draft, then `wf pack D 1 --branch draft/D`.
  3. Read the pack entry in D's log, and `pages/D/05.01/PACK.md`.
  4. Run `wf status D`.
- Expected:
  - The pack entry's `branch` is `draft/D`, and its `start` is the live head.
  - PACK.md names `draft/D` as the branch.
  - Status shows 05.01 at `pack`.

### D2 draft_return_leaves_returns_untouched
- Tests: README sections 3 (rule 2) and 5.
- Steps:
  1. Note the bare remote's `returns` tip.
  2. Builder A locks D on face 05, claims D 05.01, commits a change to the kernel file on a branch from the start, and fills the return file.
  3. `wf return D 1 --branch draft/D --commit <sha> --file <return> --push`.
  4. Read the remote's `returns` tip and `draft/D` tip again.
- Expected:
  - `returns` is exactly the same commit as in step 1.
  - `draft/D` contains A's commit.
  - D's log, with the return entry, is on `draft/D` at `.workshop/logs/D/log.jsonl`. It is not on `returns`.

### D3 live_lane_keeps_working_during_the_draft
- Tests: README sections 1 and 5 ("Why the draft branch frees the lanes").
- Steps:
  1. Run D1 and D2. D 05.01 is now returned on `draft/D` and not yet checked.
  2. On page L, worker B locks face 05, packs L 05.01 on `--branch returns`, claims it, changes the same kernel file, and returns with `--push`.
- Expected:
  - Every L command succeeds.
  - `returns` now has B's change.
  - `draft/D` is the same commit as after D2.
  - No D command was needed for L's work, and no L command was refused because of D.

### D4 one_worker_on_the_draft_page
- Tests: README section 5 (t533u, 0423).
- Steps:
  1. Worker A locks D on face 05.
  2. Worker B runs `wf lockout D 05 --reason test`.
  3. Worker B runs `wf try-out D`.
  4. Worker B runs `wf claim D 1`.
- Expected:
  - Step 2 is refused, naming face 05 and A (src/cmd.rs:579-581).
  - Step 3 prints "you would be refused" and names A (src/cmd.rs:598-603).
  - Step 4 is refused, and nothing is written. D's log is the same bytes before and after.

### D5 the_pinned_tool_never_changes_during_a_draft
- Tests: README sections 2 and 3 (rule 1).
- Steps:
  1. Copy a built wf into `<temp>/wf-bin/wf.exe` as the "pin", and record its sha256.
  2. Run D1 and D2 using that pin.
  3. Build the draft branch's code into a separate `<temp>/target-draft`.
  4. Record the pin's sha256 again.
- Expected:
  - The two hashes are equal.
  - The draft build exists only under `<temp>/target-draft`.

### D6 intake_reads_the_draft_branch_only_when_asked
- Tests: README section 5 ("Where the draft pass's log goes").
- Steps:
  1. Run D1 and D2 in a builder's run folder.
  2. In a second run folder, which is Prima's view, run `wf intake`.
  3. Then run `wf intake --branch draft/D` (src/cmd.rs:832).
- Expected:
  - Step 2 takes nothing for D.
  - Step 3 takes D's new entries.
  - After step 3, `wf verify D` says ok.

---

## Part 2: catching up and switching

### D7 catch_up_by_merge_is_append_only
- Tests: README section 6, step 2 (a change that is not a move).
- Steps:
  1. Run D2, then D3, so `returns` has moved past D's start.
  2. Record the `draft/D` tip as `old`.
  3. On `draft/D`, run `git merge --no-edit origin/returns` in a work clone, then push without force.
  4. Record the new `draft/D` tip as `new`.
- Expected:
  - `git merge-base --is-ancestor old new` is true.
  - `git merge-base --is-ancestor <returns tip> new` is true.
  - The push is accepted with no force. The test remote has `receive.denyNonFastForwards=true`, so a rewrite would be refused.

### D8 catch_up_by_replay_for_a_move
- Tests: README sections 6 (step 2) and 10 ("Why a move is the easy case").
- Steps:
  1. In a temp copy of the kit at commit X, run `python -I labs/0426-plan/tools/split_cmd.py`, and record the tree hash (`git write-tree` after `git add -- src`).
  2. Reset to X and run it again. Record the tree hash.
  3. Make a live change at X to one function in `src/cmd.rs`, for example a changed message in `claim`. Commit it as X2.
  4. Run the recipe at X2.
- Expected:
  - Steps 1 and 2 give the same tree hash. The recipe gives the same result each time.
  - After step 4, the changed message is in `src/cmd/build.rs`, and `src/cmd.rs` is gone.
  - `cargo build` succeeds at both X and X2.
- Note: this needs Python on the box. Matthew's PC has it: the recipe was run there once (labs/0426-plan/README.md:14). If a builder's box has none, the test says so and stops. It must not pass silently.

### D9 switch_is_a_merge_and_never_forced
- Tests: README sections 6 (step 6) and 7.
- Steps:
  1. Catch up `draft/D` as in D7 or D8.
  2. Record the `returns` tip as `live`.
  3. In a work clone, merge `draft/D` into `returns` with a merge commit. Push without force. The remote has `receive.denyNonFastForwards=true`.
- Expected:
  - The push is accepted.
  - `git merge-base --is-ancestor live <new returns tip>` is true.
  - Every commit on `draft/D` is now reachable from `returns`.

### D10 stale_packs_are_listed_after_the_switch
- Tests: README section 6, step 7.
- Steps:
  1. Before the switch, pack page S 05.01 at the old live head, with may-touch on the kernel file. Leave it unclaimed.
  2. Pack page T 05.01 with may-touch on a file the draft does not touch.
  3. Do the switch (D9).
  4. Run the lead's stale-pack list. It reads every page's latest pack entry, its `start` and its `may touch`. It lists a pack when its start is not a descendant of the switch merge and its may-touch overlaps the draft's may-touch. The overlap rule is the same as `paths_overlap` (src/page.rs:102).
- Expected:
  - The list names S 05.01.
  - The list does not name T 05.01.
  - With a wf that has `withdraw` (src/cmd.rs:460): `wf withdraw S 1`, then a new pack at the new head, is accepted. The log keeps the withdrawn pass.

### D11 freeze_list_finds_open_passes_on_other_pages
- Tests: README section 6, step 1, and section 5 ("The lock is per page, not per file").
- Steps:
  1. Pack and claim page L 05.01 with may-touch on the kernel file. Leave it open.
  2. Pack and claim page M 05.01 with may-touch on an unrelated file.
  3. Run the lead's freeze list for D. It lists every open pass, on any page, whose may-touch overlaps D's may-touch. An open pass is one at pack, open, return or review.
  4. Close L 05.01, and run the freeze list again.
- Expected:
  - Step 3 lists L 05.01 only.
  - Step 4 lists nothing. The switch may start.
  - This also shows the gap: `wf pack` on D alone does not refuse in step 3, because refuse_overlap reads only D's own passes (src/cmd.rs:344).

### D12 published_logs_keep_their_bytes_through_a_switch
- Tests: README section 7.
- Steps:
  1. Before the switch, save the bytes of every `.workshop/logs/*/log.jsonl` on `returns`.
  2. Do the switch (D9).
  3. Read the same files again.
- Expected:
  - Each old file is a byte prefix of its new version. Most are equal.
  - No log file is shorter, and none differs inside its old length.

---

## Part 3: dropping a failed draft

### D13 a_failed_draft_is_dropped_with_no_harm_to_live
- Tests: README section 8.
- Steps:
  1. Run D1 to D3.
  2. A checker checks D 05.01 with `--fail "test"`.
  3. The Prime signs off D 05.01 as `failed`, then closes it.
  4. Compare with the state saved before step 2: the `returns` tip, the pin's sha256, and the bytes of every other page's log.
- Expected:
  - The `returns` tip, the pin hash and every other page log are unchanged.
  - `draft/D` still exists, and its tip is unchanged.
  - `wf status D` shows 05.01 closed, outcome failed.
  - L's next pass can be packed and claimed as normal.

### D14 an_unclaimed_draft_is_withdrawn_not_deleted
- Tests: README section 8, step 2.
- Needs a wf with `withdraw` (src/cmd.rs:460).
- Steps:
  1. Pack D 05.01 on `draft/D`, and never claim it.
  2. The Prime runs `wf withdraw D 1`.
  3. Worker B runs `wf claim D 1`.
- Expected:
  - Step 2 is accepted, and the log keeps the pass as withdrawn (docs/design/STAGE-PLAN-90.50.10.md:110-115 @dcdab638).
  - Step 3 is refused.
  - `returns` and `draft/D` are unchanged.

---

## Part 4: the 0426 worked example

### D15 the_0426_proof_refreshes_before_the_move
- Tests: README section 10, steps 2 and 5.
- Uses the proof test of 0426.05.01, `tests/page_0426.rs` (labs/0426-plan/PACK-0426-05.01.txt, jobs w03-w04).
- Steps:
  1. At a live head, run `cargo test --test page_0426 -- --ignored regenerate_golden`, and commit that alone.
  2. Run the split recipe (D8), and commit.
  3. Run `cargo test --test page_0426`.
  4. Run the whole suite: `cargo test --no-fail-fast`.
- Expected:
  - Step 3 passes with the golden copy from step 1 unchanged.
  - Step 4 has no new failures compared with the same run at the step 1 commit. The return lists each test file's result before and after.

---

## What these tests do not cover

- **The pin record (QUESTIONS.md Q2).** It has no test until Matthew picks where the pin is written.
- **Approval of the switch (Q3).** It is a human step. The test can only show that the merge happens after a passed close of the switch pass.
- **A real conflict in a merge catch-up.** D7 uses changes that merge cleanly. A conflict is the builder's job inside the switch pass, and its check judges it.
