# First failures retained

These are the author-suite failures observed before the final passing run. The historical modules were not edited to remove them.

1. `n7-cycle` stopped with an empty `declared_submission`. The historical pointer cutter treated the fenced sample heading as the declaration. The candidate now reads the pointer between the one unfenced return-pointer heading and the one unfenced review heading when that structure is clear. Ambiguous structure keeps the historical cutter.
2. `malformed-and-mismatch` reported `ambiguous-submission` for a Submission line whose suffix was ` note`. That suffix is an accepted pass03 form. The fixture now uses an Artifact manifest line with a trailing ` note` beside a valid Returned line. The passing run reports `malformed-n7-declaration` and refuses the record.
3. `replay-0510` first reported measurement `incomplete` with `ambiguous-declared-root` on the submission and the manifest. The external copy and the helper root both held those relative paths. A page-only book then recorded 1 source, because prime_record keeps book-root rows. The candidate binds the book copy when the two files have equal bytes. Unequal bytes stay ambiguous. The passing replay recorded 44 sources.
4. `reporter` reported state `held` after the declared return file was appended. The declaration hash no longer matched, so the measurement was incomplete. The reporter maps an incomplete measurement to held. The stale case is now a task-body edit. That measurement stays complete and the report state is stale.

The final run exited 0 with `FAILED 0`.
