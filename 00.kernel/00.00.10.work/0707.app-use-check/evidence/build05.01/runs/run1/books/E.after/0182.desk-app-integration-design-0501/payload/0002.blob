# Desk app core: integration design (0519.desk-app 05.01)
date: 2026-10-31
who: claude-opus-5-5 (Claude), Colab/design; reviewer Codex Prime
state: proposal. Not seated, not released, not implemented in app/.
Sources: pack05.01 (51 pins verified). Clarifications received during the assignment, and acknowledged: 0519/06.02 with 0416/06.04 (the Director selected Prime's return-review cycle; compute constructs its pages/faces from structured inputs), and 0519/06.03 with 0416/06.05 (Grok-2 owns the broad execution/replay lab on 0520; this design does not duplicate it).

## 1. The first workflow
Prime reviews one builder return:

> **assignment recorded → worker retrieves → durable return → Prime retrieves and reviews → next action survives restart**

Every step already has a working tool, except two things:

- **Nobody can ask "what is waiting, and for whom".** `where` is down on the live record, and status tools need hand-kept registries.
- **The records that connect the steps are hand-typed at addresses that vary.** These are the Release, Claim and Execution lines, and the review.

The smallest core therefore adds:

- one read-only desk view over existing records;
- one constructor for the few records the loop types by hand;
- one fixed review address.

It adds no new store, no queue, no service and no model launch.

## 2. Authoritative records (all existing; none new)
| Fact | Record | Written by | Read by |
|---|---|---|---|
| Task and its instructions | `<lane>/05.NN.md` assignment region (bytes before `## Return pointer`) + `evidence/pack05.NN/source-manifest.json` | Prime (constructed from an assignment spec, §5) | worker, view, review |
| Who returns, to whom, which outputs | `01NN.<slug>/reservation.json` | Prime via `return_capture reserve` | view (open-task index) |
| Release | `Release:` line in the Return pointer, verbatim words of the Director | constructed from the relayed text | view, worker |
| Claim | `Claim:` line binding `assignment-sha256` | constructed for the worker | view (stale check) |
| Return and evidence | `01NN/return.md`, `payload/`, `manifest.json`, `receipt.json` | worker via `return_capture capture` | Prime, view via `return_inspect` |
| Execution pointer | `Execution:` line with receipt and manifest hashes | constructed from `return_inspect`, never typed | view, human reader |
| Review and next action | `<lane>/evidence/prime-review05.NN/<review_id>/record.json` + `REVIEW.md` + `COMMITTED.json` | Prime judgment via `prime_cycle record` | view, Prime, next worker |
| Review pointer on the page | one constructed line under `## Review — Codex Prime` naming the record and its sha256 | constructed | human reader |

`0401.goal/06.01.md` and `00.live.md` are notes and views. They are not authorities for this loop (§9, D5).

## 3. Interfaces
CLI first, through `app/librarian.py`, wrapping pinned modules as the app already does. Exit codes follow the existing convention: 0 ok, 1 attention, 2 refused.

```text
librarian.py desk [--as SEAT]... [--json]                    read-only view: tasks, state, actor, next   (G1)
librarian.py task show --member 01NN.slug [--json]           worker: page path, assignment sha256, outputs, capture command (G5)
librarian.py task release --member M --by TEXT --quote-file F   constructs the Release line (G5)
librarian.py task claim   --member M --as SEAT                  constructs the Claim line with assignment-sha256 (G5)
librarian.py task submit  --member M --return-file F --artifact REL|LOGICAL...   capture + verify + Execution line (G5)
librarian.py review open  --member M                            derive the review registration; write the template (G4)
librarian.py review record --member M --decision FILE           prime_cycle record at the fixed address + page pointer (G4)
librarian.py assign --spec FILE                                 page + reservation + registration entry from one spec (G2/G4)
```

- **Models and the Director use the same commands.** A model passes `--json`. A person reads the text output.
- **The browser UI is a later candidate.** It would be a renderer of `desk --json` with buttons that call the same commands. It does not duplicate working CLI code, and it is not needed for the first handoff.

## 4. Module ownership and dependency identities
| Module | Owner | Status | Used for |
|---|---|---|---|
| `return_capture.py` 8f3da5c6… / `return_inspect.py` 947915fe… | labs/return-capture-pass01 | accepted | custody |
| `batch_observe.py` 8bea1817… | labs/batch-observation-pass01 | accepted | page lines |
| `prime_cycle.py` 19ede9c2… | labs/prime-cycle-pass01 | accepted for bounded use (0515/05.03) | typed review; binding change in G3 |
| `prime_review.py` 805995a1… | labs/prime-review-pass01 | accepted | report shape and holds (inside prime_cycle) |
| `clerk.py` f697a7e4…, `handoff.py`, `prime_support.py` | labs | accepted (fixture-only) | **not used in slice 1** (§8) |
| new `app/desk_view.py` | G1 | proposed | the view |
| new `app/construct.py` | G2 | proposed | templates |

The app pins every module by path and sha256 before launch, as `app/*.json` do now. There is no highest-version discovery.

## 5. Compute construction (the Director's 0416/06.04 decision)
Models supply content and judgment. Compute supplies addresses, hashes, layout and required fields. The minimum templates for this loop, all demonstrated in `labs/desk-app-integration-pass01/desk_lab.py construct`, are:

1. **`assignment-spec/1` → `batch-page/1` + reservation + registration entry.** Prime writes one JSON with these fields:
   - title, lane, pass, executor seat and reviewer;
   - goal, steps and allowed writes;
   - the expected outputs;
   - the agreement: goal, scope, Prime discretion, Director-required items and finish criteria.

   From it compute renders `05.NN.md`, calls `reserve` with the same outputs, and emits the prime_cycle registration entry. Page, reservation and review registration then cannot disagree. The lab demonstrated the page and the reserve. The registration emission is the G2/G4 contract.
2. **`return-pointer/1`.** Three kinds:
   - `release`: the verbatim quote, the relayer and the date;
   - `claim`: compute adds `assignment-sha256`;
   - `execution`: compute reads the receipt, manifest, payload count and status from `return_inspect`, and refuses unless the status is complete.
3. **`review-section/1`.** One pointer line set derived from the committed `record.json`: disposition, terminals, next action and the record's sha256. Prime supplies a one-line summary only.

**Rules (all demonstrated):**
- **Compare-and-swap.** `--expect-sha256` must equal the current bytes. A stale hash is refused (lab 3c).
- **Edits are bounded.** Construction may create an absent file, replace a declared `PENDING.` placeholder, or append inside the declared section.
- **Bytes outside the section never change.** The check runs before writing, and anything that would remove non-placeholder text is refused (lab 8c).
- **Writes are temporary file, then rename.** The target is rechecked just before the rename. A change seen there leaves the temporary file and the target untouched. This narrows the same-user race; it does not close it.
- **Captured returns are never rewritten.** Construction does not touch `01NN` members.
- **Construction is not release, approval or acceptance.**

A universal face builder is not needed first. The next templates, after this loop works, are the 06 notes face, the source manifest and the 0401 note (§9).

## 6. State, errors and the next actor (derived per read)
| State | Condition | Actor | Next |
|---|---|---|---|
| awaiting-release | reserved; no `Release:` line | director | release words recorded |
| released | Release, no Claim | submitter | claim, work |
| claimed | Claim present; custody reserved | submitter | capture, verify |
| custody-problem | inspect incomplete or refused | prime | inspect; partial is evidence, not a return |
| awaiting-review | complete; no current review at the fixed address | reviewer | review |
| reviewed | committed typed review whose binding holds | next action's author | the typed next action |
| review-stale / review-unusable | binding changed or record altered | reviewer | successor review |
| superseded | a later reservation names this member in `supersedes` | none | read the successor |
| reviewed-untyped | legacy prose review (any of the three old addresses) | none | not machine-readable |
| historical-capture | retrospective capture | none | none |

Attention items do not change the state: assignment changed after claim, a page receipt differing from custody, more than one Release line, and an unobserved page.

**Missing versus done.** A reserved member is never done, whatever the page says. A page claiming a receipt that custody does not hold is attention. Shown in lab steps 4a and 4b.

## 7. Approval and release versus receipt
- **A receipt** says the copy is intact.
- **A review record** says what Prime judged. Its `closes_work`, `releases_action` and `authenticates_actor` are always false (prime_review).
- **A Release line** records words the Director gave. It is not verified.
- **Approval, seating and merge** stay the Director's acts. No state in §6 means approved.

## 8. Why not Clerk, a service or a database in slice 1
- **Clerk** is a second job ledger beside reservations, and its store is refused inside any Git tree. It cannot be the durable work-book record without a publication step. Keep it for later routing (inboxes and handoffs between seats).
- **A local service or database** would hold state the work book does not have. That contradicts "the files are the only memory" and the restart goal.
- **The view is about 30 s over 83 members** (one subprocess per inspect and per page). That is acceptable for a pull-based desk. A cache, if ever needed, is a derived file with its inputs' digests, never an authority.

## 9. Source revision binding, restart and partial writes
- **Claim** binds `assignment-sha256`, the bytes before `## Return pointer`. Edits after the claim are attention (lab 10d). Pack sources stay pinned by the manifest.
- **Review must bind** the assignment-sha256, the receipt sha256 and the agreement, **not the whole page**. Lab 8b reproduced the conflict: prime_cycle binds the whole page sha256, so writing the review pointer, or any later Return-pointer line, makes the review stale. G3 changes this with a new record version that keeps /2 records readable.
- **Restart.** All state is files. Fresh processes derive identical state digests (lab 9a and 9b).
- **Partial writes.** Completion markers already exist for every write that matters:
  - `receipt.json` last (return_capture);
  - `COMMITTED.json` last (prime_cycle);
  - temporary file plus compare-and-swap rename (construct);
  - the Clerk witness (not used).

  A partial is evidence, shown as custody-problem or partial review, never repaired silently.
- **Concurrency is real.** Between two read-only live views, other lanes wrote 70 files. Compare-and-swap on every page write is required, not optional.

## 10. Trust assumptions, stated plainly
- Labels, seat names, `--as` and Release text are not authentication.
- All tools run as one Windows user, and there is no OS sandbox. Path checks are integrity, not confinement.
- A same-user process can rewrite any record. Hashes detect isolated changes, not a coordinated rewrite.
- Registration of a session is a record, not enforcement.
- No enforced isolation is claimed.

## 11. Findability in the work book
- **Task:** the reservation names the page, the page holds the instructions.
- **Return:** the member named by the reservation, and pointed to by the Execution line.
- **Evidence:** the member's payload and the lane's `evidence/buildNN.NN`.
- **Review:** `<lane>/evidence/prime-review05.NN/<review_id>/`, pointed to by the page.
- **Next action:** inside that record, listed by `desk`.
- **Chat:** nothing lives only there. The release words are copied into the Release line, and each Director clarification is a page (as 0519/06.02 and 06.03 already are).

## 12. Live findings that the design answers
- **F1. `where` is down.** `assignment_state: prepared` is not in context.py STATES. Fix: G0.
- **F2. Pack-template pages read as ambiguous to batch_observe.** On 0519 the cause was verified: the template line "Release and claim: recorded in the Return pointer" matches the Release prefix, so `release_raw` is null. In the live view 78 of 83 tasks sit on pages with at least one reader ambiguity. I did not classify the cause on the other pages. Fix: the constructed page phrases it "The release and the claim are recorded…" (G2). The lab's constructed pages carry no such line.
- **F3. Review lives at three addresses.** 10 of 14 "awaiting-review" are reviewed elsewhere. Fix: the fixed address (§2), and legacy resolution in G1.
- **F4. The whole-page review binding conflicts with constructing the page.** Fix: G3.
- **F5. 16 return members are left before 0199.** Director choice D3.
- **F6. Submitter labels drift (18 labels).** Director choice D4.
- **F7. Prime's text versions (`05.NN.002.md`) and the 07NN layout (`05.NN.pack.md`, `.return.md`) are not the reservation's origin file.** The view needs a declared page-address rule, not newest-file selection (G1 contract).
- **F8. `prime_cycle` reports a registered, reserved-only member as `custody-unresolved` until the page names it,** not `no-return` (lab 4b). Harmless, but the view, not prime_cycle, should own "not returned yet".
