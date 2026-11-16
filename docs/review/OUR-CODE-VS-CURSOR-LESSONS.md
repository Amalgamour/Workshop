# Our code against the Cursor lessons

A review by Tester. Not a ruling. It checks our code at 2de94ff
(branch build) against docs/review/CURSOR-BUILD-REVIEW.md lessons
L1-L7 (lines 181-188). Focus: L2, L4, L6. L3 in passing.

The repo HEAD moved to cad88d0 while I worked. The two new commits
touch only docs/design/SEQ-FILE-PLAN.md, so the code is the same.

All runs were in a clone at /tmp/ourcode. Scratch books were in
/tmp/scratchbooks and /tmp/l3 (copies of books/*.book). The real
books/ and the repo were not touched. Servers were stopped after.

## Results

- L2 one gate: FAIL. The kernel builder writes books/ whole, with no
  compute gate. A real run erased 8 lines the compute had written.
- L4 copied text: FAIL (notes only). A 04 that repeats 01 gets a
  "finding" but is accepted, and even seated. A why reused on two
  cards gets nothing.
- L6 open door: PASS for writes. No CORS header, loopback bind,
  token needed, text/plain and form posts refused (415). Gap: the
  Host header is not checked, so reads are open to DNS rebinding.
- L3 clocks: PARTLY. The compute uses the system clock and ignores a
  typed `at`. But nothing refuses a time earlier than the line above,
  and the builder stamps a fixed typed time.

## L2 evidence: who writes book or face bytes

Gated path (the compute):
- crates/compute/src/store.rs:917-963 append after core validate.
- store.rs:927 log::file::create makes a new book file (gated).
- store.rs:746 appends `.queue` records (not a book).
- app/app/api/post/[...path]/route.ts:5 passes only propose, ask,
  ask/link, close, check.seq to the compute. The app never writes.

Ungated paths:
- kernel/build.mjs:846 `else writeFileSync(out, text);`
  Writes every books/*.book and books/00.00.axioms.jsonl whole,
  from kernel/ Markdown (OUT at :29). It uses its own checks, not
  seqaddr-core validate. n restarts at 1 on each run.
- kernel/00.00.00/*.md, kernel/00.00.axioms/*.md, kernel/samples/*:
  the face bytes the builder reads. Edited by hand or by agents.
  No git hooks are installed (.git/hooks has only *.sample).
- crates/seqpage/src/bin/seqpage.rs:72 writes a .seq page export to
  --out or --dir. A view today; under R26 it would be stored form.

Not books/ (test or mock only):
- app/mock/make-fixtures.mjs:23 writes app/mock/fixtures/*.book.
- crates/trial-compute/src/lib.rs:49 and :74 write temp test books.
- kernel/build.test.mjs:23 and :251 use mkdtempSync temp dirs.
- crates/seqaddr-core/src/log.rs:394-459 file functions. No non-test
  caller except the compute (create, append).

Real run: the builder erases gated writes.
1. The compute (see L4) approved entries 16-23 into
   /tmp/scratchbooks/10.11.21.book.
2. I copied that file into /tmp/ourcode/books/ and ran the builder.

    $ wc -l books/10.11.21.book
    24 books/10.11.21.book
    $ node kernel/build.mjs ; echo exit $?
    wrote  books/00.00.00.book  50 entries
    wrote  books/00.00.axioms.jsonl  7 entries
    wrote  books/10.00.00.book  1 entries
    wrote  books/10.11.00.book  1 entries
    wrote  books/10.11.21.book  15 entries
    exit 0
    $ wc -l books/10.11.21.book
    16 books/10.11.21.book
    $ grep -c '"by":"agent-1"' books/10.11.21.book
    0

No warning, exit 0. The 8 compute lines are gone. So there are two
writers to books/, and the builder wins. `--check` (:845) only
compares; it does not write.

## L4 evidence: copied text

The check: crates/seqaddr-core/src/validate.rs:440-441.

    if f == 1 && !w.body.trim().is_empty()
        && w.body.trim() == c.body.trim() {
        findings.push(Reason::finding("C3.2", ... "copies the 01 body"

It is a finding (a note), not a refusal. It is exact match after
trim, and face 01 only (a 04 copying 02 is not looked at). Nothing
compares one why with another, or a why with the 01 body. The builder
has the same note at kernel/build.mjs:703. The builder's checkWhy
(:724-738) wants each kernel why to BE a copy of a cited spec line.

Run 1. Server on 127.0.0.1:7791. Token agent-1. Page 10.11.21.0077,
drafts 00, 01, 04. Face 04 = face 01, word for word, no why line.

    HTTP/1.1 422 Unprocessable Entity
    "detail":"page 0077: 04 card `kettle` needs a `why:` line",
    "findings":[{"code":"finding","detail":"page 0077: 04 card
    `kettle` copies the 01 body","rule":"C3.2"}],
    "status":"rejected"

Refused only for the missing why. The copy is a note.

Run 2. Same page, two cards. Each 04 body repeats its 01 body. Both
cards use the same why, which is also the kettle 01 body:
"why: Boil water for tea."

    HTTP/1.1 200 OK
    "entries":[16,17,18],
    "findings":[{... "04 card `kettle` copies the 01 body"},
                {... "04 card `mug` copies the 01 body"}],
    "reasons":[],"status":"approved"

Run 3. Director token promotes all three drafts.

    "entries":[19,20,21], same two findings, "status":"approved"
    GET /face/10.11.21.0077.04 -> "state":"seated","by":"director"

So a copied 04 and a reused why can be seated. Cursor's gap (#10:
"gate ignores copied-why findings") is our gap too.

## L6 evidence: open door

Bind: crates/compute/src/main.rs:37-41. A non-loopback --listen
exits 2 unless --allow-remote. Default 127.0.0.1:7700 (:11).
Seen: `LISTEN 127.0.0.1:7791 ... compute`.

CORS: lib.rs:9 says "No CORS headers". rg for Access-Control in
crates/compute finds none. Tokens: lib.rs:86-97 (Bearer or
X-Seq-Token), names from <first books dir>/.identities.
Media: lib.rs:104-111, check at :185-188 for /propose.

All curls sent `Origin: http://evil.example`.

    OPTIONS /propose (preflight, POST, authorization,content-type)
    HTTP/1.1 405 Method Not Allowed
    allow: POST
    (no access-control-* header)

    POST /propose, application/json, no token
    HTTP/1.1 401 Unauthorized
    {"detail":"every write carries `Authorization: Bearer TOKEN`
    ...","error":"identity","status":"rejected"}

    POST /propose, text/plain, no token        -> 415
    POST /propose, text/plain, with token      -> 415
    POST /propose, form-urlencoded             -> 415
    {"detail":"send Content-Type application/json or text/x-seqpage
    (a cross-site form or text/plain post is refused)", ...}
    POST ask, ask/link, close, check.seq, text/plain -> 415 each

    GET /health with Origin -> 200, no access-control-* header.

So a page on another site cannot write: a simple post is refused
by type, and a JSON post needs a preflight the server does not grant.
It also has no token.

Gaps:
- Host is not checked. `curl -H 'Host: evil.example:7791' /health`
  gave 200 OK. DNS rebinding could read open GETs (books, faces).
  It still cannot write without a token.
- app route.ts:11 sets content-type to application/json when the
  request has none. A no-cors fetch with an untyped Blob sends none.
  Still 401 without a token. Not run live (app not started).
- app/mock/server.mjs:241 sends ACAO *. Mock server only.

## L3 evidence: clocks

Compute: store.rs:737 `let at = log::now_utc();` (system clock,
log.rs:246-247). store.rs:731-734 sets `by` from the token.

Run: propose with `"at":"2020-01-01T00:00:00Z","n":3,"by":"director"`
in the op, agent-1 token.

    {"entries":[22,23],"status":"approved"}
    {"n":22,"at":"2026-11-16T16:55:49Z","by":"agent-1", ...}

Typed at, n and by were ignored, silently (no note).

Earlier time: log.rs:196 check_timestamp checks shape only. The read
loop (log.rs:284-297) checks n order, not time order. Run: in
/tmp/l3 I set entry 23 to 2020-01-01T00:00:00Z (earlier than 22).

    $ seqaddr replay /tmp/l3/10.11.21.book  -> "entries": 23, ok
    compute --books /tmp/l3 on :7792 /health -> "ok":true,
    "refused":[]

Not refused anywhere. The builder uses a typed time for every line:
kernel/build.mjs:33 `const AT = '2026-11-11T19:30:00Z';` and
app/mock/make-fixtures.mjs uses a typed start clock.

## Top findings

1. Two writers to books/. The builder rewrites whole books and
   silently drops compute lines (L2). This is the worst one.
2. Copied 04 text and reused whys are notes, never refusals, and
   can be seated by the Director (L4).
3. No time-order check on read or boot (L3).
4. Writes are closed to other sites; reads are open to DNS
   rebinding because Host is not checked (L6).

## Questions for Matthew (asked the t189u way)

Each one: the question, my proposed answer, why, and the axioms
checked (Axioms.md lines). Proposed answers are not rulings.

Q1. Should the kernel builder stop writing into books/?
- Proposed: yes. The builder writes its output somewhere else, as
  an export (R26). Only the compute writes books/.
- Why: today the builder wipes lines the compute approved. The
  people whose approved work vanishes are the ones hurt.
- Axioms: 1 :13 pass (only the gate holds write authority);
  6 :23 pass (lines are never lost); 3 :17 pass (compute leads
  storage). No tension found.

Q2. Should the gate refuse a copied 04 and a reused why, not just
note them?
- Proposed: refuse an exact copy of 01 or 02 in 04, and a why
  reused word for word on another card. Near copies stay notes.
- Why: a copied 04 tells the person nothing new, and a reused why
  hides the real reason. Cursor's build had the same gap.
- Axioms: 4 :19 pass (each law keeps its own why); 3 :17 pass
  (04 is the person's own face); 2 :15 tension (inheriting is
  allowed, so refusal must only hit copies, not inherited text).

Q3. Should a line dated earlier than the line above be refused?
- Proposed: yes, on write and on replay at boot. The builder's
  fixed time (build.mjs:33) goes away with Q1.
- Why: the order of the log is the page's history. A time that
  runs backwards makes that history untrustworthy.
- Axioms: 6 :23 pass (lineage needs true order); 9 :29 pass (a
  trial can rely on order). No tension found.

Q4. Should the compute refuse a request whose Host is not its own
address?
- Proposed: yes. It is a small fix, and it closes reads to another
  site (DNS rebinding). Writes are already closed.
- Why: today another site could read pages through the browser.
  That would leak the person's work.
- Axioms: 1 :13 pass (no reading without being granted).
  No tension found.

## Not checked

- L1, L5, L7 (out of scope for this task).
- The Next app was not started; its pass-through was read only.
- No browser test; cross-site results are from curl headers.
- DNS rebinding was shown only by a Host header, not a real attack.
- A 04 copying face 02, or near copies (one word changed), were read
  in code, not run.
- --allow-remote was not run.
