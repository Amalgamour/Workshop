# Invalid and held behavior - 0512.prime-review/05.09

accepted: false
contract: review-report-hardening/1

This file records the locked behavior. The wording authority is evidence/build05.09/CONTRACT.md.

When the current cut is rejected, these fields become JSON null: accepted, action_released, approved, authority, closes_work, releases_action, task_association. envelope_withheld records cause, fields, provenance withheld-current-cut, and the reason that unknown is distinct from false. Those values are withheld as a current authority or action state.

The withheld paths are observation status unstable, observation status mismatch, and an unreadable or bad cut other than the not-recorded case. The kept paths are a coherent readable observation, a coherent historical stale observation, a not-recorded page whose journal is absent, and a coherent hold that exists only because no judgment is recorded while the cut itself is stable. On that not-recorded page the observation status is unreadable and stable stays null. The validated advisory envelope remains.

Historical judgment values that differ from a fresh base report are copied to historical_supplied, provenance historical-supplied, before the current judgment is cleared. That object is absent when no such values were supplied.

A non-dict intake row is retained. invalid_rows.count is the retained count, invalid_rows.dropped is false, and raw_rows keeps the source list. Affected counts, byte totals, and hash totals become unknown. measurement_withheld says the core measurement word is not a complete measured total. A verified empty list with measurement complete may report count 0. Absent or non-list rows stay count null.

A null or missing size uses the reason that a row omits a byte size and that this is distinct from two int sizes in conflict. A bool size and a negative size use the reason that a negative or bool size is not a valid measurement, and the byte totals are cleared. Two different non-negative int sizes keep the existing conflict reason, and size_observation is absent on that path. A content hash is a 64-character lowercase sha256. Other strings stay as written and count as not_verified.

Historical staleness is state stale, observation coherent, stale true, with the validated envelope still projected. An integrity failure is state held, observation mismatch, stale true, with the envelope withheld. Movement during the observation is state held, observation unstable, stale true, with the envelope withheld. stable true requires both the bound cut and the recheck to be readable objects. Two unreadable reads leave stable null. One unreadable side is stable false and the changed list includes cut. A missing or non-bool core stale flag stays as supplied.
