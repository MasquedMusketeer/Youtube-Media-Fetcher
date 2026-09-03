@echo off
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing via winget...
    winget install --id Python.Python.3 -e --silent
    if %errorlevel% neq 0 (
        echo Failed to install Python. Please install it manually from https://www.python.org
        pause
        exit /b 1
    )
    echo Python installed. Relaunch the app.
    pause
    exit /b 0
)
python "%~dp0downloader.py"
