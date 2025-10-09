# 国学大师 - 环境搭建指南

本文档提供完整的开发环境搭建步骤。

## 系统要求

### 开发环境
- **操作系统**: Linux / macOS / Windows
- **Node.js**: 16.0+
- **Python**: 3.11+
- **Docker**: 20.10+ (可选)
- **Docker Compose**: 2.0+ (可选)

### 生产环境
- **服务器**: 2核4GB内存 + 40GB存储
- **操作系统**: Ubuntu 20.04+ / CentOS 7+
- **Docker**: 20.10+
- **域名**: 已备案域名（微信小程序要求）

## 一、后端环境搭建

### 1.1 安装Python和Poetry

```bash
# 安装Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 添加到PATH
export PATH="$HOME/.local/bin:$PATH"

# 验证安装
poetry --version
```

### 1.2 配置后端项目

```bash
cd backend

# 安装依赖
poetry install

# 复制环境变量配置
cp .env.example .env

# 编辑环境变量
vim .env
```

### 1.3 配置环境变量

编辑 `.env` 文件：

```bash
# 数据库配置
DATABASE_URL=postgresql+asyncpg://dashi:dashi123@localhost:5432/dashi

# Redis配置
REDIS_URL=redis://localhost:6379/0

# JWT密钥（生产环境必须修改）
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# 微信配置
WECHAT_APPID=your-wechat-appid
WECHAT_SECRET=your-wechat-secret

# DeepSeek AI配置
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

### 1.4 启动数据库（Docker）

```bash
# 启动PostgreSQL和Redis
cd ..
docker-compose up -d db redis

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f db redis
```

### 1.5 初始化数据库

```bash
cd backend

# 初始化数据库表
poetry run python scripts/init_db.py

# 或使用Alembic迁移
poetry run alembic upgrade head
```

### 1.6 启动后端服务

```bash
# 开发模式
poetry run uvicorn app.main:app --reload

# 或使用脚本
bash scripts/dev.sh
```

访问：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 二、前端环境搭建

### 2.1 安装Node.js和依赖

```bash
# 安装Node.js 16+
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs

# 验证安装
node --version
npm --version

# 安装依赖
cd web
npm install
```

### 2.2 配置环境变量

编辑 `web/.env.development`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 2.3 启动前端开发服务

```bash
# 微信小程序
npm run dev:mp-weixin

# H5（浏览器预览）
npm run dev:h5
```

### 2.4 配置微信开发者工具

1. 下载微信开发者工具: https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
2. 打开工具，导入项目
3. 选择 `web/dist/dev/mp-weixin` 目录
4. 配置AppID（可使用测试号）
5. 开发设置 → 不校验合法域名

## 三、完整环境部署（Docker）

### 3.1 使用Docker Compose一键部署

```bash
# 配置环境变量
cp .env.example .env
vim .env  # 填写必要配置

# 启动所有服务
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 3.2 访问服务

- API服务: http://localhost:8000
- API文档: http://localhost:8000/docs
- Nginx: http://localhost

## 四、生产环境部署

### 4.1 服务器准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com | sh
sudo systemctl enable docker
sudo systemctl start docker

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 4.2 克隆代码

```bash
# 创建应用目录
sudo mkdir -p /app
cd /app

# 克隆代码
git clone https://github.com/yourusername/dashi.git
cd dashi
```

### 4.3 配置生产环境变量

```bash
# 创建生产环境配置
vim .env
```

填写生产配置：

```bash
# 数据库（使用强密码）
DATABASE_URL=postgresql+asyncpg://dashi:STRONG_PASSWORD@db:5432/dashi

# Redis
REDIS_URL=redis://redis:6379/0

# JWT密钥（必须修改为随机字符串）
JWT_SECRET_KEY=$(openssl rand -hex 32)

# 微信配置（生产AppID和Secret）
WECHAT_APPID=wx1234567890abcdef
WECHAT_SECRET=your-production-secret

# DeepSeek配置
DEEPSEEK_API_KEY=your-production-api-key

# 生产模式
DEBUG=false
```

### 4.4 配置域名和SSL

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com

# 配置Nginx
sudo vim /etc/nginx/sites-available/dashi
```

Nginx配置示例：

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4.5 启动服务

```bash
# 启动所有服务
docker-compose -f docker-compose.yml up -d

# 查看日志
docker-compose logs -f api

# 设置开机自启
sudo systemctl enable docker
```

### 4.6 配置微信小程序

1. 登录微信公众平台: https://mp.weixin.qq.com
2. 开发 → 开发管理 → 开发设置
3. 配置服务器域名:
   - request合法域名: `https://api.yourdomain.com`
   - uploadFile合法域名: `https://api.yourdomain.com`
   - downloadFile合法域名: `https://api.yourdomain.com`

### 4.7 构建发布前端

```bash
cd web

# 修改生产环境配置
vim .env.production

# 构建
npm run build:mp-weixin

# 上传代码
# 使用微信开发者工具上传 dist/build/mp-weixin 目录
```

## 五、常见问题

### 5.1 数据库连接失败

```bash
# 检查PostgreSQL状态
docker-compose ps db

# 查看日志
docker-compose logs db

# 测试连接
docker exec -it dashi-db psql -U dashi -d dashi
```

### 5.2 Redis连接失败

```bash
# 检查Redis状态
docker-compose ps redis

# 测试连接
docker exec -it dashi-redis redis-cli ping
```

### 5.3 API启动失败

```bash
# 查看详细日志
docker-compose logs -f api

# 检查环境变量
docker-compose exec api env | grep DATABASE_URL

# 进入容器调试
docker-compose exec api bash
```

### 5.4 微信登录失败

检查：
1. AppID和Secret是否正确
2. 小程序是否绑定到开放平台
3. 后端环境变量是否配置

### 5.5 AI调用失败

检查：
1. DeepSeek API Key是否有效
2. API余额是否充足
3. 网络是否能访问API服务器

## 六、监控和维护

### 6.1 日志查看

```bash
# 实时日志
docker-compose logs -f

# 查看特定服务
docker-compose logs -f api

# 查看最近100行
docker-compose logs --tail=100 api
```

### 6.2 数据备份

```bash
# 数据库备份
docker exec dashi-db pg_dump -U dashi dashi > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker exec -i dashi-db psql -U dashi dashi < backup_20231201.sql
```

### 6.3 服务重启

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart api

# 更新代码后重启
git pull
docker-compose down
docker-compose up -d --build
```

## 七、开发建议

1. **使用虚拟环境**: Poetry自动管理Python虚拟环境
2. **代码规范**: 提交前运行 `black .` 和 `flake8 .`
3. **API测试**: 使用 `/docs` 页面测试API
4. **版本控制**: 使用Git管理代码，定期提交
5. **环境隔离**: 开发、测试、生产环境分离

## 八、资源链接

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [uni-app文档](https://uniapp.dcloud.io/)
- [PostgreSQL文档](https://www.postgresql.org/docs/)
- [Redis文档](https://redis.io/docs/)
- [微信小程序文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [DeepSeek API](https://platform.deepseek.com/docs)

---

如有问题，请查看项目README或提交Issue。

