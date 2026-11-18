# IMPACT-MAP v2 (proposed)
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · from source inspection of pack05.06 bytes; nothing edited

## Existing tools (unchanged)
| File (pin) | Role in the reserved flow | Change |
|---|---|---|
| producer v2 `colab_support.py` (2b720434…, 53892) | prepares both packets; `verify` is the full launch check (C04) | none |
| `handoff_check.py` (7d62dde4…, 27722) | `trusted` claims for the reserved rules | none |
| workflow pass02 `colab_workflow.py` (4a2ece9e…, 47247) | `open`, `attach`, `record-review`, `append-note`, `show` for the first pass; its N1NN `place-return` is **not** used for reserved returns | none; succeeded by pass03 for K1–K3 |
| `return_capture.py`, `return_inspect.py` | **not used** by the reserved flow (C01) | none |
| v1 producer, assembler, custody checker | reached through producer v2 | none |
| design05.05 and pass01 lab | history; superseded for review by this design | none |

## New, proposed
| Path | What | Depends on |
|---|---|---|
| `labs/colab-workflow-pass03/colab_workflow.py` (+ tests) | pass02 behaviour plus K1 `seal-return-local`, K2 `open-pass`, K3 transitions with the prefix rule; disposable books only | none of the reserved code; useful to ordinary N7NN-local returns too (06.07 D1) |
| `labs/colab-reserved-pass01/reserved_check.py` (+ tests) | `launch`, `stage`, `reconcile` with `--expect`; calls the pinned producer `verify` and `handoff_check`; reads the K3 record | workflow pass03 record format (K3); the pins above |

**Pins that move together if built:**
- `reserved_check` pins producer v2, `handoff_check` and workflow pass03.
- Workflow pass03 keeps pass02's producer pin.
- **A later producer v3 would move all three.**

## Downstream
- Ordinary Colab jobs: no change.
- Existing pages using N1NN placement: unchanged history.
- **Workflow `show` consumers:** the K3 transitions appear in the record. `review_pending` semantics are unchanged (0708 F03), so they should not be read as "no review owed".
