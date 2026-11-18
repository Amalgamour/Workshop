# Prime use — fuller real-book profile

This file is the handoff for Codex Prime. The builder demonstration is not adoption. Prime uses the request, reads the brief and the drill-down, and records whether the added context reduces reconstruction.

## Request

Absolute path:

`D:\Git\lib-build\labs\prime-desk-use-pass02\request.json`

sha256 `9b8a96ba5b576e8354b38b9a5ab2a6725b06e90bedcf47883f823b6a7e4545ca`, 16032 bytes.

Run from `D:\Git\lib-build` with `PYTHONDONTWRITEBYTECODE=1`. The builder used Python 3.14.0 at `C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe`.

```text
python -B labs/prime-desk-pass04/prime_desk.py view --request D:\Git\lib-build\labs\prime-desk-use-pass02\request.json
python -B labs/prime-desk-pass04/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass02\request.json --work-id work-0524-0504
python -B labs/prime-desk-pass04/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass02\request.json --work-id work-0522-0505
python -B labs/prime-desk-pass04/prime_desk.py packet --request D:\Git\lib-build\labs\prime-desk-use-pass02\request.json --work-id work-0707-0501
```

Add `--json` for the machine view. Builder stdout is in `evidence/build05.05/run/`. Commands and exits are in `evidence/build05.05/commands.txt`.

## How to inspect one work item

The second command expands the canonical packet. On the builder run the relation was `current` and the work id was `work-0524-0504`.

The third command inspects `0522.review-construction/05.05`. The fourth inspects `0707.app-use-check/05.01.pack`. On both, the selected id stayed `work-0524-0504` and the relation was `inspection`.

The 0707 packet is band `N7NN`. Return path `0707.app-use-check/05.01.return.md`, file matched, custody unknown. Review path `0707.app-use-check/06.01.review.md`, file matched, judgment unknown. A matched return hash is not a receipt.

## Declared coverage

Declared paths only. The builder view matched 30 of 30. Unregistered sources were not searched.

Registered work:

- `work-0524-0504` at `0524.prime-desk/05.04`, selected from `0401.goal/06.01.md`
- `work-0522-0505` at `0522.review-construction/05.05`
- `work-0707-0501` at `0707.app-use-check/05.01.pack`

Canonical verification is `0524.prime-desk/evidence/prime-review05.04/REVIEW.md`, basis observed. The tool's limit is that the hash proves those bytes, not acceptance. Next reference and checkpoint are both `0420.prime-desk/06.08.md`. The catalog names three ids and `used_for_selection` is false.

Workers declared: 0. Eight supplied rows quote `0420.prime-desk/06.08.md` and appear under `### Supplied context` with speaker and limit. They are not worker rows.

The review-loop row is `labs/review-loop-pass02/review_loop.py`, matched, executed false, activation unknown. The same section pins `app/review_loop_tools_v2.py`, `app/review-loop-v2.json`, and `app/librarian.py` as read-only pins. This request does not register or launch them.

Fingerprint on the builder view: `46054c0d470d55318b5d835e425e9eb9ee0a8c7209bf42efbf47d06647f9b802`. A second process recovered the same selected id, fingerprint, and gap kinds. `observed_at` changed.

## Length

The opening through `## Brief` is 18 lines and 100 words. That is the short entry. The full markdown view is 102 lines and 1186 words. It is longer than a 30-60 second read. The extra length is the declared identities, the supplied rows, and the operation pins. Gaps stay listed in full. These counts are observations, not a readability score.

## Limitations

Open attention is 0. Gaps are `return-undeclared` for `0124.prime-desk/05.04.return.md`, and `catalog-not-chosen` for the other two ids. Custody of that return stays unknown. Judgment stays unknown.

`0522.review-construction/05.05` has no separate verification or finding file in this source cut. Its packet leaves those slots empty. The page itself is the review identity and is matched. Its return `0122.review-construction/05.05.return.md` is undeclared.

`0707.app-use-check/05.01.pack.md` and the prior assignment under `0420.prime-desk/evidence/selection-update-2026-11-01-02/` are named by this batch and hashed live. They are not rows in `pack05.05/source-manifest.json`. The return and review pages for 0707 are snapshot rows.

The previous request `labs/prime-desk-use-pass01/request.json` still hashes the older assignment. A pass04 view of it exited 1, state `partial`, selected null, gap `stale`. That file was not rewritten. Its earlier text is not the current assignment.

`00.kernel/00.live.md` was hashed and not edited. It is not a declared path. Process activity stays unknown. `assignment_state` `returned` is a record field. `validate_context` was not called.

Pass03 `prime_desk.py` stayed sha256 `cd1e74aa0a51b52dcedaa544b4fd1f2de90f84bf69a8c21234ef362ae2a5f812`, 77622 bytes.

## Manual steps that remain

1. Run the four commands above, or read the captured stdout and rerun any command you want to witness.
2. Read `## Brief`, then the supplied-context block, and record whether that reduces the reconstruction you still do by hand.
3. Leave custody unknown until a later request declares a real return file.
4. Leave the Review section of `05.05.md` for Codex Prime.

## When a new request is necessary

Write a new request when a declared file's bytes change, when coverage must add a path, or when Prime deliberately accepts a revision. `request_index.py` will not overwrite this `--out`. A mismatch without `--accept` writes nothing and prints `revision`.

Do not put `0524.prime-desk/05.05.md` or `evidence/build05.05/artifact-manifest.json` into that request. Primary work stays `0524.prime-desk/05.04`.

This request does not seat `00.live`, file 0124 custody, or activate the desk.
