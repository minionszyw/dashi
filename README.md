# 国学大师 - AI命理分析小程序

<div align="center">

🔮 基于AI的智能命理分析微信小程序

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue-3.0+-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 📋 项目简介

国学大师是一个基于AI的命理分析微信小程序，为用户提供智能化的命理咨询服务。项目采用前后端分离架构，支持20+并发用户，采用token计费模式。

### ✨ 核心特性

- 🤖 **AI驱动对话** - 基于DeepSeek大模型的智能命理分析
- 💬 **多轮会话** - 支持上下文记忆的连续对话
- ⚡ **流式响应** - 实时流式输出，优化用户体验
- 🔐 **微信登录** - 便捷的微信授权登录
- 💰 **Token计费** - 灵活的按量计费系统
- 📊 **完整记录** - 对话历史和交易记录

## 🚀 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 微信开发者工具（前端开发）

### 5分钟启动

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/dashi.git
cd dashi

# 2. 配置环境变量
cp backend/.env.example .env
vim .env  # 填写必要配置

# 3. 一键启动
docker-compose up -d

# 4. 验证服务
curl http://localhost:8000/health
```

### 必要配置

编辑 `.env` 文件，填写以下配置：

```bash
# 微信配置（从微信公众平台获取）
WECHAT_APPID=your-wechat-appid
WECHAT_SECRET=your-wechat-secret

# DeepSeek配置（从DeepSeek平台获取）
DEEPSEEK_API_KEY=your-deepseek-api-key

# JWT密钥（生产环境必须修改）
JWT_SECRET_KEY=your-random-secret-key
```

### 访问服务

- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

### 前端开发

```bash
cd web
npm install
npm run dev:mp-weixin
```

使用微信开发者工具打开 `web/dist/dev/mp-weixin` 目录。

## 🏗️ 技术架构

```
微信小程序 (uni-app + Vue 3)
    ↓ HTTPS
Nginx (反向代理)
    ↓
FastAPI (API服务)
    ↓
PostgreSQL + Redis
    ↓
LangChain + DeepSeek AI
```

### 技术栈

**后端**: FastAPI + PostgreSQL + Redis + LangChain + DeepSeek  
**前端**: uni-app + Vue 3 + TypeScript + Vite  
**部署**: Docker + Docker Compose + Nginx

## 📚 功能清单

### 已实现功能

| 模块 | 功能 | 状态 |
|------|------|------|
| 认证 | 微信登录、JWT认证 | ✅ |
| 对话 | AI对话、多轮会话 | ✅ |
| 会话 | 创建、查看、删除 | ✅ |
| 计费 | Token扣费、余额查询 | ✅ |
| 交易 | 交易记录、充值订单 | ✅ |
| 个人 | 用户信息、统计数据、信息编辑 | ✅ |
| 管理 | AI风格管理、系统配置 | ✅ |

### 待实现功能

- [ ] 微信支付集成
- [ ] 流式对话前端
- [ ] 分享裂变
- [ ] 用户等级体系

## 📖 文档

- **[环境搭建](docs/SETUP.md)** - 详细的开发环境配置指南
- **[架构设计](docs/ARCHITECTURE.md)** - 系统架构和技术设计
- **[设计文档](docs/DESIGN.md)** - 完整的项目构思和规划
- **[更新日志](CHANGELOG.md)** - 版本变更记录

## 📡 API接口

### 认证模块
- `POST /api/v1/auth/wechat/login` - 微信登录
- `GET /api/v1/auth/user/info` - 获取用户信息
- `PUT /api/v1/auth/user/info` - 更新用户信息

### 对话模块
- `POST /api/v1/chat/sessions` - 创建会话
- `GET /api/v1/chat/sessions` - 会话列表
- `GET /api/v1/chat/sessions/{id}` - 会话详情
- `DELETE /api/v1/chat/sessions/{id}` - 删除会话
- `POST /api/v1/chat/messages` - 发送消息

### 计费模块
- `GET /api/v1/billing/balance` - 查询余额
- `GET /api/v1/billing/transactions` - 交易记录
- `POST /api/v1/billing/recharge` - 发起充值

### 管理模块
- `GET /api/v1/admin/prompts` - 获取AI风格列表
- `GET /api/v1/admin/prompts/{style}` - 获取指定风格内容

完整API文档: http://localhost:8000/docs

## 📁 项目结构

```
dashi/
├── backend/           # FastAPI后端
│   ├── app/          # 应用代码
│   ├── alembic/      # 数据库迁移
│   └── scripts/      # 工具脚本
├── web/              # uni-app前端
│   ├── src/          # 源代码
│   └── dist/         # 构建输出
├── nginx/            # Nginx配置
├── scripts/          # 部署脚本
└── docs/             # 项目文档
```

## 🛠️ 开发指南

### 本地开发

```bash
# 后端开发
cd backend
poetry install
poetry run uvicorn app.main:app --reload

# 前端开发
cd web
npm install
npm run dev:mp-weixin
```

### 代码规范

```bash
# Python格式化
cd backend
poetry run black .
poetry run flake8 .

# TypeScript格式化
cd web
npm run lint
```

### 数据库迁移

```bash
cd backend
poetry run alembic revision --autogenerate -m "description"
poetry run alembic upgrade head
```

## 🐳 Docker部署

### 开发环境

```bash
docker-compose up -d
```

### 生产环境

```bash
# 配置生产环境变量
export JWT_SECRET_KEY="production-secret"
export WECHAT_APPID="production-appid"
export DEEPSEEK_API_KEY="production-key"

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f api
```

## 🔧 常见问题

### Q: 数据库连接失败？
```bash
# 检查数据库状态
docker-compose ps db
docker-compose logs db
```

### Q: 微信登录失败？
检查 `.env` 文件中的 `WECHAT_APPID` 和 `WECHAT_SECRET` 是否正确。

### Q: AI调用失败？
检查 `DEEPSEEK_API_KEY` 是否有效，账户余额是否充足。

更多问题请查看 [环境搭建文档](docs/SETUP.md)。

## 💰 成本估算

### 开发阶段（月）
- 服务器: ¥50-100
- DeepSeek API: ¥50-200
- **合计**: ~¥150/月

### 运营阶段（月）
- 服务器: ¥100-200
- DeepSeek API: ¥500-2000
- 微信认证: ¥300/年
- **合计**: ¥600-2200/月

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📝 许可证

本项目采用 [MIT](LICENSE) 许可证。

## 👥 团队

- **开发者**: minionszyw
- **邮箱**: minionszyw@gmail.com

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [uni-app](https://uniapp.dcloud.io/) - 跨平台应用开发框架
- [LangChain](https://python.langchain.com/) - AI应用开发框架
- [DeepSeek](https://www.deepseek.com/) - AI大模型服务

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！

**当前状态**: 🟢 MVP完成，功能完善，可投入测试  
**版本**: v0.2.0
