"""Render one policy source for Codex and Claude. Author: 송예찬."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "RULES.md"
PROJECTS = {
    "After_Seconds": ("unity", "after-seconds"),
    "ERGOSQUARE-ARCHITECT": ("unity", "ergo-game"),
    "Document_ERGOSQUARE-ARCHITECT": ("ergo-docs",),
    "Project_DOB": ("unity", "dob"),
    "Kasil_DevLog": ("blog",),
    "Kasil-portfolio-pages": ("blog",),
    "UnityGameFoundation": ("foundation",),
}
SOURCE_URL = "https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md"
SECRET_PATTERNS = ["**/.env", "**/.env.*", "**/secrets/**", "~/.ssh/**", "~/.aws/credentials", "~/.git-credentials"]


def sha(data: bytes | None) -> str | None:
    return hashlib.sha256(data).hexdigest() if data is not None else None


def encoded(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sections(source: bytes) -> dict[str, str]:
    text = source.decode("utf-8-sig")
    matches = re.findall(r"<!-- scope:([\w-]+) -->\s*\n(.*?)<!-- /scope -->", text, re.S)
    parts = {key: body.strip() + "\n" for key, body in matches}
    required = {"common", "workspace", "lucid-reference", "reviewer"} | {x for group in PROJECTS.values() for x in group}
    if set(parts) != required or len(parts) != len(matches) or len(matches) != text.count("<!-- scope:") or len(matches) != text.count("<!-- /scope -->"):
        raise ValueError("RULES.md 범위가 누락·중복되었거나 구분 표식이 잘못되었습니다.")
    return parts


def instructions(source: bytes, scopes: tuple[str, ...]) -> bytes:
    parts = sections(source)
    result = (
        "<!-- Generated: Kasil_DevLog/tools/agent-rules/manage.py; 직접 편집하지 않습니다. -->\n"
        f"<!-- Source SHA256: {sha(source)} -->\n\n"
        f"편집 원본: [통합 규칙]({SOURCE_URL}). 원본에서 수정하고 관리 도구로 동기화합니다.\n\n"
        + "\n".join(parts[name] for name in scopes)
    ).encode("utf-8")
    if len(result) > 25000:
        raise ValueError("적용 지침이 너무 큽니다. 범위를 더 나누세요.")
    return result


def merge_lists(base: dict, additions: dict) -> dict:
    """Preserve unrelated settings and existing permission restrictions."""
    result = json.loads(json.dumps(base))
    for key, value in additions.items():
        if isinstance(value, dict):
            previous = result.get(key, {})
            if not isinstance(previous, dict):
                raise ValueError(f"기존 설정 형태를 확인하세요: {key}")
            result[key] = merge_lists(previous, value)
        elif isinstance(value, list):
            previous = result.get(key, [])
            if not isinstance(previous, list):
                raise ValueError(f"기존 목록 설정을 확인하세요: {key}")
            result[key] = previous + [x for x in value if x not in previous]
        else:
            result[key] = value
    return result


def claude_permissions() -> dict:
    asks = [f"{shell}({command} *)" for shell in ("Bash", "PowerShell")
            for command in ("git push", "gh pr create", "gh pr merge", "gh release create")]
    denies = [f"Read({pattern})" for pattern in SECRET_PATTERNS]
    denies += [f"Edit({pattern})" for pattern in SECRET_PATTERNS]
    denies += [f"{shell}(git push *{flag}*)" for shell in ("Bash", "PowerShell") for flag in ("--force", " -f")]
    return {"permissions": {"ask": asks, "deny": denies}}


def hook_config(agent: str) -> dict:
    if agent == "claude":
        handler = {"type": "command", "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.agent-rules/runtime.py"], "timeout": 120}
    else:
        # Resolve the Git root when a session starts from a subdirectory. No shell input interpolation.
        bootstrap = "import pathlib,runpy; p=pathlib.Path.cwd(); r=next(d for d in (p,*p.parents) if (d/'.git').exists()); runpy.run_path(str(r/'.agent-rules/runtime.py'),run_name='__main__')"
        handler = {"type": "command", "command": f'python3 -c "{bootstrap}"',
                   "commandWindows": f'python -c "{bootstrap}"', "timeout": 120,
                   "statusMessage": "공통 규칙·변경 파일 검사"}
    return {"hooks": {
        "SessionStart": [{"hooks": [handler]}],
        "PreToolUse": [{"matcher": "Read|Edit|Write|Bash|PowerShell|apply_patch|exec_command", "hooks": [handler]}],
        "PostToolUse": [{"matcher": "Edit|Write|Bash|PowerShell|apply_patch|exec_command", "hooks": [handler]}],
        "Stop": [{"hooks": [handler]}],
    }}


CODEX_CONFIG = '''# Managed by Kasil_DevLog/tools/agent-rules/manage.py
# 상위 관리 정책을 변경하지 않습니다. 실제 권한은 새 세션에서 확인합니다.
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false

[agents.shared_reviewer]
description = "Read-only review when the user requests an independent reviewer."
config_file = "agents/shared-reviewer.toml"
'''

EXEC_RULES = '''# 공통 외부 반영 확인. 명령 변형 전체를 보장하는 보안 경계는 아닙니다.
prefix_rule(pattern=["git", "push"], decision="prompt")
prefix_rule(pattern=["gh", "pr", "create"], decision="prompt")
prefix_rule(pattern=["gh", "pr", "merge"], decision="prompt")
prefix_rule(pattern=["git", "push", "--force"], decision="forbidden")
prefix_rule(pattern=["git", "push", "-f"], decision="forbidden")
'''


def validation_tasks(profile: str) -> list[dict]:
    if profile == "blog":
        return [
            {"name": "agent-rules", "patterns": ["tools/agent-rules/*", ".agent-rules/*", ".claude/*", ".codex/*"],
             "requires": "tools/agent-rules/test_manage.py", "command": ["{python}", "-B", "-m", "unittest", "discover", "-s", "tools/agent-rules", "-p", "test_*.py"]},
            {"name": "blog-editor", "patterns": ["admin/*", "assets/js/*", "tools/*regression*"],
             "requires": "tools/editor-regression.test.mjs", "command": ["node", "--test", "tools/editor-regression.test.mjs", "tools/cache-regression.test.mjs"]},
        ]
    if profile == "ergo-docs":
        return [{"name": "document-links", "patterns": ["*.md", "**/*.md", "docs/*"],
                 "requires": "docs/validate_consolidation.py", "command": ["{python}", "docs/validate_consolidation.py"]}]
    return []


def render_project(project: Path, source: bytes, existing: dict[str, bytes | None]) -> dict[str, bytes]:
    scopes = PROJECTS[project.name]
    reviewer = sections(source)["reviewer"]
    result = {
        "AGENTS.md": instructions(source, ("common",) + scopes),
        "CLAUDE.md": b"# Shared agent instructions\n\n@AGENTS.md\n",
        ".agent-rules/runtime.py": (ROOT / "runtime.py").read_bytes(),
        ".agent-rules/.gitignore": b".cache/\n__pycache__/\n",
        ".codex/rules/shared.rules": EXEC_RULES.encode("utf-8"),
        ".codex/agents/shared-reviewer.toml": ('sandbox_mode = "read-only"\ndeveloper_instructions = ' + json.dumps(reviewer, ensure_ascii=False) + '\n').encode("utf-8"),
        ".claude/agents/shared-reviewer.md": ('---\nname: shared-reviewer\ndescription: Read-only review when the user explicitly requests an independent reviewer.\ntools: Read, Grep, Glob\nmodel: inherit\n---\n\n' + reviewer).encode("utf-8"),
    }
    attributes = (existing.get(".gitattributes") or b"").decode("utf-8-sig").replace("\r\n", "\n")
    attributes = re.sub(r"(?ms)^# BEGIN shared-agent-rules\r?\n.*?^# END shared-agent-rules\r?\n?", "", attributes).rstrip()
    managed_attributes = "\n".join(f"{name} text eol=lf" for name in (".gitattributes", "AGENTS.md", "CLAUDE.md", "DOCUMENT_RULES.md", ".agent-rules/**", ".claude/**", ".codex/**", "tools/agent-rules/**"))
    result[".gitattributes"] = (attributes + ("\n\n" if attributes else "") + "# BEGIN shared-agent-rules\n" + managed_attributes + "\n# END shared-agent-rules\n").encode("utf-8")
    if scopes[-1] == "ergo-docs":
        result["DOCUMENT_RULES.md"] = ("# 문서 운영 규칙\n\n작성자: 송예찬\n\n문서 운영 규칙은 [통합 작업 지침](AGENTS.md)의 ERGOSQUARE 문서 범위를 따릅니다. "
            f"[편집 원본]({SOURCE_URL})에서 고치고 동기화합니다. 이 파일은 기존 링크를 보존하는 안내입니다.\n\n"
            "게임 기획의 원본은 종합 기획서이며, 과거 문서 운영 규칙과 변경 기록은 Git 이력·통합 전 백업에서 확인합니다.\n").encode("utf-8")
    for agent, name in (("claude", ".claude/settings.json"), ("codex", ".codex/hooks.json")):
        old = json.loads(existing[name].decode("utf-8-sig")) if existing.get(name) else {}
        # Replace only our previous handlers; preserve other custom hooks.
        for groups in old.get("hooks", {}).values():
            for group in groups:
                group["hooks"] = [h for h in group.get("hooks", []) if ".agent-rules/runtime.py" not in json.dumps(h)]
        for event in list(old.get("hooks", {})):
            old["hooks"][event] = [g for g in old["hooks"][event] if g.get("hooks")]
        additions = hook_config(agent)
        if agent == "claude":
            additions = merge_lists(additions, claude_permissions())
        result[name] = encoded(merge_lists(old, additions))
    prior = existing.get(".codex/config.toml")
    if prior and prior != CODEX_CONFIG.encode("utf-8"):
        # Never replace a project's custom sandbox/model/MCP configuration silently.
        tomllib.loads(prior.decode("utf-8-sig"))
        result[".codex/config.toml"] = prior
    else:
        result[".codex/config.toml"] = CODEX_CONFIG.encode("utf-8")
    policy = {"format": 2, "profile": scopes[-1], "source_sha256": sha(source),
              "source_url": SOURCE_URL, "files": {k: sha(v) for k, v in result.items()},
              "checks": validation_tasks(scopes[-1])}
    result[".agent-rules/policy.json"] = encoded(policy)
    return result


PROJECT_FILES = ("AGENTS.md", "CLAUDE.md", ".agent-rules/runtime.py", ".agent-rules/.gitignore",
                 ".agent-rules/policy.json", ".claude/settings.json", ".codex/hooks.json",
                 ".codex/config.toml", ".codex/rules/shared.rules", ".codex/agents/shared-reviewer.toml", ".claude/agents/shared-reviewer.md", ".gitattributes", "DOCUMENT_RULES.md")
