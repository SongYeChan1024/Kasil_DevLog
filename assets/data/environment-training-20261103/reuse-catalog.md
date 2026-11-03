# Environment Training 전체 재사용 후보 · 2026-11-03

대상: Unity_NCAI_Environment_Training_V0.02 / Unity 6000.4.0f1 / URP 17.4.0.

Assets 전체 파일 목록, 주요 런타임·편집기 코드, 기존 추출 데이터로 확인함. 모든 프리팹의 플레이·빌드·렌더 검증을 끝낸 목록은 아님. 실제 반입이나 원본 씬 변경은 수행하지 않음.

## 조사 범위

주요 환경: Terminal, Garden, Cockpit, Oasis. 보조 ShipSetup과 TPSControl의 Invector_Basic까지 씬 6개를 확인함.

전체 Assets 파일 집계: 프리팹 311, FBX 264, 머티리얼 274, C# 89, Shader Graph 88, Sub Graph 40, 일반 Shader 18, HLSL 4, VFX Graph 5, Timeline 12, Animation Clip 파일 16. FBX 내부 클립 수는 이 집계에 포함하지 않음. TextMeshPro 기본 셰이더와 TPS 실습 파일도 포함하므로 기존 shader-inventory.json의 선별 138개와 범위가 다름.

## 후보와 연결 조건

아래 경로는 원본 프로젝트의 Assets 기준 상대 경로임. 우선순위는 기술 검증 결과가 아니라 시설형 게임에 활용할 때의 제안임.

| 우선 | 후보 | 원본 위치 | 가져갈 요소와 확인할 연결 |
| --- | --- | --- | --- |
| 1 | 시설 구조·소품 | Scenes/Terminal/Art/Architechture/Prefabs/Room_Prefab.prefab · Props/Prefabs/ControlPanel_Prefab.prefab | 공간 구성·재질·제어 패널 참고. 실제 길이·충돌·동선은 대상 씬에서 재설계 |
| 1 | 얼룩 Decal | Scenes/Terminal/Art/Architechture/Prefabs/GrimeDecal_Prefab.prefab | 깨끗한 벽에 사용 흔적 추가. Decal Renderer Feature와 투사 레이어 확인 |
| 1 | 홀로그램 | Scenes/Terminal/Shaders/ScrollingHologram_Graph.shadergraph · SpriteSheetHologram_Graph.shadergraph · LoadingbarHologram_Graph.shadergraph | 표시 효과만 참고. 상태 데이터와 상호작용 판정은 자체 코드로 연결 |
| 1 | 조명 기준 | 씬별 JSON · portable-presets.json · volume-profiles.json | Light·발광 재질·Bloom·노출을 분리해서 조절. 원본 베이크는 새 공간에서 재사용 결과를 보장하지 않음 |
| 1 | 먼지·증기 | Scenes/Garden/Art/VFX/Prefabs/DustSpecks_Prefab.prefab · VFX_Out_Dust_Prefab.prefab · TeapotSteam_Prefab.prefab | 머티리얼·텍스처·ParticleSystem 연결 확인. 시설 먼지·증기로 색과 방출량을 재조정할 후보 |
| 1 | 빛줄기 | Scenes/Garden/Shaders/FakeVolumetrics_Graph.shadergraph | 메시·Unlit 표현 참고. 실제 공간 광산란이나 주변을 밝히는 Light와 구분 |
| 2 | 물 표면 | Scenes/Garden/Shaders/WaterSurface_Graph.shadergraph | 깊이·노멀 이동·거품·반사 강도를 기능별로 직접 구현해 볼 자료 |
| 2 | 폭포·잔물결 | Scenes/Garden/Shaders/Waterfall_Graph.shadergraph · WaterfallRipple_Graph.shadergraph | 메시·UV·알파·버텍스 컬러와 머티리얼 참조 확인 |
| 2 | 물 반사·굴절 | SharedAssets/Shaders/Water.shadergraph · HLSL/Water.hlsl | Depth·Opaque 입력과 Custom Function 연결 확인. SSR 함수 존재만으로 사용 중이라고 판단하지 않음 |
| 2 | 물빛 무늬 | SharedAssets/Shaders/WaterCausticsDecal.shadergraph | Decal 연결과 직접 준비한 텍스처로 작은 구역부터 실험 |
| 2 | 모니터 영상 | SharedAssets/Scripts/Runtime/ScreenCamera.cs · ScreenController.cs · Scenes/Terminal/Art/Props/Prefabs/TerminalScreen_Prefab.prefab | 카메라 RenderTexture를 _ScreenColor에 연결. 기존 코드는 SceneTransitionManager·Animator·LoadingBar에도 연결됨 |
| 2 | 화면 해상도 관리 | SharedAssets/Scripts/Runtime/ScreenCamera.cs | 화면 크기에 따라 RenderTexture 생성. 재작성 시 이전 텍스처 해제·파괴와 OnDisable/OnDestroy 정리까지 설계 |
| 2 | 전환·소멸 | SharedAssets/Shaders/TriplanarDissolve_Graph.shadergraph · FullscreenTransition_Graph.shadergraph · SharedAssets/Scripts/Runtime/FullscreenTransition.cs | 연출만 도입할 후보. FullscreenEffect·머티리얼·패스 시점·전역 Shader 속성과 매니저 의존 확인 |
| 2 | 카메라 연출 | Scenes/*/Animation/의 Timeline과 SharedAssets/Scripts/Runtime/MediaSceneLoader.cs | Cinemachine·Timeline 패키지 및 PlayableDirector 바인딩·Signal 확인. Timeline 파일 하나만 복사하면 씬 연결은 복원되지 않음 |
| 2 | 점멸·거리 감쇠 | Scenes/Garden/Scripts/Runtime/LightFlicker.cs · DynamicLightController.cs · WashiLightController.cs | 강도·위치·회전·머티리얼 효과를 분리. 깜빡임은 미리보기·판정 등 게임 상태와 섞지 않기 |
| 2 | 품질 분기 | SharedAssets/Scripts/Runtime/QualityLevelToggle.cs · QualityInitialization.cs | 시작 시 품질 이름에 따른 활성 제어와 그래픽 API별 품질 선택 참고. 이름 하드코딩과 없는 품질 처리 보완 필요 |
| 3 | 높이 Fog | Scenes/Oasis/Scripts/Runtime/OasisFog.cs · OasisFogVolumeComponent.cs · Scenes/Oasis/Shaders/HeightFog.shadergraph | FullscreenEffect와 RenderGraph 패스·Volume·머티리얼·Depth를 함께 준비 |
| 3 | 다중 표면 혼합 | Scenes/Oasis/Shaders/LayeredLit_Graph.shadergraph | 텍스처·노멀·버텍스 컬러·거리 기반 혼합 참고. 불필요한 레이어는 줄여 별도 그래프 설계 |
| 3 | 모래·벌레 VFX | Scenes/Oasis/VFX/VFXGraph/ 아래 그래프 5개 | VFX Graph 패키지·텍스처·메시·SDF/Point Cache 등 개별 의존 확인. 시설 먼지로 바꿀 때 원본 지형 가정도 제거 |
| 3 | 외곽선 | Scenes/Cockpit/Scripts/CockpitOutline.cs · OutlineVolumeComponent.cs · Shaders/HullOutline.shadergraph | Fullscreen 외곽선과 메시 기반 그래프를 혼동하지 않기. 선택 대상만 표시하려면 별도 마스크 설계 |
| 3 | 스타일 조명 | Scenes/Cockpit/Shaders/ToonLighting.hlsl · ToonLitCustomLightmap_graph.shadergraph | 화풍을 결정한 뒤 비교. 기존 조명·Lightmap 입력과 일관성 확인 |
| 3 | 3D 원경 | Scenes/Cockpit/Scripts/Skybox3D.cs | 축소된 3D 배경·카메라 변환·Stencil·Depth Clear 패스 구조 참고. 일반 Skybox 머티리얼의 대체 파일 하나로 취급하지 않음 |
| 3 | 경로 연출 | Scenes/Cockpit/Scripts/SplineFollower.cs · NpcSplineFollower.cs | Splines·보조 Transform·회전 보간 연결 확인. 예측 가능한 게임 AI 자체로 채택하는 것과는 구분 |
| 필요 시 | 발사체 시각 효과 | Scenes/Cockpit/Scripts/ParticleSpawnSystem.cs | 거리/속도로 파티클 수명을 정함. 충돌·명중 판정이 들어 있는 총알 시스템은 아님. speed=0 등 입력 보호 필요 |
| 필요 시 | 셰이더 준비 | SharedAssets/Scripts/Runtime/GraphicsStateCollectionManager.cs | 플랫폼·그래픽 API·품질에 맞는 PSO 기록과 WarmUp 참고. 원본 .graphicsstate를 대상 빌드에 그대로 적용한다고 효과가 보장되지 않음 |

## 코드 그대로 도입하지 않을 후보

- SceneTransitionManager: PlayerCapsule 이름, MainCamera 태그, 레이어, PlayerManager, 여러 씬과 강하게 연결됨. 화면 전환 원리부터 작게 분리하는 방향.
- LodLightmapCopy: InitializeOnLoad와 베이크·씬 열기·빌드 등에 개입함. LOD0와 하위 LOD의 Renderer 수·순서가 맞는지 전제 확인 필요. 대상 에셋의 UV가 같다는 보장도 별도 확인.
- DirectionalLightmapperCorrector: 특정 이름의 방향성 Lightmap 텍스처 알파를 임포트 시 변경함. 일반적인 필수 조명 설정으로 복사하지 않기.
- PrefabReplacer: 임시 작업용이며 제거 TODO가 적혀 있음. 이름 기반 교체와 DestroyImmediate를 사용하므로 그대로 반입하지 않기.
- HeightMapRenderer: Renderer 인덱스 2를 지정하는 코드가 있음. 대상 Renderer 목록을 확인하고 명시적 참조로 바꾸는 방향.
- GradientTexture: 그라디언트를 작은 텍스처로 만드는 원리는 유용함. 에셋·서브에셋을 저장하는 편집기 도구라 별도 테스트 권장.
- FPSCounter·MemoryCounter: 관찰용 UI 참고. 실제 CPU/GPU 병목이나 메모리 누수 판정을 대체하지 않음.

## 출처를 구분할 부분

Scenes/TPSControl에는 Invector 이동 코드, UVC 셰이더·반사 코드, VARCO 모델·실습 어댑터가 함께 들어 있음. 해당 폴더까지 Unity 기본 환경 샘플 라이선스로 일괄 판단하지 않음.

UVC_Skybox.shader에는 GBX Studio 저작권 표기가 있고, Cockpit/Scripts/SplineFollower.cs의 Quaternion SmoothDamp에는 별도 저작권·허가문이 있음. 사용 시 해당 고지를 유지하고 적용 조건 확인.

Unity 공식 샘플 부분도 원본 획득 경로의 이용 조건을 확인함. Unity Companion License가 적용되는 부분과 다른 제3자 조건을 나눠 기록하는 방식. 원본·수정본의 라이선스 고지는 삭제하지 않음.

## 첫 실험 제안

1. 작은 방에 발광 머티리얼과 Bloom 하나만 연결하고 기본 노출부터 맞춤.
2. 먼지 또는 증기 하나를 넣고 조준 대상의 가독성과 비용 비교.
3. 자체 카메라와 RenderTexture로 모니터 한 대를 구성.
4. 자체 물 그래프에 색 → 노멀 이동 → 깊이 → 거품 순서로 기능 추가.
5. 전환·Fog·외곽선은 필요가 확인된 뒤 각각 분리해서 도입.

이번 목록은 도입 제안임. 게임 로직을 추가하거나 현재 프로젝트에 원본 에셋을 반입한 결과는 아님.
