from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
login_manager=LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = '/admin/login'
# 设置登录
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app(config):
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(config)
    # 初始化
    db.init_app(app)
    login_manager.init_app(app)
    # 设置
    configure_blueprints(app)
    return app

# 设置蓝图
def configure_blueprints(app):
    from .api import api
    from .frontend import frontend
    for bp in [api,frontend]:
        app.register_blueprint(bp)