"""
Pytest configuration and fixtures for automated audio testing.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent / "src"))


@pytest.fixture(scope="session")
def sample_rate():
    """Standard sample rate for audio tests."""
    return 16000


@pytest.fixture(scope="session")
def access_key():
    """
    Porcupine access key.

    Set via environment variable or pytest.ini.
    """
    import os

    key = os.environ.get("PORCUPINE_ACCESS_KEY")

    if key is None:
        pytest.skip("PORCUPINE_ACCESS_KEY not set")

    return key


@pytest.fixture(scope="session")
def vosk_model_path():
    """
    Path to Vosk model.

    Set via environment variable or use default.
    """
    import os

    model_path = os.environ.get("VOSK_MODEL_PATH",
                                 Path(__file__).parent.parent.parent / "models" / "vosk-model-small-pt-0.3")

    model_path = Path(model_path)

    if not model_path.exists():
        pytest.skip(f"Vosk model not found at {model_path}")

    return str(model_path)


@pytest.fixture(scope="session")
def wake_word_detector(access_key):
    """
    Initialize Porcupine wake word detector.

    Uses keyword "porcupine" by default.
    """
    from src.wake_word import WakeWordDetector

    detector = WakeWordDetector(
        access_key=access_key,
        keyword="porcupine",
        sensitivity=0.5
    )

    yield detector

    # Cleanup
    detector.release()


@pytest.fixture(scope="session")
def stt_engine(vosk_model_path):
    """
    Initialize Vosk STT engine.
    """
    from src.stt_engine import STTEngine

    engine = STTEngine(
        model_path=vosk_model_path,
        sample_rate=16000
    )

    yield engine

    # Cleanup
    engine.release()


@pytest.fixture(scope="session")
def audio_generator():
    """
    Initialize audio generator (TTS).
    """
    from tests.src.audio_generation import AudioGenerator, Pyttsx3TTS

    tts = Pyttsx3TTS(rate=150)
    generator = AudioGenerator(tts_engine=tts)

    return generator


@pytest.fixture(scope="session")
def noise_injector():
    """
    Initialize noise injector.
    """
    from tests.src.audio_generation import NoiseInjector

    return NoiseInjector()


@pytest.fixture(scope="session")
def test_runner(wake_word_detector, stt_engine):
    """
    Initialize audio test runner.
    """
    from tests.src.test_framework import AudioTestRunner

    runner = AudioTestRunner(
        wake_word_detector=wake_word_detector,
        stt_engine=stt_engine
    )

    return runner


@pytest.fixture
def temp_audio_dir(tmp_path):
    """
    Temporary directory for audio files.
    """
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir()
    return audio_dir


@pytest.fixture
def test_library_dir():
    """
    Path to test audio library.
    """
    lib_dir = Path(__file__).parent / "audio_library"
    return lib_dir


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "tts: marks tests that require TTS generation"
    )
