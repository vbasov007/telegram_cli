@echo off
echo ========================================
echo Building telegram_send.exe (using spec file)
echo ========================================
echo.

REM Activate virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Error: Virtual environment not found at .venv\Scripts\activate.bat
    echo Please create a virtual environment first.
    pause
    exit /b 1
)

echo Installing PyInstaller...
pip install -r requirements-dev.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo Building executable with spec file...
pyinstaller telegram_send.spec
if %errorlevel% neq 0 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo The executable is located at: dist\telegram_send.exe
echo The telegram_send_config.ini.example file is bundled with the executable
echo.
echo IMPORTANT: Create telegram_send_config.ini in the same directory as the .exe
echo.
pause
