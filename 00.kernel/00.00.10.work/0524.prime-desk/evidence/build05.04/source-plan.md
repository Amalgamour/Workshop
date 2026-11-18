# Source and coverage plan — 0524.prime-desk/05.04

Schema: prime-desk-source-plan/0504
Date: 2026-11-01
Executor: Grok-1

This plan is the source list for one read-only request. It was written before that request was assembled. It does not choose current work. The assignment record does.

## Instance

- Book root: `D:\Git\lib-build\00.kernel\00.00.10.work`
- Book name: `00.00.10.work`
- Role: `prime`
- Tools root: `D:\Git\lib-build`
- Workspace file: `app/development-workspace.json`
- Assignment path inside the book: `0401.goal/06.01.md`
- Coverage token: `declared-paths`

The workspace file names the assignment path. The request may hash both files. It may not replace either path. No repository walk is used to find further sources.

## Current work

Read from the live assignment, not from a filename sort:

- `current_work`: `00.kernel/00.00.10.work/0524.prime-desk/05.03.md`
- `assignment_state`: `returned`
- Registered id: `work-0524-0503`
- Address: `0524.prime-desk/05.03`

The second registered page is the reviewed `0522.review-construction/05.05.md`, id `work-0522-0505`, address `0522.review-construction/05.05`. It is available for inspection. It is not the canonical selection.

No legacy selector file is declared. A disposable selector is not written onto the live record.

## Declared book sources

| Path | Role | Binding |
| --- | --- | --- |
| `0401.goal/01.md` | goal | desk |
| `0408.seats/01.md` | scope | desk |
| `0420.prime-desk/01.md` | scope | desk |
| `0420.prime-desk/06.01.md` | authority | desk |
| `0412.prime-review/06.02.md` | dependency | desk |
| `0420.prime-desk/evidence/selection-update-2026-11-01/prior-current-assignment.md` | dependency | desk |
| `0420.prime-desk/06.07.md` | checkpoint | `work-0524-0503` |
| `0524.prime-desk/05.03.md` | criteria | `work-0524-0503` |
| `0522.review-construction/05.05.md` | criteria | `work-0522-0505` |
| `0524.prime-desk/evidence/prime-review05.03/REVIEW.md` | finding | `work-0524-0503` |
| `0522.review-construction/evidence/prime-review05.05/REVIEW.md` | finding | `work-0522-0505` |

`0420.prime-desk/06.01.md` also supplies the Director span bytes 111:403 and the model span bytes 430:834. Those spans stay separate.

The catalog is an index of the two work ids. Its provenance text says it is not a selection. The file the request binds is `0524.prime-desk/evidence/build05.04/catalog.json`. The same bytes are stored at `labs/prime-desk-use-pass01/catalog.json`.

## Tools pinned, not launched

- `labs/prime-desk-pass03/prime_desk.py`
- `labs/prime-desk-pass03/request_index.py`

`past_tests` and `activation` stay `unknown` on those operation rows. This request does not rerun the pass03 suite.

## Supplied context

Two supplied sentences are copied from `0420.prime-desk/06.07.md`: the prepared lanes `0524/05.04`, `0525/05.01`, and `0707/05.01.pack`, and the Prima remote-claim limit. No worker row is declared. A claim, an outgoing prompt, and a timestamp are not process activity.

## Omissions

These are outside this request. Their absence here is not a finding that they do not exist.

- `0524.prime-desk/05.04.md`, this pass's notes, and `artifact-manifest.json`. Binding them would make a circular hash. Primary work stays `05.03`.
- `0124.prime-desk/05.03.return.md` and `0122.review-construction/05.05.return.md`. Both are absent on disk. They are not declared and they are not created. Route custody for each stays `unknown`.
- No verification file, receipt, history body, attention hold, or legacy selector is declared.
- Pass03 tests, the pass03 demo, `app/README.md`, and `app/librarian.py` are not request inputs.
- No whole-repository scan.

## Assembly and checks

1. Write the catalog, then `labs/prime-desk-use-pass01/source-list.json` with hashes of the files above.
2. Run `labs/prime-desk-pass03/request_index.py` to `labs/prime-desk-use-pass01/request.json`. A mismatch writes nothing and is a revision record. `--accept` is not used.
3. Fingerprint the declared sources, run view, packet for `work-0524-0503`, and packet for `work-0522-0505`, then fingerprint again.
4. Run view once more in a new process and compare the selected id, the fingerprint, and the declared attention list.
5. For stale behavior, copy `05.03` into a disposable book under this evidence directory, pin a separate request, change only that copy, and run view. The live page is not edited.

Exit 1 on the real book is attention. It is not approval and it is not a failed command. Judgment stays unknown.
