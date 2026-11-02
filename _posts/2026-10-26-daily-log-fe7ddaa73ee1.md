---
title: "2026-10-26 데일리 로그 애프터 세컨즈 연구소 시안과 Unity 계층 분리"
date: 2026-10-26 12:00:00 +0900
categories: ["데일리로그"]
tags: ["Notion 이전", "CSharp"]
excerpt: "After Seconds 연구소 시안을 정리하고, Unity에서 여섯 폴더와 어셈블리 정의를 만들어 계층별 참조 경계를 구성했다."
description: "After Seconds 연구소 시안을 정리하고, Unity에서 여섯 폴더와 어셈블리 정의를 만들어 계층별 참조 경계를 구성했다."
published: true
migration_id: "40536532580e81e2ab76fe7ddaa73ee1"
migration_status: "published"
migration_flags: []
---

{% raw %}
## 기록 정보

- 작업일: 2026-10-26
- 작성자: 송예찬
- 프로젝트: 개인 프로젝트 「After Seconds(애프터 세컨즈)」
- 기획서: V0.09
- 환경: Unity 6000.4.0f1 / URP 17.4.0
- 기록 범위: 오늘 앞선 연구소·에셋·개발 준비 기록과 집에서 진행한 계층 분리 작업. 앞선 작업은 저장소의 기존 개발 일지와 인수인계 기록을 기준으로 정리했다.

## 오늘 한 일

- 연구소 전체 외관·지하 단면과 6개 층 평면도 시안을 정리하고 기획서를 V0.09까지 갱신했다. 기존 방별 좌표·SVG를 유지하고 전체 시안의 치수는 가안으로 구분했다.
- 부위별 모듈 제작, 공통 STYLE과 개별 OBJECT를 나누는 프롬프트 원칙을 정리했다. 바르코에서 장비·문 부품 및 회색 플레이어·주황 경비 더미를 포함한 에셋 후보 6종을 생성했다. 후보의 Unity 반입·치수·리깅·충돌 검수는 남아 있다.
- 참고 프로젝트의 계층과 실제 어셈블리 참조를 분석하고, 순수 데이터와 Simulation을 Unity 어댑터에서 분리하는 학습 순서를 정했다.
- 집에서 git pull --ff-only로 main을 013564f까지 갱신하고 프로젝트의 최신 기획·인수인계를 읽었다.
- Define / Simulator / System / UI / Manager / Presenter 여섯 폴더와 asmdef를 직접 만들었다.
- DefineAD와 SimulatorAD에서 No Engine References를 켰다. SimulatorAD가 DefineAD를 참조하도록 지정하고 Apply로 저장했다.
- SampleScene을 작업 루트의 01.Scenes로 옮겼다. 씬 GUID를 유지하고 빌드 설정의 씬 경로도 새 위치로 갱신했다.

## 발생한 문제와 처리

폴더를 나누는 것과 코드 참조 경계를 만드는 것은 별개였다. 처음 확인한 asmdef에는 이름만 저장되어 있었고 참조·엔진 의존 설정은 기록되지 않았다. DefineAD와 SimulatorAD의 옵션 및 참조를 설정하고 다시 읽어 실제 저장 여부를 확인했다.

역할도 구체적인 예로 구분했다. Simulation은 교환 결과와 위치 데이터를 계산하고, System은 결과를 Unity Transform에 반영한다. Manager는 세션의 생성·종료·재시작을 맡고, Presenter는 요청·규칙·표시를 연결한다.

## 오늘의 결정

- 지금 우선순위는 계층 분리와 기초 데이터 설계다. A안과 B안의 최종 선택은 프로토타입으로 비교한 뒤 한다.
- 직접 분석 → 의사코드 → 작은 구현 → 확인 순서로 배운다. Codex는 설계 검토와 질문 대응을 맡고 게임 로직을 미리 전부 구현하지 않는다.
- 일일개발일지는 이제 블로그 Git 저장소 Kasil-portfolio-pages의 \_posts에 작성한다. 프로젝트의 Docs/개발\_일지는 기존 기록과 새 글 링크를 보관한다.
- 데일리로그는 계속 노션 Logs For Develope에 작성하고, 프로젝트에는 다음 세션 인수인계를 남긴다.

## 검증과 남은 범위

- 파일로 확인: asmdef 6개 생성, DefineAD·SimulatorAD의 noEngineReferences=true, SimulatorAD → DefineAD의 유효한 meta GUID 참조.
- 파일로 확인: 씬 이동 후 기존 GUID 보존 및 빌드 설정 경로 갱신.
- 나머지 네 asmdef의 참조는 현재 비어 있다. 실제 코드에서 필요해질 때 허용 참조표에 맞춰 추가한다.
- 새 게임 C# 코드는 없다. Define 데이터와 예약 큐·교환 규칙은 아직 작성 전이다.
- Unity Console 오류 유무·실제 컴파일·플레이 실행은 이번 세션에서 확인하지 않았다.

## 다음 시작점

1. Unity Console 오류 유무를 확인한다.
2. Define에서 대상 ID·상태·위치·규칙 설정·예약 데이터에 필요한 최소 필드를 직접 적고 이유를 설명한다.
3. 데이터 역할을 정리한 뒤 ScheduleSwap / AdvanceTo / ExecuteSwap 의사코드를 작성한다.
4. 같은 시각의 예약 순서, 2.9초에서 3.2초로 넘어간 tick, 움직이거나 사라진 대상, 손에 든 대상 취소, 재시작 초기화를 검토한다.
5. 작은 예약·교환 구현으로 확인한 뒤 다음 기능으로 진행한다.

## 관련 자료

- [블로그 일일개발일지](https://songyechan1024.github.io/Kasil-portfolio-pages/posts/after-seconds-unity-assembly-setup/)
- [블로그 Git 원문](https://github.com/SongYeChan1024/Kasil-portfolio-pages/blob/main/_posts/2026-10-26-after-seconds-unity-assembly-setup.md)
- 블로그 게시 검증: 커밋 <code>84d00c2</code>, Jekyll 빌드 및 [GitHub Actions Build and Deploy](https://github.com/SongYeChan1024/Kasil-portfolio-pages/actions/runs/40341485426) 성공.
- [프로젝트 저장소](https://github.com/SongYeChan1024/After_Seconds)
- 프로젝트 인수인계: <code>Docs/이어하기_2026-10-26.md</code>
- 계층 설계·학습 자료: <code>Docs/Unity_계층_설계와_학습_순서.md</code>
{% endraw %}
