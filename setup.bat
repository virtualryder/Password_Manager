@echo off
REM SphereRyder Password Manager - Windows Setup Script
REM This script automates the installation and setup process

echo ========================================
echo SphereRyder Password Manager Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/5] Python found!
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment and install dependencies
echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Create data directory with proper permissions
echo [4/5] Setting up data directory...
if not exist "data" (
    mkdir data
    echo Data directory created.
)
echo.

REM Test the installation
echo [5/5] Testing installation...
python -c "from password_manager import PasswordManager; pm = PasswordManager(); print('✓ Installation test passed!')"
if errorlevel 1 (
    echo [ERROR] Installation test failed
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the Password Manager:
echo.
echo   CLI Mode:       run_cli.bat
echo   Web UI:         run_streamlit.bat
echo   Jupyter:        run_jupyter.bat
echo.
echo Pre-configured test accounts:
echo   Username: admin     Password: Admin@2024
echo   Username: testuser  Password: Test@2024
echo   Username: demo      Password: Demo@2024
echo.
pause
