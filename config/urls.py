"""
测试 URL 配置文件
集中管理所有测试环境地址
通过环境变量 BASE_URL 动态配置
"""
import os

# 默认测试环境
DEFAULT_BASE_URL = "https://blog.gdw1986.top/wp-content/uploads/2026/04"

# 从环境变量读取 BASE_URL，如果未设置则使用默认值
BASE_URL = os.environ.get("BASE_URL", DEFAULT_BASE_URL)

# 各个测试页面的完整 URL
TEST_PAGE = f"{BASE_URL}/test_page.html"
