from flask import Blueprint,render_template,jsonify,request,redirect,url_for,request

from . import user
from ... import db
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
def admin():
    return render_template('admin.html')
# 写文章页面
@user.route('/admin/writer',defaults={'id': ''})
@user.route('/admin/writer/<int:id>')
def writer(id):
    return render_template('writer.html')
# 404
@user.errorhandler(404)
def not_found(error):
    return render_template('404.html')