import json
from flask import jsonify,url_for,request
from . import api
from ... import db
from ...models import User,Article,Category,Tag,Comment


def check_args(args):                                        # 检查数字参数是否合法
    for arg in args:
        if arg is not None and arg.isdigit() is False:
            return 1
    return 0

@api.route('/api/test')
def test():
    return 'true'

@api.route('/api/article')                                   # 获取文章统计
def get_article_list():
    jsonObj = {}
    # 获取参数
    limit = request.args.get('limit')
    page = request.args.get('page')
    pre_page = request.args.get('pre_page')
    tag = request.args.get('tag')
    category = request.args.get('category')
    # 处理参数 str to int 
    if check_args([limit,page,pre_page]):
        jsonObj['error'] = 'The key is not valid'
        return jsonify(jsonObj)
    # 默认值
    num_of_article = Article.query.count()                                      # 总文章量 
    # 查询参数
    query = Article.query.order_by(Article.update_time.desc())
    if tag is not None:                                                         # 标签查询
        query = query.filter(Article.tags.any(name=tag))

    if category is not None:                                                    # 分类查询
        query = query.join(Category).filter(Category.name == category)

    if page is not None:                                                        # 分页
        if pre_page is None:
            pre_page = 5
        else:
            pre_page = int(pre_page)
        page = int(page)
        _start = (page-1) * pre_page                                            # 计算偏移量/分页
        query = query.limit(pre_page).offset(_start)
    
    if limit is not None:                                                       # 限制大小/非分页情况下
        limit = int(limit)
        if page is None:
            query = query.limit(limit)
    
    # 查询
    articles = query.all() 
    # 返回参数
    if len(articles) == 0:
        jsonObj['error'] = 'No article be found'
        return jsonify(jsonObj)
    else:
        jsonObj['data'] = []
        for article in articles:
            jsonObj['data'].append(article.get_info())
        # 分页情况
        jsonObj['page'] = page
        jsonObj['has_next'] = jsonObj['has_prev'] = None
        if page:
            if page > 1:
                jsonObj['has_prev'] = True
            if page < num_of_article/pre_page:
                jsonObj['has_next'] = True
        return jsonify(jsonObj)
  
@api.route('/api/article/<int:id>')
def get_article(id):
    return 'id-true'

@api.route('/api/comment')                                   # 获取评论
def get_comment():
    return 'true'