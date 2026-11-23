WORKSHOP PACK 90.50.10.0701.05.03
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0701 (wf loop lab: one harness, every wf trial)
prime:       prima
predecessor: 05.02
repo:        work
start:       a823ee284574be3d9f6247925b9088137a27a539
branch:      returns
return file: .workshop/returns/90.50.10.0701.05.03.md
grant:       tests/ (t432u)
axioms:      1.7.8
outcome:     an outside trial tests/lab_0415.rs passes the 0415 done-when, including a real Windows run
overview:    Builder: Grok-1, on Windows. Wave 3 trial for 90.50.10.0415, lab pass 05.03. Cursor-1 built 0415 and does not write this trial. One file only, beside the 0404 trial (stage plan 12.3). This lab pass starts at a823ee28, where the 0415 return is already in the tree. The trial fails on 3646e344 and passes on this tree. Template 4. The return of this pass fills the design review line. Proof line pastes the Windows cargo test --test lab_0415 output. A Linux run must also pass.
jobs:
  w01: Add tests/lab_0415.rs. It starts with mod common; and holds only 0415's cases. From outside, not from the tests inside src/log.rs: creating a page log succeeds on Windows with no error that says cannot sync or Access is denied (os error 5). On Linux the unix branch of sync_dir still opens the folder and calls sync_all (src/log.rs:125-129 at a823ee28). On Windows the directory is opened with FILE_FLAG_BACKUP_SEMANTICS and then sync_all (src/log.rs:131-141). The test fails on commit 3646e344, where that Windows open is absent, and passes on a823ee28. Do not copy the harness.
may touch:   tests/lab_0415.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --test lab_0415   (one command each, split by ;)
done when:   Done when: the wf e2e suite passes on Windows (cargo test --test wf; no failure that says cannot sync or Access is denied (os error 5)).
Done when: Linux still fsyncs the directory (the Unix branch of sync_dir still opens the folder and calls sync_all; that call is not removed and not skipped).
Done when: cargo test --lib passes on Windows, including the test that creates a log and checks the folder is synced once.
Done when: the lab trial tests/lab_0415.rs fails on start commit 3646e344 and passes on this return.
stop if:     another file must change, including src/log.rs or tests/common/mod.rs or tests/wf.rs. The trial copies the harness. The Windows run is skipped. A Linux run alone is pasted as the proof. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 15, hash 3b1c1ca11cc0
  last closed 05: 05.01 closed at entry 12
sources:
  face 01:        v4 entry 19 hash cdd753af9b46
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
