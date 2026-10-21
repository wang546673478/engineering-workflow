import json
import sqlite3
from pathlib import Path
import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('task_archive_cli', SCRIPTS / 'task_archive.py')
task_archive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_archive)

class TaskArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'
        self.root.mkdir()
        self.store = Path(self.tmp.name) / 'host-state' / 'archive.sqlite3'
        (self.root / 'engineering-manifest.json').write_text(json.dumps({'documents': [{'id': 'TASK', 'path': 'planning/task.md'}]}), encoding='utf-8')
        (self.root / 'planning').mkdir()
        (self.root / 'planning/task.md').write_bytes(b'task revision one\r\n')

    def run_cli(self, *args, expected=0):
        output = io.StringIO()
        errors = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = task_archive.main([
                '--root', str(self.root), '--manifest', 'engineering-manifest.json',
                '--project-id', 'synthetic-project', '--store', str(self.store), *args,
            ])
        self.assertEqual(code, expected, output.getvalue() + errors.getvalue())
        raw = output.getvalue().strip() or errors.getvalue().strip()
        return json.loads(raw) if raw.startswith('{') else {}

    def init(self):
        return self.run_cli('init', '--reason', 'synthetic baseline')

    def test_initial_snapshot_is_exact_and_outside_workspace(self):
        result = self.init()
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['document_count'], 2)
        self.assertTrue(self.store.is_file())
        self.assertFalse((self.root / '.engineering-state').exists())
        self.assertEqual(self.run_cli('check')['status'], 'pass')

    def test_full_overwrite_is_detected_and_remains_recoverable(self):
        initial = self.init()['revision']
        (self.root / 'planning/task.md').write_text('test text', encoding='utf-8')
        result = self.run_cli('check', expected=1)
        self.assertEqual(result['head_revision'], initial)
        self.assertIn('planning/task.md', ' '.join(result['differences']))
        history = self.run_cli('history')['revisions']
        self.assertEqual(len(history), 1)

    def test_checkpoint_and_restore_use_new_immutable_revisions(self):
        first = self.init()['revision']
        (self.root / 'planning/task.md').write_text('task revision two\n', encoding='utf-8')
        second = self.run_cli('check', '--save', '--expected-head', first, '--reason', 'accepted edit')['revision']
        self.assertNotEqual(first, second)
        restored = self.run_cli('restore', first, '--reason', 'recover saved task')
        self.assertNotEqual(restored['revision'], first)
        self.assertEqual((self.root / 'planning/task.md').read_bytes(), b'task revision one\r\n')
        history = self.run_cli('history')['revisions']
        self.assertEqual([row['revision'] for row in history], [first, second, restored['revision']])

    def test_restore_refuses_nonexistent_revision(self):
        self.init()
        result = self.run_cli('restore', 'missing-revision', expected=2)
        self.assertEqual(result['status'], 'error')

    def test_stale_checkpoint_and_unsaved_restore_are_refused(self):
        first = self.init()['revision']
        (self.root / 'planning/task.md').write_text('task revision two\n', encoding='utf-8')
        second = self.run_cli('check', '--save', '--expected-head', first)['revision']
        (self.root / 'planning/task.md').write_text('unarchived edit\n', encoding='utf-8')
        stale = self.run_cli('check', '--save', '--expected-head', first, expected=2)
        self.assertEqual(stale['status'], 'error')
        refused = self.run_cli('restore', first, expected=2)
        self.assertEqual(refused['status'], 'error')
        self.assertEqual((self.root / 'planning/task.md').read_text(encoding='utf-8'), 'unarchived edit\n')
        self.assertEqual(self.run_cli('history')['revisions'][-1]['revision'], second)

    def test_interrupted_checkpoint_transaction_keeps_old_head_and_history(self):
        first = self.init()['revision']
        (self.root / 'planning/task.md').write_text('task revision two\n', encoding='utf-8')
        connection = sqlite3.connect(self.store)
        connection.execute("CREATE TRIGGER abort_revision_file BEFORE INSERT ON files WHEN NEW.document_id='TASK' BEGIN SELECT RAISE(ABORT,'synthetic interruption'); END")
        connection.commit()
        connection.close()

        result = self.run_cli('check', '--save', '--expected-head', first, expected=2)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(self.run_cli('history')['revisions'][-1]['revision'], first)

        connection = sqlite3.connect(self.store)
        connection.execute("DROP TRIGGER abort_revision_file")
        connection.commit()
        connection.close()
        saved = self.run_cli('check', '--save', '--expected-head', first)
        self.assertEqual(saved['parent_revision'], first)

if __name__ == '__main__':
    unittest.main()
