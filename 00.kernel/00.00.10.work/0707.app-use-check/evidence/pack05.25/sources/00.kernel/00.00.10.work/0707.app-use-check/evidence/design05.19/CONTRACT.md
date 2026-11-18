# Minimum combined implementation contract — the Prime review loop (0707/05.19)
who: claude-opus-5-5 · state: **PROPOSAL for Prime review. No production code. No selection.** Future hashes are `PENDING` until the input successors are accepted and frozen.

## 1. Inputs (ownership; each is accepted separately before integration)
| Input | Owner / lane | Status at this freeze | What integration takes from it |
|---|---|---|---|
| **G**: strict N7 grammar workbook (proposed `labs/workbook-review-pass05`) | Grok-2, 0522/05.15 | PENDING | `parse_pointer` / `build_intake` with the measured-kind gate; malformed recognized N7 lines BLOCK intake |
| **K**: record capacity successor (a `prime_review` successor, path chosen by Grok-1) | Grok-1, 0512/05.10 | PENDING | an explicit supported source bound, an oversize diagnostic, every source identity kept |
| **F**: first-target cycle repair (`labs/n7-first-review-pass01` cycle and loop) | Grok-2, 0521/05.14 | ACCEPTED, isolated | the absent-create token and `render_committed` creation, re-staged under VERSIONED shared names |
| **R**: reporter hardening (v3 runtime contract `review-report-hardening/1`) | Grok-1, 0512/05.09 | ACCEPTED, not selected | report meaning; **its observation chain must be re-cut on W** |
| **W**: combined workbook overlay (NEW, `labs/workbook-review-pass06`, name proposed) | integration builder | to build | the single layer that pins G, K and F |

## 2. One chain, one overlay
The 0521 workbook is a modified COPY of pass02. pass03, pass04 and pass05 load the ORIGINAL pass02 by pinned path and hash, so **F's workbook cannot be stacked** (inv2 X3). **W** re-expresses F's workbook deltas as overlays on the G chain instead:

```
W (labs/workbook-review-pass06/workbook.py)
  -> G (pass05) -> pass03 -> pass02 -> pass01        all pinned, unchanged
  overlays on the loaded namespaces (p3, p2, wb):
    PINS["prime_review"] = K successor               (record capacity)
    PINS["review_loop"]  = F loop, versioned name    (absent-create render)
    PINS["prime_cycle"]  = F cycle, versioned name
    do_publish N7 absent-target rule                 (DIRECTOR QUESTION, section 6)
    cycle-path source records bind:false             (F's requirement; the preliminary path keeps pass03 bind = capture is None)
  REPO asserted in all namespaces, plus the canonical-root guard (as pass04)
```

Door **vN** (`app/review_loop_tools_vN.py` + `app/review-loop-vN.json`, N = next free after v9):
- schema `review-loop-pins/7`;
- pins W, G, pass03, pass02, pass01, K, F loop, F cycle, construct pass04 and the v4–v8 predecessors.

The **reporter successor R′** (`app/review_report_tools_v4.py` + JSON) runs the R runtime with observation on W, and pins the combined dispatcher bytes.

## 3. Single selection point and rollback
- **ONE edit of `app/librarian.py`:** the R hunk (`review-report` → v4) plus the review-loop selection line (→ vN), plus docstring lines. Its bytes are measured first; then R′ pins that hash. **There is no cycle:** the dispatcher pins nothing; the connectors pin the dispatcher.
- **Rollback:** restore `app/librarian.py` to c3a5be3b… (12204 bytes). All successor files stay on disk, inert. **Nothing else is edited.**
- **Never:** edit v4–v8, pass01–pass05, the reporter v1–v3 files, or any staged file in place. Those files are now declared evidence (0522/05.13, 0522/05.14 and 0512/05.07–09; inv1 C5, inv2 X5).

## 4. States (never collapsed into "done")
| Axis | Values | Who sets it |
|---|---|---|
| intake | `complete` · `incomplete` · **`blocked-malformed`** (G, N7 only) · stale | prepare |
| record | refused (incomplete / blocked / oversize / stale / changed source; judgment kept in `failed/`) · **`preliminary`** (custody missing) · **`cycle-committed`** (custody `complete-descriptor` + cycle) | record |
| publication | held (`manual-review` / `stale-own-review` / stale source / target appeared) · `published` (preliminary text into the destination) · `rendered` (cycle render; N7 absent-create) · `already-rendered` | publish / recover |
| custody | `missing` · `present-not-committed` · `measured` | intake + cycle |
| report | current · stale (exit 1) · held | review-report |

**Valid transitions:**
- `complete` → record → (`preliminary` | `cycle-committed`) → inspect (full read) → publish (separate command) → read / recover → report.
- Any source change after intake → stale everywhere, and the record is not rebound.
- **Preliminary publication is NOT cycle commitment, and NEITHER is matching N1 custody.**

## 5. Supported bounds (explicit, to be measured by the builder)
- **Book sources per record:** the K bound (today 24, measured as an exact boundary in inv1 C2).
- **Code-root artifacts** do not count as sources (inv1 C3).
- **Text and other lists:** unchanged prime_review limits (`MAX_TEXT` 12000, the other `MAX_LIST` uses) **unless K says otherwise**.
- **Concurrency, interruption, hard links (AR-01):** no claim.

## 6. The one Director question
> **"For an N7 Colab return with no matching N1 custody (so its review can only be preliminary), should a preliminary publish be allowed to create the first `06.NN.review.md` when it is absent? I recommend YES, labelled `mode: preliminary`, only when no custody descriptor exists and the file is absent at publish, because otherwise Colab N7 returns have no tool path to a first review. The accepted 0521 repair forbids this creation, and today's v7/v8 allow it."**

- **Yes:** W keeps the v7/v8 preliminary creation for the no-custody case, and F's absent-create stays the cycle-committed route.
- **No:** W adopts F's refusal; the first N7 reviews stay manual until custody exists.

**W cannot be finished until this is answered** (inv2 X4).

## 7. Preservation
- **Source and judgment:** the supplied judgment bytes are kept on every refusal (inv1 C1). Records are never overwritten (05.18 rollback). The prefix before the Review section stays unchanged. Manual Director text is byte-preserved and held.
- **History:** see HISTORY.md. Selection makes the declared-artifact evidence stale; it is reported, **never repinned**.
