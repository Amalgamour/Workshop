WORKSHOP PACK 90.50.10.0415.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0415 (a new log folder syncs on Windows)
prime:       prima
predecessor: 90.50.10.0701.05.01
repo:        work
start:       3646e3448985d1cf40da82b262cfd8852ae59234
branch:      returns
return file: .workshop/returns/90.50.10.0415.05.01.md
grant:       src/log.rs (t461u)
axioms:      1.7.8,2.6.9
outcome:     creating a page log succeeds on Windows, and on Linux the new log's folder is still fsynced
overview:    Job left blocked by 90.50.10.0701.05.01 (returns e30050dc, file .workshop/returns/90.50.10.0701.05.01.md, w02 blocked). On Windows, 123 wf end-to-end tests fail. Each one says it cannot sync the page folder, Access is denied (os error 5), from src/log.rs sync_dir. fs::File::open on a directory is refused on Windows (src/log.rs:122-127 at e30050dc). src/log.rs is the same at start 3646e344 (that commit adds only the 0701 log).
Lab is 90.50.10.0701. Trial file tests/lab_0415.rs is written by another view after this return (t425u, DIRECTOR-WORDS-t425u.md:3). This page writes no trial file and copies no harness. Unit tests already inside src/log.rs stay in that file (stage plan 12.5).
Why the folder sync exists: append syncs the new log file, then syncs the parent folder, and only when the log file was just created (src/log.rs:104-109). On Linux that second step is fsync of the directory, so a crash cannot lose the new file's name. Builders run in PowerShell (DIRECTOR-WORDS-t399u-t400u.md:7).
Unix keeps fs::File::open plus sync_all. That is the Linux fsync. Do not remove it and do not skip it. The Rust switch is cfg(unix), which is how the code names Linux. Windows is cfg(windows).
Windows cannot use fs::File::open here. Open the directory with std::os::windows::fs::OpenOptionsExt::custom_flags and FILE_FLAG_BACKUP_SEMANTICS (value 0x02000000), then sync_all. No new crate. No Cargo.toml change. If that open or the sync_all still returns an error, stop and quote the error. Do not return Ok and skip the sync.
Leave the call in append. tests/wf.rs lines 789-798 (outside may touch) require the append body to contain the text sync_dir or parent(). Moving the call out of append fails that test.
A target that is neither unix nor windows must fail the build with a clear message. It must not skip the sync.
This pass is on template 3, so wf will not ask the return for a design review line. Add one by hand in noticed, starting "design review:", naming the kit docs/AXIOMS.md and docs/DESIGN.md and what was found (t416u, DIRECTOR-WORDS-t416u.md:7; t424, DIRECTOR-WORDS-t424.md:10).
Axioms: 1.7.8 is the cold set before a write (Axioms.md:9). 2 Fractal: keep the Unix sync and write only the Windows difference (Axioms.md:15). 6 Lineage: the job is the blocked w02, not a new idea (Axioms.md:23). 9 Trial: the lab trial is another view (Axioms.md:29).
jobs:
  w01: Change only sync_dir in src/log.rs (lines 122-127 at e30050dc, same bytes at 3646e344). Keep the test counter where it is, before the open, so both platforms still count the call. Unix: fs::File::open on the directory, then sync_all, same error text "cannot sync". Windows: OpenOptions custom_flags FILE_FLAG_BACKUP_SEMANTICS (0x02000000), then sync_all, same error text if it fails. Do not call fs::File::open on the Windows path. Do not return Ok without syncing. Keep the append call (lines 104-109) so it still runs only when the log file is created.
  w02: In the existing test module in src/log.rs, keep append_syncs_the_page_folder_when_it_creates_the_log: one sync when the log is created, and no second sync on the next append (lines 201-210). Add one test that reads this same file and checks two things: the Unix branch of sync_dir still calls sync_all, and the Windows branch does not call fs::File::open and does call sync_all. That test runs under cargo test --lib on Windows, so a Windows checker can see the Linux fsync was not removed. Add no trial file.
may touch:   src/log.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib; cargo test --test wf   (one command each, split by ;)
done when:   Done when: the wf e2e suite passes on Windows (cargo test --test wf; no failure that says cannot sync or Access is denied (os error 5)).
Done when: Linux still fsyncs the directory (the Unix branch of sync_dir still opens the folder and calls sync_all; that call is not removed and not skipped).
Done when: cargo test --lib passes on Windows, including the test that creates a log and checks the folder is synced once.
Done when: the lab trial tests/lab_0415.rs fails on start commit 3646e344 and passes on this return.
stop if:     another file must change, including Cargo.toml or tests/wf.rs or tests/common/mod.rs. The Windows open or sync_all still returns an error: stop and quote it, do not hide it. The only way to pass would be to skip the folder sync on Windows. A rule above reads two ways. The append body would no longer contain sync_dir or parent().
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 4, hash c2e3d81a43c5
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash 07a581e60a26
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
