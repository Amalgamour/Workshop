WORKSHOP PACK 90.50.10.0423.05.03
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0423 (one-worker)
prime:       prima
predecessor: 05.02
repo:        work
start:       4203dc0f813570ae0030b93c1f64edf516d2a604
branch:      pass/90.50.10.0423.05.03
return file: .workshop/returns/90.50.10.0423.05.03.md
grant:       src/cmd.rs, src/page.rs, src/lib.rs, tests/page_0423.rs, tests/common/mod.rs, tests/wf.rs, tests/page_0408.rs, tests/lab_0404.rs (t562u, t584s2361 typed by Prima for Matthew)
axioms:      6.7.9
outcome:     The older test suites run again under the live lock rule. tests/common/mod.rs helpers take and release the matching lockout through the real wf commands, so tests/wf.rs, tests/page_0408.rs and tests/lab_0404.rs pass with their original assertions. No src/ file changes and live enforcement is unchanged.
overview:    Builder: Grok-2. Checker: Grok-Check. Page 90.50.10.0423, pass 05.03. Typed by Prima, t577u, t582u and t584s2361. Why: since 0423.05.02 (bf520780) 131 older tests stop at tests/common/mod.rs:46 with "refused: lockout first" because the helpers write with no lock. Before 0423 (21be13b9) the whole suite passed, 201 tests. Those tests now test nothing. They must run again before the 0426 source move, which compares behaviour against them. Grok-2's 05.02 return named the follow-up scope (tests/common/mod.rs Env::ready, Env::draft, Env::open, Env::checked, Env::close_one; tests/page_0408.rs; tests/wf.rs). Box runs also show lab_0404 (2) and page_0407 (1) failing for the same cause. page_0407 is not granted because 0407.05.01 is open; if it still fails after the helper fix, name it, do not edit it. Use the real wf lockout and release commands in the helpers, the same as a real worker. Build into your own CARGO_TARGET_DIR, never into wf-bin. Windows is the box: no std::os::unix, no sh. Use the pinned a823ee28 wf.exe for the work order. If wf fails, follow docs/plan/MANUAL-RETURN.md. This pack is template 4, so the return must fill the design review line.
jobs:
  w01: In tests/common/mod.rs, make every helper that writes (Env::ready, Env::draft, Env::draft_jobs, Env::open, Env::checked, Env::close_one and any other) take the matching lockout with the real wf command before its writes and release it after, using the right actor and face. Keep each helper's name, arguments and end state the same for its callers, so a test that calls it sees the page in the same state as before 0423.
  w02: Run cargo test --test wf, --test page_0408 and --test lab_0404. Where a test still writes directly without a lock, add the matching lockout and release in that test only. Do not delete, skip or ignore a test. Do not weaken or remove an assertion. If a test's assertion is now wrong because of the 0423 rule itself, stop and name it with the line; do not change the assertion.
  w03: Show the live rule still holds: a write with no lock is still refused (tests/page_0423.rs keeps passing, and at least one tests/wf.rs case that expects a refusal still gets it).
  w04: In proof:, paste every "test result" line from cargo test --no-fail-fast for the whole suite, plus the five packed checks. Name any remaining failure with its file, test name and cause, separately from the packed verdict.
may touch:   tests/common/mod.rs, tests/wf.rs, tests/page_0408.rs, tests/lab_0404.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib; cargo test --test wf; cargo test --test page_0408; cargo test --test lab_0404; cargo test --test page_0423   (one command each, split by ;)
done when:   Done when: The writers in tests/common/mod.rs (Env::ready, Env::draft, Env::open, Env::checked, Env::close_one and any other helper that writes) take the matching lockout through the real wf commands before each write and release it after, the way a real worker does.
Done when: cargo test --test wf, cargo test --test page_0408 and cargo test --test lab_0404 pass. No test is deleted, skipped or ignored, and each test keeps its original assertion.
Done when: cargo test --lib and cargo test --test page_0423 still pass. No src/ file changes.
Done when: cargo test --no-fail-fast for the whole suite is pasted in proof, and any remaining failure is named with its file and cause.
stop if:     the fix needs a src/ file or any path outside may touch (the return check refuses it); a test can only pass by deleting, skipping or weakening it; a helper would need to bypass or fake the lock; tests/page_0407.rs or another ungranted test still fails after the helper fix (name it, do not edit it); a rule above reads two ways. The checks only prove the suites pass; the checker judges that each helper takes the real lock, that no assertion was weakened, and that live enforcement is unchanged.
pins (Prime read these before drafting; checked again at release):
  face 04:        entry 14, hash 6d65da52f668
  face 06:        entry 25, hash e83f7b33c2ec
  last closed 05: 05.02 closed at entry 22
sources:
  face 01:        v3 entry 24 hash 3558be0ad9ce
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
