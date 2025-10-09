#!/bin/bash

# 国学大师项目快速启动脚本

set -e

echo "🚀 欢迎使用国学大师快速启动脚本"
echo ""

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未安装Docker，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 未安装Docker Compose，请先安装Docker Compose"
    exit 1
fi

echo "✅ Docker环境检查通过"
echo ""

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "⚠️  未找到.env文件，正在创建..."
    if [ -f backend/config.example.env ]; then
        cp backend/config.example.env .env
        echo "✅ 已创建.env文件，请编辑填写必要配置"
        echo ""
        echo "需要配置的项目："
        echo "- WECHAT_APPID: 微信小程序AppID"
        echo "- WECHAT_SECRET: 微信小程序Secret"
        echo "- DEEPSEEK_API_KEY: DeepSeek API密钥"
        echo "- JWT_SECRET_KEY: JWT密钥（生产环境必须修改）"
        echo ""
        read -p "是否现在编辑配置文件？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-vi} .env
        else
            echo "⚠️  请手动编辑.env文件后再次运行此脚本"
            exit 0
        fi
    else
        echo "❌ 未找到配置模板文件"
        exit 1
    fi
fi

echo "✅ 环境配置检查完成"
echo ""

# 启动服务
echo "🔄 正在启动Docker服务..."
docker-compose up -d

echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo ""
echo "📊 服务状态："
docker-compose ps

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "📍 访问地址："
echo "- API服务: http://localhost:8000"
echo "- API文档: http://localhost:8000/docs"
echo "- 健康检查: http://localhost:8000/health"
echo ""
echo "📝 下一步："
echo "1. 打开微信开发者工具"
echo "2. 导入项目: web/dist/dev/mp-weixin"
echo "3. 配置AppID"
echo "4. 开始开发！"
echo ""
echo "🛠️  常用命令："
echo "- 查看日志: docker-compose logs -f"
echo "- 停止服务: docker-compose down"
echo "- 重启服务: docker-compose restart"
echo ""
echo "📚 更多信息请查看 README.md 和 SETUP.md"

