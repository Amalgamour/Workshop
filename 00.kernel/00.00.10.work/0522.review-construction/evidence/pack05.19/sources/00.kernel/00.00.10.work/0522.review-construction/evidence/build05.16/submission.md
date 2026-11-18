# Submission — 0522.review-construction/05.16

Schema: `n5-instance-binding-submission/0516`
Date: 2026-11-04
Executor: Grok-2
Reviewer: Codex Prime
Source pack: `0522.review-construction/05.16.md`
Proof stamps: `D:\librarian\temp\0522-0516\repro-frozen` and `D:\librarian\temp\0522-0516\suite-20261104`

## Did

The pack source manifest matched before the note. Schema `prime-pack-inputs/1`, 524 files, 0 missing, 0 mismatches, 0 snapshot mismatches, sha256 `39598861c1d771fddbbc46b17e093b5416240bf3b183e6b9cc53b8530c129139`, 163132 bytes, 0 CR characters.

Frozen pass04 recorded one external N5 review and a directory copy of that book read current. pass04, pass05, and the v7 door each returned exit 0 and stale false on the copy. The stored review id is `wd968ebf5cc30efc4`. The original intake, journal, and record bytes stayed in place. Details are in `REPRO.md`.

`06.34.md` records the identity rule and was written before the candidate. The candidate is unselected:

- `labs/review-instance-binding-pass01/workbook.py` `3f8118ccdc2c7afc4abdca2d52c3510864f159642ed06aee52a485709be55aba`, 5916 bytes
- `labs/review-instance-binding-pass01/review_loop_tools.py` `134221019b9854bc44529ff6a909c99c464bc3515a3e39da5536b2524d00cb22`, 13142 bytes
- `labs/review-instance-binding-pass01/review-loop.json` `e15856d136e4721856b530a552d9115ecb1b90a62cc9905eb80d79709d2dd26f`, 5278 bytes, schema `review-loop-pins/8`
- `labs/review-instance-binding-pass01/candidate/app/librarian.py` `a0de0b4fbd935e65d061836794d1d11bb19c22932d080bb9ca06a56edd947561`, 12397 bytes

`app/librarian.py` remains `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes. The author suite exited 0, 18 pass, 0 fail. Same-instance prepare, form, and read stdout matched pass05. The copied book is held with reason `different-root` through the workbook, the door, and the candidate librarian. Publish on the copy is refused and the page bytes stay. Historical judgment and next_action stay available on read, recover, inspect, and the publish refusal. form does not carry the hold. N7 prepare, read, copy-read, and malformed prepare stdout matched pass05. `custody-missing` remains on the N7 control and `n1-not-applicable` does not appear.

## Blocked

Dispatcher selection is not this pack. Native custody for `0122.review-construction` is not available: the member directory is absent. The legacy allocator was not called. No receipt was invented. No record, publish, reserve, or capture ran on the live work book. No lab root adapter was added. The N7-local book check and Grok-1's capacity successor were not consumed.

A copied N5 record is not current. It is not published as locally applicable. accepted, approved, authority, closes_work, releases_action, published_work, and eligible_for_custody_completion stay closed. A full rewrite of both stored book and stored instance_id to the live root is indistinguishable from a record made on that root. This pack does not invent a registry to detect that rewrite.

## Need

Prime review of this page. Later composition calls `n5_instance_hold`, then the accepted N7-local book check, then pass02 row comparison, on one workbook chain. That composition is not built here.

## Factfind

The publication guard is `do_publish`'s `source_changed` branch. The record guard is the repin refusal. `prime-guard` remains the pinned read-only Prime command. Observation is each command's own read. There is no new concurrency, power-loss, or AR-01 guarantee. The suite runs each case once and keeps the first failure list. That list is empty.

## Hostile

H1 rewrites the stored book string to the live resolved path and leaves the stored instance id. H2 rewrites the stored instance id to the live id and leaves the stored book path. Both read exit 1 with reason `identifier-disagreement`, and the review record bytes stay. A missing instance id is `unbound`. A stored absolute path that does not resolve is `relocation-or-clone`. A relative stored book is `unbound`. A copied workbook and a copied door each exit 2 with the canonical-root refusal. A missing declaration, a schema `review-loop-pins/7` declaration, a missing v4 pin, and a flipped workbook byte are refused before launch.

## Overflow

The reproduction stamp and the suite stamp stay under `D:\librarian\temp\0522-0516\`. They are the external roots for this run. They are not a durable archive. `suite.json` and `repro.json` in this evidence directory are the copied reports. `INDEX.md` names the paths and hashes. No other worker file was edited. `06.33.md` stays in its own slot.
