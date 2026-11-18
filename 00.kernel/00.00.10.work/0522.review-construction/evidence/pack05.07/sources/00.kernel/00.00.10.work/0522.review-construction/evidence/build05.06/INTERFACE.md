# Interface delta - constructor pass03

date: 2026-11-01
who: Grok-2
state: describes the built constructor; not acceptance

Predecessor `labs/review-construction-pass02/construct.py` stays `b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc`, 36188 bytes. Successor `labs/review-construction-pass03/construct.py` is `6eec5653c6818cfdeb98ffcd929cdf26f0ddf15c3121c703ce795abea6eb755d`, 42216 bytes.

## Schemas

`review-construction/1` keeps the pass02 keys. `review-construction/2` adds `supplied_review_state`. That object is `supplied-review-state/1` with exact keys `schema`, `source`, `disposition`, `pass_terminal`, `goal_terminal`, and `outcome`. `source` is the label `cycle decision judgment`. Enums are the cycle's value sets. Couplings stay the cycle's.

`review-target-inspection/1` is the inspect result: `schema`, `state`, `rule`, `target_sha256`, `target_bytes`, `section_sha256`, `binding_sha256`. `state` is `absent`, `unsupported`, `pending`, `constructed-same-binding`, or `existing-review`.

`review-construction-result/1`, `review-task-binding/2`, and `review-construction-show/1` stay the pass02 result schemas.

## Commands

`preview`, `apply`, `bind`, and `show` keep their pass02 arguments. New command:

```text
construct.py inspect --fixture-root ABS --target REL [--binding HEX64]
```

`/1` section text matches pass02, including `none supplied` for both null and `[]`. `/2` renders the supplied disposition, pass terminal, and goal terminal, and renders `[]` as `none recorded`. A `/2` recorded decision keeps its text and adds `(source sha256 <hex>)`. Outcome stays on the judgment line.

`bind` still hashes measured file bytes and the canonical agreement. Schema version and `supplied_review_state` are not binding inputs. A changed source file changes the binding.

Inspect writes nothing. `constructed-same-binding` does not authorize a later apply. `ROOT` stays `D:\Git\lib-build`.
