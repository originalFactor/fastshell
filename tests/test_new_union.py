#!/usr/bin/env python3
"""
测试新式Union类型（Python 3.10+语法）
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastshell import FastShell

app = FastShell(name="new-union-test")

@app.command()
def test_new_union(value: int | str = "default"):
    """测试新式Union类型参数。
    
    Args:
        value: 可以是整数或字符串
    """
    print(f"Received value: {value} (type: {type(value).__name__})")
    return value

@app.command()
def test_new_optional(name: str | None = None):
    """测试新式Optional类型参数。
    
    Args:
        name: 可选的名称
    """
    if name is None:
        print("No name provided")
    else:
        print(f"Hello, {name}!")
    return name

if __name__ == "__main__":
    print("Testing new Union types...")
    
    try:
        # 测试新式Union[int, str]
        print("\n1. Testing new Union (int | str):")
        app.execute_command("test_new_union 123")
        app.execute_command("test_new_union hello")
        
        # 测试新式Optional (str | None)
        print("\n2. Testing new Optional (str | None):")
        app.execute_command("test_new_optional")
        app.execute_command("test_new_optional Alice")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()