# Return 90.50.10.0702.05.02
pack: e570e7a6d93e723f074d8473866d9b06c3e5e2d9f177ccfb0f1fd40b8fea86e6
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - Restate the entry-number rule at lab:176 as one booked block and one matching history entry, in book order, with references allowed (seqpage.md:135, :199-201).
w02: <done | need | blocked> - Fix lab:183 so it does not claim body text is never checked. seqpage.md:169 says a prefixed body cannot be mistaken for structure. seqpage.md:186 and crates/seqpage/src/parse.rs:366-370 do check the body's cards.
w03: <done | need | blocked> - Write a value grammar for derived values, including lineage, source, faces and counters. source := uses a full book address.
w04: <done | need | blocked> - In section 5, split superseded text from real open conflicts. Superseded: K2/R26, K4/R9, K5/R10, K7/R28, K9/R35, K10, K11 stale. Do not resolve a conflict that is still open.
w05: <done | need | blocked> - Mark Q2, Q4, Q5, Q6 and Q7 answered, with the ruling or code cite (DIRECTOR-RULINGS.md:37-41, :113-115; state.rs:607-631; derive.rs:119-141, :204-206). Keep only what truly stays open.
w06: <done | need | blocked> - Add coverage for escaped keys (seqpage.md:156), decoded ASCII checks (seqpage.md:44), and the stamp-versus-replay disagreement in examples/real/10.11.21.1001.bob.seq:85-88.
w07: <done | need | blocked> - Write labs/0702/LESSONS.md. A short list of lessons so far: what went wrong, why, and what to do next time. Each item cites a file:line or a commit (t506u).
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
