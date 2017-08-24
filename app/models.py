from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import db,login_manager

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True,index=True)
    email = db.Column(db.String(32),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password
    
    # 加密密码
    @property
    def password(self):
        raise AttributeError('No Permission')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password,method='pbkdf2:sha256',salt_length=8)

    # 验证密码
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)