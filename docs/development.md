# 开发文档

## 环境准备

### 系统要求

- **操作系统**：Linux (推荐 Ubuntu 20.04+), macOS, Windows WSL2
- **Python**：3.12+
- **Node.js**：22+
- **Docker**：20.10+
- **Docker Compose**：2.0+

### 开发工具

- **IDE**：VSCode / PyCharm / Cursor
- **API测试**：Postman / Thunder Client
- **数据库客户端**：DBeaver / pgAdmin
- **微信开发者工具**：最新版本

## 快速开始

### 1. 启动基础服务（Docker）

```bash
# 克隆项目
git clone <repository-url> && cd dashi

# 启动PostgreSQL和Redis
sudo docker-compose up -d postgres redis

# 等待服务启动（约10秒）
sleep 10

# 检查服务状态
sudo docker-compose ps
```

### 2. 配置环境变量

```bash
# 复制环境配置文件
cp backend/.env.example backend/.env

# 编辑配置文件，填入以下必需配置：
# - OPENAI_API_KEY: OpenAI API密钥
# - WX_APPID: 微信小程序AppID
# - WX_SECRET: 微信小程序Secret
vim backend/.env  # 或使用其他编辑器
```

### 3. 启动后端服务

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 首次运行：执行数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

> 💡 **数据库迁移说明**：首次启动项目时必须执行 `alembic upgrade head` 创建数据库表结构。后续开发中如果修改了模型，需要重新生成迁移文件并执行迁移。

### 4. 启动前端服务

```bash
# 新开一个终端，进入前端目录
cd frontend

# 配置小程序信息
frontend/src/manifest.json

# 安装依赖
npm install

# 启动开发服务器（微信小程序）
npm run dev:mp-weixin

# 或启动H5开发模式
# npm run dev:h5
```

### 5. 验证运行

```bash
# 检查后端API
curl http://localhost:8000/health

# 访问API文档
open http://localhost:8000/docs  # 或在浏览器打开

# 检查前端编译输出
ls frontend/dist/dev/mp-weixin/
```

### 6. 微信小程序预览

1. 打开微信开发者工具
2. 导入项目目录：`frontend/dist/dev/mp-weixin`
3. 填入微信小程序AppID（与 `backend/.env` 中的 `WX_APPID` 一致）
4. 开始调试

> 💡 **提示**: 详细配置说明和故障排除见本文档后续章节


## 开发指南

### 后端开发

#### 项目结构
```
backend/app/
├── api/v1/          # API路由（auth, user, bazi, chat）
├── core/            # 核心配置（database, security, config）
├── models/          # 数据库模型（5个核心模型）
├── schemas/         # Pydantic模型（请求/响应）
├── services/        # 业务逻辑（langchain, bazi, wechat）
└── utils/           # 工具函数
```
> 详细结构说明见 [架构设计文档](design.md)

#### 创建新的API端点

```python
# app/api/v1/example.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/example")
async def get_example(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """示例接口"""
    return {"message": "Hello World", "user": current_user.nickname}

# 在 app/api/v1/__init__.py 中注册路由
from app.api.v1 import example
api_router.include_router(example.router, prefix="/example", tags=["example"])
```

#### 创建数据库模型

```python
# app/models/example.py
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class Example(Base):
    __tablename__ = "examples"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String(100), nullable=False)
    count = Column(Integer, default=0)
```

#### 创建数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "add examples table"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

#### 使用LangChain

```python
# app/services/langchain_service.py
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage

class ChatService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            streaming=True
        )
    
    async def stream_chat(self, messages: list, bazi_info: dict):
        """流式对话"""
        prompt = self._build_prompt(bazi_info)
        
        async for chunk in self.llm.astream(messages):
            yield chunk.content
    
    def _build_prompt(self, bazi_info: dict) -> str:
        """构建提示词"""
        return f"""
        你是命理分析师。用户八字：{bazi_info.get('bazi')}
        请进行专业分析。
        """
```

### 前端开发

#### 项目结构
```
frontend/src/
├── api/          # API封装（request, auth, chat, bazi）
├── components/   # 组件（MessageBubble, ChatInput）
├── pages/        # 页面（chat, profile, login, bazi）
├── stores/       # Pinia状态（user, chat, bazi）
├── types/        # TS类型定义
└── utils/        # 工具函数
```
> 详细规范见 [前端开发规范](.cursor/rules/frontend.mdc)

#### API请求封装

```typescript
// src/api/request.ts
import { getToken } from '@/utils/storage'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: any
}

export async function request<T>(options: RequestOptions): Promise<T> {
  const token = getToken()
  
  const response = await uni.request({
    url: `${import.meta.env.VITE_API_BASE_URL}${options.url}`,
    method: options.method || 'GET',
    data: options.data,
    header: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
      ...options.header
    }
  })
  
  if (response.statusCode !== 200) {
    throw new Error(response.data.message || '请求失败')
  }
  
  return response.data as T
}

// 使用示例
import { request } from './request'

interface User {
  id: string
  nickname: string
}

export function getUserProfile(): Promise<User> {
  return request<User>({
    url: '/api/v1/user/profile',
    method: 'GET'
  })
}
```

#### Pinia状态管理

```typescript
// src/stores/user.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

interface User {
  id: string
  nickname: string
  avatarUrl: string
  tokenBalance: number
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string>('')
  
  function setUser(userData: User) {
    user.value = userData
  }
  
  function setToken(tokenValue: string) {
    token.value = tokenValue
    uni.setStorageSync('token', tokenValue)
  }
  
  function logout() {
    user.value = null
    token.value = ''
    uni.removeStorageSync('token')
  }
  
  return {
    user,
    token,
    setUser,
    setToken,
    logout
  }
})
```

#### 组件开发示例

```vue
<!-- src/components/MessageBubble.vue -->
<template>
  <view :class="['message-bubble', message.role]">
    <image v-if="message.role === 'assistant'" 
           :src="aiAvatar" 
           class="avatar" />
    
    <view class="bubble-content">
      <text>{{ message.content }}</text>
    </view>
    
    <image v-if="message.role === 'user'" 
           :src="userAvatar" 
           class="avatar" />
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  createdAt: string
}

const props = defineProps<{
  message: Message
}>()

const aiAvatar = '/static/ai-avatar.png'
const userAvatar = computed(() => {
  // 从store获取用户头像
  return '/static/user-avatar.png'
})
</script>

<style scoped lang="scss">
.message-bubble {
  display: flex;
  margin: 20rpx;
  
  &.user {
    flex-direction: row-reverse;
    
    .bubble-content {
      background: #95ec69;
      margin-right: 20rpx;
    }
  }
  
  &.assistant {
    .bubble-content {
      background: #ffffff;
      margin-left: 20rpx;
    }
  }
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 10rpx;
}

.bubble-content {
  max-width: 500rpx;
  padding: 20rpx;
  border-radius: 10rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}
</style>
```

## 调试技巧

### 后端调试

#### 1. 使用VSCode调试

创建 `.vscode/launch.json`：
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": false
    }
  ]
}
```

#### 2. 日志调试

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
```

#### 3. 数据库查询调试

```python
# 打印SQL语句
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    echo=True  # 打印SQL
)
```

### 前端调试

#### 1. 微信开发者工具

- 使用控制台查看日志
- 使用Network面板查看请求
- 使用Storage面板查看存储

#### 2. 真机调试

```javascript
// 添加调试信息
console.log('用户信息:', user)

// H5模式下使用vConsole
import VConsole from 'vconsole'
const vConsole = new VConsole()
```

### 数据库网络配置说明

**本地开发模式（推荐）**：
- 后端在宿主机运行，数据库在Docker容器
- 使用 `localhost` 访问数据库

```bash
# backend/.env
DATABASE_URL=postgresql://dashi:dashi123@localhost:5432/dashi
REDIS_URL=redis://localhost:6379/0
```

**Docker完整部署模式**：
- 后端和数据库都在Docker容器
- 使用服务名访问数据库

```bash
# backend/.env
DATABASE_URL=postgresql://dashi:dashi123@postgres:5432/dashi
REDIS_URL=redis://redis:6379/0
```

## 常用开发命令

### Docker相关

```bash
# 启动所有服务
docker-compose up -d

# 启动指定服务
docker-compose up -d postgres redis

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f postgres
docker-compose logs -f redis

# 停止所有服务
docker-compose down

# 停止并删除数据卷（危险操作！）
docker-compose down -v

# 重启服务
docker-compose restart postgres

# 进入容器
docker-compose exec postgres psql -U dashi -d dashi
docker-compose exec redis redis-cli
```

### 后端相关

```bash
# 激活虚拟环境
cd backend
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安装/更新依赖
pip install -r requirements.txt
pip install --upgrade pip

# 运行开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 数据库迁移
alembic revision --autogenerate -m "描述修改内容"
alembic upgrade head
alembic downgrade -1

# 运行测试
pytest
pytest tests/test_chat.py -v
pytest --cov=app tests/

# 代码格式化
black app/ tests/
isort app/ tests/

# 代码检查
pylint app/
flake8 app/

# 查看后端进程
ps aux | grep uvicorn

# 停止后端服务
pkill -f uvicorn
```

### 前端相关

```bash
cd frontend

# 开发环境编译
npm run dev:mp-weixin  # 微信小程序
npm run dev:h5         # H5

# 生产环境构建
npm run build:mp-weixin
npm run build:h5

# 安装/更新依赖
npm install
npm update

# 清除缓存重新安装
rm -rf node_modules package-lock.json
npm install

# 查看前端进程
ps aux | grep vite

# 类型检查
npx vue-tsc --noEmit
```

### 数据库相关

```bash
# 连接PostgreSQL
psql -U dashi -d dashi -h localhost

# 在Docker容器中连接
docker-compose exec postgres psql -U dashi -d dashi

# 导出数据库
pg_dump -U dashi -h localhost dashi > backup.sql

# 导入数据库
psql -U dashi -h localhost dashi < backup.sql

# Redis CLI
redis-cli
docker-compose exec redis redis-cli

# 查看Redis所有键
redis-cli keys "*"

# 清空Redis
redis-cli FLUSHALL
```

### 系统检查

```bash
# 检查端口占用
sudo netstat -tlnp | grep 8000    # 后端
sudo netstat -tlnp | grep 5432    # PostgreSQL
sudo netstat -tlnp | grep 6379    # Redis

# 检查服务状态
systemctl status docker
systemctl status postgresql  # 如使用本地数据库
systemctl status redis-server

# 查看系统资源
docker stats
htop
df -h
```

## 常见问题

### 后端问题

#### 1. 数据库连接失败

**问题**：`could not connect to server` 或 `Connection refused`

**原因**：
- PostgreSQL服务未启动
- 端口被占用
- 数据库URL配置错误

**解决方案**：
```bash
# 检查Docker容器状态
sudo docker-compose ps

# 查看日志
sudo docker-compose logs postgres

# 重启数据库
sudo docker-compose restart postgres

# 检查端口占用
sudo netstat -tlnp | grep 5432

# 确认数据库URL配置（本地开发使用localhost）
cat backend/.env | grep DATABASE_URL
# 应该是：DATABASE_URL=postgresql://dashi:dashi123@localhost:5432/dashi
```

#### 2. Docker镜像拉取超时

**问题**：`timeout` 或 `connection refused`

**原因**：国内网络访问Docker Hub速度慢

**解决方案**：
```bash
# 方案1：配置国内镜像源
sudo vim /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com"
  ]
}
sudo systemctl restart docker

# 方案2：只启动PostgreSQL和Redis（已有镜像）
sudo docker-compose up -d postgres redis
```

#### 3. pip 安装依赖超时

**问题**：`ReadTimeoutError` 或下载速度慢

**原因**：访问PyPI官方源速度慢

**解决方案**：
```bash
# 配置清华镜像源（永久）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 或在requirements.txt安装时指定
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 4. SQLAlchemy字段名保留字错误

**问题**：`ProgrammingError: 'metadata' is a reserved word`

**原因**：使用了数据库保留字作为字段名

**解决方案**：
```python
# 不要使用：metadata, type, order, group 等保留字
# 改用：extra_data, item_type, order_info 等
class User(Base):
    # 错误
    metadata = Column(JSONB)
    
    # 正确
    extra_data = Column(JSONB)
```

#### 5. 微信登录失败

**问题**：`invalid code` 或 `code2session failed` 或 `invalid appid`

**原因**：
- 未配置正确的AppID和Secret
- Code已过期（5分钟有效期）
- 前后端AppID不一致
- 网络连接问题

**解决方案**：
```bash
# 1. 检查后端配置
cat backend/.env | grep WX_APPID
cat backend/.env | grep WX_SECRET

# 2. 检查前端配置
cat frontend/src/manifest.json | grep appid

# 3. 确保前后端配置一致
# backend/.env: WX_APPID=wx1234567890abcdef
# frontend/src/manifest.json: "appid": "wx1234567890abcdef"

# 4. 测试API（会返回微信API错误信息）
curl -X POST http://localhost:8000/api/v1/auth/wx-login \
  -H "Content-Type: application/json" \
  -d '{"code":"test_code"}'
```

#### 6. AI对话无响应

**问题**：OpenAI API超时或无响应

**原因**：
- OpenAI API Key 未配置或无效
- Token余额不足
- 网络问题（国内访问OpenAI需要代理）

**解决方案**：
```bash
# 1. 检查配置
cat backend/.env | grep OPENAI_API_KEY

# 2. 测试API Key是否有效
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-xxxxx"

# 3. 配置代理（如使用代理）
# 编辑 backend/.env
OPENAI_BASE_URL=https://your-proxy-url/v1

# 4. 查看后端日志排查错误
ps aux | grep uvicorn
tail -f /path/to/backend.log
```

#### 7. 数据库迁移失败

**问题**：`alembic upgrade head` 报错

**原因**：
- 数据库未启动
- 迁移文件冲突
- 数据库状态与迁移不一致

**解决方案**：
```bash
# 方案1：检查数据库连接
sudo docker-compose ps
psql -U dashi -d dashi -h localhost -c "SELECT version();"

# 方案2：查看当前迁移版本
cd backend
source venv/bin/activate
alembic current

# 方案3：重置数据库（开发环境）
sudo docker-compose down -v
sudo docker-compose up -d postgres redis
sleep 10
alembic upgrade head

# 方案4：查看迁移历史
alembic history
```

#### 8. Pydantic配置格式错误

**问题**：`validation error` 或 `.env` 文件解析错误

**原因**：环境变量使用了错误的格式（如Python列表格式）

**解决方案**：
```bash
# 错误格式（Python列表）
CORS_ORIGINS=["http://localhost:3000","https://example.com"]

# 正确格式（JSON数组字符串）
CORS_ORIGINS=["http://localhost:3000","https://example.com"]

# 或使用逗号分隔
CORS_ORIGINS=http://localhost:3000,https://example.com
```

#### 9. 端口被占用

**问题**：`Address already in use` (端口8000/5432/6379)

**原因**：端口已被其他进程占用

**解决方案**：
```bash
# 查找占用进程
sudo netstat -tlnp | grep :8000
# 或
sudo lsof -i :8000

# 停止进程
kill -9 <PID>

# 或停止uvicorn进程
pkill -f uvicorn

# 或使用其他端口
uvicorn app.main:app --port 8001 --reload
```

### 前端问题

#### 1. sass 依赖缺失

**问题**：编译时报错 `Cannot find module 'sass'` 或 `Deprecation Warning [legacy-js-api]`

**原因**：项目使用了scss样式但未安装sass依赖

**解决方案**：
```bash
cd frontend
npm install -D sass

# 重新编译
npm run dev:mp-weixin
```

> **说明**：Deprecation Warning 是sass版本警告，不影响使用，可以忽略。

#### 2. TypeScript配置警告

**问题**：`tsconfig.json` 显示红色/错误

**原因**：
- `@vue/tsconfig` 包未安装
- VS Code的TypeScript插件问题
- node_modules需要重新安装

**解决方案**：

方案1：安装缺失的依赖
```bash
npm install @vue/tsconfig --save-dev
```

方案2：重新安装依赖
```bash
rm -rf node_modules package-lock.json
npm install
```

方案3：忽略警告（不影响运行）
```bash
npm run dev:mp-weixin  # 如果能正常运行，说明配置没问题
```

#### 3. 前端打包失败

**问题**：`build error` 或编译错误

**原因**：
- 依赖缺失或版本不兼容
- Node.js版本过低
- 缓存问题

**解决方案**：
```bash
# 清除缓存
rm -rf node_modules package-lock.json dist
npm install

# 检查Node版本
node -v  # 应该是 v22+

# 重新编译
npm run dev:mp-weixin
```

#### 4. uni-app类型报错

**问题**：`Cannot find name 'uni'`

**原因**：TypeScript类型定义缺失

**解决方案**：
```bash
# 确保安装了类型定义
npm install @dcloudio/types --save-dev
```

并在 `tsconfig.json` 中包含：
```json
{
  "compilerOptions": {
    "types": ["@dcloudio/types", "@dcloudio/uni-app"]
  }
}
```

#### 5. Pinia状态管理问题

**问题**：`Module 'pinia' has no exported member`

**原因**：Pinia未安装或未正确初始化

**解决方案**：
```bash
# 确保Pinia已安装
npm install pinia

# 检查main.ts中是否正确初始化
# import { createPinia } from 'pinia'
# const pinia = createPinia()
# app.use(pinia)
```

#### 6. API请求失败

**问题**：`request:fail` 或 `Network Error`

**原因**：
- 后端服务未启动
- API地址配置错误
- 跨域问题（H5模式）

**解决方案**：
```bash
# 1. 检查后端服务
curl http://localhost:8000/health

# 2. 检查API地址配置
cat frontend/src/api/request.ts
# 确认 baseURL 配置正确

# 3. 微信小程序需要在开发者工具中勾选：
# 详情 -> 本地设置 -> 不校验合法域名
```

#### 7. 微信开发者工具调试技巧

**常用操作**：
- 使用控制台查看日志：`console.log()`
- 使用Network面板查看请求
- 使用Storage面板查看本地存储
- 使用AppData面板查看页面数据
- 真机调试时注意合法域名配置

**开发设置**：
- 勾选"不校验合法域名"（开发环境）
- 勾选"不校验TLS版本"
- 启用"开发者工具安全域名"

## 团队协作提示

### 环境差异说明

- **网络环境**：国内网络建议配置代理或镜像源
- **数据库方案**：Docker容器（推荐）或本地安装
- **后端运行方式**：宿主机运行（开发）或Docker容器（生产）
- **代理地址**：根据实际网络情况配置（示例：192.168.1.175:7890）

---

**文档版本**：v2.0  
**最后更新**：2025-10-19  
**维护者**：开发团队

**更新日志**：
- v2.0 (2025-10-19): 改为默认使用本地开发模式，补充数据库迁移步骤，合并常见问题，优化文档结构
- v1.1 (2025-10-19): 新增常用开发命令、快速检查清单
- v1.0 (2025-10-18): 初始版本

