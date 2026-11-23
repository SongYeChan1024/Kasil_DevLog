---
name: spec-driven-development
description: 새 기능이나 큰 동작 변경의 요구사항과 수용 기준을 프로젝트 명세에 정리할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/spec-driven-development/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 검증 가능한 명세

1. 프로젝트에서 기준으로 삼는 문서와 현재 동작을 찾아 `shared-spec-plan`의 명세 단계를 적용합니다. 변경 전후에 사용자가 관찰할 결과, 입력과 출력, 오류·경계 사례, 호환성, 제외 범위를 씁니다.
2. 성공 조건마다 테스트나 확인 절차를 연결하고, 도구·경로·명령은 실제 저장소에서 확인합니다. 팀 결정을 기다리는 항목은 질문으로 표시합니다. 기존 명세의 같은 항목을 갱신해 기준을 한 곳에 둡니다.
