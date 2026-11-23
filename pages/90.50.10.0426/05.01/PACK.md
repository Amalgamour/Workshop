WORKSHOP PACK 90.50.10.0426.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0426 (split-commands)
prime:       Claude
predecessor: none
repo:        work
start:       bcf0680e8ceb4240d17a15f70360ca5f4f840e26
branch:      returns
return file: .workshop/returns/90.50.10.0426.05.01.md
grant:       src/cmd.rs, src/cmd/, src/lib.rs, src/page.rs, src/page/, tests/page_0426.rs (t565s2260)
axioms:      6.7.9
outcome:     tests/page_0426.rs pins wf's outside behaviour so that the 0426.05.02 move can be proved unchanged; it runs wf as a binary only, never calls src/ code, and passes on today's layout; it compares wf help and a full page loop's log and views against a golden copy kept inside the test file, after a normalisation that removes only times, hashes, commit ids and temp paths; an ignored test regenerates the golden from whatever wf is built, so 05.02 can refresh it at its own start commit before moving any code
overview:    Builder: Grok-3 (Matthew's PC, D:\Git\grok3). Checker: Grok-Check (wf check --as Grok-Check). Lead: Claude (acting lead, t562u), who reviews for Matthew. Page 90.50.10.0426, title split-commands, pass 05.01 of two (plan: labs/0426-plan/README.md on returns). Why: Matthew t565s2260 (stable kernel split) and t570u (draft 0426 beside the live kernel: write the proof test now, in a free file, so the move itself is quick and checkable). 05.02 is the move and waits for 0423 to close. This pass touches no src/ file. The test calls the built wf binary (env!("CARGO_BIN_EXE_wf") or the way tests/wf.rs and tests/common/mod.rs already do), so it keeps working when the code moves between files. You may use tests/common, but do not change it. Windows is the box: no std::os::unix, no sh, and no check command that is only true, grep or test. Use local bare git remotes in a temp folder, never the network. Build into your own CARGO_TARGET_DIR, never into the pinned wf-bin. Until 0422.05.03's trial passes, also push your report with docs/plan/REPORTS.md (kind build). If wf fails, follow docs/plan/MANUAL-RETURN.md. This pack is template 4, so the return must fill the design review line.
jobs:
  w01: A full page loop, run by the test with the built binary in a temp run folder with a local bare remote: init-page, set-prime, face-write 01, 04 (goals) and 08, face-write 06 note, draft, pack, claim, a builder commit inside the grant, return, check by a second actor, signoff, close, verify, status and board. Capture every command's stdout, stderr and exit code, the final log.jsonl, and every view file under the page folder. If a step needs something wf does not have at your start commit, leave that step out and name it in the return.
  w02: Normalise the capture, and only this: ISO times and the time_s numbers become <time>; 64-hex and 40-hex values and any 12-hex prefix printed after "hash", "head", "commit" or "start" become <hex>; the temp folder path becomes <root>; Windows backslashes in paths under <root> become /. Nothing else changes. Write the normaliser as one small function with its own unit test, which shows that two runs of the loop give identical normalised output.
  w03: Keep the golden copy inside tests/page_0426.rs, between the lines // GOLDEN BEGIN and // GOLDEN END, as one raw string per capture (wf help, each command's output and exit code, the log, and each view). The main test fails if anything differs, and prints the first differing capture and line.
  w04: Add an ignored test, regenerate_golden, run with cargo test --test page_0426 -- --ignored regenerate_golden. It runs the loop and wf help, and rewrites only the text between the GOLDEN markers in tests/page_0426.rs. Running it twice in a row leaves the file unchanged. 05.02 runs it at its own start commit, before it moves any code.
  w05: Add one negative test: a copy of the loop with one deliberate difference (for example a face 01 text one word longer) must make the comparison fail. This shows the test can fail.
  w06: In proof:, paste cargo test --test page_0426 (all pass), the regenerate run twice with git diff showing no change the second time, and cargo test --lib.
may touch:   tests/page_0426.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib; cargo test --test page_0426   (one command each, split by ;)
done when:   Done when: tests/page_0426.rs runs wf only as a built binary and touches no src/ code.
Done when: it compares wf help and a full page loop's command output, exit codes, log and views against a golden copy inside the test file, between // GOLDEN BEGIN and // GOLDEN END.
Done when: the normaliser removes only times, hex hashes and commit ids, the temp root and path separators, and its own unit test shows two runs give the same output.
Done when: the ignored test regenerate_golden rewrites only the golden region, and a second run leaves the file unchanged.
Done when: a negative test shows that a one-word change in the loop makes the comparison fail.
Done when: cargo test --lib and cargo test --test page_0426 pass on the box, on today's layout.
stop if:     you would change any file outside may touch (the return check refuses it); the test needs a src/ change or a change to tests/common (stop and raise it); a loop step behaves differently between two runs for a reason other than time, hashes or paths (stop and raise it, it is a finding); a rule above reads two ways; Matthew's direction would leave the grant (stop and raise it). The checks only prove the test compiles and passes; the checker judges whether the golden really pins the outside behaviour, whether the normaliser hides anything it should not, and whether the negative test fails for the right reason
pins (Prime read these before drafting; checked again at release):
  face 04:        entry 4, hash 6d30051239ef
  face 06:        entry 6, hash 54ee9f4cb836
  last closed 05: none
sources:
  face 01:        v2 entry 5 hash d0e93610d07c
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
