import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from werkzeug.utils import secure_filename
from models import db, Site, User, Subscription, SiteUpdate, Setting, Category
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY_HERE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/avatars'
db.init_app(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DEFAULT_SETTINGS = {
    'site_title': 'Nexus',
    'favicon_url': 'https://cdn-icons-png.flaticon.com/512/3208/3208903.png',
    'bg_image': 'https://images.unsplash.com/photo-1614850523459-c2f4c699c52e?q=80&w=2670&auto=format&fit=crop',
    'bg_color': '#F4F6F9',
    'card_bg': '#FFFFFF',
    'primary_color': '#2563EB',
    'secondary_color': '#475569',
    'text_color': '#1E293B',
    'border_radius': '16',
    'shadow_opacity': '0.05'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive'
}

def init_defaults():
    if not User.query.filter_by(email='admin@nexus.com').first():
        db.session.add(User(email='admin@nexus.com', username='superadmin', password='password123', role='superadmin', alias='系统主理人', is_first_login=True))
    for key, val in DEFAULT_SETTINGS.items():
        if not Setting.query.filter_by(key=key).first():
            db.session.add(Setting(key=key, value=val))
    if not Category.query.first():
        db.session.add(Category(name='精选枢纽'))
    db.session.commit()

with app.app_context():
    db.create_all()
    init_defaults()

def update_site_status(site):
    try:
        res = requests.get(site.url, headers=HEADERS, timeout=8, verify=False, allow_redirects=True)
        if res.status_code < 500 or res.status_code == 403:
            site.status = 'online'
        else:
            site.status = 'offline'
    except Exception:
        site.status = 'offline'
    db.session.commit()

def perform_auto_fetch(site_id):
    site = db.session.get(Site, site_id)
    if not site: return False, "节点不存在"

    update_site_status(site)
    if site.status == 'offline':
        return False, "目标节点拒绝连接或已宕机，无法抓取。"

    try:
        response = requests.get(site.url, headers=HEADERS, timeout=10, verify=False)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if not site.icon_url:
            icon_tag = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
            if icon_tag and icon_tag.get('href'): site.icon_url = urllib.parse.urljoin(site.url, icon_tag['href'])

        a_title, a_link, a_summary = "", site.url, ""
        article = soup.find('article') or soup.find(class_=lambda x: x and 'post' in x.lower())
        if article:
            a_tag = article.find('a')
            if a_tag and a_tag.get_text(strip=True):
                a_title = a_tag.get_text(strip=True)
                a_link = urllib.parse.urljoin(site.url, a_tag.get('href', ''))
            p_tag = article.find('p')
            a_summary = p_tag.get_text(strip=True)[:150] + '...' if p_tag else ""
            
        if not a_title:
            heading = soup.find(['h1', 'h2', 'h3'], class_=lambda x: x and ('title' in x.lower() or 'entry' in x.lower())) or soup.find('h2')
            if heading:
                a_tag = heading.find('a')
                if a_tag: a_title, a_link = a_tag.get_text(strip=True), urllib.parse.urljoin(site.url, a_tag.get('href', ''))
                else: a_title = heading.get_text(strip=True)

        if not a_title:
            a_title = soup.title.string.strip() if soup.title else "检测到页面变动"
            meta = soup.find('meta', attrs={'name': 'description'})
            a_summary = meta['content'][:150] + '...' if meta and meta.get('content') else ""

        if not SiteUpdate.query.filter_by(site_id=site.id, article_title=a_title[:200]).first():
            db.session.add(SiteUpdate(site_id=site.id, content=a_summary, article_title=a_title[:200], article_url=a_link, is_broadcast=False))
            db.session.commit()
            return True, f"测活成功，并捕获情报：{a_title[:15]}..."
        else:
            db.session.commit()
            return True, "测活成功。目标站点内容无更新。"
    except Exception as e: 
        return False, "站点在线，但内容防爬阻断。"

def system_background_tasks(app):
    with app.app_context():
        sites = Site.query.all()
        for site in sites:
            perform_auto_fetch(site.id)

scheduler = BackgroundScheduler()
scheduler.add_job(func=system_background_tasks, args=[app], trigger="interval", minutes=10)
scheduler.start()

@app.before_request
def enforce_first_setup():
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user and user.is_first_login:
            allowed_endpoints = ['first_setup', 'logout', 'static']
            if request.endpoint not in allowed_endpoints:
                return redirect(url_for('first_setup'))

@app.context_processor
def inject_global_data():
    settings = {s.key: s.value for s in Setting.query.all()}
    curr_user = db.session.get(User, session['user_id']) if 'user_id' in session else None
    return dict(g_settings=settings, curr_user=curr_user, g_categories=Category.query.all())

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session: return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') not in ['admin', 'superadmin']: return "权限受限！", 403
        return f(*args, **kwargs)
    return decorated_function

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'superadmin': return "仅限超管操作！", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/first_setup', methods=['GET', 'POST'])
@login_required
def first_setup():
    user = db.session.get(User, session['user_id'])
    if not user.is_first_login:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        existing = User.query.filter(User.id != user.id, ((User.email == email) | (User.username == username))).first()
        if existing:
            flash('该邮箱或代号已被其他人员占用，请更换。', 'danger')
            return redirect(url_for('first_setup'))
        user.email = email
        user.username = username
        user.password = request.form['password']
        user.is_first_login = False
        db.session.commit()
        flash('初始安全策略配置完毕，欢迎正式接入系统。', 'success')
        return redirect(url_for('index'))
    return render_template('first_setup.html', user=user)

@app.route('/')
def index(): return render_template('index.html', categories=Category.query.all())

@app.route('/category/<int:cat_id>')
def category_detail(cat_id): return render_template('category.html', category=Category.query.get_or_404(cat_id))

@app.route('/site/<int:site_id>')
def site_detail(site_id):
    site = Site.query.get_or_404(site_id)
    is_subscribed = Subscription.query.filter_by(user_id=session.get('user_id'), site_id=site_id).first() is not None if 'user_id' in session else False
    return render_template('site_detail.html', site=site, is_subscribed=is_subscribed)

@app.route('/toggle_subscribe/<int:site_id>')
@login_required
def toggle_subscribe(site_id):
    sub = Subscription.query.filter_by(user_id=session['user_id'], site_id=site_id).first()
    if sub: db.session.delete(sub)
    else: db.session.add(Subscription(user_id=session['user_id'], site_id=site_id))
    db.session.commit()
    return redirect(url_for('site_detail', site_id=site_id))

@app.route('/subscriptions')
@login_required
def subscriptions(): return render_template('subscriptions.html', sites=[sub.site for sub in db.session.get(User, session['user_id']).subscriptions])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        if User.query.filter((User.email == email) | (User.username == username)).first(): 
            flash('该邮箱或专家代号已被注册。', 'danger')
        else:
            new_user = User(email=email, username=username, password=request.form['password'], role='user', is_first_login=False)
            db.session.add(new_user)
            db.session.commit()
            session.update({'user_id': new_user.id, 'user_role': new_user.role, 'view_mode': new_user.role})
            flash('身份创建成功，已接入雷达网络。', 'success')
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email'], password=request.form['password']).first()
        if user:
            session.update({'user_id': user.id, 'user_role': user.role, 'view_mode': user.role})
            return redirect(url_for('index'))
        flash('邮箱或密码不正确。', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('index'))

@app.route('/switch_view')
@login_required
def switch_view():
    if session.get('user_role') in ['admin', 'superadmin']:
        session['view_mode'] = 'user' if session.get('view_mode') in ['admin', 'superadmin'] else session.get('user_role')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    role = session.get('user_role')
    
    # 用户视图逻辑
    if session.get('view_mode', role) == 'user':
        user = db.session.get(User, session['user_id'])
        sites = [sub.site for sub in user.subscriptions]
        updates = SiteUpdate.query.filter(SiteUpdate.site_id.in_([s.id for s in sites])).order_by(SiteUpdate.created_at.desc()).limit(15).all()
        return render_template('user_dashboard.html', user=user, sites=sites, updates=updates, real_role=role)
    
    # 🍎 管理员视图逻辑（核心隔离层）
    if role == 'superadmin':
        # 超管能看到所有人（包含其他超管、普通管理员和普通用户）
        users_list = User.query.all()
    else:
        # 普通管理员严格屏蔽所有超管信息，防止越权窥探
        users_list = User.query.filter(User.role != 'superadmin').all()
        
    return render_template('admin.html', categories=Category.query.all(), sites=Site.query.all(), users=users_list, current_role=role)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    user = db.session.get(User, session['user_id'])
    alias, password = request.form.get('alias'), request.form.get('password')
    if alias: user.alias = alias
    if password: user.password = password
    if 'avatar' in request.files:
        file = request.files['avatar']
        if file and file.filename != '':
            filename = secure_filename(f"user_{user.id}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.avatar = filename
    db.session.commit()
    flash('资料已更新。', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/ui_settings', methods=['GET', 'POST'])
@superadmin_required
def ui_settings():
    if request.method == 'POST':
        for key in DEFAULT_SETTINGS.keys():
            Setting.query.filter_by(key=key).first().value = request.form.get(key)
        db.session.commit()
        flash('UI 引擎已重绘。', 'success')
        return redirect(url_for('ui_settings'))
    return render_template('ui_settings.html')

@app.route('/admin/reset_settings', methods=['POST'])
@superadmin_required
def reset_settings():
    Setting.query.delete()
    init_defaults()
    flash('已恢复系统默认设置。', 'success')
    return redirect(url_for('ui_settings'))

@app.route('/admin/add_category', methods=['POST'])
@admin_required
def add_category(): db.session.add(Category(name=request.form['name'])); db.session.commit(); return redirect(url_for('dashboard'))

@app.route('/admin/delete_category/<int:cat_id>')
@admin_required
def delete_category(cat_id): db.session.delete(Category.query.get_or_404(cat_id)); db.session.commit(); return redirect(url_for('dashboard'))

@app.route('/admin/add_site', methods=['POST'])
@admin_required
def add_site():
    new_site = Site(category_id=request.form['category_id'], name=request.form['name'], url=request.form['url'], icon_url=request.form.get('icon_url', ''), description=request.form.get('description', ''))
    db.session.add(new_site); db.session.commit()
    perform_auto_fetch(new_site.id)
    return redirect(url_for('dashboard'))

@app.route('/admin/edit_site/<int:site_id>', methods=['POST'])
@admin_required
def edit_site(site_id):
    site = Site.query.get_or_404(site_id)
    site.category_id = request.form['category_id']
    site.name = request.form['name']
    site.url = request.form['url']
    site.icon_url = request.form.get('icon_url', '')
    site.description = request.form.get('description', '')
    db.session.commit()
    flash('节点配置已修改。', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/delete_site/<int:site_id>')
@admin_required
def delete_site(site_id): db.session.delete(Site.query.get_or_404(site_id)); db.session.commit(); return redirect(url_for('dashboard'))

@app.route('/admin/set_status/<int:site_id>', methods=['POST'])
@admin_required
def set_status(site_id): Site.query.get_or_404(site_id).status = request.form['status']; db.session.commit(); return redirect(url_for('dashboard'))

@app.route('/admin/add_update/<int:site_id>', methods=['POST'])
@admin_required
def add_update(site_id):
    db.session.add(SiteUpdate(site_id=site_id, content=request.form['content'], article_title="系统广播", is_broadcast=True)); db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/auto_fetch/<int:site_id>', methods=['POST'])
@admin_required
def auto_fetch_route(site_id):
    success, msg = perform_auto_fetch(site_id)
    flash(msg, 'success' if success else 'danger')
    return redirect(url_for('dashboard'))

@app.route('/admin/add_user', methods=['POST'])
@admin_required
def add_user():
    role = request.form['role']
    if session.get('user_role') == 'admin' and role != 'user': return redirect(url_for('dashboard'))
    if not User.query.filter_by(email=request.form['email']).first():
        db.session.add(User(email=request.form['email'], username=request.form['username'], password=request.form['password'], role=role, is_first_login=True))
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    target = User.query.get_or_404(user_id)
    if target.id != session.get('user_id') and (session.get('user_role') == 'superadmin' or target.role == 'user'):
        db.session.delete(target); db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/set_role/<int:user_id>', methods=['POST'])
@superadmin_required
def set_role(user_id):
    target = User.query.get_or_404(user_id)
    if target.id != session.get('user_id') and request.form.get('role') in ['user', 'admin']:
        target.role = request.form.get('role'); db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin/change_user_password/<int:user_id>', methods=['POST'])
@superadmin_required
def change_user_password(user_id):
    target = User.query.get_or_404(user_id)
    new_password = request.form.get('new_password')
    if new_password:
        target.password = new_password
        db.session.commit()
        flash(f'已强制更新 {target.username} 的安全密钥。', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)