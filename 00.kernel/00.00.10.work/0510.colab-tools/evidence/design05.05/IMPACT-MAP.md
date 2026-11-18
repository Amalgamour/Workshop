# IMPACT-MAP (proposed) — source and API impact of reserved two-pass support
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · state: design; from source reading of pack05.05 bytes and probe P1

## Existing tools: changed or not
| Existing file (pack pin) | Change in slice 1 | API used by the extension | Evidence |
|---|---|---|---|
| `labs/colab-support-pass02/colab_support.py` (producer v2) | **none** | `prepare`/`verify` as today; the descriptor is an ordinary `required_sources` entry; builder context is listed in `withheld` | A1; v1 `validate_request` 310–414 |
| `labs/colab-support-pass01/colab_support.py` (v1, loaded by v2) | **none** | `evaluator-overlap` logic is the model for the path-and-bytes overlap rule; not imported | A2, 410–412, 912–916 |
| `labs/colab-support-pass02/handoff_check.py` | **none** | `check --output --expected-digest --json` → `trusted.source_map`, `investigation`, `binding_sha256`, `envelope` hashes | A3; probe P1 exit 0 `valid` |
| `labs/colab-workflow-pass02/colab_workflow.py` | **none** | `open` (second pass slot), `attach`, `place-return`, `record-review` with route `request-next`; occupied-pass refusals | A4; 62–63, 1023, 1064–1083, 1101 |
| `labs/return-capture-pass01/return_capture.py`, `return_inspect.py` | **none** | capture, verify, inspect: sealing and origin of each stage's return | A5 |
| `labs/pack-assembly-pass01`, `labs/pack-custody-pass01` | **none** | reached only through the producer | — |
| 0411/01.003, exchange-layout-v2 CONTRACT | **none** | policy and naming | — |

## New, in slice 1
| New path | What |
|---|---|
| `labs/colab-reserved-pass01/reserved_check.py` | the read-only checker (CONTRACT §2–3), with pins of `handoff_check.py` and `return_inspect.py` |
| `labs/colab-reserved-pass01/tests/test_reserved_check.py` | ACCEPTANCE cases A–D on disposable fixtures |
| `labs/colab-reserved-pass01/README.md` | the operator steps (EXAMPLES §2) |
| `labs/colab-reserved-pass01/templates/` | text Prime pastes into `method`, so the reviewer emits the blocks (until the optional producer v3) |

**Pins the checker must hold:**
- `labs/colab-support-pass02/handoff_check.py` sha256 7d62dde48165c5ac80f7f92a2a91f73a66b40c1e8dd2383f0269027038c6a268, 27722 bytes (pack05.05).
- `labs/return-capture-pass01/return_inspect.py` (pack05.05 pin, 11402 bytes).
- A later handoff_check repair means a checker repin, nothing else.

## Downstream bindings to watch
- **Ordinary Colab packages, captures and workflow records:** no change and no migration. Ordinary passes never invoke the checker.
- **0511 workflow `show` and pass flags:** unaware of reserved records. The record is evidence beside the pass, not a flag (CONTRACT §1.4).
- **Optional producer v3:** would change the request, digest and handoff versions. Then handoff_check `/3`, the workflow `attach` verifier pin and this checker all move together. It is not in slice 1.
- **Grok-1 0708 audit:** not read. Where it finds an existing mechanism this map calls missing (or the reverse), Prime reconciles using CONTRACT §6 H1–H5.

## Not changed by design
No new address axis, face, tail, status store, gate, role, scheduler or model call. N7NN pass identity stays `05.NN`. The 05 and 06 tails are as agreed.
