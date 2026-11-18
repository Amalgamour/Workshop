
import sys, json, importlib.machinery, importlib.util
from pathlib import Path
sys.dont_write_bytecode = True
loader = importlib.machinery.SourceFileLoader("pass04_proposal", sys.argv[1])
spec = importlib.util.spec_from_loader("pass04_proposal", loader)
m = importlib.util.module_from_spec(spec); loader.exec_module(m)
root = Path(sys.argv[2]).resolve()
m.p3.wb.REPO = root; m.p3.p2.REPO = root; m.p3.REPO = root      # lab-only redirect, same as n7compat2 --repo-root
sys.exit(m.main(sys.argv[3:]))
