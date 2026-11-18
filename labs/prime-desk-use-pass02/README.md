# prime-desk-use-pass02

Operator guide for one pinned request against the live book. The desk code is `labs/prime-desk-pass04`. This directory does not contain a second selector.

## Request

`D:\Git\lib-build\labs\prime-desk-use-pass02\request.json`

Source list: `source-list.json` in this directory. Catalog copy: `catalog.json` in this directory. The request binds `00.kernel/00.00.10.work/0524.prime-desk/evidence/build05.05/catalog.json`. Those two catalog files are the same bytes.

Run from `D:\Git\lib-build` with `PYTHONDONTWRITEBYTECODE=1`.

```text
python -B labs/prime-desk-pass04/prime_desk.py view --request D:\Git\lib-build\labs\prime-desk-use-pass02\request.json
python -B labs/prime-desk-pass04/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass02\request.json --work-id work-0524-0504
python -B labs/prime-desk-pass04/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass02\request.json --work-id work-0522-0505
python -B labs/prime-desk-pass04/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass02\request.json --work-id work-0707-0501
```

Exit 1 on these commands is attention. It is not a failed command and it is not approval. The builder demonstration exited 1 on each of them. Captured stdout is under `00.kernel/00.00.10.work/0524.prime-desk/evidence/build05.05/run/`.

## What the request registers

Current work comes from `0401.goal/06.01.md`, the assignment path named by `app/development-workspace.json`. That record names `0524.prime-desk/05.04.md`, state `returned`. The registered id is `work-0524-0504`.

`work-0522-0505` is `0522.review-construction/05.05.md`. `work-0707-0501` is `0707.app-use-check/05.01.pack.md`. Inspect either with the packet commands. The canonical selection stays `work-0524-0504`.

The catalog names all three ids and is not a selection. No legacy selector file is declared. The worker list is empty. Eight supplied rows quote `0420.prime-desk/06.08.md`.

## Limits

`0124.prime-desk/05.04.return.md` and `0122.review-construction/05.05.return.md` are not declared. Custody stays unknown. Do not create those files from this guide.

`labs/prime-desk-use-pass01/request.json` is the previous cut. The live assignment has since changed. Leave that file in place. A new request is a new `--out`. Pass `--accept` only when Prime deliberately accepts a revision.

This request does not bind `0524.prime-desk/05.05.md` or `artifact-manifest.json`.

Prime's handoff is `00.kernel/00.00.10.work/0524.prime-desk/evidence/build05.05/PRIME-USE.md`.
