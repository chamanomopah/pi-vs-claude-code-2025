# E2E Validation Skill System

> **Philosophy: Service only works if tested/validated**

A comprehensive skill-based system for end-to-end validation of any system. Built on the research from `E2E_VALIDATION_RESEARCH.md` and `PRACTICAL_EXAMPLES.md`.

## 🎯 Core Philosophy

- **Real execution only** - NO static analysis, NO mocking, NO assumptions
- **Test behavior, not implementation** - Validate what users experience
- **Use what's available locally** - No cloud dependencies
- **Embrace volatility** - Handle non-deterministic systems gracefully

## 📁 Structure

```
skills/
├── __init__.py                           # Package initialization
├── identify_validation_case.py           # Case identification skill
├── validation_orchestrator.py            # Coordinates everything
├── validators/
│   ├── __init__.py
│   ├── python_script_validator.py       # Python script validation
│   ├── web_app_validator.py             # Web app validation (Playwright)
│   ├── voice_agent_validator.py         # Voice agent (TTS+STT local)
│   ├── api_validator.py                 # API validation (HTTP)
│   └── cli_tool_validator.py            # CLI tool validation
└── examples.py                           # Usage examples
```

## 🚀 Quick Start

### Installation

```bash
# Core dependencies (always needed)
pip install playwright

# Optional dependencies (for specific validators)
pip install pyttsx3          # TTS for voice validation
pip install openai-whisper   # STT for voice validation
pip install edge-tts         # Alternative TTS

# Install Playwright browsers
playwright install chromium
```

### Basic Usage

```python
from skills import validate

# Auto-detect and validate anything
outcome = validate("script.py")
print(f"Passed: {outcome.passed}")

# With expectations
outcome = validate("https://example.com", expect_title="Example")
outcome.print_summary()
```

## 📖 Components

### 1. Validation Case Identifier

Analyzes a target and determines the validation approach.

```python
from skills import ValidationCaseIdentifier

identifier = ValidationCaseIdentifier()
case = identifier.identify("script.py")

print(f"Type: {case.case_type.value}")           # python_script
print(f"Strategy: {case.validation_strategy}")   # subprocess_execution
print(f"Confidence: {case.confidence}")          # 0.95
print(f"Required tools: {[t.name for t in case.required_tools]}")
```

**Supported Case Types:**
- `PYTHON_SCRIPT` - Python scripts (.py)
- `NODE_SCRIPT` - Node.js scripts (.js, .mjs)
- `BASH_SCRIPT` - Bash scripts (.sh, .bash)
- `WEB_APP` - Web applications (HTTP/HTTPS URLs)
- `API_ENDPOINT` - API endpoints
- `VOICE_AGENT` - Voice agents (WebSocket endpoints)
- `CLI_TOOL` - Command-line tools

### 2. Validation Orchestrator

Coordinates case identification and skill execution.

```python
from skills import ValidationOrchestrator

orchestrator = ValidationOrchestrator()

# Auto-detect type and validate
outcome = orchestrator.validate("script.py")
outcome.print_summary()

# Validate multiple targets
outcomes = orchestrator.validate_batch([
    "script1.py",
    "script2.py",
    "https://example.com"
])

# Validate entire directory
summary = orchestrator.validate_directory(Path("./my-project"))
print(f"Passed: {summary['passed']}/{summary['total']}")
```

### 3. Validators

#### Python Script Validator

```python
from skills.validators import PythonScriptValidator

validator = PythonScriptValidator()
result = validator.validate(
    "script.py",
    expectations={
        "expect_output": "Hello, World!",
        "expect_exit_code": 0,
        "timeout": 30
    }
)

print(f"Passed: {result.passed}")
print(f"Duration: {result.duration_ms}ms")
print(f"Exit code: {result.evidence['exit_code']}")
```

#### Web App Validator

```python
from skills.validators import WebAppValidator

validator = WebAppValidator()
result = validator.validate(
    "https://example.com",
    expectations={
        "expect_title": "Example",
        "expect_text": "Domain",
        "expect_element": "h1",
        "screenshot": True
    }
)
```

#### Voice Agent Validator

```python
from skills.validators import VoiceAgentValidator

validator = VoiceAgentValidator(
    tts_engine="pyttsx3",
    stt_engine="whisper"
)

result = validator.validate(
    {
        "endpoint": "ws://localhost:8080",
        "script": "voice_agent.py"
    },
    test_cases=[
        {
            "input_text": "Hello",
            "expect_response": "hi there",
            "max_latency_ms": 3000
        }
    ]
)
```

**Note:** Full audio loopback requires:
- Virtual audio cable (VB-Cable on Windows, BlackHole on macOS)
- Or agent that accepts file input

**Component validation** (without loopback):
```python
from skills.validators.voice_agent_validator import VoiceComponentValidator

validator = VoiceComponentValidator()
result = validator.validate_components(config)
```

#### API Validator

```python
from skills.validators import APIValidator

validator = APIValidator()

# GET request
result = validator.validate(
    "https://api.example.com/health",
    expectations={
        "expect_status": 200,
        "expect_json_response": True
    }
)

# POST request
result = validator.validate({
    "url": "https://api.example.com/users",
    "method": "POST",
    "body": {"name": "John"},
    "headers": {"Authorization": "Bearer token"}
}, expectations={"expect_status": 201})
```

#### CLI Tool Validator

```python
from skills.validators import CLIToolValidator

validator = CLIToolValidator()

# Basic validation
result = validator.validate(
    "python --version",
    expectations={"expect_exit_code": 0}
)

# Validate help text
result = validator.validate(
    "mycli",
    expectations={"expect_help": True}
)

# Command with pipes
result = validator.validate_command_chain([
    "echo 'hello world'",
    "grep hello",
    "wc -l"
])
```

## 🎨 Examples

Run the examples to see the skill system in action:

```bash
python skills/examples.py
```

Examples include:
1. Case identification
2. Python script validation
3. Web application validation
4. API endpoint validation
5. CLI tool validation
6. Voice component validation
7. Orchestrator auto-detection
8. Batch validation
9. Directory validation
10. Quick validation functions

## 🔧 Advanced Usage

### Custom Validation Strategy

```python
from skills.identify_validation_case import ValidationCase, CaseType, ValidationStrategy

# Create custom validation case
custom_case = ValidationCase(
    target="my_service",
    case_type=CaseType.WEB_APP,
    validation_strategy=ValidationStrategy.BROWSER_AUTOMATION,
    required_tools=[],
    confidence=1.0,
    test_commands=[]
)
```

### Parallel Validation

```python
orchestrator = ValidationOrchestrator()
outcomes = orchestrator.validate_batch(
    ["script1.py", "script2.py", "script3.py"],
    parallel=True
)
```

### Custom Timeout and Environment

```python
validator = PythonScriptValidator(
    python_executable="python3.9",
    timeout=60,
    working_dir=Path("/path/to/project")
)

result = validator.validate(
    "script.py",
    expectations={
        "timeout": 45,
        "env": {"API_KEY": "secret", "DEBUG": "1"}
    }
)
```

## 📊 Output

### Validation Outcome

```python
outcome = validate("script.py")

# Check result
if outcome.passed:
    print("✓ Validation passed")
else:
    print(f"✗ Validation failed: {outcome.error_details}")
    for suggestion in outcome.suggestions:
        print(f"  • {suggestion}")

# Access evidence
print(f"Type: {outcome.case_type}")
print(f"Duration: {outcome.duration_ms}ms")
print(f"Strategy: {outcome.validation_strategy}")

# Print summary
outcome.print_summary()

# Export as JSON
json_output = outcome.to_json()
```

## 🔍 Philosophy in Practice

### What the Skill System DOES:

- ✅ Execute real code/scripts
- ✅ Launch real browsers
- ✅ Make real HTTP requests
- ✅ Run real CLI commands
- ✅ Generate real audio (TTS)
- ✅ Transcribe real audio (STT)
- ✅ Capture real evidence
- ✅ Measure real performance

### What the Skill System DOESN'T do:

- ❌ Static code analysis
- ❌ Mock/stub responses
- ❌ Assume behavior
- ❌ Parse source code
- ❌ Use test doubles
- ❌ Guess outcomes

## 🛠️ Troubleshooting

### Playwright Not Installed

```bash
pip install playwright
playwright install chromium
```

### TTS/STT Not Available

```bash
# For pyttsx3
pip install pyttsx3

# For whisper (larger download)
pip install openai-whisper

# For faster-whisper (recommended)
pip install faster-whisper
```

### ffmpeg Not Found

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## 📝 Validation Reports

Reports are automatically saved to `evidence/orchestrator_reports/`:

```
evidence/orchestrator_reports/
├── 20240412_143022_script_py_PASS.json
├── 20240412_143025_example_com_PASS.json
└── batch_20240412_143030.json
```

Disable auto-save:

```python
orchestrator = ValidationOrchestrator(auto_save_reports=False)
```

## 🎯 Best Practices

1. **Start Simple** - Use `validate()` for quick checks
2. **Be Specific** - Add expectations for robust validation
3. **Check Evidence** - Review captured evidence for insights
4. **Use Orchestrator** - Let it auto-detect types
5. **Batch Operations** - Validate multiple targets efficiently
6. **Component Testing** - For voice agents, test components first
7. **Review Reports** - Check saved reports for historical data

## 📚 Related Documentation

- `docs/research/E2E_VALIDATION_RESEARCH.md` - Philosophy and principles
- `docs/research/PRACTICAL_EXAMPLES.md` - Real-world validation patterns
- `agents/e2e_validator_agent.py` - Agent-based validation system

## 🤝 Integration with Agent

This skill system integrates with the E2E Validator Agent:

```python
from agents.e2e_validator_agent import E2EValidatorAgent

agent = E2EValidatorAgent()
report = agent.validate("script.py")
report.print_summary()
```

The agent uses the same skill system under the hood!

## 📄 License

Part of the E2E Validation System. See project LICENSE for details.

---

**Remember: Service only works if tested/validated**
