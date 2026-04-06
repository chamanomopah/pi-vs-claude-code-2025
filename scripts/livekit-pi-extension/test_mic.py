"""
Quick Microphone Test
=====================
Test if microphone capture works on your system.
"""

import pyaudio
import numpy as np
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 320
THRESHOLD = 500

print("🎤 Microphone Test")
print("=" * 40)
print("\nSpeak into your microphone...")
print("I'll show the volume level.")
print("Press Ctrl+C to stop.\n")

try:
    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("✓ Microphone opened - Listening...\n")

    import time
    start_time = time.time()

    try:
        while True:
            # Read audio
            data = stream.read(CHUNK, exception_on_overflow=False)

            # Calculate volume
            samples = np.frombuffer(data, dtype=np.int16)
            rms = np.sqrt(np.mean(np.square(samples.astype(float))))

            # Display
            elapsed = time.time() - start_time
            bar_length = int(rms / 100)
            bar = "█" * min(bar_length, 50)
            status = "🗣️  SPEAKING" if rms > THRESHOLD else "..."
            print(f"\r[{elapsed:5.1f}s] {status} {rms:6.0f} {bar}", end="", flush=True)

    except KeyboardInterrupt:
        print("\n\n✓ Test completed")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure your microphone is connected")
    print("2. Check microphone permissions")
    print("3. Try a different USB port")
    print("4. Check system audio settings")
