# Director words: t533u (2026-11-23, about 12:28 PM EST)

Matthew, verbatim:

> A page should never have one then one pass running at a time.  This is a dangerous thing in construction when you have too many workers in one space.  So you don't have plumbers in the same room as electrictions that is overloading a space.  Once a worker is in a page, no other workers can use it.  We can run many pages in parralel but no more then one worker per page at a time.

Reading: a page must not have more than one pass running at a time. Many pages may run in parallel. Once a worker is in a page, no other worker may use that page.

A worker is in the page from claim until return (the pass tail is `open`). That is the active window. A packed but unclaimed pass is not an occupant. A returned pass waiting for a check is not an occupant.

The checker also enters the page. A check must refuse while any pass on that page is still claimed and not yet returned. After the return, the checker may enter. A second claim on any pass of the page is refused while a claim is still open, including a claim by the same worker on a different counter.

Packing may stage later passes (draft, and a pack that is not yet the active claim). Only one pass is claimable or active at a time. Prima must not pack two open passes of one page for different workers.

This is a safety rule. It is recorded in docs/review/PENDING-RULES.md until it can be written into `docs/DESIGN.md` section 5 (Open) in the wf kit. That kit file is not edited in this turn (open packs pin it, including 0408; t381u). The wf enforcement is drafted as page 90.50.10.0423, title one-worker, which also carries the 0701 `push_log` prefix check. 0423 waits on 0408 closing, then goes first in the queue, ahead of 0422.
