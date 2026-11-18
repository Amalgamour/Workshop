# N7-local exchange contract (0707/05.20)
who: claude-opus-5-5 · state: **PROPOSAL plus a tested prototype. Not production; not selected.**

## Director's words (verbatim, 06.19.director.md)
"To confirm N7 is the colab band correct?  So how it's supposed to work is a tail of pack or return after the 05.NN so a 05.01.pack must exist before the 05.01.return can exist  It's a self contained system for N7 vs the paired model of N5 to N1."

Everything below is my interpretation, tested on copies. It is not the Director's text.

## The exchange (N7NN only)
`{page}/05.NN.pack.md` → `{page}/05.NN.return.md` → `{page}/06.NN.review.md`, on ONE book instance.

**Identity:** intake field `exchange`, schema `n7-local-exchange/0`.
| Field | Meaning |
|---|---|
| `route` = `n7-local`; `n1_custody` = `not-applicable` | N1 is not part of this route. N1 absence is never an N7 finding. |
| `book` | the resolved book path (the instance) |
| `page`, `pass` | the requested address; **never inferred** from the highest filename or nearby files |
| `pack.path`, `pack.sha256`, `pack.body_sha256`, `pack.bound_sha256` | body = bytes before `## Return pointer` (the task); bound = body + pointer (before the first `## Review`) |
| `return.path`, `return.sha256` | exactly `{page}/05.NN.return.md` |
| `declared_submission` | what the pack's pointer declares (the pass04 grammar) |
| `destination` | `{page}/06.NN.review.md` (unchanged derivation) |
| `state` | `matched` · `orphan-return` · `pack-missing` · `pointer-pending` · `return-not-local` · `assignment-not-pack` |
| `chronology` | `recorded-before-return` (an `open` record of this pack body made while no return existed) · `unverified` (no such record: all historical pairs) · `open-record-mismatch` (the body changed since opening) |
| `unfiled_return_preserved` | a return file is present but not matched; its bytes are left untouched and reported |

## What binds a return to its pack
1. The pack is `{pass}.pack.md` on the same page, in the same book instance.
2. The pack's own pointer declares the return, with a hash and a length, and **the declared path equals `{page}/{pass}.return.md` exactly.** A basename match elsewhere is refused (H2), and another pass's return is refused (T2 wrong-pass).
3. The declared evidence is measured as today (manifest rows, hash/length).
4. **Freshness** binds the pack's bound region, the return, the manifest and the artifacts. The pack's own Review section is excluded (H1); everything else is not.
5. **Book instance:** a stored intake whose book differs from the live book is stale (T2f).

**Not binding:**
- the file name alone;
- mtime or dates;
- the "latest" or highest pass.

## States and transitions (current tools, with only the overlay's additions)
| Step | Rule |
|---|---|
| **prepare** | intake plus exchange. Any non-`matched` state adds `n7-exchange-<state>` and makes measurement `incomplete`. Nothing is written. |
| **record** | **unchanged code:** an incomplete intake is refused, and the supplied judgment is kept in `failed/`. A matched intake records with mode `preliminary` (an existing label; for N7 it means "no cycle route", **not** "N1 missing"). |
| **inspect** | the full read, including `rendered` |
| **publish** (separate command) | **unchanged code.** Absent destination: the file is created. Present manual text: held as `manual-review`. A target that appears after inspect: held. A changed source: held. |
| **read / recover** | unchanged. Repeat calls are byte-equal with no writes. |
| **open** (new, lab CLI) | records the pack body hash and `return_present` once (exclusive write). The only chronology evidence the overlay accepts. |

**Separate axes, never merged:**
- local exchange state;
- record mode;
- publication;
- Director approval;
- release;
- work completion.

Filing or publishing grants `accepted`/`approved` false, `authority` none, and `closes_work`/`releases_action` false (T1).

## Bounds and guarantees
- **The observation window** is each command's own read. There is no lock: a change between two commands is caught by the next command's freshness check (T3), not prevented.
- **No concurrency, power-loss or AR-01 claim.**
- **Transport versus semantics:** the supplied judgment is compared canonically (equal JSON). Raw judgment-file bytes are not claimed (as 06.19.review asked).
- **Capacity (24 sources) and the strict grammar (A-01/A-02) are unchanged.** Positive cases use valid syntax and small fixtures.

## Documented label left unchanged (production change needed)
- The record field `custody` (pass02 `do_record`: "measured" if a cycle committed, else "missing") and its rendered line `custody: missing` (pass01 `render_body`) still say `missing` for N7.
- Production should write `not-applicable` for N7 records. **This is a shared-schema value addition, at those two functions.** The prototype does not rewrite `do_record` at runtime.
