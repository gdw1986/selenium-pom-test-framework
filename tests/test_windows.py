"""
多窗口功能测试用例
"""
import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.popup_window import PopupWindow


class TestWindows:
    """多窗口功能测试类"""
    
    @pytest.fixture(scope="function")
    def main_page(self, driver):
        """创建主页面对象并登录"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        main_page = login_page.login("test", "test")
        return main_page
    
    def test_open_windows_button_exists(self, main_page):
        """测试打开窗口按钮存在"""
        assert main_page.is_element_present(MainPage.OPEN_WINDOWS_BUTTON), "打开窗口按钮不存在"
    
    def test_open_windows_button_tooltip(self, main_page):
        """测试打开窗口按钮的tooltip"""
        tooltip_text = main_page.get_open_windows_tooltip_text()
        assert "窗口" in tooltip_text or "多窗口" in tooltip_text, f"Tooltip文本不符合预期: {tooltip_text}"
    
    def test_open_five_windows(self, main_page, driver):
        """测试打开5个新窗口"""
        main_handle = driver.current_window_handle
        initial_handles = len(driver.window_handles)
        
        new_handles = main_page.open_five_windows()
        
        # 验证打开了5个新窗口
        assert len(new_handles) == 5, f"应打开5个新窗口，实际打开了{len(new_handles)}个"
        
        # 验证总窗口数
        total_handles = len(driver.window_handles)
        assert total_handles == initial_handles + 5, f"总窗口数应为{initial_handles + 5}，实际为{total_handles}"
        
        # 清理：关闭所有弹窗
        main_page.close_all_popup_windows(main_handle)
    
    def test_popup_window_content(self, main_page, driver):
        """测试弹窗内容"""
        main_handle = driver.current_window_handle
        new_handles = main_page.open_five_windows()
        
        # 切换到第一个弹窗
        popup = PopupWindow(driver)
        popup.switch_to_window(new_handles[0])
        
        # 验证弹窗元素
        assert popup.is_element_present(PopupWindow.ALERT_BUTTON), "弹窗Alert按钮不存在"
        assert popup.is_element_present(PopupWindow.CLOSE_BUTTON), "弹窗关闭按钮不存在"
        
        # 验证窗口标题
        title = popup.get_window_title()
        assert "窗口" in title, f"窗口标题应包含'窗口': {title}"
        
        # 清理
        main_page.close_all_popup_windows(main_handle)
    
    def test_popup_window_alert(self, main_page, driver):
        """测试弹窗内的Alert功能"""
        main_handle = driver.current_window_handle
        new_handles = main_page.open_five_windows()
        
        popup = PopupWindow(driver)
        popup.switch_to_window(new_handles[0])
        
        # 点击弹窗内的Alert按钮
        popup.click_popup_alert_button()
        
        # 验证alert出现
        alert_text = popup.get_alert_text()
        assert "窗口" in alert_text, f"Alert文本应包含'窗口': {alert_text}"
        
        # 关闭alert
        popup.accept_alert()
        
        # 清理
        main_page.close_all_popup_windows(main_handle)
    
    def test_close_popup_window(self, main_page, driver):
        """测试关闭弹窗"""
        main_handle = driver.current_window_handle
        initial_handles = len(driver.window_handles)
        
        new_handles = main_page.open_five_windows()
        
        # 切换到第一个弹窗并关闭
        popup = PopupWindow(driver)
        popup.switch_to_window(new_handles[0])
        popup.click_close_button()
        
        # 验证窗口已关闭
        import time
        time.sleep(0.5)  # 等待窗口关闭
        current_handles = len(driver.window_handles)
        assert current_handles == initial_handles + 4, f"关闭后窗口数应为{initial_handles + 4}，实际为{current_handles}"
        
        # 回到主窗口
        driver.switch_to.window(main_handle)
    
    def test_switch_between_windows(self, main_page, driver):
        """测试窗口间切换"""
        main_handle = driver.current_window_handle
        new_handles = main_page.open_five_windows()
        
        popup = PopupWindow(driver)
        
        # 依次切换到每个窗口
        for i, handle in enumerate(new_handles):
            popup.switch_to_window(handle)
            title = popup.get_window_title()
            assert f"窗口 {i+1}" in title, f"第{i+1}个窗口标题应为'窗口 {i+1}'"
        
        # 回到主窗口
        driver.switch_to.window(main_handle)
        assert main_page.is_on_main_page(), "应能成功切换回主页面"
        
        # 清理
        main_page.close_all_popup_windows(main_handle)
    
    def test_popup_window_info(self, main_page, driver):
        """测试弹窗信息"""
        main_handle = driver.current_window_handle
        new_handles = main_page.open_five_windows()
        
        popup = PopupWindow(driver)
        
        # 检查每个窗口的信息
        for i, handle in enumerate(new_handles):
            popup.switch_to_window(handle)
            
            window_num = popup.get_window_number()
            assert window_num == i + 1, f"窗口编号应为{i+1}，实际为{window_num}"
            
            color = popup.get_window_color()
            assert color.startswith("#"), f"颜色应为十六进制格式: {color}"
        
        # 清理
        main_page.close_all_popup_windows(main_handle)
