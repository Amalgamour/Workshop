# Handover of 90.50.10.0416.05.01

Written: 2026-11-23, about 2:25 PM EST, by Prima.
Words: docs/review/DIRECTOR-WORDS-t547-handover-0416.md.
Rule: docs/review/PENDING-RULES.md (handover / lockout shift change).
This is a record and a check list. It does not pack anything, and it does not claim 0416.

## What happened

Matthew gave Grok-1 the 0416.05.01 prompt. Grok-1 may have run `wf claim 90.50.10.0416 1` locally, and may have edited `tests/wf.rs`. He then overwrote that prompt with 0407.05.01, so Grok-1 is now on 0407. Grok-2 was given 0408.05.01. Matthew: "we'll see if grok-2 can take it over without breaking it. You'll need to define that for checking."

Who takes 0416 next is not fixed here. The queue still names Grok-5. Matthew said Grok-2 may take it over, likely after 0408. The incoming worker, whoever it is, must follow the steps below.

## What is on GitHub (checked 2:25 PM EST)

origin/packs tip: `7c98e5b2c9b57d9a7723b1a756e15926635c6e64` (`wf: publish 90.50.10.0419`, 1:19 PM EST).

origin/returns tip: `10686c7d2412e21c4fa373a1c7e43f2362ea4a3b` (`report: Grok-Check check 90.50.10.0705 05.02`, 2:24 PM EST).

On packs, page 90.50.10.0416 is present. It was published as `77c22aae134f1743f880f40957f8423bfdc03389` at 1:19 PM EST. The log has seven entries, all from the pack itself:

1. init (matthew, 1:18 PM EST)
2-5. face writes (prima)
6. draft (prima)
7. pack (prima, 1:18 PM EST). Start `a823ee284574be3d9f6247925b9088137a27a539`. Pack hash `dce476c8a2f58191bc1cd577855920dcffa80dff99a0157a8cf3364269526b4f`. Grant: `tests/wf.rs`, `tests/page_0416.rs`. The pack names Grok-5 as the builder.

There is no claim, return, check, signoff, close, lockout, or release in that log.

On returns there is no `90.50.10.0416` log, no return file, and no report. The only "0416" hits are other pages mentioning that 0416 will fix the Windows tests.

So no 0416 claim or push has reached GitHub. If Grok-1 claimed or edited locally, that work was not published. The published page is still packed and unclaimed.

## The handover, from lockout shift change

In a shop, a worker does not leave a lock on and walk away. At a shift change they remove their lock, or a supervisor records an override if they have already gone. The incoming worker then puts on their own lock, tries it, and only then starts work. Workshop uses that same shape (t541u). Group lockout is not allowed, so two workers must not both hold 0416.

Today `wf release` does not exist. Page 0423 will add it. Until then, use only the tools we already have: `git fetch`, `git log`, `git diff`, `git status`, the published packs and returns logs, `wf status` and `wf verify` (read only), and the report file in docs/plan/REPORTS.md.

### Outgoing worker (Grok-1)

Either:

- push a release, once 0423 exists, or
- state clearly that no claim was pushed.

Grok-1 has already moved to 0407, so Prima records the second form here: no 0416 claim was pushed to origin packs or origin returns, as of 2:25 PM EST. If Grok-1 still has a local claim or dirty `tests/wf.rs` in `D:\Git\grok1`, that must not be pushed later. Do not return that local claim. Do not use that folder to finish 0416 while Grok-1 is on 0407.

If a published claim had existed, the book Prime would override it with a recorded reason (t541u). That is not needed on GitHub today, because nothing was pushed.

### Incoming worker (before any claim)

Verify the state first, in this order:

1. Fetch origin packs and origin returns.
2. What's claimed: read `pages/90.50.10.0416/log.jsonl` on packs, and look for a returns log at `.workshop/logs/90.50.10.0416/`. Today the packs log should still end at the pack (entry 7). There should be no returns log. If a claim has appeared, stop and raise it.
3. What's pushed: `git log origin/packs -- pages/90.50.10.0416` and `git log origin/returns -- .workshop/logs/90.50.10.0416`. Today only the pack publish is there.
4. What's dirty: in the incoming worker's own folder, `git status` and `git diff`. The work folder must not already hold someone else's uncommitted 0416 edits. Do not copy unpublished files out of `D:\Git\grok1` unless the report names every file and every line taken.
5. Then claim, if the published log is still unclaimed: `wf claim 90.50.10.0416 1`.

The return and the report (docs/plan/REPORTS.md) must state the handover: who left, who took over, that no claim had been pushed (or what was found if that has changed), and whether any of the first worker's local work was used.

### What the checker looks at

On a handed-over pass, Grok-Check looks at all of the following. Each item names the tool.

1. **Published tips.** `git fetch` origin packs and origin returns. Record both tip SHAs in the check report.
2. **Log chain.** The packs log, and the returns log if one exists, must be an exact prefix-extension: every earlier entry still present, in order, with the same hash chain. No entry rewritten or dropped. `wf verify 90.50.10.0416` must say ok on the checker's intake of the published log.
3. **Who claimed.** The first claim in the published log must be the incoming worker. There must not be a published claim by Grok-1. If the outgoing worker said no claim was pushed, the logs must match that.
4. **Handover statement.** The incoming worker's return and the report file under `reports/90.50.10.0416/05.01/` must state the handover in plain words. If that statement is missing, the check fails.
5. **Granted files only.** `git diff a823ee284574be3d9f6247925b9088137a27a539 <return-commit>` (the pack start, to the return commit). The only paths that may change are `tests/wf.rs` and `tests/page_0416.rs`. Name any other path. A change outside the grant fails the check.
6. **No silent mix-in.** That same diff, plus `git log` on those paths, plus the report. If work from Grok-1 appears in the return, the report must say so and say what was kept or discarded. Code from the first worker that is not recorded in the log or the report is a fail.
7. **One holder.** After the incoming claim, the log must not show two open claims. Until 0423 exists, this is judged from the published log events, not from a lockout command.

A dirty file on a local machine is not proof. The checker judges the published logs, the published return, the git commits, and the report.

## Interim, until 0423 lands

- The next builder's report must state the handover, as above.
- The checker must compare the git diffs, as in items 5 and 6.
- Prima's record that no claim was pushed is this file, at 2:25 PM EST. If that changes, write a new note; do not rewrite this one.
