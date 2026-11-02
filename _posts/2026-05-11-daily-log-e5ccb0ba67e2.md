---
title: "데일리로그260511"
date: 2026-05-11 12:00:00 +0900
categories: ["데일리로그"]
tags: ["Notion 이전", "Unity"]
excerpt: "XR Grab Interactable의 잡기 위치와 양손 잡기를 실습하고, 발사 입력·XR UI·AR Foundation의 기초를 살펴봤다."
description: "XR Grab Interactable의 잡기 위치와 양손 잡기를 실습하고, 발사 입력·XR UI·AR Foundation의 기초를 살펴봤다."
published: true
migration_id: "35e36532580e817183c0e5ccb0ba67e2"
migration_status: "published"
migration_flags: []
---

{% raw %}
## 기본 정보

- 날짜: 2026-05-11
- 주제: Unity XR — Grab(Attach/Dynamic Attach) + 양손 잡기(Select Mode: Multiple) + Activate(발사) + XR UI + AR Foundation 개요
- 작성자: 작성자

## 오늘 한 일(요약)

- <code>XR Grab Interactable</code>의 <b>Attach Transform</b>과 <b>Use Dynamic Attach</b>를 비교하면서 “잡는 위치가 왜 어긋나는지 / 어떻게 자연스럽게 잡히게 하는지”를 실습했다.
- 권총/라이플을 예시로 <b>양손 잡기(Select Mode: Multiple)</b>를 구성하고, Primary/Secondary Attach Transform으로 두 손의 그립 포인트를 분리했다.
- 손 전환(오른손→왼손) 시 위치가 미세하게 틀어지는 문제를 해결하려고 <code>XRGrabInteractableFixed</code>(커스텀)로 <b>왼손/오른손 Attach를 각각 적용</b>하는 구조를 정리했다.
- <code>activated</code> 이벤트에 리스너를 붙여 <b>트리거(Activate) 입력 시 발사 로그/발사 로직</b>을 시작했다.
- 후반에는 <b>VR UI Interaction</b> 기본 세팅(XR UI Input Module + World Space Canvas + Ray Interactor)과, <b>AR/VR/XR 개념 + AR Foundation(ARCore/ARKit)</b> 개요를 훑었다.

## 오늘 진행한 내용(상세)

### 1) Grab: Attach Transform vs Use Dynamic Attach

- Attach Transform
  - “오브젝트를 잡을 때 손이 고정될 기준점”
  - 총 손잡이 위치에 빈 오브젝트(Transform)를 만들어 지정하면, 잡을 때 그 지점으로 정렬된다.
- Use Dynamic Attach
  - “잡는 순간의 손 위치를 기준으로” 자연스럽게 잡히도록 해준다.
  - 실제 VR에서는 거의 바로 체감되는 옵션(PC 키보드 테스트보다 VR에서 장점이 큼).

### 2) 양손 잡기: Select Mode Multiple + Primary/Secondary

- 라이플처럼 양손으로 잡는 오브젝트는 Select Mode를 <b>Multiple</b>로 바꾸고,
- Primary(방아쇠/손잡이)와 Secondary(총구 받침) Attach Transform을 각각 지정해 두 손의 위치를 안정화한다.

### 3) 손 전환 이슈 대응: XRGrabInteractableFixed (커스텀)

- 문제: 한 손으로 잡다가 다른 손으로 옮길 때 <b>잡는 위치가 미세하게 어긋남</b>
- 접근:
  - <code>XRGrabInteractable</code> 상속
  - <code>OnSelectEntered(SelectEnterEventArgs args)</code>에서 interactor의 <code>handedness</code>를 기준으로
  - left/right attach transform을 각각 적용하도록 구성

### 4) Activate(발사) 이벤트 연결

- 핵심: <b>Select = 잡기(Grip)</b>, <b>Activate = 트리거(방아쇠)</b> 로 역할을 분리해서 설계
- <code>Gun</code> 스크립트에서 <code>grabFixed.activated.AddListener(Shoot)</code> 형태로 이벤트 연결
- (주의) <code>Shoot(ActivateEventArgs args)</code>처럼 매개변수가 필요한 형태를 지켜야 오류를 피할 수 있음

### 5) VR UI Interaction + AR 개요(짧게)

- VR UI
  - World Space Canvas + <code>Tracked Device Graphic Raycaster</code>
  - Event System은 일반 UI 모듈 대신 <code>XR UI Input Module</code> 사용
  - Right Hand Ray Interactor로 버튼/드롭다운/입력필드 상호작용 테스트
- AR 개요
  - AR/VR/MR/XR 차이와 현재 시장/활용 분야를 가볍게 정리
  - Unity에서는 AR Foundation(ARCore/ARKit)을 버전 맞춰 세팅하는 게 중요

## 배운 것(개념/정리)

- “잡는 느낌”은 단순히 Grab 컴포넌트만으로 결정되지 않고, <b>Attach 기준(고정 vs 동적) + 손/양손 정책(Multiple) + 이벤트 설계(Select/Activate)</b>가 같이 맞물린 결과다.
- PC에서 어색하던 조작도 VR 기기에서는 Use Dynamic Attach로 크게 자연스러워질 수 있다.
- 손 전환/양손잡기 문제는 “구조적으로” 해결해야 반복되지 않는다(왼손/오른손 attach 분리 같은 방식).

## 이슈/오류 기록

- 손 전환 시 위치가 미세하게 틀어지는 문제 → 커스텀 Interactable로 보정 방향 정리
- <code>AddListener</code> 관련 오류(매개변수 시그니처) → <code>ActivateEventArgs</code> 포함 여부 확인 필요
- 왼손/오른손 구분 방식: string 비교보다 <code>interactor.handedness</code> enum 방식이 더 적절

## 내일(다음) 할 일

- 권총(Gun Pistol) 기준
  - <code>XRGrabInteractableFixed</code> 적용 후 좌/우 손 전환 시 위치가 완전히 고정되는지 확인
  - Activated 이벤트에서 실제 Projectile(구체) 발사: Speed/수명(3초)까지 구현
- 라이플(Gun Rifle) 기준
  - Primary/Secondary Attach 위치값 튜닝 + 두 손 그립 안정화
- VR UI
  - UI Interaction Layer Mask/UI 레이캐스팅 옵션까지 포함해서 “안 되는 상황” 재현 & 해결 루틴 만들기
- AR
  - AR Foundation 튜토리얼(30분) 시청 후 AR Plane 또는 Face 프로젝트 1개 생성

---

## 짧은 버전

오늘은 Unity XR에서 오브젝트 잡기(Grab)를 “어떻게 자연스럽게/안정적으로” 만들지에 집중했다. XR Grab Interactable의 Attach Transform과 Use Dynamic Attach 차이를 실습했고, Select Mode를 Multiple로 바꿔 양손 잡기를 구성했다. 손을 바꿔 잡을 때 위치가 미세하게 어긋나는 문제를 해결하기 위해 XRGrabInteractableFixed 커스텀 스크립트 방향을 정리했고, activated 이벤트로 트리거 입력 시 발사 로직도 시작했다. 마지막으로 VR UI 상호작용 기본 세팅과 AR Foundation 개요까지 훑었다.
{% endraw %}
