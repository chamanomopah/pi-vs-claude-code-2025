"""
Sistema Wake Words Command
Detecção de wake words e reconhecimento de comandos de voz.
"""

__version__ = "1.0.0"
__author__ = "Wake Words Project"

from .audio_capture import AudioCapture, AudioDeviceManager
from .logger import WakeWordsLogger, SystemMonitor, AudioLogger
from .wake_word import WakeWordDetector, WakeWordTester
from .stt_engine import STTEngine, CommandRecorder
from .command_processor import CommandProcessor, Command

__all__ = [
    'AudioCapture',
    'AudioDeviceManager',
    'WakeWordsLogger',
    'SystemMonitor',
    'AudioLogger',
    'WakeWordDetector',
    'WakeWordTester',
    'STTEngine',
    'CommandRecorder',
    'CommandProcessor',
    'Command',
]
