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

## Files

- `lib/compute.ts` the only place that calls the compute
- `lib/seq.ts` plain-word labels and the card parser (display only, it decides no rules)
- `components/` shared pieces; `app/` the screens; `app/api/compute/` a GET-only pass-through for the word box
- `mock/server.mjs` the mock compute; `mock/fixtures/` sample books
