@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto installed
echo Creating a local Python environment...
py -3 -m venv .venv
if errorlevel 1 python -m venv .venv
if not exist ".venv\Scripts\python.exe" (
  echo Install Python 3.11 or newer, then run this launcher again.
  pause
  exit /b 1
)
:installed
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependencies could not be installed. Check your internet connection.
  pause
  exit /b 1
)
echo Starting SYSTEM. Keep this window open while studying.
".venv\Scripts\python.exe" run_laptop.py
pause
