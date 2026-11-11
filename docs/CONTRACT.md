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
