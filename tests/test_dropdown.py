"""
下拉框功能测试用例
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.main_page import MainPage


class TestDropdown:
    """下拉框功能测试类"""
    
    @pytest.fixture(scope="function")
    def driver(self):
        """测试前置：创建driver"""
        chrome_options = Options()
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
    def main_page(self, driver):
        """创建主页面对象并登录"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        main_page = login_page.login("test", "test")
        return main_page
    
    # ==================== 水果下拉框测试 ====================
    
    def test_fruit_select_exists(self, main_page):
        """测试水果下拉框存在"""
        assert main_page.is_element_present(MainPage.FRUIT_SELECT), "水果下拉框不存在"
    
    def test_fruit_select_options(self, main_page):
        """测试水果下拉框选项"""
        options = main_page.get_fruit_options()
        
        # 验证选项数量（包含空选项）
        assert len(options) == 6, f"水果选项数量应为6，实际为{len(options)}"
        
        # 验证具体选项
        values = [opt[0] for opt in options]
        expected_values = ["", "apple", "banana", "cherry", "grape", "mango"]
        assert values == expected_values, f"水果选项值不符合预期: {values}"
    
    @pytest.mark.parametrize("value,expected_text", [
        ("apple", "苹果"),
        ("banana", "香蕉"),
        ("cherry", "樱桃"),
        ("grape", "葡萄"),
        ("mango", "芒果"),
    ])
    def test_select_fruit_by_value(self, main_page, value, expected_text):
        """测试按value选择水果"""
        main_page.select_fruit_by_value(value)
        result_text = main_page.get_selected_fruit_text()
        
        assert expected_text in result_text, f"选择{value}后显示文本应包含{expected_text}"
        assert value in result_text, f"选择结果应包含value={value}"
    
    def test_select_fruit_by_text(self, main_page):
        """测试按文本选择水果"""
        main_page.select_fruit_by_text("苹果 Apple")
        result_text = main_page.get_selected_fruit_text()
        
        assert "苹果" in result_text
        assert "apple" in result_text
    
    def test_select_fruit_by_index(self, main_page):
        """测试按索引选择水果"""
        main_page.select_fruit_by_index(1)  # 选择第一个非空选项
        result_text = main_page.get_selected_fruit_text()
        
        assert "苹果" in result_text
    
    # ==================== 城市下拉框测试 ====================
    
    def test_city_select_exists(self, main_page):
        """测试城市下拉框存在"""
        assert main_page.is_element_present(MainPage.CITY_SELECT), "城市下拉框不存在"
    
    def test_city_select_dynamic_loading(self, main_page):
        """测试城市下拉框动态加载"""
        # 初始应该只有一个"加载中"选项
        from selenium.webdriver.support.ui import Select
        select = Select(main_page.find_element(MainPage.CITY_SELECT))
        initial_options = select.options
        
        # 等待加载完成
        main_page.wait_for_city_options_loaded(timeout=3)
        
        # 加载完成后应该有7个选项（空选项+6个城市）
        options = main_page.get_city_options()
        assert len(options) == 7, f"城市选项数量应为7，实际为{len(options)}"
    
    @pytest.mark.parametrize("value,expected_text", [
        ("beijing", "北京"),
        ("shanghai", "上海"),
        ("guangzhou", "广州"),
        ("shenzhen", "深圳"),
        ("chengdu", "成都"),
        ("hangzhou", "杭州"),
    ])
    def test_select_city_by_value(self, main_page, value, expected_text):
        """测试按value选择城市"""
        main_page.select_city_by_value(value)
        result_text = main_page.get_selected_city_text()
        
        assert expected_text in result_text, f"选择{value}后显示文本应包含{expected_text}"
        assert value in result_text, f"选择结果应包含value={value}"
    
    def test_select_city_by_text(self, main_page):
        """测试按文本选择城市"""
        main_page.select_city_by_text("上海 Shanghai")
        result_text = main_page.get_selected_city_text()
        
        assert "上海" in result_text
        assert "shanghai" in result_text
    
    def test_city_options_content(self, main_page):
        """测试城市选项内容"""
        options = main_page.get_city_options()
        
        expected_cities = [
            ("", "-- 请选择 --"),
            ("beijing", "北京 Beijing"),
            ("shanghai", "上海 Shanghai"),
            ("guangzhou", "广州 Guangzhou"),
            ("shenzhen", "深圳 Shenzhen"),
            ("chengdu", "成都 Chengdu"),
            ("hangzhou", "杭州 Hangzhou"),
        ]
        
        assert options == expected_cities, f"城市选项不符合预期: {options}"
