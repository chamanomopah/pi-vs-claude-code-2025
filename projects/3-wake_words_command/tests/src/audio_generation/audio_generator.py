# -*- coding: utf-8 -*-
"""
Audio Generator for Automated Testing
Generates complete library of wake words and commands.
"""

from pathlib import Path
from typing import Dict, List
import logging
import time

from .pyttsx3_tts import Pyttsx3TTS

logger = logging.getLogger(__name__)


class AudioGenerator:
    """
    Generates complete audio library for testing.
    
    Categories:
    - Wake words (porcupine, ok google, alexa, etc.)
    - Commands (ligar, desligar, perguntas)
    - Phrases (common sentences)
    - Noise/background (silence, noise)
    """
    
    def __init__(self, rate: int = 150, voice_index: int = None):
        """
        Initialize audio generator.
        
        Args:
            rate: Speech rate
            voice_index: Voice to use (None = default)
        """
        self.tts = Pyttsx3TTS(rate=rate, voice_index=voice_index)
        
        # Define audio library
        self.wake_words = [
            "porcupine",
            "ok google",
            "alexa",
            "hey siri",
            "computer",
        ]
        
        self.commands = [
            # Light commands
            "ligar a luz",
            "desligar a luz",
            "acender a luz",
            "apagar a luz",
            "ligar luz da sala",
            "desligar luz do quarto",
            
            # Time commands
            "que horas são",
            "que dia é hoje",
            "que dia é hoje",
            
            # Weather
            "como está o tempo",
            "previsão do tempo",
            
            # System
            "abrir chrome",
            "abrir navegador",
            "tocar música",
            "parar música",
        ]
        
        self.phrases = [
            "olá mundo",
            "como vai você",
            "bom dia",
            "boa tarde",
            "boa noite",
            "obrigado",
            "por favor",
            "ajuda",
        ]
        
        logger.info("Audio generator initialized")
    
    def generate_wake_words(self) -> Dict[str, Path]:
        """
        Generate all wake word audio files.
        
        Returns:
            Dictionary mapping word to file path
        """
        print("\n" + "=" * 80)
        print(" 🎤 GENERATING WAKE WORDS")
        print("=" * 80)
        
        generated = {}
        
        for word in self.wake_words:
            try:
                path = self.tts.generate_wake_word(word)
                generated[word] = path
                time.sleep(0.1)  # Small delay between generations
            except Exception as e:
                logger.error(f"Failed to generate wake word '{word}': {e}")
        
        print(f"\n✅ Generated {len(generated)}/{len(self.wake_words)} wake words")
        return generated
    
    def generate_commands(self) -> Dict[str, Path]:
        """
        Generate all command audio files.
        
        Returns:
            Dictionary mapping command to file path
        """
        print("\n" + "=" * 80)
        print(" 🎤 GENERATING COMMANDS")
        print("=" * 80)
        
        generated = {}
        
        for command in self.commands:
            try:
                path = self.tts.generate_command(command)
                generated[command] = path
                time.sleep(0.1)  # Small delay between generations
            except Exception as e:
                logger.error(f"Failed to generate command '{command}': {e}")
        
        print(f"\n✅ Generated {len(generated)}/{len(self.commands)} commands")
        return generated
    
    def generate_phrases(self) -> Dict[str, Path]:
        """
        Generate all phrase audio files.
        
        Returns:
            Dictionary mapping phrase to file path
        """
        print("\n" + "=" * 80)
        print(" 🎤 GENERATING PHRASES")
        print("=" * 80)
        
        generated = {}
        output_dir = Path("tests/audio/phrases")
        
        for phrase in self.phrases:
            try:
                path = self.tts.generate_speech(phrase, output_dir / f"{phrase.lower().replace(' ', '_')}.wav")
                generated[phrase] = path
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Failed to generate phrase '{phrase}': {e}")
        
        print(f"\n✅ Generated {len(generated)}/{len(self.phrases)} phrases")
        return generated
    
    def generate_all(self) -> Dict[str, Dict[str, Path]]:
        """
        Generate complete audio library.
        
        Returns:
            Dictionary with all generated files by category
        """
        print("\n" + "=" * 80)
        print(" 🎤 AUDIO GENERATOR - STARTING")
        print("=" * 80)
        print(f"Target: {len(self.wake_words)} wake words + {len(self.commands)} commands + {len(self.phrases)} phrases")
        print(f"Total: {len(self.wake_words) + len(self.commands) + len(self.phrases)} files")
        print("=" * 80)
        
        start_time = time.time()
        
        all_files = {}
        
        # Generate wake words
        all_files['wake_words'] = self.generate_wake_words()
        
        # Generate commands
        all_files['commands'] = self.generate_commands()
        
        # Generate phrases
        all_files['phrases'] = self.generate_phrases()
        
        elapsed = time.time() - start_time
        
        # Summary
        print("\n" + "=" * 80)
        print(" 📊 GENERATION SUMMARY")
        print("=" * 80)
        print(f" ⏱️  Time elapsed: {elapsed:.1f} seconds")
        print(f" 🎤 Wake words: {len(all_files['wake_words'])}")
        print(f" ⚡ Commands: {len(all_files['commands'])}")
        print(f" 💬 Phrases: {len(all_files['phrases'])}")
        print(f" 📁 Total files: {sum(len(v) for v in all_files.values())}")
        print("=" * 80)
        
        # List all files
        self._list_generated_files(all_files)
        
        print("\n✅ Audio library generation complete!")
        print("=" * 80 + "\n")
        
        return all_files
    
    def _list_generated_files(self, all_files: Dict[str, Dict[str, Path]]):
        """List all generated files."""
        print("\n📂 Generated Files:")
        print("-" * 80)
        
        for category, files in all_files.items():
            print(f"\n{category.upper()}:")
            for text, path in sorted(files.items()):
                size_kb = path.stat().st_size / 1024 if path.exists() else 0
                print(f"  ✓ {text:40s} -> {path.name:30s} ({size_kb:5.1f} KB)")
    
    def generate_custom(self, texts: List[str], category: str = "custom") -> Dict[str, Path]:
        """
        Generate custom audio files.
        
        Args:
            texts: List of texts to generate
            category: Category name for organization
        
        Returns:
            Dictionary mapping text to file path
        """
        print(f"\n🎤 Generating {len(texts)} custom '{category}' files...")
        
        generated = {}
        output_dir = Path(f"tests/audio/{category}")
        
        for text in texts:
            try:
                safe_name = text.lower().replace(" ", "_")
                safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '_-')
                path = self.tts.generate_speech(text, output_dir / f"{safe_name}.wav")
                generated[text] = path
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Failed to generate '{text}': {e}")
        
        print(f"✅ Generated {len(generated)}/{len(texts)} custom files")
        return generated
    
    def list_available_voices(self):
        """List all available TTS voices."""
        return self.tts.list_voices()
    
    def test_audio_output(self, text: str = "Testing TTS engine"):
        """Test TTS by speaking text."""
        print(f"\n🔊 Testing audio output...")
        self.tts.test_speaker(text)
        print("✅ Audio test complete")
