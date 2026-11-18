# Delta — return-readiness pass02

Schema: `return-route-readiness-delta/0511`
Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.
This delta is written before the successor is executed. It is not a release and not app selection. It is not revised after the suite commands.

## Boundary

`labs/return-readiness-pass02/readiness.py` is a wrapper around the unchanged `labs/return-readiness-pass01/readiness.py`. It loads that module and `labs/return-readiness-pass01/contracts.json` by path. It refuses, exit 2, if either file's sha256 differs from the `pack05.11` row: readiness.py `e9d59040920e06cc2edf0d5d2ebdec8954e83945fa2629b9eae08e5164cfcecf`, contracts.json `0bd74ada28e4828df9fe74feffdbb44af3eba4df9f57c64a9512f93373664cfc`. It does not rewrite those files and it does not invent route pins.

The command is the same shape as pass01: `--code-root` and `--book`, optional `--text`. Any other flag is refused. Exit 2, empty stdout, one `refuse:` line. The public command has no injection flag. `inspect(..., read_bytes=...)` remains the unit seam.

`importlib` loads pass01 only. The successor does not import or execute inspected app code, does not start a subprocess, and does not classify review-loop.

## T1 — invalid dispatcher text

A stable dispatcher whose bytes are not UTF-8 produces one observation, exit 0, not a traceback. `dispatcher.state` is `malformed`. Byte length and sha256 are kept. `decode` records encoding `utf-8`, the position, and the reason. Both routes are `unknown` with selector `unknown` and no selected facade. That is not `absent` and not `selected-valid`. Authority stays `not-assessed`. The three pass01 warnings stay. `coherent` is true when the two dispatcher reads match. `final_check` is `matched`.

A syntax error that decodes remains pass01's result: dispatcher `malformed`, routes `unsupported`.

`UnicodeDecodeError` and `OSError` raised by a measurement read become an observation. Any other exception still propagates. There is no catch-all that reports success.

An `OSError` from a measurement read yields routes `unknown`, `coherent` false, `final_check` `not-run`, and `read_error` set to the exception type name. It is not `selected-valid`.

## T2 — one final re-read

Pass01's adjacent pair does not cover a file that changes after that pair. After the pass01 observation, pass02 re-reads every recorded path once, through the same seam, and re-stats the door directory. One pass. No retry and no lock.

`selected-valid` remains only when pass01 reported it and every re-read matches state, sha256, and byte length, and the door directory state matches. Then `coherent` is true, `final_check` is `matched`, and `dispatcher.sha256_final` equals `dispatcher.sha256`.

A changed byte string, a disappearance, a linked or wrong-type replacement, or a missing layout that becomes present makes `coherent` false and `final_check` `changed`. `changed_paths` lists each relative path with the before and after state and sha256. Both routes become `unstable` with selector `none` and no selected facade. The first-cut route details are not kept. A changed layout or door is `unstable`, and `declared` is false. The dispatcher state becomes `unstable` when the dispatcher path changed. `sha256` stays the first measurement. `sha256_final` is the later measurement.

This whole-observation rule is deliberate. A route is not reported valid from one cut while another path in the same call changed.

A finished observation is not a guarantee against a change after the final check. That sentence is a limit. The whole dispatcher hash remains provenance. A later separate inspection may see other-branch edits and still report `selected-valid` when its own final check matches. Those edits do not become a permanent pin.

## Unchanged distinctions

The static recognizer, the old and new route pins, staged versus selected, and declaration validity stay pass01's. Invalid UTF-8 in a declaration or dependency is a byte mismatch when the pin differs. It is not executed and it is not treated as a default empty file. Layout text that is not UTF-8 stays `malformed` through pass01's layout parser. The book scan stays narrow.

Schema `return-route-readiness/2` adds `coherent`, `final_check`, `changed_paths`, `decode`, `read_error`, and `dispatcher.sha256_final`. `--text` formats that same object and adds `coherent` and `final_check`. It does not measure again.

The tool creates no file.
