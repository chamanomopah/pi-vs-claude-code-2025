@echo off
setlocal enabledelayedexpansion

REM LiveKit + Pi Setup Test Script (Windows)
REM Tests if all components are properly configured

echo ========================================
echo LiveKit + Pi Setup Test
echo ========================================
echo.

set PASSED=0
set FAILED=0

REM Function to print test result (simulated with goto)
:print_result
if %1==0 (
    echo [PASS] %~2
    set /a PASSED+=1
) else (
    echo [FAIL] %~2
    set /a FAILED+=1
)
exit /b

REM Test 1: Check Python version
echo Testing Python version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

echo Python version: %PYTHON_VERSION%
REM Note: Windows batch has limited version comparison
echo [SKIP] Version comparison requires manual check
echo.

REM Test 2: Check if required Python packages are installed
echo Testing Python packages...
python -c "import livekit" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] livekit-agents package
    set /a FAILED+=1
) else (
    echo [PASS] livekit-agents package
    set /a PASSED+=1
)

python -c "from livekit.plugins import deepgram" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] livekit-plugins-deepgram
    set /a FAILED+=1
) else (
    echo [PASS] livekit-plugins-deepgram
    set /a PASSED+=1
)

python -c "from livekit.plugins import cartesia" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] livekit-plugins-cartesia
    set /a FAILED+=1
) else (
    echo [PASS] livekit-plugins-cartesia
    set /a PASSED+=1
)

python -c "from livekit.plugins import openai" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] livekit-plugins-openai
    set /a FAILED+=1
) else (
    echo [PASS] livekit-plugins-openai
    set /a PASSED+=1
)

python -c "import dotenv" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] python-dotenv
    set /a FAILED+=1
) else (
    echo [PASS] python-dotenv
    set /a PASSED+=1
)
echo.

REM Test 3: Check if .env file exists
echo Testing configuration...
if exist ".env" (
    echo [PASS] .env file exists
    set /a PASSED+=1
) else (
    echo [FAIL] .env file not found
    set /a FAILED+=1
)
echo.

REM Test 4: Check required environment variables
if exist ".env" (
    echo Testing environment variables...
    findstr /C:"LIVEKIT_URL" .env >nul 2>&1
    if errorlevel 1 (
        echo [FAIL] LIVEKIT_URL configured
        set /a FAILED+=1
    ) else (
        echo [PASS] LIVEKIT_URL configured
        set /a PASSED+=1
    )

    findstr /C:"DEEPGRAM_API_KEY" .env >nul 2>&1
    if errorlevel 1 (
        echo [FAIL] DEEPGRAM_API_KEY configured
        set /a FAILED+=1
    ) else (
        echo [PASS] DEEPGRAM_API_KEY configured
        set /a PASSED+=1
    )

    findstr /C:"CARTESIA_API_KEY" .env >nul 2>&1
    if errorlevel 1 (
        echo [FAIL] CARTESIA_API_KEY configured
        set /a FAILED+=1
    ) else (
        echo [PASS] CARTESIA_API_KEY configured
        set /a PASSED+=1
    )
    echo.
)

REM Test 5: Check if Python agent files exist
echo Testing Python agent...
if exist "pi_agent.py" (
    echo [PASS] pi_agent.py exists
    set /a PASSED+=1
) else (
    echo [FAIL] pi_agent.py not found
    set /a FAILED+=1
)

if exist "livekit_basic_agent.py" (
    echo [PASS] livekit_basic_agent.py exists (reference)
    set /a PASSED+=1
) else (
    echo [FAIL] livekit_basic_agent.py not found
    set /a FAILED+=1
)
echo.

REM Test 6: Check if LiveKit Server is running
echo Testing LiveKit Server...
netstat -an | findstr "7880.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] LiveKit Server not running on port 7880
    set /a FAILED+=1
) else (
    echo [PASS] LiveKit Server running on port 7880
    set /a PASSED+=1
)
echo.

REM Test 7: Check if Pi extension exists
echo Testing Pi extension...
if exist "..\..\extensions\livekit.ts" (
    echo [PASS] livekit.ts extension exists
    set /a PASSED+=1
) else (
    echo [FAIL] livekit.ts extension not found
    set /a FAILED+=1
)

if exist "..\..\.pi\extensions\livekit.ts" (
    echo [PASS] livekit.ts symlink exists
    set /a PASSED+=1
) else (
    echo [SKIP] livekit.ts symlink not found (optional)
)
echo.

REM Summary
echo ========================================
echo Test Summary
echo ========================================
echo Passed: %PASSED%
echo Failed: %FAILED%
echo.

if %FAILED%==0 (
    echo All tests passed^^!
    echo.
    echo You can now run:
    echo   1. Start LiveKit Server: lk dev
    echo   2. Start Pi: pi -e extensions/livekit.ts
    echo   3. Activate voice mode: /speak
    exit /b 0
) else (
    echo Some tests failed. Please fix the issues above.
    echo.
    echo Common fixes:
    echo   - Install Python packages: pip install livekit-agents[silero] livekit-plugins-openai livekit-plugins-deepgram livekit-plugins-cartesia python-dotenv
    echo   - Start LiveKit Server: lk dev
    echo   - Create .env file with API keys
    exit /b 1
)
