#!/usr/bin/env python3
"""
FastShell 测试运行器

运行所有测试文件并生成测试报告。
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test_file(test_file):
    """运行单个测试文件"""
    print(f"\n{'='*60}")
    print(f"运行测试: {test_file.name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            cwd=test_file.parent.parent
        )
        
        if result.returncode == 0:
            print(f"[PASS] {test_file.name} - 通过")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"[FAIL] {test_file.name} - 失败")
            if result.stderr:
                print("错误输出:")
                print(result.stderr)
            if result.stdout:
                print("标准输出:")
                print(result.stdout)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"[ERROR] {test_file.name} - 运行异常: {e}")
        return False

def main():
    """主函数"""
    print("FastShell 测试套件")
    print("=" * 60)
    
    # 获取测试目录
    project_root = Path(__file__).parent
    tests_dir = project_root / "tests"
    
    if not tests_dir.exists():
        print("[ERROR] 测试目录不存在")
        return 1
    
    # 查找所有测试文件
    test_files = list(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("[ERROR] 未找到测试文件")
        return 1
    
    print(f"找到 {len(test_files)} 个测试文件:")
    for test_file in test_files:
        print(f"  - {test_file.name}")
    
    # 运行所有测试
    passed = 0
    failed = 0
    
    for test_file in test_files:
        if run_test_file(test_file):
            passed += 1
        else:
            failed += 1
    
    # 生成测试报告
    print(f"\n{'='*60}")
    print("测试报告")
    print(f"{'='*60}")
    print(f"总计: {len(test_files)} 个测试文件")
    print(f"[PASS] 通过: {passed}")
    print(f"[FAIL] 失败: {failed}")
    
    if failed == 0:
        print("\n所有测试通过！")
        return 0
    else:
        print(f"\n有 {failed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())