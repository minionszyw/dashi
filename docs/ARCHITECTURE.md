# 架构设计文档 - 国学大师

## 📋 目录

- [技术架构](#技术架构)
- [项目结构](#项目结构)
- [数据库设计](#数据库设计)
- [API设计](#api设计)
- [数据流](#数据流)
- [部署架构](#部署架构)

---

## 技术架构

### 整体架构图

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

#### 后端技术栈
- **框架**: FastAPI 0.109+
- **异步运行时**: uvicorn + asyncio
- **ORM**: SQLAlchemy 2.0 (async)
- **数据验证**: Pydantic v2
- **AI框架**: LangChain + DeepSeek API
- **认证**: JWT (python-jose)
- **密码加密**: passlib + bcrypt

#### 前端技术栈
- **框架**: uni-app 3.0
- **语言**: TypeScript + Vue 3
- **UI组件**: 自定义组件
- **状态管理**: 本地存储
- **HTTP客户端**: uni.request
- **构建工具**: Vite

#### 数据库
- **主库**: PostgreSQL 15+
- **缓存**: Redis 7+
- **连接池**: asyncpg + aioredis

---

## 项目结构

```
dashi/
├── 📄 文档
│   ├── README.md              # 项目入口
│   ├── CHANGELOG.md           # 更新日志
│   ├── LICENSE                # 许可证
│   └── docs/
│       ├── SETUP.md           # 环境搭建
│       ├── ARCHITECTURE.md    # 本文件
│       └── DESIGN.md          # 设计文档
│
├── 🔧 配置
│   ├── .gitignore
│   ├── .editorconfig
│   ├── .dockerignore
│   └── docker-compose.yml
│
├── 📦 后端 (backend/)
│   ├── app/
│   │   ├── main.py           # 应用入口
│   │   ├── api/              # API路由
│   │   │   ├── dependencies.py
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── chat.py
│   │   │       └── billing.py
│   │   ├── core/             # 核心配置
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── redis.py
│   │   │   └── security.py
│   │   ├── models/           # 数据模型
│   │   │   ├── user.py
│   │   │   ├── chat.py
│   │   │   └── billing.py
│   │   ├── schemas/          # Pydantic模型
│   │   └── services/         # 业务逻辑
│   │       ├── wechat.py
│   │       ├── ai.py
│   │       └── billing.py
│   ├── alembic/              # 数据库迁移
│   ├── scripts/              # 工具脚本
│   └── tests/                # 测试
│
├── 🎨 前端 (web/)
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── pages.json
│   │   ├── api/              # API接口
│   │   ├── pages/            # 页面
│   │   ├── utils/            # 工具
│   │   └── static/           # 静态资源
│   └── dist/                 # 构建输出
│
├── 🌐 nginx/                 # Nginx配置
└── 🛠️ scripts/              # 部署脚本
```

---

## 数据库设计

### 核心表结构

#### 1. users (用户表)
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    openid VARCHAR(128) UNIQUE NOT NULL,
    unionid VARCHAR(128),
    nickname VARCHAR(64),
    avatar_url VARCHAR(512),
    token_balance DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);
CREATE INDEX idx_users_openid ON users(openid);
```

#### 2. chat_sessions (会话表)
```sql
CREATE TABLE chat_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    title VARCHAR(128),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_sessions_user ON chat_sessions(user_id, created_at DESC);
```

#### 3. chat_messages (消息表)
```sql
CREATE TABLE chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT REFERENCES chat_sessions(id),
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    model VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_messages_session ON chat_messages(session_id, created_at);
```

#### 4. billing_transactions (交易记录)
```sql
CREATE TABLE billing_transactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    type VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    balance_after DECIMAL(10,2),
    description TEXT,
    reference_id VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_transactions_user ON billing_transactions(user_id, created_at DESC);
```

#### 5. recharge_orders (充值订单)
```sql
CREATE TABLE recharge_orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    order_no VARCHAR(64) UNIQUE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    tokens DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(20),
    transaction_id VARCHAR(128),
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_orders_user ON recharge_orders(user_id, created_at DESC);
```

### 表关系图

```
users (1) ←→ (N) chat_sessions
              ↓
         (1) ←→ (N) chat_messages

users (1) ←→ (N) billing_transactions
users (1) ←→ (N) recharge_orders
```

---

## API设计

### RESTful API架构

```
/api/v1/
├── /auth                       # 认证模块
│   ├── POST   /wechat/login   # 微信登录
│   └── GET    /user/info      # 用户信息
│
├── /chat                       # 对话模块
│   ├── POST   /sessions       # 创建会话
│   ├── GET    /sessions       # 会话列表
│   ├── GET    /sessions/{id}  # 会话详情
│   ├── DELETE /sessions/{id}  # 删除会话
│   ├── POST   /messages       # 发送消息
│   └── POST   /messages/stream # 流式发送
│
└── /billing                    # 计费模块
    ├── GET    /balance        # 查询余额
    ├── GET    /transactions   # 交易记录
    └── POST   /recharge       # 发起充值
```

### 统一响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "timestamp": 1234567890
}
```

### 认证机制

- **方式**: JWT Token
- **传递**: HTTP Header `Authorization: Bearer <token>`
- **过期**: 7天
- **刷新**: 需重新登录

---

## 数据流

### 1. 用户登录流程

```
用户 → 小程序获取code
  ↓
后端接收code → 调用微信API
  ↓
获取openid → 创建/更新用户
  ↓
生成JWT Token → 返回给前端
  ↓
前端存储Token → 后续请求携带
```

### 2. AI对话流程

```
用户发送消息 → 前端API请求
  ↓
后端验证Token → 检查余额
  ↓
保存用户消息 → 获取历史上下文
  ↓
调用LangChain → DeepSeek API
  ↓
接收AI回复 → 保存消息
  ↓
计算Token消耗 → 扣费
  ↓
返回结果 → 前端展示
```

### 3. 充值流程

```
用户发起充值 → 选择金额
  ↓
创建充值订单 → 生成订单号
  ↓
调用微信支付 → 获取支付参数
  ↓
用户完成支付 → 微信回调
  ↓
验证签名 → 更新订单状态
  ↓
增加用户余额 → 记录交易
```

---

## 部署架构

### Docker容器架构

```
┌─────────────────────┐
│   Nginx (80/443)    │  ← 入口
└──────────┬──────────┘
           │
┌──────────┴──────────┐
│  FastAPI (8000)     │  ← API服务
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    ↓             ↓
┌─────────┐  ┌──────────┐
│ Redis   │  │PostgreSQL│
│ (6379)  │  │  (5432)  │
└─────────┘  └──────────┘
```

### 服务编排 (docker-compose)

```yaml
services:
  nginx:    # 反向代理
  api:      # FastAPI应用
  db:       # PostgreSQL数据库
  redis:    # Redis缓存
```

### 环境配置

- **开发环境**: Docker Compose本地运行
- **生产环境**: Docker Compose + 云服务器
- **监控**: 日志输出 + 健康检查

---

## 性能优化

### 数据库优化
- 连接池管理 (asyncpg pool: 10-20)
- 索引优化 (高频查询字段)
- 查询优化 (避免N+1问题)

### 缓存策略
- Session缓存 (Redis)
- 热点数据缓存
- 查询结果缓存

### API优化
- 异步处理 (async/await)
- 流式响应 (SSE)
- 限流控制

---

## 安全设计

### 认证与授权
- JWT Token认证
- Token过期机制
- 敏感操作验证

### 数据安全
- HTTPS全站加密
- 密码加密存储
- SQL注入防护
- XSS防护

### 限流策略
- 用户级别: 10次/分钟
- IP级别: 30次/分钟
- API级别: 按接口配置

---

## 扩展性考虑

### 水平扩展
- API服务多实例部署
- 负载均衡 (Nginx)
- 数据库读写分离

### 功能扩展
- 插件化AI服务
- 多租户支持
- 国际化支持

### 监控告警
- 日志聚合
- 性能监控
- 错误追踪 (Sentry)

---

## 技术债务

### 待优化项
- [ ] 单元测试覆盖
- [ ] 流式响应前端实现
- [ ] 性能压测
- [ ] 监控系统
- [ ] CI/CD自动化

### 已知问题
1. 微信支付回调未完成
2. 错误处理需完善
3. 限流策略待实现

---

## 参考资源

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [LangChain文档](https://python.langchain.com/)
- [uni-app文档](https://uniapp.dcloud.io/)
- [PostgreSQL文档](https://www.postgresql.org/docs/)

---

**文档版本**: v0.1.0  
**更新时间**: 2024年1月  
**维护者**: minionszyw

