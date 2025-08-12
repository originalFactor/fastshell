#!/usr/bin/env python3
"""演示 FastShell 的自动格式化输出功能。"""

import sys
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastshell import FastShell

# 创建应用实例
app = FastShell(
    name="formatter-demo",
    description="演示 FastShell 的格式化输出功能",
    use_pydantic=True,
    output_format="auto"  # 默认自动格式化
)


@app.command()
def simple_string() -> str:
    """返回简单字符串。"""
    return "Hello, FastShell with formatting!"


@app.command()
def simple_number() -> int:
    """返回数字。"""
    return 42


@app.command()
def simple_boolean() -> bool:
    """返回布尔值。"""
    return True


@app.command()
def simple_list() -> List[str]:
    """返回简单列表。"""
    return ["apple", "banana", "cherry", "date"]


@app.command()
def large_list() -> List[int]:
    """返回大列表。"""
    return list(range(1, 21))  # 1-20


@app.command()
def simple_dict() -> Dict[str, Any]:
    """返回简单字典。"""
    return {
        "name": "FastShell",
        "version": "1.0.0",
        "active": True
    }


@app.command()
def large_dict() -> Dict[str, Any]:
    """返回复杂字典。"""
    return {
        "user_id": 12345,
        "username": "demo_user",
        "email": "demo@example.com",
        "profile": {
            "first_name": "Demo",
            "last_name": "User",
            "age": 25,
            "preferences": {
                "theme": "dark",
                "language": "zh-CN",
                "notifications": True
            }
        },
        "permissions": ["read", "write", "execute"],
        "last_login": "2024-01-15T10:30:00Z",
        "is_active": True,
        "metadata": {
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "login_count": 156
        }
    }


@app.command()
def table_data() -> List[Dict[str, Any]]:
    """返回适合表格显示的数据。"""
    return [
        {"id": 1, "name": "Alice", "age": 25, "city": "Beijing", "score": 95.5},
        {"id": 2, "name": "Bob", "age": 30, "city": "Shanghai", "score": 87.2},
        {"id": 3, "name": "Charlie", "age": 28, "city": "Guangzhou", "score": 92.8},
        {"id": 4, "name": "Diana", "age": 26, "city": "Shenzhen", "score": 89.1},
        {"id": 5, "name": "Eve", "age": 32, "city": "Hangzhou", "score": 94.3}
    ]


@app.command()
def json_string() -> str:
    """返回 JSON 字符串。"""
    import json
    data = {
        "status": "success",
        "data": {
            "items": [
                {"id": 1, "name": "Item 1", "value": 100},
                {"id": 2, "name": "Item 2", "value": 200}
            ],
            "total": 2
        },
        "timestamp": datetime.now().isoformat()
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


@app.command()
def nested_structure() -> Dict[str, Any]:
    """返回嵌套结构数据。"""
    return {
        "company": {
            "name": "Tech Corp",
            "founded": 2010,
            "departments": {
                "engineering": {
                    "head": "John Doe",
                    "employees": [
                        {"name": "Alice", "role": "Senior Developer", "years": 5},
                        {"name": "Bob", "role": "DevOps Engineer", "years": 3}
                    ],
                    "projects": {
                        "project_a": {"status": "active", "progress": 75},
                        "project_b": {"status": "planning", "progress": 10}
                    }
                },
                "marketing": {
                    "head": "Jane Smith",
                    "employees": [
                        {"name": "Charlie", "role": "Marketing Manager", "years": 4},
                        {"name": "Diana", "role": "Content Creator", "years": 2}
                    ],
                    "campaigns": [
                        {"name": "Summer Sale", "budget": 50000, "roi": 2.5},
                        {"name": "Product Launch", "budget": 100000, "roi": 3.2}
                    ]
                }
            }
        }
    }


@app.command()
def empty_data() -> Dict[str, Any]:
    """返回空数据。"""
    return {}


@app.command()
def none_result() -> Optional[str]:
    """返回 None。"""
    return None


@app.command()
def demo_all_formats():
    """演示所有格式化选项。"""
    print("\n=== FastShell 格式化输出演示 ===")
    print("\n可用的命令:")
    print("  simple_string    - 简单字符串")
    print("  simple_number    - 数字")
    print("  simple_boolean   - 布尔值")
    print("  simple_list      - 简单列表")
    print("  large_list       - 大列表")
    print("  simple_dict      - 简单字典")
    print("  large_dict       - 复杂字典")
    print("  table_data       - 表格数据")
    print("  json_string      - JSON 字符串")
    print("  nested_structure - 嵌套结构")
    print("  empty_data       - 空数据")
    print("  none_result      - None 结果")
    
    print("\n可用的格式:")
    print("  auto   - 自动选择最佳格式")
    print("  json   - JSON 格式")
    print("  table  - 表格格式")
    print("  tree   - 树形结构")
    print("  plain  - 纯文本")
    print("  pretty - 美化输出")
    
    print("\n使用方法:")
    print("  1. 运行命令查看默认格式化输出")
    print("  2. 使用 'format <type>' 更改输出格式")
    print("  3. 使用 'format' 查看当前格式")
    print("  4. 尝试不同的命令和格式组合")
    
    print("\n示例:")
    print("  table_data        # 自动选择表格格式")
    print("  format json       # 切换到 JSON 格式")
    print("  large_dict        # 以 JSON 格式显示")
    print("  format tree       # 切换到树形格式")
    print("  nested_structure  # 以树形格式显示")
    
    return "演示说明已显示，请尝试上述命令！"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # 非交互式演示
        print("=== FastShell 格式化输出演示 ===")
        
        # 演示不同类型的输出
        test_commands = [
            ("simple_string", "字符串输出"),
            ("simple_number", "数字输出"),
            ("simple_list", "列表输出"),
            ("simple_dict", "字典输出"),
            ("table_data", "表格数据"),
            ("large_dict", "复杂字典")
        ]
        
        for cmd, desc in test_commands:
            print(f"\n--- {desc} ---")
            app.execute_command(cmd)
        
        print("\n=== 演示完成 ===")
        print("运行 'python demo_formatter.py' 进入交互模式体验更多功能")
    else:
        # 交互模式
        print("欢迎使用 FastShell 格式化输出演示！")
        print("输入 'demo_all_formats' 查看使用说明")
        app.run_interactive()