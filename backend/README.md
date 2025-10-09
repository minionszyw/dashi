# 国学大师 - 后端API

基于FastAPI的AI命理分析小程序后端服务。

## 技术栈

- **框架**: FastAPI 0.109+
- **数据库**: PostgreSQL 15 + SQLAlchemy 2.0 (async)
- **缓存**: Redis 7
- **AI**: LangChain + DeepSeek API
- **认证**: JWT

## 快速开始

### 1. 环境准备

```bash
# 安装Python 3.11+
python --version

# 安装Poetry
pip install poetry

# 安装依赖
poetry install
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并填写配置：

```bash
# 数据库配置
DATABASE_URL=postgresql+asyncpg://dashi:dashi123@localhost:5432/dashi

# Redis配置
REDIS_URL=redis://localhost:6379/0

# JWT密钥（生产环境请修改）
JWT_SECRET_KEY=your-super-secret-jwt-key

# 微信配置
WECHAT_APPID=your-wechat-appid
WECHAT_SECRET=your-wechat-secret

# DeepSeek配置
DEEPSEEK_API_KEY=your-deepseek-api-key
```

### 3. 初始化数据库

```bash
# 使用Docker启动数据库
docker-compose up -d db redis

# 初始化数据库表
python scripts/init_db.py
```

### 4. 启动开发服务器

```bash
# 方式1: 使用脚本
bash scripts/dev.sh

# 方式2: 直接启动
poetry run uvicorn app.main:app --reload

# 方式3: 使用Poetry shell
poetry shell
uvicorn app.main:app --reload
```

访问：
- API文档: http://localhost:8000/docs
- ReDoc文档: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## Docker部署

### 开发环境

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 停止服务
docker-compose down
```

### 生产环境

```bash
# 构建镜像
docker build -t dashi-api:latest ./backend

# 使用环境变量
export JWT_SECRET_KEY="your-production-secret"
export WECHAT_APPID="your-appid"
export WECHAT_SECRET="your-secret"
export DEEPSEEK_API_KEY="your-api-key"

# 启动
docker-compose -f docker-compose.prod.yml up -d
```

## API文档

### 认证模块 (`/api/v1/auth`)

- `POST /auth/wechat/login` - 微信登录
- `GET /auth/user/info` - 获取用户信息

### 对话模块 (`/api/v1/chat`)

- `POST /chat/sessions` - 创建会话
- `GET /chat/sessions` - 获取会话列表
- `GET /chat/sessions/{id}` - 获取会话详情
- `DELETE /chat/sessions/{id}` - 删除会话
- `POST /chat/messages` - 发送消息
- `POST /chat/messages/stream` - 发送消息（流式）

### 计费模块 (`/api/v1/billing`)

- `GET /billing/balance` - 查询余额
- `GET /billing/transactions` - 交易记录
- `POST /billing/recharge` - 发起充值

## 项目结构

```
backend/
├── app/
│   ├── api/              # API路由
│   │   ├── dependencies.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── chat.py
│   │       └── billing.py
│   ├── core/             # 核心配置
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── redis.py
│   │   └── security.py
│   ├── models/           # 数据模型
│   │   ├── user.py
│   │   ├── chat.py
│   │   └── billing.py
│   ├── schemas/          # Pydantic模型
│   ├── services/         # 业务逻辑
│   │   ├── wechat.py
│   │   ├── ai.py
│   │   └── billing.py
│   └── main.py           # 应用入口
├── alembic/              # 数据库迁移
├── scripts/              # 工具脚本
├── tests/                # 测试
├── Dockerfile
├── pyproject.toml
└── README.md
```

## 开发指南

### 代码规范

```bash
# 格式化代码
poetry run black .

# 检查代码风格
poetry run flake8 .

# 排序导入
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

# 回滚迁移
poetry run alembic downgrade -1
```

### 测试

```bash
# 运行测试
poetry run pytest

# 覆盖率
poetry run pytest --cov=app
```

## 常见问题

### 1. 数据库连接失败

检查PostgreSQL是否启动：
```bash
docker-compose ps
```

### 2. Redis连接失败

检查Redis是否启动：
```bash
docker exec -it dashi-redis redis-cli ping
```

### 3. AI调用失败

检查DeepSeek API密钥是否正确配置。

## License

待定

