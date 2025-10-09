# 项目结构说明 - 国学大师

## 📂 目录结构

```
dashi/                          # 项目根目录
│
├── 📄 文档文件
│   ├── README.md              # 项目介绍和概览
│   ├── QUICK_START.md         # 5分钟快速上手指南
│   ├── SETUP.md               # 详细的环境搭建指南
│   ├── Ideation.md            # 项目构思和设计文档
│   ├── PROJECT_SUMMARY.md     # 项目总结文档
│   ├── DELIVERY.md            # 项目交付清单
│   ├── STRUCTURE.md           # 本文件 - 项目结构说明
│   ├── CHANGELOG.md           # 更新日志
│   └── LICENSE                # MIT许可证
│
├── 🔧 配置文件
│   ├── .gitignore             # Git忽略配置
│   ├── .editorconfig          # 编辑器配置
│   ├── .dockerignore          # Docker忽略配置
│   └── docker-compose.yml     # Docker服务编排
│
├── 📦 后端服务 (backend/)
│   ├── app/                   # 应用代码
│   │   ├── main.py           # FastAPI应用入口
│   │   ├── __init__.py
│   │   │
│   │   ├── api/              # API路由层
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py    # 依赖注入（认证等）
│   │   │   └── v1/                # API v1版本
│   │   │       ├── __init__.py
│   │   │       ├── auth.py        # 认证接口（微信登录）
│   │   │       ├── chat.py        # 对话接口
│   │   │       └── billing.py     # 计费接口
│   │   │
│   │   ├── core/             # 核心配置
│   │   │   ├── __init__.py
│   │   │   ├── config.py          # 配置管理（Pydantic Settings）
│   │   │   ├── database.py        # 数据库连接和Session
│   │   │   ├── redis.py           # Redis连接
│   │   │   └── security.py        # JWT和密码加密
│   │   │
│   │   ├── models/           # SQLAlchemy数据模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py            # 用户模型
│   │   │   ├── chat.py            # 会话和消息模型
│   │   │   └── billing.py         # 计费和订单模型
│   │   │
│   │   ├── schemas/          # Pydantic Schema（请求/响应）
│   │   │   ├── __init__.py
│   │   │   ├── common.py          # 通用响应模型
│   │   │   ├── user.py            # 用户Schema
│   │   │   ├── chat.py            # 对话Schema
│   │   │   └── billing.py         # 计费Schema
│   │   │
│   │   └── services/         # 业务逻辑层
│   │       ├── __init__.py
│   │       ├── wechat.py          # 微信服务（登录）
│   │       ├── ai.py              # AI服务（LangChain+DeepSeek）
│   │       └── billing.py         # 计费服务
│   │
│   ├── alembic/              # 数据库迁移
│   │   ├── versions/              # 迁移版本
│   │   ├── env.py                 # Alembic环境配置
│   │   └── script.py.mako         # 迁移脚本模板
│   │
│   ├── scripts/              # 工具脚本
│   │   ├── init_db.py            # 数据库初始化
│   │   └── dev.sh                # 开发环境启动脚本
│   │
│   ├── tests/                # 测试（待开发）
│   │
│   ├── Dockerfile            # Docker镜像配置
│   ├── pyproject.toml        # Poetry依赖管理
│   ├── requirements.txt      # pip依赖（参考）
│   ├── alembic.ini           # Alembic配置
│   ├── config.example.env    # 环境变量示例
│   ├── .gitignore
│   └── README.md             # 后端文档
│
├── 🎨 前端小程序 (web/)
│   ├── src/                  # 源代码
│   │   ├── main.ts          # 应用入口
│   │   ├── App.vue          # 根组件
│   │   ├── pages.json       # 页面配置
│   │   │
│   │   ├── api/             # API接口封装
│   │   │   ├── auth.ts           # 认证接口
│   │   │   ├── chat.ts           # 对话接口
│   │   │   └── billing.ts        # 计费接口
│   │   │
│   │   ├── pages/           # 页面
│   │   │   ├── index/            # 主页（对话）
│   │   │   │   └── index.vue
│   │   │   ├── login/            # 登录页
│   │   │   │   └── login.vue
│   │   │   ├── chat/             # 会话详情
│   │   │   │   └── chat.vue
│   │   │   ├── sessions/         # 会话列表
│   │   │   │   └── sessions.vue
│   │   │   └── profile/          # 个人中心
│   │   │       └── profile.vue
│   │   │
│   │   ├── utils/           # 工具函数
│   │   │   └── request.ts        # 网络请求封装
│   │   │
│   │   └── static/          # 静态资源
│   │       ├── logo.png
│   │       ├── avatar.png
│   │       └── tabbar/           # TabBar图标
│   │
│   ├── dist/                # 构建输出
│   │   ├── dev/                  # 开发版
│   │   └── build/                # 生产版
│   │
│   ├── package.json         # npm依赖
│   ├── vite.config.ts       # Vite配置
│   ├── tsconfig.json        # TypeScript配置
│   ├── env.example          # 环境变量示例
│   ├── .env.development     # 开发环境变量
│   ├── .env.production      # 生产环境变量
│   ├── .gitignore
│   └── README.md            # 前端文档
│
├── 🌐 Nginx配置 (nginx/)
│   └── nginx.conf           # Nginx配置文件
│
└── 🛠️ 脚本工具 (scripts/)
    ├── quick-start.sh       # 快速启动脚本
    └── deploy.sh            # 生产部署脚本
```

## 📋 文件说明

### 核心文件

#### 后端关键文件
| 文件 | 说明 |
|------|------|
| `backend/app/main.py` | FastAPI应用入口，路由注册 |
| `backend/app/core/config.py` | 配置管理，环境变量读取 |
| `backend/app/core/database.py` | 数据库连接和Session管理 |
| `backend/app/core/security.py` | JWT认证和密码加密 |
| `backend/app/services/ai.py` | AI对话核心逻辑 |
| `backend/app/api/dependencies.py` | 认证中间件 |

#### 前端关键文件
| 文件 | 说明 |
|------|------|
| `web/src/main.ts` | uni-app应用入口 |
| `web/src/pages.json` | 页面路由和TabBar配置 |
| `web/src/utils/request.ts` | 统一网络请求封装 |
| `web/src/pages/index/index.vue` | 主对话页面 |
| `web/src/api/auth.ts` | 认证API封装 |

#### 配置文件
| 文件 | 说明 |
|------|------|
| `docker-compose.yml` | Docker服务编排 |
| `backend/pyproject.toml` | Python依赖管理 |
| `web/package.json` | Node.js依赖管理 |
| `nginx/nginx.conf` | 反向代理配置 |

## 🔄 数据流

### 1. 用户登录流程
```
微信小程序 → 获取code → 后端API
          ↓
    调用微信API获取openid
          ↓
    创建/更新用户 → 生成JWT Token
          ↓
    返回Token和用户信息 → 前端存储
```

### 2. AI对话流程
```
前端发送消息 → 后端API
          ↓
    验证Token → 检查余额
          ↓
    保存用户消息 → 调用AI服务
          ↓
    LangChain → DeepSeek API
          ↓
    保存AI回复 → 扣费 → 返回结果
```

### 3. 数据存储流程
```
PostgreSQL:
├── users (用户表)
├── chat_sessions (会话表)
├── chat_messages (消息表)
├── billing_transactions (交易表)
└── recharge_orders (订单表)

Redis:
├── Session缓存
└── 限流计数
```

## 🔌 API架构

### RESTful API设计
```
/api/v1/
├── /auth
│   ├── POST   /wechat/login     # 微信登录
│   └── GET    /user/info        # 用户信息
├── /chat
│   ├── POST   /sessions         # 创建会话
│   ├── GET    /sessions         # 会话列表
│   ├── GET    /sessions/{id}    # 会话详情
│   ├── DELETE /sessions/{id}    # 删除会话
│   ├── POST   /messages         # 发送消息
│   └── POST   /messages/stream  # 流式发送
└── /billing
    ├── GET    /balance          # 查询余额
    ├── GET    /transactions     # 交易记录
    └── POST   /recharge         # 发起充值
```

## 🗄️ 数据库结构

### 表关系
```
users (用户)
  ↓ 1:N
chat_sessions (会话)
  ↓ 1:N
chat_messages (消息)

users (用户)
  ↓ 1:N
billing_transactions (交易)

users (用户)
  ↓ 1:N
recharge_orders (订单)
```

### 表字段
详见 `backend/app/models/` 目录下的模型定义

## 🚀 部署架构

### Docker容器
```
┌─────────────┐
│   Nginx     │  80/443端口
│  (反向代理)  │
└──────┬──────┘
       │
┌──────┴──────┐
│   FastAPI   │  8000端口
│  (API服务)   │
└──────┬──────┘
       │
    ┌──┴──┐
    ↓     ↓
┌────────┐ ┌─────────────┐
│ Redis  │ │ PostgreSQL  │
│  6379  │ │    5432     │
└────────┘ └─────────────┘
```

## 📝 代码规范

### Python (Backend)
- **格式化**: Black (line-length=100)
- **检查**: Flake8 + isort
- **类型**: mypy
- **风格**: PEP 8

### TypeScript (Frontend)
- **格式化**: Prettier
- **检查**: ESLint
- **类型**: TypeScript strict mode
- **风格**: Airbnb

### 提交规范
```
feat:     新功能
fix:      修复
docs:     文档
style:    格式
refactor: 重构
test:     测试
chore:    构建/工具
```

## 🔍 快速查找

### 常见修改位置

| 需求 | 修改位置 |
|------|---------|
| 添加API接口 | `backend/app/api/v1/` |
| 修改数据模型 | `backend/app/models/` |
| 添加业务逻辑 | `backend/app/services/` |
| 修改配置 | `backend/app/core/config.py` |
| 添加前端页面 | `web/src/pages/` + `pages.json` |
| 修改API调用 | `web/src/api/` |
| 修改样式 | 各页面的 `<style>` 标签 |
| 修改环境变量 | `.env` 或 `config.example.env` |

## 📚 扩展指南

### 添加新API端点
1. 在 `backend/app/api/v1/` 创建/修改路由文件
2. 在 `backend/app/services/` 添加业务逻辑
3. 在 `backend/app/schemas/` 定义请求/响应模型
4. 在 `web/src/api/` 添加前端API调用

### 添加新页面
1. 在 `web/src/pages/` 创建页面目录
2. 在 `pages.json` 注册页面
3. 开发Vue组件
4. 在 `api/` 目录添加API调用

### 添加新数据表
1. 在 `backend/app/models/` 定义模型
2. 运行 `alembic revision --autogenerate -m "描述"`
3. 运行 `alembic upgrade head`
4. 更新相关Schema和API

## 🛠️ 开发工具

### 推荐IDE
- **后端**: PyCharm / VSCode + Python插件
- **前端**: VSCode + Vue插件 / HBuilderX
- **数据库**: DBeaver / pgAdmin
- **API测试**: Postman / Hoppscotch
- **微信**: 微信开发者工具

### 调试方法
```bash
# 后端调试
poetry run uvicorn app.main:app --reload --log-level debug

# 查看数据库
docker exec -it dashi-db psql -U dashi

# 查看Redis
docker exec -it dashi-redis redis-cli

# 查看日志
docker-compose logs -f api
```

## 📖 学习路径

### 新手入门
1. 阅读 [QUICK_START.md](QUICK_START.md)
2. 运行项目，熟悉功能
3. 查看 [API文档](http://localhost:8000/docs)
4. 修改简单功能，如文本、样式

### 进阶开发
1. 阅读 [SETUP.md](SETUP.md) 和架构设计
2. 理解数据流和API设计
3. 学习核心技术（FastAPI、uni-app等）
4. 开发新功能

### 深入理解
1. 阅读 [Ideation.md](Ideation.md) 了解设计思路
2. 研究代码实现细节
3. 优化性能和架构
4. 参与贡献

---

**提示**: 本文档随项目更新，如有疑问请查看其他文档或联系开发者。

