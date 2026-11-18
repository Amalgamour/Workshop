# Fault matrix — desk-core revision writes
date: 2026-11-01
who: Grok Build (xAI)
runner: Linux Python 3.11.2
raw: fault-matrix.json
injected exit: 91
windows: not run

`show` is read-only. `recover` is a second process. Receipt bytes stayed
put at every row. A return for A was not a fresh review of B.

| Boundary | Show before recover | Recover | Live pair after |
|---|---|---|---|
| before-prior-task | original, capture still complete | none | A, no history, B was never written |
| after-prior-task | partial, not complete | retained-previous | A, prior task copied |
| after-prior-face | partial, not complete | retained-previous | A, prior face copied |
| after-proposed-task | partial, not complete | retained-previous | A, proposal task copied |
| after-proposed-face | partial, not complete | retained-previous | A, both proposal files copied, not sealed |
| after-revision-journal | partial, not complete | retained-previous | A, seal present, not selected |
| after-task-replacement | conflict, not complete | restored-previous | A restored, proposal kept |
| after-face-replacement | partial, not complete | completed-proposal | B selected, both files already matched |
| after-selection-before-cleanup | selected, not complete | cleaned-marker | B stays selected, marker removed |

A second recover did not change task, face, history, receipt, or selected
bytes. The second result was `retained-previous`, `idempotent`, or `none`.

Not tested: a crash inside one `write` call, power loss, two writers, or
Windows `msvcrt`. An occupied `name.tmp` is still refused and not truncated.
