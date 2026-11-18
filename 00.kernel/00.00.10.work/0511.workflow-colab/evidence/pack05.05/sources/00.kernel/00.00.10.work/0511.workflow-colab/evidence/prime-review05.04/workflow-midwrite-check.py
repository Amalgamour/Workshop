from pathlib import Path
import sys,json,importlib.util
R=Path(r'D:\Git\lib-build');L=Path(r'D:\librarian\temp\workflow-and-harness-review-nov01');T=R/'labs/colab-workflow-pass03/tests'
sys.path.insert(0,str(T));s=importlib.util.spec_from_file_location('wf_io_fixture',T/'test_pass03.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
root=L/'workflow-midwrite';root.mkdir();book,request=m.open_page(root,'0798.midwrite');page=book/'0798.midwrite';cw=m.cw
record=cw.require_loaded(page);inv=page/'investigation.json';before=inv.read_bytes();seal=(page/'seal.json').read_bytes()
realopen=cw.os.open;realwrite=cw.os.write;fd_target=None;calls=0;done=False

def op(path,*args,**kw):
 global fd_target
 fd=realopen(path,*args,**kw)
 if str(path)==str(inv):fd_target=fd
 return fd

def wr(fd,data):
 global calls,done
 if fd==fd_target and not done:
  calls+=1
  if calls==1:return realwrite(fd,data[:max(1,len(data)//2)])
  done=True;raise OSError('SYNTHETIC mid-write failure after partial record write')
 return realwrite(fd,data)

cw.os.open=op;cw.os.write=wr
try:
 try:cw.commit(page,record);outcome='completed'
 except Exception as e:outcome=type(e).__name__+': '+str(e)
finally:cw.os.open=realopen;cw.os.write=realwrite
out={'outcome':outcome,'before_bytes':len(before),'after_bytes':len(inv.read_bytes()),'prior_record_intact':inv.read_bytes()==before,'old_seal_intact':(page/'seal.json').read_bytes()==seal,'partial_marker':(page/'partial.json').exists(),'fixture':str(page),'kind':'controlled partial-write injection, not process crash'}
(L/'workflow-midwrite.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
