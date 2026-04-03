"""
登录功能测试用例
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.main_page import MainPage


class TestLogin:
    """登录功能测试类"""
    
    @pytest.fixture(scope="function")
    def driver(self):
        """测试前置：创建driver"""
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # 无头模式，需要时可开启
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    @pytest.fixture(scope="function")
    def login_page(self, driver):
        """创建登录页面对象"""
        page = LoginPage(driver)
        page.open_login_page()
        return page
    
    def test_login_page_elements_exist(self, login_page):
        """测试登录页面元素是否存在"""
        assert login_page.is_on_login_page(), "未正确显示登录页面"
        assert login_page.is_element_present(LoginPage.USERNAME_INPUT), "用户名输入框不存在"
        assert login_page.is_element_present(LoginPage.PASSWORD_INPUT), "密码输入框不存在"
        assert login_page.is_element_present(LoginPage.LOGIN_BUTTON), "登录按钮不存在"
        assert login_page.is_element_present(LoginPage.ERROR_MESSAGE), "错误提示区域不存在"
    
    def test_successful_login(self, login_page):
        """测试正常登录流程"""
        main_page = login_page.login("test", "test")
        
        # 验证登录成功，跳转到主页面
        assert main_page.is_on_main_page(), "登录后未正确跳转到主页面"
        assert main_page.is_element_present(MainPage.ALERT_BUTTON), "主页面Alert按钮不存在"
    
    def test_login_with_wrong_username(self, login_page):
        """测试错误用户名"""
        login_page.enter_username("wrong")
        login_page.enter_password("test")
        login_page.click_login_button()
        
        assert login_page.has_error(), "错误用户名应显示错误提示"
        assert "用户名或密码错误" in login_page.get_error_message()
        assert login_page.is_username_error_highlighted(), "用户名输入框应有错误高亮"
    
    def test_login_with_wrong_password(self, login_page):
        """测试错误密码"""
        login_page.enter_username("test")
        login_page.enter_password("wrong")
        login_page.click_login_button()
        
        assert login_page.has_error(), "错误密码应显示错误提示"
        assert "用户名或密码错误" in login_page.get_error_message()
        assert login_page.is_password_error_highlighted(), "密码输入框应有错误高亮"
    
    def test_login_with_both_wrong(self, login_page):
        """测试用户名和密码都错误"""
        login_page.enter_username("wrong")
        login_page.enter_password("wrong")
        login_page.click_login_button()
        
        assert login_page.has_error()
        assert login_page.is_username_error_highlighted()
        assert login_page.is_password_error_highlighted()
    
    def test_login_with_empty_credentials(self, login_page):
        """测试空用户名和密码"""
        login_page.click_login_button()
        
        assert login_page.has_error()
        assert "用户名或密码错误" in login_page.get_error_message()
    
    def test_login_by_pressing_enter(self, login_page):
        """测试按回车键登录"""
        login_page.enter_username("test")
        login_page.enter_password("test")
        login_page.press_enter_to_login()
        
        # 等待登录成功
        assert login_page.is_login_successful(), "按回车键登录失败"
    
    def test_clear_inputs(self, login_page):
        """测试清空输入框功能"""
        login_page.enter_username("test")
        login_page.enter_password("test")
        login_page.clear_inputs()
        
        username = login_page.find_element(LoginPage.USERNAME_INPUT).get_attribute("value")
        password = login_page.find_element(LoginPage.PASSWORD_INPUT).get_attribute("value")
        
        assert username == "", "用户名输入框应被清空"
        assert password == "", "密码输入框应被清空"
