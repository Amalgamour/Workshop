from pathlib import Path
import sys,json,subprocess,os
O=Path(r'D:\librarian\temp\cloud-core-repair-review');S=O/'source';sys.path.insert(0,str(S))
from app.desk_core.bookio import file_lock
lock=O/'scratch/native-lock-check.lock'
child='''import os,sys,msvcrt
fd=os.open(sys.argv[1],os.O_RDWR|os.O_BINARY)
try:
    msvcrt.locking(fd,msvcrt.LK_NBLCK,1)
except OSError:
    os.close(fd)
    sys.exit(0)
msvcrt.locking(fd,msvcrt.LK_UNLCK,1)
os.close(fd)
sys.exit(1)
'''
with file_lock(lock):
    q=subprocess.run([sys.executable,'-B','-c',child,str(lock)],capture_output=True)
result={'python':sys.version,'platform':sys.platform,'child_exit':q.returncode,'stderr':q.stderr.decode('utf-8','replace'),
        'interpretation':'exit 0 means independent Windows child could not acquire the parent-held byte lock; not a race-freedom claim'}
(O/'independent-lock.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
assert q.returncode==0,result
source=Path(r'D:\librarian\temp\probe-cloud-core-logic-oct31.py').read_text(encoding='utf-8')
source=source.replace('cloud-core-review','cloud-core-repair-review').replace("logic-probe-book'","native-logic-probe-book'").replace('logic-probes.json','native-logic-probes.json')
source=source.replace('e.file_lock=lambda path:contextlib.nullcontext()','')
source=source.replace("rr=e.revise_task(str(book),revised)","revised.update(reason='SYNTHETIC requested change', authorizing_reference='0523.sample/05.01#revision-request')\nrr=e.revise_task(str(book),revised)")
source=source.replace('serial unit probes with file_lock replaced by nullcontext in memory; native Windows CLI remains failed',
                      'native serial unit API probes using the unmodified repaired source, actual Windows lock and byte I/O; subprocess suite/demo are separately recorded; not concurrency or live-app proof')
assert 'e.file_lock=lambda' not in source
exec(compile(source,__file__,'exec'))
print('Windows held-lock probe passed:',result['child_exit'])
