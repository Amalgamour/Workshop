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

Related, not this ruling: the 0701 log overwrite is a `push_log` prefix bug. Page 90.50.10.0423 (title one-worker) is drafted to enforce rules 3 and 4 in wf, and to make `push_log` / `wf return --push` refuse unless the published log is a prefix of the local log. It waits on 0408 close, then goes first in the queue, ahead of 0422. The 0701 repair plan is `docs/review/0701-LOG-REPAIR.md` (not done in this turn).

