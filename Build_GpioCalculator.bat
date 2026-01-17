@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Script Name: Build_GpioCalculator.bat
:: Function: Package GpioCalculator.py to single EXE with PyInstaller
:: Feature: Check Python/PyInstaller installation, auto-install PyInstaller if missing

:: ======================== Configuration ========================
set "PY_SCRIPT_NAME=GpioCalculator.py"  :: Main Python script file
set "EXE_NAME=GpioCalculator"           :: Output EXE name
set "ICON_PATH=icon/icon.ico"           :: Icon file path (relative to script directory)
:: ==============================================================

echo ======================== Start Building GpioCalculator EXE ========================
echo Working Directory: %~dp0
echo Target EXE Name: %EXE_NAME%
echo.

:: Step 1: Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is NOT installed!
    echo Please download and install Python first:
    echo Official Download URL: https://www.python.org/downloads/
    echo NOTE: Check "Add Python to PATH" during installation!
    pause
    exit /b 1
)
echo [SUCCESS] Python is installed.

:: Step 2: Check if PyInstaller is installed, auto-install if missing
echo.
echo [INFO] Checking PyInstaller installation...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PyInstaller not found, installing automatically...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller! Please install manually: pip install pyinstaller
        pause
        exit /b 1
    )
)
echo [SUCCESS] PyInstaller is installed.

:: Step 3: Execute PyInstaller package command
echo.
echo [INFO] Starting to package EXE file...
pyinstaller --onefile --windowed --icon="%~dp0%ICON_PATH%" --add-data="%~dp0%ICON_PATH%;." --name "%EXE_NAME%" "%~dp0%PY_SCRIPT_NAME%"

:: Step 4: Check package result
if errorlevel 0 (
    echo.
    echo [SUCCESS] EXE packaged successfully!
    echo Output path: %~dp0dist\%EXE_NAME%.exe
    echo NOTE: The EXE file is in the "dist" folder of current directory.
) else (
    echo.
    echo [ERROR] Failed to package EXE! Please check the error message above.
)

echo.
echo ======================== Build Process Completed ========================
pause
endlocal
exit /b 0