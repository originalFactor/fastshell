# FastShell Pydantic 集成指南

## 概述

FastShell 现在集成了 Pydantic 来提供增强的类型验证功能。这个集成解决了原有类型系统的限制，特别是对 Python 3.10+ 新式 Union 类型（`int | str`）的支持问题。

## 主要特性

### ✅ 已解决的问题

1. **新式 Union 类型支持**
   - 修复了 `'types.UnionType' object has no attribute '__name__'` 错误
   - 完全支持 Python 3.10+ 的 `int | str` 语法
   - 向后兼容传统的 `Union[int, str]` 语法

2. **增强的类型验证**
   - 使用 Pydantic 提供更准确的类型转换
   - 更好的错误消息和错误处理
   - 支持复杂类型如 `List[int]`, `Optional[str]` 等

3. **灵活的配置选项**
   - 可以选择启用或禁用 Pydantic 验证
   - 保持与现有代码的完全兼容性

## 安装和配置

### 依赖项

Pydantic 已添加到项目依赖中：

```toml
# pyproject.toml
dependencies = [
    "prompt-toolkit (>=3.0.0,<4.0.0)",
    "rich (>=13.0.0,<15.0.0)",
    "typing-extensions (>=4.0.0,<5.0.0)",
    "pydantic (>=2.0.0,<3.0.0)"  # 新增
]
```

### 基本使用

```python
from fastshell import FastShell

# 启用 Pydantic 验证（默认）
app = FastShell(name="my-app", use_pydantic=True)

# 禁用 Pydantic 验证（使用传统验证）
app_legacy = FastShell(name="my-app", use_pydantic=False)
```

## 支持的类型

### 1. 基本类型

```python
@app.command()
def basic_types(name: str, age: int, score: float, active: bool):
    """支持所有基本 Python 类型"""
    pass
```

### 2. Union 类型（传统语法）

```python
@app.command()
def union_traditional(value: Union[int, str] = "default"):
    """传统 Union 语法"""
    pass
```

### 3. 新式 Union 类型（Python 3.10+）

```python
@app.command()
def union_modern(value: int | str = "default"):
    """新式 Union 语法 - 现在完全支持！"""
    pass
```

### 4. Optional 类型

```python
@app.command()
def optional_params(name: Optional[str] = None, age: str | None = None):
    """可选参数支持"""
    pass
```

### 5. 复杂类型

```python
@app.command()
def complex_types(numbers: List[int], data: Dict[str, Any]):
    """复杂类型支持（需要自定义解析）"""
    pass
```

## 错误处理改进

### Pydantic 验证错误消息

```python
# 输入: my_command invalid_number
# Pydantic 错误: Cannot convert to integer: invalid literal for int() with base 10: 'invalid_number'
# 传统错误: Type conversion error: invalid literal for int() with base 10: 'invalid_number'
```

### 类型转换示例

```python
@app.command()
def type_conversion_demo(value: int | str | float):
    """演示类型转换"""
    print(f"接收到: {value} (类型: {type(value).__name__})")
    return value

# 使用示例:
# $ my_command 123      # 转换为 int
# $ my_command hello    # 保持为 str  
# $ my_command 3.14     # 转换为 float
```

## 配置选项

### 全局配置

```python
from fastshell.validation import ValidationConfig, set_validation_config

# 设置全局验证配置
config = ValidationConfig(
    use_pydantic=True,
    strict_mode=False  # 允许类型强制转换
)
set_validation_config(config)
```

### 命令级别配置

```python
# 在创建命令时指定验证方式
command = Command.from_function(
    my_function, 
    "my_command", 
    use_pydantic=True  # 覆盖全局设置
)
```

## 迁移指南

### 从传统验证迁移到 Pydantic

1. **无需更改现有代码**
   ```python
   # 现有代码无需修改
   @app.command()
   def existing_command(value: Union[int, str]):
       pass
   ```

2. **启用 Pydantic**
   ```python
   # 只需在创建 FastShell 实例时启用
   app = FastShell(use_pydantic=True)
   ```

3. **使用新式语法**
   ```python
   # 可以开始使用新式 Union 语法
   @app.command()
   def new_style_command(value: int | str):
       pass
   ```

## 性能考虑

- **Pydantic 验证**: 提供更准确的验证，但可能有轻微的性能开销
- **传统验证**: 更快的执行速度，适合性能敏感的应用
- **建议**: 对于大多数应用，Pydantic 的性能开销是可以接受的

## 故障排除

### 常见问题

1. **`'types.UnionType' object has no attribute '__name__'`**
   - ✅ 已修复！现在完全支持新式 Union 类型

2. **类型转换失败**
   ```python
   # 检查是否启用了 Pydantic
   app = FastShell(use_pydantic=True)
   ```

3. **意外的类型转换行为**
   ```python
   # 可以禁用 Pydantic 使用传统验证
   app = FastShell(use_pydantic=False)
   ```

### 调试技巧

```python
# 启用详细错误信息
try:
    app.execute_command("my_command invalid_input")
except Exception as e:
    print(f"错误详情: {e}")
    import traceback
    traceback.print_exc()
```

## 测试

项目包含了全面的测试文件：

- `test_union_types.py` - 基本 Union 类型测试
- `test_new_union.py` - 新式 Union 语法测试
- `test_pydantic_validation.py` - Pydantic 功能测试
- `test_comprehensive_validation.py` - 全面的验证测试

运行测试：

```bash
python test_comprehensive_validation.py
```

## 未来计划

- [ ] 支持更多 Pydantic 验证器
- [ ] 自定义验证规则
- [ ] 更好的错误消息本地化
- [ ] 性能优化

## 贡献

如果您发现任何问题或有改进建议，请提交 Issue 或 Pull Request。

---

**注意**: 这个集成完全向后兼容，现有的 FastShell 应用无需任何修改即可继续工作。