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

### 1. 克隆项目

```bash
git clone <repository-url>
cd dashi
```

### 2. 后端设置

#### 2.1 创建虚拟环境

```bash
cd backend
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入实际配置
```

重要配置项：
```env
DATABASE_URL=postgresql://dashi:dashi123@localhost:5432/dashi
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-your-key-here
WX_APPID=your-appid
WX_SECRET=your-secret
```

#### 2.4 启动数据库（Docker）

```bash
# 回到项目根目录
cd ..

# 启动PostgreSQL和Redis
docker-compose up -d postgres redis
```

#### 2.5 运行数据库迁移

```bash
cd backend
alembic upgrade head
```

#### 2.6 启动后端服务

```bash
# 开发模式（热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 访问API文档
# http://localhost:8000/docs
```

### 3. 前端设置

#### 3.1 安装依赖

```bash
cd frontend
npm install
```

#### 3.2 配置小程序信息

编辑 `src/manifest.json`：
```json
{
  "mp-weixin": {
    "appid": "your-appid",
    "setting": {
      "urlCheck": false
    }
  }
}
```

#### 3.3 启动开发服务

```bash
# 微信小程序
npm run dev:mp-weixin

# H5
npm run dev:h5
```

#### 3.4 在微信开发者工具中打开

1. 打开微信开发者工具
2. 导入项目：`frontend/dist/dev/mp-weixin`
3. 填入AppID
4. 开始开发

## 开发指南

### 后端开发

#### 项目结构

```
backend/
├── app/
│   ├── api/              # API路由
│   │   ├── deps.py       # 依赖注入
│   │   └── v1/           # API v1版本
│   │       ├── auth.py   # 认证接口
│   │       ├── user.py   # 用户接口
│   │       ├── bazi.py   # 八字接口
│   │       ├── chat.py   # 对话接口
│   │       └── payment.py# 支付接口
│   ├── core/             # 核心配置
│   │   ├── config.py     # 配置管理
│   │   ├── security.py   # 安全相关
│   │   └── database.py   # 数据库连接
│   ├── models/           # 数据库模型
│   │   ├── user.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── bazi_profile.py
│   │   └── order.py
│   ├── schemas/          # Pydantic模型
│   │   ├── user.py
│   │   ├── chat.py
│   │   └── bazi.py
│   ├── services/         # 业务逻辑
│   │   ├── langchain_service.py
│   │   ├── bazi_service.py
│   │   ├── wechat_service.py
│   │   └── payment_service.py
│   ├── utils/            # 工具函数
│   └── main.py           # 应用入口
├── bazi/                 # 八字计算模块
├── alembic/              # 数据库迁移
├── tests/                # 测试
└── requirements.txt      # 依赖
```

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
├── api/                  # API封装
│   ├── request.ts        # 请求封装
│   ├── auth.ts          # 认证接口
│   ├── chat.ts          # 对话接口
│   └── bazi.ts          # 八字接口
├── components/           # 组件
│   ├── MessageBubble.vue
│   ├── ChatInput.vue
│   └── LoadingSpinner.vue
├── pages/                # 页面
│   ├── chat/
│   ├── session/
│   ├── profile/
│   └── login/
├── stores/               # 状态管理
│   ├── user.ts
│   ├── chat.ts
│   └── bazi.ts
├── types/                # 类型定义
│   ├── user.ts
│   ├── chat.ts
│   └── api.ts
├── utils/                # 工具
│   ├── format.ts
│   ├── storage.ts
│   └── wx.ts
├── App.vue
├── main.ts
├── manifest.json
└── pages.json
```

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

## 测试

### 后端测试

```python
# tests/test_chat.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_send_message():
    """测试发送消息"""
    response = client.post(
        "/api/v1/chat/message",
        json={
            "conversation_id": "test-id",
            "content": "测试消息"
        },
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    
# 运行测试
# pytest tests/
```

### 前端测试

```bash
# 单元测试
npm run test:unit

# E2E测试
npm run test:e2e
```

## 常见问题

### 后端问题

#### 1. 数据库连接失败

**问题**：`could not connect to server`

**解决**：
```bash
# 检查Docker容器状态
docker-compose ps

# 查看日志
docker-compose logs postgres

# 重启数据库
docker-compose restart postgres

# 检查端口占用
sudo netstat -tlnp | grep 5432
```

#### 2. 微信登录失败

**问题**：`invalid code` 或 `code2session failed`

**原因**：
- 未配置正确的AppID和Secret
- Code已过期（5分钟有效期）
- 网络连接问题

**解决**：
- 检查 `backend/.env` 中的 `WX_APPID` 和 `WX_SECRET`
- 检查 `frontend/src/manifest.json` 中的 `appid`
- 确保前后端配置一致

#### 3. AI对话无响应

**问题**：OpenAI API超时或无响应

**原因**：
- OpenAI API Key 未配置或无效
- Token余额不足
- 网络问题（国内访问OpenAI需要代理）

**解决**：
```bash
# 1. 检查配置
cat backend/.env | grep OPENAI

# 2. 查看后端日志
docker-compose logs -f backend

# 3. 如果使用代理，配置OPENAI_BASE_URL
# 编辑 backend/.env
OPENAI_BASE_URL=https://your-proxy-url/v1
```

#### 4. 数据库迁移失败

**问题**：`alembic upgrade head` 报错

**解决**：
```bash
# 重置数据库
docker-compose down -v
docker-compose up -d

# 重新执行迁移
docker-compose exec backend alembic upgrade head
```

### 前端问题

#### 1. TypeScript配置警告

**问题**：`tsconfig.json` 显示红色/错误

**可能原因**：
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

#### 2. 前端打包失败

**问题**：`build error` 或编译错误

**解决**：
```bash
# 清除缓存
rm -rf node_modules package-lock.json
npm install

# 检查Node版本
node -v  # 应该是 v22+

# 重新打包
npm run build:mp-weixin
```

#### 3. uni-app类型报错

**问题**：`Cannot find name 'uni'`

**解决**：
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

#### 4. Pinia状态管理问题

**问题**：`Module 'pinia' has no exported member`

**解决**：
```bash
# 确保Pinia已安装
npm install pinia

# 检查main.ts中是否正确初始化
# import { createPinia } from 'pinia'
# app.use(createPinia())
```

#### 5. 微信开发者工具调试

**技巧**：
- 使用控制台查看日志
- 使用Network面板查看请求
- 使用Storage面板查看本地存储
- 真机调试时注意合法域名配置

#### 6. 编辑器配置优化

VS Code推荐设置（创建 `.vscode/settings.json`）：
```json
{
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "vetur.validation.template": false,
  "vetur.validation.script": false,
  "vetur.validation.style": false
}
```

VS Code推荐插件：
- Volar (Vue Language Features)
- TypeScript Vue Plugin
- uni-app 开发插件

## 代码规范

详见 [项目规范文档](../project_specification.md)

## 持续集成

### GitHub Actions示例

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest
  
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node
        uses: actions/setup-node@v2
        with:
          node-version: '22'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm run test
```

---

**文档版本**：v1.0  
**最后更新**：2025-10-18  
**维护者**：开发团队

