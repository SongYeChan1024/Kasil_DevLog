# 작성자: 송예찬. 일반 터미널에서 남은 로컬 설치를 실행합니다. 자동 관리자 권한 상승은 하지 않습니다.
[CmdletBinding()]
param([string]$Workspace, [string]$ProjectPath, [switch]$WorkspaceOnly, [switch]$AdoptExisting)
$ErrorActionPreference = 'Stop'
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$manager = Join-Path $PSScriptRoot 'manage.py'
if (-not $Workspace) {
    if ($ProjectPath) { $Workspace = Split-Path -Parent (Resolve-Path -LiteralPath $ProjectPath).Path }
    else {
        $repoParent = (Get-Item -LiteralPath $PSScriptRoot).Parent.Parent.Parent
        $candidate = $repoParent
        while ($candidate -and -not (Test-Path -LiteralPath (Join-Path $candidate.FullName 'Management/projects.json'))) {
            $candidate = $candidate.Parent
        }
        $Workspace = if ($candidate) { $candidate.FullName } else { $repoParent.FullName }
    }
    if ($ProjectPath) { $ProjectPath = (Resolve-Path -LiteralPath $ProjectPath).Path }
}
$adoption = @()
if ($AdoptExisting) { $adoption += '--adopt-existing' }
if ($WorkspaceOnly) {
    if ($ProjectPath) { throw '-WorkspaceOnly와 -ProjectPath는 함께 사용할 수 없습니다.' }
    & python -X utf8 -B $manager sync --workspace $Workspace --workspace-only @adoption
    if ($LASTEXITCODE -ne 0) { throw '작업 공간 연결 설치 실패. 기존 파일 변경이 있으면 preview로 먼저 검토하세요.' }
    & python -X utf8 -B $manager check --workspace $Workspace --workspace-only
    if ($LASTEXITCODE -ne 0) { throw '작업 공간 연결 검증 실패.' }
    Write-Host "작업 공간 연결 파일 확인 완료. $Workspace 에서 새 세션의 /hooks를 확인하세요."
    Write-Host '설치·갱신 필요 프로젝트가 표시되면 해당 프로젝트의 설치·검증은 별도로 완료해야 합니다. 전체 갱신은 -WorkspaceOnly 없이 실행합니다.'
    return
}
$targets = if ($ProjectPath) { @('--project-path', $ProjectPath) } else { @('--global') }
& python -X utf8 -B $manager sync --workspace $Workspace @targets @adoption
if ($LASTEXITCODE -ne 0) { throw '일부 설치가 실패했습니다. 위 결과와 백업 경로를 확인하세요.' }
& python -X utf8 -B $manager check --workspace $Workspace @targets
if ($LASTEXITCODE -ne 0) { throw '설치 파일 검증에 실패했습니다.' }
$registry = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Workspace '.agent-rules/workspace.json') | ConvertFrom-Json
foreach ($folder in $registry.projects.PSObject.Properties.Name) {
    $docs = Join-Path $Workspace $folder
    if ($ProjectPath -and (Resolve-Path -LiteralPath $docs).Path -ne (Resolve-Path -LiteralPath ([IO.Path]::Combine($Workspace, $ProjectPath))).Path) { continue }
    $policy = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $docs '.agent-rules/policy.json') | ConvertFrom-Json
    if ($policy.profile -ne 'ergo-docs' -or -not (Test-Path -LiteralPath (Join-Path $docs 'requirements-docs.txt'))) { continue }
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
