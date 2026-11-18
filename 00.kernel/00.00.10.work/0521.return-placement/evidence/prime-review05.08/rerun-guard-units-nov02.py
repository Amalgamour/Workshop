from pathlib import Path
import importlib.util,unittest,io,json,sys
sys.dont_write_bytecode=True
out=Path('D:/librarian/temp/0521-pass08-prime');path=Path('D:/Git/lib-build/labs/return-capture-guard-pass01/tests/test_guard.py')
spec=importlib.util.spec_from_file_location('guard_author_tests',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
original_root=str(m.ROOT);m.ROOT=out/'unit-root';m.ROOT.mkdir(exist_ok=False)
stream=io.StringIO();suite=unittest.defaultTestLoader.loadTestsFromModule(m);result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
(out/'unit-relocated-root.txt').write_text(stream.getvalue(),encoding='utf-8')
summary={'adaptation':'Unmodified author test functions, ROOT assigned to a normally created retained workspace directory after import. The original tempfile-created ROOT produced WinError 5 in the first direct run. No source edits or ACL changes.','original_root':original_root,'selected_root':str(m.ROOT),'tests':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'passed':result.wasSuccessful()}
(out/'unit-relocated-root.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary));sys.exit(0 if result.wasSuccessful() else 1)
