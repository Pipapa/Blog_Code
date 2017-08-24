from flask import Blueprint,render_template,jsonify,request,redirect,url_for
from .models import User,db

user = Blueprint('user',__name__,
    template_folder='templates',
    static_folder='statics',)

api = Blueprint('api',__name__,
    template_folder='templates',
    static_folder='statics')

# 登录界面
@user.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            print(user.verify_password(password))
           
    return render_template('login.html')

# 注册界面
@user.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        # 添加用户
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User(username=username,email=email,password=password)

        db.session.add(user)
        db.session.commit()
    return render_template('register.html')

# 主界面
@user.route('/')
def index():
    return render_template('index.html')


