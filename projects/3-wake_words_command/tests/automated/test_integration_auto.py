"""
Integration tests for full workflow: wake word + command.
"""

import pytest
from pathlib import Path

from tests.src.audio_generation import AudioGenerator, Pyttsx3TTS
from tests.src.test_framework import assert_wake_word_detected, assert_wer_below


class TestIntegrationWorkflow:
    """Test complete workflow: wake word detection → command transcription."""

    @pytest.fixture
    def generator(self, sample_rate):
        """Create audio generator."""
        tts = Pyttsx3TTS(rate=150)
        return AudioGenerator(tts_engine=tts, sample_rate=sample_rate)

    @pytest.mark.parametrize("wake_word,command", [
        ("porcupine", "ligar a luz"),
        ("porcupine", "abrir a porta"),
        ("porcupine", "desligar"),
    ])
    def test_full_workflow(self, wake_word, command, generator, test_runner, temp_audio_dir):
        """Test full workflow with wake word and command."""
        # Generate complete scenario
        scenario_path = generator.generate_test_scenario(
            wake_word=wake_word,
            command=command,
            output_path=str(temp_audio_dir / f"scenario_{command.replace(' ', '_')}.wav")
        )

        # Need to split into separate files for integration test
        ww_path = generator.generate_wake_word(wake_word, str(temp_audio_dir / "ww.wav"))
        cmd_path = generator.generate_command(command, str(temp_audio_dir / "cmd.wav"))

        # Run integration test
        result = test_runner.run_integration_test(
            wake_word_path=ww_path,
            command_path=cmd_path,
            expected_command=command
        )

        # Assert
        assert result.wake_word_detected, "Wake word not detected"
        assert_wer_below(result.command_wer, 0.6, f"WER too high: {result.command_wer:.2f}")
        assert result.total_time_ms < 3000, f"Processing too slow: {result.total_time_ms:.0f}ms"

    def test_workflow_with_noise(self, generator, test_runner, noise_injector, temp_audio_dir):
        """Test workflow with noisy audio."""
        wake_word = "porcupine"
        command = "ligar a luz"

        # Generate clean audio
        ww_clean = generator.generate_wake_word(wake_word, str(temp_audio_dir / "ww_clean.wav"))
        cmd_clean = generator.generate_command(command, str(temp_audio_dir / "cmd_clean.wav"))

        # Add noise to both
        import soundfile as sf
        import numpy as np

        for clean_path, noisy_name in [(ww_clean, "ww_noisy"), (cmd_clean, "cmd_noisy")]:
            audio, sr = sf.read(clean_path)
            if len(audio.shape) > 1:
                audio = audio[:, 0]

            noisy = noise_injector.add_white_noise(audio.astype(np.int16), snr_db=15)
            noisy_path = temp_audio_dir / f"{noisy_name}.wav"
            sf.write(str(noisy_path), noisy, sr)

        # Test with noisy audio
        result = test_runner.run_integration_test(
            wake_word_path=str(temp_audio_dir / "ww_noisy.wav"),
            command_path=str(temp_audio_dir / "cmd_noisy.wav"),
            expected_command=command
        )

        # Should still work with moderate noise
        assert result.wake_word_detected, "Wake word not detected in noise"

    def test_workflow_multiple_commands(self, generator, test_runner, temp_audio_dir):
        """Test processing multiple commands in sequence."""
        commands = ["ligar a luz", "desligar a luz", "abrir a porta"]

        results = []

        for command in commands:
            # Generate scenario
            ww_path = generator.generate_wake_word("porcupine")
            cmd_path = generator.generate_command(command)

            # Test
            result = test_runner.run_integration_test(
                wake_word_path=ww_path,
                command_path=cmd_path,
                expected_command=command
            )

            results.append(result)

        # Check that at least 2 out of 3 worked
        successful = sum(1 for r in results if r.wake_word_detected and r.command_wer < 0.7)

        assert successful >= 2, f"Only {successful}/{len(commands)} commands succeeded"

    def test_end_to_end_timing(self, generator, test_runner, temp_audio_dir):
        """Test that end-to-end workflow completes in reasonable time."""
        # Generate
        ww_path = generator.generate_wake_word("porcupine", str(temp_audio_dir / "ww.wav"))
        cmd_path = generator.generate_command("ok", str(temp_audio_dir / "cmd.wav"))

        # Time the full workflow
        import time
        start = time.time()

        result = test_runner.run_integration_test(
            wake_word_path=ww_path,
            command_path=cmd_path,
            expected_command="ok"
        )

        elapsed = (time.time() - start) * 1000

        # Full workflow should be fast
        assert elapsed < 5000, f"Workflow too slow: {elapsed:.0f}ms"


class TestIntegrationEdgeCases:
    """Test edge cases in integration workflow."""

    def test_very_short_command(self, generator, test_runner, temp_audio_dir):
        """Test with very short command."""
        ww_path = generator.generate_wake_word("porcupine")
        cmd_path = generator.generate_command("ok")  # Very short

        result = test_runner.run_integration_test(
            wake_word_path=ww_path,
            command_path=cmd_path,
            expected_command="ok"
        )

        # Wake word should definitely be detected
        assert result.wake_word_detected

    def test_very_long_command(self, generator, test_runner, temp_audio_dir):
        """Test with very long command."""
        long_command = "ligar a luz da sala e abrir a janela do quarto e fechar a porta da cozinha"

        ww_path = generator.generate_wake_word("porcupine")
        cmd_path = generator.generate_command(long_command)

        result = test_runner.run_integration_test(
            wake_word_path=ww_path,
            command_path=cmd_path,
            expected_command=long_command
        )

        # Should detect wake word
        assert result.wake_word_detected

        # Transcription may not be perfect but should have some words
        assert len(result.command_transcribed) > 10, "Transcription too short"

    def test_command_with_numbers(self, generator, test_runner, temp_audio_dir):
        """Test command with numbers."""
        command = "volume 50"

        ww_path = generator.generate_wake_word("porcupine")
        cmd_path = generator.generate_command(command)

        result = test_runner.run_integration_test(
            wake_word_path=ww_path,
            command_path=cmd_path,
            expected_command=command
        )

        assert result.wake_word_detected

    def test_similar_sounding_commands(self, generator, test_runner, temp_audio_dir):
        """Test commands that sound similar."""
        commands = ["ligar", "desligar"]

        results = []
        for command in commands:
            ww_path = generator.generate_wake_word("porcupine")
            cmd_path = generator.generate_command(command)

            result = test_runner.run_integration_test(
                wake_word_path=ww_path,
                command_path=cmd_path,
                expected_command=command
            )

            results.append((command, result))

        # Both should detect wake word
        for cmd, result in results:
            assert result.wake_word_detected, f"Wake word not detected for '{cmd}'"


class TestIntegrationWithPreRecorded:
    """Test with pre-recorded audio (if available)."""

    def test_with_library_audio(self, test_runner, test_library_dir):
        """Test with pre-recorded audio from library."""
        ww_dir = test_library_dir / "wake_words"
        cmd_dir = test_library_dir / "commands"

        if not ww_dir.exists() or not cmd_dir.exists():
            pytest.skip("Pre-recorded library not complete")

        ww_files = list(ww_dir.glob("*.wav"))
        cmd_files = list(cmd_dir.glob("*.wav"))

        if not ww_files or not cmd_files:
            pytest.skip("No audio files in library")

        # Use metadata if available, otherwise test first files
        ww_file = ww_files[0]
        cmd_file = cmd_files[0]

        # Load metadata for expected text
        import json
        metadata_path = cmd_dir / "metadata.json"

        expected_command = "abrir a porta"  # Default

        if metadata_path.exists():
            with open(metadata_path) as f:
                metadata = json.load(f)
                cmd_name = cmd_file.stem
                expected_command = metadata.get(cmd_name, {}).get("text", expected_command)

        # Test
        result = test_runner.run_integration_test(
            wake_word_path=str(ww_file),
            command_path=str(cmd_file),
            expected_command=expected_command
        )

        # At least wake word should be detected
        assert result.wake_word_detected
