"""
WEB APP VALIDATOR
=================

Validates web applications using Playwright.

Philosophy: Real browser, real clicks, real validation.

Author: E2E Validation Research
Date: April 12, 2026
"""

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from skills.validators.python_script_validator import ValidationResult


class WebAppValidator:
    """
    Validates web applications using Playwright.
    
    Philosophy: Real browser, real clicks, real validation.
    
    This validator:
    - Launches a real browser (Chromium/Firefox/WebKit)
    - Navigates to the target URL
    - Validates page content and structure
    - Tests forms and navigation
    - Measures performance metrics
    - Takes screenshots on failure
    
    NO mocking, NO headless-only tests, NO API simulations
    Only REAL browsers produce TRUTH
    """
    
    def __init__(
        self,
        browser_type: str = "chromium",
        headless: bool = True,
        timeout: int = 30000,
        screenshots_dir: str = "evidence/screenshots"
    ):
        """
        Initialize the web app validator.
        
        Args:
            browser_type: Browser to use (chromium, firefox, webkit)
            headless: Run browser in headless mode
            timeout: Default timeout in milliseconds
            screenshots_dir: Directory to save screenshots
        """
        self.browser_type = browser_type
        self.headless = headless
        self.default_timeout = timeout
        self.screenshots_dir = Path(screenshots_dir)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        # Check Playwright availability
        self.playwright_available = self._check_playwright()
    
    def _check_playwright(self) -> bool:
        """Check if Playwright is available."""
        try:
            import playwright
            import playwright.async_api
            return True
        except ImportError:
            return False
    
    def validate(
        self,
        target: Union[str, Dict[str, Any]],
        expectations: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Launch browser and validate web app.
        
        Args:
            target: URL to validate or dict with config
            expectations: Validation expectations
                - expect_title: Expected page title (contains)
                - expect_text: Text that should be on page
                - expect_not_text: Text that should NOT be on page
                - expect_element: CSS selector that should exist
                - expect_clickable: CSS selector that should be clickable
                - wait_for_selector: Wait for specific selector
                - js_execute: JavaScript code to execute
                - screenshot: Take screenshot (default: True)
                - timeout: Override default timeout
        
        Returns:
            ValidationResult with comprehensive results
        
        Example:
            >>> validator = WebAppValidator()
            >>> 
            >>> # Basic validation
            >>> result = validator.validate("https://example.com")
            >>> 
            >>> # With expectations
            >>> result = validator.validate(
            ...     "https://example.com",
            ...     expectations={"expect_title": "Example"}
            ... )
            >>> 
            >>> # With element checks
            >>> result = validator.validate(
            ...     "https://example.com",
            ...     expectations={
            ...         "expect_element": "h1",
            ...         "expect_text": "Welcome"
            ...     }
            ... )
        """
        start_time = time.time()
        expectations = expectations or {}
        
        # Extract URL
        if isinstance(target, dict):
            url = target.get("url", target.get("target", ""))
        else:
            url = str(target)
        
        # Check Playwright
        if not self.playwright_available:
            return ValidationResult(
                passed=False,
                validator_type="web_app",
                target=url,
                duration_ms=0,
                validated_action="Browser check",
                error_details="Playwright not installed",
                suggestions=[
                    "Install Playwright: pip install playwright",
                    "Install browsers: playwright install chromium",
                    "Or use: playwright install --with-deps"
                ]
            )
        
        # Run async validation
        try:
            result = asyncio.run(self._validate_async(url, expectations))
            return result
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            return ValidationResult(
                passed=False,
                validator_type="web_app",
                target=url,
                duration_ms=duration_ms,
                validated_action="Browser launch failed",
                error_details=f"Browser error: {e}",
                suggestions=[
                    "Check browser installation",
                    "Try running: playwright install chromium",
                    "Verify URL is accessible"
                ]
            )
    
    async def _validate_async(
        self,
        url: str,
        expectations: Dict[str, Any]
    ) -> ValidationResult:
        """Async validation using Playwright."""
        from playwright.async_api import async_playwright, Browser, Page
        
        start_time = time.time()
        timeout = expectations.get("timeout", self.default_timeout)
        
        success_criteria_met = []
        success_criteria_failed = []
        suggestions = []
        evidence = {}
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p[self.browser_type].launch(
                headless=self.headless
            )
            
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720}
            )
            page = await context.new_page()
            
            try:
                # Navigate to URL
                response = await page.goto(
                    url,
                    timeout=timeout,
                    wait_until="domcontentloaded"
                )
                
                evidence["http_status"] = response.status if response else "unknown"
                
                # Check HTTP status
                if response and response.status >= 400:
                    success_criteria_failed.append(f"HTTP {response.status}")
                    suggestions.extend([
                        f"Server returned error status: {response.status}",
                        "Check if the server is running",
                        "Verify the URL is correct"
                    ])
                elif response:
                    success_criteria_met.append(f"HTTP {response.status}")
                
                # Wait for page to stabilize
                await page.wait_for_load_state("networkidle", timeout=5000)
                
                # Get page info
                title = await page.title()
                url_final = page.url
                content = await page.content()
                
                evidence.update({
                    "title": title,
                    "final_url": url_final,
                    "content_length": len(content),
                    "redirected": url != url_final
                })
                
                # Validate title
                if "expect_title" in expectations:
                    expected_title = expectations["expect_title"]
                    if expected_title.lower() in title.lower():
                        success_criteria_met.append(f"Title contains: {expected_title}")
                    else:
                        success_criteria_failed.append(f"Title missing: {expected_title}")
                        suggestions.append(f"Expected title to contain: {expected_title}")
                
                # Validate text content
                if "expect_text" in expectations:
                    expected_text = expectations["expect_text"]
                    page_text = await page.inner_text("body")
                    if expected_text in page_text:
                        success_criteria_met.append(f"Text found: {expected_text[:50]}")
                    else:
                        success_criteria_failed.append(f"Text not found: {expected_text[:50]}")
                        suggestions.append("Expected text not found on page")
                
                if "expect_not_text" in expectations:
                    unexpected_text = expectations["expect_not_text"]
                    page_text = await page.inner_text("body")
                    if unexpected_text not in page_text:
                        success_criteria_met.append(f"Text absent: {unexpected_text[:50]}")
                    else:
                        success_criteria_failed.append(f"Unexpected text present: {unexpected_text[:50]}")
                
                # Validate elements
                if "expect_element" in expectations:
                    selector = expectations["expect_element"]
                    try:
                        element = await page.wait_for_selector(
                            selector,
                            timeout=5000
                        )
                        if element:
                            success_criteria_met.append(f"Element exists: {selector}")
                            evidence[f"element_{selector}"] = True
                        else:
                            success_criteria_failed.append(f"Element missing: {selector}")
                            suggestions.append(f"Expected element not found: {selector}")
                    except:
                        success_criteria_failed.append(f"Element not found: {selector}")
                        suggestions.append(f"Selector didn't match any element: {selector}")
                
                # Check clickable elements
                if "expect_clickable" in expectations:
                    selector = expectations["expect_clickable"]
                    try:
                        element = await page.wait_for_selector(
                            selector,
                            timeout=5000
                        )
                        if element:
                            is_visible = await element.is_visible()
                            is_enabled = await element.is_enabled()
                            if is_visible and is_enabled:
                                success_criteria_met.append(f"Clickable: {selector}")
                                evidence[f"clickable_{selector}"] = True
                            else:
                                success_criteria_failed.append(f"Not clickable: {selector}")
                                suggestions.append(f"Element exists but not interactive: {selector}")
                        else:
                            success_criteria_failed.append(f"Element not found: {selector}")
                    except:
                        success_criteria_failed.append(f"Click check failed: {selector}")
                
                # Execute custom JavaScript
                if "js_execute" in expectations:
                    js_code = expectations["js_execute"]
                    try:
                        js_result = await page.evaluate(js_code)
                        evidence["js_result"] = js_result
                        success_criteria_met.append("JavaScript executed")
                    except Exception as e:
                        success_criteria_failed.append(f"JavaScript error: {e}")
                
                # Take screenshot
                if expectations.get("screenshot", True):
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    safe_url = "".join(c for c in url if c.isalnum() or c in ('_', '-'))[:50]
                    screenshot_path = self.screenshots_dir / f"{timestamp}_{safe_url}.png"
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    evidence["screenshot"] = str(screenshot_path)
                    success_criteria_met.append("Screenshot captured")
                
                # Performance metrics
                metrics = await page.evaluate("""() => {
                    const perfData = performance.timing;
                    return {
                        dom_content_loaded: perfData.domContentLoadedEventEnd - perfData.navigationStart,
                        page_load: perfData.loadEventEnd - perfData.navigationStart,
                        first_paint: performance.getEntriesByType('paint')[0]?.startTime || 0
                    };
                }""")
                
                evidence["performance"] = metrics
                
                # Close browser
                await context.close()
                await browser.close()
                
            except Exception as e:
                await context.close()
                await browser.close()
                
                duration_ms = (time.time() - start_time) * 1000
                
                # Try to take error screenshot
                try:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    error_screenshot = self.screenshots_dir / f"{timestamp}_error.png"
                    await page.screenshot(path=str(error_screenshot))
                    evidence["error_screenshot"] = str(error_screenshot)
                except:
                    pass
                
                return ValidationResult(
                    passed=False,
                    validator_type="web_app",
                    target=url,
                    duration_ms=duration_ms,
                    validated_action=f"Navigated to: {url}",
                    error_details=f"Browser error: {e}",
                    suggestions=[
                        "Check if the URL is accessible",
                        "Verify network connectivity",
                        "Try increasing timeout"
                    ],
                    evidence=evidence
                )
        
        duration_ms = (time.time() - start_time) * 1000
        
        # Determine overall pass/fail
        passed = len(success_criteria_failed) == 0
        
        return ValidationResult(
            passed=passed,
            validator_type="web_app",
            target=url,
            duration_ms=duration_ms,
            validated_action=f"Browser navigation to: {url}",
            evidence=evidence,
            error_details=None if passed else "Some validation criteria failed",
            suggestions=suggestions,
            success_criteria_met=success_criteria_met,
            success_criteria_failed=success_criteria_failed
        )
    
    def validate_multi_page(
        self,
        flows: List[Dict[str, Any]],
        expectations: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Validate multi-page user flows.
        
        Args:
            flows: List of page navigation steps
                Each step:
                - url: Starting URL or "continue" for subsequent
                - click: CSS selector to click
                - fill: Dict of {selector: value} to fill
                - wait: Selector to wait for
                - expect_text: Text to validate
            expectations: Overall expectations
        
        Example:
            >>> validator = WebAppValidator()
            >>> result = validator.validate_multi_page([
            ...     {
            ...         "url": "https://example.com/login",
            ...         "fill": {"#username": "user", "#password": "pass"},
            ...         "click": "#login-button",
            ...         "wait": "#dashboard"
            ...     },
            ...     {
            ...         "url": "continue",
            ...         "expect_text": "Welcome"
            ...     }
            ... ])
        """
        if not self.playwright_available:
            return ValidationResult(
                passed=False,
                validator_type="web_app",
                target="multi_page_flow",
                duration_ms=0,
                validated_action="Multi-page flow",
                error_details="Playwright not installed"
            )
        
        # Run async multi-page validation
        try:
            result = asyncio.run(self._validate_multi_page_async(flows, expectations))
            return result
        except Exception as e:
            return ValidationResult(
                passed=False,
                validator_type="web_app",
                target="multi_page_flow",
                duration_ms=0,
                validated_action="Multi-page flow",
                error_details=f"Flow error: {e}"
            )
    
    async def _validate_multi_page_async(
        self,
        flows: List[Dict[str, Any]],
        expectations: Optional[Dict[str, Any]]
    ) -> ValidationResult:
        """Async multi-page validation."""
        from playwright.async_api import async_playwright
        
        start_time = time.time()
        success_criteria_met = []
        success_criteria_failed = []
        evidence = {"steps": []}
        
        async with async_playwright() as p:
            browser = await p[self.browser_type].launch(headless=self.headless)
            context = await browser.new_context(viewport={"width": 1280, "height": 720})
            page = await context.new_page()
            
            for i, step in enumerate(flows, 1):
                step_result = {"step": i, "actions": []}
                
                # Navigate
                url = step.get("url", "")
                if url != "continue":
                    await page.goto(url, timeout=self.default_timeout)
                    step_result["actions"].append(f"Navigated to {url}")
                
                # Fill forms
                if "fill" in step:
                    for selector, value in step["fill"].items():
                        await page.fill(selector, value)
                        step_result["actions"].append(f"Filled {selector}")
                
                # Click
                if "click" in step:
                    await page.click(step["click"])
                    step_result["actions"].append(f"Clicked {step['click']}")
                
                # Wait
                if "wait" in step:
                    await page.wait_for_selector(step["wait"])
                    step_result["actions"].append(f"Waited for {step['wait']}")
                
                # Validate
                if "expect_text" in step:
                    content = await page.inner_text("body")
                    if step["expect_text"] in content:
                        step_result["validated"] = True
                        success_criteria_met.append(f"Step {i}: Text found")
                    else:
                        step_result["validated"] = False
                        success_criteria_failed.append(f"Step {i}: Text not found")
                
                evidence["steps"].append(step_result)
            
            await context.close()
            await browser.close()
        
        duration_ms = (time.time() - start_time) * 1000
        passed = len(success_criteria_failed) == 0
        
        return ValidationResult(
            passed=passed,
            validator_type="web_app_multi_page",
            target="multi_page_flow",
            duration_ms=duration_ms,
            validated_action=f"Completed {len(flows)} steps",
            evidence=evidence,
            success_criteria_met=success_criteria_met,
            success_criteria_failed=success_criteria_failed
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def validate_web_app(
    target: Union[str, Dict[str, Any]],
    **expectations
) -> ValidationResult:
    """
    Quick one-liner to validate a web app.
    
    Example:
        >>> result = validate_web_app(
        ...     "https://example.com",
        ...     expect_title="Example",
        ...     expect_element="h1"
        ... )
        >>> print(result.passed)
    """
    validator = WebAppValidator()
    return validator.validate(target, expectations)
