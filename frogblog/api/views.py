import json
from flask import jsonify,url_for,request,abort,Blueprint
from flask_login import login_required,login_user,logout_user,current_user

from frogblog import db,login_manager
from frogblog.models import User,Article,Category,Tag,Comment

api = Blueprint('api',__name__,url_prefix='/api')

@api.route('/test')
def test():
    return 'true'
# 文章列表资源
@api.route('/posts',methods=['GET','POST'])
def postsList():
    if request.method == 'GET':
        parameter = {}
        parameter['items'] = []
        page = request.args.get('page')
        pre_page = request.args.get('pre_page')
        # 默认参数
        page = int(page) if page else 1
        pre_page = int(pre_page) if pre_page else 5
        # 查询(分页)
        articles = Article.query.order_by(Article.updated.desc()).limit(pre_page).offset((page-1)*pre_page).all()
        for article in articles:
            parameter['items'].append(article.get_item()) 
        # 获取页数
        allArticle = Article.query.count()
        allPage = int(allArticle/pre_page) if allArticle % pre_page == 0 else int(allArticle/pre_page) + 1
        parameter['prevPage'] = True if page>1 else False
        parameter['nextPage'] = True if page<allPage else False
        parameter['nowPage'] = page
        parameter['allPage'] = allPage
        # 返回json
        return jsonify(parameter)
    elif request.method == 'POST':
        if current_user.is_authenticated is False:
            return jsonify({'status':'Permission denied'})
        # 新建文章
        parameter = request.get_json()
        post = parameter['items']
        article = Article(title=post['title'],content=post['content'],summary=post['summary'],
            categories=post['categories'],tags=post['tags']) 
        article.create()
        return jsonify({'status':'success'})

@api.route('/posts/<int:id>',methods=['GET','PUT','DELETE'])
def postContent(id):
    if request.method == 'GET':
        # 获取资源
        article = Article.query.get_or_404(id)
        items = {}
        items['items'] = article.get_content()
        return jsonify(items)
    # 删除资源
    elif request.method == 'DELETE':
        if current_user.is_authenticated is False:
            return jsonify({'status':'Permission denied'})
        article = Article.query.get(id)
        if article:
            article.delete() 
            return jsonify({'status':'success'})
        else:
            return jsonify({'status':'failed'})
    # 修改资源
    elif request.method == 'PUT':
        # 获取到的数据
        if current_user.is_authenticated is False:
            return jsonify({'status':'Permission denied'})
        parameter = request.get_json()
        items = parameter['items']
        article = Article.query.get(id)
        if article:
            article.updata(items)
            return jsonify({'status':'success'})
        else:
            return jsonify({'status':'failed'})
# 标签资源
@api.route('/tags')
def allTags():
    key = request.args.get('key')
    if key:
        parameter = {}
        parameter['items'] = []
        articles = Article.query.filter(Article.tags.any(Tag.name==key)).all()
        for article in articles:
            parameter['items'].append(article.get_item())
        return jsonify(parameter)
    else:
        items = {}
        items['items'] = []
        tags = Tag.query.all()
        for tag in tags:
            items['items'].append(tag.get_item())
        return jsonify(items)
# 分类资源
@api.route('/categories')
def allCategories():
    key = request.args.get('key')
    if key:
        parameter = {}
        parameter['items'] = []
        articles = Article.query.filter(Article.categories.any(Category.name==key)).all()
        for article in articles:
            parameter['items'].append(article.get_item())
        return jsonify(parameter)
    else:
        items = {}
        items['items'] = []
        categories = Category.query.all()
        for category in categories:
            items['items'].append(category.get_item())
        return jsonify(items)
# 用户资源
@api.route('/users/<string:name>',methods=['PUT'])
def user(name):
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
            return jsonify({'status':'failed'})
