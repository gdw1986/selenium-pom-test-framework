"""
基础页面类 - 所有Page Object的基类
封装通用方法和元素定位策略
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """基础页面类，提供通用的页面操作方法"""
    
    def __init__(self, driver: WebDriver, base_url: str = ""):
        self.driver = driver
        self.base_url = base_url
        self.default_timeout = 10
    
    def open(self, url: str = ""):
        """打开页面"""
        target_url = url or self.base_url
        self.driver.get(target_url)
    
    def find_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        查找单个元素，使用显式等待
        locator: (By.XXX, "value") 元组
        """
        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"元素未找到: {locator}")
    
    def find_elements(self, locator: tuple, timeout: int = None) -> list:
        """查找多个元素"""
        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []
    
    def wait_for_element_visible(self, locator: tuple, timeout: int = None) -> WebElement:
        """等待元素可见"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_clickable(self, locator: tuple, timeout: int = None) -> WebElement:
        """等待元素可点击"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def wait_for_element_invisible(self, locator: tuple, timeout: int = None):
        """等待元素不可见"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    
    def click(self, locator: tuple, timeout: int = None):
        """点击元素"""
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
    
    def send_keys(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = None):
        """输入文本"""
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """获取元素文本"""
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def is_element_present(self, locator: tuple, timeout: int = 3) -> bool:
        """判断元素是否存在"""
        try:
            self.find_element(locator, timeout)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: tuple, timeout: int = 3) -> bool:
        """判断元素是否可见"""
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def get_current_url(self) -> str:
        """获取当前URL"""
        return self.driver.current_url
    
    def get_title(self) -> str:
        """获取页面标题"""
        return self.driver.title
    
    def switch_to_alert(self, timeout: int = 5):
        """切换到alert弹窗"""
        return WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
    
    def accept_alert(self, timeout: int = 5):
        """接受alert"""
        alert = self.switch_to_alert(timeout)
        alert.accept()
    
    def dismiss_alert(self, timeout: int = 5):
        """取消alert"""
        alert = self.switch_to_alert(timeout)
        alert.dismiss()
    
    def get_alert_text(self, timeout: int = 5) -> str:
        """获取alert文本"""
        alert = self.switch_to_alert(timeout)
        return alert.text
    
    def switch_to_window(self, window_handle: str):
        """切换到指定窗口"""
        self.driver.switch_to.window(window_handle)
    
    def switch_to_new_window(self):
        """切换到最新打开的窗口"""
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])
    
    def get_window_handles(self) -> list:
        """获取所有窗口句柄"""
        return self.driver.window_handles
    
    def close_current_window(self):
        """关闭当前窗口"""
        self.driver.close()
    
    def execute_script(self, script: str, *args):
        """执行JavaScript"""
        return self.driver.execute_script(script, *args)
