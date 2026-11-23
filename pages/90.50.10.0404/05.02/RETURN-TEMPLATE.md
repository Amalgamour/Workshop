# Return 90.50.10.0404.05.02
pack: fd3b5963141a2347680e13c3faf4a4d50d65070ce04e55b20db10047c45de46d
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - In tests/wf.rs rename new_pack_records_template_version_3 (line 1327 at 464170c7) to new_pack_records_template_version_4. Change the assertion at line 1332 from templates "3" to templates "4". Change nothing else in that test.
w02: <done | need | blocked> - In stripped_hashes_with_a_rechained_log_stay_invalid_after_fix (line 2802), a fresh pack is now template 4. Change the assertion at line 2840 from templates 3 to templates 4. Leave the loop that patches versions 3 and 2 as it is. Change nothing else.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
