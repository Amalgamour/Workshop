# Return 90.50.00.0001.05.01
pack: d8f9c8b3759ff1b4c4fcf916bd6fa3fe3e079a004512e0e5c236d079a72211d1
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - in templates/v3/builder.txt, write wf.exe wherever the builder is told to run wf (the claim line, the return line, and the two "wf return ... --push" mentions). Leave "cargo install ... wf" as is: there wf names the crate.
w02: <done | need | blocked> - in tests/wf.rs, update t401u_pack_on_the_shared_branch_prints_one_builder_prompt to expect "wf.exe claim 1.2.3.4 01" and "wf.exe return 1.2.3.4 01"
proof: <commits, tests run and what they showed>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
