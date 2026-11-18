# Scoring guide — baseline-01

There are two kinds of score.
- **Mechanical** scores come from `tools/check.py` and nothing else.
- **Human** scores come from the Director, blind to the sample date and the run.

The two are recorded separately and never merged into one number. Each mechanical check reports `pass`, `establishes` and `does_not_establish`. The table copies the scope those fields state, and no score may be read more broadly.

## Mechanical scores (per run)
| task | check | what a pass establishes | what it does not establish |
|---|---|---|---|
| T1 | markers-found | both marker lines are present | anything about the copy |
| T1 | bytes-identical | the text between the markers equals the source byte for byte | that the surface and copy path left the bytes alone. A failure may be the transfer path, so the record must name it |
| T1 | nothing-outside-markers | there is no other text in the reply | anything about the copy |
| T2 | json-parses | the reply, or its single json fence, parses | content |
| T2 | exact-keys | every object has exactly the 5 keys | values |
| T2 | same-ids | the id set equals the key: I-109 left out as instructed, none missing | the other fields |
| T2 | ordered-by-id | objects are in id order | anything else |
| T2 | values-equal-key | every field equals the fixed answer key | correctness beyond this note. The preparer wrote the key, and the Director may audit it |
| T3 | one-python-block, nothing-outside-block | the reply has the required form | anything about the code |
| T3 | parses | the code is valid Python | that it runs or is right |
| T3 | others-ast-identical | `parse_line`, `total` and `format_cents` are AST-identical to the original, docstrings included | that `parse_amount` is right; runtime behaviour elsewhere |
| T3 | no-new-top-level | no imports, functions, classes or assignments were added or removed | changes inside function bodies |
| T3 | heldout-tests | the 6 held-out tests pass: 13 new-behaviour inputs, 10 kept-behaviour inputs, plus `parse_line`, `total` and `format_cents` | correctness on any input outside the tests |
| T4 | ids-once-in-order | R01–R11 each appear once, at line start, in order | that any rule says the same thing |
| T4 | backtick-spans-kept | every backticked span of a source rule appears in the same rule | that it is used with the same meaning |
| T4 | numbers-kept | every number of a source rule appears in the same rule | that it still qualifies the same thing |
| T4 | modal-counts-equal | **indicator only**: the same counts of MUST, MUST NOT and MAY per rule | equal obligations. A difference is not an error by itself; it directs the human review |
| T5a | word-count | 350–450 words by the tool's word rule | length as a reader counts it |
| T5a | required-phrases | the three phrases appear verbatim | meaningful use |
| T5a | forbidden-absent | no forbidden word appears as a whole word | quality |
| T5b | word-count, no-long-copying | 300–400 words; no 8-word run copied from the sample | voice |

No mechanical score establishes overall correctness, preservation of meaning, clarity or voice.

## Human scores (per blinded output)
Scored by the Director on the blind copies made by `tools/blind.py`, before the key is opened. Use the scales as written. A note is required whenever a score is not the top value.

**Scale used throughout:** 2 = no issue, 1 = minor issue, 0 = material issue.

| task | dimension | what to judge |
|---|---|---|
| T3 | correctness (H-C) | Read `parse_amount`. Is it right for inputs the tests do not cover, for example `"1,234.5"`, `"-0,123"` or whitespace? Note any case you checked. |
| T3 | clarity (H-L) | Is the change readable, and no larger than the task needs? |
| T4 | omissions (H-O) | Per rule: was any requirement, condition or exception dropped? Count them. |
| T4 | unauthorized changes (H-U) | Per rule: was any requirement added, weakened or strengthened? Count and name them. |
| T4 | meaning, per rule | One of: same, weakened, strengthened, changed, dropped. |
| T4 | clarity (H-L) | Is the revision clearer than the source for a new reader? |
| T5a | clarity (H-L) | Is the scene clear, and does it follow its own logic? |
| T5a | voice (H-V) | Is the voice consistent within the piece? When ranking within a sample, note sameness across runs. |
| T5b | voice (H-V) | Does it read as the author of the sample? 2 = indistinguishable, 1 = close but drifts, 0 = a different voice. |
| T5b | clarity (H-L) | Is the continuation clear, and does it follow on from the passage? |
| T1, T2 | none | These are fully mechanical. The Director may still note anything odd. |

**T4 watch points, for the judge only.** Do not paste these into any prompt; they are easy to lose in a rewrite.
- R03: "an error, not a warning".
- R04: "by the Director only".
- R06: the member "stays `reserved`".
- R08: "a new member number".
- R10: "MUST NOT include file contents".
- R11: "not re-checked".

## Comparing samples
- **Mechanical:** for each check, the pass count out of the runs in each sample, for example 4/5. Show the baseline samples (S0a, S0b) side by side, so the day-to-day spread is visible.
- **Human:** the distribution of scores per dimension per sample, after unblinding.
- **Calling a difference observed:** the later sample falls outside the range of both baseline samples on that measure. An observed difference is described, not explained.

**Attribution rule.** No difference may be attributed to watermarking, or to any other single cause, without supporting evidence: a provider statement for that model and surface, a detection result, or a controlled comparison. Unrelated changes can also produce a difference:
- model version;
- system prompt;
- product features such as memory or styles;
- surface rendering;
- the copy path.
