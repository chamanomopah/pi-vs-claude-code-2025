"""
Simple Hands-Free Voice Client for Pi
======================================
A minimal voice client that captures microphone, transcribes, sends to Pi,
and speaks the response.

This version uses the simplest possible approach:
- PyAudio for microphone capture
- Deepgram for STT (via HTTP API - simpler than WebSocket)
- Pi's existing LLM for responses
- Cartesia for TTS (via HTTP API)
- PyAudio for speaker output

Usage:
    python simple_handsfree.py
"""

import asyncio
import sys
import os
import json
import requests
import pyaudio
import numpy as np
import wave
import tempfile
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

class SimpleHandsFreeVoice:
    """Simple hands-free voice interface."""

    def __init__(self):
        # Audio settings
        self.sample_rate = 16000  # Deepgram prefers 16kHz
        self.channels = 1
        self.chunk_size = 320  # 20ms at 16kHz
        self.silence_threshold = 500
        self.silence_duration = 1.0  # seconds
        self.min_speech_duration = 0.5  # seconds

        # PyAudio
        self.pyaudio = pyaudio.PyAudio()
        self.mic_stream = None
        self.speaker_stream = None

        # API keys
        self.deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        self.cartesia_key = os.getenv("CARTESIA_API_KEY")

        # State
        self.is_listening = False
        self.audio_buffer = []
        self.silence_chunks = 0
        self.speech_chunks = 0

        # Pi communication files
        self.comm_dir = os.path.dirname(os.path.abspath(__file__))
        self.pi_comm_file = os.path.join(self.comm_dir, ".pi_comm.txt")
        self.pi_response_file = os.path.join(self.comm_dir, ".pi_response.txt")

        # Clear old communication files
        if os.path.exists(self.pi_comm_file):
            os.remove(self.pi_comm_file)
        if os.path.exists(self.pi_response_file):
            os.remove(self.pi_response_file)

    def setup_microphone(self) -> bool:
        """Set up microphone."""
        try:
            print("🎤 Setting up microphone...")

            self.mic_stream = self.pyaudio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )

            print("✓ Microphone ready")
            return True

        except Exception as e:
            print(f"✗ Microphone error: {e}")
            return False

    def setup_speaker(self) -> bool:
        """Set up speaker."""
        try:
            print("🔊 Setting up speaker...")

            self.speaker_stream = self.pyaudio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,  # Cartesia uses 24kHz
                output=True,
                frames_per_buffer=self.chunk_size
            )

            print("✓ Speaker ready")
            return True

        except Exception as e:
            print(f"✗ Speaker error: {e}")
            return False

    def detect_speech(self, audio_data: bytes) -> bool:
        """Detect if audio contains speech."""
        # Convert to numpy array
        samples = np.frombuffer(audio_data, dtype=np.int16)

        # Calculate RMS (volume)
        rms = np.sqrt(np.mean(np.square(samples.astype(float))))

        return rms > self.silence_threshold

    async def listen_for_speech(self) -> Optional[str]:
        """Listen for speech and return transcribed text."""
        print("\n🎤 Listening...")

        self.audio_buffer = []
        self.silence_chunks = 0
        self.speech_chunks = 0
        is_speaking = False

        try:
            while True:
                # Read audio chunk
                audio_data = self.mic_stream.read(self.chunk_size, exception_on_overflow=False)

                # Detect speech
                has_speech = self.detect_speech(audio_data)

                if has_speech:
                    self.speech_chunks += 1
                    self.silence_chunks = 0

                    if not is_speaking and self.speech_chunks > int(self.min_speech_duration * 50):  # 50 chunks per second
                        is_speaking = True
                        print("🗣️  Speech detected...")

                    self.audio_buffer.append(audio_data)

                elif is_speaking:
                    self.silence_chunks += 1

                    # Check for end of speech
                    silence_seconds = self.silence_chunks / 50.0  # 50 chunks per second
                    if silence_seconds >= self.silence_duration:
                        print("✓ Speech ended")
                        break

                # Safety timeout
                if len(self.audio_buffer) > 500:  # 10 seconds max
                    print("⏱️  Timeout reached")
                    break

        except Exception as e:
            print(f"✗ Listening error: {e}")
            return None

        # Check if we got enough speech
        if self.speech_chunks < 25:  # Less than 0.5 seconds
            print("⚠️  Too short, ignoring")
            return None

        # Transcribe
        return await self.transcribe()

    async def transcribe(self) -> Optional[str]:
        """Transcribe audio buffer using Deepgram."""
        try:
            print("📝 Transcribing...")

            # Save audio to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_path = tmp_file.name

                # Write WAV file
                with wave.open(tmp_path, 'wb') as wav_file:
                    wav_file.setnchannels(self.channels)
                    wav_file.setsampwidth(self.pyaudio.get_sample_size(pyaudio.paInt16))
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(b''.join(self.audio_buffer))

            # Send to Deepgram
            with open(tmp_path, 'rb') as audio_file:
                url = "https://api.deepgram.com/v1/listen"
                headers = {
                    "Authorization": f"Token {self.deepgram_key}",
                    "Content-Type": "audio/wav"
                }

                response = requests.post(url, headers=headers, data=audio_file)

                if response.status_code == 200:
                    result = response.json()
                    transcript = result.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")

                    if transcript:
                        print(f"✓ Transcribed: \"{transcript}\"")
                        return transcript
                    else:
                        print("⚠️  No transcription")
                        return None
                else:
                    print(f"✗ Deepgram error: {response.status_code}")
                    return None

        except Exception as e:
            print(f"✗ Transcription error: {e}")
            return None

        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass

    async def speak(self, text: str):
        """Synthesize speech and play it."""
        try:
            print(f"🔊 Speaking: \"{text[:100]}...\"")

            # Call Cartesia TTS API
            url = "https://api.cartesia.ai/tts/bytes"

            headers = {
                "X-API-Key": self.cartesia_key,
                "Content-Type": "application/json"
            }

            data = {
                "model": "sonic-3",
                "text": text,
                "voice": {
                    "id": "79a125e8-cd45-4c93-9ae2-3f2e0f6a0c9a"
                },
                "output_format": {
                    "container": "raw",
                    "sample_rate": 24000,
                    "encoding": "pcm_int16"
                }
            }

            response = requests.post(url, headers=headers, json=data, stream=True)

            if response.status_code == 200:
                print("✓ Playing audio...")

                # Stream audio to speaker
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        self.speaker_stream.write(chunk)

                print("✓ Finished speaking")
            else:
                print(f"✗ TTS error: {response.status_code}")
                print(f"  Response: {response.text}")

        except Exception as e:
            print(f"✗ Speech error: {e}")

    def extract_last_sentence(self, text: str) -> str:
        """Extract last sentence from text."""
        # Remove thinking tags
        cleaned = text.replace("<thinking>", "").replace("</thinking>", "").strip()

        # Split on sentence boundaries
        sentences = []
        current = []

        for char in cleaned:
            current.append(char)
            if char in ['.', '!', '?']:
                sentences.append(''.join(current).strip())
                current = []

        if current:
            sentences.append(''.join(current).strip())

        # Get last non-empty sentence
        for sentence in reversed(sentences):
            if len(sentence) > 0:
                return sentence[:100]

        return cleaned[:100]

    async def send_to_pi(self, text: str) -> str:
        """Send transcription to Pi via file and wait for response."""
        try:
            # Write transcript to file
            with open(self.pi_comm_file, 'w') as f:
                f.write(text)

            print("✓ Sent to Pi, waiting for response...")

            # Wait for response (with timeout)
            timeout = 30  # seconds
            start_time = asyncio.get_event_loop().time()

            while True:
                # Check timeout
                if asyncio.get_event_loop().time() - start_time > timeout:
                    print("⏱️  Timeout waiting for Pi response")
                    return "I'm sorry, I didn't receive a response in time."

                # Check if response file exists and has content
                if os.path.exists(self.pi_response_file):
                    try:
                        with open(self.pi_response_file, 'r') as f:
                            response = f.read().strip()

                        if response:
                            # Clear response file
                            os.remove(self.pi_response_file)
                            return response
                    except:
                        pass

                # Wait a bit before checking again
                await asyncio.sleep(0.1)

        except Exception as e:
            print(f"✗ Pi communication error: {e}")
            return "I had trouble communicating with the assistant."

    async def start(self):
        """Start the voice loop."""
        print("\n" + "="*60)
        print("🎤 HANDS-FREE VOICE MODE ACTIVE")
        print("="*60)
        print("\nSpeak naturally. I'll listen, transcribe, and respond.")
        print("Press Ctrl+C to stop.\n")

        self.is_listening = True

        try:
            while self.is_listening:
                # Listen for speech
                transcript = await self.listen_for_speech()

                if transcript:
                    # Send to Pi
                    print(f"\n📤 Sending to Pi...")
                    response = await self.send_to_pi(transcript)

                    if response:
                        # Extract last sentence for display
                        last_sentence = self.extract_last_sentence(response)
                        print(f"\n🤖 Assistant: {last_sentence}")

                        # Speak the full response
                        await self.speak(response)

                print("\n" + "-"*60)
                print("Ready for next input...\n")

        except KeyboardInterrupt:
            print("\n\n🛑 Stopping...")
        finally:
            self.shutdown()

    def shutdown(self):
        """Clean up resources."""
        print("Shutting down...")

        self.is_listening = False

        if self.mic_stream:
            self.mic_stream.stop_stream()
            self.mic_stream.close()

        if self.speaker_stream:
            self.speaker_stream.stop_stream()
            self.speaker_stream.close()

        self.pyaudio.terminate()

        print("Shutdown complete")


# For standalone testing
async def test_mode():
    """Test mode without Pi integration."""
    voice = SimpleHandsFreeVoice()

    if not voice.setup_microphone():
        return

    if not voice.setup_speaker():
        return

    try:
        await voice.start()
    except KeyboardInterrupt:
        voice.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(test_mode())
    except KeyboardInterrupt:
        print("\nExiting...")
