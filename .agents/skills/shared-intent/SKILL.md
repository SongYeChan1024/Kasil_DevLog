---
name: shared-intent
description: Clarify a materially ambiguous request or an explicit request to interview the user about intent. Establish outcome, audience, success and constraints before design; skip clear edits and information questions.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 의도 확인

작성자: 송예찬

현재 요청과 저장소의 AGENTS.md·관련 명세를 먼저 읽습니다. 이 절차는 사용자가 이루려는 결과를 구체화하며, 작업 범위나 승인 조건을 늘리지 않습니다.

1. 사용자의 말과 문서에서 이미 확인할 수 있는 목적·사용 대상·완료 조건·제약을 정리합니다. 정보가 충분하면 인터뷰를 시작하지 않고 요청한 작업을 진행합니다.
2. 결과·설계·비용·범위를 크게 바꾸는 빈칸만 질문합니다. 질문에는 현재 이해한 내용과 추천안 또는 선택지의 차이를 짧게 붙입니다. 사소한 구현 선택은 합리적인 가정을 밝히고 진행합니다.
3. 앞 답변에 의존하는 질문은 하나씩 하고, 독립적인 짧은 확인은 묶을 수 있습니다. 추측을 사실로 말하거나 사용자에게 동의를 유도하려고 일부러 틀린 가설을 제시하지 않습니다.
4. 목적, 사용 대상, 관찰 가능한 완료 조건, 제약, 이번 범위, 남은 미정 사항을 필요에 맞게 짧게 정리합니다. 확인된 사실과 작업상 가정을 구분합니다. 임의의 확신 백분율이나 고정 질문 횟수를 완료 조건으로 쓰지 않습니다. 질문이 반복되어 진전이 없으면 핵심 쟁점과 선택의 영향을 설명합니다.
5. “좋아, 진행해”와 명확한 판단 위임은 문맥의 범위 안에서 유효합니다. 이미 확인한 내용을 다시 승인받지 않습니다. 의도 정리만 요청받았다면 정리 결과를 전달합니다. 구현까지 요청받았으면 확인 후 같은 작업에서 계속 진행합니다. 핵심 답변이 필요하면 그 답에 의존하지 않는 일부터 진행하며, 응답이 없다는 사실을 승인으로 간주하지 않습니다.

예: “인벤토리를 만들어줘”에는 기존 기획서를 먼저 확인하고, 구현을 바꾸는 저장 범위나 슬롯 방식이 미정일 때만 질문합니다. “기획서대로 인벤토리 정렬 버그를 고쳐줘”에는 재현·수정·검증으로 바로 이어갑니다.
