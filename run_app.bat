@echo off
echo Philippine Utility Tools - Setup and Run Script
echo =============================================

echo Checking for Python installation...
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Installing required packages...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install required packages.
    pause
    exit /b 1
)

echo Downloading NLTK resources...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
if %ERRORLEVEL% NEQ 0 (
    echo Failed to download NLTK resources.
    pause
    exit /b 1
)

echo Starting the application...
python app.py
if %ERRORLEVEL% NEQ 0 (
    echo Failed to start the application.
    pause
    exit /b 1
)

pause