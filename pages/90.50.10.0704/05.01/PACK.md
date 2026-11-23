WORKSHOP PACK 90.50.10.0704.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0704 (Codex drift-check and worker design lab)
prime:       prima
predecessor: none
repo:        work
start:       10abb9f2598191ebf2652b70704cddc0fe3ffd56
branch:      returns
return file: .workshop/returns/90.50.10.0704.05.01.md
grant:       labs/0704/ (t523u)
axioms:      1.7.8,2.9
outcome:     labs/0704/DRIFT-REVIEW.md, labs/0704/WORKER-LOOPS.md and labs/0704/LESSONS.md: a drift review against Matthew's stated goals, a stage-goals review, proposals for how we build workers and better loops, an independent spot-check of at least three closed or returned pages, and short lessons
overview:    Builder: Codex (Matthew's PC, D:\Git\codex; Codex CLI needs network enabled for git). Checker: Grok-Check (wf check --as Grok-Check). Why: t523u (docs/review/DIRECTOR-WORDS-t523.md) "I want you to build a lab for codex to run.  I want to work with it directly on this.  It's a research planning and design lab.  On how we build our workers, better loops, and how review our current stages goals.  As well as checking what has been done.  It's a 2nd project for codex, a checker so it a different source then all grok code." and "Just to help you from accidently drifting.  We need to confirm we aren't drifting." This is a lab in the lab band (door 90.50.10.0700). It is a new lab because no lab on the door tries this subject (0701 wf loop, 0702 seq grammar, 0703 seq storage). 0704 is the next free number after 0703 on this book; old-lib 0706 prima-loop is a different book and is not used. Serves no page yet. This pack is a frame, not a script. Matthew works with Codex directly; Codex may follow Matthew's direction within the grant labs/0704/, including adding further files under that folder. Research only: do not change src/, tests/, or any code. Sources are read only: git -C work fetch origin prima/build packs returns, then read docs/plan/STAGE-PLAN-90.50.10.md, docs/plan/GROK-BUILDER-QUEUE.md, docs/plan/WORKER-ROLES.md, docs/lessons/, docs/review/DIRECTOR-WORDS-* on prima/build, and page logs on packs and returns. Cite as path:line (and the commit if the line may move). Quote short lines only; do not copy files into the report. A source that is missing or unreadable is written as such, never filled in. Return: in noticed:, add a line starting "design review:" naming the design files you compared and what you found (t416u.md:7). If wf.exe is not built from a823ee284574be3d9f6247925b9088137a27a539, rebuild it first (cargo install --path . --root D:\Git\codex\wf-bin --force, or the root you already use).
jobs:
  w01: Write labs/0704/DRIFT-REVIEW.md. Section "## 1. Drift": compare what was built and decided (docs/plan/STAGE-PLAN*, docs/plan/GROK-BUILDER-QUEUE.md, docs/plan/WORKER-ROLES.md, docs/lessons/, docs/review/DIRECTOR-WORDS-* files, recent closes in page logs) against Matthew's stated goals (DIRECTOR-WORDS files, STAGE-PLAN goals). List each place work drifted from, or matches, those goals, with file:line cites. Section "## 2. Stage goals": for the current stage(s), are the goals still right and on track, and what is done versus what is claimed done, with file:line cites. Section "## 3. Spot checks": independently check at least three closed or returned pages' claims against the code or tests, with file:line or commit cites.
  w02: Write labs/0704/WORKER-LOOPS.md. Section "## 1. Workers": how we build workers (Grok builders, Grok-Check, Cursor-1, Claude, Codex, cloud agents). Section "## 2. Loops": proposals for better loops (pack/claim/return/check/signoff/close, research loop, lessons).
  w03: Write labs/0704/LESSONS.md, a short list of lessons learned so far (what went wrong or what held, why, what to do next time), each with a file:line or commit cite (t506u).
may touch:   labs/0704/
must not:    anything outside may touch (the return check refuses it)
checks:      git ls-files --error-unmatch labs/0704/DRIFT-REVIEW.md; git ls-files --error-unmatch labs/0704/WORKER-LOOPS.md; git ls-files --error-unmatch labs/0704/LESSONS.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0704/DRIFT-REVIEW.md; git grep -q -E [#][#][[:space:]]2[.] -- labs/0704/DRIFT-REVIEW.md; git grep -q -E [#][#][[:space:]]3[.] -- labs/0704/DRIFT-REVIEW.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0704/WORKER-LOOPS.md; git grep -q -E [#][#][[:space:]]2[.] -- labs/0704/WORKER-LOOPS.md   (one command each, split by ;)
done when:   Done when: labs/0704/DRIFT-REVIEW.md lists each place work drifted from, or matches, Matthew's stated goals, with file:line cites. Sources compared: docs/plan/STAGE-PLAN*, docs/plan/GROK-BUILDER-QUEUE.md, docs/plan/WORKER-ROLES.md, docs/lessons/, docs/review/DIRECTOR-WORDS-* files, and recent closes in page logs, against DIRECTOR-WORDS files and STAGE-PLAN goals.
Done when: the same file's stage-goals review says, for the current stage(s), whether the goals are still right and on track, and what is done versus what is claimed done, with file:line cites.
Done when: labs/0704/WORKER-LOOPS.md describes how we build workers (Grok builders, Grok-Check, Cursor-1, Claude, Codex, cloud agents) and proposes better loops (pack/claim/return/check/signoff/close, research loop, lessons).
Done when: the report spot-checks at least three closed or returned pages' claims against the code or tests, with file:line or commit cites.
Done when: labs/0704/LESSONS.md is a short list of lessons, each with a file:line or commit cite.
stop if:     you would change any file outside labs/0704/ (the return check refuses it); you would change src/, tests/, or any code (research only); a check command has a caret, quotes, or a space inside a git grep pattern; a real drift or unmet goal is marked matched without a cite; Matthew's direction would leave the grant (stop and raise it); a rule above reads two ways. The checks only prove the files and headings exist; the checker judges the cites and the claims
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 4, hash 52ddd710e4f7
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash 53d52228c7d2
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
