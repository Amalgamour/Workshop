# 05.NN DRAFT — kernel update: law 0001 v005 and 0002 v004 (corrected lifecycle)
date: 2026-11-02 · drafted by: claude-opus-5-5 (Claude), 0710/05.02 · for: Codex Prime to adapt; the Director to approve
state: **DRAFT. Not released.** This replaces my 05.01 draft (preserved). It makes no kernel write, sign, approval, seat or lock.

## Authorizing work
- **Director:** 0710/06.02.decisions #01–#07 (verbatim), and Prime's application D01–D07.
- **Review:** 0710/06.01.review, R01–R08.
- **Candidates:** 0710/05.02 `evidence/design05.02/candidates/`.

**Direction is approved; the candidate bytes are not** (06.02 state line).

## Governing lifecycle (read 2026-11-02; quoted where exact)
| Step | Owner | Law |
|---|---|---|
| Draft beside the seat, from the seat read first; face 01 first | Prime or a model under a job | 0021 Order, 0060 Read/Start/Next |
| Number = the seat header + 1 | compute checks | 0024 Number |
| **Align = sign:** read every section, check the cite ("A stale cite is a halt"), then sign. "Sign is the prime stamp." | **the model requests**; compute checks; the stamp is recorded | 0060 Align, 0021 Name, AGENTS v003 draft (sign is the readiness step) |
| **Approve the exact candidate bytes** | **the Director** | 0022, D04 |
| **Seat:** rename the seat to `FF.version.09` with a retired stamp; rename `FF.VVV` → `FF` and stamp it approved; **move the retired face into this book's `00.retire.09` in the same act**; rename, never copy | **compute,** recorded by Prime (D3 practice) | 0022 Seat, 0021 Seat, 0009 Transition |
| Lock and promote | **separate,** authorized | 0023 |

## Preflight (compute; read-only; any failure halts and changes nothing)
1. **Candidate identity:**
   - sha256 and bytes of each candidate equal the reviewed and approved values recorded on 0710;
   - **line endings are CRLF,** like the seats.
2. **Seat identity:** the seats equal their 0710/05.02 pack pins:
   - `0001.law/01.md` v004, 6288 bytes;
   - `0002.schema/01.md` v003, 1521 bytes.
   
   A drifted seat halts, because the candidate no longer derives from it.
3. **Occupancy,** checked at execution and measured free on 2026-11-02:
   - `0001.law/01.005.md` and `0002.schema/01.004.md` are absent;
   - `0001.law/01.004.09.md` and `0002.schema/01.003.09.md` are absent, in the page folder and in the warehouse.
4. **Warehouse:**
   - `00.00.01.law/00.retire.09/` **does not exist today.** Per 0009 it is created by the first seating, with its `09.md`.
   - **The content of `09.md` is not specified in the laws read, so it is needed before execution** (Need N2).
   - If it exists by then, it is reused; a second home is never invented.
5. **Cite and align:**
   - every cite in the candidates resolves;
   - the stamp keys are present;
   - every section has `owner: kernel-only`;
   - the headings are unique.
6. **Checker:** run the seated checker read-only and record the finding counts before staging. **No rule is weakened.**
7. **Tool:** **no active seating tool exists in lib-build today** (only the inactive candidate `0305.clerk/02.clerk.009.py`).
   - The seat step needs either a reviewed tool, or a Prime-executed, compute-verified rename script reviewed as part of this pack.
   - **No manual copy, and no Director file handling.**

## Steps
1. **Stage** (Prime under the release; writes only new paths). Write the reviewed candidates to `0001.law/01.005.md` and `0002.schema/01.004.md` with exclusive create. Read back and match the bytes.
2. **Sign request** (model) and checks (compute): the align checks in Preflight 5; the stamp recorded.
3. **Director approval** of the exact staged sha256 for each candidate, recorded verbatim on 0710 with both identities.
4. **Seat,** one act per face, journaled:
   1. write a journal entry `{face, seat_sha, candidate_sha, retired_name, warehouse}` before any rename;
   2. create `00.retire.09/` and `09.md` if absent;
   3. rename the seat to `01.004.09.md` (0001) or `01.003.09.md` (0002), set its stamp to retired by v005 or v004, and move it into `00.retire.09/`;
   4. rename the candidate to `01.md` and set its stamp to approved;
   5. read back both; mark the journal entry complete.
   
   **0001 and 0002 are seated in the same release** (the 0001 Correspondence change and the 0002 forms depend on each other). One is completed before the next starts.
5. **Post-check:**
   - the checker again: the before and after counts;
   - every reference from the 05.01 search still resolves;
   - the retired faces are byte-equal to the pre-seat seats, apart from their stamp lines (a recorded diff).
6. **Lock and promotion are not part of this pack** (0023).

## Interruption and recovery
- The journal says which face and which step.
- **On restart:**
  - **a completed step** is verified, not repeated;
  - **a seat renamed but not moved** is moved;
  - **a candidate not yet renamed** is renamed.
  
  The procedure never re-stages over an existing file.
- **A half-seated pair** (0001 seated, 0002 not) is reported to Prime. The Director decides whether to finish or roll back. **It is not left silently.**

## Rollback (both versions preserved)
- Rename the seated `01.md` back to its draft name `01.VVV.md`, with the stamp `draft, rolled back`.
- Move the retired `01.VVV.09.md` back from `00.retire.09` and rename it `01.md` with its prior stamp.
- **Nothing is deleted.** The journal and both versions stay.
- Rollback is a Director decision, executed by the same tool path.

## Not claimed
- **Hashes prove bytes, not semantic non-regression.** Meaning is reviewed by Prime and the Director against `SECTION-IMPACT-MAP.md`.

## Required related law (substantive, not wording)
- **0001 Correspondence** is part of this pack.
- **0018 Envelope** (payload naming) is **held** (Director fork F2): `0018.seqaddr/01.011.md` already sits beside that seat.

## Not in scope
- conforming the existing 02 drafts (0302/0304/0307/0411/0413);
- a pack-template home (R05);
- Grok-1's repair;
- lock or promote;
- Git publication;
- 00.live.
