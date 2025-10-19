# 更新日志

所有重要的项目变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

## [1.1.0] - 2025-10-19

### 新增
- ✨ 用户资料编辑功能（头像、昵称）
- ✨ 系统设置功能（AI上下文条数、对话模式选择）
- 🎯 用户ID基于OpenID生成8位数字
- 🎨 Session页面右下角悬浮管理按钮

### 优化
- 🔧 Chat页输入区布局优化（发送按钮始终可见，无输入时灰色）
- 🔧 Session页时间戳显示优化（相对时间格式）
- 🔧 MessageBubble组件优化（用户头像正确显示在右侧）
- 🔧 Profile页界面优化（合并菜单项，余额显示为￥格式）

### 修复
- 🐛 修复用户登录时OpenID未返回的问题
- 🐛 修复八字排盘表单验证缺失导致400错误
- 🐛 修复清空对话后消息持久化问题
- 🐛 修复`get_current_user`导入路径错误
- 🐛 移除pages.json中过时的rpxCalc配置

### 技术改进
- 📝 添加`UpdateUserRequest`后端Schema
- 📝 添加`PUT /api/v1/auth/user`接口
- 🎨 新增两个前端页面：`pages/profile/edit`、`pages/profile/settings`
- 🔧 用户初始余额调整为100元（10000分）

## [1.0.0] - 2025-10-18

### 新增
- ✨ AI命理对话功能（基于LangChain/LangGraph）
- ✨ 八字排盘计算（真太阳时校正）
- ✨ 微信小程序登录
- ✨ 会话管理（创建、查看、删除）
- ✨ Token计费系统（新用户100初始余额）
- 📱 响应式UI设计（WhatsApp级流畅体验）
- 🎨 流式AI对话（SSE实时响应）

### 技术架构
- **前端**：uni-app + Vue 3 + TypeScript + Pinia + Vite
- **后端**：FastAPI + SQLAlchemy 2.0 + PostgreSQL 15 + Redis 7
- **AI**：LangChain + LangGraph + OpenAI GPT-4/3.5
- **部署**：Docker + Docker Compose
- **数据库**：5个核心模型（User、Conversation、Message、BaziProfile、Order）
- **API**：20+个RESTful接口

### 项目成果
- 📁 完整的项目结构（backend + frontend + docs）
- 📚 详尽的文档体系（设计、开发、部署、规范）
- 🐳 Docker开发环境（一键启动）
- ✅ 可运行的Demo（核心功能已实现）
- 📄 约6000行代码 + 20000字文档

### 修复
- 🔧 删除重复的根目录 `.env.example`，统一使用 `backend/.env.example`
- 🔧 完善 `frontend/tsconfig.json` 配置（添加uni-app类型定义、编译选项优化）
- 🔧 优化文档结构（精简为6个核心文档）

### 已知问题
- ⚠️ 微信支付功能待实现（需要商户号）
- ⚠️ AI Prompt工程需要进一步优化
- ⚠️ 部分UI细节待精细化调整

---

## 版本说明

- **未发布**：正在开发中的功能
- **[版本号]**：已发布的版本
- **新增**：新功能
- **变更**：现有功能的变更
- **弃用**：即将移除的功能
- **移除**：已移除的功能
- **修复**：问题修复
- **安全**：安全相关的修复

