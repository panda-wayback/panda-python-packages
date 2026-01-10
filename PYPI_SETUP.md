# PyPI 发布配置指南

本项目的 Python 包会发布到 PyPI，这样用户可以直接使用 `pip install panda-python-packages` 安装。

## 🔑 配置 PyPI API Token

### 1. 创建 PyPI API Token

#### 正式 PyPI (推荐)

1. 访问：https://pypi.org/manage/account/token/
2. 点击 **Add API token**
3. 填写：
   - **Token name**: `github-actions-publish` (可自定义)
   - **Scope**: 选择 **Entire account** 或 **Project: panda-python-packages**
4. 点击 **Add token**
5. **复制生成的 token**（只显示一次！格式类似：`pypi-AgEIcGl...`）

#### TestPyPI (用于测试)

1. 访问：https://test.pypi.org/manage/account/token/
2. 重复上述步骤创建测试 token
3. **注意**：TestPyPI 需要单独注册账户：https://test.pypi.org/account/register/

### 2. 在 GitHub 仓库中添加 Secrets

1. 访问你的仓库：`https://github.com/panda-wayback/panda-python-packages`
2. 进入 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**

   **对于正式 PyPI：**
   - Name: `PYPI_API_TOKEN`
   - Secret: 粘贴刚才复制的正式 PyPI token
   - 点击 **Add secret**

   **对于 TestPyPI（可选，用于测试）：**
   - Name: `TEST_PYPI_API_TOKEN`
   - Secret: 粘贴 TestPyPI token
   - 点击 **Add secret**

## 🚀 发布流程

### 自动发布（推荐）

1. **更新版本号**：在 `pyproject.toml` 中更新 `version` 字段
2. **提交并推送**：
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.1.0"
   git push
   ```
3. **创建并推送 tag**：
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. **自动触发**：推送 tag 后，GitHub Actions 会自动：
   - 构建包（wheel + source distribution）
   - 上传到正式 PyPI
   - 完成后，用户可以直接 `pip install panda-python-packages` 安装

### 手动发布

1. 访问仓库的 **Actions** 页面
2. 选择 **Publish to PyPI** workflow
3. 点击 **Run workflow**
4. 选择要上传的仓库：
   - `testpypi`：上传到测试 PyPI（用于测试）
   - `pypi`：上传到正式 PyPI（生产环境）
5. 点击 **Run workflow**

## 📦 安装方式

### 正式 PyPI（发布后）

```bash
# 直接安装，无需任何配置
pip install panda-python-packages
```

### TestPyPI（测试版本）

```bash
# 从测试索引安装
pip install -i https://test.pypi.org/simple/ panda-python-packages
```

## ✅ 验证发布

发布后，可以在以下地址查看：

- **正式 PyPI**: https://pypi.org/project/panda-python-packages/
- **TestPyPI**: https://test.pypi.org/project/panda-python-packages/

## 🔒 安全提示

- ✅ **不要**将 API token 提交到代码仓库
- ✅ **不要**在日志中打印 token
- ✅ token 只存储在 GitHub Secrets 中
- ✅ 如果 token 泄露，立即在 PyPI 管理页面撤销并重新创建

## ❓ 常见问题

### Q: 为什么上传失败？

**A:** 检查以下几点：
1. 是否正确配置了 `PYPI_API_TOKEN` secret？
2. 版本号是否已经存在于 PyPI？（每个版本只能发布一次）
3. 包名是否符合 PyPI 规范？

### Q: 如何更新版本？

**A:** 
1. 修改 `pyproject.toml` 中的 `version` 字段
2. 创建新的 tag：`git tag v新版本号`
3. 推送 tag：`git push origin v新版本号`

### Q: TestPyPI 和正式 PyPI 的区别？

**A:**
- **TestPyPI**: 用于测试发布流程，可以重复上传相同版本
- **正式 PyPI**: 生产环境，每个版本只能发布一次，永久保存

### Q: 如何回退版本？

**A:** PyPI 不支持删除已发布的版本，但可以发布新版本修复问题。如果版本有问题，建议立即发布修复版本。
