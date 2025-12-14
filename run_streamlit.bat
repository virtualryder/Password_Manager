@echo off
REM Run SphereRyder Password Manager - Streamlit Web UI

echo Starting Password Manager Web Interface...
echo.
echo The web interface will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run Streamlit
streamlit run streamlit_app.py

REM Deactivate when done
deactivate
