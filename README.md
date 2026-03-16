<div align="center">
  <h1>🚀 Nexus</h1>
  <p><b>Matrix Site Management System / 矩阵站点管理系统</b></p>


  <p>
    <a href="https://github.com/knowbul1koli/Nexus/releases/latest"><img src="https://img.shields.io/github/v/release/knowbul1koli/Nexus?color=blue&style=flat-square" alt="Latest Release"></a>
    <a href="https://github.com/knowbul1koli/Nexus/stargazers"><img src="https://img.shields.io/github/stars/knowbul1koli/Nexus?style=flat-square" alt="Stars"></a>
    <a href="https://github.com/knowbul1koli/Nexus/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"></a>
  </p>


  <p>
    <a href="#english">🇬🇧 English</a> •
    <a href="#简体中文">🇨🇳 简体中文</a>
  </p>

</div>

---

<span id="english"></span>

## 🇬🇧 English: Nexus (v1.1.1)

Nexus is a lightweight site monitoring and navigation system featuring a modern UI, highly responsive design, and enterprise-grade role-based access control (RBAC). 

The **v1.1.1** release introduces a newly upgraded **RSS/Atom Feed Parsing Engine** for robust content fetching, implements **Frontend Base64 DOM Encryption** for ultimate credential security, and perfects the day/night interactive UI experience.

### 🚀 Core Features

- **Smart Probe Engine (v2.0)**: Prioritizes automatic RSS/Atom feed parsing with HTML fallback, intelligently fetching target site favicons and the latest article updates with high anti-blocking capabilities.
- **Enterprise-Grade Security**: Introduces invisible frontend Base64 DOM encryption, protecting sensitive credentials from being scraped or inspected.
- **Modern UI/UX**: Adopts Apple-style Glassmorphism design, supporting flawless automatic day/night theme switching and silky-smooth hover animations.
- **High Availability**: Built on SQLite concurrency lock protection and the Gunicorn `--preload` mechanism.
- **Out of the Box**: A built-in interactive automated script completes environment configuration, database repair, system daemon registration, and Nginx/HTTPS automatic binding with a single click.

### 📦 Quick Start: 3-Step Automated Installation (Linux amd64)

Please ensure you log in to your Linux server using the **`root` user** or a user with `sudo` privileges.

#### 1. Download and Extract

Execute the following commands sequentially in your server terminal:

```bash
# Download the Release v1.1.1 source code package
wget [https://github.com/knowbul1koli/Nexus/releases/download/v1.1.1/nexus-linux-amd64-v1.1.1.zip](https://github.com/knowbul1koli/Nexus/releases/download/v1.1.1/nexus-linux-amd64-v1.1.1.zip)

# Extract to a dedicated directory and enter it
unzip nexus-linux-amd64-v1.1.1.zip -d /root/site_manager
cd /root/site_manager
```

#### 2. Grant Permissions and Launch

The built-in `install.sh` handles all the tedious work of dependency installation, secure database initialization, and external access configuration.

```
# Grant execution permission
chmod +x install.sh

# Run the installation script
./install.sh
```

#### 3. Interactive Configuration

After running the script, please follow the on-screen prompts:

1. **Bind Domain/IP**: When prompted `👉 请输入您的服务器公网 IP 或 已解析的域名:`, enter your domain name or IP.
2. **Configure SSL**: When prompted `👉 是否需要为您自动申请并配置 HTTPS?`, enter `y` or `n` (If using a domain name, `y` is strongly recommended. Certbot will automatically take over the certificate application).

**🎉 Deployment Complete!** The screen will print out your default initial credentials:

- **Email**: `admin@nexus.com`
- **Account**: `superadmin`
- **Password**: `password123` *(⚠️ Security Warning: For your data security, please change the default password immediately after logging in!)*

## ⚠️ Upgrade Notice (from v1.1.0 or v1.0.0)

**Your original `manager.db` database file is fully compatible**. Extracting the `.zip` package will not overwrite your existing database. After overwriting the code files, simply re-execute `./install.sh`. The script automatically repairs and completes missing data table structures seamlessly.

## 🗑️ Uninstallation (One-Click Cleanup)

To completely clear all deployment traces, execute this command in any directory:

```
systemctl stop nexus; systemctl disable nexus; rm -f /etc/systemd/system/nexus.service; systemctl daemon-reload; rm -f /etc/nginx/sites-available/nexus /etc/nginx/sites-enabled/nexus; systemctl restart nginx; rm -rf /root/site_manager
```

------

<span id="简体中文"></span>

## 🇨🇳 简体中文: Nexus (v1.1.1)

Nexus 是一款具备现代化 UI、高度响应式设计以及企业级权限隔离的轻量级站点监控与导航系统。

全新的 **v1.1.1** 版本带来了质的飞跃：集成了优先解析 **RSS/Atom** 的智能爬虫引擎、引入了**前端 Base64 DOM 隐写加密**保护敏感数据，并彻底修复和打磨了全站的昼夜 UI 悬停交互体验。

## 🚀 核心特性

- **智能探针引擎 (v2.0)**：优先支持 RSS/Atom 信息流解析（具备极强抗屏蔽能力），并向下兼容 HTML 智能抓取，全自动更新目标站点图标及情报。
- **企业级安全防护**：首创前端 Base64 DOM 隐写术，即使通过浏览器审查元素也无法窃取专家密码，守护矩阵数据绝对安全。
- **现代 UI/UX**：采用苹果级磨砂玻璃设计，支持完美的昼夜主题自动无缝切换与丝滑悬停动画。
- **高可用架构**：底层引入 SQLite 并发锁死防护与 Gunicorn `--preload` 预加载机制。
- **开箱即用**：内置交互式自动化脚本，一键完成环境配置、数据库升级修复、守护进程注册以及 Nginx/HTTPS 自动绑定。

## 📦 极简部署：三步全自动安装 (Linux amd64)

请确保您使用 **root 用户** 或具有 `sudo` 权限的用户登录您的 Linux 服务器。

#### 1. 下载并解压程序包

在您的服务器终端中依次执行以下命令，完成源码包的下载与解压：

```
# 下载 Release v1.1.1 源码压缩包
wget [https://github.com/knowbul1koli/Nexus/releases/download/v1.1.1/nexus-linux-amd64-v1.1.1.zip](https://github.com/knowbul1koli/Nexus/releases/download/v1.1.1/nexus-linux-amd64-v1.1.1.zip)

# 解压至专属目录并进入
unzip nexus-linux-amd64-v1.1.1.zip -d /root/site_manager
cd /root/site_manager
```

#### 2. 赋予权限并一键起飞

系统内置了 `install.sh` 终极自动化脚本。它包揽了依赖安装、数据库安全初始化以及外网访问配置的所有繁琐工作。

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

**🎉 部署完成！** 脚本运行结束后，屏幕会打印出您的默认初始凭证，您可以直接通过配置好的域名或 IP 访问系统：

- **邮箱**：`admin@nexus.com`
- **账号**：`superadmin`
- **密码**：`password123` *(⚠️ 安全警告：触发安全协议阻断，请务必在首次登录后台后立即设定您的高强度密钥！)* ### ⚠️ 老用户无感升级须知 (从 v1.1.0 或更早版本) **您的原有 `manager.db` 数据库文件完全兼容，且系统会自动完成旧版密码的隐式迁移。** 解压新的 `.zip` 包绝不会覆盖您现有的数据。在覆盖最新的代码文件后，您只需重新执行一遍 `./install.sh` 脚本。脚本内置了安全修复机制，会自动为您补全缺失的数据表结构。

## 🗑️ 附录：系统彻底卸载指令 (一键清理)

如果您需要推倒重来，或彻底清除所有部署痕迹，可在终端任意目录下执行下方这一行命令。它会完全关闭服务、解绑 Nginx 端口并强制删除整个项目源码目录：

```
systemctl stop nexus; systemctl disable nexus; rm -f /etc/systemd/system/nexus.service; systemctl daemon-reload; rm -f /etc/nginx/sites-available/nexus /etc/nginx/sites-enabled/nexus; systemctl restart nginx; rm -rf /root/site_manager
```
