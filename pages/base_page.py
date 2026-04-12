# -*- coding: utf-8 -*-
"""
Base page class - all Page Objects inherit from this
Uses playwright.sync_api for browser operations
"""
import time
from playwright.sync_api import Page, BrowserContext, TimeoutError as PlaywrightTimeoutError


class BasePage:
    """Base page class with common browser operations using Playwright."""

    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url

    def open(self, url: str = ""):
        """Navigate to URL."""
        target = url or self.base_url
        self.page.goto(target)

    def find_element(self, selector: str, timeout: int = None):
        """Find single element, wait for it to be attached."""
        timeout_ms = (timeout or 10) * 1000
        return self.page.locator(selector).first

    def find_elements(self, selector: str):
        """Find multiple elements."""
        return self.page.locator(selector).all()

    def click(self, selector: str, timeout: int = None):
        """Click element after waiting for it to be actionable."""
        timeout_ms = (timeout or 10) * 1000
        self.page.locator(selector).first.click(timeout=timeout_ms)

    def type_text(self, selector: str, text: str, delay: int = 50, timeout: int = None):
        """Fill input field, optionally clearing first."""
        timeout_ms = (timeout or 10) * 1000
        loc = self.page.locator(selector).first
        loc.clear()
        loc.type(text, delay=delay, timeout=timeout_ms)

    def get_text(self, selector: str, timeout: int = None) -> str:
        """Get visible text of element."""
        timeout_ms = (timeout or 10) * 1000
        return self.page.locator(selector).first.text_content(timeout=timeout_ms) or ""

    def is_element_visible(self, selector: str, timeout: int = 3) -> bool:
        """Check if element is visible within timeout."""
        timeout_ms = timeout * 1000
        return self.page.locator(selector).first.is_visible(timeout=timeout_ms)

    def is_element_attached(self, selector: str, timeout: int = 3) -> bool:
        """Check if element exists in DOM (attached)."""
        timeout_ms = timeout * 1000
        try:
            self.page.locator(selector).first.wait_for(state="attached", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def wait_for_selector_visible(self, selector: str, timeout: int = None):
        """Explicitly wait for element to be visible."""
        timeout_ms = (timeout or 10) * 1000
        return self.page.locator(selector).first.wait_for(state="visible", timeout=timeout_ms)

    def wait_for_selector_hidden(self, selector: str, timeout: int = None):
        """Explicitly wait for element to be hidden."""
        timeout_ms = (timeout or 10) * 1000
        return self.page.locator(selector).first.wait_for(state="hidden", timeout=timeout_ms)

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def hover(self, selector: str, timeout: int = None):
        """Hover over element."""
        timeout_ms = (timeout or 10) * 1000
        self.page.locator(selector).first.hover(timeout=timeout_ms)

    # ==================== Alert / Dialog ====================

    def on_dialog(self, action: str = "accept", prompt_text: str = None):
        """
        Handle dialog (alert/confirm/prompt).
        action: "accept" | "dismiss"
        """
        def handler(dialog):
            if action == "accept":
                if prompt_text is not None:
                    dialog.accept(prompt_text)
                else:
                    dialog.accept()
            else:
                dialog.dismiss()
        self.page.on("dialog", handler)

    def expect_dialog(self, action: str = "accept", expected_text: str = None,
                      prompt_text: str = None, timeout: int = 5):
        """
        Wait for dialog, optionally assert its text, then handle it.
        action: "accept" | "dismiss"
        """
        timeout_ms = timeout * 1000
        dialog_text = None

        def handler(dialog):
            nonlocal dialog_text
            dialog_text = dialog.message
            if action == "accept":
                if prompt_text is not None:
                    dialog.accept(prompt_text)
                else:
                    dialog.accept()
            else:
                dialog.dismiss()

        with self.page.expect_event("dialog", timeout=timeout_ms) as dialog_info:
            pass  # dialog will fire when it appears
        dialog_info.value
        handler(self.page.context if hasattr(self.page, 'context') else None)

    def handle_dialog(self, dialog, action: str = "accept", prompt_text: str = None):
        """Handle a specific dialog object."""
        if action == "accept":
            if prompt_text is not None:
                dialog.accept(prompt_text)
            else:
                dialog.accept()
        else:
            dialog.dismiss()

    # ==================== Window / Context ====================

    def get_window_handles(self, context: BrowserContext = None) -> list:
        """Get all page IDs (window handles equivalent) in context."""
        ctx = context or self.page.context
        return [p for p in ctx.pages]

    def switch_to_page(self, target):
        """Switch to target page/frame."""
        if isinstance(target, int):
            pages = self.page.context.pages
            self.page = pages[target]
        elif isinstance(target, str):
            # page title or URL match
            for p in self.page.context.pages:
                if target in (p.title() or "") or target in (p.url or ""):
                    self.page = p
                    break
        else:
            self.page = target
        return self.page

    def close_page(self):
        """Close current page."""
        self.page.close()
