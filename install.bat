@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Screen Location Saver - Setup / Kurulum
echo ============================================
echo.

:: Configuration
set "APP_NAME=ScreenLocSaver"
set "INSTALL_DIR=%LOCALAPPDATA%\%APP_NAME%"
set "EXE_NAME=%APP_NAME%.exe"
set "SOURCE_EXE=%~dp0dist\%EXE_NAME%"
set "STARTMENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs"

:: Check if exe exists
if not exist "%SOURCE_EXE%" (
    echo [!] EXE not found / EXE bulunamadi: %SOURCE_EXE%
    echo     Run build.bat first / Once build.bat calistirin.
    echo.
    pause
    exit /b 1
)

:: Language selection
echo   Select language / Dil secin:
echo.
echo   [1] English
echo   [2] Turkce
echo.
set /p "LANG_CHOICE=Enter / Girin (1/2): "

if "%LANG_CHOICE%"=="1" (
    set "LANG=en"
    set "MSG_STEP1=Creating installation folder..."
    set "MSG_STEP2=Copying application..."
    set "MSG_COPY_LAYOUTS=Copying default layouts..."
    set "MSG_KEEP_LAYOUTS=Keeping existing layouts..."
    set "MSG_STEP3=Adding to Windows startup..."
    set "MSG_STEP4=Creating Start Menu shortcut..."
    set "MSG_DONE=Installation complete!"
    set "MSG_LOCATION=Location"
    set "MSG_INFO1=Starts automatically with Windows"
    set "MSG_INFO2=Loads 'default' layout"
    set "MSG_INFO3=Find '%APP_NAME%' in Start Menu"
    set "MSG_UNINSTALL=To uninstall: uninstall.bat"
    set "MSG_RUN_NOW=Start now? (Y/N)"
    set "MSG_COPY_FAIL=Copy failed! App might be running."
    set "MSG_CLOSE_RETRY=Close the app and try again."
) else (
    set "LANG=tr"
    set "MSG_STEP1=Kurulum klasoru olusturuluyor..."
    set "MSG_STEP2=Uygulama kopyalaniyor..."
    set "MSG_COPY_LAYOUTS=Varsayilan layout'lar kopyalaniyor..."
    set "MSG_KEEP_LAYOUTS=Mevcut layout'lar korunuyor..."
    set "MSG_STEP3=Windows baslangicina ekleniyor..."
    set "MSG_STEP4=Start Menu kisayolu olusturuluyor..."
    set "MSG_DONE=Kurulum tamamlandi!"
    set "MSG_LOCATION=Konum"
    set "MSG_INFO1=Windows baslangicinda otomatik calisir"
    set "MSG_INFO2='default' layout'unu yukler"
    set "MSG_INFO3=Start Menu'de '%APP_NAME%' olarak bulabilirsiniz"
    set "MSG_UNINSTALL=Kaldirmak icin: uninstall.bat"
    set "MSG_RUN_NOW=Simdi baslatmak ister misiniz? (E/H)"
    set "MSG_COPY_FAIL=Kopyalama basarisiz! Uygulama acik olabilir."
    set "MSG_CLOSE_RETRY=Uygulamayi kapatip tekrar deneyin."
)

echo.

:: Create install directory
echo [1/4] %MSG_STEP1%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\layouts" mkdir "%INSTALL_DIR%\layouts"

:: Copy exe (always overwrite for upgrades)
echo [2/4] %MSG_STEP2%
copy /Y "%SOURCE_EXE%" "%INSTALL_DIR%\%EXE_NAME%" >nul
if %errorlevel% neq 0 (
    echo [ERROR] %MSG_COPY_FAIL%
    echo         %MSG_CLOSE_RETRY%
    pause
    exit /b 1
)

:: Copy default layouts only if layouts folder is empty (preserve user data on upgrade)
dir /b "%INSTALL_DIR%\layouts\*.json" >nul 2>&1
if %errorlevel% neq 0 (
    echo        %MSG_COPY_LAYOUTS%
    xcopy "%~dp0layouts\*.json" "%INSTALL_DIR%\layouts\" /Y /Q >nul 2>&1
) else (
    echo        %MSG_KEEP_LAYOUTS%
)

:: Save language config
echo {"language": "%LANG%"} > "%INSTALL_DIR%\config.json"

:: Add to Windows startup
echo [3/4] %MSG_STEP3%
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" /t REG_SZ /d "\"%INSTALL_DIR%\%EXE_NAME%\" --startup" /f >nul

:: Create Start Menu shortcut
echo [4/4] %MSG_STEP4%
powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTMENU_DIR%\%APP_NAME%.lnk'); $s.TargetPath = '%INSTALL_DIR%\%EXE_NAME%'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'Screen Location Saver'; $s.Save()" >nul 2>&1

echo.
echo ============================================
echo   %MSG_DONE%
echo ============================================
echo.
echo   %MSG_LOCATION%: %INSTALL_DIR%
echo.
echo   - %MSG_INFO1%
echo   - %MSG_INFO2%
echo   - %MSG_INFO3%
echo.
echo   %MSG_UNINSTALL%
echo.

:: Ask to run now
set /p "RUN_NOW=%MSG_RUN_NOW% "
if /i "%RUN_NOW%"=="Y" goto :run_app
if /i "%RUN_NOW%"=="E" goto :run_app
goto :end

:run_app
start "" "%INSTALL_DIR%\%EXE_NAME%"

:end
endlocal
