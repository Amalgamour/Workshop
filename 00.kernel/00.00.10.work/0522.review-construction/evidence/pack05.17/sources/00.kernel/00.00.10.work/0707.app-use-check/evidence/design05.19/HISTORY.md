# Rollback and source-history policy (0707/05.19)

## Rules
1. **Never edit a file that a frozen return declares as an artifact.** It is evidence.
   - **Known (inv2 X5):**
     - 0522/05.13 declares `app/librarian.py`, `app/README.md`, the v7 door and JSON, and pass03 files;
     - 0522/05.14 declares the v8 door and JSON and pass04;
     - 0512/05.07–09 declare reporter v1/v2/v3 connector and JSON.
   - **Successors are NEW paths only.**
2. **Selection is ONE edit of `app/librarian.py`.** It makes 0522/05.13 measure `incomplete` (`artifact-hash-mismatch`) under any parser (05.18 matrix).
   - That return and its review are **not repinned, rewritten or re-reviewed to look fresh.** They are reported as stale, with the cause "declared app artifact changed by selection".
   - A README edit has the same effect on 0522/05.13.
3. **Before selection, Prime keeps a historical observation:**
   - run the CURRENT `review-report` and `review-loop read` on each affected return;
   - store the outputs in the selection's own evidence folder.
   - Those outputs are the "as it stood" record. Afterwards, the stale state is expected and explained.
4. **Records are never overwritten.**
   - Old (v7) and new (vN) records coexist and stay distinguishable by review id and stored intake id.
   - A version marker in records stays optional (05.18 proposal; not required).

## Rollback (single point)
- **Restore `app/librarian.py` to c3a5be3b…** (12204 bytes). All successor files stay on disk, inert.
- **Measured effects (05.18 rollback rehearsal, plus inv2b X7):**
  - N7 records written under the combined loop read as `stale` under v7 (exit 1). They are held, not lost.
  - N5 records read identically.
  - The v3/v4 reporter refuses any dispatcher other than the one it pins. **After rollback, the review-report route returns to the state before selection: there is no review-report route in c3a5be3b.**
- **0522/05.13 returns to complete** (its declared bytes are back).

## Safe holds
- **Do not select while a pending review depends on a return that declares app files.** Finish it under v7 first, or accept that it will measure stale.
- **Never edit vN or R′ in place.** A changed pin is refused (05.18 P01–P04), which is the intended hold.
- **On any surprise after selection:** roll back, keep every new record, and re-read affected reviews under each selection, recording which are stale.

## Scoped rollout (does not rewrite old evidence)
1. Freeze the inputs: G, K and F (re-staged), plus the Director answer.
2. Build W, vN and R′ at the canonical root. Use read-only prepare/form on the named live cuts only; all mutation on disposable books.
3. Run the acceptance matrix (ACCEPTANCE.md). Prime reviews.
4. Keep the historical observation (rule 3).
5. Make the one selection edit.
6. Use the loop on the NEXT real returns first; old returns are re-read, not re-recorded.
7. Custody and migration stay separate deliverables and show `missing`.
