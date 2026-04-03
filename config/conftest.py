"""
Pytest配置文件
"""
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions


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
    parser.addoption(
        "--local-driver",
        action="store_true",
        default=False,
        help="使用本地已安装的WebDriver，不自动下载"
    )


@pytest.fixture(scope="session")
def browser(request):
    """获取浏览器类型"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request):
    """获取是否无头模式"""
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def local_driver(request):
    """是否使用本地WebDriver"""
    return request.config.getoption("--local-driver")


@pytest.fixture(scope="function")
def driver(browser, headless, local_driver):
    """
    创建WebDriver实例
    支持Chrome和Firefox
    支持本地驱动和自动下载
    """
    if browser.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        if local_driver:
            # 使用本地ChromeDriver（需要手动安装并添加到PATH）
            driver = webdriver.Chrome(options=chrome_options)
        else:
            # 尝试自动下载，失败则回退到本地驱动
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=chrome_options
                )
            except Exception as e:
                print(f"\n自动下载ChromeDriver失败: {e}")
                print("尝试使用本地ChromeDriver...")
                driver = webdriver.Chrome(options=chrome_options)
    
    elif browser.lower() == "firefox":
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        
        if local_driver:
            driver = webdriver.Firefox(options=firefox_options)
        else:
            try:
                from webdriver_manager.firefox import GeckoDriverManager
                driver = webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=firefox_options
                )
            except Exception as e:
                print(f"\n自动下载GeckoDriver失败: {e}")
                print("尝试使用本地GeckoDriver...")
                driver = webdriver.Firefox(options=firefox_options)
    
    else:
        raise ValueError(f"不支持的浏览器类型: {browser}")
    
    driver.implicitly_wait(10)
    
    # 添加Allure步骤：记录浏览器启动
    try:
        import allure
        allure.attach(
            f"浏览器: {browser}\n无头模式: {headless}\n本地驱动: {local_driver}",
            name="测试环境",
            attachment_type=allure.attachment_type.TEXT
        )
    except ImportError:
        pass
    
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
    测试失败时自动截图，并附加到Allure报告
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            import os as os_module
            if not os_module.path.exists(screenshot_dir):
                os_module.makedirs(screenshot_dir)
            
            screenshot_path = f"{screenshot_dir}/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n截图已保存: {screenshot_path}")
            
            # 附加截图到Allure报告
            try:
                import allure
                allure.attach.file(
                    screenshot_path,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
            except ImportError:
                pass  # Allure未安装时忽略
