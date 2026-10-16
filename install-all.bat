@echo off
chcp 65001 >nul
echo ============================================
echo   yihaiyoudao 技能包一键安装（5 个技能）
echo   前提：本机已安装 OpenClaw（见安装手册 2.3）
echo ============================================
echo.
echo [1/6] 安装 pi-jev 决策层...
openclaw skills install @lichengyu1207/pi-jev
echo [2/6] 安装 zhanlue-peipao 战略陪跑...
openclaw skills install @lichengyu1207/zhanlue-peipao
echo [3/6] 安装 qingchuang-shizhan 内容创业...
openclaw skills install @lichengyu1207/qingchuang-shizhan
echo [4/6] 安装 yihaiyoudao 内容审核...
openclaw skills install @lichengyu1207/yihaiyoudao
echo [5/6] 安装 ip-peipao-9clients 客户陪跑...
openclaw skills install @lichengyu1207/ip-peipao-9clients
echo [6/6] 更新全部已装技能...
openclaw skills update --all
echo.
echo ============================================
echo   全部完成！装好后记得激活：
echo   进入技能目录运行 python scripts/activate.py
echo   （没有 Python 就让 AI 生成安装编号）
echo ============================================
pause
