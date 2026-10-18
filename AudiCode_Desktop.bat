@echo off
cd /d "%~dp0"
if exist "venv\Scripts\pythonw.exe" (
    start "" "venv\Scripts\pythonw.exe" "audicode_desktop.py"
) else (
    start "" pythonw "audicode_desktop.py"
)
