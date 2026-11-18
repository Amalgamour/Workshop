# Code path

pass02 `build_intake` stores `book` as `str(book)` after `book_dir` resolves the directory, and `instance_id` as sha256 of canonical `{"book", "pass", "source"}`. The store is `workbook-review/{page}/{pass}/` inside the book. A directory copy carries intake.json, journal.json, and the review record. The stored book string still names the source directory.

`source_changed` compares row maps of root, role, path, and sha256. Equal maps return false. It does not compare `book` or `instance_id`.

That function is the one reached by pass03, pass04, pass05, and the v7 door:

- prepare reports `stale`
- record refuses a repin when it returns true
- inspect and read/recover use `freshness`, which calls it
- publish blocks with `Publication is blocked because the selected source changed after intake.` when it returns true

The N7-local workbook adds a book comparison only when `live["kind"] == "N7NN"`. N5 falls through to the row map.

The successor replaces pass02 `source_changed` after loading pinned pass05. For N5NN with a stored intake, `n5_instance_hold` runs first. A hold returns true before row equality can clear it. `result` adds `instance_applicability` only for that hold. `perform` clears the hold at entry so an earlier command cannot leak into a later one.
