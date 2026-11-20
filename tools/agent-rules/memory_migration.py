"""Migrate the five reviewed personal memory files; never publish their contents. Author: 송예찬."""
from pathlib import Path
import hashlib
import re

EXPECTED = {'C--GitHubProjects/agent-context-locations.md': 'bfdaf6bdcdc8f5da01724d46b5b1f2af23f7daaacf7b5e6a5b614f21ddc0f92a', 'C--GitHubProjects/reply-in-korean.md': 'fb5b1784a6c99d9673b5788474404062cbfb10aea7d3f0f91ca6a22c7bcb8abe', 'C--GitHubProjects-After-Seconds/google-doc-review-copy.md': '8dabd0baab175ef5d5232706ffb6f999d7ce2a671e66f31d50d012ec3f11bdf1', 'C--GitHubProjects-Project-DOB/devlog-blog.md': 'e1da485106b54f156f6e940e4c3e342943a8cbcf8a72b51205e8775533cffb32', 'C--GitHubProjects-Project-DOB/reply-in-korean.md': '193ce4a4ba5fc55b2046370d4e4d8b3d7533057e90e54ce6bfbc0a6865072d0b'}


def targets(claude_home: Path) -> dict[Path, bytes]:
    result = {}
    for relative, expected in EXPECTED.items():
        project, name = relative.split('/', 1)
        path = claude_home / 'projects' / project / 'memory' / name
        if not path.is_file():
            continue
        raw = path.read_bytes()
        old = raw.decode('utf-8-sig')
        marker = '<!-- migrated-to-shared-agent-rules -->'
        if marker in old:
            result[path] = raw
            continue
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('검토 이후 개인 메모가 바뀌어 보존했습니다: ' + str(path))
        front = re.match(r'(?s)\A---\r?\n.*?\r?\n---\r?\n', old)
        header = front.group(0).replace('\r\n', '\n') if front else ''
        body = marker + '\n\n이 메모의 지속 작업 규칙은 전역 AGENTS.md와 해당 저장소 AGENTS.md로 통합했습니다. 예전 메모의 도구 제한·날짜별 할 일을 현재 지침으로 적용하지 않습니다. 원문은 공통 규칙 설치 백업에서 확인합니다.\n'
        if name == 'google-doc-review-copy.md':
            refs = [line for line in old.splitlines() if 'docs.google.com/document/' in line]
            if refs:
                body += '\n아래는 기존 검토본을 찾기 위한 과거 참조입니다. 최신 검토본은 작업할 때 확인합니다.\n\n' + '\n'.join('> ' + line for line in refs) + '\n'
        result[path] = (header + '\n' + body).encode('utf-8')
    return result
