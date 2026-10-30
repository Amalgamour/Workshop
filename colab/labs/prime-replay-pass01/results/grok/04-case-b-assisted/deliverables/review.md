# Review — case-b assisted — Grok Colab

Model: Grok 4.7, this same session. Condition: assisted, fourth of four.

Carryover: the manual route already accepted this pass, with the goal complete and no pack. That file was not edited from this one. This route's `review_packet.py`, its tests, and `return.md` hash to the same bytes measured on the manual route. The notes name session 01a179d2 as the builder. This session is not that session.

## Did
- One journalled read. Exit 1. The view says pass state no-return, receipt none, and `observation-failed: reader exit 2`. Wrapper stderr was empty. The binding in `out/templates/template-case-b.json` has `receipt_sha256` null and `page_sha256` null. Fingerprint `a61722ef831872713ad2b5cb3c1ada0ff7eda611763eafff3f025ca74d67b9e4`.
- One packet command. Exit 0. Assembly complete. Custody complete. Inspector exit 0. Helper verify exit 0. Receipt in the verify text is `bf8cef9fe88b09316c69d4f1c37d824bc5b7378403d49ac3dccf486905fe0fff`. Return sha256 `b7c4fe25278f7fe09cc7fc18699bf06ab3034bb38abc6787360365e39d488fef`, 2313 bytes. The verify text says result complete, not approved, not accepted, not published. Artifact checks: none. Sources embedded: the return and the receipt.
- Hashed this route's `review_packet.py`, `test_review_packet.py`, and `return.md`. All three match the manual route.
- Wrote `out/decision-case-b.json` with that template binding copied once. Disposition accepted, pass finished, goal completed, outcome complete, semantic conflict false, next action null.
- Record once. `end.json` exit 2. Stdout: `refused: observation failed: reader exit 2`. Inspect shows `reviews: []`. No review directory was written.
- One day. It lists read ok-attention 1, packet ok 1, record refused 1, unique reviews 0. Passing `--registration` makes day call `read()` again inside that process. That call is not a second journalled read. It was not repeated.

## Blocked
- The cycle cannot record the acceptance. The reader exits 2 before the receipt rule is reached. The template receipt stays null. I did not edit the binding and I did not add `clerk_adapter.py`.
- The packet does not inventory the assembler, the tests, or the two specimen directories. Those checks remain the manual route's.

## Need
- No further build. The lab review is this file. The sealed page still says Review PENDING.

## Verified versus claimed
- Verified on this route: custody of member 0167, the return hash, the receipt text, and the three file hashes.
- Verified on the manual route and not repeated here: unittest ran 10, skipped 1, failed 0; the stored 0163 packet has 41 historical-match rows and 28 changed-live-working-copy rows.
- The cycle's no-return line is the failed reader. The return file is present and the packet verified it.

## Defects
None that require a correction of the assembler. The gap on this route is the cycle reader, which is outside the builder's grant.

## Unknowns
Tokens and cost. The reader stderr text is not in this route's wrapper log. Specimen assemble against the live book was not run.

## Disposition
Accepted. Pass finished. Goal complete. Same disposition as the manual route. The tool record was refused and does not change that.

## Pass-finished versus goal-complete
The historical pass delivered the packet. The goal of that packet is met. This replay's cycle record is a separate, unfinished tool step.

## Director needs
No model, no spending, no live-book edit, no release written on the page.

## Preservation
Keep the read exit 1, the record exit 2, the empty review list, and the packet that says custody complete and not accepted. The second reader call is the one inside day, and it stays there.

## One bounded next action
No pack. See `next-pack.md`.

## Factfind
F01. Packet `PACKET.md` embeds two sources and prints `Artifact checks` with no rows.
F02. Record refused with `observation failed: reader exit 2` and wrote no review files.
F03. This route's module hash is `f658cbe48a3a76b908e5af0bcf0b7a68abc90571d983ca785e36667268f6ee72`, 42694 bytes, the same as the manual route.

## Hostile
Using the cycle line no-return as proof that member 0167 is absent would be false. Using assembly complete as acceptance would also be false. The helper text says not accepted, and the reservation says reservation only.

## Overflow
The case-a bench correction is not this page's pack. The missing reader adapter is not a reason to change `review_packet.py`.

## Unprompted
Day and inspect were started together. The day listing does not include the inspect operation. Inspect's own result is `reviews: []`. Day was not run a second time.
