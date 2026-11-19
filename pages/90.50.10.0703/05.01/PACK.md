WORKSHOP PACK 90.50.10.0703.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0703 (seq storage lab: how .seq pages are stored)
prime:       prima
predecessor: none
repo:        work
start:       c09fa60c92ac2e4cde39c73a061166ebc2fac0e0
branch:      returns
return file: .workshop/returns/90.50.10.0703.05.01.md
grant:       labs/0703/ (t452u)
axioms:      1.7.8,6.9
outcome:     a throwaway Rust bench in labs/0703/ that stores about 1,000 sample .seq pages three ways (plain text files with git, an append-only hash-chain log, SQLite) and measures each; and labs/0703/LAB-0703-SEQ-STORAGE.md with the results, one pick with reasons, and how to rerun
overview:    Builder: Codex (t439u). Checker: Claude, by hand (wf refuses only the builder as checker, src/cmd.rs:730). Why: t451u (docs/review/DIRECTOR-WORDS-t450-t453u.md:9) "What should be the design for the storage of it." This is a lab in the lab band (door 90.50.10.0700); it serves no page yet. The bench is throwaway: it lives only in labs/0703/, is its own crate (its Cargo.toml has an empty [workspace] table so it never joins the wf crate), and nothing in src/ or tests/ uses it. Sample shape, read only, from the build design: git -C work fetch origin prima/build, then git -C work show 8e96151dbe9ff03a55e6838168033ba6bf5f4a4a:<path> for docs/spec/examples/*.seq (11 files), docs/spec/WRITE-ONCE.md and docs/spec/Axioms.md. The hash-chain option may follow wf's own log (src/log.rs:2, each line holds the sha256 of the line before). Write-once fit is judged against Axioms.md:23 and docs/spec/WRITE-ONCE.md. Return: in noticed:, add a line starting "design review:" naming the design files you compared and what you found (t416u.md:7). Install wf once: cargo install --git https://github.com/Amalgamour/Workshop.git --rev c09fa60c92ac2e4cde39c73a061166ebc2fac0e0 --root D:\Git\codex\wf --locked wf (the binary is D:\Git\codex\wf\bin\wf.exe; same code as the returns branch today).
jobs:
  w01: new crate labs/0703/ (Cargo.toml with an empty [workspace] table, src/, a .gitignore holding target/). Generate about 1,000 sample pages from the shape of the 11 example .seq files, seeded so every run makes the same pages. Store them three ways: (a) one plain text file per page, committed with git; (b) one append-only log where each record holds the sha256 of the one before; (c) SQLite (the rusqlite crate with its bundled feature).
  w02: measure each store: time to write all pages, read all, read one; size on disk; hand-readability (can a person read one page in a plain editor, and why); tamper detection (change one byte: what finds it, and how); write-once fit (can a written page change without a trace). Unit tests: each store gives back the page it was given, and a one-byte change in the log is found.
  w03: labs/0703/LAB-0703-SEQ-STORAGE.md with sections "## 1. Options", "## 2. Sample pages", "## 3. Results" (a table, with the machine and OS the numbers came from), "## 4. Pick" (one option, with reasons tied to Axioms.md:23 and WRITE-ONCE.md, and what the others are still good for) and "## 5. How to rerun" (the exact commands).
may touch:   labs/0703/
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --manifest-path labs/0703/Cargo.toml; git ls-files --error-unmatch labs/0703/LAB-0703-SEQ-STORAGE.md; git grep -q -F "## 3. Results" labs/0703/LAB-0703-SEQ-STORAGE.md; git grep -q -F "## 4. Pick" labs/0703/LAB-0703-SEQ-STORAGE.md; git grep -q -F "## 5. How to rerun" labs/0703/LAB-0703-SEQ-STORAGE.md   (one command each, split by ;)
done when:   done when: labs/0703/ is on returns with a throwaway Rust bench whose tests pass (cargo test --manifest-path labs/0703/Cargo.toml) and labs/0703/LAB-0703-SEQ-STORAGE.md with the options, the sample pages, a results table (write and read speed, size, hand-readability, tamper detection, write-once fit), one pick with reasons, and how to rerun; and the cross-check by Claude passes.
stop if:     you would change any file outside labs/0703/ (the return check refuses it); rusqlite will not build on your machine (end w01 need and say what failed; do not swap in another database silently); the timings are the only basis for the pick (say so); a rule above reads two ways. Do not commit target/ or the generated pages; the checks run cargo test, not the timing run, because timings differ by machine
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 4, hash c9182530b361
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash 9b2dba93f1ef
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
