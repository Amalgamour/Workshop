from pathlib import Path
import sys,json,zipfile,hashlib,subprocess
r=Path('D:/Git/lib-build');out=Path('D:/librarian/temp/colab-prime-review-2026-10-29')
sys.path.insert(0,str(r/'labs/colab-support-pass01'));import colab_support as cs
sys.path.insert(0,str(r/'labs/colab-workflow-pass01'));import colab_workflow as cw
cfg={'schema':'colab-config/1','repositories':{'workshop':str(r)},'python':sys.executable,**{k:str(r/v) for k,v in {'assembler':'labs/pack-assembly-pass01/pack_assembly.py','checker':'labs/pack-custody-pass01/pack_check.py','helper':'labs/return-capture-pass01/return_capture.py','inspector':'labs/return-capture-pass01/return_inspect.py'}.items()}}
(out/'config.json').write_text(json.dumps(cfg))
request=r/'00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/request-example.json'
preview,code=cs.preview(str(request),str(out/'config.json'));(out/'preview.json').write_text(json.dumps({'exit':code,'output':preview},indent=2));assert code==0,preview
prepared=out/'real-prepared'
body,code=cs.prepare(str(request),str(out/'config.json'),str(prepared),preview['digest']);(out/'prepare.json').write_text(json.dumps({'exit':code,'output':body},indent=2));assert code==0,body
verified,code=cs.verify(str(prepared),str(out/'config.json'));(out/'verify.json').write_text(json.dumps({'exit':code,'output':verified},indent=2));assert code==0,verified
files=cw.read_package(prepared/'package')
fixture=json.loads((r/'00.kernel/00.00.10.work/0511.workflow-colab/evidence/build05.01/integration-fixture.json').read_text())
req=fixture['request'];binding=json.loads(files['binding.json']);req.update(binding['investigation']);req['targets']=binding['targets']
try:
 cw.require_open_request(req)
 validation={'status':'accepted'}
except Exception as exc:
 validation={'status':'refused','reason':str(exc),'source_path':binding['targets'][0]['source']['path']}
(out/'target-validation-reproduction.json').write_text(json.dumps(validation,indent=2))
record=cw.new_record(req)
try:
 digest=cw.require_package(files,req['pass'],record)
 result={'unexpected_success':digest}
except Exception as exc:
 result={'refused':str(exc),'exception':type(exc).__name__,'expected_digest':preview['digest'],'package_files':sorted(files),'explanation':'Workflow requires request.json, in-package verification.json and different manifest/digest. Real producer uses colab-request.json, outside verification and accepted assembler manifest.'}
(out/'integration-reproduction.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
assert result.get('refused')=='malformed package',result
