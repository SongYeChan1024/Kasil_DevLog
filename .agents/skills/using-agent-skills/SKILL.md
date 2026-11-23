---
name: using-agent-skills
description: 요청에 쓸 개발 절차를 고르거나 여러 작업을 어떤 순서로 진행할지 정할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/main/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/using-agent-skills/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 작업에 맞는 스킬 고르기

1. 사용자가 이번에 받을 결과를 먼저 적습니다. 결정이 필요한 기획이면 `interview-me`나 `idea-refine`, 검증할 요구사항이 있으면 `spec-driven-development`, 이미 명세가 있으면 `planning-and-task-breakdown`에서 시작합니다.
2. 작은 버그는 `debugging-and-error-recovery`로 바로 좁힙니다. UI 상태는 `browser-testing-with-devtools`, 동작 회귀는 `test-driven-development`, 출시 준비는 `shipping-and-launch`처럼 실제 변경에 맞는 항목만 읽습니다.
3. 결과는 선택한 절차와 확인할 성공 조건입니다. 분업이 요청된 작업에서는 각 담당의 변경 범위와 최종 검증 위치를 정합니다. [여러 역할의 책임과 인계 예시](../../../.agent-rules/upstream/references/orchestration-patterns.md)
