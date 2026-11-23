---
name: planning-and-task-breakdown
description: 합의한 명세를 의존 관계와 완료 조건이 있는 구현 작업으로 나눌 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/planning-and-task-breakdown/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 명세를 작업으로 나누기

1. `shared-spec-plan`의 계획 단계를 사용합니다. 각 수용 기준에서 역으로 필요한 작업을 찾고, 선행할 데이터·인터페이스 결정과 독립적으로 진행할 작업을 구분합니다.
2. 각 작업에는 사용자에게 보이는 결과, 영향을 주는 파일이나 소유자, 확인 방법을 적습니다. 계획 전체를 따라가며 빠진 수용 기준과 두 작업이 동시에 소유하는 파일을 확인합니다.
