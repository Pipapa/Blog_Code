import json
from flask import jsonify,url_for,request
from . import api
from ... import db
from ...models import User,Article,Category,Tag,Comment

@api.route('/api/test')
def test(s):
    return s

@api.route('/api/article')                                   # 获取文章统计
def get_article_list():
    jsonObj = {}
    # 获取参数
    limit = request.args.get('limit')
    page = request.args.get('page')
    pre_page = request.args.get('pre_page')
    tag = request.args.get('tag')
    category = request.args.get('category')
    # 筛选/默认值
    num_of_article = Article.query.count()                                      # 总文章量                             
    query = Article.query.order_by(Article.update_time.desc())
    if pre_page is None:
        pre_page = 5                                                            # 默认值
    if tag is not None:
        query = query.filter(Article.tags.any(name=tag))
    if category is not None:
        query = query.join(Category).filter(Category.name == category)
    # 是否分页查询
    if page is not None:
        page = int(page)
        pre_page = int(pre_page)
        if page <= 0 or pre_page <= 0:
            jsonObj['error'] = 'TypeError page or pre_page'
            return jsonify(jsonObj)
        pagination = query.paginate(page,pre_page,False)                       # 获取分页
        articles = pagination.items
    else:
        articles = query.all()
    # 返回参数
    if len(articles) == 0:
        jsonObj['error'] = 'Not find article'
        return jsonify(jsonObj)
    else:
        jsonObj['data'] = []
        for article in articles:
            jsonObj['data'].append(article.get_info())
        jsonObj['page'] = page
        return jsonify(jsonObj)
  
@api.route('/api/article/<int:id>')
def get_article(id):
    return 'id-true'

@api.route('/api/comment')                                   # 获取评论
def get_comment():
    return 'true'