# Return 90.50.10.0408.05.01
pack: d9021b979577182fdca33d58bd8cf077630e094ec1750b50ca2a131894d5166a
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - Add wf withdraw <page> <NN>, prime only. It runs only when the pass tail is pack and there is no claim. Append a log entry and set the tail to withdrawn. The pass stays in the log. Refuse it when the tail is open, return, review, or closed. A later claim is refused. withdrawn is not an open tail, so the pass no longer holds its files (src/page.rs:151). Wire the command in src/lib.rs help and dispatch, and in src/cmd.rs.
w02: <done | need | blocked> - Add tests/page_0408.rs. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test (stage plan 11.7). Cover withdraw at pack with no claim, a refusal at open or later, a refused later claim, and the pass still present in the log.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
