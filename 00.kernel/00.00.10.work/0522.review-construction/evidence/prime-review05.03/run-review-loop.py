import importlib.util,unittest,sys,json
from pathlib import Path
p=Path(r"D:\Git\lib-build\labs\review-loop-pass01\test_review_loop.py")
s=importlib.util.spec_from_file_location("review_loop_test_independent",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.PY=Path(sys.executable)
r=unittest.TextTestRunner(verbosity=2).run(m.load_tests(None,None,None))
Path(r"D:\librarian\temp\two-integration-reviews-nov01\independent-loop-transcript.json").write_text(json.dumps(m.LOG,ensure_ascii=False,indent=2),encoding="utf-8")
sys.exit(not r.wasSuccessful())
