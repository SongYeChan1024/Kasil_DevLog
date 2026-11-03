# Environment Training 조명·셰이더 데이터

2026-11-03 · Unity 6000.4.0f1 / URP 17.4.0에서 확인한 자료

## 파일 구성

- `project.json`: 버전, 패키지, 현재 Quality·렌더 파이프라인, 환경 설정
- `TerminalScene.json`, `GardenScene.json`, `CockpitScene.json`, `OasisScene.json`: 광원·Volume·반사 프로브·머티리얼 연결과 씬의 RenderSettings·LightmapSettings 기록
- `render-settings.json`: URP Asset, Renderer Feature, Lighting Settings의 직렬화 값
- `volume-profiles.json`: Volume Profile 23개의 컴포넌트·값·Override 상태
- `shader-inventory.json`: Shader Graph·Sub Graph·HLSL·Shader·VFX 파일과 의존 경로·GUID
- `shader-graph-features.json`: 그래프에 들어 있는 노드 유형과 프로퍼티 참조 이름
- `shader-materials.json`: 커스텀 셰이더를 사용하는 머티리얼 113개의 값·텍스처 참조·키워드
- `portable-presets.json`: Light 대표값 19개와 Volume Profile 23개를 가져오기 위한 데이터
- `EnvironmentTrainingDataImporter.cs`: 새 프리팹과 Volume Profile을 만드는 Editor 도구
- `import-validation.json`, `import-report.txt`: 생성·검수 결과와 복원하지 못한 항목

## 다른 프로젝트에서 가져오는 순서

1. URP를 사용하는 Unity 프로젝트에서 진행. 확인한 기준 버전은 Unity 6000.4.0f1 / URP 17.4.0임.
2. Package Manager에서 `com.unity.nuget.newtonsoft-json` 사용 가능 여부 확인. 원본 프로젝트는 3.2.2를 사용 중.
3. `EnvironmentTrainingDataImporter.cs`를 대상 프로젝트의 `Assets/Editor/`에 넣음.
4. 컴파일이 끝나면 `Tools > Environment Training Data > Import Presets` 실행.
5. 내려받은 `portable-presets.json` 선택.
6. 새 `Assets/EnvironmentTrainingData_시간/` 폴더의 `Lights`, `Volumes`, `ImportReport.txt` 확인.

기존 씬, Renderer, Graphics·Quality 설정을 자동으로 바꾸는 도구는 아님. 새 에셋만 생성하므로 필요한 프리팹과 Profile을 직접 골라 연결하면 됨.

Light는 씬별 광원 유형·Bake 모드 조합마다 강도가 가장 큰 항목 하나를 대표값으로 고름. 최적값이나 공통 권장값이 아님. 원본 회전·광원 강도·색·범위·그림자·색온도·Area Size 등을 보관하고 프리팹은 (0, 2, 0)에 생성함. 원래 씬 위치·오브젝트 스케일·Cookie·URP 추가 속성·애니메이션 제어 스크립트까지 자동으로 연결하지는 않음. 상세 원본 값은 씬 JSON에 남아 있음.

Volume은 대상 프로젝트에 있는 컴포넌트 유형만 생성할 수 있음. 원본 샘플의 `OasisFogVolumeComponent`, `OutlineVolumeComponent`가 없으면 건너뛰고 보고서에 기록함. 없는 텍스처 참조나 지원하지 않는 속성도 같은 방식으로 기록함. 숫자와 Override를 복원해도 실제 카메라 적용은 Volume의 범위·Weight·Priority·레이어와 카메라 설정을 맞춰야 함.

원본 프로젝트에서 생성한 결과는 Light 프리팹 19개, Volume Profile 23개. DefaultVolumeProfile의 ColorCurves 곡선 8개는 이 도구가 복원하지 못해 보고서에 남김. 베이크된 광원 효과는 씬 형상과 UV에 맞춰 다시 베이크해야 함.

## 원본 셰이더를 가져올 때

공개 다운로드는 설정과 참조 데이터, 새로 작성한 가져오기 도구로 구성함. 원본 셰이더·텍스처 파일을 이 폴더에 복제한 것은 아님. 셰이더는 원본 Unity URP 3D Sample과 기록된 경로·GUID를 기준으로 확보하고, 관련 Sub Graph·HLSL·텍스처·커스텀 패스·스크립트도 함께 확인해야 함.

원본 파일을 참고할 수 있는 공식 안내: https://unity.com/demos/urp-3d-sample

## 확인 범위

원본 프로젝트에서 에셋 생성과 다시 불러오기를 확인함. Terminal·Garden·Oasis 대표 광원 강도, HighQuality Bloom 0.25, TerminalRoom Post Exposure 2를 확인함. 별도 대상 프로젝트에서의 최종 렌더·성능·베이크 일치까지 검증한 결과는 아님.

## 출처·이용 조건 확인 상태

2026-11-03 확인: 원본 프로젝트 루트와 Assets에서 LICENSE·Third Party Notices 문서를 찾지 못함. 패키지별 라이선스를 환경 에셋 전체의 라이선스로 간주하지 않음.

이 보관물은 기술 비교용 로컬 참조 사본이며, 전체 에셋의 상용 이용·수정·재배포 권한을 확인 완료했다는 의미는 아님. 실제 채택 전에 원본 획득 경로와 파일별 이용 조건을 확인하고 출처·고지·수정 기록을 유지함. 수정한 파일도 원본의 이용 조건이 적용될 수 있음. 원본 셰이더·텍스처·unitypackage는 블로그 공개 ZIP에 포함하지 않음.

참고: https://unity.com/legal/licenses/unity-companion-license · https://unity.com/legal/as-terms

## 전체 프로젝트 재사용 후보 추가

- `reuse-catalog.md`: 광원·물·홀로그램·모니터·환경 VFX·연출·품질·편집 도구의 위치와 도입 조건.
- `project-asset-index.json`: Assets 전체의 상대 경로·파일 크기·확장자·meta 존재 여부. FBX 내부 서브에셋은 별도 집계하지 않음.

TPSControl 실습·외부 에셋도 전체 목록에는 포함됨. Unity 기본 환경 샘플의 출처·조건과 구분해서 사용함. 실제 반입·대상 프로젝트 렌더 검증 완료 목록은 아님.
