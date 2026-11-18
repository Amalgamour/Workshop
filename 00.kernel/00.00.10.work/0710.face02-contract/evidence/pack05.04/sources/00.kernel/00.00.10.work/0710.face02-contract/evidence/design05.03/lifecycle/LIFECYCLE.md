# Face lifecycle — readable template (proposal, 0710/05.03)
who: claude-opus-5-5 · state: draft, nonproduction. **This is not an authority source;** each stage cites its law. Machine form: `lifecycle.template.json`. The fixture run is `runs/`, driven by `lifecycle_sim.py`. **Fixture approvals are SYNTHETIC.**

## Identities compute keeps (the model never computes these)
| Name | What it is |
|---|---|
| staged | the candidate's bytes as staged |
| content | the bytes with the two mutable stamp lines (`Authorization:`, `state:`) removed. **It must not change across sign, approve, seat or retire** |
| signed | the bytes after the sign stamp |
| approved | the signed bytes the Director's approval names |
| seated | the bytes after the approved stamp |
| retired | the old seat's bytes after the retired stamp |
| seat-before | the old seat's bytes before any change; rollback restores exactly these |

**Only stamp lines may change between stages.** Any other byte change is a content change, and it stops the run.

## Stages
| Stage | Owner | Needs | Writes and records | Held or refused when | Recovery |
|---|---|---|---|---|---|
| **stage** (0021, 0060) | model or Prime under a job; compute writes | candidate = reviewed bytes; seat = source seat; draft name free | `FF.VVV.md` by exclusive create; the stage record | any need fails | re-stage only to a free name |
| **sign** (0060 Align, 0021 Name) | the model requests; compute checks | staged; draft = staged; align checks | stamp lines only; the sign record | not staged; bytes changed | a new draft |
| **approve** (0022) | **the Director** | signed; the approval names the signed sha; draft = signed | the approval record (outside the book) | **held: approval missing**; refused: wrong sha, content changed | a new approval of the exact bytes |
| **seat + retire** (0022 Seat, 0009 Transition) | compute, recorded by Prime | approved; draft = approved; seat unchanged; warehouse name free; **every face in the release approved** | J1 journal → J2 warehouse folder and ledger line → J3 move the seat into the warehouse, retired stamp → J4 rename the draft to `FF`, approved stamp → J5 read back | **held: approval missing** (nothing renamed); **held: half-seated** (an earlier face seated, a later one stopped); held: hash mismatch on restart | restart reads the journal and **checks the actual source and destination hashes before each step**; a step label alone never renames |
| **rollback** | the Director decides; compute executes | seated; journal complete | restore seat-before into `FF`; return the seat to its draft name with the signed bytes; strike the ledger line (no delete) | — | — |
| lock / promote | **separate** (0023) | — | — | **refused here** | — |

## Warehouse (proposal)
- `00.retire.09/` sits beside the book's `00.md`. Inside it, **one folder per originating page** (`0001.law/`, `0002.schema/`), each holding the retired `FF.VVV.09.md` unchanged in name.
- `09.md` is the ledger: one line per retirement and one per rollback strike.
- **Why:** a flat folder collides when two pages retire the same `01.004.09.md`. Fixture L10 shows the collision; L1 shows the paged layout.
- **Law status:** 0009 says "Move that file into this book's `00.retire.09`" and is silent on layout. **The page folder is a proposal to approve with the kernel update.** It is not existing permission.

## Fixture outcomes (run once; `runs/results.json`; 13 of 13 as expected)
| Case | Outcome |
|---|---|
| L1 | the pair seats; two `01.004.09.md` files without collision; content unchanged through every stamp |
| L2 | content changed after signing → approval refused |
| L2b | content changed after approval → first face seated, second **held half-seated** |
| L3 | one approval missing → **held**, nothing renamed |
| L4 | stop after J3 → restart checks hashes and completes |
| L4b | draft altered before restart → **held** |
| L5 | the second seat changed after approval → **held half-seated** |
| L6 | rollback restores both versions byte for byte |
| L7 / L7b | out of order → held or refused |
| L8 | approval of the pre-sign bytes → refused |
| L9 | lock requested → refused |
| L10 | flat warehouse → collision → **held half-seated** |
