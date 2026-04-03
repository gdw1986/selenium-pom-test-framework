"""
登录页面 - Page Object
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage
from config.settings import TEST_URL, LOGIN_USERNAME, LOGIN_PASSWORD


class LoginPage(BasePage):
    """登录页面Page Object"""
    
    # URL
    URL = TEST_URL
    
    # 默认登录凭据
    DEFAULT_USERNAME = LOGIN_USERNAME
    DEFAULT_PASSWORD = LOGIN_PASSWORD
    
    # 定位器
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-btn")
    ERROR_MESSAGE = (By.ID, "login-error")
    LOGIN_PAGE_CONTAINER = (By.ID, "login-page")
    MAIN_PAGE_CONTAINER = (By.ID, "main-page")
    LOGIN_TOAST = (By.ID, "login-toast")
    
    def __init__(self, driver):
        super().__init__(driver, self.URL)
    
    def open_login_page(self):
        """打开登录页面"""
        self.open()
        return self
    
    def is_on_login_page(self) -> bool:
        """判断是否处于登录页面"""
        return self.is_element_visible(self.LOGIN_PAGE_CONTAINER) and \
               self.is_element_present(self.USERNAME_INPUT)
    
    def enter_username(self, username: str):
        """输入用户名"""
        self.send_keys(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password: str):
        """输入密码"""
        self.send_keys(self.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self):
        """点击登录按钮"""
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username: str, password: str):
        """
        执行完整登录流程
        返回MainPage对象
        """
        from .main_page import MainPage
        
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
        # 等待主页面加载
        self.wait_for_element_visible(MainPage.MAIN_PAGE_CONTAINER, timeout=3)
        return MainPage(self.driver)
    
    def get_error_message(self) -> str:
        """获取错误提示信息"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def has_error(self) -> bool:
        """判断是否有错误提示"""
        error_text = self.get_error_message()
        return bool(error_text and error_text.strip())
    
    def is_username_error_highlighted(self) -> bool:
        """判断用户名输入框是否有错误高亮"""
        username_input = self.find_element(self.USERNAME_INPUT)
        return "error" in username_input.get_attribute("class")
    
    def is_password_error_highlighted(self) -> bool:
        """判断密码输入框是否有错误高亮"""
        password_input = self.find_element(self.PASSWORD_INPUT)
        return "error" in password_input.get_attribute("class")
    
    def press_enter_to_login(self):
        """在密码框按回车登录"""
        password_input = self.find_element(self.PASSWORD_INPUT)
        password_input.send_keys("\n")
        return self
    
    def is_login_successful(self) -> bool:
        """判断登录是否成功（主页面是否显示）"""
        from .main_page import MainPage
        return self.is_element_visible(MainPage.MAIN_PAGE_CONTAINER, timeout=3)
    
    def clear_inputs(self):
        """清空所有输入框"""
        self.find_element(self.USERNAME_INPUT).clear()
        self.find_element(self.PASSWORD_INPUT).clear()
        return self
