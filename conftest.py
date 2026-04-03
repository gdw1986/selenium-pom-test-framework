"""
Pytest根配置 - 导入config目录中的配置
"""
import pytest
from config.conftest import (
    setup_proxy,
    pytest_runtest_makereport,
    browser,
    headless,
    local_driver,
    driver,
    logged_in_driver,
)


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
