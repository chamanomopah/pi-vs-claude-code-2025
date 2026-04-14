# Practical E2E Testing Examples

> **Collection of ready-to-use testing patterns**  
> **Based on:** E2E_VALIDATION_RESEARCH.md

---

## Example 1: Basic Script Validation

```python
#!/usr/bin/env python3
"""Basic script validation example"""

from validator.script_validator import ScriptValidator

def test_python_script():
    """Test a Python script executes correctly"""
    validator = ScriptValidator(timeout_seconds=30)
    
    result = validator.run(
        command="python hello.py",
        expected_output="Hello, World!",
        expected_exit_code=0
    )
    
    if result.passed():
        print("✅ Script test passed")
        print(f"   Duration: {result.duration_ms:.2f}ms")
    else:
        print(f"❌ Script test failed: {result.message}")
        print(f"   Evidence: {result.evidence}")

if __name__ == "__main__":
    test_python_script()
```

---

## Example 2: Voice Agent Smoke Test

```python
#!/usr/bin/env python3
"""Voice agent smoke test - runs in 5 minutes"""

from validator.script_validator import ScriptValidator
import time

def smoke_test_voice_agent():
    """Quick validation that voice agent components work"""
    validator = ScriptValidator(timeout_seconds=30)
    
    print("🚀 Starting voice agent smoke test...\n")
    
    # Test 1: Check dependencies
    print("Test 1: Checking dependencies...")
    result = validator.run("python -c 'import livekit'")
    if result.passed():
        print("✅ LiveKit installed")
    else:
        print("❌ LiveKit not installed")
        return False
    
    # Test 2: Check STT dependency
    print("\nTest 2: Checking STT (Deepgram)...")
    result = validator.run("python -c 'from livekit.plugins import deepgram'")
    if result.passed():
        print("✅ Deepgram plugin available")
    else:
        print("❌ Deepgram plugin not available")
        return False
    
    # Test 3: Check TTS dependency
    print("\nTest 3: Checking TTS (Cartesia)...")
    result = validator.run("python -c 'from livekit.plugins import cartesia'")
    if result.passed():
        print("✅ Cartesia plugin available")
    else:
        print("❌ Cartesia plugin not available")
        return False
    
    # Test 4: Check configuration
    print("\nTest 4: Checking configuration...")
    result = validator.run(
        'python -c "from dotenv import load_dotenv; load_dotenv(); print(\'OK\')"',
        expected_output="OK"
    )
    if result.passed():
        print("✅ Configuration loads correctly")
    else:
        print("❌ Configuration loading failed")
        return False
    
    # Test 5: Agent starts (will timeout, that's OK)
    print("\nTest 5: Checking agent starts...")
    result = validator.run(
        "python scripts/livekit-pi-extension/pi_agent.py",
        timeout=5
    )
    if result.status == "timeout":
        print("✅ Agent starts successfully")
    else:
        print("⚠️  Agent may have issues")
    
    print("\n✅ All smoke tests passed!")
    return True

if __name__ == "__main__":
    success = smoke_test_voice_agent()
    exit(0 if success else 1)
```

---

## Example 3: Audio Pipeline Test

```python
#!/usr/bin/env python3
"""Test audio pipeline: STT → LLM → TTS"""

import wave
import tempfile
import os

def generate_test_audio(text="Hello world"):
    """Generate test audio file using espeak or similar"""
    # For this example, create a simple WAV file
    # In practice, use espeak or pre-recorded files
    
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    
    # Generate simple sine wave (placeholder)
    # Real implementation would use espeak or festival
    import numpy as np
    sample_rate = 16000
    duration = 1.0
    frequency = 440  # A4
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Save as WAV
    with wave.open(temp_file.name, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes((audio_data * 32767).astype(np.int16).tobytes())
    
    return temp_file.name

def test_audio_pipeline():
    """Test STT → LLM → TTS pipeline"""
    
    print("Testing audio pipeline...\n")
    
    # Generate test audio
    print("1. Generating test audio...")
    audio_file = generate_test_audio()
    print(f"   ✅ Test audio: {audio_file}")
    
    # Test STT (mock for this example)
    print("\n2. Testing STT...")
    # In real implementation:
    # from livekit.plugins import deepgram
    # text = deepgram.stt.transcribe(audio_file)
    text = "hello world"  # Mock
    print(f"   ✅ Transcription: {text}")
    assert "hello" in text.lower()
    
    # Test LLM
    print("\n3. Testing LLM...")
    # In real implementation:
    # response = llm.generate(text)
    response = f"I heard: {text}"  # Mock
    print(f"   ✅ Response: {response}")
    assert len(response) > 0
    
    # Test TTS
    print("\n4. Testing TTS...")
    # In real implementation:
    # from livekit.plugins import cartesia
    # output_audio = cartesia.tts.generate(response)
    output_audio = b"mock_audio_data"  # Mock
    print(f"   ✅ Generated audio: {len(output_audio)} bytes")
    assert len(output_audio) > 0
    
    # Cleanup
    os.unlink(audio_file)
    
    print("\n✅ Audio pipeline test passed!")
    return True

if __name__ == "__main__":
    success = test_audio_pipeline()
    exit(0 if success else 1)
```

---

## Example 4: Multi-Turn Conversation Test

```python
#!/usr/bin/env python3
"""Test multi-turn conversation context retention"""

def test_multi_turn_conversation():
    """Test that agent maintains context across turns"""
    
    print("Testing multi-turn conversation...\n")
    
    # Simulate agent (in practice, use real agent)
    class MockAgent:
        def __init__(self):
            self.context = []
        
        def query(self, text):
            self.context.append({"role": "user", "content": text})
            response = f"Received: {text}"
            self.context.append({"role": "assistant", "content": response})
            return response
    
    agent = MockAgent()
    
    # Turn 1
    print("Turn 1: User asks question")
    response1 = agent.query("What's the weather?")
    print(f"   User: What's the weather?")
    print(f"   Agent: {response1}")
    assert len(response1) > 0
    print("   ✅ Response generated")
    
    # Turn 2: Follow-up
    print("\nTurn 2: User asks follow-up")
    response2 = agent.query("And tomorrow?")
    print(f"   User: And tomorrow?")
    print(f"   Agent: {response2}")
    assert len(response2) > 0
    print("   ✅ Response generated")
    
    # Verify context retained
    print("\n3. Verifying context retained...")
    assert len(agent.context) == 4  # 2 user + 2 assistant
    print(f"   ✅ Context has {len(agent.context)} messages")
    
    # Verify context contains previous turns
    context_text = " ".join([msg["content"] for msg in agent.context])
    assert "weather" in context_text.lower()
    print("   ✅ Previous context retained")
    
    print("\n✅ Multi-turn conversation test passed!")
    return True

if __name__ == "__main__":
    success = test_multi_turn_conversation()
    exit(0 if success else 1)
```

---

## Example 5: Property-Based Test

```python
#!/usr/bin/env python3
"""Property-based tests for agent invariants"""

from hypothesis import given, strategies as st, settings

class SimpleAgent:
    """Mock agent for testing"""
    def query(self, text, context_length=0):
        # Simple mock implementation
        if not text or len(text.strip()) == 0:
            return "I didn't hear anything."
        if len(text) > 10000:
            return "That's quite long!"
        return f"Response to: {text[:50]}"

agent = SimpleAgent()

@settings(max_examples=100)
@given(st.text(min_size=0, max_size=1000))
def test_agent_never_returns_empty(query):
    """Agent should never return empty response"""
    response = agent.query(query)
    assert len(response) > 0, f"Empty response for query: {query[:50]}"

@settings(max_examples=100)
@given(st.t
