=== WORKSHOP JOB 90.50.10.0701.05.03 ===
Pack hash: 674d965e08dbb013e4ce8e1e05a3e6d70c74c6a11b80ff4580d8e94b037838dd (log entry 21, 2026-11-23T15:29:33Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0701 03 --as <your-name>
Repo: work   Branch: returns   Start: a823ee284574be3d9f6247925b9088137a27a539
Read first: pages/90.50.10.0701/05.03/AGENTS.md (sha256 d50f26d8cc59), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: lab trial for 90.50.10.0415. Builder: Grok-1. Lab page 90.50.10.0701.
Done when: the wf e2e suite passes on Windows (cargo test --test wf; no failure that says cannot sync or Access is denied (os error 5)).
Done when: Linux still fsyncs the directory (the Unix branch of sync_dir still opens the folder and calls sync_all; that call is not removed and not skipped).
Done when: cargo test --lib passes on Windows, including the test that creates a log and checks the folder is synced once.
Done when: the lab trial tests/lab_0415.rs fails on start commit 3646e344 and passes on this return.

Jobs:
  w01: Add tests/lab_0415.rs. It starts with mod common; and holds only 0415's cases. From outside, not from the tests inside src/log.rs: creating a page log succeeds on Windows with no error that says cannot sync or Access is denied (os error 5). On Linux the unix branch of sync_dir still opens the folder and calls sync_all (src/log.rs:125-129 at a823ee28). On Windows the directory is opened with FILE_FLAG_BACKUP_SEMANTICS and then sync_all (src/log.rs:131-141). The test fails on commit 3646e344, where that Windows open is absent, and passes on a823ee28. Do not copy the harness.
May touch: tests/lab_0415.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --test lab_0415
Done when (face 01): Done when: the wf e2e suite passes on Windows (cargo test --test wf; no failure that says cannot sync or Access is denied (os error 5)).
Done when: Linux still fsyncs the directory (the Unix branch of sync_dir still opens the folder and calls sync_all; that call is not removed and not skipped).
Done when: cargo test --lib passes on Windows, including the test that creates a log and checks the folder is synced once.
Done when: the lab trial tests/lab_0415.rs fails on start commit 3646e344 and passes on this return.
Stop if: another file must change, including src/log.rs or tests/common/mod.rs or tests/wf.rs. The trial copies the harness. The Windows run is skipped. A Linux run alone is pasted as the proof. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0701/05.03/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0701.05.03.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0701 03 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0701.05.03.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
