# 部署文档

## 部署架构

```
                   Internet
                      │
                      ↓
              ┌──────────────┐
              │   CDN/域名    │
              └───────┬──────┘
                      │
                      ↓
              ┌──────────────┐
              │    Nginx      │
              │  (反向代理)    │
              └───────┬──────┘
                      │
        ┌─────────────┼─────────────┐
        │                           │
        ↓                           ↓
┌──────────────┐            ┌──────────────┐
│ FastAPI后端   │            │  静态资源     │
│ (Docker)     │            │              │
└───────┬──────┘            └──────────────┘
        │
   ┌────┴────┐
   ↓         ↓
┌────────┐ ┌────────┐
│Postgres│ │ Redis  │
└────────┘ └────────┘
```

## 服务器要求

### 最小配置（30人在线）
- **CPU**：2核
- **内存**：4GB
- **硬盘**：40GB SSD
- **带宽**：5Mbps
- **操作系统**：Ubuntu 20.04/22.04 LTS

### 推荐配置（100人在线）
- **CPU**：4核
- **内存**：8GB
- **硬盘**：100GB SSD
- **带宽**：10Mbps
- **操作系统**：Ubuntu 22.04 LTS

## 准备工作

### 1. 域名准备

```bash
# 需要准备的域名
api.yourdomain.com      # API服务
h5.yourdomain.com       # H5页面（可选）
```

### 2. SSL证书

```bash
# 使用Let's Encrypt免费证书
sudo apt install certbot
sudo certbot certonly --standalone -d api.yourdomain.com
```

### 3. 服务器基础环境

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装Nginx
sudo apt install nginx -y

# 安装Git
sudo apt install git -y
```

## Docker部署（推荐）

### 1. 克隆项目

```bash
cd /opt
sudo git clone <repository-url> dashi
cd dashi
sudo chown -R $USER:$USER /opt/dashi
```

### 2. 配置环境变量

```bash
# 创建后端环境变量
cp .env.example backend/.env
nano backend/.env
```

重要配置项：
```env
# 生产环境配置
DEBUG=False
ENVIRONMENT=production

# 数据库（使用Docker内部网络）
DATABASE_URL=postgresql://dashi:your-strong-password@postgres:5432/dashi
REDIS_URL=redis://redis:6379/0

# 微信配置
WX_APPID=your-real-appid
WX_SECRET=your-real-secret

# OpenAI配置
OPENAI_API_KEY=sk-your-real-key

# 安全配置（生成随机密钥）
JWT_SECRET_KEY=$(openssl rand -hex 32)

# 微信支付
WX_MCH_ID=your-mch-id
WX_API_KEY=your-api-key
```

### 3. 创建生产环境Docker配置

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: dashi_postgres
    environment:
      POSTGRES_DB: dashi
      POSTGRES_USER: dashi
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - dashi_network
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dashi"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: dashi_redis
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - dashi_network
    restart: always
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: dashi_backend
    env_file:
      - ./backend/.env
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - dashi_network
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  redis_data:

networks:
  dashi_network:
    driver: bridge
```

### 4. 创建生产环境Dockerfile

```dockerfile
# backend/Dockerfile.prod
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令（使用Gunicorn + Uvicorn workers）
CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

### 5. 启动服务

```bash
# 构建并启动
docker-compose -f docker-compose.prod.yml up -d --build

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f backend

# 运行数据库迁移
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### 6. 配置Nginx

```nginx
# /etc/nginx/sites-available/dashi
upstream backend {
    server localhost:8000;
    keepalive 64;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    # SSL证书
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 日志
    access_log /var/log/nginx/dashi_access.log;
    error_log /var/log/nginx/dashi_error.log;

    # 请求体大小限制
    client_max_body_size 10M;

    # 代理设置
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 静态文件缓存
    location /static {
        alias /opt/dashi/backend/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 健康检查
    location /health {
        access_log off;
        proxy_pass http://backend;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/dashi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 前端部署

### 微信小程序

#### 1. 构建生产版本

```bash
cd frontend

# 配置生产环境API地址
# 编辑 .env.production
VITE_API_BASE_URL=https://api.yourdomain.com

# 构建
npm run build:mp-weixin
```

#### 2. 上传微信平台

1. 打开微信开发者工具
2. 导入项目：`frontend/dist/build/mp-weixin`
3. 点击"上传"
4. 填写版本号和项目备注
5. 提交审核

#### 3. 配置服务器域名

在微信公众平台配置：
- **request合法域名**：`https://api.yourdomain.com`
- **socket合法域名**：`wss://api.yourdomain.com`（如使用WebSocket）
- **uploadFile合法域名**：`https://api.yourdomain.com`
- **downloadFile合法域名**：`https://api.yourdomain.com`

### H5部署（可选）

```bash
# 构建H5版本
npm run build:h5

# 将构建产物上传到服务器
scp -r dist/build/h5/* user@server:/var/www/h5
```

Nginx配置：
```nginx
server {
    listen 443 ssl http2;
    server_name h5.yourdomain.com;
    
    root /var/www/h5;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 数据库管理

### 备份

```bash
# 创建备份脚本
cat > /opt/dashi/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/dashi/backups"
mkdir -p $BACKUP_DIR

# 备份PostgreSQL
docker-compose -f /opt/dashi/docker-compose.prod.yml exec -T postgres \
    pg_dump -U dashi dashi | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# 保留最近7天的备份
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/db_$DATE.sql.gz"
EOF

chmod +x /opt/dashi/backup.sh

# 设置定时任务（每天凌晨2点）
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/dashi/backup.sh") | crontab -
```

### 恢复

```bash
# 恢复数据库
gunzip -c backups/db_20251018_020000.sql.gz | \
docker-compose -f docker-compose.prod.yml exec -T postgres \
    psql -U dashi dashi
```

## 监控与日志

### 1. 日志查看

```bash
# 查看后端日志
docker-compose -f docker-compose.prod.yml logs -f backend

# 查看Nginx日志
sudo tail -f /var/log/nginx/dashi_access.log
sudo tail -f /var/log/nginx/dashi_error.log

# 查看数据库日志
docker-compose -f docker-compose.prod.yml logs postgres
```

### 2. 性能监控

#### 安装监控工具

```bash
# 安装htop（资源监控）
sudo apt install htop

# 安装ctop（容器监控）
sudo wget https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64 -O /usr/local/bin/ctop
sudo chmod +x /usr/local/bin/ctop
```

#### 使用Prometheus + Grafana（进阶）

```yaml
# 添加到docker-compose.prod.yml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - dashi_network

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - dashi_network
```

### 3. 告警配置

```bash
# 创建健康检查脚本
cat > /opt/dashi/healthcheck.sh << 'EOF'
#!/bin/bash
ENDPOINT="https://api.yourdomain.com/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $ENDPOINT)

if [ $RESPONSE != "200" ]; then
    echo "Health check failed! Status: $RESPONSE"
    # 发送告警（邮件/钉钉/企业微信）
    curl -X POST "your-alert-webhook-url" \
        -H "Content-Type: application/json" \
        -d '{"text":"API服务异常，请检查！"}'
fi
EOF

chmod +x /opt/dashi/healthcheck.sh

# 每5分钟检查一次
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/dashi/healthcheck.sh") | crontab -
```

## 更新部署

### 滚动更新

```bash
cd /opt/dashi

# 拉取最新代码
git pull origin main

# 重新构建并启动（零停机）
docker-compose -f docker-compose.prod.yml up -d --build --no-deps backend

# 运行迁移
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# 查看状态
docker-compose -f docker-compose.prod.yml ps
```

### 回滚

```bash
# 查看提交历史
git log --oneline

# 回滚到指定版本
git checkout <commit-hash>

# 重新部署
docker-compose -f docker-compose.prod.yml up -d --build backend
```

## 安全加固

### 1. 防火墙配置

```bash
# 安装ufw
sudo apt install ufw

# 允许SSH
sudo ufw allow 22/tcp

# 允许HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable
```

### 2. 限流配置

Nginx限流：
```nginx
# 在http块中添加
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

# 在location块中使用
location /api {
    limit_req zone=api_limit burst=20 nodelay;
    proxy_pass http://backend;
}
```

### 3. fail2ban防止暴力破解

```bash
sudo apt install fail2ban

# 创建配置
sudo nano /etc/fail2ban/jail.local
```

```ini
[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/dashi_error.log
maxretry = 5
bantime = 3600
```

## 性能优化

### 1. 数据库优化

```sql
-- 创建必要索引
CREATE INDEX IF NOT EXISTS idx_conversations_user_created 
ON conversations(user_id, created_at DESC) 
WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_messages_conversation_created 
ON messages(conversation_id, created_at DESC);

-- 定期清理
VACUUM ANALYZE;
```

### 2. Redis配置优化

```conf
# redis.conf
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### 3. Nginx缓存

```nginx
# 添加缓存配置
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;

location /api/v1/bazi/profiles {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    proxy_pass http://backend;
}
```

## 故障排查

### 常见问题

1. **服务无法启动**
```bash
# 查看详细日志
docker-compose -f docker-compose.prod.yml logs backend

# 检查端口占用
sudo netstat -tlnp | grep 8000
```

2. **数据库连接失败**
```bash
# 进入容器检查
docker-compose -f docker-compose.prod.yml exec backend bash
psql -h postgres -U dashi -d dashi
```

3. **SSL证书过期**
```bash
# 续期证书
sudo certbot renew
sudo systemctl reload nginx
```

4. **内存不足**
```bash
# 查看内存使用
free -h

# 清理Docker缓存
docker system prune -a
```

## 成本估算

### 云服务器（阿里云/腾讯云）

- **2核4G**：约150元/月
- **域名**：约60元/年
- **SSL证书**：免费（Let's Encrypt）
- **OpenAI API**：按使用量计费（预估500-1000元/月）

**总计**：约650-1150元/月

---

**文档版本**：v1.0  
**最后更新**：2025-10-18  
**维护者**：开发团队

