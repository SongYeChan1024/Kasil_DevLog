---
name: source-driven-development
description: 라이브러리·엔진·API의 정확한 동작이나 버전별 지원 여부가 구현을 좌우할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/source-driven-development/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 버전에 맞는 기술 근거 확인

1. 잠금 파일·프로젝트 설정에서 실제 버전과 실행 환경을 먼저 확인합니다. 같은 버전의 공식 문서, 변경 기록, 배포된 소스 순으로 해당 옵션이나 호출의 근거를 찾습니다.
2. 가능하면 최소 예제로 이 환경에서의 동작을 확인합니다. 답에는 근거 링크나 소스 위치, 검증한 버전과 실행 결과, 아직 추론인 부분을 구분합니다.
