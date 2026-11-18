# Exact commands (Worker A unit 2; cwd /workspace/prima/run0502/workers/A2/probes; /usr/bin/python3 3.13.5)
1. `/usr/bin/python3 -B scan.py scan.raw.json` -> exit 0 (28 files scanned)
2. `/usr/bin/python3 -B pins.py pins.raw.json` -> exit 0 (147 raw pin entries incl. path-less constants)
3. `/usr/bin/python3 -B build_inventory.py` -> exit 0 (writes ../dependencies.json; 31 nodes, 9 absent)
4. `/usr/bin/python3 -B findings_src.py` -> exit 0, run twice (second after correcting the edge/pin counts in A2-01)
All are ast/static or hashlib reads of the source room. Nothing from the source room was imported or executed. No retries of failures (none occurred).
