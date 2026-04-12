# -*- coding: utf-8 -*-
"""
Login page - Page Object
"""
from .base_page import BasePage
from config.settings import TEST_URL, LOGIN_USERNAME, LOGIN_PASSWORD


class LoginPage(BasePage):
    """Login page object using Playwright."""

    URL = TEST_URL
    DEFAULT_USERNAME = LOGIN_USERNAME
    DEFAULT_PASSWORD = LOGIN_PASSWORD

    # Selectors
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = ".login-btn"
    ERROR_MESSAGE = "#login-error"
    LOGIN_PAGE_CONTAINER = "#login-page"
    MAIN_PAGE_CONTAINER = "#main-page"
    LOGIN_TOAST = "#login-toast"

    def __init__(self, page):
        super().__init__(page, self.URL)

    def open_login_page(self):
        """Open the login page."""
        self.open()
        return self

    def is_on_login_page(self) -> bool:
        """Check if currently on login page."""
        return (
            self.is_element_visible(self.LOGIN_PAGE_CONTAINER)
            and self.is_element_attached(self.USERNAME_INPUT)
        )

    def enter_username(self, username: str):
        """Enter username."""
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        """Enter password."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login_button(self):
        """Click login button."""
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        """
        Full login flow.
        Returns MainPage instance.
        """
        from .main_page import MainPage
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        # Wait for main page to appear
        self.wait_for_selector_visible(MainPage.MAIN_PAGE_CONTAINER, timeout=5)
        return MainPage(self.page)

    def get_error_message(self) -> str:
        """Get error message text."""
        return self.get_text(self.ERROR_MESSAGE)

    def has_error(self) -> bool:
        """Check if error message is shown."""
        text = self.get_error_message()
        return bool(text and text.strip())

    def is_username_error_highlighted(self) -> bool:
        """Check if username input has error class."""
        el = self.page.locator(self.USERNAME_INPUT).first
        cls = el.get_attribute("class") or ""
        return "error" in cls

    def is_password_error_highlighted(self) -> bool:
        """Check if password input has error class."""
        el = self.page.locator(self.PASSWORD_INPUT).first
        cls = el.get_attribute("class") or ""
        return "error" in cls

    def press_enter_to_login(self):
        """Press Enter in password field to submit."""
        self.page.locator(self.PASSWORD_INPUT).first.press("Enter")
        return self

    def is_login_successful(self) -> bool:
        """Check if login succeeded (main page visible)."""
        from .main_page import MainPage
        return self.is_element_visible(MainPage.MAIN_PAGE_CONTAINER, timeout=3)

    def clear_inputs(self):
        """Clear both input fields."""
        self.page.locator(self.USERNAME_INPUT).first.clear()
        self.page.locator(self.PASSWORD_INPUT).first.clear()
        return self
