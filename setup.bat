@echo off
echo.
echo  NUST FAQ Chatbot  —  Setup
echo  ─────────────────────────────────────────
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Install Python 3.10+ first.
    pause
    exit /b 1
)

REM Create venv if it doesn't exist
if not exist "venv\" (
    echo  [1/3] Creating virtual environment...
    python -m venv venv
) else (
    echo  [1/3] Virtual environment already exists, skipping.
)

REM Activate and install
echo  [2/3] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet

echo  [3/3] Setup complete.
echo.
echo  To start the chatbot, run:
echo      python app.py
echo.
pause
