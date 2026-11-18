# Prime first-use checklist — review-loop app entry

Date: 2026-11-01. This checklist is for Codex Prime. It is not a live review, not acceptance, and not seating.

The material is a read-only copy of live member `0182.desk-app-integration-design-0501`. Origin stays book `00.00.10.work`, page `0519.desk-app`, batch `05.01`. Submission stays `claude-0519-0501`. The intended matching line is `0119.desk-app`. Actual custody of the copy stays the member directory, format `legacy-in-place/1`, placement pending. The live page `0519.desk-app/05.01.md` already holds a substantive Prime review. Do not overwrite it. There is no successor renderer.

Custody records for this member do not name the review task. Task association stays `not-established`. That limit does not by itself block a supplied review of the declared copy. `accepted` stays false. `custody` stays `not-established`. `filing_claimed` stays false. `full_success` is mechanical.

## Declared example

- `example-request.json` — schema `review-loop-request/1`
- `example-registration.json` — schema `prime-cycle-registration/2`, work `pilot-0182`, task `pilot-0182-task`, evidence label `supplied`, receipt label `supplied`, review `r1` at `cycle`
- `supplied-judgment.json` — labeled `SUPPLIED` words. Not Prime's judgment and not an assessment of the 0519 design.
- `real-decision-template.json` — unfilled. Not a runnable decision. Prime fills `attribution`, `judgment`, and `supplied_record` on the prepare template.

The runnable decision is built only at pilot time: the prepare template, plus these supplied words, plus the receipt and return hashes of the copy.

## One command

From `D:\Git\lib-build`, pick a new directory that does not exist:

```text
python -B labs/prime-entry-pilot-pass01/pilot.py --destination D:\Git\lib-build\00.kernel\00.00.10.work\0522.review-construction\evidence\build05.05\pilot-demo
```

The destination must be a new directory under `evidence/build05.05`. An existing destination is refused and is not replaced. The working books stay in the temp directory, outside `D:\Git\lib-build`. The command deletes those books when it finishes. It reads the live member and the live page. It does not write them.

## What the command does

1. Fingerprint `0182.desk-app-integration-design-0501` and `0519.desk-app/05.01.md`. Confirm `return-line-layout.json` is absent on the live book.
2. Copy the member into a disposable book. Write a new PENDING page at `0519.desk-app/05.01.md` in that book.
3. `python -B app/librarian.py review-loop describe-legacy --book <disposable> --member 0182.desk-app-integration-design-0501`
4. Save that descriptor unchanged.
5. `prepare --fixture-root <disposable> --request request.json`
6. Overlay `supplied-judgment.json` onto the prepare template. The capture identity member is the derived line `0119.desk-app`.
7. `record --fixture-root <disposable> --request request.json --decision decision.json`
8. `render --fixture-root <disposable> --request request.json`
9. `read --fixture-root <disposable> --request request.json` in a new process.
10. On a second disposable book, use the live page bytes as the review target. `render` returns `render-conflict`, exit 2, and does not overwrite that page. One partial stays under that disposable book. The book is then deleted. The live page is not the render target.

## After the command

- `summary.json` has `accepted` false, `custody` `not-established`, `filing_claimed` false, `task_association` `not-established`, and `live_review_completed` false.
- `prepare-template.json` is the unfilled prepare template. Fill that object for a real judgment. Do not treat `decision.json` as Prime's judgment.
- `sample-review.md` is the disposable PENDING page after the supplied render. `conflict-page.md` is the untouched copy of the substantive page.
- Compare `fingerprints.json` before and after. The live member and the live page should match. No live layout file should appear.

Changing the declared task, evidence, or agreement after record makes the `/3` review stale and leaves the record bytes.
