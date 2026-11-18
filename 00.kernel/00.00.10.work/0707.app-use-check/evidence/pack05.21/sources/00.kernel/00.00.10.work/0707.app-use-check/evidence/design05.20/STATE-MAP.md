# Dependency and state map (0707/05.20)

## Where N1 is real and where it is only a label (current code)
| Location | Effect on N7 | Kind |
|---|---|---|
| `pass02.build_intake`: `lookup_custody` → `custody`, finding `custody-missing` | always `missing` on Colab N7 | **label.** The overlay replaces it with `n1-not-applicable` and adds `exchange.n1_custody` |
| `pass02.do_record`: `attempt_cycle` only if `custody == complete-descriptor` | the cycle never runs for N7-local | **real gate.** Correctly unused on this route |
| `pass02.do_record`: record `custody` = `missing` unless committed | stored and rendered as `custody: missing` | **label.** Production change proposed (CONTRACT) |
| `pass02.do_publish` | creates an absent N7 destination from a preliminary record | none. **This IS the local first-review route** |
| `0521` successor `do_publish`: refuses an absent N7 target for a preliminary record | would block every N7-local first review | **conflicts with the Director's route.** Must not be carried onto the N7-local route |

## Prototype chain (lab roots)
```
<root>/app/librarian.py (05.18 v8 candidate dispatcher)
  -> app/review_loop_tools_v8.py (production door bytes 0335da32…)
     validates app/review-loop-v8.json = LAB declaration ddbf3c0f… (workbook -> overlay)
  -> labs/n7-local-lifecycle-pass01/workbook.py (overlay, lab bytes 94aed777…)
     -> labs/workbook-review-pass04/workbook.py (05.18 lab adapter c6be0b97…)
        -> pass03 (9e66d7e4…) -> pass02 -> pass01 (imported from the live constants, hash-checked)
```

**Overlay functions:**
- `build_intake` (N7 only);
- `source_changed` (N7 only; otherwise the base function);
- `result` (adds `exchange` only when the intake has one);
- `open` (CLI).

## Composition with the other lanes (one chain)
| Lane | Composition |
|---|---|
| **G**, strict N7 grammar (Grok-2, pending) | The overlay reads only the parsed result (`submission` rows and finding codes), so it composes over G exactly as over pass04. G's blocking of malformed lines makes the intake incomplete before the exchange check. |
| **K**, capacity (Grok-1, pending) | independent: record validation only |
| **F**, 0521 first-target | Its cycle-render creation applies only where a cycle runs (custody). **On the N7-local route no cycle runs, so the local first review is the preliminary publish.** F's preliminary-publish REFUSAL must not be carried onto this route. Whether F stays for any route is a Prime integration choice. |
| **R**, reporter | It must observe through the same chain (overlay included). Otherwise it reports stale for matched exchanges (05.19 X7). **A dispatcher re-hash does not solve this.** |

## Write destinations (all inspectable)
| Command | Writes (book-relative) |
|---|---|
| prepare, form, inspect, read, recover | none (T1: tree hashes equal around the read/recover sequence) |
| record | `workbook-review/<page>/<pass>/intake.json`, `journal.json`, `reviews/<id>/{judgment.json,record.json,rendered.md}`; refused → `failed/<id>.json` + `.correction.txt` |
| publish | `<page>/06.NN.review.md` (create only if absent at publish), journal publication fields |
| open | `workbook-review/<page>/<pass>/exchange-open.json` (exclusive) |
