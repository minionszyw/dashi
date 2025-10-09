# 快速上手指南 - 国学大师

> 5分钟快速启动项目！

## 📋 准备工作

### 必需工具
- ✅ Docker 20.10+
- ✅ Docker Compose 2.0+
- ✅ 微信开发者工具

### 可选工具（手动启动需要）
- Node.js 16+
- Python 3.11+
- Poetry

## 🚀 方法一：Docker一键启动（推荐）

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/dashi.git
cd dashi
```

### 2. 配置环境变量

```bash
# 复制配置文件
cp backend/config.example.env .env

# 编辑配置（填写必要信息）
vim .env
```

**必须配置的项目**：
```bash
# 微信配置（从微信公众平台获取）
WECHAT_APPID=your-wechat-appid
WECHAT_SECRET=your-wechat-secret

# DeepSeek配置（从DeepSeek平台获取）
DEEPSEEK_API_KEY=your-deepseek-api-key

# JWT密钥（生成随机字符串）
JWT_SECRET_KEY=$(openssl rand -hex 32)
```

### 3. 一键启动

```bash
# 使用快速启动脚本
bash scripts/quick-start.sh

# 或手动启动
docker-compose up -d
```

### 4. 验证服务

访问以下地址确认服务正常：
- API服务: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 5. 前端开发

```bash
cd web
npm install
npm run dev:mp-weixin
```

### 6. 微信开发者工具

1. 打开微信开发者工具
2. 导入项目 → 选择 `web/dist/dev/mp-weixin` 目录
3. 配置AppID（可使用测试号）
4. 开发设置 → 勾选"不校验合法域名"
5. 开始开发！

## 🛠️ 方法二：手动启动

### 1. 启动后端

```bash
cd backend

# 安装Poetry
pip install poetry

# 安装依赖
poetry install

# 配置环境变量
cp config.example.env .env
vim .env

# 启动数据库
docker-compose up -d db redis

# 初始化数据库
poetry run python scripts/init_db.py

# 启动后端服务
poetry run uvicorn app.main:app --reload
```

### 2. 启动前端

```bash
cd web

# 安装依赖
npm install

# 配置环境变量
cat > .env.development << EOF
VITE_API_BASE_URL=http://localhost:8000
EOF

# 启动开发服务器
npm run dev:mp-weixin
```

## 🎯 快速测试

### 1. 测试API

访问 http://localhost:8000/docs

尝试以下接口：
1. `GET /health` - 健康检查
2. `POST /api/v1/auth/wechat/login` - 登录（需要微信code）
3. `GET /api/v1/chat/sessions` - 获取会话列表

### 2. 测试前端

1. 打开微信开发者工具
2. 点击"登录"按钮
3. 使用测试号登录
4. 在对话页面发送消息
5. 查看AI回复

## 📱 获取微信测试号

如果还没有小程序AppID：

1. 访问：https://mp.weixin.qq.com/wxamp/sandbox
2. 扫码登录获取测试号
3. 复制 AppID 和 AppSecret
4. 配置到 `.env` 文件

## 🔑 获取DeepSeek API Key

1. 访问：https://platform.deepseek.com
2. 注册/登录账号
3. 进入控制台
4. 创建API Key
5. 复制到 `.env` 文件

## 🐛 常见问题

### Q1: Docker启动失败？

**检查Docker状态**：
```bash
docker --version
docker-compose --version
sudo systemctl status docker
```

**解决方法**：
```bash
# 启动Docker服务
sudo systemctl start docker

# 重新启动容器
docker-compose down
docker-compose up -d
```

### Q2: 数据库连接失败？

**检查数据库**：
```bash
docker-compose ps db
docker-compose logs db
```

**解决方法**：
```bash
# 重启数据库
docker-compose restart db

# 测试连接
docker exec -it dashi-db psql -U dashi -d dashi
```

### Q3: 微信登录失败？

**检查配置**：
1. AppID和Secret是否正确
2. 是否配置了正确的环境变量
3. 后端服务是否正常运行

**调试方法**：
```bash
# 查看后端日志
docker-compose logs -f api

# 检查环境变量
docker-compose exec api env | grep WECHAT
```

### Q4: AI调用失败？

**检查DeepSeek配置**：
```bash
# 查看API Key配置
docker-compose exec api env | grep DEEPSEEK

# 测试API可用性
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Q5: 前端请求失败？

**检查API地址**：
1. `.env.development` 中API地址是否正确
2. 后端服务是否正常运行
3. 微信开发者工具是否关闭域名校验

**解决方法**：
```bash
# 检查后端服务
curl http://localhost:8000/health

# 查看前端配置
cat web/.env.development
```

## 📊 服务管理

### 查看服务状态

```bash
docker-compose ps
```

### 查看日志

```bash
# 所有服务
docker-compose logs -f

# 特定服务
docker-compose logs -f api
docker-compose logs -f db
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart api
```

### 停止服务

```bash
# 停止服务
docker-compose down

# 停止并删除数据
docker-compose down -v
```

## 🎉 成功启动！

启动成功后，你应该能看到：

✅ 后端API正常运行（http://localhost:8000）  
✅ 数据库连接成功  
✅ Redis缓存正常  
✅ 前端小程序编译成功  
✅ 微信开发者工具加载项目

## 📚 下一步

1. **阅读文档**
   - [README.md](README.md) - 项目介绍
   - [SETUP.md](SETUP.md) - 详细配置
   - [Ideation.md](Ideation.md) - 项目构思

2. **开发功能**
   - 查看 [后端API文档](http://localhost:8000/docs)
   - 修改前端页面代码
   - 测试AI对话功能

3. **部署上线**
   - 配置生产环境
   - 申请正式AppID
   - 配置服务器域名
   - 小程序提审发布

## 💡 开发技巧

### 1. 实时查看日志

```bash
# 后端日志
docker-compose logs -f api

# 数据库日志
docker-compose logs -f db
```

### 2. 进入容器调试

```bash
# 进入API容器
docker-compose exec api bash

# 进入数据库容器
docker-compose exec db psql -U dashi
```

### 3. 数据库备份

```bash
# 备份
docker exec dashi-db pg_dump -U dashi dashi > backup.sql

# 恢复
docker exec -i dashi-db psql -U dashi dashi < backup.sql
```

### 4. 代码热更新

- **后端**: 使用 `--reload` 参数，代码修改自动重启
- **前端**: Vite自动热更新，保存即生效

## 🔗 有用的链接

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [uni-app文档](https://uniapp.dcloud.io/)
- [微信小程序文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [DeepSeek API文档](https://platform.deepseek.com/docs)
- [Docker文档](https://docs.docker.com/)

---

**遇到问题？**
- 查看 [SETUP.md](SETUP.md) 详细配置
- 提交 [Issue](https://github.com/yourusername/dashi/issues)
- 联系开发者: minionszyw@gmail.com

祝开发顺利！🚀

