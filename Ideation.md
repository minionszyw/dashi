# 国学大师 - 命理分析小程序项目构思

## 📋 项目概述

### 项目定位
一个基于AI的命理分析微信小程序，为用户提供智能化的命理咨询服务。目标是支持20个并发用户，采用token计费模式。

### 核心价值
- **用户价值**：便捷的AI命理分析服务，24/7可用
- **技术价值**：API-First架构，易于扩展和维护
- **商业价值**：token计费模式，低成本高效率

---

## 🎯 MVP功能规划

### MVP v1.0（核心功能，2-3周）
- [ ] **AI对话功能**
  - 支持多轮对话
  - 命理分析专业回答
  - 流式输出优化体验
  
- [ ] **微信登录**
  - 微信授权登录
  - 用户信息存储
  - Session管理

- [ ] **基础会话管理**
  - 创建新会话
  - 查看历史会话列表
  - 删除会话

- [ ] **简单计费系统**
  - Token余额显示
  - 按消息扣费
  - 余额不足提示

### v1.1（完善功能，1-2周）
- [ ] 充值功能（微信支付）
- [ ] 会话详情查看
- [ ] 用户消费记录
- [ ] 基础数据统计

### v2.0（增值功能，后续迭代）
- [ ] 分享功能
- [ ] 收藏对话
- [ ] 多种命理分析模式
- [ ] 用户等级体系
- [ ] 推荐系统

---

## 🏗️ 技术架构

### 整体架构图
```
┌─────────────┐
│  微信小程序  │ (uni-app + uni-ui)
│   前端层    │
└──────┬──────┘
       │ HTTPS/WSS
       ↓
┌─────────────┐
│   Nginx     │ (反向代理 + SSL)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   FastAPI   │ (API服务)
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

### 技术栈详情

#### 前端技术栈
- **框架**: uni-app (支持微信小程序)
- **UI组件**: uni-ui
- **状态管理**: Pinia (推荐) 或 Vuex
- **HTTP客户端**: uni.request
- **工具库**: dayjs (日期处理)

#### 后端技术栈
- **Web框架**: FastAPI 0.104+
- **异步运行时**: uvicorn + asyncio
- **ORM**: SQLAlchemy 2.0 (async)
- **数据验证**: Pydantic v2
- **AI框架**: LangChain + DeepSeek API
- **认证**: JWT (python-jose)
- **密码加密**: passlib + bcrypt

#### 数据库
- **主库**: PostgreSQL 15+
- **缓存**: Redis 7+ (session、限流)
- **连接池**: asyncpg + aioredis

#### 第三方服务
- **AI服务**: DeepSeek API
- **支付**: 微信支付 (商户平台)
- **登录**: 微信开放平台
- **监控**: Sentry (错误追踪)
- **日志**: 阿里云SLS 或 ELK (可选)

---

## 📡 API设计 (API-First)

### API设计原则
1. RESTful风格
2. 统一响应格式
3. 版本控制 (/api/v1)
4. 完善的错误处理
5. API文档自动生成 (FastAPI Swagger)

### 统一响应格式
```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "timestamp": 1234567890
}
```

### 核心API端点设计

#### 1. 认证模块 (/api/v1/auth)
```
POST   /auth/wechat/login      # 微信登录
POST   /auth/refresh           # 刷新token
GET    /auth/user/info         # 获取用户信息
```

#### 2. 对话模块 (/api/v1/chat)
```
POST   /chat/sessions          # 创建会话
GET    /chat/sessions          # 获取会话列表
GET    /chat/sessions/{id}     # 获取会话详情
DELETE /chat/sessions/{id}     # 删除会话
POST   /chat/messages          # 发送消息 (支持SSE流式)
GET    /chat/messages/{session_id}  # 获取消息历史
```

#### 3. 计费模块 (/api/v1/billing)
```
GET    /billing/balance        # 查询余额
GET    /billing/transactions   # 交易记录
POST   /billing/recharge       # 发起充值
POST   /billing/recharge/callback  # 充值回调
```

#### 4. 用户模块 (/api/v1/user)
```
GET    /user/profile           # 用户资料
PUT    /user/profile           # 更新资料
GET    /user/stats             # 用户统计
```

### API文档
- 使用FastAPI自动生成Swagger文档
- 部署到 `/docs` 和 `/redoc`
- 导出OpenAPI 3.0 JSON规范

---

## 💾 数据库设计

### 核心表结构

#### users (用户表)
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

#### chat_sessions (会话表)
```sql
CREATE TABLE chat_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    title VARCHAR(128),
    status VARCHAR(20) DEFAULT 'active', -- active, archived, deleted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_sessions_user ON chat_sessions(user_id, created_at DESC);
```

#### chat_messages (消息表)
```sql
CREATE TABLE chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT REFERENCES chat_sessions(id),
    role VARCHAR(20) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    model VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_messages_session ON chat_messages(session_id, created_at);
```

#### billing_transactions (交易记录)
```sql
CREATE TABLE billing_transactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    type VARCHAR(20) NOT NULL, -- recharge, consume, refund
    amount DECIMAL(10,2) NOT NULL,
    balance_after DECIMAL(10,2),
    description TEXT,
    reference_id VARCHAR(128), -- 微信订单号等
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_transactions_user ON billing_transactions(user_id, created_at DESC);
```

#### recharge_orders (充值订单)
```sql
CREATE TABLE recharge_orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    order_no VARCHAR(64) UNIQUE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    tokens DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, paid, failed, refunded
    payment_method VARCHAR(20), -- wechat
    transaction_id VARCHAR(128), -- 微信交易号
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_orders_user ON recharge_orders(user_id, created_at DESC);
CREATE INDEX idx_orders_no ON recharge_orders(order_no);
```

### 数据库优化策略
- 使用连接池 (asyncpg pool size: 10-20)
- 对高频查询字段建索引
- 使用Redis缓存热点数据
- 定期清理历史数据 (归档策略)

---

## 🔌 第三方服务集成

### 1. DeepSeek AI
- **用途**: 核心AI对话能力
- **集成方式**: LangChain + DeepSeek API
- **成本**: 按token计费
- **备选方案**: 通义千问、智谱AI

### 2. 微信开放平台
- **登录**: wx.login + code2Session
- **支付**: 微信支付JSAPI
- **所需**: AppID, AppSecret, 商户号, API密钥

### 3. 对象存储 (可选)
- **用途**: 存储用户头像等
- **推荐**: 阿里云OSS / 腾讯云COS
- **MVP阶段**: 可以先用微信头像URL

### 4. 监控告警
- **错误追踪**: Sentry (免费版)
- **性能监控**: FastAPI内置 + Prometheus (可选)
- **日志**: 本地文件 + Logrotate (MVP阶段)

### 5. 短信服务 (v2.0)
- **用途**: 通知、验证码
- **推荐**: 阿里云SMS / 腾讯云SMS

---

## 🔐 安全设计

### 认证与授权
- JWT Token认证
- Token过期时间: 7天
- Refresh Token机制
- 敏感操作二次验证

### 数据安全
- HTTPS全站加密
- 数据库密码字段加密存储
- API限流防护 (Redis计数器)
- SQL注入防护 (ORM参数化)
- XSS防护 (输入验证)

### 限流策略
```python
# 用户级别
- 每分钟最多10次API请求
- 每天最多100次AI对话

# IP级别  
- 每分钟最多30次请求
```

---

## 🛠️ 开发工具与流程

### 代码管理
```bash
# Git分支策略
main        # 生产环境
develop     # 开发环境
feature/*   # 功能分支
hotfix/*    # 紧急修复
```

### 开发环境配置

#### 后端环境
```bash
# 依赖管理: Poetry
poetry init
poetry add fastapi uvicorn sqlalchemy asyncpg redis

# 环境变量管理: .env
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
DEEPSEEK_API_KEY=...
WECHAT_APPID=...
WECHAT_SECRET=...
JWT_SECRET=...
```

#### 前端环境
```bash
# 使用HBuilderX或CLI
npm install -g @dcloudio/uvm
uvm use 3.0.0
```

### 代码规范
- **Python**: Black + Flake8 + isort
- **JavaScript**: ESLint + Prettier
- **提交规范**: Conventional Commits
  ```
  feat: 新功能
  fix: 修复
  docs: 文档
  style: 格式
  refactor: 重构
  test: 测试
  chore: 构建/工具
  ```

### 自动化脚本
创建 `scripts/` 目录：
```bash
scripts/
├── setup.sh          # 一键环境搭建
├── dev.sh           # 启动开发环境
├── db_migrate.sh    # 数据库迁移
├── backup.sh        # 数据备份
└── deploy.sh        # 部署脚本
```

---

## 🚀 CI/CD方案

### CI流程 (GitHub Actions / GitLab CI)

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      - name: Run linters
        run: |
          poetry run black --check .
          poetry run flake8 .
      - name: Run tests
        run: poetry run pytest
      - name: Build Docker image
        run: docker build -t dashi-api:${{ github.sha }} .
```

### CD流程

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /app/dashi
            git pull
            docker-compose pull
            docker-compose up -d
```

### 自动化检查清单
- ✅ 代码风格检查
- ✅ 单元测试
- ✅ API测试
- ✅ 安全扫描 (Bandit)
- ✅ 依赖漏洞扫描
- ✅ Docker镜像构建
- ✅ 自动部署到测试环境

---

## 🐳 部署方案

### Docker化

#### 后端 Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dashi
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    restart: always

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=dashi
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    restart: always

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: always

volumes:
  postgres_data:
  redis_data:
```

### 服务器要求

#### MVP阶段 (20并发)
- **CPU**: 2核
- **内存**: 4GB
- **存储**: 40GB SSD
- **带宽**: 3Mbps
- **推荐**: 阿里云/腾讯云 轻量应用服务器

#### 扩展阶段
- 考虑水平扩展 (多实例)
- 使用负载均衡
- 数据库读写分离
- CDN加速静态资源

### 域名与SSL
- 备案域名
- Let's Encrypt免费SSL证书
- 自动续期 (Certbot)

---

## 💰 成本估算

### 开发阶段成本 (月)
| 项目 | 费用 | 说明 |
|-----|------|------|
| 服务器 | ¥50-100 | 轻量应用服务器 |
| 域名 | ¥50/年 | .com/.cn |
| DeepSeek API | ¥50-200 | 测试使用 |
| **合计** | **¥100-300/月** | |

### 运营阶段成本 (月)
| 项目 | 费用 | 说明 |
|-----|------|------|
| 服务器 | ¥100-200 | 按需升级 |
| DeepSeek API | ¥500-2000 | 按实际使用 |
| 微信认证 | ¥300/年 | 小程序认证 |
| 支付手续费 | ¥? | 充值金额的0.6% |
| 监控服务 | ¥0 | Sentry免费版 |
| **合计** | **¥600-2200/月** | |

### 盈利模型
- Token充值价格: ¥0.01/token
- DeepSeek成本: ¥0.001/token (估算)
- 毛利率: 90%
- 盈亏平衡点: 月充值¥700+

---

## ⚠️ 风险评估

### 技术风险
| 风险 | 可能性 | 影响 | 应对措施 |
|-----|-------|------|---------|
| API服务不稳定 | 中 | 高 | 多模型备选方案 |
| 并发性能问题 | 低 | 中 | 提前压测、优化 |
| 数据库故障 | 低 | 高 | 定期备份、主从复制 |

### 业务风险
| 风险 | 可能性 | 影响 | 应对措施 |
|-----|-------|------|---------|
| 用户增长缓慢 | 中 | 中 | 营销推广、裂变机制 |
| AI成本过高 | 中 | 高 | 使用更便宜的模型 |
| 微信封禁 | 低 | 高 | 合规运营、内容审核 |

### 合规风险
- 命理内容敏感性 → 添加免责声明
- 用户数据隐私 → 遵守GDPR/个保法
- 支付资质 → 使用正规通道

---

## 📅 开发时间规划

### 第一阶段: 基础搭建 (1周)
- [ ] Day 1-2: 项目初始化、环境配置
  - Git仓库创建
  - Docker环境搭建
  - CI/CD配置
- [ ] Day 3-4: 数据库设计与API框架
  - 数据库表设计
  - FastAPI项目结构
  - API基础框架
- [ ] Day 5-7: 前端框架搭建
  - uni-app初始化
  - UI组件库配置
  - 基础页面结构

### 第二阶段: 核心功能 (2周)
- [ ] Week 1: 后端核心功能
  - 微信登录接口
  - AI对话接口 (LangChain + DeepSeek)
  - 会话管理
  - 计费系统
- [ ] Week 2: 前端核心功能
  - 登录页面
  - 对话界面
  - 会话列表
  - 余额显示

### 第三阶段: 完善与测试 (1周)
- [ ] Day 1-3: 功能完善
  - 充值功能
  - 错误处理
  - 性能优化
- [ ] Day 4-5: 测试
  - 单元测试
  - 集成测试
  - 压力测试
- [ ] Day 6-7: 部署上线
  - 服务器部署
  - 域名配置
  - 小程序提审

### 总计: 4周完成MVP

---

## 📚 文档体系

### 必备文档
```
docs/
├── README.md                 # 项目说明
├── SETUP.md                  # 环境搭建指南
├── API.md                    # API文档
├── ARCHITECTURE.md           # 架构设计
├── DEPLOYMENT.md             # 部署指南
├── DATABASE.md               # 数据库文档
└── CHANGELOG.md              # 变更日志
```

### 文档内容要点
1. **SETUP.md**: 
   - 环境要求
   - 依赖安装
   - 配置说明
   - 常见问题

2. **ARCHITECTURE.md**:
   - 系统架构图
   - 技术选型理由
   - 关键设计决策
   - 扩展性考虑

3. **DEPLOYMENT.md**:
   - 服务器配置
   - Docker部署步骤
   - 环境变量说明
   - 回滚方案

---

## 🎯 下一步行动

### 立即开始
1. ✅ 创建Git仓库
2. ✅ 搭建开发环境
3. ✅ 设计数据库
4. ✅ 实现登录API

### 本周目标
- [ ] 完成项目框架搭建
- [ ] 实现微信登录
- [ ] 对接DeepSeek API
- [ ] 完成基础对话功能

### 本月目标
- [ ] 完成MVP所有功能
- [ ] 通过小程序审核
- [ ] 上线运营

---

## 📖 参考资源

### 官方文档
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [uni-app文档](https://uniapp.dcloud.io/)
- [LangChain文档](https://python.langchain.com/)
- [微信小程序文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [DeepSeek API](https://platform.deepseek.com/docs)

### 推荐工具
- **API测试**: Postman / Hoppscotch
- **数据库管理**: DBeaver / pgAdmin
- **代码编辑器**: VSCode / PyCharm
- **小程序开发**: 微信开发者工具 / HBuilderX
- **容器管理**: Portainer

### 学习资源
- FastAPI最佳实践
- LangChain实战教程
- 微信支付开发指南
- Docker部署实践

---

## 💡 关键成功因素

1. **快速迭代**: MVP优先，快速验证
2. **用户体验**: 流畅的对话体验是核心
3. **成本控制**: AI调用成本需要严格控制
4. **稳定性**: 服务稳定性至关重要
5. **合规性**: 内容合规、支付合规

---

## 结语

这是一个技术栈现代、架构清晰、可快速落地的项目方案。遵循以上设计，4周内可以完成MVP并上线运营。

**记住核心原则**:
- 保持简单 (KISS)
- API优先
- 自动化一切
- 文档驱动
- 持续迭代

祝开发顺利！🚀

