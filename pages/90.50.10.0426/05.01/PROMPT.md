=== WORKSHOP JOB 90.50.10.0426.05.01 ===
Pack hash: a816a1e061d32592aafddbce221cb76f7085a491977f2a99e161999d45eee090 (log entry 8, 2026-11-23T20:39:22Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0426 01 --as <your-name>
Repo: work   Branch: returns   Start: bcf0680e8ceb4240d17a15f70360ca5f4f840e26
Read first: pages/90.50.10.0426/05.01/AGENTS.md (sha256 9ad56133b40a), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: split wf into a stable kernel and command groups, with no behaviour change. The kernel is the router, Args and the page lock in src/lib.rs; the shared helpers in src/cmd/mod.rs; the page frame in src/page.rs; and the kind list in src/page/rules/mod.rs. Every page pulls from it and it rarely changes, so forks of work can run in parallel (Matthew t565s2260). Band door: 90.50.10.0400. Acting lead and Prime: Claude (t562u).
Current pass: 05.01, the proof test, drafted beside the live kernel (t570u). Pack text: labs/0426-plan/PACK-0426-05.01.txt on returns. 05.02 (the move) waits for 0423 to close.
Builder: Grok-3 (Matthew's PC, D:\Git\grok3). Checker: Grok-Check.
Lab: no lab trial for this pass; the test is the proof that 05.02 uses.
Done when: tests/page_0426.rs runs wf only as a built binary and touches no src/ code.
Done when: it compares wf help and a full page loop's command output, exit codes, log and views against a golden copy inside the test file, between // GOLDEN BEGIN and // GOLDEN END.
Done when: the normaliser removes only times, hex hashes and commit ids, the temp root and path separators, and its own unit test shows two runs give the same output.
Done when: the ignored test regenerate_golden rewrites only the golden region, and a second run leaves the file unchanged.
Done when: a negative test shows that a one-word change in the loop makes the comparison fail.
Done when: cargo test --lib and cargo test --test page_0426 pass on the box, on today's layout.

Jobs:
  w01: A full page loop, run by the test with the built binary in a temp run folder with a local bare remote: init-page, set-prime, face-write 01, 04 (goals) and 08, face-write 06 note, draft, pack, claim, a builder commit inside the grant, return, check by a second actor, signoff, close, verify, status and board. Capture every command's stdout, stderr and exit code, the final log.jsonl, and every view file under the page folder. If a step needs something wf does not have at your start commit, leave that step out and name it in the return.
  w02: Normalise the capture, and only this: ISO times and the time_s numbers become <time>; 64-hex and 40-hex values and any 12-hex prefix printed after "hash", "head", "commit" or "start" become <hex>; the temp folder path becomes <root>; Windows backslashes in paths under <root> become /. Nothing else changes. Write the normaliser as one small function with its own unit test, which shows that two runs of the loop give identical normalised output.
  w03: Keep the golden copy inside tests/page_0426.rs, between the lines // GOLDEN BEGIN and // GOLDEN END, as one raw string per capture (wf help, each command's output and exit code, the log, and each view). The main test fails if anything differs, and prints the first differing capture and line.
  w04: Add an ignored test, regenerate_golden, run with cargo test --test page_0426 -- --ignored regenerate_golden. It runs the loop and wf help, and rewrites only the text between the GOLDEN markers in tests/page_0426.rs. Running it twice in a row leaves the file unchanged. 05.02 runs it at its own start commit, before it moves any code.
  w05: Add one negative test: a copy of the loop with one deliberate difference (for example a face 01 text one word longer) must make the comparison fail. This shows the test can fail.
  w06: In proof:, paste cargo test --test page_0426 (all pass), the regenerate run twice with git diff showing no change the second time, and cargo test --lib.
May touch: tests/page_0426.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test page_0426
Done when (face 01): Done when: tests/page_0426.rs runs wf only as a built binary and touches no src/ code.
Done when: it compares wf help and a full page loop's command output, exit codes, log and views against a golden copy inside the test file, between // GOLDEN BEGIN and // GOLDEN END.
Done when: the normaliser removes only times, hex hashes and commit ids, the temp root and path separators, and its own unit test shows two runs give the same output.
Done when: the ignored test regenerate_golden rewrites only the golden region, and a second run leaves the file unchanged.
Done when: a negative test shows that a one-word change in the loop makes the comparison fail.
Done when: cargo test --lib and cargo test --test page_0426 pass on the box, on today's layout.
Stop if: you would change any file outside may touch (the return check refuses it); the test needs a src/ change or a change to tests/common (stop and raise it); a loop step behaves differently between two runs for a reason other than time, hashes or paths (stop and raise it, it is a finding); a rule above reads two ways; Matthew's direction would leave the grant (stop and raise it). The checks only prove the test compiles and passes; the checker judges whether the golden really pins the outside behaviour, whether the normaliser hides anything it should not, and whether the negative test fails for the right reason (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0426/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0426.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0426 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0426.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
