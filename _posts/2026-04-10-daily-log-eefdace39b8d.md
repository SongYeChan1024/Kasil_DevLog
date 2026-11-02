---
title: "일일 회고록 2026-04-10"
date: 2026-04-10 12:00:00 +0900
categories: ["데일리로그"]
tags: ["Notion 이전", "Unity"]
excerpt: "로비 인트로 컷씬의 자막을 기존 캔버스에 연결하고 독백과 NPC 상호작용 대사를 분리했다."
description: "로비 인트로 컷씬의 자막을 기존 캔버스에 연결하고 독백과 NPC 상호작용 대사를 분리했다."
published: true
migration_id: "35e36532580e819d9fa9eefdace39b8d"
migration_status: "published"
migration_flags: []
---

{% raw %}
## 기본 정보

- 날짜: 2026-04-10
- 프로젝트: MosAIc / EP.3
- 작성자: 작성자

## 오늘 한 일(요약)

- EP3 로비 인트로 컷씬 자막 구조를 기존 <code>Canvas_Cutscene</code>에 붙는 형태로 정리
- 컷씬 대사 구성 정리(나레이션/독백 중심) + 음악가 대사는 상호작용 이후로 분리
- 백업 프로젝트 파일 이관/중복 폴더 정리 + 상호작용 UI 연결/비주얼 방향 구상

## 구현한 것

- <code>Ep3LobbyIntroCutsceneController.cs</code>에서 씬 내 <code>CutsceneManager</code>를 찾아 기존 캔버스 아래로 자막 연결
- <code>Ep3CutsceneSubtitlePresenter.cs</code>를 “임시 오버레이 캔버스 생성” 대신 기존 <code>system / player / voice</code> 박스 우선 사용하도록 정리
  - 하이라키 이름이 <code>Canvas_Cutscene</code>(또는 예전 이름) 모두 대응하도록 범위 확장
- <code>subtitleObject</code> 지역 변수 중복으로 발생한 <code>CS0136</code> 에러 해결(폴백 변수명 분리)
- EP3 로비 인트로 컷씬 대사/데이터 통일
  - 5줄 구조의 <code>Narration / Monologue</code> 중심으로 재정리
  - <code>Episode3_Scene.unity</code>, <code>EP3LobbyIntroSequence.asset</code>, <code>ep3_lobby_intro_cutscene.json</code>에 동일 내용 반영

## 배운 것(개념/정리)

- 컷씬/자막/UI는 <b>씬-프리팹-스크립트-데이터-인스펙터 참조</b>가 얽혀 있어서, “텍스트만 수정”이 아니라 출력 박스/캔버스 구조까지 함께 맞춰야 연출이 안정적으로 나온다.
- 예전 프로젝트 파일 이관 시에는 단순 복사보다 <b>폴더 중첩/중복 컴파일</b> 여부를 먼저 점검해야 한다.
  - <code>Assets/Assets 1/...</code>처럼 경로가 겹치면 동일 스크립트가 중복 정의로 컴파일 에러가 대량 발생할 수 있다.

## 이슈/버그

- 내용: <code>subtitleObject</code> 지역 변수 이름 충돌로 <code>CS0136</code> 에러 발생
- 원인/가설: 동일 스코프에서 같은 이름의 지역 변수가 중복 선언됨
- 해결/시도: 폴백용 변수명을 별도로 분리해 충돌 제거
- 다음 액션: 이후에도 컷씬/자막 관련 수정 시, 임시 변수/폴백 로직 이름 충돌 여부 먼저 확인

## 내일 할 일

- EP3 로비 컷씬 플레이 테스트
  - 자막이 <code>system / player / voice</code> 박스에 의도대로 출력되는지
  - 음악가 대사가 컷씬과 분리되어 상호작용 후 시작되는지
- 프로젝트 이관/정리 후 Unity 리임포트 및 콘솔 에러 재확인
- 심볼 상호작용 UI 작업 이어서
  - 인스펙터 연결 + <code>OnTriggerEnter/Exit</code> 활성화 흐름 실제 적용
  - EP3 분위기에 맞는 상호작용 이미지 스프라이트 적용(Assets에 추가 → Sprite 설정 → Image 컴포넌트 연결 → Rect Transform 조정)

## 참고 링크/자료

- 정리/이관 포인트
  - 중복 폴더 격리: <code>01.Scenes/01.Scenes</code>, <code>02.Scripts/02.Scripts</code>, <code>07.Prefabs/07.Prefabs</code>
  - 씬 데이터 폴더 구분: <code>Ep3_1_Scene_Data</code>, <code>Episode3_Scene_Data</code>

<details markdown="1">
<summary>첨부/스크린샷(선택)</summary>

<ul>
<li></li>
</ul>

</details>

<details markdown="1">
<summary>회고(선택)</summary>

- 잘한 점: 연출/데이터/프로젝트 구조를 한 번에 정리해서, 컷씬과 상호작용 흐름을 분리하는 기준을 세움
- 아쉬운 점: 최종 동작(자막 출력/리임포트/상호작용 UI)까지는 플레이 테스트로 완전 검증을 못함
- 내일 개선: 먼저 “동작 검증”을 끝내고(플레이 테스트/콘솔 확인), 그 다음에 비주얼/UI 다듬기 진행

</details>
{% endraw %}
