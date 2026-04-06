"""
Hands-Free Voice Client for Pi
================================
A complete voice client that captures microphone, sends to LiveKit,
and receives TTS audio playback.

Usage:
    python hands_free_client.py --room <room-name>
"""

import asyncio
import sys
import os
import json
import queue
from typing import Optional
from dotenv import load_dotenv
from livekit import api, rtc
from livekit.plugins import deepgram, cartesia, google
import argparse
import pyaudio
import numpy as np

# Load environment variables
load_dotenv(".env")

class HandsFreeVoiceClient:
    """Complete hands-free voice client with microphone capture and speaker playback."""

    def __init__(self, room_name: str, livekit_url: str, api_key: str, api_secret: str):
        self.room_name = room_name
        self.livekit_url = livekit_url
        self.api_key = api_key
        self.api_secret = api_secret

        # Audio settings
        self.sample_rate = 48000
        self.channels = 1
        self.chunk_size = 960  # 20ms at 48kHz

        # PyAudio
        self.pyaudio = pyaudio.PyAudio()
        self.mic_stream: Optional[pyaudio.Stream] = None
        self.speaker_stream: Optional[pyaudio.Stream] = None

        # Audio queue
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.is_playing = False

        # LiveKit
        self.room: Optional[rtc.Room] = None
        self.audio_source: Optional[rtc.AudioSource] = None
        self.audio_track: Optional[rtc.LocalAudioTrack] = None

        # STT and TTS
        self.stt = None
        self.tts = None
        self.vad = None

        # State
        self.is_connected = False
        self.last_transcript = ""
        self.last_response = ""

    async def setup_stt_tts(self):
        """Set up STT and TTS plugins."""
        deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        cartesia_key = os.getenv("CARTESIA_API_KEY")
        google_key = os.getenv("GOOGLE_API_KEY")

        # STT - Deepgram (preferred) or Google
        if deepgram_key:
            self.stt = deepgram.STT(model="nova-2")
            print("[Client] Using Deepgram STT")
        elif google_key:
            self.stt = google.STT(model="chirp_2")
            print("[Client] Using Google STT")
        else:
            print("[Client] WARNING: No STT available")

        # TTS - Cartesia (preferred) or Google
        if cartesia_key:
            self.tts = cartesia.TTS(
                model="sonic-3",
                voice=os.getenv("CARTESIA_VOICE", "79a125e8-cd45-4c93-9ae2-3f2e0f6a0c9a")
            )
            print("[Client] Using Cartesia TTS")
        elif google_key:
            self.tts = google.TTS(voice="en-US-Journey-D")
            print("[Client] Using Google TTS")
        else:
            print("[Client] WARNING: No TTS available")

    def setup_microphone(self):
        """Set up microphone capture."""
        try:
            print("[Client] Setting up microphone...")

            self.mic_stream = self.pyaudio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self.mic_callback
            )

            print("[Client] ✓ Microphone ready")
            return True

        except Exception as e:
            print(f"[Client] ✗ Microphone setup failed: {e}")
            return False

    def setup_speaker(self):
        """Set up speaker playback."""
        try:
            print("[Client] Setting up speaker...")

            self.speaker_stream = self.pyaudio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=24000,  # Cartesia uses 24kHz
                output=True,
                frames_per_buffer=self.chunk_size
            )

            print("[Client] ✓ Speaker ready")
            return True

        except Exception as e:
            print(f"[Client] ✗ Speaker setup failed: {e}")
            return False

    def mic_callback(self, in_data, frame_count, time_info, status):
        """Microphone callback - called when audio is available."""
        if self.is_recording:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(in_data, dtype=np.int16)

            # Put in queue for processing
            try:
                self.audio_queue.put_nowait(audio_data)
            except queue.Full:
                pass  # Drop if full

        return (in_data, pyaudio.paContinue)

    async def connect_to_livekit(self) -> bool:
        """Connect to LiveKit room (optional, for remote processing)."""
        try:
            print(f"[Client] Connecting to LiveKit room: {self.room_name}")

            self.room = rtc.Room()

            # Set up event handlers
            self.room.on("disconnected", self.on_disconnected)
            self.room.on("data_received", self.on_data_received)

            # Connect
            token = self.create_token()
            await self.room.connect(self.livekit_url, token)

            self.is_connected = True
            print(f"[Client] ✓ Connected to LiveKit")

            return True

        except Exception as e:
            print(f"[Client] LiveKit connection failed: {e}")
            print("[Client] Continuing in local mode...")
            return False

    def create_token(self) -> str:
        """Create a token for LiveKit connection."""
        try:
            from livekit.api import AccessToken, VideoGrants

            access_token = AccessToken(self.api_key, self.api_secret)
            access_token.with_identity("pi-user")
            access_token.with_name("Pi User")

            grants = VideoGrants(
                room_join=True,
                room=self.room_name,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True
            )
            access_token.with_grants(grants)

            return access_token.to_jwt()

        except Exception as e:
            print(f"[Client] Token error: {e}")
            return ""

    async def start_voice_loop(self):
        """Main voice processing loop."""
        print("[Client] 🎤 Voice mode active - Speak now!")
        print("[Client] Press Ctrl+C to stop\n")

        self.is_recording = True
        self.mic_stream.start_stream()

        try:
            audio_buffer = []

            while self.is_recording:
                try:
                    # Get audio from queue (with timeout)
                    audio_data = await asyncio.get_event_loop().run_in_executor(
                        None, lambda: self.audio_queue.get(timeout=0.1)
                    )

                    audio_buffer.append(audio_data)

                    # Process when buffer has enough audio (1 second)
                    if len(audio_buffer) >= 50:  # 50 * 20ms = 1 second
                        # Combine audio
                        combined_audio = np.concatenate(audio_buffer)

                        # Send to STT
                        if self.stt:
                            transcript = await self.transcribe_audio(combined_audio)
                            if transcript:
                                print(f"\n[Client] 🎤 You: {transcript}")
                                self.last_transcript = transcript

                                # Send to Pi for processing
                                await self.send_to_pi(transcript)

                        # Clear buffer
                        audio_buffer = []

                except queue.Empty:
                    continue

                except Exception as e:
                    print(f"[Client] Error: {e}")
                    continue

        except KeyboardInterrupt:
            print("\n[Client] Stopping...")

    async def transcribe_audio(self, audio_data: np.ndarray) -> Optional[str]:
        """Transcribe audio using STT."""
        try:
            # This is a simplified version
            # In production, you'd use the STT plugin properly
            return None  # Placeholder

        except Exception as e:
            print(f"[Client] STT error: {e}")
            return None

    async def send_to_pi(self, text: str):
        """Send transcription to Pi for processing."""
        # This would send to Pi extension via some IPC mechanism
        # For now, just print
        print(f"[Client] Sending to Pi: {text}")

    async def synthesize_speech(self, text: str):
        """Synthesize speech using TTS and play it."""
        try:
            print(f"[Client] 🔊 Speaking...")

            # Placeholder for TTS
            # In production, you'd use the TTS plugin and send to speaker

        except Exception as e:
            print(f"[Client] TTS error: {e}")

    def on_data_received(self, data: bytes, participant: rtc.RemoteParticipant):
        """Handle data received from LiveKit."""
        try:
            message = json.loads(data.decode())
            msg_type = message.get("type")

            if msg_type == "response":
                response = message.get("text", "")
                last_sentence = self.extract_last_sentence(response)
                print(f"\n[Client] 🤖 Assistant: {last_sentence}")

                # Synthesize and play
                asyncio.create_task(self.synthesize_speech(response))

        except Exception as e:
            print(f"[Client] Data error: {e}")

    def on_disconnected(self):
        """Handle disconnection."""
        print("[Client] Disconnected from LiveKit")
        self.is_connected = False

    def extract_last_sentence(self, text: str) -> str:
        """Extract last sentence from text."""
        cleaned = text.replace("<thinking>", "").replace("</thinking>", "").strip()
        sentences = cleaned.replace(".", ".|").replace("!", "!|").replace("?", "?|").split("|")

        for sentence in reversed(sentences):
            s = sentence.strip()
            if len(s) > 0:
                return s[:100]

        return cleaned[:100]

    async def shutdown(self):
        """Clean up resources."""
        print("[Client] Shutting down...")

        self.is_recording = False

        if self.mic_stream:
            self.mic_stream.stop_stream()
            self.mic_stream.close()

        if self.speaker_stream:
            self.speaker_stream.stop_stream()
            self.speaker_stream.close()

        self.pyaudio.terminate()

        if self.room:
            await self.room.disconnect()

        print("[Client] Shutdown complete")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Hands-Free Voice Client")
    parser.add_argument("--room", required=True, help="Room name")
    parser.add_argument("--url", default=os.getenv("LIVEKIT_URL", "ws://localhost:7880"), help="LiveKit URL")
    parser.add_argument("--api-key", default=os.getenv("LIVEKIT_API_KEY", "devkey"), help="API Key")
    parser.add_argument("--api-secret", default=os.getenv("LIVEKIT_API_SECRET", "secret"), help="API Secret")
    args = parser.parse_args()

    client = HandsFreeVoiceClient(
        room_name=args.room,
        livekit_url=args.url,
        api_key=args.api_key,
        api_secret=args.api_secret
    )

    try:
        # Setup
        await client.setup_stt_tts()

        if not client.setup_microphone():
            print("[Client] Failed to setup microphone")
            return

        if not client.setup_speaker():
            print("[Client] Failed to setup speaker")
            return

        # Connect to LiveKit (optional)
        await client.connect_to_livekit()

        # Start voice loop
        await client.start_voice_loop()

    except KeyboardInterrupt:
        print("\n[Client] Interrupted")
    finally:
        await client.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Client] Exiting...")
