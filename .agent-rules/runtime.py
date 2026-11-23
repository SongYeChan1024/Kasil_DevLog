"""Shared local-only hooks. Author: 송예찬. Never uploads, formats, or reads transcripts."""
from __future__ import annotations

import ast
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib

ENTRY_BEGIN = b"<!-- BEGIN kasil-shared-instructions -->"
ENTRY_END = b"<!-- END kasil-shared-instructions -->"


def entry_parts(name: str, data: bytes) -> tuple[bytes, bytes]:
    """Only the leading managed block belongs to the installer."""
    if name not in ("AGENTS.md", "CLAUDE.md"):
        return data, b""
    text = data.removeprefix(b"\xef\xbb\xbf")
    if not text.startswith(ENTRY_BEGIN):
        return b"", text
    match = re.match(re.escape(ENTRY_BEGIN) + rb"\r?\n.*?^" + re.escape(ENTRY_END) + rb"\r?\n", text, re.S | re.M)
    if not match:
        raise ValueError(f"{name}: 공통 지침의 끝 표식을 확인하세요.")
    return match.group().replace(b"\r\n", b"\n"), text[match.end():]


def installation_hash(name: str, data: bytes) -> str:
    block, _ = entry_parts(name, data)
    return hashlib.sha256(block or data).hexdigest()


def secret_path(value: str) -> bool:
    parts = value.replace("\\", "/").lower().strip("\"'").split("/")
    return any(p == ".env" or p.startswith(".env.") or p in ("secrets", ".ssh", ".git-credentials") for p in parts) or "/.aws/credentials" in "/".join(parts)


def preflight(event: dict) -> str | None:
    args = event.get("tool_input", {})
    if isinstance(args, str):
        try: args = json.loads(args)
        except ValueError: args = {"input": args}
    if not isinstance(args, dict):
        return None
    for key in ("file_path", "path"):
        if isinstance(args.get(key), str) and secret_path(args[key]):
            return "비밀 파일 접근은 공통 규칙에서 차단합니다. 값 대신 비밀 없는 예제·키 이름을 사용하세요."
    patch = str(args.get("input", args.get("patch", args.get("command", "") if event.get("tool_name") == "apply_patch" else "")))
    for name in re.findall(r"^\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+)$", patch, re.M):
        if secret_path(name):
            return "비밀 파일을 패치하지 않습니다. 대상·범위를 별도로 확인하세요."
    if event.get("tool_name", "") in ("Bash", "PowerShell", "exec_command"):
        command = str(args.get("command", args.get("cmd", "")))
        if re.search(r"\bgit(?:\.exe)?\b[^\r\n]*\bpush\b", command, re.I) and re.search(r"(?:^|\s)(?:--force(?:-with-lease|-if-includes)?(?:=\S*)?|-f)(?:\s|$)", command):
            return "원격 이력을 덮어쓰는 강제 push는 차단합니다. 기존 이력을 보존하는 반영 경로를 사용하세요."
        for token in re.findall(r'''[^\s;|<>]+''', command):
            if secret_path(token):
                return "명령에 비밀 파일 경로가 포함되어 있습니다. 비밀 값 출력 없이 필요한 항목만 확인하세요."
    return None


def run_git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=15)
    if result.returncode:
        raise RuntimeError("Git 변경 목록 조회 실패")
    return result.stdout


def changed_files(root: Path) -> list[str]:
    tracked = run_git(root, "diff", "--name-only", "-z", "HEAD")
    untracked = run_git(root, "ls-files", "--others", "--exclude-standard", "-z")
    return sorted({x.decode("utf-8", errors="replace") for x in (tracked + untracked).split(b"\0") if x})


def fingerprint(root: Path, names: list[str]) -> dict[str, str]:
    result = {}
    for name in names:
        path = root / name
        if secret_path(name) or not path.resolve().is_relative_to(root) or ".cache/" in name:
            continue
        if not path.is_file() or path.is_symlink():
            result[name] = "missing"
        elif path.stat().st_size <= 2_000_000:
            result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            info = path.stat()
            result[name] = f"large:{info.st_size}:{info.st_mtime_ns}"
    return result


def static_checks(root: Path, names: list[str]) -> list[str]:
    errors = []
    for name in names:
        path = root / name
        if secret_path(name) or not path.resolve().is_relative_to(root) or not path.is_file() or path.is_symlink() or path.stat().st_size > 2_000_000:
            continue
        if path.suffix.lower() not in (".py", ".json", ".asmdef", ".asmref", ".toml", ".md", ".cs", ".yml", ".yaml"):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
            if re.search(r"^<<<<<<< .+$", text, re.M) and re.search(r"^>>>>>>> .+$", text, re.M):
                errors.append(f"{name}: 병합 충돌 표식")
            if path.suffix == ".py": ast.parse(text, filename=name)
            elif path.suffix in (".json", ".asmdef", ".asmref"): json.loads(text)
            elif path.suffix == ".toml": tomllib.loads(text)
        except (ValueError, SyntaxError, UnicodeError):
            errors.append(f"{name}: 문법·인코딩 오류 (원문 값은 출력하지 않음)")
    return errors


def check_install(root: Path, policy: dict) -> list[str]:
    errors = []
    for name, expected in policy["files"].items():
        path = root / name
        if not path.resolve().is_relative_to(root) or secret_path(name) or path.is_symlink():
            errors.append("설치 manifest에 허용되지 않는 경로가 있습니다.")
        elif not path.is_file() or installation_hash(name, path.read_bytes()) != expected:
            errors.append(f"{name}: 통합 원본 설치본과 불일치. 원본 수정 후 sync 또는 설치 검토가 필요합니다.")
    return errors


def write_cache(path: Path, data: dict) -> None:
    for parent in (path, *path.parents):
        if parent.is_symlink() or (hasattr(parent, "is_junction") and parent.is_junction()):
            raise ValueError("검사 캐시의 링크 경로는 사용하지 않습니다.")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix="hook-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream: json.dump(data, stream, ensure_ascii=False)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp): os.unlink(temp)


def process(root: Path, event: dict, changed: list[str] | None = None, cache_dir: Path | None = None) -> tuple[int, dict, str]:
    event_name = event.get("hook_event_name", "")
    if event_name == "PreToolUse":
        reason = preflight(event)
        return (2, {}, reason) if reason else (0, {}, "")
    policy = json.loads((root / ".agent-rules/policy.json").read_text(encoding="utf-8"))
    key = hashlib.sha256(str(event.get("session_id", "manual")).encode()).hexdigest()[:24]
    cache_path = (cache_dir if cache_dir is not None else root / ".agent-rules/.cache") / (key + ".json")
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    current = fingerprint(root, changed_files(root) if changed is None else changed)
    if event_name == "SessionStart":
        cache.setdefault("baseline", current)
        write_cache(cache_path, cache)
        errors = check_install(root, policy)
        message = f"통합 규칙 {policy['source_sha256'][:12]} / {policy['profile']} 적용 파일 확인. "
        message += "설치 불일치: " + "; ".join(errors) if errors else "변경 파일 검사와 종료 전 관련 검증을 사용합니다."
        return 0, {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": message}}, ""
    touched = set(cache.get("touched", []))
    touched.update(name for name, value in current.items() if cache.get("baseline", {}).get(name) != value)
    cache["touched"] = sorted(touched)
    snapshots = fingerprint(root, sorted(touched))
    signature = hashlib.sha256(json.dumps(snapshots, sort_keys=True).encode()).hexdigest()
    errors = static_checks(root, sorted(touched)) + check_install(root, policy)
    if event_name == "Stop" and not errors and cache.get("validated") != signature:
        for check in policy.get("checks", []):
            if not any(fnmatch.fnmatch(name, pattern) for name in touched for pattern in check["patterns"]):
                continue
            if not (root / check["requires"]).is_file():
                errors.append(check["name"] + ": 필수 검증 스크립트가 없습니다.")
                continue
            interpreter = root / ".agent-rules/.cache/venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            python = str(interpreter) if interpreter.is_file() else sys.executable
            command = [python if arg == "{python}" else arg for arg in check["command"]]
            try:
                outcome = subprocess.run(command, cwd=root, capture_output=True, timeout=90)
                if outcome.returncode:
                    errors.append(check["name"] + ": 검증 실패. 명시된 검증 명령으로 상세 결과를 확인하세요.")
            except (OSError, subprocess.TimeoutExpired):
                errors.append(check["name"] + ": 실행 실패 또는 시간 초과")
        if not errors: cache["validated"] = signature
    write_cache(cache_path, cache)
    if errors:
        message = "공통 검사 실패: " + "; ".join(errors[:12])
        if event_name == "Stop" and event.get("stop_hook_active"):
            return 0, {"systemMessage": message + " 반복 종료 차단을 중지합니다. 미해결 검증을 완료로 보고하지 마세요."}, ""
        return 2, {}, message
    note = ""
    if event_name == "Stop" and any(name.endswith((".cs", ".unity", ".prefab")) for name in touched):
        note = "정적 검사는 통과했습니다. Unity 컴파일·참조·실행 검증은 별도로 수행하고 미실행 항목을 구분하세요."
    return 0, ({"systemMessage": note} if note else {}), ""


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"): stream.reconfigure(encoding="utf-8")
    root = Path(__file__).resolve().parent.parent
    event = {}
    try:
        event = json.load(sys.stdin)
        code, output, message = process(root, event)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired):
        code, output, message = 2, {}, "공통 검사 실행 실패. 설정·Git 상태·검사 스크립트를 확인하세요."
        if event.get("hook_event_name") == "Stop" and event.get("stop_hook_active"):
            code, output, message = 0, {"systemMessage": message + " 반복 차단을 중지합니다. 검증 실패를 사용자에게 보고하세요."}, ""
    if message: print(message, file=sys.stderr)
    print(json.dumps(output, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
