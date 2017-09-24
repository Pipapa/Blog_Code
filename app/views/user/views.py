from flask import Blueprint,render_template,jsonify,request,redirect,url_for,request
from flask_login import login_required

from . import user
from ... import db,login_manager
from ...models import User,Article,Category,Tag,Comment

# 路由跳转
@user.route('/posts/pages')
@user.route('/posts')
@user.route('/')                                                        
def index():
    return redirect(url_for('user.posts',page=1))

# 文章主页
@user.route('/posts/pages/<int:page>')
def posts(page):
    return render_template('index.html')
# 文章显示
@user.route('/posts/<int:id>')
def post(id):
    return render_template('post.html') 
# 管理页面
@user.route('/admin')
@login_required
def admin():
    return render_template('admin.html')
# 写文章页面
@user.route('/admin/writer',defaults={'id': ''})
@user.route('/admin/writer/<int:id>')
def writer(id):
    return render_template('writer.html')
# 标签页面
@user.route('/tags',defaults={'key':''})
@user.route('/tags/<string:key>')
def tag(key):
    return render_template('tag.html')
# 分类页面
@user.route('/categories',defaults={'key':''})
@user.route('/categories/<string:key>')
def category(key):
    return render_template('category.html')
# 登录页面
@user.route('/admin/login')
def login():
    return render_template('login.html')
# 404
@user.errorhandler(404)
def not_found(error):
    return render_template('404.html')