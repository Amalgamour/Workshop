# Return 90.50.10.0423.05.03
pack: a478641bcd2c22e7b7fe4e71cd5be868df93cb464f41e67f0fb43225dbe69200
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - In tests/common/mod.rs, make every helper that writes (Env::ready, Env::draft, Env::draft_jobs, Env::open, Env::checked, Env::close_one and any other) take the matching lockout with the real wf command before its writes and release it after, using the right actor and face. Keep each helper's name, arguments and end state the same for its callers, so a test that calls it sees the page in the same state as before 0423.
w02: <done | need | blocked> - Run cargo test --test wf, --test page_0408 and --test lab_0404. Where a test still writes directly without a lock, add the matching lockout and release in that test only. Do not delete, skip or ignore a test. Do not weaken or remove an assertion. If a test's assertion is now wrong because of the 0423 rule itself, stop and name it with the line; do not change the assertion.
w03: <done | need | blocked> - Show the live rule still holds: a write with no lock is still refused (tests/page_0423.rs keeps passing, and at least one tests/wf.rs case that expects a refusal still gets it).
w04: <done | need | blocked> - In proof:, paste every "test result" line from cargo test --no-fail-fast for the whole suite, plus the five packed checks. Name any remaining failure with its file, test name and cause, separately from the packed verdict.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
