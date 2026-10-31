# Prime review — cycle integration 05.01

Date: 2026-10-30. Reviewer: Codex Prime.
Disposition: first build retained; affected live adoption held for 05.02 correction.

## Verified foundation

All 14 submitted tests passed independently. All 16 artifact rows match current
bytes, and capture 0170 freshly verified complete. The adapter implements read,
record, inspect and packet. It fills mechanical review fields, preserves structured
review plus readable projection and a completion marker, and separates finished
passes from explicitly completed goals. No old dependency source was changed.
These are synthetic integration results, not a fresh-model or live-use result.

## PC-01 — stale evidence still displays terminal completion

Confirmed independently. Record an explicitly completed goal, then change the
source page while keeping the same goal declaration. A new read correctly says
pass_state review-stale and attention re-review required, but still returns
pass_terminal finished and goal_terminal completed as unqualified current fields.
Retain the historical judgment, but do not expose it as current completion after
its evidence becomes stale. The stale boundary must survive JSON, readable output,
summary counts and any next-action handback. Correction required before live use.

## PC-02 — the decision template does not bind its agreement

Confirmed independently. Read a template, change the registration agreement.scope,
then record the original decision against that changed registration. record exits 0.
The page, receipt and goal hashes did not change; the fingerprint omits the actual
review agreement. This silently evaluates an old decision against changed direction.
Bind the relevant registration/work agreement and scope into the template and
record. Changed direction must require a new read/reconciliation. Do not solve this
by weakening expected-prior or source checks. Correction required before live use.

## New daily logging requirement

The Director now requests logging of what actually happens each day. This was not
a stated requirement of Claude's original pack. Keep it labelled as a new bounded
addition in 05.02 rather than retroactively calling its absence a failed original
test. Completed review records remain authoritative work-local judgment records;
a daily journal should point to them and record actual operation attempts/outcomes.

## Current adoption and next step

The proposed review location under each work page's evidence/prime-cycle-reviews
is acceptable for scoped Prime actual use after correction. No separate Director
choice is needed for that routine placement. No such live adoption occurred here.
PC-01 and PC-02 are technical binding repairs, not a new semantic authority grant.
The first real read-record-read still precedes the cold-Prime contextual Colab.
AR-01 remains held. No model call, fresh session, dispatch or 00.live migration.
