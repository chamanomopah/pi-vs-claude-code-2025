"""
CLI TOOL VALIDATOR
==================

Validates CLI tools via bash execution.

Philosophy: Run commands like a user would.

Author: E2E Validation Research
Date: April 12, 2026
"""

import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from skills.validators.python_script_validator import ValidationResult


class CLIToolValidator:
    """
    Validates CLI tools via bash execution.
    
    Philosophy: Run commands like a user would.
    
    This validator:
    - Executes CLI commands in a subprocess
    - Captures stdout, stderr, exit codes
    - Validates help text and documentation
    - Tests command execution
    - Validates output format
    
    NO mocking, NO stubbing, NO fake commands
    Only REAL command execution produces TRUTH
    """
    
    def __init__(
        self,
        shell: bool = True,
        timeout: int = 30,
        working_dir: Optional[Path] = None
    ):
        """
        Initialize the CLI tool validator.
        
        Args:
            shell: Run command in shell (allows pipes, redirects)
            timeout: Default timeout in seconds
            working_dir: Working directory for execution
        """
        self.shell = shell
        self.default_timeout = timeout
        self.working_dir = working_dir or Path.cwd()
        
        # Detect OS
        self.os_type = platform.system().lower()
        
        # Set appropriate shell for OS
        if self.os_type == "windows":
            self.default_shell = True  # cmd.exe on Windows
        else:
            self.default_shell = True  # /bin/sh on Unix
    
    def validate(
        self,
        target: Union[str, List[str]],
        expectations: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Execute CLI commands and validate.
        
        Args:
            target: Command string or list of args
                Examples:
                - "git --version"
                - ["python", "script.py", "--help"]
                - "ls -la | grep .py"
            expectations: Validation expectations
                - expect_exit_code: Expected exit code (default: 0)
                - expect_output: String that should be in stdout
                - expect_not_output: String that should NOT be in stdout
                - expect_in_stderr: String that should be in stderr
                - expect_help: Command should have --help support
                - expect_version: Command should have --version support
                - timeout: Override default timeout
        
        Returns:
            ValidationResult with comprehensive results
        
        Example:
            >>> validator = CLIToolValidator()
            >>> 
            >>> # Basic validation
            >>> result = validator.validate("python --version")
            >>> 
            >>> # With expectations
            >>> result = validator.validate(
            ...     "git status",
            ...     expectations={"expect_output": "On branch"}
            ... )
            >>> 
            >>> # Validate help text
            >>> result = validator.validate(
            ...     "mycli",
            ...     expectations={"expect_help": True}
            ... )
        """
        start_time = time.time()
        expectations = expectations or {}
        
        # Handle command as string or list
        if isinstance(target, list):
            command_str = " ".join(target)
            command_args = target
            use_shell = False
        else:
            command_str = str(target)
            command_args = None
            use_shell = self.shell
        
        # Check for help/version validation first
        if expectations.get("expect_help"):
            return self._validate_help(command_str, expectations)
        
        if expectations.get("expect_version"):
            return self._validate_version(command_str, expectations)
        
        # Build command
        if command_args:
            cmd = command_args
        else:
            cmd = command_str
        
        timeout = expectations.get("timeout", self.default_timeout)
        validated_action = f"Executed: {command_str}"
        
        # Prepare environment
        env = os.environ.copy()
        if "env" in expectations:
            env.update(expectations["env"])
        
        # Execute command
        try:
            result = subprocess.run(
                cmd,
                shell=use_shell,
                capture_output=True,
                timeout=timeout,
                cwd=self.working_dir,
                env=env,
                text=True
            )
            
            stdout = result.stdout
            stderr = result.stderr
            exit_code = result.returncode
            
        except subprocess.TimeoutExpired:
            duration_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                passed=False,
                validator_type="cli_tool",
                target=command_str,
                duration_ms=duration_ms,
                validated_action=validated_action,
                error_details=f"Command timed out after {timeout} seconds",
                suggestions=[
                    "Command may be hanging or waiting for input",
                    "Increase timeout if command is slow",
                    "Check for interactive prompts"
                ]
            )
        
        except FileNotFoundError as e:
            duration_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                passed=False,
                validator_type="cli_tool",
                target=command_str,
                duration_ms=duration_ms,
                validated_action=validated_action,
                error_details=f"Command not found: {e}",
                suggestions=[
                    "Check if the command is installed",
                    f"Try: which {command_str.split()[0]}",
                    "Verify PATH environment variable"
                ]
            )
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                passed=False,
                validator_type="cli_tool",
                target=command_str,
                duration_ms=duration_ms,
                validated_action=validated_action,
                error_details=f"Execution error: {e}",
                suggestions=[
                    "Check command syntax",
                    "Verify permissions"
                ]
            )
        
        duration_ms = (time.time() - start_time) * 1000
        
        # Validate results
        success_criteria_met = []
        success_criteria_failed = []
        suggestions = []
        
        # Check exit code
        expect_exit = expectations.get("expect_exit_code", 0)
        if isinstance(expect_exit, list):
            exit_ok = exit_code in expect_exit
        else:
            exit_ok = exit_code == expect_exit
        
        if exit_ok:
            success_criteria_met.append(f"Exit code: {exit_code}")
        else:
            success_criteria_failed.append(f"Exit code: {exit_code} (expected {expect_exit})")
            if exit_code != 0:
                suggestions.append(f"Command failed with exit code {exit_code}")
                if stderr:
                    suggestions.append(f"Error output: {stderr[:200]}")
        
        # Check stdout
        if "expect_output" in expectations:
            expected = expectations["expect_output"]
            if expected in stdout:
                success_criteria_met.append(f"Output contains: {expected[:50]}")
            else:
                success_criteria_failed.append(f"Output missing: {expected[:50]}")
                suggestions.append("Expected output not found")
        
        if "expect_not_output" in expectations:
            unexpected = expectations["expect_not_output"]
            if unexpected not in stdout:
                success_criteria_met.append(f"Output doesn't contain: {unexpected[:50]}")
            else:
                success_criteria_failed.append(f"Output contains unexpected: {unexpected[:50]}")
        
        # Check stderr
        if "expect_in_stderr" in expectations:
            expected = expectations["expect_in_stderr"]
            if expected in stderr:
                success_criteria_met.append(f"Stderr contains: {expected[:50]}")
            else:
                success_criteria_failed.append(f"Stderr missing: {expected[:50]}")
        
        # Check for errors in stderr
        if stderr and "error" in stderr.lower() and exit_code != 0:
            suggestions.append("Command produced error output")
        
        # Determine overall pass/fail
        passed = len(success_criteria_failed) == 0 and exit_ok
        
        # Collect evidence
        evidence = {
            "exit_code": exit_code,
            "stdout": {
                "content": stdout,
                "lines": stdout.count("\n") + 1 if stdout else 0,
                "chars": len(stdout)
            },
            "stderr": {
                "content": stderr,
                "lines": stderr.count("\n") + 1 if stderr else 0,
                "chars": len(stderr)
            },
            "duration_ms": duration_ms,
            "command": command_str,
            "working_dir": str(self.working_dir),
            "os_type": self.os_type
        }
        
        return ValidationResult(
            passed=passed,
            validator_type="cli_tool",
            target=command_str,
            duration_ms=duration_ms,
            validated_action=validated_action,
            evidence=evidence,
            error_details=stderr if stderr and not passed else None,
            suggestions=suggestions,
            success_criteria_met=success_criteria_met,
            success_criteria_failed=success_criteria_failed
        )
    
    def _validate_help(
        self,
        command: str,
        expectations: Dict[str, Any]
    ) -> ValidationResult:
        """Validate that command has help text."""
        start_time = time.time()
        
        # Extract base command
        base_cmd = command.split()[0]
        
        # Try common help flags
        help_flags = ["--help", "-h", "help", "/?"]
        
        for flag in help_flags:
            try:
                result = subprocess.run(
                    [base_cmd, flag] if not self.shell else f"{base_cmd} {flag}",
                    shell=self.shell,
                    capture_output=True,
                    timeout=5
                )
                
                # Check if help text looks valid
                output = result.stdout + result.stderr
                if self._is_help_text(output):
                    duration_ms = (time.time() - start_time) * 1000
                    return ValidationResult(
                        passed=True,
                        validator_type="cli_tool",
                        target=command,
                        duration_ms=duration_ms,
                        validated_action=f"Checked help: {base_cmd} {flag}",
                        evidence={
                            "help_flag": flag,
                            "exit_code": result.returncode,
                            "help_text_length": len(output)
                        },
                        success_criteria_met=[f"Help available: {flag}"],
                        suggestions=[]
                    )
            except Exception:
                continue
        
        # No help found
        duration_ms = (time.time() - start_time) * 1000
        return ValidationResult(
            passed=False,
            validator_type="cli_tool",
            target=command,
            duration_ms=duration_ms,
            validated_action="Checked help flags",
            error_details="No help text found",
            suggestions=[
                "Command doesn't support standard help flags",
                "Try: --help, -h, or 'help' subcommand",
                "Check command documentation"
            ]
        )
    
    def _validate_version(
        self,
        command: str,
        expectations: Dict[str, Any]
    ) -> ValidationResult:
        """Validate that command has version info."""
        start_time = time.time()
        
        # Extract base command
        base_cmd = command.split()[0]
        
        # Try common version flags
        version_flags = ["--version", "-v", "-V", "version", "version"]
        
        for flag in version_flags:
            try:
                result = subprocess.run(
                    [base_cmd, flag] if not self.shell else f"{base_cmd} {flag}",
                    shell=self.shell,
                    capture_output=True,
                    timeout=5
                )
                
                # Check if output looks like version info
                output = result.stdout + result.stderr
                if self._is_version_text(output):
                    duration_ms = (time.time() - start_time) * 1000
                    return ValidationResult(
                        passed=True,
                        validator_type="cli_tool",
                        target=command,
                        duration_ms=duration_ms,
                        validated_action=f"Checked version: {base_cmd} {flag}",
                        evidence={
                            "version_flag": flag,
                            "exit_code": result.returncode,
                            "version_output": output.strip()[:100]
                        },
                        success_criteria_met=[f"Version available: {flag}"],
                        suggestions=[]
                    )
            except Exception:
                continue
        
        # No version found
        duration_ms = (time.time() - start_time) * 1000
        return ValidationResult(
            passed=False,
            validator_type="cli_tool",
            target=command,
            duration_ms=duration_ms,
            validated_action="Checked version flags",
            error_details="No version info found",
            suggestions=[
                "Command doesn't support standard version flags",
                "Try: --version, -v, -V, or 'version' subcommand"
            ]
        )
    
    @staticmethod
    def _is_help_text(text: bytes) -> bool:
        """Check if text looks like help output."""
        if not text:
            return False
        
        text_str = text.decode(errors="ignore").lower()
        
        # Help text indicators
        help_indicators = [
            "usage:",
            "options:",
            "arguments:",
            "commands:",
            "available",
            "description:",
            "-h, --help",
            "help, h"
        ]
        
        # Should have at least one indicator and decent length
        return (
            any(indicator in text_str for indicator in help_indicators) and
            len(text_str) > 50
        )
    
    @staticmethod
    def _is_version_text(text: bytes) -> bool:
        """Check if text looks like version output."""
        if not text:
            return False
        
        text_str = text.decode(errors="ignore")
        
        # Version patterns
        import re
        version_patterns = [
            r'\d+\.\d+\.\d+',  # 1.2.3
            r'v\d+\.\d+',       # v1.2
            r'version\s*\d+',   # version 1
        ]
        
        for pattern in version_patterns:
            if re.search(pattern, text_str):
                return True
        
        return False
    
    def validate_command_chain(
        self,
        commands: List[str],
        expectations: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Validate a chain of commands (pipes, redirects).
        
        Args:
            commands: List of commands to chain together
            expectations: Validation expectations
        
        Example:
            >>> validator = CLIToolValidator()
            >>> result = validator.validate_command_chain([
            ...     "echo 'hello world'",
            ...     "grep hello",
            ...     "wc -l"
            ], expectations={"expect_exit_code": 0})
        """
        start_time = time.time()
        expectations = expectations or {}
        
        # Build command chain
        command_chain = " | ".join(commands)
        
        try:
            result = subprocess.run(
                command_chain,
                shell=True,
                capture_output=True,
                timeout=expectations.get("timeout", self.default_timeout),
                cwd=self.working_dir,
                text=True
            )
            
            duration_ms = (time.time() - start_time) * 1000
            
            return ValidationResult(
                passed=result.returncode == 0,
                validator_type="cli_tool_chain",
                target=command_chain,
                duration_ms=duration_ms,
                validated_action=f"Executed chain of {len(commands)} commands",
                evidence={
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                },
                error_details=result.stderr if result.returncode != 0 else None,
                success_criteria_met=["All commands executed"] if result.returncode == 0 else [],
                success_criteria_failed=["Command chain failed"] if result.returncode != 0 else []
            )
            
        except subprocess.TimeoutExpired:
            duration_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                passed=False,
                validator_type="cli_tool_chain",
                target=command_chain,
                duration_ms=duration_ms,
                validated_action="Command chain (timeout)",
                error_details="Command chain timed out"
            )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def validate_cli_tool(
    target: Union[str, List[str]],
    **expectations
) -> ValidationResult:
    """
    Quick one-liner to validate a CLI tool.
    
    Example:
        >>> result = validate_cli_tool(
        ...     "python --version",
        ...     expect_exit_code=0
        ... )
        >>> print(result.passed)
    """
    validator = CLIToolValidator()
    return validator.validate(target, expectations)


def validate_command_help(command: str) -> ValidationResult:
    """
    Validate that a command has help text.
    
    Example:
        >>> result = validate_command_help("git")
        >>> print(result.passed)
    """
    validator = CLIToolValidator()
    return validator.validate(command, expectations={"expect_help": True})


def validate_command_version(command: str) -> ValidationResult:
    """
    Validate that a command has version info.
    
    Example:
        >>> result = validate_command_version("python")
        >>> print(result.passed)
    """
    validator = CLIToolValidator()
    return validator.validate(command, expectations={"expect_version": True})
