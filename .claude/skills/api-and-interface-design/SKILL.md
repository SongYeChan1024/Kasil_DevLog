---
name: api-and-interface-design
description: 공개 API, 모듈 경계, 데이터 형식 또는 기존 호출자가 의존하는 계약을 바꿀 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/api-and-interface-design/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# API와 모듈 계약 설계

1. 실제 호출자 기준으로 입력·출력·오류·권한과 기본값을 적습니다. 재시도·중복 호출·부분 실패가 있는 작업은 상태가 어떻게 남아야 하는지 정합니다.
2. 현재 소비자와 이전 데이터가 새 계약에서 어떻게 동작하는지 예제로 확인합니다. 호환성을 깨는 변경에는 전환 경로와 종료 시점을 제시하고 계약 테스트를 연결합니다.
