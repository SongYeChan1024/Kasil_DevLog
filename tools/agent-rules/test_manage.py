"""Regression checks use disposable homes, never the user's real configuration."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch
import uuid

SPEC = importlib.util.spec_from_file_location("agent_rules_manage", Path(__file__).with_name("manage.py"))
manage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manage)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.test_root = Path(__file__).resolve().parent / ".test-tmp"
        self.root = self.test_root / uuid.uuid4().hex
        # Python 3.14 TemporaryDirectory's Windows ACL can exclude sandbox tokens.
        # Keep fixtures in the writable checkout, using inherited directory ACLs.
        self.root.mkdir(parents=True)
        self.addCleanup(self.clean_fixture)
        self.codex = self.root / "사용자 home" / "codex settings"
        self.claude = self.root / "사용자 home" / "claude settings"
        self.source = self.root / "COMMON.md"
        self.source.write_text("# 공통 규칙\n\n한국어로 대화합니다.\n", encoding="utf-8")
        self.workspace = self.root / "Projects"
        self.workspace.mkdir()

    def clean_fixture(self):
        resolved = self.root.resolve()
        if resolved.parent != self.test_root.resolve():
            raise RuntimeError("Refusing to remove a fixture outside the test root")
        shutil.rmtree(resolved)

    def install(self, workspace=None):
        return manage.Installation(self.codex, self.claude, workspace, self.source)

    def seed_existing(self):
        self.codex.mkdir(parents=True)
        self.claude.mkdir(parents=True)
        (self.codex / "AGENTS.md").write_bytes(b"old codex\r\n")
        (self.claude / "CLAUDE.md").write_bytes(b"old claude\r\n")

    def test_preview_creates_no_directories(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.install().preview()
        self.assertFalse(self.codex.exists())
        self.assertFalse(self.claude.exists())

    def test_fresh_install_escapes_spaces_and_is_idempotent(self):
        first_backup = self.install(self.workspace).sync()
        self.assertTrue(first_backup.is_dir())
        self.assertTrue(self.install().check())  # Saved workspace reused.
        self.assertIn("@../codex\\ settings/AGENTS.md", (self.claude / "CLAUDE.md").read_text("utf-8"))
        before = (self.codex / "AGENTS.md").stat().st_mtime_ns
        self.assertIsNone(self.install().sync())
        self.assertEqual(before, (self.codex / "AGENTS.md").stat().st_mtime_ns)

    def test_adoption_backs_up_original_bytes(self):
        self.seed_existing()
        with self.assertRaises(ValueError):
            self.install().sync()
        self.assertEqual(b"old codex\r\n", (self.codex / "AGENTS.md").read_bytes())
        self.assertFalse((self.codex / "agent-rules").exists())
        backup = self.install().sync(adopt_existing=True)
        entries = json.loads((backup / "manifest.json").read_text("utf-8"))
        saved = {Path(e["target"]).name: (backup / e["backup"]).read_bytes()
                 for e in entries if e["existed"]}
        self.assertEqual(b"old codex\r\n", saved["AGENTS.md"])
        self.assertEqual(b"old claude\r\n", saved["CLAUDE.md"])

    def test_source_update_preserves_project_files(self):
        project = self.workspace / "team"
        project.mkdir()
        rules = project / "CLAUDE.md"
        rules.write_bytes(b"team rules")
        self.install(self.workspace).sync()
        self.source.write_text("# 갱신한 공통 규칙\n", encoding="utf-8")
        self.assertFalse(self.install().check())
        self.install().sync()
        self.assertTrue(self.install().check())
        self.assertEqual(b"team rules", rules.read_bytes())

    def test_manual_edits_and_deletions_are_not_overwritten(self):
        self.install().sync()
        target = self.claude / "CLAUDE.md"
        target.write_bytes(b"my extra rule")
        self.assertFalse(self.install().check())
        with self.assertRaises(ValueError):
            self.install().sync()
        target.unlink()
        with self.assertRaises(ValueError):
            self.install().sync()

    def test_failure_in_second_write_rolls_back_first(self):
        self.seed_existing()
        original_write = manage.atomic_write

        def fail_claude(path, data):
            if path == self.claude / "CLAUDE.md":
                raise PermissionError("simulated write denial")
            original_write(path, data)

        with patch.object(manage, "atomic_write", side_effect=fail_claude):
            with self.assertRaises(OSError):
                self.install().sync(adopt_existing=True)
        self.assertEqual(b"old codex\r\n", (self.codex / "AGENTS.md").read_bytes())
        self.assertEqual(b"old claude\r\n", (self.claude / "CLAUDE.md").read_bytes())
        self.assertFalse((self.codex / "agent-rules" / "state.json").exists())

    def test_failure_writing_state_rolls_back_both(self):
        self.seed_existing()
        original_write = manage.atomic_write

        def fail_state(path, data):
            if path.name == "state.json":
                raise PermissionError("simulated state denial")
            original_write(path, data)

        with patch.object(manage, "atomic_write", side_effect=fail_state):
            with self.assertRaises(OSError):
                self.install().sync(adopt_existing=True)
        self.assertEqual(b"old codex\r\n", (self.codex / "AGENTS.md").read_bytes())
        self.assertEqual(b"old claude\r\n", (self.claude / "CLAUDE.md").read_bytes())

    def test_concurrent_change_prevents_any_write(self):
        self.seed_existing()
        planned = self.install()
        (self.claude / "CLAUDE.md").write_bytes(b"other session")
        with self.assertRaises(ValueError):
            planned.sync(adopt_existing=True)
        self.assertEqual(b"old codex\r\n", (self.codex / "AGENTS.md").read_bytes())

    def test_source_change_after_preview_prevents_writing(self):
        planned = self.install()
        self.source.write_text("new source", encoding="utf-8")
        with self.assertRaises(ValueError):
            planned.sync()
        self.assertFalse((self.codex / "AGENTS.md").exists())

    def test_cli_preview_sync_check_and_drift_exit_codes(self):
        command = [sys.executable, "-B", str(Path(__file__).with_name("manage.py"))]
        options = ["--codex-home", str(self.codex), "--claude-home", str(self.claude),
                   "--workspace", str(self.workspace)]

        def run(action):
            return subprocess.run(command + [action] + options, capture_output=True,
                                  text=True, encoding="utf-8", check=False)

        self.assertEqual(0, run("preview").returncode)
        self.assertFalse(self.codex.exists())
        self.assertEqual(1, run("check").returncode)
        result = run("sync")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(0, run("check").returncode)
        (self.codex / "AGENTS.md").write_text("manual edit", encoding="utf-8")
        self.assertEqual(1, run("check").returncode)
        self.assertEqual(2, run("sync").returncode)

    def test_global_override_is_reported_and_untouched(self):
        self.codex.mkdir(parents=True)
        override = self.codex / "AGENTS.override.md"
        override.write_text("override", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual("override", override.read_text("utf-8"))
        self.assertFalse((self.codex / "AGENTS.md").exists())

    def test_changed_home_is_not_silently_adopted(self):
        self.install().sync()
        with self.assertRaises(ValueError):
            manage.Installation(self.codex, self.root / "other-claude", source=self.source)

    def test_invalid_workspace_or_empty_source_fails_before_writing(self):
        with self.assertRaises(ValueError):
            self.install(self.root / "missing")
        self.source.write_bytes(b"")
        with self.assertRaises(ValueError):
            self.install()
        self.assertFalse(self.codex.exists())

    def test_audit_warns_on_bytes_without_reading_secrets_or_rewriting(self):
        project = self.workspace / "game"
        project.mkdir()
        (project / ".git").write_text("gitdir: unused", encoding="utf-8")
        rules = project / "AGENTS.md"
        rules.write_text("한" * 12000, encoding="utf-8")
        secret = project / ".env"
        secret.write_text("must-not-appear", encoding="utf-8")
        before = rules.read_bytes()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            manage.audit(self.workspace)
        self.assertIn("32KiB", output.getvalue())
        self.assertNotIn("must-not-appear", output.getvalue())
        self.assertEqual(before, rules.read_bytes())


if __name__ == "__main__":
    unittest.main()
