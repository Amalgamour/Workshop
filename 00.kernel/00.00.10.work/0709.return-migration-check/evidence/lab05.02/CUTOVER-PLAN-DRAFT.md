# CUTOVER PLAN DRAFT — rebuild correct returns, then retire (0417/06.05 D1–D3)
date: 2026-11-02 · who: claude-opus-5-5 (Claude), 0709/05.02 · state: **DRAFT for Codex Prime. Not a release. No live step runs from this file.**
Supersedes my 05.01 `CUTOVER-CHECKLIST.md` where they differ. That file stays as history.

## Facts this plan is built on (measured 2026-11-02)
- 83 legacy captures, 0101–0183:
  - 78 on matching lines;
  - 5 N7NN tails stay page-local;
  - 0154 is reserved-only.
- **18 destination lines (0102, 0104–0120); 11 of them take several passes, up to 20 on one line** (`target-lines.json`). Every destination number is occupied today by a different old capture.
- **65 old numbers are not destinations,** among them 0101, 0103 and 0121–0183. They are freed only by retirement. The pending 0521–0525 filings need 0121–0125. 0510 and 0511 add passes to the rebuilt lines 0110 and 0111.
- **The active allocator is a manual command,** `return_capture.py reserve`, as `0100.band.returns/01.md` instructs. In a line-pass-declared book it still takes the lowest free number and re-creates the door, after which the line tool refuses the whole book (probe H1).
- **A sentinel `.allocation.lock` in the door stops that unchanged command,** while in-flight legacy capture, verify and inspect keep working (probe H4).
- `return_lines` pass01 refuses any book that has the door (probe H4 step 7). Live work therefore needs Grok-2's authorized-book route. **This plan depends on that returned contract and does not guess its flags.**

## Durable locations (concrete proposal, for Director review in the bound plan)
| Role | Proposed path | Why | Git and operational tradeoff |
|---|---|---|---|
| **Archive** (retired originals, durable) | `D:\Git\lib-build\archive\returns\00.00.10.work\` (repo root, outside `00.kernel`) | Keeps each original `01NN.slug` folder **unchanged, by its old name**. The archive is therefore a book-shaped directory that the unchanged helper `verify`/`inspect`, `prime_boot` and `batch_observe` can read through their existing `members_book` parameter, so no reader code changes | **Git-tracked:** moving it within the repo is a rename, with no blob growth, `git log --follow` history, and it travels with clones. It must be outside the active work book, or the helper's slot scan would count it. **Unverified:** whether `lcheck.py` objects to a new top-level `archive/`. Check that before the bound plan; the fallback is `00.kernel/00.00.10.work.archive/` |
| **Backup** (second verifiable rollback copy) | `D:\librarian\backup\returns-cutover-<UTC stamp>\` | It is the copy that rollback uses, and it is independent of the repository and the branch | Not versioned and machine-local. It is kept until Prime's independent post-check, then retained by policy. **Never the only copy** |
| **Staging** (reconstruction) | `D:\librarian\staging\returns-cutover-<UTC stamp>\` | It sits outside the checkout, so a half-built page can never appear in the work book | Disposable after a verified publication. The journal and manifest are copied into evidence |
| **Authorization and journals** (evidence) | `00.kernel/00.00.10.work/0521.return-placement/evidence/cutover01/` | They are evidence that sits beside the owning tool page, not in the book namespace | Git-tracked, readable by review |
| **Live sentinel** | `00.kernel/00.00.10.work/0100.band.returns/.allocation.lock` | It is the only stop that the unchanged pinned `reserve` already obeys | One small Git-tracked file. **It reads as a crash leftover unless its bytes and the door page say otherwise** (see Hostile) |

## Authorization record (D3: Prime records the release and executes the bound plan)
`return-line-authorization/1`. Prime writes it after the Director's release. It is evidence of authority, **not authentication of a model.** If Grok-2's returned contract defines this schema, that contract wins, and the fields below become the minimum checklist.
- **The release:** `release.words`, the Director's text verbatim, plus `release.page` (page/face/#NN), `recorded_by`, `recorded_at`.
- **The book:** `book` (canonical resolved path), `book_fingerprint_t0` (taken after the freeze), `audit_sha256`, `plan_sha256`, `layout_sha256` (the exact declaration bytes).
- **The roots:** `staging_root`, `archive_root`, `backup_root` (canonical, each outside the work book).
- **The tool and sentinel:** `tool_pins` (the pass02 path, sha and bytes), `sentinel_sha256`.
- **The operations, ordered:** `freeze`, `backup`, `reconstruct`, `verify-staging`, `publish`, `retire`, `declare`, `post-check`, `rollback`. Each is single-use and marked consumed in the journal.
- **Staleness:** the tool refuses if the live fingerprint differs from `book_fingerprint_t0` before `publish`, or if any named hash differs.
- **Revocation:** a sibling `revocation.json`, or a recorded Prime line, refuses every unconsumed operation.
- **Refusals:** the file is missing, linked or malformed; another book; an operation that is not listed; consumed; stale; revoked.

## Order (each step names its gate. A failure stops the run, and its first output is kept)
0. **Preconditions:**
   - Grok-2's pass02 is returned and Prime-reviewed (reconstruct, publish into occupied destinations, retire, lookup after retirement, rollback, authorized book **with the door present**).
   - The Grok-1 integration slice is accepted.
   - Grok-1's app repair is reviewed.
   - The full plan has been rehearsed on a copy **with the door present**.
   - The Director's release is recorded.
1. **Freeze (T0).** Write the sentinel. From here no unchanged helper `reserve` succeeds. In-flight legacy reservations can still be captured.
   - **Transition protocol:** between T0 and step 8, **no new return is filed by any route.** Pending returns wait on their source pages, as 0510, 0511 and 0521–0525 already do. The window is recorded on the release page with its start time. An aborted run rolls back to the exact pre-T0 state, sentinel removal included.
   - **The layout is not declared yet,** so new routing never turns on while its destinations are still blocked.
2. **Fresh audit and plan, read-only,** after T0:
   - counts are derived, never hard-coded; compare with the 83 / 18 / 65 / 0154 / 5-tail facts;
   - an in-flight legacy reservation not captured by T0 joins the plan as incomplete, as 0154 does;
   - Prime writes the authorization from these hashes.
3. **Backup:**
   - copy the whole work book to `backup_root`;
   - tree-hash it;
   - re-read it in a separate process.
4. **Reconstruct in staging.** For each matched record:
   - build `{N1NN.subject}/05.NN.return.md` and `05.NN.custody/` with the **original sealed bytes**;
   - add provenance: old member, submission, origin page/pass, assignment link, the original reservation/manifest/receipt hashes and the Director replies referenced;
   - each rebuilt line holds all its passes, one page per line.
   
   Then:
   - **the 5 tails:** a byte check only;
   - **0154:** an archive entry with its incomplete state and `return: null` (missing; nothing invented).
   
   **Source-to-return links** are carried in the line page's provenance and in the book lookup index (`return-line-index.json`: old member → line/pass → archive path). **Source pages and face 05 replies are not rewritten.**
5. **Verify staging, independently.**
   - Every original byte hash matches.
   - Every old member, origin and submission resolves by lookup.
   - Every link names an existing source page/pass.
   - **Synthetic first filings in a staged copy:** new passes on `0110` and `0111`; new lines `0121`–`0125` after the staged retirement; two passes on one line.
   - Exit 0 is required to continue.
6. **Publish,** journaled, in ascending destination order. For each of the 18:
   - move the old occupant into `archive_root`, under its old name, after a byte check against the backup;
   - install the verified staged line page;
   - read it back;
   - journal the step.
   
   On interruption, resume from the journal. **A different subject is never overwritten without its verified archive copy.**
7. **Retire** the remaining 65 originals, 0154 included as incomplete:
   - each after its rebuilt return is verified **in live**;
   - each into `archive_root` under its old name;
   - journaled and resumable.
   
   **Afterwards the active namespace is the door plus the 18 line pages.**
8. **Declare.**
   - Write the layout through the authorized line tool.
   - Prime applies the new `0100.band.returns/01.md` text (Grok-1 drafts it).
   - **The sentinel stays,** permanently stopping pinned pass01 `reserve`.
   - New routing turns on only now, when every destination it needs is free or rebuilt.
9. **Independent post-check** by a separate process, or by Prime:
   - re-hash the archive against the backup;
   - check every rebuilt custody against the journal;
   - check every old-member lookup;
   - unchanged legacy readers with `members_book = archive_root` give the same status as before cutover, for every archived member (0154 stays `reserved`);
   - no original byte changed.
10. **First real filings (the completion check):**
    - the pending 0521–0525 returns land on new lines 0121–0125;
    - 0510 and 0511 add passes to 0110 and 0111.
    
    Each is a first proper filing, never a relabel. **Done only when these succeed.**
11. **Git.** Prime commits the published state on a named cutover branch, naming the release. **Merging is the Director's act.**

## Rollback
- **Before step 11,** rollback is the reverse journal:
  1. remove the installed line pages;
  2. restore the displaced and retired originals from `archive_root`, checked against `backup_root`;
  3. remove the layout;
  4. remove the sentinel;
  5. compare the live fingerprint with the pre-T0 fingerprint.
- **After step 11,** the branch is not merged, so it can be discarded.
- **The backup is never the input of a delete,** and nothing is deleted while it is the only copy.

## Completion criteria
- All 83 resolve by old member and by origin.
- 18 line pages hold their passes.
- 65 + 18 originals are in the archive under their old names, equal to the backup.
- 0154 is visibly incomplete.
- The 5 tails are unchanged.
- The layout is declared.
- The sentinel is present, and unchanged helper `reserve` refuses.
- The new door text is applied.
- The 0525 declarations are updated.
- The first real filings on 0121–0125 and the added passes on 0110/0111 succeed.
- The post-check passes, and Prime's review is recorded.
