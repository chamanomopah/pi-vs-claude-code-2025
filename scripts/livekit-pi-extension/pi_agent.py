"""
LiveKit Voice Agent for Pi Integration
========================================
A voice agent that integrates LiveKit with Pi's LLM models.

This agent handles:
- Speech-to-Text (STT) via Deepgram
- Text-to-Speech (TTS) via Cartesia
- Voice Activity Detection (VAD)
- Communication with Pi extension

Usage:
    python pi_agent.py dev --room <room-name>
    python pi_agent.py console  # For local testing
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext
from livekit.agents.llm import function_tool
from livekit.plugins import google, deepgram, cartesia, silero
import sys
import os
import asyncio

# Load environment variables
load_dotenv(".env")

class PiVoiceAssistant(Agent):
    """Voice assistant that integrates with Pi's LLM models."""

    def __init__(self):
        super().__init__(
            instructions="""You are a helpful voice AI assistant integrated with Pi.

            Your role is to:
            - Listen to user's voice input
            - Transcribe it accurately
            - Send it to Pi for processing
            - Speak Pi's response naturally

            Keep your responses concise and natural, as if having a conversation.
            Avoid technical jargon unless necessary.
            """
        )

    @function_tool
    async def get_status(self, context: RunContext) -> str:
        """Get current agent status."""
        return "Pi Voice Assistant is ready and listening."

    @function_tool
    async def echo_transcript(self, context: RunContext, text: str) -> str:
        """Echo a transcript back to the user (for testing).

        Args:
            text: The text to echo back
        """
        return f"You said: {text}"


async def entrypoint(ctx: agents.JobContext):
    """Entry point for the voice agent."""

    # Get configuration from environment
    livekit_url = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY", "")
    cartesia_api_key = os.getenv("CARTESIA_API_KEY", "")
    google_api_key = os.getenv("GOOGLE_API_KEY", "")

    # Validate required keys
    if not deepgram_api_key and not google_api_key:
        print("ERROR: DEEPGRAM_API_KEY or GOOGLE_API_KEY is required")
        return

    if not cartesia_api_key:
        print("WARNING: CARTESIA_API_KEY not found, TTS may not work")

    # Configure STT (Speech-to-Text)
    # Prefer Deepgram, fallback to Google
    if deepgram_api_key:
        stt = deepgram.STT(model="nova-2")
        print("[Agent] Using Deepgram STT (nova-2)")
    else:
        stt = google.STT(model="chirp_2")
        print("[Agent] Using Google STT (chirp_2)")

    # Configure LLM (for agent-level processing, not Pi integration)
    # This is minimal - actual intelligence comes from Pi
    llm = google.LLM(model="gemini-2.5-flash")

    # Configure TTS (Text-to-Speech)
    # Prefer Cartesia for voice quality
    if cartesia_api_key:
        # Cartesia Sonic-3 model with a nice voice
        tts = cartesia.TTS(
            model="sonic-3",
            voice=os.getenv("CARTESIA_VOICE", "79a125e8-cd45-4c93-9ae2-3f2e0f6a0c9a")
        )
        print("[Agent] Using Cartesia TTS (sonic-3)")
    else:
        tts = google.TTS(voice="en-US-Journey-D")
        print("[Agent] Using Google TTS (Journey-D)")

    # Configure VAD (Voice Activity Detection)
    vad = silero.VAD.load()
    print("[Agent] VAD loaded (Silero)")

    # Room name will be provided by LiveKit Server via JobContext
    print(f"[Agent] LiveKit URL: {livekit_url}")
    print("[Agent] Starting worker, waiting for jobs...")

    # Create the voice pipeline
    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=vad,
    )

    # Start the session
    try:
        await session.start(
            room=ctx.room,
            agent=PiVoiceAssistant()
        )

        # Room name is available via ctx.room.name
        print(f"[Agent] Connected to room: {ctx.room.name}")
        print("[Agent] Listening for voice input...")

        # Generate initial greeting
        await session.generate_reply(
            instructions="Greet the user warmly and briefly, letting them know you're ready to help."
        )

        print("[Agent] Session active. Press Ctrl+C to exit.")

    except Exception as e:
        print(f"[Agent] Error: {e}")
        return


if __name__ == "__main__":
    # Run the agent
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
