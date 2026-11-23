---
name: accessibility-engineering
description: 기존 화면의 키보드 사용, 읽기 순서, 보조기술 호환성 등을 점검하거나 고칠 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/accessibility-engineering/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 접근성 점검과 보수

1. 사용자가 완료해야 할 핵심 동작을 골라 키보드만으로 이동·입력·종료해 봅니다. 포커스 순서와 복귀, 컨트롤 이름, 오류 안내, 상태 변화를 읽을 수 있는지 확인합니다.
2. 자동 검사 결과와 직접 확인한 결과를 구분하고, 작업을 막는 항목부터 수정합니다. 같은 경로로 재검사해 영향과 미검증 환경을 기록합니다. [접근성 체크리스트](../../../.agent-rules/upstream/references/accessibility-checklist.md)
