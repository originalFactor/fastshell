#!/usr/bin/env python3
"""
全面测试FastShell的Pydantic增强类型验证功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Union, List, Optional, Dict, Any
from fastshell import FastShell
from fastshell.validation import ValidationConfig, set_validation_config

# 创建不同配置的FastShell实例
app_pydantic = FastShell(name="pydantic-enhanced", use_pydantic=True)
app_legacy = FastShell(name="legacy-validation", use_pydantic=False)

@app_pydantic.command()
def validate_email(email: str):
    """验证邮箱格式（演示Pydantic的字符串验证）。
    
    Args:
        email: 邮箱地址
    """
    # 简单的邮箱验证逻辑
    if '@' in email and '.' in email.split('@')[1]:
        print(f"[VALID] 有效邮箱: {email}")
        return True
    else:
        print(f"[INVALID] 无效邮箱: {email}")
        return False

@app_pydantic.command()
def process_numbers(numbers: List[int], operation: str = "sum"):
    """处理数字列表。
    
    Args:
        numbers: 整数列表
        operation: 操作类型 (sum, avg, max, min)
    """
    if operation == "sum":
        result = sum(numbers)
    elif operation == "avg":
        result = sum(numbers) / len(numbers)
    elif operation == "max":
        result = max(numbers)
    elif operation == "min":
        result = min(numbers)
    else:
        result = "未知操作"
    
    print(f"[RESULT] {operation}({numbers}) = {result}")
    return result

@app_pydantic.command()
def flexible_input(value: Union[int, float, str], convert_to: str = "auto"):
    """灵活的输入处理，展示Union类型的强大功能。
    
    Args:
        value: 可以是整数、浮点数或字符串
        convert_to: 转换目标类型 (int, float, str, auto)
    """
    original_type = type(value).__name__
    
    if convert_to == "auto":
        result = value
        target_type = original_type
    elif convert_to == "int":
        result = int(float(str(value)))
        target_type = "int"
    elif convert_to == "float":
        result = float(str(value))
        target_type = "float"
    elif convert_to == "str":
        result = str(value)
        target_type = "str"
    else:
        result = value
        target_type = original_type
    
    print(f"[CONVERT] 输入: {value} ({original_type}) → 输出: {result} ({target_type})")
    return result

@app_pydantic.command()
def new_union_syntax(data: int | str | float, format_output: bool = True):
    """测试Python 3.10+的新式Union语法。
    
    Args:
        data: 可以是整数、字符串或浮点数
        format_output: 是否格式化输出
    """
    data_type = type(data).__name__
    
    if format_output:
        if isinstance(data, int):
            output = f"整数: {data:,}"
        elif isinstance(data, float):
            output = f"浮点数: {data:.2f}"
        else:
            output = f"字符串: '{data}'"
    else:
        output = str(data)
    
    print(f"🆕 新式Union处理: {output} (类型: {data_type})")
    return output

@app_pydantic.command()
def optional_params(name: Optional[str] = None, age: Optional[int] = None, active: bool = True):
    """测试可选参数处理。
    
    Args:
        name: 可选的姓名
        age: 可选的年龄
        active: 是否活跃状态
    """
    info = []
    if name:
        info.append(f"姓名: {name}")
    if age is not None:
        info.append(f"年龄: {age}")
    info.append(f"状态: {'活跃' if active else '非活跃'}")
    
    result = ", ".join(info)
    print(f"👤 用户信息: {result}")
    return result

def run_validation_tests():
    """运行验证测试"""
    print("开始全面验证测试...\n")
    
    test_cases = [
        # 基本类型测试
        ("flexible_input", ["123"], "整数字符串转换"),
        ("flexible_input", ["123.45"], "浮点数字符串转换"),
        ("flexible_input", ["hello"], "纯字符串处理"),
        
        # 新式Union语法测试
        ("new_union_syntax", ["42"], "新式Union - 整数"),
        ("new_union_syntax", ["3.14"], "新式Union - 浮点数"),
        ("new_union_syntax", ["text"], "新式Union - 字符串"),
        
        # 可选参数测试
        ("optional_params", [], "全部使用默认值"),
        ("optional_params", ["--name", "Alice"], "仅提供姓名"),
        ("optional_params", ["--name", "Bob", "--age", "25"], "提供姓名和年龄"),
        ("optional_params", ["--age", "30", "--active", "false"], "年龄和状态"),
        
        # 邮箱验证测试
        ("validate_email", ["user@example.com"], "有效邮箱"),
        ("validate_email", ["invalid-email"], "无效邮箱"),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for cmd_name, args, description in test_cases:
        try:
            cmd_line = f"{cmd_name} {' '.join(args)}"
            print(f"[TEST] 测试: {description}")
            print(f"   命令: {cmd_line}")
            result = app_pydantic.execute_command(cmd_line)
            print(f"   [PASS] 成功\n")
            success_count += 1
        except Exception as e:
            print(f"   [FAIL] 失败: {e}\n")
    
    print(f"[SUMMARY] 测试结果: {success_count}/{total_count} 通过")
    return success_count == total_count

def run_error_handling_tests():
    """测试错误处理"""
    print("\n[ERROR] 错误处理测试...\n")
    
    error_test_cases = [
        ("flexible_input", ["abc", "--convert_to", "int"], "字符串转整数失败"),
        ("new_union_syntax", ["--format_output", "invalid_bool"], "无效布尔值"),
        ("optional_params", ["--age", "not_a_number"], "无效年龄"),
    ]
    
    for cmd_name, args, description in error_test_cases:
        try:
            cmd_line = f"{cmd_name} {' '.join(args)}"
            print(f"[ERROR_TEST] 错误测试: {description}")
            print(f"   命令: {cmd_line}")
            result = app_pydantic.execute_command(cmd_line)
            print(f"   [UNEXPECTED] 意外成功: {result}\n")
        except Exception as e:
            print(f"   [EXPECTED] 正确捕获错误: {e}\n")

def compare_validation_systems():
    """对比Pydantic和传统验证系统"""
    print("\n[COMPARE] 验证系统对比...\n")
    
    # 创建对比命令
    @app_legacy.command()
    def legacy_test(value: Union[int, str] = "default"):
        print(f"传统验证: {value} ({type(value).__name__})")
        return value
    
    @app_pydantic.command()
    def pydantic_test(value: Union[int, str] = "default"):
        print(f"Pydantic验证: {value} ({type(value).__name__})")
        return value
    
    test_values = ["123", "hello", "45.67"]
    
    for value in test_values:
        print(f"[TEST] 测试值: {value}")
        
        try:
            print("   传统系统:")
            app_legacy.execute_command(f"legacy_test {value}")
        except Exception as e:
            print(f"   传统系统错误: {e}")
        
        try:
            print("   Pydantic系统:")
            app_pydantic.execute_command(f"pydantic_test {value}")
        except Exception as e:
            print(f"   Pydantic系统错误: {e}")
        
        print()

if __name__ == "__main__":
    print("FastShell Pydantic增强验证系统测试")
    print("=" * 50)
    
    # 运行基本验证测试
    validation_success = run_validation_tests()
    
    # 运行错误处理测试
    run_error_handling_tests()
    
    # 对比验证系统
    compare_validation_systems()
    
    print("=" * 50)
    if validation_success:
        print("所有测试通过！Pydantic集成成功！")
    else:
        print("[WARNING] 部分测试失败，需要进一步调试。")
    
    print("\n[INFO] 使用说明:")
    print("- 创建FastShell实例时使用 use_pydantic=True 启用Pydantic验证")
    print("- 创建FastShell实例时使用 use_pydantic=False 使用传统验证")
    print("- Pydantic提供更好的错误消息和类型转换")
    print("- 支持Python 3.10+的新式Union语法 (int | str)")
    print("- 支持复杂类型如List[int], Optional[str]等")