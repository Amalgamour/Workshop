from pathlib import Path
import json,hashlib
root=Path(r'D:\Git\lib-build');page=root/'00.kernel/00.00.10.work/0709.return-migration-check';out=Path(r'D:\librarian\temp\migration-0709-review-nov02');out.mkdir(exist_ok=False)
checks=[]
for name,p in [('sources',page/'evidence/pack05.01/source-manifest.json'),('artifacts',page/'evidence/lab05.01/ARTIFACT-MANIFEST.json')]:
    rows=json.loads(p.read_text(encoding='utf-8'))['files'];bad=[]
    for row in rows:
        b=(root/row['path']).read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append(row['path'])
    checks.append({'manifest':name,'rows':len(rows),'mismatches':bad})
copy=Path(r'D:\librarian\temp\return-migration-0709\20261102T161806Z\book')
old_names=['0121.archive-resolution-0508','0122.bridge-overlap-0513','0123.boot-validation-0508','0124.clerk-seam-design-0503','0125.mapping-capture-0509']
facts={'legacy_0121_0125_still_occupied':[n for n in old_names if (copy/n).is_dir()],'rehearsal_has_live_band_door':(copy/'0100.band.returns').exists(),'live_has_band_door':(root/'00.kernel/00.00.10.work/0100.band.returns').exists(),'live_layout_present':(root/'00.kernel/00.00.10.work/return-line-layout.json').exists(),'read_only_review':True}
result={'integrity':checks,'independent_copy_inspection':facts,'independent_rehearsal_rerun':False}
(out/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result));assert not any(x['mismatches'] for x in checks) and len(facts['legacy_0121_0125_still_occupied'])==5
