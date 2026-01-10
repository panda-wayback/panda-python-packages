# Panda Python Packages

一个 Python 工具包集合，用于 Panda 项目。

## 📦 安装

### 从 PyPI 安装（推荐）

```bash
pip install panda-python-packages
```

### 从 GitHub 安装（开发版）

```bash
pip install git+https://github.com/panda-wayback/panda-python-packages.git
```

## 🚀 使用

```python
from panda_python_packages.utils import hello
print(hello())
```

## 📝 发布

包会发布到 PyPI。发布流程：

1. **更新版本号**：在 `pyproject.toml` 中更新 `version`
2. **创建并推送 tag**：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. **自动发布**：推送 tag 后，GitHub Actions 会自动构建并上传到 PyPI

详细配置请参考 [PYPI_SETUP.md](PYPI_SETUP.md)

## 🔧 开发

```bash
# 克隆仓库
git clone https://github.com/panda-wayback/panda-python-packages.git
cd panda-python-packages

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

