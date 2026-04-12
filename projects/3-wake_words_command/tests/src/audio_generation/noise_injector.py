"""
Noise Injector for adding realistic audio artifacts.
Adds white noise, background sounds, and room impulse responses.
"""

import numpy as np
import logging
from pathlib import Path
from typing import Optional
from scipy import signal as scipy_signal

logger = logging.getLogger(__name__)


class NoiseInjector:
    """
    Injects noise into audio for testing robustness.
    """

    def __init__(self, sample_rate: int = 16000):
        """
        Initialize noise injector.

        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
        logger.info(f"✅ NoiseInjector initialized (sample_rate={sample_rate})")

    def add_white_noise(self, audio: np.ndarray, snr_db: float = 20.0) -> np.ndarray:
        """
        Add white noise to audio.

        Args:
            audio: Input audio (int16 numpy array)
            snr_db: Signal-to-Noise Ratio in dB (higher = cleaner)
                    - 20-30 dB: Clean audio
                    - 10-20 dB: Noticeable noise
                    - 0-10 dB: Very noisy
                    - < 0 dB: Noise dominates

        Returns:
            Audio with noise added (int16)
        """
        # Convert to float for processing
        audio_float = audio.astype(np.float64)

        # Calculate signal power
        signal_power = np.mean(audio_float ** 2)

        # Calculate required noise power
        # SNR(dB) = 10 * log10(P_signal / P_noise)
        # P_noise = P_signal / 10^(SNR/10)
        noise_power = signal_power / (10 ** (snr_db / 10.0))

        # Generate white noise
        noise = np.random.normal(0, np.sqrt(noise_power), audio.shape)

        # Add noise to signal
        noisy_audio = audio_float + noise

        # Clip to prevent overflow
        max_val = np.iinfo(np.int16).max
        noisy_audio = np.clip(noisy_audio, -max_val, max_val)

        # Convert back to int16
        return noisy_audio.astype(np.int16)

    def add_background(self, audio: np.ndarray, background_path: str, snr_db: float = 10.0) -> np.ndarray:
        """
        Add background sound (e.g., room ambience, music).

        Args:
            audio: Input audio (int16)
            background_path: Path to background audio file
            snr_db: Signal-to-Noise Ratio (signal vs background)

        Returns:
            Audio with background added
        """
        try:
            import soundfile as sf

            # Load background audio
            bg_audio, bg_sr = sf.read(background_path)

            # Convert to mono if stereo
            if len(bg_audio.shape) > 1:
                bg_audio = bg_audio[:, 0]

            # Resample if necessary
            if bg_sr != self.sample_rate:
                from scipy import signal
                num_samples = int(len(bg_audio) * self.sample_rate / bg_sr)
                bg_audio = signal.resample(bg_audio, num_samples)

            # Convert to int16 if float
            if bg_audio.dtype == np.float32 or bg_audio.dtype == np.float64:
                bg_audio = (bg_audio * np.iinfo(np.int16).max).astype(np.int16)

            # Loop or crop background to match audio length
            bg_len = len(bg_audio)
            audio_len = len(audio)

            if bg_len < audio_len:
                # Loop background
                repeats = (audio_len // bg_len) + 1
                bg_audio = np.tile(bg_audio, repeats)[:audio_len]
            else:
                # Crop background
                bg_audio = bg_audio[:audio_len]

            # Mix with specified SNR
            # Scale background to achieve desired SNR
            audio_float = audio.astype(np.float64)
            bg_float = bg_audio.astype(np.float64)

            signal_power = np.mean(audio_float ** 2)
            bg_power = np.mean(bg_float ** 2)

            # Calculate scaling factor
            # SNR = 10 * log10(P_signal / (P_bg * scale^2))
            # scale = sqrt(P_signal / (P_bg * 10^(SNR/10)))
            scale = np.sqrt(signal_power / (bg_power * (10 ** (snr_db / 10.0))))

            # Mix
            mixed = audio_float + (bg_float * scale)

            # Clip and convert
            max_val = np.iinfo(np.int16).max
            mixed = np.clip(mixed, -max_val, max_val)

            return mixed.astype(np.int16)

        except Exception as e:
            logger.error(f"Failed to add background: {e}")
            return audio

    def add_room_impulse(self, audio: np.ndarray, room_size: str = "medium") -> np.ndarray:
        """
        Simulate room reverberation using impulse response.

        Args:
            audio: Input audio
            room_size: "small", "medium", or "large"

        Returns:
            Audio with reverb
        """
        # Simple reverb using delay and attenuation
        audio_float = audio.astype(np.float64)

        # Room characteristics
        room_configs = {
            "small": {"delay_ms": 50, "decay": 0.3},
            "medium": {"delay_ms": 100, "decay": 0.5},
            "large": {"delay_ms": 200, "decay": 0.7},
        }

        config = room_configs.get(room_size, room_configs["medium"])

        # Calculate delay samples
        delay_samples = int((config["delay_ms"] / 1000.0) * self.sample_rate)

        # Create delayed and attenuated version
        delayed = np.zeros_like(audio_float)
        delayed[delay_samples:] = audio_float[:-delay_samples] * config["decay"]

        # Mix
        reverb = audio_float + delayed

        # Normalize to prevent clipping
        max_val = np.abs(reverb).max()
        if max_val > 0:
            reverb = reverb / max_val * 0.9

        return (reverb * np.iinfo(np.int16).max).astype(np.int16)

    def add_clicks(self, audio: np.ndarray, num_clicks: int = 3, amplitude: float = 0.3) -> np.ndarray:
        """
        Add random clicks/pops to audio (simulates bad connection).

        Args:
            audio: Input audio
            num_clicks: Number of clicks to add
            amplitude: Click amplitude (0.0 to 1.0)

        Returns:
            Audio with clicks
        """
        result = audio.copy().astype(np.float64)

        for _ in range(num_clicks):
            # Random position
            pos = np.random.randint(0, len(audio))

            # Random duration (1-10 samples)
            duration = np.random.randint(1, 11)

            # Add click
            click = np.random.randn(duration) * amplitude * np.iinfo(np.int16).max

            end_pos = min(pos + duration, len(audio))
            actual_duration = end_pos - pos

            result[pos:end_pos] += click[:actual_duration]

        # Clip
        max_val = np.iinfo(np.int16).max
        result = np.clip(result, -max_val, max_val)

        return result.astype(np.int16)

    def add_low_pass_filter(self, audio: np.ndarray, cutoff_hz: int = 3000) -> np.ndarray:
        """
        Apply low-pass filter (simulates phone/low-quality mic).

        Args:
            audio: Input audio
            cutoff_hz: Cutoff frequency in Hz

        Returns:
            Filtered audio
        """
        # Design Butterworth low-pass filter
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff_hz / nyquist

        b, a = scipy_signal.butter(4, normalized_cutoff, btype='low')

        # Apply filter
        filtered = scipy_signal.filtfilt(b, a, audio.astype(np.float64))

        # Normalize
        max_val = np.abs(filtered).max()
        if max_val > 0:
            filtered = filtered / max_val * 0.9

        return (filtered * np.iinfo(np.int16).max).astype(np.int16)

    def add_high_pass_filter(self, audio: np.ndarray, cutoff_hz: int = 300) -> np.ndarray:
        """
        Apply high-pass filter (removes low-frequency noise).
        """
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff_hz / nyquist

        b, a = scipy_signal.butter(4, normalized_cutoff, btype='high')

        filtered = scipy_signal.filtfilt(b, a, audio.astype(np.float64))

        max_val = np.abs(filtered).max()
        if max_val > 0:
            filtered = filtered / max_val * 0.9

        return (filtered * np.iinfo(np.int16).max).astype(np.int16)

    def apply_distortion(self, audio: np.ndarray, amount: float = 0.3) -> np.ndarray:
        """
        Apply soft clipping distortion.

        Args:
            audio: Input audio
            amount: Distortion amount (0.0 to 1.0)

        Returns:
            Distorted audio
        """
        audio_float = audio.astype(np.float64) / np.iinfo(np.int16).max

        # Soft clipping
        distorted = np.tanh(audio_float * (1 + amount * 10))

        # Denormalize
        result = distorted * np.iinfo(np.int16).max

        return result.astype(np.int16)

    def simulate_phone_call(self, audio: np.ndarray) -> np.ndarray:
        """
        Simulate phone call quality audio.
        Band-limited (300Hz-3.4kHz) + compression.
        """
        # Band-pass filter
        filtered = self.add_low_pass_filter(audio, cutoff_hz=3400)
        filtered = self.add_high_pass_filter(filtered, cutoff_hz=300)

        # Add slight compression
        return self.apply_distortion(filtered, amount=0.2)

    def create_test_suite(self, clean_audio: np.ndarray, output_dir: str) -> dict:
        """
        Create a test suite with various noise conditions.

        Args:
            clean_audio: Clean input audio
            output_dir: Directory to save test files

        Returns:
            Dict with paths to all generated files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        import soundfile as sf

        results = {}

        # Clean audio
        clean_path = output_dir / "00_clean.wav"
        sf.write(str(clean_path), clean_audio, self.sample_rate)
        results["clean"] = str(clean_path)

        # Various SNR levels
        for snr in [30, 20, 10, 5, 0]:
            noisy = self.add_white_noise(clean_audio, snr)
            path = output_dir / f"01_noise_{snr}db.wav"
            sf.write(str(path), noisy, self.sample_rate)
            results[f"noise_{snr}db"] = str(path)

        # Room sizes
        for size in ["small", "medium", "large"]:
            reverb = self.add_room_impulse(clean_audio, size)
            path = output_dir / f"02_reverb_{size}.wav"
            sf.write(str(path), reverb, self.sample_rate)
            results[f"reverb_{size}"] = str(path)

        # Phone call
        phone = self.simulate_phone_call(clean_audio)
        path = output_dir / "03_phone.wav"
        sf.write(str(path), phone, self.sample_rate)
        results["phone"] = str(path)

        # Clicks
        clicks = self.add_clicks(clean_audio, num_clicks=5)
        path = output_dir / "04_clicks.wav"
        sf.write(str(path), clicks, self.sample_rate)
        results["clicks"] = str(path)

        logger.info(f"✅ Created test suite with {len(results)} variations")
        return results


if __name__ == "__main__":
    # Test noise injection
    logging.basicConfig(level=logging.INFO)

    print("Testing NoiseInjector...\n")

    # Create test audio (1kHz tone)
    injector = NoiseInjector()
    from .audio_generator import AudioGenerator

    generator = AudioGenerator()
    tone = generator.generate_tone(1000, 2.0)

    # Test 1: White noise
    print("1. Adding white noise...")
    noisy = injector.add_white_noise(tone, snr_db=10)
    print(f"✅ Added noise (SNR=10dB), shape={noisy.shape}\n")

    # Test 2: Room impulse
    print("2. Adding room reverb...")
    reverb = injector.add_room_impulse(tone, room_size="medium")
    print(f"✅ Added reverb, shape={reverb.shape}\n")

    # Test 3: Clicks
    print("3. Adding clicks...")
    clicks = injector.add_clicks(tone, num_clicks=5)
    print(f"✅ Added clicks, shape={clicks.shape}\n")

    # Test 4: Phone simulation
    print("4. Simulating phone call...")
    phone = injector.simulate_phone_call(tone)
    print(f"✅ Phone simulation, shape={phone.shape}\n")

    # Test 5: Create test suite
    print("5. Creating test suite...")
    suite = injector.create_test_suite(tone, "test_noise_suite")
    print(f"✅ Created {len(suite)} test variations\n")

    for name, path in suite.items():
        print(f"  - {name}: {path}")

    print("\n✅ All tests passed!")
