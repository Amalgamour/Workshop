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
