import json
from flask import jsonify,url_for,request
from . import api
from .. import db
from ..models import User,Article,Category,Tag,Comment

@api.route('/api/test')
def test():
    return 'ok'

# 不需要登录api 
@api.route('/api/article.all')                                   # TODO获取全站统计
def get_statistic():
    jsonObj = {}
    jsonObj['num_of_article'] = Article.query.count()
    return jsonify(jsonObj)

@api.route('/api/article.list')                                  # 获取文章列表
def get_articles():
    jsonObj = {'status':'0'}

    category = request.args.get('category')
    tag = request.args.get('tag')
    articles = []

    # 查询全部
    if category is None and tag is None:
        articles = Article.query.all()

    # 查询category
    if category is not None:
        category = Category.query.filter_by(name=category).first()
        if category is not None:
            articles = Article.query.filter_by(category_id=category.id).all()

    # 查询tag
    if tag is not None:
       articles = Article.query.filter(Article.tags.any(name=tag)).all()

    # 输出article
    if len(articles) != 0: 
        jsonObj['status']='1'
        jsonObj['num_of_articles']=len(articles)
        for article in articles:
            jsonObj[str(article.id)]=article.get_info()
        return jsonify(jsonObj)

    return jsonify(jsonObj)

@api.route('/api/article',methods=['POST','GET'])                # 获取文章详情/POST修改,添加文章
def query_articles():
    # 查询id
    jsonObj = {'status':'False'}
    id = request.args.get('id')
    if id is not None:
        article = Article.query.get(id)
        if article is None:
            return jsonify(jsonObj)
        else:
            article.add_view()
            jsonObj['status'] = '1'
            jsonObj['detail'] = article.get_detail()
            return jsonify(jsonObj)
    # POST方式
    
    return jsonify(jsonObj)
