from flask import Blueprint,render_template,jsonify,request,redirect,url_for,request,abort
from flask_login import login_required

from frogblog import db,login_manager
from frogblog.models import User,Article,Category,Tag,Comment

frontend = Blueprint('user',__name__)

# 路由跳转
@frontend.route('/posts/pages')
@frontend.route('/posts')
@frontend.route('/')                                                        
def index():
    return redirect(url_for('user.posts',page=1))

# 文章主页
@frontend.route('/posts/pages/<int:page>')
def posts(page):
    return render_template('index.html')
# 文章显示
@frontend.route('/posts/<int:id>')
def post(id):
    return render_template('post.html') 
# 管理页面
@frontend.route('/admin')
@login_required
def admin():
    return render_template('admin.html')
# 写文章页面
@frontend.route('/admin/writer',defaults={'id': ''})
@frontend.route('/admin/writer/<int:id>')
@login_required
def writer(id):
    return render_template('writer.html')
# 标签页面
@frontend.route('/tags',defaults={'key':''})
@frontend.route('/tags/<string:key>')
def tag(key):
    return render_template('tag.html')
# 分类页面
@frontend.route('/categories',defaults={'key':''})
@frontend.route('/categories/<string:key>')
def category(key):
    return render_template('category.html')
# 登录页面
@frontend.route('/admin/login')
def login():
    return render_template('login.html')
# 404
@frontend.errorhandler(404)
def not_found(error):
    return render_template('404.html')