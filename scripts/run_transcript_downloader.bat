@echo off
REM YouTube Transcript Downloader - Quick Launcher
REM Double-click to run or drag a YouTube URL onto this file

echo ========================================
echo YouTube Transcript Downloader
echo ========================================
echo.

REM Check if URL is provided as argument
if "%~1"=="" (
    set /p URL="Enter YouTube URL: "
) else (
    set URL=%~1
)

echo.
echo Installing dependencies if needed...
py -m pip install -q youtube-transcript-api

echo.
echo Running transcript downloader...
py youtube_transcript_downloader.py "%URL%"

echo.
pause
