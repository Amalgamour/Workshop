# prime-desk-use-pass01

Operator guide for one pinned request against the live book. The desk code is `labs/prime-desk-pass03`. This directory does not contain a second selector.

## Request

`D:\Git\lib-build\labs\prime-desk-use-pass01\request.json`

Source list: `source-list.json` in this directory. Catalog copy: `catalog.json` in this directory. The request binds the book catalog `00.kernel/00.00.10.work/0524.prime-desk/evidence/build05.04/catalog.json`. Those two catalog files are the same bytes.

Run from `D:\Git\lib-build` with `PYTHONDONTWRITEBYTECODE=1`.

```text
python -B labs/prime-desk-pass03/prime_desk.py view --request D:\Git\lib-build\labs\prime-desk-use-pass01\request.json
python -B labs/prime-desk-pass03/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass01\request.json --work-id work-0524-0503
python -B labs/prime-desk-pass03/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass01\request.json --work-id work-0522-0505
```

Exit 0 means the tool found nothing it classifies as attention. Exit 1 means attention. Exit 1 is not a failed command and it is not approval. Exit 2 is a refusal. The builder demonstration exited 1 on each of these three commands. The captured outputs are under `00.kernel/00.00.10.work/0524.prime-desk/evidence/build05.04/run/`.

## What the request registers

Current work comes from `0401.goal/06.01.md`, the assignment path named by `app/development-workspace.json`. That record names `0524.prime-desk/05.03.md`, state `returned`. The registered id is `work-0524-0503`.

`work-0522-0505` is the second registered page, `0522.review-construction/05.05.md`. Inspect it with the third command. The canonical selection stays `work-0524-0503`.

The catalog names both ids and is not a selection. No legacy selector file is declared.

## Limits

Return paths `0124.prime-desk/05.03.return.md` and `0122.review-construction/05.05.return.md` are not declared. Custody stays unknown. Do not create those files from this guide.

No verification file is bound to the canonical work. The verification gap stays visible.

`request_index.py` refuses to overwrite an existing `--out`. A byte change in a declared file needs a new absolute output path. Pass `--accept` only when Prime deliberately accepts that revision. This request does not bind `0524.prime-desk/05.04.md` or `artifact-manifest.json`.

Prime's handoff is `00.kernel/00.00.10.work/0524.prime-desk/evidence/build05.04/PRIME-USE.md`.
