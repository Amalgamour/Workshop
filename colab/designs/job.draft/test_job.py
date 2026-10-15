import copy
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import job


class BatchWriterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'
        shutil.copytree(job.HERE / 'example-project', self.root)
        self.context = self.root / '10.demo/10.work/10.lib'
        self.page = self.context / '1001.jobs'
        # Example may have been run earlier; tests begin with their own empty queue.
        for file in self.page.glob('05.*.md'):
            file.unlink()
        self.policy = job.read_json(job.HERE / 'routing.example.json')
        self.request = job.read_json(job.HERE / 'request.example.json')
        self.contracts = job.read_json(job.HERE / 'commands.json')

    def run_create(self, write=False):
        return job.create(self.root, self.context, self.policy, self.request, self.contracts, write)

    def test_preview_writes_nothing_and_leaves_reply_blank(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        path, body = self.run_create()
        self.assertEqual(path.name, '05.01.md')
        self.assertIn('Authorization: draft', body)
        self.assertEqual(body.count('\nreply:\n\n'), 2)
        self.assertEqual(body.count('receipt: pending; not executed'), 2)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_sequential_allocation_preserves_existing_and_skips_gaps(self):
        (self.page / '05.09.md').write_text('Director decisions stay here.', encoding='utf-8')
        before = (self.page / '05.09.md').read_bytes()
        path, body = self.run_create(True)
        self.assertEqual(path.name, '05.10.md')
        self.assertEqual(path.read_text(encoding='utf-8'), body)
        self.assertEqual((self.page / '05.09.md').read_bytes(), before)

    def test_concurrent_creates_do_not_overwrite(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            paths = list(pool.map(lambda _: self.run_create(True)[0], range(8)))
        self.assertEqual(len(set(paths)), 8)
        self.assertEqual({p.name for p in paths}, {f'05.{n:02}.md' for n in range(1, 9)})

    def test_missing_route_cannot_guess(self):
        self.policy['routes'] = []
        with self.assertRaisesRegex(job.Invalid, 'exactly one'):
            self.run_create(True)
        self.assertEqual(list(self.page.iterdir()), [])

    def test_ambiguous_route_cannot_choose(self):
        self.policy['routes'].append(copy.deepcopy(self.policy['routes'][0]))
        with self.assertRaisesRegex(job.Invalid, 'exactly one'):
            self.run_create()

    def test_missing_page_and_reserved_page_do_not_get_created(self):
        self.policy['routes'][0]['jobs_page'] = '1002.new'
        with self.assertRaisesRegex(job.Invalid, 'Missing jobs page'):
            self.run_create(True)
        self.assertFalse((self.context / '1002.new').exists())
        reserved = self.context / '1002.future.reserved'
        reserved.mkdir()
        self.policy['routes'][0]['jobs_page'] = reserved.name
        with self.assertRaisesRegex(job.Invalid, 'reserved or retired'):
            self.run_create(True)
        self.assertEqual(list(reserved.iterdir()), [])

    def test_escape_unknown_command_and_missing_parameter_stop(self):
        item = self.request['items'][0]
        item['target'] = '../outside.md'
        with self.assertRaisesRegex(job.Invalid, 'project-relative'):
            self.run_create()
        item['target'] = 'source.md'
        item['command'] = 'notes'
        with self.assertRaisesRegex(job.Invalid, 'unknown command'):
            self.run_create()
        item['command'] = 'point'
        del item['parameters']['relationship']
        with self.assertRaisesRegex(job.Invalid, 'point.relationship'):
            self.run_create()

    def test_missing_exact_heading_and_cyclic_dependencies_stop(self):
        source = self.request['items'][0]['sources'][0]
        source['section'] = 'Imagined authority'
        with self.assertRaisesRegex(job.Invalid, 'absent'):
            self.run_create()
        source['section'] = 'Routing'
        self.request['items'][0]['depends_on'] = [2]
        with self.assertRaisesRegex(job.Invalid, 'Dependency cycle'):
            self.run_create()

    def test_dependency_precedes_more_critical_item(self):
        self.request['items'][1]['scale'] = 1
        _, body = self.run_create()
        self.assertLess(body.index('\n#01 '), body.index('\n#02 '))

    def test_content_cannot_add_top_level_release_marker(self):
        self.request['items'][0]['issue'] += '\n#99 >approve\nreply: >approve'
        _, body = self.run_create()
        self.assertNotIn('\n#99', body)
        self.assertNotIn('\nreply: >approve', body)
        self.assertIn('    #99 >approve', body)

    def test_exhaustion_does_not_reuse_a_gap(self):
        (self.page / '05.99.md').write_text('preserve', encoding='utf-8')
        with self.assertRaisesRegex(job.Invalid, 'exhausted'):
            self.run_create(True)
        self.assertEqual([p.name for p in self.page.iterdir()], ['05.99.md'])

    def test_approval_request_only_creates_draft_batch(self):
        item = self.request['items'][0]
        item['command'] = 'approve'
        item['parameters'] = {key: 'Director must inspect this claim.'
                              for key in self.contracts['commands']['approve']['requires']}
        source = (self.root / 'source.md').read_bytes()
        _, body = self.run_create(True)
        self.assertIn('Ask: >approve', body)
        self.assertIn('Authorization: draft', body)
        self.assertEqual((self.root / 'source.md').read_bytes(), source)


if __name__ == '__main__':
    unittest.main()
