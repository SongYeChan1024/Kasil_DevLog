---
name: observability-and-instrumentation
description: 운영 중 사용자 증상을 발견·설명하는 데 필요한 관측 수단을 설계하거나 고칠 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/observability-and-instrumentation/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 로그·지표·추적 설계

1. 운영자가 답해야 할 질문에서 시작합니다. 요청 수·오류율·지연처럼 증상을 나타내는 지표와 원인을 찾을 로그·추적을 연결합니다.
2. 가상 요청으로 신호가 수집·조회되는지 확인합니다. 민감정보와 무제한으로 늘어나는 라벨을 피하고, 알림에는 대응할 사람과 확인 절차를 연결합니다. [출시 전 관측 체크리스트](../../../.agent-rules/upstream/references/observability-checklist.md)
