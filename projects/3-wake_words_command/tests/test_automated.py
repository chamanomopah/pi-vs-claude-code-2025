#!/usr/bin/env python
"""
Automated Audio Testing - Main Entry Point
Tests wake words and STT without human interaction using TTS.

Usage:
    python tests/test_automated.py                    # Run all tests
    python tests/test_automated.py --wake-word        # Test wake word only
    python tests/test_automated.py --stt              # Test STT only
    python tests/test_automated.py --integration      # Test integration only
    python tests/test_automated.py --generate-audio   # Generate test audio
    python tests/test_automated.py --quick            # Quick test suite

Environment Variables:
    PORCUPINE_ACCESS_KEY: Required for wake word tests
    VOSK_MODEL_PATH: Path to Vosk model (default: models/vosk-model-small-pt-0.3)

Examples:
    # Set keys and run all tests
    set PORCUPINE_ACCESS_KEY=your_key_here
    python tests/test_automated.py

    # Quick test (fewer tests)
    python tests/test_automated.py --quick

    # Generate audio library first
    python tests/test_automated.py --generate-audio
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Add paths
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests" / "src"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(ROOT / "logs" / "automated_tests.log")
    ]
)

logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []

    try:
        import pytest
    except ImportError:
        missing.append("pytest")

    try:
        import pvporcupine
    except ImportError:
        missing.append("pvporcupine")

    try:
        import vosk
    except ImportError:
        missing.append("vosk")

    try:
        import pyttsx3
    except ImportError:
        missing.append("pyttsx3")

    if missing:
        logger.error(f"❌ Missing dependencies: {', '.join(missing)}")
        logger.error("Install with: pip install " + " ".join(missing))
        return False

    logger.info("✅ All dependencies installed")
    return True


def check_environment():
    """Check if environment variables are set."""
    access_key = os.environ.get("PORCUPINE_ACCESS_KEY")

    if not access_key:
        logger.warning("⚠️  PORCUPINE_ACCESS_KEY not set")
        logger.warning("Wake word tests will be skipped")
        logger.warning("Get your key at: https://console.picovoice.ai/")
    else:
        logger.info("✅ PORCUPINE_ACCESS_KEY is set")

    model_path = os.environ.get("VOSK_MODEL_PATH",
                                 str(ROOT / "models" / "vosk-model-small-pt-0.3"))

    if Path(model_path).exists():
        logger.info(f"✅ Vosk model found: {model_path}")
    else:
        logger.warning(f"⚠️  Vosk model not found: {model_path}")
        logger.warning("STT tests will be skipped")
        logger.warning("Download from: https://alphacephei.com/vosk/models")

    return True


def generate_audio_library():
    """Generate audio library for testing."""
    logger.info("📝 Generating audio library...")

    from tests.src.audio_generation import AudioGenerator, Pyttsx3TTS, NoiseInjector

    tts = Pyttsx3TTS(rate=150)
    generator = AudioGenerator(tts_engine=tts)
    injector = NoiseInjector()

    # Create output directory
    output_dir = ROOT / "tests" / "audio_library" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate wake words
    logger.info("Generating wake words...")
    for keyword in ["porcupine", "computer"]:
        path = generator.generate_wake_word(keyword, str(output_dir / f"ww_{keyword}.wav"))
        logger.info(f"  - {keyword}: {path}")

    # Generate commands
    logger.info("Generating commands...")
    commands = [
        "ligar a luz",
        "desligar a luz",
        "abrir a porta",
        "fechar a porta",
        "volume 50",
        "ok",
        "sim",
        "não",
    ]

    for command in commands:
        safe_name = command.replace(" ", "_").replace("'", "")
        path = generator.generate_command(command, str(output_dir / f"cmd_{safe_name}.wav"))
        logger.info(f"  - '{command}': {path}")

    # Generate scenarios
    logger.info("Generating scenarios...")
    scenarios = [
        ("porcupine", "ligar a luz"),
        ("porcupine", "desligar"),
        ("porcupine", "abrir a porta"),
    ]

    for i, (ww, cmd) in enumerate(scenarios, 1):
        path = generator.generate_test_scenario(ww, cmd, str(output_dir / f"scenario_{i}.wav"))
        logger.info(f"  - Scenario {i}: {path}")

    logger.info(f"✅ Audio library generated: {output_dir}")


def run_tests(test_type="all", quick=False, verbose=False):
    """
    Run pytest tests.

    Args:
        test_type: Type of tests to run ("all", "wake_word", "stt", "integration")
        quick: Run quick test subset
        verbose: Verbose output
    """
    import pytest

    # Build pytest args
    pytest_args = [
        "tests/automated/",
        "-v" if verbose else "",
        "--tb=short",
        "--color=yes",
    ]

    # Add marker options
    if quick:
        pytest_args.extend(["-m", "not slow"])

    # Select test file
    if test_type == "wake_word":
        pytest_args.append("tests/automated/test_wake_word_auto.py")
    elif test_type == "stt":
        pytest_args.append("tests/automated/test_stt_auto.py")
    elif test_type == "integration":
        pytest_args.append("tests/automated/test_integration_auto.py")

    # Filter empty strings
    pytest_args = [arg for arg in pytest_args if arg]

    logger.info(f"🧪 Running tests: {' '.join(pytest_args)}")

    # Run pytest
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        logger.info("✅ All tests passed!")
    else:
        logger.error(f"❌ Tests failed with exit code {exit_code}")

    return exit_code


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automated Audio Testing for Wake Words",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tests/test_automated.py                 # Run all tests
  python tests/test_automated.py --wake-word     # Test wake word only
  python tests/test_automated.py --quick         # Quick test suite
  python tests/test_automated.py --generate-audio  # Generate audio library

Environment Variables:
  PORCUPINE_ACCESS_KEY    Required for wake word tests
  VOSK_MODEL_PATH         Path to Vosk model
        """
    )

    parser.add_argument("--wake-word", action="store_true",
                       help="Run wake word tests only")
    parser.add_argument("--stt", action="store_true",
                       help="Run STT tests only")
    parser.add_argument("--integration", action="store_true",
                       help="Run integration tests only")
    parser.add_argument("--quick", "-q", action="store_true",
                       help="Run quick test subset")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    parser.add_argument("--generate-audio", action="store_true",
                       help="Generate audio library")
    parser.add_argument("--skip-checks", action="store_true",
                       help="Skip dependency checks")

    args = parser.parse_args()

    # Create logs directory
    (ROOT / "logs").mkdir(exist_ok=True)

    # Print header
    print("\n" + "=" * 70)
    print(" " * 15 + "AUTOMATED AUDIO TESTING")
    print("=" * 70 + "\n")

    # Check dependencies
    if not args.skip_checks:
        if not check_dependencies():
            return 1

        check_environment()

    # Generate audio library
    if args.generate_audio:
        generate_audio_library()
        return 0

    # Determine test type
    test_type = "all"
    if args.wake_word:
        test_type = "wake_word"
    elif args.stt:
        test_type = "stt"
    elif args.integration:
        test_type = "integration"

    # Run tests
    exit_code = run_tests(
        test_type=test_type,
        quick=args.quick,
        verbose=args.verbose
    )

    print("\n" + "=" * 70)
    if exit_code == 0:
        print(" " * 25 + "✅ SUCCESS")
    else:
        print(" " * 25 + "❌ FAILED")
    print("=" * 70 + "\n")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
