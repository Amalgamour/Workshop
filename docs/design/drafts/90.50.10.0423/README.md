# Pack draft, 90.50.10.0423 (one-worker)

t533u: one worker per page at a time. t541u: a page is held only while one worker is actively working on a face (01, 04 or 05). The face is locked for the whole work session, and released when the worker is done. The lock follows lockout/tagout (LOTO) practice. One model at a time. Between sessions the page is not held. Also the 0701 `push_log` prefix check (docs/review/DRIFT-0704-RESPONSE.md). Title: one-worker. Grant: `src/cmd.rs`, `src/page.rs`, `src/lib.rs`, `tests/page_0423.rs`. The grant grows to include `src/lib.rs` because lockout, try-out and release are new commands (help text and dispatch live there). It waits until 0408 is closed (that page holds `src/cmd.rs`, `src/lib.rs` and `src/page.rs`). Then it goes first in the queue, ahead of 0422, because it is a safety rule.

This folder is pack text only. Do not `wf draft` or `wf pack` it until 0408 is closed and its grant is free. Start is chosen at pack time. Kit pin until then is `a823ee28`.

Words: docs/review/DIRECTOR-WORDS-t533.md and docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md (including the 12:57 PM and 12:58 PM EST answers). Ruling: docs/review/PENDING-RULES.md. Queue: docs/plan/GROK-BUILDER-QUEUE.md. 0701 repair (not part of this pack): docs/review/0701-LOG-REPAIR.md.

This face lock is not the short `.wf-lock` file that stops two commands from writing at the same instant. That file lock already exists in `src/lib.rs`. The face lockout is a session lock recorded in the page log.

## Lockout steps, in plain words

The template is lockout/tagout (LOTO) from industrial construction and maintenance safety. Matthew (12:58 PM EST): "It's a lock out. Look at lockouts as your template from industrial construction and maintaince safety practices."

The source steps, and how 0423 uses each one:

1. Apply your own lock and tag. In the shop, each worker puts their named lock and a tag on the isolator before they start. In wf, the worker runs `wf lockout <page> <01|04|05> --reason T`. The log entry is the lock and the tag. It names the worker, the face, the reason, and the start time.
2. Try-out, before work starts. In the shop, you try to start the machine to prove it cannot start. In wf, the worker runs `wf try-out <page>`. That command writes nothing. It checks the log and reports who holds which face, the reason, and the start time. It says the lock holds only if that unreleased lockout is in the log. A second worker must be refused. Every later work command also checks the same fact before it writes.
3. Do the work only while your lock is on. In the shop, no one works on equipment that is not locked out by them. In wf, face-write, draft, pack, claim, return, check, signoff and close refuse unless this worker holds the unreleased lockout on the face that work belongs to (01, 04 or 05). While it is held, every other worker is refused.
4. Only you remove your lock. In the shop, only the worker who applied a lock takes it off, and that is recorded. In wf, `wf release <page>` is accepted only from that worker. It appends a release entry naming the lockout it closes. The lock lasts the whole work session and is released when the worker is done (Matthew, 12:57 PM EST).
5. No group lockout. In the shop, a hasp can hold several locks so a machine stays locked until every worker is done. Workshop does not allow that. One worker per face, and one worker per page at a time, so a page may have only one unreleased lockout. A second `wf lockout` on that page is refused, including a second lock by the same worker on another face. Release first, then start a new session.
6. Abandoned lock, supervisor override. In the shop, a lock left on after the worker has gone is removed only under a recorded supervisor procedure. In wf, `wf release <page> --override --reason T` is accepted only from Prima or Matthew (the page's person). It needs a reason. The log keeps the override, the reason, who overrode, and whose lock was removed. No one else may do it.

## Conflicts and open questions

The earlier "no session-long hold, do not add a command" flag is closed by the 12:57 PM and 12:58 PM answers. PENDING-RULES now records the t541 rule next to t533. These points remain:

1. Grant growth. New commands cannot be added from `src/cmd.rs` and `src/page.rs` alone. Help text and command dispatch live in `src/lib.rs`. The grant therefore grows to `src/cmd.rs`, `src/page.rs`, `src/lib.rs`, `tests/page_0423.rs`. 0408 already holds those three source files, so 0423 still waits on 0408 close, then takes all three. 0409, which also wants `src/lib.rs`, still waits until 0423 has freed them. Do not take `src/status.rs` or `src/board.rs` in this pack; the lock lives in the log, and the command prints the holder. Showing the lockout on `wf status` or `wf board` is for 0424 and later.
2. "Prima or Matthew" for override. This pack takes Prima as `--as Prima`, and Matthew as the page's person. If the page's prime is someone other than Prima, that prime may not override. If that reading is wrong, stop and raise it.
3. Faces 02, 06 and 08. t541 names lockout faces 01, 04 and 05 only. This pack still refuses a second worker from writing 02, 06 or 08 while a lockout is held. The worker who holds the lockout may write 02, 06 or 08 as part of that same session. A later ruling can give those faces their own lockout if needed.
4. Claim-until-return still stands inside the 05 session. A worker lockouts 05, then claims, works, returns, then releases. Return does not release the face lockout. A checker cannot start until the builder has released (or an override has). A packed but unclaimed pass is not an occupant. A returned pass waiting for a check is not an occupant once the builder has released.
5. Packing later passes is allowed only when no lockout is held on the page.
