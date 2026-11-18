# C01–C05 change account and H1–H5 ledger
date: 2026-11-01 · who: claude-opus-5-5 (Claude)

## C01–C05: what changed from 05.05
| ID | Prime finding | Change | Evidence |
|---|---|---|---|
| C01 | N7NN custody regression (`--member 01NN`, two N1NN reservations) | **No N1NN for the reserved pair.** Returns are sealed page-locally by the missing connector K1. A later pass needs K2, and recorded order needs K3. Descriptor `/2` drops `member`/`receipt_sha256` and names the seal transition. The existing N1NN `place-return` is not the reserved route. Whether ordinary N7NN returns change route is flagged, not chosen (06.07 D1). | CONTRACT §1, §6; 06.07 S1–S5; tests `Stage.test_no_n1nn_member_anywhere`, the `WorkflowModel` cases |
| C02 | Hash dependency overstated as chronology; receipt equality not checked | **Four facts kept apart:** byte identity, seal identity, recorded order, declared exposure. The informed stage binds the first package digest, the seal seq and transition hash, the return bytes and the cut. Every result carries `not_proved` (wall clock, exposure time, wholesale rewrite outside the tool). The receipt is replaced by a seal transition that is checked (`first-not-sealed`), not just proposed. | CONTRACT §2; `Stage.test_valid` (`not_proved`), `test_descriptor_names_other_seal`, `test_chain_tamper`, `test_first_packet_digest_differs` |
| C03 | CRLF block rejected | **Parse view:** raw hashed, BOM recorded, lone CR refused, CRLF→LF for parsing only. Typed accessors throughout. The pass01 failure is preserved: re-observed in run 1 and run 2, P1 (`CRLF … missing-reserved-findings`); pass01 is unchanged. | CONTRACT §5; `ParseView`, `Types`, `Stage.test_crlf_first_return_end_to_end` |
| C04 | Standalone handoff valid has narrower coverage | **Launch needs** producer `verify` intact with no findings **and** handoff `valid`, both at the expected digest, with the same investigation. The pins are recomputed. A handoff valid alone refuses. | CONTRACT §3; `Verifier` cases |
| C05 | Ordinary result versus a requested reserved job | **`--expect` is required.** Reserved with no descriptor refuses; a descriptor in an ordinary job refuses. Ordinary jobs need not call the checker. | CONTRACT §4; `Mode` cases |

**Also incorporated:**
- 0708 F01: every execution gets a new exclusive run directory and nothing is deleted (`run_probe.py`; two runs kept).
- 0708 F03: the workflow `show` field `review_pending: false` with `review_recorded: false` is not "no review owed". Consumers of the reserved flow must read the K3 transitions, not that flag.
- 0708 Factfind 6: the producer reads committed blobs, so descriptors must be committed before preparation.

## H1–H5 ledger
| ID | Assumption | Status | Citation |
|---|---|---|---|
| H1 | `handoff_check` trusted `source_map` carries roles `target`/`required` | **exercised** | design05.05 probe P1 (exit 0, `valid`, roles present); Prime's 05.05 review; 0708 exercised the checker (valid, and the tamper case gave mismatch) |
| H2 | a JSON descriptor under `<page>/evidence/` packages as a required source | **source-inspected only; end-to-end unknown** | v1 `declared_path` (pass01 `colab_support.py` 204–215) accepts such a path. The producer reads committed blobs only (0708 Factfind 6, Blocked). No disposable repository was made here (scope) |
| H3 | the workflow attaches a second pass on the same page after `request-next` | **false by source inspection** | slots are created only in `fresh_record` (539–550); `open` refuses an existing page (759); `attach` refuses an unknown pass (811). Hence K2 |
| H4 | the inspector or N1 member route can seal an N7NN return | **superseded (not a legal route under C01)** | Prime's 05.05 review H4; workflow `command_place` is N1NN-only (964–1030). Hence K1 |
| H5 | reviewers emit the blocks reliably | **unknown (empirical); parser side corrected** | C03 parse view; format failures are coded and not findings. No model was run |

## Pass01 failures preserved
- pass01 code, examples and evidence are unchanged.
- Its CRLF rejection is re-observed in `runs/*/P1-pass01-crlf.stdout`.
- Its unhashable-type risk (`fid not in seen` with a list) is fixed in pass02 by the typed accessors (`Types.test_reconcile_finding_list_is_type_not_typeerror`). It was not edited in pass01.
- The `malformed-enum-list` TypeError in Prime's `checks.json` is Grok-2's constructor, not this lab.
