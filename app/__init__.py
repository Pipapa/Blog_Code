from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
login_manager=LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = '/login'

def create_app(config):
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(config)
    # 初始化
    db.init_app(app)
    login_manager.init_app(app)
    # 蓝图
    from .views import user,api
    app.register_blueprint(api)
    app.register_blueprint(user)

    return app