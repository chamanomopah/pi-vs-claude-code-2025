"""
VALIDATION ORCHESTRATOR
=======================

Coordinates case identification and skill execution.

Philosophy: Service only works if tested/validated

Author: E2E Validation Research
Date: April 12, 2026
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.identify_validation_case import (
    ValidationCaseIdentifier,
    ValidationCase,
    CaseType,
    ValidationStrategy
)
from skills.validators.python_script_validator import PythonScriptValidator, ValidationResult
from skills.validators.web_app_validator import WebAppValidator
from skills.validators.voice_agent_validator import VoiceAgentValidator
from skills.validators.api_validator import APIValidator
from skills.validators.cli_tool_validator import CLIToolValidator


@dataclass
class ValidationOutcome:
    """
    Result of a complete validation pipeline.
    
    Contains:
    - The identified validation case
    - The validation result from the appropriate skill
    - Timing and performance data
    - Actionable feedback
    """
    
    passed: bool
    target: str
    case_type: str
    validation_strategy: str
    confidence: float
    duration_ms: float
    validated_action: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    error_details: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)
    success_criteria_met: List[str] = field(default_factory=list)
    success_criteria_failed: List[str] = field(default_factory=list)
    validation_case: Optional[ValidationCase] = None
    validation_result: Optional[ValidationResult] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "passed": self.passed,
            "target": self.target,
            "case_type": self.case_type,
            "validation_strategy": self.validation_strategy,
            "confidence": self.confidence,
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
        return json.dumps(self.to_dict(), indent=indent)
    
    def print_summary(self) -> None:
        """Print a comprehensive summary."""
        status = "[PASS]" if self.passed else "[FAIL]"
        print(f"\n{'='*70}")
        print(f"E2E VALIDATION OUTCOME")
        print(f"{'='*70}")
        print(f"Status:       {status}")
        print(f"Target:       {self.target}")
        print(f"Type:         {self.case_type}")
        print(f"Strategy:     {self.validation_strategy}")
        print(f"Confidence:   {self.confidence:.0%}")
        print(f"Action:       {self.validated_action}")
        print(f"Duration:     {self.duration_ms:.2f}ms")

        if self.error_details:
            print(f"\nError: {self.error_details}")

        if self.success_criteria_met:
            print(f"\n✓ Met Criteria ({len(self.success_criteria_met)}):")
            for criterion in self.success_criteria_met[:5]:
                print(f"    • {criterion}")
            if len(self.success_criteria_met) > 5:
                print(f"    ... and {len(self.success_criteria_met) - 5} more")

        if self.success_criteria_failed:
            print(f"\n✗ Failed Criteria ({len(self.success_criteria_failed)}):")
            for criterion in self.success_criteria_failed[:5]:
                print(f"    • {criterion}")
            if len(self.success_criteria_failed) > 5:
                print(f"    ... and {len(self.success_criteria_failed) - 5} more")

        if self.suggestions:
            print(f"\nSuggestions ({len(self.suggestions)}):")
            for i, suggestion in enumerate(self.suggestions[:5], 1):
                print(f"  {i}. {suggestion}")
            if len(self.suggestions) > 5:
                print(f"  ... and {len(self.suggestions) - 5} more")

        print(f"{'='*70}\n")


class ValidationOrchestrator:
    """
    Coordinates case identification and skill execution.
    
    Philosophy: Service only works if tested/validated.
    
    This orchestrator:
    1. Identifies what type of system is being tested
    2. Selects the appropriate validation skill
    3. Executes real validation
    4. Collects and presents evidence
    5. Returns actionable results
    
    NO static analysis, NO assumptions, NO guessing
    Only REAL validation produces TRUTH
    """
    
    def __init__(
        self,
        auto_save_reports: bool = True,
        reports_dir: str = "evidence/orchestrator_reports"
    ):
        """
        Initialize the validation orchestrator.
        
        Args:
            auto_save_reports: Automatically save validation reports
            reports_dir: Directory to save reports
        """
        self.auto_save_reports = auto_save_reports
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize case identifier
        self.identifier = ValidationCaseIdentifier()
        
        # Initialize validators for each case type
        self.validators = {
            CaseType.PYTHON_SCRIPT: PythonScriptValidator(),
            CaseType.NODE_SCRIPT: None,  # Could add NodeScriptValidator
            CaseType.BASH_SCRIPT: None,  # Could add BashScriptValidator
            CaseType.WEB_APP: WebAppValidator(),
            CaseType.API_ENDPOINT: APIValidator(),
            CaseType.VOICE_AGENT: VoiceAgentValidator(),
            CaseType.CLI_TOOL: CLIToolValidator(),
            CaseType.RUST_SCRIPT: None,
            CaseType.GO_SCRIPT: None,
            CaseType.DIRECTORY: None,
            CaseType.PROJECT: None,
            CaseType.BINARY: None,
            CaseType.UNKNOWN: None,
        }
    
    def validate(
        self,
        target: Union[str, Path, Dict[str, Any]],
        expectations: Optional[Dict[str, Any]] = None,
        test_cases: Optional[List[Dict[str, Any]]] = None
    ) -> ValidationOutcome:
        """
        Complete validation pipeline.
        
        This is the main entry point. The orchestrator will:
        1. Identify the case (what type of system)
        2. Select the appropriate skill (validator)
        3. Execute validation
        4. Collect evidence
        5. Return actionable result
        
        Args:
            target: File path, directory, URL, or config dict
            expectations: Validation expectations (passed to validator)
            test_cases: Test cases for complex validation (e.g., voice agents)
        
        Returns:
            ValidationOutcome with comprehensive results
        
        Example:
            >>> orchestrator = ValidationOrchestrator()
            >>> 
            >>> # Auto-detect and validate
            >>> outcome = orchestrator.validate("script.py")
            >>> outcome.print_summary()
            >>> 
            >>> # With expectations
            >>> outcome = orchestrator.validate(
            ...     "https://example.com",
            ...     expectations={"expect_title": "Example"}
            ... )
            >>> 
            >>> # Voice agent with test cases
            >>> outcome = orchestrator.validate(
            ...     {"endpoint": "ws://localhost:8080"},
            ...     test_cases=[{"input_text": "Hello"}]
            ... )
        """
        start_time = time.time()
        expectations = expectations or {}
        
        # Step 1: Identify the case
        validation_case = self.identifier.identify(target)
        
        # Step 2: Select appropriate validator
        validator = self.validators.get(validation_case.case_type)
        
        if validator is None:
            # No validator available for this type
            duration_ms = (time.time() - start_time) * 1000
            
            return ValidationOutcome(
                passed=False,
                target=str(target),
                case_type=validation_case.case_type.value,
                validation_strategy=validation_case.validation_strategy.value,
                confidence=validation_case.confidence,
                duration_ms=duration_ms,
                validated_action="Case identification only",
                error_details=f"No validator available for type: {validation_case.case_type.value}",
                suggestions=validation_case.suggestions,
                validation_case=validation_case
            )
        
        # Step 3: Execute validation
        try:
            if validation_case.case_type == CaseType.VOICE_AGENT:
                # Voice agent needs test_cases
                validation_result = validator.validate(
                    validation_case.target,
                    test_cases or expectations
                )
            else:
                # Other validators use expectations
                validation_result = validator.validate(
                    validation_case.target,
                    expectations
                )
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            return ValidationOutcome(
                passed=False,
                target=str(target),
                case_type=validation_case.case_type.value,
                validation_strategy=validation_case.validation_strategy.value,
                confidence=validation_case.confidence,
                duration_ms=duration_ms,
                validated_action="Validation failed",
                error_details=f"Validator error: {e}",
                suggestions=[
                    "Check validator configuration",
                    "Verify target is accessible"
                ],
                validation_case=validation_case
            )
        
        # Step 4: Collect outcome
        duration_ms = (time.time() - start_time) * 1000
        
        outcome = ValidationOutcome(
            passed=validation_result.passed,
            target=str(target),
            case_type=validation_case.case_type.value,
            validation_strategy=validation_case.validation_strategy.value,
            confidence=validation_case.confidence,
            duration_ms=duration_ms,
            validated_action=validation_result.validated_action,
            evidence={
                "validation_case": validation_case.to_dict(),
                "validation_result": validation_result.to_dict()
            },
            error_details=validation_result.error_details,
            suggestions=validation_result.suggestions,
            success_criteria_met=validation_result.success_criteria_met,
            success_criteria_failed=validation_result.success_criteria_failed,
            validation_case=validation_case,
            validation_result=validation_result
        )
        
        # Step 5: Save report if enabled
        if self.auto_save_reports:
            self._save_outcome(outcome)
        
        return outcome
    
    def validate_batch(
        self,
        targets: List[Union[str, Path, Dict[str, Any]]],
        parallel: bool = False
    ) -> List[ValidationOutcome]:
        """
        Validate multiple targets.
        
        Args:
            targets: List of targets to validate
            parallel: Run validations in parallel (experimental)
        
        Returns:
            List of ValidationOutcome objects
        
        Example:
            >>> orchestrator = ValidationOrchestrator()
            >>> outcomes = orchestrator.validate_batch([
            ...     "script1.py",
            ...     "script2.py",
            ...     "https://example.com"
            ... ])
            >>> for outcome in outcomes:
            ...     print(f"{outcome.target}: {outcome.passed}")
        """
        outcomes = []
        
        if not parallel:
            # Sequential validation
            for i, target in enumerate(targets, 1):
                print(f"\n[{i}/{len(targets)}] Validating: {target}")
                outcome = self.validate(target)
                outcomes.append(outcome)
        else:
            # Parallel validation (experimental)
            import concurrent.futures
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self.validate, target): target
                    for target in targets
                }
                
                for future in concurrent.futures.as_completed(futures):
                    outcome = future.result()
                    outcomes.append(outcome)
        
        # Save summary
        self._save_batch_summary(outcomes)
        
        return outcomes
    
    def validate_directory(
        self,
        path: Path,
        recursive: bool = True
    ) -> Dict[str, Any]:
        """
        Scan and validate all testable components in a directory.
        
        Args:
            path: Directory path to scan
            recursive: Scan subdirectories
        
        Returns:
            Summary dictionary with all outcomes
        
        Example:
            >>> orchestrator = ValidationOrchestrator()
            >>> summary = orchestrator.validate_directory(Path("./my-project"))
            >>> print(f"Total: {summary['total']}, Passed: {summary['passed']}")
        """
        # Identify all cases in directory
        cases = self.identifier.analyze_directory(path)
        
        # Validate each case
        outcomes = []
        for case in cases:
            # Skip project/directory cases themselves
            if case.case_type in [CaseType.PROJECT, CaseType.DIRECTORY]:
                continue
            
            outcome = self.validate(case.target)
            outcomes.append(outcome)
        
        # Generate summary
        summary = {
            "total": len(outcomes),
            "passed": sum(1 for o in outcomes if o.passed),
            "failed": sum(1 for o in outcomes if not o.passed),
            "by_type": {},
            "outcomes": outcomes
        }
        
        # Group by type
        for outcome in outcomes:
            case_type = outcome.case_type
            if case_type not in summary["by_type"]:
                summary["by_type"][case_type] = {"passed": 0, "failed": 0}
            
            if outcome.passed:
                summary["by_type"][case_type]["passed"] += 1
            else:
                summary["by_type"][case_type]["failed"] += 1
        
        # Save summary
        self._save_directory_summary(path, summary)
        
        return summary
    
    def _save_outcome(self, outcome: ValidationOutcome) -> None:
        """Save validation outcome to file."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        # Make the filename safe - replace path separators with underscores
        safe_target = "".join(
            c if c.isalnum() else '_'
            for c in outcome.target
        )[:50]
        status = "PASS" if outcome.passed else "FAIL"
        filename = f"{timestamp}_{safe_target}_{status}.json"
        filepath = self.reports_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(outcome.to_json())
    
    def _save_batch_summary(self, outcomes: List[ValidationOutcome]) -> None:
        """Save batch validation summary."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"batch_{timestamp}.json"
        filepath = self.reports_dir / filename
        
        summary = {
            "timestamp": timestamp,
            "total": len(outcomes),
            "passed": sum(1 for o in outcomes if o.passed),
            "failed": sum(1 for o in outcomes if not o.passed),
            "outcomes": [o.to_dict() for o in outcomes]
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json.dumps(summary, indent=2))
    
    def _save_directory_summary(
        self,
        path: Path,
        summary: Dict[str, Any]
    ) -> None:
        """Save directory validation summary."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_path = str(path).replace("/", "_").replace("\\", "_")[:50]
        filename = f"dir_{safe_path}_{timestamp}.json"
        filepath = self.reports_dir / filename
        
        # Remove full outcomes from summary for cleaner report
        clean_summary = summary.copy()
        clean_summary["outcomes"] = [o.to_dict() for o in summary["outcomes"]]
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json.dumps(clean_summary, indent=2))
    
    def print_summary(self) -> None:
        """Print a summary of available validators."""
        print(f"\n{'='*70}")
        print(f"VALIDATION ORCHESTRATOR")
        print(f"{'='*70}")
        print(f"Reports directory: {self.reports_dir}")
        print(f"\nAvailable validators:")
        
        for case_type, validator in self.validators.items():
            status = "✓" if validator else "✗"
            print(f"  [{status}] {case_type.value:20s} - {validator.__class__.__name__ if validator else 'Not implemented'}")
        
        print(f"{'='*70}\n")


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def validate(
    target: Union[str, Path, Dict[str, Any]],
    **kwargs
) -> ValidationOutcome:
    """
    Quick one-liner to validate anything.
    
    Example:
        >>> outcome = validate("script.py", expect_output="Hello")
        >>> if outcome.passed:
        ...     print("Works!")
    """
    orchestrator = ValidationOrchestrator()
    return orchestrator.validate(target, kwargs)


def validate_batch(
    targets: List[Union[str, Path, Dict[str, Any]]]
) -> List[ValidationOutcome]:
    """
    Validate multiple targets.
    
    Example:
        >>> outcomes = validate_batch(["script1.py", "script2.py"])
        >>> for o in outcomes:
        ...     print(f"{o.target}: {o.passed}")
    """
    orchestrator = ValidationOrchestrator()
    return orchestrator.validate_batch(targets)


def validate_directory(path: Path) -> Dict[str, Any]:
    """
    Validate all testable components in a directory.
    
    Example:
        >>> summary = validate_directory(Path("./my-project"))
        >>> print(f"Passed: {summary['passed']}/{summary['total']}")
    """
    orchestrator = ValidationOrchestrator()
    return orchestrator.validate_directory(path)


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Command-line interface for the Validation Orchestrator."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validation Orchestrator - Validate anything end-to-end",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect and validate
  python validation_orchestrator.py script.py
  
  # Validate with expectations
  python validation_orchestrator.py script.py --expect-output "Hello"
  
  # Validate web app
  python validation_orchestrator.py https://example.com
  
  # Validate directory
  python validation_orchestrator.py ./my-project --directory
  
  # Batch validation
  python validation_orchestrator.py script1.py script2.py --batch
        """
    )
    
    parser.add_argument(
        "targets",
        nargs="+",
        help="Targets to validate (files, URLs, directories)"
    )
    parser.add_argument(
        "--expect-output", "-e",
        help="Expected output in response"
    )
    parser.add_argument(
        "--expect-status", "-s",
        type=int,
        help="Expected HTTP status code"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Timeout in seconds (default: 30)"
    )
    parser.add_argument(
        "--directory", "-d",
        action="store_true",
        help="Treat target as directory to scan"
    )
    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="Validate multiple targets"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output result as JSON"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only print pass/fail status"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save reports"
    )
    
    args = parser.parse_args()
    
    # Build expectations
    expectations = {}
    if args.expect_output:
        expectations["expect_output"] = args.expect_output
    if args.expect_status:
        expectations["expect_status"] = args.expect_status
    if args.timeout:
        expectations["timeout"] = args.timeout
    
    # Run validation
    orchestrator = ValidationOrchestrator(
        auto_save_reports=not args.no_save
    )
    
    if args.directory:
        # Directory validation
        summary = orchestrator.validate_directory(Path(args.targets[0]))
        
        if args.json:
            print(json.dumps(summary, indent=2))
        elif args.quiet:
            print(f"PASS" if summary["failed"] == 0 else "FAIL")
        else:
            print(f"\nDirectory validation complete:")
            print(f"  Total:   {summary['total']}")
            print(f"  Passed:  {summary['passed']}")
            print(f"  Failed:  {summary['failed']}")
    
    elif args.batch or len(args.targets) > 1:
        # Batch validation
        outcomes = orchestrator.validate_batch(args.targets)
        
        if args.json:
            print(json.dumps([o.to_dict() for o in outcomes], indent=2))
        elif args.quiet:
            all_passed = all(o.passed for o in outcomes)
            print("PASS" if all_passed else "FAIL")
        else:
            for outcome in outcomes:
                status = "[PASS]" if outcome.passed else "[FAIL]"
                print(f"{status} {outcome.target}")
    
    else:
        # Single target validation
        outcome = orchestrator.validate(args.targets[0], expectations)
        
        if args.json:
            print(outcome.to_json())
        elif args.quiet:
            print("PASS" if outcome.passed else "FAIL")
        else:
            outcome.print_summary()
    
    # Exit with appropriate code
    if args.directory:
        sys.exit(0 if summary["failed"] == 0 else 1)
    elif args.batch:
        sys.exit(0 if all(o.passed for o in outcomes) else 1)
    else:
        sys.exit(0 if outcome.passed else 1)


if __name__ == "__main__":
    main()
