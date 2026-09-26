param(
    [ValidateSet("windows", "linux", IgnoreCase = $true)]
    [string]$Target = "windows"
)

$ErrorActionPreference = "Stop"

$Target = $Target.ToLower()
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "=== Building YouTube Downloader for target: $Target ===" -ForegroundColor Cyan

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found. Installing via pip..." -ForegroundColor Yellow
    pip install pyinstaller
}

$IconFlag = ""
if (Test-Path "yt.ico") {
    if ($Target -eq "windows") {
        $IconFlag = '--icon=yt.ico --add-data "yt.ico;."'
    } else {
        $IconFlag = '--icon=yt.ico --add-data "yt.ico:."'
    }
}

switch ($Target) {
    "windows" {
        Write-Host "Building Windows standalone executable..." -ForegroundColor Green
        Invoke-Expression "pyinstaller --noconfirm --onefile --windowed --name `"YouTubeDownloader`" $IconFlag main.py"
        Write-Host "Build complete: dist/YouTubeDownloader.exe" -ForegroundColor Green
    }
    "linux" {
        Write-Host "Building Linux executable..." -ForegroundColor Green
        Invoke-Expression "pyinstaller --noconfirm --onefile --windowed --name `"YouTubeDownloader`" $IconFlag main.py"
        Write-Host "Build complete: dist/YouTubeDownloader" -ForegroundColor Green
    }
}
