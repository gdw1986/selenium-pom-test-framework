#!/usr/bin/env python3
"""
并行运行测试脚本

使用方法:
    python run_parallel.py              # 自动检测CPU核心数并行运行
    python run_parallel.py -n 4         # 指定4个进程并行
    python run_parallel.py --allure     # 并行运行并生成Allure报告
    python run_parallel.py --dist load  # 按负载均衡分配测试

并行模式:
    --dist load     # 按负载均衡分配（默认，推荐）
    --dist no       # 每个进程独立收集测试
    --dist loadscope # 按作用域分组（如class）
"""

import argparse
import subprocess
import sys
import os
import multiprocessing


def get_cpu_count():
    """获取CPU核心数"""
    return multiprocessing.cpu_count()


def main():
    parser = argparse.ArgumentParser(description='并行运行测试')
    parser.add_argument('-n', '--numprocesses', default='auto',
                        help='并行进程数 (auto 或数字，默认: auto)')
    parser.add_argument('--dist', default='load',
                        choices=['load', 'no', 'loadscope', 'loadfile'],
                        help='测试分配策略 (默认: load)')
    parser.add_argument('--allure', action='store_true',
                        help='生成Allure报告')
    parser.add_argument('--clean', action='store_true',
                        help='清理历史报告数据')
    parser.add_argument('--browser', default='chrome',
                        help='选择浏览器 (chrome/firefox)')
    parser.add_argument('--headless', action='store_true',
                        help='启用无头模式')
    parser.add_argument('--tests', default='tests/',
                        help='指定测试目录或文件')
    parser.add_argument('--maxfail', type=int,
                        help='失败N次后停止')
    parser.add_argument('--local-driver', action='store_true',
                        help='使用本地WebDriver')
    
    args = parser.parse_args()
    
    # 确定进程数
    if args.numprocesses == 'auto':
        num_processes = get_cpu_count()
    else:
        num_processes = int(args.numprocesses)
    
    print("="*60)
    print(f"🚀 并行运行测试")
    print(f"   进程数: {num_processes}")
    print(f"   分配策略: {args.dist}")
    print(f"   浏览器: {args.browser}")
    print("="*60)
    
    # 清理历史数据
    if args.clean and args.allure:
        import shutil
        for dir_name in ['allure-results', 'allure-report']:
            if os.path.exists(dir_name):
                print(f"清理目录: {dir_name}")
                shutil.rmtree(dir_name)
    
    # 构建pytest命令
    pytest_cmd = [
        sys.executable, '-m', 'pytest',
        args.tests,
        '-v',
        f'-n={num_processes}',
        f'--dist={args.dist}',
        f'--browser={args.browser}'
    ]
    
    if args.headless:
        pytest_cmd.append('--headless')
    
    if args.local_driver:
        pytest_cmd.append('--local-driver')
    
    if args.maxfail:
        pytest_cmd.append(f'--maxfail={args.maxfail}')
    
    if args.allure:
        pytest_cmd.append('--alluredir=allure-results')
    
    # 运行测试
    print(f"\n执行: {' '.join(pytest_cmd)}\n")
    result = subprocess.run(pytest_cmd)
    
    # 生成Allure报告
    if args.allure and result.returncode in [0, 1]:  # 0=成功, 1=部分失败
        print("\n" + "="*60)
        print("生成Allure报告...")
        print("="*60)
        
        gen_result = subprocess.run([
            'allure', 'generate', 'allure-results',
            '-o', 'allure-report',
            '--clean'
        ])
        
        if gen_result.returncode == 0:
            print(f"✅ 报告已生成: allure-report/index.html")
            print("\n💡 启动Allure服务器查看报告:")
            print("   allure serve allure-results")
        else:
            print("❌ 生成报告失败")
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
