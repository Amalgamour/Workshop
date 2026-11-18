# 05.NN DRAFT — kernel update: law 0001 v005 and 0002 v004 (lifecycle v2)
date: 2026-11-02 · drafted by: claude-opus-5-5 (Claude), 0710/05.04 · for: Codex Prime to adapt; the Director to approve
state: **DRAFT. Not released. Not executable** until P1–P4 are met. Supersedes the 05.03 draft (preserved). Its checks are those shown by `lifecycle/runs/` (35/35).

## Candidates (unchanged from 05.03)
| Face | Candidate | sha256 | Draft target | Retired name |
|---|---|---|---|---|
| 0001/01 | `design05.02/candidates/0001.law.01.005.candidate.md` | f46ae1cd… (7832 bytes) | `0001.law/01.005.md` | `01.004.09.md` |
| 0002/01 | `design05.03/candidates/0002.schema.01.004.candidate.md` | d16f05b2… (8586 bytes) | `0002.schema/01.004.md` | `01.003.09.md` |

Both are CRLF.

## Prerequisites
- **P1 — Review and approval route.** Prime reviews the candidate bytes. The Director approves the **signed** sha of each face.
- **P2 — A seating tool** built to `SEATING-TOOL-SPEC.md` and passing its measurable finish. **None exists today;** the simulator is evidence, not a tool.
- **P3 — Warehouse layout approved** (U1). The stamp whitelist (U2) and record location (U3) are decided.
- **P4 — A released pack** naming both faces as one release.

## Order (per `lifecycle/lifecycle2.template.json`)
1. **stage:** candidate = reviewed; seat = source pin (0001 v004, 6288 bytes; 0002 v003, 1521 bytes); draft name free.
2. **sign:** the model requests. Compute checks alignment and that the draft equals the staged bytes; stamp lines only.
3. **approve:** the Director names the signed sha; draft = signed.
4. **seat**, per face:
   - preflight: approved; draft = approved; seat unchanged; warehouse name free; every face in the release approved;
   - then J1 plan and raw images → J2 `planned` → J3 → J4 → J5 → J6 → J7 `retired`.
   
   **A half-seated pair is held for the Director.**
5. **post-check:** run the checker read-only and record the counts before and after. **A restart at any time re-verifies the actual hashes.**
6. **Lock and promotion are separate** (0023), not in this pack.

## Recovery and rollback
- **Restart** derives the state from hashes. An unknown state, a malformed journal, or drift after completion **holds with no write**.
- **Rollback:**
  - needs a Director decision naming the seated, retired and restore identities;
  - preflights before the first rename; any change or occupied destination holds with no write;
  - is journaled R1–R6 and restartable;
  - restores raw before-images;
  - **keeps the seated version as an image** and appends typed ledger lines.

**Nothing is deleted.**

## Not claimed
- generic power-loss recovery;
- concurrency;
- releases larger than two faces;
- semantic non-regression from hashes (that is a review judgment).
