from pathlib import Path
import sys, json, tempfile, hashlib, os
R=Path(r'D:\Git\lib-build'); O=Path(r'D:\librarian\temp\review0518-probes')
O.mkdir(exist_ok=False);(O/'scratch').mkdir()
tempfile.tempdir=str(O/'scratch');os.environ['TEMP']=tempfile.tempdir;os.environ['TMP']=tempfile.tempdir
sys.path.insert(0,str(R/'labs/colab-review-pass01/tests'))
sys.path.insert(0,str(R/'labs/colab-review-pass01'))
import fixture as F
import colab_review as cr
d=F.Desk(prefix='prime-0518-')
pp,pb,req,out,digest,bd=F.route(d)
results=[]
def walk(name,specs):
    book=d.new_book(name)
    members=[d.capture(out,f'{name}-{n:02d}',r,book=book) for n,r in enumerate(specs,1)]
    code,i,err=d.intake(bd,pp,members,name=name+'-intake',book=book)
    ip=d.path(name+'-intake')/'intake.json'
    known=i['findings_index']
    s={'schema':'colab-review-synthesis/1','plan_id':'plan-1','intake_sha256':hashlib.sha256(ip.read_bytes()).hexdigest(),
       'by':'Codex Prime independent SYNTHETIC probe','label':'SYNTHETIC',
       'items':[], 'retained':[{'finding':f,'disposition':'minority','reason':'Keep this concern visible','of':None} for f in known],
       'disagreements':[],'incomplete':i['incomplete'],'residual_uncertainty':[],'acceptance':None}
    rc,report,e=d.synthesize(d.path(name+'-intake'),s,name=name+'-report')
    md=(d.path(name+'-report')/'REPORT.md').read_text(encoding='utf-8')
    result={'name':name,'intake_exit':code,'intake_status':i['status'],'intake_findings':i['findings'],
            'incomplete':i['incomplete'],'report_exit':rc,'report_status':report['status'],
            'report_findings':report['findings'],'report_markdown':md,'fixture_root':str(d.tmp)}
    results.append(result)
    (O/'results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(name,code,rc,report['status'],flush=True)
Rr=d.result
def required():
    return [Rr(pb,'R01','S01'),Rr(pb,'R02','S01'),Rr(pb,'R01','S02',[],comprehension=False),Rr(pb,'R02','S02',[],comprehension=False)]
specs=required();specs[0]['context']['conversation_supplied']='full'
walk('context-error',specs)
specs=required()+[Rr(pb,'R01','S03',[],status='failed',comprehension=False)]
walk('optional-failed',specs)
specs=required();specs[2]['findings']=[{'id':'R01-S02-F01','target':'T01','location':'section 2','text':'SYNTHETIC ORIGINAL: return recording may lose its evidence.'}]
walk('retained-text',specs)
print('Preserved all disposable inputs and outputs at',d.tmp)
