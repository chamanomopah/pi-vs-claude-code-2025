#!/usr/bin/env python3
"""
YouTube Transcript Downloader
A simple script to download and format YouTube video transcripts.

Usage:
    python youtube_transcript_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
    python youtube_transcript_downloader.py "https://youtu.be/VIDEO_ID"
"""

import sys
import re
import argparse
from typing import Optional

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    from youtube_transcript_api import (
        YouTubeTranscriptApi,
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
        CouldNotRetrieveTranscript
    )
except ImportError as e:
    print("Error: youtube-transcript-api is not installed.")
    print(f"Import error: {e}")
    print("Install it with: pip install youtube-transcript-api")
    print("Or: py -m pip install youtube-transcript-api")
    sys.exit(1)


def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def format_transcript(transcript_data, language_code='en') -> str:
    """
    Format transcript with proper punctuation and structure.
    
    Args:
        transcript_data: Raw transcript data from YouTube API
        language_code: Language code for punctuation rules ('en' or 'pt')
    
    Returns:
        Formatted transcript text
    """
    if not transcript_data:
        return ""
    
    # Configuration for different languages
    if language_code.startswith('pt'):
        # Portuguese punctuation rules
        sentence_enders = r'(?<=[.!?])\s+'
        abbreviation_pattern = r'\b(?:Sr|Sra|Dr|Dra|Prof|Profa|etc|ex|vs)\.$'
    else:
        # English punctuation rules (default)
        sentence_enders = r'(?<=[.!?])\s+'
        abbreviation_pattern = r'\b(?:Mr|Mrs|Ms|Dr|Prof|etc|e\.g|i\.e)\.$'
    
    formatted_lines = []
    current_paragraph = []
    char_count = 0
    max_chars = 1000  # Characters per paragraph
    
    for entry in transcript_data:
        text = entry.text.strip()
        
        # Skip empty entries
        if not text:
            continue
        
        # Clean up common issues
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = re.sub(r'&#39;', "'", text)  # Fix HTML entities
        text = re.sub(r'&quot;', '"', text)
        text = re.sub(r'&amp;', '&', text)
        
        # Ensure proper spacing after punctuation
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
        text = re.sub(r'([.!?])([a-z])', r'\1 \2', text)
        
        # Add proper capitalization after sentence endings
        sentences = re.split(r'([.!?]\s+)', text)
        for i, sentence in enumerate(sentences):
            if i > 0 and sentence and sentence[0].isalpha():
                sentence = sentence[0].upper() + sentence[1:]
            sentences[i] = sentence
        text = ''.join(sentences)
        
        # Build paragraph
        current_paragraph.append(text)
        char_count += len(text)
        
        # Start new paragraph after reaching max_chars or on logical breaks
        if char_count >= max_chars or any(marker in text.lower() for marker in ['chapter', 'section', 'part ', 'firstly', 'secondly']):
            formatted_lines.append(' '.join(current_paragraph))
            formatted_lines.append('')  # Empty line between paragraphs
            current_paragraph = []
            char_count = 0
    
    # Add remaining content
    if current_paragraph:
        formatted_lines.append(' '.join(current_paragraph))
    
    # Add timestamps as reference at the end
    result = '\n'.join(formatted_lines)
    result += '\n\n' + '=' * 80 + '\n'
    result += 'TIMESTAMP REFERENCE\n'
    result += '=' * 80 + '\n'
    
    for entry in transcript_data[:20]:  # First 20 entries for reference
        time = entry.start
        minutes = int(time // 60)
        seconds = int(time % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
        result += f"[{timestamp}] {entry.text[:80]}...\n"
    
    if len(transcript_data) > 20:
        result += f"... and {len(transcript_data) - 20} more entries\n"
    
    return result


def get_transcript(video_id: str, language_pref: str = 'auto') -> tuple:
    """
    Get transcript for a YouTube video.

    Returns:
        tuple: (transcript_data, language_code, actual_language)
    """
    # Common language codes to try
    if language_pref == 'auto':
        language_priority = [
            ['pt', 'pt-BR', 'pt-PT'],  # Portuguese variants
            ['en', 'en-US', 'en-GB'],  # English variants
            ['en'],  # Fallback to English
        ]
    else:
        language_priority = [language_pref.split(',')]

    last_error = None
    ytt_api = YouTubeTranscriptApi()

    for languages in language_priority:
        try:
            transcript_list = ytt_api.list(video_id)

            # Try to find a transcript in the preferred languages
            for lang in languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    transcript_data = transcript.fetch()
                    return transcript_data, languages[0], lang
                except NoTranscriptFound:
                    continue

            # If no exact match, try auto-generated transcripts
            for lang in languages:
                try:
                    transcript = transcript_list.find_manually_created_transcript([lang])
                    transcript_data = transcript.fetch()
                    return transcript_data, languages[0], f"{lang} (manual)"
                except NoTranscriptFound:
                    pass

                try:
                    transcript = transcript_list.find_generated_transcript([lang])
                    transcript_data = transcript.fetch()
                    return transcript_data, languages[0], f"{lang} (auto-generated)"
                except NoTranscriptFound:
                    pass

        except (VideoUnavailable, TranscriptsDisabled, CouldNotRetrieveTranscript) as e:
            last_error = e
            continue
        except Exception as e:
            last_error = e
            continue

    # If all else fails, try to get any available transcript
    try:
        transcript_list = ytt_api.list(video_id)
        for transcript in transcript_list:
            transcript_data = transcript.fetch()
            return transcript_data, 'en', f"{transcript.language_code} (available)"
    except Exception as e:
        last_error = e

    raise last_error or Exception("Could not retrieve transcript")


def main():
    parser = argparse.ArgumentParser(
        description='Download and format YouTube video transcripts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube_transcript_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  python youtube_transcript_downloader.py "https://youtu.be/dQw4w9WgXcQ" --language pt
  python youtube_transcript_downloader.py "URL" --output my_transcript.txt
        """
    )
    
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-o', '--output', default='transcript.txt', 
                        help='Output file name (default: transcript.txt)')
    parser.add_argument('-l', '--language', default='auto',
                        help='Language preference (default: auto-detect, tries PT first then EN)')
    parser.add_argument('--no-display', action='store_true',
                        help='Don\'t display transcript in terminal (only save to file)')
    
    args = parser.parse_args()
    
    # Extract video ID
    video_id = extract_video_id(args.url)
    if not video_id:
        print("❌ Error: Invalid YouTube URL format")
        print(f"   URL provided: {args.url}")
        print("\nValid formats:")
        print("  • https://www.youtube.com/watch?v=VIDEO_ID")
        print("  • https://youtu.be/VIDEO_ID")
        print("  • https://www.youtube.com/embed/VIDEO_ID")
        sys.exit(1)
    
    print(f"📺 Video ID: {video_id}")
    print(f"🔍 Fetching transcript...")
    
    try:
        # Get transcript
        transcript_data, lang_code, actual_lang = get_transcript(video_id, args.language)
        
        if not transcript_data:
            print("❌ Error: No transcript data available")
            sys.exit(1)
        
        print(f"✅ Transcript found! ({actual_lang}, {len(transcript_data)} entries)")
        
        # Format transcript
        formatted = format_transcript(transcript_data, lang_code)
        
        # Save to file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        print(f"💾 Saved to: {args.output}")
        print(f"📝 Character count: {len(formatted):,}")
        
        # Display in terminal
        if not args.no_display:
            print("\n" + "=" * 80)
            print("TRANSCRIPT CONTENT")
            print("=" * 80 + "\n")
            
            # Display first 2000 characters to avoid spamming terminal
            preview_length = 2000
            if len(formatted) > preview_length:
                print(formatted[:preview_length])
                print(f"\n... ({len(formatted) - preview_length:,} more characters)")
                print(f"\n💡 Full transcript saved in: {args.output}")
            else:
                print(formatted)
        
        print(f"\n✨ Done!")
        
    except VideoUnavailable:
        print("❌ Error: Video is unavailable or private")
        sys.exit(1)
    except TranscriptsDisabled:
        print("❌ Error: Transcripts are disabled for this video")
        sys.exit(1)
    except NoTranscriptFound:
        print("❌ Error: No transcript found for this video")
        print("   The video may not have captions available.")
        sys.exit(1)
    except CouldNotRetrieveTranscript as e:
        print("❌ Error: Could not retrieve transcript")
        print(f"   Details: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
