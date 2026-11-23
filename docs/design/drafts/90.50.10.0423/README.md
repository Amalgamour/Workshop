# Pack draft, 90.50.10.0423 (one-worker)

t533u: one worker per page at a time. Also the 0701 `push_log` prefix check (docs/review/DRIFT-0704-RESPONSE.md). Title: one-worker. Grant: `src/cmd.rs`, `src/page.rs`, `tests/page_0423.rs`. It waits until 0408 is closed (that page holds `src/cmd.rs` and `src/page.rs`). Then it goes first in the queue, ahead of 0422, because it is a safety rule.

This folder is pack text only. Do not `wf draft` or `wf pack` it until 0408 is closed and its grant is free. Start is chosen at pack time. Kit pin until then is `a823ee28`.

Words: docs/review/DIRECTOR-WORDS-t533.md. Ruling: docs/review/PENDING-RULES.md. Queue: docs/plan/GROK-BUILDER-QUEUE.md. 0701 repair (not part of this pack): docs/review/0701-LOG-REPAIR.md.
