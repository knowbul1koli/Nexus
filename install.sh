#!/bin/bash
# Nexus 终极自动化部署脚本 (环境部署 + 数据库修复 + Nginx & SSL 自动配置)

# 1. 强制检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
  echo "❌ 错误：请使用 root 用户或 sudo 运行此脚本！"
  exit 1
fi

APP_DIR=$(pwd)
echo "🚀 开始自动化安装 Nexus 生产环境..."

# 2. 安装系统所有核心依赖
echo "📦 安装系统基础依赖 (Python, Nginx, SQLite, Certbot)..."
apt-get update
apt-get install -y python3-venv python3-pip nginx sqlite3 certbot python3-certbot-nginx zip unzip

# 3. 构建 Python 隔离环境
echo "🐍 构建 Python 隔离环境并安装依赖..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. 动态生成并执行安全初始化脚本
echo "🗄️ 安全初始化与修复数据库结构..."
cat << 'EOF' > run_init.py
from app import app, db, init_defaults
from models import User, Site, Category, Setting, Subscription, SiteUpdate

with app.app_context():
    db.create_all()  # 自动补全缺失的表，不覆盖已有旧数据
    init_defaults()  # 自动生成你设定的 superadmin 默认账号
    print("✅ 数据库表结构和默认数据已完美初始化/修复！")
EOF

python3 run_init.py

# 修复数据库权限，允许 Nginx 读取，随后清理临时脚本
chown root:www-data manager.db
chmod 664 manager.db
rm -f run_init.py

# 5. 注册 Systemd 后台服务
echo "⚙️ 注册 Systemd 后台服务..."
cat << EOF > /etc/systemd/system/nexus.service
[Unit]
Description=Nexus Gunicorn Service
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
# 单进程+预加载，杜绝 SQLite 并发锁死
ExecStart=$APP_DIR/venv/bin/gunicorn --preload --workers 1 --bind 127.0.0.1:5000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable nexus
systemctl restart nexus

# ==========================================
# 6. 交互式 Nginx 与 SSL 自动化配置
# ==========================================
echo "====================================================="
echo "🌐 后端启动成功！现在开始为您配置 Nginx 外部网络访问..."
echo "====================================================="
read -p "👉 请输入您的服务器公网 IP 或 已解析的域名 (例如: 123.45.67.89 或 example.com): " USER_DOMAIN
read -p "👉 是否需要为您自动申请并配置 HTTPS (SSL小绿锁)? (需要请输入 y，仅IP访问请输入 n): " NEED_SSL

echo "📝 正在生成 Nginx 配置文件..."
cat << EOF > /etc/nginx/sites-available/nexus
server {
    listen 80;
    server_name $USER_DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }

    location /static/ {
        alias $APP_DIR/static/;
        expires 7d;
        access_log off;
    }
}
EOF

# 激活配置并重启 Nginx
ln -sf /etc/nginx/sites-available/nexus /etc/nginx/sites-enabled/
systemctl restart nginx

# 根据用户选择触发 Certbot 申请证书
if [[ "$NEED_SSL" == "y" || "$NEED_SSL" == "Y" ]]; then
    echo "🔐 开始为您申请 SSL 证书，请根据屏幕提示按要求输入..."
    certbot --nginx -d $USER_DOMAIN
    echo "✅ SSL 证书配置完成！"
fi

# ==========================================
# 7. 打印完成信息与默认密码
# ==========================================
echo "====================================================="
echo "🎉 恭喜！Nexus 全栈部署已彻底完成！"
if [[ "$NEED_SSL" == "y" || "$NEED_SSL" == "Y" ]]; then
    echo "🌐 您的访问地址为: https://$USER_DOMAIN"
else
    echo "🌐 您的访问地址为: http://$USER_DOMAIN"
fi
echo ""
echo "🔑 【系统初始超级管理员凭证】"
echo "📧 邮箱：admin@nexus.com"
echo "👤 账号：superadmin"
echo "🔒 密码：password123"
echo "⚠️ (安全警告：请立即登录后台修改此默认密码！)"
echo "====================================================="