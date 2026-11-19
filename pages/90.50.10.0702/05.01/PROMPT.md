=== WORKSHOP JOB 90.50.10.0702.05.01 ===
Pack hash: 533cee460c3e4c3ac848614736c4657edb0c65db11169b8da4515ab6b740cd6f (log entry 6, 2026-11-19T20:03:35Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0702 01 --as <your-name>
Repo: work   Branch: returns   Start: c09fa60c92ac2e4cde39c73a061166ebc2fac0e0
Read first: pages/90.50.10.0702/05.01/AGENTS.md (sha256 e73bab2b11c9), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: the seq grammar lab, reusable by every stage. It learns, by reading the design and trying it on real examples, what a .seq file is and how it reads: the address form, the line kinds and the references, and how each axiom is kept. Matthew: "We have a lot to learn about axioms, designing and building our grammar out of seqaddr.  How a .seq file should work." (t451u). Lab band door: 90.50.10.0700.
Builder (pass 1): Claude (t439u; t453u). Checker: Codex, by hand: wf only refuses the builder as checker (src/cmd.rs:730).
Serves: no page yet. Stage 1 is wf itself; the pages that will use this lab are the .seq pages of later stages (roadmap stage 3 First proof, stage 4 Safe storage). Each is listed here, and lists this lab back, when it is made.
Related lab: 90.50.10.0703 seq storage lab (it stores what this lab describes).
Pass 1 done when: labs/0702/LAB-0702-SEQ-GRAMMAR.md is on returns with its seven sections (0 sources read, 1 what a .seq file is, 2 grammar, 3 three worked examples, 4 how each axiom is kept, 5 conflicts in the docs, 6 open questions with defaults), every claim cites path:line at build commit 8e96151d, and the cross-check by Codex passes.

Jobs:
  w01: new labs/0702/LAB-0702-SEQ-GRAMMAR.md. Section "## 0. Sources read": each source path, the commit, and read or missing. Section "## 1. What a .seq file is": what it holds, one page per file or not, how it is named, who writes it, cited.
  w02: section "## 2. Grammar": the address form (desk, shelf, book, page, face, counter, tail), the line kinds, and how a line refers to another page or line, each rule cited. Section "## 3. Worked examples": three real files from docs/spec/examples at 8e96151d, each read line by line against section 2, with any line the grammar does not cover marked.
  w03: section "## 4. How each axiom is kept": axioms 1-9, each with where the grammar keeps it or a gap (Axioms.md lines). Section "## 5. Conflicts in the docs": each conflict with file:line on both sides, not resolved. Section "## 6. Open questions": each with options and the fractal option marked (default) (t384u.md:5).
May touch: labs/0702/LAB-0702-SEQ-GRAMMAR.md
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: git ls-files --error-unmatch labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 0. Sources read" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 1. What a .seq file is" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 2. Grammar" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 3. Worked examples" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 4. How each axiom is kept" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 5. Conflicts in the docs" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 6. Open questions" labs/0702/LAB-0702-SEQ-GRAMMAR.md
Done when (face 01): done when: labs/0702/LAB-0702-SEQ-GRAMMAR.md is on returns with its seven sections (0 sources read, 1 what a .seq file is, 2 grammar, 3 three worked examples, 4 how each axiom is kept, 5 conflicts in the docs, 6 open questions with defaults), every claim cites path:line at build commit 8e96151d, and the cross-check by Codex passes.
Stop if: you would change any file outside may touch (the return check refuses it); a source cannot be fetched at 8e96151d (write it as missing in section 0 and go on; stop only if Axioms.md or seqAddr.md is missing); the docs do not settle a grammar point (put it under section 5 or 6 with a default, do not decide it silently); a rule above reads two ways. The checks only prove the sections exist; the checker reads the cites (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0702/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0702.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0702 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0702.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
