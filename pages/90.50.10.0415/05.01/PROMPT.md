=== WORKSHOP JOB 90.50.10.0415.05.01 ===
Pack hash: f488ad74fcf2f79d8316176fc10b9cd1fc3e6eb49b2bc1974faead402c62f11c (log entry 6, 2026-11-19T20:27:24Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0415 01 --as <your-name>
Repo: work   Branch: returns   Start: 3646e3448985d1cf40da82b262cfd8852ae59234
Read first: pages/90.50.10.0415/05.01/AGENTS.md (sha256 48c8d63a9d38), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: when wf creates a page log, syncing that folder must succeed on Windows. On Linux, that same step must still fsync the folder (side label: fsync means the folder entry is forced to disk, not only the file). Band door: 90.50.10.0400.
Lab: 90.50.10.0701 (wf loop lab); trial file tests/lab_0415.rs.
Why: 0701 pass 1 left this blocked (returns e30050dc, job w02). On Windows, 123 of the wf end-to-end tests fail with "cannot sync" and "Access is denied (os error 5)" from src/log.rs sync_dir. Opening a folder with File::open is refused on Windows (src/log.rs:122-127 at e30050dc). Builders run in PowerShell (DIRECTOR-WORDS-t399u-t400u.md:7).
Done when: the wf e2e suite passes on Windows (cargo test --test wf; no failure that says cannot sync or Access is denied (os error 5)).
Done when: Linux still fsyncs the directory (the Unix branch of sync_dir still opens the folder and calls sync_all; that call is not removed and not skipped).
Done when: cargo test --lib passes on Windows, including the test that creates a log and checks the folder is synced once.
Done when: the lab trial tests/lab_0415.rs fails on start commit 3646e344 and passes on this return.

Jobs:
  w01: Change only sync_dir in src/log.rs (lines 122-127 at e30050dc, same bytes at 3646e344). Keep the test counter where it is, before the open, so both platforms still count the call. Unix: fs::File::open on the directory, then sync_all, same error text "cannot sync". Windows: OpenOptions custom_flags FILE_FLAG_BACKUP_SEMANTICS (0x02000000), then sync_all, same error text if it fails. Do not call fs::File::open on the Windows path. Do not return Ok without syncing. Keep the append call (lines 104-109) so it still runs only when the log file is created.
  w02: In the existing test module in src/log.rs, keep append_syncs_the_page_folder_when_it_creates_the_log: one sync when the log is created, and no second sync on the next append (lines 201-210). Add one test that reads this same file and checks two things: the Unix branch of sync_dir still calls sync_all, and the Windows branch does not call fs::File::open and does call sync_all. That test runs under cargo test --lib on Windows, so a Windows checker can see the Linux fsync was not removed. Add no trial file.
May touch: src/log.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test wf
Done when (face 01): Done when: the wf e2e suite passes on Windows (cargo test --test wf; no failure that says cannot sync or Access is denied (os error 5)).
Done when: Linux still fsyncs the directory (the Unix branch of sync_dir still opens the folder and calls sync_all; that call is not removed and not skipped).
Done when: cargo test --lib passes on Windows, including the test that creates a log and checks the folder is synced once.
Done when: the lab trial tests/lab_0415.rs fails on start commit 3646e344 and passes on this return.
Stop if: another file must change, including Cargo.toml or tests/wf.rs or tests/common/mod.rs. The Windows open or sync_all still returns an error: stop and quote it, do not hide it. The only way to pass would be to skip the folder sync on Windows. A rule above reads two ways. The append body would no longer contain sync_dir or parent(). (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0415/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0415.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0415 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0415.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
