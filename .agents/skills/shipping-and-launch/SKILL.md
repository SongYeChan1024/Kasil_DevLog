---
name: shipping-and-launch
description: 배포 준비, 점진 공개, 출시 검증 또는 롤백 계획을 요청할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/shipping-and-launch/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 출시 준비와 복구

1. 배포할 버전·환경·대상, 남은 검증, 데이터 변경의 가역성을 확인합니다. 공개 단위, 상태를 판단할 지표, 중단·복구 기준과 담당을 정합니다.
2. 준비 검증에는 이전 버전으로 돌아가는 방법과 사용자 핵심 동작을 포함합니다. 실제 배포는 승인된 환경에서 수행하고, 실행했다면 버전·관측 결과·미확인 항목을 기록합니다. [공통 완료 기준](../../../.agent-rules/upstream/references/definition-of-done.md)
