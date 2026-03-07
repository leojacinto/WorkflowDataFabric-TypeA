@echo off
REM ============================================================
REM Demo Hub WDF Lab Instance Prep — Windows Launcher
REM ============================================================
REM This script checks for Python 3, installs dependencies,
REM and launches the web UI in your browser.
REM ============================================================

echo.
echo   ================================================
echo   Demo Hub WDF Lab — Instance Prep
echo   ================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%.venv"
set "REQUIREMENTS=%SCRIPT_DIR%requirements.txt"
set "APP=%SCRIPT_DIR%demo_hub_prep.py"

REM --- Check Python 3 ---
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo   Python 3 is not installed.
    echo.
    echo   Attempting to install via winget...
    winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    if %errorlevel% neq 0 (
        echo.
        echo   Could not auto-install Python. Please install manually:
        echo     https://www.python.org/downloads/
        echo.
        echo   After installing, re-run this script.
        pause
        exit /b 1
    )
    echo   Python installed. You may need to restart this script.
    echo   Press any key to continue...
    pause >nul
)

REM --- Verify Python version ---
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PY_VER=%%i
echo   Using: %PY_VER%

REM --- Create virtual environment if needed ---
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo   Setting up environment (first run only^)...
    python -m venv "%VENV_DIR%"
)

REM --- Activate venv and install dependencies ---
call "%VENV_DIR%\Scripts\activate.bat"
pip install -q --upgrade pip 2>nul
pip install -q -r "%REQUIREMENTS%" 2>nul
echo   Dependencies ready.
echo.

REM --- Run the app ---
python "%APP%"

pause
