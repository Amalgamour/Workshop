# Return 90.50.10.0704.05.01
pack: 309bc88cabca9564972892abec0a9c8b7939b6dccc3ec587c13da9698ec1cf2a
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - Write labs/0704/DRIFT-REVIEW.md. Section "## 1. Drift": compare what was built and decided (docs/plan/STAGE-PLAN*, docs/plan/GROK-BUILDER-QUEUE.md, docs/plan/WORKER-ROLES.md, docs/lessons/, docs/review/DIRECTOR-WORDS-* files, recent closes in page logs) against Matthew's stated goals (DIRECTOR-WORDS files, STAGE-PLAN goals). List each place work drifted from, or matches, those goals, with file:line cites. Section "## 2. Stage goals": for the current stage(s), are the goals still right and on track, and what is done versus what is claimed done, with file:line cites. Section "## 3. Spot checks": independently check at least three closed or returned pages' claims against the code or tests, with file:line or commit cites.
w02: <done | need | blocked> - Write labs/0704/WORKER-LOOPS.md. Section "## 1. Workers": how we build workers (Grok builders, Grok-Check, Cursor-1, Claude, Codex, cloud agents). Section "## 2. Loops": proposals for better loops (pack/claim/return/check/signoff/close, research loop, lessons).
w03: <done | need | blocked> - Write labs/0704/LESSONS.md, a short list of lessons learned so far (what went wrong or what held, why, what to do next time), each with a file:line or commit cite (t506u).
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
