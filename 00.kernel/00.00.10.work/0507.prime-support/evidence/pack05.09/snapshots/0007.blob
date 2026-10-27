# CONTRACT — repair05.08 (0507.prime-support 05.08), additive to build05.07/CONTRACT.md

Author: claude-opus-5-5. Date: 2026-10-27.
Everything in build05.07/CONTRACT.md stands unless this file changes it. The tool pins, packet, scope, outcome rules and `authority: none` are unchanged.

## 1. Exit semantics, all commands

| exit | meaning |
|---|---|
| 0 | the stage is complete and positive: `prepared`, checks `ok`, outcome `oriented`, or `show` |
| 1 | the stage is complete and negative: prepare `partial`, checks `failed`, outcome `partial` or `not-oriented` |
| 2 | refused: nothing new was recorded. This covers a conflict, a precondition not met, a records store that can't be used, and a prepare stage failure (as in 05.07) |
| 3 | incomplete: an identical replay found the raw input but no readable terminal record. Nothing was written. Start a new attempt that links this one |

## 2. Shape validation (PB-06)

Supplied JSON is checked for type before any iteration, membership test, sort or dereference. A wrong-shaped value fails in a controlled way. It is never a traceback. The raw bytes are always kept.

**Answers.**
- Top level: `{schema, attempt_id, answers}`, with `answers` an object holding exactly O1..O6.
- Each item is checked for shape first:
  - `text` must be a string;
  - `citations` must be a list of strings;
  - O1 `target` must be a string;
  - O1 `conflicts_seen` must be a list of integers, not booleans;
  - O2 `fields` must be an object with exactly release, claim, execution and review, each `{value: str, citation: str}`;
  - O5 must be `{none_found: true, text}` or `{citations, text}`.
- A shape failure records `fail` for that item, and its semantic checks are skipped.
- An envelope failure writes 22 `status: failed`, with a reason, and no 21.

**Judgement.**
- The fields are `schema, attempt_id, reviewer (label), grades (O1..O6 → "pass" | "gap" | "wrong"), reasons (O1..O6 → str), remediation [{kind: "reference" | "question", detail: str}]`.
- Invalid JSON or any wrong shape writes:
  - `31.judgement.json`: `{status: failed, reason}`;
  - `39.outcome.json`: `{outcome: not-oriented, judgement: invalid, reason, authority}`.
- Exit 1. No grade from an invalid judgement is used.

**Inspected registry and tool reports.**
- The registry must be an object. If `lanes` is present, it must be a list of objects, and each `clerk_jobs` must be absent or a list. A non-empty `clerk_jobs` is still `unsupported`.
- The status report must be an object, with:
  - `lanes`: a list of objects, each with `files` a list of objects whose `path` is a string;
  - `conflicts`: a list of strings;
  - `attention`: a list.
- The check_book report must be an object, with `findings` a list of objects.
- Any other shape fails the stage with `StageFailure: … shape …`.

**Errors that are not caught.** Only `StageFailure` and the existing I/O and subprocess errors become records. A real code defect still raises, and is not dressed up as a recorded result.

## 3. Stage-aware replay (PB-07)

Terminal records: check → `22.checks.json`; judge → `39.outcome.json`.

`check`, when `20.answers.raw` exists:
- **Different bytes:** exit 2 `conflict`.
- **Identical bytes, 22 readable:** `already-recorded: checks <status>`. Exit 0 if ok, 1 if failed.
- **Identical bytes, 22 missing or unreadable:** exit 3 `incomplete: answers recorded without a check result; replay does not complete a stage; start a new linked attempt`.

`judge`:
- It needs a readable 22. If 20 exists without 22, it refuses with exit 2 `check stage incomplete`.
- When 30 exists, replay follows the same pattern against 39:
  - `already-recorded: outcome <x>`, exit 0 if oriented, otherwise 1;
  - exit 3 incomplete when 39 is missing or unreadable.

Replay writes nothing, and it never repairs, overwrites or completes a stage.

## 4. show states

These are evaluated in order. The first match wins.

| state | when |
|---|---|
| `interrupted after <file>; not oriented` | no 19 |
| `failed at <stage>; not oriented` | 19 failed |
| `<outcome>` (plus `; judgement invalid` when 31 failed) | 39 readable |
| `<prep>; judgement incomplete (raw judgement without an outcome); not oriented; start a new linked attempt` | 30 without a readable 39 |
| `<prep>; checks <status>; awaiting judgement; not oriented` | a readable 22 |
| `<prep>; check incomplete (raw answers without a check result); not oriented; start a new linked attempt` | 20 without a readable 22 |
| `<prep>; awaiting answers; not oriented` | otherwise |

`show --json` adds a `stage` key: interrupted, prepare-failed, awaiting-answers, check-incomplete, checked, judgement-incomplete or outcome. It also adds `complete: bool`.

Only 39 yields an outcome. The presence of a raw file never does.
