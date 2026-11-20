# Codex · Claude 공통 규칙 관리

작성자: 송예찬

[RULES.md](RULES.md)가 공통·프로젝트별·검토 역할 지침의 단일 편집 원본입니다. AGENTS.md·CLAUDE.md·검토 역할 파일은 이 원본에서 생성합니다. 권한과 훅의 도구별 문법은 `rules_core.py`, 공통 검사는 `runtime.py`에서 관리합니다. 기존 `COMMON.md`는 원본 이동 안내입니다.

## 설치 대상과 파일

| 대상 | 적용 내용 |
| --- | --- |
| After Seconds, ERGO 게임·문서, DOB, 블로그 두 worktree, UnityGameFoundation | 공통 + 해당 프로젝트 규칙, Claude 연결 파일, 검증·접근 검사 훅, 외부 반영 확인 규칙, 읽기 전용 검토 역할 |
| 작업 공간 | 공통 규칙과 프로젝트 지도 |
| 선택적 홈 전역 설치 | Codex 공통 지침, Claude 연결 파일·auto 모드·추가 권한 규칙, 기존 Codex 설정에 없는 안전한 기본값 |
| LucidDiver 참고용 사본 | 원래 읽기 전용 방침을 유지하며 설치 대상에서 제외 |

저장소별 AGENTS에는 공통 규칙을 함께 담아 홈 설정이 없는 환경에서도 읽을 수 있게 합니다. 생성된 내용이 반복되더라도 사람이 수정하는 원본은 RULES.md 하나입니다. 팀 README·게임 명세·아키텍처는 해당 자료의 현행 계약으로 유지합니다.

## 의도 확인·명세·품질 스킬

세 스킬의 내용과 호출 조건은 RULES.md의 `shared-intent`, `shared-spec-plan`, `shared-quality` 구간에서 관리합니다. `sync`가 Codex용 `.agents/skills/<이름>/SKILL.md`와 Claude용 `.claude/skills/<이름>/SKILL.md`를 같은 내용으로 생성합니다. 설치 해시·수동 수정 보존·백업도 기존 지침과 같은 방식으로 적용합니다.

| 스킬 | 사용할 때 | 동작 |
| --- | --- | --- |
| shared-intent | 중요한 요구사항이 모호하거나 의도 정리를 요청했을 때 | 문서를 먼저 읽고 결과를 바꾸는 질문만 확인 |
| shared-spec-plan | 큰 기능·설계 변경 또는 명세/계획 요청 | 기존 문서에 완료 조건과 검증 방법을 맞추고 작업 분해 |
| shared-quality | 품질 기준 설정·변경 또는 검사 완화 검토 | 기준·실제 검사·실패 조건을 연결하고 변경 근거 검토 |

자연어로 요청해도 적용 조건에 맞는 스킬을 선택할 수 있습니다. 명시하려면 “shared-intent로 이 기획의 의도부터 정리해줘”, “shared-spec-plan으로 명세를 보완하고 구현까지 진행해줘”, “shared-quality로 이번 변경에서 검사가 약해졌는지 검토해줘”처럼 요청합니다. 설치 후 새 세션에서 스킬 목록을 확인합니다. 이 세션의 목록에 파일이 즉시 추가됐다고 가정하지 않습니다.

명확한 수정에는 인터뷰를 붙이지 않습니다. 진행 지시·위임을 인정하며, 구현까지 승인된 작업은 계획이나 확인 뒤에 강제로 중단하지 않습니다. 기존 프로젝트의 학습·팀 합의·외부 반영 조건은 유지합니다. 내용은 필요한 스킬만 읽으며 새 에이전트 위임이나 원본 패키지 전체 설치를 자동으로 수행하지 않습니다.

품질 기준 스킬은 판단 절차입니다. 테스트 삭제·임계값 완화를 전부 자동 차단하는 새 검사기를 설치한 것으로 보고하지 않습니다. 기계 검증은 현재 공통 훅·프로젝트 검사와 연결하고 새 차단을 만들 때 정상·위반·실행 오류를 실제로 확인합니다.

원문에서 조정한 내용과 고정된 참고 버전, MIT 고지는 [출처·라이선스](THIRD_PARTY_NOTICES.md)에 있습니다. 스킬을 개별 프로젝트로 배포할 때도 고지를 함께 생성하므로 외부 저장소의 참조 경로에 의존하지 않습니다.

## 사용

Python 3.11 이상과 Git이 필요합니다. Claude 훅은 현재 2.1.325의 exec-form 명령을, Codex 훅은 현재 0.167.0의 command/commandWindows 형식을 기준으로 구성했습니다. 모델은 바꾸지 않습니다.

```powershell
python -B tools/agent-rules/manage.py preview --workspace C:\GitHubProjects
python -B tools/agent-rules/manage.py sync --workspace C:\GitHubProjects --adopt-existing
python -B tools/agent-rules/manage.py check --workspace C:\GitHubProjects
```

처음 설치할 때만 검토한 기존 파일을 `--adopt-existing`으로 이전합니다. 이후 원본을 고친 뒤 일반 `sync`를 사용합니다. 생성 파일을 수동으로 수정하면 덮어쓰지 않고 검토를 요구합니다. `--projects Project_DOB`처럼 특정 저장소만 선택할 수도 있으며 작업 공간 지도는 함께 확인합니다.

홈 전역 설정까지 설치하려면 해당 경로를 쓸 수 있는 일반 터미널에서 실행합니다.

```powershell
python -B tools/agent-rules/manage.py preview --workspace C:\GitHubProjects --global
python -B tools/agent-rules/manage.py sync --workspace C:\GitHubProjects --global --adopt-existing
python -B tools/agent-rules/manage.py check --workspace C:\GitHubProjects --global
```

전역만 처리하려면 `--global-only`를 사용합니다. 기존 `CODEX_HOME`·`CLAUDE_CONFIG_DIR`를 읽으며 명시적 `--codex-home`·`--claude-home`도 지원합니다. 이 경로들은 권한 제한을 우회하는 기능이 아닙니다. 접근 거부는 해당 환경에서 해결해야 합니다.

현재 PC에서 남은 설치는 `tools/agent-rules/Finish-Setup.ps1`로 실행할 수 있습니다. DOB main이 깨끗할 때 기존 backend 브랜치로 전환하고 전체 설치·전역 설정·검증을 수행합니다. 변경이 있거나 쓰기 권한이 없으면 중단하며 관리자 권한 상승·보안 우회·Git push는 하지 않습니다. DOB 설정은 문서 예외에 포함되지 않으므로 역할 브랜치에서 반영합니다.

전역 설치는 검토한 Claude 개인 메모 5개도 새 지침으로 연결합니다. 원문은 백업하고 검토본 식별용 링크는 개인 메모에 유지합니다. 검토 이후 내용이 바뀌었으면 해시로 감지해 먼저 확인하도록 중단합니다. 개인 메모 본문·링크는 이 공개 도구에 포함하지 않습니다.

기존 model·MCP·theme·별도 훅·deny/allow 목록을 유지합니다. 프로젝트의 기존 custom Codex config는 통째로 교체하지 않습니다. 새 설정이 기존 보호를 완화한다고 가정하지 말고 실제 활성 설정을 확인합니다.

완료 스크립트는 ERGO 문서 저장소의 `requirements-docs.txt`를 격리된 `.agent-rules/.cache/venv`에 설치하고 링크 검사도 실행합니다. 패키지 다운로드에는 네트워크 연결이 필요합니다. 훅은 이 가상 환경이 있으면 검증용 Python으로 사용합니다.

## 자동 검사

- SessionStart: 통합 설치본의 해시를 확인하고 기존 변경을 기준 상태로 기록합니다.
- PreToolUse: 명시적인 비밀 파일 경로와 강제 push의 일반적인 형태를 검사합니다. 차단 시 비밀 값·명령 원문을 출력하지 않습니다.
- PostToolUse: 이번 세션에서 바뀐 파일의 Python·JSON·TOML 문법, 병합 충돌 표식, 규칙 설치본의 차이를 검사합니다.
- Stop: 바뀐 경로에 관련된 검증만 실행합니다. 블로그 관리 도구·편집기 회귀 검사와 ERGO 문서 링크 검사가 연결됩니다. 성공한 동일 변경에 대한 검사는 반복하지 않습니다.
- 실패는 종료 코드 2로 전달합니다. 이미 종료 훅 때문에 재개된 턴에서 문제가 계속되면 반복 차단을 중단하고 미해결 검증을 보고하도록 알립니다.
- Unity 코드는 정적 검사와 실제 에디터 컴파일·참조·Play 검증을 구분합니다. 훅이 Unity를 임의로 띄우거나 사용 중인 씬을 바꾸지 않습니다.

훅은 자동 포맷·외부 업로드·메시지·Git push·대화 로그 수집을 하지 않습니다. 캐시는 각 저장소 `.agent-rules/.cache/`에만 두고 Git에서 제외합니다. hooks는 사용자가 신뢰한 코드가 실행되는 기능이므로 스크립트와 명령을 함께 검토합니다.

## 권한과 활성화

Claude: `.env`·`secrets`·일부 인증 파일의 Read/Edit 거부, push·PR·릴리스 생성의 확인 규칙을 추가합니다. 전역 설치는 사용자 설정에서 auto 모드를 지정하고 기본 autoMode 규칙을 `$defaults`로 유지합니다. 이미 받은 대상·내용 승인을 중복 요청하지 않는 의미 규칙과 native 권한 확인은 서로 다른 층입니다.

Codex: 새 프로젝트 설정은 workspace-write와 on-request, 기본 네트워크 차단을 사용합니다. `.codex/rules/shared.rules`의 외부 반영 확인과 일반 강제 push 거부를 추가합니다. 상위 관리 정책을 바꾸거나 자동 승인하지 않습니다.

**파일 설치만으로 모든 기능이 활성화됐다고 보장하지 않습니다.** Codex는 새 세션의 `/hooks`에서 정확한 훅 정의를 검토·신뢰해야 합니다. Claude도 신뢰한 프로젝트에서 `/hooks`·`/status`로 로드된 설정을 확인합니다. 이 도구는 신뢰 기록을 위조하거나 bypass 플래그를 사용하지 않습니다.

Claude의 OS 샌드박스는 macOS·Linux·WSL2에서 지원되며 native Windows에서는 지원되지 않습니다. 전역 설치를 지원 OS에서 실행할 때 sandbox.enabled·failIfUnavailable·unsandboxed 재시도 금지를 추가합니다. Windows에서는 작동하지 않는 설정을 켰다고 보고하지 않습니다. 파일 도구 규칙과 문자열 기반 명령 검사만으로 임의 하위 프로세스의 모든 비밀 접근을 막는다고 보장하지 않습니다.

현재 Codex Windows 환경의 OS 보호는 실제 활성 샌드박스·관리 정책을 따릅니다. 이 패키지는 임의의 네트워크 허용·전역 폴더 쓰기·새 관리자 권한을 부여하지 않습니다.

## 검토 역할과 클라우드

`shared-reviewer`는 같은 RULES.md의 reviewer 구간에서 생성합니다. Claude는 Read/Grep/Glob만, Codex는 read-only sandbox로 검토하며 모델은 부모 설정을 상속합니다. 사용자가 독립 검토·분담을 요청했을 때 사용하고 파일 수정·외부 반영을 맡기지 않습니다. 정의 설치와 실제 검토 실행은 별도입니다.

클라우드용 규칙·프로젝트 설정·검사 스크립트는 저장소 안에 있으며 홈의 비밀·인증 상태에 의존하지 않습니다. 새 환경에 Python·Git과 프로젝트에 필요한 검사 의존성을 설치해야 합니다. 서비스의 신뢰·권한·네트워크·훅 지원을 확인한 뒤 실행합니다. 이 작업은 클라우드 계정·실행 환경을 새로 만들거나 유료 세션을 시작하지 않습니다. Codex Work Cloud의 local orchestration에서는 로컬 command hook이 실행되지 않을 수 있으므로 아래 공식 지원 범위를 확인합니다.

## 백업과 검증

`.state/<대상>/backups/<시각>/`에 원문과 manifest를 저장합니다. manifest에는 원래 경로와 변경 전후 SHA256이 있습니다. 각 대상 설치 중 실패하면 그 대상의 쓰기를 되돌립니다. 먼저 성공한 다른 대상까지 되돌리지는 않습니다. 로그와 `check`로 부분 성공 여부를 확인합니다. 백업·설치 상태는 개인 경로·기존 설정을 포함할 수 있어 공개하지 않습니다.

```powershell
python -B -m unittest discover -s tools/agent-rules -p 'test_*.py' -v
python -B tools/agent-rules/verify_bundle.py
```

CI도 같은 검사로 백업·충돌·복원·범위 분리·훅 실패 처리를 확인하고 생성물의 차이를 잡습니다. 전역 설치·actual 세션의 hook 활성화는 CI가 대신 검증하지 않습니다.

## 공식 근거

- [Codex 지침](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Codex hooks와 신뢰](https://learn.chatgpt.com/docs/hooks), [Codex 권한](https://learn.chatgpt.com/docs/permissions)
- [Claude 설정 범위](https://code.claude.com/docs/en/settings-reference), [hooks](https://code.claude.com/docs/en/hooks), [샌드박스](https://code.claude.com/docs/en/sandboxing), [검토 역할](https://code.claude.com/docs/en/sub-agents)

## 변경 기록

| 날짜 | 작성자 | 내용 |
| --- | --- | --- |
| 2026-11-20 | 송예찬 | 단일 원본에서 의도 확인·명세/계획·품질 스킬 생성, Codex·Claude 공통 적용과 출처 고지 추가 |
| 2026-11-20 | 송예찬 | 전역 공통 규칙 v1을 프로젝트별 범위·검증 훅·권한 확인·읽기 전용 검토 역할까지 포함하는 단일 원본 관리 방식으로 확장 |
