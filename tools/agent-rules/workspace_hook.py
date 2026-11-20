"""Route shared hooks to installed repositories without executing their scripts. Author: 송예찬."""
from __future__ import annotations

from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import runtime


def safe(path: Path, workspace: Path) -> Path:
    path = path.absolute()
    if not path.resolve().is_relative_to(workspace.resolve()):
        raise ValueError('작업 공간 밖의 검사 대상')
    for part in (path, *path.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('링크·junction 검사 대상')
        if part == workspace: break
    return path.resolve()


@contextmanager
def session_lock(path: Path, workspace: Path):
    safe(path, workspace).parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        stream.seek(0)
        if not stream.read(1): stream.write(b'0'); stream.flush()
        deadline = time.monotonic() + 200
        while True:
            stream.seek(0)
            try:
                if os.name == 'nt':
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline: raise RuntimeError('동시 검사 잠금 시간 초과')
                time.sleep(0.05)
        try: yield
        finally:
            stream.seek(0)
            if os.name == 'nt': msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else: fcntl.flock(stream, fcntl.LOCK_UN)


def snapshot(root: Path) -> dict:
    return {'files': runtime.fingerprint(root, runtime.changed_files(root)),
            'head': runtime.run_git(root, 'rev-parse', 'HEAD').decode().strip()}


def changed_since(root: Path, before: dict) -> list[str]:
    after = snapshot(root)
    names = set(before['files']) | set(after['files'])
    # Include changes committed inside the tool call, which no longer appear in git status.
    if before['head'] != after['head']:
        if not re.fullmatch(r'[0-9a-f]{40,64}', before['head']): raise ValueError('잘못된 기준 커밋')
        committed = runtime.run_git(root, 'diff', '--name-only', '-z', before['head'], 'HEAD')
        names.update(x.decode('utf-8') for x in committed.split(b'\0') if x)
    values = runtime.fingerprint(root, sorted(names))
    changed = {name for name in names if values.get(name) != before['files'].get(name)}
    if before['head'] != after['head']:
        changed.update(x.decode('utf-8') for x in committed.split(b'\0') if x)
    return sorted(changed)


def tool_args(event: dict) -> dict:
    args = event.get('tool_input', {})
    if isinstance(args, str):
        try: args = json.loads(args)
        except ValueError: return {'input': args}
    return args if isinstance(args, dict) else {}


def selection(workspace: Path, event: dict, registry: dict) -> tuple[list[str], list[str]]:
    args = tool_args(event)
    cwd = Path(event.get('cwd') or workspace)
    raw_base = args.get('workdir', args.get('cwd'))
    base = Path(raw_base) if isinstance(raw_base, str) else cwd
    if not base.is_absolute(): base = cwd / base
    values = [base]
    files = []
    for key in ('file_path', 'path'):
        if isinstance(args.get(key), str): files.append(args[key])
    patch = str(args.get('input', args.get('patch', args.get('command', '') if event.get('tool_name') == 'apply_patch' else '')))
    files += re.findall(r'^\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+)$', patch, re.M)
    for name in files:
        path = Path(name)
        values.append(path if path.is_absolute() else base / path)
    selected, workspace_files = set(), set()
    known = registry['projects']
    missing = set(registry.get('uninstalled', []))
    for value in values:
        if not value.resolve().is_relative_to(workspace.resolve()): continue
        value = safe(value, workspace)
        relative = value.relative_to(workspace)
        first = relative.parts[0] if relative.parts else ''
        if first in missing:
            raise ValueError(f'{first}: 공통 검사 설치·갱신이 필요합니다.')
        if first in known: selected.add(first)
        elif value != workspace and not runtime.secret_path(str(relative)):
            # Do not treat an unregistered Git repository as a loose workspace file.
            if any((p / '.git').exists() for p in (value.parent, *value.parents) if p != workspace and p.is_relative_to(workspace)):
                raise ValueError('등록되지 않은 저장소의 검사 대상입니다.')
            if value != base: workspace_files.add(relative.as_posix())
    # Shells can cd or invoke git -C across repositories. Compare all registered
    # repositories around an opaque shell call instead of trying to execute/parse it.
    if event.get('tool_name') in ('Bash', 'PowerShell', 'exec_command') or not selected and not workspace_files:
        selected = set(known)
    return sorted(selected), sorted(workspace_files)


def combine(event: dict, results: list[tuple[int, dict, str]], note: str = '') -> tuple[int, dict, str]:
    failures = [message or output.get('systemMessage', '공통 검사 실패') for code, output, message in results if code]
    notices = [output['systemMessage'] for _, output, _ in results if output.get('systemMessage')]
    if failures:
        message = '; '.join(failures[:8])
        if event.get('hook_event_name') == 'Stop' and event.get('stop_hook_active'):
            return 0, {'systemMessage': message + ' 반복 차단을 중지합니다. 미해결 검증을 보고하세요.'}, ''
        return 2, {}, message
    if note: notices.append(note)
    if event.get('hook_event_name') == 'SessionStart':
        return 0, {'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': ' '.join(notices)}}, ''
    return 0, ({'systemMessage': ' '.join(notices)} if notices else {}), ''


def dispatch(workspace: Path, event: dict) -> tuple[int, dict, str]:
    event = dict(event)
    # Do not read transcripts. Separate subagent caches when the host provides an id.
    session = str(event.get('session_id', 'manual')) + ':' + str(event.get('agent_id', ''))
    key = hashlib.sha256(session.encode()).hexdigest()[:24]
    event['session_id'] = 'workspace-' + key
    cache_path = workspace / '.agent-rules/.cache' / ('workspace-' + key + '.json')
    with session_lock(cache_path.with_suffix('.lock'), workspace):
        return process(workspace, event, cache_path)


def process(workspace: Path, event: dict, cache_path: Path) -> tuple[int, dict, str]:
    kind = event.get('hook_event_name')
    if kind not in ('SessionStart', 'PreToolUse', 'PostToolUse', 'Stop'): return 0, {}, ''
    registry = json.loads(safe(workspace / '.agent-rules/workspace.json', workspace).read_text(encoding='utf-8'))
    if registry.get('format') != 1: raise ValueError('지원하지 않는 작업 공간 연결 형식')
    for name, expected in registry['files'].items():
        if hashlib.sha256(safe(workspace / name, workspace).read_bytes()).hexdigest() != expected:
            raise ValueError('작업 공간 연결 파일이 설치본과 다릅니다. sync가 필요합니다.')
    cache = json.loads(safe(cache_path, workspace).read_text(encoding='utf-8')) if cache_path.exists() else {}
    cache.setdefault('active', {}); cache.setdefault('pending', {}); cache.setdefault('done', {})
    if kind == 'PreToolUse':
        reason = runtime.preflight(event)
        if reason: return 2, {}, reason
        if event.get('tool_name') == 'Read': return 0, {}, ''
    selected, loose = (list(registry['projects']), []) if kind == 'SessionStart' else ([], [])
    token = str(event.get('tool_use_id') or event.get('turn_id') or 'serial')
    if kind == 'PreToolUse':
        selected, loose = selection(workspace, event, registry)
        if token in cache['pending']: return 0, {}, ''
        if event.get('tool_use_id') and token in cache['done']: return 0, {}, ''
        cache['done'].pop(token, None)
    results = []
    if kind in ('SessionStart', 'PreToolUse'):
        before = {}
        for name in selected:
            root = safe(workspace / name, workspace)
            policy_path = safe(root / '.agent-rules/policy.json', workspace)
            if hashlib.sha256(policy_path.read_bytes()).hexdigest() != registry['projects'][name]:
                raise ValueError(f'{name}: 설치 등록과 정책이 다릅니다. sync가 필요합니다.')
            policy = json.loads(policy_path.read_text(encoding='utf-8'))
            problems = runtime.check_install(root, policy)
            if problems: raise ValueError(f'{name}: 설치 파일이 바뀌었습니다. sync 또는 검토가 필요합니다.')
            if name not in cache.setdefault('initialized', []):
                runtime.process(root, {**event, 'hook_event_name': 'SessionStart'}, cache_dir=workspace / '.agent-rules/.cache/projects' / name)
                cache['initialized'].append(name)
            if kind == 'PreToolUse': before[name] = snapshot(root)
        if kind == 'PreToolUse':
            unmanaged = {}
            if event.get('tool_name') in ('Bash', 'PowerShell', 'exec_command'):
                for name in registry.get('uninstalled', []):
                    root = safe(workspace / name, workspace)
                    if (root / '.git').exists(): unmanaged[name] = snapshot(root)
            cache['pending'][token] = {'before': before, 'loose': runtime.fingerprint(workspace, loose), 'unmanaged': unmanaged}
    if kind == 'PostToolUse' and token in cache['done']:
        return tuple(cache['done'][token])
    if kind == 'PostToolUse' or kind == 'Stop':
        pending = [token] if kind == 'PostToolUse' else list(cache['pending'])
        if kind == 'PostToolUse' and token not in cache['pending']:
            return 2, {}, '작업 전 훅 기록이 없습니다. PreToolUse 활성화와 연결을 확인하세요.'
        for pending_id in pending:
            entry = cache['pending'].pop(pending_id)
            for name, before in entry['before'].items():
                root = safe(workspace / name, workspace)
                changed = changed_since(root, before)
                if changed:
                    active = set(cache['active'].get(name, [])); active.update(changed)
                    cache['active'][name] = sorted(active)
                    results.append(runtime.process(root, {**event, 'hook_event_name': 'PostToolUse'}, changed, workspace / '.agent-rules/.cache/projects' / name))
            loose_changed = [name for name, value in runtime.fingerprint(workspace, list(entry['loose'])).items() if value != entry['loose'][name]]
            cache['loose'] = sorted(set(cache.get('loose', [])) | set(loose_changed))
            for name, before in entry.get('unmanaged', {}).items():
                if changed_since(safe(workspace / name, workspace), before):
                    cache['unmanaged'] = sorted(set(cache.get('unmanaged', [])) | {name})
        errors = runtime.static_checks(workspace, cache.get('loose', []))
        if cache.get('unmanaged'): errors.append('설치·갱신이 필요한 저장소의 변경 감지: ' + ', '.join(cache['unmanaged']) + '. 설치와 별도 검증이 필요합니다.')
        if errors: results.append((2, {}, '; '.join(errors)))
        if kind == 'Stop':
            jobs = []
            for name, changed in cache['active'].items():
                root = safe(workspace / name, workspace)
                policy = safe(root / '.agent-rules/policy.json', workspace)
                if hashlib.sha256(policy.read_bytes()).hexdigest() != registry['projects'][name]:
                    raise ValueError(f'{name}: 검사 정책 변경 감지. 원본 동기화가 필요합니다.')
                jobs.append((root, changed))
            # Repositories are independent. Keep the hook within its timeout even
            # when several repositories each have a 90-second validation task.
            with ThreadPoolExecutor(max_workers=max(1, len(jobs))) as pool:
                results.extend(pool.map(lambda job: runtime.process(job[0], event, job[1], workspace / '.agent-rules/.cache/projects' / job[0].name), jobs))
    note = ''
    if kind == 'SessionStart':
        note = f"상위 작업 공간 훅 연결: {len(registry['projects'])}개 저장소. 도구 실행 전후 변경을 대상별로 검사합니다."
        if registry.get('uninstalled'): note += ' 설치·갱신 필요: ' + ', '.join(registry['uninstalled'])
    result = combine(event, results, note)
    if kind == 'PostToolUse':
        cache['done'][token] = result
        if len(cache['done']) > 128: cache['done'].pop(next(iter(cache['done'])))
    runtime.write_cache(cache_path, cache)
    return result


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'): stream.reconfigure(encoding='utf-8')
    event = {}
    try:
        event = json.load(sys.stdin)
        code, output, message = dispatch(Path(__file__).resolve().parent.parent, event)
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, runtime.subprocess.TimeoutExpired):
        code, output, message = combine(event, [(2, {}, '작업 공간 훅 연결 실패. 설치 상태·대상 경로·Git 상태를 확인하세요.')])
    if message: print(message, file=sys.stderr)
    print(json.dumps(output, ensure_ascii=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
