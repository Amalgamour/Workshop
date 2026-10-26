# plan.4 source of truth

Authorization: draft — 2026-10-15
who: claude-opus-5-5
state: draft
page: 1008.app-plan
why: Where each kind of thing lives, what may change it, and what the app guarantees against what a model is only asked to do.

## Where things live
| kind | where | authoritative? |
| --- | --- | --- |
| Rules (syntax and law) | `00.00.00.kernel.draft`, seated faces `FF.md` | Yes. The working reference. `00.00.00.kernel` is stale and not used. |
| Local rules of a book or shelf | its `00.axioms` and local pages, when present | Yes, for that place. Looked up book, shelf, desk, kernel (`05.03` #05). |
| Content of a book | its page folders, seated faces `FF.md` | Yes, for that book (local governs downward, law `0055`) |
| Drafts | `FF.VVV.md` beside the seat (`05.02` #06); older `FF.VVV.draft.md` still read | A proposal. Never governs until approved. |
| Retired faces | `00.retire.09` in the book, `FF.VVV.09` | History. Read-only. Never governs. |
| Work, stops, findings, decisions | face `05` batches `05.NN.md`: the `#NN` line, your `reply:`, the worker's `status:` | Your reply is the decision. The file is the record. |
| Commands a line may ask | the desk command list (`05.03` #06) | Yes. A command not on it is kicked back. |
| Grants | a batch line at the desk naming the shelf or book it covers (`05.03` #04) | Yes. A worker write outside its grant is kicked back. |
| What a page is doing and why | face `01` of that page | Yes, for that page |
| Notes and history of a page | face `06`, `## Note` and `### notes` sections | History. Not rewritten. Later marked `applied:` (`05.02` #07). |
| Worker rules | `AGENTS.md` (the seat); drafts `AGENTS.VVV.md` beside it | The seat governs. A draft governs nothing until the Director seats it. |
| Planning and design of the app | this page, and band `2000` members | Draft until you sign. |
| App code | `app/` (`05.01` #01) | Code. Versioned by git. |
| App state | `.librarian/`, outside git (`05.01` #12) | No. Convenience and undo only. |
| Search index (later) | `.librarian/index.sqlite` | No. Rebuilt from the files at any time. |
| History | git: work branches for model commits, `main` for what you merged (`05.01` #07) | `main` is the approved record. A branch is work waiting for review. |

**Rule:** if a fact is not in a tree file, it is not true for Librarian. The app may cache, but any cache can be deleted and rebuilt with no loss. A future move to a database as the truth (your note on `1006.redraft/05.10` `#17`) would be its own decision with its own migration stage (`05.01` #02).

## Batches
A batch is the review queue. All work a model does, every stop, every conflict, every idea found during work is a `#NN` line on a `05.NN` before or as the work happens. Nothing a model does should exist only in a file it changed.
- **One name:** `05.NN.md`, never renamed. State in the header: `open`, then `ran` (`05.02` #01). Old forms are read, not renamed.
- **The shape is `1006`'s:** the header (`Overview`, `Learned`, `How`, `Scale`); each line `#NN >command subject`, `issue` when there is a conflict, `recommend`, `Ask: >command` with the reason, `path`, `scale`, `reply:`, `status:`.
- **The command is the kind** (`05.02` #02). It comes from the desk command list. `>note` is a finding. `>stop` is an escalation and is shown first.
- **A wrong decision** goes into the next batch as a line with `reason: From 05.NN #NN`. The old line keeps its reply and gets `status: next. … Carried to 05.NN #NN.` (the form `jobs.py carry` checks).
- **A page that is a piece of work** (your timer example, `1006.redraft`): face `01` says what and why and the current state; each `05.NN` is a round; face `06` holds notes.

## Grants and solo work
- **Grants follow the structure** (`05.03` #04). The desk grants a worker a shelf or a book, on a batch line, and can withdraw it the same way. The app checks every worker write against the grant that covers its location and kicks back anything outside it, with the reason.
- **`reply:` comes only from the user side of the desk** (`05.02` #03). The app refuses a reply through any model command.
- **Solo work:** under a grant, a model skips the reply, works through the batch, and writes the `status:` after each line. A blank reply with a status is the solo mark. If you reply during the run, the model follows your reply. Your reply afterwards is the review: `>take`, or a correction carried to the next batch.
- **Without a grant,** a blank reply waits, as AGENTS says.

## Edits
In the first version the app makes six kinds of write, and no other:
| write | who uses it | rule |
| --- | --- | --- |
| New page folder with faces `01` and `08` | model (`page new`) | Only inside a granted shelf or book; lowest open slot; never into an existing folder |
| New batch `05.NN.md` | model (`batch new`) | Next free `NN` on that page; never over an existing file |
| Line appended to an open batch | model (`item add`, `stop`) | Only to a batch with `state: open`; command on the desk list; appended at the end |
| Status | model (`status`) | After the whole reply; or under a blank reply inside a grant (solo) |
| Reply | you (`reply`, the screen, or `confirm` for replies you wrote in a file) | Only into a blank `reply:`; only from the user side |
| Commit on a work branch | the app, when a status closes a line | Only on the branch the job names or the page has set (face `01` or batch header); only the files that line names; message names the `#NN`; never on `main`. No named branch: no commit, a `>stop` |

You may also edit `05.NN` files directly (dev mode, `05.01` #06). Workers may still edit other files directly, as today (drafts, code). Those changes show up in "unseen work" unless a batch line names them. Nobody, app or model, overwrites a seat in place. Approve is a rename (law `0022`), and it is yours. Merging into `main` is yours.

## Checks before a write is accepted
The `write` and `batches` modules refuse unless every check passes. The refusal names the check. Anything that violates the design is kicked back.
1. **Zone.** Inside the repo; not inside `00.00.00.kernel` or `00.00.00.kernel.draft` (first version); not inside `.git`; not a retired `.09` file.
2. **Grant.** For a worker write: inside the shelf or book its grant covers.
3. **Kind.** The write is one of the six above.
4. **Command.** A new line's command is on the desk command list.
5. **Version.** For a change: the file's hash equals the hash when it was read. For a new file: the file does not exist.
6. **Target.** The `#NN` exists once; for a reply, its `reply:` is blank and the writer is the user side; for a status, the reply is filled, or a grant covers the location; for an appended line, the batch is `open`.
7. **Shape.** No line of the new text starts with `#` plus two digits, `reply:`, `status:` or `Authorization:` unless that line is the one being written. Valid UTF-8.
8. **Only the intended bytes changed.** The app compares old and new before the swap. Line endings are kept as found.
9. **Swap and re-read.** The temp file replaces the old one in one step. The app reads it back and compares the hash.
10. **Journal.** The before-copy and the record are saved before the swap. If the journal cannot be written, nothing is written.

## Version checks, recovery, backups
- **Version check:** SHA-256 of the raw bytes, the identity `clerk.py` and solo `face.py` already store.
- **Undo of an app write before a commit:** `librarian undo` restores the before-copy of the last write, only if the file still has the hash the app left. Otherwise it shows both and asks you.
- **After a commit:** git. A line's work is one commit on its branch; it can be reverted on its own.
- **A stage that went wrong:** do not merge its branch; or, after the merge, revert the merge.
- **Crash mid-write:** the old file is untouched until the swap. A leftover temp file is reported on next start.
- **Lost app state:** delete `.librarian/` and restart. You lose "since last visit", the undo copies and the reply confirmations. The tree and git are unchanged.

## Discussion, proposal, decision, execution
| state | what marks it on disk | what the app shows |
| --- | --- | --- |
| Discussion | text with no `#NN >` | nothing in the batch views |
| Proposal | `#NN >command` with a blank `reply:` | **waiting on you** |
| Stop | `#NN >stop`, blank `reply:` | **stopped, needs you**, at the top |
| Solo work | blank `reply:` with a `status:`, inside a grant | **done, waiting for your review** |
| Decision | your nonblank `reply:` | **replied**. The app does not decide if a reply releases, rejects or defers. The worker reads it, as AGENTS step 4 says. A reply not written through your side is listed until you confirm it. |
| Execution | `status:` after the full reply, and a commit on the work branch | **closed** or **carried**, with who, when and the commit |
| Approved record | the branch merged into `main` | **merged** |

## Guarantees and instructions
| the app guarantees (code enforces; a test proves it) | models are asked to (AGENTS; the app cannot enforce) |
| --- | --- |
| It never writes inside either kernel in the first version | Never edit `rules.toml` or `moves.toml` unless named |
| It never writes over a file that changed since it was read | Reopen the page before a write |
| It never changes a reply that is not blank | Never remove or replace a Director reply |
| It refuses a reply from any model command | Never write `reply:`, by any means |
| It never changes bytes other than the ones it was told to add | Append status after the whole reply |
| It refuses a worker write outside its grant, and a command not on the list | Record every piece of work as a `#NN` before or as it is done |
| It commits only on the named work branch, only the files a line names, never on `main` | Never commit on `main`, never merge (AGENTS.003, once seated) |
| Every app write has a before-copy and a record | Never approve, sign, lock, promote |
| It never runs `lcheck.py` with `--fix-sentinel` or `--write-moves` | Use the job's scope only |
| It **detects** a reply that did not come through your side, and a reply of yours later changed or removed | Use `librarian` commands for batch writes (AGENTS.004, after stage 3) |
| It **detects** changed files that no batch line names | Escalate with `>stop` instead of guessing |
| Its index and caches can be deleted with no loss | Say "not verified" when a check could not run |

The left column is the app's promise and each line has a test. A model that edits a file directly, around the app, is not stopped. It is caught after the fact by the reply check and the unseen-work check, and its branch does not reach `main` until you merge it.
