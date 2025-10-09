#!/bin/bash

# 生产环境部署脚本

set -e

echo "🚀 开始部署国学大师项目..."
echo ""

# 检查是否在正确的分支
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "⚠️  当前不在main分支，是否继续部署？(y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "❌ 取消部署"
        exit 1
    fi
fi

# 拉取最新代码
echo "📥 拉取最新代码..."
git pull origin "$CURRENT_BRANCH"

# 检查环境变量
if [ ! -f .env ]; then
    echo "❌ 未找到.env文件，请先配置环境变量"
    exit 1
fi

# 检查必要的环境变量
required_vars=("DATABASE_URL" "REDIS_URL" "JWT_SECRET_KEY" "WECHAT_APPID" "DEEPSEEK_API_KEY")
for var in "${required_vars[@]}"; do
    if ! grep -q "^${var}=" .env; then
        echo "❌ 环境变量 ${var} 未配置"
        exit 1
    fi
done

echo "✅ 环境配置检查完成"
echo ""

# 备份数据库
echo "💾 备份数据库..."
timestamp=$(date +%Y%m%d_%H%M%S)
docker exec dashi-db pg_dump -U dashi dashi > "backup_${timestamp}.sql"
echo "✅ 数据库备份完成: backup_${timestamp}.sql"
echo ""

# 停止旧服务
echo "🛑 停止旧服务..."
docker-compose down

# 构建新镜像
echo "🔨 构建新镜像..."
docker-compose build --no-cache

# 启动新服务
echo "🚀 启动新服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 健康检查
echo "🏥 健康检查..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$response" = "200" ]; then
    echo "✅ 服务健康检查通过"
else
    echo "❌ 服务健康检查失败，HTTP状态码: $response"
    echo "🔄 回滚到备份..."
    docker-compose down
    # 这里可以添加回滚逻辑
    exit 1
fi

# 显示服务状态
echo ""
echo "📊 服务状态："
docker-compose ps

echo ""
echo "✅ 部署完成！"
echo ""
echo "📍 服务地址："
echo "- API服务: http://your-domain.com"
echo "- API文档: http://your-domain.com/docs"
echo ""
echo "📝 后续步骤："
echo "1. 检查服务日志: docker-compose logs -f api"
echo "2. 测试API接口"
echo "3. 小程序提审发布"
echo ""
echo "💡 提示："
echo "- 数据库备份: backup_${timestamp}.sql"
echo "- 如需回滚，请联系管理员"

