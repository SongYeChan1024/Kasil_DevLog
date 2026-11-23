---
name: deprecation-and-migration
description: 구버전 API·기능·데이터 형식을 전환하거나 제거할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/deprecation-and-migration/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 폐기와 데이터 이전

1. 호출자, 기존 데이터, 사용 중인 버전을 조사하고 강제 전환이 필요한지 결정합니다. 읽기 호환, 쓰기 전환, 기존 데이터 이전, 구경로 제거의 순서와 복구 가능 지점을 정합니다.
2. 구버전과 신버전 표본, 중단 후 재시도를 검증합니다. 실제 사용량과 완료 조건을 확인한 후 구경로를 제거하고 전환하지 못한 대상을 기록합니다.
