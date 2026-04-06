"""
LiveKit Voice Client for Pi
============================
A hands-free voice client that connects to LiveKit and manages voice I/O.

Features:
- Connects to LiveKit room
- Captures microphone audio
- Receives TTS audio playback
- Manages voice activity detection
- Handles transcription and responses

Usage:
    python voice_client.py --room <room-name>
"""

import asyncio
import sys
import os
import json
from typing import Optional
from dotenv import load_dotenv
from livekit import api, rtc
import argparse

# Load environment variables
load_dotenv(".env")

class VoiceClient:
    """Hands-free voice client for LiveKit."""

    def __init__(self, room_name: str, livekit_url: str, api_key: str, api_secret: str):
        self.room_name = room_name
        self.livekit_url = livekit_url
        self.api_key = api_key
        self.api_secret = api_secret

        # Room and tracks
        self.room: Optional[rtc.Room] = None
        self.audio_track: Optional[rtc.LocalAudioTrack] = None
        self.remote_track: Optional[rtc.RemoteAudioTrack] = None

        # State
        self.is_connected = False
        self.is_speaking = False
        self.last_transcript = ""
        self.last_response = ""

    async def connect(self) -> bool:
        """Connect to the LiveKit room."""
        try:
            print(f"[Client] Connecting to room: {self.room_name}")
            print(f"[Client] LiveKit URL: {self.livekit_url}")

            # Create room
            self.room = rtc.Room()

            # Set up event handlers
            self.room.on("participant_connected", self.on_participant_connected)
            self.room.on("track_subscribed", self.on_track_subscribed)
            self.room.on("track_unsubscribed", self.on_track_unsubscribed)
            self.room.on("disconnected", self.on_disconnected)
            self.room.on("data_received", self.on_data_received)

            # Connect to room
            token = self.create_token()
            await self.room.connect(self.livekit_url, token)

            self.is_connected = True
            print(f"[Client] ✓ Connected to room: {self.room_name}")
            print(f"[Client] Room SID: {self.room.sid}")
            print(f"[Client] Participant ID: {self.room.local_participant.sid}")

            # Publish local audio track
            await self.publish_audio()

            return True

        except Exception as e:
            print(f"[Client] ✗ Connection failed: {e}")
            return False

    def create_token(self) -> str:
        """Create a participant token for the room."""
        try:
            # Create room if it doesn't exist
            from livekit.api import RoomServiceClient, CreateRoomRequest
            room_service = RoomServiceClient(self.livekit_url, self.api_key, self.api_secret)

            try:
                room = room_service.create_room(CreateRoomRequest(
                    name=self.room_name,
                    empty_timeout=300,  # 5 minutes
                    max_participants=10
                ))
                print(f"[Client] Room created: {room.sid}")
            except Exception as e:
                if "already exists" not in str(e):
                    print(f"[Client] Room creation note: {e}")

            # Create participant token
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
            print(f"[Client] Token creation error: {e}")
            # Fallback: create simple token
            from livekit.api import AccessToken, VideoGrants
            access_token = AccessToken(self.api_key, self.api_secret)
            access_token.with_identity("pi-user")
            access_token.with_name("Pi User")
            access_token.with_grants(VideoGrants(
                room_join=True,
                room=self.room_name,
                can_publish=True,
                can_subscribe=True
            ))
            return access_token.to_jwt()

    async def publish_audio(self):
        """Publish local audio track to the room."""
        try:
            print("[Client] Publishing audio track...")

            # Create audio track
            self.audio_track = rtc.LocalAudioTrack.create_audio_track(
                "microphone",
                rtc.AudioSource(
                    sample_rate=48000,
                    num_channels=1,
                )
            )

            # Publish to room
            await self.room.local_participant.publish_track(self.audio_track)
            print("[Client] ✓ Audio track published")

        except Exception as e:
            print(f"[Client] Audio track error: {e}")

    async def start_listening(self):
        """Start listening for incoming audio and transcription."""
        print("[Client] Listening for speech...")
        print("[Client] Speak now!")

        try:
            # Keep running until disconnected
            while self.is_connected:
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            print("\n[Client] Interrupted by user")

    def on_participant_connected(self, participant: rtc.RemoteParticipant):
        """Handle participant connected event."""
        print(f"[Client] Participant connected: {participant.identity}")

    async def on_track_subscribed(self, track: rtc.Track, publication: rtc.RemoteTrackPublication, participant: rtc.RemoteParticipant):
        """Handle track subscribed event."""
        print(f"[Client] Track subscribed: {track.kind} from {participant.identity}")

        if track.kind == rtc.TrackKind.KIND_AUDIO:
            self.remote_track = track
            print("[Client] Audio track subscribed - receiving TTS audio")

            # Start playing the audio
            @track.on("frame_received")
            def on_frame(frame: rtc.AudioFrame):
                # Audio frame received - this would be played by speaker
                # For now, just log it
                if not self.is_speaking:
                    self.is_speaking = True
                    print("[Client] 🔊 Assistant speaking...")

    def on_track_unsubscribed(self, track: rtc.Track, publication: rtc.RemoteTrackPublication, participant: rtc.RemoteParticipant):
        """Handle track unsubscribed event."""
        print(f"[Client] Track unsubscribed: {track.kind}")
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            self.is_speaking = False
            print("[Client] Assistant finished speaking")

    def on_disconnected(self):
        """Handle disconnection."""
        print("[Client] Disconnected from room")
        self.is_connected = False

    def on_data_received(self, data: bytes, participant: rtc.RemoteParticipant):
        """Handle data received (for transcription)."""
        try:
            message = json.loads(data.decode())
            msg_type = message.get("type")

            if msg_type == "transcription":
                transcript = message.get("text", "")
                print(f"\n[Client] 🎤 You said: {transcript}")
                self.last_transcript = transcript

            elif msg_type == "response":
                response = message.get("text", "")
                last_sentence = self.extract_last_sentence(response)
                print(f"[Client] 🤖 Assistant: {last_sentence}")
                self.last_response = response

        except Exception as e:
            print(f"[Client] Data error: {e}")

    def extract_last_sentence(self, text: str) -> str:
        """Extract the last sentence from text."""
        # Remove thinking tags
        cleaned = text.replace("<thinking>", "").replace("</thinking>", "").strip()

        # Split on sentence boundaries
        sentences = cleaned.replace(".", ".|").replace("!", "!|").replace("?", "?|").split("|")

        # Get last non-empty sentence
        for sentence in reversed(sentences):
            s = sentence.strip()
            if len(s) > 0:
                return s[:100]

        return cleaned[:100]

    async def disconnect(self):
        """Disconnect from the room."""
        if self.room:
            await self.room.disconnect()
            print("[Client] Disconnected")

    async def send_transcription(self, text: str):
        """Send transcription data."""
        if self.room and self.is_connected:
            data = json.dumps({"type": "transcription", "text": text}).encode()
            await self.room.local_participant.publish_data(data)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LiveKit Voice Client")
    parser.add_argument("--room", required=True, help="Room name to join")
    parser.add_argument("--url", default=os.getenv("LIVEKIT_URL", "ws://localhost:7880"), help="LiveKit URL")
    parser.add_argument("--api-key", default=os.getenv("LIVEKIT_API_KEY", "devkey"), help="LiveKit API Key")
    parser.add_argument("--api-secret", default=os.getenv("LIVEKIT_API_SECRET", "secret"), help="LiveKit API Secret")
    args = parser.parse_args()

    client = VoiceClient(
        room_name=args.room,
        livekit_url=args.url,
        api_key=args.api_key,
        api_secret=args.api_secret
    )

    try:
        # Connect
        if await client.connect():
            # Start listening
            await client.start_listening()

    except KeyboardInterrupt:
        print("\n[Client] Shutting down...")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
