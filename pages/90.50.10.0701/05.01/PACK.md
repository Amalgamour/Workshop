WORKSHOP PACK 90.50.10.0701.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0701 (wf loop lab: one harness, every wf trial)
prime:       prima
predecessor: none
repo:        work
start:       c09fa60c92ac2e4cde39c73a061166ebc2fac0e0
branch:      returns
return file: .workshop/returns/90.50.10.0701.05.01.md
grant:       tests/ (t432u)
axioms:      1.7.8,2.9
outcome:     the test harness lives once, in tests/common/mod.rs, and tests/wf.rs uses it; the tests build and run on Windows, with unix-only tests gated and named; the five hand-written return strings in tests/wf.rs already carry a design review line, ready for 0404
overview:    Lab band 90.50.10.0700-0799, door 90.50.10.0700 (its face 01 lists this lab; t434.md:24). Why: t432.md:16 "We want those labs to be reusable.  So a seperate band for storing them makes sense to me." t425u.md:3 "Correction, each page should be linked to the test lab for it.  We don't need to copy paste lab code a bunch of times.  We'll bloat if we do that." So the harness is moved once, never copied, and every later trial imports it with `mod common;`. Builders work on Windows (t400u.md:7); today tests/wf.rs does not compile there (tests/wf.rs:4 imports std::os::unix; set_mode at :820, :841; symlinks at :954, :959, :1021, :1117, all at c09fa60c). The harness is struct Env and its helpers at tests/wf.rs:10-170 (Env :10-12, impl Env :14-140, Drop :142-146, seed_closed_passes :149-157, closed_chain :160-170). The test helper init_page at tests/wf.rs:3100 is test-case code for the init_page_address tests; it stays in tests/wf.rs. The five return strings at tests/wf.rs:94, :858, :994, :1575 and :1789 get the design review line now so that 0404 (template 4, t416u.md:7) does not break them; wf today reads only the keys it knows (parse_return, src/cmd.rs:467-482). Axioms: 1.7.8 is the cold set before a write (Axioms.md:9); then 2 Fractal (one harness inherited, no copy, Axioms.md:15) and 9 Trial (the lab is where another view tries to break the work, Axioms.md:29). Return: this pass is on template 3, so add by hand in noticed: a line starting "design review:" naming the kit docs/AXIOMS.md and docs/DESIGN.md compared and what was found (t416u gate, t424.md:10).
jobs:
  w01: new tests/common/mod.rs. Move into it, do not copy, the shared harness from tests/wf.rs: struct Env, impl Env, impl Drop for Env, seed_closed_passes and closed_chain (tests/wf.rs:10-170 at c09fa60c). tests/wf.rs then starts with `mod common;` and `use common::*;` and keeps only its test cases. No harness line may be left in tests/wf.rs. Mark items `pub` as needed and add `#![allow(dead_code)]` in the module, since each test file uses only part of it.
  w02: make the tests build and run on Windows. Gate unix-only code with #[cfg(unix)] and a one-line comment naming why: the std::os::unix import, the permission tests (set_mode), and the symlink tests. Where a test uses `true`, `grep -q ...` or `test` as a pack check command, change it to a command that runs on both (for example `cargo --version` for an always-pass check), or gate the test with #[cfg(unix)] and say why. List every gated test in the return's proof line.
  w03: in tests/wf.rs add "design review: kit docs compared (test)\n" after the proof line in each of the five hand-written return strings (tests/wf.rs:94, :858, :994, :1575, :1789 at c09fa60c). Add no other tests.
may touch:   tests/common/mod.rs, tests/wf.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --test wf; cargo build --tests   (one command each, split by ;)
done when:   done when: cargo test --test wf passes on the box with the harness moved to tests/common/mod.rs and none of it left in tests/wf.rs, and the tests build on Windows with every skip named.
stop if:     another file must change (anything outside may touch is refused by the return check); a test can only pass by changing its meaning; a harness line would be copied, not moved; wf refuses a return with the extra design review line (then end w03 blocked and say so); a rule above reads two ways. Run cargo test on your Windows machine and put what it showed on the proof line; the checker runs cargo test --test wf on the box
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 4, hash 882adbc770d3
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash deb27dbbefd8
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
