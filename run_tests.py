#!/usr/bin/env python3
"""
测试运行脚本
提供多种运行方式
"""
import argparse
import subprocess
import sys


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("运行所有测试")
    print("=" * 50)
    result = subprocess.run(["pytest", "-v"])
    return result.returncode


def run_test_by_module(module_name: str):
    """按模块运行测试"""
    print(f"运行模块: {module_name}")
    result = subprocess.run(["pytest", f"tests/test_{module_name}.py", "-v"])
    return result.returncode


def run_with_browser(browser: str, headless: bool = False):
    """指定浏览器运行测试"""
    print(f"使用浏览器: {browser}")
    cmd = ["pytest", "-v", f"--browser={browser}"]
    if headless:
        cmd.append("--headless")
    result = subprocess.run(cmd)
    return result.returncode


def run_smoke_tests():
    """运行冒烟测试"""
    print("=" * 50)
    print("运行冒烟测试")
    print("=" * 50)
    result = subprocess.run(["pytest", "-v", "-m", "smoke"])
    return result.returncode


def run_with_report():
    """运行测试并生成HTML报告"""
    print("=" * 50)
    print("运行测试并生成HTML报告")
    print("=" * 50)
    result = subprocess.run([
        "pytest", 
        "-v",
        "--html=report.html",
        "--self-contained-html"
    ])
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Selenium测试运行脚本")
    parser.add_argument(
        "--module", "-m",
        choices=["login", "alert", "dropdown", "file_upload", "comments", "windows"],
        help="指定要运行的测试模块"
    )
    parser.add_argument(
        "--browser", "-b",
        choices=["chrome", "firefox"],
        default="chrome",
        help="指定浏览器（默认: chrome）"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="启用无头模式"
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="只运行冒烟测试"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="生成HTML测试报告"
    )
    
    args = parser.parse_args()
    
    if args.smoke:
        return run_smoke_tests()
    elif args.report:
        return run_with_report()
    elif args.module:
        return run_test_by_module(args.module)
    else:
        if args.browser != "chrome" or args.headless:
            return run_with_browser(args.browser, args.headless)
        else:
            return run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
