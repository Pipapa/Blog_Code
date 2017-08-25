from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

from . import db,login_manager

# admin用户类
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(16),unique=True,index=True)
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

# 为tag和article建立many-to-many关系
tag_relationship = db.Table('tag_relationship',
    db.Column('tag_id',db.Integer,db.ForeignKey('tags.id')),
    db.Column('article_id',db.Integer,db.ForeignKey('articles.id'))
)
# 为comment和article建立many-to-many关系
comment_relationship = db.Table('comment_relationship',
    db.Column('article_id',db.Integer,db.ForeignKey('articles.id')),
    db.Column('comment_id',db.Integer,db.ForeignKey('comments.id'))
)
# 文章类
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    public_time = db.Column(db.DateTime,index=True)
    update_time = db.Column(db.DateTime,index=True)
    num_of_view = db.Column(db.Integer,default=0)
    # 连接其他表单
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    tags = db.relationship('Tag',secondary=tag_relationship,
                            backref=db.backref('articles',lazy='dynamic'))
    comments = db.relationship('Comment',secondary=comment_relationship,
                            backref=db.backref('articles',lazy='dynamic'))
    
    def __init__(self,title,content,category,tag,num_of_view=0):
        self.title = title
        self.content = content
        self.num_of_view = 0
        # 分类
        # 标签

    # 更新文章
    def update_article(self,title=None,content=None):
        article = Article.query.get(self.id)
        # 修改
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        # 保存
        self.update_time = datetime.utcnow()
        db.session.add(article)
        db.session.commit()


# Category文章类别
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)
    num_of_articles = db.Column(db.Integer,default=0)
    articles = db.relationship('Article',backref='categorys',
                                lazy='dynamic')

    def __init__(self,name,num_of_articles):
        self.name = name
        self.num_of_articles = 0

# Tag标签
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)

# 评论类
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(16))
    email = db.Column(db.String(32))
    content = db.Column(db.Text)

