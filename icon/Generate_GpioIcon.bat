@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Script Name: Generate_GpioIcon.bat
:: Function: Resize PNG to 16/32/48/256 sizes (simplified filenames), merge to ICO, and delete intermediate PNGs
:: Feature: Dynamic working dir (script's location), auto-delete intermediate files after successful ICO generation

:: ======================== Configuration ========================
set "SOURCE_PNG=GpioCalculator.png"  :: Source PNG in script's directory
set "ICO_OUTPUT=icon.ico"            :: Final ICO file name
set "ICON_SIZES=16x16 32x32 48x48 256x256"  :: Icon sizes to generate
set "MERGE_FILES=icon-16.png icon-32.png icon-48.png icon-256.png"  :: Intermediate PNG files
:: Dynamic target dir: use the directory where this bat script is located
set "TARGET_DIR=%~dp0"
:: ==============================================================

echo ======================== Start GPIO Icon Generation ========================
echo Source PNG: %SOURCE_PNG%
echo Target Dir (script's location): %TARGET_DIR%
echo.

:: Step 1: Check ImageMagick
magick --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ImageMagick not found! Download: https://imagemagick.org/script/download.php#windows
    pause
    exit /b 1
)

:: Step 2: Switch to script's directory
cd /d "%TARGET_DIR%" >nul 2>&1
echo [INFO] Working dir (script's location): %cd%

:: Step 3: Check source PNG
if not exist "%SOURCE_PNG%" (
    echo [ERROR] Source PNG missing in script directory: %SOURCE_PNG%
    echo Please put GpioCalculator.png in the same folder as this bat script!
    pause
    exit /b 1
)

:: Step 4: Resize to simplified filenames (icon-16.png, icon-32.png, etc.)
for %%s in (%ICON_SIZES%) do (
    :: Extract size number (e.g., 16 from 16x16, 32 from 32x32)
    for /f "tokens=1 delims=x" %%n in ("%%s") do (
        set "RESIZED_PNG=icon-%%n.png"
        echo [INFO] Resizing to %%s -> !RESIZED_PNG!
        magick "%SOURCE_PNG%" -resize %%s "!RESIZED_PNG!"
        
        :: Check if resized PNG is generated
        if not exist "!RESIZED_PNG!" (
            echo [ERROR] Resized file NOT generated: !RESIZED_PNG!
            echo Possible reasons: Source PNG corrupted / ImageMagick error / Permission denied
            pause
            exit /b 1
        )
        echo [SUCCESS] Generated: !RESIZED_PNG!
    )
)

:: Step 5: Check all merge files before ICO creation
echo.
echo [INFO] Checking merge files...
for %%f in (%MERGE_FILES%) do (
    if not exist "%%f" (
        echo [ERROR] Merge file missing: %%f
        pause
        exit /b 1
    )
    echo [INFO] Found merge file: %%f
)

:: Step 6: Merge to ICO (with detailed error output)
echo.
echo [INFO] Merging to ICO: %ICO_OUTPUT%
magick %MERGE_FILES% "%ICO_OUTPUT%" 2> magick_error.log
if errorlevel 1 (
    echo [ERROR] Failed to merge ICO! Check error log: magick_error.log
    echo Open magick_error.log to see detailed ImageMagick error.
    pause
    exit /b 1
)

:: Step 7: Final validation and auto-delete intermediate files
if exist "%ICO_OUTPUT%" (
    echo.
    echo [SUCCESS] ICO generated: %cd%\%ICO_OUTPUT%
    :: Delete intermediate PNG files
    echo [INFO] Deleting intermediate PNG files...
    del /q %MERGE_FILES% >nul 2>&1
    if errorlevel 0 (
        echo [SUCCESS] Deleted intermediate files: %MERGE_FILES%
    ) else (
        echo [WARNING] Failed to delete some intermediate files (may be in use)
    )
    :: Delete error log if success
    del /q magick_error.log >nul 2>&1
) else (
    echo [ERROR] ICO file not found after merge!
    pause
    exit /b 1
)

echo.
echo ======================== Generation Completed ========================
echo Only final file retained: %ICO_OUTPUT%
pause
endlocal
exit /b 0