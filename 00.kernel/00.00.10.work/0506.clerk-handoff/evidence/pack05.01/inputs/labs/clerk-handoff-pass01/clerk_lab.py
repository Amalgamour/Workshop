"""Isolated Workshop dispatcher experiment. Python standard library only."""
from pathlib import Path
import argparse
from contextlib import contextmanager
import hashlib
import json
import sqlite3
import subprocess
import sys
import uuid

LAB_ID = 'clerk-handoff-pass01'
SPEC = 'Count lines containing at least one non-whitespace character.'
CASES = [('apple\n\npear\n', 2), (' \n\t\n', 0), ('', 0), (' apple \n pear', 2)]


class Refusal(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def event_hash(seq, kind, payload, prev):
    return digest(canonical([seq, kind, payload, prev]).encode('utf-8'))


def events(conn):
    return [dict(seq=s, kind=k, payload=json.loads(p), prev=prev, hash=h)
            for s, k, p, prev, h in conn.execute('SELECT seq,kind,payload,prev,hash FROM events ORDER BY seq')]


def append(conn, kind, payload):
    last = conn.execute('SELECT seq,hash FROM events ORDER BY seq DESC LIMIT 1').fetchone()
    seq, prev = (last[0] + 1, last[1]) if last else (1, '')
    h = event_hash(seq, kind, payload, prev)
    conn.execute('INSERT INTO events VALUES (?,?,?,?,?)', (seq, kind, canonical(payload), prev, h))


def project(rows):
    """Derived views never replace the event record."""
    state = {'job': None, 'work': {}, 'decisions': {}, 'closed': False, 'deliveries': {}}
    prev = ''
    for expected, e in enumerate(rows, 1):
        p, kind = e['payload'], e['kind']
        if e['seq'] != expected or e['prev'] != prev or e['hash'] != event_hash(e['seq'], kind, p, prev):
            raise Refusal('event integrity mismatch')
        prev = e['hash']
        if kind == 'JOB':
            if state['job'] is not None:
                raise Refusal('job already declared')
            state['job'] = p
        elif kind == 'WORK':
            if p['id'] in state['work']:
                raise Refusal('duplicate work identity')
            state['work'][p['id']] = dict(p, state='pending', claim=None, result=None)
        elif kind == 'CLAIM':
            w = state['work'][p['work']]
            if w['state'] != 'pending' or w['role'] != p['role']:
                raise Refusal('invalid claim')
            w.update(state='claimed', claim=p['claim'])
        elif kind == 'RETURN':
            w = state['work'][p['work']]
            if w['state'] != 'claimed' or w['claim'] != p['claim'] or w['role'] != p['role']:
                raise Refusal('return does not match claim')
            if p['delivery'] in state['deliveries']:
                raise Refusal('duplicate delivery event')
            w.update(state='returned', result=p)
            state['deliveries'][p['delivery']] = p
        elif kind == 'DECISION':
            state['decisions'][p['id']] = p['value']
        elif kind == 'CLOSED':
            if state['closed']:
                raise Refusal('duplicate closure')
            state['closed'] = True
        else:
            raise Refusal('unrecognized event')
    return state


class Clerk:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.db = self.root / 'events.sqlite'

    @contextmanager
    def connect(self):
        if not self.db.is_file():
            raise Refusal('workspace is not initialized')
        con = sqlite3.connect(self.db, timeout=10)
        try:
            con.execute('BEGIN IMMEDIATE')
            yield con
            con.commit()
        except BaseException:
            con.rollback()
            raise
        finally:
            con.close()

    def init(self):
        self.root.mkdir(parents=True, exist_ok=True)
        if self.db.exists():
            raise Refusal('workspace already initialized')
        with sqlite3.connect(self.db) as con:
            con.execute('CREATE TABLE events(seq INTEGER PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL, prev TEXT NOT NULL, hash TEXT NOT NULL)')
            append(con, 'JOB', {
                'id': 'job-001', 'spec': SPEC,
                'route': {'build': 'colab', 'changes': 'builder', 'accepted': 'close'},
                'authority': 'Director-approved lab; correction within the original task is pre-authorized',
                'max_build_attempts': 2,
            })
            append(con, 'WORK', {'id': 'build-1', 'role': 'builder', 'kind': 'build', 'attempt': 1,
                                 'requires': None, 'dependencies': []})
        con.close()
        return self.live()

    def state(self):
        with self.connect() as con:
            return project(events(con))

    def file(self, rel):
        relpath = Path(rel)
        if relpath.is_absolute():
            raise Refusal('artifact path must be relative')
        p = (self.root / relpath).resolve()
        if not p.is_relative_to(self.root):
            raise Refusal('artifact escapes workspace')
        return p

    def verify(self, artifact):
        p = self.file(artifact['path'])
        if not p.is_file():
            raise Refusal('artifact missing')
        if digest(p.read_bytes()) != artifact['sha256']:
            raise Refusal('artifact changed')
        return p

    def availability(self, w, state):
        if w['requires'] and state['decisions'].get(w['requires']) != 'released':
            return 'waiting-director'
        if any(state['work'].get(d, {}).get('state') != 'returned' for d in w['dependencies']):
            return 'waiting-dependency'
        return 'ready'

    def next(self, role, resume=False):
        with self.connect() as con:
            state = project(events(con))
            claimed = [w for w in state['work'].values() if w['role'] == role and w['state'] == 'claimed']
            if claimed:
                if not resume:
                    raise Refusal('unfinished claim exists; explicit resume required')
                w = claimed[0]
                if 'source' in w:
                    self.verify(w['source'])
                return w
            for w in state['work'].values():
                if w['role'] == role and w['state'] == 'pending' and self.availability(w, state) == 'ready':
                    if 'source' in w:
                        self.verify(w['source'])
                    claim = str(uuid.uuid4())
                    append(con, 'CLAIM', {'work': w['id'], 'role': role, 'claim': claim})
                    return dict(w, state='claimed', claim=claim)
            return None

    def artifact(self, path):
        p = self.file(path)
        if not p.is_file():
            raise Refusal('artifact missing')
        return {'path': str(p.relative_to(self.root)).replace('\\', '/'), 'sha256': digest(p.read_bytes())}

    def hand(self, role, work, claim, delivery, artifact, outcome, evidence):
        record = {'role': role, 'work': work, 'claim': claim, 'delivery': delivery,
                  'artifact': artifact, 'outcome': outcome, 'evidence': evidence}
        with self.connect() as con:
            state = project(events(con))
            if delivery in state['deliveries']:
                if state['deliveries'][delivery] != record:
                    raise Refusal('delivery identity reused with different contents')
                self.verify(artifact)
                return 'already-recorded'
            if work not in state['work']:
                raise Refusal('unknown work')
            w = state['work'][work]
            if w['role'] != role or w['state'] != 'claimed' or w['claim'] != claim:
                raise Refusal('return does not match claim')
            if self.availability(w, state) != 'ready':
                raise Refusal('work no longer released or dependency incomplete')
            self.verify(artifact)
            if 'source' in w:
                self.verify(w['source'])
            if not evidence:
                raise Refusal('return evidence missing')
            if w['kind'] == 'build' and outcome != 'built':
                raise Refusal('builder cannot accept its own result')
            if w['kind'] == 'review' and outcome not in ('changes', 'accepted'):
                raise Refusal('review disposition missing')
            if w['kind'] == 'review' and outcome == 'changes' and w['attempt'] >= state['job']['max_build_attempts']:
                raise Refusal('correction limit reached; intelligence must choose a new route')
            append(con, 'RETURN', record)
            if w['kind'] == 'build':
                append(con, 'WORK', {'id': 'review-' + str(w['attempt']), 'role': 'colab', 'kind': 'review',
                                     'attempt': w['attempt'], 'requires': None, 'dependencies': [work],
                                     'source': artifact})
            elif outcome == 'changes':
                n = w['attempt'] + 1
                append(con, 'WORK', {'id': 'build-' + str(n), 'role': 'builder', 'kind': 'build',
                                     'attempt': n, 'requires': None, 'dependencies': [work], 'source': artifact})
            else:
                append(con, 'CLOSED', {'job': state['job']['id'], 'review': work,
                                       'accepted_artifact': w['source']})
        return 'recorded'

    def live(self):
        state = self.state()
        with self.connect() as con:
            count = con.execute('SELECT COUNT(*) FROM events').fetchone()[0]
        view = {'job': state['job']['id'], 'goal': state['job']['spec'], 'closed': state['closed'],
                'events': count, 'actions': [
                    {'id': w['id'], 'role': w['role'], 'state': w['state'],
                     'availability': self.availability(w, state) if w['state'] == 'pending' else w['state']}
                    for w in state['work'].values()]}
        text = '# 00.live — lab projection\n\n' + '\n'.join([
            'job: ' + view['job'], 'goal: ' + view['goal'], 'closed: ' + str(view['closed']),
            'events: ' + str(count), '', '| action | role | state | availability |', '|---|---|---|---|',
            *['| {id} | {role} | {state} | {availability} |'.format(**w) for w in view['actions']]]) + '\n'
        # Rebuilt from the ledger on each request; a stale projection never drives routing.
        (self.root / '00.live.md').write_bytes(text.encode('utf-8'))
        return view


def exercise(source, all_cases=True):
    script = '''import json,runpy,sys
ns=runpy.run_path(sys.argv[1])
cases=json.loads(sys.argv[2])
rows=[{'input':s,'expected':n,'actual':ns['count_lines'](s)} for s,n in cases]
print(json.dumps(rows))
raise SystemExit(0 if all(r['actual']==r['expected'] for r in rows) else 1)
'''
    cases = CASES if all_cases else CASES[:1]
    proc = subprocess.run([sys.executable, '-B', '-c', script, str(source), json.dumps(cases)],
                          capture_output=True, text=True, encoding='utf-8', timeout=10)
    if proc.returncode not in (0, 1) or not proc.stdout.strip():
        raise Refusal('artifact test could not run: ' + proc.stderr)
    return {'passed': proc.returncode == 0, 'cases': json.loads(proc.stdout)}


def actor(root, role):
    """Scripted role fixture, deliberately not an LLM or semantic reviewer."""
    clerk = Clerk(root)
    work = clerk.next(role)
    if work is None:
        raise Refusal('no ready action for role')
    out = clerk.root / 'artifacts'; out.mkdir(exist_ok=True)
    if work['kind'] == 'build':
        path = out / ('counter-' + str(work['attempt']) + '.py')
        body = 'return sum(bool(line) for line in text.splitlines())' if work['attempt'] == 1 else 'return sum(bool(line.strip()) for line in text.splitlines())'
        path.write_bytes(('def count_lines(text):\n    ' + body + '\n').encode('utf-8'))
        evidence = exercise(path, all_cases=False)
        artifact = clerk.artifact(path.relative_to(clerk.root))
        outcome = 'built'
    else:
        source = clerk.verify(work['source'])
        evidence = exercise(source)
        path = out / ('review-' + str(work['attempt']) + '.json')
        outcome = 'accepted' if evidence['passed'] else 'changes'
        path.write_bytes(json.dumps({'source': work['source'], 'outcome': outcome, 'tests': evidence}, indent=2).encode('utf-8'))
        artifact = clerk.artifact(path.relative_to(clerk.root))
    clerk.hand(role, work['id'], work['claim'], 'delivery-' + work['id'], artifact, outcome, evidence)
    clerk.live()
    return {'role': role, 'work': work['id'], 'outcome': outcome, 'artifact': artifact, 'tests': evidence}


def _audit(root):
    """Acceptance checker reads raw events/artifacts, never trusts 00.live or a PASS label."""
    clerk = Clerk(root)
    with clerk.connect() as con:
        rows = events(con)
    state = project(rows)
    issues = []
    expected = [('build-1', 'builder', 'built'), ('review-1', 'colab', 'changes'),
                ('build-2', 'builder', 'built'), ('review-2', 'colab', 'accepted')]
    returns = [e['payload'] for e in rows if e['kind'] == 'RETURN']
    actual = [(p['work'], p['role'], p['outcome']) for p in returns]
    if actual != expected:
        issues.append('expected build/review/correction/review route missing or different')
    if not state['closed']:
        issues.append('job not closed')
    for e in rows:
        p = e['payload']
        if e['kind'] == 'RETURN':
            try:
                clerk.verify(p['artifact'])
            except Refusal as exc:
                issues.append(str(exc))
            if not p['evidence']:
                issues.append('missing evidence')
        if e['kind'] == 'WORK':
            for dep in p['dependencies']:
                earlier = [x['payload']['work'] for x in rows if x['seq'] < e['seq'] and x['kind'] == 'RETURN']
                if dep not in earlier:
                    issues.append('route created before dependency returned')
    if len(actual) == 4:
        for n in (1, 2):
            build = state['work']['build-' + str(n)]['result']
            review = state['work']['review-' + str(n)]
            if review['source'] != build['artifact']:
                issues.append('review does not cover exact build revision')
            path = clerk.verify(review['result']['artifact'])
            doc = json.loads(path.read_text(encoding='utf-8'))
            if doc['source'] != build['artifact']:
                issues.append('review artifact names another revision')
        final = clerk.verify(state['work']['build-2']['result']['artifact'])
        if not exercise(final)['passed']:
            issues.append('final function fails independent expected cases')
    return {'passed': not issues, 'issues': issues, 'events': len(rows), 'route': actual,
            'final_state': 'closed' if state['closed'] else 'open',
            'boundary': 'real persistence/routing; scripted roles, not live models'}


def audit(root):
    try:
        return _audit(root)
    except (Refusal, KeyError, ValueError, sqlite3.DatabaseError) as exc:
        return {'passed': False, 'issues': [str(exc)], 'boundary': 'raw ledger/artifact validation failed'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['init', 'live', 'role', 'audit'])
    p.add_argument('root', type=Path)
    p.add_argument('--role', choices=['builder', 'colab'])
    a = p.parse_args()
    try:
        if a.command == 'init':
            result = Clerk(a.root).init()
        elif a.command == 'live':
            result = Clerk(a.root).live()
        elif a.command == 'role':
            if a.role is None:
                raise Refusal('role required')
            result = actor(a.root, a.role)
        else:
            result = audit(a.root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if a.command == 'audit' and not result['passed']:
            raise SystemExit(1)
    except Refusal as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
