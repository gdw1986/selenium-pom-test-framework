# RF + Playwright Test Framework

基于 [selenium-pom-test-framework](https://github.com/gdw1986/selenium-pom-test-framework) 的 Robot Framework + Playwright 重构版本。

## 目录结构

```
rf-playwright-test-framework/
├── pages/                   # Page Object 层 (Python)
│   ├── base_page.py         # 基础页面类（Playwright 封装）
│   ├── login_page.py        # 登录页面
│   ├── main_page.py         # 主页面（Alert/下拉框/上传/评论/多窗口）
│   └── popup_window.py      # 弹窗页面
├── resources/
│   └── common.robot         # 公共关键字（登录、对话框等）
├── tests/                   # Robot Framework 测试套件
│   ├── test_login.robot      # 登录测试（8 个用例）
│   ├── test_alert.robot      # Alert 弹窗测试（4 个用例）
│   ├── test_dropdown.robot   # 下拉框测试（19 个用例）
│   ├── test_file_upload.robot # 文件上传测试（6 个用例）
│   ├── test_comments.robot   # 评论功能测试（8 个用例）
│   └── test_windows.robot    # 多窗口测试（8 个用例）
├── config/
│   └── settings.py          # 配置（URL、凭据、超时等）
├── test_page.html           # 测试用网页（从原项目复制）
├── requirements.txt          # Python 依赖
├── run_tests.py             # 顺序执行测试
├── run_parallel.py          # pabot 并行执行
└── run_allure.py            # 生成 Allure 报告
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 HTTP 服务器

测试页面需要通过 HTTP 访问：

```bash
cd rf-playwright-test-framework
python -m http.server 8080
```

### 3. 运行测试

```bash
# 顺序执行全部测试
python run_tests.py

# 只跑某个套件
python run_tests.py --suite login
python run_tests.py --suite dropdown

# 并行执行（pabot）
python run_parallel.py --workers 4

# 有头模式（有浏览器窗口）
python run_tests.py --suite login

# 无头模式
python run_tests.py --suite login --headless
```

## 与原 Selenium 框架的对照

| Selenium (原) | Playwright + RF (新) |
|---|---|
| `selenium.webdriver` | `playwright.sync_api` / `Browser` |
| `WebDriverWait + EC` | `Wait For Elements State` / `Wait For Function` |
| `driver.find_element(By.ID, "x")` | `#x` (CSS selector) |
| `element.send_keys(text)` | `Fill Text` / `Type Text` |
| `element.click()` | `Click` |
| `Select(element)` | `Select Options By ... value/label/index` |
| `ActionChains.move_to_element()` | `Hover` |
| `driver.switch_to.alert` | `Handle Future Dialogs` + `Wait For Alert` |
| `driver.window_handles` | `Get Pages` / `Switch Page` |
| `file_input.send_keys(path)` | `Upload File By Selector` |
| pytest fixtures | RF Suite Setup / Test Setup |

## 依赖说明

- **robotframework==7.4.2** — Robot Framework 核心
- **robotframework-browser==19.14.2** — Browser 库（基于 Playwright）
- **robotframework-pabot==2.10.2** — 并行执行支持
