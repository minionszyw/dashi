# 开发文档

## 环境准备

### 系统要求

- **操作系统**：Linux (Ubuntu 20.04+), macOS, Windows WSL2
- **Python**：3.12+
- **Node.js**：22+
- **Docker**：20.10+ & Docker Compose 2.0+

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
vim backend/.env
```

### 3. 启动后端服务

```bash
cd backend

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# 安装依赖
pip install -r requirements.txt

# 执行数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 启动前端服务

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器（微信小程序）
npm run dev:mp-weixin
```

### 5. 验证运行

```bash
# 检查后端API
curl http://localhost:8000/health

# 访问API文档
open http://localhost:8000/docs
```

### 6. 微信小程序预览

1. 打开微信开发者工具
2. 导入项目目录：`frontend/dist/dev/mp-weixin`
3. 配置AppID（测试号或正式AppID）
4. 点击编译预览

## 开发指南

### 后端开发

#### 项目结构

```
backend/
├── app/
│   ├── api/v1/          # API路由
│   ├── core/            # 核心配置
│   ├── models/          # 数据库模型
│   ├── schemas/         # Pydantic模型
│   ├── services/        # 业务逻辑层
│   ├── prompts/         # AI提示词管理
│   └── utils/           # 工具函数
├── alembic/             # 数据库迁移
└── requirements.txt     # Python依赖
```

#### 创建新的API端点

```python
# app/api/v1/example.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/example")
async def get_example(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {"message": "Hello World"}
```

#### 创建数据库模型

```python
# app/models/example.py
from sqlalchemy import Column, String, DateTime
from app.core.database import Base
import uuid

class Example(Base):
    __tablename__ = "examples"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

#### 创建数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "add example table"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### 前端开发

#### 项目结构

```
frontend/src/
├── api/                 # API接口封装
├── components/          # 公共组件
├── pages/               # 页面
├── stores/              # Pinia状态管理
├── types/               # TypeScript类型
├── utils/               # 工具函数
└── styles/              # 全局样式
```

#### API请求封装

```typescript
// api/request.ts
export const request = <T>(options: UniApp.RequestOptions): Promise<T> => {
  return new Promise((resolve, reject) => {
    uni.request({
      ...options,
      url: BASE_URL + options.url,
      header: { 'Authorization': `Bearer ${token}`, ...options.header },
      success: (res) => res.data.code === 0 ? resolve(res.data.data) : reject(res.data),
      fail: reject
    })
  })
}
```

#### Pinia状态管理

```typescript
// stores/user.ts
export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref('')
  const isLogin = computed(() => !!token.value)
  
  const login = async (code: string) => {
    const data = await authApi.wxLogin(code)
    token.value = data.token
    user.value = data.user
  }
  
  return { user, token, isLogin, login }
})
```

## 调试技巧

### 后端调试

#### VSCode调试配置

创建 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

#### 日志调试

```python
import logging
logger = logging.getLogger(__name__)

# 使用
logger.info("用户登录: %s", user.id)
logger.error("错误信息: %s", error)
```

### 前端调试

#### 微信开发者工具

1. 打开调试器：`F12` 或 右上角"调试器"
2. Console查看日志
3. Network查看网络请求
4. Storage查看本地存储

#### 真机调试

1. 微信开发者工具 → 预览 → 扫码
2. 真机上打开vConsole：点击右上角 → 打开调试
3. 查看Console、Network、System信息

## 常用开发命令

### 后端命令

```bash
# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 数据库迁移
alembic revision --autogenerate -m "描述"
alembic upgrade head
alembic downgrade -1

# 依赖管理
pip install <package>
pip freeze > requirements.txt

# 代码检查
pylint app/
black app/ --check
```

### 前端命令

```bash
# 开发
npm run dev:mp-weixin    # 微信小程序
npm run dev:h5           # H5

# 构建
npm run build:mp-weixin
npm run build:h5

# 类型检查
npm run type-check
```

### Docker命令

```bash
# 启动所有服务
docker-compose up -d

# 启动指定服务
docker-compose up -d postgres redis

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f postgres

# 重启服务
docker-compose restart postgres
```

## 常见问题

### 1. 后端启动失败

**问题**：`sqlalchemy.exc.OperationalError: could not connect to server`

**解决**：
```bash
# 检查PostgreSQL服务
sudo docker-compose ps postgres

# 重启PostgreSQL
sudo docker-compose restart postgres

# 检查环境变量
cat backend/.env | grep DATABASE_URL
```

### 2. 前端编译错误

**问题**：`Module not found: Error: Can't resolve '@/xxx'`

**解决**：
```bash
# 清除缓存
rm -rf node_modules
rm package-lock.json

# 重新安装
npm install

# 清除编译缓存
rm -rf dist
npm run dev:mp-weixin
```

### 3. 微信小程序白屏

**问题**：小程序打开后白屏，无任何显示

**解决**：
1. 检查微信开发者工具Console是否有错误
2. 检查`manifest.json`中的AppID是否正确
3. 清除缓存：工具 → 清除缓存 → 清除全部缓存
4. 重新编译

### 4. API请求超时

**问题**：前端请求后端API超时

**解决**：
```bash
# 检查后端是否运行
curl http://localhost:8000/health

# 检查前端API配置
# frontend/src/api/request.ts
const BASE_URL = 'http://localhost:8000'  # 确保地址正确

# 微信小程序需要配置合法域名
# manifest.json → mp-weixin → h5 → devServer
```

### 5. 数据库迁移冲突

**问题**：`alembic.util.exc.CommandError: Can't locate revision identified by 'xxx'`

**解决**：
```bash
# 查看当前版本
alembic current

# 查看迁移历史
alembic history

# 强制设置版本（谨慎使用）
alembic stamp head
```

### 6. Token余额不足

**问题**：对话时提示"Token余额不足"

**解决**：
```sql
-- 连接PostgreSQL
psql -U postgres -d dashi

-- 查询用户余额
SELECT id, nickname, token_balance FROM users;

-- 增加用户余额（测试用）
UPDATE users SET token_balance = 10000 WHERE id = 'user-id';
```

### 7. 微信登录失败

**问题**：点击登录后无响应或报错

**解决**：
1. 检查 `backend/.env` 中的 `WX_APPID` 和 `WX_SECRET`
2. 确保微信开发者工具中的AppID与配置一致
3. 检查后端日志：`docker-compose logs -f backend`
4. 测试环境可以使用测试号（不需要企业认证）

### 8. TabBar图标不显示

**问题**：微信小程序TabBar图标不显示

**解决**：
1. 确认图标格式为PNG（不支持SVG）
2. 图标尺寸建议81×81像素
3. 清除缓存后重新编译
4. 检查 `pages.json` 中路径是否正确

## 团队协作提示

### Git提交规范

```bash
# 提交格式
git commit -m "type(scope): subject"

# 示例
git commit -m "feat(chat): 实现流式对话功能"
git commit -m "fix(auth): 修复登录失败的问题"
git commit -m "docs(readme): 更新安装说明"
```

### 分支管理

```bash
# 开发新功能
git checkout -b feature/chat-history

# 修复Bug
git checkout -b bugfix/login-error

# 完成后合并到main
git checkout main
git merge feature/chat-history
```

### 代码审查要点

1. **功能完整性**：是否实现了需求
2. **代码规范**：是否符合项目规范
3. **错误处理**：是否有完善的异常处理
4. **测试覆盖**：是否有必要的测试
5. **文档更新**：是否更新了相关文档

---

**文档版本**：v2.0  
**最后更新**：2025-10-23  
**行数**：约500行（精简版）

> 更多详细信息请参考：
> - [项目设计文档](design.md)
> - [部署文档](deploy.md)
> - [AI对话架构](ai-chat-architecture.md)
> - [开发规范](.cursor/rules/)
