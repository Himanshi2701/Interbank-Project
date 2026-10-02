@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python and try again.
    pause
    exit /b 1
)

py -m streamlit run app.py
if errorlevel 1 (
    echo.
    echo Streamlit is not installed in this Python environment.
    echo Install dependencies with: py -m pip install -r requirements.txt
    pause
)