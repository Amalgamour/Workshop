# Prime review — 0504.app-entry/05.20

Date:2026-10-29. Reviewer:Codex Prime.

Accepted within the existing capture-handoff backend scope. Prime independently ran the app handoff suite:6 passes,15 expected refusals,1 file-symlink privilege skip,0 failures. Existing app-entry suite:12 passes,46 expected refusals,1 privilege skip,0 failures. Tests ran in a disposable checkout, not the live book. Complete capture matches backend semantics (timestamp-derived hashes differ between separate successful captures); identical readonly repeat is byte-identical. Changed bindings/payloads refuse without replacing custody. Partial handoff remains attention, unknown child exit is not success, and no automatic retry/outer timeout was added. New door uses four fixed backend pins. Fresh0149 verification passes. The app now exposes capture-return --binding ABS; it does not reserve, queue, claim, deliver a worker or approve work. No general exactly-once or OS-sandbox guarantee is implied.
