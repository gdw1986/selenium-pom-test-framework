"""
Pytest配置文件
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome",
        help="选择浏览器: chrome 或 firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="启用无头模式"
    )


@pytest.fixture(scope="session")
def browser(request):
    """获取浏览器类型"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request):
    """获取是否无头模式"""
    return request.config.getoption("--headless")


@pytest.fixture(scope="function")
def driver(browser, headless):
    """
    创建WebDriver实例
    支持Chrome和Firefox
    """
    if browser.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    
    elif browser.lower() == "firefox":
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=firefox_options
        )
    
    else:
        raise ValueError(f"不支持的浏览器类型: {browser}")
    
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    提供已登录的driver
    返回(driver, main_page)元组
    """
    from pages.login_page import LoginPage
    from pages.main_page import MainPage
    
    login_page = LoginPage(driver)
    login_page.open_login_page()
    main_page = login_page.login("test", "test")
    
    yield driver, main_page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动截图
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            import os
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            screenshot_path = f"{screenshot_dir}/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n截图已保存: {screenshot_path}")
