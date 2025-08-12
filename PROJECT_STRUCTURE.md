# FastShell 项目结构

## 📁 目录组织

```
fastshell/
├── 📄 核心文件
│   ├── .gitignore              # Git忽略文件
│   ├── LICENSE                 # 开源许可证
│   ├── MANIFEST.in             # 打包清单
│   ├── README.md               # 项目概览
│   ├── pyproject.toml          # 项目配置
│   ├── poetry.lock             # 依赖锁定文件
│   └── run_tests.py            # 测试运行器
│
├── 📚 docs/                    # 文档目录
│   ├── README.md               # 详细使用文档
│   ├── USAGE.md                # 使用指南
│   ├── CHANGELOG.md            # 版本变更记录
│   └── PYDANTIC_INTEGRATION.md # Pydantic集成指南
│
├── 🎯 examples/                # 示例代码
│   ├── demo.py                 # 基础功能演示
│   ├── demo_pydantic.py        # Pydantic功能演示
│   └── example.py              # 更多实用示例
│
├── 🧪 tests/                   # 测试文件
│   ├── __init__.py             # 测试包初始化
│   ├── test_comprehensive_validation.py  # 全面验证测试
│   ├── test_new_union.py       # 新式Union语法测试
│   ├── test_pydantic_validation.py      # Pydantic功能测试
│   └── test_union_types.py     # Union类型测试
│
└── 🔧 fastshell/               # 核心库代码
    ├── __init__.py             # 包初始化
    ├── app.py                  # 主应用类
    ├── command.py              # 命令处理
    ├── completer.py            # 自动补全
    ├── decorators.py           # 装饰器
    ├── exceptions.py           # 异常定义
    ├── parser.py               # 参数解析
    ├── types.py                # 类型定义
    ├── utils.py                # 工具函数
    └── validation.py           # Pydantic验证
```

## 🎯 文件分类说明

### 📄 核心配置文件
- **README.md**: 项目概览和快速开始
- **pyproject.toml**: 项目配置、依赖管理
- **run_tests.py**: 统一测试运行器

### 📚 文档文件 (docs/)
- **README.md**: 详细的使用文档和API说明
- **USAGE.md**: 实用技巧和最佳实践
- **CHANGELOG.md**: 版本更新记录和新功能说明
- **PYDANTIC_INTEGRATION.md**: Pydantic集成的详细指南

### 🎯 示例代码 (examples/)
- **demo.py**: 基础功能演示，适合初学者
- **demo_pydantic.py**: Pydantic增强功能的完整演示
- **example.py**: 更多实际应用场景的示例

### 🧪 测试文件 (tests/)
- **test_comprehensive_validation.py**: 全面的验证功能测试
- **test_new_union.py**: Python 3.10+ 新式Union语法测试
- **test_pydantic_validation.py**: Pydantic特定功能测试
- **test_union_types.py**: 传统Union类型测试

### 🔧 核心库 (fastshell/)
- **app.py**: FastShell主应用类，应用入口
- **command.py**: 命令定义和执行逻辑
- **validation.py**: Pydantic增强验证系统
- **utils.py**: 类型转换和工具函数
- **parser.py**: 命令行参数解析
- **completer.py**: 自动补全功能

## 🚀 快速导航

### 开始使用
1. 查看 [README.md](README.md) 了解项目概览
2. 运行 `python examples/demo.py` 体验基础功能
3. 运行 `python examples/demo_pydantic.py --demo` 查看新功能

### 深入了解
1. 阅读 [docs/README.md](docs/README.md) 获取详细文档
2. 查看 [docs/PYDANTIC_INTEGRATION.md](docs/PYDANTIC_INTEGRATION.md) 了解新功能
3. 参考 [docs/USAGE.md](docs/USAGE.md) 学习最佳实践

### 开发和测试
1. 运行 `python run_tests.py` 执行所有测试
2. 查看 `tests/` 目录了解测试用例
3. 参考 `examples/` 目录学习使用方法

## 📈 项目特点

### ✅ 优势
- **清晰的目录结构**: 按功能分类，易于维护
- **完整的文档**: 从入门到高级使用的全面指南
- **丰富的示例**: 多个实际应用场景的演示
- **全面的测试**: 确保功能稳定性和可靠性
- **模块化设计**: 核心功能分离，便于扩展

### 🔄 版本管理
- 使用语义化版本控制
- 详细的变更日志记录
- 向后兼容性保证

### 🛠️ 开发友好
- 统一的测试运行器
- 清晰的代码组织
- 完善的类型注解
- 详细的错误处理

---

**注意**: 这个项目结构是经过精心设计的，旨在提供清晰、可维护和用户友好的开发体验。