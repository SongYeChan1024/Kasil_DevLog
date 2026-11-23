---
name: interview-me
description: Interview me, grill me, 인터뷰 미, 의도부터 물어봐 달라는 요청이나 대상·성공 조건이 불분명해 결과가 크게 달라질 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/interview-me/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# Interview Me · 요구 의도 확인

1. 이 프로젝트의 `shared-intent` 절차를 적용합니다. 사용자의 말과 기존 문서에서 확인한 결과를 한 문장으로 돌려주고, 아직 추측인 부분을 표시합니다.
2. 명시적으로 인터뷰를 요청하면 한 번에 한 질문만 합니다. 현재의 예상 답과 그렇게 본 이유를 붙이고, 사용자의 답에 따라 다음 질문을 고릅니다. 예를 들어 “인벤토리를 편하게 해줘”라면 아이템을 찾는 시간과 꺼내는 동작 중 어느 쪽이 불편한지 먼저 묻습니다.
3. 답을 사용자 표현으로 정리합니다. 결과물, 사용자, 지금 필요한 이유, 성공 기준, 제약, 이번 범위 밖의 일을 짚고 정정을 반영합니다. 인터뷰만 요청한 경우 확인된 의도를 전달합니다. 이미 합의한 구현까지 요청한 경우 그 범위에서 이어갑니다.
4. 검수 예시에서 모호한 관리자 페이지 요청과 테스트 실행 요청의 차이를 확인할 수 있습니다. [Interview Me 호출·대화 평가 사례](../../../.agent-rules/upstream/evals/cases/interview-me.json)
