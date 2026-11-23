WORKSHOP PACK 90.50.10.0703.05.02
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0703 (seq storage lab: how .seq pages are stored)
prime:       prima
predecessor: 05.01
repo:        work
start:       86770ec221da36d3edaed3d1399459b555a86fa3
branch:      returns
return file: .workshop/returns/90.50.10.0703.05.02.md
grant:       labs/0703/ (t452u)
axioms:      1.7.8
outcome:     the storage bench supports its pick, and labs/0703/LESSONS.md lists the lessons
overview:    Builder: Codex. Checker: Claude. Pass 05.01 closed failed. Claude's cross-check (signoff entry 10) said the pick is not supported. Start is returns 86770ec221da36d3edaed3d1399459b555a86fa3. Template 4. Grant is already labs/0703/. Cite SEQ-FILE-PLAN.md:246 and :251, and R37 at DIRECTOR-RULINGS.md:192, on prima/build. Do not write docs/lessons/ (outside the grant). The lessons file feeds that folder later (t506u). The pass 1 table said the chain failed at the next record, 91.07.03.0502, after an edit to a middle page. If cheap, name the edited record, and keep sample titles free of spaces (seqAddr.md:281). Check commands have no spaces inside a pattern.
jobs:
  w01: Make write durability equal. Fsync the log, or compare git, the log and SQLite at the same durability, and say which in the results table.
  w02: Use the same tamper attack and the same outside reference for every store. Include a rewrite-and-rehash attack on the log, and an attack on Git's .git history.
  w03: Add an update workload. A page gets a second version. read_one returns the latest.
  w04: Add tests for a truncated tail and for a removed middle record.
  w05: Weigh Git's commit chain as an append-only option, or state a reason it loses.
  w06: Name the conflict with SEQ-FILE-PLAN.md:246 and :251 (stored form is a folder per page and a file per face) and say what this result means for that plan.
  w07: Cite R37 by file:line. It is DIRECTOR-RULINGS.md:192 on prima/build.
  w08: Write labs/0703/LESSONS.md. A short list of lessons so far: what went wrong, why, and what to do next time. Each item cites a file:line or a commit (t506u). If cheap, fix sample titles that contain spaces (seqAddr.md:281) and make the tamper error name the edited record, not the next one.
may touch:   labs/0703/
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --manifest-path labs/0703/Cargo.toml; git ls-files --error-unmatch labs/0703/LAB-0703-SEQ-STORAGE.md; git ls-files --error-unmatch labs/0703/LESSONS.md   (one command each, split by ;)
done when:   Done when: writes have equal durability (fsync the log, or compare all three at the same durability) and the table says so.
Done when: every store gets the same tamper attack and the same outside reference, including a rewrite-and-rehash attack on the log and an attack on Git's .git history.
Done when: an update workload gives a page a second version, and read_one returns the latest.
Done when: tests cover a truncated tail and a removed middle record.
Done when: Git's commit chain is weighed as an append-only option, or the report states a reason it loses.
Done when: the report names the conflict with SEQ-FILE-PLAN.md:246 and :251 (folder per page, file per face) and says what the result means for it.
Done when: R37 is cited by file:line (DIRECTOR-RULINGS.md:192).
Done when: labs/0703/LESSONS.md is a short list of lessons learned so far (what went wrong, why, what to do next time), each with a file:line or commit cite (t506u). Claude checks it in the cross-check. It feeds docs/lessons/ later.
stop if:     another file must change, including docs/lessons/ or src/. A check command has a space inside a quoted pattern. The table still compares stores at different durability without saying so. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 12, hash ab45d867f8b3
  last closed 05: 05.01 closed at entry 11
sources:
  face 01:        v2 entry 13 hash e6c53ee26e58
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
