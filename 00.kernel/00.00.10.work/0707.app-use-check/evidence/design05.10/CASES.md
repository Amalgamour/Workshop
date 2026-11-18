# Independent acceptance cases for core-managed review (0522/05.11) — 0707/05.10
who: claude-opus-5-5 (Claude), Colab design/labs · state: design. **Every target assertion is NOT RUN.** The fixtures are SYNTHETIC.

These cases are derived only from the frozen contract prefix (C-line numbers refer to `evidence/pack05.10/sources/review-integration-contract.md`) and from 0412/01, 06.06, 06.07 and the Director agreement. I did not read Grok-1's return, source or tests. **Prime binds each step to the real returned API.** No API is assumed here. Machine index: `index.json`.

## Requirement → case map
| Req | Requirement (source) | Cases |
|---|---|---|
| R1 | address-first intake; no caller paths, hashes or registration (C12, C34; 06.06 #02) | A |
| R2 | a thin submission is not the whole packet; bounded index; unknown pointers are findings (C14) | A |
| R3 | missing N1NN custody is truthful preliminary: no fake receipt, task association or completion; no custody-dependent closure (C16) | A |
| R4 | unknown tests never become passed; findings never empty; a missing decision is never consent (C19) | A, F |
| R5 | Prime supplies meaning; each finding answered, fixed or elevated; Director text verbatim and separate (C21) | A, B |
| R6 | candidate identity before judgment, final identity separate; record before publish; drift → stale, old record kept; replay idempotent; conflict refused; input kept (C23) | A, C, D, F |
| R7 | compute-derived targets; N7NN page-local 06.NN review; earlier and manual reviews preserved, not adopted (C26) | B, D |
| R8 | pointer diff restricted, no self-invalidation; unrelated change blocks; partial publication visible; **recovery re-verifies completed bytes**; exact new-process recovery; a block never erases the judgment or reports completion (C28) | A, C, D, E |
| R9 | a Director reply does not auto-release; a hold affects dependent work only (C36; 0412/01; agreement) | B |
| R10 | no meaning or approval inferred from headers, filenames, green tests or "yes" (0412/01; C21) | B, F |

## Cases (35 assertions in total, all NOT RUN)
- **A — thin N5NN submission, pending custody, preliminary judgment.**
  - Fixture `0599.fixture-review`: a thin `submission.md`; a substantive `VERIFICATION.md` (T1 passed, T2 failed, T3 unknown); `payload/parser.py`; an artifact manifest with one digest deliberately missing. **No `0199.*` line exists.**
  - **It expects:** the evidence index goes beyond the submission; the missing digest is a finding; **custody is preliminary, with no receipt, association or completion**; the judgment survives a new process; T3 stays unknown; the sources are unchanged; **the candidate and final identities are separate and compute-returned**; both findings keep their dispositions.
- **B — N7NN hold, reply and successor.**
  - Fixture `0799.fixture-colab`: prior review `06.01` (director-input; Q1; D1 held; I1 independent); SYNTHETIC Director reply `06.02`.
  - **It expects:** the predecessors are byte-identical; the successor is a new 06.NN; the Director words are verbatim and separate; **D1 is still held until the successor is recorded; the reply alone releases nothing**; I1 was never held; nothing is executed.
- **C — drift: unrelated change versus the tool's own pointer write (PRIMARY HOSTILE).**
  - C-a edits the 05.01 Scope; C-b edits the T3 row in `VERIFICATION.md`; C-c is a normal publish.
  - **It expects:** C-a and C-b are stale or blocked, the judgment is kept, the edits are not reverted, and **the stale state survives recovery**; in C-c the tool's own pointer write does **not** self-invalidate, and the diff is limited to the Review area.
- **D — publication blocked by an existing manual review.**
  - The Review area holds hand-written text.
  - **It expects:** no overwrite and no adoption; the judgment is durable in the record, not only in the render; a new process recovers the exact judgment, next action and holds; publication is reported incomplete.
- **E — interruption and false completion (PRIMARY HOSTILE).**
  - E-a stops between render and pointer; E-b changes the rendered file after a completed publish; E-c changes the pointer area.
  - **It expects:** a partial publication is visible; recovery re-verifies the bytes before finishing; **in E-b and E-c recovery reports drift and holds, never "completed", and never overwrites.**
- **F — replay, conflict, wrong type, omitted tests.**
  - **It expects:** a same-byte replay is idempotent; a conflicting replay is refused with the original intact; T3 = "yes" is refused at the field with help; **an omitted T3 is refused or recorded as unknown, never passed.**

## The two primary hostile cases and the mistakes they catch
- **E (false completion).** The likely mistake is a recovery that reads a done flag or step label and returns already-complete without re-reading the rendered review and the pointer. That is the same defect class Prime found in the 0710 lifecycle simulator (L-P1). **E-b is the decisive variant:** a changed output after completion.
- **C (self-invalidation versus missed drift).** The likely mistake is hashing the whole work page at intake. The tool's own pointer write then makes its own review stale (C3 fails). Or, after that bug is "fixed" by excluding the page, a real Scope edit passes unnoticed (C1 fails). **C-a and C-c together catch both directions.**

## Assertion versus ambiguity
These are reproducible assertions with a contract basis. They are not judgment calls:
- A1–A9, B1–B6, C1–C6, D1–D4, E1–E5, F1–F5.

**Ambiguities for Prime or the Director:**
- the D1 state after a successor "continue" (B);
- whether non-evidence files on the page count as an "unrelated change" (C);
- whether an omitted test is refused or recorded as unknown (F).

## Fixture prerequisites for API binding
- **Copy `fixtures/book` per case;** never run in place.
- **The filed (native or relocated) mode** needs a fixture produced by the accepted line tool. None is fabricated.
- **E-a needs a supported stop point.** If the API has none, report E-a as NOT BINDABLE.
- **The judgment files are semantic content** for Prime to transcribe into the returned form.

## Limits
**Not covered:**
- the C36 case "missing/ambiguous return";
- the same address in another book instance (C14);
- refusal of a finding without a disposition;
- the 0412 per-operation report floor.

`make_fixtures.py` checks only the fixtures' own validity. **No target behavior was run.**
