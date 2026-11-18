# Contract — desk overview and declared profile 05.05

Schema: prime-desk-contract/0505
Batch: 0524.prime-desk/05.05
Date: 2026-11-01
Executor: Grok-1

This contract was written before labs/prime-desk-pass04. It adds a readable supplied-context block and a fuller declared profile. It does not replace the 05.03 routing contract or the 05.04 request. labs/prime-desk-pass03 and labs/prime-desk-use-pass01 stay in place, including when the live assignment makes the old request stale.

## What stays

Request schema remains `prime-desk-request/2`. Coverage remains `declared-paths`. Current work still comes only from the assignment-record v1 named by the workspace file and parsed with pinned `app/context.parse_assignment`. `validate_context` is not called. A legacy selector is a hint. A catalog does not select. Director and model text remain explicit byte spans. View and packet command names stay. The tool writes no source, no destination, no receipt, and no status transition.

N5NN and N7NN routes stay as in the 05.03 contract. Inspection still does not change the canonical id. A stale declared file is withheld. Exit 0 is not acceptance. Exit 1 is attention.

## Output versions

View schema `prime-desk-view/4`. Packet schema `prime-desk-packet/4`.

The JSON field `record.supplied_without_worker` keeps its name. Markdown now prints those rows. Pass03 remains `prime-desk-view/3` and `prime-desk-packet/3`.

## Supplied context

Section 4 keeps the worker list. An empty list still says that no worker is declared and that process activity is unknown.

A following block is titled `Supplied context`. It prints each `supplied_without_worker` row with its id, speaker, text, and limit. The block says a row there is not a declared worker, not a running process, and not a verified return. A supplied sentence is not copied into the worker list.

## Review-loop row

If the request declares an operation whose name is `review-loop`, the view shows that declared row and does not add the synthetic pending row. `executed` stays false. `activation` stays the declared token. A pin mismatch stays a stale or missing source on that row.

If no such operation is declared, the synthetic row remains: name `review-loop`, limitation `Pending. Successor modules were not imported.`, source none. The omission stays visible.

## Brief

The markdown starts with `## Brief` after the book header. The brief names the selected id and address, review file state, return custody, verified-result basis, next-reference path, open attention count, gap kinds, supplied-context count, and worker count. It states that process activity is unknown and that the brief grants nothing.

The numbered sections remain. Gaps are still listed in full. Source identities remain in those sections and in the packet. The brief is not a score. The pass03 fixture ceiling of 80 lines is remeasured after this block exists. A larger full markdown is recorded. It is not trimmed by hiding a hold.

## Profile

The new profile is labs/prime-desk-use-pass02. It is built after this contract. It binds the live assignment's current page `0524.prime-desk/05.04.md`, reviewed `0522.review-construction/05.05.md`, and `0707.app-use-check/05.01.pack.md`. It binds Prime's 05.04 review as the canonical verification and finding, `0420.prime-desk/06.08.md` as the checkpoint and the next reference, and the 0707 return and review pages that are already in the source cut. Workers stay an empty list. Supplied rows quote 06.08. They use an empty `about` field.

The profile does not bind `0524.prime-desk/05.05.md` or `evidence/build05.05/artifact-manifest.json`.

## Tests before the real book

The new lab tests these cases on disposable books: supplied context with no workers; a matched verification and a matched next reference; a missing verification file; a stale verification file withheld; an N7NN pack whose return and review match; inspection leaving the canonical id unchanged; a declared review-loop pin replacing the pending row; an undeclared review-loop row staying pending. The pass03 suite is not the suite for this pass. The pass04 suite is.
