# Changelog

All notable changes to FastShell will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-19

### 🎉 Major Features Added

#### Pydantic Integration
- **NEW**: Integrated Pydantic for enhanced type validation and conversion
- **NEW**: Added `use_pydantic` parameter to `FastShell` class (defaults to `True`)
- **NEW**: Enhanced error messages with more detailed validation feedback
- **NEW**: Configurable validation system - choose between Pydantic and legacy validation

#### Python 3.10+ Union Syntax Support
- **FIXED**: Resolved `'types.UnionType' object has no attribute '__name__'` error
- **NEW**: Full support for modern Union syntax (`int | str`, `str | None`)
- **NEW**: Backward compatibility with traditional `Union[int, str]` and `Optional[str]` syntax
- **NEW**: Enhanced `format_type_name` function to handle `types.UnionType`

### 🔧 Technical Improvements

#### Core Enhancements
- **IMPROVED**: `convert_value` function now handles `types.UnionType` objects
- **IMPROVED**: Better type conversion logic with Pydantic validation
- **IMPROVED**: Enhanced error handling and user feedback
- **NEW**: Added `ValidationConfig` class for global validation settings
- **NEW**: Added `EnhancedValidator` class with Pydantic integration

#### Dependencies
- **ADDED**: Pydantic (>=2.0.0,<3.0.0) as a core dependency
- **UPDATED**: Enhanced `pyproject.toml` with new dependency

### 📁 New Files

- `fastshell/validation.py` - Pydantic validation system
- `PYDANTIC_INTEGRATION.md` - Comprehensive integration guide
- `demo_pydantic.py` - Interactive demo showcasing new features
- `test_pydantic_validation.py` - Pydantic-specific tests
- `test_comprehensive_validation.py` - Full validation test suite
- `test_new_union.py` - New Union syntax tests
- `CHANGELOG.md` - This changelog file

### 🧪 Testing

- **NEW**: Comprehensive test suite for Pydantic integration
- **NEW**: Tests for new-style Union types (`int | str`)
- **NEW**: Error handling validation tests
- **NEW**: Comparison tests between Pydantic and legacy validation
- **IMPROVED**: Enhanced test coverage for type conversion edge cases

### 📚 Documentation

- **UPDATED**: README.md with Pydantic integration information
- **NEW**: Detailed Pydantic integration guide
- **NEW**: Migration guide for existing users
- **NEW**: Configuration examples and best practices
- **NEW**: Troubleshooting section for common issues

### 🔄 Breaking Changes

**None** - This release is fully backward compatible. Existing FastShell applications will continue to work without any modifications.

### 🐛 Bug Fixes

- **FIXED**: `AttributeError: 'types.UnionType' object has no attribute '__name__'` when using Python 3.10+ Union syntax
- **FIXED**: Type conversion issues with complex Union types
- **IMPROVED**: Better handling of Optional parameters
- **IMPROVED**: More consistent type conversion behavior

### ⚡ Performance

- **OPTIMIZED**: Type validation performance with Pydantic caching
- **IMPROVED**: Reduced overhead for simple type conversions
- **ADDED**: Option to disable Pydantic for performance-critical applications

### 🎯 Usage Examples

#### Before (v1.x)
```python
# This would cause an error in Python 3.10+
@app.command()
def process(value: int | str):  # ❌ AttributeError
    pass
```

#### After (v2.0)
```python
# Now fully supported!
@app.command()
def process(value: int | str):  # ✅ Works perfectly
    pass

# Enhanced validation
app = FastShell(use_pydantic=True)  # Better error messages
app = FastShell(use_pydantic=False) # Legacy mode for performance
```

### 🔮 Future Plans

- Custom Pydantic validators
- Enhanced error message localization
- Performance optimizations
- Additional type validation features

---

## [1.0.0] - Previous Release

### Initial Features
- FastAPI-like decorators
- Automatic parsing of docstrings and type annotations
- Auto-completion support
- Subcommands structure
- Basic type conversion
- Cross-platform support
- Rich terminal output

---

**Note**: Version 2.0.0 represents a significant enhancement to FastShell while maintaining complete backward compatibility. All existing applications will continue to work seamlessly while gaining access to improved type validation and modern Python syntax support.