@echo off
setlocal
cd /d "%~dp0"

python -c "from pathlib import Path; p=Path.cwd(); raise SystemExit('ERROR: move this project to an ASCII-only path: ' + str(p)) if not str(p).isascii() else None"
if errorlevel 1 exit /b 1

if not exist .venv (
    python -m venv .venv
    if errorlevel 1 exit /b 1
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Setup complete. Run: .venv\Scripts\python main.py
endlocal