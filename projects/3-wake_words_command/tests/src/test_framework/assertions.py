"""
Custom assertions for audio testing.
Provides pytest-compatible assertion helpers.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AssertionError(Exception):
    """Custom assertion error."""
    pass


def assert_wake_word_detected(result, min_detections: int = 1, msg: Optional[str] = None):
    """
    Assert that wake word was detected.

    Args:
        result: WakeWordTestResult or similar object
        min_detections: Minimum number of detections required
        msg: Custom error message

    Raises:
        AssertionError: If assertion fails
    """
    detected = getattr(result, 'detected', False)
    num_detections = getattr(result, 'num_detections', 1 if detected else 0)

    if not detected or num_detections < min_detections:
        error_msg = msg or f"Wake word not detected (got {num_detections} detections, expected >= {min_detections})"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)

    logger.info(f"✅ Assertion passed: Wake word detected ({num_detections} times)")


def assert_wake_word_not_detected(result, msg: Optional[str] = None):
    """
    Assert that wake word was NOT detected (false positive test).

    Args:
        result: WakeWordTestResult or similar object
        msg: Custom error message

    Raises:
        AssertionError: If wake word was detected
    """
    detected = getattr(result, 'detected', False)

    if detected:
        error_msg = msg or f"Wake word falsely detected (should not have been)"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)

    logger.info("✅ Assertion passed: Wake word NOT detected (correctly)")


def assert_stt_transcription(result, expected_text: str, max_wer: float = 0.5, msg: Optional[str] = None):
    """
    Assert that STT transcription matches expected text.

    Args:
        result: STTTestResult or similar object
        expected_text: Expected transcription
        max_wer: Maximum acceptable WER (default 0.5 = 50%)
        msg: Custom error message

    Raises:
        AssertionError: If WER exceeds threshold
    """
    text = getattr(result, 'text', '')
    wer = getattr(result, 'wer', 1.0)

    if wer > max_wer:
        error_msg = msg or f"STT transcription WER too high: {wer*100:.1f}% (max {max_wer*100:.1f}%)"
        error_msg += f"\n  Expected: '{expected_text}'"
        error_msg += f"\n  Got: '{text}'"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)

    logger.info(f"✅ Assertion passed: STT transcription acceptable (WER: {wer*100:.1f}%)")


def assert_wer_below(wer: float, threshold: float, msg: Optional[str] = None):
    """
    Assert that WER is below threshold.

    Args:
        wer: Word Error Rate (0.0 to 1.0)
        threshold: Maximum acceptable WER
        msg: Custom error message

    Raises:
        AssertionError: If WER exceeds threshold
    """
    if wer > threshold:
        error_msg = msg or f"WER {wer*100:.1f}% exceeds threshold {threshold*100:.1f}%"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)

    logger.info(f"✅ Assertion passed: WER {wer*100:.1f}% <= {threshold*100:.1f}%")


def assert_audio_level_above(audio, threshold: float = 0.01, msg: Optional[str] = None):
    """
    Assert that audio level is above threshold (not silent).

    Args:
        audio: Audio array
        threshold: Minimum RMS level
        msg: Custom error message

    Raises:
        AssertionError: If audio is too quiet
    """
    from .metrics import calculate_audio_level

    level = calculate_audio_level(audio)

    if level < threshold:
        error_msg = msg or f"Audio level too low: {level:.4f} (threshold: {threshold:.4f})"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)

    logger.info(f"✅ Assertion passed: Audio level {level:.4f} >= {threshold:.4f}")


def assert_processing_time_below(result, max_time_ms: float, msg: Optional[str] = None):
    """
    Assert that processing time is below threshold.

    Args:
        result: Result object with processing_time_ms attribute
        max_time_ms: Maximum acceptable processing time (ms)
        msg: Custom error message

    Raises:
        AssertionError: If processing is too slow
    """
    time_ms = getattr(result, 'processing_time_ms', 0) or getattr(result, 'detection_time_ms', 0) or getattr(result, 'total_time_ms', 0)

    if time_ms > max_time_ms:
        error_msg = msg or f"Processing time too slow: {time_ms:.1f}ms (max {max_time_ms:.1f}ms)"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)

    logger.info(f"✅ Assertion passed: Processing time {time_ms:.1f}ms <= {max_time_ms:.1f}ms")


def assert_file_exists(path: str, msg: Optional[str] = None):
    """
    Assert that file exists.

    Args:
        path: File path
        msg: Custom error message

    Raises:
        AssertionError: If file doesn't exist
    """
    from pathlib import Path

    if not Path(path).exists():
        error_msg = msg or f"File does not exist: {path}"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)

    logger.info(f"✅ Assertion passed: File exists: {path}")


# Pytest-style assertion functions (can be used with pytest.raises)
def assert_true(condition, msg: Optional[str] = None):
    """Assert condition is True."""
    if not condition:
        error_msg = msg or f"Expected True, got False"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)
    logger.info("✅ Assertion passed: condition is True")


def assert_false(condition, msg: Optional[str] = None):
    """Assert condition is False."""
    if condition:
        error_msg = msg or f"Expected False, got True"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)
    logger.info("✅ Assertion passed: condition is False")


def assert_equal(a, b, msg: Optional[str] = None):
    """Assert two values are equal."""
    if a != b:
        error_msg = msg or f"Values not equal: {a} != {b}"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)
    logger.info(f"✅ Assertion passed: {a} == {b}")


def assert_not_equal(a, b, msg: Optional[str] = None):
    """Assert two values are not equal."""
    if a == b:
        error_msg = msg or f"Values are equal: {a} == {b}"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)
    logger.info(f"✅ Assertion passed: {a} != {b}")


def assert_in_range(value, min_val, max_val, msg: Optional[str] = None):
    """Assert value is within range [min_val, max_val]."""
    if not (min_val <= value <= max_val):
        error_msg = msg or f"Value {value} not in range [{min_val}, {max_val}]"
        logger.error(f"❌ Assertion failed: {error_msg}")
        raise AssertionError(error_msg)
    logger.info(f"✅ Assertion passed: {value} in range [{min_val}, {max_val}]")


if __name__ == "__main__":
    # Test assertions
    print("Testing assertions...\n")

    from dataclasses import dataclass

    @dataclass
    class MockResult:
        detected: bool = True
        num_detections: int = 2
        text: str = "hello world"
        wer: float = 0.1
        processing_time_ms: float = 100.0

    result = MockResult()

    print("1. Testing assert_wake_word_detected...")
    assert_wake_word_detected(result, min_detections=1)

    print("2. Testing assert_wer_below...")
    assert_wer_below(result.wer, 0.5)

    print("3. Testing assert_processing_time_below...")
    assert_processing_time_below(result, 200)

    print("\n✅ All assertion tests passed!")
