# Prime use — real book request

This file is the handoff for Codex Prime. The builder demonstration below is not adoption. Prime still uses the request, reviews the output, and records whether it reduces manual reconstruction.

## Request

Absolute path:

`D:\Git\lib-build\labs\prime-desk-use-pass01\request.json`

sha256 `87f5d657304025ef6654688170226bcb921d9eca5cee11a0fc4bd8a898242e93`, 7306 bytes.

Run from `D:\Git\lib-build` with `PYTHONDONTWRITEBYTECODE=1`. The builder used Python 3.14.0 at `C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe`.

```text
python -B labs/prime-desk-pass03/prime_desk.py view --request D:\Git\lib-build\labs\prime-desk-use-pass01\request.json
python -B labs/prime-desk-pass03/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass01\request.json --work-id work-0524-0503
python -B labs/prime-desk-pass03/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass01\request.json --work-id work-0522-0505
```

Add `--json` for the machine view. The builder's stdout is in `evidence/build05.04/run/`. Commands and exits are in `evidence/build05.04/commands.txt`.

## How to inspect one work item

The second command expands the canonical packet. Relation on that run was `current`. Canonical id and packet work id were both `work-0524-0503`.

The third command inspects the other registered page. On that run the selected id stayed `work-0524-0503`, the relation was `inspection`, and the packet work id was `work-0522-0505`. Criteria on that packet were `crit-0522` only. The inspection gap says the selection was not changed.

Any other `--work-id` has to be a row already in this request. This request has those two ids.

## What the builder run showed

View and both packets exited 1, state `attention` on the canonical view. Selected address `0524.prime-desk/05.03`. Rule `assignment-record/v1`. Review path `0524.prime-desk/05.03.md`, file matched, judgment unknown. Return path `0124.prime-desk/05.03.return.md`, undeclared, custody unknown. The 0522 return path `0122.review-construction/05.05.return.md` is also undeclared, custody unknown. Catalog `used_for_selection` false. Coverage matched 16 of 16. Fingerprint `3956f4ca6b90469c666d3624f24dd2a7e8cf9fb2b754f05e0e3457a56023f644`.

Open declared attention: 0. Gaps on the view: `return-undeclared`, `catalog-not-chosen` for `work-0522-0505`, and `verification` because no matched verification is bound to the canonical work.

A second process recovered the same selected id, fingerprint, gap kinds, and empty attention list. `observed_at` changed. The fingerprint string does not include that clock.

Director bytes 111:403 of `0420.prime-desk/06.01.md` and model bytes 430:834 are separate spans. The packet prints them under `### Director wording` and `### Model explanation`. The markdown uses `### Review` and `### Return line`. It has no `Review home` heading.

The markdown view is 65 lines. The overview before `## Packet` is 66 lines. The packet then quotes the task page. Those counts do not establish that the overview is readable or complete.

## Limitations

Declared paths only. Unregistered sources were not searched. That is not a report that none exist.

`00.kernel/00.live.md` was read for a before/after hash and was not edited. It is not a declared request path. Workers are an empty list. Process activity stays unknown.

Supplied sentences `sup-lanes` and `sup-prima` are in `run/view.json` under `supplied_without_worker`. The markdown Workers section says none are declared. The same sentences are inside the quoted checkpoint `0420.prime-desk/06.07.md` in the packet. Pass03 was not changed. A later pack can print `supplied_without_worker` in the markdown Workers section. This pass does not do that.

Section 1 of the markdown view lists goal, scope, and authority. The checkpoint is on the selected-work lines. Reporting policy and the retained prior assignment appear in the packet under Dependencies and Desk policy.

Exit 1 is attention. It is not approval and it is not acceptance. Judgment stays unknown. `assignment_state` `returned` is a record field. `validate_context` was not called.

The pass03 suite was not repeated. `labs/prime-desk-pass03/prime_desk.py` stayed sha256 `cd1e74aa0a51b52dcedaa544b4fd1f2de90f84bf69a8c21234ef362ae2a5f812`, 77622 bytes.

## Stale copy, already shown

`run/stale-book` is disposable. Its request is `run/stale-request.json`, sha256 `45bd63a4421041818f974a6290356aa4b35b4b9f59b11892ed6d5200b596cad9`. The first view selected `work-0524-0503`. After the marker `STALE-MARKER-NOT-A-SOURCE` was appended to that copy only, the second view withheld the page, left selected null, and did not contain the marker. The live `0524.prime-desk/05.03.md` stayed sha256 `c8851a91f7dfbcadd13124988fae7057ff94b7dbef5971effc9aebb9c9123dc7`, 8326 bytes. Do not edit a live source to reproduce this.

## Manual steps that remain

1. Run the three commands above, or read the captured stdout and rerun any command you want to witness.
2. Record whether the overview and packet reduce the reconstruction you still do by hand.
3. Leave custody unknown until a later request declares a real return file. Do not create `0124` or `0122` return files from this handoff.
4. Leave the Review section of `05.04.md` for Codex Prime.

## When a new request is necessary

Write a new request when a declared file's bytes change, when coverage must add a path, or when Prime deliberately accepts a revision. `request_index.py` will not overwrite this `--out`. A mismatch without `--accept` writes nothing and prints `revision`. `--accept` belongs on a new output path, and only for a revision Prime has decided to take.

Do not put `0524.prime-desk/05.04.md` or `evidence/build05.04/artifact-manifest.json` into that request. Primary work stays `0524.prime-desk/05.03`.

This request does not seat `00.live`, file 0124 custody, or activate the desk.
