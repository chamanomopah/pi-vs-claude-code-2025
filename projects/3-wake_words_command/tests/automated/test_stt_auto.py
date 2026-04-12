"""
Automated tests for STT (Speech-to-Text) using TTS-generated audio.
"""

import pytest
import numpy as np
from pathlib import Path

from tests.src.audio_generation import AudioGenerator, Pyttsx3TTS
from tests.src.test_framework import (
    assert_stt_transcription,
    assert_wer_below,
    assert_audio_level_above
)


class TestSTTTTS:
    """Test STT with TTS-generated audio."""

    @pytest.fixture
    def generator(self, sample_rate):
        """Create audio generator."""
        tts = Pyttsx3TTS(rate=150)
        return AudioGenerator(tts_engine=tts, sample_rate=sample_rate)

    @pytest.mark.parametrize("command,expected_wer", [
        ("ligar a luz", 0.5),      # Simple command
        ("abrir a porta", 0.5),    # Another command
        ("desligar", 0.5),         # Single word
    ])
    def test_transcribe_commands(self, command, expected_wer, generator, test_runner, temp_audio_dir):
        """Test transcription of commands."""
        # Generate command audio
        audio_path = generator.generate_command(
            command=command,
            output_path=str(temp_audio_dir / f"command_{command.replace(' ', '_')}.wav")
        )

        # Test transcription
        result = test_runner.run_stt_test(
            audio_path,
            expected_text=command,
            max_wer=expected_wer
        )

        # Assert
        assert result.wer <= expected_wer, f"WER {result.wer:.2f} > {expected_wer}"
        assert_audio_level_above(
            np.zeros(1000),  # Just to show we can test audio level
            threshold=0.01
        )

    def test_transcribe_empty_audio(self, generator, test_runner, temp_audio_dir):
        """Test that empty/silent audio returns empty transcription."""
        # Generate silence
        silence = generator.generate_silence(2.0)

        import soundfile as sf
        silence_path = temp_audio_dir / "silence.wav"
        sf.write(str(silence_path), silence, 16000)

        # Test
        result = test_runner.run_stt_test(
            str(silence_path),
            expected_text="",
            max_wer=1.0  # Allow any result for silence
        )

        # Should be empty or very short
        assert len(result.text) < 20, "Silence should produce empty transcription"

    def test_transcribe_with_noise(self, generator, test_runner, noise_injector, temp_audio_dir):
        """Test transcription with background noise."""
        command = "ligar a luz"

        # Generate clean audio
        clean_path = generator.generate_command(
            command=command,
            output_path=str(temp_audio_dir / "clean.wav")
        )

        # Load and add noise
        import soundfile as sf
        audio, sr = sf.read(clean_path)

        if len(audio.shape) > 1:
            audio = audio[:, 0]

        noisy_audio = noise_injector.add_white_noise(
            audio.astype(np.int16),
            snr_db=20  # Moderate noise
        )

        # Save
        noisy_path = temp_audio_dir / "noisy.wav"
        sf.write(str(noisy_path), noisy_audio, sr)

        # Test
        result = test_runner.run_stt_test(
            str(noisy_path),
            expected_text=command,
            max_wer=0.7  # Allow higher WER with noise
        )

        # Should still be reasonable
        assert result.wer < 0.8, f"WER too high with noise: {result.wer:.2f}"

    def test_transcribe_repeated_text(self, generator, test_runner, temp_audio_dir):
        """Test transcription of repeated text."""
        command = "ligar luz ligar luz"

        audio_path = generator.generate_command(
            command=command,
            output_path=str(temp_audio_dir / "repeated.wav")
        )

        result = test_runner.run_stt_test(
            audio_path,
            expected_text=command,
            max_wer=0.6
        )

        # Check that text was transcribed
        assert len(result.text) > 0, "No text transcribed"
        assert "ligar" in result.text.lower(), "Key word missing"

    def test_transcribe_numbers(self, generator, test_runner, temp_audio_dir):
        """Test transcription of commands with numbers."""
        command = "volume 50"

        audio_path = generator.generate_command(
            command=command,
            output_path=str(temp_audio_dir / "numbers.wav")
        )

        result = test_runner.run_stt_test(
            audio_path,
            expected_text=command,
            max_wer=0.7  # Numbers may be harder
        )

        # Should have transcribed something
        assert len(result.text) > 0


class TestSTTMetrics:
    """Test STT metrics and WER calculation."""

    def test_wer_perfect_match(self):
        """Test WER with perfect match."""
        from tests.src.test_framework import calculate_wer

        wer = calculate_wer("ligar a luz", "ligar a luz")
        assert wer == 0.0, f"Expected WER=0.0, got {wer}"

    def test_wer_substitution(self):
        """Test WER with substitution."""
        from tests.src.test_framework import calculate_wer

        wer = calculate_wer("desligar a luz", "ligar a luz")
        # 1 substitution / 3 words = 0.33
        assert 0.3 < wer < 0.4, f"Expected WER~0.33, got {wer}"

    def test_wer_deletion(self):
        """Test WER with deletion."""
        from tests.src.test_framework import calculate_wer

        wer = calculate_wer("ligar luz", "ligar a luz")
        # 1 deletion / 3 words = 0.33
        assert 0.3 < wer < 0.4, f"Expected WER~0.33, got {wer}"

    def test_wer_insertion(self):
        """Test WER with insertion."""
        from tests.src.test_framework import calculate_wer

        wer = calculate_wer("ligar as luz", "ligar a luz")
        # 1 substitution / 3 words = 0.33
        assert 0.3 < wer < 0.4, f"Expected WER~0.33, got {wer}"

    def test_wer_case_insensitive(self):
        """Test that WER is case-insensitive."""
        from tests.src.test_framework import calculate_wer

        wer1 = calculate_wer("Ligar A Luz", "ligar a luz")
        wer2 = calculate_wer("ligar a luz", "ligar a luz")

        assert wer1 == wer2, "WER should be case-insensitive"

    def test_wer_empty_reference(self):
        """Test WER with empty reference."""
        from tests.src.test_framework import calculate_wer

        # Empty reference, empty hypothesis = 0% error
        wer = calculate_wer("", "")
        assert wer == 0.0

        # Empty reference, non-empty hypothesis = 100% error
        wer = calculate_wer("hello", "")
        assert wer == 1.0


class TestSTTPerformance:
    """Test STT performance."""

    def test_processing_time_short_audio(self, generator, test_runner, temp_audio_dir):
        """Test that short audio is processed quickly."""
        command = "ok"

        audio_path = generator.generate_command(
            command=command,
            output_path=str(temp_audio_dir / "short.wav")
        )

        result = test_runner.run_stt_test(
            audio_path,
            expected_text=command,
            max_wer=1.0  # Don't care about accuracy here
        )

        # Should process short audio in < 1 second
        assert result.processing_time_ms < 1000, \
            f"Processing too slow: {result.processing_time_ms:.0f}ms"

    def test_processing_time_longer_audio(self, generator, test_runner, temp_audio_dir):
        """Test processing time for longer audio."""
        command = "ligar a luz do quarto e abrir a porta da cozinha"

        audio_path = generator.generate_command(
            command=command,
            output_path=str(temp_audio_dir / "long.wav")
        )

        result = test_runner.run_stt_test(
            audio_path,
            expected_text=command,
            max_wer=0.7
        )

        # Should process reasonable length audio in < 3 seconds
        assert result.processing_time_ms < 3000, \
            f"Processing too slow: {result.processing_time_ms:.0f}ms"
