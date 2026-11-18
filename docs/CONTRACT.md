# Lane contract (Prima, 2026-11-11) — shared by all build lanes

Spec in docs/spec governs. Where this contract and the spec disagree, the spec wins; record it in BUILD-LOG as a finding.

## Book file
JSON Lines, per spec/format.md section 3. Line 1 header `{"seqbook":1,"address":"DD.SS.BB"}`. Each later line:
`{"n":int,"at":ISO8601 UTC,"by":string,"op":"put"|"tail"|"snapshot"|..., "addr":full face address, "tail"?:string, "from"?:string, "to"?:string, "body"?:markdown, "proposal"?:id}`
Book files live in `books/` named `DD.SS.BB.book`. Kernel: `books/00.00.00.book`.

## Compute HTTP API (default http://127.0.0.1:7700, JSON)
- GET  /health                         -> {"ok":true,"books":n}
- GET  /books                          -> [{"address","title","pages":n}]
- GET  /book/{DD.SS.BB}                -> {"address","title","pages":[{"page":"PPPP","title","faces":["01","04",...]}]}
- GET  /page/{DD.SS.BB.PPPP}           -> {"address","title","faces":{"01":{"body","tail"?,"source":addr},...},"inherited":[addr...]}
- GET  /face/{full face address}       -> {"address","body","tail"?,"source":addr,"resolved_from":"local"|"kernel"|"missing"}
- GET  /resolve/{address}              -> resolution trace: [{"step","checked":addr,"found":bool}]  (inheritance: local face wins, else go up to kernel at same page.face; missing stays missing)
- GET  /history/{address}              -> [log entries touching it]
- GET  /links/{page address}           -> {"forward":[addr],"back":[addr],"missing":[addr]}  (face 08 + derived)
- GET  /brands?q=word                  -> [{"word","brand":addr,"title","why"}]  (special-word lookup, spec/brands.md)
- GET  /cards?title=...                -> cards matched by title across faces
- POST /propose  {"by","ops":[...]}    -> {"status":"approved"|"rejected","reasons":[...],"entries":[n...]}  (all-or-nothing)
- GET  /queue                          -> recent proposals with status and reasons
Errors: {"error":code,"detail"}. Missing is a 404 with {"error":"missing","axiom":"7"}; two live claims is 409 {"error":"conflict","axiom":"1"}.

## Repo rules
- Commit often in /workspace/workshop-build/repo on branch `build`; every commit message ends with a blank line then `Model: Grok Bot (Prima)`.
- Only touch your lane's folders plus append-only lines in docs/BUILD-LOG.md (prefix your lane tag).
- Never push anywhere. No network installs beyond crates.io / npm registry.
- Never invent a rule the spec doesn't give: mark it `7` in BUILD-LOG ("spec silent; chose X provisionally because Y") and keep it isolated/configurable.

## Addendum (SEQPAGE lane, 2026-11-11): .seq page routes, proposed for COMPUTE
Per R3 the book is the real copy and a `.seq` file is a view; import is a proposal. Layout: docs/spec/seqpage.md. Library: `crates/seqpage` (`seqpage::export`, `seqpage::import`, `seqpage::check_text`).
- GET  /page.seq?addr=DD.SS.BB.PPPP    -> `text/plain; charset=us-ascii` body = `seqpage::export(&book_log, page)`; header `Content-Disposition: attachment; filename="<seqpage::file_name>"`. 404 `{"error":"missing","axiom":"7"}` when the page has no entries. 422 `{"error":"invalid","rule":"R4",...}` when a book entry is not plain ASCII.
- POST /propose  with `Content-Type: text/x-seqpage` (body = a .seq file; `by` from the `by` query parameter or the session) -> `seqpage::import(text, Some(&book_log), by)`; on error 422 with the Report `{"ok":false,"errors":[{"line","code","axiom","rule","detail"}],"findings":[...]}`; on success its `proposal` goes through the normal queue and the response is the usual `{"status","reasons","entries"}` plus `"findings"` from the import. JSON bodies to /propose are unchanged.
- POST /check.seq (optional) -> the Report from `seqpage::check_text(text, filename, Some(&book_log))`, writes nothing.
Error axioms used by the Report: 7 missing, 7.8 broken pointer to the book, 1 conflict/authority, 6 lineage (past rewritten), 8 connection. Status codes: missing 404, conflict 409, others 422 (match SeqError::http_status).

## Addendum (COMPUTE lane, 2026-11-11): identity, /ask, /ask/link, /close; .seq routes wired
Identity (provisional, 7 in BUILD-LOG until the Director confirms):
- Every write (POST /propose, /ask/link, /close) carries `Authorization: Bearer TOKEN` (or `X-Seq-Token: TOKEN`). Tokens live in `books/.identities` (gitignored; `NAME TOKEN` per line, `#` comments; scripts/dev.sh makes it if missing). The compute sets `by` from the token; a body's `by` is ignored. No token or an unknown token -> 401 `{"error":"identity"}`; the `compute` name is internal and refused 403. Names are exact: lowercase letters, digits, hyphens.
- Writes need `Content-Type: application/json` (or `text/x-seqpage` on /propose); anything else is 415. No CORS headers are sent. The compute refuses a non-loopback `--listen` unless `--allow-remote`.
- Seating a face, on any path (put, promote, tail draft->bare), needs `approved_by`: `director` (only from the director token) or `build-stage (R2)` with `trial: docs/trial/NAME.md[#anchor]` naming an existing file whose author (first `Lane NAME` / `author: NAME` line) is not the face's maker. Checked before the core: refusal is 403 `{"error":"authority","axiom":"1","reasons":[{"rule":"R2",...}]}`. Core rule failures stay 422; conflict and elevate are 409; missing 404; a malformed address is 400 everywhere.
- `queue_id`s persist across restarts (`books/.queue`, JSONL).
- GET /page/{addr} gains `"boards":{"FF":[{"counter":"NN","tail"}]}`; no `FF.00` face key (R9). Draft faces carry `"state":"draft"` and `"why_draft"` (R5).
- (FOLLOWUPS, 2026-11-11) `why_draft` on GET /page/{addr} carries `"reason"` when the entry that opened the draft has a `reason` field (R5 follow-up "why is it a draft?"), the same value GET /face gives (`DraftWhy.reason`, seqaddr-core API.md). No reason on the entry: the key is absent. Full shape: `{"opened_by_entry":n, "reason"?:string, "has_seated":bool, "open_notes":[{"n","by","text"}], "merged_notes":n}`.
- (FOLLOWUPS, 2026-11-11) GET /whoami (a read that needs a token) -> 200 `{"name":string, "director":bool}` for the request's `Authorization: Bearer TOKEN` (or `X-Seq-Token`), the same check a write uses: no token or an unknown token 401 `{"error":"identity","axiom":"1"}`, the internal `compute` name 403 `{"error":"authority","axiom":"1"}`. The token and the identities file contents are never echoed. 7: the identity design itself is still provisional.

Routes:
- POST /ask `{"prompt":string, "book"?:"DD.SS.BB"}` (a read; no token) -> 200 `{"heard":[{"text","norm","kind":"key"|"link"|"question"}], "ranked":[...], "threshold", "formula", "books":[...], "pieces":[{"address":card addr, "card":{"address","title","key","fields","body","state","source","resolved_from"}, "matched":[word], "score":0..1, "why":string, "via":{"kind":"question"|"brand","address","title","phrasing"}}]}` with 1-3 pieces, or `..., "probe":{"question":string, "near":[...]}}` when nothing reaches the threshold. Non-ASCII prompt -> 422 `{"error":"invalid","rule":"R4"}`. With no `book`, the compute's `--book` chain is read, else the kernel only.
- POST /ask/link `{"question":"DD.SS.BB.PPPP.FF.key", "phrasing":string}` (write) -> through the queue as copy (if seated) + note + merge on the question's draft; response is the usual propose answer plus `"linked"`. Already a phrasing -> 409; not a question card -> 404; non-ASCII -> 422 R4.
- POST /close `{"addr":counter address, "outcome":"passed"|"failed"|"blocked"|"needs-authority"}` (write) -> the compute closes a review for the counter's reviewer only (403 for anyone else). 7: route name and shape are the compute's choice.
- GET /page.seq?addr=, POST /propose with `text/x-seqpage`, POST /check.seq: as in the SEQPAGE addendum; `by` comes from the token. The import's findings are returned as `"seq_findings"` (the core's `"findings"` keep their name).

## Addendum (COMPUTE lane, 2026-11-18): delivery ids on POST /propose

A write sent twice is booked once (R37 item 2, K4). Auth runs first, then the delivery id is checked, then this writer's receipt, then the write rules (`crates/compute/src/lib.rs:191-194`, `crates/compute/src/store.rs:748-755`). `seqaddr-core` stores the id; it does not enforce write-once.

- Field name and where it goes: optional `delivery_id` on each op in the JSON body of `POST /propose` (`seqaddr-core` `OpRequest`; serde also accepts `delivery-id`). The compute stores it on the booked book line as `delivery_id` (`crates/seqaddr-core/src/validate.rs:229-230`, `crates/seqaddr-core/src/log.rs:177-179`). An empty or whitespace-only value is treated as no id (`crates/compute/src/store.rs:1030`). Pinned by `crates/compute/tests/delivery.rs:24` (`delivery_id_retry_writes_once_and_no_id_behaves_as_today`; the book line at `:50`).
- Per-writer scope: ids are per writer. The same id from another writer is a new write, not a replay (`crates/compute/src/store.rs:1130-1131`, the index key is `(writer, id)`). Pinned by `crates/compute/tests/delivery.rs:150` (`another_writers_same_id_is_not_a_replay`).
- Limits (400): a delivery id longer than 128 characters, or holding a control character (including a newline or a tab), is refused with 400; 128 characters is accepted. Mixed delivery ids in one proposal, or an id on some ops and none on others, are refused with 400. Nothing is booked (`crates/compute/src/store.rs:1025-1048`, `delivery_request_error`). Pinned by `crates/compute/tests/delivery.rs:172` (`refuse_long_or_control_or_mixed_delivery_ids`) and `:292` (`partial_delivery_ids_are_refused`). A proposal with no ids at all is booked as before.
- Replay (200): the same writer, same id, and same content returns the first answer and writes nothing (`+0`) (`crates/compute/src/store.rs:1132-1134`). In the same session the body is the original body (`crates/compute/tests/delivery.rs:24`). After a restart the replay is 200 with the original `book`, `status` and `entries` (`crates/compute/tests/delivery.rs:59`, `lost_reply_survives_restart`). `queue_id` comes back from `.queue` when a matching approved record is found (`crates/compute/src/store.rs:1108-1123` and `:1192-1195`; `crates/compute/tests/delivery.rs:328`, `queue_id_comes_back_after_restart`). `findings` comes back as `[]` after a restart: they are worked out against the world at write time and are stored nowhere on disk (`crates/compute/src/store.rs:1193`; `delivery.rs:342`). If no `.queue` record matches, `queue_id` is missing (7).
- Other content (409): the same writer and id with other content is refused with 409 `{"error":"conflict","rule":"K4"}`. The answer names `first_fingerprint` (64-character lowercase hex SHA-256 of the first proposal's content) and `first_book`. Nothing is booked (`crates/compute/src/store.rs:1136-1141`). How the fingerprint is made: SHA-256 of the JSON array of the ops with the `delivery_id` field removed; object keys are sorted (`serde_json`'s default map). Request layout, key order and escapes do not change it; a change to a field value (including body whitespace) does (`crates/compute/src/store.rs:1068-1085`, `crates/compute/src/sha256.rs`). Pinned by `crates/compute/tests/delivery.rs:212` (`other_content_same_id_is_refused_before_and_after_restart`).
- Refused answers are not remembered: a non-200 answer does not occupy the id; a later good write with that id is booked (`crates/compute/src/store.rs:761-763`, `remember_delivery` only when `code == 200`). Pinned by `crates/compute/tests/delivery.rs:310` (`refused_answer_leaves_the_id_free`).
- Auth first: a missing or unknown token is 401 `{"error":"identity"}`, not a replay, and writes nothing (`crates/compute/src/lib.rs:191-194`, `who` before the write). Pinned by `crates/compute/tests/delivery.rs:123` (`resend_with_wrong_or_missing_token_is_auth_refusal_not_replay`).

Pinned status codes: 400 for a bad or mixed delivery id; 409 for the same id with other content; 200 for a replay of the same content.

## Addendum (COMPUTE lane, 2026-11-18): delivery ids, 05.05 corrections

Corrections and client gaps for the addendum above. That 2026-11-18 addendum was not rewritten. Cites below replace the stale ones in it: auth is `crates/compute/src/lib.rs:190-193` (not :191-194); `findings` after a restart is `crates/compute/src/store.rs:1192` (not :1193); the findings test line is `crates/compute/tests/delivery.rs:343` (not :342).

- Non-ASCII: a delivery id holding a non-ASCII character (for example `é`) is refused with 422, rule `R4`, after the 400 shape checks. Control characters (newline, tab, DEL) are still 400. (`crates/seqaddr-core/src/validate.rs:183`, `crates/compute/src/store.rs:914-919`).
- Ids are trimmed and case-sensitive: leading and trailing whitespace is stripped before the id is used (`crates/compute/src/store.rs:1030`, `:1056`, `:1179`); `Id` and `id` are different ids (no case folding).
- 409 and 400 carry no `queue_id` and are not written to `.queue` (the id checks and the 409 return before a queue id is issued, `crates/compute/src/store.rs:750-755` and `:761`).
- 400 body shape: `{"status":"rejected","error":"invalid","detail":...,"reasons":[],"entries":[]}`. The `detail` is `delivery id must be 1-128 characters with no control characters` for length or control characters; `every op in a proposal must carry the same delivery id` for mixed ids; `every op in a proposal must carry the same delivery id (some ops have none)` when some ops have an id and others have none (`crates/compute/src/store.rs:1025-1048`).
- What to do on 409: do not resend the other content; the first write stands. To book new content, send a new delivery id. To get the first answer, resend the same content with the same id (`crates/compute/src/store.rs:1136-1141`; test `crates/compute/tests/delivery.rs:212`).
- Auth first: a missing or unknown token is 401 `{"error":"identity"}`, not a replay (`crates/compute/src/lib.rs:190-193`). 128 characters is accepted; 129 is refused with 400.

Pinned status codes: 400 for a bad or mixed delivery id; 409 for the same id with other content; 200 for a replay of the same content.
