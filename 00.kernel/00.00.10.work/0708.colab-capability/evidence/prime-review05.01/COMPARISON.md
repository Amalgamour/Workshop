# Compact-first versus expanded Prime review
Date: 2026-11-01. Case: 0708.colab-capability/05.01.

## Method and limitations
Same Prime session, compact first, expanded second. Prior session context already included predecessor reviews/pins and some return content. Not blinded, independent, or a complete recreation of every historical review habit. The compact conclusion was saved before raw source/evidence inspection and was explicitly provisional pending verification. Its SHA256 is b09647083502be47e696451ea555053b114215784adac72cab02c476ca70357d.

Compact input: entire current pack and return, 18645 file bytes, plus inherited context. It retained missing reserved mechanics, stale review pointers, commit-only packaging limit, misleading pending flag, grammar refusal, and direct-call versus CLI distinction. Expanded inspection added the 9341-byte builder notes, 17818-byte new driver, selected source functions, raw results and predecessor review artifacts. Compute hashed 544164 source bytes and 95734 artifact bytes without requiring all of those bytes in model context. File-byte counts are not token counts or total route costs.

## Comparison
| Question | Compact provisional review | Expanded review |
|---|---|---|
| Existing versus proposed capabilities | Preserved | Confirmed against source and raw outputs |
| Independence, custody, live-use limits | Preserved | Confirmed |
| Status and documentation drift | Preserved | Confirmed |
| Artifact/source integrity | Unknown, requested checks | 32 source rows and 60 artifact rows match |
| Current package mechanically intact | Not independently established | Checker valid; full verifier intact after documented permission change |
| New driver safe to rerun preserving evidence | Not caught | F01: driver deletes prior run directory; held for reuse |
| Audit conclusion | Provisional bounded acceptance | Bounded acceptance of findings, driver reuse held |

## What was learned
The compact pass preserved the main design interpretation, but failed to notice a meaningful implementation/evidence-retention defect. This is a limit of return-only review, not proof that all reduced-overhead review is unsound. The actual replacement process must include source inspection of new or changed executable files and independent integrity checks before acceptance. Hashes cannot reveal this defect: the problematic bytes match perfectly.

The experiment itself also incurred avoidable overhead: an overly broad instruction-file search traversed unrelated scratch fixtures and emitted access-denied noise; large combined outputs were truncated. Those are examples to remove from normal reviews. Use explicit ancestor instruction checks, bounded excerpts and structured summaries instead. Do not reduce the reasoning or source checks to compensate for inefficient tool output.

## Minimum review floor proposed for continued use
1. Read the exact full pack and return; keep uncertainty and unique findings.
2. Compute-check source/artifact manifests and predecessor pins.
3. Inspect every new/changed executable and the relevant contract; unchanged dependencies need targeted checks rather than automatic full rereads.
4. Reproduce decisive success/refusal cases when they establish acceptance. Never rerun a driver that overwrites sealed evidence. Keep environmental failures and changed-condition retries separate.
5. Write the full review at its correct workbook home; give the Director a concise outcome, material findings and next step.
6. Broaden review for conflicts, unknown dependencies, judgment forks or missing evidence. Preserve the Director's hard-stop agreement.

No exact token savings, percentage savings, or causal cost benefit were measured. Both routes shared context, and the full route benefited from the compact pass. This single diagnostic case does not establish equal quality for future build reviews. Correctness takes priority where additional inspection is necessary.

## Luna assistance proposal (research only)
Official model documentation read on 2026-11-01: https://developers.openai.com/api/docs/models/gpt-6-luna . Hosted model ID gpt-6-luna; standard input $0.10/M, cached input $0.01/M, output $0.50/M; Responses API and structured outputs supported. API account access has not been tested. No paid calls, credentials, installs or bot scheduling performed.

A local Clerk worker can call hosted Luna: this is local orchestration, not local inference. First test bounded evidence extraction: return claim -> cited path/lines -> reported versus independently checked -> missing evidence. Compute handles hashes, schemas and budgets; Luna handles extraction/search proposals; Prime keeps the judgment and checks source references. Do not replace a deterministic hash check with a model.

Use job-scoped inputs, structured outputs, no approval authority or unrestricted shell, capped calls/output/retries, and a usage receipt with actual tokens and cost. Proposed shadow test: use this same archived return, compare against F01–F04, and include the new driver so F01 is discoverable. A 20k-input/2k-output standard-text call calculates to $0.003 before any extra reasoning/tool/retry costs; it is an illustrative arithmetic estimate, not measured spend or a billing cap. Evaluate how much Prime verification work remains before claiming savings.
