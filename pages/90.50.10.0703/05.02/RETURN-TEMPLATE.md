# Return 90.50.10.0703.05.02
pack: 0defb2bef51bdaee7ffe4f0a768c8353c3fc7d64c78140391663d121ed964a45
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - Make write durability equal. Fsync the log, or compare git, the log and SQLite at the same durability, and say which in the results table.
w02: <done | need | blocked> - Use the same tamper attack and the same outside reference for every store. Include a rewrite-and-rehash attack on the log, and an attack on Git's .git history.
w03: <done | need | blocked> - Add an update workload. A page gets a second version. read_one returns the latest.
w04: <done | need | blocked> - Add tests for a truncated tail and for a removed middle record.
w05: <done | need | blocked> - Weigh Git's commit chain as an append-only option, or state a reason it loses.
w06: <done | need | blocked> - Name the conflict with SEQ-FILE-PLAN.md:246 and :251 (stored form is a folder per page and a file per face) and say what this result means for that plan.
w07: <done | need | blocked> - Cite R37 by file:line. It is DIRECTOR-RULINGS.md:192 on prima/build.
w08: <done | need | blocked> - Write labs/0703/LESSONS.md. A short list of lessons so far: what went wrong, why, and what to do next time. Each item cites a file:line or a commit (t506u). If cheap, fix sample titles that contain spaces (seqAddr.md:281) and make the tamper error name the edited record, not the next one.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
