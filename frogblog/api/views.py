import json
from flask import jsonify,url_for,request,abort,Blueprint,Response
from flask_login import login_required,login_user,logout_user,current_user

from frogblog import db,login_manager
from frogblog.models import User,Article,Category,Tag,Comment

from functools import wraps

api = Blueprint('api',__name__,url_prefix='/api')

# 文章总览
@api.route('/info')
def postsInfo():
    # 获取标签/分类
    def appendItem(model):
        models = model.query.all()
        items = []
        for m in models:
            items.append(m.get_item())
        return items

    parameter = {}
    parameter['tags'] = appendItem(Tag)
    parameter['categories'] = appendItem(Category)
    return jsonify(parameter)

# 文章列表资源
@api.route('/posts',methods=['GET','POST'])
def postsList():
    if request.method == 'GET':
        parameter = {}
        articles = Article.query.all()
        for article in articles:
            parameter['items'].append(article.get_item())
        # 返回json
        return jsonify(parameter)
    elif request.method == 'POST':
        # 未登录
        if current_user.is_authenticated is False:
            abort(403)
        # 新建文章
        parameter = request.get_json()
        post = parameter['items']
        article = Article(title=post['title'],content=post['content'],summary=post['summary'],
            categories=post['categories'],tags=post['tags']) 
        article.create()
        return jsonify({'status':'success'})

@api.route('/posts/<int:id>',methods=['GET','PUT','DELETE'])
def postsContent(id):
    if request.method == 'GET':
        # 获取资源 
        items = {}
        article = Article.query.get_or_404(id)
        items['items'] = article.get_content()
        article.add_view()
        return jsonify(items)
    # 删除资源
    elif request.method == 'DELETE':
        if current_user.is_authenticated is False:
            abort(403)
        article = Article.query.get_or_404(id)
        article.delete() 
        return jsonify({'status':'success'})
    # 修改资源
    elif request.method == 'PUT':
        # 未登录
        if current_user.is_authenticated is False:
            abort(403)
        parameter = request.get_json()
        items = parameter['items']
        article = Article.query.get_or_404(id)
        article.updata(items)
        return jsonify({'status':'success'})

# 标签资源
@api.route('/tags/<string:key>')
def allTags(key):
    query_key = Tag.name==key if key else None
    parameter = {}
    parameter['items'] = []
    articles = Article.query.filter(Article.tags.any(query_key)).all()
    for article in articles:
        parameter['items'].append(article.get_item())
    return jsonify(parameter)

# 分类资源
@api.route('/categories/<string:key>')
def allCategories(key):
    query_key = Category.name==key if key else None
    parameter = {}
    parameter['items'] = []
    articles = Article.query.filter(Article.categories.any(query_key)).all()
    for article in articles:
        parameter['items'].append(article.get_item())
    return jsonify(parameter)
   
# 用户资源
@api.route('/users/<string:name>',methods=['PUT'])
def allUsers(name):
    if request.method == 'PUT':
        if current_user.is_authenticated is True:
            logout_user()
            return jsonify({'status':'success'})
        items = request.get_json()
        user = User.query.filter_by(username = items['username']).first()
        if user and user.verify_password(items['password']):
            login_user(user)
            return jsonify({'status':'success'})
        else:
            abort(404)

@api.errorhandler(404)
def statusFailed(error):
    return jsonify({'status':'failed'})
@api.errorhandler(403)
def statusForbidden(error):
    return jsonify({'status':'forbidden'})
