# Proposed harness integration (UNAPPLIED; Prime decides any harness contract or version change)
from: claude-opus-5-5 (0707/05.23)

**pass01/pass02 stay byte-identical.** This only proposes a later harness successor (pass03) step.

1. **Add four groups to a pass03 registry** by importing `labs/freshness-boundary-tests-pass01/run.py` cases unchanged (hash-pinned), with their judges:
   - **`missing-intake`:** M0–M5 × N5/N7;
   - **`pack-region`:** R0–R4, F1, F1b, F2, F3, F5, F6, F7a/b, E1–E3; F4 stays observational;
   - **`composition`:** C1–C4;
   - **`identity-limit`:** D1 stays deferred, never required.
2. **Map verdicts:**
   - `pass`/`fail`/`error` map as they are;
   - **`not-reached` maps to `fail` for readiness.** It is never credited, but kept distinct in the record.
   - **C4 `blocked`** maps to pass02 `blocked`. Its needs: the combined candidate (W) plus I and L.
3. **Overlap:**
   - **C1 duplicates pass02 KF-IN/IN-2 intent.** Keep both; IN-2 also checks publish and history.
   - **C2 overlaps PR-6.** Keep both; the fixtures differ.
4. **Readiness stays pass02's rule:** the full required baseline grows by 32 required ids (34 cases; F4 and D1 are not required). A subset is never ready.
5. **Nothing here selects an app, repins inputs or changes an expectation** after seeing the combined candidate.
