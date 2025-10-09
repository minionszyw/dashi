# 国学大师 - AI命理分析小程序

<div align="center">

🔮 基于AI的智能命理分析微信小程序

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue-3.0+-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 📋 项目简介

国学大师是一个基于AI的命理分析微信小程序，为用户提供智能化的命理咨询服务。项目采用前后端分离架构，支持20个并发用户，采用token计费模式。

### 核心特性

- 🤖 **AI驱动对话** - 基于DeepSeek大模型的智能命理分析
- 💬 **多轮会话** - 支持上下文记忆的连续对话
- ⚡ **流式响应** - 实时流式输出，优化用户体验
- 🔐 **微信登录** - 便捷的微信授权登录
- 💰 **Token计费** - 灵活的按量计费系统
- 📊 **数据统计** - 完善的用户数据和交易记录

## 🏗️ 技术架构

### 整体架构

```
┌─────────────┐
│  微信小程序  │  (uni-app + Vue 3 + TypeScript)
│   前端层    │
└──────┬──────┘
       │ HTTPS/WSS
       ↓
┌─────────────┐
│   Nginx     │  (反向代理 + SSL)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   FastAPI   │  (API服务)
│   后端层    │
└──────┬──────┘
       │
    ┌──┴──┐
    ↓     ↓
┌────────┐ ┌─────────────┐
│ Redis  │ │ PostgreSQL  │
│ (缓存) │ │  (主数据库) │
└────────┘ └─────────────┘
       │
       ↓
┌──────────────┐
│  LangChain   │
│  + DeepSeek  │
│   (AI层)     │
└──────────────┘
```

### 技术栈

#### 前端
- **框架**: uni-app 3.0
- **UI**: 自定义UI组件
- **语言**: TypeScript + Vue 3 Composition API
- **构建**: Vite

#### 后端
- **框架**: FastAPI 0.109+
- **数据库**: PostgreSQL 15 + SQLAlchemy 2.0 (async)
- **缓存**: Redis 7
- **AI**: LangChain + DeepSeek API
- **认证**: JWT

## 🚀 快速开始

### 环境要求

- Node.js 16+
- Python 3.11+
- Docker 20.10+ (可选)
- PostgreSQL 15+
- Redis 7+

### 一键启动（Docker）

```bash
# 克隆项目
git clone https://github.com/yourusername/dashi.git
cd dashi

# 配置环境变量
cp .env.example .env
vim .env  # 填写必要配置

# 启动所有服务
docker-compose up -d

# 查看运行状态
docker-compose ps
```

访问：
- API文档: http://localhost:8000/docs
- API服务: http://localhost:8000

### 手动启动

#### 1. 后端启动

```bash
cd backend

# 安装依赖
poetry install

# 配置环境变量
cp .env.example .env
vim .env

# 启动数据库（Docker）
docker-compose up -d db redis

# 初始化数据库
poetry run python scripts/init_db.py

# 启动服务
poetry run uvicorn app.main:app --reload
```

#### 2. 前端启动

```bash
cd web

# 安装依赖
npm install

# 配置环境变量
vim .env.development

# 启动开发服务器
npm run dev:mp-weixin
```

#### 3. 微信开发者工具

1. 打开微信开发者工具
2. 导入项目，选择 `web/dist/dev/mp-weixin` 目录
3. 配置AppID（可使用测试号）

## 📁 项目结构

```
dashi/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic模型
│   │   ├── services/    # 业务逻辑
│   │   └── main.py      # 应用入口
│   ├── alembic/         # 数据库迁移
│   ├── scripts/         # 工具脚本
│   └── tests/           # 测试
├── web/                 # 前端小程序
│   ├── src/
│   │   ├── api/        # API接口
│   │   ├── pages/      # 页面
│   │   ├── utils/      # 工具函数
│   │   └── static/     # 静态资源
│   └── package.json
├── nginx/              # Nginx配置
├── docker-compose.yml  # Docker编排
├── Ideation.md        # 项目构思
├── SETUP.md           # 环境搭建指南
└── README.md          # 本文件
```

## 📡 API文档

### 核心接口

#### 认证模块 (`/api/v1/auth`)
- `POST /auth/wechat/login` - 微信登录
- `GET /auth/user/info` - 获取用户信息

#### 对话模块 (`/api/v1/chat`)
- `POST /chat/sessions` - 创建会话
- `GET /chat/sessions` - 获取会话列表
- `GET /chat/sessions/{id}` - 获取会话详情
- `DELETE /chat/sessions/{id}` - 删除会话
- `POST /chat/messages` - 发送消息
- `POST /chat/messages/stream` - 发送消息（流式）

#### 计费模块 (`/api/v1/billing`)
- `GET /billing/balance` - 查询余额
- `GET /billing/transactions` - 交易记录
- `POST /billing/recharge` - 发起充值

完整API文档：http://localhost:8000/docs

## 💾 数据库设计

### 核心表结构

- **users** - 用户表
- **chat_sessions** - 会话表
- **chat_messages** - 消息表
- **billing_transactions** - 交易记录表
- **recharge_orders** - 充值订单表

详细设计见 [DATABASE.md](docs/DATABASE.md)

## 🔐 环境配置

### 后端环境变量 (`.env`)

```bash
# 数据库
DATABASE_URL=postgresql+asyncpg://dashi:dashi123@localhost:5432/dashi

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT密钥
JWT_SECRET_KEY=your-super-secret-jwt-key

# 微信配置
WECHAT_APPID=your-wechat-appid
WECHAT_SECRET=your-wechat-secret

# DeepSeek AI
DEEPSEEK_API_KEY=your-deepseek-api-key
```

### 前端环境变量 (`.env.development`)

```bash
VITE_API_BASE_URL=http://localhost:8000
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

# 启动
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 文档

- [环境搭建指南](SETUP.md) - 完整的开发环境搭建步骤
- [项目构思](Ideation.md) - 详细的项目规划和设计
- [后端文档](backend/README.md) - 后端开发文档
- [前端文档](web/README.md) - 前端开发文档
- [API文档](http://localhost:8000/docs) - 在线API文档

## 🛠️ 开发指南

### 代码规范

```bash
# Python代码格式化
cd backend
poetry run black .
poetry run flake8 .
poetry run isort .

# 类型检查
poetry run mypy .
```

### 数据库迁移

```bash
# 创建迁移
poetry run alembic revision --autogenerate -m "description"

# 执行迁移
poetry run alembic upgrade head
```

### 测试

```bash
# 后端测试
cd backend
poetry run pytest

# 前端测试
cd web
npm run test
```

## 💰 成本估算

### 开发阶段（月）
- 服务器: ¥50-100
- 域名: ¥50/年
- DeepSeek API: ¥50-200
- **合计**: ¥100-300/月

### 运营阶段（月）
- 服务器: ¥100-200
- DeepSeek API: ¥500-2000
- 微信认证: ¥300/年
- **合计**: ¥600-2200/月

## 📅 开发计划

- [x] 项目初始化
- [x] 后端框架搭建
- [x] 数据库设计
- [x] API开发
- [x] 前端页面开发
- [x] Docker配置
- [ ] 微信支付集成
- [ ] 性能优化
- [ ] 安全加固
- [ ] 上线部署

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📝 License

待定

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
