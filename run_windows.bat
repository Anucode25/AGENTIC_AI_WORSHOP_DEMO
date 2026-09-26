@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
  if errorlevel 1 (
    echo Install Python 3.11 and try again.
    pause
    exit /b 1
  )
)
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
if not exist ".env" copy ".env.example" ".env" >nul
".venv\Scripts\python.exe" demo.py
pause
