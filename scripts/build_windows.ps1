# Build AudiCode for Windows: venv + PyInstaller -> dist\AudiCode and dist\AudiCode-windows.zip
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not (Test-Path .venv-build)) { python -m venv .venv-build }
$py = ".\.venv-build\Scripts\python.exe"
& $py -m pip install --upgrade pip
& $py -m pip install -r requirements.txt pyinstaller pywebview
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }

& $py -m PyInstaller audicode.spec --noconfirm --clean
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }

$zip = "dist\AudiCode-windows.zip"
if (Test-Path $zip) { Remove-Item $zip }
Compress-Archive -Path "dist\AudiCode" -DestinationPath $zip
Write-Host "Built dist\AudiCode and $zip"
