# Selenium Page Object 测试框架

基于 Page Object Pattern 的 Selenium 自动化测试框架，用于测试 test_page.html 页面的所有功能。

## 项目结构

```
selenium-pom-test-framework/
├── pages/                      # Page Object 层
│   ├── __init__.py
│   ├── base_page.py           # 基础页面类
│   ├── login_page.py          # 登录页面
│   ├── main_page.py           # 主页面
│   └── popup_window.py        # 弹窗页面
├── tests/                      # 测试用例层
│   ├── __init__.py
│   ├── test_login.py          # 登录功能测试
│   ├── test_alert.py          # Alert弹窗测试
│   ├── test_dropdown.py       # 下拉框测试
│   ├── test_file_upload.py    # 文件上传测试
│   ├── test_comments.py       # 评论功能测试
│   └── test_windows.py        # 多窗口测试
├── config/                     # 配置目录
│   ├── __init__.py
│   ├── conftest.py            # Pytest配置（fixture、hook）
│   └── pytest.ini             # Pytest配置（标记、选项）
├── conftest.py                # 根目录Pytest配置（导入config）
├── test_page.html             # 测试页面（被测系统）
├── requirements.txt           # 依赖包
├── run_tests.py               # 基础测试运行脚本
├── run_allure.py              # Allure报告运行脚本 ⭐
├── run_parallel.py            # 并行运行测试脚本 ⚡
├── run_with_proxy.py          # 带代理的测试运行脚本 🌐
└── README.md                  # 说明文档
```

## 快速开始

### 1. 启动测试页面
```bash
# 在项目根目录启动HTTP服务器
python3 -m http.server 8080
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行测试

#### 方式一：基础运行
```bash
pytest
```

#### 方式二：生成Allure报告（推荐）
```bash
# 运行测试并生成Allure报告
python run_allure.py

# 生成报告并启动Allure服务器
python run_allure.py --serve

# 清理历史数据后运行
python run_allure.py --clean

# 保留历史趋势（用于趋势图）
python run_allure.py --history
```

#### 方式三：命令行直接运行
```bash
# 生成Allure结果
pytest --alluredir=allure-results

# 生成HTML报告
allure generate allure-results -o allure-report --clean

# 启动Allure服务器
allure serve allure-results
```

## 运行选项

### 运行指定模块
```bash
pytest tests/test_login.py -v
# 或
python run_tests.py --module login
```

### 使用Firefox浏览器
```bash
pytest --browser firefox
# 或
python run_allure.py --browser firefox
```

### 无头模式运行
```bash
pytest --headless
# 或
python run_allure.py --headless
```

### 运行冒烟测试
```bash
pytest -m smoke
# 或
python run_tests.py --smoke
```

### 并行运行测试
```bash
# 使用所有CPU核心并行运行
pytest -n auto

# 指定并行进程数
pytest -n 4

# 并行运行 + 生成Allure报告
pytest -n auto --alluredir=allure-results

# 失败时立即终止
pytest -n auto --maxfail=1
```

## 测试覆盖功能

| 功能模块 | 测试文件 | 覆盖内容 |
|---------|---------|---------|
| 登录功能 | test_login.py | 正常登录、错误用户名/密码、空输入、回车登录、错误高亮 |
| Alert弹窗 | test_alert.py | Alert按钮、Tooltip、弹窗确认/取消 |
| 下拉框 | test_dropdown.py | 静态水果选择、动态城市加载、按value/text/index选择 |
| 文件上传 | test_file_upload.py | 正常上传、多扩展名、空文件、清除上传、路径显示 |
| 评论功能 | test_comments.py | 添加评论、多条评论、空评论、特殊字符、emoji、长文本 |
| 多窗口 | test_windows.py | 打开5窗口、窗口切换、弹窗Alert、关闭窗口、窗口信息验证 |

## Page Object 设计

### BasePage
- 封装通用操作方法（查找元素、点击、输入、等待等）
- 提供Alert处理和窗口切换方法

### LoginPage
- 登录相关元素定位
- 登录流程封装
- 错误验证方法

### MainPage
- 主页面所有功能元素
- Alert按钮、下拉框、文件上传、评论等方法
- 多窗口操作方法

### PopupWindow
- 弹窗页面元素
- 弹窗内Alert和关闭按钮操作

## 测试页面说明

`test_page.html` 是一个专门为Selenium自动化测试设计的练习页面，包含以下功能：

| 功能 | 描述 |
|-----|------|
| 登录验证 | 用户名/密码均为 `test`，错误时显示红色高亮 |
| Alert弹窗 | 点击按钮弹出JavaScript alert |
| 静态下拉框 | 水果选择列表（苹果、香蕉等） |
| 动态下拉框 | 城市列表，页面加载1.5秒后异步填充 |
| 文件上传 | 支持拖拽和点击上传，显示fakepath |
| 评论功能 | 输入评论后1秒延迟显示在列表顶部 |
| 多窗口 | 点击按钮打开5个彩色弹窗 |

## 常见问题

### 1. WebDriver下载失败（网络问题）

如果遇到 `Could not reach host. Are you offline?` 错误，说明自动下载WebDriver失败。

#### 使用代理（如果你有代理）

**方式1：命令行临时设置（推荐）**
```bash
# Windows PowerShell
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"
pytest

# Windows CMD
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
pytest

# 或使用脚本
python run_with_proxy.py
```

**方式2：使用本地WebDriver**
```bash
pytest --local-driver
```

#### 其他解决方案

#### 方案A：使用本地WebDriver（推荐）
```bash
# 先手动下载ChromeDriver并添加到系统PATH
# 下载地址：https://chromedriver.chromium.org/downloads

# 然后使用 --local-driver 参数运行
pytest --local-driver
python run_allure.py --local-driver
```

#### 方案B：手动下载并配置
1. 查看Chrome版本：`chrome://version/`
2. 下载对应版本的ChromeDriver：https://chromedriver.chromium.org/downloads
3. 解压后将chromedriver.exe放在以下任一位置：
   - 系统PATH目录
   - 项目根目录
   - 指定路径并修改代码

### 2. Firefox驱动问题

Firefox需要下载geckodriver：
- 下载地址：https://github.com/mozilla/geckodriver/releases
- 同样添加到PATH或使用 `--local-driver` 参数

## 注意事项

1. 确保测试页面服务已启动：`python3 -m http.server 8080`
2. 首次运行会自动下载对应浏览器的WebDriver（需要网络）
3. 测试失败会自动截图保存到 screenshots/ 目录，并附加到Allure报告
4. 默认使用Chrome浏览器，可通过参数切换
5. 使用Allure报告前需要安装Allure命令行工具：`brew install allure` (macOS)
6. 离线环境请使用 `--local-driver` 参数
