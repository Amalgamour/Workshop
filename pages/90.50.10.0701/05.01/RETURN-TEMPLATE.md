# Return 90.50.10.0701.05.01
pack: e6b21e3fde72d10f44d6fa2ed7be3096680535191201af4a63fb3eba082d701b
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - new tests/common/mod.rs. Move into it, do not copy, the shared harness from tests/wf.rs: struct Env, impl Env, impl Drop for Env, seed_closed_passes and closed_chain (tests/wf.rs:10-170 at c09fa60c). tests/wf.rs then starts with `mod common;` and `use common::*;` and keeps only its test cases. No harness line may be left in tests/wf.rs. Mark items `pub` as needed and add `#![allow(dead_code)]` in the module, since each test file uses only part of it.
w02: <done | need | blocked> - make the tests build and run on Windows. Gate unix-only code with #[cfg(unix)] and a one-line comment naming why: the std::os::unix import, the permission tests (set_mode), and the symlink tests. Where a test uses `true`, `grep -q ...` or `test` as a pack check command, change it to a command that runs on both (for example `cargo --version` for an always-pass check), or gate the test with #[cfg(unix)] and say why. List every gated test in the return's proof line.
w03: <done | need | blocked> - in tests/wf.rs add "design review: kit docs compared (test)\n" after the proof line in each of the five hand-written return strings (tests/wf.rs:94, :858, :994, :1575, :1789 at c09fa60c). Add no other tests.
proof: <commits, tests run and what they showed>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
