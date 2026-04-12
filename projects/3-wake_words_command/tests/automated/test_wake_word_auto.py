"""
Automated tests for wake word detection using TTS-generated audio.
"""

import pytest
import numpy as np
from pathlib import Path

from tests.src.audio_generation import AudioGenerator, Pyttsx3TTS
from tests.src.test_framework import assert_wake_word_detected, assert_wake_word_not_detected


class TestWakeWordTTS:
    """Test wake word detection with TTS-generated audio."""

    @pytest.fixture
    def generator(self, sample_rate):
        """Create audio generator."""
        tts = Pyttsx3TTS(rate=150)
        return AudioGenerator(tts_engine=tts, sample_rate=sample_rate)

    def test_detect_porcupine_tts(self, generator, test_runner, temp_audio_dir):
        """Test detection of 'porcupine' generated via TTS."""
        # Generate wake word
        audio_path = generator.generate_wake_word(
            keyword="porcupine",
            output_path=str(temp_audio_dir / "porcupine.wav")
        )

        # Test detection
        result = test_runner.run_wake_word_test(audio_path, expected_detect=True)

        # Assert
        assert_wake_word_detected(result, min_detections=1)

    @pytest.mark.parametrize("keyword", [
        "porcupine",
        "computer",
    ])
    def test_detect_various_keywords(self, keyword, generator, test_runner, temp_audio_dir):
        """Test detection of various wake words."""
        # Note: Only works if keyword is configured in Porcupine
        # Default is "porcupine", others may fail

        audio_path = generator.generate_wake_word(
            keyword=keyword,
            output_path=str(temp_audio_dir / f"{keyword}.wav")
        )

        result = test_runner.run_wake_word_test(
            audio_path,
            expected_detect=(keyword == "porcupine")  # Only porcupine configured
        )

        if keyword == "porcupine":
            assert_wake_word_detected(result)
        else:
            # Other keywords may not be detected
            pytest.xfail(f"Keyword '{keyword}' not configured in Porcupine")

    def test_detect_with_silence_prefix(self, generator, test_runner, temp_audio_dir):
        """Test detection with silence before wake word."""
        from tests.src.audio_generation import AudioGenerator

        # Generate wake word
        ww_path = generator.generate_wake_word(
            keyword="porcupine",
            output_path=str(temp_audio_dir / "ww.wav")
        )

        # Add silence
        silence = generator.generate_silence(2.0)  # 2 seconds

        # Concatenate
        import soundfile as sf
        ww_audio, sr = sf.read(ww_path)

        if len(ww_audio.shape) > 1:
            ww_audio = ww_audio[:, 0]

        combined = np.concatenate([silence, ww_audio.astype(np.float64)])

        output_path = temp_audio_dir / "with_silence.wav"
        sf.write(str(output_path), combined, sr)

        # Test
        result = test_runner.run_wake_word_test(str(output_path), expected_detect=True)
        assert_wake_word_detected(result)

    @pytest.mark.parametrize("snr_db", [30, 20, 10])
    def test_detect_with_noise(self, snr_db, generator, test_runner, noise_injector, temp_audio_dir):
        """Test detection with various noise levels."""
        # Generate clean audio
        clean_path = generator.generate_wake_word(
            keyword="porcupine",
            output_path=str(temp_audio_dir / "clean.wav")
        )

        # Load and add noise
        import soundfile as sf
        audio, sr = sf.read(clean_path)

        if len(audio.shape) > 1:
            audio = audio[:, 0]

        noisy_audio = noise_injector.add_white_noise(
            audio.astype(np.int16),
            snr_db=snr_db
        )

        # Save noisy audio
        noisy_path = temp_audio_dir / f"noisy_{snr_db}db.wav"
        sf.write(str(noisy_path), noisy_audio, sr)

        # Test
        result = test_runner.run_wake_word_test(str(noisy_path), expected_detect=True)

        # Should still detect at SNR >= 10dB
        if snr_db >= 10:
            assert_wake_word_detected(result)
        else:
            # May fail at very low SNR
            pytest.xfail(f"Detection may fail at SNR {snr_db}dB")

    def test_multiple_detections(self, generator, test_runner, temp_audio_dir):
        """Test multiple wake words in sequence."""
        # Generate multiple wake words
        ww1_path = generator.generate_wake_word("porcupine", str(temp_audio_dir / "ww1.wav"))
        ww2_path = generator.generate_wake_word("porcupine", str(temp_audio_dir / "ww2.wav"))

        # Concatenate with silence
        combined_path = generator.concatenate_audio(
            [ww1_path, ww2_path],
            str(temp_audio_dir / "multiple.wav"),
            silence_between=1.0
        )

        # Test
        result = test_runner.run_wake_word_test(combined_path, expected_detect=True)

        # Should detect at least once (ideally twice)
        assert_wake_word_detected(result, min_detections=1)
        assert result.num_detections >= 1


class TestWakeWordSynthetic:
    """Test wake word detection with synthetic audio."""

    def test_silence_no_detection(self, test_runner, temp_audio_dir):
        """Test that silence doesn't trigger false detection."""
        from tests.src.audio_generation import AudioGenerator

        generator = AudioGenerator()
        silence = generator.generate_silence(2.0)

        import soundfile as sf
        silence_path = temp_audio_dir / "silence.wav"
        sf.write(str(silence_path), silence, 16000)

        result = test_runner.run_wake_word_test(str(silence_path), expected_detect=False)

        assert_wake_word_not_detected(result)

    def test_tone_no_detection(self, test_runner, temp_audio_dir):
        """Test that pure tones don't trigger false detection."""
        from tests.src.audio_generation import AudioGenerator

        generator = AudioGenerator()

        # Generate various tones
        for freq in [440, 1000, 2000]:
            tone = generator.generate_tone(freq, duration=1.0)

            import soundfile as sf
            tone_path = temp_audio_dir / f"tone_{freq}hz.wav"
            sf.write(str(tone_path), tone, 16000)

            result = test_runner.run_wake_word_test(str(tone_path), expected_detect=False)

            assert_wake_word_not_detected(result)


class TestWakeWordPreRecorded:
    """Test with pre-recorded audio (if available)."""

    def test_with_library_audio(self, test_runner, test_library_dir):
        """Test with pre-recorded wake words from library."""
        wake_words_dir = test_library_dir / "wake_words"

        if not wake_words_dir.exists():
            pytest.skip("No pre-recorded audio library")

        # Find all WAV files
        wav_files = list(wake_words_dir.glob("*.wav"))

        if not wav_files:
            pytest.skip("No WAV files in library")

        # Test first file
        audio_path = wav_files[0]
        result = test_runner.run_wake_word_test(str(audio_path), expected_detect=True)

        assert_wake_word_detected(result)
