# Working tool: 10.workshop/10.10.work/10.10.10.lib/code/install.py
import runpy
from pathlib import Path
runpy.run_path(
    str(Path(__file__).resolve().parents[1] / '10.workshop' / '10.10.work' / '10.10.10.lib' / 'code' / 'install.py'),
    run_name='__main__',
)
