# Baseline protocol — baseline-01
Date: 2026-10-31. Prepared by claude-opus-5-5 (Anthropic), Colab session. State: prepared and self-tested; **no model has been run.**
Beside: ../NOTES.md, ../REPORT.md and ../PREMISE-CHECK.md, all unchanged. Notes for this protocol: NOTES.md, written first.

## Purpose and limits
This protocol preserves a dated, repeatable sample of current model performance, to compare with a later sample.
- It is **not** a watermark on/off experiment. `watermark_status` is `"unknown"` for every run, unless there is reliable evidence for that model and surface.
- A difference between samples is described, never attributed to watermarking or any single cause without supporting evidence (SCORING.md, attribution rule).
- Mechanical checks establish only what each states (SCORING.md table). None establishes overall correctness, preservation of meaning, clarity or voice; those are blind human judgments.

## Contents
| file | role |
|---|---|
| MANIFEST.json | protocol version, every prompt's sha256 and byte size, fixture hashes, tool hashes |
| tasks/*/prompt.txt | the exact text to send, one per task, composed by tools/build.py |
| tasks/* fixtures | T1 source, T2 note and answer key, T3 ledger.py and held-out tests, T4 spec, T5a constraints |
| tools/check.py | mechanical checks per task |
| tools/selftest.py | runs every check on known-good and planted-bad replies |
| tools/blind.py | blinds outputs for human scoring |
| tools/build.py | composes the prompts, writes MANIFEST.json |
| SCORING.md | mechanical vs human scores, scales, the comparison rule |
| RECORD.md, record-template.json | the per-run execution record |
| verification/ | the build and self-test logs from preparation, first-run failure included |

## Tasks (all v1)
| id | covers | prompt sha256 (first 12) | checks |
|---|---|---|---|
| T1 | exact copy: em dash, curly quotes, tab, trailing spaces, non-breaking space, accents, 64-hex pin, backslash path, no final newline | e09bfcf5e57f | byte equality, form |
| T2 | structured output: prose to JSON, an exclusion instruction, mixed date forms, a null | 4e9cb3224679 | parse, keys, ids, order, values vs key |
| T3 | a bounded code change, "do not change other functions" | 8e858dc0be28 | form, AST identity of other functions, no new top level, 6 held-out tests |
| T4 | spec revision preserving 11 rules | e3de8d1f6317 | ids, backticks, numbers, modal-count indicator; meaning is human |
| T5a | original constrained prose | dbf4f73cd3bf | length, required phrases, forbidden words; voice and clarity are human |
| T5b | voice continuation of the Director's writing | **withheld** | needs `tasks/T5b-voice/VOICE-SAMPLE.txt` (about 300 words of the Director's own prose); then rerun build.py |

Full hashes are in MANIFEST.json. The rule for prompt versions: a changed prompt is a new version (`T3.v2`) with its own hash, and samples are compared only on the same version.

## Procedure for one sample
1. **Before the sample.** Run `python -I -B tools/build.py` and confirm that every `prompt_sha256` it prints equals the table above and MANIFEST.json. The folder is untracked, so `git diff` cannot show this yet. Run `python -I -B tools/selftest.py` and expect `SELFTEST OK`.
2. **For each run.** Open a fresh conversation, with no system prompt and with account features the same as in every other sample. Send `prompt.txt` byte for byte; on the API, as the single user message. Save the reply unmodified as `output.txt`, and record the transfer path.
3. **Fill `record.json`** (RECORD.md). Take `model_id` from the surface, never from memory.
4. **Run `tools/check.py`.**
   - For T3, read the code first, then add `--reviewed`. The held-out tests then execute the model's code in a temporary folder with `python -I -B`. **This is not a sandbox.**
5. **After the whole sample.** Do no human scoring yet. Scoring happens once, after the later sample, on blinded copies of all samples together.

## Repeated samples
- **Runs per sample:** 5 per ready task, each in a fresh conversation. Within a round, the order of tasks is shuffled, and the order is recorded.
- **Baseline samples:**
  - S0a: as soon as released, 2026-10-31 or 11-01;
  - S0b: on a different day, 2026-11-02;
  - two days show day-to-day spread before anything is compared.
- **Later sample S1:** on or after 2026-11-10, with the same model id, surface, features, settings and prompt versions. If the model id differs, S1 is a different model and the comparison says so.
- **Optional S2:** about a month later, the same way.
- **Volume:**
  - 5 ready tasks × 5 runs = 25 runs per sample per model (30 with T5b);
  - S0a + S0b + S1 = 75 runs per model (90 with T5b);
  - each run is a short prompt and a reply under about 1,000 tokens.
- **Comparison** (SCORING.md):
  - mechanical pass counts per check, S0a and S0b side by side with S1;
  - a difference is "observed" only when S1 falls outside the range of both baselines;
  - human scores are taken blind across all samples at once, then unblinded.

## Known limits of the design
- **Five runs is small.** It shows gross spread, not small effects.
- **The surface matters.**
  - claude.ai renders Markdown and its copy button may alter whitespace (T1).
  - claude.ai adds its own system prompt and features, which can change between dates without notice.
  - The API with no system prompt gives the cleanest record.
- **The preparer's hand.** The answer keys and held-out tests were written by the preparer, an Anthropic model, and are open to audit.
- **Provider changes.** Silent changes, such as a model snapshot or the system prompt, cannot be ruled out, only recorded as far as the surface reports them.
- **Not this session.** This session wrote the tasks, so its own replies are not a valid sample.

## What running it needs
Pick one surface per model, and keep it for every sample.
- **(a) Claude API.** Cleanest record: exact `model` field, explicit settings, raw bytes.
  - Needs an Anthropic API key on a billed account, available to whoever runs it. For me, that means set in the environment, never pasted into chat.
  - Needs a release for 75 to 90 calls per model.
  - Needs a small runner script. It is not written: running it means paid calls, which are not released. It is about 60 lines that send `prompt.txt` and write `output.txt` and `record.json`, and it can be prepared without running it.
- **(b) claude.ai or the Claude app, run by the Director by hand.** About 25 fresh conversations per sample.
  - Settings are not exposed, `model_id` comes from the picker, and the transfer path is the copy button, which weakens T1.
  - It is the right choice only if the claim to protect is "the product I use".
- **Either way:** the Director's T5b voice sample, if voice continuation is to be covered.

## Verification of the preparation (2026-10-31)
- **build1 and selftest1** (verification/): the self-test crashed with a harness fault, not a check fault. On Windows, check.py's stdout was cp1252, so the em dash in the T1 diff reached the self-test as byte 0x97. Fixed by writing stdout as UTF-8. Kept.
- **build2 and selftest2:** `SELFTEST OK`.
  - 5 of 5 known-good replies pass every check. This includes a reference T3 solution passing the held-out tests, which shows they can be satisfied.
  - 21 of 21 planted faults are caught, each by the check aimed at it.
  - This shows the checks detect these planted faults. It does not show they detect every fault.
- **Git:** nothing staged, committed or pushed. The folder is untracked in the workshop (HEAD 960d20c5…, branch workshop).
