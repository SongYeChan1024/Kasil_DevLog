---
name: ci-cd-and-automation
description: CI나 배포 파이프라인을 추가·변경하고 실패 신호를 검증할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/ci-cd-and-automation/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 빌드·검사 자동화

1. 현재 트리거·권한·종속성·산출물을 확인합니다. 반복 가능한 환경에서 빠른 검사부터 배치하고, 실제 배포는 기존 환경과 승인 조건에 연결합니다.
2. 정상 변경이 통과하고 대표 실패가 해당 단계에서 중단되는지 확인합니다. 로그에 원인이 남는지, 실패로 불완전한 산출물이 게시되는 일이 없는지 점검합니다.
