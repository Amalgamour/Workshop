# Director words: t557u manual return (2026-11-23)

Matthew asked for a process when wf is not working, then answered the three questions in docs/plan/MANUAL-RETURN.md. Words as given, below. Readings follow. Nothing was packed.

## t557u  -  the request (2:39 PM EST)

> We need a process for a manual return if the compute isn't working.  So what it does if the prompt and the pack don't execute correctly.

Reading: if the prompt and the pack do not run correctly, there must be a manual return. The process is in docs/plan/MANUAL-RETURN.md. The rule is in docs/review/PENDING-RULES.md. It follows lockout/tagout: tag the break, record it, and never bypass wf by hand.

## t557s2212  -  the three questions (2:45 PM EST)

Matthew picked the default on all three.

Q1. Is the fixed location on returns just the granted file paths, plus the report at `reports/<page>/05.NN/`?

> the granted files plus the report, with no second copy.

Reading: the work stays in the granted paths. The report is the record. Do not add a second copy of the code.

Q2. The record releases the face lock, but the builder still holds the page. May the checker enter while that tag is open?

> Prima and the checker may review while the tag is open, and no other builder may claim the page.

Reading: Prima and the checker may review a page that has an open manual-return tag, as after a normal release. No other builder may claim that page until the tag is cleared, after intake, or by a recorded override.

Q3. Lab 0705 said a pasted report must not stand in for a push, because it is not in the hash chain. This process allows a paste when the returns push also fails.

> pasting the report is a last resort only, and the pass never closes until the report is committed.

Reading: a paste to Matthew is last resort only, when the push to `returns` has also failed. The pass never closes until that report is committed to `returns`. A paste alone is never a passed close. Prima or Matthew commits the report when they can.
