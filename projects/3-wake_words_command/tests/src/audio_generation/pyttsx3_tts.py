# -*- coding: utf-8 -*-
"""
TTS Engine using pyttsx3 for offline audio generation.
Generates wake words and commands for automated testing.
"""

import pyttsx3
from pathlib import Path
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class Pyttsx3TTS:
    """
    Text-to-Speech engine using pyttsx3.
    
    Features:
    - Offline operation (no internet required)
    - Cross-platform (Windows, Linux, macOS)
    - Multiple voices
    - Configurable rate and volume
    """
    
    def __init__(self, rate: int = 150, volume: float = 0.9, voice_index: Optional[int] = None):
        """
        Initialize TTS engine.
        
        Args:
            rate: Speech rate (words per minute). Default: 150
            volume: Volume level (0.0 to 1.0). Default: 0.9
            voice_index: Specific voice to use. None = default
        """
        self.rate = rate
        self.volume = volume
        self.voice_index = voice_index
        
        # Initialize engine
        try:
            self.engine = pyttsx3.init()
            
            # Configure properties
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # Set voice if specified
            if voice_index is not None:
                voices = self.engine.getProperty('voices')
                if 0 <= voice_index < len(voices):
                    self.engine.setProperty('voice', voices[voice_index].id)
                    logger.info(f"Using voice: {voices[voice_index].name}")
            
            logger.info("TTS engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            raise
    
    def list_voices(self):
        """List all available voices."""
        voices = self.engine.getProperty('voices')
        print(f"\n📢 Available Voices ({len(voices)}):")
        print("=" * 80)
        
        for i, voice in enumerate(voices):
            gender = "♂️ Masculine" if "male" in voice.name.lower() or "david" in voice.name.lower() else "♀️ Feminine"
            print(f"  [{i}] {voice.name}")
            print(f"      {gender} | {voice.languages[0] if voice.languages else 'Unknown'}")
            print(f"      ID: {voice.id}")
        
        print("=" * 80)
        return voices
    
    def generate_wake_word(self, word: str, output_dir: Optional[Path] = None) -> Path:
        """
        Generate audio for wake word.
        
        Args:
            word: Wake word to speak
            output_dir: Output directory (default: tests/audio/wake_words)
        
        Returns:
            Path to generated audio file
        """
        if output_dir is None:
            output_dir = Path("tests/audio/wake_words")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create safe filename
        safe_name = word.lower().replace(" ", "_").replace("-", "_")
        output_path = output_dir / f"{safe_name}.wav"
        
        try:
            # Generate audio
            self.engine.save_to_file(word, str(output_path))
            self.engine.runAndWait()
            
            # Verify file was created
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                logger.info(f"✅ Generated wake word: {word} -> {output_path} ({size_kb:.1f} KB)")
                return output_path
            else:
                raise FileNotFoundError(f"Audio file not created: {output_path}")
                
        except Exception as e:
            logger.error(f"Failed to generate wake word '{word}': {e}")
            raise
    
    def generate_command(self, command: str, output_dir: Optional[Path] = None) -> Path:
        """
        Generate audio for command.
        
        Args:
            command: Command text to speak
            output_dir: Output directory (default: tests/audio/commands)
        
        Returns:
            Path to generated audio file
        """
        if output_dir is None:
            output_dir = Path("tests/audio/commands")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create safe filename
        safe_name = command.lower().replace(" ", "_").replace(":", "").replace("?", "")
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '_-')
        output_path = output_dir / f"{safe_name}.wav"
        
        try:
            # Generate audio
            self.engine.save_to_file(command, str(output_path))
            self.engine.runAndWait()
            
            # Verify file was created
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                logger.info(f"✅ Generated command: {command} -> {output_path} ({size_kb:.1f} KB)")
                return output_path
            else:
                raise FileNotFoundError(f"Audio file not created: {output_path}")
                
        except Exception as e:
            logger.error(f"Failed to generate command '{command}': {e}")
            raise
    
    def generate_speech(self, text: str, output_path: Path) -> Path:
        """
        Generate audio for any text.
        
        Args:
            text: Text to speak
            output_path: Full output path for audio file
        
        Returns:
            Path to generated audio file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Generate audio
            self.engine.save_to_file(text, str(output_path))
            self.engine.runAndWait()
            
            # Verify file was created
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                logger.info(f"✅ Generated speech: {text} -> {output_path} ({size_kb:.1f} KB)")
                return output_path
            else:
                raise FileNotFoundError(f"Audio file not created: {output_path}")
                
        except Exception as e:
            logger.error(f"Failed to generate speech '{text}': {e}")
            raise
    
    def test_speaker(self, text: str = "Testing TTS engine"):
        """
        Test TTS engine by speaking text.
        
        Args:
            text: Text to speak
        """
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            logger.info(f"🔊 Spoke: {text}")
        except Exception as e:
            logger.error(f"Failed to speak: {e}")
            raise
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        try:
            self.engine.stop()
        except:
            pass
