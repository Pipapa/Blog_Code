from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import db,login_manager

# admin用户类
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

    # 检测用户/邮箱是否存在
    @staticmethod
    def exist_user(username=None,email=None):
        if username is None and email is None:
            raise AttributeError('Error')
        if username is not None:
            if User.query.filter_by(username=username).first() is not None:
                return True
        if email is not None:
            if User.query.filter_by(email=email).first() is not None:
                return True
        return False

# 文章类
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64),unique=True)
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    public_time = db.Column(db.DateTime,index=True)
    update_time = db.Column(db.DateTime,index=True)
    num_of_view = db.Column(db.Integer,default=0)
    # 连接其他表单
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'))

# Category文章类别
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)
    num_of_articles = db.Column(db.Integer,default=0)
    articles = db.relationship('Article',backref='categorys',
                                lazy='dynamic')

# Tag标签
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)
    articles = db.relationship('Article',backref='tags',
                               lazy='dynamic')

