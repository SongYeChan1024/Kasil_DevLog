"""Real Git fixtures for workspace routing. Author: 송예찬."""
import json
import contextlib
import io
import subprocess
import sys
from unittest.mock import patch

import rules_core as core
import manage
import runtime
import workspace_hook as router
from test_manage import Fixture


class WorkspaceTests(Fixture):
    def setUp(self):
        super().setUp()
        self.roots = {}
        for name in ('After_Seconds', 'UnityGameFoundation'):
            root = self.base / name
            root.mkdir()
            self.roots[name] = root
            generated = core.render_project(root, core.SOURCE.read_bytes(), {})
            policy = json.loads(generated['.agent-rules/policy.json'])
            policy['checks'] = [{'name': 'fixture-check', 'patterns': ['*.json'], 'requires': 'check.py',
                                 'command': ['{python}', 'check.py']}]
            generated['.agent-rules/policy.json'] = core.encoded(policy)
            for file, data in generated.items():
                path = root / file
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            (root / 'data.json').write_text('{}\n', encoding='utf-8')
            (root / 'check.py').write_text("from pathlib import Path\np=Path('.agent-rules/.cache/check-count')\np.parent.mkdir(parents=True,exist_ok=True)\np.write_text(str(int(p.read_text())+1 if p.exists() else 1))\n", encoding='utf-8')
            self.git(root, 'init', '-q')
            self.git(root, 'add', '.')
            self.git(root, '-c', 'user.name=Test fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture')
        self.install_workspace()

    def git(self, root, *args):
        return subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=True, timeout=15)

    def install_workspace(self, missing=None):
        policies = {name: (root / '.agent-rules/policy.json').read_bytes() for name, root in self.roots.items()}
        generated = core.render_workspace(core.SOURCE.read_bytes(), policies, missing or [], {})
        for file, data in generated.items():
            path = self.base / file
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    def event(self, kind, tool='apply_patch', args=None, token='tool-1', **extra):
        return {'hook_event_name': kind, 'session_id': 'fixture-session', 'tool_use_id': token,
                'tool_name': tool, 'tool_input': args or {}, 'cwd': str(self.base), **extra}

    def call(self, kind, **kw):
        return router.dispatch(self.base, self.event(kind, **kw))

    def write(self, name, text='{"updated":true}\n'):
        (self.roots[name] / 'data.json').write_text(text, encoding='utf-8')

    def count(self, name):
        file = self.roots[name] / '.agent-rules/.cache/check-count'
        return int(file.read_text()) if file.exists() else 0

    def test_workspace_bootstrap_from_root_and_subdirectory(self):
        for cwd in (self.base, self.roots['After_Seconds'] / '.agent-rules'):
            result = subprocess.run([sys.executable, '-B', '-c', core.HOOK_BOOTSTRAP], cwd=cwd,
                                    input=json.dumps(self.event('SessionStart')), encoding='utf-8', capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('2개 저장소', json.loads(result.stdout)['hookSpecificOutput']['additionalContext'])

    def test_standalone_project_fallback(self):
        (self.base / '.agent-rules/workspace.json').unlink()
        result = subprocess.run([sys.executable, '-B', '-c', core.HOOK_BOOTSTRAP], cwd=self.roots['After_Seconds'],
                                input=json.dumps(self.event('SessionStart')), encoding='utf-8', capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('통합 규칙', json.loads(result.stdout)['hookSpecificOutput']['additionalContext'])

    def test_two_repo_patch_and_successful_stop_not_repeated(self):
        args = {'command': '\n'.join('*** Update File: ' + name + '/data.json' for name in self.roots)}
        self.assertEqual(self.call('PreToolUse', args=args)[0], 0)
        for name in self.roots: self.write(name)
        self.assertEqual(self.call('PostToolUse', args=args)[0], 0)
        self.assertEqual(self.call('Stop')[0], 0)
        self.assertEqual(self.call('Stop')[0], 0)
        self.assertEqual([self.count(name) for name in self.roots], [1, 1])

    def test_preexisting_invalid_edit_in_other_repo_is_not_checked(self):
        self.write('UnityGameFoundation', '{preexisting invalid')
        args = {'file_path': str(self.roots['After_Seconds'] / 'data.json')}
        self.assertEqual(self.call('PreToolUse', tool='Write', args=args)[0], 0)
        self.write('After_Seconds')
        self.assertEqual(self.call('PostToolUse', tool='Write', args=args)[0], 0)
        self.assertEqual(self.call('Stop')[0], 0)
        self.assertEqual(self.count('UnityGameFoundation'), 0)

    def test_shell_detects_other_repository_and_committed_change(self):
        args = {'workdir': str(self.roots['After_Seconds']), 'cmd': 'opaque shell command'}
        self.assertEqual(self.call('PreToolUse', tool='exec_command', args=args)[0], 0)
        self.write('UnityGameFoundation')
        root = self.roots['UnityGameFoundation']
        self.git(root, 'add', 'data.json')
        self.git(root, '-c', 'user.name=Test fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'change')
        self.assertEqual(self.call('PostToolUse', tool='exec_command', args=args)[0], 0)
        self.assertEqual(self.call('Stop')[0], 0)
        self.assertEqual(self.count('UnityGameFoundation'), 1)
        self.assertEqual(self.count('After_Seconds'), 0)

    def test_pending_tool_recovered_at_stop_and_failure_does_not_loop(self):
        self.assertEqual(self.call('PreToolUse', args={'path': 'After_Seconds/data.json'})[0], 0)
        self.write('After_Seconds', '{invalid')
        self.assertEqual(self.call('Stop')[0], 2)
        self.assertEqual(self.call('Stop', stop_hook_active=True)[0], 0)
        self.assertEqual(self.count('After_Seconds'), 0)

    def test_duplicate_hook_events_are_idempotent(self):
        args = {'path': 'After_Seconds/data.json'}
        self.call('PreToolUse', args=args)
        self.call('PreToolUse', args=args)
        self.write('After_Seconds')
        with patch.object(runtime, 'process', wraps=runtime.process) as process:
            self.call('PostToolUse', args=args)
            self.call('PreToolUse', args=args)
            self.call('PostToolUse', args=args)
            self.assertEqual(process.call_count, 1)
        self.assertEqual(self.call('Stop')[0], 0)
        self.assertEqual(self.count('After_Seconds'), 1)

    def test_serial_fallback_does_not_reuse_previous_post_result(self):
        args = {'path': 'After_Seconds/data.json'}
        self.call('PreToolUse', args=args, token=None)
        self.write('After_Seconds')
        self.assertEqual(self.call('PostToolUse', args=args, token=None)[0], 0)
        self.call('PreToolUse', args=args, token=None)
        self.write('After_Seconds', '{invalid')
        self.assertEqual(self.call('PostToolUse', args=args, token=None)[0], 2)

    def test_policy_change_blocks_validation_execution(self):
        self.call('PreToolUse', args={'path': 'After_Seconds/data.json'})
        self.write('After_Seconds')
        self.call('PostToolUse')
        policy = self.roots['After_Seconds'] / '.agent-rules/policy.json'
        policy.write_bytes(policy.read_bytes() + b' ')
        with self.assertRaises(ValueError): self.call('Stop')
        self.assertEqual(self.count('After_Seconds'), 0)

    def test_secret_codex_patch_command_blocked(self):
        self.assertEqual(self.call('PreToolUse', args={'command': '*** Add File: After_Seconds/.env'})[0], 2)

    def test_uninstalled_repository_is_reported_not_silently_skipped(self):
        missing = self.roots.pop('UnityGameFoundation')
        self.install_workspace(['UnityGameFoundation'])
        with self.assertRaises(ValueError):
            self.call('PreToolUse', args={'path': 'UnityGameFoundation/data.json'})
        self.call('PreToolUse', tool='Bash')
        (missing / 'data.json').write_text('{"change":true}', encoding='utf-8')
        self.assertEqual(self.call('PostToolUse', tool='Bash')[0], 2)

    def test_workspace_path_escape_rejected(self):
        with self.assertRaises(ValueError): router.safe(self.base / '../outside', self.base)

    def test_relative_parent_path_routes_to_resolved_repository(self):
        registry = json.loads((self.base / '.agent-rules/workspace.json').read_bytes())
        selected, _ = router.selection(self.base, self.event('PreToolUse', args={'path': 'After_Seconds/../UnityGameFoundation/data.json'}), registry)
        self.assertEqual(selected, ['UnityGameFoundation'])

    def test_workspace_install_can_defer_then_complete_codex_config(self):
        config = self.base / '.codex/hooks.json'
        config.unlink()
        def command(*options):
            with patch.object(manage, 'ROOT', self.base / 'manager'), patch.object(sys, 'argv', ['manage.py', *options, '--workspace', str(self.base), '--workspace-only']), contextlib.redirect_stdout(io.StringIO()):
                return manage.main()
        self.assertEqual(command('sync', '--defer-workspace-codex', '--adopt-existing'), 0)
        self.assertFalse(config.exists())
        self.assertEqual(command('sync'), 0)
        self.assertTrue(config.exists())
        self.assertEqual(command('check'), 0)
        # These fixtures intentionally have custom policy checks. They must not
        # be presented as the current generated installation by the manager.
        registry = json.loads((self.base / '.agent-rules/workspace.json').read_bytes())
        self.assertEqual(registry['projects'], {})
        self.assertEqual(set(registry['uninstalled']), set(self.roots))

    def test_session_start_does_not_write_into_untouched_repositories(self):
        original = runtime.write_cache
        def central_only(path, data):
            self.assertTrue(path.is_relative_to(self.base / '.agent-rules/.cache'))
            original(path, data)
        with patch.object(runtime, 'write_cache', side_effect=central_only):
            self.assertEqual(self.call('SessionStart')[0], 0)

    def test_custom_workspace_hooks_preserved_and_generation_stable(self):
        prior = core.encoded({'hooks': {'Stop': [{'hooks': [{'type': 'command', 'command': 'custom-check'}]}]}})
        first = core.merged_hooks('codex', prior)
        self.assertEqual(first, core.merged_hooks('codex', first))
        self.assertIn('custom-check', first.decode())

    def test_post_without_pre_is_visible_failure(self):
        self.assertEqual(self.call('PostToolUse')[0], 2)
