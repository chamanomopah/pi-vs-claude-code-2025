#!/bin/bash
# YouTube Transcript Downloader - Quick Launcher for Linux/Mac
# Make executable with: chmod +x run_transcript_downloader.sh

echo "========================================"
echo "YouTube Transcript Downloader"
echo "========================================"
echo ""

# Check if URL is provided as argument
if [ -z "$1" ]; then
    read -p "Enter YouTube URL: " URL
else
    URL="$1"
fi

echo ""
echo "Installing dependencies if needed..."
pip3 install -q youtube-transcript-api 2>/dev/null || pip install -q youtube-transcript-api

echo ""
echo "Running transcript downloader..."
python3 youtube_transcript_downloader.py "$URL"

echo ""
