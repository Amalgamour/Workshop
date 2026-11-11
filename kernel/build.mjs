#!/usr/bin/env node
// Builds kernel/ Markdown faces into JSON Lines book files (docs/spec/format.md section 3, docs/CONTRACT.md).
// Deterministic: files sorted by address, fixed timestamp, fixed author. No dependencies. Self-checking:
// hard checks stop the build; findings print. Rulings applied: docs/spec/DIRECTOR-RULINGS.md R1-R21
// (R19 face 00 layout follows docs/spec/face00.md, a DRAFT). Tests: node kernel/build.test.mjs
// Usage: node kernel/build.mjs          write books/
//        node kernel/build.mjs --check  rebuild in memory and fail if books/ differs
import { readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
const OUT = join(ROOT, 'books');
const SPEC = join(ROOT, 'docs', 'spec');
const BY = 'prima-kernel-seed';
// 7: format.md gives no rule for the time of a seed write. A fixed time keeps the build deterministic.
const AT = '2026-11-11T19:30:00Z';
// R6: the axioms sit outside any book, at desk level. Working address `00.00.axioms` (7: exact address).
// 7: its storage form is not given; it is written as JSON Lines like a book, under a name other lanes' `*.book` globs skip.
const AXIOMS = '00.00.axioms';
const AXIOMS_FILE = '00.00.axioms.jsonl';

const FACE_TAILS = ['draft', 'retired']; // seqAddr.md section 4
const COUNTER_TAILS = ['draft', 'pack', 'open', 'return', 'review'];
const TAIL_WORDS = ['draft', 'retired', 'pack', 'open', 'return', 'review']; // seqAddr.md:283
const CONTENT_FACES = ['01', '02', '03', '04', '05', '06', '08']; // C1.1
// decisions.md C8.9 card types and face defaults (seqAddr.md section 5.3). `work` from workflow-loop.003 section 5.2 (draft).
const CARD_TYPES = ['rule', 'schema', 'menu', 'why', 'task', 'note', 'link', 'brand', 'index', 'work', 'question'];
// R11: `question` matches crates/ask QuestionCard (COMPUTE). 7: not yet in decisions.md C8.9 or seqaddr-core CARD_TYPES.
const FACE_DEFAULT = { '01': 'rule', '02': 'schema', '03': 'menu', '04': 'why', '05': 'task', '06': 'note', '08': 'link' };
const CARD_KEY = /^[a-z][a-z0-9-]*$/; // seqAddr.md:280 `card = LOWER *( LOWER / DIGIT / "-" ) ; not a tail word`
// R7: an override page in 0001-0009 states what it changes, why it is there, why it is needed, what it should achieve.
// 7: these field names are this build's; the ruling gives the four things, not their names.
const OVERRIDE_FIELDS = ['changing', 'there', 'needed', 'achieve'];
const NAME = /^(\d{2})\.(\d{2})\.(\d{2})\.(\d{4})\.(\d{2})(?:\.(\d{2}))?(?:\.([a-z]+))?\.md$/;
const AX_NAME = /^00\.00\.axioms\.(\d{2})(?:\.(\d{2}))?(?:\.([a-z]+))?\.md$/;
// R1 and R10 merges, so a `why:` still matches its cited line after the door wording change.
const R1 = [['identity page', 'door page'], ['only an identity has', 'only a registry has'], ['only an identity has', 'only a door has'], ['board', 'door'], ['identity', 'door'], ['A page with only a registry has no reason to exist.', 'A page with only a registry has no reason to exist, except a door page 0000, which holds only face 00 (R10).']]; // last: R10 pass-4 merge (TRIAL-K2 finding 1)

const errors = [], findings = [], lookups = [];
const err = (f, m) => errors.push(`${f}: ${m}`);
const find = (f, m) => findings.push(`${f}: ${m}`);

// R4 (DIRECTOR-RULINGS.md:16): printable ASCII 0x20-0x7E plus newline only.
function checkAscii(where, text) {
  const lines = text.split('\n');
  for (let i = 0; i < lines.length; i++) for (let j = 0; j < lines[i].length; j++) {
    const c = lines[i].charCodeAt(j);
    if (c < 0x20 || c > 0x7e) { err(where, `line ${i + 1} col ${j + 1}: character U+${c.toString(16).toUpperCase().padStart(4, '0')} is not plain ASCII (R4)`); return; }
  }
}

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
  const dirs = [join(HERE, '00.00.00'), join(HERE, AXIOMS)].filter(existsSync);
  const s = join(HERE, 'samples');
  if (existsSync(s)) for (const d of readdirSync(s).sort()) if (statSync(join(s, d)).isDirectory()) dirs.push(join(s, d));
  return dirs;
}

function loadBook(dir) {
  const book = dir.split('/').pop();
  const isAx = book === AXIOMS;
  const faces = [];
  for (const file of readdirSync(dir).filter((f) => f.endsWith('.md')).sort()) {
    let dd, ss, bb, pppp, ff, nn, tail;
    if (isAx) {
      const m = AX_NAME.exec(file);
      if (!m) { err(file, `name is not ${AXIOMS}.FF[.NN][.tail].md`); continue; }
      [, ff, nn, tail] = m; pppp = null;
    } else {
      const m = NAME.exec(file);
      if (!m) { err(file, 'name is not a full address DD.SS.BB.PPPP.FF[.NN][.tail].md'); continue; }
      [, dd, ss, bb, pppp, ff, nn, tail] = m;
      if (`${dd}.${ss}.${bb}` !== book) err(file, `belongs to book ${dd}.${ss}.${bb}, found in ${book}`);
    }
    if (nn) {
      // R9 (DIRECTOR-RULINGS.md:37): faces have no sentinels; counters run 01-98.
      if (nn === '00' || nn === '99') err(file, `counter ${nn} is a face sentinel; faces have none, counters run 01-98 (R9)${ff === '03' && nn === '00' ? '; 7: R16 calls the dictionary 03.00 a door, held for the Director' : ''}`);
      if (tail && !COUNTER_TAILS.includes(tail)) err(file, `tail ${tail} not allowed on a counter`);
    } else if (tail && !FACE_TAILS.includes(tail)) err(file, `tail ${tail} not allowed on a face`);
    const page = isAx ? AXIOMS : `${book}.${pppp}`;
    const spot = `${page}.${ff}${nn ? '.' + nn : ''}`;
    // R8 (DIRECTOR-RULINGS.md:35): a draft is addressed `...PPPP.FF.draft`.
    const addr = tail ? `${spot}.${tail}` : spot;
    const body = readFileSync(join(dir, file), 'utf8');
    checkAscii(file, body);
    faces.push({ file, page, pppp, ff, nn, tail, spot, addr, body, cards: parseCards(body) });
  }
  return { book, isAx, faces };
}

// R10 (DIRECTOR-RULINGS.md:40): face 00 is the registry, listing the page's faces. Lines: "- `FF[.NN][.tail]` job: ...".
// Git blob id of a file body, so a seat can name exactly what was trialed.
function blobOf(text) {
  const b = Buffer.from(text, 'utf8');
  return createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${b.length}\0`), b])).digest('hex');
}
// R2 (DIRECTOR-RULINGS.md:7-9) seat record, kept on the registry line of face 00 (7: where it lives, QUESTIONS Q34):
// "seated; approved-by: build-stage (R2); trial: <file>@<commit>; blob: <prefix>".
const SEAT_LINE = /^seated; approved-by: (build-stage \(R2\)|director); trial: (\S+); blob: ([0-9a-f]{7,40})$/;
function seatOf(reg, f) {
  const line = reg && reg.get(`${f.ff}${f.nn ? '.' + f.nn : ''}`);
  const m = line && SEAT_LINE.exec(line.trim());
  return m ? { by: m[1], trial: m[2], blob: m[3] } : null;
}

// Layout (R19, docs/spec/face00.md DRAFT): front-matter stamp (address, title, type, state, why-draft), then a
// `## Registry` card: `faces: 01 seated, 04 draft, 06.01 draft`, then `why-NN:` for each draft and `seat-NN:` for each seat.
// Returns a map from the face as found on disk (`04.draft`, `01`, and `00.<tail>` for face 00 itself) to
// "draft because <why>" or "seated; <seat record>", or `null` when there is no registry.
export function stampOf(body) {
  const m = /^---\n([\s\S]*?)\n---\n/.exec(body);
  return m ? Object.fromEntries(m[1].split('\n').map((l) => /^([\w-]+):\s*(.*)$/.exec(l)).filter(Boolean).map((x) => [x[1], x[2]])) : {};
}
function registry(f) {
  const reg = f.cards.find((c) => c.key === 'registry');
  if (!reg || reg.fields.faces === undefined) return null;
  const out = new Map();
  const st = stampOf(f.body);
  out.set(f.tail ? `00.${f.tail}` : '00', f.tail ? `draft because ${st['why-draft'] || ''}` : `seated; ${st['seat-00'] || ''}`);
  for (const item of reg.fields.faces.trim() === '-' ? [] : reg.fields.faces.split(',')) {
    const [spot, state] = item.trim().split(/\s+/);
    if (state === 'seated') out.set(spot, `seated; ${reg.fields[`seat-${spot}`] || ''}`);
    else out.set(`${spot}.${state}`, state === 'draft' ? `draft because ${reg.fields[`why-${spot}`] || ''}` : state);
  }
  return out;
}

function validate({ book, isAx, faces }) {
  const byPage = new Map();
  for (const f of faces) (byPage.get(f.page) || byPage.set(f.page, []).get(f.page)).push(f);
  if (!isAx && !byPage.has(`${book}.0000`)) err(book, 'container has no door page 0000 (A3.1, R1)');
  for (const [page, fs] of byPage) {
    const stamp = fs.find((f) => f.ff === '00' && !f.nn);
    if (!stamp) { err(page, 'no face 00, the registry (R10)'); continue; }
    const st = stampOf(stamp.body);
    if (!['live', 'draft', 'retired'].includes(st.state)) err(stamp.file, `stamp state ${st.state} is not live, draft or retired (R12; face00.md section 1)`);
    if (st.address !== page) err(stamp.file, `stamp address ${st.address} != ${page}`);
    if (!isAx && Number(page.slice(-4)) >= 1000 && !st.title) err(stamp.file, 'pages 1000 and up need a title (A2.8)');
    const reg = registry(stamp);
    if (!reg) err(stamp.file, 'face 00 has no `## Registry` card with a `faces:` line (R10, R19; face00.md section 3.1)');
    else {
      const have = fs.map((f) => `${f.ff}${f.nn ? '.' + f.nn : ''}${f.tail ? '.' + f.tail : ''}`).sort();
      const listed = [...reg.keys()].sort();
      if (have.join() !== listed.join()) err(stamp.file, `registry lists [${listed}] but the page has [${have}] (R10)`);
      for (const [k, why] of reg) if (k.endsWith('.draft') && !/draft because \S/.test(why)) err(stamp.file, `a draft must say why (R5): ${k === '00.draft' ? 'the stamp has no why-draft:' : `the registry has no why-${k.replace(/\.draft$/, '')}:`}`);
    }
    if (!isAx && page.endsWith('.0000')) {
      // R10: on a door page 0000, face 00 is the only face.
      for (const f of fs) if (f.ff !== '00') err(f.file, 'page 0000 has only face 00 (R10)');
    } else if (!fs.some((f) => CONTENT_FACES.includes(f.ff))) err(page, 'needs a content face 01-06 or 08 (C1.1)');
    // R2: a seated face needs a seat record naming the trial and the exact blob that passed it.
    for (const f of fs.filter((x) => !x.tail && !x.nn && x.ff !== '00')) {
      const seat = seatOf(reg, f);
      if (!seat) err(f.file, `seated face has no seat-${f.ff}: record in face 00 (R2: approved-by, trial, blob); write it as FF.draft`);
      else if (!blobOf(f.body).startsWith(seat.blob)) err(f.file, `seated face changed since its trial: blob ${blobOf(f.body).slice(0, 8)} is not ${seat.blob} (R2, axiom 9); write it as FF.draft and re-trial`);
    }
    const k04 = new Map();
    for (const f of fs.filter((f) => f.ff === '04')) for (const c of f.cards) k04.set(c.key, c);
    for (const f of fs) {
      const seen = new Set();
      for (const c of f.cards) {
        if (f.ff === '00') continue;
        if (seen.has(c.key)) err(f.file, `card key ${c.key} repeats in one face (C2)`);
        seen.add(c.key);
        if (!CARD_KEY.test(c.key) || TAIL_WORDS.includes(c.key)) err(f.file, `card key ${c.key} breaks the card grammar or is a tail word (seqAddr.md:280)`);
        const type = c.fields.type || FACE_DEFAULT[f.ff];
        if (type && !CARD_TYPES.includes(type)) err(f.file, `card ${c.key}: type ${type} is not a kernel card type (C8.9)`);
        if ((f.ff === '01' || f.ff === '02') && type !== 'brand') { // R15: a brand card needs no 04 card
          const w = k04.get(c.key); // presence is checked across the lookup in crossChecks (C3.2, TRIAL-K2 finding 8)
          if (!w) { /* looked up */ }
          else if (!w.fields.why || !w.body) err(f.file, `04 card ${c.key} lacks why: or body (C3.2)`);
          else {
            if (w.body === c.body) find(f.file, `04 ${c.key} copies the ${f.ff} body (C3.2 finding)`);
            if (w.fields.why.trim() === '4.7') find(f.file, `04 ${c.key}: why missing (4.7)`);
          }
        }
        if (f.ff === '04' && !c.fields.why) err(f.file, `04 card ${c.key} has no why: (C3.2)`);
        if (f.ff === '04' && c.fields.why && c.fields.why.trim() !== '4.7') checkWhy(f.file, c);
      }
    }
    // R21 (DIRECTOR-RULINGS.md:82-84): no override pages while the Workshop app is built. R7 code below stays, not exercised.
    if (!isAx && book !== '00.00.00' && /\.000[1-9]$/.test(page)) err(page, 'no override pages while the Workshop app is built; build the change into the page (R21)');
    // R7: override statements belong only on a 0001-0009 page (TRIAL-K2 finding 19).
    if (!/\.000[1-9]$/.test(page)) for (const f of fs) for (const c of f.cards) if (OVERRIDE_FIELDS.some((k) => c.fields[k] !== undefined)) err(f.file, `card ${c.key} states an override outside 0001-0009 (R7)`);
    // R7: an override page lives in 0001-0009 and states its four parts.
    if (!isAx && book !== '00.00.00' && /\.000[1-9]$/.test(page)) {
      const cards = fs.filter((f) => f.ff !== '00').flatMap((f) => f.cards);
      if (!cards.length) err(page, 'override page has no card stating the override (R7)');
      for (const c of cards) for (const k of OVERRIDE_FIELDS) if (!c.fields[k]) err(page, `override card ${c.key} lacks ${k}: (R7: what it changes, why it is there, why it is needed, what it should achieve)`);
    }
  }
}

// A why must be copied from the line its source names: `why: docs/spec/FILE:LINE`.
function checkWhy(file, c) {
  const m = /why: docs\/spec\/([\w.\-]+):(\d+)/.exec(c.fields.source || '');
  if (!m) { err(file, `04 card ${c.key}: why: has no cited line (source: ... why: docs/spec/FILE:LINE)`); return; }
  const p = join(SPEC, m[1]);
  if (!existsSync(p)) { err(file, `04 card ${c.key}: cited file ${m[1]} is missing`); return; }
  let line = readFileSync(p, 'utf8').split('\n')[Number(m[2]) - 1] || '';
  for (const [a, b] of [['\u2014', '-'], ['\u2013', '-'], ['\u00a7', 'section '], ['\u201c', '"'], ['\u201d', '"']]) line = line.split(a).join(b); // R4 merges
  const w = c.fields.why.trim();
  if (line.includes(w)) return;
  for (const [a, b] of R1) line = line.split(a).join(b);
  if (!line.includes(w)) err(file, `04 card ${c.key}: why is not on ${m[1]}:${m[2]}`);
}

// Lookup (seqAddr.md:101): book -> shelf -> desk -> kernel, first match per face spot.
// R5: a draft is found; a seated face at the same spot wins over its draft; the result shows the draft and why.
function resolve(byBook, book, pppp, ff) {
  const [dd, ss] = book.split('.');
  const chain = pppp === '0000' ? [book] : [book, `${dd}.${ss}.00`, `${dd}.00.00`, '00.00.00'].filter((x, i, a) => a.indexOf(x) === i);
  for (const bk of chain) {
    const b = byBook.get(bk); if (!b) continue;
    const here = b.faces.filter((x) => x.pppp === pppp && x.ff === ff && !x.nn);
    const seated = here.find((x) => !x.tail), draft = here.find((x) => x.tail === 'draft');
    const f = seated || draft;
    if (!f) continue;
    const reg = registry(b.faces.find((x) => x.pppp === pppp && x.ff === '00' && !x.nn) || { cards: [] });
    return { addr: f.addr, draft: !seated, why: reg && reg.get(`${ff}.draft`) };
  }
  return null;
}

function lookupReport(books) {
  const byBook = new Map(books.map((b) => [b.book, b]));
  for (const b of books) {
    if (b.book === '00.00.00' || b.isAx) continue;
    for (const f of b.faces.filter((x) => /^000[1-9]$/.test(x.pppp) && x.ff !== '00'))
      for (const c of f.cards) {
        const t = /(\d{2}\.\d{2}\.\d{2})\.(\d{4})\.(\d{2})/.exec(c.fields.source || '');
        if (!t) { find(f.file, `override card ${c.key}: no target address in source:`); continue; }
        const r = resolve(byBook, b.book, t[2], t[3]);
        lookups.push(`${b.book}.${t[2]}.${t[3]} -> ${r ? r.addr + (r.draft ? ` (found draft; ${r.why || 'no reason listed'})` : ' (seated)') : 'missing'}; override ${f.page} card ${c.key} states a change to it (R7)`);
      }
  }
}

// TRIAL-K2 finding 8. Across the lookup chain (seqAddr.md:101):
// (a) a book face at a spot an ancestor (shelf, desk, kernel) already fills replaces it in place. R7 (DIRECTOR-RULINGS.md:32):
//     "An override does not silently replace a face in place." Under R21 the change is built into the ancestor instead.
// (b) C3.2: every 01/02 card (not brand, R15) has a 04 card with the same key on the 04 face the lookup returns.
function chainOf(book) {
  const [dd, ss] = book.split('.');
  return [book, `${dd}.${ss}.00`, `${dd}.00.00`, '00.00.00'].filter((x, i, a) => a.indexOf(x) === i);
}
function crossChecks(books) {
  const byBook = new Map(books.filter((b) => !b.isAx).map((b) => [b.book, b]));
  for (const b of byBook.values()) {
    const up = chainOf(b.book).slice(1);
    for (const f of b.faces.filter((x) => x.ff !== '00' && !x.nn && x.pppp !== '0000')) {
      const anc = up.map((u) => byBook.get(u)).find((ub) => ub && ub.faces.some((x) => x.pppp === f.pppp && x.ff === f.ff && !x.nn));
      if (anc) err(f.file, `replaces ${anc.book}.${f.pppp}.${f.ff} in place; an override does not silently replace a face (R7), and none are made while the app is built (R21)`);
    }
    const pages = new Set(b.faces.filter((x) => x.pppp !== '0000').map((x) => x.pppp));
    for (const pppp of pages) {
      const eff = (ff) => { const r = resolve(byBook, b.book, pppp, ff); if (!r) return null; return books.flatMap((x) => x.faces).find((x) => x.addr === r.addr) || null; };
      const f04 = eff('04');
      const keys04 = new Set(f04 ? f04.cards.map((c) => c.key) : []);
      for (const ff of ['01', '02']) {
        const f = eff(ff); if (!f) continue;
        for (const c of f.cards) {
          if ((c.fields.type || FACE_DEFAULT[ff]) === 'brand') continue; // R15
          if (!keys04.has(c.key)) err(f.file, `card ${c.key} has no 04 card${f04 ? ' on ' + f04.addr : ''} across the lookup from ${b.book} (C3.2)`);
        }
      }
    }
  }
}

function render(entriesOf, address) {
  const lines = [JSON.stringify({ seqbook: 1, address })];
  let n = 0;
  const regs = new Map();
  for (const f of entriesOf) if (f.ff === '00' && !f.nn) regs.set(f.page, registry(f) || new Map());
  for (const f of entriesOf) {
    const e = { n: ++n, at: AT, by: BY, op: 'put', addr: f.addr };
    if (f.tail) e.tail = f.tail; // same word as the address tail, for readers that read the field (seqaddr-core accepts both when they agree)
    // R5 follow-up: a draft says why it is a draft. Copied from its registry line. 7: field name `reason` (CORE is adding one).
    if (f.tail === 'draft') {
      const r = (regs.get(f.page) || new Map()).get(`${f.ff}${f.nn ? '.' + f.nn : ''}.draft`);
      if (r) e.reason = r.replace(/^draft because /, '');
    }
    if (!f.tail && !f.nn && f.ff !== '00') {
      const seat = seatOf(regs.get(f.page), f);
      if (seat) { e['approved-by'] = seat.by; e.trial = `${seat.trial} blob ${seat.blob}`; }
    }
    e.body = f.body.replace(/\n+$/, '');
    e.proposal = `${BY}:${f.page}`; // format.md section 3.3 proposal batches (proposed): a page arrives with its faces.
    lines.push(JSON.stringify(e));
  }
  const text = lines.join('\n') + '\n';
  checkAscii(address, text);
  return text;
}

const check = process.argv.includes('--check');
const books = sources().map(loadBook);
books.forEach(validate);
crossChecks(books);
lookupReport(books);
for (const f of findings) console.log('finding  ' + f);
for (const l of lookups) console.log('lookup   ' + l);
const outputs = books.map((b) => [join(OUT, b.isAx ? AXIOMS_FILE : `${b.book}.book`), render(b.faces, b.book)]);
for (const e of errors) console.error('ERROR    ' + e);
if (errors.length) { console.error(`${errors.length} errors; nothing written`); process.exit(1); }
if (!check) mkdirSync(OUT, { recursive: true });
let diff = 0;
for (const [out, text] of outputs) {
  if (check) { if (!existsSync(out) || readFileSync(out, 'utf8') !== text) { console.error(`differs: ${out}`); diff++; } }
  else writeFileSync(out, text);
  console.log(`${check ? 'checked' : 'wrote'}  ${out.slice(ROOT.length + 1)}  ${text.split('\n').length - 2} entries`);
}
console.log(`${findings.length} findings, 0 errors`);
if (diff) process.exit(1);
