from flask import Blueprint,render_template,jsonify,request,redirect,url_for,request

from . import user
from ... import db
from ...models import User,Article,Category,Tag,Comment

@user.route('/posts')
@user.route('/')                                                        # 主界面,跳转到文章
def index():
    return redirect(url_for('user.posts',page=1))

# 文章主页
@user.route('/posts/pages',defaults={'page':1})
@user.route('/posts/pages/<int:page>')
def posts(page):
    return render_template('index.html')
# 404
@user.errorhandler(404)
def not_found(error):
    return render_template('404.html')