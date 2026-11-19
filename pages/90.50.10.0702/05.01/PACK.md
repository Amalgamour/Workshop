WORKSHOP PACK 90.50.10.0702.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0702 (seq grammar lab: what a .seq file is and how it reads)
prime:       prima
predecessor: none
repo:        work
start:       c09fa60c92ac2e4cde39c73a061166ebc2fac0e0
branch:      returns
return file: .workshop/returns/90.50.10.0702.05.01.md
grant:       labs/0702/ (t452u)
axioms:      1.7.8,2.6.8
outcome:     one report, labs/0702/LAB-0702-SEQ-GRAMMAR.md, that says what a .seq file is and how it reads (address form, line kinds, references), with three worked examples from real files, how each axiom is kept, the conflicts in the docs with file:line on both sides, and open questions each with a marked default
overview:    Builder: Claude (t439u). Checker: Codex, by hand (wf refuses only the builder as checker, src/cmd.rs:730). Why: t451u (docs/review/DIRECTOR-WORDS-t450-t453u.md:9) "We have a lot to learn about axioms, designing and building our grammar out of seqaddr.  How a .seq file should work." This is a lab in the lab band (door 90.50.10.0700); it learns before any .seq work page exists, so it serves no page yet. Sources are read only and live in the build design, not in this repo: run git -C work fetch origin prima/build, then read each with git -C work show 8e96151dbe9ff03a55e6838168033ba6bf5f4a4a:<path>. Read: docs/spec/Axioms.md, docs/spec/seqpage.md, docs/spec/seqpage-QUESTIONS.md, docs/spec/SEQ-GUIDE.md, docs/spec/face00.md, docs/spec/KERNEL-FILE-TITLES.md, docs/spec/examples/ (11 .seq files), docs/spec/seqAddr.md (address rules, sections 1, 4, 8, 10, 11), docs/design/SEQ-FILE-PLAN.md, docs/design/SEQ-FILE-PLAN-TEST.md, docs/design/SEQ-FILE-PLAN-TEST-2.md, docs/design/SEQ-PROTO-RESULTS.md, docs/design/AXIOM-CITE-GRAMMAR-draft-t383u.md. Cite as path:line@8e96151d. Quote short lines only; do not copy files into the report (Axioms.md:15). A source that is missing or unreadable is written as such, never filled in (Axioms.md:25). Matthew may talk the design through with you (t452u); write what he says in the report with the time he said it. Return: in noticed:, add a line starting "design review:" naming the design files you compared and what you found (t416u.md:7). Install wf once: cargo install --git https://github.com/Amalgamour/Workshop.git --rev c09fa60c92ac2e4cde39c73a061166ebc2fac0e0 --root D:\Git\claude\wf --locked wf (the binary is D:\Git\claude\wf\bin\wf.exe; same code as the returns branch today).
jobs:
  w01: new labs/0702/LAB-0702-SEQ-GRAMMAR.md. Section "## 0. Sources read": each source path, the commit, and read or missing. Section "## 1. What a .seq file is": what it holds, one page per file or not, how it is named, who writes it, cited.
  w02: section "## 2. Grammar": the address form (desk, shelf, book, page, face, counter, tail), the line kinds, and how a line refers to another page or line, each rule cited. Section "## 3. Worked examples": three real files from docs/spec/examples at 8e96151d, each read line by line against section 2, with any line the grammar does not cover marked.
  w03: section "## 4. How each axiom is kept": axioms 1-9, each with where the grammar keeps it or a gap (Axioms.md lines). Section "## 5. Conflicts in the docs": each conflict with file:line on both sides, not resolved. Section "## 6. Open questions": each with options and the fractal option marked (default) (t384u.md:5).
may touch:   labs/0702/LAB-0702-SEQ-GRAMMAR.md
must not:    anything outside may touch (the return check refuses it)
checks:      git ls-files --error-unmatch labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 0. Sources read" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 1. What a .seq file is" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 2. Grammar" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 3. Worked examples" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 4. How each axiom is kept" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 5. Conflicts in the docs" labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -F "## 6. Open questions" labs/0702/LAB-0702-SEQ-GRAMMAR.md   (one command each, split by ;)
done when:   done when: labs/0702/LAB-0702-SEQ-GRAMMAR.md is on returns with its seven sections (0 sources read, 1 what a .seq file is, 2 grammar, 3 three worked examples, 4 how each axiom is kept, 5 conflicts in the docs, 6 open questions with defaults), every claim cites path:line at build commit 8e96151d, and the cross-check by Codex passes.
stop if:     you would change any file outside may touch (the return check refuses it); a source cannot be fetched at 8e96151d (write it as missing in section 0 and go on; stop only if Axioms.md or seqAddr.md is missing); the docs do not settle a grammar point (put it under section 5 or 6 with a default, do not decide it silently); a rule above reads two ways. The checks only prove the sections exist; the checker reads the cites
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 4, hash a797e025a662
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash a4d5cc36c506
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
