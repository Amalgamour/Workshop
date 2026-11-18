# CONTRACT delta — harness successor (0707/05.22) over the 05.21 contract
from: claude-opus-5-5 · lab: `labs/loop-convergence-harness-pass02` · predecessor: `labs/loop-convergence-harness-pass01` (frozen, unchanged)

The 05.21 contract (`evidence/design05.21/CONTRACT.md`) still holds. Only the changes are listed here.

## Readiness (H2, H4)
- **READY** means all of the following:
  - the scope is **full**;
  - every id in the **immutable full required baseline** (the registry's 37 required cases, independent of `--suite`) has exactly one well-formed record with verdict `pass`;
  - nothing crashed;
  - every dependency row is well-formed and `accepted`.
- **Collections are type-checked.** None, a dict, a string or an empty list in place of a list is a reason (verdict) or a refusal (inputs). It is never "zero items".
- **`--suite G1,G2` is a diagnostic subset.**
  - It reports `aggregate.scope = subset`, the selected ids, `subset.all_selected_required_pass`, and `coverage_missing` (every required id not run).
  - It is never READY.
  - Its exit is **4** when every selected required case passed and nothing else is wrong except coverage, and **1** otherwise.
  - An unknown group name is refused (exit 2).
- **Exits:**

| Exit | Meaning |
|---|---|
| 0 | READY, full scope |
| 1 | NOT READY |
| 2 | refused before execution |
| 3 | harness crash |
| 4 | subset passed; full coverage not run |

- **READY is test evidence. It is never approval, selection or release.**

## Inputs (`harness-inputs/2`, H2)
- **Exactly the six dependency rows G, L, K, I, R and W, each `required: true`** (the boolean). Unknown, duplicate or missing rows refuse.
- **`accepted` rows** need frozen `files` pins **and** a `review_ref` {path, sha256, bytes} naming the Prime review. The harness checks that the reference is byte-unchanged.
  - It does not decide what the review says. **"Accepted" stays declared evidence, backed by that frozen reference.**
  - A status string flipped to `accepted` without pins refuses (HX-10, S14).
- **`pending` and `rejected` rows** carry `files: "PENDING"` and no `review_ref`.
- **An accepted R row must declare `interface.route: "review-report"`.**
- **Judgments** are exactly the three retained ids.

## Required callbacks (H1). Blocked while their input is pending; executable once it is accepted.
| Case | Executes, through the candidate's own `app/librarian.py` | Required (`judges.py`) |
|---|---|---|
| CAP-4 (K) | Synthetic N5 pages with harness-counted 64 and 65 sources, a 3-source page with a 25-reason judgment, and a 3-source page with a 265605-byte judgment: prepare → record (→ read). | **64:** complete; records; reads back canonically equal. **65:** complete; refused cleanly, naming `sources`. **25 reasons:** refused, naming `limit` and `reasons`. **Oversize document:** refused, naming the document bound. |
| RP-1 (R) | Three local N7 pairs: published (current); published, then the return changed (stale); an artifact missing (held). Core `read` + `prepare`, then `review-report`. | **States:** current → `state` `readable`, `stale` false; stale → `stale`/true; held → `held`. **Exchange, custody and review id:** `exchange.state`, `exchange.chronology`, `exchange.n1_custody`, `custody` and `review_id` equal the core. **Flags:** `authority` `none`; `accepted`, `work_complete`, `action_released` and `releases_action` false. Missing field = fail. No JSON body = an unimplemented operation = fail. |
| RP-2 (R) | Untampered control; tampered dispatcher; tampered selected workbook (restored after); unknown flag, repeated flag, relative book, bad pass, missing source; control again. | **The control succeeds**, so an always-refusing reporter fails. **Every probe refuses:** nonzero exit, no traceback, no observation state. |
| IN-2 (I) | An N5 page in book A: prepare → record → read. Byte-copy to book B. In B: read, recover, publish. Then A: read again. | **Original (A):** current before and after; byte-unchanged. **Copy (B):** positive hold evidence (nonzero read, `stale` true or `applicable` false), the lab judgment retained via read or recover, and publish refused with no destination file. A crash is not a hold. |

**Interface assumption (named, not hidden):**
- **The R interface is the dispatcher route `review-report --book --source --pass`.** That is the route shape of the frozen hardening lab (`labs/review-report-hardening-pass01/DISPATCHER.diff`).
- **The R output must use the field names of the frozen reporter tests** (`state`, `stale`, `authority`, `accepted`, `work_complete`, `action_released`, `releases_action`, `review_id`, `custody`), plus `exchange`.
- **If Prime's accepted R uses other names, Prime amends this table.** The harness does not guess a mapping.
- **K and I need no new interface.** They are exercised through `review-loop`.

## Strict N7 (H3)
**ST-1, ST-2 and ST-3 pass only if all of these hold:**
- the codes include **`malformed-n7-declaration`**;
- the rejected alternative is **not bound in its declared role**:
  - ST-1: the decoy `artifact-manifest.json,` as `artifact-manifest`;
  - ST-2: `06.15.notes.md` as `submission`/`return`;
- the intake is incomplete;
- record and publish are refused;
- the destination is unchanged.

**A pair-mismatch refusal no longer counts.** That was the 05.21 proto-l ST-2 situation.

**ST-4 (new control):** legitimate N5 filename punctuation (`,` `;` `)`) prepares complete, without the malformed code.

## N7-local route (#04)
- **N7-3 (new, G+L):** a recorded local N7 pair stores custody `not-applicable` in the record, and renders `custody: not-applicable`, never `missing`. The intake exchange carries `n1_custody: not-applicable`, and an N5 control keeps its own N5 custody value.
- **The report side of this** is RP-1.
- **LR-6** now also requires the destination `06.NN.review.md` on the same page and the same `.NN`.
- **LR-5** (historical chronology `unverified`) and **LR-7** (a second pass preserves the first) are unchanged.

## Evidence honesty
- **The automated inspect checkpoint** now stores the **full** inspect stdout (`<case>-inspect.stdout`) beside its hashes, labelled "not a human/model read".
- **Probe runs** (`probe.py`) bypass the dependency gate, carry `mode: probe`, and always exit 1. **They are not readiness.**
- **Scripted callback tests** (`test_callbacks.py`) are harness-behaviour tests. **They are not app acceptance.**
