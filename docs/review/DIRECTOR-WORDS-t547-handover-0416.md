# Director words: t547u handover of 0416 (2026-11-23, about 2:24 PM EST)

Matthew, verbatim, on Grok-1 leaving 0416 after a start, and on checking a takeover.

> I had given grok-1 the previous prompt for it but you then said not to unless it finished 0407, then I gave it and overwrote it with the current prompt for grok-1 and gave the new prompt for grok-2 to grok-2

Then:

> we'll see if grok-2 can take it over without breaking it. You'll need to define that for checking.

Reading: Matthew first gave Grok-1 the 0416.05.01 prompt. Prima had said not to, unless 0407 was finished. He then gave that 0416 prompt, then overwrote Grok-1 with the current 0407.05.01 prompt, and gave Grok-2 the 0408.05.01 prompt. Grok-1 may have run `wf claim 90.50.10.0416 1` locally and edited `tests/wf.rs` before the overwrite. Grok-1 is now on 0407. Grok-2 is now on 0408. A later worker, possibly Grok-2, may take over 0416. Prima must define how that handover is checked so the takeover does not break the page.

The check is defined in docs/review/HANDOVER-0416.md. The general rule is in docs/review/PENDING-RULES.md. Nothing was packed. 0423 will add `wf release`; today that command does not exist, so the interim steps use only the tools we already have.
