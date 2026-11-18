# Integration contract — v8 review entry (0707/05.18)
who: claude-opus-5-5 · state: **PROPOSAL for Prime review. Not installed, not selected.** The grammar is unchanged from `design05.17/CONTRACT.md`, which Prime accepted on 06.17.

## Selection chain (candidate)
`app/librarian.py review-loop …`
→ loads `app/review_loop_tools_v8.py` (the only code change in the dispatcher: the selection line, plus the docstring line that names the door)
→ the v8 door validates `app/review-loop-v8.json`:
- strict UTF-8 JSON with no BOM;
- exact top keys;
- schema `review-loop-pins/6`, version 1;
- **20 tool names:** the 17 from v7, plus `workbook_pass03`, `review_loop_v7` and `review_loop_v7_json`;
- each tool has exactly `{bytes, path, sha256}`, a safe relative path, no link, and is inside the code root, with matching hash and length.

It then hash-pins its predecessors:
- v4, v5, v6 and v7 doors and their JSON;
- pass01 and pass02 with their forms;
- **pass03 (new).**

After that it resolves every RESOLVE tool and runs `labs/workbook-review-pass04/workbook.py` in a subprocess with `cwd = code root`.

**pass04:**
- refuses unless its own location equals `REPO` (the canonical-root guard);
- loads pinned pass03, which loads pass02 and then pass01 under their own pins;
- asserts the same `REPO` in the p3, p2 and wb namespaces;
- installs the kind-gated `parse_pointer` and the context-setting `build_intake` in the three namespaces.

**`build_intake`:**
1. sets `KIND` from `wb.address_of(source, pass)["kind"]`;
2. delegates to pass03's `build_intake`;
3. resets `KIND` in `finally`, so the reset also happens on an exception (ctx02 X3).

**Fixture commands** (`--fixture-root`, describe-legacy, render, reproduce, run) stay on the pinned v4 door, unchanged.

## Grammar (from 05.17, accepted)
- **N5NN or no context:** the pass03 parser object, unchanged.
- **N7NN:** `Returned: PATH (ATTRIBUTION), sha256 H, N bytes.` and `Artifact manifest: PATH, sha256 H, N bytes.` first, then the pass03 forms.
- **The one collision** (`Artifact manifest: X, sha256 …`) is read as the N7 delimiter only in N7 context. This is decided by the measured kind, never by the filesystem.

## Root contract (new in 05.18)
- **The finding:** every workbook in the chain hard-codes `REPO = D:\Git\lib-build`, and pass02 and pass01 are imported at import time from that constant. A copied app tree therefore runs its own door but resolves code-root data from the live checkout. That is the W ("wrong-root") column of the matrix: `ambiguous-declared-root` on N5 and live data read for a copied book.
- **pass04 production bytes turn this into a refusal:** they refuse unless they are located at `REPO` (hostile N01).
- **The lab used one adapter line** (`REPO` = its own root) so it could run in disposable roots. The difference is exactly line 28 (`proposal/LAB-ADAPTER-pass04.diff`), and the lab declaration pins those adapter bytes (`proposal/LAB-ADAPTER-v8-json.diff`).
- **Disclosed:** even in the lab, the pass02 and pass01 module CODE is imported from the live checkout (read-only, hash-checked, byte-identical). Only their runtime `REPO` is the copy root.

## Identity contract (measured)
- **N5:** on the same file state, the v8 door equals the faithful pass03 baseline: intake_id, rows, cuts, findings and measurement (matrix02 B == D and B2 == C, for 0522/05.13 and 0512/05.06).
- **N7:** the intake gains the declared submission, the manifest and every artifact (26/26 for 05.15, 33/33 for 05.17, measured hash equal to the manifest hash, no row lost). The intake_id therefore changes by design.
- **The dispatcher is itself declared evidence.** 0522/05.13 lists `app/librarian.py` (c3a5be3b…), `app/README.md`, the v7 door and its JSON, and pass03 files as artifacts.
  - **Selecting v8 rewrites `app/librarian.py`, so 0522/05.13 then measures `incomplete` (`artifact-hash-mismatch`) under the old and new parser alike** (matrix02 B2 == C).
  - This is not a parser regression. It is a selection consequence, and Prime must accept it or plan for it (see `BUILD-PACK.md` stop conditions).
- **intake_id includes the book path.** Ids are compared only on the same root. Rows and cuts are root-independent (matrix01 equals matrix02).

## Lifecycle contract (measured on copies, real v8 entry)
- **Preserved:** missing custody, the preliminary mode, no release (`releases_action false`, `published_work false`) and `task_association not-established`.
- **Existing manual review:** Prime's 06.15 text is byte-preserved and publication is held as `manual-review`.
- **A page that already carries a v7 review:** publication is held as `stale-own-review`.
- **A manual target that appears between record and publish:** publication is held and the text preserved (P11).
- **A material source change after read:**
  - read, recover and publish are held as stale;
  - re-record is refused;
  - nothing is silently rebound.
- **read and recover are idempotent** (equal output, no writes).
- **v8 records are never overwritten by v7.** Under v7 an N7 v8 record reads as stale, and v7 adds only `failed/` correction files.

## Not established
- **Production bytes at the canonical root:** the success path of pass04's production bytes is not executed. Only the refusal (N01) and the one-line equivalence are.
- **Cycle commitment:** `cycle.called` was false in every lifecycle run.
- **Concurrency and interruption:** no guarantee is tested or claimed.
- **The authoring and return-lines routes:** these were checked only up to the same missing-pin stop.
