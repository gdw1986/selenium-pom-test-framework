"""
弹窗页面 - Page Object
用于处理openFiveWindows()打开的弹窗
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class PopupWindow(BasePage):
    """弹窗页面Page Object"""
    
    # 定位器
    ALERT_BUTTON = (By.CSS_SELECTOR, "button[onclick*='alert']")
    CLOSE_BUTTON = (By.CSS_SELECTOR, "button[onclick='window.close()']")
    WINDOW_TITLE = (By.CSS_SELECTOR, "h2")
    WINDOW_INFO = (By.CSS_SELECTOR, ".info")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_popup_alert_button(self):
        """点击弹窗内的Alert按钮"""
        self.click(self.ALERT_BUTTON)
        return self
    
    def click_close_button(self):
        """点击关闭窗口按钮"""
        self.click(self.CLOSE_BUTTON)
    
    def get_window_title(self) -> str:
        """获取弹窗标题"""
        return self.get_text(self.WINDOW_TITLE)
    
    def get_window_info(self) -> str:
        """获取弹窗信息文本"""
        return self.get_text(self.WINDOW_INFO)
    
    def get_window_number(self) -> int:
        """从info文本中提取窗口编号"""
        info = self.get_window_info()
        # 格式: "窗口编号: X | 颜色: #XXXXXX"
        try:
            return int(info.split("窗口编号: ")[1].split(" |")[0])
        except (IndexError, ValueError):
            return 0
    
    def get_window_color(self) -> str:
        """从info文本中提取窗口颜色"""
        info = self.get_window_info()
        try:
            return info.split("颜色: ")[1]
        except IndexError:
            return ""
