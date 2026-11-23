# Return 90.50.10.0701.05.02
pack: 0fe67d63e293f6102674cf21a06ba8a9c6be07c310e499ff07bc9ca74783023c
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - Add tests/lab_0404.rs. It starts with mod common; and holds only 0404's cases. From outside, not from the builder's tests: a return on template 4 with no design review line is refused, the refusal names t416u, and it is recorded; a template 4 return with the line filled is accepted; a return for a pack on template 1, 2, or 3 is accepted without that line. cargo test --lib and cargo test --test wf still pass. Do not copy tests/common.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
