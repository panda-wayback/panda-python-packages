# 测试说明

## 运行测试

### 安装测试依赖

```bash
pip install -e ".[test]"
```

或者直接安装 pytest：

```bash
pip install pytest pytest-cov
```

### 运行所有测试

```bash
pytest
```

### 运行测试并显示覆盖率

```bash
pytest --cov=src/panda_python_packages --cov-report=html
```

### 运行特定测试文件

```bash
pytest tests/test_singleton.py
```

### 运行特定测试类或函数

```bash
pytest tests/test_singleton.py::TestSingleton::test_basic_singleton
```

## 测试覆盖范围

- ✅ 基本单例功能
- ✅ 带参数的 `__init__` 方法
- ✅ 状态共享
- ✅ 多个单例类
- ✅ 线程安全性
- ✅ 继承场景
- ✅ `singleton` 和 `singleton_class` 功能等价性
