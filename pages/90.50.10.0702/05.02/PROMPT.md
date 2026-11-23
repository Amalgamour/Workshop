=== WORKSHOP JOB 90.50.10.0702.05.02 ===
Pack hash: e570e7a6d93e723f074d8473866d9b06c3e5e2d9f177ccfb0f1fd40b8fea86e6 (log entry 15, 2026-11-23T15:51:39Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0702 02 --as <your-name>
Repo: work   Branch: returns   Start: 86770ec221da36d3edaed3d1399459b555a86fa3
Read first: pages/90.50.10.0702/05.02/AGENTS.md (sha256 7f88956c2d3f), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: the seq grammar lab, reusable by every stage. It learns, by reading the design and trying it on real examples, what a .seq file is and how it reads: the address form, the line kinds and the references, and how each axiom is kept. Matthew: "We have a lot to learn about axioms, designing and building our grammar out of seqaddr.  How a .seq file should work." (t451u). Lab band door: 90.50.10.0700.
Builder (pass 2): Claude. Checker: Codex, by hand.
Serves: no page yet. Stage 1 is wf itself; the pages that will use this lab are the .seq pages of later stages. Each is listed here, and lists this lab back, when it is made.
Related lab: 90.50.10.0703 seq storage lab.
Pass 1 closed failed. Pass 2 redos the grammar report from Codex's cross-check.
Done when: the entry-number rule (lab:176) is restated as one booked block and one matching history entry, in book order, with references allowed (seqpage.md:135, :199-201).
Done when: lab:183 no longer claims body text is never checked (seqpage.md:169, :186; crates/seqpage/src/parse.rs:366-370).
Done when: derived values have a written value grammar, and source := uses full book addresses.
Done when: section 5 splits superseded text (K2/R26, K4/R9, K5/R10, K7/R28, K9/R35, K10, K11 stale) from real open conflicts.
Done when: Q2, Q4, Q5, Q6 and Q7 are marked answered with the ruling or code cite (DIRECTOR-RULINGS.md:37-41, :113-115; state.rs:607-631; derive.rs:119-141, :204-206), and only what truly stays open remains open.
Done when: the report covers escaped keys (seqpage.md:156), decoded ASCII checks (seqpage.md:44), and the stamp-versus-replay disagreement in examples/real/10.11.21.1001.bob.seq:85-88.
Done when: labs/0702/LESSONS.md is a short list of lessons learned so far (what went wrong, why, what to do next time), each with a file:line or commit cite (t506u). Codex checks it in the cross-check. It feeds docs/lessons/ later.

Jobs:
  w01: Restate the entry-number rule at lab:176 as one booked block and one matching history entry, in book order, with references allowed (seqpage.md:135, :199-201).
  w02: Fix lab:183 so it does not claim body text is never checked. seqpage.md:169 says a prefixed body cannot be mistaken for structure. seqpage.md:186 and crates/seqpage/src/parse.rs:366-370 do check the body's cards.
  w03: Write a value grammar for derived values, including lineage, source, faces and counters. source := uses a full book address.
  w04: In section 5, split superseded text from real open conflicts. Superseded: K2/R26, K4/R9, K5/R10, K7/R28, K9/R35, K10, K11 stale. Do not resolve a conflict that is still open.
  w05: Mark Q2, Q4, Q5, Q6 and Q7 answered, with the ruling or code cite (DIRECTOR-RULINGS.md:37-41, :113-115; state.rs:607-631; derive.rs:119-141, :204-206). Keep only what truly stays open.
  w06: Add coverage for escaped keys (seqpage.md:156), decoded ASCII checks (seqpage.md:44), and the stamp-versus-replay disagreement in examples/real/10.11.21.1001.bob.seq:85-88.
  w07: Write labs/0702/LESSONS.md. A short list of lessons so far: what went wrong, why, and what to do next time. Each item cites a file:line or a commit (t506u).
May touch: labs/0702/
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: git ls-files --error-unmatch labs/0702/LAB-0702-SEQ-GRAMMAR.md; git ls-files --error-unmatch labs/0702/LESSONS.md; git grep -q -E "^##[[:space:]]0[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]1[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]2[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]3[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]4[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]5[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]6[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md
Done when (face 01): Done when: the entry-number rule (lab:176) is restated as one booked block and one matching history entry, in book order, with references allowed (seqpage.md:135, :199-201).
Done when: lab:183 no longer claims body text is never checked (seqpage.md:169, :186; crates/seqpage/src/parse.rs:366-370).
Done when: derived values have a written value grammar, and source := uses full book addresses.
Done when: section 5 splits superseded text (K2/R26, K4/R9, K5/R10, K7/R28, K9/R35, K10, K11 stale) from real open conflicts.
Done when: Q2, Q4, Q5, Q6 and Q7 are marked answered with the ruling or code cite (DIRECTOR-RULINGS.md:37-41, :113-115; state.rs:607-631; derive.rs:119-141, :204-206), and only what truly stays open remains open.
Done when: the report covers escaped keys (seqpage.md:156), decoded ASCII checks (seqpage.md:44), and the stamp-versus-replay disagreement in examples/real/10.11.21.1001.bob.seq:85-88.
Done when: labs/0702/LESSONS.md is a short list of lessons learned so far (what went wrong, why, what to do next time), each with a file:line or commit cite (t506u). Codex checks it in the cross-check. It feeds docs/lessons/ later.
Stop if: another file must change, including docs/lessons/ or src/. A check command has a space inside a quoted pattern. A real open conflict is marked answered. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0702/05.02/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0702.05.02.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0702 02 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0702.05.02.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
