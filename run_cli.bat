@echo off
REM Run SphereRyder Password Manager - CLI Interface

echo Starting Password Manager CLI...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the CLI application
python cli_interface.py

REM Deactivate when done
deactivate
