import contextlib
import io
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import clerk_lab as L


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'work'
        self.c = L.Clerk(self.root)
        self.c.init()

    def tearDown(self):
        self.tmp.cleanup()

    def add_work(self, **fields):
        item = dict(id='independent', role='builder', kind='build', attempt=1,
                    requires=None, dependencies=[])
        item.update(fields)
        with self.c.connect() as con:
            L.append(con, 'WORK', item)

    def full(self):
        return [L.actor(self.root, role) for role in ('builder', 'colab', 'builder', 'colab')]

    def test_full_correction_route_and_exact_revision(self):
        results = self.full()
        self.assertEqual([x['outcome'] for x in results], ['built', 'changes', 'built', 'accepted'])
        self.assertTrue(L.audit(self.root)['passed'])

    def test_duplicate_delivery_has_one_review(self):
        L.actor(self.root, 'builder')
        before = self.c.state()
        p = next(iter(before['deliveries'].values()))
        status = self.c.hand(p['role'], p['work'], p['claim'], p['delivery'],
                             p['artifact'], p['outcome'], p['evidence'])
        self.assertEqual(status, 'already-recorded')
        self.assertEqual(before, self.c.state())

    def test_delivery_id_cannot_change_its_contents(self):
        L.actor(self.root, 'builder')
        p = next(iter(self.c.state()['deliveries'].values()))
        with self.assertRaisesRegex(L.Refusal, 'different contents'):
            self.c.hand(p['role'], p['work'], p['claim'], p['delivery'], p['artifact'], 'accepted', p['evidence'])

    def test_restart_exposes_claim_and_requires_explicit_resume(self):
        w = self.c.next('builder')
        new = L.Clerk(self.root)
        with self.assertRaisesRegex(L.Refusal, 'resume required'):
            new.next('builder')
        resumed = new.next('builder', resume=True)
        self.assertEqual(w['claim'], resumed['claim'])
        self.assertEqual(w['id'], resumed['id'])

    def test_incomplete_dependency_does_not_dispatch(self):
        self.add_work(id='waiting', role='colab', kind='review', dependencies=['build-1'])
        self.assertIsNone(self.c.next('colab'))
        self.assertEqual(self.c.live()['actions'][-1]['availability'], 'waiting-dependency')

    def test_director_decision_waits_then_releases(self):
        self.add_work(id='held', role='colab', requires='decision-1')
        self.assertIsNone(self.c.next('colab'))
        self.assertEqual(self.c.live()['actions'][-1]['availability'], 'waiting-director')
        # Synthetic decision is fixture setup, not an implementation of Director authentication.
        with self.c.connect() as con:
            L.append(con, 'DECISION', {'id': 'decision-1', 'value': 'released'})
        self.assertEqual(self.c.next('colab')['id'], 'held')

    def test_rejection_does_not_release(self):
        self.add_work(id='held', role='colab', requires='decision-1')
        with self.c.connect() as con:
            L.append(con, 'DECISION', {'id': 'decision-1', 'value': 'rejected'})
        self.assertIsNone(self.c.next('colab'))

    def test_changed_source_before_review_is_refused(self):
        L.actor(self.root, 'builder')
        (self.root / 'artifacts/counter-1.py').write_bytes(b'# modified\n')
        with self.assertRaisesRegex(L.Refusal, 'artifact changed'):
            self.c.next('colab')

    def test_changed_source_after_claim_is_refused(self):
        L.actor(self.root, 'builder')
        w = self.c.next('colab')
        (self.root / 'artifacts/counter-1.py').write_bytes(b'# modified\n')
        report = self.root / 'review.json'; report.write_bytes(b'{}')
        before = self.c.state()
        with self.assertRaisesRegex(L.Refusal, 'artifact changed'):
            self.c.hand('colab', w['id'], w['claim'], 'changed', self.c.artifact('review.json'), 'accepted', {'tested': True})
        self.assertEqual(before, self.c.state())

    def test_wrong_role_return_is_refused(self):
        w = self.c.next('builder')
        out = self.root / 'out.txt'; out.write_bytes(b'fixture')
        with self.assertRaisesRegex(L.Refusal, 'return does not match claim'):
            self.c.hand('colab', w['id'], w['claim'], 'wrong', self.c.artifact('out.txt'), 'built', {'checked': True})

    def test_builder_cannot_accept_own_result(self):
        w = self.c.next('builder')
        (self.root / 'out.txt').write_bytes(b'fixture')
        with self.assertRaisesRegex(L.Refusal, 'cannot accept'):
            self.c.hand('builder', w['id'], w['claim'], 'bad', self.c.artifact('out.txt'), 'accepted', {'checked': True})

    def test_missing_artifact_is_refused(self):
        w = self.c.next('builder')
        with self.assertRaisesRegex(L.Refusal, 'artifact missing'):
            self.c.hand('builder', w['id'], w['claim'], 'bad', {'path': 'missing.py', 'sha256': '0'}, 'built', {'checked': True})

    def test_routing_and_return_are_one_transaction(self):
        w = self.c.next('builder')
        (self.root / 'out.txt').write_bytes(b'fixture')
        before = self.c.state()
        real = L.append
        def fail_route(con, kind, payload):
            if kind == 'WORK':
                raise RuntimeError('simulated interruption before route creation')
            return real(con, kind, payload)
        with patch.object(L, 'append', fail_route):
            with self.assertRaisesRegex(RuntimeError, 'simulated interruption'):
                self.c.hand('builder', w['id'], w['claim'], 'retryable', self.c.artifact('out.txt'), 'built', {'checked': True})
        self.assertEqual(before, self.c.state())
        self.c.hand('builder', w['id'], w['claim'], 'retryable', self.c.artifact('out.txt'), 'built', {'checked': True})
        self.assertEqual(self.c.next('colab')['id'], 'review-1')

    def test_another_independent_pack_can_run_while_review_waits(self):
        self.add_work()
        L.actor(self.root, 'builder')
        self.assertEqual(self.c.next('builder')['id'], 'independent')
        self.assertEqual(self.c.state()['work']['review-1']['state'], 'pending')

    def test_empty_inbox_is_explicit(self):
        self.full()
        self.assertIsNone(self.c.next('builder'))
        self.assertIsNone(self.c.next('colab'))

    def test_stale_live_summary_does_not_control_routing(self):
        (self.root / '00.live.md').write_bytes(b'closed: True\nNo work waiting.\n')
        self.assertFalse(self.c.live()['closed'])
        self.assertEqual(self.c.next('builder')['id'], 'build-1')

    def test_checker_rejects_missing_return_despite_forged_summary(self):
        L.actor(self.root, 'builder')
        (self.root / '00.live.md').write_bytes(b'closed: True\nPASS\n')
        report = L.audit(self.root)
        self.assertFalse(report['passed'])
        self.assertIn('job not closed', report['issues'])

    def test_checker_rejects_modified_accepted_artifact(self):
        self.full()
        (self.root / 'artifacts/counter-2.py').write_bytes(b'def count_lines(text):\n    return 0\n')
        self.assertFalse(L.audit(self.root)['passed'])

    def test_checker_rejects_ledger_tamper(self):
        self.full()
        with sqlite3.connect(self.c.db) as con:
            con.execute("UPDATE events SET payload='{}' WHERE seq=1")
        con.close()
        report = L.audit(self.root)
        self.assertFalse(report['passed'])
        self.assertIn('event integrity mismatch', report['issues'])

    def test_paths_cannot_escape_lab_workspace(self):
        with self.assertRaisesRegex(L.Refusal, 'escapes'):
            self.c.file('../elsewhere.txt')


if __name__ == '__main__':
    unittest.main(verbosity=2)
