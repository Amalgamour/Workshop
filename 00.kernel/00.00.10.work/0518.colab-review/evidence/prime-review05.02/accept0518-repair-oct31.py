from pathlib import Path
import json,shutil,hashlib
R=Path(r'D:\Git\lib-build');P=R/'00.kernel/00.00.10.work/0518.colab-review'
C=Path(r'D:\librarian\temp\review0518-repair');Q=Path(r'D:\librarian\temp\review0518-repair-probes')
checks=json.loads((C/'checks.json').read_text(encoding='utf-8'))
assert checks['tests']['exit']==0
assert 'Ran 17 tests' in (C/'tests.stderr').read_text(encoding='utf-8')
probes=json.loads((Q/'results.json').read_text(encoding='utf-8'))
for probe in probes:
    root=Path(probe['fixture_root']); name=probe['name']
    report=json.loads((root/(name+'-report')/'report.json').read_text(encoding='utf-8'))
    md=probe['report_markdown']
    if name=='context-error':
        assert report['intake_status']=='incomplete' and report['distinctions']['required_review']=='incomplete'
        assert report['intake_findings'][0]['finding']=='context-mismatch' and 'context-mismatch' in md
    elif name=='optional-failed':
        assert report['intake_status']=='complete'
        assert any(x['stage']=='S03' and x['status']=='failed' and not x['required'] for x in report['stage_status'])
        assert 'optional failed' in md
    elif name=='retained-text':
        assert 'SYNTHETIC ORIGINAL: return recording may lose its evidence.' in md
        assert 'custody: member' in md and 'target: T01' in md
E=P/'evidence/prime-review05.02'
assert not E.exists() and not (P/'06.04.md').exists()
E.mkdir()
shutil.copytree(C,E/'independent-checks',ignore=shutil.ignore_patterns('scratch'))
shutil.copytree(Q,E/'independent-probes',ignore=shutil.ignore_patterns('.git'))
for name in ['review0518-repair-oct31.py','probe-colab0518-oct31.py','accept0518-repair-oct31.py']:
    shutil.copyfile(Path(r'D:\librarian\temp')/name,E/name)
report='''# Prime review - 0518/05.02
date: 2026-10-31
who: Codex Prime
disposition: accepted bounded lab repair

## Did and verified
Verified capture 0181 complete, receipt
1deb97b0fa21fbc6781658f9093b4d2d8f085f3f6e98388ce8ea89f7368aa189.
Original capture 0179 also verifies complete. All declared repaired artifacts match
their manifest bytes and lengths. All 65 original pinned reused sources still
match. The live repaired adapter/test/doc files supersede their earlier working
versions; original source snapshots and captured 05.01 evidence remain preserved.
Independent supplied suite: 17 tests passed, zero skips. See independent-checks.
Three original independent route probes were rerun against the new implementation,
using actual synthetic captures and existing producer/custody interfaces. Raw inputs,
outputs and reports are retained in independent-probes; no model reviewer was run.

## Findings resolved
PR-01: context mismatch remains in report intake_findings and Markdown; required
review is visibly incomplete. Mapping may remain consistent with exit 0, but this
is explicitly separate from review completion and acceptance.
PR-02: optional failed S03 is present in stage_status and readable Markdown while
required review remains complete. Optional absence/failure is no longer hidden.
PR-03: retained original text, target/location and member/receipt appear in Markdown.
The supplied exact original wording survived the independent probe.

## Compatibility and limits
New intake/report records are explicitly /2. /1 intake compatibility is covered
by the independently rerun suite; no optional-stage inventory is invented for old
records. Supplied synthesis and review meaning remain intelligent judgments.
Custody is not acceptance. There is no automatic model launch, provider call,
production activation or proof of isolation. One return is still placed per pass;
other reviewer results stay in N1 custody. This repair does not implement the app.
No new app/ source changes were observed by git diff for this review.

## Next
No further repair is required for PR-01 to PR-03. The adapter is available for
bounded Prime use with these declared limits; no universal adoption or seating.
Keep Grok-1 available for the app implementation slices after 0519 design and
0520 independent execution evidence are reviewed. Do not add unrelated features
merely to keep the worker occupied. No Director decision is needed to close these
technical findings. Existing AR-01 hold remains unchanged.

## Record
Recorded here, in 0518/06.04.md and the 05.02 Prime review. Captures unchanged.
This review makes no Git commit or push; publication remains pending.
'''
(E/'REVIEW.md').write_text(report,encoding='utf-8')
(P/'06.04.md').write_text('''# Prime disposition - 0518/05.02
date: 2026-10-31
who: Codex Prime
state: accepted bounded lab repair; PR-01 to PR-03 resolved

Independent 17-test suite passed, zero skips. Three original independent probes
now preserve intake diagnostics, optional failed-stage status and minority text.
Original 0179 and repair 0181 verify complete; declared artifacts and 65 reused
source pins match. Full evidence: evidence/prime-review05.02/REVIEW.md.
No production app changes, capture rewrite, seating or Git publication.
Next: app design 0519 and independent lab 0520, then bounded implementation packs.
''',encoding='utf-8')
p=P/'05.02.md';data=p.read_bytes();old='## Review — Codex Prime\nPENDING.'.encode()
if old not in data:old='## Review — Codex Prime\r\nPENDING.'.encode()
assert old in data
new='''## Review — Codex Prime
2026-10-31: accepted bounded repair. Independent 17 tests passed, zero skips;
three original independent probes resolve PR-01 to PR-03. Both 0179 and 0181
captures verify; repaired artifacts and all 65 reused source pins match.
Evidence: evidence/prime-review05.02/REVIEW.md. Disposition: 06.04.md.
No production activation, seating or Git publication. Original captures preserved.'''.encode()
p.write_bytes(data.replace(old,new,1))
rows=[]
for f in sorted(E.rglob('*')):
    if f.is_file():
        b=f.read_bytes();rows.append({'path':f.relative_to(E).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(E/'evidence-manifest.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
print('Accepted and recorded bounded repair on 0518; evidence files',len(rows))
