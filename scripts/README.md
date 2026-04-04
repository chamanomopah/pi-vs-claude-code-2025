# YouTube Transcript Downloader

A simple Python script to download and format YouTube video transcripts with proper punctuation and structure.

## Features

✅ **Multiple URL formats** - Supports youtube.com, youtu.be, and embed links  
✅ **Auto language detection** - Prioritizes Portuguese, then English  
✅ **Smart formatting** - Proper punctuation, capitalization, and paragraph structure  
✅ **Timestamp reference** - Includes clickable timestamps at the end  
✅ **Error handling** - Graceful handling of invalid URLs, missing transcripts, etc.  
✅ **Easy to use** - Simple command-line interface with helpful messages  

## Installation

1. **Install Python 3.7+** (if not already installed)

2. **Install dependencies:**
   
   **Windows:**
   ```bash
   py -m pip install youtube-transcript-api
   ```
   
   **Linux/Mac:**
   ```bash
   pip3 install youtube-transcript-api
   # or
   pip install youtube-transcript-api
   ```

   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

**Windows:**
```bash
py youtube_transcript_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Linux/Mac:**
```bash
python3 youtube_transcript_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### With Custom Output File

**Windows:**
```bash
py youtube_transcript_downloader.py "URL" --output my_transcript.txt
```

**Linux/Mac:**
```bash
python3 youtube_transcript_downloader.py "URL" --output my_transcript.txt
```

### Specify Language Preference

```bash
py youtube_transcript_downloader.py "URL" --language pt
```

### Quick Launch Scripts

**Windows:** Double-click `run_transcript_downloader.bat` or drag a URL onto it

**Linux/Mac:** Run `./run_transcript_downloader.sh` (make it executable first with `chmod +x run_transcript_downloader.sh`)

## Examples

```bash
# Short URL format
py youtube_transcript_downloader.py "https://youtu.be/dQw4w9WgXcQ"

# Standard URL format  
py youtube_transcript_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Portuguese video with custom filename
py youtube_transcript_downloader.py "URL" --language pt --output entrevista.txt

# Don't display in terminal (only save to file)
py youtube_transcript_downloader.py "URL" --no-display
```

## Output

The script will:
1. Display progress messages with emojis ✅
2. Show the transcript in the terminal (first 2000 chars)
3. Save the complete formatted transcript to `transcript.txt` (or custom filename)
4. Include timestamp references at the bottom

## Sample Output Structure

```
[Formatted paragraph 1 with proper sentences and punctuation...]

[Formatted paragraph 2...]

================================================================================
TIMESTAMP REFERENCE
================================================================================
[00:00] This is the beginning of the video where...
[00:45] Now we're going to discuss the main topic...
... and 150 more entries
```

## Error Handling

The script handles common errors gracefully:

- ❌ Invalid YouTube URL format
- ❌ Video unavailable or private
- ❌ Transcripts disabled for this video
- ❌ No transcript available
- ❌ Network connection issues

## Language Support

By default, the script tries to get transcripts in this order:
1. Portuguese (pt, pt-BR, pt-PT)
2. English (en, en-US, en-GB)
3. Any available transcript

You can override this with the `--language` parameter.

## Requirements

- Python 3.7 or higher
- youtube-transcript-api package

## Troubleshooting

**"Module not found" error?**
```bash
pip install youtube-transcript-api
```

**Video has no transcript?**
Some videos don't have transcripts available. Check if captions are available on YouTube.

**Want transcripts in other languages?**
Use the `--language` parameter with a language code (e.g., `es` for Spanish).

## License

Free to use and modify.
