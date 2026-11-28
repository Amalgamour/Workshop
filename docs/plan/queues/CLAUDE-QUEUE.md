# Claude queue

Plan doc. Written by Prima on Sat Nov 28 2026 (t599u). It lists the packs of work page docs/plan/WORK-PAGE-2026-11-30.md in the order they go out, with each one's status.

Status words:
- done: returned and on returns.
- batch 1: goes out first. Matthew pastes each prompt himself.
- ready: the prompt is written and nothing blocks it. It goes out when its batch comes up and Matthew says so.
- held: the prompt is written, but the pack waits for the thing in the last column.

Prompts: docs/plan/queues/CLAUDE-PROMPTS.md. Order follows docs/plan/WORK-PAGE-2026-11-26-WEEK.md, section 7, with the changes in the notes below.

| Order | Pack | Batch | Status | Folder | Report file | Waits for / return |
|---|---|---|---|---|---|---|
| 1 | C1 | done | done | labs/review-stage1-route/ | reports/lab/review-stage1-route/Claude-20261125-1450.md | returns 128a541b28a6456d01a0f2a09ca362e0216d5e3e |
| 2 | C2 | 1 | batch 1 | labs/review-stage1-route/ | reports/lab/review-stage1-route/Claude-C2.md | - |
| 3 | C3 | 1 | batch 1 | labs/draft-page/ | reports/lab/draft-page/Claude-C3.md | - |
| 4 | C21 | 1 | batch 1 | labs/ui-scaffold/ | reports/lab/ui-scaffold/Claude-C21.md | - |
| 5 | C8 | 2 | ready | labs/delegated-grant/ | reports/lab/delegated-grant/Claude-C8.md | - |
| 6 | C9 | 2 | ready | labs/delegated-grant/ | reports/lab/delegated-grant/Claude-C9.md | C8 returned |
| 7 | C20 | 2 | ready | labs/draft-page/ | reports/lab/draft-page/Claude-C20.md | X2 returned |
| 8 | C4 | 3 | held | labs/pin-record/ | reports/lab/pin-record/Claude-C4.md | Matthew answers work page question 2, or says to use its default |
| 9 | C5 | 3 | held | labs/pin-record/ | reports/lab/pin-record/Claude-C5.md | C4 returned |
| 10 | C6 | 3 | held | labs/pin-move/ | reports/lab/pin-move/Claude-C6.md | C4 returned |
| 11 | C7 | 4 | held | labs/pin-move/ | reports/lab/pin-move/Claude-C7.md | C6 returned |
| 12 | C10 | 4 | ready | labs/overlap-check/ | reports/lab/overlap-check/Claude-C10.md | - |
| 13 | C11 | 4 | ready | labs/overlap-check/ | reports/lab/overlap-check/Claude-C11.md | C10 returned |
| 14 | C12 | 5 | ready | labs/stale-pack/ | reports/lab/stale-pack/Claude-C12.md | - |
| 15 | C13 | 5 | ready | labs/stale-pack/ | reports/lab/stale-pack/Claude-C13.md | C12 returned |
| 16 | C14 | 5 | ready | labs/retire-0409/ | reports/lab/retire-0409/Claude-C14.md | - |
| 17 | C15 | 6 | ready | labs/retire-0409/ | reports/lab/retire-0409/Claude-C15.md | C14 returned |
| 18 | C16 | 6 | ready | labs/catch-log-flow/ | reports/lab/catch-log-flow/Claude-C16.md | - |
| 19 | C17 | 6 | ready | labs/catch-log-flow/ | reports/lab/catch-log-flow/Claude-C17.md | C16 returned |
| 20 | C18 | 7 | ready | labs/prompt-check/ | reports/lab/prompt-check/Claude-C18.md | - |
| 21 | C19 | 7 | ready | labs/prompt-check/ | reports/lab/prompt-check/Claude-C19.md | C18 returned |

## Notes

- C1 is done. It ran as the first undone pack when its prompt had a blank (catch log row 17).
- Batch 1 is C2, C3 and C21, not C2, C4 and C5. C4 and C5 write down where the live wf build is recorded. That is work page question 2, and Matthew has not answered it. C3 helps him answer it. C21 fixes Claude's own UI-1 errors and needs no answer.
- C20 answers Codex X1 and X2, so it waits for X2 to return.
- C4 to C7 wait for question 2. If Matthew says "use the default", they run on option A (one line on face 08 of door 90.50.10.0400).
- Claude has no close, signoff or pack authority. Every Claude pack is "not usable until checked". Codex checks them in X21 to X24.
- C8 and C9 are spec and test plan only. Option C is not decided (t584u).
- Batch numbers are a plan. Prima may move a pack when an answer arrives. Each change is written here.

