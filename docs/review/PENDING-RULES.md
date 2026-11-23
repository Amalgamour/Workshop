# Pending rules

Rulings that belong in a spec file but cannot be written there yet, because an open pass cites that file (t381u: a rule file never changes mid pass, only after review and before a new draft starts).

## t530u  -  band N6 holds worker pages

Status: pending. Apply to `docs/spec/seqAddr.md` as a versioned note (after section 11, the lab and stage bands) once 90.50.10.0705.05.01 is closed. That pass is returned, not closed, and its face 08 cites seqAddr.md section 11. Do not edit seqAddr.md, DIRECTOR-RULINGS.md or decisions.md while it is open.

Update (23 Nov 2026, 2:55 PM EST): 0705.05.01 and 05.02 are closed passed, so that lock is gone. Matthew's words fully define the band rule (rules 1-4 below; the door and continuation follow from seqAddr.md section 10, rule 4, and the lowercase title from seqAddr.md:112). But 90.50.10.0418.05.01 is packed and open, and its face 01, face 08 and PACK.md cite `seqAddr.md:199-204` on prima/build (the t512 seated-05 rule). By t381u, seqAddr.md does not change while that pass is open. So the note waits until 0418.05.01 is closed (or until Matthew says an append after section 11 may go in while 0418 is open).

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

Authority: t541u, docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md. Verbatim: "A worker only holds the page when they are activelly working on it." "If it's being updated as 01 or more work on 05 or just the human readable version of the page's scope and design as 04." "One model should be working on it at a time." "It's the 05 face, 01 is the agents and scope, 04 is the planned out work we are doing on it. So the face must be locked while it's being worked on." "Lock the face for the whole work session, released when the worker is done." "It's a lock out. Look at lockouts as your template from industrial construction and maintaince safety practices." "Only Prima or Matthew may break an abandoned lock, with a reason." "Project lead of the book can break or higher authority." "The book has a prime or lead, that is the position below the director/person."

The rules, in plain words:

1. **A page is held only while one worker is actively working on a face (01, 04 or 05).** One model at a time. Many pages may run in parallel. Between sessions, when no lockout is held, the page is not held.
2. **The face lock is a lockout.** It lasts the whole work session and is released when the worker is done. The template is lockout/tagout (LOTO) practice from industrial construction and maintenance safety.
3. **Each worker applies their own named lock and tag.** The log entry names the face, the worker, the reason, and the start time.
4. **Only the worker who applied a lock removes it.** The removal is a release entry in the log.
5. **Before work starts, try-out verifies the lock holds.** Work commands also check that this worker holds the unreleased lockout on the face they are working on.
6. **Group lockout is not allowed.** Several locks may not sit on one face, or on one page. A page may have only one unreleased lockout at a time.
7. **An abandoned lock is removed only by a recorded supervisor override.** The book's Prime (the lead, one position below the Director) or a higher authority (the Director, who is the person) may do it. It always needs a reason. The log keeps it. The book's Prime belongs on the book identity page `DD.SS.BB.0000` face 00 (seqAddr.md sections 1.4, 1.5 and 6). wf does not record it yet; that is pending page 90.50.10.0425. Until it exists, only the person may override. A work page's Prime is not enough.
8. **While a lockout is held, every other worker is refused on that page.** Packing may stage a later pass only when no lockout is held.

Related: page 90.50.10.0423 (title one-worker) is drafted to enforce these rules, the t533u claim and check refusals, and the `push_log` prefix check. It reads the book's Prime; it does not create the identity page. Recording that Prime is pending page 90.50.10.0425 (title book-prime). The 0423 grant grows to include `src/lib.rs` because lockout, try-out and release are new commands. This lockout is not the short `.wf-lock` file. Neither page is packed. 0423 waits on 0408 close, then goes first in the queue, ahead of 0422.

## t547u  -  handover (lockout shift change)

Status: pending. Apply to the wf kit `docs/DESIGN.md` section 5 (Open), as a versioned note, together with the t533u and t541u rules, once no open pass that pins or cites that file stands in the way (t381u). Do not edit the kit DESIGN.md in this turn. 0423 will enforce release and lockout in wf; it is not packed yet. Until then this rule uses only the tools we already have.

Authority: t547u, docs/review/DIRECTOR-WORDS-t547-handover-0416.md. Verbatim: "I had given grok-1 the previous prompt for it but you then said not to unless it finished 0407, then I gave it and overwrote it with the current prompt for grok-1 and gave the new prompt for grok-2 to grok-2" "we'll see if grok-2 can take it over without breaking it. You'll need to define that for checking."

The rules, in plain words, from lockout/tagout shift change:

1. **A worker who leaves a page must not leave a hidden hold.** In the shop, you remove your lock at the end of a shift, or a supervisor records an override if you have already gone. The incoming worker then applies their own lock, tries it, and only then starts work. Two workers must not both hold the same page (t541u: no group lockout).
2. **The outgoing worker either releases, or is overridden.** Once 0423 exists, they push a `wf release`, or the book Prime records an override with a reason. Until 0423 exists, they (or Prima, if they have already left the prompt) must state in a published note or report whether a claim was pushed. Do not push a late local claim after leaving the work.
3. **The incoming worker verifies the state before claiming.** They fetch origin packs and origin returns, then check three things: what is claimed in the published log, what is dirty in their own work folder, and what has been pushed. They do not start from another worker's unpublished files unless the report names every part taken.
4. **The checker verifies the handover.** On a handed-over pass the checker looks at: the published packs and returns tips; that the log chain is unbroken (an exact prefix-extension, `wf verify` ok); that the first published claim is the incoming worker; that the return and the report state the handover; that `git diff` from the pack start to the return commit touches only granted files; and that no work from the first worker was silently mixed in without being recorded in the log or the report. Dirty local files are not proof. Only published logs, published returns, git commits, and the reports count.
5. **Interim, until 0423 lands.** There is no `wf release` command today. The next builder's report must state the handover, and the checker must compare the git diffs. Use only `git fetch`, `git log`, `git diff`, `git status`, the published packs and returns logs, `wf status`, `wf verify`, and the report file in docs/plan/REPORTS.md.

Related: the 0416.05.01 case, and the exact checker list for that pass, are in `docs/review/HANDOVER-0416.md`. As of 2:25 PM EST on 2026-11-23, origin packs has the packed unclaimed 0416 page, and origin returns has no 0416 claim or push.

## t557u  -  manual return when wf fails

Status: approved by Matthew (t557s2212, 2:45 PM EST, 23 Nov 2026). He picked the default on all three questions. This is a process rule for builders and checkers. Keep it in `docs/plan/MANUAL-RETURN.md` until it can be written into the wf kit `docs/DESIGN.md` section 5 (Open), together with the t533u, t541u and t547u rules, once no open pass that pins or cites that file stands in the way (t381u). Do not edit the kit DESIGN.md in this turn. 0423 will add lockout and release in wf; it is not packed yet. Until then this process uses only the tools we already have: git, the report file, and a last-resort paste to Matthew.

Authority: t557u and t557s2212, docs/review/DIRECTOR-WORDS-t557-manual-return.md. Verbatim: "We need a process for a manual return if the compute isn't working. So what it does if the prompt and the pack don't execute correctly." Then, picking the defaults: "the granted files plus the report, with no second copy." "Prima and the checker may review while the tag is open, and no other builder may claim the page." "pasting the report is a last resort only, and the pass never closes until the report is committed."

The rules, in plain words, from lockout/tagout (when equipment fails, tag it out of service and record it; never bypass it by hand):

1. **If wf fails, stop and retry at most once.** Same command, same arguments. If it fails again, do not keep trying, and do not switch wf binaries on your own. Triggers include a wf error, a failed claim, verify flagging a hand edit, a template or version mismatch, a rejected push, a stale `.wf-lock`, a blocked network, or a pack that does not match the repo.
2. **Never bypass wf by hand.** Never hand-edit `.workshop` logs or the `log.jsonl` hash chain. Never fake a claim, a return, a check, or a close. Never remove a `.wf-lock` on your own judgement.
3. **Save the work and a report on `returns`.** Keep the work inside the grant. The location is the granted files plus the report, with no second copy (t557s2212). Stage files by path only (never `add -A`, never `commit -a`). Commit with the trailer `Builder: <name>`. The report path is `reports/<page>/05.NN/<Builder>-MANUAL-RETURN-<stamp>.md`, with the fixed fields in `docs/plan/MANUAL-RETURN.md`. Never force push. If the push fails too, paste that same report to Matthew in one block. A paste is last resort only. The pass never closes until the report is committed to `returns`.
4. **The builder keeps the page while the manual return is open.** This is not a handover (t547u). The manual-return record releases the face lock. Prima and the checker may review while the tag is open. No other builder may claim the page until the tag is cleared.
5. **A manual return never closes as passed without the checker's review.** Prima and the checker confirm the diff stays in the grant, run the tests, and confirm the log chain was not touched. Then either fix wf and re-run normal intake for the same pass, or, if wf cannot be fixed soon, record a manual intake through wf once wf works, with a note saying it was a manual return. The wf failure itself becomes a bug note or a page.

Related: the full process, the report fields, and the prompt block are in `docs/plan/MANUAL-RETURN.md`. The three questions were decided at t557s2212 (defaults). If wf still works and only the network is down, first follow labs/0705 FAILURES.md.

## t558s2225  -  report-system rollout and offline return

Status: approved by Matthew (t558s2225, 2:53 PM EST, 23 Nov 2026). He picked the default on both questions (M1, M2 in docs/review/ANSWERS-0422-PLAN.md). Write it into the wf kit `docs/REPORTS.md` when 0422.05.05 adds that doc, and into the wf kit `docs/DESIGN.md` section 5 (Open) with the other pending wf rules, once no open pass that pins or cites that file stands in the way (t381u). The 0422 pack texts on returns (labs/0422-plan/) carry it until then.

Authority: t558s2225, docs/review/DIRECTOR-WORDS-t558-report-system.md. Verbatim: "warn and carry on, and block later" (M1). "not now, use the manual return" (M2).

The rules, in plain words:

1. **A run folder with no report config warns and carries on (for now).** wf runs the command as before, writes no report entry, and ends with lines naming `.wf/config.json`, docs/plan/REPORTS.md and `wf setup`. The worker pushes the stopgap report. There is no flag. A config that is present but invalid still refuses.
2. **Block later.** A later small pass brings back the refusal for a missing config. Prima packs it only when every active worker has a setup report on its N6 page.
3. **A configured worker's real `wf check` always writes and pushes its report** (t530u Q3, "Always"). Rule 1 does not loosen that.
4. **An offline return is a manual return, not now a wf feature.** An offline `return --push` still fails at the fetch and records nothing. The builder follows docs/plan/MANUAL-RETURN.md. A return counts when it lands on `returns` (t557s2212 Q3). Recording an offline return locally is not queued.

