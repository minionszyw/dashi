# 部署指南

## 🔐 GitHub认证配置

由于项目需要推送到GitHub，您需要配置认证凭证。有两种方式：

### 方式一：使用GitHub Personal Access Token（推荐）

1. **创建Personal Access Token**
   - 访问：https://github.com/settings/tokens
   - 点击 "Generate new token" → "Generate new token (classic)"
   - 设置名称：`dashi-project`
   - 选择权限：勾选 `repo` (完整仓库访问权限)
   - 点击 "Generate token"
   - **复制生成的token（只显示一次）**

2. **推送代码**
   ```bash
   cd /home/w/dashi
   git push -u origin main
   ```
   - Username: `minionszyw`
   - Password: `粘贴你的Personal Access Token`

### 方式二：使用SSH密钥

1. **生成SSH密钥**
   ```bash
   ssh-keygen -t ed25519 -C "minionszyw@gmail.com"
   # 按回车使用默认路径，设置密码（或留空）
   ```

2. **添加SSH密钥到GitHub**
   ```bash
   # 复制公钥
   cat ~/.ssh/id_ed25519.pub
   ```
   - 访问：https://github.com/settings/keys
   - 点击 "New SSH key"
   - 粘贴公钥内容

3. **更改远程仓库URL为SSH**
   ```bash
   cd /home/w/dashi
   git remote set-url origin git@github.com:minionszyw/dashi.git
   git push -u origin main
   ```

## 📦 当前状态

✅ 已完成：
- Git仓库初始化
- 用户信息配置（minionszyw / minionszyw@gmail.com）
- 本地提交完成（2个commits）
- 远程仓库配置（origin → https://github.com/minionszyw/dashi.git）

⏳ 待完成：
- GitHub认证配置
- 代码推送

## 🚀 快速推送命令

完成认证配置后，执行：

```bash
cd /home/w/dashi
git push -u origin main
```

推送成功后，访问：https://github.com/minionszyw/dashi 查看项目

