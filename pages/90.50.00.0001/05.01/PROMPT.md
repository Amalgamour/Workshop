=== WORKSHOP JOB 90.50.00.0001.05.01 ===
Pack hash: d8f9c8b3759ff1b4c4fcf916bd6fa3fe3e079a004512e0e5c236d079a72211d1 (log entry 6, 2026-11-19T17:57:37Z)
You are: the builder. Claim first:
  wf claim 90.50.00.0001 01 --as <your-name>
Repo: work   Branch: returns   Start: 3daaa4861346ebf7829a5f3eace6a99387be4d1c
Read first: pages/90.50.00.0001/05.01/AGENTS.md (sha256 aa128a665a94), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: BUILDER-PROMPT.md tells the builder to run wf.exe, not wf, at every step (PowerShell resolves wf to Windows Fax, t407u; wf.exe also works in Git Bash).
Done when: every wf command line in a printed BUILDER-PROMPT.md starts with wf.exe, and cargo test --test wf builder_prompt passes on the box.
Jobs:
  w01: in templates/v3/builder.txt, write wf.exe wherever the builder is told to run wf (the claim line, the return line, and the two "wf return ... --push" mentions). Leave "cargo install ... wf" as is: there wf names the crate.
  w02: in tests/wf.rs, update t401u_pack_on_the_shared_branch_prints_one_builder_prompt to expect "wf.exe claim 1.2.3.4 01" and "wf.exe return 1.2.3.4 01"
May touch: templates/v3/builder.txt, tests/wf.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --test wf builder_prompt
Done when (face 01): Done when: every wf command line in a printed BUILDER-PROMPT.md starts with wf.exe, and cargo test --test wf builder_prompt passes on the box.
Stop if: another file must change. On Windows tests/wf.rs does not compile yet (unix-only imports, known): run cargo build instead, say so on the proof line, and go on; the checker runs the test on the box (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.00.0001/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.00.0001.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.00.0001 01 --branch returns --commit <sha> --file .workshop/returns/90.50.00.0001.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
