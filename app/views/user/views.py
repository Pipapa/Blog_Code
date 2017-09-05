from flask import Blueprint,render_template,jsonify,request,redirect,url_for,request

from . import user
from ... import db
from ...models import User,Article,Category,Tag,Comment

@user.route('/')                                                        # 主界面,跳转到文章
def index():
    return redirect(url_for('user.article_index'))
@user.route('/admin/login',methods=['POST','GET'])                      # 登录
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            redirect(url_for('user.index'))
           
    return render_template('login.html')
@user.route('/register',methods=['POST','GET'])                         # 注册
def register():
    if request.method == 'POST':
        # 添加用户
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.exist_user(username=username,email=email):
            # 用户存在(前端表单验证,POST)
            pass
        else:
            # 用户不存在
            user=User(username=username,email=email,password=password)
            db.session.add(user)
            db.session.commit()

    return render_template('register.html')
@user.route('/article')                                                 # 文章/主页面
@user.route('/article/<int:article_id>')
def article_index(article_id=None):
    if article_id is not None:
        return render_template('article.html')
    else:
        return render_template('index.html')

@user.route('/tag')                                                     # 标签
@user.route('/tag/<string:tag>')
def tag_index(tag=None):
    return render_template('tag.html')
@user.route('/category')                                                # 分类
@user.route('/category/<string:category>')
def category_index(category=None):
    return render_template('category.html')

@user.route('/admin/writer')                                            # 编辑文章
def writer_admin():
    return render_template('writer.html')


# 404
@user.errorhandler(404)
def not_found(error):
    return render_template('404.html')