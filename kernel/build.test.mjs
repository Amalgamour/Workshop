#!/usr/bin/env node
// Tests for kernel/build.mjs. Each test makes a scratch git clone of HEAD (no checkout; it shares history, so seat checks
// can reach trial commits, rulings and books at HEAD, TRIAL-K4 Q52), copies the working kernel/, docs/spec/, docs/trial/ and
// books/ into it, adds one hostile change, runs the builder there, and checks the result. The repo is never written.
// Usage: node kernel/build.test.mjs
import { mkdtempSync, mkdirSync, cpSync, writeFileSync, readFileSync, rmSync, appendFileSync, renameSync, symlinkSync } from 'node:fs';
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
// opts.scratch makes the scratch copy (default: scratch()); opts.env adds to the builder's environment (TRIAL-K5 H15).
function run(name, setup, expect, opts = {}) {
  const d = (opts.scratch || scratch)();
  try {
    setup(d);
    const r = spawnSync(process.execPath, [join(d, 'kernel', 'build.mjs')], { encoding: 'utf8', env: { ...process.env, ...(opts.env ? opts.env(d) : {}) } });
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

// Trial file blobs as their lanes added them (Q53: a seat cites the trial by path and blob, not by commit).
const T2 = 'da5d51424fee3bea1d8443c619fcba3c534a1ace', T4 = 'a5d253d5e12722956afea38e79cb7fc1cf492c7b';
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
  edit(k('00.00.00.0051.00.draft.md'), '\n## Registry\n', `\n## Registry\nseat-06.01: approved-by: build-stage (R2); trial: docs/trial/kernel-trial-4.md blob ${T4}; blob: ${b}\n`);
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
  seat0013(d, (b) => `approved-by: build-stage (R2); trial: docs/trial/does-not-exist.md blob ${'0'.repeat(40)}; blob: ${b}`);
}, { match: /cites trial docs\/trial\/does-not-exist\.md, which does not exist/ });
run('R2: a seat citing a real trial that did not pass the face is refused', (d) => {
  seat0013(d, (b) => `approved-by: build-stage (R2); trial: docs/trial/kernel-trial-4.md blob ${T4}; blob: ${b}`);
}, { match: /its PASS list does not name 10\.11\.21\.0013\.01/ });
// TRIAL-K5 finding 1 (Q53): the old commit form is refused with a re-pin message.
run('Q53: a seat citing a trial by commit id is refused (K5 finding 1)', (d) => {
  edit(S(d, '10.11.21', '10.11.21.1001.00.draft.md'), `kernel-trial-2.md blob ${T2};`, 'kernel-trial-2.md@ed82086;');
}, { match: /cites a commit id, which changes in the filter-branched published copy; re-pin it as trial: docs\/trial\/kernel-trial-2\.md blob/ });
run('R2: approved-by director with no ruling id is refused (H2)', (d) => {
  seat0013(d, (b) => `approved-by: director; trial: docs/trial/does-not-exist.md blob ${'0'.repeat(40)}; blob: ${b}`);
}, { match: /approved-by: director but gives no ruling id/ });
run('R2: approved-by director citing a ruling that does not name the face is refused', (d) => {
  seat0013(d, (b) => `approved-by: director; ruling: R22; blob: ${b}`);
}, { match: /seat cites R22, but that ruling does not name 10\.11\.21\.0013\.01/ });
run('R2: an approved-by value other than build-stage (R2) or director is refused', (d) => {
  seat0013(d, (b) => `approved-by: prima; trial: docs/trial/kernel-trial-2.md blob ${T2}; blob: ${b}`);
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
  edit(r, '\n## Registry\n', '\n## Registry\nunseat-01: test fixture retirement; was blob 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d (TRIAL-K2)\n');
}, { ok: true });
// TRIAL-K5 finding 5 (H13, Q54 d): an un-seat record names the full old blob and gives a reason.
run('Q54 d: an unseat record with a short blob is refused (K5 H13)', (d) => {
  edit(unseat(d), '\n## Registry\n', '\n## Registry\nunseat-01: test fixture retirement; was blob 5415cef2\n');
}, { match: /unseat-01: must name the full old blob 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d/ });
run('Q54 d: an unseat record with no reason is refused (K5 H13)', (d) => {
  edit(unseat(d), '\n## Registry\n', '\n## Registry\nunseat-01: was blob 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d\n');
}, { match: /unseat-01: gives no reason/ });

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
  edit(join(d, 'kernel', '00.00.00', '00.00.00.0056.00.draft.md'), `kernel-trial-2.md blob ${T2}; blob: 112c169ccd06d54c6d9ab607fee6c2d16004cc62`, `forged.md blob ${blob(trial)}; blob: ${nb}`);
}, { match: /lists 00\.00\.00\.0056\.01 by the short prefix [0-9a-f]{8}, and blob [0-9a-f]{40} is not this face's file in the commit that added the trial/ });
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
  void c;
  seat0013(d, (bb) => `approved-by: build-stage (R2); trial: docs/trial/forged.md blob ${blob(t(b))}; blob: ${bb}`);
}, { match: /no commit reachable from HEAD adds docs\/trial\/forged\.md/ });
// TRIAL-K4 finding 5 (HC, Q52 d): with no git, a seat cannot be verified, so it is an error, not a finding.
run('R2: with no git a seat is an error (K4 finding 5)', (d) => {
  rmSync(join(d, '.git'), { recursive: true, force: true });
}, { match: /00\.00\.00\.0056\.01\.md: no git repo at .*so this seat cannot be verified/ });
// TRIAL-K4 finding 6 (HI, Q52 b): past seats come from HEAD:books/, so deleting books/ does not hide an un-seat.
run('R2: retiring a seated face after deleting books/ is still refused (K4 HI)', (d) => {
  rmSync(join(d, 'books'), { recursive: true, force: true });
  unseat(d);
}, { match: /10\.11\.21\.1001\.01 was seated \(build-stage \(R2\)\) in the last build but is not now/ });

// ---- KERNEL pass 7: TRIAL-K5 findings 1-5 (Q53, Q54) ----
const ID = { GIT_AUTHOR_NAME: 't', GIT_AUTHOR_EMAIL: 't@t', GIT_COMMITTER_NAME: 't', GIT_COMMITTER_EMAIL: 't@t' };
// Commit the copied working files on top of HEAD in a scratch clone (it has no checkout, so the index is built from HEAD).
const commitWork = (d, msg = 'work') => {
  const env = { ...process.env, ...ID };
  sh(d, ['read-tree', 'HEAD'], { env });
  sh(d, ['add', '-A', '--', 'kernel', 'docs/spec', 'docs/trial', 'books'], { env });
  sh(d, ['commit', '-q', '--no-verify', '--allow-empty', '-m', msg], { env }); // empty in a clean clone, where the work is HEAD
};
// The seated 0051.05.02 is edited and its seat re-pinned to the new blob, citing a trial file that names the new blob.
const k = (d, n) => join(d, 'kernel', '00.00.00', n);
const forge0051 = (d, trialPath) => {
  const f = k(d, '00.00.00.0051.05.02.md');
  appendFileSync(f, '\nforged line\n');
  const nb = blob(readFileSync(f, 'utf8'));
  const old = '7dbf70bd22af1bf0354edd82aff3ddb405ef892d';
  edit(k(d, '00.00.00.0051.00.draft.md'), `trial: docs/trial/kernel-trial-4.md blob ${T4}; blob: ${old}`, `trial: ${trialPath}; blob: ${nb}`);
  return nb;
};
// A scratch clone with a checkout (filter-branch refuses a tree with unstaged changes), then the working files copied in.
const fullScratch = () => {
  const d = mkdtempSync(join(tmpdir(), 'kbuild-full-'));
  sh(ROOT, ['clone', '-q', '--shared', ROOT, d]);
  for (const p of ['kernel', 'docs/spec', 'docs/trial', 'books']) { rmSync(join(d, p), { recursive: true, force: true }); cpSync(join(ROOT, p), join(d, p), { recursive: true }); }
  return d;
};
// Q53 / K5 finding 1: a history rewrite (filter-branch dropping target/, as the publish copy is made) changes every commit id,
// and the seats still verify, because they cite trial and face blobs.
run('Q53: seats still verify after a filter-branch rewrite changes every commit id (K5 finding 1)', (d) => {
  commitWork(d, 'pass 7 work');
  const before = sh(d, ['rev-parse', 'HEAD']);
  const env = { ...process.env, ...ID, FILTER_BRANCH_SQUELCH_WARNING: '1' };
  sh(d, ['filter-branch', '-f', '--index-filter', 'git rm -r -q --cached --ignore-unmatch target', '--msg-filter', 'cat; echo rewritten', 'HEAD'], { env });
  sh(d, ['update-ref', '-d', 'refs/original/refs/heads/build']);
  for (const r of sh(d, ['for-each-ref', '--format=%(refname)', 'refs/remotes/']).split('\n').filter(Boolean)) sh(d, ['update-ref', '-d', r]);
  if (sh(d, ['rev-parse', 'HEAD']) === before) throw new Error('fixture: HEAD did not change');
  if (spawnSync('git', ['-C', d, 'merge-base', '--is-ancestor', '4b369fae89b965734011278166a906e3307c770a', 'HEAD']).status === 0) throw new Error('fixture: old trial commit still an ancestor');
}, { ok: true }, { scratch: fullScratch });
// Q54 a / K5 HR: git replace serves a forged trial blob; the guard runs git with --no-replace-objects and refuses replace refs.
run('Q54 a: a git replace forge of a trial blob is refused (K5 HR)', (d) => {
  const real = sh(d, ['cat-file', 'blob', T4]);
  const f = k(d, '00.00.00.0051.05.02.md');
  appendFileSync(f, '\nforged line\n');
  const nb = blob(readFileSync(f, 'utf8'));
  const forged = real.replace('**PASS list, eligible for an R2 seat**', `**PASS list, eligible for an R2 seat**\n- \`00.00.00.0051.05.02\` (blob \`${nb}\`)`);
  const fb = sh(d, ['hash-object', '-w', '--stdin'], { input: forged + '\n' });
  sh(d, ['replace', T4, fb]);
  edit(k(d, '00.00.00.0051.00.draft.md'), 'blob: 7dbf70bd22af1bf0354edd82aff3ddb405ef892d', `blob: ${nb}`);
}, { match: /the repo has replace refs \(refs\/replace\/a5d253d5/ });
// Q54 a / K5 H15: GIT_DIR pointed at another clone that adds a forged trial is ignored (GIT_* is stripped).
let evil;
run('Q54 a: GIT_DIR pointing at a clone with a forged trial is ignored (K5 H15)', (d) => {
  evil = scratch();
  const nb = forge0051(d, 'docs/trial/evil.md blob EVILBLOB');
  const t = `# evil\n\n**PASS list:**\n- \`00.00.00.0051.05.02\` (blob \`${nb}\`)\n`;
  writeFileSync(join(d, 'docs', 'trial', 'evil.md'), t);
  edit(k(d, '00.00.00.0051.00.draft.md'), 'EVILBLOB', blob(t));
  sh(evil, ['update-ref', 'HEAD', commitOnHead(evil, 'docs/trial/evil.md', t)]);
}, { match: /no commit reachable from HEAD adds docs\/trial\/evil\.md/ }, { env: () => ({ GIT_DIR: join(evil, '.git'), GIT_WORK_TREE: evil }) });
if (evil) rmSync(evil, { recursive: true, force: true });
// Q54 b / K5 H11: dropping a seat and its books line in a commit does not hide the un-seat; seat lines are read from history.
run('Q54 b: an un-seat hidden by a committed books edit is refused (K5 H11)', (d) => {
  unseat(d);
  const b = join(d, 'books', '10.11.21.book');
  writeFileSync(b, readFileSync(b, 'utf8').split('\n').filter((l) => !l.includes('"addr":"10.11.21.1001.01"')).join('\n'));
  edit(S(d, '10.11.21', '10.11.21.1001.00.draft.md'), /^seat-01: .*\n/m.exec(readFileSync(S(d, '10.11.21', '10.11.21.1001.00.draft.md'), 'utf8'))[0], '');
  commitWork(d, 'hide the un-seat');
}, { match: /10\.11\.21\.1001\.01 was seated \(build-stage \(R2\)\) in the last build but is not now; write unseat-01: <reason>; was blob 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d/ });
// Q54 c / K5 H5: a PASS line added to a real trial in a later commit cannot be cited; the seat must cite the added blob.
run('Q54 c: a PASS line added to a real trial in a later commit is refused (K5 H5)', (d) => {
  const real = sh(d, ['cat-file', 'blob', T4]) + '\n';
  const f = k(d, '00.00.00.0051.05.02.md');
  appendFileSync(f, '\nforged line\n');
  const nb = blob(readFileSync(f, 'utf8'));
  const t = real.replace('**PASS list, eligible for an R2 seat**', `**PASS list, eligible for an R2 seat**\n- \`00.00.00.0051.05.02\` (blob \`${nb}\`)`);
  writeFileSync(join(d, 'docs', 'trial', 'kernel-trial-4.md'), t);
  sh(d, ['update-ref', 'HEAD', commitOnHead(d, 'docs/trial/kernel-trial-4.md', t)]);
  edit(k(d, '00.00.00.0051.00.draft.md'), `kernel-trial-4.md blob ${T4}; blob: 7dbf70bd22af1bf0354edd82aff3ddb405ef892d`, `kernel-trial-4.md blob ${blob(t)}; blob: ${nb}`);
}, { match: /trial docs\/trial\/kernel-trial-4\.md was added at blob a5d253d5e12722956afea38e79cb7fc1cf492c7b .*not [0-9a-f]{40}; a seat cites the trial as its lane wrote it/ });
// Q54 c: a trial added in the same commit as a kernel change (a builder writing its own trial) is refused.
run('Q54 c: a trial added in a commit that also changes kernel/ is refused', (d) => {
  const f = k(d, '00.00.00.0051.05.02.md');
  appendFileSync(f, '\nforged line\n');
  const nb = blob(readFileSync(f, 'utf8'));
  const t = `# mixed\n\n**PASS list:**\n- \`00.00.00.0051.05.02\` (blob \`${nb}\`)\n`;
  writeFileSync(join(d, 'docs', 'trial', 'mixed.md'), t);
  edit(k(d, '00.00.00.0051.00.draft.md'), `kernel-trial-4.md blob ${T4}; blob: 7dbf70bd22af1bf0354edd82aff3ddb405ef892d`, `mixed.md blob ${blob(t)}; blob: ${nb}`);
  commitWork(d, 'builder adds its own trial');
}, { match: /the commit that added trial docs\/trial\/mixed\.md \([0-9a-f]{12}\) also changes .*kernel\// });
// Q54: a shallow clone is refused (the guard reads the full history).
run('Q54: a shallow clone is refused', (d) => {
  writeFileSync(join(d, '.git', 'shallow'), sh(d, ['rev-parse', 'HEAD']) + '\n');
}, { match: /the repo is a shallow clone/ });

// ---- KERNEL pass 8: TRIAL-K6 findings 1 and 2 (Q56) ----
// A temp index on HEAD (or a given tree-ish), files added from the scratch working tree or as blobs, and a tree id out.
const tmpIdx = (d) => ({ ...process.env, ...ID, GIT_INDEX_FILE: join(d, '.git', 'k8-index') });
const treeOf = (d, base, fill) => { const env = tmpIdx(d); sh(d, ['read-tree', base], { env }); fill(env); return sh(d, ['write-tree'], { env }); };
const commitTree = (d, tree, parents, msg) => sh(d, ['commit-tree', tree, ...parents.flatMap((p) => ['-p', p]), '-m', msg], { env: tmpIdx(d) });
// The quiet un-seat of K5 H11: the seated 1001.01 is retired with no record, its seat line and its books line dropped.
const quietUnseat = (d) => {
  unseat(d);
  const b = join(d, 'books', '10.11.21.book');
  writeFileSync(b, readFileSync(b, 'utf8').split('\n').filter((l) => !l.includes('"addr":"10.11.21.1001.01"')).join('\n'));
  const r = S(d, '10.11.21', '10.11.21.1001.00.draft.md');
  edit(r, /^seat-01: .*\n/m.exec(readFileSync(r, 'utf8'))[0], '');
};
const UNSEAT_1001 = /10\.11\.21\.1001\.01 was seated \(build-stage \(R2\)\) in the last build but is not now; write unseat-01: <reason>; was blob 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d/;
// Q56 a / K6 K21: a committed `.gitattributes` line `kernel/** -diff` makes `git log -p -G` blind to seat lines.
run('Q56 a: a committed .gitattributes kernel/** -diff does not hide an un-seat (K6 K21)', (d) => {
  writeFileSync(join(d, '.gitattributes'), 'kernel/** -diff\nbooks/** -diff\n');
  const ab = sh(d, ['hash-object', '-w', join(d, '.gitattributes')]);
  sh(d, ['update-ref', 'HEAD', commitTree(d, treeOf(d, 'HEAD', (env) => sh(d, ['update-index', '--add', '--cacheinfo', `100644,${ab},.gitattributes`], { env })), ['HEAD'], 'harmless attributes')]);
  quietUnseat(d);
  commitWork(d, 'hide the un-seat behind attributes');
}, { match: UNSEAT_1001 });
// Q56 a / K6 K22: the same with only the local .git/info/attributes, nothing committed.
run('Q56 a: .git/info/attributes kernel/** -diff does not hide an un-seat (K6 K22)', (d) => {
  mkdirSync(join(d, '.git', 'info'), { recursive: true });
  writeFileSync(join(d, '.git', 'info', 'attributes'), 'kernel/** binary\nbooks/** binary\n');
  quietUnseat(d);
  commitWork(d, 'hide the un-seat behind local attributes');
}, { match: UNSEAT_1001 });
// Q56 b / K6 K26: a merge whose kernel/ comes from a side branch cut before a seat commit; plain `git log -- kernel/` follows
// only the side (history simplification) and never sees the commit that added the seat line.
run('Q56 b: a merge from a side branch cut before a seat does not hide an un-seat (K6 K26)', (d) => {
  commitWork(d, 'work');
  const reg = 'kernel/00.00.00/00.00.00.0054.00.draft.md';
  const seatCommit = sh(d, ['log', '--format=%H', '--reverse', '--full-history', '-a', '--no-textconv', '-G', '^seat-05\\.01:', 'HEAD', '--', reg]).split('\n')[0];
  const f = k(d, '00.00.00.0054.05.01.md');
  renameSync(f, k(d, '00.00.00.0054.05.01.draft.md'));
  const r = join(d, reg);
  edit(r, '05.01 seated', '05.01 draft');
  edit(r, /^seat-05\.01: .*\n/m.exec(readFileSync(r, 'utf8'))[0], 'why-05.01: side branch fixture\n');
  const b = join(d, 'books', '00.00.00.book');
  writeFileSync(b, readFileSync(b, 'utf8').split('\n').filter((l) => !l.includes('"addr":"00.00.00.0054.05.01"')).join('\n'));
  const t = treeOf(d, 'HEAD', (env) => sh(d, ['add', '-A', '--', 'kernel', 'books'], { env }));
  const side = commitTree(d, t, [`${seatCommit}^`], 'side branch from before the seat');
  sh(d, ['update-ref', 'HEAD', commitTree(d, t, ['HEAD', side], 'merge the side, taking its kernel/')]);
}, { match: /00\.00\.00\.0054\.05\.01 was seated \(build-stage \(R2\)\) in the last build but is not now; write unseat-05\.01: <reason>; was blob aa07b61116572c9e25353a5e7f3b6ed97941d2a0/ });
// Q56 c / K6 K25: a merge takes a side branch's edited copy of a real trial (the side cut before the trial was added), so plain
// `git log --diff-filter=A` finds only the side's add and the write-once check (Q54 c) is bypassed. kernel-trial-3 is used, as
// in K25, because no seat cites it. The path is added twice on HEAD's full history with two different blobs, so it is refused.
run('Q56 c: a merge citing an edited copy of a real trial from the side branch is refused (K6 K25)', (d) => {
  const path = 'docs/trial/kernel-trial-3.md';
  const [added, addedBlob] = sh(d, ['log', '--format=C %H', '--raw', '--no-abbrev', '--no-renames', '--full-history', '--diff-filter=A', 'HEAD', '--', path])
    .split('\n').filter(Boolean).reduce((a, l) => (l.startsWith('C ') ? [l.slice(2), a[1]] : [a[0], l.split(' ')[3]]), []);
  const nb = forge0051(d, `${path} blob FORGED`);
  const t = sh(d, ['cat-file', 'blob', addedBlob]) + `\n\n**PASS list:**\n- \`00.00.00.0051.05.02\` (blob \`${nb}\`)\n`;
  writeFileSync(join(d, path), t);
  edit(k(d, '00.00.00.0051.00.draft.md'), 'FORGED', blob(t));
  const tb = sh(d, ['hash-object', '-w', join(d, path)]);
  const put = (env) => sh(d, ['update-index', '--add', '--cacheinfo', `100644,${tb},${path}`], { env });
  const side = commitTree(d, treeOf(d, `${added}^`, put), [`${added}^`], 'docs only: trial copy');
  sh(d, ['update-ref', 'HEAD', commitTree(d, treeOf(d, 'HEAD', put), ['HEAD', side], 'merge the side, taking its trial copy')]);
}, { match: /trial docs\/trial\/kernel-trial-3\.md is added more than once on HEAD's full history with different blobs/ });

// ---- KERNEL pass 9: TRIAL-K7 findings 1 and 2 (Q58, Q59) ----
// Commits built on HEAD in the scratch clone: `ops` is a list of [mode, blob, path] to put, or [null, null, path] to drop.
const putTree = (d, base, ops) => treeOf(d, base, (env) => {
  for (const [mode, b, p] of ops) sh(d, mode ? ['update-index', '--add', '--cacheinfo', `${mode},${b},${p}`] : ['update-index', '--force-remove', p], { env });
});
const hashText = (d, t) => sh(d, ['hash-object', '-w', '--stdin'], { input: t });
const R1001 = 'kernel/samples/10.11.21/10.11.21.1001.00.draft.md';
const FAKE_SEAT = `seat-05.03: approved-by: build-stage (R2); trial: docs/trial/kernel-trial-7.md blob ${'1'.repeat(40)}; blob: ${'2'.repeat(40)}\n`;
const UNSEAT_FAKE = /10\.11\.21\.1001\.05\.03 was seated \(build-stage \(R2\)\) in the last build but is not now; write unseat-05\.03: <reason>; was blob 2{40}/;
// Q58 A / K7 T18: face 00 of page 1001 is a symlink to a file outside kernel/. The builder refuses it and does not follow it.
run('Q58: a symlinked face 00 is refused (K7 T18)', (d) => {
  mkdirSync(join(d, 'docs', 'x'), { recursive: true });
  renameSync(join(d, R1001), join(d, 'docs', 'x', 'f00.md'));
  symlinkSync('../../../docs/x/f00.md', join(d, R1001));
}, { match: /kernel\/samples\/10\.11\.21\/10\.11\.21\.1001\.00\.draft\.md: is a symlink; the builder reads only regular files/ });
// Q58 history / K7 T18: commit 1 makes face 00 a link to docs/x/f00.md, commit 2 adds a seat line through the link, commit 3
// puts the regular file back without it. The live tree has no link, so only the history walk can see the seat: it follows the
// link it finds in kernel/ history to docs/x/f00.md and asks for the un-seat record.
run('Q58: a seat written through a face 00 link and removed later is still found in history (K7 T18)', (d) => {
  const orig = sh(d, ['cat-file', 'blob', `HEAD:${R1001}`]) + '\n';
  const link = hashText(d, '../../../docs/x/f00.md');
  const c1 = commitTree(d, putTree(d, 'HEAD', [['120000', link, R1001], ['100644', hashText(d, orig), 'docs/x/f00.md']]), ['HEAD'], 'face 00 moved behind a link');
  const c2 = commitTree(d, putTree(d, c1, [['100644', hashText(d, orig.replace('\n## Registry\n', `\n## Registry\n${FAKE_SEAT}`)), 'docs/x/f00.md']]), [c1], 'seat through the link');
  sh(d, ['update-ref', 'HEAD', commitTree(d, sh(d, ['rev-parse', 'HEAD^{tree}']), [c2], 'link gone, seat gone, no record')]);
}, { match: UNSEAT_FAKE });
// Q58 A / K7 T18b: the book folder 10.11.21 is a symlink into kernel/parked/, a folder the history walk skips.
run('Q58: a symlinked book folder is refused (K7 T18b)', (d) => {
  mkdirSync(join(d, 'kernel', 'parked'), { recursive: true });
  renameSync(S(d, '10.11.21'), join(d, 'kernel', 'parked', '10.11.21-real'));
  symlinkSync('../parked/10.11.21-real', S(d, '10.11.21'));
}, { match: /kernel\/samples\/10\.11\.21: is a symlink/ });
// Q58 history / K7 T18b: the same through history: the folder moves to kernel/parked/ behind a link, a seat line is added
// there, then the folder comes back without it. The walk follows the folder link and reads under /parked/ for it.
run('Q58: a seat written through a book folder link into kernel/parked is still found in history (K7 T18b)', (d) => {
  const rows = sh(d, ['ls-tree', '-r', 'HEAD', 'kernel/samples/10.11.21/']).split('\n').map((l) => /^(\d+) blob ([0-9a-f]{40})\t(.*)$/.exec(l));
  const moved = (p) => p.replace('kernel/samples/10.11.21/', 'kernel/parked/10.11.21-real/');
  const ops = rows.flatMap(([, m, b, p]) => [[null, null, p], [m, b, moved(p)]]);
  const c1 = commitTree(d, putTree(d, 'HEAD', [...ops, ['120000', hashText(d, '../parked/10.11.21-real'), 'kernel/samples/10.11.21']]), ['HEAD'], 'book behind a link');
  const orig = sh(d, ['cat-file', 'blob', `HEAD:${R1001}`]) + '\n';
  const c2 = commitTree(d, putTree(d, c1, [['100644', hashText(d, orig.replace('\n## Registry\n', `\n## Registry\n${FAKE_SEAT}`)), moved(R1001)]]), [c1], 'seat in the parked copy');
  sh(d, ['update-ref', 'HEAD', commitTree(d, sh(d, ['rev-parse', 'HEAD^{tree}']), [c2], 'folder back, seat gone, no record')]);
}, { match: UNSEAT_FAKE });
// Q58 A / K7 T18c: a seated face is a symlink to an untracked file with the same bytes.
const F1001_0502 = 'kernel/samples/10.11.21/10.11.21.1001.05.02.md';
run('Q58: a seated face that is a symlink to an untracked copy is refused (K7 T18c)', (d) => {
  mkdirSync(join(d, 'docs', 'x'), { recursive: true });
  renameSync(join(d, F1001_0502), join(d, 'docs', 'x', 'copy.md'));
  symlinkSync('../../../docs/x/copy.md', join(d, F1001_0502));
}, { match: /kernel\/samples\/10\.11\.21\/10\.11\.21\.1001\.05\.02\.md: is a symlink/ });
// Q58 B / K7 T18c in git: the link is committed, and the working copy is a regular file with the seated bytes. git holds the
// link text, not the face, so the seat is refused.
run('Q58: a seated face committed as a symlink is refused though the working file has the seated bytes (K7 T18c)', (d) => {
  sh(d, ['update-ref', 'HEAD', commitTree(d, putTree(d, 'HEAD', [['120000', hashText(d, '../../../docs/x/copy.md'), F1001_0502]]), ['HEAD'], 'seated face committed as a link')]);
}, { match: /seated face kernel\/samples\/10\.11\.21\/10\.11\.21\.1001\.05\.02\.md is mode 120000 in git \(HEAD\), not a regular file/ });
// Q58 B: a seated face that is not in git at all (removed from HEAD, file left on disk) is refused.
run('Q58: a seated face that git does not hold (untracked) is refused', (d) => {
  sh(d, ['update-ref', 'HEAD', commitTree(d, putTree(d, 'HEAD', [[null, null, F1001_0502]]), ['HEAD'], 'seated face dropped from git')]);
}, { match: /seated face kernel\/samples\/10\.11\.21\/10\.11\.21\.1001\.05\.02\.md is not in git \(untracked; not at HEAD or in the index\)/ });
// Q59 / K7 T11: an orphan root commit adds an edited copy of a real trial at the same path and is merged in. `%P` is empty for a
// root commit; before pass 9 the header was not parsed and the builder crashed (TypeError). Now it is the plain refusal.
run('Q59: an orphan root commit adding an edited trial copy is refused, not a crash (K7 T11)', (d) => {
  const path = 'docs/trial/kernel-trial-3.md';
  const nb = forge0051(d, `${path} blob FORGED`);
  const t = sh(d, ['cat-file', 'blob', `HEAD:${path}`]) + `\n\n**PASS list:**\n- \`00.00.00.0051.05.02\` (blob \`${nb}\`)\n`;
  writeFileSync(join(d, path), t);
  edit(k(d, '00.00.00.0051.00.draft.md'), 'FORGED', blob(t));
  const tb = hashText(d, t);
  const root = commitTree(d, putTree(d, sh(d, ['mktree'], { input: '' }), [['100644', tb, path]]), [], 'orphan: trial copy');
  sh(d, ['update-ref', 'HEAD', commitTree(d, putTree(d, 'HEAD', [['100644', tb, path]]), ['HEAD', root], 'merge the orphan, taking its trial copy')]);
}, { match: /trial docs\/trial\/kernel-trial-3\.md is added more than once on HEAD's full history with different blobs/ });
// Q59 (decided): a root commit that adds only a trial file is an origin like any other first add. A new trial in an orphan root
// commit, merged in, passes the draft 0013.05.02; the seat is committed and builds.
run('Q59: a trial added by an orphan root commit (trial only) is a valid origin', (d) => {
  const draft = S(d, '10.11.21', '10.11.21.0013.05.02.draft.md');
  const fb = blob(readFileSync(draft, 'utf8'));
  const t = `# orphan trial\n\n**PASS list, eligible for an R2 seat**\n- \`10.11.21.0013.05.02\` (blob \`${fb}\`)\n`;
  const path = 'docs/trial/orphan.md';
  writeFileSync(join(d, path), t);
  const tb = hashText(d, t);
  const root = commitTree(d, putTree(d, sh(d, ['mktree'], { input: '' }), [['100644', tb, path]]), [], 'orphan: trial only');
  sh(d, ['update-ref', 'HEAD', commitTree(d, putTree(d, 'HEAD', [['100644', tb, path]]), ['HEAD', root], 'merge the orphan trial')]);
  renameSync(draft, S(d, '10.11.21', '10.11.21.0013.05.02.md'));
  const r = S(d, '10.11.21', '10.11.21.0013.00.draft.md');
  edit(r, '05.02 draft', '05.02 seated');
  edit(r, /^why-05\.02: .*\n/m.exec(readFileSync(r, 'utf8'))[0], `seat-05.02: approved-by: build-stage (R2); trial: ${path} blob ${tb}; blob: ${fb}\n`);
  commitWork(d, 'seat 0013.05.02 from the orphan trial');
}, { ok: true });

if (failed) { console.log(`${failed} failed`); process.exit(1); }
console.log('all passed');
