import json,sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from bridge.adapter import LocalProcessAdapter,CLEANUP_ALLOWANCE_S
root=Path(sys.argv[2]);root.mkdir();inp=root/'input';out=root/'output';inp.mkdir();out.mkdir()
ad=LocalProcessAdapter(root/'store',{'prime-inherited':{'kind':'protocol test worker','argv':['{python}','-B','-I','fixtures/prime_inherited_pipes.py']}},Path(sys.argv[1]))
e={'schema':'worker-bridge/request@1','delivery_id':'probe-inherited','job_id':'probe','role':'builder','work_ref':'isolated Prime review fixture','inputs':[],'input_root':str(inp),'output_root':str(out),'limits':{'timeout_s':0.2,'max_stdout_bytes':1000,'max_stderr_bytes':1000},'release':{'by':'Prime review','ref':'local fixture only'},'backend':'prime-inherited'}
t=time.monotonic();r=ad.deliver(e)
print(json.dumps({'elapsed_s':time.monotonic()-t,'timeout_s':0.2,'cleanup_allowance_s':CLEANUP_ALLOWANCE_S,'receipt':r}))
