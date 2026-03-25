@echo off
echo ============================================
echo   Screen Location Saver - Build
echo ============================================
echo.

:: Install Python dependencies
echo [1/2] Installing dependencies / Paketler kuruluyor...
pip install -r "%~dp0requirements.txt" pyinstaller --quiet
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed / pip install basarisiz!
    pause
    exit /b 1
)

:: Build exe
echo [2/2] Building EXE / EXE olusturuluyor...
python "%~dp0build_exe.py"
if %errorlevel% neq 0 (
    echo [ERROR] Build failed / Build basarisiz!
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Build complete / Build tamamlandi!
echo ============================================
echo   EXE: %~dp0dist\ScreenLocSaver.exe
echo.
echo   To install / Kurmak icin: install.bat
echo.
