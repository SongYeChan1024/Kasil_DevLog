---
name: security-and-hardening
description: 인증·권한·입력·데이터 저장·의존성 변경에 대한 방어적 보안 검토에 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/main/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/security-and-hardening/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 보호해야 할 경계 검토

1. 보호할 데이터와 신뢰 경계를 표시하고 각 진입점에서 입력 검증과 접근 판정이 어디서 이루어지는지 확인합니다. 민감정보가 오류·로그·클라이언트 응답에 노출되는지도 살핍니다.
2. 필요한 최소 권한과 안전한 기본값을 적용합니다. 소유자·권한이 다른 정상 테스트 계정과 가상 데이터로 허용·거부 결과를 확인하고 수정 위치와 남은 위험을 기록합니다. [방어 점검표](../../../.agent-rules/upstream/references/security-checklist.md)
