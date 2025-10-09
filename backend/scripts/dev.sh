#!/bin/bash

# 开发环境启动脚本

echo "🚀 启动开发环境..."

# 检查环境变量
if [ ! -f .env ]; then
    echo "⚠️  未找到.env文件，使用默认配置"
    cp .env.example .env 2>/dev/null || echo "请手动创建.env文件"
fi

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

