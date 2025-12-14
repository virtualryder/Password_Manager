@echo off
REM Run SphereRyder Password Manager - Jupyter Notebook Tutorial

echo Starting Jupyter Notebook...
echo.
echo The notebook will open in your browser
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run Jupyter Notebook
jupyter notebook password_manager_tutorial.ipynb

REM Deactivate when done
deactivate
