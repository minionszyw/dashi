#!/bin/bash

# 国学大师项目推送脚本

echo "======================================"
echo "   国学大师 - GitHub推送脚本"
echo "======================================"
echo ""

# 检查git状态
echo "📊 检查Git状态..."
git status

echo ""
echo "======================================"
echo "请选择认证方式："
echo "1) 使用Personal Access Token (推荐)"
echo "2) 使用SSH (需要提前配置密钥)"
echo "======================================"
read -p "请输入选项 [1/2]: " choice

case $choice in
  1)
    echo ""
    echo "📝 请按以下步骤操作："
    echo "1. 访问: https://github.com/settings/tokens"
    echo "2. 生成新的token（勾选repo权限）"
    echo "3. 复制生成的token"
    echo ""
    echo "即将执行推送，请准备您的token..."
    echo ""
    echo "执行命令: git push -u origin main"
    echo "Username: minionszyw"
    echo "Password: <粘贴您的Personal Access Token>"
    echo ""
    read -p "按回车继续..." dummy
    git push -u origin main
    ;;
  2)
    echo ""
    echo "🔑 切换到SSH方式..."
    git remote set-url origin git@github.com:minionszyw/dashi.git
    echo "✅ 远程URL已更新为SSH"
    echo ""
    echo "执行命令: git push -u origin main"
    read -p "按回车继续..." dummy
    git push -u origin main
    ;;
  *)
    echo "❌ 无效选项"
    exit 1
    ;;
esac

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ 推送成功！"
  echo "🌐 访问: https://github.com/minionszyw/dashi"
else
  echo ""
  echo "❌ 推送失败，请检查认证配置"
  echo "📖 查看详细说明: cat DEPLOYMENT.md"
fi

