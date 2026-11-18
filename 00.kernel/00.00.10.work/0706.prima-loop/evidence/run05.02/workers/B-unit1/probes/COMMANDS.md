# Probe commands (cwd /workspace/prima/run0502/workers/B/probes)

1. `/usr/bin/python3 -B probe1.py > probe1.out 2>&1`, exit 1. The first failure was in my own harness, not the source: `TypeError: required field "lineno" missing from stmt` at extract.py:20 (the synthesized ast.ImportFrom had no location info). Its output is saved as probe1.run1-harness-bug.out. Nothing in the source ran.
2. I fixed the harness only (added `ast.fix_missing_locations(mod)` in extract.py). Source code and expected results were not changed.
3. `/usr/bin/python3 -B probe1.py > probe1.out 2>&1`, exit 0. Output is in probe1.out.

The original functions that ran (AST-extracted, exec'd in an isolated namespace): pass01 same, word, apply_envelope (with ENVELOPE); pass02 counter, unknown_counter, sum_bytes, row_item, integrity_of, sha_key, unique_files, artifacts_of, counter_text, changed_keys (these last two were defined but not called); pass03 _unknown, _measured, _sizes, addressed_sources, content_blobs, physical_files, artifacts_of. publication_class was defined but not called. No module import was performed, and no core subprocess, CLI or test suite was run.
