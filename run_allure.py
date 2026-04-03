#!/usr/bin/env python3
"""
Allure报告运行脚本

使用方法:
    python run_allure.py              # 运行测试并生成Allure报告
    python run_allure.py --serve      # 运行测试并启动Allure服务器
    python run_allure.py --clean      # 清理历史报告数据后运行
    python run_allure.py --history    # 保留历史趋势数据
"""

import argparse
import subprocess
import sys
import os
import shutil


def run_command(cmd, description=""):
    """运行命令并输出结果"""
    if description:
        print(f"\n{'='*60}")
        print(f"📌 {description}")
        print('='*60)
    
    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def clean_allure_results():
    """清理Allure结果目录"""
    dirs_to_clean = ['allure-results', 'allure-report']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)


def main():
    parser = argparse.ArgumentParser(description='运行测试并生成Allure报告')
    parser.add_argument('--serve', action='store_true', 
                        help='生成报告后启动Allure服务器')
    parser.add_argument('--clean', action='store_true',
                        help='清理历史报告数据')
    parser.add_argument('--history', action='store_true',
                        help='保留历史趋势数据（用于趋势图）')
    parser.add_argument('--browser', default='chrome',
                        help='选择浏览器 (chrome/firefox)')
    parser.add_argument('--headless', action='store_true',
                        help='启用无头模式')
    parser.add_argument('--tests', default='tests/',
                        help='指定测试目录或文件')
    
    args = parser.parse_args()
    
    # 清理历史数据（如果需要）
    if args.clean:
        clean_allure_results()
    
    # 构建pytest命令
    pytest_cmd = [
        'python', '-m', 'pytest',
        args.tests,
        '-v',
        '--alluredir=allure-results',
        f'--browser={args.browser}'
    ]
    
    if args.headless:
        pytest_cmd.append('--headless')
    
    # 运行测试
    if not run_command(pytest_cmd, "运行测试并生成Allure结果"):
        print("\n⚠️  部分测试失败，继续生成报告...")
    
    # 处理历史数据
    if args.history and os.path.exists('allure-report/history'):
        print("\n复制历史数据...")
        os.makedirs('allure-results', exist_ok=True)
        if os.path.exists('allure-results/history'):
            shutil.rmtree('allure-results/history')
        shutil.copytree('allure-report/history', 'allure-results/history')
    
    # 生成Allure报告
    allure_generate_cmd = [
        'allure', 'generate', 'allure-results',
        '-o', 'allure-report',
        '--clean'
    ]
    
    if not run_command(allure_generate_cmd, "生成Allure HTML报告"):
        print("\n❌ 生成报告失败，请确保已安装Allure命令行工具")
        print("安装方法: brew install allure (macOS)")
        print("          scoop install allure (Windows)")
        sys.exit(1)
    
    print(f"\n✅ 报告已生成: allure-report/index.html")
    
    # 启动Allure服务器（如果需要）
    if args.serve:
        run_command(['allure', 'serve', 'allure-results'], "启动Allure服务器")
    else:
        print("\n💡 使用以下命令启动报告服务器:")
        print("   allure serve allure-results")
        print("\n💡 或直接打开报告文件:")
        print("   open allure-report/index.html")


if __name__ == "__main__":
    main()
