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

## ✨ 主要特性

- 🚀 **FastAPI风格装饰器** - 简单直观的API设计
- 🛡️ **Pydantic验证** - 增强的类型验证和错误处理
- 🔧 **自动补全** - 命令和参数的智能补全
- 📊 **自动格式化** - 智能识别数据类型，自动选择最佳显示格式
- 🌳 **子命令支持** - 嵌套命令结构
- 🖥️ **跨平台** - 支持Windows、macOS和Linux

## 🎯 示例

### 格式化输出示例

查看 `examples/` 目录中的示例代码

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用 GNU General Public License v3.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。