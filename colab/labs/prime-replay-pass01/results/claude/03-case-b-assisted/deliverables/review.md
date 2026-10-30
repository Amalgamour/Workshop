# Review — case B (0514.review-packet 05.01, member 0167), ASSISTED condition

Reviewer: claude-opus-5-5, Colab run 03-case-b-assisted. A lab output, not a live review.

**Disclosure.**
- **Builder:** Grok Builder 1 (submission `grok-1-0514-0501`), not me.
- **My exposure:** I have used this module as a pinned dependency (prime_cycle `packet`), and I wrote that caller.
- **Circularity:** in this assisted condition, the subject tool (review_packet, f658cbe4, byte-identical in `assistance/` and in the subject) helped assemble its own review packet.
- **Carryover:** from case A I already knew the frozen reader fails and that the default packet holds only the return and receipt. I also knew the 0163 return, which this subject used as a specimen.

## Did, Blocked, Need
**Did:**
- prime_cycle `read --templates` (observation failed, as in run 02), `packet`, `record` (refused), a re-read, and `day`, all journalled;
- direct reads of the assignment, the return, CONTRACT.md and REAL-USE.md;
- re-ran the subject's tests in the disposable copy;
- a direct `review_packet assemble` with the 0514 artifact-manifest checked against the disposable commit, live included;
- a code check of the link refusal.

**Blocked:** no typed review record. prime_cycle record refuses: `observation failed: reader exit 2`, because the frozen bundle lacks `labs/prime-support-pass01/clerk_adapter.py`. This is the same lab omission as run 02. The judgment is in `out/decision-case-b.json` and here.

**Need:** nothing for case B. For the lab, the reader's dependency should be added to the bundle.

## Verified versus claimed

| claim (return 0167) | status | how |
|---|---|---|
| Tests: ran 10, skipped 1 (file symlink, WinError 1314), failed 0 | **verified** | re-run here: `Ran 10 … OK (skipped=1)`, the same skip reason; the junction refusal passed |
| Custody complete, receipt bf8cef9f…, 7 payloads | **verified, by the reviewed inspector and helper** | packet custody.json `complete`, problems none; helper verify `result complete` |
| Pins: helper 8f3da5c6…, inspector 947915fe… | **verified** | sha256 of the subject copies equal the contract |
| Own artifact manifest binds the build | **verified** | direct assemble: artifact-manifest/1, 19 rows, all `historical-match`, live equal, no origin conflicts |
| Unknown schema reported, not interpreted (0164 pin manifest) | **verified by test** | `test_changed_live_artifact_and_unknown_schema` ok. The specimen bytes were not re-assembled: their commits are not in the disposable repo. |
| 0163 specimen: 69 rows, 41 historical-match and 28 changed-live | **claimed; internally consistent** | not reproducible here (commit 749cfd9c is absent from the disposable repo). REAL-USE explains the hand 27 against the tool 28 as README changing between observations. |
| Never says "corruption" | **verified by test** | `test_module_does_not_label_drift_as_corruption` ok |
| No acceptance or authority inference | **verified** | packet.json `acceptance`, `approved`, `published`, `seated` and `authority_inferred` false; `next_task` null; the fixed statement is present |
| Link and reparse refusal | **partly verified** | the junction is tested; the file-symlink test skips; the code path exists (`is_reparse`, `ancestor_link`) |

## Defects and meaningful unknowns
- **No defect found against the 0514 05.01 grant.** #01–#05 are each met by the code, the tests or the evidence above.
- **Unknown:** file-symlink refusal on this host. It is implemented but untested here.
- **Pack ambiguity (not a builder defect).** #04 says "Do not open Claude's uncommitted benchmark work", and also "the helper must explain differing live bytes". The 0163 specimen hashed live row files (`compare_live: true`) without copying or reading their text, and disclosed that. That is a reasonable reading. Whether hashing counts as "opening" is Prime's call; I would accept it.
- **Caller-side observation (not this lane):** prime_cycle's default `packet` requests no artifact checks. The helper supports them well; the caller underuses it.

## Disposition
- **Pass:** finished, accepted.
- **Goal** ("a bounded mechanical packet for reviewing a return, preserving exact evidence and leaving judgment and authority with Prime"): **completed** as supplied. The tool exists, its claims reproduce, and it keeps judgment and authority out. One limit stays: the file-symlink refusal is untested on this host.
- **Director:** not needed.

## Preservation
Member 0167, the requests, both specimens and the subject code are unchanged. My packets are under `out/` only.

## One bounded next action
None for this lane: NO PACK REQUIRED (next-pack.md).

## Factfind
- The packet in prime_cycle's default form held only the return and receipt, so the substantive review needed CONTRACT, REAL-USE and the code read directly.
- A direct `review_packet` request with `artifact_manifest` added the most useful mechanical fact here: 19/19 rows bound.

## Hostile
The path that should break: treating "assembly complete, custody complete" as acceptance. The packet itself refuses that reading. The face I was tempted to obey: the tool's own view saying `no-return` for a captured, verified member, which is wrong (the adapter defect from run 02).

## Overflow
- I did not re-assemble the two historical specimens: their commits are not in the disposable repo.
- The 0163 specimen's 28 changed-live rows record the live bench being edited at the time. That links to case A's later history, which I did not inspect.

## Unprompted
The assisted route here gave real mechanical value: custody, plus artifact rows through a direct request. But it needed a hand-written request, with paths, commit and python typed. The prime_cycle `packet` default would have missed the artifact check.
