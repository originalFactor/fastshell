# FastShell

A FastAPI-like framework for building interactive shell applications with automatic completion, type conversion, and subcommands.

## 🚀 Quick Start

```bash
pip install fastshell
```

```python
from fastshell import FastShell

app = FastShell(use_pydantic=True)

@app.command()
def hello(name: str = "World", count: int = 1):
    """Say hello to someone."""
    for _ in range(count):
        print(f"Hello, {name}!")

if __name__ == "__main__":
    app.run()
```

## 📁 Project Structure

```
fastshell/
├── fastshell/          # 核心库代码
├── docs/              # 文档文件
│   ├── README.md      # 详细文档
│   ├── USAGE.md       # 使用指南
│   ├── CHANGELOG.md   # 变更日志
│   └── PYDANTIC_INTEGRATION.md  # Pydantic集成指南
├── examples/          # 示例代码
│   ├── demo.py        # 基础演示
│   ├── demo_pydantic.py  # Pydantic功能演示
│   └── example.py     # 更多示例
├── tests/             # 测试文件
│   ├── test_*.py      # 各种测试
└── pyproject.toml     # 项目配置
```

## ✨ 主要特性

- 🚀 **FastAPI风格装饰器** - 简单直观的API设计
- 🆕 **现代Union语法** - 完全支持Python 3.10+ `int | str`语法
- 🛡️ **Pydantic验证** - 增强的类型验证和错误处理
- 🔧 **自动补全** - 命令和参数的智能补全
- 📊 **自动格式化** - 智能识别数据类型，自动选择最佳显示格式
- 🌳 **子命令支持** - 嵌套命令结构
- 🖥️ **跨平台** - 支持Windows、macOS和Linux

## 📚 文档

- [详细文档](docs/README.md) - 完整的使用指南
- [Pydantic集成](docs/PYDANTIC_INTEGRATION.md) - 类型验证增强功能
- [输出格式化指南](docs/FORMATTING.md) - 自动格式化功能详解
- [使用指南](docs/USAGE.md) - 实用技巧和最佳实践
- [变更日志](docs/CHANGELOG.md) - 版本更新记录

## 🎯 示例

### 基础示例

```bash
# 运行基础功能演示
python examples/demo.py

# 运行 Pydantic 功能演示
python examples/demo_pydantic.py --demo

# 运行格式化输出演示
python examples/demo_formatter.py --demo

# 查看更多示例
python examples/example.py
```

### 格式化输出示例

```python
from fastshell import FastShell

app = FastShell(output_format="auto")

@app.command()
def get_users():
    return [
        {"id": 1, "name": "Alice", "age": 25},
        {"id": 2, "name": "Bob", "age": 30}
    ]

# 自动以表格格式显示
app.run_interactive()
```

在交互模式中：
```bash
my-app> get_users
# 自动显示为表格格式

my-app> format json
# 切换到 JSON 格式

my-app> get_users
# 现在以 JSON 格式显示
```

查看 `examples/` 目录中的示例代码：

- `demo.py` - 基础功能演示
- `demo_pydantic.py` - Pydantic增强功能演示
- `demo_formatter.py` - 格式化输出演示
- `example.py` - 更多实用示例

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python tests/test_comprehensive_validation.py
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。