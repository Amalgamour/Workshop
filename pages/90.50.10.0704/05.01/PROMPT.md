=== WORKSHOP JOB 90.50.10.0704.05.01 ===
Pack hash: 309bc88cabca9564972892abec0a9c8b7939b6dccc3ec587c13da9698ec1cf2a (log entry 6, 2026-11-23T16:49:04Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0704 01 --as <your-name>
Repo: work   Branch: returns   Start: 10abb9f2598191ebf2652b70704cddc0fe3ffd56
Read first: pages/90.50.10.0704/05.01/AGENTS.md (sha256 1ef44fedebba), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: the drift-check and worker design lab, reusable by every stage. It is a research, planning and design lab. It reviews how we build our workers and how our loops run, reviews whether current stage goals still hold, and independently checks what has been done, so we can confirm we are not drifting. Matthew: "I want you to build a lab for codex to run.  I want to work with it directly on this.  It's a research planning and design lab.  On how we build our workers, better loops, and how review our current stages goals.  As well as checking what has been done.  It's a 2nd project for codex, a checker so it a different source then all grok code." and "Just to help you from accidently drifting.  We need to confirm we aren't drifting." (t523u, docs/review/DIRECTOR-WORDS-t523.md). Lab band door: 90.50.10.0700.
Builder: Codex (Matthew's PC, D:\Git\codex; Codex CLI needs network enabled for git). Checker: Grok-Check (wf check --as Grok-Check). This is a second Codex project, a different source from the Grok builders.
Serves: no page yet. This lab reviews stage work and design. A page it spot-checks is named in the report; it is listed here, and lists this lab back, only if that two-way link is made later.
Why a new lab: no lab on the door tries this subject. 0701 is the wf loop harness, 0702 is seq grammar, 0703 is seq storage. This lab needs its own page (door 0700: a new lab is made only when no lab here tries that subject).
This pack is a frame, not a script. Matthew works with Codex directly. Codex may follow Matthew's direction within the grant labs/0704/. Research only: no changes to src/, tests/, or any code.
Done when: labs/0704/DRIFT-REVIEW.md lists each place work drifted from, or matches, Matthew's stated goals, with file:line cites. Sources compared: docs/plan/STAGE-PLAN*, docs/plan/GROK-BUILDER-QUEUE.md, docs/plan/WORKER-ROLES.md, docs/lessons/, docs/review/DIRECTOR-WORDS-* files, and recent closes in page logs, against DIRECTOR-WORDS files and STAGE-PLAN goals.
Done when: the same file's stage-goals review says, for the current stage(s), whether the goals are still right and on track, and what is done versus what is claimed done, with file:line cites.
Done when: labs/0704/WORKER-LOOPS.md describes how we build workers (Grok builders, Grok-Check, Cursor-1, Claude, Codex, cloud agents) and proposes better loops (pack/claim/return/check/signoff/close, research loop, lessons).
Done when: the report spot-checks at least three closed or returned pages' claims against the code or tests, with file:line or commit cites.
Done when: labs/0704/LESSONS.md is a short list of lessons, each with a file:line or commit cite.

Jobs:
  w01: Write labs/0704/DRIFT-REVIEW.md. Section "## 1. Drift": compare what was built and decided (docs/plan/STAGE-PLAN*, docs/plan/GROK-BUILDER-QUEUE.md, docs/plan/WORKER-ROLES.md, docs/lessons/, docs/review/DIRECTOR-WORDS-* files, recent closes in page logs) against Matthew's stated goals (DIRECTOR-WORDS files, STAGE-PLAN goals). List each place work drifted from, or matches, those goals, with file:line cites. Section "## 2. Stage goals": for the current stage(s), are the goals still right and on track, and what is done versus what is claimed done, with file:line cites. Section "## 3. Spot checks": independently check at least three closed or returned pages' claims against the code or tests, with file:line or commit cites.
  w02: Write labs/0704/WORKER-LOOPS.md. Section "## 1. Workers": how we build workers (Grok builders, Grok-Check, Cursor-1, Claude, Codex, cloud agents). Section "## 2. Loops": proposals for better loops (pack/claim/return/check/signoff/close, research loop, lessons).
  w03: Write labs/0704/LESSONS.md, a short list of lessons learned so far (what went wrong or what held, why, what to do next time), each with a file:line or commit cite (t506u).
May touch: labs/0704/
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: git ls-files --error-unmatch labs/0704/DRIFT-REVIEW.md; git ls-files --error-unmatch labs/0704/WORKER-LOOPS.md; git ls-files --error-unmatch labs/0704/LESSONS.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0704/DRIFT-REVIEW.md; git grep -q -E [#][#][[:space:]]2[.] -- labs/0704/DRIFT-REVIEW.md; git grep -q -E [#][#][[:space:]]3[.] -- labs/0704/DRIFT-REVIEW.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0704/WORKER-LOOPS.md; git grep -q -E [#][#][[:space:]]2[.] -- labs/0704/WORKER-LOOPS.md
Done when (face 01): Done when: labs/0704/DRIFT-REVIEW.md lists each place work drifted from, or matches, Matthew's stated goals, with file:line cites. Sources compared: docs/plan/STAGE-PLAN*, docs/plan/GROK-BUILDER-QUEUE.md, docs/plan/WORKER-ROLES.md, docs/lessons/, docs/review/DIRECTOR-WORDS-* files, and recent closes in page logs, against DIRECTOR-WORDS files and STAGE-PLAN goals.
Done when: the same file's stage-goals review says, for the current stage(s), whether the goals are still right and on track, and what is done versus what is claimed done, with file:line cites.
Done when: labs/0704/WORKER-LOOPS.md describes how we build workers (Grok builders, Grok-Check, Cursor-1, Claude, Codex, cloud agents) and proposes better loops (pack/claim/return/check/signoff/close, research loop, lessons).
Done when: the report spot-checks at least three closed or returned pages' claims against the code or tests, with file:line or commit cites.
Done when: labs/0704/LESSONS.md is a short list of lessons, each with a file:line or commit cite.
Stop if: you would change any file outside labs/0704/ (the return check refuses it); you would change src/, tests/, or any code (research only); a check command has a caret, quotes, or a space inside a git grep pattern; a real drift or unmet goal is marked matched without a cite; Matthew's direction would leave the grant (stop and raise it); a rule above reads two ways. The checks only prove the files and headings exist; the checker judges the cites and the claims (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0704/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0704.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0704 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0704.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
