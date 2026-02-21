@echo off
REM ============================================================================
REM BRD Agent - One-Click Launcher (Windows)
REM ============================================================================

ECHO ============================================================================
ECHO   BRD AGENT - HACKATHON LAUNCHER
ECHO   Starting Streamlit Application...
ECHO ============================================================================

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Python is not installed or not in your PATH.
    PAUSE
    EXIT /B
)

REM Check if dependencies are installed (simple check for streamlit)
python -c "import streamlit" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Installing dependencies first...
    pip install -r requirements_brd.txt
    
    ECHO Initializing database...
    python -c "from brd_agent.db_setup import init_database; init_database()"
    python -c "from brd_agent.data_ingest import load_sample_data; load_sample_data()"
)

ECHO.
ECHO Launching Streamlit Frontend...
ECHO (Press Ctrl+C to stop)
ECHO.

streamlit run brd_agent/frontend.py

PAUSE
