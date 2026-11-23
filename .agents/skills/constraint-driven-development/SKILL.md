---
name: constraint-driven-development
description: 허용할 성능·품질 기준을 정하거나 검사 생략·임계값 변경의 근거를 검토할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/constraint-driven-development/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 품질 기준 정하기

1. 현재 측정 방법과 기준값, 실제 실패 조건을 확인한 뒤 `shared-quality` 절차를 적용합니다. 각 항목의 상태를 관찰만 하는 기준, 실제로 실패시키는 기준, 기간을 두고 허용한 예외로 구분합니다.
2. 빠른 검사는 수정 직후에, 비용이 큰 검사는 기존 CI 등 맞는 위치에 둡니다. 자동 차단을 변경했다면 정상·위반 입력과 검사 실행 실패를 확인합니다. 예외에는 이유와 해제 조건을 남깁니다. [팀 공통 완료 기준 예시](../../../.agent-rules/upstream/references/definition-of-done.md)
