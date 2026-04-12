# -*- coding: utf-8 -*-
"""
Generate audio library for automated testing.
Creates wake words, commands, and phrases using TTS.
"""

import sys
import logging
from pathlib import Path
import io

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.audio_generation import AudioGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    print("\n" + "=" * 80)
    print(" 🎤 AUDIO LIBRARY GENERATOR")
    print("=" * 80)
    print("\nThis script generates a complete library of audio files for testing.")
    print("It uses pyttsx3 TTS engine (offline, cross-platform).")
    print("\nGenerating:")
    print("  • Wake words (porcupine, ok google, alexa, etc.)")
    print("  • Commands (ligar, desligar, perguntas)")
    print("  • Phrases (common sentences)")
    print("\nOutput directory: tests/audio/")
    print("=" * 80)
    
    # Check if pyttsx3 is installed
    try:
        import pyttsx3
        print(f"\n✅ pyttsx3 is installed and ready")
    except ImportError:
        print("\n❌ pyttsx3 is not installed!")
        print("Install with: pip install pyttsx3")
        return 1
    
    # Create generator
    try:
        generator = AudioGenerator(rate=150)
        
        # Optional: list available voices
        print("\n" + "=" * 80)
        print("Available TTS voices:")
        print("=" * 80)
        voices = generator.list_available_voices()
        
        # Generate all audio files
        print("\n" + "=" * 80)
        print("Starting generation...")
        print("=" * 80)
        
        all_files = generator.generate_all()
        
        # Final summary
        total_files = sum(len(v) for v in all_files.values())
        print("\n" + "=" * 80)
        print(f" ✅ SUCCESS! Generated {total_files} audio files")
        print("=" * 80)
        print("\n📁 Output directories:")
        print("  • tests/audio/wake_words/")
        print("  • tests/audio/commands/")
        print("  • tests/audio/phrases/")
        print("\nYou can now use these files for automated testing!")
        print("=" * 80 + "\n")
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to generate audio library: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
