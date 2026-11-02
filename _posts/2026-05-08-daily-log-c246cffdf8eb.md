---
title: "데일리 로그 260508"
date: 2026-05-08 12:00:00 +0900
categories: ["데일리로그"]
tags: ["Notion 이전", "Unity"]
excerpt: "Unity XR의 손 모델과 입력 바인딩을 점검하고, 손 애니메이션·이동·회전·텔레포트·등반 기능의 연결을 실습했다."
description: "Unity XR의 손 모델과 입력 바인딩을 점검하고, 손 애니메이션·이동·회전·텔레포트·등반 기능의 연결을 실습했다."
published: true
migration_id: "35e36532580e817f97a2c246cffdf8eb"
migration_status: "published"
migration_flags: []
---

{% raw %}
## 기본 정보

- 날짜: 2026-05-08
- 주제: Unity XR — 손 모델/손 애니메이션(Input System) + Locomotion(Move/Turn/Teleport) + Climb 연결
- 실습 환경: XR Device Simulator(Mock Runtime) 기반 키보드/마우스 테스트
- 작성자: 작성자

## 오늘 한 일(요약)

- Props 씬에서 손(Hand) 프리팹이 플레이어와 분리되어 움직이던 문제를 <b>입력 바인딩/TrackedPoseDriver/XR Device Simulator 조작 방식</b> 관점에서 원인을 나눠 점검하고 연결을 수정했다.
- 손 애니메이션(Grip/Trigger)이 실제 입력값에 반응하도록 <b>Animator + Blend Tree + HandAnimations 스크립트 + InputActionReference</b> 흐름을 정리하고 적용했다.
- DemoScene에서 기존 locomotion 구조 위에 손 비주얼/애니메이션만 얹는 방식으로 <b>Move/Turn/Grab/Teleport/Climb</b> 기능이 유지되도록 구성했다.
- Mesh Collider 관련 경고(Concave Mesh Collider 등)를 확인하며 <b>콜라이더/리짓바디/상호작용 컴포넌트</b>가 XR에서 왜 묶여 돌아가는지 다시 체감했다.

## 오늘 진행한 내용(상세)

### 1) Props 씬: 손이 플레이어와 분리되어 움직이던 문제 해결

- 현상: 플레이 시 손이 플레이어 리그와 분리되어 떠다니거나, 원하는 트래킹 기준을 따르지 않음
- 점검 포인트
  - Input Action 바인딩이 실제로 어떤 디바이스/모드(Mock Runtime)에서 값을 내는지
  - TrackedPoseDriver(또는 유사 트래킹 컴포넌트) / XR Origin 하위 구조가 정상인지
  - XR Device Simulator의 HMD/Controller/Hand 모드 차이와 조작 키(T/Y/WASD/QE 등) 역할
- 조치: “손 프리팹이 플레이어 기준으로 따라오도록” 리그 연결을 다시 확인하고 수정

### 2) 손 애니메이션: Grip/Trigger 입력 → Blend Tree 파라미터 연동

- 핵심 흐름
  - Animator Controller 구성 → Float 파라미터(Grip/Pinch 또는 Grip/Trigger) 준비
  - Blend Tree(2D)로 손 모양을 입력값에 따라 자연스럽게 전환
  - <code>HandAnimations</code> 스크립트에서 <code>InputActionReference</code>로 값을 읽어 Animator에 전달
- 정리한 개념
  - <b>Grip vs Trigger(Pinch)</b>: 둘 다 손 모양 입력이지만, Blend Tree 축 매핑/용도가 달라 헷갈리기 쉬움
  - <b>Select vs Activate</b>: “잡기(Select)”와 “추가 동작(Activate)”을 분리해서 설계하는 개념(예: 잡고 발사)
- 적용/확인
  - 입력값이 실제로 0\~1로 들어오고, 손 모양이 그에 맞춰 변하는지 플레이 모드에서 확인

### 3) DemoScene 통합: Move/Turn/Grab/Teleport/Climb 유지

- 접근 방식
  - 샘플 XR Rig를 통째로 교체하기보다, 이미 구성된 locomotion 구조를 유지한 채 손 비주얼/애니메이션을 덧씌우는 방식이 안전함
- 확인한 것
  - Teleport가 먼저 정상 동작하는지 확인 → 이후 ClimbProvider/LocomotionMediator/ClimbTeleportInteractor/Climb Interactable 연결 점검
  - 최종적으로 climb 동작까지 완료

## 배운 것(개념/정리)

- XR 프로젝트는 “기능 추가”보다 <b>입력(Input System) ↔ 리그(XR Origin) ↔ 콜라이더/리짓바디 ↔ 상호작용(XRI 컴포넌트)</b> 연결 관계를 이해하는 게 핵심이다.
- 문제를 하나로 보지 않고 “입력/트래킹/리그/상호작용”으로 <b>분해해서 원인 좁히기</b>가 잘 먹혔다.
- 버전/프리셋(XRI 3.0 등) 변화로 자동/수동 설정 방식이 달라질 수 있어, “어디가 자동이고 어디가 수동인지”를 체크하는 습관이 필요하다.

## 이슈/경고 기록

- Concave Mesh Collider 관련 경고 확인
- 다음에 체크할 것: 동적 오브젝트에서 Collider 설정(Convex 여부), Rigidbody 유무, Interaction Layer Mask 분리

## 내일(다음) 할 일

- 양손 상호작용(Secondary Attach 포함) 케이스로 확장
- 손 위치 보정(그립 위치/Attach Transform)과 애니메이션 파라미터 네이밍(Grip/Pinch/Trigger) 정리
- Climb 중 이동 제한/안정화 같은 “세부 동작” 다듬기

---

## 짧은 버전

Unity XR 실습에서 Props 씬과 DemoScene을 중심으로 손 모델, 손 애니메이션, 입력 연결, 텔레포트, 클라임 기능을 점검하고 완성했다. 손이 플레이어와 분리되어 움직이던 문제를 해결하면서 Mock Runtime과 XR Device Simulator 조작 방식을 이해했고, Animator/Blend Tree/HandAnimations로 손 모양이 입력값에 따라 반응하도록 설정했다. 마지막으로 DemoScene에서 Move/Turn/Grab/Teleport에 이어 Climb까지 연결해 XR 상호작용 구조를 전체적으로 정리했다.
{% endraw %}
