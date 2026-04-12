# -*- coding: utf-8 -*-
"""
Popup window - Page Object
Handles windows opened by openFiveWindows()
"""
import re
from .base_page import BasePage


class PopupWindow(BasePage):
    """Popup window page object using Playwright."""

    ALERT_BUTTON = "button[onclick*='alert']"
    CLOSE_BUTTON = "button[onclick='window.close()']"
    WINDOW_TITLE = "h2"
    WINDOW_INFO = ".info"

    def click_popup_alert_button(self):
        """Click Alert button inside popup."""
        self.click(self.ALERT_BUTTON)
        return self

    def click_close_button(self):
        """Click close button to close this window."""
        self.click(self.CLOSE_BUTTON)

    def get_window_title(self) -> str:
        """Get popup window title."""
        return self.get_text(self.WINDOW_TITLE)

    def get_window_info(self) -> str:
        """Get popup window info text."""
        return self.get_text(self.WINDOW_INFO)

    def get_window_number(self) -> int:
        """Extract window number from info text."""
        info = self.get_window_info()
        # Format: "窗口编号: X | 颜色: #XXXXXX"
        nums = re.findall(r'\d+', info)
        return int(nums[0]) if nums else 0

    def get_window_color(self) -> str:
        """Extract color from info text."""
        info = self.get_window_info()
        # Format: "窗口编号: X | 颜色: #XXXXXX"
        colors = re.findall(r'#[0-9a-fA-F]{6}', info)
        return colors[0] if colors else ""
