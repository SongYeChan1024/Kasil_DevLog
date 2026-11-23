"""Installation, policy scope and hook safety regression checks. Author: 송예찬."""
import json
import os
from pathlib import Path
import re
import shutil
import unittest
from unittest.mock import patch
import uuid

import manage
import rules_core as core
import runtime
import memory_migration


class Fixture(unittest.TestCase):
    def setUp(self):
        self.test_root = Path(__file__).parent.resolve() / ".test-tmp"
        self.base = self.test_root / uuid.uuid4().hex
        self.base.mkdir(parents=True)

    def tearDown(self):
        target = self.base.resolve()
        if target.is_relative_to(self.test_root.resolve()) and target != self.test_root.resolve():
            def remove_readonly(function, name, error):
                path = Path(name)
                if not path.resolve().is_relative_to(target) or not isinstance(error[1], PermissionError):
                    raise error[1]
                # Git fixture objects have the Windows read-only attribute.
                os.chmod(path, 0o700)
                function(path)
            shutil.rmtree(target, onerror=remove_readonly)

    def transaction(self, value=b"new"):
        return manage.Transaction({self.base / "AGENTS.md": value, self.base / "CLAUDE.md": b"@AGENTS.md\n"}, self.base / "state.json")

    def project(self):
        root = self.base / "Project_DOB"
        root.mkdir()
        rendered = core.render_project(root, core.SOURCE.read_bytes(), {})
        for name, data in rendered.items():
            path = root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        return root


class InstallationTests(Fixture):
    def test_install_and_repeat(self):
        self.assertIsNotNone(self.transaction().sync())
        self.assertTrue(self.transaction().check())
        self.assertIsNone(self.transaction().sync())

    def test_adoption_preserves_original_bytes(self):
        old = b"original\r\n"
        (self.base / "AGENTS.md").write_bytes(old)
        with self.assertRaises(ValueError): self.transaction().sync()
        backup = self.transaction().sync(adopt=True)
        manifest = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
        saved = next(x for x in manifest if x["target"].endswith("AGENTS.md"))
        self.assertEqual((backup / saved["backup"]).read_bytes(), old)

    def test_manual_edit_preserved(self):
        self.transaction().sync()
        (self.base / "AGENTS.md").write_bytes(b"user edit")
        with self.assertRaises(ValueError): self.transaction(b"updated").sync()
        self.assertEqual((self.base / "AGENTS.md").read_bytes(), b"user edit")

    def test_manual_deletion_preserved(self):
        self.transaction().sync()
        (self.base / "AGENTS.md").unlink()
        with self.assertRaises(ValueError): self.transaction().sync()

    def test_concurrent_write_preserved(self):
        plan = self.transaction()
        (self.base / "AGENTS.md").write_bytes(b"another session")
        with self.assertRaises(ValueError): plan.sync()

    def test_failed_second_write_rolls_back(self):
        original_write = manage.atomic_write
        def fail(path, data):
            if path.name == "CLAUDE.md": raise OSError("injected failure")
            return original_write(path, data)
        with patch.object(manage, "atomic_write", side_effect=fail):
            with self.assertRaises(OSError): self.transaction().sync()
        self.assertFalse((self.base / "AGENTS.md").exists())
        self.assertFalse((self.base / "state.json").exists())

    def test_failed_state_rolls_back_original(self):
        (self.base / "AGENTS.md").write_bytes(b"old")
        original_write = manage.atomic_write
        def fail(path, data):
            if path.name == "state.json": raise OSError("injected state failure")
            return original_write(path, data)
        with patch.object(manage, "atomic_write", side_effect=fail):
            with self.assertRaises(OSError): self.transaction().sync(adopt=True)
        self.assertEqual((self.base / "AGENTS.md").read_bytes(), b"old")
        self.assertFalse((self.base / "CLAUDE.md").exists())

    def test_global_settings_preserve_existing(self):
        codex, claude = self.base / "codex home", self.base / "claude home"
        codex.mkdir(); claude.mkdir()
        (codex / "config.toml").write_text('model = "existing-model"\n', encoding="utf-8")
        (claude / "settings.json").write_text(json.dumps({"theme": "dark", "permissions": {"deny": ["Read(private/**)"]}, "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "existing"}]}]}}), encoding="utf-8")
        result = manage.global_targets(core.SOURCE.read_bytes(), codex, claude)
        settings = json.loads(result[claude / "settings.json"])
        self.assertEqual(settings["theme"], "dark")
        self.assertIn("Read(private/**)", settings["permissions"]["deny"])
        self.assertEqual(settings["permissions"]["defaultMode"], "auto")
        self.assertIn('model = "existing-model"', result[codex / "config.toml"].decode())
        self.assertIn(b'codex\\ home/AGENTS.md', result[claude / "CLAUDE.md"])
        self.assertIn("Stop", settings["hooks"])

    def test_global_override_refuses(self):
        codex = self.base / "codex"; codex.mkdir()
        (codex / "AGENTS.override.md").write_text("override", encoding="utf-8")
        with self.assertRaises(ValueError): manage.global_targets(core.SOURCE.read_bytes(), codex, self.base / "claude")


class RenderingTests(Fixture):
    def test_skill_reference_links_resolve_in_standalone_install(self):
        root = self.base / "Project_DOB"
        bundle = core.render_project(root, core.SOURCE.read_bytes(), {})
        policy = json.loads(bundle[".agent-rules/policy.json"])["files"]
        for host in (".agents", ".claude"):
            resources = set()
            for name in core.UPSTREAM_SKILLS:
                entry = f"{host}/skills/{name}/SKILL.md"
                body = bundle[entry].decode("utf-8")
                self.assertIn(f"/{core.UPSTREAM_REVISION}/skills/{name}/SKILL.md", body)
                for target in re.findall(r"\]\(([^ )]+)\)", body):
                    if target.startswith(("https://", "#")):
                        continue
                    path = ((root / entry).parent / target).resolve().relative_to(root).as_posix()
                    self.assertIn(path, bundle, (entry, target))
                    if path in core.RESOURCE_FILES:
                        self.assertEqual(core.sha(bundle[path]), policy[path])
                        resources.add(path)
            self.assertEqual(resources, set(core.RESOURCE_FILES))

    def test_skills_share_source_and_include_portable_license(self):
        source = core.SOURCE.read_bytes()
        rendered = core.render_project(self.base / 'Project_DOB', source, {})
        policy = json.loads(rendered['.agent-rules/policy.json'])
        for name in core.SKILLS:
            codex, claude = (f'{folder}/skills/{name}/SKILL.md' for folder in ('.agents', '.claude'))
            self.assertEqual(rendered[codex], rendered[claude])
            self.assertTrue(rendered[codex].startswith(b'---\n'))
            self.assertEqual(policy['files'][codex], core.sha(rendered[codex]))
            self.assertIn(codex, core.PROJECT_FILES)
        self.assertIn('.agent-rules/THIRD_PARTY_NOTICES.md', policy['files'])
        changed = source.replace(b'# ', b'# Source edit: ', 1)
        updated = core.render_skills(changed)
        self.assertNotEqual(updated[core.SKILL_FILES[0]], rendered[core.SKILL_FILES[0]])

    def test_skill_metadata_mismatch_fails_before_install(self):
        source = core.SOURCE.read_bytes().replace(b'name: shared-intent', b'name: wrong-name')
        with self.assertRaises(ValueError): core.render_skills(source)

    def test_manual_skill_edit_is_preserved_on_sync(self):
        root = self.base / 'Project_DOB'
        initial = core.render_project(root, core.SOURCE.read_bytes(), {})
        state = self.base / 'state.json'
        manage.Transaction({root / p: data for p, data in initial.items()}, state).sync()
        skill = root / core.SKILL_FILES[0]
        skill.write_bytes(b'user-edited-skill')
        with self.assertRaises(ValueError):
            manage.Transaction({root / p: data for p, data in initial.items()}, state).sync()
        self.assertEqual(skill.read_bytes(), b'user-edited-skill')

    def test_existing_attributes_preserved(self):
        root = self.base / "Project_DOB"
        prior = b'*.unity text eol=lf\n'
        once = core.render_project(root, core.SOURCE.read_bytes(), {".gitattributes": prior})
        twice = core.render_project(root, core.SOURCE.read_bytes(), once)
        self.assertEqual(once, twice)
        self.assertIn(prior, twice[".gitattributes"])

    def test_scope_boundaries(self):
        source = core.SOURCE.read_bytes()
        dob = core.render_project(self.base / "Project_DOB", source, {})["AGENTS.md"].decode()
        ergo = core.render_project(self.base / "ERGOSQUARE-ARCHITECT", source, {})["AGENTS.md"].decode()
        self.assertNotIn("3~6단계", dob)
        self.assertIn("3~6단계", ergo)
        self.assertIn("복잡도에 관계없이", dob)
        self.assertLess(len(dob.encode()), 25000)

    def test_duplicate_scope_fails(self):
        source = core.SOURCE.read_bytes().replace(b"scope:dob", b"scope:common")
        with self.assertRaises(ValueError): core.sections(source)

    def test_settings_preserved_and_hooks_not_duplicated(self):
        root = self.base / "Project_DOB"
        first = core.render_project(root, core.SOURCE.read_bytes(), {".claude/settings.json": core.encoded({"permissions": {"deny": ["Read(custom/**)"]}})})
        second = core.render_project(root, core.SOURCE.read_bytes(), first)
        self.assertEqual(first, second)
        self.assertIn("Read(custom/**)", json.loads(second[".claude/settings.json"])["permissions"]["deny"])

    def test_custom_codex_configuration_not_replaced(self):
        old = b'approval_policy = "never"\nsandbox_mode = "read-only"\n'
        result = core.render_project(self.base / "Project_DOB", core.SOURCE.read_bytes(), {".codex/config.toml": old})
        self.assertEqual(result[".codex/config.toml"], old)


class HookTests(Fixture):
    def test_stop_uses_project_validation_environment(self):
        root = self.project()
        policy_path = root / '.agent-rules/policy.json'
        policy = json.loads(policy_path.read_text(encoding='utf-8'))
        policy['checks'] = [{'name': 'check', 'patterns': ['check.py'], 'requires': 'check.py', 'command': ['{python}', 'check.py']}]
        policy_path.write_bytes(core.encoded(policy))
        interpreter = root / '.agent-rules/.cache/venv' / ('Scripts/python.exe' if runtime.os.name == 'nt' else 'bin/python')
        interpreter.parent.mkdir(parents=True)
        interpreter.write_bytes(b'test-only')
        (root / 'check.py').write_text('pass\n', encoding='utf-8')
        with patch.object(runtime, 'changed_files', return_value=['check.py']), patch.object(runtime.subprocess, 'run') as run:
            run.return_value.returncode = 0
            self.assertEqual(runtime.process(root, {'hook_event_name': 'Stop'})[0], 0)
            self.assertEqual(run.call_args.args[0], [str(interpreter), 'check.py'])

    def test_secret_guard_and_safe_read(self):
        for name in (".env", "a/.env.local", "C:\\work\\secrets\\key.json", "~/.ssh/id_ed25519"):
            self.assertIsNotNone(runtime.preflight({"tool_name": "Read", "tool_input": {"file_path": name}}))
        self.assertIsNone(runtime.preflight({"tool_name": "Read", "tool_input": {"file_path": "README.md"}}))
        self.assertIsNotNone(runtime.preflight({"tool_name": "Bash", "tool_input": {"command": "cat .env"}}))

    def test_force_push_variants(self):
        for command in ("git push --force", "git -C repo push origin main -f", "git push --force-with-lease=main:abc"):
            self.assertIsNotNone(runtime.preflight({"tool_name": "PowerShell", "tool_input": {"command": command}}))
        self.assertIsNone(runtime.preflight({"tool_name": "Bash", "tool_input": {"command": "git push origin docs"}}))

    def test_existing_dirty_files_are_not_claimed(self):
        root = self.project(); (root / "old.json").write_text("invalid", encoding="utf-8")
        with patch.object(runtime, "changed_files", return_value=["old.json"]):
            self.assertEqual(runtime.process(root, {"hook_event_name": "SessionStart"})[0], 0)
            self.assertEqual(runtime.process(root, {"hook_event_name": "Stop"})[0], 0)

    def test_failed_stop_blocks_then_releases_loop(self):
        root = self.project()
        with patch.object(runtime, "changed_files", return_value=[]):
            runtime.process(root, {"hook_event_name": "SessionStart"})
        (root / "bad.json").write_text("invalid", encoding="utf-8")
        with patch.object(runtime, "changed_files", return_value=["bad.json"]):
            self.assertEqual(runtime.process(root, {"hook_event_name": "Stop"})[0], 2)
            code, output, _ = runtime.process(root, {"hook_event_name": "Stop", "stop_hook_active": True})
            self.assertEqual(code, 0); self.assertIn("미해결", output["systemMessage"])
            (root / "bad.json").write_text("{}", encoding="utf-8")
            self.assertEqual(runtime.process(root, {"hook_event_name": "Stop"})[0], 0)

    def test_install_drift_detected(self):
        root = self.project()
        policy = json.loads((root / ".agent-rules/policy.json").read_text(encoding="utf-8"))
        self.assertFalse(runtime.check_install(root, policy))
        (root / "AGENTS.md").write_text("changed", encoding="utf-8")
        self.assertTrue(runtime.check_install(root, policy))

    def test_skill_install_drift_detected(self):
        root = self.project()
        policy = json.loads((root / '.agent-rules/policy.json').read_text(encoding='utf-8'))
        self.assertFalse(runtime.check_install(root, policy))
        (root / core.SKILL_FILES[0]).write_bytes(b'changed')
        self.assertTrue(runtime.check_install(root, policy))

    def test_parser_errors_do_not_echo_secret_values(self):
        root = self.base; (root / "a.json").write_text('{"private": "do-not-echo",}', encoding="utf-8")
        errors = runtime.static_checks(root, ["a.json"])
        self.assertTrue(errors); self.assertNotIn("do-not-echo", str(errors))


class MemoryTests(Fixture):
    def test_reviewed_memory_migrates_but_changed_memory_refuses(self):
        memory = self.base / 'projects/example/memory/reply-in-korean.md'
        memory.parent.mkdir(parents=True)
        data = b'---\nname: example\ntype: feedback\n---\nold preference\n'
        memory.write_bytes(data)
        with patch.object(memory_migration, 'EXPECTED', {'example/reply-in-korean.md': core.sha(data)}):
            result = memory_migration.targets(self.base)
            self.assertIn(b'migrated-to-shared-agent-rules', result[memory])
            self.assertNotIn(b'old preference', result[memory])
            memory.write_bytes(b'new preference')
            with self.assertRaises(ValueError): memory_migration.targets(self.base)

    def test_review_document_reference_stays_private_at_home(self):
        memory = self.base / 'projects/example/memory/google-doc-review-copy.md'
        memory.parent.mkdir(parents=True)
        data = b'old tool limitation\nReview: https://docs.google.com/document/d/example-private-reference/edit\n'
        memory.write_bytes(data)
        with patch.object(memory_migration, 'EXPECTED', {'example/google-doc-review-copy.md': core.sha(data)}):
            result = memory_migration.targets(self.base)
            self.assertIn(b'example-private-reference', result[memory])
            self.assertNotIn(b'old tool limitation', result[memory])


if __name__ == "__main__": unittest.main()
