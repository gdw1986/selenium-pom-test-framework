# -*- coding: utf-8 -*-
"""Pytest 配置 - Playwright 浏览器 Fixtures"""
import pytest
import os


@pytest.fixture(scope="session")
def test_url():
    """被测页面 URL"""
    return os.environ.get("TEST_URL", "https://blog.gdw1986.top/wp-content/uploads/2026/04/test_page.html")


@pytest.fixture(scope="session")
def browser_type():
    """浏览器类型"""
    return os.environ.get("BROWSER_TYPE", "chromium")


@pytest.fixture(scope="session")
def playwright_instance(browser_type):
    """Playwright 实例（session 级，整个测试会话共享）"""
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    yield pw
    pw.stop()


@pytest.fixture(scope="function")
def browser(playwright_instance, browser_type):
    """每个测试函数独立的新浏览器实例"""
    headless = os.environ.get("HEADLESS", "true").lower() == "true"
    browser = playwright_instance.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()

    yield page

    context.close()
    browser.close()


@pytest.fixture(scope="function")
def logged_in_page(browser, test_url):
    """已登录的页面（自动完成登录流程）"""
    browser.goto(test_url)
    browser.wait_for_selector("#username", state="visible")
    browser.fill("#username", "test")
    browser.fill("#password", "test")
    browser.click(".login-btn")
    browser.wait_for_selector("#main-page.active", state="visible")
    yield browser
