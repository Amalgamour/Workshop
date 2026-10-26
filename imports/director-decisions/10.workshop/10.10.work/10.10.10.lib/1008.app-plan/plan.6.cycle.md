# plan.6 cycle

Authorization: draft — 2026-10-15
who: claude-opus-5-5
state: draft
page: 1008.app-plan
why: The loop every batch follows, who decides what, and the defaults that do not need your approval.

## The loop
1. **Plan a bounded batch.** The model places a `05.NN` batch on the page of the stage, using the `1006` form: the batch header (`Overview`, `Learned`, `How`, `Scale`), then each line as `#NN >command subject`, `issue` when there is a conflict, `recommend`, `Ask: >command` with the reason, `path`, `scale`, blank `reply:`. The command is the kind and comes from the desk command list. One `#NN` is one piece of work. Work is batched before or as it is done, never only after (plan.4, Batches). The `Ask` names the files it will touch and the test that proves it.
2. **You reply.** Your reply is kept whole. A blank reply waits. A reply may take, change, hold, or reject. Under a grant that covers the location, the model skips the reply, works through the batch, and writes the status after; your reply later is the review (plan.4, Solo mode).
3. **Implement.** The model reads the module page and the kernel page it comes from, reads the existing code first (your rule: reference what exists before building), and writes only inside the scope the reply released. If something stops it, it adds a `>stop` line saying where it stopped, what it had planned, and what it needs, and does not guess. A conflict or idea found on the way becomes a `>note` line.
4. **Test.** The model runs the app tests and the common gate in plan.5, and pastes the real output. If Python could not run, it writes "not verified" and stops short of "done".
5. **Report.** Under your reply, after the whole of it: `status:` with what changed (files), why (which `#NN`), what was noticed and not touched (overflow), what it was unsure of. This is AGENTS Report.
6. **Review.** You read the report and run the demo. You reply on the same `#NN` or a new one: accept, or a correction.
7. **Correct.** A decision that proves wrong goes into the next batch: a new line with `reason: From 05.NN #NN`, and the old line gets `status: next. … Carried to 05.NN #NN.` A reply is never edited.
8. **Accept and preserve.** Each closed line was committed on the work branch, its message naming the `#NN`. You merge the branch into `main`. The batch is filed as `ran`. Anything learned that should outlive the batch goes onto the module page's `## Note`, dated, with its source.

Where this lives: each stage gets a member in band `2000` (for example `2006.batch-desk` for stages 1 to 3). Its face `01` says what compute fills, what the model fills, and the test, as `2001.page.README` asks. Its `05.NN` files are the batches. This page, `1008.app-plan`, stays the plan and is updated only by its own batches.

## What the model handles alone
Inside a released `#NN`:
- Code structure, names of internal functions and files inside `app/`.
- Which existing function to reuse, and how to wrap it, as long as the original file is not edited.
- Test design and fixtures.
- Small refactors inside `app/` that keep every test passing.
- Error messages and help text.
- Fixing its own bug found during the same batch.

## What comes to you
- Anything that changes what the app writes, where, or when.
- Anything that changes a rule, a kernel page, `AGENTS.md`, `rules.toml`, or `moves.toml`.
- New dependencies (a new library to install).
- Moving to the next stage.
- Anything that costs money (paid services, paid model calls from the app).
- A conflict between two faces (filed as a hole, never picked by the model).
- Retiring an existing tool (`clerk.py`, `face.py`, `jobs.py`).
- Merge into `main`, sign, approve, lock, promote. Always.

## Defaults (no approval needed unless you object)
| topic | default | why |
| --- | --- | --- |
| Language | Python 3.14, the version installed | All existing tools are Python |
| Packaging of the code | one package `librarian` under `app/`, with `app/tests/` | One program instead of twelve scripts |
| Tests | `pytest` (see `#04`), with fixtures made by hand in `app/tests/fixtures` | Standard; readable output |
| Code style | the existing scripts' style: short docstring, `## notes` comment with born, source, who | Matches the tree; carries the why |
| Text encoding | UTF-8 read and write; line endings kept as found | AGENTS step 7; `clerk.py` CRLF lesson |
| Hash | SHA-256 of raw bytes | Already used by `clerk.py` and `face.py` |
| Output | plain text by default, `--json` on every read command | Models and scripts read the same thing |
| Dates | ISO dates, local time, as the batches already use | Matches `placed:` and `created:` |
| `who` | always passed in; no default name in code | Return hole 6 |

## Signals that a batch is too big
Over about 400 lines of new code, more than one module, or a test that cannot be shown in the report. Then the model splits it into two `#NN` before starting.
