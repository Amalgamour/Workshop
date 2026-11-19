=== WORKSHOP JOB 90.50.10.0703.05.01 ===
Pack hash: 3cbdea445b7a6e063f446f4fad030b0f4f4821e39cb6f09f3f1419fb11578f92 (log entry 6, 2026-11-19T20:03:35Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0703 01 --as <your-name>
Repo: work   Branch: returns   Start: c09fa60c92ac2e4cde39c73a061166ebc2fac0e0
Read first: pages/90.50.10.0703/05.01/AGENTS.md (sha256 de04b0e5a66d), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: the seq storage lab, reusable by every stage. It learns, by measuring, how .seq pages should be stored: plain text files with git, an append-only hash-chain log, or SQLite, on about 1,000 sample pages. Matthew: "What should be the design for the storage of it." (t451u). Lab band door: 90.50.10.0700.
Builder (pass 1): Codex (t439u; t453u). Checker: Claude, by hand: wf only refuses the builder as checker (src/cmd.rs:730).
Serves: no page yet. The pages that will use this lab are the storage pages of a later stage (roadmap stage 4, Safe storage). Each is listed here, and lists this lab back, when it is made.
Related lab: 90.50.10.0702 seq grammar lab (it describes what this lab stores).
Pass 1 done when: labs/0703/ is on returns with a throwaway Rust bench whose tests pass (cargo test --manifest-path labs/0703/Cargo.toml) and labs/0703/LAB-0703-SEQ-STORAGE.md with the options, the sample pages, a results table (write and read speed, size, hand-readability, tamper detection, write-once fit), one pick with reasons, and how to rerun; and the cross-check by Claude passes.

Jobs:
  w01: new crate labs/0703/ (Cargo.toml with an empty [workspace] table, src/, a .gitignore holding target/). Generate about 1,000 sample pages from the shape of the 11 example .seq files, seeded so every run makes the same pages. Store them three ways: (a) one plain text file per page, committed with git; (b) one append-only log where each record holds the sha256 of the one before; (c) SQLite (the rusqlite crate with its bundled feature).
  w02: measure each store: time to write all pages, read all, read one; size on disk; hand-readability (can a person read one page in a plain editor, and why); tamper detection (change one byte: what finds it, and how); write-once fit (can a written page change without a trace). Unit tests: each store gives back the page it was given, and a one-byte change in the log is found.
  w03: labs/0703/LAB-0703-SEQ-STORAGE.md with sections "## 1. Options", "## 2. Sample pages", "## 3. Results" (a table, with the machine and OS the numbers came from), "## 4. Pick" (one option, with reasons tied to Axioms.md:23 and WRITE-ONCE.md, and what the others are still good for) and "## 5. How to rerun" (the exact commands).
May touch: labs/0703/
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --manifest-path labs/0703/Cargo.toml; git ls-files --error-unmatch labs/0703/LAB-0703-SEQ-STORAGE.md; git grep -q -F "## 3. Results" labs/0703/LAB-0703-SEQ-STORAGE.md; git grep -q -F "## 4. Pick" labs/0703/LAB-0703-SEQ-STORAGE.md; git grep -q -F "## 5. How to rerun" labs/0703/LAB-0703-SEQ-STORAGE.md
Done when (face 01): done when: labs/0703/ is on returns with a throwaway Rust bench whose tests pass (cargo test --manifest-path labs/0703/Cargo.toml) and labs/0703/LAB-0703-SEQ-STORAGE.md with the options, the sample pages, a results table (write and read speed, size, hand-readability, tamper detection, write-once fit), one pick with reasons, and how to rerun; and the cross-check by Claude passes.
Stop if: you would change any file outside labs/0703/ (the return check refuses it); rusqlite will not build on your machine (end w01 need and say what failed; do not swap in another database silently); the timings are the only basis for the pick (say so); a rule above reads two ways. Do not commit target/ or the generated pages; the checks run cargo test, not the timing run, because timings differ by machine (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0703/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0703.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0703 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0703.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
