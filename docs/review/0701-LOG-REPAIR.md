# 0701 log repair plan

Plan only. Do not do this repair in the same turn as t533u. Do not publish-pack 0701 until the repair is done.

Times are America/Toronto (EST, UTC-5). The facts are in docs/review/DRIFT-0704-RESPONSE.md.

## What is wrong

The live log on `origin/returns` (`.workshop/logs/90.50.10.0701/log.jsonl`) has 24 entries. Entries 1-22 are a shared prefix, through the pack of 05.02 and 05.03. Entries 23-24 are the 05.02 claim and return (Grok-1, 10:47 AM and 10:49 AM EST, log commit `a3a0f83a`, work commit `018892ba`).

The 05.03 claim and return were written first (Grok-1, 10:38 AM and 10:41 AM EST, log commit `b71ab3e0`, work commit `b142884d`) as entries 23-24, hashed from entry 22. `push_log` later overwrote those two slots with the 05.02 events. `b71ab3e0` is still an ancestor of `origin/returns`. This was not a history rewrite.

The 05.03 pack is still in the live log (entries 20-21). The return file `.workshop/returns/90.50.10.0701.05.03.md` and `tests/lab_0415.rs` are still on the tip. Packs still has only the 22-entry prefix (`pages/90.50.10.0701/log.jsonl`). Views from the current tip would show 05.03 as packed but never claimed, which is wrong.

## What must not happen

- Do not rewrite entries 23-24. The log is a hash chain. The 05.02 claim and return now occupy those sequence numbers.
- Do not force-push `returns` or `packs`.
- Do not hand-edit `log.jsonl` or page views. `wf verify --fix` reprints views from the log; nobody writes page files directly.
- Do not publish-pack 0701 until entries for the 05.03 claim and return exist again, as new events after the current head.
- Do not use today's `push_log` against a stale run-folder log. Prefer to repair after 0423 lands, or push the repaired log by path only after an explicit prefix check.

## The repair

Append the preserved 05.03 claim and return as new entries 25 and 26, hashed from the current head (entry 24). They will be new wf events. They will not carry the original timestamps or the original entry hashes from `b71ab3e0`. The write-up must cite `b71ab3e0` as the original filing, so the record does not pretend 25-26 are those earlier events.

Recommended steps, in order:

1. Wait if possible until 90.50.10.0423 is packed, returned, checked and closed, so `push_log` can no longer overwrite a published suffix. If the repair cannot wait, skip `wf return --push` and push the log by path only after the prefix check in step 6.
2. In a clean run folder, fetch `origin/returns` and intake 0701 only. Confirm the local log has 24 entries, that 23-24 are the 05.02 claim and return, and that 05.03 is at pack. Do not publish-pack.
3. Copy out the original events from `git show b71ab3e0:.workshop/logs/90.50.10.0701/log.jsonl` (entries 23 and 24 there): actor, times, return text, pack hash, work commit `b142884d`, return file path. Keep that copy as evidence, not as a file to paste into the live log.
4. Confirm the work is still on the tip: `tests/lab_0415.rs`, `.workshop/returns/90.50.10.0701.05.03.md`, and that `b142884d` is an ancestor of `origin/returns` and of the 05.03 pack start.
5. File a new claim of 05.03 as Grok-1, then a new return of the existing work commit `b142884d` and the existing return file. That is a replay through wf, so `Page::add` chains entries 25 and 26 from the current head and reprints the views. Grok-1 should file it, or Prima only with Director leave. Do not invent a different builder. Do not restore the original timestamps by editing the log. In the repair note (the return `noticed:` line, or a short docs/review addendum), say that these events replay the filing first made at `b71ab3e0`.
6. Before any push, fetch `origin/returns` and confirm `.workshop/logs/90.50.10.0701/log.jsonl` is still an exact prefix of the local log (24 entries, then the two new ones). Only then commit the log by path and push, with no force. If 0423 is already in, `wf return --push` may do this itself.
7. Intake the repaired log and publish-pack 0701 only. Packs should then have 26 entries: the 22-entry prefix, the 05.02 claim and return, and the replayed 05.03 claim and return. Views should show both 05.02 and 05.03 as returned. Confirm 05.md matches the log. Leave other pages alone.

If step 5 cannot go through wf (for example a rule change mid-repair, or the existing return file no longer satisfies the current template), stop and raise it. Do not splice JSON into the log by hand.

## Why this waits

0423 will refuse a divergent `push_log`, which is what broke this log. The live 05.02 suffix is already the published history and must stay. A later intake of the unrepaired tip would publish that suffix to packs and make 05.03 look unclaimed. Packs has not taken it yet. That is why the repair comes first.
