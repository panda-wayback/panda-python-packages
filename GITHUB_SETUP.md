# GitHub Packages 配置检查清单

## 📋 请检查以下 GitHub 仓库设置：

### 1. 仓库设置检查
- [ ] 进入仓库的 **Settings** → **General**
- [ ] 确认 **Features** 部分中的 **Packages** 是否已启用
- [ ] 如果未启用，请启用它

### 2. Actions 权限检查
- [ ] 进入 **Settings** → **Actions** → **General**
- [ ] 确认 **Workflow permissions** 设置为 **Read and write permissions**
- [ ] 确认勾选了 **Allow GitHub Actions to create and approve pull requests**

### 3. 包权限检查
- [ ] 进入 **Settings** → **Actions** → **General** → **Workflow permissions**
- [ ] 确认 **Packages** 权限已授予（这通常由 workflow 文件中的 `permissions: packages: write` 控制）

### 4. 手动创建第一个包（如果需要）
如果以上都正确，但依然 404，可能需要：
1. 手动在 GitHub 上创建一个包：
   - 访问：`https://github.com/panda-wayback?tab=packages`
   - 或者直接访问：`https://github.com/orgs/panda-wayback/packages`
2. 如果包不存在，GitHub Packages 可能不会自动创建

## 🔧 临时解决方案

如果 GitHub Packages 持续有问题，可以考虑：
1. 使用 GitHub Releases 上传构建产物（虽然不能直接 pip install，但可以作为分发渠道）
2. 使用私有 PyPI 服务器（如 devpi、pypiserver）
3. 使用 Artifactory 或其他包管理服务
