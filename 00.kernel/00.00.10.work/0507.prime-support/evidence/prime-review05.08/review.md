# Prime review — boot validation and truthful retries
Date: 2026-10-27. Reviewer: Codex Prime. Disposition: ACCEPTED for PB-06/PB-07.

Independent disposable-copy suite:26 tests pass, no skips. Existing two-attempt
demo passes unchanged. All7 captured outputs and the dedicated submission match
0123, which freshly verifies and inspects complete without captured-byte changes.
All9 pack snapshots match their pins. No other lane was reviewed or staged.

Independent exact-probe replay confirms citations:null now records checks failed
with exit1 and no traceback; an identical retry reports checks failed, also exit1.
grades.O1={} records invalid judgement/not-oriented with exit1 and no traceback;
identical retry reports that outcome, also exit1. Raw inputs are kept. Expanded
tests cover malformed shapes, missing/truncated terminal records, stage-aware
show, read-only retries and conflicts. Interrupted stages return3/incomplete and
never manufacture a completed result. Existing success/authority separation holds.

The test15 exit change is confirmed as appropriate: invalid supplied judgement
is now a recorded processing failure (exit1), while command refusals/conflicts
remain exit2. The old expectation was revised for the requested behavior, not
weakened. Initial development failures remain in the Builder's captured logs.

This accepts the fixture prototype and repair, not a cold model boot, live install,
seated role or authentication. Clerk jobs and structured member identities remain
deferred in this version. Now that return_inspect is separately accepted, the next
bounded slice can compose its read-only projection into recorded member evidence,
without inventing a second validator or treating a receipt as approval.
