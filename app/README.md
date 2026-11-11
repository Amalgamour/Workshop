# Workshop reader (app/)

A calm reader for seqAddr books. It shows what the compute holds and changes nothing.
It talks only to the compute HTTP API (`docs/CONTRACT.md`).

## Run it

```bash
cd app
npm install
npm run mock          # terminal 1: read-only mock compute on http://127.0.0.1:7700
npm run build && npm start   # terminal 2: reader on http://127.0.0.1:3000
```

- Use the real compute instead of the mock: start it, then `COMPUTE_URL=http://host:port npm start`.
- The mock reads `books/*.book` (and `kernel/*.book`) at the repo root. If none exist it uses `app/mock/fixtures/`.
  Choose another folder with `BOOKS_DIR=/path npm run mock`. It re-reads the files on every request and never writes.
- Rebuild the sample books: `node mock/make-fixtures.mjs`.
- Screenshots (needs both servers up and Chrome): `npm run screenshots` -> `app/screenshots/`.

## Screens

| Screen | Where | Shows |
|---|---|---|
| Library | `/` | desks > shelves > books > pages, with titles, addresses and faces |
| Page | `/page/DD.SS.BB.PPPP?face=01` | the stamp, faces as tabs, cards, state badge, local / inherited / missing |
| Card matching | `/cards?title=key` | one card key on every face that has it |
| Links and map | `/links/DD.SS.BB.PPPP` | links out, links in, missing and one-way links, face 08 as written |
| History | `/history/address` | every log entry: when (Toronto and UTC), who, what, entry number |
| Word lookup | `/words` | typed words that are brands light up, with meanings and the connect web |
| Resolve trace | `/resolve?addr=...` | each step of book -> shelf -> desk -> kernel |

Every screen has "Check it yourself": the raw compute answer and its URL.

## Desk working side (round 2: needs the real compute, which writes)

| Screen | Where | Does |
|---|---|---|
| Desk | `/desk/DD` | one desk: its door (`DD.00.00.0000`, R1), shelves, books, and every job on it as a board |
| Draft a face | `/draft?page=...&face=FF` | new page (door + face, both drafts), new face (draft), or change a live face: copy -> note -> merge (D0) |
| Seat a face | `/seat?addr=...FF` | promote a draft: `build-stage (R2)` + trial reference, or `director` |
| Work loop | `/work?page=...` | face 05 jobs: draft -> pack -> open -> return -> review -> closed, one plain rule per step |
| Queue | `/queue` | every proposal, approved or not, with rule, axiom and detail |
| Export | `/export?addr=...` | the page as a `.seq` file, when the compute serves `GET /page.seq` (CONTRACT addendum) |

- "Writing as" in the sidebar is the `by` name sent with each proposal. There is no sign-in yet.
- Every write shows the exact proposal first ("Check before sending") and the compute's answer after.
- After an approved write the screen reloads with `?done=<queue id>` and reads the result back from `/queue`.
- Try it without touching the real books: copy `books/` to a temp folder and run the compute on it:

```bash
mkdir -p /tmp/w/books && cp books/*.book /tmp/w/books/
./target/debug/compute --books /tmp/w/books --listen 127.0.0.1:7710 &
cd app && npm run build && COMPUTE_URL=http://127.0.0.1:7710 npx next start -p 3010
APP_URL=http://127.0.0.1:3010 node scripts/screenshots-live-2x.mjs   # drives every flow, saves live-2x-*.png
```

## Round 3: Ask, sign in, .seq import (real compute)
- **Ask** (`/ask`): type a question; POST /ask (no token). Shows 1 · What I heard (important / linking / question words), 2 · the 1-3 pieces with why each matched, its score, a Draft badge, and the question it came through, or the probe question when nothing fits. 3 · Teach a new way of asking: POST /ask/link `{question, phrasing}` (token needed); the questions come from page `READER_BOOK.0013` (default 10.11.21).
- **Signed in** box in the sidebar: paste your token (your line in `books/.identities`). The app checks it with an empty POST /propose (400 = known, 401 = unknown; nothing is queued). Your name shows after your first write (no "who am I" route yet). 401 shows "Not signed in", 403 "Not allowed for your name" (axiom 1), 415 wrong content type.
- **Page view**: face 00 is shown as the Registry (1 · Stamp, 2 · Type, 3 · Registry; docs/spec/face00.md is a DRAFT). Every draft face shows why it is a draft (R5): the reason recorded when it was opened, else its first open note. Bottom of the page: Export page as .seq, and Import: load this page's .seq or a file, 1 · Check it (POST /check.seq, writes nothing), 2 · Import through the queue (POST /propose, text/x-seqpage).
- Draft a face asks "Why is this a draft?" and sends it as `reason`.
- Screenshots: `APP_URL=http://127.0.0.1:3020 COMPUTE=http://127.0.0.1:7720 TOKEN=tok-app-demo node scripts/screenshots-live-3x.mjs` against a compute on a COPY of the books with demo tokens in that copy's `.identities` -> `screenshots/live-3x-*.png`.
- All writes go through `app/api/post/[...path]` (propose, ask, ask/link, close, check.seq), which forwards the token and content type. The mock has no /ask and no writes.

## Files

- `lib/compute.ts` the only place that calls the compute
- `lib/seq.ts` plain-word labels and the card parser (display only, it decides no rules)
- `components/` shared pieces; `app/` the screens; `app/api/compute/` a GET-only pass-through for the word box
- `mock/server.mjs` the mock compute; `mock/fixtures/` sample books
