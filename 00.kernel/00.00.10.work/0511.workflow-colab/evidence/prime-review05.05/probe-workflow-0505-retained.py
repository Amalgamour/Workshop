from pathlib import Path
import sys,importlib.util,json,hashlib
root=Path(r'D:\Git\lib-build');out=Path(r'D:\librarian\temp\workflow-pass04-review-nov01')
tests=root/'labs/colab-workflow-pass04/tests';sys.path.insert(0,str(tests))
spec=importlib.util.spec_from_file_location('workflow_probe_helpers',tests/'test_pass04.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cw=m.cw;fixture=out/'retained-fixture';fixture.mkdir()
book,folder,saved=m.prepare_second(fixture,'0731.retained-proof')
before=(folder/'investigation.json').read_bytes();oldseal=(folder/'seal.json').read_bytes();(out/'prior-investigation.json').write_bytes(before);(out/'prior-seal.json').write_bytes(oldseal)
def fail_seal(src,dest):
    if Path(dest)==folder/'seal.json':raise OSError('PRIME controlled failure after investigation replacement, before seal replacement')
cw.REPLACE_HOOK=fail_seal
try:code,body,err=m.seal(book,'0731.retained-proof','05.02',b'Second pass retained proof\n','Prime disposable fixture',fixture)
finally:cw.REPLACE_HOOK=None
checkpoint=folder/'checkpoints'/cw.sha256(before)
assert (checkpoint/'investigation.json').read_bytes()==before
assert (checkpoint/'seal.json').read_bytes()==oldseal
assert (folder/'investigation.json').read_bytes()!=before
assert (folder/'seal.json').read_bytes()==oldseal
m.assert_refused(body,folder);m.assert_blocked(book)
paths={'artifact':'artifacts/05.01/return.md','pack':'artifacts/05.01/package/05.01.pack.md','review':'06.01.review.md','projection':'05.01.return.md'}
for key,rel in paths.items():assert (folder/rel).read_bytes()==saved[key]
result={'fixture':str(fixture),'exit':code,'response':body,'stderr':err.decode(errors='replace'),'prior_pair_verified_in_checkpoint':True,'root_pair_mixed_and_blocked':True,'prior_pass_artifacts_unchanged':True,'producer_verification':'stubbed in helper; separate real two-pass test runs pinned producer'}
(out/'retention-probe.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
