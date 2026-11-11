#!/usr/bin/env node
// Builds kernel/ Markdown faces into JSON Lines book files (docs/spec/format.md §3, docs/CONTRACT.md).
// Deterministic: files sorted by address, fixed timestamp, fixed author. No dependencies.
// Usage: node kernel/build.mjs          write books/
//        node kernel/build.mjs --check  rebuild in memory and fail if books/ differs
import { readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
const OUT = join(ROOT, 'books');
const BY = 'prima-kernel-seed';
// 7: format.md gives no rule for the time of a seed write. A fixed time keeps the build deterministic.
const AT = '2026-11-11T19:30:00Z';

// seqAddr.md §4 / §8. Face 00 is the door face (DIRECTOR-RULINGS.md R1); like any face it may be `draft` (seqAddr.md:283).
const FACE_TAILS = ['draft', 'retired'];
const COUNTER_TAILS = ['draft', 'pack', 'open', 'return', 'review'];
const CONTENT_FACES = ['01', '02', '03', '04', '05', '06', '08']; // C1.1
// decisions.md C8.9 card types, and face defaults (seqAddr.md §5.3). `work` from workflow-loop.003 §5.2 (draft).
const CARD_TYPES = ['rule', 'schema', 'menu', 'why', 'task', 'note', 'link', 'brand', 'index', 'work'];
const FACE_DEFAULT = { '01': 'rule', '02': 'schema', '03': 'menu', '04': 'why', '05': 'task', '06': 'note', '08': 'link' };
const TAIL_WORDS = ['draft', 'retired', 'pack', 'open', 'return', 'review']; // seqAddr.md:283
const CARD_KEY = /^[a-z][a-z0-9-]*$/; // seqAddr.md:280 `card = LOWER *( LOWER / DIGIT / "-" )   ; not a tail word`
// R1 (DIRECTOR-RULINGS.md:5): copied spec text says "door" where it said identity/board/owner. Used only to check
// that a `why:` still matches its cited line after the R1 merges recorded in each page's 06.01 note.
const R1 = [['identity page', 'door page'], ['only an identity has', 'only a door has'], ['board', 'door'], ['identity', 'door']];
const SPEC = join(ROOT, 'docs', 'spec');
const NAME = /^(\d{2})\.(\d{2})\.(\d{2})\.(\d{4})\.(\d{2})(?:\.(\d{2}))?(?:\.([a-z]+))?\.md$/;

const errors = [], findings = [];
const err = (f, m) => errors.push(`${f}: ${m}`);
const find = (f, m) => findings.push(`${f}: ${m}`);

// Title form of a heading (C2: `Retry Policy` -> `retry-policy`).
export const keyOf = (h) => h.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');

// Cards: `##` headings outside code fences; field lines until the first blank line; then the body.
export function parseCards(md) {
  const cards = []; let cur = null, fence = false, inFields = false;
  for (const line of md.split('\n')) {
    if (/^(```|~~~)/.test(line)) fence = !fence;
    if (!fence && /^## /.test(line)) {
      cur = { heading: line.slice(3).trim(), key: keyOf(line.slice(3)), fields: {}, body: [] };
      cards.push(cur); inFields = true; continue;
    }
    if (!cur) continue;
    if (inFields) {
      if (line.trim() === '') { inFields = false; continue; }
      const m = /^([A-Za-z][\w.\- ]*?):\s?(.*)$/.exec(line);
      if (m) { cur.fields[m[1]] = m[2]; continue; }
      inFields = false;
    }
    cur.body.push(line);
  }
  for (const c of cards) c.body = c.body.join('\n').trim();
  return cards;
}

function sources() {
  const dirs = [join(HERE, '00.00.00')];
  const s = join(HERE, 'samples');
  if (existsSync(s)) for (const d of readdirSync(s).sort()) if (statSync(join(s, d)).isDirectory()) dirs.push(join(s, d));
  return dirs;
}

function loadBook(dir) {
  const book = dir.split('/').pop();
  const faces = [];
  for (const file of readdirSync(dir).filter((f) => f.endsWith('.md')).sort()) {
    const m = NAME.exec(file);
    if (!m) { err(file, 'name is not a full seated address DD.SS.BB.PPPP.FF[.NN][.tail].md'); continue; }
    const [, dd, ss, bb, pppp, ff, nn, tail] = m;
    if (`${dd}.${ss}.${bb}` !== book) err(file, `belongs to book ${dd}.${ss}.${bb}, found in ${book}`);
    if (nn) {
      if (nn === '00') err(file, 'FF.00 is a door; format.md:102 says it is derived and never written (CONFLICTS.md K02, QUESTIONS.md)');
      if (tail && !COUNTER_TAILS.includes(tail)) err(file, `tail ${tail} not allowed on a counter`);
    } else if (tail) {
      if (!FACE_TAILS.includes(tail)) err(file, `tail ${tail} not allowed on a face`);
    }
    const page = `${book}.${pppp}`;
    const addr = `${page}.${ff}${nn ? '.' + nn : ''}`;
    const body = readFileSync(join(dir, file), 'utf8');
    faces.push({ file, page, pppp, ff, nn, tail, addr, body, cards: ff === '00' ? [] : parseCards(body) });
  }
  return { book, faces };
}

function validate({ book, faces }) {
  const byPage = new Map();
  for (const f of faces) (byPage.get(f.page) || byPage.set(f.page, []).get(f.page)).push(f);
  if (!byPage.has(`${book}.0000`)) err(book, 'container has no door page 0000 (A3.1, R1)');
  for (const [page, fs] of byPage) {
    const stamp = fs.find((f) => f.ff === '00' && !f.nn);
    if (!stamp) { err(page, 'no door face 00 (C1.1, R1)'); continue; }
    const st = Object.fromEntries([...stamp.body.matchAll(/^(\w+):\s*(.*)$/gm)].map((m) => [m[1], m[2]]));
    if (st.address !== page) err(stamp.file, `stamp address ${st.address} != ${page}`);
    if (Number(page.slice(-4)) >= 1000 && !st.title) err(stamp.file, 'pages 1000 and up need a title (A2.8)');
    if (!fs.some((f) => CONTENT_FACES.includes(f.ff))) {
      if (page.endsWith('.0000')) find(page, 'door page has no content face; C1.1 vs A3.1 (CONFLICTS.md K10, QUESTIONS.md)');
      else err(page, 'needs a content face 01-06 or 08 (C1.1)');
    }
    // C3.2 hard: every 01/02 card key has a 04 card with why: and a body, in this book.
    const k04 = new Map();
    for (const f of fs.filter((f) => f.ff === '04')) for (const c of f.cards) k04.set(c.key, c);
    for (const f of fs) {
      const seen = new Set();
      for (const c of f.cards) {
        if (seen.has(c.key)) err(f.file, `card key ${c.key} repeats in one face (C2)`);
        if (!CARD_KEY.test(c.key) || TAIL_WORDS.includes(c.key)) err(f.file, `card key ${c.key} breaks the card grammar or is a tail word (seqAddr.md:280)`);
        if (!f.tail && f.ff !== '00' && !f.nn && !/R2/.test(c.fields['approved-by'] || '')) err(f.file, `seated card ${c.key} has no approved-by (DIRECTOR-RULINGS.md R2); write the face as FF.draft`);
        if (f.ff === '04' && c.fields.why && c.fields.why.trim() !== '4.7') checkWhy(f.file, c);
        seen.add(c.key);
        const type = c.fields.type || FACE_DEFAULT[f.ff];
        if (type && !CARD_TYPES.includes(type)) err(f.file, `card ${c.key}: type ${type} is not a kernel card type (C8.9)`);
        if (f.ff === '01' || f.ff === '02') {
          const w = k04.get(c.key);
          if (!w) err(f.file, `card ${c.key} has no 04 card (C3.2)`);
          else if (!w.fields.why || !w.body) err(f.file, `04 card ${c.key} lacks why: or body (C3.2)`);
          else {
            if (w.body === c.body) find(f.file, `04 ${c.key} copies the ${f.ff} body (C3.2 finding)`);
            if (w.fields.why.trim() === '4.7') find(f.file, `04 ${c.key}: why missing (4.7)`);
          }
        }
        if (f.ff === '04' && !c.fields.why) err(f.file, `04 card ${c.key} has no why: (C3.2)`);
      }
    }
    for (const f of fs.filter((f) => f.nn)) find(f.file, `counter without a written ${f.ff}.00 door; format.md:102 vs :123 (CONFLICTS.md K02, QUESTIONS.md)`);
  }
}

// A why must be copied from the line its source names: `why: docs/spec/FILE:LINE`. Text outside docs/spec cannot be checked here.
function checkWhy(file, c) {
  const m = /why: docs\/spec\/([\w.\-]+):(\d+)/.exec(c.fields.source || '');
  if (!m) { err(file, `04 card ${c.key}: why: has no cited line (source: ... why: docs/spec/FILE:LINE)`); return; }
  const p = join(SPEC, m[1]);
  if (!existsSync(p)) { err(file, `04 card ${c.key}: cited file ${m[1]} is missing`); return; }
  let line = readFileSync(p, 'utf8').split('\n')[Number(m[2]) - 1] || '';
  const w = c.fields.why.trim();
  if (line.includes(w)) return;
  for (const [a, b] of R1) line = line.split(a).join(b);
  if (!line.includes(w)) err(file, `04 card ${c.key}: why is not on ${m[1]}:${m[2]}`);
}

// Lookup across books (seqAddr.md:101): book -> shelf -> desk -> kernel, first match per face.
// A draft is "being written; not active" (seqAddr.md:133), so a draft face is not found (QUESTIONS.md asks whether it should be).
function lookupReport(books) {
  const by = new Map(books.map((b) => [b.book, b]));
  for (const b of books) {
    const [dd, ss] = b.book.split('.');
    const chainAll = [b.book, `${dd}.${ss}.00`, `${dd}.00.00`, '00.00.00'].filter((x, i, a) => a.indexOf(x) === i && by.has(x));
    const pages = new Set(b.faces.map((f) => f.pppp));
    for (const pppp of [...pages].sort()) {
      // Page 0000 is each container's own door page; it is not inherited (seqAddr.md:56-62).
      const chain = pppp === '0000' ? [b.book] : chainAll;
      const facesSeen = new Set();
      for (const bk of chain) for (const f of by.get(bk).faces) if (f.pppp === pppp && !f.nn) facesSeen.add(f.ff);
      for (const ff of [...facesSeen].sort()) {
        let got = null, draftAt = null;
        for (const bk of chain) {
          const f = by.get(bk).faces.find((x) => x.pppp === pppp && x.ff === ff && !x.nn);
          if (!f) continue;
          if (f.tail === 'draft') { draftAt = draftAt || f.addr; continue; }
          got = f.addr; break;
        }
        if (b.book !== '00.00.00' && !got) find(`${b.book}.${pppp}.${ff}`, `lookup: missing; only a draft exists (${draftAt}), not active (seqAddr.md:133)`);
      }
      // C3.2 on the resolved page, per face, drafts included (shows what a per-face override would hide).
      if (b.book === '00.00.00') continue;
      const resolved = new Map();
      for (const bk of chain) for (const f of by.get(bk).faces) if (f.pppp === pppp && !f.nn && !resolved.has(f.ff)) resolved.set(f.ff, f);
      const k04 = new Set((resolved.get('04')?.cards || []).map((c) => c.key));
      for (const ff of ['01', '02']) for (const c of resolved.get(ff)?.cards || []) if (!k04.has(c.key))
        find(`${b.book}.${pppp}`, `per-face lookup hides 04 card ${c.key} for ${resolved.get(ff).addr} (C3.2; QUESTIONS.md per face or per card)`);
    }
  }
}

function render({ book, faces }) {
  const lines = [JSON.stringify({ seqbook: 1, address: book })];
  let n = 0;
  for (const f of faces) {
    const e = { n: ++n, at: AT, by: BY, op: 'put', addr: f.addr };
    if (f.tail) e.tail = f.tail;
    e.body = f.body.replace(/\n+$/, '');
    e.proposal = `${BY}:${f.page}`; // format.md §3.3 proposal batches (proposed): a page arrives with its faces.
    lines.push(JSON.stringify(e));
  }
  return lines.join('\n') + '\n';
}

const check = process.argv.includes('--check');
const books = sources().map(loadBook);
books.forEach(validate);
lookupReport(books);
for (const f of findings) console.log('finding  ' + f);
for (const e of errors) console.error('ERROR    ' + e);
if (errors.length) { console.error(`${errors.length} errors; nothing written`); process.exit(1); }
if (!check) mkdirSync(OUT, { recursive: true });
let diff = 0;
for (const b of books) {
  const out = join(OUT, `${b.book}.book`), text = render(b);
  if (check) { if (!existsSync(out) || readFileSync(out, 'utf8') !== text) { console.error(`differs: ${out}`); diff++; } }
  else writeFileSync(out, text);
  console.log(`${check ? 'checked' : 'wrote'}  books/${b.book}.book  ${b.faces.length} entries`);
}
console.log(`${findings.length} findings, 0 errors`);
if (diff) process.exit(1);
