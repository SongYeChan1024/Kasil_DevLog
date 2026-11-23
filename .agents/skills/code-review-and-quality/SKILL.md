---
name: code-review-and-quality
description: 변경 diff에서 오류·회귀·검증 누락을 찾아 달라는 요청에 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/code-review-and-quality/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 변경 검토

1. 변경 의도와 수용 기준, 이를 검사하는 테스트를 먼저 읽습니다. 변경된 코드와 호출자를 따라 정확성, 가독성, 구조, 보안, 성능상의 영향을 확인합니다.
2. 발견 사항마다 위치, 어떤 입력에서 문제가 되는지, 사용자 영향과 확인 방법을 제시합니다. 검증된 결함과 설계 제안을 구분하고, 실행하지 않은 검사는 기록합니다.
