---
title: "261103_NCAI_Environment_Training_조명과_셰이더_데이터"
date: 2026-11-03 11:49:00 +0900
categories: [데이터, Unity]
tags: [Unity, URP, 조명, ShaderGraph, Volume, 환경제작, 재사용]
pin: false
toc: true
---

Environment Training 프로젝트에 있는 조명과 셰이더 구성을 나중에 다시 보기 위해 정리해 둠\
화면이 예뻐 보인다고 Light 강도 하나만 복사하면 같은 결과가 나오지는 않을 것 같아서\
광원, URP 설정, 후처리, 머티리얼, 셰이더 의존 파일을 같이 확인해 봄

확인한 프로젝트는 `Unity_NCAI_Environment_Training_V0.02`\
Terminal, Garden, Cockpit, Oasis 구성이 들어 있으며 [Unity URP 3D Sample](https://unity.com/demos/urp-3d-sample)과 연결해서 참고할 수 있음\
아래 숫자는 이 프로젝트의 파일과 현재 열린 씬에서 추출한 값임

## 데이터 내려받기

- [설정 데이터와 가져오기 도구 ZIP](/assets/data/environment-training-20261103.zip)
- [자료 구성과 사용 순서](/assets/data/environment-training-20261103/README.md)
- [Light·Volume 가져오기용 JSON](/assets/data/environment-training-20261103/portable-presets.json)
- [Unity Editor 가져오기 스크립트](/assets/data/environment-training-20261103/EnvironmentTrainingDataImporter.cs)
- [생성·검수 결과](/assets/data/environment-training-20261103/import-validation.json)
- [자동 변환에서 제외된 항목](/assets/data/environment-training-20261103/import-report.txt)

다운로드에는 설정값과 참조 목록, 새로 작성한 가져오기 도구를 넣어 둠\
원본 셰이더와 의존 에셋은 로컬 참조 폴더에도 unitypackage와 파일 사본으로 따로 보관함\
공개 데이터에 원본 프로젝트의 전체 모델이나 텍스처를 넣은 구성은 아님

## 먼저 확인할 버전과 렌더링 설정

| 항목 | 확인한 값 |
| --- | --- |
| Unity | 6000.4.0f1 |
| URP / Shader Graph / VFX Graph | 17.4.0 |
| Color Space | Linear |
| 확인 당시 Quality | PC High |
| 현재 씬 | TerminalScene |
| 현재 URP Asset | PC_High |

| 설정 | PC High | PC Low |
| --- | --- | --- |
| 기본 Renderer 경로 | Forward+ | Deferred |
| Render Scale | 1.0 | 약 0.8 |
| HDR | 켬 | 켬 |
| Opaque Texture | 켬 | 켬 |
| URP Asset의 Depth Texture | 끔 | 끔 |
| MSAA | Disabled | Disabled |
| Shadow Distance | 50 | 50 |
| Shadow Cascade | 4 | 1 |
| Depth Priming | Forced | Disabled |

PC High Renderer에는 SSAO, Decal, FullscreenMask용 Render Objects Feature가 들어 있음\
PC Low는 Decal과 Render Objects를 사용하는 구성\
여기서는 Low라는 이름이라고 무조건 Forward를 쓰는 건 아니었음

Depth Texture 항목이 꺼져 있다고 모든 패스에서 깊이 정보를 안 쓴다는 뜻은 아님\
Renderer의 Depth Priming이나 개별 커스텀 패스의 Depth 입력 요청도 함께 봐야 함\
깊이를 읽는 효과를 다른 프로젝트로 옮길 때는 실제로 Depth Texture가 제공되는지 확인해야 함\
[Scene Depth 노드 설명](https://docs.unity.cn/Packages/com.unity.shadergraph@17.4/manual/Scene-Depth-Node.html)

상세 기록은 [렌더 설정 JSON](/assets/data/environment-training-20261103/render-settings.json)과 [프로젝트 정보](/assets/data/environment-training-20261103/project.json)에 보관

## 씬별 광원 구성

| 씬 | Light 컴포넌트 | Reflection Probe | 주광원 설정 |
| --- | ---: | ---: | --- |
| Terminal | 138 | 7 | Directional / Mixed / Intensity 5 |
| Garden | 86 | 9 | Directional / Baked / Intensity 0.4 |
| Cockpit | 3 | 0 | Directional / Realtime / Intensity 2 |
| Oasis | 3 | 3 | Directional / Mixed / Intensity 2.5 |

Light 수는 비활성 오브젝트와 꺼진 Light까지 포함해서 센 값\
실제 프레임에서 저 숫자만큼의 실시간 광원을 동시에 계산한다는 뜻은 아님\
Cockpit과 Oasis는 저장된 시작 상태에서 루트가 비활성인 구성도 있어, 실행 후 씬 로더가 켜는 상태와 구분해야 함

Terminal은 Baked Spot 47개, Baked Rectangle 57개, Mixed Spot 21개 등을 함께 사용 중\
Garden도 Baked, Mixed, Realtime 광원을 섞어 사용하고 있음\
밝은 부분마다 전부 Realtime Light 하나씩 넣는 방식으로 만들어진 건 아님

Intensity 숫자만으로 어느 씬이 더 밝다고 단정하면 안 됨\
광원 유형, 색, 거리, 면적, 머티리얼, 베이크와 노출이 같이 영향을 주기 때문\
대표값은 복사의 출발점으로 보고 새 씬에서 다시 맞추는 게 좋을 듯

- [Terminal 광원과 연결 정보](/assets/data/environment-training-20261103/TerminalScene.json)
- [Garden 광원과 연결 정보](/assets/data/environment-training-20261103/GardenScene.json)
- [Cockpit 광원과 연결 정보](/assets/data/environment-training-20261103/CockpitScene.json)
- [Oasis 광원과 연결 정보](/assets/data/environment-training-20261103/OasisScene.json)

## 빛이 보이는 효과와 실제 광원은 구분하기

### Garden의 동적 광원과 깜빡임

`DynamicLightController.cs`는 카메라와 광원 사이의 거리를 보고 빛을 조절하는 코드\
설정된 거리 밖에서는 Light를 끄고, 경계 구간에서는 강도와 범위를 커브로 줄여 줌\
코드의 기본값은 표시 거리 50, 감쇠 구간 5이며 실제 컴포넌트별 값은 씬 데이터에서 확인 가능

`LightFlicker.cs`는 Perlin Noise를 사용해서 위치, 회전, 광원 강도를 흔드는 구조\
불빛이나 촛불처럼 일정하지 않은 느낌을 만들 때 참고할 수 있을 듯\
빛 강도만 흔드는 게 아니라 위치와 회전도 같이 바뀔 수 있다는 점을 봐야 함

`WashiLightController.cs`는 별도로 머티리얼의 `_Intensity`를 바꾸고 렌더러 표시도 조절함\
즉 실제 Light의 강도를 바꾸는 것과 종이·창문 표면이 빛나 보이는 표현을 따로 다루고 있음

### Fake Volumetrics

Garden의 `FakeVolumetrics_Graph.shadergraph`는 Unlit Target을 사용 중\
위치와 Fresnel 계산으로 겉보기 효과를 만드는 그래프이며\
공간 전체의 빛 산란을 계산하는 볼류메트릭 조명으로 보면 안 됨

빛줄기처럼 보이는 표현을 가져오더라도\
그 표현만으로 주변 벽이나 플레이어까지 실제로 밝아지는 건 아니라는 점을 구분해야 함

### Oasis의 높이 Fog

`HeightFog.shadergraph`는 Scene Depth를 읽는 Fullscreen 계열 그래프\
높이 범위, 시작 거리, Density, Tint, Sun Scattering 값을 사용하고 있음

여기서는 그래프만 옮기면 끝나는 게 아님\
`OasisFogVolumeComponent`의 값 → `OasisFog` 패스 → 머티리얼 → Fullscreen Shader가 이어지는 구조\
관련 Volume 타입과 패스 주입 코드도 함께 연결해야 함

코드에는 Unity 6000.4용 RenderGraph 경로도 들어 있음\
구버전 Unity로 옮기면 관련 API 차이를 먼저 확인할 필요가 있음

## Volume 후처리 설정

Volume Profile은 총 23개를 확인함\
아래는 그중 비교하기 좋은 대표 설정

| Profile | 대표 값 |
| --- | --- |
| HighQualityVolumeProfile | ACES, Bloom Intensity 0.25 / Threshold 1, Vignette 약 0.2 |
| LowQualityVolumeProfile | Neutral, Bloom Intensity 0.5 / Threshold 2, Contrast 50 / Saturation -10 |
| TerminalRoom_Profile | Post Exposure 2, Saturation 약 13.7, Bloom 0.25 |
| GardenOutdoorVolumeProfile | Post Exposure 1, White Balance Temperature -16 / Tint 10, Bloom 1 |
| CockpitVolume | Post Exposure 0.5, Bloom 약 0.7, Vignette 약 0.304 |
| Oasis_Outdoor_Volume_Profile | Post Exposure 0.25, Contrast 15, Bloom 0.5, 커스텀 Fog Density 약 0.005 |

Profile에 숫자가 적혀 있어도 그 값이 항상 최종 화면에 적용되는 건 아님\
컴포넌트 활성 상태, 각 항목의 Override 체크, Volume의 Weight·Priority·범위와 카메라 레이어를 함께 봐야 함\
예를 들어 HighQuality Profile의 Motion Blur에는 값이 들어 있지만 컴포넌트는 비활성 상태였음

전체 값과 Override 상태는 [Volume Profile 데이터](/assets/data/environment-training-20261103/volume-profiles.json)에 보관함

## 셰이더 파일과 세팅 보관

TextMeshPro 기본 셰이더를 제외하고 확인한 관련 파일은 총 138개

| 형식 | 수 |
| --- | ---: |
| Shader Graph | 86 |
| Sub Graph | 40 |
| HLSL | 4 |
| 일반 Shader | 3 |
| VFX Graph | 5 |

| 참고할 효과 | 파일과 확인한 구성 |
| --- | --- |
| Garden 수면 | WaterSurface_Graph: Scene Depth, 시간, 노멀 이동, 반사 강도, 거품 거리·강도 |
| Garden 빛줄기 표현 | FakeVolumetrics_Graph: Unlit, Fresnel, 위치 기반 계산 |
| Cockpit 스타일 조명 | Cockpit / ToonLitCustomLightmap 그래프, ToonLighting.hlsl: 커스텀 조명·Lightmap 입력 |
| Oasis 바위·모래 혼합 | LayeredLit_Graph: 다중 텍스처, 노멀 혼합, 버텍스 컬러, 노이즈, 거리 기반 파라미터 |
| Oasis Fog | HeightFog 그래프와 Volume·Fullscreen 패스 연결 |
| Terminal 홀로그램 | Hologram 계열 Graph와 Sub Graph, 머티리얼 값·텍스처·키워드 |

노드가 들어 있다는 것과 모든 기능을 현재 머티리얼에서 켜서 쓰고 있다는 건 별개\
셰이더 이름만 복사하지 않도록 실제 머티리얼 113개의 프로퍼티, 텍스처 참조, 키워드도 저장해 둠

- [셰이더·의존 파일 목록](/assets/data/environment-training-20261103/shader-inventory.json)
- [Shader Graph 노드·참조 이름 목록](/assets/data/environment-training-20261103/shader-graph-features.json)
- [머티리얼 설정값](/assets/data/environment-training-20261103/shader-materials.json)

다른 프로젝트에서 물이나 Fog 효과가 보이지 않으면\
Sub Graph, Custom Function HLSL, 텍스처뿐 아니라 Opaque·Depth 입력과 렌더 패스 시점까지 같이 확인해야 함

## 물 표현과 렌더링 기법을 우리 게임에 맞추기

물은 하나의 셰이더만 있는 구성이 아니었음\
수면, 폭포, 잔물결, 물빛 무늬를 나눠서 참고할 수 있음

| 확인한 파일·구성 | 참고할 요소 | 우리 쪽에서 바꿔볼 부분 |
| --- | --- | --- |
| Garden `WaterSurface_Graph` | Scene Depth, 움직이는 노멀, 거품 거리·강도, 반사 강도 | 물 색, 흐름 속도, 접촉부 거품 폭을 새 맵 크기에 맞추기 |
| Garden `Waterfall_Graph` | 시간·노이즈·버텍스 컬러, 폭포 속도·알파·거품 프로퍼티 | 폭포 메시와 UV를 직접 준비하고 낙하 방향·속도 조절 |
| Garden `WaterfallRipple_Graph` | Unlit, UV·시간·노이즈, 잔물결 속도·색 | 낙수 위치에 맞는 작은 효과로 구성 |
| Shared `Water.shadergraph` | Scene Color·Depth, Fresnel, Reflection Probe, 굴절 관련 프로퍼티 | 얕은 물·깊은 물 색과 굴절 강도를 게임 시야에 맞추기 |
| Shared `WaterCausticsDecal` | Decal Target, 위치·시간·텍스처 샘플링 | 물 밑 빛무늬 텍스처를 직접 준비하고 크기·이동 속도 조절 |
| Shared `Water.hlsl` | 깊이 샘플링, 환경 반사, 화면 공간 Raymarch 함수와 샘플 수 분기 | 연결된 그래프·키워드부터 확인하고 목표 기기에 맞춰 비용 비교 |

`Water.hlsl`에는 SSR 반복 수를 4·8·16·32로 나누는 분기가 들어 있음\
코드에 함수가 있다는 것만으로 모든 물 머티리얼이 SSR을 사용한다고 보면 안 됨\
실제 그래프 연결, 활성 키워드, 카메라 입력까지 확인할 필요가 있음

광원도 같은 방식으로 나눠 보면 좋을 듯\
실제 조명과 그림자는 Light·베이크 쪽에서 다루고\
빛나는 표면, Bloom, 빛줄기 메시, Fog는 화면에 보이는 효과로 따로 조절하는 식

렌더링 참고 항목은 Forward+·Deferred, SSAO, Decal, Render Objects, Reflection Probe, 베이크, Fullscreen Fog와 Volume 후처리까지 포함함\
원본의 High·Low 값을 그대로 정답처럼 쓰기보다는\
같은 카메라에서 효과를 하나씩 켜고 끄면서 화면 차이와 프레임 비용을 비교하는 기준으로 사용하면 좋을 듯

## 수정해서 쓰는 것과 저작권

우리 식으로 바꿔 쓰는 게 무조건 금지되는 건 아님\
원본 라이선스에서 사용·수정·배포를 어디까지 허용하는지가 먼저임\
이름이나 색, 숫자를 바꿨다고 원본 코드·텍스처의 권리가 사라지는 건 아님

| 사용 방식 | 확인할 기준 |
| --- | --- |
| 깊이 기반 거품, UV 이동 같은 원리를 이해하고 직접 구현 | 원본 표현을 복제한 부분이 있는지 확인하고 자체 코드·텍스처로 구성 |
| 원본 셰이더·텍스처를 그대로 또는 수정해서 게임에 포함 | 해당 파일에 적용되는 라이선스의 사용·수정·게임 배포 조건 확인 |
| 원본 또는 수정한 에셋을 블로그에서 내려받게 제공 | 게임에 포함할 권한과 별도로 소스·에셋 재배포 권한 확인 |

일반 Asset Store EULA의 비제한 에셋은 조건에 맞는 게임에 포함하고 수정할 수 있는 범위를 두고 있음\
게임에 포함해 배포하는 것과 에셋 자체를 자료집으로 나눠 주는 것은 구분해야 함\
Restricted Asset이나 별도 약관이 있으면 해당 조건도 확인\
[Unity Asset Store EULA 2.2](https://unity.com/legal/as-terms)

Unity Companion License가 실제로 적용되는 파일이라면 Unity 라이선스 아래 콘텐츠 제작·배포와 연결된 사용 조건을 따르게 됨\
원본·수정본의 고지 유지와 제3자 별도 조건도 확인해야 함\
Unity 샘플처럼 보인다는 이유만으로 모든 파일에 같은 라이선스를 적용하면 안 됨\
[Unity Companion License](https://unity.com/legal/licenses/unity-companion-license)

이번 로컬 프로젝트의 루트와 Assets에서는 LICENSE·Third Party Notices 문서를 찾지 못함\
따라서 전체 에셋의 상용 사용·재배포 허가를 확인 완료한 상태는 아님\
원본 획득 경로의 조건과 추가된 외부 에셋의 조건은 실제 채택 전에 따로 확인할 필요가 있음

블로그에는 관찰한 설정값·참조 목록·직접 작성한 설명과 가져오기 도구를 정리함\
JSON으로 추출했다고 모든 자료의 재배포 권리가 자동으로 생기는 건 아님\
원본 셰이더·텍스처·unitypackage는 공개 다운로드에 넣지 않고 로컬 참조 자료로 보관 중\
우리 게임용으로 옮길 때는 출처·라이선스·사용 파일·수정 내역을 같이 남기는 방식으로 진행하면 좋을 듯

## 다른 프로젝트에서 재사용하는 순서

1. 먼저 Unity와 URP 버전, Color Space를 확인.
2. 출처와 라이선스를 확인한 뒤 필요한 셰이더·Sub Graph·HLSL·텍스처를 함께 가져오거나 직접 구현함.
3. Renderer Feature와 Depth·Opaque 입력이 필요한지 확인.
4. Light·Volume 프리셋을 생성하고 필요한 항목만 씬과 카메라에 연결.
5. 머티리얼 값과 키워드, Volume Override·Weight를 원본 JSON과 비교.
6. 새 씬의 조명·Reflection Probe·베이크 결과를 다시 확인.

### 가져오기 도구 사용법

URP 프로젝트에서 `com.unity.nuget.newtonsoft-json` 패키지를 확인\
원본에서는 3.2.2를 사용 중

내려받은 `EnvironmentTrainingDataImporter.cs`를 `Assets/Editor/`에 넣고 컴파일을 기다림\
그 후 `Tools > Environment Training Data > Import Presets`에서 `portable-presets.json`을 선택하면 됨

새 폴더에 Light 프리팹 19개와 Volume Profile 23개를 만드는 도구\
기존 씬이나 Graphics·Quality의 URP Asset을 자동 교체하지는 않음

Light 19개는 씬별 광원 유형과 Bake 모드 조합에서 강도가 가장 큰 항목을 하나씩 고른 대표값\
원래 배치를 그대로 복원하는 도구가 아니라 기본 광원 설정을 다시 꺼내 쓰기 위한 프리셋임\
프리팹은 (0, 2, 0)에 생성되고 Cookie·URP 추가 속성·제어 스크립트는 원본 데이터와 비교해 따로 연결해야 함

원본 프로젝트에서 생성과 다시 불러오기를 확인했으며\
대표 광원 강도, Bloom 0.25, Terminal Post Exposure 2가 유지되는지도 확인함\
ColorCurves 곡선 8개는 자동 변환에서 제외돼 `ImportReport.txt`에 남겨 둠

대상 프로젝트에 `OasisFogVolumeComponent`나 `OutlineVolumeComponent`가 없으면 해당 항목은 건너뛰고 기록함\
원본 소스가 필요한 기능은 그래프·컴포넌트·패스를 함께 준비해야 함

### 베이크 결과는 새 씬에서 다시 확인

새 씬의 형상과 UV가 다르면 원본 Lightmap을 그대로 가져오는 것만으로 같은 빛이 나오지는 않음\
이번 보관 자료는 씬 전체를 복제해 완성된 화면을 재현하는 템플릿과는 구분해서 사용해야 함\
[Unity의 Lightmap·베이크 설명](https://docs.unity.com/en-us/engine/6000.6/manual/lighting-overview/direct-and-indirect-lighting/lightmapping/baking-before-runtime/lightmappers)

이번에는 원본 프로젝트의 씬·조명·파이프라인 연결을 변경하지 않고 자료를 추출함\
별도 프로젝트에서 최종 렌더가 똑같이 나오는지, 성능이 충분한지까지 검증한 건 아님\
필요한 효과를 하나씩 가져와 확인할 때 사용할 기준 데이터로 보관
