# Selection delta — rules for Prime

Schema: `return-access-handoff-delta/0509`
Date: 2026-11-02. Written before the successors. This file states the substitutions. It does not contain successor hashes. Measured pins are recorded later in `SELECTION.md`, after the files exist. Filling `SELECTION.md` does not revise this file.

## Two branch substitutions

After Grok-1's review-loop return and after Prime review of this build, Prime measures the then-current dispatcher and applies only these load-path substitutions:

| Command | Current load in the pre-Grok-1 snapshot | Successor load |
| --- | --- | --- |
| `return-lines` | `app/return_line_tools_v2.py` | `app/return_line_tools_v3.py` |
| `capture-return` | `app/handoff_tools.py` | `app/handoff_tools_v2.py` |

The replacement Prime applies is those two path strings, plus the additive documentation sentences in `SELECTION.md`. It is not a wholesale copy of an older dispatcher. `authoring` stays on `authoring_tools_v2.py`. `review-loop` stays on the successor Grok-1 returns. Boot and batch stay on their current helper pins.

## Dependency closure Prime remeasures

The successor facades close over pass04, pass03, pass02, pass01, placement, the historical reader, the reviewed guard, the new handoff, the Clerk, and the inspector. Prime remeasures those bytes at selection time. A mismatch stops the selection. This build does not silently repin.

## What stays unselected here

This file does not select the routes. It does not create a live layout, a live authority, or a live root. It does not move the `01NN` band. It does not file a receipt. Root choices and the real execution release remain Director decisions. The concrete candidate roots, guard proof, and rollback evidence are named in `CUTOVER.md` after the suite measures them.
