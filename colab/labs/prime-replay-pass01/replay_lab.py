"""Bounded setup/command recorder for a contextual Prime replay. No model or network calls."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

LAB = Path(__file__).resolve().parent
BOOK = '00.kernel/00.00.10.work'
def stamp(): return datetime.now(timezone.utc).isoformat()
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
def verify():
    seal = json.loads((LAB / 'seal.json').read_text(encoding='utf-8'))
    for row in seal['files']:
        p = LAB / row['path']
        assert p.is_file() and p.stat().st_size == row['bytes'] and digest(p) == row['sha256'], row['path']
    return seal
def prepare(model):
    seal = verify()
    root = LAB / 'runs' / model
    root.mkdir(parents=True, exist_ok=False)
    started, t = stamp(), time.monotonic()
    order = json.loads((LAB / 'roster.json').read_text())[model]
    for index, (case, condition) in enumerate(order, 1):
        run = root / f'{index:02}-{case}-{condition}'
        shutil.copytree(LAB / 'inputs' / case / 'repository', run / 'repository')
        (run / 'out').mkdir()
        (run / 'deliverables').mkdir()
        c = json.loads((LAB / 'inputs' / case / 'case.json').read_text())
        shutil.copyfile(LAB / 'inputs' / case / 'case.json', run / 'case.json')
        repo = run / 'repository'
        env = dict(os.environ, GIT_AUTHOR_NAME='Replay lab', GIT_AUTHOR_EMAIL='replay@local',
                   GIT_COMMITTER_NAME='Replay lab', GIT_COMMITTER_EMAIL='replay@local')
        for argv in [['git', 'init', '-q'], ['git', 'add', '--all'],
                     ['git', 'commit', '-q', '-m', 'Frozen replay input, not project work']]:
            subprocess.run(argv, cwd=repo, env=env, check=True, capture_output=True)
        # The same registration and work agreement is visible to both conditions.
        # Only assisted may invoke the reviewed optional interfaces.
        reg = {'schema': 'prime-cycle-registration/1', 'repository': str(repo), 'book': BOOK,
            'book_label': '00.00.10.work', 'source': {'kind': 'live-file', 'commit': None},
            'members_book': str(repo / BOOK), 'output_root': str(run / 'out'),
            'bounds': {'max_works': 16, 'max_page_bytes': 262144, 'max_output_bytes': 2097152},
            'works': [{'work_id': case, 'page': c['page'], 'pass': c['pass'], 'member': c['member'],
                'goal': {'goal_id': case + '-goal', 'statement': c['goal']}, 'agreement': c['agreement'],
                'review_location': c['page'].rsplit('/', 1)[0] + '/evidence/prime-cycle-reviews/05.01'}]}
        save(run / 'registration.json', reg)
        save(run / 'run.json', {'model_label': model, 'case': case, 'condition': condition, 'order': index,
            'repository': str(repo), 'out': str(run / 'out'), 'registration': str(run / 'registration.json'),
            'journal': str(run / 'out/journal'), 'assistance': str(LAB / 'assistance/labs/prime-cycle-pass01/prime_cycle.py'),
            'notice': 'Labels are supplied, not model identity authentication. Same-session carryover is expected.'})
    save(root / 'setup.json', {'started_utc': started, 'ended_utc': stamp(), 'seconds': time.monotonic() - t,
        'seal_sha256': digest(LAB / 'seal.json'), 'conditions_prepared_before_answers': True,
        'note': 'Preparation only. No reviewed helper, historical target code or model answer was executed.'})
    print(root)
def command(model, run_id, argv):
    root = LAB / 'runs' / model
    run = root / run_id
    assert run.parent == root and run.is_dir() and run_id in {p.name for p in root.iterdir() if p.is_dir()}
    if argv and argv[0] == '--': argv = argv[1:]
    assert argv, 'Supply an executable and arguments after --'
    event = run / 'operations' / uuid.uuid4().hex
    event.mkdir(parents=True, exist_ok=False)
    save(event / 'start.json', {'started_utc': stamp(), 'argv': argv, 'cwd': str(run / 'repository'),
        'coverage': 'This wrapped subprocess and captured stdout/stderr only; tool-reader calls and model thinking are not observed.'})
    t = time.monotonic()
    try:
        with (event / 'stdout.txt').open('xb') as out, (event / 'stderr.txt').open('xb') as err:
            p = subprocess.run(argv, cwd=run / 'repository', stdout=out, stderr=err)
        save(event / 'end.json', {'ended_utc': stamp(), 'seconds': time.monotonic() - t, 'exit': p.returncode,
            'stdout_sha256': digest(event / 'stdout.txt'), 'stdout_bytes': (event / 'stdout.txt').stat().st_size,
            'stderr_sha256': digest(event / 'stderr.txt'), 'stderr_bytes': (event / 'stderr.txt').stat().st_size})
        print('operation', event, 'exit', p.returncode)
        for name in ['stdout.txt', 'stderr.txt']:
            raw = (event / name).read_bytes()
            sys.stdout.write(raw[:16000].decode('utf-8', 'replace'))
            if len(raw) > 16000: print('\n[Display truncated; full bytes retained in operation file.]')
        return p.returncode
    except BaseException:
        print('Incomplete operation retained at', event, file=sys.stderr)
        raise
def export(model):
    root = LAB / 'runs' / model
    assert (root / 'return.md').is_file(), 'Write the substantive Colab return first.'
    target = LAB / 'results' / model
    target.mkdir(parents=True, exist_ok=False)
    for name in ['return.md', 'setup.json']:
        shutil.copyfile(root / name, target / name)
    metrics = []
    for run in sorted(p for p in root.iterdir() if p.is_dir()):
        dest = target / run.name
        dest.mkdir()
        for name in ['run.json', 'registration.json', 'case.json']:
            shutil.copyfile(run / name, dest / name)
        for name in ['deliverables', 'out', 'operations']:
            if (run / name).exists(): shutil.copytree(run / name, dest / name)
        repo = run / 'repository'
        diff = subprocess.check_output(['git', 'diff', '--binary', 'HEAD'], cwd=repo)
        (dest / 'source-changes.patch').write_bytes(diff)
        reviews = repo / BOOK
        for folder in reviews.glob('*/evidence/prime-cycle-reviews'):
            shutil.copytree(folder, dest / 'typed-reviews' / folder.parent.parent.name)
        events = list((run / 'operations').glob('*/start.json')) if (run / 'operations').exists() else []
        ends = [json.loads(p.read_text()) for p in (run / 'operations').glob('*/end.json')] if events else []
        metrics.append({'run': run.name, 'wrapped_commands_started': len(events), 'wrapped_commands_ended': len(ends),
            'command_seconds_sum': sum(e['seconds'] for e in ends), 'stdout_bytes': sum(e['stdout_bytes'] for e in ends),
            'stderr_bytes': sum(e['stderr_bytes'] for e in ends), 'exit_counts': {str(k): sum(e['exit'] == k for e in ends) for k in sorted({e['exit'] for e in ends})},
            'tokens': None, 'cost': None, 'note': 'Command duration sum excludes reasoning, direct file readers and setup; not model latency or productivity. See supplied per-run friction notes.'})
    save(target / 'measurements.json', {'schema': 'prime-replay-measurements/1', 'model_label': model, 'runs': metrics})
    files = [{'path': p.relative_to(target).as_posix(), 'bytes': p.stat().st_size, 'sha256': digest(p)}
             for p in sorted(target.rglob('*')) if p.is_file()]
    save(target / 'artifact-index.json', {'schema': 'prime-replay-artifacts/1', 'files': files, 'note': 'Index excludes itself. Frozen inputs are referenced by the sealed lab, not duplicated here.'})
    print(target)
def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest='mode', required=True)
    s.add_parser('verify')
    q = s.add_parser('prepare'); q.add_argument('--model', choices=['codex', 'grok', 'claude'], required=True)
    q = s.add_parser('export'); q.add_argument('--model', choices=['codex', 'grok', 'claude'], required=True)
    q = s.add_parser('command'); q.add_argument('--model', choices=['codex', 'grok', 'claude'], required=True)
    q.add_argument('--run', required=True); q.add_argument('argv', nargs=argparse.REMAINDER)
    a = p.parse_args()
    if a.mode == 'verify':
        print('seal verified', len(verify()['files']), 'files'); return 0
    if a.mode == 'prepare': prepare(a.model); return 0
    if a.mode == 'export': export(a.model); return 0
    return command(a.model, a.run, a.argv)
if __name__ == '__main__':
    raise SystemExit(main())
