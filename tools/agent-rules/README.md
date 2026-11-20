# 공통 에이전트 규칙 관리

작성자: 송예찬

이 폴더의 [COMMON.md](COMMON.md)가 개인 공통 규칙의 Git 원본이다. 한 번 설치하면 Codex와 Claude Code가 모든 로컬 프로젝트에서 같은 규칙을 읽는다. 프로젝트 파일을 일괄 덮어쓰지 않아 팀 합의·담당 범위·직접 코딩 학습 방침을 보존한다.

```text
블로그 Git: tools/agent-rules/COMMON.md  ← 공통 규칙 수정
                │ manage.py sync
                ▼
PC: ~/.codex/AGENTS.md                 ← 공통 규칙 설치본
    ~/.claude/CLAUDE.md                ← 위 설치본을 @import
                +
프로젝트: AGENTS.md / CLAUDE.md         ← 프로젝트 고유 규칙
          인수인계 문서                  ← 현재 상태·작업 이력
```

전역 설치가 핵심이다. 상위 `C:\GitHubProjects\AGENTS.md` 하나만 바꾸면 하위 Git 저장소에도 자동으로 적용된다고 가정하지 않는다. Codex는 전역 지침과 저장소 안의 지침을 조합한다. Claude는 개인 지침에서 공통 설치본을 가져온다. [Codex 지침 검색](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [Claude 가져오기](https://code.claude.com/docs/en/memory#import-additional-files)

## 처음 설치

Python 3.10 이상이 필요하며 추가 패키지는 없다. 아래 명령은 블로그 저장소 루트의 일반 터미널에서 실행한다. 샌드박스가 사용자 홈 쓰기를 막는 세션에서는 미리보기와 검증까지만 가능하다.

```powershell
python tools/agent-rules/manage.py preview --workspace C:\GitHubProjects
```

`COMMON.md`와 기존 `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`를 비교한 뒤 이전한다. 기존 파일은 백업한다. 원본에 없는 개인 규칙이 있다면 먼저 공통 원본 또는 해당 프로젝트 지침으로 옮긴다.

```powershell
python tools/agent-rules/manage.py sync --workspace C:\GitHubProjects --adopt-existing
python tools/agent-rules/manage.py check
```

- `--adopt-existing`은 기존 지침을 공통 원본으로 **교체하는 첫 이전**에 사용한다. 설치 후 수동 편집을 무시하는 데도 사용될 수 있으므로 평소 갱신에서는 생략한다.
- 설치본과 원본이 이미 같으면 파일을 다시 쓰거나 백업을 늘리지 않는다.
- `CODEX_HOME`, `CLAUDE_CONFIG_DIR`를 사용 중이면 따른다. `--codex-home`, `--claude-home`으로 직접 지정할 수도 있다.
- 홈 경로가 바뀌면 기존 설치 기록을 확인하고 이전한다. 링크·정션 경로에는 쓰지 않는다.
- `AGENTS.override.md`가 공통 지침을 가리고 있으면 설치를 멈추고 그 경로를 알려 준다. 자동으로 삭제하지 않는다.
- `--workspace`는 PC별 경로이며 설치 기록에만 저장한다. 다른 PC에서는 그 PC의 프로젝트 모음 경로를 지정한다. 이후 생략하면 기록된 경로를 사용한다.

설치 후 **새 Codex·Claude 세션**에서 “현재 적용된 공통 지침의 출처와 프로젝트 고유 규칙을 요약해 줘”라고 확인한다. `check` 성공은 파일과 설치 기록이 일치한다는 뜻이며, 실행 중인 세션의 재로딩이나 실제 모델 준수 여부를 보장하지 않는다.

## 다른 PC와 이후 갱신

블로그 저장소를 받은 뒤 같은 설치 명령을 실행한다. 폴더 이름과 절대 경로가 달라도 된다. 블로그 worktree를 쓰는 PC는 `git worktree list`로 현재 브랜치부터 확인한다.

```powershell
git status --short --branch
git pull --ff-only
python tools/agent-rules/manage.py preview
python tools/agent-rules/manage.py sync
python tools/agent-rules/manage.py check
```

`pull` 실패 시 중단하고 차이를 확인한다. 스크립트가 Git pull·commit·push를 대신 실행하지 않는다. 다른 PC가 받는 변경은 공통 원본이 해당 원격 브랜치에 반영된 이후부터다. 동기화 없이 원본만 바꿔도 설치본이 자동 갱신되는 것은 아니다.

## 프로젝트별 적용

이미 `AGENTS.md`와 `CLAUDE.md`가 있는 프로젝트는 그대로 사용한다. 공통 규칙을 복사해서 넣지 않고 프로젝트 고유 규칙만 관리한다. 팀 규칙은 팀 저장소의 기존 문서를 기준으로 유지하며 개인 전역 지침으로 팀 합의를 바꾸지 않는다.

새 프로젝트에는 [Codex 안내 템플릿](templates/AGENTS.md.txt)과 [프로젝트 규칙 템플릿](templates/CLAUDE.md.txt)을 참고한다. 기존 파일에 자동으로 덮어쓰지 않는다. Claude의 `@문서` 구문이 Codex에서도 자동으로 펼쳐진다고 가정하지 말고, Codex 안내에 읽을 문서를 명시한다.

작업 공간과 바로 아래 Git 저장소의 지침 크기는 읽기 전용으로 확인할 수 있다.

```powershell
python tools/agent-rules/manage.py audit --workspace C:\GitHubProjects
```

이 검사는 파일명·줄 수·UTF-8 바이트 크기만 확인한다. Codex의 기본 지침 크기 한도는 합산 32KiB이므로 개별 파일이 그보다 작아도 중첩 지침과 합치면 잘릴 수 있다. 200줄은 정리의 참고 기준이며 Codex의 강제 줄 수 제한이 아니다. 오래된 상태 기록을 옮길 때는 최신 인수인계 링크와 고유 규칙을 남기고 기록 자체는 보존한다. [Codex 크기 한도](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [지침 정리 기준](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

## 권한·비밀 파일·검사 자동화

이번 동기화 대상은 **작업 지침**이다. `config.toml`, Claude `settings.json`, MCP 연결, 승인 정책, 모델, 샌드박스, 훅은 설치 스크립트가 변경하지 않는다. 지침에 “비밀을 출력하지 않는다”고 적는 것과 OS 수준에서 읽기를 차단하는 것은 다르다.

추가 설정은 해당 실행 환경과 프로젝트에 맞춰 별도로 검증한다.

| 대상 | 적용 기준 |
| --- | --- |
| 파일·네트워크 권한 | Codex 권한 프로필과 Claude 샌드박스의 현재 지원 범위를 확인한 뒤 필요한 경로·도메인만 지정한다. 더 넓은 권한으로 기존 제한을 우회하지 않는다. |
| 자동 승인 | 현재 승인 정책을 확인한다. 공통 지침의 외부 반영 승인 범위를 설정 파일로 임의 완화하지 않는다. |
| 검사 훅 | 해당 프로젝트에서 이미 검증한 명령을 연결한다. Unity·문서·블로그에 똑같은 `npm test`를 적용하지 않는다. |
| 종료 시 검사 | 관련 변경이 있을 때 실행한다. 실패 시 동작과 반복 방지까지 검증한 뒤 켠다. 매 편집마다 전체 테스트를 강제하지 않는다. |
| 클라우드 세션 | 로컬 홈 설치가 자동 전달된다고 가정하지 않는다. 그 환경의 설정·지침 로딩을 따로 확인한다. |

Codex의 로컬 훅은 `hooks.json` 또는 `config.toml`에 둘 수 있지만 환경별 지원이 다르다. Claude 예제의 `type: "agent"` 핸들러를 그대로 옮기지 않는다. 문서상 Codex는 `command`, `mcp_tool` 핸들러를 지원하고 `agent`, `prompt`는 건너뛴다. [Codex 훅](https://learn.chatgpt.com/docs/hooks) · [Codex 권한](https://learn.chatgpt.com/docs/permissions)

## 백업과 복구

변경 전 원본과 설치 기록은 `~/.codex/agent-rules/backups/<시각-식별자>/`에 저장한다. `manifest.json`은 원래 경로와 백업 파일을 대응시킨다. 백업은 개인 PC에만 두며 Git에 올리지 않는다.

설치 중 파일 쓰기가 실패하면 이미 쓴 파일을 이전 내용으로 되돌린다. 자동 복원이 실패한 경로와 백업 위치는 오류로 출력한다. 수동 복구 시 실행 중인 편집을 먼저 멈추고, `manifest.json`의 `existed: true` 항목은 해당 백업을 원래 `target`에 복사한다. `existed: false` 항목은 이번 설치로 생성된 파일이므로 이후 편집이 없는지 확인한 뒤 제거한다. 이전 `state.json`도 함께 복구한다.

## 도구 검증

```powershell
python -B -m unittest discover -s tools/agent-rules -p "test_*.py" -v
```

테스트는 임시 홈만 사용한다. 첫 설치·기존 파일 백업·반복 실행·원본 갱신·수동 변경 보호·쓰기 실패 복원·전역 override·공백과 한글 경로를 확인한다. 실제 사용자 설정과 외부 서비스는 변경하지 않는다.

종료 코드는 성공 `0`, `check` 불일치 `1`, 사용·설치 오류 `2`다. 이는 이 CLI의 종료 코드이며 에이전트 훅의 종료 코드 계약과 별개다.

## 변경 기록

| 날짜 | 작성자 | 내용 |
| --- | --- | --- |
| 2026-11-20 | 송예찬 | 개인 공통 규칙을 Git 원본으로 분리하고 Codex·Claude 전역 지침 동기화·백업·점검 도구 추가 |
