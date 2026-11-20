# 작성자: 송예찬. 일반 터미널에서 남은 로컬 설치를 실행합니다. 자동 관리자 권한 상승은 하지 않습니다.
[CmdletBinding()]
param([string]$Workspace = 'C:\GitHubProjects')
$ErrorActionPreference = 'Stop'
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$manager = Join-Path $PSScriptRoot 'manage.py'
$dob = Join-Path $Workspace 'Project_DOB'
if (Test-Path -LiteralPath (Join-Path $dob '.git')) {
    $branch = (& git -C $dob branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'DOB 브랜치를 확인하지 못했습니다.' }
    if ($branch -eq 'main') {
        $changes = & git -C $dob status --porcelain
        if ($changes) { throw 'DOB main에 미커밋 변경이 있습니다. 보존한 뒤 backend 브랜치에서 다시 실행하세요.' }
        & git -C $dob switch backend
        if ($LASTEXITCODE -ne 0) { throw 'DOB backend 전환 실패. 변경을 덮어쓰지 않았습니다.' }
    }
}
& python -X utf8 -B $manager sync --workspace $Workspace --global --adopt-existing
if ($LASTEXITCODE -ne 0) { throw '일부 설치가 실패했습니다. 위 결과와 백업 경로를 확인하세요.' }
& python -X utf8 -B $manager check --workspace $Workspace --global
if ($LASTEXITCODE -ne 0) { throw '설치 파일 검증에 실패했습니다.' }
$docs = Join-Path $Workspace 'Document_ERGOSQUARE-ARCHITECT'
if (Test-Path -LiteralPath (Join-Path $docs 'requirements-docs.txt')) {
    $venv = Join-Path $docs '.agent-rules/.cache/venv'
    $venvPython = Join-Path $venv 'Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $venvPython)) {
        & python -m venv $venv
        if ($LASTEXITCODE -ne 0) { throw '문서 검사용 가상 환경을 만들지 못했습니다.' }
    }
    & $venvPython -m pip install -r (Join-Path $docs 'requirements-docs.txt')
    if ($LASTEXITCODE -ne 0) { throw '문서 검사 의존성 설치 실패. 네트워크 연결 후 다시 실행하세요.' }
    & $venvPython (Join-Path $docs 'docs/validate_consolidation.py')
    if ($LASTEXITCODE -ne 0) { throw '문서 링크 검사에 실패했습니다.' }
}
Write-Host '파일 설치·동기화 확인 완료. 새 Codex/Claude 세션에서 /hooks를 열어 훅을 검토·활성화하세요.'
Write-Host 'Native Windows의 Claude OS 샌드박스와 클라우드 계정 설정은 이 스크립트가 활성화하지 않습니다.'
