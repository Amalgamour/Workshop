#!/usr/bin/env node
// Builds kernel/ Markdown faces into JSON Lines book files (docs/spec/format.md section 3, docs/CONTRACT.md).
// Deterministic: files sorted by address, fixed timestamp, fixed author. No dependencies. Self-checking:
// hard checks stop the build; findings print. Rulings applied: docs/spec/DIRECTOR-RULINGS.md R1-R22
// (R19 face 00 layout follows docs/spec/face00.md, a DRAFT; R22 lets a face 05 counter 05.NN be seated, Q41 open;
// no other counter is seated until a ruling allows it, Q35, TRIAL-K4 finding 7).
// Seat records are checked, not trusted (TRIAL-K3 findings 1, 2, 11; TRIAL-K4 findings 1, 2, 4-6: full blobs, rulings and
// past seats read from HEAD, no git is an error; TRIAL-K5 findings 1-3, 5, Q53, Q54: a trial is cited by path and blob, not
// commit, so seats verify in the filter-branched published copy; git runs with no replace objects and no GIT_* env; past
// seats come from the history of seat lines; TRIAL-K6 findings 1, 2, Q56: history is read with -a --no-textconv --full-history
// --no-abbrev, and seat lines from the face 00 blobs themselves, so attributes and merges hide nothing; TRIAL-K7 findings 1, 2,
// Q58, Q59: no symlink anywhere the builder reads, a seated face must be a regular file in git with the seat blob, history
// follows any symlink ever committed under kernel/, and a root commit is parsed; TRIAL-K8 findings 1, 2, Q61, Q62: the history
// walk follows a link at `kernel` itself, absolute links and link chains, a face 00 with seat records must be the bytes git
// holds, and past seats are also read from every committed version of books/; TRIAL-K9 findings 1-4, Q63-Q66: an un-seat names
// the last real seat blob from structured registry and stamp fields in face 00 history and from books/ history, books are read
// in any mode and a current book must be 100644, history walks read -z output, and un-seat records make face 00 git-checked).
// Tests: node kernel/build.test.mjs
// Usage: node kernel/build.mjs          write books/
//        node kernel/build.mjs --check  rebuild in memory and fail if books/ differs
import { readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync, lstatSync, statSync } from 'node:fs';
import { join, dirname, relative, isAbsolute, sep, posix } from 'node:path';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
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
// R22 (DIRECTOR-RULINGS.md:86-88) names "the seated 05" only. Seating any other counter (06 notes, 03 dictionary sections)
// is open (QUESTIONS Q35), and R2 lets nobody answer an open question, so the builder refuses it (TRIAL-K4 finding 7).
// Add a face here only when a ruling allows it, and cite the ruling.
const SEATABLE_COUNTERS = { '05': 'R22' };
const FACE_DEFAULT = { '01': 'rule', '02': 'schema', '03': 'menu', '04': 'why', '05': 'task', '06': 'note', '08': 'link' };
const CARD_KEY = /^[a-z][a-z0-9-]*$/; // seqAddr.md:280 `card = LOWER *( LOWER / DIGIT / "-" ) ; not a tail word`
// R7: an override page in 0001-0009 states what it changes, why it is there, why it is needed, what it should achieve.
// 7: these field names are this build's; the ruling gives the four things, not their names.
const OVERRIDE_FIELDS = ['changing', 'there', 'needed', 'achieve'];
const NAME = /^(\d{2})\.(\d{2})\.(\d{2})\.(\d{4})\.(\d{2})(?:\.(\d{2}))?(?:\.([a-z]+))?\.md$/;
const AX_NAME = /^00\.00\.axioms\.(\d{2})(?:\.(\d{2}))?(?:\.([a-z]+))?\.md$/;
// R1 and R10 merges, so a `why:` still matches its cited line after the door wording change. Last: R18 (TRIAL-K3 finding 5).
const R1 = [['identity page', 'door page'], ['only an identity has', 'only a registry has'], ['only an identity has', 'only a door has'], ['board', 'door'], ['identity', 'door'], ['A page with only a registry has no reason to exist.', 'A page with only a registry has no reason to exist, except a door page 0000, which holds only face 00 (R10).'], ['sets linked by number', 'sets matched by number and title (R18)']]; // R10 pass-4 merge (TRIAL-K2 finding 1); R18 pass-5 merge (TRIAL-K3 finding 5)

const errors = [], findings = [], lookups = [];
const err = (f, m) => errors.push(`${f}: ${m}`);
const find = (f, m) => findings.push(`${f}: ${m}`);
const CHECK = process.argv.includes('--check');

// TRIAL-K7 finding 1, Q58 (decided by KERNEL pass 9, builder lane: option C, both A and B). A symlink lets a face 00 or a
// whole book live outside kernel/ (or under kernel/parked/), where the history walk did not look, so a seat added and removed
// through it left no trace (T18, T18b), and a seated face could be a link to bytes git never held (T18c). The builder follows
// no symlink: every path it reads (book folders, faces, books/, cited trial and spec files) is checked from ROOT down with
// lstat, and a link at any step is an error. A path outside ROOT is an error too.
const there = (p) => { try { lstatSync(p); return true; } catch { return false; } };
function linkIn(abs) {
  const rel = relative(ROOT, abs);
  if (rel === '') return null;
  if (rel.startsWith('..') || isAbsolute(rel)) return abs;
  let p = ROOT;
  for (const part of rel.split(sep)) {
    p = join(p, part);
    let st; try { st = lstatSync(p); } catch { return null; } // missing: the caller reports it
    if (st.isSymbolicLink()) return p;
  }
  return null;
}
function noLink(abs) {
  const l = linkIn(abs);
  if (!l) return true;
  const r = relative(ROOT, l);
  err(r.startsWith('..') || isAbsolute(r) ? l : r, `${r.startsWith('..') || isAbsolute(r) ? 'is outside the repo' : 'is a symlink'}; the builder reads only regular files and folders in the repo and follows no link, because a link moves seat lines where the history check cannot see them (R2; TRIAL-K7 finding 1, Q58)`);
  return false;
}

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
  const dirs = [join(HERE, '00.00.00'), join(HERE, AXIOMS)].filter((d) => there(d) && noLink(d));
  const s = join(HERE, 'samples');
  if (there(s) && noLink(s)) for (const d of readdirSync(s).sort()) {
    const st = lstatSync(join(s, d));
    if (st.isSymbolicLink()) noLink(join(s, d)); // Q58: a linked book folder (T18b) is an error, never followed
    else if (st.isDirectory()) dirs.push(join(s, d));
  }
  return dirs;
}

function loadBook(dir) {
  const book = dir.split('/').pop();
  const isAx = book === AXIOMS;
  const faces = [];
  for (const file of readdirSync(dir).sort()) {
    const st = lstatSync(join(dir, file));
    if (st.isSymbolicLink()) { noLink(join(dir, file)); continue; } // Q58: a linked face (T18, T18c) is an error, never read
    if (!file.endsWith('.md')) continue;
    if (!st.isFile()) { err(file, 'is not a regular file (TRIAL-K7 finding 1, Q58)'); continue; }
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
    const rel = relative(ROOT, join(dir, file)).split(sep).join('/');
    faces.push({ file, rel, page, pppp, ff, nn, tail, spot, addr, body, cards: parseCards(body) });
  }
  return { book, isAx, faces };
}

// R10 (DIRECTOR-RULINGS.md:40): face 00 is the registry, listing the page's faces. Lines: "- `FF[.NN][.tail]` job: ...".
// Git blob id of a file body, so a seat can name exactly what was trialed.
function blobOf(text) {
  const b = Buffer.from(text, 'utf8');
  return createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${b.length}\0`), b])).digest('hex');
}
// R2 (DIRECTOR-RULINGS.md:7-9) seat record, kept on the registry line of face 00 (7: where it lives, QUESTIONS Q34).
// Face 00 itself keeps its record in the stamp as `seat-00:` (TRIAL-K3 finding 1). Two forms:
//   "seated; approved-by: build-stage (R2); trial: docs/trial/<file>.md blob <40 hex>; blob: <40 hex>"
//   "seated; approved-by: director; ruling: R<n>; blob: <40 hex>"   (the ruling must name the face, TRIAL-K3 finding 2)
// The blob is the full 40-hex git blob, compared for equality; a short prefix is an error (TRIAL-K4 finding 1, Q52 a).
// TRIAL-K5 finding 1, Q53 (option A taken by KERNEL pass 7): the trial is named by its path and the full blob of the trial
// file, not by a commit id. Blob ids survive the filter-branch that makes the published copy; commit ids do not. The old
// `<file>.md@<commit>` form is refused with a message saying how to re-pin it.
const SEAT_LINE = /^seated; approved-by: (build-stage \(R2\)|director); (trial|ruling): ([^;]+?); blob: ([0-9a-f]{7,40})$/;
const spotKey = (f) => `${f.ff}${f.nn ? '.' + f.nn : ''}`;
function seatOf(reg, f) {
  const line = reg && reg.get(spotKey(f));
  const m = line && SEAT_LINE.exec(line.trim());
  return m ? { by: m[1], kind: m[2], ref: m[3], blob: m[4], line } : null;
}
// TRIAL-K3 finding 2: a seat is checked, not trusted. A build-stage seat must cite a trial file that exists (at the
// cited commit when git is there) and whose PASS list names this face at this blob. A director seat must cite a ruling
// in DIRECTOR-RULINGS.md that names this face. Anything that cannot be verified blocks the seat (an error).
// TRIAL-K4 findings 2, 4, 5, 6 (Q52 b-d): rulings and past seats are read from git at HEAD, never the working tree;
// a cited trial commit must be an ancestor of HEAD; with no git a seat cannot be verified, so it is an error.
// TRIAL-K5 finding 2, Q54 a (taken by KERNEL pass 7): git runs with --no-replace-objects and an environment with every GIT_*
// variable removed (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES,
// GIT_NAMESPACE, GIT_CONFIG_*, ...), so the caller cannot point the guard at another repo (H15). A repo with any ref under
// refs/replace/, a grafts file, or a shallow history is refused: it can make git serve content that is not in the history (HR),
// or hide the history the guard reads (gitTrust).
let gitOk = null;
const GIT_ENV = Object.fromEntries(Object.entries(process.env).filter(([k]) => !/^GIT_/i.test(k)));
GIT_ENV.GIT_NO_REPLACE_OBJECTS = '1';
const git = (...a) => spawnSync('git', ['--no-replace-objects', '-C', ROOT, ...a], { encoding: 'utf8', maxBuffer: 1 << 28, env: GIT_ENV });
function hasGit() {
  if (gitOk === null) gitOk = git('rev-parse', '--show-toplevel').stdout?.trim() === ROOT && git('rev-parse', '--verify', '-q', 'HEAD').status === 0;
  return gitOk;
}
let trustMsg;
function gitTrust() {
  if (trustMsg !== undefined) return trustMsg;
  trustMsg = null;
  const rr = git('for-each-ref', '--format=%(refname)', 'refs/replace/');
  if (rr.status !== 0 || rr.stdout.trim()) trustMsg = `the repo has replace refs (${rr.stdout.trim().split('\n').join(', ') || 'unreadable'}); git replace can serve a forged trial, so no seat is verified until they are removed (TRIAL-K5 finding 2, Q54 a)`;
  const gp = git('rev-parse', '--git-path', 'info/grafts').stdout?.trim();
  const gpath = gp && (gp.startsWith('/') ? gp : join(ROOT, gp));
  if (!trustMsg && gpath && existsSync(gpath)) trustMsg = `the repo has a grafts file (${gp}); grafts rewrite history, so no seat is verified (TRIAL-K5 finding 2, Q54 a)`;
  if (!trustMsg && git('rev-parse', '--is-shallow-repository').stdout?.trim() === 'true') trustMsg = 'the repo is a shallow clone; seats and past seats are read from the full history, so fetch it (git fetch --unshallow) before the check (Q54)';
  return trustMsg;
}
// TRIAL-K6 findings 1, 2, Q56 (decided by KERNEL pass 8, builder lane): every history walk that looks for seat lines or trial
// content uses these flags. -a --no-textconv: a `-diff`/`binary` line in .gitattributes or .git/info/attributes, or a textconv
// driver, cannot hide text (K21, K22). --full-history: at a merge git walks every parent, so a side branch cannot drop the
// commit that added a seat or a trial (K25, K26). -m: a merge's own changes are listed too. --no-abbrev: full ids only.
// --root (TRIAL-K7 finding 2, Q59): a root commit's adds are listed even if log.showRoot is set false.
const HIST = ['-a', '--no-textconv', '--no-ext-diff', '--full-history', '-m', '--root', '--no-abbrev', '--no-renames', '--no-color'];
// TRIAL-K9 finding 3, Q65 (decided by KERNEL pass 11, builder lane: option A). Without -z git C-quotes a path with `"`, a
// backslash, a control byte or (core.quotePath) a non-ASCII byte, so a quoted path never matched an unquoted target. Every
// walk that lists paths runs `--raw -z` and is read here: a header token `C <sha>[ <parents>]` from --format, then per file a
// meta token `:<old mode> <new mode> <old blob> <new blob> <status>` and a path token, each ended by NUL. With --no-renames each
// change has one path. A header token may start with a newline; a path token is taken as it is.
function rawZ(out) {
  const rows = []; let head = null;
  const t = out.split('\0');
  for (let i = 0; i < t.length; i++) {
    const x = t[i].replace(/^\n+/, '');
    if (x.startsWith('C ')) { head = x; continue; }
    const m = /^:(\d+) (\d+) ([0-9a-f]{40}) ([0-9a-f]{40}) ([A-Z])\d*$/.exec(x);
    if (m && i + 1 < t.length) rows.push({ head, oldMode: m[1], mode: m[2], blob: m[4], status: m[5], path: t[++i] });
  }
  return rows;
}
// ls-tree -z / ls-files -s -z entries: `<mode> <type or blob> <...>\t<path>` ended by NUL.
const lsZ = (r) => (r.status === 0 ? r.stdout.split('\0').filter(Boolean).map((l) => { const i = l.indexOf('\t'); return { meta: l.slice(0, i).split(' '), path: l.slice(i + 1) }; }) : []);
function gitShow(commit, path) {
  if (!hasGit()) return undefined; // no repo here: nothing can be verified, and the caller makes that an error
  const r = git('cat-file', 'blob', `${commit}:${path}`); // Q56: cat-file reads the object; no attribute or textconv applies
  return r.status === 0 ? r.stdout : null;
}
// TRIAL-K5 finding 1 and 4, Q53 A, Q54 c (partly): the cited trial blob must be the version of the file that the trial lane
// added (the oldest commit reachable from HEAD that adds the path), so a PASS line added in a later edit of a real trial (H5)
// cannot be cited. Later edits (a fix-pass appendix) are allowed but not citable. The adding commit must touch only
// docs/trial/ and kernel/QUESTIONS.md, as every real trial commit does; a builder commit cannot also add a trial.
// Returns { commit } or { err }.
// TRIAL-K6 finding 2b, Q56 (K25): with --full-history every commit on HEAD's history that adds the path is seen, whichever
// parent a merge takes. All of them must add the same blob; two different added blobs mean one is a copy brought in by a merge
// (or a re-add), and git cannot say which is the lane's, so the seat is blocked. This does not depend on commit dates.
// The adding commit that passes the touch rule must be a plain commit (a trial lane never adds its file in a merge).
function trialOrigin(path, tblob) {
  const r = git('log', ...HIST, '--format=C %H %P', '--raw', '-z', '--diff-filter=A', 'HEAD', '--', path); // Q65: -z
  if (r.status !== 0) return { err: `git log could not read the history of ${path}` };
  let commit = null, merge = false, parents = [];
  const adds = [];
  // TRIAL-K7 finding 2, Q59 (KERNEL pass 9): a root commit has no parents, so `%P` is empty and the line is `C <sha> ` with a
  // trailing space. It is parsed like any other commit; an add seen before any readable header blocks the seat with a message.
  let lastHead;
  for (const row of rawZ(r.stdout)) {
    if (row.head !== lastHead) {
      lastHead = row.head;
      const c = row.head && /^C ([0-9a-f]{40})((?: [0-9a-f]{40})*) *$/.exec(row.head);
      if (c) { commit = c[1]; parents = c[2].trim().split(/ +/).filter(Boolean); merge = parents.length > 1; } else commit = null;
    }
    const m = row.status === 'A' ? [null, row.blob, row.path] : null;
    // Q59 (KERNEL pass 9): with -m a merge is diffed against each parent, so merging an unrelated (orphan) history lists every
    // file as added against the orphan side. A merge only carries a blob that one of its parents already holds at this path;
    // that add is the parent's, and --full-history walks it, so it is not counted again. A merge that brings a blob no parent
    // has (an evil merge) is still an add.
    if (m && m[2] === path && !(merge && parents.some((p) => git('rev-parse', '--verify', '-q', `${p}:${path}`).stdout.trim() === m[1])))
      adds.push({ commit, blob: m[1], merge });
  }
  if (!adds.length) return { err: `no commit reachable from HEAD adds ${path}; the seat is blocked (R2; TRIAL-K5 finding 1)` };
  if (adds.some((a) => !a.commit)) return { err: `git log listed an add of ${path} under a commit header the builder could not read, so its origin cannot be verified; the seat is blocked (TRIAL-K7 finding 2, Q59)` };
  const blobs = [...new Set(adds.map((a) => a.blob))];
  if (blobs.length > 1) return { err: `trial ${path} is added more than once on HEAD's full history with different blobs (${blobs.join(', ')}; commits ${[...new Set(adds.map((a) => a.commit.slice(0, 12)))].join(', ')}); a merge can bring in an edited copy, so the seat is blocked (TRIAL-K6 finding 2, Q56)` };
  const added = adds[adds.length - 1]; // log is newest first; the last one seen is the oldest add
  if (added.blob !== tblob) return { err: `trial ${path} was added at blob ${added.blob} (commit ${added.commit.slice(0, 12)}), not ${tblob}; a seat cites the trial as its lane wrote it, and later edits cannot add a PASS (TRIAL-K5 finding 4, Q54 c)` };
  let why = '';
  for (const a of adds.filter((x) => !x.merge)) {
    // Q59: diff-tree --root lists a root commit's files against the empty tree, so a root commit that adds only the trial
    // (and kernel/QUESTIONS.md) is an origin like any other first add; one that adds anything else is refused below.
    const t = git('diff-tree', '--root', '-r', '-z', '--no-commit-id', '--name-only', '--no-renames', a.commit);
    const stray = t.status === 0 ? t.stdout.split('\0').filter((x) => x && !x.startsWith('docs/trial/') && x !== 'kernel/QUESTIONS.md') : ['(unreadable)'];
    if (!stray.length) return { commit: a.commit };
    why = `the commit that added trial ${path} (${a.commit.slice(0, 12)}) also changes ${stray.slice(0, 3).join(', ')}; a trial commit touches only docs/trial/ and kernel/QUESTIONS.md (TRIAL-K5 finding 4, Q54 c)`;
  }
  return { err: why || `trial ${path} is added only by a merge commit (${added.commit.slice(0, 12)}); a trial lane adds its file in a plain commit (TRIAL-K6 finding 2, Q56)` };
}
// A trial PASS list written before TRIAL-K4 names a short blob prefix (kernel-trial-2.md:25-26). A prefix alone can be
// forged (TRIAL-K4 HM), so the full seat blob must also be the blob of this face's file in the trial commit's tree.
function inTrialTree(commit, spot, blob) {
  const r = git('ls-tree', '-r', '-z', commit); // Q65: -z
  if (r.status !== 0) return false;
  return lsZ(r).some(({ meta, path }) => { const name = path.split('/').pop(); return meta[1] === 'blob' && meta[2] === blob && (name === `${spot}.md` || name.startsWith(`${spot}.`) && /^[a-z]+\.md$/.test(name.slice(spot.length + 1))); });
}
export function passList(text) {
  const out = new Map(); let inPass = false;
  for (const line of text.split('\n')) {
    if (/^\*\*PASS\b/.test(line)) { inPass = true; continue; }
    if (!inPass) continue;
    const m = /^- `([^`]+)` \(blob `([0-9a-f]{7,40})`\)/.exec(line);
    if (m) out.set(m[1], m[2]);
    else if (line.trim() !== '' || out.size) inPass = false;
  }
  return out;
}
// TRIAL-K7 finding 1 (T18c), Q58 B: the seated bytes must be the bytes git holds. The face must be a regular file (mode
// 100644) in git whose blob is the seat blob: at HEAD under --check, and in the index (else HEAD) when writing, so a seat can be
// built before its commit. A symlink (120000), an untracked path or a different blob is an error.
// TRIAL-K8 finding 2, Q62 (1) (decided by KERNEL pass 10): the same rule holds for a face 00 that carries a seat record; its
// `want` is the blob of the bytes on disk, so face 00 must be committed (or, when writing, staged) exactly as read.
function gitEntry(rel, want, what = 'seated face', wantIs = 'the seat blob', why = 'the seated bytes must be the committed bytes') {
  const parse = (r, re) => (r.status === 0 ? r.stdout.split('\n').map((l) => re.exec(l)).find(Boolean) : null);
  const head = parse(git('--literal-pathspecs', 'ls-tree', '--full-tree', 'HEAD', '--', rel), /^(\d+) \w+ ([0-9a-f]{40})\t/);
  const idx = CHECK ? null : parse(git('--literal-pathspecs', 'ls-files', '-s', '--', rel), /^(\d+) ([0-9a-f]{40}) \d\t/);
  const e = idx || head;
  if (!e) return `${what} ${rel} is not in git (untracked; not at HEAD${CHECK ? '' : ' or in the index'}), so its ${what === 'seated face' ? 'seated bytes are' : 'seat records are'} not in the committed tree; commit it (R2; TRIAL-K7 finding 1, Q58; TRIAL-K8 finding 2, Q62)`;
  if (e[1] !== '100644') return `${what} ${rel} is mode ${e[1]} in git${idx ? ' (index)' : ' (HEAD)'}, not a regular file (100644); a symlink's blob is its link text, not the face (R2; TRIAL-K7 finding 1, Q58)`;
  if (e[2] !== want) return `${what} ${rel} is blob ${e[2]} in git${idx ? ' (index)' : ' (HEAD)'}, not ${wantIs} ${want}; ${why} (R2; TRIAL-K7 finding 1, Q58; TRIAL-K8 finding 2, Q62)`;
  return null;
}
function verifySeat(f, seat) {
  const blob = blobOf(f.body);
  if (seat.blob.length !== 40) return `seat blob ${seat.blob} is a short prefix; a seat pins the full 40-hex git blob (${blob} for this file now) and a prefix can be forged (TRIAL-K4 finding 1, Q52 a)`;
  if (blob !== seat.blob) return `seated face changed since its trial: blob ${blob} is not ${seat.blob} (R2, axiom 9); write it as FF.draft and re-trial`;
  if (!hasGit()) return `no git repo at ${ROOT}, so this seat cannot be verified; the seat is blocked (TRIAL-K4 finding 5, Q52 d)`;
  if (gitTrust()) return gitTrust();
  if (seat.by === 'director') {
    if (seat.kind !== 'ruling' || !/^R\d+$/.test(seat.ref)) return `seat says approved-by: director but gives no ruling id (ruling: R<n>); only the Director approves, and this cannot be verified, so the seat is blocked (R2; TRIAL-K3 finding 2)`;
    // TRIAL-K4 finding 2: the committed rulings file at HEAD, not the working tree, and a line that names the face and a seat.
    const text = gitShow('HEAD', 'docs/spec/DIRECTOR-RULINGS.md') || '';
    const sec = text.split(/^## /m).find((x) => new RegExp(`^${seat.ref}\\b|\\b${seat.ref} to R\\d+\\b|\\*\\*${seat.ref} `).test(x));
    if (!sec) return `seat cites ${seat.ref}, which is not in DIRECTOR-RULINGS.md as committed at HEAD; the seat is blocked (TRIAL-K3 finding 2, TRIAL-K4 finding 2)`;
    if (!sec.split('\n').some((l) => l.includes(f.spot) && /\bseat/i.test(l))) return `seat cites ${seat.ref}, but that ruling does not name ${f.spot} in a seat approval; a director seat cannot be verified, so it is blocked (TRIAL-K3 finding 2, TRIAL-K4 finding 2)`;
    return gitEntry(f.rel, seat.blob); // Q58: checked last, so the trial or ruling error is the one reported
  }
  if (seat.kind !== 'trial') return `a build-stage (R2) seat must cite trial: docs/trial/<file>.md blob <40 hex> (R2)`;
  if (/^docs\/trial\/[\w.\-]+\.md@[0-9a-f]{7,40}$/.test(seat.ref)) return `seat trial ${seat.ref} cites a commit id, which changes in the filter-branched published copy; re-pin it as trial: ${seat.ref.split('@')[0]} blob <the trial file's 40-hex blob> (TRIAL-K5 finding 1, Q53)`;
  const m = /^(docs\/trial\/[\w.\-]+\.md) blob ([0-9a-f]{7,40})$/.exec(seat.ref);
  if (!m) return `seat trial ${seat.ref} is not docs/trial/<file>.md blob <40 hex> (R2; TRIAL-K3 finding 2; Q53)`;
  if (m[2].length !== 40) return `seat trial blob ${m[2]} is a short prefix; cite the trial file's full 40-hex blob (TRIAL-K5 finding 1, Q53)`;
  const file = join(ROOT, m[1]);
  if (linkIn(file)) return `seat cites trial ${m[1]}, and that path is or goes through a symlink; the builder follows no link (TRIAL-K7 finding 1, Q58)`;
  if (!existsSync(file)) return `seat cites trial ${m[1]}, which does not exist; the seat is blocked (R2; TRIAL-K3 finding 2)`;
  const origin = trialOrigin(m[1], m[2]);
  if (origin.err) return `seat cites trial ${seat.ref}: ${origin.err}`;
  const text = git('cat-file', 'blob', m[2]);
  if (text.status !== 0 || blobOf(text.stdout) !== m[2]) return `seat cites trial ${m[1]} at blob ${m[2]}, which git cannot read back as that blob; the seat is blocked (R2; TRIAL-K5 finding 2)`;
  const passed = passList(text.stdout).get(f.spot);
  if (!passed) return `seat cites trial ${seat.ref}, but its PASS list does not name ${f.spot}; the seat is blocked (R2; TRIAL-K3 finding 2)`;
  if (passed.length === 40) { if (passed !== blob) return `trial ${seat.ref} passed ${f.spot} at blob ${passed}, not this blob ${blob}; re-trial (R2, axiom 9)`; }
  else if (!blob.startsWith(passed) || !inTrialTree(origin.commit, f.spot, blob)) return `trial ${seat.ref} lists ${f.spot} by the short prefix ${passed}, and blob ${blob} is not this face's file in the commit that added the trial; a prefix alone can be forged, re-trial (R2, axiom 9; TRIAL-K4 finding 1)`;
  return gitEntry(f.rel, seat.blob); // Q58: checked last, so the trial or ruling error is the one reported
}

// TRIAL-K3 finding 11: a face seated in the last build (books/) that is no longer seated needs an un-seat record:
// `unseat-NN:` on the registry (face 00 itself: `unseat-00:` in the stamp), giving the reason and the old blob.
// 7: the last build in books/ is the record of past seats (where an un-seat record lives is the build's own choice, Q34).
// TRIAL-K4 finding 6: read as committed at HEAD (git show HEAD:books/...), so deleting or editing books/ hides nothing.
// TRIAL-K5 finding 3, Q54 b (taken by KERNEL pass 7): HEAD:books/ is one snapshot, and a committed books edit hid an un-seat
// (H11). Past seats are also read from history: every `seat-NN:` (or stamp `seat-00:`) line ever added to a face 00 file under
// kernel/ on HEAD's history. A face seated there and not seated now needs an un-seat record naming its newest seated blob.
// TRIAL-K6 findings 1, 2a, Q56 (KERNEL pass 8): the walk lists every face 00 blob ever committed under kernel/ (`--raw`, with
// HIST: attributes cannot blind it, K21/K22, and a merge cannot drop a parent, K26) and reads each blob with `git cat-file
// --batch`, which applies no attributes or textconv. Seat lines are parsed from the blobs themselves, not from a `-G` diff.
const FACE00 = /^(\d{2}\.\d{2}\.\d{2}\.\d{4}|00\.00\.axioms)\.00(?:\.[a-z]+)?\.md$/;
// TRIAL-K9 finding 1, Q63 (decided by KERNEL pass 11, builder lane): a past seat is read only from structured fields, the way
// the live build reads one: a `seat-NN:` field line in the field block of a `## Registry` card (every such card, every such
// line, duplicates kept), and `seat-00:` in the front-matter stamp. A `seat-NN:` line in prose, below the field block, or a
// stamp `seat-NN:` other than seat-00, is never a seat (D1, D2). `seatFields` is also used on the live face 00 (validate).
const SEAT_VAL = /^\s*(?:seated;\s*)?approved-by: (build-stage \(R2\)|director);.*; blob: ([0-9a-f]{7,40})\s*$/;
export function seatFields(text) {
  const out = []; // [where, key, value]: where is 'stamp', 'registry', 'unseat-stamp' or 'unseat' (an `unseat-NN:` field)
  const fm = /^---\n([\s\S]*?)\n---\n/.exec(text);
  if (fm) for (const l of fm[1].split('\n')) { const m = /^(un)?seat-(\d{2}(?:\.\d{2})?):\s*(.*)$/.exec(l); if (m) out.push([m[1] ? 'unseat-stamp' : 'stamp', m[2], m[3]]); }
  let fence = false, inFields = false;
  for (const line of text.split('\n')) { // the card rules of parseCards: `##` outside fences, fields until a blank or non-field line
    if (/^(```|~~~)/.test(line)) fence = !fence;
    if (!fence && /^## /.test(line)) { inFields = keyOf(line.slice(3)) === 'registry'; continue; }
    if (!inFields) continue;
    if (line.trim() === '') { inFields = false; continue; }
    const m = /^([A-Za-z][\w.\- ]*?):\s?(.*)$/.exec(line);
    if (!m) { inFields = false; continue; }
    const k = /^(un)?seat-(\d{2}(?:\.\d{2})?)$/.exec(m[1]);
    if (k) out.push([k[1] ? 'unseat' : 'registry', k[2], m[2]]);
  }
  return out;
}
// Past seats in one face 00 blob: key -> set of blobs (registry `seat-NN:` for NN != 00, stamp `seat-00:`). A blob that also
// holds the un-seat record for a key is the retiring version: its old seat line (kept beside the record) is not the last seat,
// so the seat being retired is read from the versions before it (D2).
function blobSeats(text) {
  const out = new Map();
  const f = seatFields(text);
  const retiring = new Set(f.filter(([w, k]) => w === 'unseat' && k !== '00' || w === 'unseat-stamp' && k === '00').map(([, k]) => k));
  for (const [where, key, val] of f) {
    if (where !== 'stamp' && where !== 'registry') continue;
    if ((key === '00') !== (where === 'stamp')) continue; // the live parser reads seat-00 only from the stamp, others only from the registry
    if (retiring.has(key)) continue;
    const m = SEAT_VAL.exec(val); if (!m) continue;
    (out.get(key) || out.set(key, { by: m[1], blobs: new Set() }).get(key)).blobs.add(m[2]);
  }
  return out;
}
function catBlobs(ids) {
  const out = new Map();
  if (!ids.length) return out;
  const r = spawnSync('git', ['--no-replace-objects', '-C', ROOT, 'cat-file', '--batch'], { input: ids.join('\n') + '\n', maxBuffer: 1 << 28, env: GIT_ENV });
  if (r.status !== 0) return null;
  const buf = r.stdout; let i = 0;
  while (i < buf.length) {
    const nl = buf.indexOf(10, i); if (nl < 0) return null;
    const [id, type, size] = buf.slice(i, nl).toString('utf8').split(' ');
    if (type !== 'blob') return null;
    const n = Number(size);
    out.set(id, buf.slice(nl + 1, nl + 1 + n).toString('utf8'));
    i = nl + 1 + n + 1;
  }
  return out;
}
// TRIAL-K7 finding 1, Q58 (KERNEL pass 9): belt and braces behind the symlink refusal. A symlink ever committed under kernel/
// (a face 00 file, a book folder, or kernel/samples itself) is followed in history: its link text names a repo path, and that
// path's history is walked too, so seat lines written through a link (T18 docs/x/f00.md, T18b kernel/parked/...) are found.
// A target under a linked folder is read even under /parked/. Targets are added in rounds until no new link appears, and the
// final walk is one `git log` over every path, so the newest-first order holds across them.
// TRIAL-K8 finding 1, Q61 (decided by KERNEL pass 10: cover the shapes, not best-effort). Three blind spots are closed:
//   H1, a link at `kernel` itself: the walk's pathspec is `kernel` (no slash), which names the path `kernel` and all below it;
//   H2, an absolute link (or a relative one that climbs out of the repo): the link text cannot be resolved against a clone
//       that sits elsewhere, so every tail of its path (`/tmp/x/docs/f.md` -> `tmp/x/docs/f.md`, `x/docs/f.md`, `docs/f.md`,
//       `f.md`) is walked as a repo path; a tail that never existed in the repo matches nothing;
//   H5, a link to a link: a link found at a target carries that target's page (a face 00 link's page) to its own target, for
//       any number of hops up to the round limit.
// A link to the repo root (or `/`) makes the root a linked folder: the walk then reads every face 00 name in the whole history.
// TRIAL-K9 finding 3, Q65 (KERNEL pass 11): paths are read from `--raw -z` output, so a target with `"`, a backslash, a control
// byte or a non-ASCII (UTF-8) letter is matched as written.
// Not followed (still): a link inside a submodule (mode 160000; its files are another repo); a seat line in a file git never
// held (the books/ history below, Q62, is the backup, and only if a book recording the seat was committed); link text with
// Windows `\` separators (read as one file name, as Linux reads it); a path name that is not valid UTF-8 (git's bytes are
// read as UTF-8, so the target named back to git may not match); a chain longer than 16 hops stops the build (fail closed).
function linkTargets(path, raw) {
  const tails = (rest) => { const parts = rest.split('/').filter((x) => x && x !== '.'); return parts.length ? parts.map((_, i) => parts.slice(i).join('/')) : ['.']; };
  if (raw.startsWith('/')) return tails(posix.normalize(raw));
  const t = posix.normalize(posix.join(posix.dirname(path), raw)).replace(/\/+$/, '');
  if (t === '..' || t.startsWith('../')) return tails(t.replace(/^(\.\.\/)+/, '').replace(/^\.\.$/, ''));
  return [t === '' ? '.' : t];
}
function historySeats() {
  const out = new Map();
  const fail = (why = 'git log could not read the history of seat lines') => { err('kernel', `${why}, so un-seats cannot be checked (TRIAL-K5 finding 3, Q54 b; Q56; Q58; Q61; Q65)`); return out; };
  const targets = new Map(); // repo path a link pointed at -> page of the linked face 00, or '' for a linked folder ('.' is the root)
  const linkText = new Map();
  let rows;
  for (let round = 0; ; round++) {
    const specs = targets.has('.') ? [] : ['--', 'kernel', ...targets.keys()]; // Q61: `kernel`, not `kernel/` (H1); root: no pathspec
    const r = git('--literal-pathspecs', 'log', ...HIST, '--raw', '-z', '--format=C %H', 'HEAD', ...specs); // Q65: -z
    if (r.status !== 0) return fail();
    rows = rawZ(r.stdout).filter((x) => 'AMT'.includes(x.status) && x.mode !== '160000');
    const links = rows.filter((x) => x.mode === '120000');
    const need = [...new Set(links.map((x) => x.blob))].filter((b) => !linkText.has(b));
    if (need.length) { const t = catBlobs(need); if (!t) return fail(); for (const [b, v] of t) linkText.set(b, v); }
    let added = false;
    for (const { path, blob } of links) {
      const raw = (linkText.get(blob) || '').replace(/\n$/, '');
      if (!raw) continue;
      const n = FACE00.exec(path.split('/').pop());
      const page = targets.get(path) || (n ? n[1] : ''); // Q61 (H5): a link at a face 00 target carries that page on
      for (const t of linkTargets(path, raw)) {
        if (!targets.has(t)) { targets.set(t, page); added = true; }
        else if (page && !targets.get(t)) { targets.set(t, page); added = true; }
      }
    }
    if (!added) break;
    if (round >= 16) return fail('a symlink chain in history is longer than 16 hops (the round limit)');
  }
  const folders = [...targets].filter(([, v]) => v === '').map(([k]) => (k === '.' ? '' : k + '/'));
  const seen = []; // [page, blob] newest first
  for (const { mode, blob, path } of rows) {
    if (mode === '120000') continue;
    const viaFolder = folders.some((f) => path.startsWith(f));
    if (targets.get(path)) seen.push([targets.get(path), blob]); // a file a face 00 link pointed at (T18)
    if (!path.startsWith('kernel/') && !viaFolder) continue;
    if (!viaFolder && path.includes('/parked/')) continue; // kernel/parked is not built (R21); its pages are never seated
    const n = FACE00.exec(path.split('/').pop());
    if (n) seen.push([n[1], blob]);
  }
  const text = catBlobs([...new Set(seen.map((x) => x[1]))]);
  if (!text) return fail();
  // Q63: log is newest first, so the first blob that holds a structured seat for an address gives its last seat (every blob that
  // blob's fields name for it). A newer blob with only prose or a stamp `seat-NN:` line gives none, so it cannot set the blob.
  for (const [page, b] of seen)
    for (const [key, v] of blobSeats(text.get(b))) {
      const addr = `${page}.${key}`;
      if (!out.has(addr)) out.set(addr, { addr, by: v.by, blobs: [...v.blobs].map((x) => [x, 'face 00 history']) });
    }
  return out;
}
function priorSeats() {
  const out = [];
  if (!hasGit()) { err('books', `no git repo at ${ROOT}, so past seats cannot be read from HEAD:books/ and un-seats cannot be checked (TRIAL-K4 findings 5, 6; Q52 b, d)`); return out; }
  if (gitTrust()) { err('books', gitTrust()); return out; }
  // Q58: a symlink committed (or staged) anywhere the builder reads hides its target from git's view of these paths.
  const isBook = (p) => /^books\/[^/]+$/.test(p) && (p.endsWith('.book') || p === `books/${AXIOMS_FILE}`);
  for (const [where, r] of [['HEAD', git('ls-tree', '-r', '-z', '--full-tree', 'HEAD', '--', 'kernel', 'books', 'docs/trial', 'docs/spec')], ['index', git('ls-files', '-s', '-z', '--', 'kernel', 'books', 'docs/trial', 'docs/spec')]])
    for (const { meta, path } of lsZ(r)) {
      if (meta[0] === '120000') err(path, `is a symlink in git (${where}); the builder follows no link (R2; TRIAL-K7 finding 1, Q58)`);
      // TRIAL-K9 finding 2, Q64 (decided by KERNEL pass 11, builder lane: A and B): a current book is a regular file, 100644.
      else if (isBook(path) && meta[0] !== '100644') err(path, `is mode ${meta[0]} in git (${where}); a book file must be a regular 100644 file, because a book with another mode was skipped by the books/ history walk (TRIAL-K9 finding 2, Q64)`);
    }
  const hist = historySeats();
  // TRIAL-K8 finding 2 (H3), Q62 (2) (decided by KERNEL pass 10): past seats are also read from every version of every book file
  // ever committed under books/ on HEAD's history (HEAD's own first, then newest first), not only HEAD:books/. A seat built from
  // a face 00 that git never held still left its `approved-by` line in a committed book, so its un-seat needs a record too.
  // The walk uses HIST (attributes, textconv and merges hide nothing) and `git cat-file --batch` (no attributes apply).
  // Q64 (A): book blobs are read whatever their mode (100644, 100755, ...), only a gitlink (160000, not a blob) is skipped;
  // Q65: both lists are read with -z.
  const ids = [];
  for (const { meta, path } of lsZ(git('ls-tree', '-z', '--full-tree', 'HEAD', 'books/'))) if (meta[1] === 'blob' && isBook(path)) ids.push(meta[2]);
  const bh = git('--literal-pathspecs', 'log', ...HIST, '--raw', '-z', '--format=C %H', 'HEAD', '--', 'books');
  if (bh.status !== 0) { err('books', 'git log could not read the history of books/, so un-seats cannot be checked (TRIAL-K8 finding 2, Q62)'); return [...hist.values()]; }
  for (const x of rawZ(bh.stdout)) if ('AMT'.includes(x.status) && x.mode !== '160000' && isBook(x.path)) ids.push(x.blob);
  const order = [...new Set(ids)];
  const texts = catBlobs(order);
  if (!texts) { err('books', 'git cat-file could not read the books/ history, so un-seats cannot be checked (TRIAL-K8 finding 2, Q62)'); return [...hist.values()]; }
  // Q63: the newest book line with `approved-by` for an address (HEAD's books first, then newest first) gives its last built
  // seat. It is always read, not only when face 00 history has none, and joined to the face 00 history seat: an un-seat record
  // must name every one of these blobs, so a made-up seat line cannot replace the real one.
  const got = new Map();
  for (const id of order)
    for (const l of texts.get(id).split('\n')) {
      if (!l.trim()) continue;
      let e; try { e = JSON.parse(l); } catch { continue; }
      const ref = e.trial || e.ruling || '';
      if (typeof e.addr === 'string' && e['approved-by'] && !got.has(e.addr)) got.set(e.addr, { by: e['approved-by'], blob: (/face blob ([0-9a-f]+)/.exec(ref) || /blob ([0-9a-f]+)/.exec(ref) || [])[1] || '' });
    }
  for (const [addr, b] of got) {
    const h = hist.get(addr);
    if (!h) out.push({ addr, by: b.by, blobs: b.blob ? [[b.blob, 'books/ history']] : [] });
    else if (b.blob && !h.blobs.some(([x]) => x === b.blob)) h.blobs.push([b.blob, 'books/ history']);
  }
  return [...hist.values(), ...out];
}
function unseatChecks(books, prior) {
  const all = books.flatMap((b) => b.faces);
  for (const p of prior) {
    const now = all.find((x) => x.addr === p.addr && !x.tail);
    if (now) continue; // still seated (its record is checked in validate)
    const page = p.addr.startsWith(AXIOMS + '.') ? AXIOMS : p.addr.split('.').slice(0, 4).join('.');
    const key = p.addr.slice(page.length + 1);
    const f00 = all.find((x) => x.page === page && x.ff === '00' && !x.nn);
    const reg = f00 && f00.cards.find((c) => c.key === 'registry');
    const rec = f00 && (key === '00' ? stampOf(f00.body)['unseat-00'] : reg && reg.fields[`unseat-${key}`]);
    const blobs = p.blobs.map(([b]) => b);
    if (!rec || !rec.trim()) err(f00 ? f00.file : p.addr, `${p.addr} was seated (${p.by}) in the last build but is not now; write unseat-${key}: <reason>; was blob ${blobs.join(', blob ') || '(unknown)'} (R2: every seat can be found and re-reviewed; TRIAL-K3 finding 11)`);
    else {
      // TRIAL-K5 finding 5, Q54 d (taken by KERNEL pass 7): the record names the full old blob and gives a reason besides it.
      // TRIAL-K9 finding 1, Q63 (KERNEL pass 11): the old blob is the last real seat, from the structured seat fields of face 00
      // history and from books/ history; when they differ the record names each, so a made-up blob never satisfies it.
      // A last-seat blob that git does not hold as a blob was never a seated face (every seat is checked against the committed
      // face, Q58), so the seat line that gave it is made up; the un-seat cannot be checked and is refused (fail closed).
      for (const [b, src] of p.blobs) if (hasGit() && git('cat-file', '-e', `${b}^{blob}`).status !== 0) err(f00.file, `the last seat of ${p.addr} in ${src} names blob ${b}, which git does not hold, so that seat line is made up and the un-seat cannot be checked (TRIAL-K9 finding 1, Q63)`);
      const miss = p.blobs.filter(([b]) => !rec.includes(b));
      for (const [b, src] of miss) err(f00.file, `unseat-${key}: must name the full old blob ${b} (the last seat of ${p.addr} in ${src}; TRIAL-K3 finding 11; TRIAL-K5 finding 5; TRIAL-K9 finding 1, Q63)`);
      if (!miss.length && !/[a-z]{3,}/i.test(blobs.reduce((t, b) => t.split(b).join(' '), rec).replace(/\b(was|blob|and)\b/gi, ' '))) err(f00.file, `unseat-${key}: gives no reason; write unseat-${key}: <reason>; was blob ${blobs.join(', blob ')} (R2 re-review needs the reason; TRIAL-K5 finding 5)`);
    }
  }
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
    // R2: every seated face (no tail), face 00 and counters included (TRIAL-K3 finding 1; R22), needs a seat record
    // naming the trial (or Director ruling) and the exact blob, and the record is verified (TRIAL-K3 finding 2).
    for (const f of fs.filter((x) => !x.tail)) {
      const k = spotKey(f);
      if (f.nn && !SEATABLE_COUNTERS[f.ff]) err(f.file, `a ${f.ff} counter may not be seated: R22 allows only face 05 counters, and seating others is open (QUESTIONS Q35; R2 answers no open question; TRIAL-K4 finding 7); write it as ${f.ff}.${f.nn}.draft`);
      const where = k === '00' ? 'seat-00: in its stamp' : `seat-${k}: on the face 00 registry`;
      const raw = reg && reg.get(k);
      const seat = seatOf(reg, f);
      if (!seat) err(f.file, raw && raw !== 'seated; ' ? `seat record "${raw.replace(/^seated; /, '')}" is not in the R2 form; approved-by must be build-stage (R2) with trial:, or director with ruling: (R2; TRIAL-K3 finding 2)` : `seated face has no ${where} (R2: approved-by, trial, blob); write it as FF.draft`);
      else { const bad = verifySeat(f, seat); if (bad) err(f.file, bad); }
    }
    // TRIAL-K8 finding 2 (H3), Q62 (1) (decided by KERNEL pass 10): face 00 holds the seat lines, so a face 00 that carries any
    // seat record (a seated face on its page, a `seat-NN:` line, or a stamp `seat-00:`) must be the bytes git holds: HEAD under
    // --check, the index (else HEAD) when writing. An untracked or excluded face 00, or one edited and not committed (staged,
    // when writing), is an error, so a seat cannot be built from a face 00 that git never sees.
    const regCard = stamp.cards.find((c) => c.key === 'registry');
    // TRIAL-K9 finding 4, Q66 (decided by KERNEL pass 11, builder lane: option A): an `unseat-NN:` field, or a stamp `unseat-00:`,
    // is a seat record too, so a face 00 that holds only un-seat records is checked against git by the same rule.
    const carries = fs.some((f) => !f.tail) || (regCard && Object.keys(regCard.fields).some((k) => /^(un)?seat-/.test(k))) || st['seat-00'] !== undefined || st['unseat-00'] !== undefined;
    // TRIAL-K9 finding 1, Q63: the live face 00 states each seat once, in its structured place, for a face it lists as seated:
    // a repeated `seat-NN:` field, a `seat-NN:` for a face not listed as seated, or a stamp `seat-NN:` other than seat-00 is
    // an error, so no extra seat line can sit in face 00 waiting to be read as a past seat.
    const sf = seatFields(stamp.body), sk = new Set();
    const unseats = new Set(sf.filter(([w]) => w.startsWith('unseat')).map(([, k]) => k));
    for (const [where, key] of sf) {
      if (where.startsWith('unseat')) continue;
      if (where === 'stamp' && key !== '00') err(stamp.file, `stamp has seat-${key}:; a seat record for face ${key} lives on the registry, only seat-00: lives in the stamp (TRIAL-K9 finding 1, Q63)`);
      else if (where === 'registry' && key === '00') err(stamp.file, `registry has seat-00:; face 00's own seat record lives in the stamp (TRIAL-K9 finding 1, Q63)`);
      else if (sk.has(`${where} ${key}`)) err(stamp.file, `seat-${key}: is written more than once; a face has one seat record (TRIAL-K9 finding 1, Q63)`);
      else if (where === 'registry' && !unseats.has(key) && !(reg && reg.has(key) && reg.get(key).startsWith('seated;'))) err(stamp.file, `registry has seat-${key}:, but ${key} is not listed as seated in faces:; write unseat-${key}: <reason>; was blob <blob> to retire a seat (TRIAL-K9 finding 1, Q63)`);
      sk.add(`${where} ${key}`);
    }
    if (carries && hasGit() && !gitTrust()) { const bad = gitEntry(stamp.rel, blobOf(stamp.body), 'face 00', 'the bytes on disk', `face 00 carries seat records, so it must be ${CHECK ? 'committed' : 'committed or staged'} exactly as read`); if (bad) err(stamp.file, bad); }
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
          // Books: presence is checked across the lookup. The axioms sit outside any book (R6) and have no lookup,
          // so they are checked here, as at ed82086 (TRIAL-K3 finding 3).
          if (!w) { if (isAx) err(f.file, `card ${c.key} has no 04 card (C3.2)`); }
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
  if (!noLink(p)) return; // Q58
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
    if (!f.tail) {
      const seat = seatOf(regs.get(f.page), f);
      // Book field: trial "docs/trial/<file>.md blob <trial blob>; face blob <blob>", ruling "R<n> blob <blob>" (Q53).
      if (seat) { e['approved-by'] = seat.by; e[seat.kind] = seat.kind === 'trial' ? `${seat.ref}; face blob ${seat.blob}` : `${seat.ref} blob ${seat.blob}`; }
    }
    e.body = f.body.replace(/\n+$/, '');
    e.proposal = `${BY}:${f.page}`; // format.md section 3.3 proposal batches (proposed): a page arrives with its faces.
    lines.push(JSON.stringify(e));
  }
  const text = lines.join('\n') + '\n';
  checkAscii(address, text);
  return text;
}

const check = CHECK;
const books = sources().map(loadBook);
books.forEach(validate);
crossChecks(books);
unseatChecks(books, priorSeats());
lookupReport(books);
for (const f of findings) console.log('finding  ' + f);
for (const l of lookups) console.log('lookup   ' + l);
const outputs = books.map((b) => [join(OUT, b.isAx ? AXIOMS_FILE : `${b.book}.book`), render(b.faces, b.book)]);
// Q58: never read or write books/ through a link. Q64 (B): a book on disk with an exec bit is refused too, before git can stage it.
for (const [out] of outputs) if (noLink(out) && there(out) && (statSync(out).mode & 0o111)) err(out.slice(ROOT.length + 1), `is executable on disk (mode ${(statSync(out).mode & 0o777).toString(8)}); a book file must be a regular 100644 file (TRIAL-K9 finding 2, Q64)`);
for (const e of errors) console.error('ERROR    ' + e);
if (errors.length) { console.error(`${errors.length} errors; nothing written`); process.exit(1); }
if (!check) mkdirSync(OUT, { recursive: true });
let diff = 0;
for (const [out, text] of outputs) {
  if (check) { if (!existsSync(out) || readFileSync(out, 'utf8') !== text) { console.error(`differs: ${out}`); diff++; } }
  else writeFileSync(out, text);
  console.log(`${check ? 'checked' : 'wrote'}  ${out.slice(ROOT.length + 1)}  ${text.split('\n').length - 2} entries`);
}
// Seat count (KERNEL pass 7): every seated face (no tail) has a verified record by now, or the build stopped above.
const seated = books.flatMap((b) => b.faces).filter((f) => !f.tail);
console.log(`seats ${seated.length}`);
console.log(`${findings.length} findings, 0 errors`);
if (diff) process.exit(1);
