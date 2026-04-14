"""
VALIDATION CASE IDENTIFIER
=========================

Analyzes a target and determines:
1. What type of system it is
2. What validation approach to use
3. What tools are needed
4. What success criteria look like

Philosophy: Service only works if tested/validated

Author: E2E Validation Research
Date: April 12, 2026
"""

import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Set
import mimetypes
import json


class CaseType(Enum):
    """Types of systems that can be validated."""
    
    # Script types
    PYTHON_SCRIPT = "python_script"
    NODE_SCRIPT = "node_script"
    BASH_SCRIPT = "bash_script"
    RUST_SCRIPT = "rust_script"
    GO_SCRIPT = "go_script"
    
    # Application types
    WEB_APP = "web_app"
    API_ENDPOINT = "api_endpoint"
    VOICE_AGENT = "voice_agent"
    
    # Tool types
    CLI_TOOL = "cli_tool"
    BINARY = "binary"
    
    # Project types
    DIRECTORY = "directory"
    PROJECT = "project"
    
    # Unknown
    UNKNOWN = "unknown"


class ValidationStrategy(Enum):
    """Validation strategies for different case types."""
    
    # Execution strategies
    SUBPROCESS_EXECUTION = "subprocess_execution"  # Run script/command
    BROWSER_AUTOMATION = "browser_automation"      # Playwright/Selenium
    HTTP_REQUEST = "http_request"                  # curl/requests
    
    # Audio strategies
    TTS_STT_LOOPBACK = "tts_stt_loopback"         # Local audio loopback
    AUDIO_COMPONENT = "audio_component"            # Test individual components
    
    # Project strategies
    SMOKE_TEST = "smoke_test"                      # Quick validation
    INTEGRATION_TEST = "integration_test"          # Full integration
    
    # General strategies
    MANUAL = "manual"                              # Manual validation
    HYBRID = "hybrid"                              # Multiple strategies


@dataclass
class ToolRequirement:
    """Represents a tool required for validation."""
    
    name: str
    command: str
    check_cmd: Optional[str] = None
    install_hint: Optional[str] = None
    optional: bool = False
    version_min: Optional[str] = None
    
    def is_available(self) -> bool:
        """Check if the tool is available."""
        import subprocess
        
        check_command = self.check_cmd or self.command
        try:
            result = subprocess.run(
                check_command,
                shell=True,
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "command": self.command,
            "available": self.is_available(),
            "install_hint": self.install_hint,
            "optional": self.optional
        }


@dataclass
class SuccessCriterion:
    """Defines a success criterion for validation."""
    
    name: str
    check_type: str  # "exit_code", "output_contains", "http_status", "response_time", etc.
    expected_value: Any
    comparison: str = "equals"  # "equals", "contains", "greater_than", "less_than", "matches", etc.
    required: bool = True
    weight: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "check_type": self.check_type,
            "expected_value": self.expected_value,
            "comparison": self.comparison,
            "required": self.required,
            "weight": self.weight
        }


@dataclass
class TestCommand:
    """Represents a test command to execute."""
    
    command: str
    description: str
    timeout: int = 30
    expected_exit_code: int = 0
    expected_output: Optional[str] = None
    not_expected_output: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "command": self.command,
            "description": self.description,
            "timeout": self.timeout,
            "expected_exit_code": self.expected_exit_code,
            "expected_output": self.expected_output,
            "not_expected_output": self.not_expected_output
        }


@dataclass
class ValidationCase:
    """
    Represents a complete validation case for a target.
    
    This contains all information needed to validate a target:
    - What type of system it is
    - How to validate it
    - What tools are needed
    - What success looks like
    - How confident we are in this identification
    """
    
    target: str
    case_type: CaseType
    validation_strategy: ValidationStrategy
    required_tools: List[ToolRequirement] = field(default_factory=list)
    optional_tools: List[ToolRequirement] = field(default_factory=list)
    success_criteria: List[SuccessCriterion] = field(default_factory=list)
    test_commands: List[TestCommand] = field(default_factory=list)
    confidence: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)
    
    def get_all_tools(self) -> List[ToolRequirement]:
        """Get all tools (required + optional)."""
        return self.required_tools + self.optional_tools
    
    def get_missing_tools(self) -> List[ToolRequirement]:
        """Get tools that are required but not available."""
        return [t for t in self.required_tools if not t.is_available()]
    
    def is_ready_to_validate(self) -> bool:
        """Check if all required tools are available."""
        return all(t.is_available() for t in self.required_tools)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "target": self.target,
            "case_type": self.case_type.value,
            "validation_strategy": self.validation_strategy.value,
            "required_tools": [t.to_dict() for t in self.required_tools],
            "optional_tools": [t.to_dict() for t in self.optional_tools],
            "success_criteria": [c.to_dict() for c in self.success_criteria],
            "test_commands": [c.to_dict() for c in self.test_commands],
            "confidence": self.confidence,
            "metadata": self.metadata,
            "suggestions": self.suggestions,
            "ready_to_validate": self.is_ready_to_validate(),
            "missing_tools": [t.name for t in self.get_missing_tools()]
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def print_summary(self) -> None:
        """Print a human-readable summary."""
        print(f"\n{'='*70}")
        print(f"VALIDATION CASE: {self.target}")
        print(f"{'='*70}")
        print(f"Type:         {self.case_type.value}")
        print(f"Strategy:     {self.validation_strategy.value}")
        print(f"Confidence:   {self.confidence:.0%}")
        
        if self.required_tools:
            print(f"\nRequired Tools:")
            for tool in self.required_tools:
                status = "✓" if tool.is_available() else "✗"
                print(f"  [{status}] {tool.name}")
        
        if self.success_criteria:
            print(f"\nSuccess Criteria:")
            for criterion in self.success_criteria:
                print(f"  - {criterion.name}: {criterion.check_type} {criterion.comparison} {criterion.expected_value}")
        
        if self.test_commands:
            print(f"\nTest Commands:")
            for cmd in self.test_commands[:3]:  # Show first 3
                print(f"  $ {cmd.command}")
            if len(self.test_commands) > 3:
                print(f"  ... and {len(self.test_commands) - 3} more")
        
        if self.suggestions:
            print(f"\nSuggestions:")
            for suggestion in self.suggestions[:3]:
                print(f"  • {suggestion}")
        
        print(f"{'='*70}\n")


class ValidationCaseIdentifier:
    """
    Analyzes a target and determines the validation approach.
    
    This is the intelligence layer that figures out:
    1. What type of system we're dealing with
    2. How to validate it
    3. What we need to validate it
    4. What success looks like
    
    Philosophy: Service only works if tested/validated
    """
    
    def __init__(self):
        """Initialize the identifier."""
        # File extension patterns
        self.extension_map = {
            ".py": CaseType.PYTHON_SCRIPT,
            ".pyw": CaseType.PYTHON_SCRIPT,
            ".js": CaseType.NODE_SCRIPT,
            ".mjs": CaseType.NODE_SCRIPT,
            ".cjs": CaseType.NODE_SCRIPT,
            ".ts": CaseType.NODE_SCRIPT,  # Assume TypeScript runs via Node
            ".sh": CaseType.BASH_SCRIPT,
            ".bash": CaseType.BASH_SCRIPT,
            ".rs": CaseType.RUST_SCRIPT,
            ".go": CaseType.GO_SCRIPT,
        }
        
        # Shebang patterns
        self.shebang_map = {
            "#!/usr/bin/env python": CaseType.PYTHON_SCRIPT,
            "#!/usr/bin/python": CaseType.PYTHON_SCRIPT,
            "#!/usr/bin/env python3": CaseType.PYTHON_SCRIPT,
            "#!/usr/bin/python3": CaseType.PYTHON_SCRIPT,
            "#!/usr/bin/env node": CaseType.NODE_SCRIPT,
            "#!/usr/bin/node": CaseType.NODE_SCRIPT,
            "#!/bin/bash": CaseType.BASH_SCRIPT,
            "#!/usr/bin/env bash": CaseType.BASH_SCRIPT,
            "#!/bin/sh": CaseType.BASH_SCRIPT,
        }
        
        # Project file markers
        self.project_markers = {
            "package.json": CaseType.NODE_SCRIPT,
            "requirements.txt": CaseType.PYTHON_SCRIPT,
            "pyproject.toml": CaseType.PYTHON_SCRIPT,
            "setup.py": CaseType.PYTHON_SCRIPT,
            "Cargo.toml": CaseType.RUST_SCRIPT,
            "go.mod": CaseType.GO_SCRIPT,
            "package.yaml": CaseType.UNKNOWN,  # Helm chart
            "docker-compose.yml": CaseType.UNKNOWN,
            "Dockerfile": CaseType.UNKNOWN,
        }
    
    def identify(
        self,
        target: Union[str, Path, Dict[str, Any]]
    ) -> ValidationCase:
        """
        Analyze a target and return a ValidationCase.
        
        Args:
            target: File path, directory, URL, or config dict
        
        Returns:
            ValidationCase with complete validation information
        """
        # Handle different target types
        if isinstance(target, dict):
            return self._identify_from_config(target)
        
        target_path = Path(target) if isinstance(target, str) else target
        target_str = str(target)
        
        # URL detection
        if self._is_url(target_str):
            return self._identify_url(target_str)
        
        # File/directory detection
        if target_path.exists():
            if target_path.is_file():
                return self._identify_file(target_path)
            elif target_path.is_dir():
                return self._identify_directory(target_path)
        
        # Command-like string
        if self._is_command(target_str):
            return self._identify_command(target_str)
        
        # Unknown target
        return self._create_unknown_case(target_str)
    
    def analyze_directory(
        self,
        path: Path
    ) -> List[ValidationCase]:
        """
        Scan directory and identify all testable components.
        
        Args:
            path: Directory path to scan
        
        Returns:
            List of ValidationCase objects
        """
        cases = []
        
        if not path.exists() or not path.is_dir():
            return cases
        
        # Identify the directory/project itself
        project_case = self.identify(path)
        cases.append(project_case)
        
        # Scan for individual testable files
        for item in path.rglob("*"):
            if item.is_file():
                # Skip common non-testable files
                if self._should_skip_file(item):
                    continue
                
                case = self.identify(item)
                if case.case_type != CaseType.UNKNOWN:
                    cases.append(case)
        
        return cases
    
    def analyze_config(
        self,
        config: Dict[str, Any]
    ) -> ValidationCase:
        """
        Parse config and determine validation approach.
        
        Args:
            config: Configuration dictionary
        
        Returns:
            ValidationCase based on config
        """
        return self._identify_from_config(config)
    
    # ========================================================================
    # PRIVATE METHODS - Identification logic
    # ========================================================================
    
    def _identify_from_config(self, config: Dict[str, Any]) -> ValidationCase:
        """Identify validation case from configuration dict."""
        target = config.get("target", config.get("name", "unknown"))
        case_type_str = config.get("type", config.get("case_type"))
        
        # Try to parse explicit type
        if case_type_str:
            try:
                case_type = CaseType(case_type_str)
                return self._create_case_from_type(target, case_type, config)
            except ValueError:
                pass
        
        # Check for voice agent config
        if any(k in config for k in ["endpoint", "ws_url", "websocket", "stt", "tts"]):
            return self._create_voice_agent_case(target, config)
        
        # Check for API config
        if any(k in config for k in ["url", "endpoint", "api", "base_url"]):
            url = config.get("url", config.get("endpoint", ""))
            if self._is_url(url):
                return self._identify_url(url)
        
        # Check for script config
        if "script" in config or "command" in config:
            script = config.get("script", config.get("command", ""))
            return self._identify_command(script)
        
        return self._create_unknown_case(target)
    
    def _identify_url(self, url: str) -> ValidationCase:
        """Identify validation case for URL."""
        if url.startswith(("ws://", "wss://")):
            # WebSocket URL - likely voice agent
            return self._create_voice_agent_case(url, {"endpoint": url})
        
        # HTTP URL - web app or API
        # We'll determine by checking if it's likely an API endpoint
        if any(keyword in url.lower() for keyword in ["/api/", "/v1/", "/v2/", "/graphql"]):
            return self._create_api_case(url)
        
        return self._create_web_app_case(url)
    
    def _identify_file(self, file_path: Path) -> ValidationCase:
        """Identify validation case for file."""
        # Check file extension
        suffix = file_path.suffix.lower()
        
        if suffix in self.extension_map:
            case_type = self.extension_map[suffix]
            return self._create_script_case(str(file_path), case_type)
        
        # Check shebang for scripts without extensions
        if suffix == "" or file_path.suffix is None:
            shebang = self._read_shebang(file_path)
            if shebang and shebang in self.shebang_map:
                case_type = self.shebang_map[shebang]
                return self._create_script_case(str(file_path), case_type)
        
        # Check if it's an executable binary
        if os.access(file_path, os.X_OK):
            return self._create_binary_case(str(file_path))
        
        # Check if it's a config file (JSON, YAML, etc.)
        if suffix in [".json", ".yaml", ".yml", ".toml", ".xml"]:
            return self._create_config_file_case(str(file_path))
        
        return self._create_unknown_case(str(file_path))
    
    def _identify_directory(self, dir_path: Path) -> ValidationCase:
        """Identify validation case for directory."""
        # Check for project markers
        project_types = []
        found_markers = []
        
        for marker, case_type in self.project_markers.items():
            marker_path = dir_path / marker
            if marker_path.exists():
                found_markers.append(marker)
                if case_type != CaseType.UNKNOWN:
                    project_types.append(case_type)
        
        # Determine primary project type
        primary_type = project_types[0] if project_types else CaseType.UNKNOWN
        
        return ValidationCase(
            target=str(dir_path),
            case_type=CaseType.PROJECT,
            validation_strategy=ValidationStrategy.SMOKE_TEST,
            confidence=0.9 if found_markers else 0.5,
            metadata={
                "project_type": primary_type.value if primary_type else "unknown",
                "markers": found_markers,
                "file_count": sum(1 for _ in dir_path.rglob("*") if _.is_file())
            },
            suggestions=[
                "Run smoke tests to validate project structure",
                "Check for test files and run them"
            ]
        )
    
    def _identify_command(self, command: str) -> ValidationCase:
        """Identify validation case for command string."""
        parts = command.strip().split()
        if not parts:
            return self._create_unknown_case(command)
        
        cmd = parts[0].lower()
        
        # Map commands to case types
        command_map = {
            "python": CaseType.PYTHON_SCRIPT,
            "python3": CaseType.PYTHON_SCRIPT,
            "python2": CaseType.PYTHON_SCRIPT,
            "node": CaseType.NODE_SCRIPT,
            "bash": CaseType.BASH_SCRIPT,
            "sh": CaseType.BASH_SCRIPT,
            "cargo": CaseType.RUST_SCRIPT,
            "go": CaseType.GO_SCRIPT,
            "go run": CaseType.GO_SCRIPT,
        }
        
        # Check for exact match
        if cmd in command_map:
            case_type = command_map[cmd]
            return self._create_script_case(command, case_type)
        
        # Check for "go run" special case
        if " ".join(parts[:2]).lower() == "go run":
            return self._create_script_case(command, CaseType.GO_SCRIPT)
        
        # Unknown command - treat as CLI tool
        return self._create_cli_tool_case(command)
    
    # ========================================================================
    # CASE CREATION HELPERS
    # ========================================================================
    
    def _create_script_case(
        self,
        target: str,
        case_type: CaseType
    ) -> ValidationCase:
        """Create validation case for script."""
        # Determine required tools based on case type
        tool_map = {
            CaseType.PYTHON_SCRIPT: [
                ToolRequirement("Python", "python", "python --version"),
            ],
            CaseType.NODE_SCRIPT: [
                ToolRequirement("Node.js", "node", "node --version"),
                ToolRequirement("npm", "npm", "npm --version", optional=True),
            ],
            CaseType.BASH_SCRIPT: [
                ToolRequirement("Bash", "bash", "bash --version"),
            ],
            CaseType.RUST_SCRIPT: [
                ToolRequirement("Rust", "cargo", "cargo --version"),
            ],
            CaseType.GO_SCRIPT: [
                ToolRequirement("Go", "go", "go version"),
            ],
        }
        
        required_tools = tool_map.get(case_type, [])
        
        return ValidationCase(
            target=target,
            case_type=case_type,
            validation_strategy=ValidationStrategy.SUBPROCESS_EXECUTION,
            required_tools=required_tools,
            confidence=0.95,
            test_commands=[
                TestCommand(
                    command=target,
                    description="Execute script",
                    timeout=30
                )
            ],
            success_criteria=[
                SuccessCriterion(
                    name="exit_code_zero",
                    check_type="exit_code",
                    expected_value=0,
                    comparison="equals"
                )
            ]
        )
    
    def _create_web_app_case(self, url: str) -> ValidationCase:
        """Create validation case for web application."""
        return ValidationCase(
            target=url,
            case_type=CaseType.WEB_APP,
            validation_strategy=ValidationStrategy.BROWSER_AUTOMATION,
            required_tools=[
                ToolRequirement(
                    "Playwright",
                    "playwright",
                    "python -c 'import playwright'",
                    install_hint="pip install playwright && playwright install chromium"
                ),
            ],
            confidence=0.9,
            test_commands=[
                TestCommand(
                    command=f"curl -s -o /dev/null -w '%{{http_code}}' {url}",
                    description="Check HTTP status",
                    timeout=10
                )
            ],
            success_criteria=[
                SuccessCriterion(
                    name="page_loads",
                    check_type="http_status",
                    expected_value=200,
                    comparison="equals"
                ),
                SuccessCriterion(
                    name="response_time",
                    check_type="response_time",
                    expected_value=5000,
                    comparison="less_than"
                )
            ]
        )
    
    def _create_api_case(self, url: str) -> ValidationCase:
        """Create validation case for API endpoint."""
        return ValidationCase(
            target=url,
            case_type=CaseType.API_ENDPOINT,
            validation_strategy=ValidationStrategy.HTTP_REQUEST,
            required_tools=[
                ToolRequirement("curl", "curl", "curl --version"),
            ],
            confidence=0.9,
            test_commands=[
                TestCommand(
                    command=f"curl -s {url}",
                    description="API GET request",
                    timeout=10
                )
            ],
            success_criteria=[
                SuccessCriterion(
                    name="http_success",
                    check_type="http_status",
                    expected_value=200,
                    comparison="in_range",
                    weight=1.0
                )
            ]
        )
    
    def _create_voice_agent_case(
        self,
        target: str,
        config: Dict[str, Any]
    ) -> ValidationCase:
        """Create validation case for voice agent."""
        return ValidationCase(
            target=target,
            case_type=CaseType.VOICE_AGENT,
            validation_strategy=ValidationStrategy.TTS_STT_LOOPBACK,
            required_tools=[
                ToolRequirement(
                    "Python",
                    "python",
                    "python --version"
                ),
            ],
            optional_tools=[
                ToolRequirement(
                    "LiveKit",
                    "livekit",
                    "python -c 'import livekit'",
                    install_hint="pip install livekit"
                ),
                ToolRequirement(
                    "pyttsx3 (TTS)",
                    "pyttsx3",
                    "python -c 'import pyttsx3'",
                    install_hint="pip install pyttsx3"
                ),
                ToolRequirement(
                    "whisper (STT)",
                    "whisper",
                    "python -c 'import whisper'",
                    install_hint="pip install openai-whisper"
                ),
            ],
            confidence=0.85,
            metadata={"config": config},
            success_criteria=[
                SuccessCriterion(
                    name="agent_responds",
                    check_type="response_received",
                    expected_value=True,
                    comparison="equals"
                ),
                SuccessCriterion(
                    name="latency_acceptable",
                    check_type="latency_ms",
                    expected_value=3000,
                    comparison="less_than",
                    required=False
                )
            ]
        )
    
    def _create_cli_tool_case(self, command: str) -> ValidationCase:
        """Create validation case for CLI tool."""
        return ValidationCase(
            target=command,
            case_type=CaseType.CLI_TOOL,
            validation_strategy=ValidationStrategy.SUBPROCESS_EXECUTION,
            required_tools=[],
            confidence=0.6,
            test_commands=[
                TestCommand(
                    command=f"{command} --help",
                    description="Check help text",
                    timeout=5
                )
            ],
            success_criteria=[
                SuccessCriterion(
                    name="help_available",
                    check_type="exit_code",
                    expected_value=0,
                    comparison="in_range",  # 0 or some tools return non-zero for --help
                    required=False
                )
            ],
            suggestions=[
                "Verify the tool is installed and in PATH",
                "Check if the command requires specific arguments"
            ]
        )
    
    def _create_binary_case(self, path: str) -> ValidationCase:
        """Create validation case for binary executable."""
        return ValidationCase(
            target=path,
            case_type=CaseType.BINARY,
            validation_strategy=ValidationStrategy.SUBPROCESS_EXECUTION,
            confidence=0.8,
            test_commands=[
                TestCommand(
                    command=path,
                    description="Execute binary",
                    timeout=10
                )
            ],
            success_criteria=[
                SuccessCriterion(
                    name="executes",
                    check_type="exit_code",
                    expected_value=0,
                    comparison="in_range",
                    required=False
                )
            ]
        )
    
    def _create_config_file_case(self, path: str) -> ValidationCase:
        """Create validation case for config file."""
        return ValidationCase(
            target=path,
            case_type=CaseType.UNKNOWN,
            validation_strategy=ValidationStrategy.MANUAL,
            confidence=0.3,
            suggestions=[
                "Config files cannot be directly validated",
                "Use a tool/script that consumes this config",
                "Validate schema if applicable"
            ]
        )
    
    def _create_unknown_case(self, target: str) -> ValidationCase:
        """Create validation case for unknown target."""
        return ValidationCase(
            target=target,
            case_type=CaseType.UNKNOWN,
            validation_strategy=ValidationStrategy.MANUAL,
            confidence=0.0,
            required_tools=[],
            success_criteria=[],
            suggestions=[
                "Could not determine validation approach",
                "Specify test_type explicitly",
                "Check if target path is correct"
            ]
        )
    
    def _create_case_from_type(
        self,
        target: str,
        case_type: CaseType,
        config: Dict[str, Any]
    ) -> ValidationCase:
        """Create case from explicit type in config."""
        creators = {
            CaseType.PYTHON_SCRIPT: lambda t: self._create_script_case(t, CaseType.PYTHON_SCRIPT),
            CaseType.NODE_SCRIPT: lambda t: self._create_script_case(t, CaseType.NODE_SCRIPT),
            CaseType.BASH_SCRIPT: lambda t: self._create_script_case(t, CaseType.BASH_SCRIPT),
            CaseType.WEB_APP: self._create_web_app_case,
            CaseType.API_ENDPOINT: self._create_api_case,
            CaseType.VOICE_AGENT: lambda t: self._create_voice_agent_case(t, config),
            CaseType.CLI_TOOL: self._create_cli_tool_case,
        }
        
        creator = creators.get(case_type)
        if creator:
            return creator(target)
        
        return self._create_unknown_case(target)
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    @staticmethod
    def _is_url(s: str) -> bool:
        """Check if string is a URL."""
        return s.startswith(("http://", "https://", "ws://", "wss://"))
    
    @staticmethod
    def _is_command(s: str) -> bool:
        """Check if string looks like a command."""
        parts = s.strip().split()
        if not parts:
            return False
        
        cmd = parts[0].lower()
        # Check for common command prefixes
        command_prefixes = [
            "python", "python3", "node", "npm", "bash", "sh",
            "cargo", "go", "dotnet", "java", "ruby", "php",
            "curl", "wget", "git", "docker"
        ]
        
        return cmd in command_prefixes or "/" in cmd or "\\" in cmd
    
    @staticmethod
    def _read_shebang(file_path: Path, max_lines: int = 1) -> Optional[str]:
        """Read shebang from file."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for _ in range(max_lines):
                    line = f.readline()
                    if line.startswith("#!"):
                        return line.strip()
        except (IOError, UnicodeDecodeError):
            pass
        return None
    
    @staticmethod
    def _should_skip_file(file_path: Path) -> bool:
        """Check if file should be skipped during directory scan."""
        skip_patterns = [
            "__pycache__", "node_modules", ".git", ".venv", "venv",
            "target", "build", "dist", ".next", ".nuxt"
        ]
        
        # Skip files in common directories to ignore
        for part in file_path.parts:
            if part in skip_patterns:
                return True
        
        # Skip based on extension
        skip_extensions = {
            ".pyc", ".pyo", ".pyd", ".so", ".dll", ".dylib",
            ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
            ".woff", ".woff2", ".ttf", ".eot",
            ".zip", ".tar", ".gz", ".rar", ".7z",
            ".class", ".jar", ".war",
        }
        
        if file_path.suffix.lower() in skip_extensions:
            return True
        
        return False


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def identify_case(target: Union[str, Path, Dict]) -> ValidationCase:
    """Quick one-liner to identify validation case.
    
    Example:
        >>> case = identify_case("script.py")
        >>> case.print_summary()
    """
    identifier = ValidationCaseIdentifier()
    return identifier.identify(target)


def identify_directory_cases(path: Path) -> List[ValidationCase]:
    """Identify all validation cases in a directory.
    
    Example:
        >>> cases = identify_directory_cases(Path("./my-project"))
        >>> for case in cases:
        ...     print(f"{case.case_type.value}: {case.target}")
    """
    identifier = ValidationCaseIdentifier()
    return identifier.analyze_directory(path)
