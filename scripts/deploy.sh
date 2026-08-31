#!/bin/bash
# 咪蒙文集 - GitHub Pages 部署脚本
# 仓库: git@github.com:Chandler-Song/mimeng.git
# 访问: https://chandler-song.github.io/mimeng/

set -e

REMOTE_URL="git@github.com:Chandler-Song/mimeng.git"
BRANCH="main"

echo "========================================"
echo "  咪蒙文集 - GitHub Pages 部署脚本"
echo "========================================"
echo ""

# 检查是否在项目根目录
if [ ! -f "book/index.html" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查 SSH 配置
echo "步骤1: 检查 SSH 配置..."
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "  ✅ SSH 已配置"
else
    echo "  ❌ SSH 未配置，请先运行:"
    echo "     ssh-keygen -t ed25519 -C \"你的邮箱\""
    echo "     并将 ~/.ssh/id_ed25519.pub 添加到 GitHub"
    exit 1
fi

# Git 初始化
echo ""
echo "步骤2: Git 初始化..."
if [ ! -d ".git" ]; then
    git init
    echo "  ✅ Git 仓库已初始化"
else
    echo "  ⏭️  Git 仓库已存在"
fi

# 配置 remote
echo ""
echo "步骤3: 配置远程仓库..."
if git remote get-url origin 2>/dev/null; then
    git remote set-url origin "$REMOTE_URL"
    echo "  ✅ Remote 已更新"
else
    git remote add origin "$REMOTE_URL"
    echo "  ✅ Remote 已添加"
fi

# 检查必要文件
echo ""
echo "步骤4: 检查必要文件..."
for file in ".gitignore" "book/.nojekyll" ".github/workflows/deploy.yml" "book/index.html"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ 缺少 $file"
        exit 1
    fi
done

# 统计文件
echo ""
echo "步骤5: 统计文件..."
CHAPTER_COUNT=$(ls book/chapters/*.md 2>/dev/null | wc -l)
echo "  📖 章节文件: $CHAPTER_COUNT 个"
echo "  📄 HTML页面: 1 个"
echo "  🎨 封面SVG: 1 个"

# 提交代码
echo ""
echo "步骤6: 提交代码..."
git add -A

if git diff --cached --quiet; then
    echo "  ⏭️  没有变更需要提交"
else
    COMMIT_MSG="feat: 咪蒙文集 - 747篇文章网页版

- 基于book_design_style设计风格
- Navy+Gold商务配色，衬线正文
- Alpine.js双视图，marked.js渲染
- 747篇文章全部收录，按编号排序
- GitHub Actions自动部署"
    git commit -m "$COMMIT_MSG"
    echo "  ✅ 代码已提交"
fi

# 推送到远程
echo ""
echo "步骤7: 推送到远程仓库..."
git branch -M "$BRANCH"
git push -u origin "$BRANCH"
echo "  ✅ 代码已推送到 origin/$BRANCH"

# 完成提示
echo ""
echo "========================================"
echo "  ✅ 部署脚本执行完成！"
echo "========================================"
echo ""
echo "📋 后续手动操作（重要！）："
echo "   1. 打开 GitHub 仓库 Settings → Pages"
echo "   2. Source 选择 'GitHub Actions'"
echo "   3. 等待 Actions 自动部署完成"
echo ""
echo "🌐 访问地址:"
echo "   https://chandler-song.github.io/mimeng/"
echo ""
echo "📊 查看部署状态:"
echo "   https://github.com/Chandler-Song/mimeng/actions"
echo ""