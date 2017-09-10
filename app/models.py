from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

from . import db,login_manager

class User(db.Model,UserMixin):                                         # 账号
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
Tag_relationship = db.Table('tag_relationship',
    db.Column('tag_id',db.Integer,db.ForeignKey('tags.id')),
    db.Column('article_id',db.Integer,db.ForeignKey('articles.id'))
)
# 为comment和article建立many-to-many关系
Comment_relationship = db.Table('comment_relationship',
    db.Column('article_id',db.Integer,db.ForeignKey('articles.id')),
    db.Column('comment_id',db.Integer,db.ForeignKey('comments.id'))
)
class Category(db.Model):                                               # 类别
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)
    num_of_articles = db.Column(db.Integer,default=0)
    articles = db.relationship('Article',backref='categorys',
                                lazy='dynamic')

    def __init__(self,name,num_of_articles=0):
        self.name = name
        self.num_of_articles = num_of_articles

    def get_info(self):
        categories = {}
        categories['name'] = self.name
        categories['url'] = '/category/' + self.name
        categories['num_of_article'] = self.num_of_articles
        return categories
class Tag(db.Model):                                                    # 标签
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)

    def __init__(self,name):
        self.name = name
    def get_info(self):
        tags = {}
        tags['name'] = self.name
        tags['url'] = '/tag/' + self.name
        return tags


class Comment(db.Model):                                                # 评论
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(16))
    email = db.Column(db.String(32))
    public_time = db.Column(db.DateTime)
    content = db.Column(db.Text)

    def __init__(self,username,email,content):
        self.username=username
        self.email=email
        self.content=content
        self.public_time=datetime.utcnow()    

class Article(db.Model):                                                # 文章
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    public_time = db.Column(db.DateTime,index=True)
    update_time = db.Column(db.DateTime,index=True)
    num_of_view = db.Column(db.Integer,default=0)
    # 连接其他表单
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    tags = db.relationship('Tag',secondary=Tag_relationship,
                            backref=db.backref('articles',lazy='dynamic'))
    comments = db.relationship('Comment',secondary=Comment_relationship,
                            backref=db.backref('articles',lazy='dynamic'))
    
    # 构造
    def __init__(self,title,content,
                category=None,tags=None,num_of_view=0):
        self.title = title
        self.content = content
        self.public_time = self.update_time = datetime.utcnow()
        self.num_of_view = num_of_view

        # 添加类型
        if category is not None:
            category_ = Category.query.filter_by(name=category).first()
            if category_ is None:
                category_ = Category(name=category)
                db.session.add(category_)
                db.session.commit()
            self.category_id = category_.id

        # 添加标签
        if tags is not None:
            for tag in tags:
                tag_ = Tag.query.filter_by(name=tag).first()
                if tag_ is None:
                    tag_ = Tag(name=tag)
                    db.session.add(tag_)
                    db.session.commit()
                self.tags.append(tag_)
    
    def add_view(self):                                 # 增加浏览量
        self.num_of_view += 1
        db.session.commit()
    def add_comment(self,comment):                      # 添加评论
        self.num_of_comment += 1
        self.comments.append(comment)
        db.session.commit()
    def get_category(self):                             # 获取category
        categories = []
        if self.category_id is not None:
            categories.append(Category.query.get(self.category_id).name)
        return categories
    
  
    def get_tag(self):                                  # 获取tag
        tags = []
        if self.tags is not None:
            for tag in self.tags:
                tags.append(tag.name)
        return tags

    
    def get_comment(self):                              # 获取comment
        comments = {}
        comments['date'] = []
        for comment in self.comments:
            content = {}
            content['username'] = comment.username
            content['content'] = comment.content
            content['public_time'] = comment.public_time.strftime('%Y-%m-%d %H:%M')
            comments['date'].append(content)
        return comments

   
    def get_info(self):                                 # 获取属性
        info={}
        info['id'] = self.id
        info['url'] = '/article/' + str(self.id)
        info['title'] = self.title
        info['tag'] = self.get_tag()
        info['category'] = self.get_category()
        info['public_time'] = self.public_time.strftime("%Y-%m-%d")
        info['update_time'] = self.update_time.strftime("%Y-%m-%d")
        info['num_of_view'] = self.num_of_view
        info['num_of_comment'] = len(self.comments)
        return info
    def get_detail(self):                               # 获取详情
        detail={}
        detail['info']=self.get_info()
        detail['content'] = self.content
        detail['comment']=self.get_comment()
        return detail