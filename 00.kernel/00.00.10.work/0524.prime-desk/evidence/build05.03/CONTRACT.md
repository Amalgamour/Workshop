# Contract — prime desk route repair 05.03

Schema: prime-desk-contract/0503
Batch: 0524.prime-desk/05.03
Date: 2026-11-01
Executor: Grok-1

This contract was written before labs/prime-desk-pass03. It repairs routing in the read-only desk view. It does not replace the 05.02 selection, hash, or attribution contract. labs/prime-desk-pass01 and labs/prime-desk-pass02 stay in place.

The band rule follows the existing placement clarification in 0417.return-placement/06.01.md and the page digits used by the desk identity function: the second digit is the band, the first digit is a preserved prefix, and NN is the last two digits. This lab does not import or edit that app module.

## What stays

Request schema remains `prime-desk-request/2`. Coverage remains `declared-paths`. Current work still comes only from the assignment-record v1 named by the workspace file and parsed with pinned `app/context.parse_assignment`. `validate_context` is not called. A legacy selector is a hint. A catalog does not select. Director and model text remain explicit byte spans. View and packet command names stay. The tool writes no source, no destination, no receipt, and no status transition.

## Output versions

View schema `prime-desk-view/3`. Packet schema `prime-desk-packet/3`.

`selected.review_home` is removed. `selected.route` replaces it. Pass02's N1NN path without a `.return.md` tail is not emitted as a review destination.

## Identities

A page path is `NNNN.subject/face.md`. Subject is lowercase digits and words separated by `.` or `-`. Pass digits are 01 through 99. Any other shape is unsupported. The tool does not invent an alias.

The band is `NNNN`'s second digit. The prefix is its first digit. These digits are the declared identity. The tool does not accept a page only when the whole number sits in 0500-0599 or 0700-0799.

| Face | Band digit | Kind | Executable source |
| --- | --- | --- | --- |
| `05.PP.md` | 5 | work | yes |
| `05.PP.pack.md` | 7 | pack | yes |
| `05.PP.return.md` | any | return | no |
| `06.PP.review.md` | any | review | no |
| `05.PP.md` | 1 | return-line | no |
| any other combination | any | unsupported | no |

Executable sources:

- N5NN work. Return path is `{prefix}1{NN}.subject/05.PP.return.md`. Review path is the source page itself. The review section of that page is not parsed.
- N7NN pack. Return path is the same page `05.PP.return.md`. Review path is the same page `06.PP.review.md`. No N1NN path is allocated.

A return artifact or a review artifact used as `current_work` is a refusal. Selected stays null. The kind is named. No source page is inferred from that artifact.

Band 1 with a work face is a return line, not a source. No page is allocated. Any other band stops. No N1NN route is invented for it.

## Evidence states

Each of source, return, and review has its own file state: `matched`, `missing`, `stale`, `changed`, or `undeclared`.

`undeclared` means the derived path was not in the request. The tool does not search the book and does not create the file. Undeclared is not a finding that the review text is absent.

`missing` means the request named the path and the file was not there. For the return line, custody is `pending` and no receipt is fabricated. That pending return does not change the review file state.

A matched return file proves those bytes only. Custody stays `unknown`. Judgment stays `unknown`. The tool does not decide acceptance.

The required route examples are:

| Source | Return | Review |
| --- | --- | --- |
| 0521.return-placement/05.03.md | 0121.return-placement/05.03.return.md | 0521.return-placement/05.03.md |
| 1599.synth-lab/05.01.md | 1199.synth-lab/05.01.return.md | 1599.synth-lab/05.01.md |
| 0705.prime-desk-check/05.01.pack.md | 0705.prime-desk-check/05.01.return.md | 0705.prime-desk-check/06.01.review.md |
| 1705.prime-desk-check/05.01.pack.md | 1705.prime-desk-check/05.01.return.md | 1705.prime-desk-check/06.01.review.md |

An address that differs in subject or pass does not select that row. A foreign prefix is a refusal. `05.00` is unsupported.

## Packets

`packet --work-id` of the canonical id expands that work's bound task material.

`packet --work-id` of another registered executable source expands an inspection packet. `selected` remains the canonical assignment. The packet names `relation: inspection` and the canonical id. Inspection adds a gap, so the exit is not 0. Inspection does not change selection.

A packet id that is a return, a review, or an unknown kind is not expanded. The kind is visible. Selection stays canonical.

Two different source pages keep their own criteria, returns, findings, and next routes.

## Limits

Exit 0 is not acceptance. Exit 2 still refuses a mechanically unusable request, instance, coverage token, or current-work identity, and it does not fill the hole from a catalog or a newer filename.

Pass02 files and tests are not rewritten. The 0705 checker is not edited. No live book layout change, no renumbering, and no migration.
