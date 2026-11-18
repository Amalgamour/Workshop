# PORTABILITY — a separately bounded slice (assessment and acceptance)
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · state: assessment from source reading plus Prima's preserved cloud failure. Nothing here was run relocated.

## 1. Current observation
**Hard-coded roots in the reachable files** (static scan of pack05.02 bytes):

| File | Line | Use |
|---|---|---|
| `app/review_loop_tools_v2.py` | 24–25 | `CHECKOUT = Path(r"D:\Git\lib-build")`, `LIVE_BOOK`: **only** the disposable-root guard (207–209); refusal text at 208 |
| `labs/review-loop-pass02/review_loop.py` | 27 | `ROOT`: all 7 tool paths (29–48), `LIVE_BOOK`/`EVIDENCE` (53–54), the fixture-root guard (101), `pin_file` relpath (145), `run_tool` cwd (171), the reproduce guards (598–602, 843) |
| `labs/prime-cycle-pass03/prime_cycle.py` | 28 | `ROOT`: 6 tool paths (29–46), the fixture-root guard (263), tool cwd (342) |
| `labs/review-construction-pass02/construct.py` | 27 | `ROOT`: `TOOL` (28), the fixture-root guard (153), `prime_review` cwd (482) |

**Already module-relative:** `app/librarian.py` (`__file__`, 97–99), the door's `code_root` (301), `return_lines.py` (105, 255), `return_placement.py` (206), and `return_inspect.py`'s sibling (34). The two `prime_review` files have no root constant.

**Windows-only checks that degrade safely by construction:**
- Every `REPARSE`/`st_file_attributes` test uses `getattr(…, 0)` together with `S_ISLNK`.
- `O_BINARY` is guarded by `hasattr`.

These are source readings, not tests, and need a POSIX symlink case to confirm.

**Prima's preserved first failure (0706 #03):** on Linux, the door's relative pins passed. Then `review_loop.py` `pin_set()` hit `CONSTRUCT` under the literal `D:\Git\lib-build` and raised `FileNotFoundError`: a traceback, exit 1, not a refusal. The traceback is kept; it was not retried.

## 2. What the slice must change (proposed)
1. **All four roots derive from module location, together, in successors:**
   - door: `code_root = Path(__file__).resolve().parents[1]`, already used for pins;
   - loop, cycle and constructor: `Path(__file__).resolve().parents[2]`.

   Changing one file alone leaves a mixed state: on a relocated checkout, the loop would run relocated tools while the cycle and constructor still guard and execute against `D:\Git\lib-build`. Prima's "one line" fix (`review_loop.py:27`) would move the first failure to the cycle's `pin_file`, not remove it. That is source reading; Prima's #04 left it untested.
2. **The guard protects the actual checkout.** Each fixture-root and book guard compares against its own derived root, resolved. It must not compare against a constant.
   - On POSIX today, `Path(r"D:\Git\lib-build")` is one relative component, so `abspath` resolves it under the cwd, and a fixture root inside the real checkout would pass (Prima #05, an inference).
   - On Windows relocated to another drive, the guard protects the old path, not the running checkout.
   - **This is the safety-critical part, more than the crash.**
3. **Transitive agreement.** The door passes no root to the loop; each module derives its own. The tests assert that all four resolved roots are equal, and a mismatch is a refusal before any write.
4. **Missing pinned file → refusal.** `pin_file` (loop 142–145, cycle around 303), `pin_tool` (construct 372–374) and the door's `resolve_tool` must turn a missing or unreadable pinned file into the module's `Refusal` (exit 2, `pinned tool is missing: <label>`), never a traceback.
5. **Refusal texts** name the derived root, not `D:\Git\lib-build`.
6. **Repin.** New bytes for the loop, cycle and constructor mean new pins in:
   - the loop (CONSTRUCT, CYCLE);
   - the cycle (CONSTRUCT);
   - the door TOOLS and declaration;
   - the 0525 declaration records (in the accepted v2 representation, not `/1`).

   `prime_review`, `return_*` and the inspector are unchanged.
7. **Not to be done to make describe work:** no live-book mutation, no relaxed guard, no caller-chosen root or tool path, no pin bypass.

## 3. Acceptance slice (proposed)
| ID | Where | Case | Expected |
|---|---|---|---|
| P1 | native Windows, checkout at `D:\Git\lib-build` | the full A–F operator cases from 0707/05.01 | identical results to the v2/v3 baseline (regression) |
| P2 | native Windows, a relocated copy (for example `C:\…\scratch\lib-build-copy`) built from pinned bytes | `describe-legacy` and the A path on a disposable book | success. The `pins` in results name repo-relative paths. A `ROOT`-derived cwd is the copy, not `D:\Git\lib-build` (assert from a recorded `run_tool` cwd or a trace) |
| P3 | relocated copy | fixture root **inside the copy** | `stop: fixture root must stay outside <copy root>`, exit 2 |
| P4 | relocated copy | fixture root inside the original `D:\Git\lib-build` | **allowed or refused? Prime decides.** It is outside the running checkout but inside another checkout's live book. A module cannot know every other checkout in general. Recommendation: refuse the running checkout and its book only, and state that limit in the operator guide |
| P5 | Linux (cloud, Prima route) | Worker B's single `describe-legacy` command on a fresh snapshot | exit 0 and a descriptor. Then prepare, record, render and read on a disposable book |
| P6 | Linux | the fixture root is the snapshot itself | refused (the containment regression that is currently an inference) |
| P7 | any | delete one pinned tool from a disposable copy | exit 2, `pinned tool is missing: <label>`, no traceback, nothing written |
| P8 | Linux | a symlinked fixture root | refused (`is not a directory`/linked), confirming the `S_ISLNK` path without `st_file_attributes` |
| P9 | any | the four modules' derived roots differ (a test harness copies one module elsewhere) | refusal before any write |

## 4. Order and ownership (recommendation)
**Order: usability first (slice 1), portability second (slice 2).**
- Current Prime use is native Windows at `D:\Git\lib-build`, where F4 and F8 affect review correctness today.
- Cloud use is a pilot, not a current operating path.
- Slice 2 also changes the cycle, which slice 1 avoids.

**One code owner, sequential change sets.** Both slices change `review_loop.py` and `construct.py` successors and the door and declaration pins.
- Running them concurrently would produce two competing repins of the same files.
- Either one owner builds slice 1 and then slice 2 on top of the slice-1 successors, or Prime merges them into one change set deliberately.
- Do not write slice-1 files with module-relative roots "for free." Doing so creates the mixed-root state of §2.1, with the cycle and constructor guard still on `D:`.

**Dependencies.**
- Slice 2's repin needs the 0525/05.02 representation (D-04 working-tree basis, D-05 digest-only pin) to record the new identities truthfully.
- Slice 1 does not need it to be correct, but its declarations also land there.
