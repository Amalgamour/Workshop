import pathlib,runpy,shutil,sys,tempfile
base=pathlib.Path(sys.argv[1]).resolve();base.mkdir()
tempfile.tempdir=str(base)
original=shutil.rmtree
def guarded(path,*a,**kw):
    assert pathlib.Path(path).resolve().is_relative_to(base)
    return original(path,*a,**kw)
shutil.rmtree=guarded
script=sys.argv[2];sys.argv=[script,*sys.argv[3:]]
runpy.run_path(script,run_name='__main__')
