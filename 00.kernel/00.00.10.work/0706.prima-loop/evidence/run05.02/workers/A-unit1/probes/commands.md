# Exact commands (Worker A, cwd /workspace/prima/run0502/workers/A/probes)
1. `/usr/bin/python3 -B probe_parse.py > probe_parse.out.json` -> exit 0, no failures. Ran once, no retries.
2. `/usr/bin/python3 -B findings_src.py` -> exit 0 (writes ../findings.json and ../findings.md); run twice (second run after adding one evidence line to A-01).
Read-only inspection used `cat -n`, `sed -n`, `rg`, `sha256sum`, `wc` on the source room. No production CLI, no imports of source modules, no writes outside workers/A.
