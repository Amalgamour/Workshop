# Return 90.50.10.0703.05.01
pack: 3cbdea445b7a6e063f446f4fad030b0f4f4821e39cb6f09f3f1419fb11578f92
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - new crate labs/0703/ (Cargo.toml with an empty [workspace] table, src/, a .gitignore holding target/). Generate about 1,000 sample pages from the shape of the 11 example .seq files, seeded so every run makes the same pages. Store them three ways: (a) one plain text file per page, committed with git; (b) one append-only log where each record holds the sha256 of the one before; (c) SQLite (the rusqlite crate with its bundled feature).
w02: <done | need | blocked> - measure each store: time to write all pages, read all, read one; size on disk; hand-readability (can a person read one page in a plain editor, and why); tamper detection (change one byte: what finds it, and how); write-once fit (can a written page change without a trace). Unit tests: each store gives back the page it was given, and a one-byte change in the log is found.
w03: <done | need | blocked> - labs/0703/LAB-0703-SEQ-STORAGE.md with sections "## 1. Options", "## 2. Sample pages", "## 3. Results" (a table, with the machine and OS the numbers came from), "## 4. Pick" (one option, with reasons tied to Axioms.md:23 and WRITE-ONCE.md, and what the others are still good for) and "## 5. How to rerun" (the exact commands).
proof: <commits, tests run and what they showed>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
