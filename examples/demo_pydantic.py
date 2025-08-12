#!/usr/bin/env python3
"""
FastShell Pydantic Integration Demo

这个演示展示了 FastShell 的 Pydantic 集成功能，包括：
- 新式 Union 语法支持 (Python 3.10+)
- 增强的类型验证
- 更好的错误处理
- 向后兼容性
"""

from typing import Union, Optional, List
from fastshell import FastShell

# 创建启用 Pydantic 的 FastShell 应用
app = FastShell(
    name="pydantic-demo",
    description="FastShell Pydantic Integration Demo",
    use_pydantic=True  # 启用 Pydantic 验证
)

@app.command()
def modern_union(value: int | str, optional: str | None = None):
    """演示新式 Union 语法 (Python 3.10+)。
    
    Args:
        value: 可以是整数或字符串
        optional: 可选的字符串参数
    """
    result = {
        "input_value": value,
        "input_type": type(value).__name__,
        "syntax": "modern (Python 3.10+)",
        "optional_param": optional,
        "validation_success": True
    }
    return result

@app.command()
def traditional_union(value: Union[int, str], optional: Optional[str] = None):
    """演示传统 Union 语法。
    
    Args:
        value: 可以是整数或字符串
        optional: 可选的字符串参数
    """
    result = {
        "input_value": value,
        "input_type": type(value).__name__,
        "syntax": "traditional (typing.Union)",
        "optional_param": optional,
        "validation_success": True
    }
    return result

@app.command()
def type_conversion(number: int, text: str, flag: bool, decimal: float):
    """演示基本类型转换。
    
    Args:
        number: 整数
        text: 字符串
        flag: 布尔值
        decimal: 浮点数
    """
    return {
        "conversion_results": {
            "integer": {"value": number, "type": type(number).__name__, "original_input": str(number)},
            "string": {"value": text, "type": type(text).__name__, "length": len(text)},
            "boolean": {"value": flag, "type": type(flag).__name__, "truthiness": bool(flag)},
            "float": {"value": decimal, "type": type(decimal).__name__, "rounded": round(decimal, 2)}
        },
        "summary": {
            "total_params": 4,
            "all_converted": True,
            "validation_method": "Pydantic"
        }
    }

@app.command()
def flexible_input(data: int | str | float, mode: str = "auto"):
    """演示灵活的输入处理。
    
    Args:
        data: 可以是整数、字符串或浮点数
        mode: 处理模式
    """
    print(f"🎯 灵活输入: {data} (类型: {type(data).__name__})")
    
    if isinstance(data, int):
        print(f"   处理整数: {data * 2}")
    elif isinstance(data, float):
        print(f"   处理浮点数: {data:.2f}")
    else:
        print(f"   处理字符串: '{data.upper()}'")

@app.command()
def optional_demo(name: str, age: int | None = None, active: bool = True):
    """演示可选参数处理。
    
    Args:
        name: 必需的名称
        age: 可选的年龄
        active: 是否激活（默认 True）
    """
    print(f"👤 用户信息:")
    print(f"   姓名: {name}")
    print(f"   年龄: {age if age is not None else '未提供'}")
    print(f"   状态: {'激活' if active else '未激活'}")

@app.command()
def error_demo(value: int):
    """演示错误处理（尝试传入无效的整数）。
    
    Args:
        value: 必须是有效的整数
    """
    print(f"✅ 成功转换: {value}")
    print(f"   类型: {type(value).__name__}")
    print(f"   值: {value}")

@app.command()
def complex_example(user_id: int, email: str, tags: str = "", priority: int | str = "normal"):
    """复杂的实际应用示例。
    
    Args:
        user_id: 用户ID
        email: 电子邮件地址
        tags: 标签（逗号分隔）
        priority: 优先级（数字或文本）
    """
    print(f"📋 用户处理:")
    print(f"   ID: {user_id}")
    print(f"   邮箱: {email}")
    
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        print(f"   标签: {tag_list}")
    
    print(f"   优先级: {priority} (类型: {type(priority).__name__})")

def demo_commands():
    """演示各种命令的使用"""
    print("🚀 FastShell Pydantic 集成演示\n")
    
    commands = [
        # 新式 Union 语法
        "modern_union 123",
        "modern_union hello",
        "modern_union 456 --optional world",
        
        # 传统 Union 语法
        "traditional_union 789",
        "traditional_union goodbye",
        
        # 类型转换
        "type_conversion 42 hello true 3.14",
        "type_conversion -10 'world' false 2.718",
        
        # 灵活输入
        "flexible_input 100",
        "flexible_input 3.14159",
        "flexible_input hello",
        
        # 可选参数
        "optional_demo Alice",
        "optional_demo Bob --age 25",
        "optional_demo Charlie --age 30 --active false",
        
        # 复杂示例
        "complex_example 1001 user@example.com",
        "complex_example 1002 admin@test.com --tags 'admin,vip' --priority high",
        "complex_example 1003 guest@demo.com --priority 5",
    ]
    
    print("📝 执行以下命令演示:\n")
    for cmd in commands:
        print(f"$ {cmd}")
        try:
            app.execute_command(cmd)
            print()
        except Exception as e:
            print(f"❌ 错误: {e}\n")
    
    # 错误处理演示
    print("[ERROR] 错误处理演示:\n")
    error_commands = [
        "error_demo invalid_number",  # 应该失败
        "error_demo 42",             # 应该成功
    ]
    
    for cmd in error_commands:
        print(f"$ {cmd}")
        try:
            app.execute_command(cmd)
            print()
        except Exception as e:
            print(f"❌ 预期错误: {e}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # 运行演示
        demo_commands()
    else:
        # 交互模式
        print("🎯 FastShell Pydantic 集成演示")
        print("💡 提示: 运行 'python demo_pydantic.py --demo' 查看自动演示")
        print("📚 可用命令: modern_union, traditional_union, type_conversion, flexible_input, optional_demo, error_demo, complex_example")
        print("🔍 使用 'help <command>' 查看命令帮助\n")
        app.run()