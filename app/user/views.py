from flask import Blueprint,render_template,jsonify,request,redirect,url_for

from . import user
from .. import db
from ..models import User

# 登录界面
@user.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            redirect(url_for('user.index'))
           
    return render_template('login.html')

# 注册界面
@user.route('/register',methods=['POST','GET'])
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

# 主界面
@user.route('/')
def index():
    return render_template('index.html')

# 404
@user.errorhandler(404)
def not_found(error):
    return render_template('404.html')