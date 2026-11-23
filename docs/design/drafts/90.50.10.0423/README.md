# Pack draft, 90.50.10.0423 (one-worker)

t533u: one worker per page at a time. t541u: a page is held only while one worker is actively working on a face (01, 04 or 05), and that face is locked. One model at a time. Between steps the page is not held. Also the 0701 `push_log` prefix check (docs/review/DRIFT-0704-RESPONSE.md). Title: one-worker. Grant: `src/cmd.rs`, `src/page.rs`, `tests/page_0423.rs`. It waits until 0408 is closed (that page holds `src/cmd.rs` and `src/page.rs`). Then it goes first in the queue, ahead of 0422, because it is a safety rule.

This folder is pack text only. Do not `wf draft` or `wf pack` it until 0408 is closed and its grant is free, and until the conflicts below are settled or accepted. Start is chosen at pack time. Kit pin until then is `a823ee28`.

Words: docs/review/DIRECTOR-WORDS-t533.md and docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md. Ruling: docs/review/PENDING-RULES.md (t533 section still has the older reading; see conflicts). Queue: docs/plan/GROK-BUILDER-QUEUE.md. 0701 repair (not part of this pack): docs/review/0701-LOG-REPAIR.md.

## Conflicts and open questions (do not pack until raised)

These are conflicts between t541u and the t533 reading, or between t541u and the earlier 0423 draft. They are flagged here, not packed away.

1. The t533 reading and PENDING-RULES.md items 2 and 5 still say a worker is in the page only from 05 claim until return, and that packing may stage later passes while a builder holds the page. t541u widens "in the page" to active work on faces 01, 04 or 05, and says one model at a time, so Prima must not pack, draft or face-write while another worker holds a face of that page. The "held only while actively working" and "not held between steps" parts of t533 still stand. PENDING-RULES was left as the t533 record in this turn; it needs a t541 update before the rule is written into the kit DESIGN.md.

2. wf today has no session-long hold for faces 01 or 04. `wf face-write` and `wf draft` are single commands. `wf claim` until `wf return` is the only lasting occupancy, and it is only for a 05 pass. This pack must refuse other workers during those existing commands, and while a 05 claim is open. It must not add a new hold or release command, and must not take `src/lib.rs`. If a lock that lasts across several 01 or 04 edits is required, stop and raise it before packing.

3. The earlier draft said a packed but unclaimed pass is not an occupant, and a returned pass waiting for a check is not an occupant. That still matches "between steps the page is not held." What changes is that check, signoff, close, face-write, draft and pack are themselves active work, and they refuse (and are refused) while another worker already holds a face of the page. Two checkers at once are refused.

4. t533 allowed packing later passes (draft, and a pack that is not yet the active claim). Under t541u that is allowed only when no one is actively working on the page.
