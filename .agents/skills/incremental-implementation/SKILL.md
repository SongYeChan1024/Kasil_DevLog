---
name: incremental-implementation
description: 여러 계층을 연결하는 변경을 실제로 검증 가능한 단위로 진행할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/main/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/incremental-implementation/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 작게 구현하고 확인하기

1. 첫 단위는 사용자가 쓰는 진입점에서 결과까지 이어지는 가장 작은 동작으로 정합니다. 예를 들어 저장 기능이면 화면에서 입력한 한 항목이 저장되고 다시 열리는 경로를 먼저 연결합니다.
2. 각 단위에서 기존 호출자와 저장 데이터의 호환성을 확인합니다. 실패 시 되돌릴 수 있는 경계를 두고, 검증된 동작과 남은 작업을 기준으로 다음 단위로 넘어갑니다.
