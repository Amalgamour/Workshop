# Commands (all run from /workspace/prima/run0502/source-room/00.kernel/00.00.10.work unless noted)
1. Presence loop over referenced 0512 files -> probes/presence-0512.txt. exit 0.
2. `/usr/bin/python3 -B probes/check_pointers.py > probes/check_pointers.out`. exit 0. The first run had wrong page:line labels, which came from my own notes; it is saved as check_pointers.run1-wrong-labels.out. I corrected the labels only (hashes, paths and logic unchanged) and reran: exit 0. The results were identical apart from the labels.
3. `grep -n -i director` across the 0512 and 0521 pages and evidence. exit 0.
4. Python json read of build05.06 current-review/report.json and summary.json; `sha256sum` of known-failures/identical-files-pass02.json and current-review/report.json. exit 0.
5. Presence check of 0521 06.25.md and evidence/pack05.13/source-manifest.json (both ABSENT). exit 0.
6. `cat -n` and `grep -n` reads of 05.05.md, 05.06.md, 05.07.md, 06.09.md, 05.13.md, 06.26.md (partial), and build05.13 submission.md, CONTRACT.md and verification.json.
No production CLI, no imports of source modules, no D: tree, no writes outside workers/B2.
