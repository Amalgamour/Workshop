"""Reproduce demo using separate processes and run the acceptance suite."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def run(command, timeout=60):
    return subprocess.run(command, cwd=HERE, env=dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1'),
                          capture_output=True, text=True, encoding='utf-8', timeout=timeout)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = out / 'demo'
    if work.exists():
        raise SystemExit('Choose a new output directory; preserved results will not be overwritten.')
    tests = run([sys.executable, '-B', '-X', 'utf8', str(HERE/'test_lab.py')], timeout=90)
    (out/'tests.txt').write_bytes((tests.stdout+tests.stderr).encode('utf-8'))
    steps = [('init', []), ('role', ['--role', 'builder']), ('live', []),
             ('role', ['--role', 'colab']), ('role', ['--role', 'builder']),
             ('role', ['--role', 'colab']), ('live', []), ('audit', [])]
    trace = []
    for command, extra in steps:
        result = run([sys.executable, '-B', '-X', 'utf8', str(HERE/'clerk_lab.py'), command, str(work), *extra])
        item = {'step': len(trace)+1, 'command': [command, *extra], 'exit': result.returncode,
                'stdout': result.stdout, 'stderr': result.stderr}
        trace.append(item)
        if result.returncode != 0:
            break
    (out/'transcript.json').write_bytes(json.dumps(trace,ensure_ascii=False,indent=2).encode('utf-8'))
    passed = tests.returncode == 0 and len(trace) == len(steps) and all(x['exit']==0 for x in trace)
    assessment = json.loads(trace[-1]['stdout']) if passed else {'passed': False}
    passed = passed and assessment.get('passed', False)
    report = {'passed': passed, 'test_exit': tests.returncode, 'processes': len(trace),
              'audit': assessment, 'role_fixture': 'Scripted Python actors, not live models',
              'manual_work_item_paths_given_to_roles': 0,
              'launcher_role_schedule': ['builder','colab','builder','colab'],
              'limitation': 'The launcher opens each role process. No model wakeup, autonomous scheduler, semantic AI review, or Director authentication is implemented.'}
    (out/'results.json').write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8'))
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
