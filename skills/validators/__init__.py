"""
VALIDATORS - Specific validation skills for each case type
==========================================================

Each validator implements real validation for a specific type of system.
All validators follow the philosophy: Service only works if tested/validated

Available Validators:
- PythonScriptValidator: Execute and validate Python scripts
- WebAppValidator: Validate web apps with Playwright
- VoiceAgentValidator: Local TTS+STT loopback for voice agents
- APIValidator: HTTP request validation for APIs
- CLIToolValidator: CLI tool validation via bash execution

Usage:
    >>> from skills.validators import PythonScriptValidator
    >>> 
    >>> validator = PythonScriptValidator()
    >>> result = validator.validate("script.py", {"expect_exit_code": 0})
    >>> print(result.summary())
"""

from skills.validators.python_script_validator import PythonScriptValidator
from skills.validators.web_app_validator import WebAppValidator
from skills.validators.voice_agent_validator import VoiceAgentValidator
from skills.validators.api_validator import APIValidator
from skills.validators.cli_tool_validator import CLIToolValidator

__all__ = [
    "PythonScriptValidator",
    "WebAppValidator",
    "VoiceAgentValidator",
    "APIValidator",
    "CLIToolValidator",
]
