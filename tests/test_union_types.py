#!/usr/bin/env python3
"""
测试Union类型处理
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Union, Optional
from fastshell import FastShell

app = FastShell(name="union-test")

@app.command()
def test_union(value: Union[int, str] = "default"):
    """测试Union类型参数。
    
    Args:
        value: 可以是整数或字符串
    """
    print(f"Received value: {value} (type: {type(value).__name__})")
    return value

@app.command()
def test_optional(name: Union[str, None] = None):
    """测试Optional类型参数。
    
    Args:
        name: 可选的名称
    """
    if name is None:
        print("No name provided")
    else:
        print(f"Hello, {name}!")
    return name

if __name__ == "__main__":
    print("Testing Union types...")
    
    try:
        # 测试Union[int, str]
        print("\n1. Testing Union[int, str]:")
        app.execute_command("test_union 123")
        app.execute_command("test_union hello")
        
        # 测试Optional (Union[str, None])
        print("\n2. Testing Optional (Union[str, None]):")
        app.execute_command("test_optional")
        app.execute_command("test_optional Alice")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()