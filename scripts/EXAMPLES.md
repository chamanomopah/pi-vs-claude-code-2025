# YouTube Transcript Downloader - Quick Examples

## Installation (One-time setup)

```bash
# Windows
py -m pip install youtube-transcript-api

# Linux/Mac
pip3 install youtube-transcript-api
```

## Basic Usage

### Example 1: Download transcript from a short URL
```bash
py youtube_transcript_downloader.py "https://youtu.be/jNQXAC9IVRw"
```
**Output:** Saves to `transcript.txt` and displays in terminal

### Example 2: Custom output filename
```bash
py youtube_transcript_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output rick_roll.txt
```
**Output:** Saves to `rick_roll.txt`

### Example 3: Portuguese video
```bash
py youtube_transcript_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --language pt
```
**Output:** Prioritizes Portuguese transcripts

### Example 4: Long video, don't display in terminal
```bash
py youtube_transcript_downloader.py "URL" --no-display
```
**Output:** Only saves to file, doesn't display in terminal

### Example 5: Combine options
```bash
py youtube_transcript_downloader.py "URL" --language pt --output entrevista.txt --no-display
```
**Output:** Portuguese transcript saved to `entrevista.txt` only

## Quick Launch (Windows)

Double-click `run_transcript_downloader.bat` and paste your URL when prompted.

## Quick Launch (Linux/Mac)

```bash
chmod +x run_transcript_downloader.sh
./run_transcript_downloader.sh
```

## Sample Output

The script generates:
1. **Formatted transcript** with proper punctuation and paragraphs
2. **Timestamp reference** at the bottom with clickable links
3. **Progress messages** showing what's happening
4. **Error handling** for invalid URLs or missing transcripts

## Troubleshooting

**"Module not found" error?**
```bash
# Windows
py -m pip install youtube-transcript-api

# Linux/Mac
pip3 install youtube-transcript-api
```

**Video has no transcript?**
- Check if captions are available on YouTube
- Try a different video
- Some videos don't have transcripts available

**Want to translate transcripts?**
The script saves plain text that you can paste into any translation tool.
