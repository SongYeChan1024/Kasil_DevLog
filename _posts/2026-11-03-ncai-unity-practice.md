---
title: "261103_NCAI_Unity_실습"
date: 2026-11-03 10:07:00 +0900
categories: [데일리로그, Unity]
tags: [Unity, CSharp, Invector, 로코모션, Rigidbody, Animator, 점프]
pin: false
toc: true
---

오늘은 Unity 실습에서 Invector 캐릭터 컨트롤러의 스크립트 구성을 살펴봤다. 캐릭터를 움직이다가 점프한 뒤에도 공중에서 방향을 바꿀 수 있다는 점이 눈에 들어왔다. 어떻게 이동시키고 있길래 가능한지 궁금해서 입력부터 Rigidbody, Animator까지 이어지는 흐름을 따라가 봤다.

이번 기록은 실습 프로젝트에 들어 있는 코드와 `Invector_Basic` 씬의 `Rigged_Dummy` 설정을 기준으로 한다. Invector의 모든 버전이나 다른 컨트롤러에도 똑같이 적용되는 설명은 아니다.

## 로코모션을 구성하는 스크립트

로코모션은 캐릭터의 걷기·달리기·방향 전환처럼 이동에 필요한 동작을 다루는 부분이다. 이 프로젝트에서는 실제 위치를 움직이는 코드와 화면에 보여 줄 애니메이션을 함께 살펴봐야 했다.

| 스크립트 | 맡은 역할 |
| --- | --- |
| `vThirdPersonInput` | 이동·카메라·점프·스트레이프·전력질주 입력을 받고 업데이트 함수를 호출한다. |
| `vThirdPersonController` | 카메라 기준 이동 방향, 자유 이동·스트레이프 모드, 회전 방향과 점프 시작을 결정한다. |
| `vThirdPersonMotor` | Rigidbody 속도, 접지·경사 판정, 점프·중력·공중 이동을 처리한다. |
| `vThirdPersonAnimator` | 이동과 접지 상태를 Animator 파라미터에 전달한다. |

상속 관계는 다음과 같다.

```text
MonoBehaviour
└─ vThirdPersonMotor
   └─ vThirdPersonAnimator
      └─ vThirdPersonController

vThirdPersonInput → vThirdPersonController 호출
```

역할별로 파일은 나뉘어 있지만 Controller가 Animator와 Motor를 상속한다. Input은 별도 컴포넌트로 같은 캐릭터의 Controller를 찾아 사용한다.

## 입력부터 이동까지의 흐름

`vThirdPersonInput.Update()`에서는 입력을 읽고 Animator를 갱신한다. `FixedUpdate()`에서는 다음 순서로 이동과 회전을 처리한다.

```text
Update
  입력 읽기
  카메라 기준 이동 방향 갱신
  Animator 파라미터 갱신

FixedUpdate
  UpdateMotor: 접지·경사·점프·공중 조작
  ControlLocomotionType: 이동 모드와 속도 결정, 지상 이동
  ControlRotationType: 캐릭터 회전
```

WASD나 패드 입력은 `input`에 들어간다. 이 입력을 보간한 `inputSmooth`와 카메라의 오른쪽·앞쪽 방향을 조합해서 `moveDirection`을 만든다. 현재 설정은 `rotateByWorld=false`라서 카메라가 보는 방향을 기준으로 이동 방향을 계산한다.

즉 W는 항상 월드의 같은 방향을 의미하는 것이 아니라, 카메라 기준 앞쪽으로 이동하라는 입력이다.

## 지상 이동은 Rigidbody의 속도를 바꾼다

현재 컨트롤러의 `useRootMotion`은 `false`다. 지상 이동을 담당하는 `MoveCharacter()`에서는 목표 위치를 구하고, 그 위치로 가기 위한 속도를 계산해 Rigidbody에 넣는다.

원리를 정리하면 다음과 같다. 아래 코드는 흐름을 이해하기 위한 축약 예시다.

```csharp
Vector3 targetPosition = rigidbody.position
    + moveDirection * moveSpeed * deltaTime;

Vector3 targetVelocity = (targetPosition - transform.position) / deltaTime;
targetVelocity.y = rigidbody.linearVelocity.y;

rigidbody.linearVelocity = targetVelocity;
```

수평 이동은 코드가 제어하고 기존 수직 속도는 유지한다. 충돌과 중력에는 Rigidbody와 CapsuleCollider를 사용한다. `MoveCharacter()`는 공중이거나 점프 중이면 지상 속도 적용을 중단하고, 공중 처리는 별도의 `AirControl()`에 맡긴다.

현재 자유 이동과 스트레이프의 속도 설정은 같다.

| 설정 | 값 |
| --- | ---: |
| 걷기 `walkSpeed` | 2 |
| 달리기 `runningSpeed` | 4 |
| 전력질주 `sprintSpeed` | 6 |
| 입력·속도 보간 `movementSmooth` | 6 |
| 회전 속도 `rotationSpeed` | 16 |
| 애니메이션 보간 `animationSmooth` | 0.2 |

`walkByDefault=false`이므로 현재 기본 이동의 목표 속도는 달리기 값인 4다. 전력질주 상태에서는 6을 사용한다. 이동 속도와 입력을 보간하기 때문에 누르자마자 모든 값이 즉시 최댓값으로 바뀌는 것은 아니다. 이 값들은 설정값이며 실제 주행 속도를 별도로 측정한 결과는 아니다.

## 자유 이동과 스트레이프의 차이

현재 모드는 `FreeWithStrafe`이고 Tab 입력으로 `isStrafing`을 전환한다.

**자유 이동에서는 이동하려는 방향으로 몸을 돌린다.** 왼쪽으로 이동하면 캐릭터도 왼쪽을 향한다. 현재 자유 이동의 `rotateWithCamera`는 꺼져 있다.

**스트레이프에서는 카메라 방향을 바라보며 옆이나 뒤로 이동할 수 있다.** 이동 방향과 몸이 바라보는 방향을 나누어 처리하는 것이다. 현재 스트레이프의 `rotateWithCamera`는 켜져 있다. 다만 전력질주 중에는 `sprintOnlyFree` 같은 조건에 따라 회전 기준이 달라진다.

옆걸음이 자연스럽게 보이려면 위치만 옆으로 옮기는 것으로 끝나지 않는다. Animator에도 캐릭터 기준 앞뒤·좌우 이동값을 전달해야 한다.

## Animator는 어떻게 동작을 섞을까?

실제 연결된 `Invector@BasicLocomotion` 컨트롤러에서 자유 이동은 `InputMagnitude`를 사용하는 1D Blend Tree다.

| `InputMagnitude` 기준값 | 연결된 동작 |
| --- | --- |
| 0 | Idle |
| 0.5 | Walk |
| 1 | Run |
| 1.5 | Sprint |

값이 중간에 있으면 인접한 동작을 섞는다. 이 숫자는 Rigidbody의 실제 속도 그 자체가 아니라, 코드가 Animator에 보내는 동작 선택용 값이다.

스트레이프는 속도 단계 안에 `InputHorizontal`과 `InputVertical`을 사용하는 2D Blend Tree가 들어 있다. 앞으로 달리기·뒤로 달리기·옆으로 달리기·대각선 이동을 방향값에 따라 섞는 구조다.

`SetAnimatorMoveSpeed()`는 월드 기준 이동 방향을 `transform.InverseTransformDirection()`으로 캐릭터 기준 방향으로 바꾼다. 그 결과의 X와 Z로 좌우·앞뒤 값을 구한다. 카메라 기준으로 만든 이동 방향을 다시 캐릭터 기준으로 해석하는 부분이 인상적이었다.

접지와 공중 상태는 `IsGrounded`, `GroundDistance` 등으로 전달한다. 점프 시작 때는 코드에서 `Jump` 또는 `JumpMove`로 전환하고, Animator에는 낙하와 착지 상태도 연결돼 있다.

주의할 점은 Animator 컴포넌트의 `Apply Root Motion`은 켜져 있지만, 컨트롤러의 `useRootMotion`은 꺼져 있다는 것이다. `OnAnimatorMove()`에서 별도로 처리하므로 체크박스 하나만 보고 실제 이동 방식을 판단하면 안 된다. 현재 코드는 입력이 0일 때 Animator의 루트 위치·회전을 적용하는 경로도 갖고 있다.

## 점프한 뒤에도 방향을 바꿀 수 있는 이유

공중에서도 입력과 `moveDirection`을 계속 갱신하고, `AirControl()`에서 Rigidbody의 수평 속도를 새 방향으로 보간한다.

현재 사용 중인 분기를 원리만 남겨 정리하면 다음과 같다.

```csharp
// 현재 입력 방향으로 공중 목표 속도를 만든다.
Vector3 targetVelocity = moveDirection * airSpeed;

// 상승하거나 떨어지는 속도는 유지한다.
targetVelocity.y = rigidbody.linearVelocity.y;

// 수평 속도를 새 입력 방향으로 부드럽게 바꾼다.
rigidbody.linearVelocity = Vector3.Lerp(
    rigidbody.linearVelocity,
    targetVelocity,
    airSmooth * deltaTime
);
```

앞으로 점프한 뒤 오른쪽을 누르면 목표 수평 속도가 오른쪽으로 바뀐다. 현재 속도가 그쪽으로 서서히 바뀌면서 공중 궤적이 휘어진다. 출발할 때의 수평 속도를 착지할 때까지 그대로 유지하는 구조가 아니다.

| 공중 관련 설정 | 현재 값 | 의미 |
| --- | --- | --- |
| `airSpeed` | 5 | 공중 수평 이동의 목표 속도에 사용 |
| `airSmooth` | 6 | 공중 입력과 속도를 보간하는 정도 |
| `jumpAndRotate` | true | 공중에서 캐릭터의 몸 회전을 허용 |
| `jumpWithRigidbodyForce` | false | 현재는 목표 속도를 보간하는 분기 사용 |

**몸이 돌아가는 것과 이동 궤적이 바뀌는 것은 별개였다.** `jumpAndRotate`를 꺼도 `AirControl()`의 수평 속도 제어가 사라지는 것은 아니다. 공중 조작을 제한하려면 회전 허용 여부와 공중 입력 반영을 각각 봐야 한다.

`jumpWithRigidbodyForce`를 켰을 때는 `AddForce(..., ForceMode.VelocityChange)`로 입력 방향의 속도 변화를 누적하는 다른 분기를 사용한다. 현재 관찰한 캐릭터는 이 분기를 사용하지 않는다.

## 이름이 jumpHeight라고 해서 실제 높이는 아니었다

`ControlJumpBehaviour()`는 점프 상태인 동안 수직 속도를 반복해서 `jumpHeight`로 설정한다. 현재 `jumpTimer=0.3`, `jumpHeight=4`다.

여기서 4는 실제 높이 4m가 아니라 **위쪽 속도로 대입되는 값**이다. 약 0.3초 동안 상승 속도를 유지하는 처리가 있고, 이후 Rigidbody 중력과 추가 중력이 낙하에 영향을 준다. 실제 최고 높이는 이 값 하나만으로 정해지지 않는다.

변수 이름이나 Inspector 설명만 읽는 것보다, 그 값이 실제로 위치에 들어가는지 속도에 들어가는지 확인해야 한다는 것을 배웠다.

## 내 로코모션을 만들 때 참고할 점

이번에 확인한 구조에서 참고하고 싶은 부분은 지상 이동, 공중 수평 이동, 수직 속도, 몸의 회전, 애니메이션 표시를 나누어 생각하는 방식이다.

공중 방향 전환도 Rigidbody가 알아서 제공하는 동작이 아니라, 코드가 공중에서도 입력에 맞춰 속도를 바꿔 주기 때문에 가능했다. CharacterController를 쓰더라도 공중에 입력을 얼마나 반영할지 정해 구현할 수 있다.

내 이동 코드를 확장할 때는 먼저 지상과 공중의 입력 반영 정도를 정하고, 그 결과를 Animator에 어떻게 전달할지 이어서 생각해 보려고 한다. 이번에는 기존 코드와 설정을 읽어 구조를 확인했으며, 내 프로젝트에 이 컨트롤러를 옮기거나 점프를 새로 구현하지는 않았다.
