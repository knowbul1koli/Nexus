<h2>Nexus - Matrix Site Management System</h2>

<a href="#english">English</a> | <a href="#中文版">中文版</a>

------

# English

## Nexus - Matrix Site Management System (v1.1.0 One-Click Deployment Edition)

Nexus is a lightweight site monitoring and navigation system featuring a modern UI, highly responsive design, and enterprise-grade role-based access control (RBAC). The v1.1.0 release completely refactors the underlying data flow, resolves concurrency deadlock issues, and brings an unprecedented "no-brainer" fully automated deployment experience.

## 🚀 Features

- **Smart Probe Engine**: Supports automated polling for uptime monitoring, intelligently fetching target site favicons and the latest article updates.
- **Modern UI/UX**: Adopts Apple-style Glassmorphism design and supports automatic day/night theme switching.
- **High Availability Architecture**: Introduces SQLite concurrency lock protection and Gunicorn `--preload` mechanism at the underlying layer.
- **Out of the Box**: Built-in interactive automated script to complete environment configuration, database repair, system daemon registration, and Nginx/HTTPS automatic binding with one click.

------

## 📦 Minimalist Deployment: 3-Step Automated Installation (Linux amd64)

Please ensure you log in to your Linux server using the **`root` user** or a user with `sudo` privileges.

#### 1. Download and Extract the Package

Execute the following commands sequentially in your server terminal to download and extract the source code package:

Bash

```
# Download the Release source code package
wget https://github.com/knowbul1koli/Nexus/releases/download/v1.1.0/nexus-linux-amd64-v1.1.0.zip

# Extract to a dedicated directory and enter it
unzip nexus-linux-amd64-v1.1.0.zip -d /root/site_manager
cd /root/site_manager
```

#### 2. Grant Permissions and Launch

The system includes the `install.sh` ultimate automation script. It handles all the tedious work of dependency installation, secure database initialization, and external access configuration.

Bash

```
# Grant execution permission
chmod +x install.sh

# Run the installation script
./install.sh
```

#### 3. Interactive Configuration and Completion

After running the script, please follow the on-screen prompts to complete two simple interactive steps:

1. **Bind Domain/IP**: When prompted `👉 请输入您的服务器公网 IP 或 已解析的域名:`, enter your domain name or IP and press Enter.
2. **Configure SSL**: When prompted `👉 是否需要为您自动申请并配置 HTTPS?`, enter `y` or `n` and press Enter (If using a domain name, `y` is strongly recommended. Certbot will automatically take over the certificate application).

🎉 **Deployment Complete!** After the script finishes running, the screen will print out your default initial credentials. You can access the system directly via the configured domain or IP:

- **Email**: `admin@nexus.com`

- **Account**: `superadmin`

- **Password**: `password123`

  *(⚠️ Security Warning: For your data security, please be sure to change the default password immediately after logging into the backend for the first time!)*

------

## ⚠️ Upgrade Notice for Existing Users (from v1.0.0)

If you are upgrading from v1.0.0, **your original `manager.db` database file is fully compatible**.

Extracting the `.zip` package will not overwrite your existing database. After overwriting the latest code files, you only need to re-execute the `./install.sh` script. The script has a built-in security repair mechanism that will automatically complete missing data table structures for you, and it will absolutely not affect or overwrite your existing data.

------

## 🗑️ Appendix: Complete System Uninstallation Command (One-Click Cleanup)

If you need to start over from scratch or completely clear all deployment traces, you can execute the following one-line command in the terminal in any directory. It will completely shut down the service, unbind the Nginx port, and forcefully delete the entire project source code directory:

Bash

```
systemctl stop nexus; systemctl disable nexus; rm -f /etc/systemd/system/nexus.service; systemctl daemon-reload; rm -f /etc/nginx/sites-available/nexus /etc/nginx/sites-enabled/nexus; systemctl restart nginx; rm -rf /root/site_manager
```

------

# 中文版

## Nexus - 矩阵站点管理系统 (v1.1.0 一键部署版)

Nexus 是一款具备现代化 UI、高度响应式设计以及企业级权限隔离的轻量级站点监控与导航系统。v1.1.0 版本彻底重构了底层数据流，解决了并发死锁问题，并带来了前所未有的“无脑式”全自动部署体验。

## 🚀 核心特性 (Features)

- **智能探针引擎**：支持自动化轮询测活，智能抓取目标站点图标及最新文章情报。
- **现代 UI/UX**：采用苹果级磨砂玻璃设计，支持昼夜主题自动切换。
- **高可用架构**：底层引入 SQLite 并发锁死防护与 Gunicorn `--preload` 预加载机制。
- **开箱即用**：内置交互式自动化脚本，一键完成环境配置、数据库修复、系统守护进程注册以及 Nginx/HTTPS 全自动绑定。

------

## 📦 极简部署：三步全自动安装 (Linux amd64)

请确保您使用 **root 用户** 或具有 `sudo` 权限的用户登录您的 Linux 服务器。

#### 1. 下载并解压程序包

在您的服务器终端中依次执行以下命令，完成源码包的下载与解压：

Bash

```
# 下载 Release 源码压缩包
wget https://github.com/knowbul1koli/Nexus/releases/download/v1.1.0/nexus-linux-amd64-v1.1.0.zip

# 解压至专属目录并进入
unzip nexus-linux-amd64-v1.1.0.zip -d /root/site_manager
cd /root/site_manager
```

#### 2. 赋予权限并一键起飞

系统内置了 `install.sh` 终极自动化脚本。它包揽了依赖安装、数据库安全初始化以及外网访问配置的所有繁琐工作。

Bash

```
# 赋予执行权限
chmod +x install.sh

# 运行安装脚本
./install.sh
```

#### 3. 互动配置与完成

运行脚本后，请根据屏幕提示完成两步简单的互动：

1. **绑定域名/IP**：提示 `👉 请输入您的服务器公网 IP 或 已解析的域名:` 时，输入您的域名或 IP 并回车。
2. **配置 SSL**：提示 `👉 是否需要为您自动申请并配置 HTTPS?` 时，输入 `y` 或 `n` 回车（若使用域名强烈建议选 `y`，Certbot 将全自动接管证书申请）。

🎉 **部署完成！** 脚本运行结束后，屏幕会打印出您的默认初始凭证，您可以直接通过配置好的域名或 IP 访问系统：

- **邮箱**：`admin@nexus.com`

- **账号**：`superadmin`

- **密码**：`password123`

  *(⚠️ 安全警告：为了您的数据安全，请务必在首次登录后台后立即修改默认密码！)*

------

## ⚠️ 老用户升级须知 (从 v1.0.0 升级)

如果您是从 v1.0.0 升级，**您的原有 `manager.db` 数据库文件完全兼容**。

解压 `.zip` 包不会覆盖您现有的数据库。在覆盖最新的代码文件后，您只需重新执行一遍 `./install.sh` 脚本。脚本内置了安全修复机制，会自动为您补全缺失的数据表结构，且绝对不会影响或覆盖您的已有数据。

------

## 🗑️ 附录：系统彻底卸载指令 (一键清理)

如果您需要推倒重来，或彻底清除所有部署痕迹，可在终端任意目录下执行下方这一行命令。它会完全关闭服务、解绑 Nginx 端口并强制删除整个项目源码目录：

```
systemctl stop nexus; systemctl disable nexus; rm -f /etc/systemd/system/nexus.service; systemctl daemon-reload; rm -f /etc/nginx/sites-available/nexus /etc/nginx/sites-enabled/nexus; systemctl restart nginx; rm -rf /root/site_manager
```

