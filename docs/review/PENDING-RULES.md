# Pending rules

Rulings that belong in a spec file but cannot be written there yet, because an open pass cites that file (t381u: a rule file never changes mid pass, only after review and before a new draft starts).

## t530u  -  band N6 holds worker pages

Status: pending. Apply to `docs/spec/seqAddr.md` as a versioned note (after section 11, the lab and stage bands) once 90.50.10.0705.05.01 is closed. That pass is returned, not closed, and its face 08 cites seqAddr.md section 11. Do not edit seqAddr.md, DIRECTOR-RULINGS.md or decisions.md while it is open.

Authority: t530u, docs/review/DIRECTOR-WORDS-t530.md. Verbatim: "N6 is where worker pages should live." "One page per worker" "The title should be the worker's name." And, for numbering: "First open slot after N600."

The rules, in plain words:

1. **Worker pages have their own band, `DD.SS.BB.0600-0699` (N6).** The band head `0600` is the door (seqAddr.md section 10, rule 4). Worker pages sit on `0601-0698`. `0699` is the band's continuation, not a worker page.
2. **One page per worker.** Not a shared workers page.
3. **The title is the worker's name, lowercase.** seqAddr.md:112: titles use lowercase letters, digits and hyphens, and start with a letter. So Grok-Check is titled `grok-check`. The exact name (including its capital letters) is kept in the page stamp and in the worker config. Exact-case titles would need a further ruling.
4. **The first page is the first open slot after 0600.** Today no 06NN page exists on packs or returns, so the first open slot is 0601.

Related, not an address rule: setup reports for a new worker chain on that worker's page (t530u Q1). Lab 0705 pass 05.02 is to fold that into the report-system design.

## t533u  -  one worker per page

Status: pending. Apply to the wf kit `docs/DESIGN.md` section 5 (Open), as a versioned note, once no open pass that pins or cites that file stands in the way (t381u). Do not edit the kit DESIGN.md, AXIOMS.md, DIRECTOR-RULINGS.md or decisions.md in this turn. 0408 is packed and holds `src/cmd.rs` and `src/page.rs`. Lab 0705.05.01 is still open and cites seqAddr.md section 11; this ruling is not a seqAddr band rule.

Authority: t533u, docs/review/DIRECTOR-WORDS-t533.md. Verbatim: "A page should never have one then one pass running at a time." "Once a worker is in a page, no other workers can use it." "We can run many pages in parralel but no more then one worker per page at a time."

The rules, in plain words:

1. **One worker per page at a time.** Many pages may run in parallel. A page must not have more than one pass running at a time.
2. **A worker is in the page from claim until return.** The active window is a pass whose tail is `open`. A packed but unclaimed pass is not an occupant. A returned pass waiting for a check is not an occupant.
3. **A page with a claimed, unreturned pass refuses any other claim on any pass of that page.** Same worker or a different worker, it does not matter. The refusal names the open pass and who holds it.
4. **The checker also enters the page.** `wf check` refuses while any pass on that page is claimed and not yet returned. After the return, the checker may enter.
5. **Packing may stage later passes, but only one pass is claimable or active at a time.** Prima must not pack two open passes of one page for different workers. That planning rule also lives in `docs/plan/GROK-BUILDER-QUEUE.md`.

Rules 2 and 5 are refined by t541u below: the active window is the lockout session, not only claim-until-return, and packing later passes is allowed only when no lockout is held. Rules 1, 3 and 4 still stand inside that session.

Related, not this ruling: the 0701 log overwrite is a `push_log` prefix bug. Page 90.50.10.0423 (title one-worker) is drafted to enforce this rule and the t541u lockout, and to make `push_log` / `wf return --push` refuse unless the published log is a prefix of the local log. It waits on 0408 close, then goes first in the queue, ahead of 0422. The 0701 repair plan is `docs/review/0701-LOG-REPAIR.md` (not done in this turn).

## t541u  -  face lockout (session lock)

Status: pending. Apply to the wf kit `docs/DESIGN.md` section 5 (Open), as a versioned note, together with the t533u rule above, once no open pass that pins or cites that file stands in the way (t381u). Do not edit the kit DESIGN.md, AXIOMS.md, DIRECTOR-RULINGS.md or decisions.md in this turn. 0408 is packed and holds `src/cmd.rs`, `src/lib.rs` and `src/page.rs`. This ruling is not a seqAddr band rule.

Authority: t541u, docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md. Verbatim: "A worker only holds the page when they are activelly working on it." "If it's being updated as 01 or more work on 05 or just the human readable version of the page's scope and design as 04." "One model should be working on it at a time." "It's the 05 face, 01 is the agents and scope, 04 is the planned out work we are doing on it. So the face must be locked while it's being worked on." "Lock the face for the whole work session, released when the worker is done." "It's a lock out. Look at lockouts as your template from industrial construction and maintaince safety practices."

The rules, in plain words:

1. **A page is held only while one worker is actively working on a face (01, 04 or 05).** One model at a time. Many pages may run in parallel. Between sessions, when no lockout is held, the page is not held.
2. **The face lock is a lockout.** It lasts the whole work session and is released when the worker is done. The template is lockout/tagout (LOTO) practice from industrial construction and maintenance safety.
3. **Each worker applies their own named lock and tag.** The log entry names the face, the worker, the reason, and the start time.
4. **Only the worker who applied a lock removes it.** The removal is a release entry in the log.
5. **Before work starts, try-out verifies the lock holds.** Work commands also check that this worker holds the unreleased lockout on the face they are working on.
6. **Group lockout is not allowed.** Several locks may not sit on one face, or on one page. A page may have only one unreleased lockout at a time.
7. **An abandoned lock is removed only by a recorded supervisor override.** Only Prima or Matthew (the page's person) may do it. It needs a reason. The log keeps it.
8. **While a lockout is held, every other worker is refused on that page.** Packing may stage a later pass only when no lockout is held.

Related: page 90.50.10.0423 (title one-worker) is drafted to enforce these rules, the t533u claim and check refusals, and the `push_log` prefix check. The grant grows to include `src/lib.rs` because lockout, try-out and release are new commands. This lockout is not the short `.wf-lock` file. The draft is not packed. It waits on 0408 close, then goes first in the queue, ahead of 0422.
