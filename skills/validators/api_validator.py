"""
API VALIDATOR
=============

Validates API endpoints via HTTP requests.

Philosophy: Real HTTP calls, real responses, real validation.

Author: E2E Validation Research
Date: April 12, 2026
"""

import json
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path
import subprocess
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from skills.validators.python_script_validator import ValidationResult


class APIValidator:
    """
    Validates API endpoints via HTTP requests.
    
    Philosophy: Real HTTP calls, real responses, real validation.
    
    This validator:
    - Makes real HTTP requests (GET, POST, PUT, DELETE, etc.)
    - Validates response status codes
    - Validates response structure and content
    - Measures performance and latency
    - Tests error handling
    
    NO mocking, NO stubbing, NO fake servers
    Only REAL HTTP requests produce TRUTH
    """
    
    def __init__(
        self,
        method: str = "GET",
        timeout: int = 10,
        headers: Optional[Dict[str, str]] = None,
        use_curl: bool = True
    ):
        """
        Initialize the API validator.
        
        Args:
            method: Default HTTP method
            timeout: Default timeout in seconds
            headers: Default headers to include
            use_curl: Use curl for requests (fallback to urllib)
        """
        self.default_method = method.upper()
        self.default_timeout = timeout
        self.default_headers = headers or {}
        self.use_curl = use_curl and self._check_curl()
    
    @staticmethod
    def _check_curl() -> bool:
        """Check if curl is available."""
        try:
            result = subprocess.run(
                ["curl", "--version"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def validate(
        self,
        target: Union[str, Dict[str, Any]],
        expectations: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Make HTTP requests and validate API endpoint.
        
        Args:
            target: URL or config dict with:
                - url: API endpoint URL
                - method: HTTP method (GET, POST, etc.)
                - body: Request body (for POST/PUT)
                - headers: Request headers
                - params: Query parameters
            expectations: Validation expectations
                - expect_status: Expected HTTP status (int or list)
                - expect_json_response: Response should be valid JSON
                - expect_field: JSON field that should exist
                - expect_field_value: JSON field with specific value
                - expect_in_response: Text that should be in response
                - expect_response_time_ms: Max response time
        
        Returns:
            ValidationResult with comprehensive results
        
        Example:
            >>> validator = APIValidator()
            >>> 
            >>> # Basic validation
            >>> result = validator.validate("https://api.example.com/health")
            >>> 
            >>> # With expectations
            >>> result = validator.validate(
            ...     "https://api.example.com/users/1",
            ...     expectations={"expect_status": 200, "expect_field": "name"}
            ... )
            >>> 
            >>> # POST request
            >>> result = validator.validate({
            ...     "url": "https://api.example.com/users",
            ...     "method": "POST",
            ...     "body": {"name": "John"}
            ... }, expectations={"expect_status": 201})
        """
        start_time = time.time()
        expectations = expectations or {}
        
        # Extract configuration
        if isinstance(target, dict):
            url = target.get("url", target.get("endpoint", ""))
            method = target.get("method", self.default_method)
            body = target.get("body")
            headers = {**self.default_headers, **target.get("headers", {})}
            params = target.get("params", {})
        else:
            url = str(target)
            method = self.default_method
            body = None
            headers = self.default_headers
            params = {}
        
        # Build query string
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{query_string}" if "?" not in url else f"{url}&{query_string}"
        
        # Make request
        validated_action = f"{method} {url}"
        
        if self.use_curl:
            result = self._make_request_curl(url, method, body, headers, expectations.get("timeout", self.default_timeout))
        else:
            result = self._make_request_python(url, method, body, headers, expectations.get("timeout", self.default_timeout))
        
        duration_ms = (time.time() - start_time) * 1000
        
        if result["error"]:
            return ValidationResult(
                passed=False,
                validator_type="api_endpoint",
                target=url,
                duration_ms=duration_ms,
                validated_action=validated_action,
                error_details=result["error"],
                suggestions=[
                    "Check if the server is running",
                    "Verify the URL is correct",
                    "Check network connectivity"
                ],
                evidence=result
            )
        
        # Validate response
        success_criteria_met = []
        success_criteria_failed = []
        suggestions = []
        evidence = result.copy()
        
        # Check status code
        expect_status = expectations.get("expect_status")
        if expect_status is not None:
            if isinstance(expect_status, list):
                status_ok = result["status_code"] in expect_status
            else:
                status_ok = result["status_code"] == expect_status
            
            if status_ok:
                success_criteria_met.append(f"HTTP {result['status_code']}")
            else:
                success_criteria_failed.append(f"HTTP {result['status_code']} (expected {expect_status})")
                suggestions.append(f"API returned unexpected status: {result['status_code']}")
                
                # Provide specific suggestions based on status
                if result["status_code"] == 404:
                    suggestions.append("Endpoint may not exist - check URL path")
                elif result["status_code"] == 401:
                    suggestions.append("Authentication required - check headers/API key")
                elif result["status_code"] == 403:
                    suggestions.append("Authorization failed - check permissions")
                elif result["status_code"] == 500:
                    suggestions.append("Server error - check API logs")
        else:
            # Any 2xx or 3xx status is OK
            if 200 <= result["status_code"] < 400:
                success_criteria_met.append(f"HTTP {result['status_code']}")
            else:
                success_criteria_failed.append(f"HTTP {result['status_code']}")
        
        # Check JSON response
        if expectations.get("expect_json_response"):
            if result.get("json") is not None:
                success_criteria_met.append("Valid JSON response")
                evidence["json_data"] = result["json"]
                
                # Check for expected fields
                if "expect_field" in expectations:
                    field = expectations["expect_field"]
                    if field in result["json"]:
                        success_criteria_met.append(f"Field exists: {field}")
                        evidence[f"field_{field}"] = result["json"][field]
                    else:
                        success_criteria_failed.append(f"Field missing: {field}")
                        suggestions.append(f"Response does not contain expected field: {field}")
                
                # Check for expected field value
                if "expect_field_value" in expectations:
                    field, value = expectations["expect_field_value"]
                    if field in result["json"]:
                        actual = result["json"][field]
                        if actual == value:
                            success_criteria_met.append(f"Field value: {field}={value}")
                        else:
                            success_criteria_failed.append(f"Field value mismatch: {field}={actual} (expected {value})")
                            suggestions.append(f"Field {field} has unexpected value")
            else:
                success_criteria_failed.append("Invalid JSON response")
                suggestions.append("Response is not valid JSON")
        
        # Check for text in response
        if "expect_in_response" in expectations:
            expected_text = expectations["expect_in_response"]
            response_text = result.get("text", "")
            if expected_text in response_text:
                success_criteria_met.append(f"Response contains: {expected_text[:50]}")
            else:
                success_criteria_failed.append(f"Response missing: {expected_text[:50]}")
        
        # Check response time
        if "expect_response_time_ms" in expectations:
            max_time = expectations["expect_response_time_ms"]
            if duration_ms <= max_time:
                success_criteria_met.append(f"Response time: {duration_ms:.0f}ms")
            else:
                success_criteria_failed.append(f"Response too slow: {duration_ms:.0f}ms > {max_time}ms")
                suggestions.append("API response is slower than expected")
        
        # Determine overall pass/fail
        passed = len(success_criteria_failed) == 0
        
        return ValidationResult(
            passed=passed,
            validator_type="api_endpoint",
            target=url,
            duration_ms=duration_ms,
            validated_action=validated_action,
            evidence=evidence,
            error_details=None if passed else "Some validation criteria failed",
            suggestions=suggestions,
            success_criteria_met=success_criteria_met,
            success_criteria_failed=success_criteria_failed
        )
    
    def _make_request_curl(
        self,
        url: str,
        method: str,
        body: Any,
        headers: Dict[str, str],
        timeout: int
    ) -> Dict[str, Any]:
        """Make HTTP request using curl."""
        cmd = ["curl", "-s", "-w", "\\n---HTTP_STATUS---%{http_code}", "-o", "-"]
        
        # Add method
        if method not in ["GET", "HEAD"]:
            cmd.extend(["-X", method])
        
        # Add headers
        for key, value in headers.items():
            cmd.extend(["-H", f"{key}: {value}"])
        
        # Add body
        if body:
            body_str = json.dumps(body) if isinstance(body, dict) else str(body)
            cmd.extend(["-d", body_str])
        
        # Add timeout
        cmd.extend(["--max-time", str(timeout)])
        
        # Add URL
        cmd.append(url)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=timeout + 1
            )
            
            output = result.stdout.decode()
            
            # Split response and status
            if "---HTTP_STATUS---" in output:
                response_body, status = output.split("---HTTP_STATUS---")
                status_code = int(status.strip())
            else:
                response_body = output
                status_code = 0
            
            # Parse response
            parsed = self._parse_response(response_body, status_code)
            return parsed
            
        except subprocess.TimeoutExpired:
            return {
                "error": f"Request timed out after {timeout} seconds",
                "status_code": None
            }
        except Exception as e:
            return {
                "error": f"Request failed: {e}",
                "status_code": None
            }
    
    def _make_request_python(
        self,
        url: str,
        method: str,
        body: Any,
        headers: Dict[str, str],
        timeout: int
    ) -> Dict[str, Any]:
        """Make HTTP request using Python urllib."""
        try:
            import urllib.request
            import urllib.parse
            
            # Prepare request
            if method == "GET" and body:
                # GET with body is unusual, convert to query params
                query = urllib.parse.urlencode(body if isinstance(body, dict) else {"data": body})
                url = f"{url}?{query}" if "?" not in url else f"{url}&{query}"
            
            data = None
            if body and method in ["POST", "PUT", "PATCH"]:
                body_str = json.dumps(body) if isinstance(body, dict) else str(body)
                data = body_str.encode()
            
            req = urllib.request.Request(url, data=data, method=method)
            
            # Add headers
            for key, value in headers.items():
                req.add_header(key, value)
            
            # Make request
            with urllib.request.urlopen(req, timeout=timeout) as response:
                response_body = response.read().decode()
                return self._parse_response(response_body, response.status)
                
        except urllib.error.HTTPError as e:
            return {
                "error": f"HTTP Error: {e.code}",
                "status_code": e.code,
                "text": e.read().decode() if hasattr(e, 'read') else ""
            }
        except urllib.error.URLError as e:
            return {
                "error": f"Connection failed: {e.reason}",
                "status_code": None
            }
        except Exception as e:
            return {
                "error": f"Request failed: {e}",
                "status_code": None
            }
    
    def _parse_response(self, response_body: str, status_code: int) -> Dict[str, Any]:
        """Parse HTTP response body."""
        result = {
            "status_code": status_code,
            "text": response_body,
            "body_length": len(response_body),
            "headers": {}
        }
        
        # Try to parse as JSON
        try:
            result["json"] = json.loads(response_body)
        except (json.JSONDecodeError, ValueError):
            pass
        
        return result
    
    def validate_endpoints(
        self,
        endpoints: List[Dict[str, Any]]
    ) -> ValidationResult:
        """
        Validate multiple API endpoints.
        
        Args:
            endpoints: List of endpoint configs, each with:
                - url: API endpoint URL
                - method: HTTP method
                - expectations: Validation expectations for this endpoint
        
        Returns:
            Aggregated ValidationResult
        
        Example:
            >>> validator = APIValidator()
            >>> result = validator.validate_endpoints([
            ...     {"url": "https://api.example.com/health", "expectations": {"expect_status": 200}},
            ...     {"url": "https://api.example.com/users", "expectations": {"expect_status": [200, 301]}}
            ... ])
        """
        start_time = time.time()
        
        all_results = []
        success_criteria_met = []
        success_criteria_failed = []
        evidence = {"endpoints": {}}
        suggestions = []
        
        for endpoint in endpoints:
            url = endpoint.get("url", "")
            expectations = endpoint.get("expectations", {})
            
            result = self.validate(url, expectations)
            all_results.append(result)
            
            # Store result
            evidence["endpoints"][url] = result.to_dict()
            
            if result.passed:
                success_criteria_met.append(f"OK: {url}")
            else:
                success_criteria_failed.append(f"FAIL: {url}")
                suggestions.extend(result.suggestions)
        
        duration_ms = (time.time() - start_time) * 1000
        passed = len(success_criteria_failed) == 0
        
        return ValidationResult(
            passed=passed,
            validator_type="api_multiple",
            target=f"{len(endpoints)} endpoints",
            duration_ms=duration_ms,
            validated_action=f"Validated {len(endpoints)} API endpoint(s)",
            evidence=evidence,
            error_details=None if passed else f"{len(success_criteria_failed)} endpoint(s) failed",
            suggestions=suggestions,
            success_criteria_met=success_criteria_met,
            success_criteria_failed=success_criteria_failed
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def validate_api(
    target: Union[str, Dict[str, Any]],
    **expectations
) -> ValidationResult:
    """
    Quick one-liner to validate an API endpoint.
    
    Example:
        >>> result = validate_api(
        ...     "https://api.example.com/health",
        ...     expect_status=200,
        ...     expect_json_response=True
        ... )
        >>> print(result.passed)
    """
    validator = APIValidator()
    return validator.validate(target, expectations)


def validate_apis(endpoints: List[Dict[str, Any]]) -> ValidationResult:
    """
    Validate multiple API endpoints.
    
    Example:
        >>> result = validate_apis([
        ...     {"url": "https://api.example.com/health", "expectations": {"expect_status": 200}},
        ...     {"url": "https://api.example.com/users", "expectations": {"expect_status": 200}}
        ... ])
        >>> print(f"Passed: {result.passed}")
    """
    validator = APIValidator()
    return validator.validate_endpoints(endpoints)
