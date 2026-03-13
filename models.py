from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')
    alias = db.Column(db.String(50))
    avatar = db.Column(db.String(255), default='default.png')
    # 🍎 新增：判断是否为首次登录的安全标记
    is_first_login = db.Column(db.Boolean, default=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True, cascade="all, delete-orphan")

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sites = db.relationship('Site', backref='category', lazy=True, cascade="all, delete-orphan")

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    icon_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='offline')
    is_approved = db.Column(db.Boolean, default=False)
    updates = db.relationship('SiteUpdate', backref='site', lazy=True, cascade="all, delete-orphan")
    subscribers = db.relationship('Subscription', backref='site', lazy=True, cascade="all, delete-orphan")

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SiteUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    article_title = db.Column(db.String(255))
    article_url = db.Column(db.String(255))
    is_broadcast = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)