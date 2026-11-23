---
name: shared-spec-plan
description: Turn a substantial feature, design change or explicit planning request into scoped acceptance criteria and verifiable tasks using existing project documents. Preserve authorization to continue implementation and skip ceremony for small clear fixes.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/chore/shared-agent-rules-20261120/tools/agent-rules/RULES.md). [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# 명세와 작업 계획

작성자: 송예찬

현재 요청, 적용되는 AGENTS.md, 현행 명세·인수인계를 읽습니다. 프로젝트에 이미 있는 기획서·작업 카드·명세의 위치를 유지합니다. 팀 계약·기획 수치와 개인 작업 규칙은 각자의 원본에서 관리합니다.

1. 기존 명세에서 이번 변경의 목적·입출력·성공 조건과 빠진 결정을 확인합니다. 명세 검토만 요청했으면 구현하지 않습니다. 구현 요청에 명세 보완이 필요하면 그 범위에서 함께 처리합니다.
2. 큰 변경은 목표, 이번 범위, 영향받는 상태·데이터·인터페이스, 관찰 가능한 완료 조건, 검증 방법을 현행 문서에 적습니다. 기존 문서와 중복되는 SPEC.md를 만들지 않습니다. 원본이 없고 여러 세션에 걸친 작업이면 해당 프로젝트의 문서 관례에 맞춰 한 곳을 정합니다.
3. 독립적으로 확인할 수 있는 기능이 여럿이면 책임과 의존 관계를 먼저 나눕니다. 한 기능의 작은 수정에 기능 지도나 별도 계획 문서를 강제하지 않습니다. 팀의 미정 기획과 개인 구현 선택을 구분합니다.
4. 각 작업은 하나의 확인 가능한 결과를 갖게 합니다. 필요한 경우 아래 표를 사용하며, 작업 크기를 임의의 줄 수로 제한하거나 작업마다 커밋·승인을 의무화하지 않습니다.

| 작업 | 완료 조건 | 검증 방법 | 선행 조건·영향 범위 |
| --- | --- | --- | --- |
| 이번에 만들거나 고칠 동작 | 사용자가 확인할 수 있는 결과 | 실제 명령 또는 수동 확인 절차 | 의존 작업과 변경할 책임 |

5. 구현까지 허용되고 중요한 미정 사항이 해결되었으면 계획에서 구현·검증으로 이어갑니다. 명세 작성 후 또는 사용자 확인 후라는 이유만으로 턴을 강제 종료하지 않습니다. 비용·외부 반영·범위 확대처럼 별도 승인이 필요한 단계는 기존 규칙을 적용합니다.
6. 구현 중 결정이나 범위가 바뀌면 근거와 명세·검증을 함께 맞춥니다. 제안·합의·구현·검증 완료를 구분하고, 다음 세션에 필요한 결정과 미완료 항목만 지정된 인수인계 문서에 남깁니다.

Unity에서는 기존 의사코드·상태 소유·씬/프리팹 인계 방침을 유지합니다. After Seconds의 사용자 주도 학습, DOB의 팀 기획·역할 브랜치, ERGO의 기존 명세 체계를 이 절차로 대체하지 않습니다.
