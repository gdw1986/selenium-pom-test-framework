# pages/__init__.py
from .base_page import BasePage
from .login_page import LoginPage
from .main_page import MainPage
from .popup_window import PopupWindow

__all__ = ["BasePage", "LoginPage", "MainPage", "PopupWindow"]
