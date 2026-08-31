@echo off
chcp 65001 >nul
REM 咪蒙文集 - GitHub Pages 部署脚本 (Windows)
REM 仓库: git@github.com:Chandler-Song/mimeng.git
REM 访问: https://chandler-song.github.io/mimeng/

set REMOTE_URL=git@github.com:Chandler-Song/mimeng.git
set BRANCH=main

echo ========================================
echo   咪蒙文集 - GitHub Pages 部署脚本
echo ========================================
echo.

REM 检查是否在项目根目录
if not exist "book\index.html" (
    echo ❌ 错误: 请在项目根目录运行此脚本
    exit /b 1
)

echo 步骤1: Git 初始化...
if not exist ".git" (
    git init
    echo   ✅ Git 仓库已初始化
) else (
    echo   Git 仓库已存在
)

echo.
echo 步骤2: 配置远程仓库...
git remote remove origin 2>nul
git remote add origin %REMOTE_URL%
echo   ✅ Remote 已配置

echo.
echo 步骤3: 检查必要文件...
if exist ".gitignore" (echo   ✅ .gitignore) else (echo   ❌ 缺少 .gitignore & exit /b 1)
if exist "book\.nojekyll" (echo   ✅ book\.nojekyll) else (echo   ❌ 缺少 book\.nojekyll & exit /b 1)
if exist ".github\workflows\deploy.yml" (echo   ✅ deploy.yml) else (echo   ❌ 缺少 deploy.yml & exit /b 1)
if exist "book\index.html" (echo   ✅ index.html) else (echo   ❌ 缺少 index.html & exit /b 1)

echo.
echo 步骤4: 提交代码...
git add -A
git commit -m "feat: 咪蒙文集 - 747篇文章网页版"
echo   ✅ 代码已提交

echo.
echo 步骤5: 推送到远程仓库...
git branch -M %BRANCH%
git push -u origin %BRANCH%
echo   ✅ 代码已推送

echo.
echo ========================================
echo   ✅ 部署脚本执行完成！
echo ========================================
echo.
echo 📋 后续手动操作（重要！）：
echo    1. 打开 GitHub 仓库 Settings → Pages
echo    2. Source 选择 "GitHub Actions"
echo    3. 等待 Actions 自动部署完成
echo.
echo 🌐 访问地址:
echo    https://chandler-song.github.io/mimeng/
echo.
pause