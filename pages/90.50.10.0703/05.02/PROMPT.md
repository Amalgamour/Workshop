=== WORKSHOP JOB 90.50.10.0703.05.02 ===
Pack hash: 0defb2bef51bdaee7ffe4f0a768c8353c3fc7d64c78140391663d121ed964a45 (log entry 15, 2026-11-23T15:51:39Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0703 02 --as <your-name>
Repo: work   Branch: returns   Start: 86770ec221da36d3edaed3d1399459b555a86fa3
Read first: pages/90.50.10.0703/05.02/AGENTS.md (sha256 e11292c4f34e), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: the seq storage lab, reusable by every stage. It learns, by measuring, how .seq pages should be stored: plain text files with git, an append-only hash-chain log, or SQLite, on about 1,000 sample pages. Matthew: "What should be the design for the storage of it." (t451u). Lab band door: 90.50.10.0700.
Builder (pass 2): Codex. Checker: Claude, by hand.
Serves: no page yet. The pages that will use this lab are the storage pages of a later stage. Each is listed here, and lists this lab back, when it is made.
Related lab: 90.50.10.0702 seq grammar lab.
Pass 1 closed failed. Pass 2 redos the bench so the pick is supported.
Done when: writes have equal durability (fsync the log, or compare all three at the same durability) and the table says so.
Done when: every store gets the same tamper attack and the same outside reference, including a rewrite-and-rehash attack on the log and an attack on Git's .git history.
Done when: an update workload gives a page a second version, and read_one returns the latest.
Done when: tests cover a truncated tail and a removed middle record.
Done when: Git's commit chain is weighed as an append-only option, or the report states a reason it loses.
Done when: the report names the conflict with SEQ-FILE-PLAN.md:246 and :251 (folder per page, file per face) and says what the result means for it.
Done when: R37 is cited by file:line (DIRECTOR-RULINGS.md:192).
Done when: labs/0703/LESSONS.md is a short list of lessons learned so far (what went wrong, why, what to do next time), each with a file:line or commit cite (t506u). Claude checks it in the cross-check. It feeds docs/lessons/ later.

Jobs:
  w01: Make write durability equal. Fsync the log, or compare git, the log and SQLite at the same durability, and say which in the results table.
  w02: Use the same tamper attack and the same outside reference for every store. Include a rewrite-and-rehash attack on the log, and an attack on Git's .git history.
  w03: Add an update workload. A page gets a second version. read_one returns the latest.
  w04: Add tests for a truncated tail and for a removed middle record.
  w05: Weigh Git's commit chain as an append-only option, or state a reason it loses.
  w06: Name the conflict with SEQ-FILE-PLAN.md:246 and :251 (stored form is a folder per page and a file per face) and say what this result means for that plan.
  w07: Cite R37 by file:line. It is DIRECTOR-RULINGS.md:192 on prima/build.
  w08: Write labs/0703/LESSONS.md. A short list of lessons so far: what went wrong, why, and what to do next time. Each item cites a file:line or a commit (t506u). If cheap, fix sample titles that contain spaces (seqAddr.md:281) and make the tamper error name the edited record, not the next one.
May touch: labs/0703/
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --manifest-path labs/0703/Cargo.toml; git ls-files --error-unmatch labs/0703/LAB-0703-SEQ-STORAGE.md; git ls-files --error-unmatch labs/0703/LESSONS.md
Done when (face 01): Done when: writes have equal durability (fsync the log, or compare all three at the same durability) and the table says so.
Done when: every store gets the same tamper attack and the same outside reference, including a rewrite-and-rehash attack on the log and an attack on Git's .git history.
Done when: an update workload gives a page a second version, and read_one returns the latest.
Done when: tests cover a truncated tail and a removed middle record.
Done when: Git's commit chain is weighed as an append-only option, or the report states a reason it loses.
Done when: the report names the conflict with SEQ-FILE-PLAN.md:246 and :251 (folder per page, file per face) and says what the result means for it.
Done when: R37 is cited by file:line (DIRECTOR-RULINGS.md:192).
Done when: labs/0703/LESSONS.md is a short list of lessons learned so far (what went wrong, why, what to do next time), each with a file:line or commit cite (t506u). Claude checks it in the cross-check. It feeds docs/lessons/ later.
Stop if: another file must change, including docs/lessons/ or src/. A check command has a space inside a quoted pattern. The table still compares stores at different durability without saying so. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0703/05.02/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0703.05.02.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0703 02 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0703.05.02.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
