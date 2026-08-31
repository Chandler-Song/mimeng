@echo off
chcp 65001 >nul
echo ========================================
echo 咪蒙文章提取脚本
echo ========================================
echo.
echo 此脚本将自动提取PDF中的所有文章
echo 支持断点续传，可以随时中断和继续
echo.
echo 按任意键开始提取...
pause >nul

:loop
python "c:\Users\Administrator\IDEProjects\mimeng\scripts\extract_fast.py"
echo.
echo ========================================
echo 脚本已结束或超时
echo ========================================
echo.
echo 如果还有文章未提取完成，按任意键继续...
echo 如果已完成，请关闭此窗口
pause >nul
goto loop