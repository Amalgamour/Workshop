# Return 90.50.10.0701.05.03
pack: 674d965e08dbb013e4ce8e1e05a3e6d70c74c6a11b80ff4580d8e94b037838dd
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - Add tests/lab_0415.rs. It starts with mod common; and holds only 0415's cases. From outside, not from the tests inside src/log.rs: creating a page log succeeds on Windows with no error that says cannot sync or Access is denied (os error 5). On Linux the unix branch of sync_dir still opens the folder and calls sync_all (src/log.rs:125-129 at a823ee28). On Windows the directory is opened with FILE_FLAG_BACKUP_SEMANTICS and then sync_all (src/log.rs:131-141). The test fails on commit 3646e344, where that Windows open is absent, and passes on a823ee28. Do not copy the harness.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
