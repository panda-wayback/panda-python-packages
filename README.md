# Panda Python Packages

## 安装

```bash
pip install panda_python_packages --index-url https://x-access-token:${GITHUB_TOKEN}@pypi.pkg.github.com/panda-wayback/
```

## 使用

```python
from panda_python_packages.utils import hello
print(hello())
```

## 发布
推送到 `main` 分支会自动触发 GitHub Actions 发布新版本到 GitHub Packages。

