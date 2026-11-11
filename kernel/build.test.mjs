#!/usr/bin/env node
// Tests for kernel/build.mjs. Each test copies kernel/ and docs/spec/ into a scratch folder, adds one hostile
// change, runs the builder there, and checks the result. The repo is never written. Usage: node kernel/build.test.mjs
import { mkdtempSync, cpSync, writeFileSync, readFileSync, rmSync, appendFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
let failed = 0;

function scratch() {
  const d = mkdtempSync(join(tmpdir(), 'kbuild-'));
  cpSync(HERE, join(d, 'kernel'), { recursive: true });
  cpSync(join(ROOT, 'docs', 'spec'), join(d, 'docs', 'spec'), { recursive: true });
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

if (failed) { console.log(`${failed} failed`); process.exit(1); }
console.log('all passed');
