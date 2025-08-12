#!/usr/bin/env python3
"""
测试Pydantic增强的类型验证功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Union, List, Optional
from fastshell import FastShell

# 创建启用Pydantic的FastShell实例
app_pydantic = FastShell(name="pydantic-test", use_pydantic=True)

# 创建禁用Pydantic的FastShell实例用于对比
app_legacy = FastShell(name="legacy-test", use_pydantic=False)

@app_pydantic.command()
def test_union_pydantic(value: Union[int, str] = "default"):
    """测试Union类型参数（Pydantic版本）。
    
    Args:
        value: 可以是整数或字符串
    """
    print(f"Pydantic - Received value: {value} (type: {type(value).__name__})")
    return value

@app_legacy.command()
def test_union_legacy(value: Union[int, str] = "default"):
    """测试Union类型参数（传统版本）。
    
    Args:
        value: 可以是整数或字符串
    """
    print(f"Legacy - Received value: {value} (type: {type(value).__name__})")
    return value

@app_pydantic.command()
def test_new_union_pydantic(value: int | str = "default"):
    """测试新式Union类型参数（Pydantic版本）。
    
    Args:
        value: 可以是整数或字符串
    """
    print(f"Pydantic New Union - Received value: {value} (type: {type(value).__name__})")
    return value

@app_pydantic.command()
def test_optional_pydantic(name: Optional[str] = None):
    """测试Optional类型参数（Pydantic版本）。
    
    Args:
        name: 可选的名称
    """
    if name is None:
        print("Pydantic - No name provided")
    else:
        print(f"Pydantic - Hello, {name}!")
    return name

@app_pydantic.command()
def test_list_pydantic(numbers: List[int]):
    """测试List类型参数（Pydantic版本）。
    
    Args:
        numbers: 整数列表
    """
    total = sum(numbers)
    print(f"Pydantic - Sum of {numbers} = {total}")
    return total

@app_pydantic.command()
def test_complex_pydantic(age: int, score: float, active: bool = True):
    """测试复杂类型组合（Pydantic版本）。
    
    Args:
        age: 年龄（整数）
        score: 分数（浮点数）
        active: 是否活跃（布尔值）
    """
    print(f"Pydantic - Age: {age}, Score: {score}, Active: {active}")
    return {"age": age, "score": score, "active": active}

def test_error_handling():
    """测试错误处理和错误消息质量"""
    print("\n=== 测试错误处理 ===")
    
    test_cases = [
        ("test_union_pydantic", ["123"]),  # 应该成功
        ("test_union_pydantic", ["hello"]),  # 应该成功
        ("test_new_union_pydantic", ["456"]),  # 应该成功
        ("test_complex_pydantic", ["25", "95.5", "true"]),  # 应该成功
        ("test_complex_pydantic", ["invalid_age", "95.5", "true"]),  # 应该失败
        ("test_complex_pydantic", ["25", "invalid_score", "true"]),  # 应该失败
        ("test_complex_pydantic", ["25", "95.5", "invalid_bool"]),  # 应该失败
    ]
    
    for cmd_name, args in test_cases:
        try:
            cmd_line = f"{cmd_name} {' '.join(args)}"
            print(f"\n执行: {cmd_line}")
            result = app_pydantic.execute_command(cmd_line)
            print(f"成功: {result}")
        except Exception as e:
            print(f"错误: {e}")

def test_comparison():
    """对比Pydantic和传统验证的差异"""
    print("\n=== 对比Pydantic和传统验证 ===")
    
    test_cases = [
        ("test_union_pydantic", "test_union_legacy", ["123"]),
        ("test_union_pydantic", "test_union_legacy", ["hello"]),
    ]
    
    for pydantic_cmd, legacy_cmd, args in test_cases:
        cmd_line_args = ' '.join(args)
        print(f"\n测试参数: {cmd_line_args}")
        
        try:
            print("Pydantic版本:")
            app_pydantic.execute_command(f"{pydantic_cmd} {cmd_line_args}")
        except Exception as e:
            print(f"Pydantic错误: {e}")
        
        try:
            print("传统版本:")
            app_legacy.execute_command(f"{legacy_cmd} {cmd_line_args}")
        except Exception as e:
            print(f"传统错误: {e}")

if __name__ == "__main__":
    print("测试Pydantic增强的类型验证...")
    
    # 基本功能测试
    print("\n=== 基本功能测试 ===")
    try:
        print("\n1. 测试Union类型:")
        app_pydantic.execute_command("test_union_pydantic 123")
        app_pydantic.execute_command("test_union_pydantic hello")
        
        print("\n2. 测试新式Union类型:")
        app_pydantic.execute_command("test_new_union_pydantic 456")
        app_pydantic.execute_command("test_new_union_pydantic world")
        
        print("\n3. 测试Optional类型:")
        app_pydantic.execute_command("test_optional_pydantic")
        app_pydantic.execute_command("test_optional_pydantic Alice")
        
        print("\n4. 测试复杂类型:")
        app_pydantic.execute_command("test_complex_pydantic 25 95.5 true")
        app_pydantic.execute_command("test_complex_pydantic 30 88.0 false")
        
    except Exception as e:
        print(f"基本测试错误: {e}")
        import traceback
        traceback.print_exc()
    
    # 错误处理测试
    test_error_handling()
    
    # 对比测试
    test_comparison()
    
    print("\n测试完成!")