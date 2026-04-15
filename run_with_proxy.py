#!/usr/bin/env python3
"""
带代理的测试运行脚本

使用方法:
    python run_with_proxy.py              # 使用系统代理环境变量
    python run_with_proxy.py --serve      # 生成Allure报告并启动服务器
    
设置代理（Windows PowerShell）:
    $env:HTTP_PROXY="http://127.0.0.1:7890"
    $env:HTTPS_PROXY="http://127.0.0.1:7890"
    python run_with_proxy.py

设置代理（Windows CMD）:
    set HTTP_PROXY=http://127.0.0.1:7890
    set HTTPS_PROXY=http://127.0.0.1:7890
    python run_with_proxy.py
"""

import argparse
import subprocess
import sys
import os


def check_proxy():
    """检查代理设置"""
    http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    
    if http_proxy or https_proxy:
        print(f"✓ 检测到代理设置:")
        print(f"  HTTP_PROXY: {http_proxy or '未设置'}")
        print(f"  HTTPS_PROXY: {https_proxy or '未设置'}")
    else:
        print("⚠ 未检测到代理环境变量")
        print("  如需使用代理，请先设置环境变量:")
        print("  Windows PowerShell: $env:HTTP_PROXY=\"http://127.0.0.1:7890\"")
        print("  Windows CMD: set HTTP_PROXY=http://127.0.0.1:7890")
    
    return http_proxy or https_proxy


def main():
    parser = argparse.ArgumentParser(description='带代理运行测试')
    parser.add_argument('--serve', action='store_true', 
                        help='生成Allure报告并启动服务器')
    parser.add_argument('--clean', action='store_true',
                        help='清理历史报告数据')
    parser.add_argument('--history', action='store_true',
                        help='保留历史趋势数据')
    parser.add_argument('--browser', default='chrome',
                        help='选择浏览器 (chrome/firefox)')
    parser.add_argument('--headless', action='store_true',
                        help='启用无头模式')
    parser.add_argument('--tests', default='tests/',
                        help='指定测试目录或文件')
    parser.add_argument('--local-driver', action='store_true',
                        help='使用本地WebDriver')
    
    args = parser.parse_args()
    
    # 检查代理
    print("="*60)
    has_proxy = check_proxy()
    print("="*60)
    
    # 构建pytest命令
    pytest_cmd = [
        sys.executable, '-m', 'pytest',
        args.tests,
        '-v',
        '--alluredir=allure-results',
        f'--browser={args.browser}'
    ]
    
    if args.headless:
        pytest_cmd.append('--headless')
    
    if args.local_driver:
        pytest_cmd.append('--local-driver')
    
    # 运行测试
    print(f"\n运行: {' '.join(pytest_cmd)}\n")
    result = subprocess.run(pytest_cmd)
    
    if result.returncode != 0:
        print("\n⚠️  部分测试失败")
    
    # 处理Allure报告
    if not args.local_driver:
        import shutil
        
        if args.clean:
            print("\n清理历史数据...")
            for dir_name in ['allure-results', 'allure-report']:
                if os.path.exists(dir_name):
                    shutil.rmtree(dir_name)
        
        if args.history and os.path.exists('allure-report/history'):
            print("复制历史数据...")
            os.makedirs('allure-results', exist_ok=True)
            if os.path.exists('allure-results/history'):
                shutil.rmtree('allure-results/history')
            shutil.copytree('allure-report/history', 'allure-results/history')
        
        # 生成报告
        print("\n生成Allure报告...")
        gen_result = subprocess.run([
            'allure', 'generate', 'allure-results',
            '-o', 'allure-report',
            '--clean'
        ])
        
        if gen_result.returncode == 0:
            print(f"✅ 报告已生成: allure-report/index.html")
            
            if args.serve:
                print("\n启动Allure服务器...")
                subprocess.run(['allure', 'serve', 'allure-results'])
        else:
            print("❌ 生成报告失败，请确保已安装Allure命令行工具")


if __name__ == "__main__":
    main()
