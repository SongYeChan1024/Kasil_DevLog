---
name: browser-testing-with-devtools
description: 브라우저 화면의 입력·렌더링·네트워크 문제를 실제 페이지에서 확인할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/browser-testing-with-devtools/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 브라우저에서 실제 동작 검증

1. 브라우저 종류·화면 크기·초기 상태와 재현 입력을 기록합니다. 화면 증상에 맞춰 DOM, 콘솔, 요청 결과, 타이밍 중 필요한 근거만 확인합니다.
2. 실제 클릭·키 입력과 기대 결과를 비교하고, 새로고침 또는 재진입이 관련되면 다시 확인합니다. 캡처에는 민감한 입력을 남기지 않으며, 브라우저를 실행하지 못한 경우 정적 검사 범위를 표시합니다.
