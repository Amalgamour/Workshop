=== WORKSHOP JOB 90.50.10.0701.05.01 ===
Pack hash: e6b21e3fde72d10f44d6fa2ed7be3096680535191201af4a63fb3eba082d701b (log entry 6, 2026-11-19T19:22:27Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0701 01 --as <your-name>
Repo: work   Branch: returns   Start: c09fa60c92ac2e4cde39c73a061166ebc2fac0e0
Read first: pages/90.50.10.0701/05.01/AGENTS.md (sha256 66ac07c0ab76), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: the wf loop lab, reusable by every stage. One harness for wf end-to-end trials, kept once in tests/common/mod.rs, and one trial file per page it serves (tests/lab_PPPP.rs), written by another view after that page returns. Pages it serves hold no test code and copy no harness (t425u). Lab band door: 90.50.10.0700 (t432u, t434).
Serves (written on both pages): 90.50.10.0404 tests/lab_0404.rs; 0406 tests/lab_0406.rs; 0407 tests/lab_0407.rs; 0408 tests/lab_0408.rs; 0409 tests/lab_0409.rs; 0411 tests/lab_0411.rs; 0412 tests/lab_0412.rs; 0498 tests/lab_0498.rs. Each page is listed when it is made; later stages' pages are added the same way.
Each trial must fail on the work's start commit and pass on its return, and the harness lives only in tests/common/mod.rs.
Pass 1 done when: cargo test --test wf passes on the box with the harness moved to tests/common/mod.rs and none of it left in tests/wf.rs, and the tests build on Windows with every skip named.

Jobs:
  w01: new tests/common/mod.rs. Move into it, do not copy, the shared harness from tests/wf.rs: struct Env, impl Env, impl Drop for Env, seed_closed_passes and closed_chain (tests/wf.rs:10-170 at c09fa60c). tests/wf.rs then starts with `mod common;` and `use common::*;` and keeps only its test cases. No harness line may be left in tests/wf.rs. Mark items `pub` as needed and add `#![allow(dead_code)]` in the module, since each test file uses only part of it.
  w02: make the tests build and run on Windows. Gate unix-only code with #[cfg(unix)] and a one-line comment naming why: the std::os::unix import, the permission tests (set_mode), and the symlink tests. Where a test uses `true`, `grep -q ...` or `test` as a pack check command, change it to a command that runs on both (for example `cargo --version` for an always-pass check), or gate the test with #[cfg(unix)] and say why. List every gated test in the return's proof line.
  w03: in tests/wf.rs add "design review: kit docs compared (test)\n" after the proof line in each of the five hand-written return strings (tests/wf.rs:94, :858, :994, :1575, :1789 at c09fa60c). Add no other tests.
May touch: tests/common/mod.rs, tests/wf.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --test wf; cargo build --tests
Done when (face 01): done when: cargo test --test wf passes on the box with the harness moved to tests/common/mod.rs and none of it left in tests/wf.rs, and the tests build on Windows with every skip named.
Stop if: another file must change (anything outside may touch is refused by the return check); a test can only pass by changing its meaning; a harness line would be copied, not moved; wf refuses a return with the extra design review line (then end w03 blocked and say so); a rule above reads two ways. Run cargo test on your Windows machine and put what it showed on the proof line; the checker runs cargo test --test wf on the box (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0701/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0701.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0701 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0701.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
