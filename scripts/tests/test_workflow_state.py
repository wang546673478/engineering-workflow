import json
import contextlib
import codecs
import ctypes
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import workflow_state
import task_archive
import check_project
class WorkflowStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'
        (self.root / 'planning').mkdir(parents=True)
        (self.root / 'planning/task.md').write_text('''# Current

## Decisions
Old decision

## Deferred
Later
''', encoding='utf-8')
        (self.root / 'planning/spec.md').write_text('# Spec\nREQ-1\n', encoding='utf-8')
        manifest = {'workflow': {'active_task': 'TASK-1'}, 'modules': [{'id': 'instructions'}], 'documents': [{'id': 'TASK_DOC', 'path': 'planning/task.md', 'kind': 'task'}, {'id': 'SPEC_DOC', 'path': 'planning/spec.md', 'kind': 'spec'}], 'tasks': [{'id': 'TASK-1', 'status': 'in_progress', 'artifact_links': {'spec': 'SPEC_DOC'}, 'artifact_revisions': {'spec': 'SPEC-1'}}]}
        (self.root / 'engineering-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        self.request = self.root / 'request.json'
        self.store = Path(self.tmp.name) / 'host' / 'archive.sqlite3'
    def context(self):
        return workflow_state.load_project(self.root, 'engineering-manifest.json')[:3]
    def init_archive(self):
        self.assertEqual(task_archive.main(['--root', str(self.root), '--manifest', 'engineering-manifest.json', '--project-id', 'state-test', '--store', str(self.store), 'init']), 0)
        with contextlib.closing(task_archive.open_archive(self.store, 'state-test')) as db:
            return task_archive.head(db)
    def test_index_preserves_lifecycle_and_unknown_history(self):
        manifest = json.loads((self.root / 'engineering-manifest.json').read_text())
        manifest['documents'][0]['lifecycle'] = {'status': 'current'}
        (self.root / 'planning/spec-2.md').write_text('# Spec 2\n', encoding='utf-8')
        manifest['documents'].append({'id': 'SPEC-2', 'path': 'planning/spec-2.md', 'kind': 'spec'})
        manifest['documents'][1]['lifecycle'] = {'status': 'superseded', 'reason': 'replaced', 'superseded_by': 'SPEC-2', 'evidence': 'TASK_DOC'}
        manifest['documents'].extend([{'id': 'DONE', 'path': 'planning/done.md', 'kind': 'task', 'lifecycle': {'status': 'completed', 'evidence': 'TASK_DOC'}}, {'id': 'LATER', 'path': 'planning/later.md', 'kind': 'plan', 'lifecycle': {'status': 'deferred', 'module': 'instructions', 'conclusion': 'wait', 'question': 'when?', 'impact': 'Blocks rollout', 'depends_on': ['SPEC_DOC'], 'resumption_condition': 'approval'}}])
        for name in ('done.md', 'later.md'):
            (self.root / 'planning' / name).write_text(name, encoding='utf-8')
        (self.root / 'planning/old.md').write_text('unregistered legacy', encoding='utf-8')
        (self.root / 'engineering-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        rows = workflow_state.build_index(*self.context())
        by_id = {row['id']: row for row in rows}
        self.assertEqual(by_id['TASK_DOC']['lifecycle_status'], 'current')
        self.assertEqual(by_id['SPEC_DOC']['lifecycle_status'], 'superseded')
        self.assertEqual(by_id['SPEC_DOC']['lifecycle']['superseded_by'], 'SPEC-2')
        self.assertEqual(by_id['DONE']['lifecycle_status'], 'completed')
        self.assertEqual(by_id['LATER']['lifecycle_status'], 'deferred')
        self.assertEqual(by_id['TASK-1']['lifecycle_status'], 'current')
        self.assertEqual(by_id['TASK-1']['task_status'], 'in_progress')
        self.assertEqual(next(row for row in rows if row['path'] == 'planning/old.md')['lifecycle_status'], 'unknown/unverified')
    def test_nonactive_without_lifecycle_is_unverified_not_obsolete(self):
        (self.root / 'planning/old.md').write_text('unregistered history', encoding='utf-8')
        rows = workflow_state.build_index(*self.context())
        self.assertEqual(next(row for row in rows if row['id'] == 'SPEC_DOC')['lifecycle_status'], 'unknown/unverified')
        self.assertEqual(next(row for row in rows if row['path'] == 'planning/old.md')['lifecycle_status'], 'unknown/unverified')
    def test_active_pointer_and_explicit_lifecycle_conflict_is_exposed(self):
        manifest = json.loads((self.root / 'engineering-manifest.json').read_text())
        manifest['workflow']['active_spec'] = 'SPEC_DOC'
        manifest['documents'][1]['lifecycle'] = {'status': 'superseded', 'reason': 'replaced', 'superseded_by': 'TASK_DOC', 'evidence': 'TASK_DOC'}
        (self.root / 'engineering-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        row = next(row for row in workflow_state.build_index(*self.context()) if row['id'] == 'SPEC_DOC')
        self.assertEqual(row['lifecycle_status'], 'conflict')
    def test_snapshot_reads_exact_sections_and_returns_hash(self):
        result = workflow_state.snapshot(*self.context(), ['TASK_DOC'], ['Decisions'])
        self.assertEqual(result['documents'][0]['sections'][0]['content'], 'Old decision')
        self.assertRegex(result['documents'][0]['sha256'], r'^[0-9a-f]{64}$')
        with self.assertRaises(workflow_state.WorkflowStateError):
            workflow_state.snapshot(*self.context(), ['TASK_DOC'], ['Decisions', 'Decisions'])
    def test_snapshot_does_not_treat_heading_examples_inside_fences_as_sections(self):
        fence = chr(96) * 3
        (self.root / 'planning/task.md').write_text('# Real\n\n' + fence + 'markdown\n## Decisions\nexample only\n' + fence + '\n', encoding='utf-8')
        with self.assertRaises(workflow_state.WorkflowStateError):
            workflow_state.snapshot(*self.context(), ['TASK_DOC'], ['Decisions'])
    def test_snapshot_includes_full_content_when_no_sections_are_requested(self):
        result = workflow_state.snapshot(*self.context(), ['TASK_DOC'])
        self.assertIn('Old decision', result['documents'][0]['content'])
    def test_batch_section_replace_preserves_utf8_bom_and_normalizes_source_newlines(self):
        root, manifest_path, manifest = self.context()
        path = self.root / 'planning/task.md'
        path.write_bytes(codecs.BOM_UTF8 + b'# Current\r\n\r\n## Decisions\r\nOld\r\n')
        head = self.init_archive()
        digest = workflow_state.digest(path.read_bytes())
        request = {'operation_id': 'bom-crlf-1', 'expected_archive_head': head, 'operations': [{'document_id': 'TASK_DOC', 'expected_sha256': digest, 'type': 'replace-section', 'section_id': 'Decisions', 'content': 'New\nLine'}]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        applied = workflow_state.apply_batch(root, manifest_path, manifest, self.request, self.store, 'state-test', apply=True)
        self.assertEqual(applied['status'], 'applied')
        raw = path.read_bytes()
        self.assertTrue(raw.startswith(codecs.BOM_UTF8))
        self.assertIn(b'New\r\nLine', raw)
        self.assertNotIn(b'\n', raw.replace(b'\r\n', b''))
    def test_public_cli_index_and_snapshot_return_machine_readable_results(self):
        (self.root / 'planning/legacy.md').write_text('unregistered historical record', encoding='utf-8')
        script = SCRIPTS / 'workflow_state.py'
        index = subprocess.run([sys.executable, str(script), '--root', str(self.root), 'index'], capture_output=True, text=True, check=False)
        self.assertEqual(index.returncode, 0, index.stderr)
        rows = json.loads(index.stdout)['entries']
        self.assertIn('planning/legacy.md', {row['path'] for row in rows})
        snap = subprocess.run([sys.executable, str(script), '--root', str(self.root), 'snapshot', '--document-id', 'TASK_DOC', '--section', 'Decisions'], capture_output=True, text=True, check=False)
        self.assertEqual(snap.returncode, 0, snap.stderr)
        self.assertEqual(json.loads(snap.stdout)['documents'][0]['sections'][0]['content'], 'Old decision')
    def test_apply_batch_is_explicit_idempotent_and_archived(self):
        head = self.init_archive()
        task = next(row for row in workflow_state.build_index(*self.context()) if row['id'] == 'TASK_DOC')
        spec_hash = workflow_state.digest((self.root / 'planning/spec.md').read_bytes())
        request = {'operation_id': 'update-1', 'expected_archive_head': head, 'operations': [{'document_id': 'TASK_DOC', 'expected_sha256': task['sha256'], 'type': 'replace-section', 'section_id': 'Decisions', 'content': 'New decision'}, {'document_id': 'SPEC_DOC', 'expected_sha256': spec_hash, 'type': 'replace-section', 'section_id': 'Spec', 'content': 'Updated spec'}]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        dry = workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=False)
        self.assertEqual(dry['status'], 'dry-run')
        self.assertIn('Old decision', (self.root / 'planning/task.md').read_text())
        applied = workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)
        self.assertEqual(applied['status'], 'applied')
        self.assertIn('New decision', (self.root / 'planning/task.md').read_text())
        self.assertEqual(workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)['status'], 'already_applied')
        with contextlib.closing(task_archive.open_archive(self.store, 'state-test')) as db:
            self.assertEqual(task_archive.head(db), applied['archive_revision'])
            self.assertEqual(db.execute('SELECT COUNT(*) FROM revisions').fetchone()[0], 2)
    def test_operation_id_reuse_with_different_request_is_rejected(self):
        head = self.init_archive()
        task = next(row for row in workflow_state.build_index(*self.context()) if row['id'] == 'TASK_DOC')
        request = {'operation_id': 'same-id', 'expected_archive_head': head, 'operations': [{'document_id': 'TASK_DOC', 'expected_sha256': task['sha256'], 'type': 'replace-section', 'section_id': 'Decisions', 'content': 'First'}]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)
        request['operations'][0]['content'] = 'Different request'
        self.request.write_text(json.dumps(request), encoding='utf-8')
        with self.assertRaises(workflow_state.BatchConflict):
            workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)
        self.assertIn('First', (self.root / 'planning/task.md').read_text())
    def test_stale_archive_head_is_rejected_before_target_write(self):
        head = self.init_archive()
        task = next(row for row in workflow_state.build_index(*self.context()) if row['id'] == 'TASK_DOC')
        request = {'operation_id': 'stale-head', 'expected_archive_head': 'stale', 'operations': [{'document_id': 'TASK_DOC', 'expected_sha256': task['sha256'], 'type': 'replace-section', 'section_id': 'Decisions', 'content': 'Never written'}]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        original = (self.root / 'planning/task.md').read_bytes()
        with self.assertRaises(workflow_state.BatchConflict):
            workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)
        self.assertEqual((self.root / 'planning/task.md').read_bytes(), original)
        with contextlib.closing(task_archive.open_archive(self.store, 'state-test')) as db:
            self.assertEqual(task_archive.head(db), head)
    def test_conflict_refuses_whole_batch(self):
        head = self.init_archive()
        original = (self.root / 'planning/task.md').read_bytes()
        request = {'operation_id': 'conflict-1', 'expected_archive_head': head, 'operations': [{'document_id': 'TASK_DOC', 'expected_sha256': '0' * 64, 'type': 'replace-section', 'section_id': 'Decisions', 'content': 'x'}]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        with self.assertRaises(workflow_state.BatchConflict):
            workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)
        self.assertEqual((self.root / 'planning/task.md').read_bytes(), original)
    def test_protected_manifest_gate_fields_cannot_be_batch_written(self):
        manifest = json.loads((self.root / 'engineering-manifest.json').read_text())
        for pointer in ('/workflow/active_task', '/tasks/0/approval/status', '/tasks/0/status', '/checks/0/timeout_seconds'):
            self.assertTrue(workflow_state.is_protected_manifest_path(pointer, manifest))
        self.assertFalse(workflow_state.is_protected_manifest_path('/documents/1/lifecycle/status', manifest))
    def test_lifecycle_json_update_requires_traceable_evidence(self):
        head = self.init_archive()
        manifest_raw = (self.root / 'engineering-manifest.json').read_bytes()
        pointer = '/documents/1/lifecycle'
        request = {'operation_id': 'lifecycle-1', 'expected_archive_head': head, 'operations': [{'document_id': 'ENGINEERING_MANIFEST', 'expected_sha256': workflow_state.digest(manifest_raw), 'type': 'set-json-pointer', 'pointer': pointer, 'value': {'status': 'obsolete', 'reason': 'replaced', 'superseded_by': 'unknown', 'evidence': 'no-such-doc'}}]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        with self.assertRaises(workflow_state.WorkflowStateError):
            workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=False)
        self.assertEqual((self.root / 'engineering-manifest.json').read_bytes(), manifest_raw)
    def test_writer_rejects_duplicate_json_keys_before_any_update(self):
        raw = b'{"operation_id":"x","operation_id":"y","expected_archive_head":"head","operations":[]}'
        with self.assertRaisesRegex(workflow_state.WorkflowStateError, 'duplicate JSON key'):
            workflow_state.strict_json(raw, 'request')
    def test_batch_rejects_request_inside_mutable_manifest_documents(self):
        head = self.init_archive()
        task = next(row for row in workflow_state.build_index(*self.context()) if row['id'] == 'TASK_DOC')
        request = {'operation_id': 'self-target', 'expected_archive_head': head, 'operations': [{'document_id': 'TASK_DOC', 'expected_sha256': task['sha256'], 'type': 'replace-section', 'section_id': 'Decisions', 'content': 'No'}]}
        request_path = self.root / 'planning/task.md'
        request_path.write_text(json.dumps(request), encoding='utf-8')
        with self.assertRaisesRegex(workflow_state.WorkflowStateError, 'must not be one of'):
            workflow_state.apply_batch(*self.context(), request_path, self.store, 'state-test', apply=False)
    def test_lifecycle_conflict_is_derived_and_cannot_be_persisted(self):
        errors = workflow_state.lifecycle_metadata_errors({'status': 'conflict'}, {'documents': [], 'modules': []})
        self.assertTrue(any('lifecycle status' in error for error in errors))
    def test_manifest_lifecycle_update_is_explicit_and_preserves_approval_state(self):
        head = self.init_archive()
        manifest_raw = (self.root / 'engineering-manifest.json').read_bytes()
        manifest = json.loads(manifest_raw)
        manifest['documents'][1]['lifecycle'] = {'status': 'draft'}
        request = {'operation_id': 'lifecycle-valid-1', 'expected_archive_head': head, 'operations': [{'document_id': 'ENGINEERING_MANIFEST', 'expected_sha256': workflow_state.digest(manifest_raw), 'type': 'set-json-pointer', 'pointer': '/documents/1/lifecycle', 'value': {'status': 'draft'}}]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        result = workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)
        updated = json.loads((self.root / 'engineering-manifest.json').read_text())
        self.assertEqual(result['status'], 'applied')
        self.assertEqual(updated['documents'][1]['lifecycle']['status'], 'draft')
        self.assertEqual(updated['tasks'][0]['status'], manifest['tasks'][0]['status'])
        self.assertEqual(updated['workflow'], manifest['workflow'])
    def test_json_lifecycle_pointer_is_created_only_on_declared_document(self):
        head = self.init_archive()
        raw = (self.root / 'engineering-manifest.json').read_bytes()
        request = {'operation_id': 'lifecycle-create', 'expected_archive_head': head, 'operations': [{'document_id': 'ENGINEERING_MANIFEST', 'expected_sha256': workflow_state.digest(raw), 'type': 'set-json-pointer', 'pointer': '/documents/1/lifecycle/status', 'value': 'draft'}]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        result = workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)
        self.assertEqual(result['status'], 'applied')
        updated = json.loads((self.root / 'engineering-manifest.json').read_text())
        self.assertEqual(updated['documents'][1]['lifecycle'], {'status': 'draft'})
    def test_snapshot_contains_task_spec_plan_and_open_item_summary(self):
        manifest = json.loads((self.root / 'engineering-manifest.json').read_text())
        manifest['workflow'].update({'active_spec': 'SPEC_DOC', 'active_plan': 'TASK_DOC'})
        manifest['documents'][0]['lifecycle'] = {'status': 'deferred', 'module': 'instructions', 'conclusion': 'later', 'question': 'when?', 'impact': 'Blocks completion', 'depends_on': ['TASK_DOC'], 'resumption_condition': 'approval'}
        (self.root / 'engineering-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        result = workflow_state.snapshot(*self.context(), ['TASK_DOC'])
        self.assertEqual(result['summary']['task']['id'], 'TASK-1')
        self.assertEqual({row['artifact'] for row in result['current_artifacts']}, {'spec', 'plan'})
        self.assertEqual(result['open_items'][0]['id'], 'TASK_DOC')
    def test_failed_second_replace_rolls_back_first_and_archive_head(self):
        head = self.init_archive()
        task = next(row for row in workflow_state.build_index(*self.context()) if row['id'] == 'TASK_DOC')
        spec = next(row for row in workflow_state.build_index(*self.context()) if row['id'] == 'SPEC_DOC')
        request = {'operation_id': 'rollback-1', 'expected_archive_head': head, 'operations': [
            {'document_id': 'TASK_DOC', 'expected_sha256': task['sha256'], 'type': 'replace-section', 'section_id': 'Decisions', 'content': 'Changed'},
            {'document_id': 'SPEC_DOC', 'expected_sha256': spec['sha256'], 'type': 'replace-section', 'section_id': 'Spec', 'content': 'Changed'},
        ]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        original = (self.root / 'planning/task.md').read_bytes()
        replace = workflow_state.atomic_replace
        calls = {'count': 0}
        def fail_second_replace(path, raw):
            calls['count'] += 1
            if calls['count'] == 2:
                raise OSError('injected second-file failure')
            return replace(path, raw)
        with self.assertRaises(OSError):
            with mock.patch.object(workflow_state, 'atomic_replace', side_effect=fail_second_replace):
                workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)
        self.assertEqual((self.root / 'planning/task.md').read_bytes(), original)
        self.assertEqual(calls['count'], 4)  # Both prepared files are attempted; the first one is restored after the injected second-file error.
        with contextlib.closing(task_archive.open_archive(self.store, 'state-test')) as db:
            self.assertEqual(task_archive.head(db), head)
    def test_unrelated_workspace_drift_rejects_batch_before_any_write(self):
        head = self.init_archive()
        task = next(row for row in workflow_state.build_index(*self.context()) if row['id'] == 'TASK_DOC')
        request = {'operation_id': 'drift-1', 'expected_archive_head': head, 'operations': [{'document_id': 'TASK_DOC', 'expected_sha256': task['sha256'], 'type': 'replace-section', 'section_id': 'Decisions', 'content': 'Changed'}]}
        self.request.write_text(json.dumps(request), encoding='utf-8')
        original = (self.root / 'planning/task.md').read_bytes()
        (self.root / 'planning/spec.md').write_text('concurrent edit', encoding='utf-8')
        with self.assertRaises(workflow_state.BatchConflict):
            workflow_state.apply_batch(*self.context(), self.request, self.store, 'state-test', apply=True)
        self.assertEqual((self.root / 'planning/task.md').read_bytes(), original)
        with contextlib.closing(task_archive.open_archive(self.store, 'state-test')) as db:
            self.assertEqual(task_archive.head(db), head)
    def test_invalid_project_root_is_reported_without_retry(self):
        with self.assertRaises(workflow_state.UnsupportedHostError):
            workflow_state.resolve_root(str(self.root / 'missing'))
    @unittest.skipUnless(os.name == 'nt', 'Windows short-path aliases are Windows-specific')
    def test_batch_accepts_short_alias_for_project_root(self):
        with tempfile.TemporaryDirectory(prefix='workflow state alias ') as tmp:
            root = Path(tmp) / 'project'
            (root / 'planning').mkdir(parents=True)
            task_path = root / 'planning/task.md'
            task_path.write_text('# Current\n\n## Decisions\nOld\n', encoding='utf-8')
            (root / 'planning/spec.md').write_text('# Spec\nREQ-1\n', encoding='utf-8')
            outside = Path(tmp) / 'outside'
            outside.mkdir()
            (outside / 'secret.md').write_text('outside', encoding='utf-8')
            manifest = {'workflow': {'active_task': 'TASK-1'}, 'modules': [{'id': 'instructions'}], 'documents': [{'id': 'TASK_DOC', 'path': 'planning/task.md', 'kind': 'task'}, {'id': 'SPEC_DOC', 'path': 'planning/spec.md', 'kind': 'spec'}], 'tasks': [{'id': 'TASK-1', 'status': 'in_progress'}]}
            (root / 'engineering-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            buffer = ctypes.create_unicode_buffer(32768)
            get_short = ctypes.windll.kernel32.GetShortPathNameW
            get_short.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint)
            get_short.restype = ctypes.c_uint
            written = get_short(str(root), buffer, len(buffer))
            self.assertGreater(written, 0)
            alias = Path(buffer.value)
            if alias == root:
                self.skipTest('This volume does not generate a short-path alias for the fixture')
            outside_alias = ctypes.create_unicode_buffer(32768)
            self.assertGreater(get_short(str(outside), outside_alias, len(outside_alias)), 0)

            request_path = alias / 'request.json'
            store = Path(tmp) / 'host/archive.sqlite3'
            head = task_archive.main(['--root', str(alias), '--manifest', 'engineering-manifest.json', '--project-id', 'short-alias', '--store', str(store), 'init'])
            self.assertEqual(head, 0)
            with contextlib.closing(task_archive.open_archive(store, 'short-alias')) as db:
                archive_head = task_archive.head(db)
            request = {'operation_id': 'short-alias-1', 'expected_archive_head': archive_head, 'operations': [{'document_id': 'TASK_DOC', 'expected_sha256': workflow_state.digest(task_path.read_bytes()), 'type': 'replace-section', 'section_id': 'Decisions', 'content': 'Updated'}]}
            request_path.write_text(json.dumps(request), encoding='utf-8')
            result = workflow_state.apply_batch(*workflow_state.load_project(alias, 'engineering-manifest.json')[:3], request_path, store, 'short-alias', apply=True)
            self.assertEqual(result['status'], 'applied')
            self.assertIn('Updated', task_path.read_text(encoding='utf-8'))
            with self.assertRaisesRegex(check_project.ConfigError, 'path escapes project root'):
                check_project.safe_path(root.resolve(), Path(outside_alias.value) / 'secret.md')
    def test_nonexistent_project_root_cli_returns_unsupported_without_retry(self):
        script = SCRIPTS / 'workflow_state.py'
        result = subprocess.run([sys.executable, str(script), '--root', str(self.root / 'missing'), 'index'], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)['status'], 'unsupported')
    def test_manifest_index_reports_reference_conflict_instead_of_selecting_latest(self):
        manifest = json.loads((self.root / 'engineering-manifest.json').read_text())
        manifest['workflow']['active_spec'] = 'MISSING'
        (self.root / 'engineering-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        with self.assertRaisesRegex(workflow_state.WorkflowStateError, 'active_spec references unknown'):
            self.context()
    def test_manifest_index_rejects_duplicate_task_and_document_id(self):
        manifest = json.loads((self.root / 'engineering-manifest.json').read_text())
        manifest['tasks'][0]['id'] = 'TASK_DOC'
        (self.root / 'engineering-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        with self.assertRaisesRegex(workflow_state.WorkflowStateError, 'task ID duplicates a document ID'):
            self.context()
    def test_nonstandard_unicode_line_separator_is_not_treated_as_json_whitespace(self):
        raw = b'{"ok":true}\xe2\x80\xa8{"second":true}'
        with self.assertRaises(workflow_state.WorkflowStateError):
            workflow_state.strict_json(raw, 'request')
    def test_manifest_snapshot_is_strict_duplicate_key_rejecting_json(self):
        raw = (self.root / 'engineering-manifest.json').read_text()
        raw = raw.replace('"active_task": "TASK-1"', '"active_task": "TASK-1", "active_task": "TASK-1"')
        (self.root / 'engineering-manifest.json').write_text(raw, encoding='utf-8')
        with self.assertRaisesRegex(workflow_state.WorkflowStateError, 'duplicate JSON key'):
            self.context()
    def test_document_pointer_rejects_noncanonical_array_index(self):
        manifest = json.loads((self.root / 'engineering-manifest.json').read_text())
        with self.assertRaises(workflow_state.WorkflowStateError):
            workflow_state.is_protected_manifest_path('/documents/01/lifecycle/status', manifest)
if __name__ == '__main__':
    unittest.main()
