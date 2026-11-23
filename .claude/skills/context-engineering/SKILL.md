---
name: context-engineering
description: 작업을 이어받거나 자료가 흩어져 에이전트의 판단에 필요한 맥락을 복원할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/context-engineering/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 작업 맥락 구성

1. 현행 지침, 대상 브랜치와 변경 상태, 기준 명세, 정상 진입점, 검증 명령의 위치를 찾습니다. 날짜가 지난 인수인계와 코드가 다르면 현재 동작을 직접 확인합니다.
2. 다음 작업자가 필요한 결정과 근거 위치, 이미 검증한 범위, 풀어야 할 질문을 짧게 남깁니다. 문서 전문을 여러 곳에 복제하는 대신 원본과 관련 구간을 연결합니다.
