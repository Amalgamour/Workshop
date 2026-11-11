#!/usr/bin/env node
// Tests for kernel/build.mjs. Each test makes a scratch git clone of HEAD (no checkout; it shares history, so seat checks
// can reach trial commits, rulings and books at HEAD, TRIAL-K4 Q52), copies the working kernel/, docs/spec/, docs/trial/ and
// books/ into it, adds one hostile change, runs the builder there, and checks the result. The repo is never written.
// Usage: node kernel/build.test.mjs
import { mkdtempSync, cpSync, writeFileSync, readFileSync, rmSync, appendFileSync, renameSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
let failed = 0;

const sh = (d, args, opts = {}) => {
  const r = spawnSync('git', ['-C', d, ...args], { encoding: 'utf8', ...opts });
  if (r.status !== 0) throw new Error(`git ${args.join(' ')}: ${r.stderr}`);
  return r.stdout.trim();
};
function scratch() {
  const d = mkdtempSync(join(tmpdir(), 'kbuild-'));
  sh(ROOT, ['clone', '-q', '--shared', '--no-checkout', ROOT, d]);
  cpSync(HERE, join(d, 'kernel'), { recursive: true });
  cpSync(join(ROOT, 'docs', 'spec'), join(d, 'docs', 'spec'), { recursive: true });
  cpSync(join(ROOT, 'docs', 'trial'), join(d, 'docs', 'trial'), { recursive: true }); // seat records cite trials (TRIAL-K3 finding 2)
  cpSync(join(ROOT, 'books'), join(d, 'books'), { recursive: true }); // the last build is the record of past seats (TRIAL-K3 finding 11)
  return d;
}
const stamp = (addr, title, faces, whys) => `---\naddress: ${addr}\ntitle: ${title}\ntype: general\nstate: draft\nwhy-draft: test fixture\n---\n\n## Registry\nfaces: ${faces}\n${whys}\n`;
function run(name, setup, expect) {
  const d = scratch();
  try {
    setup(d);
    const r = spawnSync(process.execPath, [join(d, 'kernel', 'build.mjs')], { encoding: 'utf8' });
    const out = r.stdout + r.stderr;
    const ok = expect.ok ? r.status === 0 : r.status !== 0 && expect.match.test(out);
    console.log(`${ok ? 'ok  ' : 'FAIL'}  ${name}`);
    if (!ok) { failed++; console.log(out.split('\n').filter((l) => /ERROR|errors/.test(l)).join('\n')); }
  } finally { rmSync(d, { recursive: true, force: true }); }
}
const S = (d, ...p) => join(d, 'kernel', 'samples', ...p);

run('baseline: the real sources build', () => {}, { ok: true });

// TRIAL-K2 finding 8 (a): a book face at a spot the kernel fills replaces it in place (R7, R21).
run('book face replacing a kernel face is flagged', (d) => {
  writeFileSync(S(d, '10.11.21', '10.11.21.0056.00.draft.md'), stamp('10.11.21.0056', 'drafting', '04 draft', 'why-04: test fixture'));
  writeFileSync(S(d, '10.11.21', '10.11.21.0056.04.draft.md'), '## never from memory\nsource: test; why: docs/spec/drafting.md:7\nwhy: A rewrite from memory silently drops what the model did not remember.\n\nlocal text\n');
}, { match: /10\.11\.21\.0056\.04\.draft\.md: replaces 00\.00\.00\.0056\.04 in place/ });

// TRIAL-K2 finding 8 (b): C3.2 is checked across the lookup. A book 01 card whose 04 is found up the chain passes ...
const desk1500 = (d) => {
  writeFileSync(S(d, '10.00.00', '10.00.00.1500.00.draft.md'), stamp('10.00.00.1500', 'shared', '04 draft', 'why-04: test fixture'));
  writeFileSync(S(d, '10.00.00', '10.00.00.1500.04.draft.md'), '## x\nsource: test; why: docs/spec/drafting.md:7\nwhy: A rewrite from memory silently drops what the model did not remember.\n\nwhy x exists\n');
};
run('C3.2 across the lookup: 04 found on the desk passes', (d) => {
  desk1500(d);
  writeFileSync(S(d, '10.11.21', '10.11.21.1500.00.draft.md'), stamp('10.11.21.1500', 'shared', '01 draft', 'why-01: test fixture'));
  writeFileSync(S(d, '10.11.21', '10.11.21.1500.01.draft.md'), '## x\n\nrule x\n');
}, { ok: true });
// ... and a book 01 card with no 04 card anywhere on the lookup fails.
run('C3.2 across the lookup: missing 04 card is flagged', (d) => {
  desk1500(d);
  writeFileSync(S(d, '10.11.21', '10.11.21.1500.00.draft.md'), stamp('10.11.21.1500', 'shared', '01 draft', 'why-01: test fixture'));
  writeFileSync(S(d, '10.11.21', '10.11.21.1500.01.draft.md'), '## z\n\nrule z\n');
}, { match: /card z has no 04 card on 10\.00\.00\.1500\.04\.draft across the lookup from 10\.11\.21 \(C3\.2\)/ });

// R21: no override pages while the app is built (finding 17 parked).
run('R21: an override page 0001-0009 is refused', (d) => {
  cpSync(join(HERE, 'parked', '10.11.21', '10.11.21.0001.04.draft.md'), S(d, '10.11.21', '10.11.21.0001.04.draft.md'));
  writeFileSync(S(d, '10.11.21', '10.11.21.0001.00.draft.md'), stamp('10.11.21.0001', 'override', '04 draft', 'why-04: test fixture'));
}, { match: /no override pages while the Workshop app is built/ });

// TRIAL-K2 finding 19: override statements outside 0001-0009.
run('R7: override fields outside 0001-0009 are refused', (d) => {
  writeFileSync(S(d, '10.11.21', '10.11.21.0020.00.draft.md'), stamp('10.11.21.0020', 'behavior', '04 draft', 'why-04: test fixture'));
  writeFileSync(S(d, '10.11.21', '10.11.21.0020.04.draft.md'), '## q\nchanging: x\nsource: test; why: docs/spec/drafting.md:7\nwhy: A rewrite from memory silently drops what the model did not remember.\n\nbody\n');
}, { match: /states an override outside 0001-0009 \(R7\)/ });

// TRIAL-K2 finding 18: a draft with no why gets the R5 message.
run('R5: a draft with no why-NN says so', (d) => {
  const f = S(d, '10.11.21', '10.11.21.0013.00.draft.md');
  writeFileSync(f, readFileSync(f, 'utf8').replace(/^why-01: .*\n/m, ''));
}, { match: /a draft must say why \(R5\): the registry has no why-01:/ });

// R2: a seated face that changed after its trial is refused.
run('R2: a seated face changed after its trial is refused', (d) => {
  appendFileSync(S(d, '10.11.21', '10.11.21.1001.01.md'), '\nedited\n');
}, { match: /seated face changed since its trial/ });

const blob = (t) => { const b = Buffer.from(t, 'utf8'); return createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${b.length}\0`), b])).digest('hex'); };
const edit = (f, a, b) => { const t = readFileSync(f, 'utf8'); if (!t.includes(a)) throw new Error(`fixture: ${a} not in ${f}`); writeFileSync(f, t.replace(a, b)); };

// TRIAL-K3 finding 1 (H1, H1b): renaming a face 00 draft to a seated file, with no seat record, fails.
run('R2: a face 00 seated with no seat-00 record is refused (H1)', (d) => {
  renameSync(S(d, '10.11.21', '10.11.21.1001.00.draft.md'), S(d, '10.11.21', '10.11.21.1001.00.md'));
}, { match: /10\.11\.21\.1001\.00\.md: seated face has no seat-00: in its stamp/ });
run('R2: a kernel face 00 seated with no record is refused (H1b)', (d) => {
  const k = (n) => join(d, 'kernel', '00.00.00', n);
  renameSync(k('00.00.00.0056.00.draft.md'), k('00.00.00.0056.00.md'));
}, { match: /00\.00\.00\.0056\.00\.md: seated face has no seat-00:/ });
// ... and a counter (R22 lets counters be seated) seated with no record fails too.
run('R2: a counter seated with no seat record is refused', (d) => {
  renameSync(S(d, '10.11.21', '10.11.21.0012.03.14.draft.md'), S(d, '10.11.21', '10.11.21.0012.03.14.md'));
  edit(S(d, '10.11.21', '10.11.21.0012.00.draft.md'), '03.14 draft', '03.14 seated');
}, { match: /10\.11\.21\.0012\.03\.14\.md: seated face has no seat-03\.14:/ });

// TRIAL-K4 finding 7 (HK): only face 05 counters may be seated (R22); a 06 note seated with a well-formed record is refused (Q35).
run('R22: seating a 06 note counter is refused (K4 HK)', (d) => {
  const k = (n) => join(d, 'kernel', '00.00.00', n);
  renameSync(k('00.00.00.0051.06.01.draft.md'), k('00.00.00.0051.06.01.md'));
  const b = blob(readFileSync(k('00.00.00.0051.06.01.md'), 'utf8'));
  edit(k('00.00.00.0051.00.draft.md'), '06.01 draft', '06.01 seated');
  edit(k('00.00.00.0051.00.draft.md'), '\n## Registry\n', `\n## Registry\nseat-06.01: approved-by: build-stage (R2); trial: docs/trial/kernel-trial-4.md@4b369fa; blob: ${b}\n`);
}, { match: /00\.00\.00\.0051\.06\.01\.md: a 06 counter may not be seated: R22 allows only face 05 counters/ });

// TRIAL-K3 finding 2 (H2): seat records are verified, not trusted.
const seat0013 = (d, rec) => {
  const f = S(d, '10.11.21', '10.11.21.0013.01.md');
  renameSync(S(d, '10.11.21', '10.11.21.0013.01.draft.md'), f);
  const r = S(d, '10.11.21', '10.11.21.0013.00.draft.md');
  edit(r, '01 draft', '01 seated');
  edit(r, '\n## Registry\n', `\n## Registry\nseat-01: ${rec(blob(readFileSync(f, 'utf8')))}\n`);
};
run('R2: a seat citing a trial file that does not exist is refused (H2)', (d) => {
  seat0013(d, (b) => `approved-by: build-stage (R2); trial: docs/trial/does-not-exist.md@0000000; blob: ${b}`);
}, { match: /cites trial docs\/trial\/does-not-exist\.md, which does not exist/ });
run('R2: a seat citing a real trial that did not pass the face is refused', (d) => {
  seat0013(d, (b) => `approved-by: build-stage (R2); trial: docs/trial/kernel-trial-3.md@d37e532; blob: ${b}`);
}, { match: /its PASS list does not name 10\.11\.21\.0013\.01/ });
run('R2: approved-by director with no ruling id is refused (H2)', (d) => {
  seat0013(d, (b) => `approved-by: director; trial: docs/trial/does-not-exist.md@0000000; blob: ${b}`);
}, { match: /approved-by: director but gives no ruling id/ });
run('R2: approved-by director citing a ruling that does not name the face is refused', (d) => {
  seat0013(d, (b) => `approved-by: director; ruling: R22; blob: ${b}`);
}, { match: /seat cites R22, but that ruling does not name 10\.11\.21\.0013\.01/ });
run('R2: an approved-by value other than build-stage (R2) or director is refused', (d) => {
  seat0013(d, (b) => `approved-by: prima; trial: docs/trial/kernel-trial-2.md@ed82086; blob: ${b}`);
}, { match: /is not in the R2 form/ });

// TRIAL-K3 finding 3 (H3): C3.2 on the axioms again (as at ed82086).
run('C3.2: an axioms 01 card with no 04 card is refused (H3)', (d) => {
  appendFileSync(join(d, 'kernel', '00.00.axioms', '00.00.axioms.01.draft.md'), '\n## ghost rule\n\nno why\n');
}, { match: /00\.00\.axioms\.01\.draft\.md: card ghost-rule has no 04 card \(C3\.2\)/ });

// TRIAL-K3 finding 11 (H7): un-seating a seated face needs a record ...
const unseat = (d) => {
  renameSync(S(d, '10.11.21', '10.11.21.1001.01.md'), S(d, '10.11.21', '10.11.21.1001.01.retired.md'));
  const r = S(d, '10.11.21', '10.11.21.1001.00.draft.md');
  edit(r, '01 seated', '01 retired');
  return r;
};
run('R2: retiring a seated face with no unseat record is refused (H7)', (d) => { unseat(d); },
  { match: /10\.11\.21\.1001\.01 was seated \(build-stage \(R2\)\) in the last build but is not now; write unseat-01:/ });
// ... and with one naming the old blob it builds.
run('R2: retiring a seated face with an unseat record builds', (d) => {
  const r = unseat(d);
  edit(r, '\n## Registry\n', '\n## Registry\nunseat-01: test fixture retirement; was blob 5415cef2 (TRIAL-K2)\n');
}, { ok: true });

// TRIAL-K4 finding 1 (Q52 a): a seat pins the full blob. A short prefix in a seat line is refused ...
run('R2: a seat line with a short blob prefix is refused (K4 finding 1)', (d) => {
  edit(S(d, '10.11.21', '10.11.21.1001.00.draft.md'), 'blob: 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d', 'blob: 5415cef2');
}, { match: /seat blob 5415cef2 is a short prefix; a seat pins the full 40-hex git blob/ });
// ... and a prefix collision forge (HM) fails: the seated law is changed and its seat re-pinned to the new full blob, and a
// trial committed on the branch lists the new blob by its 8-hex prefix, as a forged collision would match the old prefix.
// The full blob is not this face's file in that trial's commit, so the seat is refused.
const commitOnHead = (d, path, text) => {
  const env = { ...process.env, GIT_INDEX_FILE: join(d, '.git', 'k6-index'), GIT_AUTHOR_NAME: 't', GIT_AUTHOR_EMAIL: 't@t', GIT_COMMITTER_NAME: 't', GIT_COMMITTER_EMAIL: 't@t' };
  const b = sh(d, ['hash-object', '-w', '--stdin'], { input: text, env });
  sh(d, ['read-tree', 'HEAD'], { env });
  sh(d, ['update-index', '--add', '--cacheinfo', `100644,${b},${path}`], { env });
  const c = sh(d, ['commit-tree', sh(d, ['write-tree'], { env }), '-p', 'HEAD', '-m', 'forged'], { env });
  return c;
};
run('R2: a prefix-collision forge of a seated face is refused (K4 HM)', (d) => {
  const f = join(d, 'kernel', '00.00.00', '00.00.00.0056.01.md');
  edit(f, 'is calculated and never drafted.', 'may be rewritten from memory when a model is confident.');
  const nb = blob(readFileSync(f, 'utf8'));
  const trial = `# forged\n\n**PASS list:**\n- \`00.00.00.0056.01\` (blob \`${nb.slice(0, 8)}\`)\n`;
  writeFileSync(join(d, 'docs', 'trial', 'forged.md'), trial);
  const c = commitOnHead(d, 'docs/trial/forged.md', trial);
  sh(d, ['update-ref', 'HEAD', c]);
  edit(join(d, 'kernel', '00.00.00', '00.00.00.0056.00.draft.md'), 'kernel-trial-2.md@ed82086; blob: 112c169ccd06d54c6d9ab607fee6c2d16004cc62', `forged.md@${c}; blob: ${nb}`);
}, { match: /lists 00\.00\.00\.0056\.01 by the short prefix [0-9a-f]{8}, and blob [0-9a-f]{40} is not this face's file in commit/ });
// TRIAL-K4 finding 2 (HG, Q52 b): a ruling appended to the working-tree rulings file and never committed does not seat.
run('R2: a director seat citing an uncommitted ruling is refused (K4 HG)', (d) => {
  appendFileSync(join(d, 'docs', 'spec', 'DIRECTOR-RULINGS.md'), '\n## R23 - fake\nDirector approves the seat of 10.11.21.0013.01.\n');
  seat0013(d, (b) => `approved-by: director; ruling: R23; blob: ${b}`);
}, { match: /seat cites R23, which is not in DIRECTOR-RULINGS\.md as committed at HEAD/ });
// TRIAL-K4 finding 4 (HA, Q52 c): a trial committed off the branch (not an ancestor of HEAD) does not seat.
run('R2: a seat citing a trial commit not on the branch is refused (K4 finding 4)', (d) => {
  const t = (b) => `# forged\n\n**PASS list:**\n- \`10.11.21.0013.01\` (blob \`${b}\`)\n`;
  const b = blob(readFileSync(S(d, '10.11.21', '10.11.21.0013.01.draft.md'), 'utf8'));
  writeFileSync(join(d, 'docs', 'trial', 'forged.md'), t(b));
  const c = commitOnHead(d, 'docs/trial/forged.md', t(b)); // a child of HEAD; HEAD is not moved
  seat0013(d, (bb) => `approved-by: build-stage (R2); trial: docs/trial/forged.md@${c}; blob: ${bb}`);
}, { match: /which is not an ancestor of HEAD/ });
// TRIAL-K4 finding 5 (HC, Q52 d): with no git, a seat cannot be verified, so it is an error, not a finding.
run('R2: with no git a seat is an error (K4 finding 5)', (d) => {
  rmSync(join(d, '.git'), { recursive: true, force: true });
}, { match: /00\.00\.00\.0056\.01\.md: no git repo at .*so this seat cannot be verified/ });
// TRIAL-K4 finding 6 (HI, Q52 b): past seats come from HEAD:books/, so deleting books/ does not hide an un-seat.
run('R2: retiring a seated face after deleting books/ is still refused (K4 HI)', (d) => {
  rmSync(join(d, 'books'), { recursive: true, force: true });
  unseat(d);
}, { match: /10\.11\.21\.1001\.01 was seated \(build-stage \(R2\)\) in the last build but is not now/ });

if (failed) { console.log(`${failed} failed`); process.exit(1); }
console.log('all passed');
