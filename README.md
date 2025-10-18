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

- ✅ Docker & Docker Compose
- ✅ Node.js 22+
- ✅ Python 3.12+
- ✅ 微信开发者工具

### ⚡️ 5分钟快速上手

#### Step 1: 启动后端服务（2分钟）

```bash
# 1. 启动数据库和后端
docker-compose up -d

# 2. 等待服务启动完成（约30秒）
docker-compose logs -f backend

# 3. 执行数据库迁移（首次运行）
docker-compose exec backend alembic revision --autogenerate -m "initial"
docker-compose exec backend alembic upgrade head

# 4. 验证后端运行：访问 http://localhost:8000/docs
```

#### Step 2: 启动前端服务（2分钟）

```bash
# 1. 进入前端目录并安装依赖
cd frontend
npm install

# 2. 启动微信小程序开发模式
npm run dev:mp-weixin

# 3. 打开微信开发者工具
#    - 导入项目：选择 frontend/dist/dev/mp-weixin 目录
#    - 填入AppID（测试号或正式AppID）
#    - 开始开发
```

#### Step 3: 配置密钥（1分钟）

编辑 `backend/.env` 文件（需替换为实际值）：

```env
# OpenAI配置
OPENAI_API_KEY=sk-your-real-openai-key
OPENAI_BASE_URL=https://api.openai.com/v1  # 可选：使用代理

# 微信配置
WX_APPID=your-wechat-appid
WX_SECRET=your-wechat-secret

# 用户初始余额
INITIAL_TOKEN_BALANCE=100
```

编辑 `frontend/src/manifest.json`：

```json
{
  "mp-weixin": {
    "appid": "your-wechat-appid",
    "setting": {
      "urlCheck": false
    }
  }
}
```

### ✅ 验证功能

#### 1. 后端API测试
访问 http://localhost:8000/docs，测试以下接口：
- `GET /health` - 健康检查
- `POST /api/v1/auth/wx-login` - 登录
- `POST /api/v1/bazi/calculate` - 八字计算

#### 2. 前端功能测试
在微信开发者工具中：
- **登录功能**：点击"微信一键登录"，授权后跳转到对话页
- **AI对话**：输入消息测试对话，观察流式输出效果
- **八字排盘**：个人中心 → 八字排盘 → 填写出生信息 → 查看结果

### 🚨 常见问题

#### 后端启动失败
```bash
# 查看详细日志
docker-compose logs backend postgres redis

# 检查端口占用
sudo netstat -tlnp | grep -E "5432|6379|8000"
```

#### 微信登录失败
- 检查 `backend/.env` 中的 `WX_APPID` 和 `WX_SECRET`
- 检查 `frontend/src/manifest.json` 中的 `appid`
- 确保前后端配置一致

#### AI对话无响应
```bash
# 1. 检查配置
cat backend/.env | grep OPENAI

# 2. 查看后端日志
docker-compose logs -f backend

# 3. 如果使用代理，配置OPENAI_BASE_URL
OPENAI_BASE_URL=https://your-proxy-url/v1
```

## 📖 文档

- [架构设计](docs/design.md)
- [开发文档](docs/development.md)
- [部署文档](docs/deploy.md)
- [项目规范](project_specification.md)
- [开发日志](CHANGELOG.md)

## 🔧 开发

### 后端开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端开发

```bash
cd frontend
npm run dev:mp-weixin  # 微信小程序
npm run dev:h5         # H5
```

## 🧪 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

## 📦 部署

参考 [部署文档](docs/deploy.md)

## 📝 许可证

[MIT License](LICENSE)

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系

如有问题，请联系：your-email@example.com

