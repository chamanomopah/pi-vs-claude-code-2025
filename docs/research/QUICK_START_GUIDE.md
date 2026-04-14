# Quick Start Guide: E2E Validation Implementation

> **Companion to:** E2E_VALIDATION_RESEARCH.md  
> **Purpose:** Get started quickly with practical validation

---

## Step 1: Use Existing Validators

The project already has validation frameworks. Start with these.

### Script Validation

```python
from validator.script_validator import ScriptValidator

validator = ScriptValidator(timeout_seconds=30)

# Run and validate
result = validator.run(
    command="python script.py",
    expected_output="Success",
    expected_exit_code=0
)

if result.passed():
    print("✅ Test passed")
else:
    print(f"❌ Failed: {result.message}")
```

### Web Validation

```python
from validator.web_validator import WebValidator

validator = WebValidator(browser_type="chromium")

result = await validator.test_url(
    "https://example.com",
    expected_text="Example Domain"
)

if result.passed():
    print("✅ Site works")
```

---

## Step 2: Create Your First Smoke Test

Create `tests/smoke_test.py`:

```python
#!/usr/bin/env python3
"""Basic smoke test"""

from validator.script_validator import ScriptValidator

def smoke_test():
    validator = ScriptValidator(timeout_seconds=30)
    
    print("🚀 Running smoke tests...")
    
    # Test 1: Dependencies available
    result = validator.run("python -c 'import livekit'")
    assert result.passed(), "LiveKit not installed"
    print("✅ Dependencies OK")
    
    # Test 2: Configuration loads
    result = validator.run("python -c 'from dotenv import load_dotenv; load_dotenv()'")
    assert result.passed(), "Config loading failed"
    print("✅ Configuration OK")
    
    # Test 3: Agent starts
    result = validator.run("python pi_agent.py", timeout=5)
    # Should start then timeout when we kill it
    print("✅ Agent starts")
    
    print("\n✅ All smoke tests passed!")

if __name__ == "__main__":
    smoke_test()
```

Run it:
```bash
python tests/smoke_test.py
```

---

## Step 3: Test Critical Workflows

Identify your 3 most critical workflows and create tests.

Example for voice agent:

```python
# tests/critical_workflows.py

def test_voice_query_workflow():
    """Test: User asks question, gets answer"""
    
    # 1. Start agent
    agent = VoiceAgent()
    assert agent.status == "ready"
    
    # 2. Send voice query
    response = agent.voice_query("What's the weather?")
    
    # 3. Validate response
    assert len(response) > 0
    assert agent_understands(response)
    assert response_helpful(response)
    
    print("✅ Voice query workflow works")

def test_script_execution_workflow():
    """Test: Agent generates and executes script"""
    
    # 1. Agent generates script
    script = agent.generate_script("List all .ts files")
    
    # 2. Validate script
    assert "find" in script or "glob" in script
    assert not dangerous_commands(script)
    
    # 3. Execute script
    result = validator.run_python(script_content=script)
    assert result.passed()
    assert ".ts" in result.evidence["stdout"]["content"]
    
    print("✅ Script execution workflow works")
```

---

## Step 4: Add Audio Testing (When Ready)

### Set Up Virtual Audio Device

**Windows:**
```bash
# Download and install VB-Cable
# https://vb-audio.com/Cable/
```

**macOS:**
```bash
brew install blackhole
```

**Linux:**
```bash
# PulseAudio loopback (usually built-in)
pactl load-module module-loopback
```

### Create Audio Test

```python
# tests/audio_test.py

def test_audio_pipeline():
    """Test STT → LLM → TTS pipeline"""
    
    # Load test audio
    audio = load_test_audio("hello.wav")
    
    # STT
    text = stt.transcribe(audio)
    assert "hello" in text.lower()
    
    # LLM
    response = llm.generate(text)
    assert len(response) > 0
    
    # TTS
    output_audio = tts.generate(response)
    assert duration(output_audio) > 0.5
    assert duration(output_audio) < 10
    
    print("✅ Audio pipeline works")
```

Generate test audio:
```bash
# Using espeak
espeak "Hello, this is a test" --stdout > tests/fixtures/hello.wav
```

---

## Step 5: Add Property-Based Tests

```python
# tests/property_tests.py

from hypothesis import given, strategies as st

@given(st.text())
def test_agent_never_crashes(query):
    """Agent should never crash on any text input"""
    try:
        response = agent.query(query)
        assert response is not None
    except Exception as e:
        assert False, f"Agent crashed on: {query[:50]}"

@given(st.text(), st.integers(min_value=0, max_value=1000))
def test_response_properties(query, context_length):
    """Response should have certain properties"""
    response = agent.query(query, context_length)
    
    # Never empty
    assert len(response) > 0
    
    # Not too long
    assert len(response) < 10000
    
    # No error phrases
    assert "i apologize" not in response.lower()
    assert "i cannot" not in response.lower()
```

---

## Step 6: Run Tests Regularly

### Before Committing

```bash
# Run smoke tests
python tests/smoke_test.py

# Run critical workflow tests
python tests/critical_workflows.py
```

### In CI/CD

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run smoke tests
        run: python tests/smoke_test.py
      
      - name: Run critical workflow tests
        run: python tests/critical_workflows.py
```

---

## Step 7: Collect Evidence

Configure evidence collection for debugging:

```python
# In your tests
validator = ScriptValidator(
    timeout_seconds=30,
    log_dir="evidence/logs"  # Evidence will be saved here
)

# After test run
result = validator.run("python script.py")

# Evidence is automatically saved to:
# evidence/logs/script_python_script.py.log
```

Evidence includes:
- Full stdout/stderr
- Exit codes
- Execution time
- Working directory
- Environment variables

---

## Common Patterns

### Test Script Execution

```python
def test_script():
    result = validator.run("python script.py")
    assert result.passed()
```

### Test API Call

```python
def test_api():
    result = validator.run(
        'curl -X POST https://api.example.com/data',
        expected_output='"status": "success"'
    )
    assert result.passed()
```

### Test File Creation

```python
def test_file_creation():
    result = validator.run(
        "python create_file.py",
        expected_files=["output.txt"]
    )
    assert result.passed()
```

### Test Error Handling

```python
def test_error_handling():
    result = validator.run(
        "python script.py --invalid",
        expected_exit_code=1,
        expected_in_stderr="Invalid argument"
    )
    assert result.passed()
```

---

## Checklist

- [ ] Set up `validator/script_validator.py`
- [ ] Create `tests/smoke_test.py`
- [ ] Identify 3 critical workflows
- [ ] Create tests for critical workflows
- [ ] Run tests manually
- [ ] Set up virtual audio device (for voice agents)
- [ ] Add audio pipeline tests
- [ ] Add property-based tests
- [ ] Configure evidence collection
- [ ] Set up CI/CD integration
- [ ] Document test procedures

---

## Troubleshooting

### Script Times Out

```python
# Increase timeout
result = validator.run("python script.py", timeout=60)
```

### Can't Find Expected Output

```python
# Use partial matching
result = validator.run("python script.py", expected_output="Success")
# Instead of exact match
```

### Virtual Audio Not Working

```bash
# Check if device is available
# Windows:
python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_device_count())"

# macOS:
# Check BlackHole in Audio MIDI Setup

# Linux:
pactl list sources short
```

---

## Next Steps

1. **Read the full research:** `E2E_VALIDATION_RESEARCH.md`
2. **Explore existing validators:** `validator/` directory
3. **Check voice agent docs:** `docs/LIVEKIT_SUMMARY.md`
4. **Review test examples:** `docs/TEST_CHECKLIST.md`

---

## Summary

*
