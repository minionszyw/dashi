# 部署文档

## 部署架构

```
┌─────────────────────────────────────────────┐
│              Nginx (反向代理)                 │
│         https://yourdomain.com               │
└──────────────┬──────────────────────────────┘
               │
    ┌──────────┼──────────┐
    │                     │
    ↓                     ↓
┌─────────┐         ┌─────────┐
│  后端   │         │  前端   │
│ FastAPI │         │  静态   │
│  8000   │         │  网页   │
└────┬────┘         └─────────┘
     │
  ┌──┴──┐
  ↓     ↓
┌────┐ ┌────┐
│ PG │ │Redis│
└────┘ └────┘
```

## 服务器要求

### 最低配置

- **CPU**：2核
- **内存**：4GB
- **硬盘**：40GB SSD
- **带宽**：5Mbps
- **操作系统**：Ubuntu 20.04+ / CentOS 8+

### 推荐配置（生产环境）

- **CPU**：4核+
- **内存**：8GB+
- **硬盘**：100GB SSD
- **带宽**：10Mbps+

## 准备工作

### 1. 域名与SSL证书

```bash
# 购买域名并解析到服务器IP
A记录: @ -> 服务器IP
A记录: www -> 服务器IP

# 申请SSL证书（Let's Encrypt免费）
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 2. 安装Docker

```bash
# 安装Docker
curl -fsSL https://get.docker.com | sudo sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 3. 配置防火墙

```bash
# 开放必要端口
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## Docker部署（推荐）

### 1. 克隆项目

```bash
git clone <repository-url>
cd dashi
```

### 2. 配置环境变量

```bash
# 复制并编辑配置文件
cp backend/.env.example backend/.env
vim backend/.env
```

**必填配置**：

```bash
# 数据库配置
DATABASE_URL=postgresql://postgres:your_password@postgres:5432/dashi

# Redis配置
REDIS_URL=redis://redis:6379/0

# JWT密钥（随机生成）
SECRET_KEY=your_secret_key_here

# OpenAI配置
OPENAI_API_KEY=sk-your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# 微信小程序配置
WX_APPID=your_wx_appid
WX_SECRET=your_wx_secret
```

### 3. 启动服务

```bash
# 启动所有服务
sudo docker-compose up -d

# 查看运行状态
sudo docker-compose ps

# 查看日志
sudo docker-compose logs -f
```

### 4. 初始化数据库

```bash
# 进入后端容器
sudo docker exec -it dashi-backend bash

# 执行数据库迁移
alembic upgrade head

# 退出容器
exit
```

### 5. 配置Nginx

```nginx
# /etc/nginx/sites-available/dashi
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # 后端API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # SSE支持
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 3600s;
    }

    # 前端静态文件
    location / {
        root /var/www/dashi;
        try_files $uri $uri/ /index.html;
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

### 1. 构建前端

```bash
cd frontend

# 安装依赖
npm install

# H5构建
npm run build:h5

# 微信小程序构建
npm run build:mp-weixin
```

### 2. 部署H5

```bash
# 复制构建产物到Nginx目录
sudo cp -r dist/build/h5/* /var/www/dashi/
```

### 3. 微信小程序上传

1. 打开微信开发者工具
2. 导入 `frontend/dist/build/mp-weixin`
3. 点击"上传"
4. 填写版本号和备注
5. 提交审核

## 数据库管理

### 备份

```bash
# 备份数据库
sudo docker exec dashi-postgres pg_dump -U postgres dashi > backup_$(date +%Y%m%d).sql

# 定时备份（每天凌晨3点）
crontab -e
0 3 * * * /home/ubuntu/backup.sh
```

### 恢复

```bash
# 恢复数据库
sudo docker exec -i dashi-postgres psql -U postgres dashi < backup_20250101.sql
```

## 监控与日志

### 查看日志

```bash
# 查看所有服务日志
sudo docker-compose logs -f

# 查看指定服务日志
sudo docker-compose logs -f backend
sudo docker-compose logs -f postgres

# 查看最近100行
sudo docker-compose logs --tail=100 backend
```

### 日志切割

```bash
# /etc/logrotate.d/dashi
/var/log/dashi/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

### 监控工具（可选）

- **Prometheus + Grafana**：系统监控
- **Sentry**：错误追踪
- **Uptime Kuma**：服务可用性监控

## 更新部署

```bash
# 拉取最新代码
git pull origin main

# 重新构建并启动
sudo docker-compose down
sudo docker-compose up -d --build

# 执行数据库迁移（如果有）
sudo docker exec dashi-backend alembic upgrade head
```

## 安全加固

### 1. SSH安全

```bash
# 禁用root登录
sudo vim /etc/ssh/sshd_config
PermitRootLogin no

# 修改SSH端口
Port 2222

# 重启SSH
sudo systemctl restart sshd
```

### 2. 数据库安全

```bash
# 修改默认密码
ALTER USER postgres WITH PASSWORD 'strong_password';

# 限制远程访问
# postgresql.conf
listen_addresses = 'localhost'
```

### 3. 定期更新

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 更新Docker镜像
sudo docker-compose pull
sudo docker-compose up -d
```

## 性能优化

### 1. 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_conversations_user ON conversations(user_id);

-- 清理旧数据（可选）
DELETE FROM messages WHERE created_at < NOW() - INTERVAL '90 days';
```

### 2. Redis缓存

```python
# 缓存热点数据
# - 用户信息（TTL: 1小时）
# - 会话列表（TTL: 10分钟）
# - 八字结果（TTL: 1天）
```

### 3. Nginx优化

```nginx
# 启用Gzip压缩
gzip on;
gzip_types text/plain text/css application/json application/javascript;

# 静态资源缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 7d;
    add_header Cache-Control "public, immutable";
}
```

## 故障排查

### 1. 服务无法启动

```bash
# 查看详细日志
sudo docker-compose logs backend

# 检查端口占用
sudo netstat -tunlp | grep 8000

# 重启服务
sudo docker-compose restart backend
```

### 2. 数据库连接失败

```bash
# 检查PostgreSQL状态
sudo docker-compose ps postgres

# 测试连接
sudo docker exec dashi-postgres psql -U postgres -c "SELECT 1"

# 查看日志
sudo docker-compose logs postgres
```

### 3. 内存不足

```bash
# 查看内存使用
free -h
docker stats

# 调整容器资源限制（docker-compose.yml）
services:
  backend:
    mem_limit: 2g
    mem_reservation: 1g
```

## 成本估算

### 云服务器（按月）

- **基础版**：¥100-200/月（2核4G）
- **标准版**：¥300-500/月（4核8G）
- **企业版**：¥800-1500/月（8核16G）

### AI服务（按Token）

- **OpenAI GPT-3.5**：$0.002/1K tokens
- **国产大模型**：¥0.001-0.01/1K tokens

### 其他成本

- **域名**：¥50-100/年
- **SSL证书**：免费（Let's Encrypt）
- **对象存储**：¥0.1-0.5/GB/月
- **CDN**：¥0.2-0.8/GB

---

**文档版本**：v2.0  
**最后更新**：2025-10-23  
**行数**：约400行（精简版）

> 更多信息请参考：
> - [开发文档](development.md)
> - [项目设计](design.md)
> - [AI对话架构](ai-chat-architecture.md)
