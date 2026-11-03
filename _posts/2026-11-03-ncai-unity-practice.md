---
title: "261103_NCAI_Unity_실습"
date: 2026-11-03 10:07:00 +0900
categories: [데일리로그, Unity]
tags: [Unity, CSharp, Invector, 로코모션, Rigidbody, Animator, 점프, Skybox]
pin: false
toc: true
---

오늘은 Invector 캐릭터 컨트롤러를 보면서 로코모션 쪽을 확인해 봄\
캐릭터를 움직여 보니까 점프한 상태에서도 공중에서 방향을 바꿀 수 있었음\
근데 이건 어떤 식으로 움직이길래 가능한 거지?

내가 만드는 After Seconds는 CharacterController로 이동 중인데 이쪽은 Rigidbody를 쓰고 있었음\
그래서 입력이 어디로 들어가고, 실제 이동과 애니메이션이 어떻게 이어지는지 같이 정리해 봄

이번에 확인한 건 실습 프로젝트의 `Invector_Basic` 씬과 `Rigged_Dummy` 설정 기준

## 로코모션 스크립트 구성

로코모션은 걷기, 달리기, 방향 전환 같은 캐릭터 이동을 다루는 부분\
위치를 움직이는 코드와 움직이는 모습을 보여 주는 애니메이션을 같이 봐야 함

| 스크립트 | 역할 |
| --- | --- |
| `vThirdPersonInput` | 이동, 카메라, 점프, 스트레이프, 전력질주 입력 |
| `vThirdPersonController` | 이동 모드, 카메라 기준 이동 방향, 몸 회전, 점프 시작 |
| `vThirdPersonMotor` | 실제 Rigidbody 속도 제어, 접지, 경사, 중력, 공중 이동 |
| `vThirdPersonAnimator` | 이동과 접지 상태를 Animator에 전달 |

```text
MonoBehaviour
└─ vThirdPersonMotor
   └─ vThirdPersonAnimator
      └─ vThirdPersonController

vThirdPersonInput → Controller를 찾아 호출
```

이렇게 상속으로 연결된 구조임\
Input은 따로 붙어 있는 컴포넌트고, 같은 캐릭터의 Controller를 가져와서 사용 중

## 입력이 들어가서 움직이기까지

```text
Update
  입력 읽기
  카메라 기준 이동 방향 갱신
  Animator 파라미터 갱신

FixedUpdate
  UpdateMotor → 접지, 경사, 점프, 공중 조작
  ControlLocomotionType → 이동 모드, 속도, 지상 이동
  ControlRotationType → 몸 회전
```

입력은 `input`에 들어가고, 이걸 부드럽게 보간한 값이 `inputSmooth`\
그 값과 카메라의 앞쪽, 오른쪽 방향을 조합해서 `moveDirection`을 구함

현재 `rotateByWorld=false`라서 카메라 기준으로 움직이는 상태\
W를 눌렀을 때 월드의 고정된 방향으로 가는 게 아니라 카메라 기준 앞으로 가게 됨

## 지상 이동은 어떻게 하는지

현재 컨트롤러의 `useRootMotion`은 false\
`MoveCharacter()`에서 목표 속도를 계산해서 Rigidbody에 넣어 주는 방식

아래는 흐름만 보기 쉽게 줄인 코드

```csharp
Vector3 targetPosition = rigidbody.position
    + moveDirection * moveSpeed * deltaTime;

Vector3 targetVelocity = (targetPosition - transform.position) / deltaTime;
targetVelocity.y = rigidbody.linearVelocity.y;

rigidbody.linearVelocity = targetVelocity;
```

이동 방향과 속도로 목표 위치를 구함\
거기까지 가기 위한 속도를 계산해서 `linearVelocity`에 넣는 구조\
Y는 기존 값을 유지해서 상승, 낙하 속도를 수평 이동으로 덮어쓰지 않게 해 둠

공중이거나 점프 중이면 이 지상 이동 처리를 빠져나감\
그때는 따로 있는 `AirControl()`에서 처리

현재 자유 이동과 스트레이프의 속도 설정은 같음

| 항목 | 값 |
| --- | ---: |
| 걷기 `walkSpeed` | 2 |
| 달리기 `runningSpeed` | 4 |
| 전력질주 `sprintSpeed` | 6 |
| 입력과 속도 보간 `movementSmooth` | 6 |
| 회전 속도 `rotationSpeed` | 16 |
| 애니메이션 보간 `animationSmooth` | 0.2 |

`walkByDefault=false`라서 기본 이동의 목표 속도는 달리기 값인 4\
전력질주 상태가 되면 6을 사용함\
입력과 속도에 보간이 들어가서 처음 누르는 순간부터 바로 최댓값이 되는 건 아님

이건 설정값을 확인한 거고 실제 이동 거리를 재서 측정한 속도는 아님

## 자유 이동과 스트레이프

현재 모드는 `FreeWithStrafe`\
Tab으로 `isStrafing`을 바꿔서 두 이동 방식을 전환할 수 있음

자유 이동은 가려는 방향으로 몸도 돌아가는 방식\
왼쪽으로 움직이면 캐릭터도 왼쪽을 바라보게 됨\
현재 자유 이동의 `rotateWithCamera`는 꺼져 있음

스트레이프는 카메라 쪽을 바라보면서 옆이나 뒤로 움직이는 방식\
몸이 보는 방향과 실제 이동 방향을 따로 다룰 수 있음\
현재 스트레이프의 `rotateWithCamera`는 켜져 있음

다만 전력질주 중에는 `sprintOnlyFree` 같은 조건에 따라 회전 기준이 달라짐\
단순히 스트레이프를 켜면 모든 상황에서 카메라만 보는 구조는 아님

## Animator에서 걷기와 달리기를 섞는 방법

실제 연결된 `Invector@BasicLocomotion`을 확인해 보니\
자유 이동은 `InputMagnitude`로 1D Blend Tree를 제어 중

| 기준값 | 동작 |
| --- | --- |
| 0 | Idle |
| 0.5 | Walk |
| 1 | Run |
| 1.5 | Sprint |

중간값이면 옆에 있는 동작끼리 섞어서 표현함\
여기서 0.5, 1 같은 숫자는 실제 이동 속도가 아니라 애니메이션을 선택하기 위한 값

스트레이프는 속도 단계 안에 2D Blend Tree가 들어 있음\
`InputHorizontal`과 `InputVertical`로 앞, 뒤, 옆, 대각선 동작을 섞는 방식

`SetAnimatorMoveSpeed()`에서 이동 방향을 `transform.InverseTransformDirection()`으로 바꿔 주는데\
이건 월드 기준 방향을 캐릭터 기준 방향으로 바꾸는 부분\
여기서 나온 X와 Z로 옆으로 움직이는지, 앞으로 움직이는지를 Animator에 알려 줌

카메라 기준으로 이동 방향을 만들고 → 캐릭터 기준으로 다시 해석해서 애니메이션을 고르는 흐름

접지 쪽은 `IsGrounded`, `GroundDistance` 등을 전달하고 있음\
점프 시작은 코드에서 `Jump` 또는 `JumpMove`로 전환\
그 후 낙하와 착지 상태도 Animator에 연결돼 있음

그리고 Animator의 `Apply Root Motion`은 켜져 있었는데 컨트롤러의 `useRootMotion`은 꺼져 있었음\
`OnAnimatorMove()`에서 별도로 처리하는 구조라 체크박스 하나만 보고 판단하면 안 됨\
입력이 0일 때 Animator의 루트 위치와 회전을 적용하는 코드도 남아 있음

## 공중에서 방향을 바꿀 수 있는 이유

점프했다고 입력을 끊는 게 아니라 공중에서도 계속 새 입력을 읽고 있음\
그 입력으로 목표 수평 속도를 바꾸고, 현재 속도를 그쪽으로 보간하기 때문에 가능한 것

현재 사용하는 분기를 원리만 남겨 줄인 코드

```csharp
// 현재 이동 방향으로 공중 목표 속도를 계산
Vector3 targetVelocity = moveDirection * airSpeed;

// 상승, 낙하 속도는 유지
targetVelocity.y = rigidbody.linearVelocity.y;

// 현재 속도를 목표 속도 쪽으로 보간
rigidbody.linearVelocity = Vector3.Lerp(
    rigidbody.linearVelocity,
    targetVelocity,
    airSmooth * deltaTime
);
```

앞으로 점프하다가 오른쪽을 누름 → 목표 수평 속도가 오른쪽으로 바뀜\
현재 속도가 그쪽으로 바뀌면서 공중 궤적도 휘어지는 구조임

| 설정 | 현재 값 | 의미 |
| --- | --- | --- |
| `airSpeed` | 5 | 공중 목표 수평 속도에 사용 |
| `airSmooth` | 6 | 공중 입력과 속도를 보간하는 정도 |
| `jumpAndRotate` | true | 공중에서 몸 회전 허용 |
| `jumpWithRigidbodyForce` | false | 현재는 목표 속도를 보간하는 분기 사용 |

여기서 몸이 돌아가는 것과 실제 이동 방향이 바뀌는 건 별개\
`jumpAndRotate`를 꺼도 `AirControl()`이 없어지는 건 아니라서\
공중 이동까지 막으려면 수평 입력을 반영하는 부분도 따로 봐야 함

`jumpWithRigidbodyForce`를 켜면 `AddForce(..., ForceMode.VelocityChange)`로 속도 변화를 누적하는 다른 분기를 사용함\
지금 캐릭터는 이쪽을 사용하는 상태는 아님

## jumpHeight가 실제 높이는 아님

이름만 보면 점프 높이 같은데 실제로는 Y 속도에 넣고 있었음\
현재 `jumpHeight=4`, `jumpTimer=0.3`

점프 상태인 약 0.3초 동안 위쪽 속도를 반복해서 4로 설정하는 방식\
그 이후에는 Rigidbody 중력과 추가 중력이 낙하에 영향을 줌

그래서 4라고 해서 4m를 뛰는 뜻은 아님\
변수 이름만 보지 말고 이 값이 위치에 쓰이는지, 속도에 쓰이는지도 확인해야 함

## 내가 쓰는 CharacterController와는 어떤 차이가 있는지

After Seconds의 `PlayerMotor`는 Rigidbody 속도를 바꾸는 방식이 아님\
내가 계산한 속도에 시간을 곱해서 이번에 이동할 거리를 구한 다음\
`CharacterController.Move()`로 전달하고 있음

```csharp
// 현재 PlayerMotor의 흐름을 줄인 예시
Vector3 horizontalVelocity = moveDirection * settings.MoveSpeed;
verticalVelocity += settings.GravityAcceleration * deltaTime;

Vector3 velocity = horizontalVelocity + Vector3.up * verticalVelocity;
characterController.Move(velocity * deltaTime);
```

| 비교 | After Seconds | Invector 실습 코드 |
| --- | --- | --- |
| 전달하는 값 | 이번에 이동할 거리 | Rigidbody 속도 |
| 이동 호출 | `CharacterController.Move(속도 × 시간)` | `Rigidbody.linearVelocity = 목표 속도` |
| 중력 | 코드에서 수직 속도에 누적 | Rigidbody 중력과 추가 중력, 점프 속도 제어 |
| 관성, 밀림 | 필요한 동작을 별도로 설계 | 물리 영향을 받지만 속도 대입으로 덮어쓸 수도 있음 |
| 공중 방향 전환 | 공중에 입력을 얼마나 적용할지 코드로 결정 | `AirControl()`에서 목표 속도로 보간 |

CharacterController도 벽과 바닥의 충돌 처리는 해 줌\
대신 Rigidbody처럼 힘에 반응해서 움직이는 방식은 아니라서\
넉백이나 가속, 감속이 필요하면 별도 속도를 계산해서 합쳐 주는 식으로 만들 수 있음

반대로 Rigidbody라고 무조건 관성이 그대로 유지되는 것도 아님\
지금 Invector처럼 매번 속도를 넣어 주면 외부에서 밀린 속도를 이동 코드가 다시 바꿀 수도 있음

내 `PlayerMotor.Move()`는 공중이라고 수평 입력을 막는 조건이 없음\
이 흐름으로 점프를 추가하면 공중에서도 새 입력 방향으로 수평 속도를 구하게 됨\
아직 점프 기능은 없으니 실제 점프 테스트를 했다는 의미는 아님

Invector처럼 부드럽게 방향을 바꾸고 싶으면\
수평 속도를 따로 기억해 두고 목표 속도로 보간하는 부분을 참고할 수 있을 듯

## 어떤 게임에서 쓰기 좋을지

Unity 공식 문서의 이동 방식 설명을 바탕으로 생각해 본 사례\
아래는 어떤 게임을 만들 때 검토할지 정리한 거고, 특정 출시작의 내부 코드를 확인한 목록은 아님

| 만들려는 게임과 상황 | 먼저 검토할 방식 | 이유 |
| --- | --- | --- |
| 1인칭 퍼즐, 잠입 게임 | CharacterController | 좁은 발판이나 엄폐물 앞에서 정확히 멈추고 조준하기 좋음 |
| 정밀한 점프가 중요한 플랫폼 액션 | CharacterController 또는 별도 이동 코드 | 점프 궤적과 공중 입력을 직접 설계하기 좋음. Rigidbody로도 구현 가능 |
| 서로 밀고 넘어뜨리는 물리 난투 | Rigidbody와 필요한 Joint | 충돌, 외력, 회전 자체가 게임의 재미가 되는 경우 |
| 공 굴리기, 차량 조작 | Rigidbody | 경사, 마찰, 힘, 토크, 관성을 이동에 활용하기 좋음 |
| 달리기, 회피, 스트레이프가 있는 3인칭 액션 | 두 방식 모두 검토 | 조작 반응과 물리 반응 중 어디에 비중을 둘지에 따라 달라짐 |

예를 들면 좁은 발판에서 입력을 놓는 순간 멈추게 하고 싶으면 CharacterController 쪽부터 볼 수 있음\
반대로 큰 물체에 부딪혀 튕겨 나가는 것 자체가 재미라면 Rigidbody 쪽을 먼저 검토하는 식

그리고 플레이어와 물체가 꼭 같은 방식을 쓸 필요는 없음\
플레이어는 CharacterController, 던지는 상자는 Rigidbody로 구성하는 것도 가능함\
대신 서로 미는 동작이나 무게 판정 같은 연결은 따로 구현해야 함

## 내 게임에서는 왜 CharacterController로 시작했는지

기획서에는 플레이어 이동은 CharacterController로 시작하고\
교환과 끼임 처리는 규칙 코드로 다룬다는 가안이 적혀 있음

미리보기는 경비 상태를 계산하고 플레이어 이동까지 예측하지 않는 범위를 전제로 한 선택\
처음부터 모든 이동을 자체 물리로 만들기보다 기본 이동과 충돌은 준비된 기능으로 시작하는 방향임

여기에 현재 게임 구성을 같이 보면 이런 장점이 있을 것 같음

- 좁은 공간이나 냉각조 가장자리에서 멈추고 조준하는 걸 입력 중심으로 조절하기 좋음
- 평소 걷기, 벽 충돌과 예약된 시각의 위치 교환을 나누어서 생각할 수 있음
- 지금의 입력 → 이동 방향 → 속도 → 중력 → Move 구조에서 점프나 달리기를 하나씩 붙여 보기 좋음

이 세 가지는 현재 설계를 보고 정리한 해석\
처음 선택할 때 전부 이유로 적혀 있던 건 아니고, CharacterController도 아직 시작 가안으로 기록돼 있음

그리고 CharacterController를 쓴다고 미래 예측이나 교환이 자동으로 정확해지는 건 아님\
교환할 자리에 공간이 있는지, 벽에 끼지 않는지\
교환 후 낙하 속도를 유지할지 초기화할지 같은 건 별도로 정해야 함

Rigidbody로 위치 교환을 만드는 것도 가능함\
나중에 폭발, 줄, 움직이는 구조물의 힘을 플레이어에게 그대로 전달하는 게 중요해지면\
그때는 이동 방식과 외력 처리도 다시 비교해 볼 필요가 있어 보임

지금은 현재 이동 구조에서 지상 이동, 공중 입력, 수직 속도, 몸 회전, 애니메이션을 나눠서 이해하는 게 먼저일 듯\
이번에는 기존 코드를 읽고 설정을 확인한 상태고, 내 프로젝트의 이동 코드를 교체하거나 점프를 구현한 건 아님

## 스카이박스 유형

스카이박스는 씬 바깥에 보이는 하늘이나 먼 배경을 표현하는 머티리얼\
같은 하늘을 보여 주더라도 이미지를 어떤 형태로 넣는지, 이미지 없이 계산해서 만드는지에 따라 유형이 나뉨

이번에 정리할 건 `6 Sided`, `Cubemap`, `Panoramic`, `Procedural` 네 가지\
앞의 세 가지는 텍스처를 사용하는 방식이고, Procedural은 머티리얼 설정값으로 하늘을 만드는 방식임\
[Unity 스카이박스 유형 설명](https://docs.unity3d.com/6000.4/Documentation/Manual/skybox-shaders.html) 기준으로 정리

### 6 Sided · 6사이디드

앞, 뒤, 왼쪽, 오른쪽, 위, 아래에 사용할 이미지 6장을 각각 넣는 방식\
큰 상자 안쪽 여섯 면에 배경 그림을 붙인다고 생각하면 이해하기 쉬움

각 방향 이미지를 따로 넣을 수 있어서 6면으로 나눠진 배경 자료를 사용할 때 맞는 방식\
대신 방향이나 회전이 맞지 않으면 하늘이 뒤집히거나 경계가 어색하게 이어질 수 있음\
면끼리 맞닿는 부분의 구름이나 색이 연결되는지도 확인해야 함

머티리얼 Shader에서 `Skybox/6 Sided`를 선택하고 각 면의 텍스처 슬롯에 연결\
색감, 노출, 회전도 조절할 수 있음\
[6 Sided 설정 설명](https://docs.unity3d.com/6000.4/Documentation/Manual/shader-skybox-6sided.html)

### Cubemap · 큐브맵

여섯 방향을 담은 **Cubemap 에셋 하나**를 연결하는 방식\
이것도 여섯 면으로 주변을 표현하지만, 머티리얼에서 이미지 6장을 따로 받는 6 Sided와 입력 형태가 다름

`Skybox/Cubemap`을 선택하고 `Cubemap (HDR)` 슬롯에 연결\
일반 Texture2D 이미지를 그대로 넣는 슬롯과는 구분해야 함

이미 준비된 Cubemap 에셋을 배경으로 쓸 때 검토할 수 있음\
노출과 색감, Y축 회전을 조절해서 배경 방향을 맞출 수 있음\
[Cubemap 설정 설명](https://docs.unity3d.com/6000.4/Documentation/Manual/shader-skybox-cubemap.html)

### Panoramic · 파노라믹

주변 풍경을 한 장에 펼친 2D 이미지를 씬 주위로 감싸는 방식\
가로와 세로에 경도, 위도 방향을 펼쳐 놓은 Lat-Long 이미지가 기준\
일반 사진 한 장을 넣는다고 자동으로 자연스러운 전 방향 배경이 되는 건 아님

`Skybox/Panoramic`을 사용하고 텍스처는 `Texture Shape=2D`로 준비\
전 방향으로 펼쳐진 HDRI 같은 자료를 배경으로 활용할 때 검토하기 좋은 방식

Cubemap도 하나, Panoramic도 하나를 연결하니까 비슷해 보일 수 있는데\
Cubemap은 여섯 면을 담은 큐브 텍스처 에셋이고, Panoramic은 펼쳐진 2D 텍스처라는 차이가 있음\
[Panoramic 입력 형태 설명](https://docs.unity3d.com/6000.4/Documentation/Manual/skybox-shaders.html#panoramic-skybox-shader)

### Procedural · 프로시저럴

하늘 이미지를 넣는 대신 설정값을 계산해서 하늘을 만드는 방식\
`Skybox/Procedural`에서 하늘 색, 대기 두께, 지평선 아래 색, 노출, 태양 크기 등을 조절할 수 있음

태양 원반을 표시하는 경우에는 사용하는 Directional Light의 회전으로 태양 방향을 정함\
빛의 방향과 머티리얼 설정값을 바꾸는 식으로 낮이나 노을 분위기를 만들 때 검토할 수 있을 듯

다만 Procedural을 고르는 것만으로 시간이 흐르거나 날씨가 자동으로 바뀌는 건 아님\
기본 제공 항목에 구름, 비, 밤낮 주기 전체가 들어 있는 것도 아니라서 필요한 기능은 따로 구성해야 함\
[Procedural 설정 설명](https://docs.unity3d.com/6000.4/Documentation/Manual/shader-skybox-procedural.html)

### 네 가지 비교

| 유형 | 넣는 자료 | 구분할 부분 |
| --- | --- | --- |
| 6 Sided | 방향별 텍스처 6장 | 각 면에 직접 연결, 방향과 경계 확인 |
| Cubemap | Cubemap 에셋 1개 | 여섯 방향을 담은 큐브 텍스처 |
| Panoramic | 펼쳐진 2D 텍스처 1장 | Lat-Long 형태로 준비 |
| Procedural | 별도 하늘 텍스처 없이 설정값 사용 | 하늘과 태양 표현을 계산해서 생성 |

준비한 이미지가 여섯 장인지, Cubemap인지, 펼쳐진 한 장인지부터 보면 선택하기 쉬울 듯\
이미지를 준비하지 않고 하늘 색과 태양부터 조절해 보고 싶으면 Procedural을 검토

위 설명은 Built-in과 URP의 Skybox Shader 기준\
HDRP는 별도의 Sky 시스템을 사용하므로 같은 Shader 메뉴를 그대로 적용하는 방식과는 다름\
이번 항목은 유형 설명을 정리한 메모이고 실제 프로젝트의 스카이박스를 교체한 건 아님

## 참고 자료

- [Unity 6.4 — Character Controller 설명](https://docs.unity3d.com/6000.4/Documentation/Manual/CharacterControllers.html)
- [Unity 6.4 — Rigidbody 설명](https://docs.unity3d.com/6000.4/Documentation/Manual/class-Rigidbody.html)
