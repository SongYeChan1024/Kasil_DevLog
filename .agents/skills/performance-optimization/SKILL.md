---
name: performance-optimization
description: 지연·메모리·렌더링 비용 등 측정 가능한 병목이나 성능 회귀를 다룰 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/performance-optimization/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 성능 측정과 개선

1. 사용자가 느끼는 증상과 대표 입력·기기·빌드 조건을 정하고 변경 전 기준을 측정합니다. 추적으로 가장 큰 비용이 생기는 구간을 확인한 뒤 한 가지 병목을 수정합니다.
2. 같은 조건으로 다시 측정해 수치의 변화와 편차, 다른 자원의 비용을 기록합니다. 웹과 게임은 각각 브라우저 지표와 프레임·메모리 등 환경에 맞는 값을 씁니다. [성능 측정 체크리스트](../../../.agent-rules/upstream/references/performance-checklist.md)
