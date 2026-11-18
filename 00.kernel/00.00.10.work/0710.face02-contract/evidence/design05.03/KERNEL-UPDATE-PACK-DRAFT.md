# 05.NN DRAFT — kernel update: law 0001 v005 and 0002 v004 (lifecycle corrected again)
date: 2026-11-02 · drafted by: claude-opus-5-5 (Claude), 0710/05.03 · for: Codex Prime to adapt; the Director to approve
state: **DRAFT. Not released. Not executable:** the prerequisites P1–P4 below are missing. Supersedes the 05.02 draft, which is preserved.

## Candidates
| Face | Candidate | sha256 | Draft target | Retired name |
|---|---|---|---|---|
| 0001/01 | `design05.02/candidates/0001.law.01.005.candidate.md` | f46ae1cd… (7832 bytes) | `0001.law/01.005.md` (free on 2026-11-02) | `01.004.09.md` |
| 0002/01 | `design05.03/candidates/0002.schema.01.004.candidate.md` | d16f05b2… (8586 bytes) | `0002.schema/01.004.md` (free) | `01.003.09.md` |

- **Both are CRLF,** like their seats.
- **0018:** no candidate; it is not part of this update.
- **0009:** the warehouse layout is a proposal inside this update (prerequisite P3).

## Missing prerequisites (nothing executes until all four are met)
- **P1 — Review and approval route.** Prime reviews the exact candidate bytes. The Director approves the **signed** bytes.
- **P2 — Seating tool.** A reviewed compute tool or procedure implements `lifecycle.template.json`. **None is active in lib-build;** the inactive `0305.clerk` code is not revived. The fixture simulator is evidence only.
- **P3 — Warehouse layout.**
  - Approve `00.retire.09/{PPPP.title}/{FF}.{VVV}.09.md` plus the `09.md` ledger (`LIFECYCLE.md`), or choose another collision-free layout.
  - **0009 is silent on layout.** A flat layout collides (fixture L10).
- **P4 — Release.** A released pack names both faces as one release.

## Order (follows `lifecycle.template.json`; each step's checks belong to that step)
1. **Stage.**
   - Checks: each candidate equals its reviewed sha; each seat equals its source pin (0001 v004, 6288 bytes; 0002 v003, 1521 bytes); the draft names are free.
   - Act: exclusive create.
2. **Sign.**
   - The model requests. Compute runs the align checks (0060: stamp keys, unique headings, cites resolve) and confirms the draft still equals the staged bytes.
   - It changes the stamp lines only, and the content sha stays equal.
3. **Approve.** The Director's record names each **signed** sha. Compute confirms that the draft equals that sha.
4. **Seat preflight** (only now, after approval):
   - approved; draft = approved;
   - seat unchanged since staging;
   - warehouse names free;
   - **every face in the release approved.**
   
   Then run the checker read-only and record the counts.
5. **Seat and retire**, one face at a time, journaled J1–J5. **Restart checks the hashes, never the labels.**
   - **A half-seated pair is held for the Director.** It is neither finished nor rolled back automatically.
6. **Post-check:**
   - the checker counts before and after;
   - the retired faces' content sha equals their seat-before content sha (stamp-only change);
   - the seated faces' content sha equals the reviewed content sha.
7. **Lock and promotion** are separate (0023) and **not in this pack.**

## Recovery and rollback
As in `LIFECYCLE.md` (fixtures L4, L4b, L6):
- **Restart** from the journal with hash checks.
- **Rollback**, by Director decision:
  - restores seat-before bytes to `01.md`;
  - returns the new face to its draft name with its signed bytes;
  - strikes the ledger line.
  
  **Both versions stay, and nothing is deleted.**

## Preserved
- Notes: 06.01–06.03.
- The section maps for 05.01, 05.02 and 05.03.
- The authorizing work: the 06.02 and 06.03 decisions; the 06.01 and 06.02 reviews.
- Approval identity: the signed sha, recorded by the Director.

**Hashes prove bytes, not meaning.** Semantic non-regression is a review judgment.
