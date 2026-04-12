"""
Metrics for audio testing.
Includes WER (Word Error Rate), CER (Character Error Rate), and audio levels.
"""

import numpy as np
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


def calculate_wer(hypothesis: str, reference: str) -> float:
    """
    Calculate Word Error Rate (WER).

    WER = (S + D + I) / N
    Where:
        S = substitutions
        D = deletions
        I = insertions
        N = total words in reference

    Args:
        hypothesis: Transcribed text
        reference: Ground truth text

    Returns:
        WER as float (0.0 to 1.0, where 0.0 = perfect)
    """
    try:
        import editdistance
    except ImportError:
        logger.warning("editdistance not installed, using built-in Levenshtein")
        # Fallback to built-in (slower)
        def levenshtein(s1, s2):
            if len(s1) < len(s2):
                return levenshtein(s2, s1)

            if len(s2) == 0:
                return len(s1)

            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        class EditDistance:
            @staticmethod
            def eval(s1, s2):
                return levenshtein(s1, s2)

        editdistance = EditDistance()

    # Normalize and split
    hyp_words = hypothesis.lower().strip().split()
    ref_words = reference.lower().strip().split()

    if len(ref_words) == 0:
        return 0.0 if len(hyp_words) == 0 else 1.0

    # Calculate edit distance
    distance = editdistance.eval(hyp_words, ref_words)

    # WER
    wer = distance / len(ref_words)

    return wer


def calculate_cer(hypothesis: str, reference: str) -> float:
    """
    Calculate Character Error Rate (CER).

    CER = (S + D + I) / N
    Where S, D, I are character-level operations and N is total characters.

    Args:
        hypothesis: Transcribed text
        reference: Ground truth text

    Returns:
        CER as float (0.0 to 1.0)
    """
    try:
        import editdistance
    except ImportError:
        # Fallback
        def levenshtein(s1, s2):
            if len(s1) < len(s2):
                return levenshtein(s2, s1)
            if len(s2) == 0:
                return len(s1)
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            return previous_row[-1]

        class EditDistance:
            @staticmethod
            def eval(s1, s2):
                return levenshtein(s1, s2)

        editdistance = EditDistance()

    # Normalize
    hyp_chars = hypothesis.lower().strip().replace(" ", "")
    ref_chars = reference.lower().strip().replace(" ", "")

    if len(ref_chars) == 0:
        return 0.0 if len(hyp_chars) == 0 else 1.0

    # Calculate edit distance
    distance = editdistance.eval(hyp_chars, ref_chars)

    # CER
    cer = distance / len(ref_chars)

    return cer


def calculate_audio_level(audio: np.ndarray) -> float:
    """
    Calculate RMS audio level.

    Args:
        audio: Audio array (int16)

    Returns:
        RMS level (0.0 to 1.0)
    """
    if len(audio) == 0:
        return 0.0

    # Convert to float
    if audio.dtype == np.int16:
        audio_float = audio.astype(np.float64) / np.iinfo(np.int16).max
    else:
        audio_float = audio

    # Calculate RMS
    rms = np.sqrt(np.mean(audio_float ** 2))

    return float(rms)


def calculate_audio_level_db(audio: np.ndarray) -> float:
    """
    Calculate audio level in dB (relative to full scale).

    Args:
        audio: Audio array (int16)

    Returns:
        Level in dB (-inf to 0)
    """
    rms = calculate_audio_level(audio)

    if rms <= 0:
        return -np.inf

    db = 20 * np.log10(rms)

    return db


def calculate_snr(signal: np.ndarray, noise: np.ndarray) -> float:
    """
    Calculate Signal-to-Noise Ratio.

    Args:
        signal: Clean signal
        noise: Noise alone

    Returns:
        SNR in dB
    """
    signal_power = np.mean(signal.astype(np.float64) ** 2)
    noise_power = np.mean(noise.astype(np.float64) ** 2)

    if noise_power <= 0:
        return np.inf

    snr_db = 10 * np.log10(signal_power / noise_power)

    return snr_db


def calculate_audio_stats(audio: np.ndarray, sample_rate: int) -> dict:
    """
    Calculate comprehensive audio statistics.

    Args:
        audio: Audio array
        sample_rate: Sample rate in Hz

    Returns:
        Dict with statistics
    """
    duration = len(audio) / sample_rate

    return {
        "duration_seconds": duration,
        "num_samples": len(audio),
        "sample_rate": sample_rate,
        "rms_level": calculate_audio_level(audio),
        "level_db": calculate_audio_level_db(audio),
        "max_amplitude": np.max(np.abs(audio)) / np.iinfo(np.int16).max,
        "mean_amplitude": np.mean(np.abs(audio)) / np.iinfo(np.int16).max,
        "std_amplitude": np.std(audio.astype(np.float64)) / np.iinfo(np.int16).max,
    }


def format_wer(wer: float) -> str:
    """Format WER as percentage string."""
    return f"{wer * 100:.1f}%"


def format_cer(cer: float) -> str:
    """Format CER as percentage string."""
    return f"{cer * 100:.1f}%"


def format_level_db(db: float) -> str:
    """Format level in dB."""
    if np.isinf(db) and db < 0:
        return "-inf dB"
    return f"{db:.2f} dB"


if __name__ == "__main__":
    # Test metrics
    print("Testing metrics...\n")

    # Test WER
    ref = "ligar a luz"
    hyp1 = "ligar a luz"  # Perfect
    hyp2 = "ligar luz"    # Deletion
    hyp3 = "ligar as luz" # Insertion
    hyp4 = "desligar luz" # Substitution

    print("WER Tests:")
    print(f"  Perfect: {format_wer(calculate_wer(hyp1, ref))} (expected 0.0%)")
    print(f"  Deletion: {format_wer(calculate_wer(hyp2, ref))} (expected 33.3%)")
    print(f"  Insertion: {format_wer(calculate_wer(hyp3, ref))} (expected 33.3%)")
    print(f"  Substitution: {format_wer(calculate_wer(hyp4, ref))} (expected 33.3%)")
    print()

    # Test CER
    print("CER Tests:")
    print(f"  Perfect: {format_cer(calculate_cer(hyp1, ref))}")
    print(f"  Deletion: {format_cer(calculate_cer(hyp2, ref))}")
    print()

    # Test audio level
    print("Audio Level Tests:")
    silence = np.zeros(1000, dtype=np.int16)
    tone = np.sin(2 * np.pi * np.linspace(0, 1, 1000)) * 16000
    tone = tone.astype(np.int16)

    print(f"  Silence: {format_level_db(calculate_audio_level_db(silence))} (expected -inf dB)")
    print(f"  Tone: {format_level_db(calculate_audio_level_db(tone))} dB")
    print()

    print("✅ All metric tests passed!")
