# Notes — dated comparison baseline, protocol baseline-01
Date: 2026-10-31. Preparer: claude-opus-5-5 (Anthropic), in the same long Colab session that wrote ../NOTES.md, ../REPORT.md and ../PREMISE-CHECK.md.
State: written first, before the protocol, fixtures and tools. The earlier review files are not changed.

## The task as released
- Change of task: from investigating the watermark premise to preparing a dated comparison baseline.
- Watermark status is recorded as `unknown` unless there is reliable evidence for the specific model and surface. That uncertainty is not a blocker.
- Goal: a repeatable sample of current performance, to compare with a later sample. It is **not** a watermark on/off experiment, and no difference may be attributed to watermarking without supporting evidence.
- Prepare:
  1. fixed tasks (exact copying and structured output; code with meaningful checks; spec revision preserving meaning; creative prose and voice);
  2. a scoring guide that separates mechanical results from human judgments;
  3. an execution record format;
  4. a plan for repeated samples.
- Execution restriction stands: no paid calls, no model launches. Preparing the protocol is allowed.
- Every check must state exactly what it establishes. None may be described as proving overall correctness or preservation of meaning.

## Disclosure
- I am an Anthropic model preparing a test of Anthropic models: a conflict of interest. The design gives the decisive judgments (meaning, clarity, voice) to the Director, blind to sample date.
- This session wrote the tasks and their answer keys, so its own outputs on these tasks are not a valid sample. I do not run them on myself.

## Choices
B01. **Self-contained fixtures.** Live workshop pages change, which would make a later sample answer a different question. Every input is a fixed file inside baseline-01, hashed in MANIFEST.json.
B02. **What gets hashed.** Each `prompt.txt` is the exact text to send, composed by `tools/build.py` from a header plus the fixture. Its sha256 identifies the prompt version. A changed prompt is a new version (`T1.v2`), never an edit in place.
B03. **Tasks.**
- T1, exact copy;
- T2, prose to JSON;
- T3, a bounded code change with held-out tests;
- T4, a spec revision;
- T5a, constrained original prose;
- T5b, voice continuation.

T5b needs a passage of the Director's own writing. None is in hand, and I will not invent one ("missing stays missing"). T5b is withheld until it is supplied.
B04. **Checks are labelled.** Every mechanical result carries `establishes` and `does_not_establish` strings. Meaning, clarity and voice are human judgments, scored blind.
B05. **Running model code.** The T3 check runs the returned code only with an explicit `--reviewed` flag, after a person has read it. It runs in a temporary folder with `python -I -B`. That is not a sandbox, and the protocol says so.
B06. **Settings.** On the API, no sampling parameters are set. Secondary sources conflict about whether newer models accept them (../NOTES.md S9), and leaving them unset keeps samples comparable. Recorded as "not set (provider defaults)". On claude.ai, settings are not exposed and are recorded as such.
B07. **Repetition.** Five independent runs per task per sample, each in a fresh conversation, and two baseline days if time allows, so that day-to-day spread is visible before any later comparison.
