# Report

- Builder: Grok-Check
- Page/pass: 90.50.10.0423 05.03
- Kind: check
- Verdict: fail
- Commands run:
  - git checkout -- pages; git pull --ff-only origin packs
  - git -C work fetch origin; git -C work pull --ff-only origin returns
  - wf.exe intake
  - cargo test --lib; cargo test --test page_0423; cargo test --test page_0408; cargo test --test lab_0404; cargo test --test wf; cargo test --no-fail-fast, at f1e2481a05a95cb506c3f22dec2e35326dbb437a with CARGO_TARGET_DIR C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target
  - wf.exe check 90.50.10.0423 3 --dry-run
  - wf.exe check 90.50.10.0423 3 --as Grok-Check --fail "cargo test --test wf does not pass: 113 passed, 20 failed, 0 ignored. Done when line 2 is not met. The 20 names match Grok-2. No test was deleted, skipped, ignored, or rewritten." --note "Entry 30 elevates w02 need. That stop is working as written, not a missing job. Fourteen tests/wf.rs failures are assertions the 0423 lock entries made false (entry numbers or one holder). Five are Windows limits (seq, sh, or Os error 123). draft_refuses_a_99th_pass still asserts under 10 s and took 20.7567982 s in the checker cargo test --test wf. tests/page_0407.rs:45 fails with lockout first and is outside the grant; it was not edited. Catch row 16, reprint_failure_after_append_says_logged_as, was not seen on Windows. It is Unix-only. Prima recorded its release refusal as view files differ from the log. It is not a pass or a fail from this run."
  - copy pages/90.50.10.0423/log.jsonl to work/.workshop/logs/90.50.10.0423/log.jsonl; git add -- that path; commit; git -C work push origin returns
  - wf.exe verify 90.50.10.0423
- Packed Cargo, separate from the verdict:
  - Dry-run exit 0. Wrote nothing. The log stayed 139036 bytes, 30 lines. Worktree C:\Users\misg\AppData\Local\Temp\wf-check-11560-f1e2481a of f1e2481a. Frame ok: A .workshop/returns/90.50.10.0423.05.03.md, M tests/common/mod.rs, M tests/lab_0404.rs, M tests/page_0408.rs, M tests/wf.rs. Wall 57384 ms, 2026-11-25T21:55:56.907Z through 2026-11-25T21:56:54.292Z.
  - Dry-run results: cargo test --lib 52 passed, 0 failed, finished in 0.12s, compile finished in 5.21s. cargo test --test wf FAILED, 113 passed, 20 failed, 0 ignored, finished in 30.57s, compile finished in 3.92s. cargo test --test page_0408 3 passed, 0 failed, finished in 7.91s, compile finished in 0.39s. cargo test --test lab_0404 2 passed, 0 failed, finished in 3.29s, compile finished in 0.42s. cargo test --test page_0423 17 passed, 0 failed, finished in 3.65s, compile finished in 0.70s. The 20 wf names are the same list as the independent run. draft_refuses_a_99th_pass took 21.4736889s in that dry-run.
  - Recorded check exit 0, verdict fail. Worktree C:\Users\misg\AppData\Local\Temp\wf-check-25220-f1e2481a of f1e2481a. Same frame. Wall 52725 ms, 2026-11-25T21:57:34.584Z through 2026-11-25T21:58:27.309Z. Windows PowerShell 5.1. Checker wf.exe is the install built from a823ee284574be3d9f6247925b9088137a27a539 (986624 bytes, 2026-11-23T10:26:18).
  - Recorded packed results: cargo test --lib ok, 52 passed, 0 failed, finished in 0.12s, compile finished in 4.87s. cargo test --test wf FAIL, 113 passed, 20 failed, 0 ignored, finished in 28.72s, compile finished in 3.90s. cargo test --test page_0408 ok, 3 passed, 0 failed, finished in 5.90s, compile finished in 0.36s. cargo test --test lab_0404 ok, 2 passed, 0 failed, finished in 2.91s, compile finished in 0.41s. cargo test --test page_0423 ok, 17 passed, 0 failed, finished in 3.48s, compile finished in 0.79s. draft_refuses_a_99th_pass took 20.3725897s in that packed wf run.
  - Because cargo test --test wf failed, wf printed every Done when line as "not met", and printed "jobs not done: w02" because the return marks w02 need. That text is the packed-command result. The checker's judgment of the four lines is below. The verdict is fail because Done when line 2 is unmet and --fail names it.
- Results:
  - wf check 05.03: fail (exit 0).
  - Independent target at the return commit, worktree C:\Users\misg\AppData\Local\Temp\wf-0423-ret. Wall of the set: 2026-11-25T21:48:34.877Z through 2026-11-25T21:50:19.900Z.
  - cargo test --lib exit 0, 52 passed, 0 failed, 0 ignored, finished in 0.21s, compile 5.64s. Wall 6748 ms, 2026-11-25T21:48:34.877Z through 21:48:41.625Z.
  - cargo test --test page_0423 exit 0, 17 passed, 0 failed, finished in 4.22s. Wall 7245 ms, 21:48:41.626Z through 21:48:48.871Z.
  - cargo test --test page_0408 exit 0, 3 passed, 0 failed, finished in 6.50s. Wall 6957 ms, 21:48:48.871Z through 21:48:55.829Z.
  - cargo test --test lab_0404 exit 0, 2 passed, 0 failed, finished in 2.92s. Wall 3464 ms, 21:48:55.829Z through 21:48:59.293Z.
  - cargo test --test wf exit 101, 113 passed, 20 failed, 0 ignored, finished in 28.74s. Wall 30531 ms, 21:48:59.293Z through 21:49:29.825Z.
  - cargo test --no-fail-fast exit 101. Wall 50075 ms, 21:49:29.825Z through 21:50:19.900Z. Two targets failed: page_0407 and wf. Suite summaries: lib 52/0 finished in 0.13s; main 0/0 finished in 0.00s; lab_0404 2/0 finished in 4.17s; lab_0415 1/0 finished in 0.23s; lab_0419 1/0 finished in 0.29s; lab_0423 4/0 finished in 6.32s; page_0407 FAILED 0 passed, 1 failed, finished in 0.01s; page_0408 3/0 finished in 5.74s; page_0419 4/0 finished in 0.13s; page_0423 17/0 finished in 3.39s; wf FAILED 113 passed, 20 failed, finished in 28.23s; doc-tests 0/0 finished in 0.00s.
  - The 20 tests/wf.rs names match Grok-2's w02 list. None new. None missing. The 21st name Grok-2 recorded is tests/page_0407.rs a_band_door_lists_each_page_with_its_log_state_and_a_non_door_has_no_list at line 45. This run failed that test the same way. No other ungranted file failed.
  - Catch row 16, reprint_failure_after_append_says_logged_as, was not seen on Windows. It is Unix-only (#[cfg(unix)] at tests/wf.rs:976). It is not a pass and not a fail from this run. Prima recorded its release refusal as "view files differ from the log". The sibling reprint_failure_when_temp_path_is_a_directory_says_logged_as passed.
  - Start 4203dc0f813570ae0030b93c1f64edf516d2a604 is an ancestor of f1e2481a. Diff is five files, 422 insertions, 210 deletions. No src/ file.
  - Verify after the log push: ok, log chain holds (31 entries, head a39069bbd653). Views match. 05.01 AGENTS.md ace6c87175b7, PROMPT.md 9582bbde9bbb. 05.02 AGENTS.md f174acc65161, PROMPT.md 30bd10e82ed4. 05.03 AGENTS.md e30cc84722d2, PROMPT.md 6bcec3cafa71. Links 4 hold on each pass.
  - Before the check the returns log and the run-folder log were equal, 139036 bytes, 30 lines, head 6bfc3fad8695. After the check the local log is 186249 bytes, 31 lines. origin/returns:.workshop/logs/90.50.10.0423/log.jsonl was still those 139036 bytes and is a byte prefix of the local log. The copied bytes match. The pushed file is that 31-line log. Returns tip at the push was 1b82a124, so no fast-forward was required before the copy.
  - Intake, after the packs fast-forward already held the 30-line log, printed ready to check: none. It refused only 90.50.00.0001 and 90.50.10.0403. Returns at intake was 1b82a124.
  - Did not sign off. Did not close.
- wf entry numbers:
  - close of 05.02 is entry 22, actor prima, outcome passed, time 2026-11-24T19:34:31Z
  - grant is entry 23, actor matthew, paths tests/common/mod.rs, tests/wf.rs, tests/page_0408.rs, tests/lab_0404.rs, ref t584s2361, time 2026-11-25T20:09:50Z
  - face 01 replace is entry 24, time 2026-11-25T20:10:07Z, prev fe1b17648ca9d4dc8f9987ec9e3b8f9f8a6dcb35c128aa55779803f1532b272a
  - face 06 note is entry 25
  - draft of pass 3 is entry 26
  - pack is entry 27, pack hash a478641bcd2c22e7b7fe4e71cd5be868df93cb464f41e67f0fb43225dbe69200, time 2026-11-25T20:10:14Z, prev 67611de016ebfe1e11d14cf30784e562738f74d954ff551651968193deeef1fb
  - claim is entry 28, actor Grok-2, role builder, pass 3, time 2026-11-25T20:14:48Z, prev b8e20e634c4f7e9655bc33f015eead61e09759fbbc7b42f9c00cb4c2f4bbc4b0
  - return is entry 29, actor Grok-2, role builder, pass 3, time 2026-11-25T20:57:08Z, commit f1e2481a05a95cb506c3f22dec2e35326dbb437a, file .workshop/returns/90.50.10.0423.05.03.md, text hash 03ac2f8534f4b1defd14bcc3462de47eeadf6d9047c3c8ba93d82efc89b07ee6, branch pass/90.50.10.0423.05.03, prev 04cfc7fcb58ce0b7e2e1ce232021f0b1a4a4fc42e542cd5bd25225b98608e252. Jobs: w01 done, w02 need, w03 done, w04 done.
  - elevation is entry 30, actor wf, role tool, to prime, time 2026-11-25T20:57:08Z, prev 72f806251d1a99ea394ff585f2de1708848de8c7e1554298b84a89721290521e, same w02 need text
  - check is entry 31, actor Grok-Check, role checker, pass 3, verdict fail, time 2026-11-25T21:58:27Z, prev 6bfc3fad8695ed943b89118d55c978b36931856db195b77cbd51ec9529ddd470. Line hash a39069bbd653c894ae0ccd9a9a7b66317c7a9b824f0839c2b790f57c818bcd1e.
- Push commits:
  - check log c91c759ff8c344212470400539a68d6a53331ce8
  - builder commit f1e2481a05a95cb506c3f22dec2e35326dbb437a
  - pack start 4203dc0f813570ae0030b93c1f64edf516d2a604
  - pack hash a478641bcd2c22e7b7fe4e71cd5be868df93cb464f41e67f0fb43225dbe69200
- Face 01 drift:
  - Sealed pin: v3 entry 24 hash 3558be0ad9ce.
  - Live face 01: v3 entry 24 hash 3558be0ad9ce. Pack sources record the same string.
  - The dry-run and the recorded check printed no drift line.
- Evidence:
  - Diff 4203dc0f..f1e2481a is the return file plus the four granted test files. git diff --name-only -- src is empty.
  - Test and helper names, 4203dc0f against f1e2481a: tests/common/mod.rs has no #[test] fn; added add_held, held, held_no, held_wf, lock, lock_face_for, unlock; removed none. tests/wf.rs #[test] fns 138 to 138, removed none; added helpers lock_code and unlock_code. tests/page_0408.rs #[test] fns 3 to 3, removed none. tests/lab_0404.rs #[test] fns 2 to 2, removed none.
  - Cargo on this box reported 0 ignored on every target. The Windows wf binary ran 133 tests (113 passed, 20 failed). That is the same 113 and 20 Grok-2 named. No #[ignore] and no skipped test showed up.
  - Removed lines in the diff are the old unlocked call sites. The same writes and the same assertion strings are now inside lock, held, or unlock. The panic text in this run still contains the old expected strings: entry 3, entry 4, entry 6, entry 7, entry 8, entry 10, "want under 10 s", "view files differ from the log", "seq", "sh", and the allowed claim-loser wording. Those strings were not rewritten to the new entry numbers.
  - Done when line 1, the writers take the matching lockout through the real wf commands: met. tests/common/mod.rs:55 lock calls wf lockout. tests/common/mod.rs:58 unlock calls wf release. tests/common/mod.rs:62 held locks, writes, releases, and asserts both ok. ready at 88-96 inits the page (init is not a locked write), holds face 04 for the goals write, then one lock on 01 covering face 01 and face 06, then unlock. draft_jobs at 101-104 holds 04. open at 107-110 holds pack as pri and claim as bob. checked at 172-178 holds check as cat. close_one at 157-169 holds the writes, then one lock covering signoff and close. Each of those ends with no holder. Env::ret at 130-142 runs the return unlocked first. If it succeeds, or the refusal is something other than "refused: lockout first", it returns that result so a caller that already holds 05 keeps the hold. Otherwise it takes 05 through held_wf. add_held at 203-216 writes lockout, the event, and release through Page::add in-process, on the same append path, and does not write Page.hold by hand. It exists so seed_closed_passes does not spawn wf for 98 closed passes and blow the 10 second bound. The return discloses it. It is not a skipped lock and not a deleted assertion. Line 1 stays met.
  - Done when line 2, cargo test --test wf, page_0408, and lab_0404 pass, with no deleted, skipped, ignored, or rewritten assertion: unmet. page_0408 is 3 passed. lab_0404 is 2 passed. cargo test --test wf is 113 passed, 20 failed, 0 ignored. This is the --fail. w02 is marked need, and entry 30 elevates that need to prime. The stop is the written stop-if: name an assertion the 0423 rule made false, and do not change the line. w02 is not a missing job.
  - Done when line 3, cargo test --lib and cargo test --test page_0423 still pass, and no src/ file changes: met. Lib 52 passed, 0 failed, in the independent run and in both packed runs. page_0423 17 passed, 0 failed, in all three. git diff --name-only start..f1e2481a -- src is empty. work_refuses_with_no_lock_and_under_another_workers_lock passed.
  - Done when line 4, cargo test --no-fail-fast is pasted in proof and any remaining failure is named with its file and cause: met as the proof obligation. The return pastes the twelve "test result:" summaries and names page_0407 line 45 plus the same 20 wf tests. It says lab_0415, lab_0419, lab_0423, and page_0419 passed, and that no other ungranted file failed. "Pasted" there means those result summaries and the named failures. This checker's own run produced the same two failing targets and no extra name. Every test result line from this checker's run is below. The Unix-only reprint test is not in that paste and is not scored here.
  - Each named failure, from this run's panic text:
    - pack_prints_prompt_and_pins_axioms_and_design, tests/wf.rs:37. Assertion the 0423 rule made false. The link still wants log entry 3, face 01 v1. The printed link is entry 6.
    - last_line_tamper_shows_in_the_stamp, tests/wf.rs:289, panicked at tests/common/mod.rs:52. Assertion the 0423 rule made false. Wanted "view files differ from the log (hand edit or a failed reprint)". Got "log chain broken at line 8" because the release is the last line.
    - eight_claim_runs_leave_one_claim, tests/wf.rs:482. Assertion the 0423 rule made false. All eight got "refused: lockout first". Left 0, right 1. One holder cannot cover eight claimers.
    - check_commands_run_without_holding_the_page_lock, tests/wf.rs:607. Assertion the 0423 rule made false. "refused: lockout first".
    - check_report_includes_drift_that_happens_during_the_check, tests/wf.rs:648. Assertion the 0423 rule made false. "refused: lockout first". The check needs cat on 05 and the mid-check face 01 write needs pri.
    - check_refuses_if_another_check_is_filed_first, tests/wf.rs:663. Assertion the 0423 rule made false. Both refused lockout first. Left 0, right 1.
    - board_marks_a_waiting_pass_and_drift_as_stale, tests/wf.rs:1622. Assertion the 0423 rule made false. The board printed 17 entries, last entry 16, observer entry 17.
    - board_marks_a_check_on_another_commit_and_an_old_signoff, tests/wf.rs:1644. Assertion the 0423 rule made false. Printed check entry 25 and return entry 19.
    - entry_for_a_missing_pass_is_unreadable_not_a_panic, tests/wf.rs:1790. Assertion the 0423 rule made false. 10.10.10.0401 printed entries 8. The other page still showed unreadable.
    - book_board_lists_pages_and_shows_an_unreadable_one, tests/wf.rs:1843. Assertion the 0423 rule made false. 10.10.10.0401 printed entries 8.
    - wrong_order_entries_make_the_page_unreadable, tests/wf.rs:1985. Assertion the 0423 rule made false. 10.10.10.0401 printed entries 8. The forged pages still printed as unreadable.
    - check_after_a_signoff_says_signed_off_and_next_close, tests/wf.rs:2135, panicked at tests/common/mod.rs:52. Assertion the 0423 rule made false. Wanted signoff entry 10. The refusal names entry 25.
    - t379u_edited_link_target_is_invalid, tests/wf.rs:2821. Assertion the 0423 rule made false. verify names entry 6, face 01 v1.
    - stripped_hashes_with_a_rechained_log_stay_invalid_after_fix, tests/wf.rs:2892. Assertion the 0423 rule made false. verify names pack entry 13.
    - check_stores_at_most_last_40_lines_of_output, tests/wf.rs:385. Windows limit. "'seq' is not recognized as an internal or external command".
    - check_escapes_ansi_cursor_codes_so_a_fail_cannot_repaint_the_screen, tests/wf.rs:417. Windows limit. "'sh' is not recognized". The frame still printed ok.
    - return_accepts_git_paths_with_spaces_tabs_newlines_and_non_ascii, tests/wf.rs:855. Windows limit. Os error 123 InvalidFilename.
    - planted_file_names_are_escaped_in_views, tests/wf.rs:1475. Windows limit. Os error 123 InvalidFilename.
    - board_escapes_hostile_log_text_everywhere, tests/wf.rs:1685. Windows limit. Os error 123 InvalidFilename.
    - draft_refuses_a_99th_pass, tests/wf.rs:969. Something else. The assertion text is still "want under 10 s" (count unchanged). This cargo test --test wf run took 20.7567982s. The same test in cargo test --no-fail-fast took 20.2819715s. Grok-2 recorded 5.78s when the test ran alone, 18.8434974s inside cargo test --test wf, and 17.9402722s in the whole suite. The packed dry-run took 21.4736889s and the recorded packed wf run took 20.3725897s. The 10 second line was not changed. This is suite timing under load.
    - tests/page_0407.rs a_band_door_lists_each_page_with_its_log_state_and_a_non_door_has_no_list, line 45. Assertion the 0423 rule made false, and outside the grant. Panicked at tests/page_0407.rs:45:85: refused, nothing written: refused: lockout first. The file was not edited. This is the stop-if that says name it and do not edit it. Done when line 2 does not require this file to pass.
- Code commit: f1e2481a05a95cb506c3f22dec2e35326dbb437a
- Time taken: independent suite about 105s (21:48:34Z through 21:50:19Z). Dry-run 57384 ms. Recorded check 52725 ms.

## Checker test result lines

Every `test ... ok` line, every `test ... FAILED` line, and every `test result:` line from the independent run at f1e2481a. Panic bodies are omitted here. The cause of each failure is in Evidence.

```
===== cargo test --lib =====
     Running unittests src\lib.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\wf-6f6048d9c6267a7e.exe)
running 52 tests
test addr::tests::classifiers_match_seqaddr_core ... ok
test addr::tests::each_rule_has_its_own_message ... ok
test addr::tests::work_pages_pass ... ok
test board::tests::card_takes_nn_or_05_nn ... ok
test board::tests::clip_cuts_after_escape_and_never_inside_an_escape ... ok
test board::tests::short_values_are_cut_before_escaping ... ok
test chars::tests::categories_and_fillers_match_the_table ... ok
test board::tests::check_on_another_commit_names_which_commit ... ok
test chars::tests::escape_is_identity_without_an_unsafe_char ... ok
test board::tests::missing_time_is_unknown_and_never_stale ... ok
test chars::tests::escape_uses_rust_style_hex_and_keeps_newlines_in_text ... ok
test board::tests::open_pass_is_stale_after_the_stall_hours ... ok
test cmd::tests::check_text_refuses_each_class_and_keeps_newlines_only_when_asked ... ok
test cmd::tests::fields_join_indented_lines ... ok
test board::tests::card_says_unknown_for_fields_not_in_the_log ... ok
test cmd::tests::pass_number_ok_allows_01_to_98_and_refuses_0_and_99 ... ok
test cmd::tests::pin_text_pads_pass_number ... ok
test board::tests::attention_order_and_none_found ... ok
test cmd::tests::why_ref_needs_a_reason_and_parenthetical ... ok
test git::tests::clip_check_out_keeps_short_output ... ok
test cmd::tests::v4_return_needs_a_filled_design_review_and_v3_does_not ... ok
test git::tests::clip_check_out_keeps_last_40_and_notes_the_cut ... ok
test board::tests::each_tail_shows_in_its_column ... ok
test git::tests::parse_name_status_keeps_letters_and_splits_a_rename ... ok
test git::tests::parse_name_status_rejects_a_bad_line ... ok
test git::tests::parse_name_status_z_keeps_spaces_tabs_newlines_and_non_ascii ... ok
test lock_tests::board_is_read_only ... ok
test log::tests::iso_known_dates ... ok
test board::tests::small_cap_cuts_cards_but_stays_within_40_lines ... ok
test board::tests::hostile_log_text_is_escaped_on_board_and_card ... ok
test log::tests::sync_dir_source_keeps_unix_fsync_and_windows_does_not_use_file_open ... ok
test log::tests::write_record_sends_the_line_and_newline_in_one_write ... ok
test page::tests::done_when_lines_reads_face_01 ... ok
test page::tests::face01_drift_compares_pack_source_to_current_face ... ok
test page::tests::inside_scope ... ok
test page::tests::open_tails_hold_files ... ok
test cmd::tests::write_commands_refuse_missing_parts_without_a_panic ... ok
test page::tests::paths_overlap_file_and_folder ... ok
test render::tests::connections_table_cells_cannot_add_a_column ... ok
test render::tests::missing_or_v1_selects_the_8eb1fdb_text ... ok
test render::tests::unknown_version_names_the_page_and_entry ... ok
test render::tests::v2_selects_the_current_text ... ok
test lock_tests::acquire_succeeds_when_free ... ok
test render::tests::v4_uses_the_v3_agents_and_prompt_and_the_v4_return ... ok
test render::tests::v3_agents_has_nothing_pass_specific ... ok
test board::tests::cap_never_cuts_person_questions_or_the_halt ... ok
test lock_tests::acquire_waits_then_succeeds ... ok
test log::tests::append_syncs_the_page_folder_when_it_creates_the_log ... ok
test lock_tests::acquire_refuses_after_the_wait ... ok
test log::tests::read_names_a_torn_last_line_and_leaves_the_file ... ok
test log::tests::read_names_a_last_line_with_no_newline_and_leaves_the_file ... ok
test git::tests::bracket_hash_git_grep_matches_a_heading_through_run ... ok
test result: ok. 52 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.21s
EXIT 0 cargo test --lib
START 2026-11-25T21:48:34.877572+00:00
END 2026-11-25T21:48:41.625922+00:00
MS 6748
===== cargo test --test page_0423 =====
     Running tests\page_0423.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\page_0423-f4887d3a68fbf93b.exe)
running 17 tests
test push_log_does_not_pull_merge ... ok
test post_lockout_replay_checks_lifecycle ... ok
test help_names_lockout_try_out_and_release ... ok
test missing_book_lets_only_the_person_override ... ok
test pre_lockout_order_loads_and_a_new_write_still_needs_a_lock ... ok
test legacy_page_takes_its_first_lock_and_release_does_not_restore_the_exemption ... ok
test published_0408_and_0423_logs_load_without_changing_bytes ... ok
test lockout_on_01_lasts_across_two_face_writes_until_release ... ok
test old_shape_override_reloads_after_succession_and_a_new_one_needs_live_authority ... ok
test override_accepts_the_book_prime_or_the_person ... ok
test override_basis_survives_book_prime_succession ... ok
test withdraw_still_runs_without_a_lockout ... ok
test work_refuses_with_no_lock_and_under_another_workers_lock ... ok
test second_claim_is_refused_while_one_claim_is_open ... ok
test session_05_returns_under_the_lock_and_checks_after_release ... ok
test push_refuses_when_the_published_log_is_not_a_prefix ... ok
test push_accepts_a_prefix_extension ... ok
test result: ok. 17 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 4.22s
EXIT 0 cargo test --test page_0423
START 2026-11-25T21:48:41.626103+00:00
END 2026-11-25T21:48:48.871733+00:00
MS 7245
===== cargo test --test page_0408 =====
     Running tests\page_0408.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\page_0408-1b8e9997ca55673c.exe)
running 3 tests
test withdraw_at_pack_with_no_claim_keeps_the_pass ... ok
test a_later_claim_is_refused ... ok
test withdraw_is_refused_at_open_or_later ... ok
test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 6.50s
EXIT 0 cargo test --test page_0408
START 2026-11-25T21:48:48.871791+00:00
END 2026-11-25T21:48:55.829219+00:00
MS 6957
===== cargo test --test lab_0404 =====
     Running tests\lab_0404.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\lab_0404-e7c91bf9fa4e5712.exe)
running 2 tests
test template_4_return_without_a_design_review_is_refused_and_a_filled_line_is_accepted ... ok
test templates_1_2_and_3_print_no_design_review_line_and_accept_a_return_without_one ... ok
test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.92s
EXIT 0 cargo test --test lab_0404
START 2026-11-25T21:48:55.829275+00:00
END 2026-11-25T21:48:59.293936+00:00
MS 3464
===== cargo test --test wf =====
     Running tests\wf.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\wf-f6419a392b27fab9.exe)
running 133 tests
test agents_overlap_line_cites_t262u ... ok
test board_on_real_pages_is_read_only_and_short ... ok
test board_handles_a_log_without_times_and_an_empty_log ... ok
test board_marks_a_waiting_pass_and_drift_as_stale ... FAILED
test board_escapes_hostile_log_text_everywhere ... FAILED
test board_refuses_unknown_flags_and_extra_arguments ... ok
test board_cap_never_cuts_person_questions_or_the_halt ... ok
test board_card_shows_full_commits_on_return_and_check ... ok
test board_card_with_all_is_refused_and_bad_addresses_are_escaped ... ok
test board_prints_from_the_log_over_a_hand_edit ... ok
test board_marks_a_check_on_another_commit_and_an_old_signoff ... FAILED
test book_board_lists_pages_and_shows_an_unreadable_one ... FAILED
test board_attention_puts_person_questions_first_and_the_halt_second ... ok
test answer_text_must_be_nonblank ... ok
test board_puts_each_tail_in_its_column ... ok
test board_card_names_evidence_paths_that_exist ... ok
test a_stray_agents_md_on_a_reusing_pass_is_warned_and_kept ... ok
test board_writes_nothing ... ok
test check_with_no_verdict_makes_the_page_unreadable ... ok
test builder_cannot_check_own_work ... ok
test check_escapes_ansi_cursor_codes_so_a_fail_cannot_repaint_the_screen ... FAILED
test claim_refusals_escape_a_forged_holder ... ok
test check_commands_run_without_holding_the_page_lock ... FAILED
test check_lists_jobs_not_done_apart_from_checks_ok ... ok
test check_dry_run_prints_full_output_and_writes_nothing ... ok
test check_refuses_if_another_check_is_filed_first ... FAILED
test draft_needs_a_06_note_after_the_last_close ... ok
test check_after_a_signoff_says_signed_off_and_next_close ... FAILED
test check_report_includes_drift_that_happens_during_the_check ... FAILED
test draft_field_keys_are_checked ... ok
test check_reads_done_when_from_the_pack_and_notes_drift ... ok
test eight_init_page_runs_leave_one_init ... ok
test check_stores_at_most_last_40_lines_of_output ... FAILED
test draft_refuses_pass_0 ... ok
test entry_for_a_missing_pass_is_unreadable_not_a_panic ... FAILED
test draft_waits_while_a_pass_is_open_so_files_cannot_overlap ... ok
test eight_claim_runs_leave_one_claim ... FAILED
test face_writes_follow_roles ... ok
test grant_ref_must_be_nonblank ... ok
test close_escapes_forged_record_fields_and_the_signer_refusal ... ok
test halt_and_resume_need_prime_or_person_and_a_note_with_ref ... ok
test halt_note_refuses_a_newline ... ok
test close_passed_refuses_face_01_change_after_signoff_even_with_a_stored_note ... ok
test first_claim_wins_and_only_holder_returns ... ok
test help_lists_overlap_ok_and_check_flags ... ok
test init_page_address_accepts_a_work_page ... ok
test close_passed_reruns_signoff_refusals ... ok
test init_page_address_refuses_each_rule ... ok
test job_agents_template_has_clean_and_touch ... ok
test halted_refusal_escapes_forged_halt_name_and_note ... ok
test init_page_address_system_without_a_ref_is_refused ... ok
test log_append_source_writes_one_record_and_syncs_new_dir ... ok
test init_page_address_system_records_the_ref_and_the_page_still_reads ... ok
test hand_edited_face_is_refused_then_reprinted ... ok
test last_line_tamper_shows_in_the_stamp ... FAILED
test full_pass_closes_with_a_record ... ok
test log_tamper_is_detected ... ok
test log_without_trailing_newline_is_named_and_left_alone ... ok
test job_box_names_axioms_in_the_kit_folder ... ok
test failed_check_twice_goes_up_and_blocks_passed_signoff ... ok
test draft_is_refused_while_an_earlier_pass_is_not_closed ... ok
test halted_page_shows_in_status_and_stops_draft_pack_claim ... ok
test may_touch_outside_grant_is_refused ... ok
test observe_escapes_a_forged_prime_and_elevation_target ... ok
test observe_escapes_a_forged_job_key_in_the_same_blocker_line ... ok
test observe_escapes_forged_close_outcomes_in_the_loop_line ... ok
test new_pack_records_template_version_4 ... ok
test only_prime_drafts_and_packs ... ok
test halt_is_refused_while_a_pass_is_open ... ok
test draft_overlap_ok_lets_prime_draft_while_a_pass_is_open ... ok
test overlap_ok_error_for_pass_100_does_not_print_05_100 ... ok
test observer_reports_and_files_but_prime_cannot ... ok
test need_item_goes_up_to_prime_and_prime_answers ... ok
test pack_prints_prompt_and_pins_axioms_and_design ... FAILED
test page_needs_its_person_to_start_it ... ok
test pack_reads_inline_done_when_from_real_face_01 ... ok
test past_packed_pages_still_verify ... ok
test pack_warns_on_stderr_when_face_01_has_no_done_when ... ok
test pass_100_is_not_printed_as_05_100 ... ok
test out_of_frame_return_is_refused_and_recorded ... ok
test non_prime_cannot_sign_off_and_close_needs_signoff ... ok
test pass_numbers_outside_01_98_are_refused_not_wrapped ... ok
test pack_refuses_overlapping_may_touch ... ok
test pack_allows_overlap_with_flag ... ok
test recheck_only_after_a_failed_check_and_resignoff_still_loads ... ok
test planted_file_names_are_escaped_in_views ... FAILED
test plus_one_is_not_read_as_pass_1 ... ok
test pack_allows_overlap_after_other_closes ... ok
test read_only_commands_run_while_a_lock_file_exists ... ok
test refused_append_says_nothing_was_written_and_why ... ok
test reprint_failure_when_temp_path_is_a_directory_says_logged_as ... ok
test planted_return_job_line_is_escaped_on_status_observe_and_views ... ok
test printed_fields_refuse_every_unsafe_char_class ... ok
test overlap_ok_needs_why_and_set_prime_needs_ref ... ok
test return_and_check_commits_must_be_40_or_64_hex ... ok
test overlap_ok_refuses_a_pass_that_is_not_open ... ok
test return_accepts_git_paths_with_spaces_tabs_newlines_and_non_ascii ... FAILED
test return_refusals_escape_forged_pack_branch_and_file ... ok
test role_refusals_escape_a_forged_prime_and_person ... ok
test prime_change_is_kept_and_old_prime_cannot_sign ... ok
test return_escapes_a_hostile_commit_in_its_error ... ok
test signed_off_refusal_escapes_log_text ... ok
test pin_text_in_pack_is_05_01 ... ok
test signoff_outcome_must_be_one_wf_accepts ... ok
test return_refusal_escapes_a_forged_job_key ... ok
test return_with_missing_parts_is_refused ... ok
test status_escapes_a_forged_signer_name ... ok
test return_refuses_a_rename_out_of_scope ... ok
test return_keeps_git_letters_and_prints_them_as_evidence ... ok
test stripped_hashes_with_a_rechained_log_stay_invalid_after_fix ... FAILED
test t373u_changed_template_with_fix_is_refused ... ok
test stale_pin_is_refused_until_redrafted ... ok
test t373u_hand_edited_agents_md_is_invalid ... ok
test t373u_old_page_without_a_hash_still_verifies ... ok
test sha256_repo_runs_a_full_pass_and_loads ... ok
test t379u_edited_link_target_is_invalid ... FAILED
test t379u_forged_link_is_escaped_and_refused ... ok
test t379u_valid_links_pass ... ok
test t379u_missing_link_target_is_invalid ... ok
test write_atomic_source_opens_temp_with_create_new ... ok
test t381u_lock_shows_in_status_and_observe_still_runs ... ok
test signoff_passed_refuses_unfinished_jobs_until_named ... ok
test t401u_pack_on_the_shared_branch_prints_one_builder_prompt ... ok
test torn_last_log_line_is_named_and_left_alone ... ok
test write_commands_on_forged_logs_refuse_without_a_panic ... ok
test signoff_passed_refuses_unanswered_person_elevation_and_drift ... ok
test t381u_rule_file_changed_mid_pass_locks_the_pass ... ok
test wrong_order_entries_make_the_page_unreadable ... FAILED
test t378u_hand_edit_of_a_reused_agents_md_is_invalid ... ok
test t378u_changed_agents_text_prints_a_new_hashed_file ... ok
test t378u_unchanged_agents_md_is_reused ... ok
test draft_refuses_a_99th_pass ... FAILED
test t381u_rule_file_change_is_history_for_a_closed_pass_and_the_next_pass_records_it ... ok
failures:

failures:
    board_escapes_hostile_log_text_everywhere
    board_marks_a_check_on_another_commit_and_an_old_signoff
    board_marks_a_waiting_pass_and_drift_as_stale
    book_board_lists_pages_and_shows_an_unreadable_one
    check_after_a_signoff_says_signed_off_and_next_close
    check_commands_run_without_holding_the_page_lock
    check_escapes_ansi_cursor_codes_so_a_fail_cannot_repaint_the_screen
    check_refuses_if_another_check_is_filed_first
    check_report_includes_drift_that_happens_during_the_check
    check_stores_at_most_last_40_lines_of_output
    draft_refuses_a_99th_pass
    eight_claim_runs_leave_one_claim
    entry_for_a_missing_pass_is_unreadable_not_a_panic
    last_line_tamper_shows_in_the_stamp
    pack_prints_prompt_and_pins_axioms_and_design
    planted_file_names_are_escaped_in_views
    return_accepts_git_paths_with_spaces_tabs_newlines_and_non_ascii
    stripped_hashes_with_a_rechained_log_stay_invalid_after_fix
    t379u_edited_link_target_is_invalid
    wrong_order_entries_make_the_page_unreadable

test result: FAILED. 113 passed; 20 failed; 0 ignored; 0 measured; 0 filtered out; finished in 28.74s
error: test failed, to rerun pass `--test wf`
EXIT 101 cargo test --test wf
START 2026-11-25T21:48:59.293996+00:00
END 2026-11-25T21:49:29.825076+00:00
MS 30531
===== cargo test --no-fail-fast =====
     Running unittests src\lib.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\wf-6f6048d9c6267a7e.exe)
running 52 tests
test addr::tests::classifiers_match_seqaddr_core ... ok
test addr::tests::work_pages_pass ... ok
test addr::tests::each_rule_has_its_own_message ... ok
test board::tests::card_takes_nn_or_05_nn ... ok
test board::tests::clip_cuts_after_escape_and_never_inside_an_escape ... ok
test board::tests::short_values_are_cut_before_escaping ... ok
test board::tests::check_on_another_commit_names_which_commit ... ok
test chars::tests::categories_and_fillers_match_the_table ... ok
test board::tests::card_says_unknown_for_fields_not_in_the_log ... ok
test chars::tests::escape_is_identity_without_an_unsafe_char ... ok
test board::tests::missing_time_is_unknown_and_never_stale ... ok
test chars::tests::escape_uses_rust_style_hex_and_keeps_newlines_in_text ... ok
test cmd::tests::check_text_refuses_each_class_and_keeps_newlines_only_when_asked ... ok
test board::tests::open_pass_is_stale_after_the_stall_hours ... ok
test cmd::tests::fields_join_indented_lines ... ok
test board::tests::attention_order_and_none_found ... ok
test cmd::tests::pass_number_ok_allows_01_to_98_and_refuses_0_and_99 ... ok
test cmd::tests::pin_text_pads_pass_number ... ok
test cmd::tests::why_ref_needs_a_reason_and_parenthetical ... ok
test cmd::tests::v4_return_needs_a_filled_design_review_and_v3_does_not ... ok
test board::tests::each_tail_shows_in_its_column ... ok
test git::tests::clip_check_out_keeps_short_output ... ok
test git::tests::clip_check_out_keeps_last_40_and_notes_the_cut ... ok
test git::tests::parse_name_status_keeps_letters_and_splits_a_rename ... ok
test git::tests::parse_name_status_rejects_a_bad_line ... ok
test git::tests::parse_name_status_z_keeps_spaces_tabs_newlines_and_non_ascii ... ok
test lock_tests::board_is_read_only ... ok
test board::tests::hostile_log_text_is_escaped_on_board_and_card ... ok
test log::tests::iso_known_dates ... ok
test board::tests::small_cap_cuts_cards_but_stays_within_40_lines ... ok
test log::tests::sync_dir_source_keeps_unix_fsync_and_windows_does_not_use_file_open ... ok
test cmd::tests::write_commands_refuse_missing_parts_without_a_panic ... ok
test log::tests::write_record_sends_the_line_and_newline_in_one_write ... ok
test page::tests::done_when_lines_reads_face_01 ... ok
test page::tests::face01_drift_compares_pack_source_to_current_face ... ok
test page::tests::inside_scope ... ok
test page::tests::open_tails_hold_files ... ok
test page::tests::paths_overlap_file_and_folder ... ok
test lock_tests::acquire_succeeds_when_free ... ok
test render::tests::connections_table_cells_cannot_add_a_column ... ok
test render::tests::missing_or_v1_selects_the_8eb1fdb_text ... ok
test render::tests::unknown_version_names_the_page_and_entry ... ok
test render::tests::v2_selects_the_current_text ... ok
test render::tests::v4_uses_the_v3_agents_and_prompt_and_the_v4_return ... ok
test render::tests::v3_agents_has_nothing_pass_specific ... ok
test board::tests::cap_never_cuts_person_questions_or_the_halt ... ok
test log::tests::append_syncs_the_page_folder_when_it_creates_the_log ... ok
test log::tests::read_names_a_torn_last_line_and_leaves_the_file ... ok
test log::tests::read_names_a_last_line_with_no_newline_and_leaves_the_file ... ok
test lock_tests::acquire_waits_then_succeeds ... ok
test lock_tests::acquire_refuses_after_the_wait ... ok
test git::tests::bracket_hash_git_grep_matches_a_heading_through_run ... ok
test result: ok. 52 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.13s
     Running unittests src\main.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\wf-900e32a801e04186.exe)
running 0 tests
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests\lab_0404.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\lab_0404-e7c91bf9fa4e5712.exe)
running 2 tests
test template_4_return_without_a_design_review_is_refused_and_a_filled_line_is_accepted ... ok
test templates_1_2_and_3_print_no_design_review_line_and_accept_a_return_without_one ... ok
test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 4.17s
     Running tests\lab_0415.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\lab_0415-c17d06aadbcff957.exe)
running 1 test
test creating_a_page_log_succeeds_and_sync_dir_keeps_both_branches ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.23s
     Running tests\lab_0419.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\lab_0419-8c9ed2fd87bda803.exe)
running 1 test
test safe_git_grep_form_holds_outside_page_0419 ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.29s
     Running tests\lab_0423.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\lab_0423-81339c9ccd2389f6.exe)
running 4 tests
test held_page_stays_readable_and_excludes_a_second_writer ... ok
test old_override_survives_succession_and_failed_build_does_not ... ok
test fresh_checker_sees_the_published_release ... ok
test divergent_push_is_refused_and_a_valid_extension_is_accepted ... ok
test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 6.32s
     Running tests\page_0407.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\page_0407-c8e836d454a6733a.exe)
running 1 test
test a_band_door_lists_each_page_with_its_log_state_and_a_non_door_has_no_list ... FAILED
failures:

failures:
    a_band_door_lists_each_page_with_its_log_state_and_a_non_door_has_no_list

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s
error: test failed, to rerun pass `--test page_0407`
     Running tests\page_0408.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\page_0408-1b8e9997ca55673c.exe)
running 3 tests
test withdraw_at_pack_with_no_claim_keeps_the_pass ... ok
test a_later_claim_is_refused ... ok
test withdraw_is_refused_at_open_or_later ... ok
test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 5.74s
     Running tests\page_0419.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\page_0419-5a2f72fed3971458.exe)
running 4 tests
test git_rs_documents_the_bare_form_and_the_safe_form ... ok
test bare_hash_form_is_a_sh_comment_with_no_pattern ... ok
test bracket_form_matches_a_heading_under_sh_c ... ok
test bracket_form_matches_a_heading_under_cmd ... ok
test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.13s
     Running tests\page_0423.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\page_0423-f4887d3a68fbf93b.exe)
running 17 tests
test push_log_does_not_pull_merge ... ok
test help_names_lockout_try_out_and_release ... ok
test post_lockout_replay_checks_lifecycle ... ok
test missing_book_lets_only_the_person_override ... ok
test pre_lockout_order_loads_and_a_new_write_still_needs_a_lock ... ok
test legacy_page_takes_its_first_lock_and_release_does_not_restore_the_exemption ... ok
test lockout_on_01_lasts_across_two_face_writes_until_release ... ok
test old_shape_override_reloads_after_succession_and_a_new_one_needs_live_authority ... ok
test override_accepts_the_book_prime_or_the_person ... ok
test override_basis_survives_book_prime_succession ... ok
test published_0408_and_0423_logs_load_without_changing_bytes ... ok
test withdraw_still_runs_without_a_lockout ... ok
test work_refuses_with_no_lock_and_under_another_workers_lock ... ok
test second_claim_is_refused_while_one_claim_is_open ... ok
test session_05_returns_under_the_lock_and_checks_after_release ... ok
test push_refuses_when_the_published_log_is_not_a_prefix ... ok
test push_accepts_a_prefix_extension ... ok
test result: ok. 17 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 3.39s
     Running tests\wf.rs (C:\Users\misg\AppData\Local\Temp\wf-0423-ret-target\debug\deps\wf-f6419a392b27fab9.exe)
running 133 tests
test agents_overlap_line_cites_t262u ... ok
test board_on_real_pages_is_read_only_and_short ... ok
test board_handles_a_log_without_times_and_an_empty_log ... ok
test board_marks_a_waiting_pass_and_drift_as_stale ... FAILED
test board_escapes_hostile_log_text_everywhere ... FAILED
test board_refuses_unknown_flags_and_extra_arguments ... ok
test board_cap_never_cuts_person_questions_or_the_halt ... ok
test board_card_with_all_is_refused_and_bad_addresses_are_escaped ... ok
test board_card_shows_full_commits_on_return_and_check ... ok
test board_prints_from_the_log_over_a_hand_edit ... ok
test board_marks_a_check_on_another_commit_and_an_old_signoff ... FAILED
test book_board_lists_pages_and_shows_an_unreadable_one ... FAILED
test answer_text_must_be_nonblank ... ok
test board_attention_puts_person_questions_first_and_the_halt_second ... ok
test board_puts_each_tail_in_its_column ... ok
test board_card_names_evidence_paths_that_exist ... ok
test a_stray_agents_md_on_a_reusing_pass_is_warned_and_kept ... ok
test board_writes_nothing ... ok
test check_with_no_verdict_makes_the_page_unreadable ... ok
test builder_cannot_check_own_work ... ok
test claim_refusals_escape_a_forged_holder ... ok
test check_escapes_ansi_cursor_codes_so_a_fail_cannot_repaint_the_screen ... FAILED
test check_commands_run_without_holding_the_page_lock ... FAILED
test check_refuses_if_another_check_is_filed_first ... FAILED
test check_lists_jobs_not_done_apart_from_checks_ok ... ok
test check_dry_run_prints_full_output_and_writes_nothing ... ok
test check_after_a_signoff_says_signed_off_and_next_close ... FAILED
test draft_needs_a_06_note_after_the_last_close ... ok
test check_report_includes_drift_that_happens_during_the_check ... FAILED
test check_reads_done_when_from_the_pack_and_notes_drift ... ok
test draft_field_keys_are_checked ... ok
test eight_init_page_runs_leave_one_init ... ok
test check_stores_at_most_last_40_lines_of_output ... FAILED
test draft_refuses_pass_0 ... ok
test entry_for_a_missing_pass_is_unreadable_not_a_panic ... FAILED
test draft_waits_while_a_pass_is_open_so_files_cannot_overlap ... ok
test eight_claim_runs_leave_one_claim ... FAILED
test face_writes_follow_roles ... ok
test grant_ref_must_be_nonblank ... ok
test close_escapes_forged_record_fields_and_the_signer_refusal ... ok
test close_passed_refuses_face_01_change_after_signoff_even_with_a_stored_note ... ok
test first_claim_wins_and_only_holder_returns ... ok
test halt_and_resume_need_prime_or_person_and_a_note_with_ref ... ok
test halt_note_refuses_a_newline ... ok
test help_lists_overlap_ok_and_check_flags ... ok
test init_page_address_accepts_a_work_page ... ok
test init_page_address_refuses_each_rule ... ok
test halted_refusal_escapes_forged_halt_name_and_note ... ok
test job_agents_template_has_clean_and_touch ... ok
test close_passed_reruns_signoff_refusals ... ok
test init_page_address_system_records_the_ref_and_the_page_still_reads ... ok
test log_append_source_writes_one_record_and_syncs_new_dir ... ok
test init_page_address_system_without_a_ref_is_refused ... ok
test hand_edited_face_is_refused_then_reprinted ... ok
test full_pass_closes_with_a_record ... ok
test last_line_tamper_shows_in_the_stamp ... FAILED
test log_tamper_is_detected ... ok
test halted_page_shows_in_status_and_stops_draft_pack_claim ... ok
test log_without_trailing_newline_is_named_and_left_alone ... ok
test failed_check_twice_goes_up_and_blocks_passed_signoff ... ok
test job_box_names_axioms_in_the_kit_folder ... ok
test draft_is_refused_while_an_earlier_pass_is_not_closed ... ok
test may_touch_outside_grant_is_refused ... ok
test observe_escapes_a_forged_prime_and_elevation_target ... ok
test observe_escapes_a_forged_job_key_in_the_same_blocker_line ... ok
test new_pack_records_template_version_4 ... ok
test observe_escapes_forged_close_outcomes_in_the_loop_line ... ok
test only_prime_drafts_and_packs ... ok
test halt_is_refused_while_a_pass_is_open ... ok
test draft_overlap_ok_lets_prime_draft_while_a_pass_is_open ... ok
test overlap_ok_error_for_pass_100_does_not_print_05_100 ... ok
test observer_reports_and_files_but_prime_cannot ... ok
test need_item_goes_up_to_prime_and_prime_answers ... ok
test page_needs_its_person_to_start_it ... ok
test pack_prints_prompt_and_pins_axioms_and_design ... FAILED
test non_prime_cannot_sign_off_and_close_needs_signoff ... ok
test past_packed_pages_still_verify ... ok
test pack_reads_inline_done_when_from_real_face_01 ... ok
test pack_warns_on_stderr_when_face_01_has_no_done_when ... ok
test pass_100_is_not_printed_as_05_100 ... ok
test out_of_frame_return_is_refused_and_recorded ... ok
test pass_numbers_outside_01_98_are_refused_not_wrapped ... ok
test pack_refuses_overlapping_may_touch ... ok
test pack_allows_overlap_with_flag ... ok
test planted_file_names_are_escaped_in_views ... FAILED
test recheck_only_after_a_failed_check_and_resignoff_still_loads ... ok
test plus_one_is_not_read_as_pass_1 ... ok
test pack_allows_overlap_after_other_closes ... ok
test read_only_commands_run_while_a_lock_file_exists ... ok
test refused_append_says_nothing_was_written_and_why ... ok
test reprint_failure_when_temp_path_is_a_directory_says_logged_as ... ok
test planted_return_job_line_is_escaped_on_status_observe_and_views ... ok
test overlap_ok_needs_why_and_set_prime_needs_ref ... ok
test overlap_ok_refuses_a_pass_that_is_not_open ... ok
test printed_fields_refuse_every_unsafe_char_class ... ok
test return_and_check_commits_must_be_40_or_64_hex ... ok
test return_accepts_git_paths_with_spaces_tabs_newlines_and_non_ascii ... FAILED
test return_refusals_escape_forged_pack_branch_and_file ... ok
test role_refusals_escape_a_forged_prime_and_person ... ok
test prime_change_is_kept_and_old_prime_cannot_sign ... ok
test signoff_outcome_must_be_one_wf_accepts ... ok
test signed_off_refusal_escapes_log_text ... ok
test pin_text_in_pack_is_05_01 ... ok
test return_escapes_a_hostile_commit_in_its_error ... ok
test return_refusal_escapes_a_forged_job_key ... ok
test status_escapes_a_forged_signer_name ... ok
test return_with_missing_parts_is_refused ... ok
test return_refuses_a_rename_out_of_scope ... ok
test stripped_hashes_with_a_rechained_log_stay_invalid_after_fix ... FAILED
test return_keeps_git_letters_and_prints_them_as_evidence ... ok
test t373u_changed_template_with_fix_is_refused ... ok
test stale_pin_is_refused_until_redrafted ... ok
test t373u_hand_edited_agents_md_is_invalid ... ok
test t373u_old_page_without_a_hash_still_verifies ... ok
test sha256_repo_runs_a_full_pass_and_loads ... ok
test t379u_edited_link_target_is_invalid ... FAILED
test t379u_forged_link_is_escaped_and_refused ... ok
test t379u_missing_link_target_is_invalid ... ok
test t379u_valid_links_pass ... ok
test write_atomic_source_opens_temp_with_create_new ... ok
test torn_last_log_line_is_named_and_left_alone ... ok
test t381u_lock_shows_in_status_and_observe_still_runs ... ok
test signoff_passed_refuses_unfinished_jobs_until_named ... ok
test t401u_pack_on_the_shared_branch_prints_one_builder_prompt ... ok
test write_commands_on_forged_logs_refuse_without_a_panic ... ok
test signoff_passed_refuses_unanswered_person_elevation_and_drift ... ok
test t381u_rule_file_changed_mid_pass_locks_the_pass ... ok
test wrong_order_entries_make_the_page_unreadable ... FAILED
test t378u_hand_edit_of_a_reused_agents_md_is_invalid ... ok
test t378u_changed_agents_text_prints_a_new_hashed_file ... ok
test draft_refuses_a_99th_pass ... FAILED
test t378u_unchanged_agents_md_is_reused ... ok
test t381u_rule_file_change_is_history_for_a_closed_pass_and_the_next_pass_records_it ... ok
failures:

failures:
    board_escapes_hostile_log_text_everywhere
    board_marks_a_check_on_another_commit_and_an_old_signoff
    board_marks_a_waiting_pass_and_drift_as_stale
    book_board_lists_pages_and_shows_an_unreadable_one
    check_after_a_signoff_says_signed_off_and_next_close
    check_commands_run_without_holding_the_page_lock
    check_escapes_ansi_cursor_codes_so_a_fail_cannot_repaint_the_screen
    check_refuses_if_another_check_is_filed_first
    check_report_includes_drift_that_happens_during_the_check
    check_stores_at_most_last_40_lines_of_output
    draft_refuses_a_99th_pass
    eight_claim_runs_leave_one_claim
    entry_for_a_missing_pass_is_unreadable_not_a_panic
    last_line_tamper_shows_in_the_stamp
    pack_prints_prompt_and_pins_axioms_and_design
    planted_file_names_are_escaped_in_views
    return_accepts_git_paths_with_spaces_tabs_newlines_and_non_ascii
    stripped_hashes_with_a_rechained_log_stay_invalid_after_fix
    t379u_edited_link_target_is_invalid
    wrong_order_entries_make_the_page_unreadable

test result: FAILED. 113 passed; 20 failed; 0 ignored; 0 measured; 0 filtered out; finished in 28.23s
error: test failed, to rerun pass `--test wf`
running 0 tests
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
error: 2 targets failed:
    `--test page_0407`
    `--test wf`
EXIT 101 cargo test --no-fail-fast
START 2026-11-25T21:49:29.825193+00:00
END 2026-11-25T21:50:19.900787+00:00
MS 50075
```
