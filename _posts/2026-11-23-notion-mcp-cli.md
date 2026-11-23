---
title: "Codex와 Claude Code에서 팀 Notion 기획서 읽기"
date: 2026-11-23 17:00:00 +0900
categories: [기술 스택, 협업 도구]
tags: [Notion, MCP, Codex, Claude Code, OAuth]
---

팀 기획서를 보면서 코드를 확인할 때마다 Notion 앱이 앞으로 튀어나왔음. 원했던 건 작업하던 창을 그대로 두고 터미널에서 기획서 한 문장을 확인하는 것. 그래서 두 CLI를 Notion이 운영하는 MCP 서버에 직접 연결해 봄.

## 두 CLI에 같은 서버 등록하기

Windows PowerShell에서 사용한 버전은 Codex CLI 0.171.0과 Claude Code 2.1.330. 둘 다 서버 주소는 `https://mcp.notion.com/mcp`를 씀.

```powershell
codex mcp add notion --url https://mcp.notion.com/mcp
claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp
```

Codex는 등록하자마자 OAuth 인증을 시작했음. Claude의 `--scope user`는 이 PC의 내 계정으로 여는 다른 프로젝트에서도 같은 설정을 쓰게 해 줌. Claude 인증은 대화형 터미널에서 아래 명령으로 진행함.

```powershell
claude mcp login notion
```

Codex에서 다시 인증할 때는 `codex mcp login notion`을 씀. 브라우저가 열리면 **워크스페이스 선택** 아래에 현재 공간의 이름이 보임. 팀 문서를 작업하려면 그 이름을 눌러 팀 공간으로 바꾸고 **계속하기**를 누르면 됨. Codex와 Claude가 각각 인증 창을 열기 때문에 두 번 모두 확인함. [Notion 공식 연결 가이드](https://developers.notion.com/guides/mcp/get-started-with-mcp)

## 로그인 뒤에 원본 링크로 한 번 더 확인한 이유

`codex mcp list`에서 `OAuth`, `claude mcp get notion`에서 `Connected`가 뜨는 것까지 확인함. 그런데 새 CLI 세션에서 팀 기획서 주소를 읽어 달라고 하니 처음엔 양쪽 다 `object_not_found`가 나왔음. 같은 제목을 검색하면 개인 공간에 만들어 둔 복사본은 잘 나왔음.

이때 확인하기 좋았던 건 제목과 링크였음. Notion에서 원본 페이지의 링크를 복사한 뒤 새 CLI 세션에 이렇게 요청하면 됨.

> Notion MCP로 이 페이지를 직접 열고 페이지 제목과 첫 소제목 하나만 알려줘. 열리지 않으면 오류 코드를 알려줘.

팀 공간으로 다시 인증하고 같은 링크를 보냈더니 Codex는 원본의 제목과 첫 소제목을 돌려줬고, Claude Code에서도 같은 페이지의 본문을 가져왔음. 두 터미널에서 문서를 확인하는 동안 Notion 데스크톱 창을 열 필요가 없었음.
