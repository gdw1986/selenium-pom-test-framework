# -*- coding: utf-8 -*-
"""
Main page - Page Object
All functional elements on the main page.
"""
import os
from .base_page import BasePage


class MainPage(BasePage):
    """Main page object using Playwright."""

    # Container
    MAIN_PAGE_CONTAINER = "#main-page"

    # Alert section
    ALERT_BUTTON = "button[onclick='showAlert()']"
    ALERT_BUTTON_TOOLTIP = "button[onclick='showAlert()'] .tooltip"

    # Multi-window section
    OPEN_WINDOWS_BUTTON = "button.btn-orange[onclick='openFiveWindows()']"
    OPEN_WINDOWS_TOOLTIP = "button.btn-orange .tooltip"

    # Fruit dropdown
    FRUIT_SELECT = "#fruit-select"
    FRUIT_SELECT_RESULT = "#select-result"

    # City dropdown
    CITY_SELECT = "#city-select"
    CITY_SELECT_RESULT = "#city-result"

    # File upload
    FILE_INPUT = "#file-input"
    UPLOAD_DROP_ZONE = "#upload-drop-zone"
    UPLOAD_FILE_INFO = "#upload-file-info"
    UPLOAD_FILE_NAME = "#upload-file-name"
    UPLOAD_FILE_META = "#upload-file-meta"
    UPLOAD_FILE_FULLPATH = "#upload-file-fullpath"
    UPLOAD_CLEAR_BUTTON = ".upload-clear-btn"

    # Comment section
    COMMENT_INPUT = "#comment-input"
    COMMENT_SUBMIT_BUTTON = ".comment-submit-btn"
    COMMENT_LIST = "#comment-list"
    COMMENT_ITEMS = ".comment-item"
    COMMENT_TOAST = "#comment-toast"

    def __init__(self, page):
        super().__init__(page)

    def is_on_main_page(self) -> bool:
        """Check if on main page."""
        return self.is_element_visible(self.MAIN_PAGE_CONTAINER)

    # ==================== Alert ====================

    def click_alert_button(self):
        """Click the Alert button."""
        self.click(self.ALERT_BUTTON)
        return self

    def get_alert_button_tooltip_text(self) -> str:
        """Hover button and get tooltip text."""
        self.hover(self.ALERT_BUTTON)
        self.page.wait_for_timeout(300)  # small wait for tooltip to appear
        return self.get_text(self.ALERT_BUTTON_TOOLTIP)

    # ==================== Multi-Window ====================

    def click_open_windows_button(self):
        """Click button to open 5 new windows."""
        self.click(self.OPEN_WINDOWS_BUTTON)
        return self

    def get_open_windows_tooltip_text(self) -> str:
        """Hover button and get tooltip text."""
        self.hover(self.OPEN_WINDOWS_BUTTON)
        self.page.wait_for_timeout(300)
        return self.get_text(self.OPEN_WINDOWS_TOOLTIP)

    def open_five_windows(self) -> list:
        """
        Click button to open 5 new windows.
        Returns list of page objects sorted by window number 1-5.
        """
        ctx = self.page.context
        initial_pages = set(ctx.pages)
        self.click_open_windows_button()

        # Wait for 5 new pages to appear
        self.page.wait_for_function(
            "() => document.querySelectorAll ? true : false"
        )
        # Wait until we have 5 new pages
        for _ in range(20):
            if len(ctx.pages) >= len(initial_pages) + 5:
                break
            self.page.wait_for_timeout(200)

        new_pages = [p for p in ctx.pages if p not in initial_pages]

        # Read title from each new page to sort by window number
        handle_order = []
        for p in new_pages:
            try:
                title_el = p.locator("h2").first
                title_el.wait_for(timeout=3000)
                title = title_el.text_content() or ""
                # Extract number: "窗口 3" -> 3
                import re
                nums = re.findall(r'\d+', title)
                num = int(nums[0]) if nums else 0
            except Exception:
                num = 0
            handle_order.append((num, p))

        handle_order.sort(key=lambda x: x[0])
        return [p for _, p in handle_order]

    def close_all_popup_windows(self, main_page):
        """Close all popup windows, switch back to main_page."""
        ctx = self.page.context
        for p in ctx.pages:
            if p != main_page:
                p.close()
        return main_page

    # ==================== Dropdown - Fruit ====================

    def select_fruit_by_value(self, value: str):
        """Select fruit by option value."""
        self.page.select_option(self.FRUIT_SELECT, value)
        return self

    def select_fruit_by_text(self, text: str):
        """Select fruit by visible text."""
        self.page.select_option(self.FRUIT_SELECT, label=text)
        return self

    def select_fruit_by_index(self, index: int):
        """Select fruit by index (0-based, 0 = first option)."""
        opts = self.page.locator(f"{self.FRUIT_SELECT} option").all()
        if 0 <= index < len(opts):
            value = opts[index].get_attribute("value")
            self.page.select_option(self.FRUIT_SELECT, value=value)
        return self

    def get_selected_fruit_text(self) -> str:
        """Get selected fruit result text."""
        return self.get_text(self.FRUIT_SELECT_RESULT)

    def get_fruit_options(self) -> list:
        """Get all fruit options as (value, text) tuples."""
        opts = self.page.locator(f"{self.FRUIT_SELECT} option").all()
        return [(o.get_attribute("value") or "", o.text_content() or "") for o in opts]

    # ==================== Dropdown - City (dynamic) ====================

    def wait_for_city_options_loaded(self, timeout: int = 5):
        """Wait for city options to load (async, 1.5s delay in page)."""
        timeout_ms = timeout * 1000
        # Wait until more than 1 option exists
        self.page.wait_for_function(
            """() => {
                const opts = document.querySelectorAll('#city-select option');
                return opts.length > 1;
            }""",
            timeout=timeout_ms
        )
        return self

    def select_city_by_value(self, value: str):
        """Select city by option value."""
        self.wait_for_city_options_loaded()
        self.page.select_option(self.CITY_SELECT, value)
        return self

    def select_city_by_text(self, text: str):
        """Select city by visible text."""
        self.wait_for_city_options_loaded()
        self.page.select_option(self.CITY_SELECT, label=text)
        return self

    def get_selected_city_text(self) -> str:
        """Get selected city result text."""
        return self.get_text(self.CITY_SELECT_RESULT)

    def get_city_options(self) -> list:
        """Get all city options as (value, text) tuples."""
        self.wait_for_city_options_loaded()
        opts = self.page.locator(f"{self.CITY_SELECT} option").all()
        return [(o.get_attribute("value") or "", o.text_content() or "") for o in opts]

    # ==================== File Upload ====================

    def upload_file(self, file_path: str):
        """Upload file via file input."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        self.page.set_input_files(self.FILE_INPUT, file_path)
        return self

    def is_file_uploaded(self) -> bool:
        """Check if file info section is visible."""
        el = self.page.locator(self.UPLOAD_FILE_INFO).first
        cls = el.get_attribute("class") or ""
        return "visible" in cls

    def get_uploaded_file_name(self) -> str:
        """Get uploaded file name."""
        return self.get_text(self.UPLOAD_FILE_NAME)

    def get_uploaded_file_meta(self) -> str:
        """Get uploaded file meta (size and type)."""
        return self.get_text(self.UPLOAD_FILE_META)

    def get_uploaded_file_fullpath(self) -> str:
        """Get uploaded file full path (fakepath)."""
        return self.get_text(self.UPLOAD_FILE_FULLPATH)

    def clear_uploaded_file(self):
        """Clear uploaded file."""
        self.click(self.UPLOAD_CLEAR_BUTTON)
        return self

    # ==================== Comments ====================

    def enter_comment(self, text: str):
        """Type comment text."""
        self.type_text(self.COMMENT_INPUT, text)
        return self

    def submit_comment(self):
        """Click submit button."""
        self.click(self.COMMENT_SUBMIT_BUTTON)
        return self

    def add_comment(self, text: str):
        """
        Full add-comment flow.
        Waits for comment to appear in list.
        """
        self.enter_comment(text)
        self.submit_comment()
        # Wait for button text to return to normal (indicating completion)
        self.page.wait_for_function(
            """() => {
                const btn = document.querySelector('.comment-submit-btn');
                return btn && btn.textContent.includes('发布评论');
            }""",
            timeout=5000
        )
        return self

    def get_all_comments(self) -> list:
        """Get all comment item elements."""
        return self.find_elements(self.COMMENT_ITEMS)

    def get_comments_count(self) -> int:
        """Get number of comments."""
        return len(self.get_all_comments())

    def get_first_comment_text(self) -> str:
        """Get text of first comment."""
        items = self.get_all_comments()
        if items:
            return (items[0].locator(".comment-content").first.text_content() or "")
        return ""

    def get_first_comment_author(self) -> str:
        """Get author of first comment."""
        items = self.get_all_comments()
        if items:
            return (items[0].locator(".comment-author").first.text_content() or "")
        return ""

    def get_all_comment_texts(self) -> list:
        """Get all comment texts in display order."""
        items = self.get_all_comments()
        texts = []
        for item in items:
            try:
                txt = item.locator(".comment-content").first.text_content()
                if txt:
                    texts.append(txt)
            except Exception:
                pass
        return texts

    def is_comment_toast_visible(self) -> bool:
        """Check if comment toast notification is visible."""
        el = self.page.locator(self.COMMENT_TOAST).first
        cls = el.get_attribute("class") or ""
        return "show" in cls
