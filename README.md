# Panda Python Packages (panda-wayback)

这是一个集成的 Python 工具库，采用命名空间 (Namespace) 模式管理多个模块。

## 项目结构

- `src/panda/utils/`: 基础工具模块
- `src/panda/sys/`: 系统相关模块 (预留)

## 安装

```bash
pip install panda-wayback --index-url https://x-access-token:${GITHUB_TOKEN}@pypi.pkg.github.com/panda-wayback/panda-python-packages
```

## 使用

```python
from panda.utils import hello
print(hello())
```

## 发布
推送到 `main` 分支会自动触发 GitHub Actions 发布新版本到 GitHub Packages。

