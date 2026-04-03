"""
主页面 - Page Object
包含所有功能元素的定位和操作
"""
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class MainPage(BasePage):
    """主页面Page Object"""
    
    # 定位器 - 页面容器
    MAIN_PAGE_CONTAINER = (By.ID, "main-page")
    
    # 定位器 - Alert按钮
    ALERT_BUTTON = (By.CSS_SELECTOR, "button[onclick='showAlert()']")
    ALERT_BUTTON_TOOLTIP = (By.CSS_SELECTOR, "button[onclick='showAlert()'] .tooltip")
    
    # 定位器 - 多窗口按钮
    OPEN_WINDOWS_BUTTON = (By.CSS_SELECTOR, "button.btn-orange[onclick='openFiveWindows()']")
    OPEN_WINDOWS_TOOLTIP = (By.CSS_SELECTOR, "button.btn-orange .tooltip")
    
    # 定位器 - 水果下拉框
    FRUIT_SELECT = (By.ID, "fruit-select")
    FRUIT_SELECT_RESULT = (By.ID, "select-result")
    
    # 定位器 - 城市下拉框
    CITY_SELECT = (By.ID, "city-select")
    CITY_SELECT_RESULT = (By.ID, "city-result")
    
    # 定位器 - 文件上传
    FILE_INPUT = (By.ID, "file-input")
    UPLOAD_DROP_ZONE = (By.ID, "upload-drop-zone")
    UPLOAD_FILE_INFO = (By.ID, "upload-file-info")
    UPLOAD_FILE_NAME = (By.ID, "upload-file-name")
    UPLOAD_FILE_META = (By.ID, "upload-file-meta")
    UPLOAD_FILE_FULLPATH = (By.ID, "upload-file-fullpath")
    UPLOAD_CLEAR_BUTTON = (By.CSS_SELECTOR, ".upload-clear-btn")
    
    # 定位器 - 评论区
    COMMENT_INPUT = (By.ID, "comment-input")
    COMMENT_SUBMIT_BUTTON = (By.CSS_SELECTOR, ".comment-submit-btn")
    COMMENT_LIST = (By.ID, "comment-list")
    COMMENT_ITEMS = (By.CSS_SELECTOR, ".comment-item")
    COMMENT_TOAST = (By.ID, "comment-toast")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_on_main_page(self) -> bool:
        """判断是否处于主页面"""
        return self.is_element_visible(self.MAIN_PAGE_CONTAINER)
    
    # ==================== Alert功能 ====================
    
    def click_alert_button(self):
        """点击Alert按钮"""
        self.click(self.ALERT_BUTTON)
        return self
    
    def get_alert_button_tooltip_text(self) -> str:
        """获取Alert按钮的tooltip文本"""
        # 先悬停在按钮上，然后获取tooltip
        from selenium.webdriver.common.action_chains import ActionChains
        button = self.find_element(self.ALERT_BUTTON)
        ActionChains(self.driver).move_to_element(button).perform()
        return self.get_text(self.ALERT_BUTTON_TOOLTIP)
    
    # ==================== 多窗口功能 ====================
    
    def click_open_windows_button(self):
        """点击打开5个新窗口按钮"""
        self.click(self.OPEN_WINDOWS_BUTTON)
        return self
    
    def get_open_windows_tooltip_text(self) -> str:
        """获取打开窗口按钮的tooltip文本"""
        from selenium.webdriver.common.action_chains import ActionChains
        button = self.find_element(self.OPEN_WINDOWS_BUTTON)
        ActionChains(self.driver).move_to_element(button).perform()
        return self.get_text(self.OPEN_WINDOWS_TOOLTIP)
    
    def open_five_windows(self) -> list:
        """
        打开5个新窗口，返回所有窗口句柄
        """
        initial_handles = set(self.get_window_handles())
        self.click_open_windows_button()
        
        # 等待新窗口打开
        WebDriverWait(self.driver, 5).until(
            lambda d: len(d.window_handles) == len(initial_handles) + 5
        )
        
        all_handles = self.get_window_handles()
        new_handles = [h for h in all_handles if h not in initial_handles]
        return new_handles
    
    def close_all_popup_windows(self, main_handle: str):
        """关闭所有弹窗，回到主窗口"""
        for handle in self.get_window_handles():
            if handle != main_handle:
                self.switch_to_window(handle)
                self.close_current_window()
        self.switch_to_window(main_handle)
    
    # ==================== 下拉框功能 ====================
    
    def select_fruit_by_value(self, value: str):
        """
        按value选择水果
        value可选: apple, banana, cherry, grape, mango
        """
        from selenium.webdriver.support.ui import Select
        select = Select(self.find_element(self.FRUIT_SELECT))
        select.select_by_value(value)
        return self
    
    def select_fruit_by_text(self, text: str):
        """按文本选择水果"""
        from selenium.webdriver.support.ui import Select
        select = Select(self.find_element(self.FRUIT_SELECT))
        select.select_by_visible_text(text)
        return self
    
    def select_fruit_by_index(self, index: int):
        """按索引选择水果"""
        from selenium.webdriver.support.ui import Select
        select = Select(self.find_element(self.FRUIT_SELECT))
        select.select_by_index(index)
        return self
    
    def get_selected_fruit_text(self) -> str:
        """获取选中的水果文本"""
        return self.get_text(self.FRUIT_SELECT_RESULT)
    
    def get_fruit_options(self) -> list:
        """获取所有水果选项"""
        from selenium.webdriver.support.ui import Select
        select = Select(self.find_element(self.FRUIT_SELECT))
        return [(opt.get_attribute("value"), opt.text) for opt in select.options]
    
    def wait_for_city_options_loaded(self, timeout: int = 5):
        """等待城市选项加载完成"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "#city-select option")) > 1
        )
        return self
    
    def select_city_by_value(self, value: str):
        """
        按value选择城市
        value可选: beijing, shanghai, guangzhou, shenzhen, chengdu, hangzhou
        """
        from selenium.webdriver.support.ui import Select
        self.wait_for_city_options_loaded()
        select = Select(self.find_element(self.CITY_SELECT))
        select.select_by_value(value)
        return self
    
    def select_city_by_text(self, text: str):
        """按文本选择城市"""
        from selenium.webdriver.support.ui import Select
        self.wait_for_city_options_loaded()
        select = Select(self.find_element(self.CITY_SELECT))
        select.select_by_visible_text(text)
        return self
    
    def get_selected_city_text(self) -> str:
        """获取选中的城市文本"""
        return self.get_text(self.CITY_SELECT_RESULT)
    
    def get_city_options(self) -> list:
        """获取所有城市选项"""
        from selenium.webdriver.support.ui import Select
        self.wait_for_city_options_loaded()
        select = Select(self.find_element(self.CITY_SELECT))
        return [(opt.get_attribute("value"), opt.text) for opt in select.options]
    
    # ==================== 文件上传功能 ====================
    
    def upload_file(self, file_path: str):
        """
        上传文件
        file_path: 文件的绝对路径
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        file_input = self.find_element(self.FILE_INPUT)
        file_input.send_keys(file_path)
        return self
    
    def is_file_uploaded(self) -> bool:
        """判断文件是否已上传"""
        return "visible" in self.find_element(self.UPLOAD_FILE_INFO).get_attribute("class")
    
    def get_uploaded_file_name(self) -> str:
        """获取上传文件的文件名"""
        return self.get_text(self.UPLOAD_FILE_NAME)
    
    def get_uploaded_file_meta(self) -> str:
        """获取上传文件的元信息（大小和类型）"""
        return self.get_text(self.UPLOAD_FILE_META)
    
    def get_uploaded_file_fullpath(self) -> str:
        """获取上传文件的完整路径（fakepath）"""
        return self.get_text(self.UPLOAD_FILE_FULLPATH)
    
    def clear_uploaded_file(self):
        """清除已上传的文件"""
        self.click(self.UPLOAD_CLEAR_BUTTON)
        return self
    
    # ==================== 评论功能 ====================
    
    def enter_comment(self, text: str):
        """输入评论内容"""
        self.send_keys(self.COMMENT_INPUT, text)
        return self
    
    def submit_comment(self):
        """提交评论"""
        self.click(self.COMMENT_SUBMIT_BUTTON)
        return self
    
    def add_comment(self, text: str):
        """
        添加评论的完整流程
        等待评论显示在列表中
        """
        self.enter_comment(text)
        self.submit_comment()
        
        # 等待提交按钮恢复（表示提交完成）
        WebDriverWait(self.driver, 3).until(
            lambda d: d.find_element(*self.COMMENT_SUBMIT_BUTTON).text == "发布评论"
        )
        return self
    
    def get_all_comments(self) -> list:
        """获取所有评论元素"""
        return self.find_elements(self.COMMENT_ITEMS)
    
    def get_comments_count(self) -> int:
        """获取评论数量"""
        return len(self.get_all_comments())
    
    def get_first_comment_text(self) -> str:
        """获取第一条评论的文本"""
        comments = self.get_all_comments()
        if comments:
            return comments[0].find_element(By.CSS_SELECTOR, ".comment-content").text
        return ""
    
    def get_first_comment_author(self) -> str:
        """获取第一条评论的作者"""
        comments = self.get_all_comments()
        if comments:
            return comments[0].find_element(By.CSS_SELECTOR, ".comment-author").text
        return ""
    
    def get_all_comment_texts(self) -> list:
        """获取所有评论的文本内容列表，按页面显示顺序"""
        comments = self.get_all_comments()
        texts = []
        for comment in comments:
            try:
                text = comment.find_element(By.CSS_SELECTOR, ".comment-content").text
                texts.append(text)
            except:
                pass
        return texts
    
    def is_comment_toast_visible(self) -> bool:
        """判断评论提交成功提示是否显示"""
        toast = self.find_element(self.COMMENT_TOAST)
        return "show" in toast.get_attribute("class")
