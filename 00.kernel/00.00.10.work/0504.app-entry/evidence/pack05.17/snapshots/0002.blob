# Prime review — 0504/05.16
Date: 2026-10-28. Reviewer: Codex Prime.

Accepted as design/proof input. Independent rerun of the unchanged harness, with
only its evidence destination redirected, exited 0 and reported 12 proof cases.
Existing tools allow capture despite a claimed job or changed outbox; composing
commands is not an enforced handoff. No adapter has been built by this return.
Fresh capture verify is complete; that does not approve or close the work.

CH-01: The final report must itself be bound to a returned artifact, not merely a
new caller-supplied hash. A caller hash proves selected bytes, not that those bytes
were part of the returned job. Separate its transport role from its final-report
role while checking path, hash and byte count against the returned artifact record.

CH-02: Idempotency needs a durable binding record. A complete capture alone does
not prove which Clerk event was previously connected to it. Record the canonical
binding identity and event/receipt together outside the sealed member. A complete
capture without the matching completed handoff record requires attention, not an
invented successful retry. No automatic repair after partial failure.

The supplied work_ref remains a declared label: Clerk has no equivalent field to
verify. Say this explicitly. Make instructions_base required for the first slice.
No route, seat, release, review, acknowledgement, closure or acceptance is granted.
Next bounded action: fixture-only adapter implementing these guards.
