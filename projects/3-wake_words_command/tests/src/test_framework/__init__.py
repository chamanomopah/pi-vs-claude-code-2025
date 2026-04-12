"""
Test Framework for Automated Audio Testing
Provides test runners, assertions, and metrics for wake word and STT testing.
"""

from .audio_test_runner import AudioTestRunner, WakeWordTestResult, STTTestResult, IntegrationTestResult
from .assertions import assert_wake_word_detected, assert_stt_transcription, assert_wer_below
from .metrics import calculate_wer, calculate_cer, calculate_audio_level

__all__ = [
    'AudioTestRunner',
    'WakeWordTestResult',
    'STTTestResult',
    'IntegrationTestResult',
    'assert_wake_word_detected',
    'assert_stt_transcription',
    'assert_wer_below',
    'calculate_wer',
    'calculate_cer',
    'calculate_audio_level',
]
