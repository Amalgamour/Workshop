# CONTRACT - isolated constructor pass03, slice 1a
date: 2026-11-01
who: Grok-2
state: delta written before code; not Prime review and not acceptance

This file is the delta for 0522.review-construction/05.06. It was written before labs/review-construction-pass03. It does not revise the 0707 design contract. It binds only this constructor.

Predecessor: labs/review-construction-pass02/construct.py sha256 b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc, 36188 bytes. That file stays byte-identical. The cycle, loop, door, app, prime_review, and readers stay byte-identical.

## What this slice builds

A new labs/review-construction-pass03/construct.py. It is the pass02 constructor plus four additions:

- schema review-construction/2
- a supplied review-state section on that version
- recorded-decision source-hash text on that version, and null versus [] wording on that version only
- read-only inspect

ROOT remains the literal D:\Git\lib-build. This slice does not make the root module-relative.

## Envelope

review-construction/1 keeps the pass02 key set and the pass02 checks. An unknown key, including supplied_review_state, is still a refusal on /1. A schema other than review-construction/1 on that key set is still `bad schema`.

review-construction/2 uses the /1 keys plus supplied_review_state. That object has exact keys schema, source, disposition, pass_terminal, goal_terminal, outcome.

- schema is supplied-review-state/1
- source is the exact label `cycle decision judgment`
- disposition is accepted, held, or correction-required
- pass_terminal is open or finished
- goal_terminal is open or completed
- outcome is continue, director-input, develop, or complete

The constructor checks those shapes and enums. It does not check the cycle's couplings. held with finished is a constructor-valid shape. `approved` is a bad disposition. The constructor does not infer approval, seating, semantic meaning, or authority. accepted: false, authority: none, custody: not-established, and allocated: false stay on the result object.

## Rendering

For review-construction/1, the review section text is byte-identical to pass02, including `recorded_decisions: none supplied` for both null and []. A recorded decision stays `- <id>: <text>` with no source hash. Bytes outside the review section stay the caller's bytes.

For review-construction/2, the same judgment block is kept, including the outcome line from the prime_review report. Directly after that block the section adds:

```text
### Supplied review state
review_disposition (supplied): <disposition>
pass_terminal (supplied): <pass_terminal>
goal_terminal (supplied): <goal_terminal>
This is the reviewer's supplied state. It is not Director acceptance, approval, seating or authority; see authority: none above.
```

The three values are the supplied object, labelled supplied. Outcome stays on the judgment line. This renderer does not print a second outcome line and does not prove that the supplied outcome equals the report outcome. That comparison belongs to a later loop check against the hash-verified committed record. This standalone renderer does not perform that check.

On /2, recorded_decisions null renders `none supplied`. An empty list renders `none recorded`. A supplied decision renders `- <id>: <text> (source sha256 <hex>)`. The text is the supplied text. The hash is the supplied source_sha256. A missing or non-hex hash is a refusal. The hash is provenance display, not authentication.

## Binding

bind and measure keep the pass02 inputs: measured assignment, evidence, receipt, return, and manifest bytes, plus the canonical agreement. The envelope schema version and supplied_review_state are not binding inputs. Equivalent agreement bytes and equivalent source-file bytes therefore produce the same binding_sha256 on /1 and /2, and the same binding_sha256 as pass02 bind of the /1 envelope. A changed source file or a changed agreement changes the binding. The check is not weakened to force that equality.

The unchanged cycle computes its task binding by calling pass02 bind on a review-construction/1 envelope it builds. This constructor's bind of the caller's envelope is the candidate. The experiment compares those two digests. It does not patch the cycle to make them equal.

## Inspect

```text
construct.py inspect --fixture-root ABS --target REL [--binding HEX64]
```

Exit 0 returns review-target-inspection/1 with keys schema, state, rule, target_sha256, target_bytes, section_sha256, binding_sha256. state is absent, unsupported, pending, constructed-same-binding, or existing-review.

The classification reuses newline_of, locate, and the compose order. Absent means the path is not present. A locate or newline refusal is unsupported and the rule is that refusal text. A stripped section of PENDING or PENDING. is pending. After that, a task_binding line equal to the optional --binding is constructed-same-binding. Every other located section is existing-review.

constructed-same-binding means the binding line matches. It does not mean a different judgment would install idempotently. compose still refuses a non-pending section that is not byte-identical to the new body. Inspect does not authorize a write, does not skip the expected-hash or write-token checks, and does not replace an existing review.

Inspect writes no target, support, partial, or trace file. A symlink, a non-regular file, a path that escapes the fixture root, a fixture root inside D:\Git\lib-build, and a bad --binding are refusals, exit 2. Those protections stay the pass02 protections. Inspect does not read the pinned prime_review file.

## Commands and exits

preview, apply, bind, and show keep their pass02 arguments and result schemas. preview writes nothing. apply writes only inside the disposable fixture root, and only through the existing support, partial, and target rules.

inspect exits 0 for every classified state. Exit 2 is a refusal. A missing pinned prime_review file remains a refusal from the existing pin check on preview and apply, not a new inspect read.

Exit 0 is an answer about the constructor command. It is not Prime review, seating, or app activation.

## Cycle experiment

One record and one read of the unchanged labs/prime-cycle-pass03/prime_cycle.py, in a disposable root outside D:\Git\lib-build, with a review-construction/2 envelope. The envelope's record equals the decision's supplied_record. The envelope's target equals the registration target. supplied_review_state is copied from that decision's judgment. Raw inputs and outputs are hashed and kept. If the cycle refuses the envelope, or the recorded task binding does not equal this constructor's bind of that envelope, the first failure is kept and integration stops. The cycle, loop, door, and pins are not changed.

## Left outside this slice

Loop pass03, the v3 door, librarian.py, README, pilot pass02, F7 mechanical next, portability, and any edit to pass02 evidence. Matching line 0122.review-construction stays pending. This pass does not write a receipt and does not allocate 0184.
