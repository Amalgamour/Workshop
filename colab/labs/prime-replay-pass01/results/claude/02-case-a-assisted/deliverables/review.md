# Review — case A (0513.bench-build 05.01, member 0163), ASSISTED condition

Reviewer: claude-opus-5-5, Colab run 02-case-a-assisted. A lab output, not a live review.

**Disclosure.**
- I am the original Builder of case A, so this is self-review.
- I am also the builder of the frozen prime_cycle adapter used here.
- **Carryover:** run 01 (A manual) came immediately before. Its findings were in my context, and I did not re-derive them independently. Agreement with run 01 is not independent confirmation.

## Did, Blocked, Need
**Did** (assisted steps, all journalled under out/journal):
- `read --templates`;
- `read --json`;
- `packet` (review_packet assemble);
- filled my own judgment into the template;
- `record`;
- `inspect`;
- a re-read;
- `day --registration`.

I also ran the pinned reader directly to diagnose its failure.

**Blocked: the assistance could not observe the page.**
- `batch_observe.py` exits 2 with `missing clerk_adapter.py`.
- The frozen bundle lacks `labs/prime-support-pass01/clerk_adapter.py`, which batch_observe pins as its sibling (`ADAPTER_PATH`, line 66).
- So read shows `observation-failed`, and the template binding has no receipt.
- `record` refused: `observation failed: reader exit 2`. **No typed review was recorded.**
- I did not repair the bundle (contract step 5).

**Need:**
- For the lab: a bundle with its full pinned dependency closure.
- For case A: the same bounded correction pack as run 01.

## What the tools contributed
- **Custody, verified by the reviewed modules,** through the packet's inspector and helper verify:
  - status `complete`;
  - receipt `7efb07af…`, manifest `39d9404e…`, 6 payloads, submission `claude-0513-0501`, origin 0513.bench-build/05.01, not retrospective.
  These equal my manual hashes from run 01. Here they come from the reviewed inspector, not from my script.
- **Packet coverage: only `return` (builder-claim) and `receipt` (custody).** For a live-file registration the adapter adds no page source. The CONTRACT, code, keys and method context are not in the packet. Every substantive finding below came from direct reads, carried over from run 01.
- **Journal and day view:** they gave an exact account of the attempts (read ×3, packet, refused record, inspect) and correctly reported no review and nothing finished or completed.

## Verified versus claimed
These are the same as run 01. The custody rows are now also tool-verified. The test and mutation claims are still not reproduced: the dependency is absent in the frozen subject repository. I did not re-run `validate` or the tests in this run, so those results are carried from run 01 and are not repeated evidence.

## Assessment, defects and unknowns (case A)
These are the same as run 01:
- **F01:** partly met; no pair parity check.
- **F02:** contradicted; `must_quote` wording keys and no commitment scoring.
- **F03:** partly met; no candidate re-hash after prepare (`prime_bench.py` 785-860, 1088-1160).
- **F04:** partly met; no preparation and repair cost record.
- **F05:** respected.

No new case A defect came from the tools.

## Disposition
- **Pass:** finished, accepted as a bounded first instrument.
- **Goal:** open.
- **Correction required** before any live trial. Prime decides it within the design; the Director is not needed now.

The typed record of this judgment could not be written: the tool refused. The judgment exists as `out/decision-case-a.json` and this file.

## Preservation
Nothing in the subject repository changed. inspect shows no review directories, so no partial review was left.

## One bounded next action
The same as run 01: one implementation correction pack for F01–F04 (next-pack.md).

## Factfind (assistance, as observed in use)
1. **Bundle closure.** batch_observe needs `labs/prime-support-pass01/clerk_adapter.py`, which is absent from `assistance/`. This is a lab preparation omission; the reader's pin is right to refuse.
2. **A hidden reason.** prime_cycle `read` reports `observation-failed: reader exit 2`, but the view omits the reader's stderr. `observe()` keeps it in `rec["stderr"]`, but `derive()` copies only exit, stdout sha and failed. I had to run the reader by hand to learn why. *(The adapter is my own code.)*
3. **A misleading state.** When observation fails, `pass_state` is `no-return`, which asserts there is no return. The packet shows that a verified return exists. The correct state is unknown or observation-failed. *(My code.)*
4. **Packet coverage** is the return and receipt only, by default, for live-file. That matches the contract warning; it is not a defect, but it means the "assisted" view held no review content.

## Hostile
Following the tool's view literally ("no-return") would conclude there is nothing to review. That is the face I was tempted to obey, and it is wrong.

## Overflow
I did not use `prime_review report` directly on a hand-built prime-review-record. It would have needed hand-copying the receipt and binding fields, which defeats the purpose of the assistance. Noted as an untried route.

## Unprompted
The assisted route cost more commands than manual for this case, with no added review substance: 10 wrapped commands, including 2 diagnostic ones. The only gain was independent custody verification by reviewed code.
