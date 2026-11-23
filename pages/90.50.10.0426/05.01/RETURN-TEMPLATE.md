# Return 90.50.10.0426.05.01
pack: a816a1e061d32592aafddbce221cb76f7085a491977f2a99e161999d45eee090
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - A full page loop, run by the test with the built binary in a temp run folder with a local bare remote: init-page, set-prime, face-write 01, 04 (goals) and 08, face-write 06 note, draft, pack, claim, a builder commit inside the grant, return, check by a second actor, signoff, close, verify, status and board. Capture every command's stdout, stderr and exit code, the final log.jsonl, and every view file under the page folder. If a step needs something wf does not have at your start commit, leave that step out and name it in the return.
w02: <done | need | blocked> - Normalise the capture, and only this: ISO times and the time_s numbers become <time>; 64-hex and 40-hex values and any 12-hex prefix printed after "hash", "head", "commit" or "start" become <hex>; the temp folder path becomes <root>; Windows backslashes in paths under <root> become /. Nothing else changes. Write the normaliser as one small function with its own unit test, which shows that two runs of the loop give identical normalised output.
w03: <done | need | blocked> - Keep the golden copy inside tests/page_0426.rs, between the lines // GOLDEN BEGIN and // GOLDEN END, as one raw string per capture (wf help, each command's output and exit code, the log, and each view). The main test fails if anything differs, and prints the first differing capture and line.
w04: <done | need | blocked> - Add an ignored test, regenerate_golden, run with cargo test --test page_0426 -- --ignored regenerate_golden. It runs the loop and wf help, and rewrites only the text between the GOLDEN markers in tests/page_0426.rs. Running it twice in a row leaves the file unchanged. 05.02 runs it at its own start commit, before it moves any code.
w05: <done | need | blocked> - Add one negative test: a copy of the loop with one deliberate difference (for example a face 01 text one word longer) must make the comparison fail. This shows the test can fail.
w06: <done | need | blocked> - In proof:, paste cargo test --test page_0426 (all pass), the regenerate run twice with git diff showing no change the second time, and cargo test --lib.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
