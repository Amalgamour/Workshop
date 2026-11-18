# PRIME-USE — coherent return-route readiness

From `D:\Git\lib-build`:

`python -B labs/return-readiness-pass02/readiness.py --code-root D:\Git\lib-build --book D:\Git\lib-build\00.kernel\00.00.10.work`

`--text` prints a projection of that same JSON object and adds `coherent` and `final_check`. The demonstration saved as `live-stdout.txt` used `--text`. Exit 0. Stderr was empty. The tool created no file.

## What that output says

Schema `return-route-readiness/2`. Authority `not-assessed`. Authorization false. App selection applied false. `coherent` true. `final_check` `matched`.

`return-lines` is `selected-valid`, selector `old`, facade `app/return_line_tools_v2.py`. The successor `app/return_line_tools_v3.py` is staged and its reviewed facade and declaration bytes match.

`capture-return` is `selected-valid`, selector `old`, facade `app/handoff_tools.py`. The successor `app/handoff_tools_v2.py` is staged and its reviewed facade and declaration bytes match.

The dispatcher is measured, sha256 `b15919adb7664f993373fbc6eaaaf86d66100f396b3401845900734f920248ea`, 12204 bytes. `sha256_final` is the same hash. The predecessor snapshot is sha256 `826167161000ac3eab78c466ae47e31b37ff435ea33f4104caf7651ecd21436e`, 12153 bytes. `matches_predecessor_snapshot` is false. That whole-file difference is provenance.

The book door `0100.band.returns` is present. `01.md` is sha256 `c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d`, 10206 bytes. `return-line-layout.json` is missing. `declared` is false.

The observation has 20 reads: the dispatcher, the selected old closure, the staged successor facade and declaration files, the layout path, and the door page. It does not classify other branches.

These warnings are in the report:

- An unselected successor does not protect the app.
- A guard on an undeclared book delegates to the historical writer.
- Historical direct scripts remain runnable.

These limits are added by the successor:

- Invalid UTF-8 leaves route selection unknown.
- One final re-read is not a lock and is not retried.
- A completed bounded observation is not a guarantee against changes after the final check.

Missing prerequisites: no valid line-pass declaration, the reviewed successor is not selected on both routes, migration and release authority were not assessed, and this tool records no Director release.

## What that output does not do

It does not select the app, write a layout, assess a release, approve the work, or file custody. A non-UTF-8 dispatcher returns an observation with both routes `unknown` and keeps the measured byte identity. A change in the bounded read set, including a file that changes after its first measurement, makes `coherent` false and both routes `unstable`. Prime reviews the observation before any selection.

The focused suite command is `python -B labs/return-readiness-pass02/tests/run_suite.py`. Its exit 0 is not Prime review.
