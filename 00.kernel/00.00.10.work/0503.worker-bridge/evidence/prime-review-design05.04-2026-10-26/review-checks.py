from pathlib import Path
import csv,hashlib,json
W=Path(r'D:\Git\lib-build');P=W/'00.kernel/00.00.10.work/0503.worker-bridge';E=P/'evidence/design05.04';K=P/'evidence/pack05.04'
def sha(b):return hashlib.sha256(b).hexdigest()
facts={'reviewer':'Codex Prime','kind':'design review; no worker execution','snapshot_rows':0,'design_manifest_rows':0,'bridge_pins':0,'live_differences':[]}
for row in csv.DictReader((K/'source-manifest.tsv').open(encoding='utf8'),delimiter='\t'):
 b=(K/'inputs'/row['path']).read_bytes();assert sha(b)==row['sha256'] and len(b)==int(row['bytes'])
 facts['snapshot_rows']+=1
 if sha((W/row['path']).read_bytes())!=row['sha256']:facts['live_differences'].append(row['path'])
for line in (E/'SHA256SUMS.txt').read_text().splitlines():
 h,rel=line.split('  ',1);assert sha((E/rel).read_bytes())==h,rel;facts['design_manifest_rows']+=1
config=json.loads((E/'example/worker-bridge.json').read_text())
for rel,h in config['files'].items():
 assert sha((W/config['bridge_dir']/rel).read_bytes())==h,rel;facts['bridge_pins']+=1
job=json.loads((E/'example/job.json').read_text());inputb=(E/'example/input.txt').read_bytes()
assert sha(inputb)==job['inputs'][0]['sha256'] and len(inputb)==job['inputs'][0]['bytes']
assert json.loads((E/'example/expected-result.json').read_bytes())=={'count':3}
assert len([line for line in inputb.decode().splitlines() if line.strip()])==3
batch=P/'05.04.md';b=batch.read_bytes();assert b'\0' not in b
# Instruction prefix stays exact; the Return section alone was filled.
original=Path(r'D:\librarian\temp\pack-claude-bridge-design.py').read_text()
import ast
tree=ast.parse(original)
seed=next(node.value.value for node in tree.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='text' for t in node.targets))
assert b.split('## Return — Claude'.encode())[0]==seed.encode().split('## Return — Claude'.encode())[0]
facts['instruction_prefix_preserved']=True
facts['reviewed_return_sha256']=sha(b)
facts['expected_artifact_sha256']=sha((E/'example/expected-result.json').read_bytes())
facts['no_nul_bytes']=True
out=P/'evidence/prime-review-design05.04-2026-10-26';out.mkdir(exist_ok=False)
(out/'reviewed-return.md').write_bytes(b)
(out/'verification.json').write_bytes((json.dumps(facts,indent=2)+'\n').encode())
(out/'review-checks.py').write_bytes(Path(__file__).read_bytes())
review='''Reviewed return SHA-256: `{digest}`.
Disposition: ACCEPTED AS DESIGN INPUT with the implementation clarifications below.
This is not an implementation release, activation, or a tested app integration.

Prime read the complete 05.04 return, 06.04 notes and DESIGN.md; independently
verified all 13 input snapshots, 7 design manifest artifacts, all 8 proposed bridge
pins against current lab bytes, and the input length/hash and expected three-line
count. No worker, app integration or model was executed for this design review.
The return's no-live-differences statement is historical: app/context.py is now
changing in Grok's independent APP-01 repair. Pinned inputs remain intact.

What works: a bounded fixture-only exchange; reuse of the accepted lab; concrete
request, artifacts and receipts; no automatic retry; explicit separation of
collection, review and acceptance; proper deferral of the real-model connection.
Claude also correctly caught missing transitive inputs in Prime's original pack.
Add canon.py, ids.py, worker_fixture.py AND __init__.py to the next input manifest.

Implementation clarifications (fold into the implementation batch, no design rework):
1. Hash-check all executable bridge dependencies before importing any bridge helper.
   Section 4 step 3 uses the bridge strict loader before step 4 checks/imports it;
   reorder these steps. Keep package imports private and contained. A pin check is
   a development integrity check, not an OS security boundary.
2. Define authorization per command. New delivery requires the reviewed execution
   release; status is read-only inspection and must remain available when the job
   becomes returned/accepted. Recovery writes evidence but never launches: require
   an explicit scoped recovery request and verify the stored delivery's context;
   do not require or invent a new worker-launch release just to inspect history.
   Replays use the original recorded request identity; never rebuild one with a
   changed assignment-record hash and silently call it the same request.
3. Complete the app result/exit mapping for all existing adapter outcomes, including
   unknown delivery, accepted-not-launched, launch-failed, crashed and output-limit.
   Never report an unknown delivery as collected, or use exit 2's pre-launch wording
   to imply that a conflicting existing delivery had no earlier launch. A new ID
   after uncertain work is a deliberate retry decision, not automatic permission.
4. Until an implementation dependency is deliberately published, the app cannot
   rely on an untracked local lab. The build must pin AND include the exact needed
   dependency files in the workshop branch, with custody, while preserving the lab.
   Do not quietly copy it into law or add it to main.

Next bounded action: finish and independently accept Grok's APP-01 repair; pin that
actual interface, then pack one fixture bridge integration. The design's suggested
single app writer is correct. Bridge long-term placement does not block that slice.
No further Director design decision is required now. No new queue or Git edits.
Evidence: evidence/prime-review-design05.04-2026-10-26/.
'''.format(digest=sha(b))
text=b.decode();assert text.endswith('## Review — Codex Prime\nPENDING.\n')
batch.write_bytes(text.replace('## Review — Codex Prime\nPENDING.\n','## Review — Codex Prime\n'+review).encode())
print(json.dumps(facts,indent=2));print('Prime design review recorded. No implementation or Git writes.')
