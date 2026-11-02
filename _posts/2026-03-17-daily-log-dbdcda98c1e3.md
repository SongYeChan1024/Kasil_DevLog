---
title: "26-03-17_일일 회고록"
date: 2026-03-17 12:00:00 +0900
categories: ["데일리로그"]
tags: ["Notion 이전", "Unity"]
excerpt: "스토리와 게임 진행 방식을 논의하고 에피소드 3의 환경·악기·퍼즐용 에셋 후보를 정리했다."
description: "스토리와 게임 진행 방식을 논의하고 에피소드 3의 환경·악기·퍼즐용 에셋 후보를 정리했다."
published: true
migration_id: "35e36532580e81c09c0cdbdcda98c1e3"
migration_status: "published"
migration_flags: []
---

{% raw %}
<h3 color="purple_bg">
Scrum
</h3>

스토리라인 작성, 게임 진행 방식 구성 필요

캐릭터 및 맵에 사용할 에셋 탐색 및 선정

---

![첨부 자료](/assets/img/uploads/notion/ff2a2382357eca751e8b8734a0333326628cb82cdd5360412195b3d7aa2fb657.png)

<h3 color="purple_bg">
Project
</h3>

---

#### 오늘 진행한 작업

- GitHub 및 리포지토리 생성
- 스테이지 3에 사용할 에셋 일부 선정
- 이젤과 캐릭터 에셋 구성 완료

#### 진행 중인 작업

- 스테이지별 에셋 일부 선정 아직 완료가 덜 되어서 더 찾아볼 예정
- 현재 캐릭터들의 디자인과 에셋구성은 완료 하였음

#### 내일 개발 계획 및 목표

- NPC AI 연동 및 애니메이션 구현
- 스테이지별 레벨디자인 착수
- 로비 구성 및 UI 디자인

<h3 color="purple_bg">
Trouble Shooting
</h3>

---

1. 문제 상황 파악

- 맵에 필요한 에셋이 잘 찾아지지 않아 계속 찾아볼 예정

1. 문제 발생 조건 파악
2. 결과 검증, 해결

## 그 외 과제 제출 (선택기입)

<h3 color="purple_bg">
Github / Blog
</h3>

<i>\\</i>별도로 회고를 정리하는 깃헙, 블로그 게시글 링크가 있다면 첨부해주세요.\*

---

- Github: [https://github.com/WooSeonghyeok/Moumi\_moz.A.I.c\_Documents#](https://github.com/WooSeonghyeok/Moumi_moz.A.I.c_Documents#)
- Blog:
- Velog:

<h3 color="purple_bg">
기술탐구
</h3>

<i>\\</i>프로젝트 작업을 위해 추가로 학습한 게시글이 있다면 링크를 첨부해주세요\*

---

- (예시) 부트스트랩 설치방법: [https://datamoney.tistory.com/149](https://datamoney.tistory.com/149)
- 링크 1:
- 링크 2:

Episode 3 - 멈춰버린 노래

1. 맵 환경
2. 멜로디 오브젝트
3. 배경 장식
4. 퍼즐 오브젝트 - 음표 배열, 리듬 퍼즐, 순서 기억 퍼즐
5. NPC 관련
6. 스토리 오브젝트

[https://assetstore.unity.com/packages/vfx/particles/polygonal-s-low-poly-particle-pack-118355#content](https://assetstore.unity.com/packages/vfx/particles/polygonal-s-low-poly-particle-pack-118355#content) - 파티클 팩

[https://assetstore.unity.com/packages/audio/music/bard-s-tales-peaceful-harp-music-pack-lite-lite-190602](https://assetstore.unity.com/packages/audio/music/bard-s-tales-peaceful-harp-music-pack-lite-lite-190602) -BGM

## 1. 맵 환경 에셋 (Environment)

- 몽환적인 음악 공간 (기본 맵)
- 공중에 떠 있는 플랫폼 - [https://assetstore.unity.com/packages/3d/environments/landscapes/cross-plains-lowpoly-environment-by-unvik-3d-203644#content](https://assetstore.unity.com/packages/3d/environments/landscapes/cross-plains-lowpoly-environment-by-unvik-3d-203644#content)
- [https://assetstore.unity.com/packages/3d/environments/3d-ground-platforms-platform-terrain-set-floating-islandas-258146](https://assetstore.unity.com/packages/3d/environments/3d-ground-platforms-platform-terrain-set-floating-islandas-258146)
- 음악 파동 형태의 지형 (웨이브 느낌)
- 안개 / 볼륨 라이트 (기억 느낌)
- 공간 왜곡 효과 (흐릿한 경계)
- 빛나는 길 (플레이어 유도)
- 부서진 악보가 흩어진 바닥
- 잔향이 퍼지는 바닥 이펙트-[https://assetstore.unity.com/packages/vfx/particles/spells/magic-effects-free-247933](https://assetstore.unity.com/packages/vfx/particles/spells/magic-effects-free-247933)
- 배경용 거대한 음표 구조물

---

## 2. 작업실 오브젝트 (Art Studio Props)

👉 음악가의 공간 느낌

- 낡은 피아노 (핵심 오브젝트)
- 오르골
- 악보 스탠드
- 흩어진 악보 종이
- 바이올린 / 기타 (장식 + 인터랙션 가능)
- 의자 / 작업용 테이블
- 잉크병 / 펜
- 음악가의 노트 (스토리 단서)

---

## 3. 배경 장식 오브젝트 (Decoration)

- 떠다니는 작은 음표 파티클
- 빛나는 먼지 (sparkle)
- 공중에 떠 있는 기억 조각 (빛나는 큐브/구체)
- 흐르는 음악 라인 (라인 이펙트)
- 색이 변하는 빛 기둥
- 잔상 효과 (이전 기억 흔적)
- 공간에 떠다니는 작은 종이 조각

## 4. 퍼즐 오브젝트 (Puzzle Objects)

---

### 🎼 음표 배열 퍼즐

- 음표 블록 (Do, Re, Mi 형태 구분 가능) [https://assetstore.unity.com/packages/2d/gui/icons/puzzle-blocks-icon-pack-278862](https://assetstore.unity.com/packages/2d/gui/icons/puzzle-blocks-icon-pack-278862)
- 음표 슬롯 (배치 위치)
- 정답 라인 UI (가이드)
- 음표 선택 하이라이트 이펙트
- 성공 시 빛나는 효과

---

### 🥁 리듬 퍼즐

- 타이밍 바 UI
- 박자 타격 포인트 (히트 존)
- 리듬 타일 (밟거나 누르는 오브젝트)
- 입력 피드백 이펙트 (성공/실패)
- 리듬 파티클 (음파 형태)

---

### 🧠 순서 기억 퍼즐

- 빛나는 패널 (눌리는 버튼)
- 순서 표시 애니메이션
- 기억 재생 효과 (빛이 흐르는 연출)
- 선택 상태 표시 이펙트
- 실패 시 초기화 효과

---

## 5. NPC 관련 오브젝트

- 음악가 NPC (핵심 캐릭터)
- NPC 주변 오라 효과 (슬픔 / 공허 느낌)
- NPC 주변 깨진 음표
- NPC 기억 조각 (상호작용 가능)
- 대화 시작 트리거 오브젝트
- 감정 변화 연출 (노래 완성 전/후)

---

## 6. 스토리 상호작용 오브젝트

- 멜로디 조각 (수집 아이템 ⭐ 핵심)
- 기억 회상 오브젝트 (빛나는 구체)
- 악보 조각 (스토리 텍스트 포함)
- 특정 위치 트리거 존
- 상호작용 시 재생되는 사운드 오브젝트
- 스토리 진행 UI 트리거

---

## 7. 스테이지 목표 오브젝트 (Final Goal)

- 완성된 악보
- 되찾은 기억을 연출할 오브젝트
- 노래 완성과 동시에 NPC 주위에 음표가 떠다니게 연출할 오브젝트
- 빛이 퍼지는 중앙 오브젝트 (엔딩 포인트)
- 음악 파동이 퍼지는 환경 이펙트
- 배경 색 변화 시스템 (어두움 → 밝음)
- NPC 애니메이션 변화 (슬픔 → 안정)
{% endraw %}
