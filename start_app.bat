@echo off
title IQ-EQ Unified Agent Mesh

echo ==========================================
echo Starting IQ-EQ Agent Mesh (Backend + Frontend)
echo ==========================================

cd /d "%~dp0"

REM Create virtual environment if it does not exist
if not exist ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing requirements...
pip install -r requirements.txt

REM Start the browser to point to the frontend
echo [INFO] Opening dashboard in your default browser...
start http://127.0.0.1:8010/

REM Start the FastAPI application (serves both backend and static frontend)
echo [INFO] Starting FastAPI Uvicorn Server...
echo Press Ctrl+C to stop the server at any time.
echo ==========================================

python -m uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload

pause
