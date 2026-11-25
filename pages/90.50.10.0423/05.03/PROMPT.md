=== WORKSHOP JOB 90.50.10.0423.05.03 ===
Pack hash: a478641bcd2c22e7b7fe4e71cd5be868df93cb464f41e67f0fb43225dbe69200 (log entry 27, 2026-11-25T20:10:14Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0423 03 --as <your-name>
Repo: work   Branch: pass/90.50.10.0423.05.03   Start: 4203dc0f813570ae0030b93c1f64edf516d2a604
Read first: pages/90.50.10.0423/05.03/AGENTS.md (sha256 e30cc84722d2), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: Make the older test helpers take the live lock, so the 131 tests stopped by 0423 run again, without weakening live enforcement.
Builder: Grok-2. Checker: Grok-Check.
Done when: The writers in tests/common/mod.rs (Env::ready, Env::draft, Env::open, Env::checked, Env::close_one and any other helper that writes) take the matching lockout through the real wf commands before each write and release it after, the way a real worker does.
Done when: cargo test --test wf, cargo test --test page_0408 and cargo test --test lab_0404 pass. No test is deleted, skipped or ignored, and each test keeps its original assertion.
Done when: cargo test --lib and cargo test --test page_0423 still pass. No src/ file changes.
Done when: cargo test --no-fail-fast for the whole suite is pasted in proof, and any remaining failure is named with its file and cause.
The 0426 golden refresh and the 0424 repack follow this pass.

Jobs:
  w01: In tests/common/mod.rs, make every helper that writes (Env::ready, Env::draft, Env::draft_jobs, Env::open, Env::checked, Env::close_one and any other) take the matching lockout with the real wf command before its writes and release it after, using the right actor and face. Keep each helper's name, arguments and end state the same for its callers, so a test that calls it sees the page in the same state as before 0423.
  w02: Run cargo test --test wf, --test page_0408 and --test lab_0404. Where a test still writes directly without a lock, add the matching lockout and release in that test only. Do not delete, skip or ignore a test. Do not weaken or remove an assertion. If a test's assertion is now wrong because of the 0423 rule itself, stop and name it with the line; do not change the assertion.
  w03: Show the live rule still holds: a write with no lock is still refused (tests/page_0423.rs keeps passing, and at least one tests/wf.rs case that expects a refusal still gets it).
  w04: In proof:, paste every "test result" line from cargo test --no-fail-fast for the whole suite, plus the five packed checks. Name any remaining failure with its file, test name and cause, separately from the packed verdict.
May touch: tests/common/mod.rs, tests/wf.rs, tests/page_0408.rs, tests/lab_0404.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test wf; cargo test --test page_0408; cargo test --test lab_0404; cargo test --test page_0423
Done when (face 01): Done when: The writers in tests/common/mod.rs (Env::ready, Env::draft, Env::open, Env::checked, Env::close_one and any other helper that writes) take the matching lockout through the real wf commands before each write and release it after, the way a real worker does.
Done when: cargo test --test wf, cargo test --test page_0408 and cargo test --test lab_0404 pass. No test is deleted, skipped or ignored, and each test keeps its original assertion.
Done when: cargo test --lib and cargo test --test page_0423 still pass. No src/ file changes.
Done when: cargo test --no-fail-fast for the whole suite is pasted in proof, and any remaining failure is named with its file and cause.
Stop if: the fix needs a src/ file or any path outside may touch (the return check refuses it); a test can only pass by deleting, skipping or weakening it; a helper would need to bypass or fake the lock; tests/page_0407.rs or another ungranted test still fails after the helper fix (name it, do not edit it); a rule above reads two ways. The checks only prove the suites pass; the checker judges that each helper takes the real lock, that no assertion was weakened, and that live enforcement is unchanged. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0423/05.03/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0423.05.03.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0423 03 --branch pass/90.50.10.0423.05.03 --commit <sha> --file .workshop/returns/90.50.10.0423.05.03.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
