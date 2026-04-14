"""
SKILL SYSTEM FOR E2E VALIDATION
==============================

A comprehensive skill-based system for end-to-end validation of any system.

Philosophy (from E2E_VALIDATION_RESEARCH.md):
- Service only works if tested/validated
- Test behavior, not implementation
- Use what's available locally
- Real execution only (NO static analysis)
- Embrace volatility (non-deterministic systems)

Core Components:
1. ValidationCaseIdentifier - Analyzes targets and determines validation approach
2. ValidationOrchestrator - Coordinates case identification and skill execution
3. Validators - Specific skills for each validation case type

Usage:
    >>> from skills import ValidationOrchestrator
    >>> 
    >>> orchestrator = ValidationOrchestrator()
    >>> result = orchestrator.validate("script.py")
    >>> print(result.summary())
"""

from skills.identify_validation_case import (
    ValidationCaseIdentifier,
    ValidationCase,
    CaseType,
    ValidationStrategy
)
from skills.validation_orchestrator import (
    ValidationOrchestrator,
    ValidationOutcome,
    validate,
    validate_batch,
    validate_directory
)

__all__ = [
    "ValidationCaseIdentifier",
    "ValidationCase",
    "CaseType",
    "ValidationStrategy",
    "ValidationOrchestrator",
    "ValidationOutcome",
    "validate",
    "validate_batch",
    "validate_directory"
]

__version__ = "1.0.0"
