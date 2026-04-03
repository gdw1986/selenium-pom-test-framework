"""
Alert弹窗功能测试用例
"""
import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage


class TestAlert:
    """Alert弹窗功能测试类"""
    
    @pytest.fixture(scope="function")
    def main_page(self, driver):
        """创建主页面对象并登录"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        main_page = login_page.login("test", "test")
        return main_page
    
    def test_alert_button_exists(self, main_page):
        """测试Alert按钮存在"""
        assert main_page.is_element_present(MainPage.ALERT_BUTTON), "Alert按钮不存在"
    
    def test_alert_button_tooltip(self, main_page):
        """测试Alert按钮的tooltip"""
        tooltip_text = main_page.get_alert_button_tooltip_text()
        assert "悬停" in tooltip_text or "提示" in tooltip_text, f"Tooltip文本不符合预期: {tooltip_text}"
    
    def test_alert_popup_and_accept(self, main_page):
        """测试Alert弹窗并点击确定"""
        main_page.click_alert_button()
        
        # 验证alert出现
        alert_text = main_page.get_alert_text()
        assert "Selenium" in alert_text or "Alert" in alert_text, f"Alert文本不符合预期: {alert_text}"
        
        # 点击确定
        main_page.accept_alert()
        
        # 验证alert已关闭（不应再抛出异常）
        # 如果alert还在，下面的操作会失败
        assert main_page.is_element_present(MainPage.ALERT_BUTTON)
    
    def test_alert_popup_and_dismiss(self, main_page):
        """测试Alert弹窗并点击取消（dismiss）"""
        main_page.click_alert_button()
        
        # 获取alert文本
        alert_text = main_page.get_alert_text()
        assert alert_text is not None
        
        # 点击取消（对于alert，dismiss和accept效果相同）
        main_page.dismiss_alert()
        
        # 验证alert已关闭
        assert main_page.is_element_present(MainPage.ALERT_BUTTON)
