"""
TTS (Text-to-Speech) Engine for generating test audio.
Supports both offline (pyttsx3) and online (edge-tts) engines.
"""

import os
import tempfile
import numpy as np
import logging
from pathlib import Path
from typing import Optional, List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class TTSError(Exception):
    """Exception raised when TTS generation fails."""
    pass


class TTSEngine(ABC):
    """
    Abstract base class for TTS engines.
    """

    @abstractmethod
    def text_to_speech(self, text: str, output_path: str) -> str:
        """
        Convert text to speech and save to WAV file.

        Args:
            text: Text to convert
            output_path: Path to save WAV file

        Returns:
            Path to generated WAV file

        Raises:
            TTSError: If generation fails
        """
        pass

    @abstractmethod
    def text_to_audio_array(self, text: str, sample_rate: int = 16000) -> np.ndarray:
        """
        Convert text to audio array.

        Args:
            text: Text to convert
            sample_rate: Target sample rate (default 16kHz for Porcupine/Vosk)

        Returns:
            Numpy array with audio (int16, mono)
        """
        pass

    @abstractmethod
    def get_voices(self) -> List[str]:
        """Return list of available voices."""
        pass

    @abstractmethod
    def set_voice(self, voice_name: str):
        """Set the voice to use."""
        pass


class Pyttsx3TTS(TTSEngine):
    """
    pyttsx3-based TTS engine.
    100% offline, uses system voices (SAPI5 on Windows).
    """

    def __init__(self, voice_id: Optional[str] = None, rate: int = 150):
        """
        Initialize pyttsx3 TTS engine.

        Args:
            voice_id: Voice ID to use (None = default)
            rate: Speech rate (words per minute)
        """
        try:
            import pyttsx3
            self.pyttsx3 = pyttsx3
            self.engine = pyttsx3.init()

            # Configure voice
            if voice_id:
                self.engine.setProperty('voice', voice_id)

            # Configure rate
            self.engine.setProperty('rate', rate)

            # Configure volume (max for better detection)
            self.engine.setProperty('volume', 1.0)

            logger.info(f"✅ Pyttsx3TTS initialized (rate={rate})")

        except ImportError:
            raise TTSError("pyttsx3 not installed. Run: pip install pyttsx3")
        except Exception as e:
            raise TTSError(f"Failed to initialize pyttsx3: {e}")

    def text_to_speech(self, text: str, output_path: str) -> str:
        """Convert text to WAV file using pyttsx3."""
        try:
            # Ensure output directory exists
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # pyttsx3 requires absolute path
            output_path = output_path.resolve()

            # Save to file
            self.engine.save_to_file(text, str(output_path))

            # runAndWait() is required to actually process
            self.engine.runAndWait()

            # Verify file was created
            if not Path(output_path).exists():
                raise TTSError(f"File not created: {output_path}")

            logger.debug(f"📝 Generated TTS audio: {output_path}")
            return str(output_path)

        except Exception as e:
            raise TTSError(f"Failed to generate speech: {e}")

    def text_to_audio_array(self, text: str, sample_rate: int = 16000) -> np.ndarray:
        """Convert text to numpy array."""
        # Generate temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Generate WAV
            wav_path = self.text_to_speech(text, tmp_path)

            # Load with soundfile
            import soundfile as sf
            audio, sr = sf.read(wav_path)

            # Convert to mono if stereo
            if len(audio.shape) > 1:
                audio = audio[:, 0]

            # Resample if necessary
            if sr != sample_rate:
                from scipy import signal
                number_of_samples = round(len(audio) * float(sample_rate) / sr)
                audio = signal.resample(audio, number_of_samples)

            # Convert to int16
            audio = (audio * np.iinfo(np.int16).max).astype(np.int16)

            return audio

        finally:
            # Cleanup temp file
            try:
                Path(tmp_path).unlink()
            except:
                pass

    def get_voices(self) -> List[str]:
        """Get list of available voices."""
        voices = []
        for voice in self.engine.getProperty('voices'):
            voices.append(voice.id)
        return voices

    def set_voice(self, voice_name: str):
        """Set voice by name."""
        # Find voice ID by name
        for voice in self.engine.getProperty('voices'):
            if voice_name.lower() in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                logger.info(f"🎤 Voice set to: {voice.name}")
                return

        logger.warning(f"Voice '{voice_name}' not found, using default")

    @staticmethod
    def print_available_voices():
        """Print all available system voices."""
        try:
            import pyttsx3
            engine = pyttsx3.init()

            print("\n" + "=" * 60)
            print("AVAILABLE VOICES (pyttsx3)")
            print("=" * 60)

            voices = engine.getProperty('voices')
            for i, voice in enumerate(voices, 1):
                print(f"{i}. {voice.name}")
                print(f"   ID: {voice.id}")
                print(f"   Languages: {voice.languages}")
                print()

            print("=" * 60 + "\n")

        except Exception as e:
            logger.error(f"Failed to list voices: {e}")


class EdgeTTS(TTSEngine):
    """
    edge-tts based TTS engine.
    Uses Microsoft Edge online TTS (requires internet).
    Higher quality voices, including Portuguese neural voices.
    """

    def __init__(self, voice: str = "pt-BR-FranciscaNeural"):
        """
        Initialize edge-tts engine.

        Args:
            voice: Voice to use (default: pt-BR-FranciscaNeural)
        """
        try:
            import edge_tts
            self.edge_tts = edge_tts
            self.voice = voice
            logger.info(f"✅ EdgeTTS initialized (voice={voice})")

        except ImportError:
            raise TTSError("edge-tts not installed. Run: pip install edge-tts")

    def text_to_speech(self, text: str, output_path: str) -> str:
        """Convert text to WAV file using edge-tts."""
        try:
            import asyncio

            # Ensure output directory exists
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Async function
            async def _generate():
                communicate = self.edge_tts.Communicate(text, self.voice)
                await communicate.save(str(output_path))

            # Run async
            asyncio.run(_generate())

            # Verify file was created
            if not Path(output_path).exists():
                raise TTSError(f"File not created: {output_path}")

            logger.debug(f"📝 Generated TTS audio (edge-tts): {output_path}")
            return str(output_path)

        except Exception as e:
            raise TTSError(f"Failed to generate speech (edge-tts): {e}")

    def text_to_audio_array(self, text: str, sample_rate: int = 16000) -> np.ndarray:
        """Convert text to numpy array."""
        # Generate temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Generate WAV
            wav_path = self.text_to_speech(text, tmp_path)

            # Load with soundfile
            import soundfile as sf
            audio, sr = sf.read(wav_path)

            # Convert to mono if stereo
            if len(audio.shape) > 1:
                audio = audio[:, 0]

            # Resample if necessary
            if sr != sample_rate:
                from scipy import signal
                number_of_samples = round(len(audio) * float(sample_rate) / sr)
                audio = signal.resample(audio, number_of_samples)

            # Convert to int16
            audio = (audio * np.iinfo(np.int16).max).astype(np.int16)

            return audio

        finally:
            # Cleanup temp file
            try:
                Path(tmp_path).unlink()
            except:
                pass

    def get_voices(self) -> List[str]:
        """Get list of available edge-tts voices."""
        # This would require calling edge-tts --list-voices
        # For now, return common Portuguese voices
        return [
            "pt-BR-FranciscaNeural",
            "pt-BR-AntonioNeural",
            "pt-BR-BrendaNeural",
            "en-US-JennyNeural",
            "en-US-GuyNeural",
        ]

    def set_voice(self, voice_name: str):
        """Set voice."""
        self.voice = voice_name
        logger.info(f"🎤 EdgeTTS voice set to: {voice_name}")

    @staticmethod
    def print_available_voices():
        """Print available edge-tts voices."""
        print("\n" + "=" * 60)
        print("AVAILABLE VOICES (edge-tts - Portuguese)")
        print("=" * 60)
        print("pt-BR-FranciscaNeural  - Female, Portuguese (Brazil)")
        print("pt-BR-AntonioNeural    - Male, Portuguese (Brazil)")
        print("pt-BR-BrendaNeural     - Female, Portuguese (Brazil)")
        print("\nFor more voices, run: edge-tts --list-voices")
        print("=" * 60 + "\n")


def get_tts_engine(prefer: str = "pyttsx3", **kwargs) -> TTSEngine:
    """
    Factory function to get TTS engine.

    Args:
        prefer: Preferred engine ("pyttsx3" or "edge-tts")
        **kwargs: Arguments to pass to engine

    Returns:
        TTSEngine instance

    Raises:
        TTSError: If preferred engine not available
    """
    if prefer == "pyttsx3":
        return Pyttsx3TTS(**kwargs)
    elif prefer == "edge-tts":
        return EdgeTTS(**kwargs)
    else:
        raise TTSError(f"Unknown TTS engine: {prefer}")


# Convenience function for quick usage
def text_to_speech(text: str, output_path: str, engine: str = "pyttsx3") -> str:
    """
    Quick function to generate speech from text.

    Args:
        text: Text to convert
        output_path: Path to save WAV
        engine: TTS engine to use

    Returns:
        Path to generated file
    """
    tts = get_tts_engine(prefer=engine)
    return tts.text_to_speech(text, output_path)


if __name__ == "__main__":
    # Test TTS generation
    logging.basicConfig(level=logging.INFO)

    print("Testing TTS engines...\n")

    # Test pyttsx3
    print("1. Testing pyttsx3...")
    try:
        pyttsx_tts = Pyttsx3TTS()
        pyttsx_tts.print_available_voices()

        output = pyttsx_tts.text_to_speech("porcupine", "test_pytttsx3.wav")
        print(f"✅ Generated: {output}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test edge-tts
    print("2. Testing edge-tts...")
    try:
        edge_tts = EdgeTTS()
        output = edge_tts.text_to_speech("porcupine", "test_edge.wav")
        print(f"✅ Generated: {output}\n")
    except Exception as e:
        print(f"❌ Error (may require internet): {e}\n")
