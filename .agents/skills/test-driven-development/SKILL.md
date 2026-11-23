---
name: test-driven-development
description: 동작 변경이나 버그 수정에 재현 가능한 회귀 테스트가 필요할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/test-driven-development/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 테스트로 동작 고정하기

1. 기존 테스트 도구와 공개 진입점을 확인합니다. 요구한 동작을 표현하는 작은 테스트를 작성하고, 수정 전 예상한 이유로 실패하는지 봅니다.
2. 필요한 범위만 수정한 뒤 같은 테스트의 통과를 확인합니다. 정리 후 인접한 회귀 검사도 실행하고, 대역을 사용한 범위와 실제 연동을 검증한 범위를 기록합니다. [테스트 구조와 대역 예시](../../../.agent-rules/upstream/references/testing-patterns.md)
