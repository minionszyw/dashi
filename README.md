# 大师AI命理小程序

一个基于AI的命理分析微信小程序，提供八字排盘、智能对话、命理分析等功能。

## ✨ 特性

- 🤖 **AI智能对话**：基于LangChain/LangGraph的AI命理分析
- 📊 **八字排盘**：精准的八字计算和真太阳时校正
- 💬 **会话管理**：支持多会话历史记录
- 💰 **Token计费**：灵活的积分充值系统
- 📱 **多端支持**：微信小程序、H5、App
- 🎨 **流畅体验**：WhatsApp级的流畅交互体验

## 🏗️ 技术栈

### 前端
- uni-app (Vue 3 + TypeScript)
- Pinia (状态管理)
- Vite (构建工具)

### 后端
- FastAPI (Python 3.12+)
- SQLAlchemy 2.0 (ORM)
- PostgreSQL 15 (数据库)
- Redis 7 (缓存)
- LangChain + LangGraph (AI框架)

### AI服务
- OpenAI GPT-4/GPT-3.5
- 支持切换国内大模型

## 📁 项目结构

```
dashi/
├── docs/               # 文档
├── frontend/           # 前端代码
├── backend/            # 后端代码（包含.env.example）
└── docker-compose.yml  # Docker开发环境
```

## 📋 当前进度

### ✅ 已完成（可立即运行）

#### 项目基础（100%）
- [x] 完整的项目目录结构
- [x] 详尽的文档（README、规范、设计、开发、部署）
- [x] Docker开发环境（一键启动）
- [x] 环境变量配置

#### 后端开发（100%）
- [x] FastAPI应用架构
- [x] 5个数据库模型（User、Conversation、Message、BaziProfile、Order）
- [x] 20+个API接口（认证、用户、八字、对话）
- [x] 服务层（微信、八字、LangChain）
- [x] JWT认证和权限控制
- [x] Alembic数据库迁移

#### 前端开发（100%）
- [x] uni-app项目结构（Vue 3 + TypeScript）
- [x] API接口封装（request、auth、user、chat、bazi）
- [x] Pinia状态管理（user、chat、bazi）
- [x] 公共组件（MessageBubble、ChatInput、Loading）
- [x] 5个核心页面：
  - 登录页（微信授权）
  - 对话页（流式AI对话）
  - 会话列表页（管理会话）
  - 个人中心页（用户信息）
  - 八字排盘页（表单输入）
- [x] 路由和Tabbar配置

### 🚧 待完善（可选）

- [ ] AI对话功能优化（Prompt工程、上下文管理）
- [ ] 微信支付集成
- [ ] 更多八字分析功能
- [ ] UI/UX精细化调整

## 🚀 快速开始

### 前置要求
- Docker & Docker Compose
- Node.js 22+
- Python 3.12+
- 微信开发者工具

### ⚡ 一键启动

```bash
# 1. 启动所有服务
docker-compose up -d

# 2. 配置环境变量（首次运行）
cp backend/.env.example backend/.env
# 编辑 backend/.env 填入你的 OPENAI_API_KEY 和 WX_APPID

# 3. 启动前端
cd frontend && npm install && npm run dev:mp-weixin

# 4. 打开微信开发者工具，导入 frontend/dist/dev/mp-weixin
```

### ✅ 验证运行
- **后端API**: http://localhost:8000/docs
- **前端**: 微信开发者工具预览

> 详细的开发环境配置、常见问题解决，请查看 [开发文档](docs/development.md)

## 📖 文档

- [架构设计](docs/design.md)
- [开发文档](docs/development.md)
- [部署文档](docs/deploy.md)
- [开发规范](.cursor/rules/)
- [开发日志](CHANGELOG.md)

## 🔧 开发与部署

详细信息请查看：
- [开发文档](docs/development.md) - 环境配置、调试技巧、常见问题
- [部署文档](docs/deploy.md) - 生产环境部署、监控、安全加固

## 📝 许可证

[MIT License](LICENSE)

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系

如有问题，请联系：your-email@example.com

