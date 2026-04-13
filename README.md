# Selenium Page Object 测试框架

基于 Page Object Pattern 的双框架自动化测试项目，涵盖 Selenium (pytest) + Robot Framework 两种测试技术栈，共同测试 `test_page.html` 页面全部功能。

## 项目结构

```
selenium-pom-test-framework/
├── selenium-pom/               # Selenium + pytest 框架
│   ├── pages/                  # Page Object 层
│   ├── tests/                  # pytest 测试用例
│   ├── config/                 # 配置和 fixtures
│   ├── conftest.py            # pytest 根配置
│   ├── run_tests.py           # 顺序执行
│   ├── run_parallel.py         # pytest-xdist 并行
│   └── run_allure.py           # Allure 报告
│
├── rf-playwright/              # Robot Framework + Playwright 框架
│   ├── tests/                  # .robot 测试套件
│   ├── tests_py/               # pytest + Playwright（Python）
│   ├── resources/              # RF 公共关键字
│   ├── locators/               # 统一 locator 配置（JSON）
│   ├── config/                 # Python 配置
│   ├── run_tests.py            # Robot Framework 顺序执行
│   ├── run_parallel.py          # pabot 并行
│   └── pytest.ini              # pytest 配置（tests_py）
│
└── test_page.html             # 被测页面（共享）
```

## 快速开始

### Selenium + pytest

```bash
cd selenium-pom
pip install -r requirements.txt
python -m http.server 8080        # 启动服务
python run_tests.py              # 跑全部测试
python run_parallel.py --workers 4
```

### Robot Framework + Playwright

```bash
cd rf-playwright
pip install -r requirements.txt
python -m http.server 8080        # 启动服务
robot tests/                       # 跑全部 .robot 套件
robot --suite tabs tests/          # 只跑指定套件
pabot --processes 4 tests/        # 并行执行
pytest tests_py/ -v               # pytest + Playwright
```

## 测试覆盖

| 功能 | Selenium (pytest) | RF (robot) | pytest + Playwright |
|------|:-----------------:|:----------:|:-------------------:|
| 登录 | ✅ | ✅ | — |
| Alert 弹窗 | ✅ | ✅ | — |
| 下拉框 | ✅ | ✅ | — |
| 文件上传 | ✅ | ✅ | — |
| 评论区 | ✅ | ✅ | — |
| 多窗口 | ✅ | ✅ | — |
| Tab 导航 | — | ✅ | ✅ |
| iFrame | — | ✅ | ✅ |
| 任务表格 | — | ✅ | ✅ |
| 进度条 | — | ✅ | ✅ |
| 通知系统 | — | ✅ | ✅ |
| 倒计时器 | — | ✅ | ✅ |

## 框架对比

| | Selenium + pytest | Robot Framework |
|---|---|---|
| 编程语言 | Python | DSL（关键字） |
| 报告 | Allure | Robot 原生 + Allure |
| 并行 | pytest-xdist | pabot |
| 学习曲线 | 需 Python 基础 | 非程序员友好 |
| 数据驱动 | pytest fixtures | RF Variables |

## 原始项目

本项目源自 [gdw1986/selenium-pom-test-framework](https://github.com/gdw1986/selenium-pom-test-framework)，新增 Robot Framework + Playwright 框架作为扩展。
