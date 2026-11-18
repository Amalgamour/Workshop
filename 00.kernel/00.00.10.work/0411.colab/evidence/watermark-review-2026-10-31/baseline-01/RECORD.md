# Execution record — baseline-01

Every run leaves one folder:
`runs/<sample_id>/<task>/<run_n>/`, for example `runs/S0a/T3/03/`. It holds:
- `prompt.txt`, a byte copy of the manifest prompt that was sent. Its sha256 must equal `prompt_sha256` in MANIFEST.json.
- `output.txt`, the reply exactly as saved, with no cleanup.
- `record.json`, from `record-template.json`, every field filled. Use `"unknown"` or `"not exposed"` where a value is not known, never a guess.
- `check.json`, the output of `python -I -B tools/check.py <task> output.txt --json check.json`. For T3, add `--reviewed` only after reading the code.

A record is written once and never edited. A correction is a new file, `record.correction-01.json`, naming the field, the old value, the new value and why.

## Fields (record-template.json)
- `run_id`: `<sample_id>-<task>-<run_n>`.
- `protocol`, `task_version`, `prompt_sha256`: taken from MANIFEST.json, and re-hashed from `prompt.txt` at record time.
- `model_id`: exactly as the surface reports it.
  - API: the `model` field of the response.
  - claude.ai: the name shown in the model picker, with a screenshot path.
  - Never inferred.
- `surface`, `surface_version`: where it was run, for example "Claude API (Messages)" or "claude.ai web". Give the app or SDK version if shown.
- `account_features`: memory, projects, styles and custom instructions, each on, off or unknown. They must be the same across all samples.
- `settings`: every request parameter actually sent. Parameters not sent are "not set (provider defaults)"; on claude.ai, "not exposed".
- `system_prompt`: "none", or the exact text with its sha256.
- `conversation`: "fresh" is required; one task prompt per conversation.
- `started_utc`, `finished_utc`: ISO 8601 times.
- `transfer_path`: how the reply reached `output.txt`. Examples: "API response text field, written as UTF-8 bytes" or "claude.ai copy button, pasted into editor X, saved UTF-8 LF". This matters for T1.
- `output_sha256`, `output_bytes`: of `output.txt`.
- `watermark_status`: `"unknown"`, unless there is reliable evidence for this model and this surface; that evidence goes in `watermark_evidence`, with source and date.
- `checks_run`: the check.py command line, its exit code, and `check.json`'s sha256.
- `operator`: who ran it.
- `notes`: anything unusual, such as a refusal, an error, a retry, or a truncation.

**Retries.** A run with an error, such as a timeout, an overload or a cut-off reply, is kept with its record and marked `"run_state": "error"`. A replacement run gets the next `run_n`. Nothing is overwritten or deleted.
