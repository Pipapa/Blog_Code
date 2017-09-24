import json
from flask import jsonify,url_for,request,abort
from . import api
from ... import db
from ...models import User,Article,Category,Tag,Comment

# 文章列表资源
@api.route('/api/posts/',methods=['GET','POST'])
def postsList():
    # 获取文章列表资源 method == 'GET'
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
    # 新建文章
    elif request.method == 'POST':
        parameter = request.get_json()
        post = parameter['items']
        article = Article(title=post['title'],content=post['content'],summary=post['summary'],
            categories=post['categories'],tags=post['tags']) 
        article.create()
        status = {'status':'success'}
        return jsonify(status)
# 文章资源
@api.route('/api/posts/<int:id>',methods=['GET','PUT','DELETE'])
def postsContent(id):
    status = {} 
    status['status'] = 'failed'
    # 获取资源
    if request.method == 'GET':
        article = Article.query.get(id)
        if article is None:
            return jsonify({'status':'failed'})
        items = {}
        items['items'] = article.get_content()
        return jsonify(items)
    # 删除资源
    elif request.method == 'DELETE':
        article = Article.query.get(id)
        if article:
            article.delete() 
            return jsonify({'status':'success'})
        else:
            return jsonify({'status':'failed'})
    # 修改资源
    elif request.method == 'PUT':
        # 获取到的数据
        parameter = request.get_json()
        items = parameter['items']
        article = Article.query.get(id)
        if article:
            article.updata(items)
            return jsonify({'status':'success'})
        else:
            return jsonify({'status':'failed'})
    return jsonify(status)
# 标签资源
@api.route('/api/tags')
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
@api.route('/api/categories')
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
