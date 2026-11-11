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

// seqAddr.md §4 / §8. Face 00 takes no tail here (7: spec silent on a draft stamp; see MAP.md).
const FACE_TAILS = ['draft', 'retired'];
const COUNTER_TAILS = ['draft', 'pack', 'open', 'return', 'review'];
const CONTENT_FACES = ['01', '02', '03', '04', '05', '06', '08']; // C1.1
// decisions.md C8.9 card types, and face defaults (seqAddr.md §5.3). `work` from workflow-loop.003 §5.2 (draft).
const CARD_TYPES = ['rule', 'schema', 'menu', 'why', 'task', 'note', 'link', 'brand', 'index', 'work'];
const FACE_DEFAULT = { '01': 'rule', '02': 'schema', '03': 'menu', '04': 'why', '05': 'task', '06': 'note', '08': 'link' };
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
      if (nn === '00') err(file, 'FF.00 is a board; boards are derived and never written (format.md §3.3)');
      if (tail && !COUNTER_TAILS.includes(tail)) err(file, `tail ${tail} not allowed on a counter`);
    } else if (tail) {
      if (ff === '00') err(file, 'face 00 written with a tail (7: not used in this build)');
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
  if (!byPage.has(`${book}.0000`)) err(book, 'container has no identity page 0000 (A3.1)');
  for (const [page, fs] of byPage) {
    const stamp = fs.find((f) => f.ff === '00' && !f.nn);
    if (!stamp) { err(page, 'no face 00 (C1.1)'); continue; }
    const st = Object.fromEntries([...stamp.body.matchAll(/^(\w+):\s*(.*)$/gm)].map((m) => [m[1], m[2]]));
    if (st.address !== page) err(stamp.file, `stamp address ${st.address} != ${page}`);
    if (Number(page.slice(-4)) >= 1000 && !st.title) err(stamp.file, 'pages 1000 and up need a title (A2.8)');
    if (!fs.some((f) => CONTENT_FACES.includes(f.ff))) {
      if (page.endsWith('.0000')) find(page, 'identity page has no content face; C1.1 vs A3.1 (CONFLICTS.md)');
      else err(page, 'needs a content face 01-06 or 08 (C1.1)');
    }
    // C3.2 hard: every 01/02 card key has a 04 card with why: and a body, in this book.
    const k04 = new Map();
    for (const f of fs.filter((f) => f.ff === '04')) for (const c of f.cards) k04.set(c.key, c);
    for (const f of fs) {
      const seen = new Set();
      for (const c of f.cards) {
        if (seen.has(c.key)) err(f.file, `card key ${c.key} repeats in one face (C2)`);
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
    for (const f of fs.filter((f) => f.nn)) find(f.file, `counter without a written ${f.ff}.00 board; boards are derived (CONFLICTS.md)`);
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
