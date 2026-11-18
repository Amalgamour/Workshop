# Worker B, unit 1 findings (prima-0706-0502)

Hashes of the sources cited: pass01 report.py 72e9bda1...94cc, pass02 report.py d13d8d4f...852e, pass03 report.py 70028dfe...dfade, app/review_report_tools_v1.py 00489768...2c5c. Probe outputs are in probes/probe1.out. The probe extracts the named original functions by AST and executes only those (no module import, so pass01/pass02 module-level code never ran).

## B-01 Non-dict intake rows are silently dropped, and every count then reads "measured"
- **fact:** pass02 `artifacts_of` keeps only dict rows (`kept = [row_item(row) for row in raw_rows if isinstance(row, dict)]`). With 1 valid row plus 3 malformed rows ("garbage", 7, null), and measurement "complete", the report shows intake_roles count 1, addressed_sources 1/10 measured, content_blobs 1/10 measured, declared 1/10, rows kept 1. Nothing records that 3 rows were dropped. pass03's guard `if isinstance(row, dict) else None` -> REASON_ADDRESSED_MISSING (pass03 :97-100, :126-128) can never fire for a non-dict row, because rows are already filtered.
- **evidence:** labs/review-report-pass02/report.py:321-329 (sha256 d13d8d4f54d79cbdb22e1a40fdffb89bd26b85a611bf8620dc36854be9eb852e); labs/review-report-pass03/report.py:97-100, :126-128, :161 (70028dfe97bc6178a3497c814cf585476bb0b41650ce67fc79dd3d5b118dfade).
- **method:** probe P3. The functions that ran: pass03 artifacts_of, addressed_sources, content_blobs, _sizes, _measured, physical_files; pass02 artifacts_of, row_item, sum_bytes, integrity_of, unique_files, counter, sha_key.
- **severity and impact:** medium. An undercount presents as a complete measured total, so malformed intake metadata becomes invisible.
- **recommendation:** count the dropped rows and, when any row is not a dict, make the intake, addressed and content counters unknown with a reason (or report a dropped_rows field).
- **label:** verified (probe)

## B-02 A missing or null byte size gets a misleading reason, and the declared total still shows as declared
- **fact:** with one row whose bytes is null, addressed_sources and content_blobs say "rows of one addressed source do not agree on one int byte size" (and the content equivalent). No disagreement exists; the size is absent. In the same report the declared artifacts still show count 1 and bytes 10 "declared", taken from declared_bytes, while the measured bytes are unknown. A bool size (True) is treated the same way (P8).
- **evidence:** pass03 report.py:77-86 (_sizes), :41, :48 (REASON_*_SIZE), :107-111, :134-138; pass02 report.py:357-366.
- **method:** probes P2 and P8 (same functions as B-01).
- **severity and impact:** low. The reason text points a reader at a conflict that does not exist, so it is wrong evidence for triage.
- **test coverage:** `test_author_size_disagreement_and_boolean_bytes` (tests/test_report.py:401-422) checks bytes None for a bool size but does not assert the reason text.
- **recommendation:** tell "size missing or not int" apart from "sizes disagree" in _sizes, with separate reasons.
- **label:** verified (probe)

## B-03 Negative byte sizes are accepted as measured and declared totals
- **fact:** bytes = -10 with declared_bytes = -10 gives addressed, content, intake and declared bytes of -10, all states "measured" or "declared". The only check is `type(value) is int`.
- **evidence:** pass03 report.py:82; pass02 report.py:190, :198-199, :358, :362.
- **method:** probe P5.
- **severity and impact:** low to medium. Invalid metadata produces a plausible-looking total, and a negative row can cancel a real one so the sum looks normal.
- **recommendation:** require value >= 0, otherwise the state is unknown with a reason.
- **label:** verified (probe)

## B-04 An empty row list with measurement "complete" yields 0 declared artifacts, presented as "declared"
- **fact:** rows = [] and measurement "complete" give count 0 / bytes 0 with state "declared", scope "manifest-declared-artifact-entries" and provenance "declared", plus 0/0 measured addressed and content. `all()` over an empty artifact list makes declared_ready True. Relatedly (P9), intake rows with no role "artifact" also give declared 0/0. The "declared" figure is derived from declared_* fields on intake rows, not from a manifest count, so absent evidence is projected as "the manifest declares zero".
- **evidence:** pass02 report.py:327, :357-366, :297; pass03 report.py:112-115, :139-142.
- **method:** probes P4 and P9.
- **severity and impact:** medium. A missing artifact binding reads as a confirmed empty declaration. Scope note: the author test `test_author_null_measurement_and_empty_rows` (tests/test_report.py:366-385) deliberately expects addressed and content 0/0 for empty rows, so that part is intended. It does not assert the declared count or count_state, so the "declared 0" projection is untested.
- **recommendation:** do not set count_state "declared" when there are no artifact rows unless an independent manifest count of 0 is available; otherwise leave it unknown with a reason.
- **label:** verified (probe); "no independent manifest count is consulted" is inferred from reading artifacts_of only.

## B-05 Authority envelope fields are copied from the core unvalidated and survive an unstable or held cut
- **fact:** pass01 `apply_envelope` copies accepted, approved, authority, closes_work, releases_action and task_association from inspect verbatim, of any JSON type, and sets action_released = releases_action. pass02 `clear_judgment` resets only JUDGMENT_KEYS, which do not include those six fields or action_released. So `mark_unstable` (called at pass02 :599, :679, :717 and from `finish` :842-845) and `hold_mismatch` clear the judgment but leave authority, action_released and the rest from the moved cut, and the projection prints them (`authority:`, `action_released:` at pass02 :759-760). The probe showed authority "Director" and releases_action {"x":1} accepted and printed by `word()` as "Director" and "{'x': 1}". OBSERVATION_LIMIT promises only that judgment, attention and custody stay out on a change. It does not cover authority.
- **evidence:** pass01 report.py:28-35, :479-489, :733-741 (72e9bda15c5f3ca844350be5dae2fcfcf4e7c609c262b8f7e702d64467eb94cc); pass02 report.py:69-94, :477-499, :534-558, :605, :759-761, :836-846.
- **method:** probe P12 ran pass01 apply_envelope and word. The survival across mark_unstable is from reading the code, not a run (observe needs core subprocesses, which are not allowed).
- **severity and impact:** medium to high for authority projection. A held or unstable report can still show a non-null authority or action_released taken from a cut the reader itself rejected, and any string a core emits is shown as authority.
- **test coverage:** `test_author_finish_recheck_withholds_attention` (tests/test_report.py:499-517) checks that attention is withheld after a finish recheck, but asserts nothing about authority, action_released or the other envelope fields.
- **recommendation:** add the envelope keys and action_released to the keys reset on unstable or mismatch; type-check them (bool or None, or a fixed vocabulary) before projecting.
- **label:** verified (type passthrough, probe); inferred (survival through mark_unstable, by reading)

## B-06 "stale" is used for integrity failures, not just superseded history
- **fact:** pass02 sets stale = True when read and recover report "No recorded judgment" while inspect names a current id (:631-646), and when checked_record returns record-mismatch or digest-mismatch (:686-692). mark_unstable and hold_mismatch call clear_judgment(report, True), so stale = True on any moved cut too (:536, :551). In the readable path, stale comes only from core flags (:719). A missing or non-bool stale flag counts as not stale, so state is "readable" with exit 0.
- **evidence:** pass02 report.py:477-499, :536, :551, :634, :688, :719-721; pass01 report.py:573-574.
- **method:** read
- **severity and impact:** medium. A consumer cannot tell "superseded by newer history" from "record bytes do not match the journal" or "observation moved" using stale alone. In the readable path, null or invalid stale metadata defaults to fresh.
- **recommendation:** keep stale for supersession only and add a separate integrity or observation reason. In the readable path, if any core stale value is not a bool, report unknown rather than fresh.
- **label:** verified (read)

## B-07 Observation can report stable = true while the bound cut was unreadable
- **fact:** in the mismatch branches at pass02 :603, :607 and :649, stable is set from `recheck_why == "ok"` alone. If the first read_cut failed (bound None, bind_why "unreadable"/"bad") and the recheck succeeded, the observation says status "mismatch", stable true, bound null. Line :595 only flags movement when bind_why == "ok".
- **evidence:** pass02 report.py:573, :591, :595-608, :647-651.
- **method:** read
- **severity and impact:** low. The observation is internally incoherent: a cut that appeared mid-observation is reported as stable.
- **recommendation:** stable = True only if both bind_why and recheck_why are "ok"; otherwise None or False with "cut" in changed.
- **label:** verified (read)

## B-08 The brief calls the reader "accepted", but its own PRIME-USE says accepted: false
- **fact:** labs/review-report-pass03/PRIME-USE.md:3-4 reads "accepted: false / state: staged successor; no core edit". The app declaration's note (app/review-report-v1.json) says "Staged read-only connector for the accepted pass03 reporter".
- **evidence:** PRIME-USE.md:3-4; app/review-report-v1.json "_note" (5295f98fe22024524bf9059fee24c3a617da73ed3ed58deff8c726080c64445b).
- **method:** read
- **severity and impact:** low, but it matters for authority: the room carries contradictory acceptance statements.
- **recommendation:** Prima or the Director should confirm which statement is current. The PRIME-USE file may simply predate acceptance.
- **label:** verified (read); which one is current is unknown

## B-09 Uppercase sha256 makes content_blobs unknown while integrity can still match
- **fact:** with sha256 and declared_sha256 both uppercase, content_blobs is unknown ("lacks a 64-character lowercase sha256"), yet integrity_of counts the row as a hash match, because it compares the strings without format checks. Declared and addressed totals stay measured or declared.
- **evidence:** pass02 report.py:208-226; pass03 report.py:126-128.
- **method:** probe P6
- **severity and impact:** low. The hash_match counter accepts digests that the content counter rejects, which is an internal inconsistency.
- **test coverage:** `test_author_uppercase_hash_blocks_the_content_total` (tests/test_report.py:424-430) intends content to be unknown. It does not check hash_match.
- **recommendation:** apply sha_key in integrity_of too, and treat a malformed digest as not verified.
- **label:** verified (probe)

## B-10 Open questions I could not settle in this unit
- **fact:** (a) I did not run the end-to-end observe or finish paths (they need core subprocesses, which are not allowed), so B-05's survival claim and B-07 are from reading only. (b) I listed app/review_report_tools_v1.py's functions but did not audit its seating or launch logic (:317-376) in depth. (c) I did not check whether the core (workbook pass03) can actually emit a non-bool authority or stale value, which decides how reachable B-05 and B-06 are. (d) Under pass01 `same()`, NaN never equals itself, and json.loads accepts NaN by default. If a core ever emitted NaN in an envelope or instance_id field, the result would be a spurious mismatch. I did not determine whether the core can emit it.
- **evidence:** app/review_report_tools_v1.py (00489768c33874b282a3732709eb40503d0c3ebfad2826a9b3e8be6d832a5e2c); pass01 report.py:95-104, :179-192; probe P11 (same(nan, nan) is False).
- **method:** read; probe P11 for (d) only
- **severity and impact:** unknown
- **recommendation:** a follow-up unit with an approved fixture harness for observe, plus a read of the workbook core's emit schema.
- **label:** inferred / unknown
