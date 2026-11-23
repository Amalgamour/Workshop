# Return 90.50.10.0419.05.02
pack: b1882a4544faf8fa7865d570c351f2633df21cd4e049528bf9eb073a8c1e43f6
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - Add tests/lab_0419.rs. It starts with mod common; and holds only 0419's cases. From outside, not from tests/page_0419.rs: the form git grep -q -E [#][#][[:space:]]0[.] -- <file> matches a heading under sh -c (exit 0), the pattern token has no caret, no quotes, no spaces, and does not start with #, and the bare form git grep -q -E ##[[:space:]]0[.] -- <file> exits 128 under sh -c with no pattern given. src/git.rs still documents both forms in the run comment (the [#][#] form, the bare ## form, exit 128, and no pattern given). The test fails on commit a823ee284574be3d9f6247925b9088137a27a539, which has no tests/page_0419.rs, and passes on 710485918b0f7ef90638d8ab57c363ba1f2d0a71 and on this return. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test. Do not copy tests/common. cargo test --lib and cargo test --test page_0419 still pass.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
