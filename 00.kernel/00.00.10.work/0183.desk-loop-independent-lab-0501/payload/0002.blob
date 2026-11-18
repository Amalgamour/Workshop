# Contract — desk-loop replay, 0520.desk-loop-lab/05.01

Date: 2026-10-31. Author: Grok-2. This contract is the lab's bound. It is not seated law, not an adoption, and not a release.

## 1. Place

New code lives only in `labs/desk-loop-replay-pass01`. Fixture state is a temporary directory outside `D:\Git\lib-build`. The live book `00.kernel/00.00.10.work` receives this assignment's notes, this evidence directory, the Return pointer after a successful verify, and the reserved member `0183.desk-loop-independent-lab-0501`. Nothing else in that book is written by the lab.

`0519.desk-app/05.01.md` stays unread. Its pack pin was checked as bytes.

## 2. Existing tools, called and not edited

Each call is `python -B` on the pinned file, in its own process, from `D:\Git\lib-build`.

| Step | Existing command | What it already does |
| --- | --- | --- |
| Record a job | `clerk.py queue` | Stores the supplied job and checks the instruction hash. |
| Retrieve instructions | `clerk.py claim` and `show --json` | Returns the claim token when the instruction hash still matches. |
| Submit the handback | `clerk.py return` | Writes the witness and the returned event, or refuses. |
| Reserve custody | `return_capture.py reserve` | Allocates one member in the disposable book. |
| Capture the return | `handoff.py perform` | Captures from the clerk outbox into that member and verifies. |
| Second capture attempt | `return_capture.py capture` | The helper's own conflict rule. |
| Review view | `prime_cycle.py read` | Observes the page and custody. `elected` stays null. |
| Record judgment | `prime_cycle.py record` | Checks the template binding and runs `prime_review.py report`. |
| Recover | a new `prime_cycle.py read` | Reads the files again. It does not call a model. |

Pins checked before this contract, and left unchanged: clerk `f697a7e4…`, handoff `a8380136…`, return_capture `8f3da5c6…`, return_inspect `947915fe…`, batch_observe `8bea1817…`, prime_cycle `19ede9c2…`, prime_review `805995a1…`.

## 3. Lab glue, named as glue

These steps are not existing app behavior:

- Writing the clerk job JSON, the instruction file, and the synthetic `piece.txt`.
- Writing the disposable work-book page, including a Return pointer that quotes the member and the receipt. No current tool builds that page from a capture.
- Writing `prime-cycle-registration/1`. No current tool builds a registration from a clerk job.
- Filling judgment fields on the decision template. The words are supplied by this lab. They are not a model and they are not Prime.
- Classifying each observed exit as existing behavior, glue, missing, blocked, or unverified.

The glue does not import or patch the modules above. It does not write `00.live`, elect a task, or dispatch a worker.

## 4. Disposable book

The disposable repository contains `00.kernel/00.00.10.work/0599.loop-lab/05.01.md`. Registration source is `live-file` with commit null. The clerk store sits beside that repository, outside any `.git` directory. Output and journal directories sit beside it and do not contain each other.

Capture origin is book `00.00.10.work`, page `0599.loop-lab`, batch `05.01`, retrospective false. That origin is what the existing reader uses to call a complete member the primary current candidate. A pointer that does not match stays unresolved or absent. The lab records which one it observes.

## 5. Cases

1. Supported loop. Queue, claim, return, reserve, handoff, then a new-process read before any review. Record one supplied held judgment with a next action. Read again in a new process and recover that action.
2. Worker handback without a capture. The clerk job can be `returned` while the page pointer stays `PENDING.` The cycle must not show the pass or the goal complete.
3. Identical handback. The same clerk return identity, then the same handoff binding. Record whether each one writes.
4. Changed bytes, same identity. The same clerk delivery with different artifact bytes. A second `return_capture.py capture` whose return bytes differ. Record the refusal or the defect from the tool, not a guessed safety claim.
5. Stale instruction. Change the instruction file after queue and claim. Record the refusal.
6. Stale page. After a review is committed, change the page bytes and read again. Then offer the old decision to `record`.
7. Unresolved question. Record a supplied director-input hold and an unresolved question string. Read in a new process and keep the question visible.

Each case keeps the command, the exit, and the stdout and stderr. A refused interface stays in the transcript. The lab does not invent a success for it.

## 6. Holds

AR-01 stays held. The lab does not run `inventory.py`, `worker_bridge.py`, app tests, or link-race probes. `app/` is not imported.

No model, network, Git write in `D:\Git\lib-build`, install, or edit of a pinned module.

## 7. What a green result is

Exit 0 from clerk, handoff, or prime-cycle is a shaped tool result. A verified receipt is custody. A recorded review is a supplied judgment stored by the cycle. None of these accept the work, release it, or publish it. `closes_work` stays false inside the cycle's own report.

## 8. Capture

The reserved submission is `grok-2-0520-0501`. The return file starts Did, Blocked, Need. The capture command is the one in `05.01.md`. The reservation hash is rechecked immediately before capture and the capture stops if it differs. The Return pointer is filled only after fresh verify exits 0. Review — Codex Prime stays `PENDING.`
