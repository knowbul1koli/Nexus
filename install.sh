#!/bin/bash
# Nexus 自动化部署脚本 (Linux amd64)

# --- 新增：强制检查是否为 root 用户 ---
if [ "$EUID" -ne 0 ]; then 
  echo "❌ 错误：请使用 root 用户或 sudo 运行此脚本！"
  exit 1
fi

echo "🚀 开始安装 Nexus 生产环境..."
APP_DIR=$(pwd)

# 1. 安装系统依赖
echo "📦 安装系统基础依赖 (Python, Nginx, SQLite)..."
apt-get update
apt-get install -y python3-venv python3-pip nginx sqlite3

# 2. 配置 Python 虚拟环境
echo "🐍 构建 Python 隔离环境并安装依赖..."
# 如果存在旧的 venv 先删掉，保证纯净
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 初始化安全数据库
echo "🗄️ 初始化数据库结构..."
if [ ! -f "manager.db" ]; then
    python3 run_init.py
    # 修改权限，允许 Nginx 读取
    chown root:www-data manager.db
    chmod 664 manager.db
else
    echo "⚠️ 检测到当前目录已存在 manager.db，跳过初始化以保护您的数据。"
fi

# 4. 配置 Systemd 守护进程
echo "⚙️ 注册 Systemd 后台服务..."
cat << EOF > /etc/systemd/system/nexus.service
[Unit]
Description=Nexus Gunicorn Service
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
# 使用单进程 + 预加载，彻底杜绝 SQLite 锁死
ExecStart=$APP_DIR/venv/bin/gunicorn --preload --workers 1 --bind 127.0.0.1:5000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 重载并启动服务
systemctl daemon-reload
systemctl enable nexus
systemctl restart nexus

echo "✅ Nexus 后台服务已成功启动并在 127.0.0.1:5000 监听！"
echo "🌐 接下来请根据 README.md 中的【双路部署方案】配置 Nginx，即可绑定域名并开放外网访问。"