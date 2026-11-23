# Manual return (when wf is not working)

t557u (2:39 PM EST, 23 Nov 2026): "We need a process for a manual return if the compute isn't working. So what it does if the prompt and the pack don't execute correctly."

This is the process for that case. It is pending (docs/review/PENDING-RULES.md). It is not a way to skip wf when wf works.

The template is lockout/tagout. When a machine fails, you tag it out of service and record it. You never bypass the lock by hand.

## The idea

If wf fails, stop.

Do not fake a return.

Save the work and a report by hand, inside the grant.

Prima and the checker review it.

The pass never closes as passed until that check is done.

## 1. Triggers

A manual return starts when any of these happen, and one retry does not fix it:

1. A wf command errors (claim, return, verify, intake, pack, lockout, release, or any other).
2. The claim fails.
3. `wf verify` flags a hand edit.
4. A template or version mismatch. Example: the pack was made with one wf (such as 3daaa48) and the builder is running another (such as a823), so a `wf` / `wf.exe` check fails.
5. A push is rejected, and one fetch-and-retry still fails.
6. A stale `.wf-lock` is left behind, so later writes refuse.
7. The network is blocked (for example, a Codex sandbox with no git network), and wf cannot finish the step.
8. The pack does not match the repo (wrong start commit, wrong grant, or the work tree is not the packed start).

If wf still works and only the network is down, first follow labs/0705 FAILURES.md (record locally, then retry the push). Use this process when wf itself does not execute correctly.

## 2. What the builder does

Stop. Tag it. Record it. Do not bypass.

1. **Stop.** Do not keep running wf commands hoping it will go through.
2. **Retry wf at most once.** Same command, same arguments. If it fails again, stop. Do not switch wf binaries on your own.
3. **Never bypass.**
   - Never hand-edit `.workshop` logs or the `log.jsonl` hash chain.
   - Never fake a claim, a return, a check, or a close.
   - Never remove a `.wf-lock` on your own judgement (labs/0705 FAILURES.md). Tell Prima. Confirm no wf process is running before anyone removes it.
   - Never pipe or filter wf output. That can leave a stale `.wf-lock`.
4. **Record the failure.** Write down the exact command, the exit code, the full error text, the wf commit it was built from, and the OS.
5. **Keep the work inside the grant only.**
6. **Commit on the `returns` branch.** Stage files by path only (never `add -A`, never `commit -a`). Use the trailer `Builder: <name>`. Never force push.
   - The work stays in its granted paths. That commit is the work.
   - The report path is fixed: `reports/<page>/05.NN/<Builder>-MANUAL-RETURN-<stamp>.md`.
   - The stamp is `YYYYMMDD-HHMM` in the machine's local time (America/Toronto).
   - Do not write under `.workshop/`.
   - Do not make a second copy of the code somewhere else.
7. **Write the report** with these fixed fields:
   - page
   - pass
   - builder
   - pack hash
   - start commit
   - the failing step
   - the error (command, exit code, full text, wf commit, OS)
   - what was done
   - files touched
   - test results
   - the code commit
8. **Push** that commit to `returns`. If the push is rejected, fetch origin returns and try again once, still never force.
9. **If the push fails too**, paste the full report to Matthew in one block. A paste is only a last resort. It does not close the pass. It does not replace the GitHub record. Prima or Matthew commits it to `returns` when they can.

The builder keeps the page while the manual return is open. This is not a handover to another builder.

## 3. What Prima and the checker do

1. Confirm the diff stays inside the grant: `git diff <start-commit> <code-commit>`. Name any path outside the grant. That is a fail.
2. Run the tests.
3. Confirm the log chain was not touched. No hand edit of `.workshop/logs` or `log.jsonl`. `wf verify` may be used when wf can run.
4. Then pick one path:
   - **Fix wf, then re-run the normal intake** for the same pass. The builder's work commit is the return body. wf records the intake once it can.
   - **If wf cannot be fixed soon** (Prima or Matthew decide), wait until wf works, then record a manual intake through wf, with a note saying it was a manual return.
5. A manual return never closes as passed without the checker's review.
6. The wf failure itself becomes a bug note or a page, so the same break is fixed, not bypassed next time.

## 4. The lock and the hold

The template is lockout/tagout (t541u, page 0423).

When equipment fails, you tag it out of service and record it. You never run it by hand around the lock.

- The builder who was working keeps the page while the manual return is open. No other builder takes it. This is not a handover (t547u). An incoming worker who sees an open manual-return report must stop and raise it.
- The face lock is released by the manual-return record. That ends the work session. Prima and the checker may then review, as they would after a normal release.
- Until 0423 exists, there is no `wf release` command. The report is the release record, the same way t547u uses a published note until 0423 lands.
- Do not leave a hidden local claim. Do not push a late local claim after writing the report (t547u).
- Only Prima or Matthew may clear an abandoned manual-return tag, with a reason, if the builder has gone. That is the same authority as an abandoned-lock override (t541u). Once page 0425 records the book's Prime, that Prime may do it too.

## 5. Paste-ready block

Prima adds this block at the end of every builder prompt from now on:

```
MANUAL RETURN (docs/plan/MANUAL-RETURN.md). If wf fails:
1. Stop. Retry the same wf command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, the wf commit it was built from, and the OS.
4. Keep all work inside the grant. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: <name>" to returns. Do not write under .workshop/.
5. Write reports/<page>/05.NN/<Builder>-MANUAL-RETURN-<stamp>.md with: page, pass, builder, pack hash, start commit, failing step, error, what was done, files touched, test results, and the code commit. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block. You still hold the page. The report releases the face lock. This is not a handover. A manual return never closes as passed until the checker reviews it.
```

## Questions for Matthew

Q1. Is the fixed location on returns just the granted file paths, plus the report at `reports/<page>/05.NN/`?

- Recommended (default): yes. The work stays in the grant. The report is the record. Do not add a second copy of the code.

Q2. The record releases the face lock, but the builder still holds the page. May the checker enter while that tag is open?

- Recommended (default): yes. Prima and the checker may review, as after a normal release. No other builder may claim the page until the tag is cleared, after intake, or by a recorded override.

Q3. Lab 0705 said a pasted report must not stand in for a push, because it is not in the hash chain. This process allows a paste when the returns push also fails.

- Recommended (default): a paste is last resort only. It does not close or intake the pass. Prima or Matthew commits the report to `returns` when they can. A paste alone is never a passed close.
