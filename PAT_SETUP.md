# GitHub Packages 配置指南

## 🔑 关键步骤：配置 Personal Access Token (PAT)

### 1. 创建 PAT

1. 访问：https://github.com/settings/tokens
2. 点击 **Generate new token** → **Generate new token (classic)**
3. 设置以下权限：
   - ✅ `write:packages` - 上传包
   - ✅ `read:packages` - 读取包
   - ✅ `repo` - 访问仓库（如果仓库是私有）
4. 点击 **Generate token**
5. **复制生成的 token**（只显示一次！）

### 2. 在仓库中添加 Secret

1. 访问你的仓库：`https://github.com/panda-wayback/panda-python-packages`
2. 进入 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. Name: `GITHUB_PAT`
5. Secret: 粘贴刚才复制的 token
6. 点击 **Add secret**

### 3. 验证仓库设置

- [ ] 进入 **Settings** → **General** → 确认 **Features** 中的 **Packages** 已启用
- [ ] 进入 **Settings** → **Actions** → **General** → **Workflow permissions** 设置为 **Read and write permissions**

## 📦 上传说明

修复后的 workflow 使用：
- ✅ 正确端点：`https://upload.pypi.github.com/panda-wayback/panda-python-packages/`
- ✅ PAT 认证：通过 `GITHUB_PAT` secret
- ✅ 用户名：使用 `github.repository_owner`

完成以上配置后，推送代码到 `main` 分支即可自动发布！
