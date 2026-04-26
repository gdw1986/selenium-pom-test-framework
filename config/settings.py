"""
测试配置文件
集中管理测试环境配置
"""

# 测试页面配置
TEST_URL = "https://blog.gdw1986.top/wp-content/uploads/2026/04/test_page.html"

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
