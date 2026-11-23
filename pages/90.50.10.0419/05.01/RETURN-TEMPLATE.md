# Return 90.50.10.0419.05.01
pack: 3ed7f6c93aad3e7d847f9029b1c77e36c94ca4e2fd9e8e7351665fad0f619e9c
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - In src/git.rs, make check commands safe on Windows and still correct on Linux. A git grep pattern in a check must have no caret, no quotes, and no spaces. Do not leave Linux broken: a bare ## pattern must not be the form packs rely on, because it is a comment under sh -c. If the right fix also needs a pack-time lint, stop and say so (src/cmd.rs is held by 0408).
w02: <done | need | blocked> - Add tests/page_0419.rs. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test (stage plan 11.7). Prove that the form git grep -q -E [#][#][[:space:]]0[.] -- <file> matches a heading under sh -c, and that the bare ## form fails under sh -c with no pattern given. If a test needs Windows cmd /C and this box is Linux, still run the sh -c cases here and state what must be proven on Windows.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
