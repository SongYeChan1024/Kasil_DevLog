---
name: idea-refine
description: 해결할 문제는 알지만 구현 방향이나 첫 버전을 정해야 할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/main/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/idea-refine/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 아이디어 구체화

1. 누가 어떤 상황에서 무엇을 하려는지와 가장 큰 제약을 한 문장씩 적습니다. 같은 아이디어를 표현만 바꿔 반복하지 않도록 동작 방식이 다른 후보를 만듭니다.
2. 후보별로 가치, 구현 비용, 틀릴 수 있는 가정, 가장 작은 검증 방법을 비교합니다. 제약을 충족하는 첫 버전과 보류한 기능, 다음에 판단할 질문을 남깁니다. 사용자가 선택하지 않은 안은 제안 상태로 표시합니다.
