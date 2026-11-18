# Builder handoff — task agreements in pack authoring and review intake (0707/05.14)
who: claude-opus-5-5 · state: **implementation-ready PROPOSAL for a future builder.**
- Nothing is installed or selected, and no production module is edited.
- The connectors below are **proposals**: none exists, and **no hashes are guessed**.
- Read with `SPEC.md`. The reference behavior is `labs/task-agreement-reference-pass01` (16 author lab cases).

## 1. Module responsibilities
| Module (proposed) | Owns | Must not |
|---|---|---|
| **A. agreement library** (successor of the lab `ta.py`, as a builder-owned NEW lab module) | parse the block; cut resolution (fences, exact-once, escape/link refusal, raw bytes); bind and compare; reconcile-request records | apply a release, terminal or hold rule; read meaning; rebind |
| **B. authoring connector** (a successor of the authoring module, as a NEW pass; the old pins stay) | a new form kind `agreement`: it offers the cut menu, takes intelligence choices, and **generates the block itself** during draft rendering, before review and freeze | ask Prime for hashes or paths it can enumerate; freeze a block holding hashes |
| **C. intake connector** (a successor of the workbook-review intake) | at prepare, read the block with A; store the binding **in the existing intake record**; replace the generic `agreement.* unknown` attention with field states | create a queue, ledger or current-state database; keep an old intake id after adding agreement evidence |
| **D. report projection** (the reader/report successor) | show the per-field state, status, provenance and compare status; show unknowns and `block-absent` plainly | add release wording, or hide unknowns |

## 2. Declared connectors (inputs and outputs)
- **A ← B:** `construct(book, page, pass, choices) → block_text | refusal(field, reason, help)`.
- **B → frozen pack:** the block sits under `## Task agreement`, before `## Return pointer`, inside the reviewed candidate. **The block holds no hashes,** so freezing introduces no self-reference.
- **C ← A:** `bind(book instance, page, pass) → binding` (the spec §5 schema), stored in the intake record. The intake and review ids **change** when agreement evidence is added; callers copy the returned ids.
- **D ← C:** `binding + compare(binding)` → the rendered rows.
- **Host policy:** C passes field states to the **existing** declared policy (the 0412 source-bound holds). **A new policy is a separate, named record, not part of A–D.**

## 3. Field → source map (recommended cuts)
| Field | Usual source | Example cut |
|---|---|---|
| goal | the pack itself | `self#Goal` (or the existing `Objective / …` heading) |
| scope | the pack itself | `self#Scope` (included, excluded, allowed writes) |
| finish_criteria | the pack itself | `self#Finish`, or `not-applicable` with a reason |
| prime_discretion | standing | `0412.prime-review/01.md#Local work agreement` |
| director_required | standing | `0412.prime-review/evidence/director-agreement.md` (whole) |
| recorded_decisions | 06.NN records | verbatim `#Director - verbatim`; interpretation `#Prime - exact proposal this reply approves`; answers = that proposal or a review question |

## 4. Model-facing interaction (SIMULATION; design only, not production tooling)
**Step 1 — Prime asks the authoring tool for the agreement form** (illustrative command, as in authoring-v2):
```text
librarian authoring form --book BOOK --profile 0707-colab --kind agreement --json
```
Simulated reply (compute enumerates exact headings; it does not interpret them):
```json
{"form": "agreement", "for": {"page": "0707.app-use-check", "pass": "05.14"},
 "fields": ["goal","scope","finish_criteria","prime_discretion","director_required","recorded_decisions"],
 "states": ["cited","unknown","none-recorded (recorded_decisions; reason)","not-applicable (reason)"],
 "menu": {"self": ["Objective / boundaries of this larger assignment", "#01 - Correct and finish the contract", "#05 - Reread and return a usable handoff"],
          "standing": ["0412.prime-review/01.md#Local work agreement", "0412.prime-review/evidence/director-agreement.md (whole)"],
          "decision_records": ["0412.prime-review/06.08.md (Director - verbatim | Prime - exact proposal this reply approves)"]},
 "help": "choose cuts; do not send hashes or paths outside the menu"}
```

**Step 2 — Prime supplies only meaning and choices** (small):
```json
{"goal": {"state": "cited", "refs": [{"source": "self", "heading": "Objective / boundaries of this larger assignment"}]},
 "scope": {"state": "cited", "refs": [{"source": "self", "heading": "Objective / boundaries of this larger assignment"}]},
 "finish_criteria": {"state": "cited", "refs": [{"source": "self", "heading": "#05 - Reread and return a usable handoff"}]},
 "prime_discretion": {"state": "cited", "refs": [{"source": "0412.prime-review/01.md", "heading": "Local work agreement", "applicability": "standing"}]},
 "director_required": {"state": "cited", "refs": [{"source": "0412.prime-review/evidence/director-agreement.md", "whole": true, "applicability": "standing"}]},
 "recorded_decisions": {"state": "unknown"},
 "gloss": {"text": "06.13.review 'Scope increase' paraphrases a Director observation; no verbatim Director record for this increase was found, so it stays unknown.", "by": "Codex Prime"}}
```

**Step 3 — the tool renders the draft with the generated block.** Prime inspects the whole draft and reviews the candidate (copying the returned `candidate_sha256`), and the tool freezes. **No hand-assembled metadata.**

**Step 4 — later, review intake binds the frozen pack.** The agreement view shows five fields `cited`, and `recorded_decisions` `unknown` (provenance block). **The host's existing policy decides what that unknown affects.** The resolver decides nothing.

## 5. File ownership for the build (proposal)
- **A:** NEW `labs/task-agreement-pass02/`. **B, C and D:** NEW successor passes of their current modules.
- **Prime** updates the pinned app declarations only after review.
- **Not touched:** the existing authoring-v2 and review pins, `labs/task-agreement-reference-pass01` (kept as reference), live pages, the kernel.

## 6. Tests the builder must pass
- **All 16 lab cases**, ported to A on disposable copies, with the same observed values.
- **Prime's independent probes**, kept separately labelled.
- **Integration cases:**
  1. B generates the block, and freeze leaves no hash in the block;
  2. C binds the frozen pack; the tool's own Return-pointer and review writes leave the agreement `current` (lab T01);
  3. a decision record edited outside its cut gives `context-changed` (T10);
  4. an old pack gives `block-absent`, and an explicitly selected profile gives profile provenance (T03);
  5. **intake ids change when agreement evidence is added,** and the old intake record is unchanged;
  6. D shows every unknown and adds no release text.

## 7. Bounded build order
1. **A** (library and CLI) to the 16 cases.
2. **C** reporting-only, with existing policy untouched.
3. **D** projection.
4. **B** authoring generation.

**Each step is separately reviewed;** B last, because it changes how Prime authors packs.
