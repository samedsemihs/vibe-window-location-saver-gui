@echo off
setlocal enabledelayedexpansion

:: Configuration
set "APP_NAME=ScreenLocSaver"
set "INSTALL_DIR=%LOCALAPPDATA%\%APP_NAME%"
set "STARTMENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "LANG=en"

:: Try to detect language from config
if exist "%INSTALL_DIR%\config.json" (
    for /f "tokens=2 delims=:}" %%a in ('type "%INSTALL_DIR%\config.json" ^| findstr "language"') do (
        set "DETECTED=%%a"
        set "DETECTED=!DETECTED:"=!"
        set "DETECTED=!DETECTED: =!"
        if "!DETECTED!"=="tr" set "LANG=tr"
    )
)

:: Set messages based on language
if "%LANG%"=="tr" (
    set "MSG_TITLE=Screen Location Saver - Kaldirma"
    set "MSG_NOT_INSTALLED=Uygulama kurulu degil."
    set "MSG_LOCATION=Konum"
    set "MSG_STEP1=Uygulama kapatiliyor..."
    set "MSG_STEP2=Windows baslangictan kaldiriliyor..."
    set "MSG_STEP3=Start Menu kisayolu kaldiriliyor..."
    set "MSG_LAYOUTS_LOC=Layout dosyalariniz"
    set "MSG_DELETE_ALL=Tum dosyalari silmek ister misiniz? (E/H)"
    set "MSG_STEP4=Dosyalar kaldiriliyor..."
    set "MSG_ALL_DELETED=Tum dosyalar silindi."
    set "MSG_EXE_DELETED=EXE silindi, layout'lar korundu."
    set "MSG_LAYOUTS_FOLDER=Layout klasoru"
    set "MSG_DONE=Kaldirma tamamlandi!"
    set "YES_CHAR=E"
) else (
    set "MSG_TITLE=Screen Location Saver - Uninstall"
    set "MSG_NOT_INSTALLED=Application is not installed."
    set "MSG_LOCATION=Location"
    set "MSG_STEP1=Closing application..."
    set "MSG_STEP2=Removing from Windows startup..."
    set "MSG_STEP3=Removing Start Menu shortcut..."
    set "MSG_LAYOUTS_LOC=Your layout files"
    set "MSG_DELETE_ALL=Delete all files? (Y/N)"
    set "MSG_STEP4=Removing files..."
    set "MSG_ALL_DELETED=All files deleted."
    set "MSG_EXE_DELETED=EXE deleted, layouts preserved."
    set "MSG_LAYOUTS_FOLDER=Layouts folder"
    set "MSG_DONE=Uninstall complete!"
    set "YES_CHAR=Y"
)

echo ============================================
echo   %MSG_TITLE%
echo ============================================
echo.

:: Check if installed
if not exist "%INSTALL_DIR%" (
    echo [!] %MSG_NOT_INSTALLED%
    echo     %MSG_LOCATION%: %INSTALL_DIR%
    pause
    exit /b 0
)

:: Kill running process
echo [1/4] %MSG_STEP1%
taskkill /f /im "%APP_NAME%.exe" >nul 2>&1

:: Remove from Windows startup
echo [2/4] %MSG_STEP2%
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" /f >nul 2>&1

:: Remove Start Menu shortcut
echo [3/4] %MSG_STEP3%
if exist "%STARTMENU_DIR%\%APP_NAME%.lnk" del "%STARTMENU_DIR%\%APP_NAME%.lnk" >nul 2>&1

:: Ask about layouts
echo.
echo   %MSG_LAYOUTS_LOC%: %INSTALL_DIR%\layouts
echo.
set /p "DELETE_ALL=%MSG_DELETE_ALL% "

echo [4/4] %MSG_STEP4%
if /i "%DELETE_ALL%"=="%YES_CHAR%" goto :delete_all
if /i "%DELETE_ALL%"=="Y" goto :delete_all
if /i "%DELETE_ALL%"=="E" goto :delete_all
goto :keep_layouts

:delete_all
rmdir /s /q "%INSTALL_DIR%" >nul 2>&1
echo        %MSG_ALL_DELETED%
goto :done

:keep_layouts
del "%INSTALL_DIR%\%APP_NAME%.exe" >nul 2>&1
del "%INSTALL_DIR%\config.json" >nul 2>&1
echo        %MSG_EXE_DELETED%
echo        %MSG_LAYOUTS_FOLDER%: %INSTALL_DIR%\layouts

:done
echo.
echo ============================================
echo   %MSG_DONE%
echo ============================================
echo.

pause
endlocal
