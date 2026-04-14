"""
PYTHON SCRIPT VALIDATOR
=======================

Validates Python scripts by executing them.

Philosophy: Run it for real, don't analyze code.

Author: E2E Validation Research
Date: April 12, 2026
"""

import os
import sys
import subprocess
import time
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from skills.identify_validation_case import (
    ValidationCase,
    TestCommand,
    SuccessCriterion
)


@dataclass
class ValidationResult:
    """Result of a validation execution."""
    
    passed: bool
    validator_type: str
    target: str
    duration_ms: float
    validated_action: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    error_details: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)
    success_criteria_met: List[str] = field(default_factory=list)
    success_criteria_failed: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "passed": self.passed,
            "validator_type": self.validator_type,
            "target": self.target,
            "duration_ms": self.duration_ms,
            "validated_action": self.validated_action,
            "evidence": self.evidence,
            "error_details": self.error_details,
            "suggestions": self.suggestions,
            "success_criteria_met": self.success_criteria_met,
            "success_criteria_failed": self.success_criteria_failed
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        import json
        return json.dumps(self.to_dict(), indent=indent)
    
    def print_summary(self) -> None:
        """Print a human-readable summary."""
        status = "[PASS]" if self.passed else "[FAIL]"
        print(f"\n{'='*60}")
        print(f"VALIDATION RESULT: {self.validator_type}")
        print(f"{'='*60}")
        print(f"Status:     {status}")
        print(f"Target:     {self.target}")
        print(f"Action:     {self.validated_action}")
        print(f"Duration:   {self.duration_ms:.2f}ms")

        if self.error_details:
            print(f"\nError: {self.error_details}")

        if self.suggestions:
            print(f"\nSuggestions:")
            for i, suggestion in enumerate(self.suggestions, 1):
                print(f"  {i}. {suggestion}")

        if self.success_criteria_met:
            print(f"\nMet Criteria:")
            for criterion in self.success_criteria_met:
                print(f"  ✓ {criterion}")

        if self.success_criteria_failed:
            print(f"\nFailed Criteria:")
            for criterion in self.success_criteria_failed:
                print(f"  ✗ {criterion}")

        print(f"{'='*60}\n")


class PythonScriptValidator:
    """
    Validates Python scripts by executing them.
    
    Philosophy: Run it for real, don't analyze code.
    
    This validator:
    - Executes Python scripts in a subprocess
    - Captures stdout, stderr, exit code
    - Validates output against expectations
    - Measures execution time
    - Provides actionable feedback
    
    NO static analysis, NO linting, NO type checking
    Only REAL execution produces TRUTH
    """
    
    def __init__(
        self,
        python_executable: str = "python",
        timeout: int = 30,
        working_dir: Optional[Path] = None
    ):
        """
        Initialize the Python script validator.
        
        Args:
            python_executable: Python command to use (python, python3, etc.)
            timeout: Default timeout in seconds
            working_dir: Working directory for execution
        """
        self.python_executable = python_executable
        self.default_timeout = timeout
        self.working_dir = working_dir or Path.cwd()
        
        # Check Python availability
        self._check_python()
    
    def _check_python(self) -> None:
        """Verify Python is available."""
        try:
            result = subprocess.run(
                [self.python_executable, "--version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stderr.decode().strip() or result.stdout.decode().strip()
                self.python_version = version
            else:
                raise RuntimeError(f"{self.python_executable} not available")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f"Python not available: {e}")
    
    def validate(
        self,
        target: Union[str, Path, ValidationCase],
        expectations: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Execute Python script and validate.
        
        Args:
            target: Script path, command, or ValidationCase
            expectations: Validation expectations
                - expect_exit_code: Expected exit code (default: 0)
                - expect_output: String that should be in stdout
                - expect_not_output: String that should NOT be in stdout
                - expect_in_stderr: String that should be in stderr
                - timeout: Override default timeout
                - args: Command line arguments to pass
                - env: Environment variables (dict)
        
        Returns:
            ValidationResult with comprehensive results
        
        Example:
            >>> validator = PythonScriptValidator()
            >>> 
            >>> # Basic validation
            >>> result = validator.validate("script.py")
            >>> 
            >>> # With expectations
            >>> result = validator.validate(
            ...     "script.py",
            ...     expectations={"expect_output": "Hello World"}
            ... )
            >>> 
            >>> # With arguments
            >>> result = validator.validate(
            ...     "script.py",
            ...     expectations={"args": ["--input", "data.txt"]}
            ... )
        """
        start_time = time.time()
        expectations = expectations or {}
        
        # Extract target info
        if isinstance(target, ValidationCase):
            script_path = target.target
            case_type = target.case_type.value
        else:
            script_path = str(target)
            case_type = "python_script"
        
        # Build command
        command_parts = [self.python_executable]
        
        # Check if target is a file or a full command
        if script_path.endswith(".py") and Path(script_path).exists():
            command_parts.append(script_path)
        elif not script_path.startswith(self.python_executable):
            # It's a script path, might need .py extension
            if Path(script_path).exists():
                command_parts.append(script_path)
            else:
                # Treat as a Python command
                command_parts = [self.python_executable, "-c", script_path]
        else:
            # Full command provided
            command_parts = script_path.split()
        
        # Add arguments
        if "args" in expectations:
            command_parts.extend(expectations["args"])
        
        # Prepare environment
        env = os.environ.copy()
        if "env" in expectations:
            env.update(expectations["env"])
        
        # Set timeout
        timeout = expectations.get("timeout", self.default_timeout)
        
        # Execute script
        validated_action = f"Executed: {' '.join(command_parts)}"
        
        try:
            result = subprocess.run(
                command_parts,
                capture_output=True,
                timeout=timeout,
                cwd=self.working_dir,
                env=env,
                text=True
            )
            
            stdout = result.stdout
            stderr = result.stderr
            exit_code = result.returncode
            
        except subprocess.TimeoutExpired as e:
            duration_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                passed=False,
                validator_type=case_type,
                target=script_path,
                duration_ms=duration_ms,
                validated_action=validated_action,
                error_details=f"Script timed out after {timeout} seconds",
                suggestions=[
                    "Script may be hanging or waiting for input",
                    "Increase timeout if script is slow",
                    "Check for infinite loops"
                ],
                evidence={
                    "timeout": timeout,
                    "partial_output": e.stdout.decode() if e.stdout else None
                }
            )
        
        except FileNotFoundError as e:
            duration_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                passed=False,
                validator_type=case_type,
                target=script_path,
                duration_ms=duration_ms,
                validated_action=validated_action,
                error_details=f"File not found: {e}",
                suggestions=[
                    "Check if the script path is correct",
                    "Verify Python executable path"
                ]
            )
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                passed=False,
                validator_type=case_type,
                target=script_path,
                duration_ms=duration_ms,
                validated_action=validated_action,
                error_details=f"Execution error: {e}",
                suggestions=[
                    "Check script permissions",
                    "Verify dependencies are installed"
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
                suggestions.append("Check for unhandled exceptions in the script")
                suggestions.append("Verify the script has a proper entry point")
        
        # Check stdout
        if "expect_output" in expectations:
            expected = expectations["expect_output"]
            if expected in stdout:
                success_criteria_met.append(f"Output contains: {expected[:50]}")
            else:
                success_criteria_failed.append(f"Output missing: {expected[:50]}")
                suggestions.append("Verify the script prints the expected output")
        
        if "expect_not_output" in expectations:
            unexpected = expectations["expect_not_output"]
            if unexpected not in stdout:
                success_criteria_met.append(f"Output does not contain: {unexpected[:50]}")
            else:
                success_criteria_failed.append(f"Output contains unexpected: {unexpected[:50]}")
        
        # Check stderr
        if "expect_in_stderr" in expectations:
            expected = expectations["expect_in_stderr"]
            if expected in stderr:
                success_criteria_met.append(f"Stderr contains: {expected[:50]}")
            else:
                success_criteria_failed.append(f"Stderr missing: {expected[:50]}")
        
        # Determine overall pass/fail
        # Fail if any required criteria failed
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
            "command": " ".join(command_parts),
            "working_dir": str(self.working_dir)
        }
        
        # Add Python version
        if hasattr(self, "python_version"):
            evidence["python_version"] = self.python_version
        
        return ValidationResult(
            passed=passed,
            validator_type=case_type,
            target=script_path,
            duration_ms=duration_ms,
            validated_action=validated_action,
            evidence=evidence,
            error_details=stderr if stderr and not passed else None,
            suggestions=suggestions,
            success_criteria_met=success_criteria_met,
            success_criteria_failed=success_criteria_failed
        )
    
    def validate_with_input(
        self,
        script_path: Union[str, Path],
        input_data: str,
        expectations: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Validate script with stdin input.
        
        Args:
            script_path: Path to Python script
            input_data: Data to send to stdin
            expectations: Validation expectations
        
        Example:
            >>> validator = PythonScriptValidator()
            >>> result = validator.validate_with_input(
            ...     "calculator.py",
            ...     "2 + 2\\n",
            ...     {"expect_output": "4"}
            ... )
        """
        expectations = expectations or {}
        start_time = time.time()
        
        try:
            result = subprocess.run(
                [self.python_executable, str(script_path)],
                input=input_data,
                capture_output=True,
                timeout=expectations.get("timeout", self.default_timeout),
                cwd=self.working_dir,
                text=True
            )
            
            # Reuse the validate method's logic
            # Create a mock result
            duration_ms = (time.time() - start_time) * 1000
            
            # Build validation result manually
            success_criteria_met = []
            success_criteria_failed = []
            suggestions = []
            
            expect_exit = expectations.get("expect_exit_code", 0)
            exit_ok = result.returncode == expect_exit
            
            if exit_ok:
                success_criteria_met.append(f"Exit code: {result.returncode}")
            else:
                success_criteria_failed.append(f"Exit code: {result.returncode}")
            
            passed = exit_ok
            
            if "expect_output" in expectations:
                if expectations["expect_output"] in result.stdout:
                    success_criteria_met.append("Output matches expectation")
                else:
                    success_criteria_failed.append("Output does not match")
                    passed = False
            
            return ValidationResult(
                passed=passed,
                validator_type="python_script",
                target=str(script_path),
                duration_ms=duration_ms,
                validated_action=f"Executed with stdin input",
                evidence={
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "stdin_provided": len(input_data)
                },
                error_details=result.stderr if result.stderr else None,
                suggestions=suggestions,
                success_criteria_met=success_criteria_met,
                success_criteria_failed=success_criteria_failed
            )
            
        except subprocess.TimeoutExpired:
            duration_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                passed=False,
                validator_type="python_script",
                target=str(script_path),
                duration_ms=duration_ms,
                validated_action="Executed with stdin (timeout)",
                error_details="Script timed out waiting for input",
                suggestions=["Script may be waiting for more input"]
            )
    
    def validate_snippet(
        self,
        code: str,
        expectations: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Validate a Python code snippet.
        
        Args:
            code: Python code to execute
            expectations: Validation expectations
        
        Example:
            >>> validator = PythonScriptValidator()
            >>> result = validator.validate_snippet(
            ...     "print('Hello, World!')",
            ...     {"expect_output": "Hello, World!"}
            ... )
        """
        expectations = expectations or {}
        
        # Write code to temp file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            return self.validate(temp_path, expectations)
        finally:
            # Clean up temp file
            try:
                Path(temp_path).unlink()
            except:
                pass


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def validate_python_script(
    target: Union[str, Path],
    **expectations
) -> ValidationResult:
    """
    Quick one-liner to validate a Python script.
    
    Example:
        >>> result = validate_python_script(
        ...     "script.py",
        ...     expect_output="Hello",
        ...     timeout=10
        ... )
        >>> print(result.passed)
    """
    validator = PythonScriptValidator()
    return validator.validate(target, expectations)
