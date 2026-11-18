# CONTRACT — Colab review adapter (labs/colab-review-pass01)

Written before the code, for 0518.colab-review 05.01. This is a lab adapter, not seated and not a review engine. It validates declared review plans, links and results, and derives reports. It never launches a model, a reviewer or a session, never authenticates isolation, and never judges meaning.

## 1. Seam with the existing tools (byte-identical, pinned before every launch)

| tool | pinned identity | how this adapter uses it |
|---|---|---|
| producer v2 `labs/colab-support-pass02/colab_support.py` | 2b720434… / 53892 | `preview`, `prepare` and `verify`, launched as documented; never imported |
| workflow v2 `labs/colab-workflow-pass02/colab_workflow.py` | sha recorded at build | `open`, `attach`, `place-return` and `record-review` (demo only) |
| helper `return_capture.py` | 8f3da5c6… / 45767 | `reserve` and `verify`; capture goes through producer `intake` |
| inspector `return_inspect.py` | 947915fe… / 11402 | `inspect --json` for each result member |

**What the adapter adds:**
- review files appended as `required_sources` of a Prime-supplied `colab-request/2`, committed beside the target in one disposable source repository and commit;
- its own records, in its own new output folders.

**What it never does:** add to a producer OUT, change a digest preimage, or relabel data.

**Old data stays readable:**
- a producer package with no plan binds as `legacy-no-review-plan`;
- a member with no `review-result.json` reads as `legacy-no-result`;
- neither is an error.

## 2. `colab-review-plan/1` (Prime-supplied; strict JSON, exact keys)

```
{"schema", "plan_id" (label), "investigation": {"book","page","pass"},
 "mode": "cold-comprehension"|"contextual-critique"|"implementation-check"|"combination",
 "reviewers": [{"id": "R01..", "label", "context": {"conversation_supplied": "none"|"summary"|"full",
                "host_context": str, "familiarity": str, "isolation": "unknown"|"host-declared"|"unverified"}}],
 "stages": [{"id": "S01..", "kind": "comprehension"|"critique"|"simplicity"|"implementation",
             "reviewers": ["R01",…] (≥1), "required": bool}],
 "ordered": bool,
 "read_scope": [str], "withheld": [{"item","reason"}], "finish_boundary": str,
 "simplicity": null | {"before": str, "after": str, "fixes_under_review": [str]},
 "round": {"number": int ≥ 1, "cap": int|null}}
```

**Refused:**
- a cold mode where any reviewer has `conversation_supplied` other than `none`;
- a stage with no reviewers, or naming an undeclared reviewer;
- a simplicity stage with `simplicity` null, or `simplicity` set without a simplicity stage;
- ids out of the `R01`/`S01` order;
- duplicates;
- an isolation value outside the list. There is no "verified".

## 3. `stage` — commit the review sources and compose the request

`stage --plan P --request BASE --repo DISPOSABLE --out-request NEW` does the following:
1. Checks the base request: `colab-request/2` shape, with every target in `--repo`.
2. Writes these new files into `--repo` under `reviews/<plan_id>/` (exclusive; refused if any exist):
   - `review-plan.json`, the exact plan bytes;
   - `COMPREHENSION.md`, a prompt to explain the proposed behaviour, the current system, the task and authority boundaries, and the handback route before any finding;
   - `SIMPLICITY.md`, only when a simplicity stage exists;
   - `RESULT-TEMPLATE.json`, a `colab-review-result/1` skeleton.
3. Commits them with a task-local identity (`git -c user.name=… -c user.email=… commit`). The global config is never touched.
4. Re-pins every target to the new commit, after checking each target blob is unchanged.
5. Appends one `required_sources` row per review file.

The output is the new request. Prime then runs the producer's `preview` and `prepare` unchanged.

## 4. `bind` — prove the review sources survived prepare and verify

`bind --output PRODUCER_OUT --config C --producer ABS_PRODUCER_V2 --expect-digest D --out NEW [--plan P]` (the producer path is explicit because `colab-config/2` has exact keys; it is pin-checked before launch):
- **Verify:** runs the pinned producer `verify`. It must report `intact` with digest `D`.
- **Locate:** reads `package/source-manifest.json`, finds each review file by path, and compares the snapshot bytes with the plan, its re-rendered prompts and the template.
- **Write** `colab-review-binding/1`, `binding.json` in the new folder:
  - the digest and plan sha;
  - each review file's path, snapshot and sha;
  - `covered_by: {"producer-verify": [the package files, digest], "adapter": ["review file presence and content equality"]}`.
- **No plan in the package:** `legacy-no-review-plan`, exit 0.
- **Exits:** a mismatch is exit 1; a refusal is exit 2.

## 5. `colab-review-result/1` (reviewer-supplied; travels as artifact `review-result.json` in an N1 member)

```
{"schema", "plan_id", "plan_sha256", "reviewer", "stage", "status": "completed"|"partial"|"failed"|"not-run",
 "context": {"conversation_supplied","host_context","familiarity","isolation"},
 "comprehension": null | {"proposed","current_system","task_authority","handback_route"} (each non-empty text),
 "findings": [{"id": "<reviewer>-<stage>-F<NN>", "target": str, "location": str, "text": str}],
 "simplicity": null | {"added_complexity", "addresses_failure", "reuse_or_duplication", "accepted_limitations": [str]},
 "label": "SYNTHETIC"|"ACTUAL"}
```

## 6. `intake` — derive what came back

`intake --binding B --plan P --book BOOK --member M… --config C --out NEW`:
- **Per member:**
  - runs the pinned inspector, and requires `complete`;
  - reads `review-result.json` from the member's own payload, by its manifest logical path, and checks its sha.
- **Checks, each a finding, never a repair:**
  - `plan_sha256` equals the bound plan (otherwise `source-identity-altered`);
  - the reviewer and stage are declared, and the reviewer is assigned to that stage;
  - one result per (reviewer, stage); a duplicate is `duplicate-result`;
  - the context equals the plan's (otherwise `context-mismatch`), and `isolation` is shown as declared;
  - a comprehension stage needs all four paraphrase fields, otherwise `missing-comprehension`; the paraphrase is kept verbatim, with zero findings allowed;
  - finding ids are well formed, unique, and prefixed with the reviewer and stage; otherwise `bad-finding-id` or `duplicate-finding-id`;
  - a simplicity stage needs a `simplicity` block;
  - with `ordered`, each stage's earliest `captured_at` must follow every earlier stage's latest; otherwise `sequence-violation`.
- **Every (reviewer, stage) the plan requires** and that is absent, `failed`, `partial` or `not-run` goes into `incomplete`, with its status. It is never counted as zero findings.
- **Output:** `colab-review-intake/1`, `intake.json`, with `status` `complete` only when there are no findings and nothing is incomplete. `covered_by` names the inspector for custody; everything else is adapter validation.

## 7. `colab-review-synthesis/1` and `synthesize`

```
{"schema", "plan_id", "intake_sha256", "by": str, "label": "SYNTHETIC"|"ACTUAL",
 "items": [{"id": "X01..", "title", "findings": [ids], "recommendation"}],
 "retained": [{"finding": id, "disposition": "dissent"|"minority"|"rejected-with-reason"|"duplicate-of", "reason", "of": id|null}],
 "disagreements": [{"findings": [ids], "text"}], "incomplete": [{"reviewer","stage","status"}],
 "residual_uncertainty": [str], "acceptance": null}
```

`synthesize --intake I --synthesis S --out NEW` checks mechanically:
- `intake_sha256` matches;
- every original finding id appears exactly once across `items[].findings` and `retained[].finding` (otherwise `lost-finding`, `unknown-finding` or `double-mapped`);
- `duplicate-of` names an existing id;
- disagreements cite known ids;
- `incomplete` equals the intake's incomplete set exactly (otherwise `incomplete-mismatch`);
- `acceptance` is null, or the input is refused.

If the plan's round cap equals its round number, the report says `cap-reached: not acceptance`.

The output is `colab-review-report/1`: `report.json` plus `REPORT.md`, a derived report.
- It quotes the original finding texts and comprehension paraphrases from the intake.
- It keeps dissent, disagreements, incomplete and uncertainty.
- It states `derived; originals are in N1 custody and the workflow page; not a review, not acceptance`.

`report_digest` is the sha256 of the canonical `report.json` without that field. The domain is `colab-review-report/1`.

## 8. Outputs, exits, bounds

- Every `--out` and `--out-request` must be new, under an existing plain parent, with no link in the path. Files are exclusive-create.
- A failed write is `partial` (exit 3), and the files are kept.
- Exits: 0 clean; 1 answered with findings or mismatch; 2 refused; 3 partial.
- Bounds: 32 reviewers, 16 stages, 256 findings per result, 256 KiB per input, 2 MiB per output.

## 9. Readiness and dependencies

The accepted readiness checker may be pointed at the prepared package, within its declared-record capability: transport hashes and declared dependencies only. It establishes neither semantic quality nor an authenticated smoke result.

The dependency prototype is not consulted. It is optional, and not a gate.
