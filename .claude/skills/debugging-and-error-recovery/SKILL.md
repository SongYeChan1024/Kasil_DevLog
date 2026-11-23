---
name: debugging-and-error-recovery
description: 재현되는 실패, 간헐 오류 또는 부분 실패 뒤의 복구 동작을 조사할 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: efee7b4bd3ed234c9f2727b2e365c29bb949f7eaac82ca6b4cba3ec9b57ce886 -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/debugging-and-error-recovery/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 오류 원인 좁히기

1. 기대 결과, 최초 실패, 최소 입력과 환경을 기록합니다. 정상 사례와 처음 갈라지는 지점을 찾아 한 번에 하나의 가정을 바꿉니다.
2. 원인과 증상을 구분해 수정하고 같은 재현 절차로 확인합니다. 저장·전환 실패라면 남은 상태, 재시도와 중복 실행까지 확인해 결과를 남깁니다.
