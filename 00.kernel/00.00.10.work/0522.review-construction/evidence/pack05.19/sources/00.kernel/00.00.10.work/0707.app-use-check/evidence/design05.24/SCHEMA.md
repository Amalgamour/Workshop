# SCHEMA — explicit candidate identity for the test equipment (0707/05.24; contract 0420/06.57)
Reader: `labs/freshness-boundary-tests-pass02/identity.py`. It is used by `freshness-boundary-tests-pass02/run.py` and `loop-convergence-harness-pass03/harness.py`.

## `harness-inputs/3`
It is `harness-inputs/2` (dependencies, fixture_source, judgments: unchanged rules from pass02 `inputs_check.py`) with this candidate block:

| Field | Rule |
|---|---|
| `schema` | `"candidate-identity/1"` (anything else refuses) |
| `name`, `kind` | non-empty strings. **C4 runs only when `kind` is `"combined"`.** |
| `entry` | exactly `"app/librarian.py"`, and a declared file |
| `workbook_entry` | a declared file; exactly one file carries role `workbook`. **The execution proof must show it runs.** |
| `open_entry` | null, or a declared file with role `open`, or equal to `workbook_entry`. It must exit 0 on a new root and be proved loaded. |
| `reporter_entry` | null, or a declared file with role `reporter` (or equal to `workbook_entry`); proved executed by `review-report`. |
| `candidate_json_sha256` | sha256 of the root's CANDIDATE.json |
| `files[]` | `{path, sha256, bytes, role}`. Role is one of entry, workbook, open, reporter, dependency, adapter, declaration, data. Unique paths. |
| `lab_differences` | a list of `{path, differs}`. Production-proposal bytes and lab adapter bytes stay separately named. |
| `builder` (optional; pass03 RC-1) | `{path, sha256, bytes, args[]}`, a frozen builder under the live repo, run as `builder args… --root NEW`. **Absent means RC-1 fails** (a new candidate must be reconstructible). |

**Paths are untrusted:**
- relative POSIX;
- no `..`, `.`, empty segment, drive letter, backslash or leading `/`;
- the resolved file must stay inside the root;
- a regular non-link file;
- hash and length must match.

**The root must be outside the live repo.** A PENDING candidate refuses (fbt) or stays all-blocked (pass03).

## Execution proof (before any case)
1. **Three runs of a fixed probe at the SAME absolute path, each from a fresh copy of the root:** control, control, and a copy with `raise SystemExit('LAB-TAMPER-<nonce>')` **prepended** to the target. Each finished room is renamed aside, never deleted.
2. **The probes:**
   - workbook: `entry review-loop prepare` on a tiny N5 fixture;
   - open: `open_entry open` on a tiny N7 pack;
   - reporter: `entry review-report`.
3. **Verdicts:**
   - **executed:** the two controls agree and the tamper differs;
   - **DECOY:** the tamper is identical to the controls;
   - **INCONCLUSIVE:** the controls disagree.
   - **Only `executed` passes the gate.** Anything else refuses (exit 2).
4. **Evidence class, recorded honestly:**
   - `executed` (the nonce surfaced);
   - `loaded` (compile broke);
   - `checked` (a refusal naming the target, e.g. a pin check: a check of the bytes, not proof they run);
   - `changed`.
5. **Other `dependency` files can be traced the same way.** An unused one is flagged (it does not refuse), because a candidate root legitimately carries unused files.

## Backward compatibility (legacy, labelled)
- **`harness-inputs/2` is read ONLY for the two frozen baselines,** keyed by CANDIDATE.json sha256:
  - proto-l `172ec4e9…`;
  - staged-g `062a3c8d…`.
- **Their workbook is found by the old `review_loop_tools_vN.py` rule, labelled `legacy-discovery`,** and it still passes through the same execution proof.
- **Any other v2 input refuses with its real reasons.** For Prime's old combined identity, those are: "only for the two frozen baselines", "open_entry … is not a declared file", "no workbook_entry is declared".
- **Old manifests are never migrated, repinned or edited.**

## What did NOT change
| Equipment | Preserved |
|---|---|
| Freshness | 34 cases / 32 required (F1, F1b, E1, E2 and C4 included), cases, judges and expectations: the pinned pass01 `run.py` and `judges.py` |
| Convergence | 40 cases / 37 required, ids, requirements, needs, judges, verdict and inputs_check: pinned pass02. Only CTX-1 and RC-1 sources differ (identity), and RP-2 reaches its workbook through `selected_workbook()` |

- **A subset is still diagnostic** (exit 4 or 1, never ready).
- **not-reached, blocked and deferred never count as pass.**
