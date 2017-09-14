from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

from . import db,login_manager

# 用户
class User(db.Model,UserMixin):                                        
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(16),unique=True,index=True)
    email = db.Column(db.String(32),unique=True,index=True)
    hashPassword = db.Column(db.String(128))

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
        self.hashPassword = generate_password_hash(password,method='pbkdf2:sha256',salt_length=8)

    # 验证密码
    def verify_password(self,password):
        return check_password_hash(self.hashPassword,password)


# 为tag和article建立many-to-many关系
Tag_relationship = db.Table('tag_relationship',
    db.Column('tag_id',db.Integer,db.ForeignKey('tags.id')),
    db.Column('article_id',db.Integer,db.ForeignKey('articles.id'))
)
# 为comment和article建立many-to-many关系
Comment_relationship = db.Table('comment_relationship',
    db.Column('article_id',db.Integer,db.ForeignKey('articles.id')),
    db.Column('comment_id',db.Integer,db.ForeignKey('comments.id'))
)
# 为category和article建立many-to-many关系
Category_relationship = db.Table('category_relationship',
    db.Column('article_id',db.Integer,db.ForeignKey('articles.id')),
    db.Column('comment_id',db.Integer,db.ForeignKey('categories.id'))
)
# 分类表单
class Category(db.Model):                                               
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)

    def __init__(self,name):
        self.name = name
        db.session.add(self)
        db.session.commit()

# 标签表单
class Tag(db.Model):                                                   
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)

    def __init__(self,name):
        self.name = name
        db.session.add(self)
        db.session.commit()

# 评论表单
class Comment(db.Model):                                                
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(16))
    email = db.Column(db.String(32))
    published = db.Column(db.DateTime)
    comment = db.Column(db.Text)

    def __init__(self,username,email,comment):
        self.username = username
        self.email = email
        self.comment = comment
        self.published = datetime.utcnow()    
        db.session.add(self)
        db.session.commit()

#文章表单
class Article(db.Model):                                               
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    published = db.Column(db.DateTime,index=True)
    updated = db.Column(db.DateTime,index=True)
    viewnum = db.Column(db.Integer,default=0)
    # 连接其他表单
    categories = db.relationship('Category',secondary=Category_relationship,
                                 backref=db.backref('articles',lazy='dynamic'))
    tags = db.relationship('Tag',secondary=Tag_relationship,
                            backref=db.backref('articles',lazy='dynamic'))
    comments = db.relationship('Comment',secondary=Comment_relationship,
                            backref=db.backref('articles',lazy='dynamic'))

    # 添加分类
    def add_categories(self,categories=[]):
        for category in categories:
            queryCategory = Category.query.filter_by(name=category).first()
            if queryCategory is None:
                queryCategory = Category(name=category)
            self.categories.append(queryCategory)
    # 添加标签
    def add_tags(self,tags=[]):
        for tag in tags:
            queryTag = Tag.query.filter_by(name=tag).first()
            if queryTag is None:
                queryTag = Tag(name=tag)
            self.tags.append(queryTag)
    # 构造
    def __init__(self,title,content,categories=[],tags=[]):
        self.title = title
        self.content = content
        self.published = self.updated = datetime.utcnow()
        self.add_categories(categories)
        self.add_tags(tags)
        db.session.add(self)
        db.session.commit()