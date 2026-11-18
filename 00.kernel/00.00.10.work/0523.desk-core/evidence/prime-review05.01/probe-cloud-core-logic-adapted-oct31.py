from pathlib import Path
source=Path(r'D:\librarian\temp\probe-cloud-core-logic-oct31.py').read_text(encoding='utf-8')
source=source.replace("logic-probe-book'","logic-probe-book-02'")
source=source.replace("logic-probes.json","logic-probes-adapted.json")
source=source.replace("from app.desk_core import engine as e", "from app.desk_core import engine as e\nfrom app.desk_core import bookio as io")
injection='''
def binary_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
def binary_exclusive(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'xb') as h:
        h.write(data)
io.atomic_write=binary_write
io.exclusive_write=binary_exclusive
e.atomic_write=binary_write
e.exclusive_write=binary_exclusive
'''
source=source.replace("e.file_lock=lambda path:contextlib.nullcontext()", "e.file_lock=lambda path:contextlib.nullcontext()\n"+injection)
source=source.replace('serial unit probes with file_lock replaced by nullcontext in memory; native Windows CLI remains failed',
                      'serial exploratory unit probes: lock replaced by nullcontext AND low-level writes replaced by binary Python writes in memory; native submitted CLI remains failed; no platform/concurrency validation')
exec(compile(source,__file__,'exec'))
