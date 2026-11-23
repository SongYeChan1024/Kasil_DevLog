---
name: git-workflow-and-versioning
description: 변경을 커밋 단위로 나누거나 브랜치·worktree·릴리스 버전을 다룰 때 사용합니다.
---

<!-- Generated from RULES.md; 직접 편집하지 않습니다. -->
<!-- Source SHA256: 3920ad73435d4a2ef7ec10524f66d5879fbea7a19a2f8cd288df9084c9b93c8a -->
편집 원본: [통합 규칙](https://github.com/SongYeChan1024/Kasil_DevLog/blob/main/tools/agent-rules/RULES.md). [원본 절차](https://github.com/addyosmani/agent-skills/blob/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee/skills/git-workflow-and-versioning/SKILL.md) · [출처·라이선스](../../../.agent-rules/THIRD_PARTY_NOTICES.md).

# Git 변경과 버전 관리

1. 저장소, 현재 브랜치, 추적 대상과 worktree를 확인합니다. 작업 전부터 있던 변경과 이번 변경을 구분하고 커밋할 경로만 선택합니다.
2. 스테이징된 diff와 검증 결과를 확인하고 해당 프로젝트의 형식으로 기록합니다. 브랜치 운용과 원격 반영은 프로젝트 정책과 사용자가 지정한 대상·범위를 따릅니다.
