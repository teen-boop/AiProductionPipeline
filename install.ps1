# Installs every skill in skills\ of this repository into a Claude Code skills folder.
# Windows PowerShell / PowerShell 7+ version of install.sh.
#
# Usage:
#   .\install.ps1                        Installs globally, into %USERPROFILE%\.claude\skills
#   .\install.ps1 -Dest "C:\path\to\project"   Installs scoped to one project,
#                                               into C:\path\to\project\.claude\skills
#
# If PowerShell refuses to run this script (execution policy), run it as:
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#
# Safe to re-run: each skill folder is overwritten with the version in
# this bundle, so re-running after pulling an updated version brings an
# existing install up to date.

param(
    [string]$Dest = ""
)

$ScriptDir = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "skills"

if ($Dest -ne "") {
    $TargetDir = Join-Path $Dest ".claude\skills"
    $Scope = "project ($Dest)"
} else {
    $TargetDir = Join-Path $HOME ".claude\skills"
    $Scope = "global (all projects)"
}

New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

Write-Host "Installing skills from: $ScriptDir"
Write-Host "Installing into:        $TargetDir"
Write-Host "Scope:                  $Scope"
Write-Host ""

$installed = 0
$skipped = 0

Get-ChildItem -Path $ScriptDir -Directory | ForEach-Object {
    $skillDir = $_.FullName
    $name = $_.Name
    $skillMd = Join-Path $skillDir "SKILL.md"

    if (-not (Test-Path $skillMd)) {
        $script:skipped++
        return
    }

    $destPath = Join-Path $TargetDir $name
    if (Test-Path $destPath) {
        Remove-Item -Recurse -Force $destPath
    }
    Copy-Item -Recurse -Force $skillDir $destPath
    Write-Host "  + $name"
    $script:installed++
}

Write-Host ""
Write-Host "Done: $installed skill(s) installed, $skipped non-skill folder(s) skipped."
Write-Host "Restart Claude Code (or start a new session) to pick them up."
