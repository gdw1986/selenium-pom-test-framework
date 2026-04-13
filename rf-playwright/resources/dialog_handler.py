# dialog_handler.py - Custom Robot Framework library for handling browser dialogs
# Uses Playwright Python API directly to avoid Browser library dialog bugs

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class DialogHandler:
    """Custom keyword library for handling browser dialogs in Robot Framework.
    
    Works around robotframework-browser's dialog handling bugs by using
    Playwright's Python API directly via the Browser library's Playwright instance.
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self._dialog_message = ""
        self._dialog_type = ""

    def setup_dialog_listener(self):
        """Register a dialog event listener on the current page.
        
        Must be called BEFORE the action that triggers the dialog.
        The dialog will be automatically accepted.
        """
        self._dialog_message = ""
        self._dialog_type = ""
        browser_lib = BuiltIn().get_library_instance("Browser")
        page = browser_lib.get_playwright_page()
        
        def on_dialog(dialog):
            self._dialog_message = dialog.message
            self._dialog_type = dialog.type
            logger.info(f"Dialog detected: type={dialog.type}, message={dialog.message}")
            dialog.accept()
        
        page.on("dialog", on_dialog)

    def setup_dialog_listener_dismiss(self):
        """Register a dialog event listener that dismisses the dialog.
        
        Must be called BEFORE the action that triggers the dialog.
        """
        self._dialog_message = ""
        self._dialog_type = ""
        browser_lib = BuiltIn().get_library_instance("Browser")
        page = browser_lib.get_playwright_page()
        
        def on_dialog(dialog):
            self._dialog_message = dialog.message
            self._dialog_type = dialog.type
            logger.info(f"Dialog detected: type={dialog.type}, message={dialog.message}")
            dialog.dismiss()
        
        page.on("dialog", on_dialog)

    def get_dialog_message(self):
        """Return the message text from the last dialog that was handled."""
        return self._dialog_message

    def get_dialog_type(self):
        """Return the type of the last dialog (alert, confirm, prompt, beforeunload)."""
        return self._dialog_type

    def dialog_message_should_contain(self, expected):
        """Verify that the last dialog message contains the expected text."""
        if expected not in self._dialog_message:
            raise AssertionError(
                f"Dialog message '{self._dialog_message}' does not contain '{expected}'"
            )

    def dialog_message_should_not_be_empty(self):
        """Verify that the last dialog message is not empty."""
        if not self._dialog_message:
            raise AssertionError("Dialog message is empty")
