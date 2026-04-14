"""
SKILL SYSTEM EXAMPLES
=====================

Practical examples demonstrating the E2E Validation Skill System.

Philosophy: Service only works if tested/validated

Author: E2E Validation Research
Date: April 12, 2026
"""

import time
from pathlib import Path
import tempfile

# Import skill system components
from skills import (
    ValidationOrchestrator,
    ValidationCaseIdentifier,
    validate,
    validate_batch
)
from skills.validators import (
    PythonScriptValidator,
    WebAppValidator,
    VoiceAgentValidator,
    APIValidator,
    CLIToolValidator,
    validate_python_script,
    validate_web_app,
    validate_cli_tool
)


def example_1_basic_identification():
    """
    Example 1: Basic Case Identification
    
    Demonstrates automatic detection of system types.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Case Identification")
    print("="*70)
    
    identifier = ValidationCaseIdentifier()
    
    # Test different targets
    targets = [
        "script.py",
        "https://example.com",
        "https://api.github.com/users",
        "ls -la",
        {"endpoint": "ws://localhost:8080", "type": "voice_agent"}
    ]
    
    for target in targets:
        case = identifier.identify(target)
        print(f"\nTarget: {target}")
        print(f"  Type:       {case.case_type.value}")
        print(f"  Strategy:   {case.validation_strategy.value}")
        print(f"  Confidence: {case.confidence:.0%}")
        print(f"  Ready:      {case.is_ready_to_validate()}")


def example_2_python_validation():
    """
    Example 2: Python Script Validation
    
    Demonstrates real script execution and validation.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Python Script Validation")
    print("="*70)
    
    # Create a test script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
import sys

def main():
    print("Hello, World!")
    print("Script executed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
""")
        script_path = f.name
    
    try:
        # Using the validator directly
        print("\n--- Direct Validator Usage ---")
        validator = PythonScriptValidator()
        result = validator.validate(
            script_path,
            expectations={
                "expect_output": "Hello, World!",
                "expect_exit_code": 0
            }
        )
        
        print(f"Passed: {result.passed}")
        print(f"Duration: {result.duration_ms:.2f}ms")
        print(f"Exit code: {result.evidence.get('exit_code')}")
        print(f"Output: {result.evidence.get('stdout', {}).get('content', '')[:100]}")
        
        # Using convenience function
        print("\n--- Convenience Function ---")
        result = validate_python_script(
            script_path,
            expect_output="Hello"
        )
        print(f"Passed: {result.passed}")
        
        # Using orchestrator (auto-detection)
        print("\n--- Orchestrator Auto-Detection ---")
        orchestrator = ValidationOrchestrator()
        outcome = orchestrator.validate(script_path)
        outcome.print_summary()
        
    finally:
        Path(script_path).unlink(missing_ok=True)


def example_3_web_validation():
    """
    Example 3: Web Application Validation
    
    Demonstrates browser automation validation.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Web Application Validation")
    print("="*70)
    
    # Test a real website
    url = "https://example.com"
    
    print(f"\nValidating: {url}")
    
    # Check if Playwright is available
    validator = WebAppValidator()
    
    if not validator.playwright_available:
        print("⚠ Playwright not installed - skipping browser test")
        print("  Install with: pip install playwright && playwright install chromium")
        return
    
    # Basic validation
    result = validator.validate(
        url,
        expectations={
            "expect_title": "Example",
            "timeout": 10000
        }
    )
    
    print(f"Passed: {result.passed}")
    print(f"HTTP Status: {result.evidence.get('http_status')}")
    print(f"Title: {result.evidence.get('title')}")
    
    if result.passed:
        print(f"Screenshot: {result.evidence.get('screenshot')}")


def example_4_api_validation():
    """
    Example 4: API Endpoint Validation
    
    Demonstrates HTTP request validation.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: API Endpoint Validation")
    print("="*70)
    
    # Test public APIs
    endpoints = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/json",
        "https://api.github.com/zen"
    ]
    
    validator = APIValidator()
    
    for endpoint in endpoints:
        print(f"\nValidating: {endpoint}")
        
        result = validator.validate(
            endpoint,
            expectations={
                "expect_status": 200,
                "expect_json_response": "json" in endpoint or "github" in endpoint
            }
        )
        
        print(f"  Status: {result.evidence.get('status_code')}")
        print(f"  Duration: {result.duration_ms:.2f}ms")
        print(f"  Passed: {result.passed}")


def example_5_cli_validation():
    """
    Example 5: CLI Tool Validation
    
    Demonstrates command execution validation.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: CLI Tool Validation")
    print("="*70)
    
    validator = CLIToolValidator()
    
    # Test common commands
    commands = [
        ("python --version", {"expect_exit_code": 0}),
        ("echo 'Hello, World!'", {"expect_output": "Hello"}),
        ("ls --help", {"expect_help": True})
    ]
    
    for command, expectations in commands:
        print(f"\nValidating: {command}")
        
        result = validator.validate(command, expectations)
        
        print(f"  Passed: {result.passed}")
        print(f"  Exit code: {result.evidence.get('exit_code')}")
        print(f"  Duration: {result.duration_ms:.2f}ms")


def example_6_voice_component_validation():
    """
    Example 6: Voice Agent Component Validation
    
    Demonstrates component-level validation for voice agents.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Voice Agent Component Validation")
    print("="*70)
    
    # Test voice agent components
    config = {
        "script": "voice_agent.py",
        "endpoint": "ws://localhost:8080"
    }
    
    validator = VoiceAgentValidator()
    
    # Check available tools
    print("\nAvailable tools:")
    for tool, available in validator.tools_available.items():
        status = "✓" if available else "✗"
        print(f"  [{status}] {tool}")
    
    # Validate components (without full loopback)
    from skills.validators.voice_agent_validator import VoiceComponentValidator
    
    component_validator = VoiceComponentValidator()
    result = component_validator.validate_components(config)
    
    print(f"\nComponent validation passed: {result.passed}")
    print(f"Met criteria: {len(result.success_criteria_met)}")
    print(f"Failed criteria: {len(result.success_criteria_failed)}")


def example_7_orchestrator_auto_detect():
    """
    Example 7: Orchestrator Auto-Detection
    
    Demonstrates the orchestrator's automatic type detection.
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Orchestrator Auto-Detection")
    print("="*70)
    
    orchestrator = ValidationOrchestrator(auto_save_reports=False)
    
    # Create test Python script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('print("Auto-detected Python script")')
        script_path = f.name
    
    try:
        # Test various targets
        targets = [
            ("Python script", script_path),
            ("CLI command", "python --version"),
            ("API endpoint", "https://httpbin.org/status/200"),
        ]
        
        for name, target in targets:
            print(f"\n{name}: {target}")
            outcome = orchestrator.validate(target)
            
            print(f"  Type:     {outcome.case_type}")
            print(f"  Strategy: {outcome.validation_strategy}")
            print(f"  Passed:   {outcome.passed}")
    
    finally:
        Path(script_path).unlink(missing_ok=True)


def example_8_batch_validation():
    """
    Example 8: Batch Validation
    
    Demonstrates validating multiple targets at once.
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Batch Validation")
    print("="*70)
    
    # Create test scripts
    test_files = []
    for i in range(3):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(f'print("Script {i+1}")')
            test_files.append(f.name)
    
    try:
        # Validate all scripts
        outcomes = validate_batch(test_files)
        
        print(f"\nValidated {len(outcomes)} scripts:")
        for outcome in outcomes:
            status = "✓" if outcome.passed else "✗"
            print(f"  [{status}] {Path(outcome.target).name}: {outcome.duration_ms:.2f}ms")
        
        # Summary
        passed = sum(1 for o in outcomes if o.passed)
        print(f"\nSummary: {passed}/{len(outcomes)} passed")
    
    finally:
        for path in test_files:
            Path(path).unlink(missing_ok=True)


def example_9_directory_validation():
    """
    Example 9: Directory Validation
    
    Demonstrates scanning and validating a directory.
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: Directory Validation")
    print("="*70)
    
    # Create temporary directory with test files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create some Python scripts
        for i in range(3):
            script_path = tmpdir_path / f"script_{i}.py"
            script_path.write_text(f'print("Script {i}")')
        
        # Create a README
        readme_path = tmpdir_path / "README.md"
        readme_path.write_text("# Test Project")
        
        # Validate directory
        orchestrator = ValidationOrchestrator(auto_save_reports=False)
        summary = orchestrator.validate_directory(tmpdir_path)
        
        print(f"\nDirectory validation results:")
        print(f"  Total scripts: {summary['total']}")
        print(f"  Passed: {summary['passed']}")
        print(f"  Failed: {summary['failed']}")


def example_10_quick_validate():
    """
    Example 10: Quick Validation Functions
    
    Demonstrates the convenience functions.
    """
    print("\n" + "="*70)
    print("EXAMPLE 10: Quick Validation Functions")
    print("="*70)
    
    # Create test script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('print("Quick test")')
        script_path = f.name
    
    try:
        # Using the ultra-convenient validate() function
        outcome = validate(script_path, expect_output="Quick test")
        
        print(f"Quick validation result:")
        print(f"  Passed: {outcome.passed}")
        print(f"  Type: {outcome.case_type}")
        print(f"  Duration: {outcome.duration_ms:.2f}ms")
    
    finally:
        Path(script_path).unlink(missing_ok=True)


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("E2E VALIDATION SKILL SYSTEM - EXAMPLES")
    print("="*70)
    print("\nThese examples demonstrate the complete skill system.")
    print("Philosophy: Service only works if tested/validated\n")
    
    examples = [
        ("Case Identification", example_1_basic_identification),
        ("Python Script Validation", example_2_python_validation),
        ("Web Application Validation", example_3_web_validation),
        ("API Endpoint Validation", example_4_api_validation),
        ("CLI Tool Validation", example_5_cli_validation),
        ("Voice Component Validation", example_6_voice_component_validation),
        ("Orchestrator Auto-Detection", example_7_orchestrator_auto_detect),
        ("Batch Validation", example_8_batch_validation),
        ("Directory Validation", example_9_directory_validation),
        ("Quick Validation Functions", example_10_quick_validate),
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\n" + "-"*70)
    choice = input("\nRun example (1-10) or 'all': ").strip().lower()
    
    if choice == "all":
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"\n❌ Example failed: {e}")
                import traceback
                traceback.print_exc()
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        idx = int(choice) - 1
        name, func = examples[idx]
        try:
            func()
        except Exception as e:
            print(f"\n❌ Example failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Invalid choice")
    
    print("\n" + "="*70)
    print("Examples complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
