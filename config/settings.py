"""
测试配置文件
集中管理测试环境配置
"""
from config.urls import TEST_PAGE

# 测试页面配置 - 从 urls.py 导入，支持通过 BASE_URL 环境变量动态配置
TEST_URL = TEST_PAGE

# 登录配置
LOGIN_USERNAME = "test"
LOGIN_PASSWORD = "test"

# 浏览器配置
DEFAULT_BROWSER = "chrome"
DEFAULT_HEADLESS = False
DEFAULT_TIMEOUT = 10

# 测试数据
VALID_FRUITS = ["apple", "banana", "orange", "grape", "mango"]
VALID_CITIES = ["beijing", "shanghai", "guangzhou", "shenzhen", "hangzhou"]

# 文件上传配置
UPLOAD_TEST_FILES = {
    "txt": "test_file.txt",
    "jpg": "test_image.jpg",
    "pdf": "test_doc.pdf"
}
