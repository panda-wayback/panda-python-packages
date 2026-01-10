# Panda Python Packages

这是一个集成的 Python 工具库。

## 安装

```bash
pip install panda-python-packages --index-url https://x-access-token:${GITHUB_TOKEN}@pypi.pkg.github.com/panda-wayback/panda-python-packages
```

## 使用

```python
from panda_python_packages.utils import hello
print(hello())
```

## 发布
推送到 `main` 分支会自动触发 GitHub Actions 发布新版本到 GitHub Packages。

