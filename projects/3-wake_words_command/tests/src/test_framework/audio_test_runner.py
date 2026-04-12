"""
Audio Test Runner for automated testing.
Runs wake word and STT tests with audio files.
"""

import time
import logging
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, field

import numpy as np

# Import from existing codebase
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from wake_word import WakeWordDetector
from stt_engine import STTEngine
from .metrics import calculate_wer, calculate_audio_level

logger = logging.getLogger(__name__)


@dataclass
class WakeWordTestResult:
    """Result of wake word detection test."""
    detected: bool
    confidence: float = 0.0
    detection_time_ms: float = 0.0
    num_detections: int = 0
    audio_stats: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)


@dataclass
class STTTestResult:
    """Result of STT transcription test."""
    text: str
    expected_text: str
    wer: float = 1.0
    processing_time_ms: float = 0.0
    audio_stats: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)


@dataclass
class IntegrationTestResult:
    """Result of full integration test."""
    wake_word_detected: bool
    command_transcribed: str
    expected_command: str
    command_wer: float = 1.0
    total_time_ms: float = 0.0
    metadata: dict = field(default_factory=dict)


class AudioTestRunner:
    """
    Runs automated tests with audio files.
    """

    def __init__(self,
                 wake_word_detector: Optional[WakeWordDetector] = None,
                 stt_engine: Optional[STTEngine] = None):
        """
        Initialize test runner.

        Args:
            wake_word_detector: Porcupine detector (None = skip WW tests)
            stt_engine: Vosk STT (None = skip STT tests)
        """
        self.detector = wake_word_detector
        self.stt = stt_engine

        logger.info("✅ AudioTestRunner initialized")

    def run_wake_word_test(self,
                           audio_path: str,
                           expected_detect: bool = True,
                           min_confidence: float = 0.0) -> WakeWordTestResult:
        """
        Test wake word detection on audio file.

        Args:
            audio_path: Path to WAV file
            expected_detect: Whether detection is expected
            min_confidence: Minimum confidence threshold (if applicable)

        Returns:
            WakeWordTestResult
        """
        if self.detector is None:
            logger.warning("No wake word detector configured, skipping test")
            return WakeWordTestResult(detected=False, metadata={"skipped": True})

        import soundfile as sf

        logger.info(f"🎯 Testing wake word: {audio_path}")

        start_time = time.time()

        try:
            # Load audio
            audio, sr = sf.read(audio_path)

            # Convert to mono if stereo
            if len(audio.shape) > 1:
                audio = audio[:, 0]

            # Convert to int16 if needed
            if audio.dtype == np.float32 or audio.dtype == np.float64:
                audio = (audio * np.iinfo(np.int16).max).astype(np.int16)

            # Resample if necessary
            if sr != self.detector.sample_rate:
                from scipy import signal
                num_samples = int(len(audio) * self.detector.sample_rate / sr)
                audio = signal.resample(audio, num_samples).astype(np.int16)

            # Process frame by frame
            frame_len = self.detector.frame_length
            detections = 0

            for i in range(0, len(audio) - frame_len, frame_len):
                frame = audio[i:i + frame_len]

                if self.detector.process_frame(frame):
                    detections += 1
                    logger.debug(f"✨ Detection at frame {i}")

            detection_time = (time.time() - start_time) * 1000  # ms

            # Audio stats
            audio_stats = {
                "duration_seconds": len(audio) / sr,
                "num_samples": len(audio),
                "sample_rate": sr,
                "rms_level": float(calculate_audio_level(audio)),
            }

            detected = detections > 0

            result = WakeWordTestResult(
                detected=detected,
                confidence=0.5 if detected else 0.0,  # Porcupine doesn't give confidence
                detection_time_ms=detection_time,
                num_detections=detections,
                audio_stats=audio_stats,
                metadata={
                    "audio_path": str(audio_path),
                    "expected_detect": expected_detect,
                }
            )

            logger.info(f"  Result: {'✅ DETECTED' if detected else '❌ NOT DETECTED'} ({detections} detections, {detection_time:.1f}ms)")

            return result

        except Exception as e:
            logger.error(f"❌ Error in wake word test: {e}")
            return WakeWordTestResult(
                detected=False,
                metadata={"error": str(e), "audio_path": str(audio_path)}
            )

    def run_stt_test(self,
                     audio_path: str,
                     expected_text: str,
                     max_wer: float = 0.5) -> STTTestResult:
        """
        Test STT transcription on audio file.

        Args:
            audio_path: Path to WAV file
            expected_text: Expected transcription
            max_wer: Maximum acceptable WER

        Returns:
            STTTestResult
        """
        if self.stt is None:
            logger.warning("No STT engine configured, skipping test")
            return STTTestResult(
                text="",
                expected_text=expected_text,
                wer=1.0,
                metadata={"skipped": True}
            )

        logger.info(f"🎤 Testing STT: {audio_path}")
        logger.info(f"   Expected: '{expected_text}'")

        start_time = time.time()

        try:
            # Transcribe
            result = self.stt.transcribe_file(audio_path)

            processing_time = (time.time() - start_time) * 1000  # ms

            if result.get("error"):
                logger.error(f"   ❌ STT Error: {result['error']}")
                return STTTestResult(
                    text="",
                    expected_text=expected_text,
                    wer=1.0,
                    processing_time_ms=processing_time,
                    metadata={"error": result["error"]}
                )

            text = result.get("text", "").strip()
            wer = calculate_wer(text, expected_text)

            logger.info(f"   Result: '{text}'")
            logger.info(f"   WER: {wer * 100:.1f}% ({processing_time:.1f}ms)")

            # Audio stats
            import soundfile as sf
            audio, sr = sf.read(audio_path)
            audio_stats = {
                "duration_seconds": len(audio) / sr,
                "num_samples": len(audio),
                "sample_rate": sr,
                "rms_level": float(calculate_audio_level(audio)),
            }

            return STTTestResult(
                text=text,
                expected_text=expected_text,
                wer=wer,
                processing_time_ms=processing_time,
                audio_stats=audio_stats,
                metadata={
                    "audio_path": str(audio_path),
                    "max_wer": max_wer,
                    "passed": wer <= max_wer,
                }
            )

        except Exception as e:
            logger.error(f"❌ Error in STT test: {e}")
            return STTTestResult(
                text="",
                expected_text=expected_text,
                wer=1.0,
                metadata={"error": str(e)}
            )

    def run_integration_test(self,
                             wake_word_path: str,
                             command_path: str,
                             expected_command: str) -> IntegrationTestResult:
        """
        Test full workflow: wake word detection + command transcription.

        Args:
            wake_word_path: Path to wake word audio
            command_path: Path to command audio
            expected_command: Expected command transcription

        Returns:
            IntegrationTestResult
        """
        logger.info("🔄 Running integration test...")

        start_time = time.time()

        # Test wake word
        ww_result = self.run_wake_word_test(wake_word_path, expected_detect=True)

        # Test STT
        stt_result = self.run_stt_test(command_path, expected_command)

        total_time = (time.time() - start_time) * 1000

        result = IntegrationTestResult(
            wake_word_detected=ww_result.detected,
            command_transcribed=stt_result.text,
            expected_command=expected_command,
            command_wer=stt_result.wer,
            total_time_ms=total_time,
            metadata={
                "wake_word_path": str(wake_word_path),
                "command_path": str(command_path),
                "ww_detection_count": ww_result.num_detections,
                "stt_processing_time_ms": stt_result.processing_time_ms,
            }
        )

        logger.info(f"   Wake Word: {'✅' if result.wake_word_detected else '❌'}")
        logger.info(f"   Command: '{result.command_transcribed}' (WER: {result.command_wer * 100:.1f}%)")
        logger.info(f"   Total Time: {total_time:.1f}ms")

        return result

    def batch_test(self, test_cases: List[dict]) -> dict:
        """
        Run multiple tests.

        Args:
            test_cases: List of test case dicts with keys:
                        - type: "wake_word", "stt", or "integration"
                        - audio_path: path to audio
                        - expected: expected result
                        - command_path: (for integration) command audio

        Returns:
            Dict with all results
        """
        results = {
            "wake_word": [],
            "stt": [],
            "integration": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
            }
        }

        for case in test_cases:
            test_type = case.get("type")

            if test_type == "wake_word":
                result = self.run_wake_word_test(
                    case["audio_path"],
                    expected_detect=case.get("expected_detect", True)
                )
                results["wake_word"].append(result)

                if result.metadata.get("skipped"):
                    results["summary"]["skipped"] += 1
                elif result.detected == case.get("expected_detect", True):
                    results["summary"]["passed"] += 1
                else:
                    results["summary"]["failed"] += 1

            elif test_type == "stt":
                result = self.run_stt_test(
                    case["audio_path"],
                    case["expected_text"],
                    max_wer=case.get("max_wer", 0.5)
                )
                results["stt"].append(result)

                if result.metadata.get("skipped"):
                    results["summary"]["skipped"] += 1
                elif result.metadata.get("passed", False):
                    results["summary"]["passed"] += 1
                else:
                    results["summary"]["failed"] += 1

            elif test_type == "integration":
                result = self.run_integration_test(
                    case["wake_word_path"],
                    case["command_path"],
                    case["expected_command"]
                )
                results["integration"].append(result)

                if result.wake_word_detected and result.command_wer < 0.5:
                    results["summary"]["passed"] += 1
                else:
                    results["summary"]["failed"] += 1

            results["summary"]["total"] += 1

        return results


if __name__ == "__main__":
    # Example usage
    print("AudioTestRunner - Example usage\n")
    print("This module is used by test_automated.py")
    print("See tests/automated/ for examples")
