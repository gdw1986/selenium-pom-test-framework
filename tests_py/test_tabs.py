# -*- coding: utf-8 -*-
"""Pytest 测试套件 - Tab 新功能模块"""
import pytest


class TestTabNavigation:
    """Tab 导航测试"""

    def test_tab_nav_exists(self, logged_in_page):
        page = logged_in_page
        assert page.locator("#tab-nav").count() == 1

    def test_tab_count(self, logged_in_page):
        page = logged_in_page
        assert page.locator(".tab-btn").count() == 5

    def test_default_active_is_iframe(self, logged_in_page):
        page = logged_in_page
        assert "active" in page.locator("#tab-btn-iframe").get_attribute("class")
        assert "active" in page.locator("#tab-iframe").get_attribute("class")

    def test_switch_to_task_tab(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-task")
        page.wait_for_selector("#tab-task.active", state="visible", timeout=3000)
        assert "active" in page.locator("#tab-btn-task").get_attribute("class")

    def test_switch_to_progress_tab(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-progress")
        page.wait_for_selector("#tab-progress.active", state="visible", timeout=3000)

    def test_switch_to_notify_tab(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-notify")
        page.wait_for_selector("#tab-notify.active", state="visible", timeout=3000)

    def test_switch_to_countdown_tab(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-countdown")
        page.wait_for_selector("#tab-countdown.active", state="visible", timeout=3000)


class TestIFrame:
    """iFrame 测试"""

    def test_iframe_exists(self, logged_in_page):
        page = logged_in_page
        page.wait_for_selector("#tab-iframe.active", state="visible")
        assert page.locator("#iframe-form").count() == 1


class TestTaskTable:
    """任务表格 CRUD 测试"""

    def test_initial_rows(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-task")
        page.wait_for_selector("#tab-task.active", state="visible")
        rows = page.locator("#task-tbody tr")
        assert rows.count() == 3

    def test_add_task(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-task")
        page.wait_for_selector("#tab-task.active", state="visible")
        init = page.locator("#task-tbody tr").count()
        page.fill("#new-task-name", "pytest新增任务")
        page.click("#tab-task button:has-text('添加')")
        page.wait_for_timeout(400)
        assert page.locator("#task-tbody tr").count() == init + 1

    def test_delete_task(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-task")
        page.wait_for_selector("#tab-task.active", state="visible")
        init = page.locator("#task-tbody tr").count()
        page.locator("#task-tbody tr").first.locator("button:has-text('删除')").click()
        page.wait_for_timeout(400)
        assert page.locator("#task-tbody tr").count() == init - 1

    def test_filter_tasks(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-task")
        page.wait_for_selector("#tab-task.active", state="visible")
        page.fill("#task-filter", "登录")
        page.wait_for_timeout(400)
        # 验证至少有一条可见的记录
        visible = page.evaluate(
            "() => document.querySelectorAll('#task-tbody tr:not([style*=\"display: none\"])').length"
        )
        assert visible >= 1


class TestProgressBar:
    """进度条测试"""

    def test_initial_0_percent(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-progress")
        page.wait_for_selector("#tab-progress.active", state="visible")
        assert page.text_content("#progress-label") == "0%"

    def test_increase_10_percent(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-progress")
        page.wait_for_selector("#tab-progress.active", state="visible")
        page.click("#btn-progress-plus")
        page.wait_for_timeout(600)
        assert page.text_content("#progress-label") == "10%"

    def test_increase_25_percent(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-progress")
        page.wait_for_selector("#tab-progress.active", state="visible")
        # 0 + 10 + 25 = 35
        page.click("#btn-progress-plus")
        page.click("#btn-progress-plus25")
        page.wait_for_timeout(600)
        assert page.text_content("#progress-label") == "35%"

    def test_reset(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-progress")
        page.wait_for_selector("#tab-progress.active", state="visible")
        page.click("#btn-progress-plus25")
        page.click("#btn-progress-plus25")
        page.wait_for_timeout(300)
        # 精确定位 progress tab 里的重置按钮
        page.locator("#tab-progress button:has-text('重置')").click()
        page.wait_for_timeout(600)
        assert page.text_content("#progress-label") == "0%"

    def test_max_100_percent(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-progress")
        page.wait_for_selector("#tab-progress.active", state="visible")
        for _ in range(12):
            page.click("#btn-progress-plus")
        page.wait_for_timeout(600)
        assert page.text_content("#progress-label") == "100%"


class TestNotifications:
    """通知系统测试"""

    def test_notify_triggers_exist(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-notify")
        page.wait_for_selector("#tab-notify.active", state="visible")
        assert page.locator("button:has-text('成功通知')").count() == 1
        assert page.locator("button:has-text('错误通知')").count() == 1

    def test_success_notification(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-notify")
        page.wait_for_selector("#tab-notify.active", state="visible")
        page.click("button:has-text('成功通知')")
        page.wait_for_timeout(500)
        assert page.locator(".notif.success").count() == 1

    def test_error_notification(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-notify")
        page.wait_for_selector("#tab-notify.active", state="visible")
        page.click("button:has-text('错误通知')")
        page.wait_for_timeout(500)
        assert page.locator(".notif.error").count() == 1


class TestCountdown:
    """倒计时测试"""

    def test_default_00_00(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-countdown")
        page.wait_for_selector("#tab-countdown.active", state="visible")
        assert page.text_content("#countdown-display") == "00:00"

    def test_start_30_seconds(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-countdown")
        page.wait_for_selector("#tab-countdown.active", state="visible")
        page.click("button:has-text('30秒')")
        page.wait_for_timeout(1500)
        text = page.text_content("#countdown-display")
        # 00:29 到 00:28 之间
        assert text.startswith("00:2") or text.startswith("00:3")

    def test_reset(self, logged_in_page):
        page = logged_in_page
        page.click("#tab-btn-countdown")
        page.wait_for_selector("#tab-countdown.active", state="visible")
        page.click("button:has-text('30秒')")
        page.wait_for_timeout(1000)
        # 精确定位 countdown tab 里的重置按钮
        page.locator("#tab-countdown button:has-text('重置')").click()
        page.wait_for_timeout(300)
        assert page.text_content("#countdown-display") == "00:00"
