# Selection and rollback

Unselected. `app/librarian.py` stays `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes, loading `review_loop_tools_v7.py`.

The on-disk candidate loader is `labs/review-instance-binding-pass01/candidate/app/librarian.py`, `a0de0b4fbd935e65d061836794d1d11bb19c22932d080bb9ca06a56edd947561`, 12397 bytes. Its review-loop branch sets code_root to `D:\Git\lib-build` and loads `labs/review-instance-binding-pass01/review_loop_tools.py`.

## Minimum integration patch, not applied

When Prime composes one dispatcher, the review-loop load names the composed door, and that door's workbook pin names the composed workbook. The composed `source_changed` calls, in order:

1. `n5_instance_hold` from this workbook
2. the N7-local book check for kind N7NN
3. pass02 row comparison

Pass05 `parse_pointer` and `build_intake` stay in that chain for the strict N7 grammar. This pack does not write that composition.

## Rollback

Leave `app/librarian.py` at the hash above. Leave the lab files on disk, inert. No migration of stored intakes is required, because the hold is a read-time comparison and does not rewrite intake.json.
