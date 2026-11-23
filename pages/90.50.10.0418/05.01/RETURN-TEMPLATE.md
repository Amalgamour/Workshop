# Return 90.50.10.0418.05.01
pack: 5f94dd5099e30e7363f9877baadab3e4fc1286be7788eeb7e247f90f46172163
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - In crates/seqaddr-core, apply the seated-05 rule. A body on face 05 with no counter is the seat (plain 05). 05.NN stays a pass. The board of the passes stays 05.00. Face 06 stays counted and is never seated. Change only state.rs, resolve.rs, validate.rs and face.rs, at the cited sites and any other line in those four files the new rule requires.
w02: <done | need | blocked> - Add crates/seqaddr-core/tests/page_0418.rs. Show: a seat at plain 05 is accepted; a pass 05.NN is still a pass; plain 06 is still not a seat; face 06 still has no door of its own. Tests must build on Windows: no std::os::unix. If an existing test file must change, stop and say so; do not edit it.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
