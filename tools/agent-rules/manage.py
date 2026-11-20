#!/usr/bin/env python3
"""Backed-up, conflict-aware rule deployment. Author: 송예찬."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import tomllib
import uuid
from rules_core import ROOT, SOURCE, PROJECTS, PROJECT_FILES, WORKSPACE_FILES, sha, encoded, instructions, render_project, render_workspace, merge_lists, claude_permissions
from memory_migration import targets as memory_targets


def plain(path: Path) -> Path:
    path = path.expanduser().absolute()
    for p in (path, *path.parents):
        if p.is_symlink() or (hasattr(p, "is_junction") and p.is_junction()):
            raise ValueError(f"링크·junction에는 설치하지 않습니다: {p}")
    return path


def read(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".agent-rules-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
        if path.exists(): os.chmod(temporary, stat.S_IMODE(path.stat().st_mode))
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)


class Transaction:
    def __init__(self, targets: dict[Path, bytes], state_path: Path):
        self.targets = {plain(k): v for k, v in targets.items()}
        self.state_path = plain(state_path)
        if self.state_path in self.targets: raise ValueError("설치 기록과 대상 경로가 겹칩니다.")
        self.original_state = read(self.state_path)
        self.old_state = json.loads(self.original_state) if self.original_state else {}
        if self.old_state and self.old_state.get("format") != 2: raise ValueError("설치 기록 버전을 확인하세요.")
        self.before = {p: read(p) for p in self.targets}
        self.state = encoded({"format": 2, "targets": {str(p): sha(data) for p, data in self.targets.items()}})

    def changed(self) -> list[Path]:
        return [p for p, data in self.targets.items() if data != self.before[p]]

    def conflicts(self) -> list[Path]:
        old = self.old_state.get("targets", {})
        return [p for p in self.changed() if (str(p) in old and sha(self.before[p]) != old[str(p)]) or (str(p) not in old and self.before[p] is not None)]

    def check(self) -> bool:
        return not self.changed() and self.original_state == self.state

    def sync(self, adopt: bool = False) -> Path | None:
        if self.conflicts() and not adopt:
            raise ValueError("기존·수동 수정 파일을 보존했습니다. preview 후 --adopt-existing으로 백업·이전하세요.")
        if self.check(): return None
        for path in self.targets:
            plain(path)
            if read(path) != self.before[path]: raise ValueError(f"준비 중 파일이 바뀌었습니다: {path}")
        if read(self.state_path) != self.original_state: raise ValueError("준비 중 설치 기록이 바뀌었습니다.")
        backup = self.state_path.parent / "backups" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
        plain(backup).mkdir(parents=True, exist_ok=False)
        originals = {p: self.before[p] for p in self.changed()}
        originals[self.state_path] = self.original_state
        manifest = []
        for i, (path, data) in enumerate(originals.items()):
            name = f"{i:03d}.backup" if data is not None else None
            if data is not None: (backup / name).write_bytes(data)
            manifest.append({"target": str(path), "backup": name, "before_sha256": sha(data),
                             "after_sha256": sha(self.state if path == self.state_path else self.targets[path])})
        (backup / "manifest.json").write_bytes(encoded(manifest))
        written = []
        try:
            for path in self.changed():
                if read(path) != self.before[path]: raise OSError(f"동시 변경 감지: {path}")
                atomic_write(path, self.targets[path]); written.append(path)
            atomic_write(self.state_path, self.state); written.append(self.state_path)
        except OSError as error:
            failures = []
            for path in reversed(written):
                try:
                    if originals[path] is None: path.unlink(missing_ok=True)
                    else: atomic_write(path, originals[path])
                except OSError: failures.append(str(path))
            detail = "자동 복원 완료" if not failures else "자동 복원 실패: " + ", ".join(failures)
            raise OSError(f"설치 실패; {detail}; 백업={backup}; {error}") from error
        return backup


def global_targets(source: bytes, codex_home: Path, claude_home: Path) -> dict[Path, bytes]:
    codex_home, claude_home = plain(codex_home), plain(claude_home)
    override = codex_home / "AGENTS.override.md"
    if override.exists() and override.read_text(encoding="utf-8-sig").strip():
        raise ValueError("전역 AGENTS.override.md부터 검토하세요.")
    imported = Path(os.path.relpath(codex_home / "AGENTS.md", claude_home)).as_posix().replace(" ", "\\ ")
    settings_path = claude_home / "settings.json"
    existing = json.loads(settings_path.read_text(encoding="utf-8-sig")) if settings_path.exists() else {}
    addition = merge_lists(claude_permissions(), {
        "permissions": {"defaultMode": "auto"},
        "autoMode": {
            "environment": ["$defaults", "Personal development work in the current trusted workspace."],
            "allow": ["$defaults", "Local analysis, edits and relevant validation within the user's requested task."],
            "soft_deny": ["$defaults", "External writes, publishing, push, messages or paid generation without explicit approval of the target and content."],
            "hard_deny": ["$defaults", "Expose credentials, overwrite unrelated work, or force-push remote history."],
        },
    })
    if os.name != "nt":
        addition["sandbox"] = {"enabled": True, "failIfUnavailable": True, "allowUnsandboxedCommands": False,
                               "filesystem": {"denyRead": ["~/.ssh", "~/.aws/credentials", "~/.git-credentials"]}}
    config_path = codex_home / "config.toml"
    config = config_path.read_text(encoding="utf-8-sig") if config_path.exists() else ""
    parsed = tomllib.loads(config)
    prefix = []
    if "approval_policy" not in parsed: prefix.append('approval_policy = "on-request"')
    if "default_permissions" not in parsed and "sandbox_mode" not in parsed: prefix.append('sandbox_mode = "workspace-write"')
    if prefix: config = "# Shared rule defaults; existing settings preserved.\n" + "\n".join(prefix) + "\n\n" + config
    result = {codex_home / "AGENTS.md": instructions(source, ("common",)),
            claude_home / "CLAUDE.md": ("# Shared global instructions\n\n@" + imported + "\n").encode("utf-8"),
            settings_path: encoded(merge_lists(existing, addition)), config_path: config.encode("utf-8")}
    result.update(memory_targets(claude_home))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["preview", "sync", "check"])
    parser.add_argument("--workspace", type=Path, default=ROOT.parents[2])
    parser.add_argument("--projects", nargs="*", choices=list(PROJECTS))
    parser.add_argument("--global", dest="global_install", action="store_true", help="홈 전역 지침·자동 모드도 설치. 해당 경로 쓰기 권한 필요")
    parser.add_argument("--global-only", action="store_true")
    parser.add_argument("--workspace-only", action="store_true", help="기존 프로젝트 설치를 연결하는 작업 공간 훅만 설치")
    parser.add_argument("--defer-workspace-codex", action="store_true", help="보호된 작업 공간 .codex 쓰기를 보류. 전체 설치 완료를 의미하지 않음")
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))))
    parser.add_argument("--claude-home", type=Path, default=Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude"))))
    parser.add_argument("--adopt-existing", action="store_true")
    args = parser.parse_args()
    if args.workspace_only and (args.global_only or args.global_install or args.projects is not None):
        parser.error("--workspace-only는 --global/--global-only/--projects와 함께 사용할 수 없습니다.")
    workspace = plain(args.workspace)
    source = SOURCE.read_bytes()
    selected = args.projects if args.projects is not None else [name for name in PROJECTS if (workspace / name).is_dir()]
    transactions = []
    policies = {}
    if not args.global_only:
        if not workspace.is_dir(): raise ValueError("작업 공간이 없습니다.")
        for name in ([] if args.workspace_only else selected):
            project = plain(workspace / name)
            if not (project / ".git").exists(): raise ValueError(f"Git 프로젝트가 아닙니다: {project}")
            if name == "Project_DOB" and args.command == "sync":
                branch = subprocess.run(["git", "-C", str(project), "branch", "--show-current"], capture_output=True, text=True, check=True).stdout.strip()
                if branch == "main":
                    raise ValueError("DOB 설정 변경은 backend 등 역할 브랜치에서 적용하세요. main 직접 반영 예외는 합의된 문서에만 적용됩니다.")
            override = project / "AGENTS.override.md"
            if override.exists() and override.read_text(encoding="utf-8-sig").strip(): raise ValueError(f"우선 지침 검토 필요: {override}")
            existing = {key: read(plain(project / key)) for key in PROJECT_FILES}
            desired = render_project(project, source, existing)
            policies[name] = desired[".agent-rules/policy.json"]
            transactions.append((name, Transaction({project / key: value for key, value in desired.items()}, ROOT / ".state" / name / "state.json")))
        missing = []
        for name in PROJECTS:
            if name in policies or not (workspace / name).is_dir(): continue
            project = plain(workspace / name)
            installed = read(plain(project / ".agent-rules/policy.json"))
            if installed:
                import runtime
                if runtime.check_install(project, json.loads(installed)):
                    raise ValueError(f"{name}: 기존 설치 불일치. 프로젝트를 먼저 동기화하세요.")
                expected = render_project(project, source, {key: read(plain(project / key)) for key in PROJECT_FILES})
                if installed == expected[".agent-rules/policy.json"]: policies[name] = installed
                else: missing.append(name)
            else: missing.append(name)
        desired_workspace = render_workspace(source, policies, missing, {name: read(plain(workspace / name)) for name in WORKSPACE_FILES})
        targets = {workspace / key: value for key, value in desired_workspace.items() if key != ".codex/hooks.json"}
        transactions.append(("workspace", Transaction(targets, ROOT / ".state/workspace/state.json")))
        if not args.defer_workspace_codex:
            transactions.append(("workspace-codex", Transaction({workspace / ".codex/hooks.json": desired_workspace[".codex/hooks.json"]}, ROOT / ".state/workspace-codex/state.json")))
    if args.global_install or args.global_only:
        transactions.append(("global", Transaction(global_targets(source, args.codex_home, args.claude_home), ROOT / ".state/global/state.json")))
    if SOURCE.read_bytes() != source: raise ValueError("준비 중 규칙 원본이 바뀌었습니다.")
    valid = True
    for name, transaction in transactions:
        if args.command == "preview":
            print(f"{name}: 변경 {len(transaction.changed())}개 / 기존·수동 변경 {len(transaction.conflicts())}개")
            for path in transaction.changed(): print("  " + str(path))
        elif args.command == "sync":
            backup = transaction.sync(args.adopt_existing)
            print(f"{name}: " + (f"설치 완료 / 백업 {backup}" if backup else "이미 일치"))
        else:
            okay = transaction.check(); valid &= okay
            print(f"{name}: " + ("PASS" if okay else "설치 불일치"))
    if args.defer_workspace_codex and not args.global_only:
        print("보류: 작업 공간 .codex/hooks.json 설치·검사를 생략했습니다. 일반 터미널에서 Finish-Setup.ps1 -WorkspaceOnly를 실행하세요. 전체 설치 완료가 아닙니다.")
    if not args.global_only and missing:
        print("프로젝트 설치·갱신 필요: " + ", ".join(missing) + ". 연결 완료 대상으로 계산하지 않습니다.")
    if args.global_install or args.global_only:
        print("전역 설정 파일 검사와 실제 세션 활성화는 다릅니다. 새 세션에서 /hooks 신뢰와 자동 모드를 확인하세요.")
        if os.name == "nt": print("Claude OS 샌드박스는 native Windows에서 지원되지 않습니다. WSL2 사용 시 별도 설치가 필요합니다.")
    return 0 if valid else 1


if __name__ == "__main__":
    try: raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error: raise SystemExit(f"오류: {error}")
