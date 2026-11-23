---
name: code-simplification
description: 동작을 유지하면서 중복·불필요한 분기·따라가기 어려운 추상화를 정리할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/main/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/code-simplification/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 동작을 보존하는 코드 단순화

1. 변경 경계와 호출자가 의존하는 동작을 먼저 고정합니다. 중복 분기, 더 이상 도달하지 않는 경로, 한 번만 쓰는 우회 계층 등 이해 비용을 만드는 부분을 고릅니다.
2. 한 가지 책임씩 정리한 뒤 공개 인터페이스, 예외, 실행 순서와 출력이 보존되는지 비교합니다. 동작이 달라져야 하는 부분은 별도 요구사항으로 표시합니다.
