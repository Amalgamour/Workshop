=== WORKSHOP JOB 90.50.10.0702.05.03 ===
Pack hash: 841660920ba0a469641307b96ac3ab8d4644d72f931bbef56808a36d86f7dee4 (log entry 24, 2026-11-23T16:30:20Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0702 03 --as <your-name>
Repo: work   Branch: returns   Start: 9c669caecce46cc94622d744e8698ea1e79899da
Read first: pages/90.50.10.0702/05.03/AGENTS.md (sha256 93289ba80510), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: the seq grammar lab, reusable by every stage. It learns, by reading the design and trying it on real examples, what a .seq file is and how it reads: the address form, the line kinds and the references, and how each axiom is kept. Matthew: "We have a lot to learn about axioms, designing and building our grammar out of seqaddr.  How a .seq file should work." (t451u). Lab band door: 90.50.10.0700.
Builder (pass 3): Claude (Matthew's PC, D:\Git\claude). Checker: Grok-Check (wf check --as Grok-Check). Codex's manual check of pass 2 (return ba9a5b7) is the source of this redo.
Serves: no page yet. Stage 1 is wf itself; the pages that will use this lab are the .seq pages of later stages. Each is listed here, and lists this lab back, when it is made.
Related lab: 90.50.10.0703 seq storage lab.
Pass 1 closed failed. Pass 2 closed failed on Codex's manual check (4 met, 3 not met). Pass 3 fixes those findings. Keep what pass 2 already met.
Done when: the text production used at lab :231-232 is defined, and the registry row at lab :205 includes counters := for face 00 counter history (derive.rs:247-249).
Done when: the open-conflict table is narrowed: O2 separates the v1 ASCII page view from the proposed whole-book format (SEQ-FILE-PLAN.md:315-327); O6 acknowledges the settled 0700-0799 allocation (seqAddr.md:345-351); O9 is parked by R21 (DIRECTOR-RULINGS.md:82-84), not treated as a live conflict.
Done when: Q2 marks R9's general rule answered and carries the R16 dictionary 03.00 exception as open (DIRECTOR-RULINGS.md:65-66, face00.md:470).
Done when: Q6's fallback is the first nonblank trimmed note line (derive.rs:137-138).
Done when: lab :343 no longer calls Bob's booked body imported; import checks booked bodies when a book is supplied and sends only new blocks as proposals (import.rs:45-51, 64-87).
Done when: lessons 3, 4, 6 and 7 are tightened as Codex said: lesson 3 carries the R16 exception; lesson 4 distinguishes current implementation from an open design decision; lesson 6 cites a dry-run transcript for the actual error and notes that avoiding spaces alone leaves the Windows caret issue; lesson 7's intake incident is not independently established by the cited material.
Done when: what pass 2 already met stays true (entry numbers, body checks, added cases, and lessons 1, 2, 5 and 8).

Jobs:
  w01: Define the text production used at lab :231-232 (why-draft-v and stamp-v). Write it from the code that prints those values. Do not leave text undefined.
  w02: Add counters := to the registry (face 00) row at lab :205, for face 00 counter history. derive.rs:247-249 keeps that value when rendering face 00, for losslessness, even though the core does not treat it as legal.
  w03: Narrow the open-conflict table. O2 must separate the v1 ASCII page view from the proposed whole-book format, which explicitly frames binary faces (SEQ-FILE-PLAN.md:315-327). O6 must acknowledge the settled 0700-0799 allocation (seqAddr.md:345-351). O9 is parked by R21 (DIRECTOR-RULINGS.md:82-84); do not treat it as a live conflict.
  w04: Q2 already states R9's general rule. Mark that general rule answered, and carry the R16 dictionary 03.00 exception as open (DIRECTOR-RULINGS.md:65-66, face00.md:470).
  w05: Tighten two implementation claims. Q6's fallback is the first nonblank trimmed note line (derive.rs:137-138). Lab :343 calls Bob's booked body imported; import checks booked bodies when a book is supplied and sends only new blocks as proposals (import.rs:45-51, 64-87). Fix the wording.
  w06: Tighten lessons 3, 4, 6 and 7 as Codex said. Lesson 3: carry the R16 exception. Lesson 4: distinguish current implementation from an open design decision. Lesson 6: cite a dry-run transcript for the actual error, and note that avoiding spaces alone leaves the Windows caret issue. Lesson 7: the builder prompt supports the sequencing rule, but the cited material does not independently establish the reported intake incident. Keep lessons 1, 2, 5 and 8.
May touch: labs/0702/
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: git ls-files --error-unmatch labs/0702/LAB-0702-SEQ-GRAMMAR.md; git ls-files --error-unmatch labs/0702/LESSONS.md; git grep -q -E [#][#][[:space:]]0[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]2[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]3[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]4[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]5[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E [#][#][[:space:]]6[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md
Done when (face 01): Done when: the text production used at lab :231-232 is defined, and the registry row at lab :205 includes counters := for face 00 counter history (derive.rs:247-249).
Done when: the open-conflict table is narrowed: O2 separates the v1 ASCII page view from the proposed whole-book format (SEQ-FILE-PLAN.md:315-327); O6 acknowledges the settled 0700-0799 allocation (seqAddr.md:345-351); O9 is parked by R21 (DIRECTOR-RULINGS.md:82-84), not treated as a live conflict.
Done when: Q2 marks R9's general rule answered and carries the R16 dictionary 03.00 exception as open (DIRECTOR-RULINGS.md:65-66, face00.md:470).
Done when: Q6's fallback is the first nonblank trimmed note line (derive.rs:137-138).
Done when: lab :343 no longer calls Bob's booked body imported; import checks booked bodies when a book is supplied and sends only new blocks as proposals (import.rs:45-51, 64-87).
Done when: lessons 3, 4, 6 and 7 are tightened as Codex said: lesson 3 carries the R16 exception; lesson 4 distinguishes current implementation from an open design decision; lesson 6 cites a dry-run transcript for the actual error and notes that avoiding spaces alone leaves the Windows caret issue; lesson 7's intake incident is not independently established by the cited material.
Done when: what pass 2 already met stays true (entry numbers, body checks, added cases, and lessons 1, 2, 5 and 8).
Stop if: another file must change, including docs/lessons/ or src/. A check command has a caret, quotes, or a space inside a git grep pattern. A real open conflict is marked answered. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0702/05.03/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0702.05.03.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0702 03 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0702.05.03.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
