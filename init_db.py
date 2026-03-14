from app import app, db
import os

# 如果你有初始化默认账号的函数，取消下方注释并修改名字
# from app import init_defaults 

def setup():
    with app.app_context():
        # 1. 创建所有表
        db.create_all()
        
        # 2. 执行你的默认数据写入逻辑 (如果有)
        # init_defaults()
        
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            print(f"✅ 完美！数据库已在绝对路径创建: {db_path}")
        else:
            print("❌ 创建失败，请检查路径。")

if __name__ == '__main__':
    setup()