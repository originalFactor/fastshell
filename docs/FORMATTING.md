# FastShell 输出格式化指南

## 概述

FastShell 提供了强大的自动输出格式化功能，可以将命令的返回值以美观、易读的方式显示。系统支持多种格式化选项，并能根据数据类型自动选择最佳的显示方式。

## 功能特点

### ✨ 自动格式检测
- **智能分析**: 根据返回值类型自动选择最佳格式
- **类型感知**: 针对不同数据结构优化显示效果
- **美观输出**: 使用 Rich 库提供彩色、结构化的输出

### 🎨 多种格式选项
- **auto**: 自动选择最佳格式（默认）
- **json**: JSON 格式，带语法高亮
- **table**: 表格格式，适合列表和字典
- **tree**: 树形结构，适合嵌套数据
- **plain**: 纯文本格式
- **pretty**: 美化的 Python 对象显示

## 使用方法

### 基本使用

```python
from fastshell import FastShell

# 创建应用时指定默认格式
app = FastShell(
    name="my-app",
    output_format="auto"  # 默认格式
)

@app.command()
def get_data():
    return {"name": "FastShell", "version": "1.0.0"}

# 运行应用
app.run_interactive()
```

### 交互式格式切换

在交互模式中，可以动态更改输出格式：

```bash
# 查看当前格式
my-app> format

# 切换到 JSON 格式
my-app> format json

# 切换到表格格式
my-app> format table

# 切换回自动格式
my-app> format auto
```

## 格式化效果示例

### 1. 自动格式 (auto)

**简单值**:
```
14:30:25 ✓ str: Hello, FastShell!
14:30:25 ✓ int: 42
14:30:25 ✓ bool: true
```

**小型数据结构**:
```
14:30:25 ✓ dict: {name: FastShell, version: 1.0.0, active: true}
14:30:25 ✓ list: [apple, banana, cherry]
```

**大型数据结构**: 自动切换到 pretty 或 tree 格式

### 2. JSON 格式 (json)

```json
╭─ JSON Output ─╮
│ {             │
│   "name": "FastShell",
│   "version": "1.0.0",
│   "active": true
│ }             │
╰───────────────╯
```

### 3. 表格格式 (table)

**字典数据**:
```
      Command Result
┏━━━━━━━━━┳━━━━━━━━━━━┓
┃ Key     ┃ Value     ┃
┡━━━━━━━━━╇━━━━━━━━━━━┩
│ name    │ FastShell │
│ version │ 1.0.0     │
│ active  │ True      │
└─────────┴───────────┘
```

**列表数据**:
```
         Command Result
┏━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Index ┃ Value         ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 0     │ Alice         │
│ 1     │ Bob           │
│ 2     │ Charlie       │
└───────┴───────────────┘
```

### 4. 树形格式 (tree)

```
Command Result
├── user_id: 12345
├── username: demo_user
├── profile (dict)
│   ├── first_name: Demo
│   ├── last_name: User
│   └── preferences (dict)
│       ├── theme: dark
│       └── language: zh-CN
└── permissions (list[3])
    ├── [0]: read
    ├── [1]: write
    └── [2]: execute
```

### 5. 美化格式 (pretty)

```python
{
    'name': 'FastShell',
    'version': '1.0.0',
    'features': [
        'auto-completion',
        'type-validation',
        'rich-output'
    ],
    'active': True
}
```

## 自动格式选择规则

### 数据类型检测

| 数据类型 | 自动选择的格式 | 说明 |
|----------|----------------|------|
| `str`, `int`, `float`, `bool` | plain | 简单值直接显示 |
| 小型 `dict` (≤3 键) | auto | 内联显示 |
| 大型 `dict` (>3 键) | tree | 树形结构显示 |
| 小型 `list` (≤5 项) | auto | 内联显示 |
| 大型 `list` (>5 项) | pretty | 美化显示 |
| `List[Dict]` | table | 表格显示 |
| JSON 字符串 | json | 语法高亮显示 |
| 嵌套结构 | tree | 树形结构显示 |

### 特殊处理

- **空数据**: 显示为 `empty`
- **None 值**: 不显示任何输出
- **时间戳**: 自动添加到输出头部
- **类型信息**: 显示数据类型和元信息

## 编程接口

### 手动格式化

```python
from fastshell.formatter import ResultFormatter, OutputFormat
from rich.console import Console

console = Console()
formatter = ResultFormatter(console, OutputFormat.JSON)

# 格式化输出
data = {"name": "test", "value": 123}
formatter.format_result(data)

# 临时使用不同格式
formatter.format_result(data, OutputFormat.TABLE)
```

### 自定义格式化器

```python
from fastshell.formatter import create_formatter

# 创建自定义格式化器
formatter = create_formatter(console, "json")

# 在应用中使用
app = FastShell()
app.formatter = formatter
```

## 配置选项

### 应用级配置

```python
app = FastShell(
    name="my-app",
    output_format="auto",  # 默认格式
    use_pydantic=True      # 启用类型验证
)
```

### 运行时配置

```python
# 更改默认格式
app.set_output_format("json")

# 获取可用格式
formats = app.get_available_formats()
print(formats)  # ['auto', 'json', 'table', 'tree', 'plain', 'pretty']
```

## 最佳实践

### 1. 命令设计

**推荐**: 返回结构化数据
```python
@app.command()
def get_user_info(user_id: int):
    return {
        "user_id": user_id,
        "name": "Alice",
        "email": "alice@example.com",
        "active": True
    }
```

**避免**: 只打印不返回
```python
@app.command()
def bad_command(name: str):
    print(f"Hello, {name}!")  # 不会被格式化
    # 应该返回数据
```

### 2. 数据结构

**表格数据**: 使用字典列表
```python
return [
    {"id": 1, "name": "Alice", "score": 95},
    {"id": 2, "name": "Bob", "score": 87}
]
```

**层次数据**: 使用嵌套字典
```python
return {
    "company": {
        "name": "Tech Corp",
        "departments": {
            "engineering": {"head": "John", "size": 10},
            "marketing": {"head": "Jane", "size": 5}
        }
    }
}
```

### 3. 格式选择

- **开发调试**: 使用 `pretty` 格式
- **数据展示**: 使用 `table` 格式
- **API 输出**: 使用 `json` 格式
- **层次结构**: 使用 `tree` 格式
- **一般使用**: 使用 `auto` 格式

## 故障排除

### 常见问题

**Q: 命令没有格式化输出？**
A: 检查命令是否返回了值（不是 None）

**Q: 格式化效果不理想？**
A: 尝试手动指定格式类型，或调整数据结构

**Q: 中文显示有问题？**
A: 确保终端支持 UTF-8 编码

**Q: 输出太长被截断？**
A: 使用 `tree` 或 `json` 格式，或优化数据结构

### 调试技巧

```python
# 测试不同格式
formats = ["auto", "json", "table", "tree", "pretty"]
for fmt in formats:
    print(f"\n=== {fmt.upper()} ===")
    app.set_output_format(fmt)
    app.execute_command("your_command")
```

## 扩展功能

### 自定义格式化器

可以继承 `ResultFormatter` 类来创建自定义格式化器：

```python
from fastshell.formatter import ResultFormatter

class CustomFormatter(ResultFormatter):
    def _format_custom(self, result):
        # 自定义格式化逻辑
        self.console.print(f"[bold]Custom: {result}[/bold]")
```

### 插件支持

未来版本将支持格式化插件系统，允许第三方扩展格式化功能。

---

**提示**: 格式化功能基于 [Rich](https://rich.readthedocs.io/) 库，支持丰富的样式和布局选项。